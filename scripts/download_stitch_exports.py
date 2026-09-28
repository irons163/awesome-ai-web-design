#!/usr/bin/env python3
"""Save native Stitch HTML and screenshots from a one-line download manifest."""

from __future__ import annotations

import hashlib
import json
import sys
import termios
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / '.stitch-work' / 'current-official'
ALLOWED_HOSTS = {
    'contribution.usercontent.google.com',
    'lh3.googleusercontent.com',
}


def main() -> None:
    if sys.stdin.isatty():
        attributes = termios.tcgetattr(sys.stdin.fileno())
        attributes[3] &= ~termios.ECHO
        termios.tcsetattr(sys.stdin.fileno(), termios.TCSANOW, attributes)
    if len(sys.argv) > 1:
        manifest = json.loads(Path(sys.argv[1]).read_text())
    else:
        print('ready', flush=True)
        manifest = json.loads(sys.stdin.readline())
    saved = []
    for item in manifest:
        url = item['url']
        parsed = urllib.parse.urlsplit(url)
        if parsed.scheme != 'https' or parsed.hostname not in ALLOWED_HOSTS:
            raise ValueError(f'Unexpected Stitch export host for {item["path"]}')
        target = (ROOT / item['path']).resolve()
        target.relative_to(ROOT.resolve())
        if target.suffix not in ('.html', '.png'):
            raise ValueError(f'Unexpected export suffix: {target}')
        request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(request, timeout=60) as response:
            data = response.read()
            if response.status != 200 or not data:
                raise ValueError(f'Export unavailable: {target.name}')
        target.write_bytes(data)
        saved.append({
            'path': target.name,
            'bytes': len(data),
            'sha256': hashlib.sha256(data).hexdigest(),
        })
    print(json.dumps(saved), flush=True)


if __name__ == '__main__':
    main()
