#!/usr/bin/env python3
"""Capture Nike Canada public media observed in the dated official reference."""

from __future__ import annotations

import hashlib
import json
import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / '.stitch-work' / 'current-official'
ASSETS = ROOT / 'nike-assets'
NIKE_CDN = 'https://static.nike.com/a/images/'
FONT_CDN = 'https://www.nike.com/static/ncss/'

# IDs and image variants were observed in the current Nike Canada source and
# desktop/mobile browser DOM. The downloaded variants request WebP at a size
# suitable for the static study while retaining the same official source image.
IMAGES = {
    'hero-desktop.webp': ('2ff6b112-c162-43a6-bd26-f46b0d0593a6', 'image.jpg', 1280),
    'hero-mobile.webp': ('2e6b4d2a-2b2c-492a-88ab-8432b7238930', 'image.jpg', 600),
    'hero-body-desktop.webp': ('a75f8e66-d973-4eef-b8b9-fe5708c225de', 'image.png', 1280),
    'hero-body-mobile.webp': ('aecd249e-1ffc-4360-962b-5e4c8ed024c6', 'image.png', 600),
    'studio-desktop.webp': ('092ba7ea-eb61-40d2-8967-27a56186785e', 'nike-just-do-it.png', 1280),
    'studio-mobile.webp': ('d3427710-348d-4a1f-a25d-fe17f505b278', 'nike-just-do-it.png', 600),
    'jordan-desktop.webp': ('e43c5ee7-1c1a-45fa-ba7e-052fe82bf65b', 'nike-just-do-it.jpg', 800),
    'jordan-mobile.webp': ('dd02b14e-2ca6-424f-a304-fe3ae2ce259e', 'nike-just-do-it.jpg', 600),
    'snkrs-desktop.webp': ('a7500dde-5200-4efa-8b9c-c41c89956902', 'nike-just-do-it.jpg', 800),
    'snkrs-mobile.webp': ('d8325dc0-057f-4653-9ee8-c80afa4c27dd', 'nike-just-do-it.jpg', 600),
    'acg-desktop.webp': ('d56e7a28-4e94-4ac6-a3d8-2216afab832d', 'nike-just-do-it.jpg', 1280),
    'acg-mobile.webp': ('1a452448-ebe6-4a83-9d77-60f03a4c7274', 'nike-just-do-it.jpg', 600),
    'acg-wordmark.webp': ('570d1fba-724b-4a37-a190-af9470b3edfa', 'nike-just-do-it.png', 800),
    'bottom-wordmark.webp': ('82524845-2637-4b3c-a7cb-67a416108197', 'nike-just-do-it.png', 700),
    'sport-running.webp': ('f26f86a2-5539-4298-aa99-373adb9874ad', 'nike-just-do-it.jpg', 500),
    'sport-running-mobile.webp': ('69a8ef57-1c33-4b3f-b381-6f7ce3a9757c', 'nike-just-do-it.jpg', 400),
    'sport-tennis.webp': ('cb68588d-4a21-4c6b-a82b-4d323378ba07', 'nike-just-do-it.jpg', 500),
    'sport-basketball.webp': ('e2487352-1a64-48d1-aa9b-1d175fbb05ab', 'nike-just-do-it.jpg', 500),
    'sport-training.webp': ('93b7242b-db86-4774-b8c0-f113f9118b86', 'nike-just-do-it.jpg', 500),
}
FONTS = {
    'Nike-Futura-ND.woff2': FONT_CDN + 'nike-design-system-fonts/dotcom/fonts/Nike-Futura-ND-L-CnXBd.woff2',
    'HelveticaNowText.woff2': FONT_CDN + '5.0/dotcom/fonts/HelveticaNowText.woff2',
    'HelveticaNowTextMedium.woff2': FONT_CDN + '5.0/dotcom/fonts/HelveticaNowTextMedium.woff2',
    'HelveticaNowDisplayMedium.woff2': FONT_CDN + '5.0/dotcom/fonts/HelveticaNowDisplayMedium.woff2',
}


def capture(entry: tuple[str, str]) -> dict:
    name, url = entry
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/130.0 Safari/537.36',
        'Accept': 'image/webp,image/avif,image/*,font/woff2,*/*;q=0.8',
    })
    with urllib.request.urlopen(req, timeout=40) as response:
        data, mime, status = response.read(), response.headers.get('Content-Type', ''), response.status
    if status != 200 or not data:
        raise RuntimeError(f'{name}: HTTP {status}, {len(data)} bytes')
    (ASSETS / name).write_bytes(data)
    return {'path': 'nike-assets/' + name, 'url': url, 'status': status,
            'content_type': mime, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def extract_brand_svg(source: str, name: str) -> bytes:
    start = source.index(f'aria-label="{name}"')
    match = re.search(r'<svg\b.*?</svg>', source[start:], re.DOTALL)
    if not match or match.start() > 300:
        raise ValueError(f'Could not find {name} official inline SVG')
    markup = match.group(0)
    if 'xmlns=' not in markup:
        markup = markup.replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" ', 1)
    return markup.encode()


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    urls = {name: (NIKE_CDN + f'f_webp,q_75,cs_srgb/w_{width},c_limit/{asset_id}/{filename}')
            for name, (asset_id, filename, width) in IMAGES.items()}
    urls.update(FONTS)
    with ThreadPoolExecutor(max_workers=8) as pool:
        records = list(pool.map(capture, urls.items()))

    source = (ROOT / 'nike-source-current.html').read_text()
    for name, label in (('jordan.svg', 'Jordan'), ('converse.svg', 'Converse')):
        data = extract_brand_svg(source, label)
        (ASSETS / name).write_bytes(data)
        records.append({'path': 'nike-assets/' + name, 'url': 'inline svg in https://www.nike.com/ca/',
                        'status': 200, 'content_type': 'image/svg+xml', 'bytes': len(data),
                        'sha256': hashlib.sha256(data).hexdigest()})
    swoosh = ('<svg xmlns="http://www.w3.org/2000/svg" width="64" height="22" viewBox="0 0 64 22" fill="none">'
              '<path fill-rule="evenodd" clip-rule="evenodd" d="M17.7277 12.1511C15.999 12.598 14.4241 12.8196 13.0469 12.8196C11.3396 12.8196 9.94617 12.4728 8.97074 11.7793C4.02962 8.28845 8.54956 0.885548 9.06118 0.0629324C6.88551 2.37923 4.65235 4.80341 2.89851 7.44593C-0.0575023 11.9597 -0.812655 16.2475 0.910825 18.906C2.23896 20.9642 4.40042 22 7.37517 22C10.0146 22 13.2975 21.1832 17.1928 19.5559L64 0.0173385L63.9981 0L17.7277 12.1511Z" fill="#111111"/></svg>').encode()
    (ASSETS / 'swoosh.svg').write_bytes(swoosh)
    records.append({'path': 'nike-assets/swoosh.svg', 'url': 'inline svg in https://www.nike.com/ca/',
                    'status': 200, 'content_type': 'image/svg+xml', 'bytes': len(swoosh),
                    'sha256': hashlib.sha256(swoosh).hexdigest()})
    record = {'reference': 'https://www.nike.com/ca/',
              'captured_at': datetime.now().astimezone().isoformat(),
              'source_html_sha256': hashlib.sha256((ROOT / 'nike-source-current.html').read_bytes()).hexdigest(),
              'note': 'All files derive from live Nike Canada first-party public URLs or inline SVGs; images are CDN WebP transforms of observed source IDs.',
              'assets': records}
    (ROOT / 'nike-asset-provenance.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps({'count': len(records), 'total_bytes': sum(x['bytes'] for x in records),
                      'largest': sorted(((x['path'], x['bytes']) for x in records), key=lambda x: -x[1])[:5]}))


if __name__ == '__main__':
    main()
