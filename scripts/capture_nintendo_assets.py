#!/usr/bin/env python3
"""Retain observed Nintendo/Stitch public bytes with explicit HTTP provenance."""
import hashlib
import json
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen

from official_html_tree import Tree

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / '.stitch-work/current-official'
DEST = WORK / 'nintendo-2001-assets'
ORIGIN = 'https://www.nintendo.com/en-ca/'


def payload(result):
    return result.get('structuredContent') or json.loads(next(c['text'] for c in result['content'] if c['type'] == 'text'))


def download(url, target):
    request = Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': '*/*'})
    with urlopen(request, timeout=45) as response:
        if response.status != 200:
            raise ValueError(f'Unusable public response: {response.status} {url}')
        data, content_type = response.read(), response.headers.get('Content-Type', '').split(';')[0]
    target.write_bytes(data)
    return {'source_url': url, 'path': str(target.relative_to(WORK)), 'http_status': 200,
            'content_type': content_type, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def main():
    DEST.mkdir(exist_ok=True)
    reference = json.loads((WORK / 'nintendo-2001-desktop-browser-export.json').read_text())
    assert reference['reference_url'] == ORIGIN
    urls = {i['src'] for i in reference['images'] if i['src'].startswith('https://')}
    tree = Tree(''.join(reference['root_parts'])).root
    for node in tree.walk():
        if node.tag == 'source' and node.attrs.get('media') == '(min-width: 316px)':
            urls.add(node.attrs['srcset'].split(' 1x')[0])
    for sheet in reference['stylesheet_order']:
        if sheet.get('href'):
            urls.add(sheet['href'])
        for batch in sheet['rules']:
            for rule in batch:
                for raw in re.findall(r'url\(([^)]+)\)', rule):
                    raw = raw.strip(' \"\'')
                    if raw.startswith('data:'):
                        continue
                    value = urljoin(sheet.get('href') or ORIGIN, raw)
                    if urlsplit(value).path.endswith(('.woff', '.woff2', '.ttf')):
                        urls.add(value)
    def capture(url):
        file_id = hashlib.sha256(url.encode()).hexdigest()[:16]
        target = DEST / file_id
        record = download(url, target)
        suffix = {'image/png': '.png', 'image/jpeg': '.jpg', 'image/webp': '.webp',
                  'image/avif': '.avif', 'image/svg+xml': '.svg', 'image/gif': '.gif',
                  'text/css': '.css', 'font/woff2': '.woff2', 'font/woff': '.woff',
                  'application/font-woff2': '.woff2', 'font/ttf': '.ttf'}.get(record['content_type'])
        if not suffix:
            suffix = Path(urlsplit(url).path).suffix if Path(urlsplit(url).path).suffix in ('.woff2', '.ttf', '.css') else '.bin'
        final = target.with_suffix(suffix)
        target.rename(final)
        record['path'] = str(final.relative_to(WORK))
        return record
    with ThreadPoolExecutor(max_workers=4) as executor:
        assets = list(executor.map(capture, sorted(urls)))
    (WORK / 'nintendo-2001-asset-provenance.json').write_text(json.dumps({'reference_url': ORIGIN, 'assets': assets}, ensure_ascii=False, indent=2) + '\n')
    native = []
    for mode in ('desktop', 'mobile', 'mobile-correction'):
        result_path = WORK / f'nintendo-2001-stitch-{mode}-response.json'
        if not result_path.exists():
            continue
        response = payload(json.loads(result_path.read_text()))
        for component in response.get('outputComponents', []):
            for screen in component.get('design', {}).get('screens', []):
                for key, suffix in (('htmlCode', 'html'), ('screenshot', 'png')):
                    target = WORK / f'nintendo-2001-stitch-{mode}-raw.{suffix}'
                    record = download(screen[key]['downloadUrl'], target)
                    record.update({'screen': screen['name'], 'device_type': screen.get('deviceType')})
                    native.append(record)
    (WORK / 'nintendo-2001-stitch-downloads.json').write_text(json.dumps(native, indent=2) + '\n')
    print(json.dumps({'original_assets': len(assets), 'original_bytes': sum(a['bytes'] for a in assets), 'native_exports': len(native)}))


if __name__ == '__main__':
    main()
