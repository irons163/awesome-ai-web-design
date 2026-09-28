#!/usr/bin/env python3
"""Capture SpaceX's dated public homepage images and fonts with curl provenance."""

from __future__ import annotations

import hashlib
import json
import subprocess
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / '.stitch-work' / 'current-official'
ASSETS = ROOT / 'spacex-assets'
SOURCES = ROOT / 'spacex-asset-sources.json'
HOSTS = {'www.spacex.com', 'sxcontent9668.azureedge.us'}


def capture(item: dict) -> dict:
    name, url = item['name'], item['url']
    parsed = urllib.parse.urlsplit(url)
    if Path(name).name != name or parsed.scheme != 'https' or parsed.hostname not in HOSTS:
        raise ValueError(f'Unexpected SpaceX asset: {name}')
    path = ASSETS / name
    subprocess.run([
        'curl', '--fail', '--location', '--silent', '--show-error',
        '--max-time', '60', '-A', 'Mozilla/5.0', url, '-o', str(path),
    ], check=True)
    data = path.read_bytes()
    if not data:
        raise RuntimeError(f'Empty SpaceX asset: {name}')
    return {'path': 'spacex-assets/' + name, 'url': url,
            'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    sources = json.loads(SOURCES.read_text())
    with ThreadPoolExecutor(max_workers=6) as pool:
        records = list(pool.map(capture, sources['assets']))
    provenance = {
        'reference': sources['reference'],
        'captured_at': datetime.now().astimezone().isoformat(),
        'source_html_sha256': hashlib.sha256((ROOT / 'spacex-source-current.html').read_bytes()).hexdigest(),
        'assets': records,
        'note': 'First-party resources observed on the current SpaceX homepage at desktop or phone size.',
    }
    (ROOT / 'spacex-asset-provenance.json').write_text(json.dumps(provenance, indent=2) + '\n')
    print(json.dumps({'count': len(records), 'bytes': sum(r['bytes'] for r in records)}))


if __name__ == '__main__':
    main()
