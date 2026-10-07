#!/usr/bin/env python3
"""Preserve observed official Revolut assets; never use security-check HTML as UI."""
import hashlib
import json
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote, urlsplit
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1] / '.stitch-work/current-official'
ALLOWED = {'www.revolut.com', 'assets.revolut.com'}
EXTRA = [
    'https://assets.revolut.com/published-assets-v3/4bcf4f81-c0b1-4bde-82f5-0b4cd2ddd2ef/f94bbcee-b4a0-49f2-8043-c472b47d0ac7.png',
    'https://assets.revolut.com/published-assets-v3/c1d9d317-7303-4f79-8756-937632237bb5/0eb1515a-91e8-4d4e-8e19-ff7c82de5410.png',
    'https://assets.revolut.com/published-assets-v3/d6d0bfe6-bc41-44db-8dde-dd3665b3c359/e306c6b0-8d4e-4b03-ae84-c2e6c4da0904.png',
    'https://assets.revolut.com/published-assets-v3/af2fd3c8-cfef-40f0-a673-4a2c9fa85d69/e0cd59b6-e3e1-4084-b269-a736c0ce8f78.png',
    'https://assets.revolut.com/published-assets-v3/4ac38203-f6a2-4510-afed-cabe180f1512/d4473a07-a3bd-47c8-b46d-af2e1ee8e54a.png',
    'https://assets.revolut.com/published-assets-v3/397c950a-ce30-4f8e-9d43-6c958bf9e1c0/a1310b7f-ed8e-4575-b805-d7eac1166bc4.png',
    'https://assets.revolut.com/published-assets-v3/1d77543f-cc03-4518-aa5c-4967ac6504ef/76336c8a-ffc4-417e-88e9-b023b5edb433.png',
    'https://assets.revolut.com/assets/fonts/AeonikPro-Medium.woff2',
    'https://assets.revolut.com/published-assets-v3/01f199ee-b3f2-4203-9ab7-27d133045284/a1b80bd3-607e-450e-80a0-83317969cf66.png',
    'https://assets.revolut.com/published-assets-v3/d6d0bfe6-bc41-44db-8dde-dd3665b3c359/00544e46-b5db-4906-b0ed-87b558057f3f.png',
    'https://assets.revolut.com/published-assets-v3/af2fd3c8-cfef-40f0-a673-4a2c9fa85d69/aab65826-2d49-49f9-803b-061c5c68b842.png',
    'https://assets.revolut.com/published-assets-v3/ecad5fbe-66ca-48bb-8694-ffe6f33d3ef9/b639119d-f475-48cb-a239-a14eeda2b5e2.png',
    'https://assets.revolut.com/published-assets-v3/4ddae90c-6272-457d-a3e6-202835b6e225/60631149-1b04-4ffb-b620-ade697d9d668.png',
    'https://assets.revolut.com/published-assets-v3/0b709a3f-3f22-48ba-9af7-70552fb3cb10/949abf57-54b0-4e7c-9cd9-4e6f5076cab0.png',
    'https://assets.revolut.com/published-assets-v3/38a40981-07a2-49fe-93c7-7de5f6070228/0f637881-5998-4bff-8538-f4f6dbf765fe.png',
    'https://assets.revolut.com/published-assets-v3/e33846f9-ef6b-4234-8bba-fb264119f37f/50faab41-525e-410d-8b14-51f95fed6584.png',
    'https://assets.revolut.com/published-assets-v3/dbda1cf2-0f02-4e27-b0ce-1ea086d048b2/3352558a-4eb5-4810-9dbe-4a9c245b61b3.png',
    'https://assets.revolut.com/assets/icons/Menu.svg',
    'https://assets.revolut.com/assets/icons/16/ChevronDownSmall.svg',
]

def record(data, url, name, method, content_type=None):
    stem = Path(unquote(name)).name
    if not Path(stem).suffix:
        stem += '.svg' if url.startswith('inline-svg:') else '.asset'
    target = ROOT / 'revolut-assets' / (hashlib.sha256(url.encode()).hexdigest()[:10] + '-' + stem)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    return {'source_url': url, 'path': str(target.relative_to(ROOT)), 'bytes': len(data),
            'sha256': hashlib.sha256(data).hexdigest(), 'content_type': content_type,
            'method': method, 'observed_at': datetime.now(ZoneInfo('Asia/Taipei')).isoformat()}

def capture(url):
    if urlsplit(url).hostname not in ALLOWED:
        raise ValueError('Unobserved host: ' + url)
    with tempfile.TemporaryDirectory(prefix='revolut-asset-') as folder:
        output = Path(folder) / 'resource'
        response = subprocess.run(['curl', '--silent', '--show-error', '--location', '--max-time', '45',
                                   '--output', str(output), '--write-out', '%{http_code}', url], capture_output=True)
        status = int(response.stdout or '0')
        if response.returncode or status != 200:
            return None, {'source_url': url, 'status': status, 'error': response.stderr.decode(errors='replace')}
        data = output.read_bytes()
        if not data or data.lstrip().lower().startswith((b'<!doctype html', b'<html')):
            return None, {'source_url': url, 'status': status, 'error': 'Unexpected empty or HTML resource'}
    return record(data, url, Path(urlsplit(url).path).name, 'ordinary public HTTP; observed first-party URL; original bytes'), None

def main():
    provenance = ROOT / 'revolut-asset-provenance.json'
    evidence = json.loads(provenance.read_text()) if provenance.exists() else {'assets': [], 'capture_failures': []}
    rows = {r['source_url']: r for r in evidence['assets']}
    for path in sys.argv[1:]:
        bundle = json.loads(Path(path).read_text())
        for asset in bundle['assets']:
            url = asset['url']
            if not url.startswith('inline-svg:') and urlsplit(url).hostname not in ALLOWED:
                raise ValueError('Unexpected bundled resource: ' + url)
            rows[url] = record(Path(asset['path']).read_bytes(), url, asset['name'],
                               'documented pageAssets bundle; original file bytes or observed inline SVG markup', asset.get('contentType'))
        evidence['browser_bundle_failures'] = bundle['failures']
    missing = [url for url in EXTRA if url not in rows]
    with ThreadPoolExecutor(max_workers=4) as pool:
        for row, failure in pool.map(capture, missing):
            if row:
                rows[row['source_url']] = row
            else:
                evidence['capture_failures'].append(failure)
    evidence['assets'] = list(rows.values())
    provenance.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + '\n')
    source = ROOT / 'revolut-source-current.html'
    metadata = ROOT / 'revolut-source-metadata.json'
    if not metadata.exists():
        metadata.write_text(json.dumps({
        'url': 'https://www.revolut.com/', 'status': 403, 'usable_homepage_html': False,
        'title': 'Just a quick security check | Revolut', 'bytes': source.stat().st_size,
        'sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'reference_method': 'dated rendered desktop/mobile browser observations, not this response',
        'observed_at': datetime.now(ZoneInfo('Asia/Taipei')).isoformat()}, indent=2) + '\n')
    print(json.dumps({'assets': len(rows), 'bytes': sum(r['bytes'] for r in rows.values()),
                      'failures': evidence['capture_failures']}))

if __name__ == '__main__':
    main()
