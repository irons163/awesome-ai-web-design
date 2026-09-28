#!/usr/bin/env python3
"""Capture the dated MiniMax homepage's observed first-party static media."""

from __future__ import annotations

import hashlib
import json
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / '.stitch-work' / 'current-official'
ASSETS = ROOT / 'minimax-assets'
SOURCES = ROOT / 'minimax-asset-sources.json'
HOSTS = {'www.minimax.io', 'file.cdn.minimax.io', 'filecdn.minimax.chat'}


def capture(item: dict) -> dict:
    name, url = item['name'], item['url']
    if Path(name).name != name or urllib.parse.urlsplit(url).hostname not in HOSTS:
        raise ValueError(f'Unexpected MiniMax asset: {name}')
    request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'image/webp,image/*,font/*,*/*;q=0.8'})
    with urllib.request.urlopen(request, timeout=40) as response:
        data = response.read()
        status, content_type = response.status, response.headers.get('Content-Type', '')
    if status != 200 or not data:
        raise RuntimeError(f'MiniMax asset {name}: HTTP {status}, {len(data)} bytes')
    (ASSETS / name).write_bytes(data)
    return {'path': 'minimax-assets/' + name, 'url': url, 'status': status,
            'content_type': content_type, 'bytes': len(data),
            'sha256': hashlib.sha256(data).hexdigest()}


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    sources = json.loads(SOURCES.read_text())
    with ThreadPoolExecutor(max_workers=8) as pool:
        records = list(pool.map(capture, sources['assets']))
    provenance = {
        'reference': sources['reference'],
        'captured_at': datetime.now().astimezone().isoformat(),
        'source_html_sha256': hashlib.sha256((ROOT / 'minimax-source-current.html').read_bytes()).hexdigest(),
        'note': 'Observed first-party MiniMax assets; some CDN image URLs explicitly request WebP conversion.',
        'assets': records,
    }
    (ROOT / 'minimax-asset-provenance.json').write_text(json.dumps(provenance, indent=2) + '\n')
    print(json.dumps({'count': len(records), 'total_bytes': sum(x['bytes'] for x in records)}))


if __name__ == '__main__':
    main()
