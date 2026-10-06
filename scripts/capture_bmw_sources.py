#!/usr/bin/env python3
"""Retain dated public BMW sources and their directly linked stylesheets."""
import hashlib
import json
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin
from zoneinfo import ZoneInfo
from official_html_tree import Tree

ROOT = Path(__file__).resolve().parents[1] / '.stitch-work/current-official'
SOURCES = {'bmw': 'https://www.bmw.com.tw/zh/index.html',
           'bmw-m': 'https://www.bmw-m.com/en/index.html'}


def get(url):
    with tempfile.TemporaryDirectory(prefix='bmw-reference-') as directory:
        target = Path(directory) / 'response'
        response = subprocess.run(['curl', '--silent', '--show-error', '--location',
                                   '--fail', '--max-time', '30', '--output', str(target),
                                   '--write-out', '%{http_code}\n%{url_effective}', url],
                                  capture_output=True, check=False)
        if response.returncode:
            raise OSError(response.stderr.decode('utf-8', errors='replace').strip())
        status, final = response.stdout.decode().split('\n', 1)
        return target.read_bytes(), final, int(status)


def capture(item):
    brand, url = item
    stamp = datetime.now(ZoneInfo('Asia/Taipei')).isoformat()
    previous = ROOT / (brand + '-source-metadata.json')
    history = [json.loads(previous.read_text())] if previous.exists() else []
    metadata = {'requested_url': url, 'observed_at': stamp,
                'method': 'standard_public_http_curl_request', 'prior_attempts': history}
    saved_assets = ROOT / (brand + '-asset-provenance.json')
    records = ([a for a in json.loads(saved_assets.read_text())['assets'] if a.get('kind') == 'font']
               if saved_assets.exists() else [])
    failures = []
    try:
        data, final, status = get(url)
        metadata.update({'final_url': final, 'status': status,
                         'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
        (ROOT / (brand + '-source-current.html')).write_bytes(data)
        tree = Tree(data.decode('utf-8'))
        styles = [urljoin(final, n.attrs['href']) for n in tree.root.walk()
                  if n.tag == 'link' and n.attrs.get('rel') == 'stylesheet' and n.attrs.get('href')]
        for i, source in enumerate(dict.fromkeys(styles)):
            try:
                css, resolved, code = get(source)
                relative = brand + '-assets/source-' + str(i) + '.css'
                target = ROOT / relative
                target.parent.mkdir(exist_ok=True)
                target.write_bytes(css)
                records.append({'source_url': source, 'resolved_url': resolved, 'path': relative,
                                'status': code, 'bytes': len(css),
                                'sha256': hashlib.sha256(css).hexdigest(), 'observed_at': stamp})
            except OSError as error:
                failures.append({'url': source, 'error': str(error)})
    except OSError as error:
        metadata.update({'status': getattr(error, 'code', None), 'error': str(error)})
    (ROOT / (brand + '-source-metadata.json')).write_text(json.dumps(metadata, indent=2) + '\n')
    (ROOT / (brand + '-asset-provenance.json')).write_text(json.dumps({'assets': records, 'capture_failures': failures}, indent=2) + '\n')
    return {'brand': brand, **metadata, 'stylesheets': sum(a['path'].endswith('.css') for a in records)}


if __name__ == '__main__':
    ROOT.mkdir(exist_ok=True)
    with ThreadPoolExecutor(max_workers=2) as pool:
        for result in pool.map(capture, SOURCES.items()):
            print(json.dumps(result))
