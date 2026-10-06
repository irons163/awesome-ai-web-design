#!/usr/bin/env python3
"""Save the fonts observed on the two public BMW homepage references."""
import hashlib
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urljoin
from capture_bmw_sources import ROOT, get

FONTS = {
    'bmw': ('https://www.bmw.com.tw/etc.clientlibs/bmw-web/clientlibs/clientlib-site/resources/',
            ['fonts/BMWTypeNext-Light.woff2', 'fonts/BMWTypeNext-Regular.woff2',
             'fonts/BMWTypeNext-Medium.woff2', 'fonts/BMWTypeNext-Bold.woff2',
             'icons/bmw_next_icons_light.woff2', 'icons/bmw_next_icons_regular.woff2']),
    'bmw-m': ('https://www.bmw-m.com/etc.clientlibs/bmwcom/clientlibs/clientlib-site/resources/fonts/',
              ['BMWTypeNextLatin-Light.woff2', 'BMWTypeNextLatin.woff2', 'playfair.woff2']),
}


def download(item):
    brand, base, name = item
    url = urljoin(base, name)
    data, final, status = get(url)
    if data[:4] != b'wOF2':
        raise ValueError('Unexpected font response: ' + name)
    relative = brand + '-assets/' + Path(name).name
    (ROOT / relative).write_bytes(data)
    return brand, {'source_url': url, 'resolved_url': final, 'path': relative,
                   'kind': 'font', 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
                   'status': status, 'capture_method': 'standard_public_http_download'}


if __name__ == '__main__':
    work = [(brand, base, name) for brand, (base, names) in FONTS.items() for name in names]
    with ThreadPoolExecutor(max_workers=4) as pool:
        records = list(pool.map(download, work))
    for brand in FONTS:
        target = ROOT / (brand + '-asset-provenance.json')
        saved = json.loads(target.read_text())
        saved['assets'] = [a for a in saved['assets'] if a.get('kind') != 'font'] + [a for b,a in records if b == brand]
        target.write_text(json.dumps(saved, indent=2) + '\n')
    print(json.dumps({'fonts': len(records), 'bytes': sum(a['bytes'] for _,a in records)}))
