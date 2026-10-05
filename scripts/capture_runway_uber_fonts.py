#!/usr/bin/env python3
"""Retain observed first-party fonts and native bundler failure evidence."""
import argparse
import hashlib
import json
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / '.stitch-work/current-official'
UBER_FONTS = ['UberMove-Bold.woff2', 'UberMove-Regular.woff2',
              'UberMoveText-Medium.woff2', 'UberMoveText-Regular.woff2']


def record(brand, name, data, url, method):
    relative = brand + '-assets/' + name
    path = ROOT / relative
    path.parent.mkdir(exist_ok=True)
    path.write_bytes(data)
    return {'source_url': url, 'path': relative, 'kind': 'font',
            'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
            'capture_method': method, 'observed_at': '2026-10-05'}


def download(name):
    url = 'https://tb-static.uber.com/prod/uber-static/' + name
    with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=35) as response:
        data = response.read()
        assert response.status == 200 and data[:4] == b'wOF2'
    return record('uber', name, data, url, 'observed_official_font_direct_download')


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--runway-manifest',type=Path)
    parser.add_argument('--uber-manifest',type=Path)
    args=parser.parse_args()
    if args.runway_manifest:
        captured=[]
        for asset in json.loads(args.runway_manifest.read_text())['assets']:
            captured.append(record('runwayml', asset['name'], Path(asset['path']).read_bytes(),
                                   asset['url'], 'native_page_assets_bundle'))
        (ROOT / 'runwayml-asset-provenance.json').write_text(json.dumps({'assets': captured, 'capture_failures': []}, indent=2) + '\n')
    else:
        # Reuse the dated native capture; temporary browser paths are never required.
        captured=json.loads((ROOT/'runwayml-asset-provenance.json').read_text())['assets']
        for asset in captured:
            data=(ROOT/asset['path']).read_bytes()
            assert hashlib.sha256(data).hexdigest()==asset['sha256']
    with ThreadPoolExecutor(max_workers=4) as pool:
        captured = list(pool.map(download, UBER_FONTS))
    failures=(json.loads(args.uber_manifest.read_text())['failures'] if args.uber_manifest else
              json.loads((ROOT/'uber-asset-provenance.json').read_text()).get('capture_failures',[]))
    (ROOT / 'uber-asset-provenance.json').write_text(json.dumps({'assets': captured, 'capture_failures': failures}, indent=2) + '\n')
    print(json.dumps({'runway_fonts': 3, 'uber_fonts': len(captured), 'uber_bundle_failures_retained': len(failures)}))
