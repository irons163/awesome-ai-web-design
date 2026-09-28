#!/usr/bin/env python3
"""Capture selected, dated first-party Kraken homepage media with provenance."""

from __future__ import annotations

import hashlib
import json
import re
import urllib.parse
import urllib.request
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1] / '.stitch-work' / 'current-official'
ASSETS = ROOT / 'kraken-assets'
SOURCE = ROOT / 'kraken-source-current.html'
BASE = 'https://www.kraken.com/'
ALLOWED_HOSTS = {'www.kraken.com', 'assets-cms.kraken.com', 'assets.kraken.com'}


class Images(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.urls: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == 'img':
            src = dict(attrs).get('src')
            if src and not src.startswith('data:'):
                self.urls.append(urllib.parse.urljoin(BASE, src))


def image_url(images: Images, fragment: str, *, webp: bool = False) -> str:
    matches = [url for url in images.urls if fragment in url]
    if len(matches) != 1:
        # The same wordmark may appear in header and footer; both resolve to
        # the same first-party image URL.
        matches = list(dict.fromkeys(matches))
    if len(matches) != 1:
        raise ValueError(f'Expected one official image for {fragment}: {len(matches)}')
    url = matches[0]
    if webp:
        url = url.split('?', 1)[0] + '?w=2880&fit=min&fm=webp'
    return url


def capture(name: str, url: str, records: list[dict[str, object]]) -> None:
    if urllib.parse.urlsplit(url).hostname not in ALLOWED_HOSTS:
        raise ValueError(f'Unexpected asset origin for {name}')
    request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(request, timeout=60) as response:
        data = response.read()
        if response.status != 200 or not data:
            raise ValueError(f'Unable to retrieve {name}')
    path = ASSETS / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    records.append({
        'path': f'kraken-assets/{name}',
        'url': url,
        'bytes': len(data),
        'sha256': hashlib.sha256(data).hexdigest(),
        'content_type': response.headers.get('Content-Type'),
        'observed_at': datetime.now(ZoneInfo('Asia/Taipei')).isoformat(),
    })
    print(name, len(data))


def main() -> None:
    images = Images()
    images.feed(SOURCE.read_text())
    ASSETS.mkdir(exist_ok=True)
    selected = {
        'wordmark.svg': ('4d67f3f4eac6aa0702c6ae62b1e0b1abc41b10cd-650x155.svg', False),
        'forbes.svg': ('1698017cf06d51d17fff161c3704544f8402ecc5-68x18.svg', False),
        'pro-logo.svg': ('ebe60e0d899368ee5c501148232e2b94c76b72c1-360x101.svg', False),
        'pro-terminal.webp': ('18bdae5aa5c55c7079759a3b3f0791a7ccf6b3e7-3528x1922.png', True),
        'consumer-logo.svg': ('6b1b0a92eb0de8b2f5cc9b71ec64afdd95c7830b-650x101.svg', False),
        'consumer-image.webp': ('94670e838d81f32713c41c5ba8d5ffdab856011f-1506x870.png', True),
        'wallet-logo.svg': ('cdad5a95928a06d370c69e09a74143e8b808824b-126x24.svg', False),
        'wallet-image.webp': ('a73da2b426e71b92358d5f5dbb525260a5e1b44e-3351x1094.png', True),
        'krak-logo.svg': ('cc0a15892d68e7927c1cd74a464047e15da98e71-84x18.svg', False),
        'krak-card-front.webp': ('83a218968d1312c9878ced6d19e0c94d33b60856-1200x548.png', True),
        'krak-card-wide.webp': ('ef0574a3da54c037807191db5ad497fcc7efaf57-2176x660.png', True),
        'leverage.webp': ('6292080a30469f68c4b38c602eb4df41a6f7ca31-1380x776.png', True),
        'beast.webp': ('d73d254daec5b3bfcccd3b8c05fd35202025c86a-1200x1200.png', True),
    }
    records: list[dict[str, object]] = []
    for name, (fragment, webp) in selected.items():
        capture(name, image_url(images, fragment, webp=webp), records)
    for symbol in ('btc', 'eth', 'usdt', 'bnb', 'xrp', 'usdc', 'sol', 'ltc', 'zec', 'near'):
        capture(f'{symbol}.webp',
                f'https://assets.kraken.com/marketing/web/icons-uni-webp/s_{symbol}.webp?i=kds',
                records)
    for font in ('Kraken-Brand-Regular.otf', 'Kraken-Brand-Bold.otf',
                 'Kraken-Product-Regular.woff2', 'Kraken-Product-Medium.woff2',
                 'Kraken-Product-SemiBold.woff2'):
        capture(font, f'https://www.kraken.com/_assets/fonts/{font}', records)
    source = SOURCE.read_text()
    for label, name in (('Apple', 'apple-signin.svg'), ('Google', 'google-signin.svg')):
        match = re.search(
            rf'aria-label="Sign in with {label}".*?(<svg\b.*?</svg>)',
            source, re.S,
        )
        if not match:
            raise ValueError(f'Official {label} sign-in icon not found in HTML')
        data = match.group(1).encode()
        (ASSETS / name).write_bytes(data)
        records.append({
            'path': f'kraken-assets/{name}',
            'url': f'https://www.kraken.com/#signin-{label.lower()}-inline-svg',
            'bytes': len(data),
            'sha256': hashlib.sha256(data).hexdigest(),
            'content_type': 'image/svg+xml',
            'capture_method': 'official_html_inline_svg_extraction',
            'observed_at': datetime.now(ZoneInfo('Asia/Taipei')).isoformat(),
        })
    (ROOT / 'kraken-asset-provenance.json').write_text(
        json.dumps(records, ensure_ascii=False, indent=2) + '\n'
    )
    print('captured', len(records), 'assets')


if __name__ == '__main__':
    main()
