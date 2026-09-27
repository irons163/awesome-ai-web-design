#!/usr/bin/env python3
"""Save dated, public Tesla homepage media with a URL and hash trail."""

from __future__ import annotations

import hashlib
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1] / '.stitch-work' / 'current-official'
DESTINATION = ROOT / 'tesla-assets'
IMAGE_BASE = 'https://digitalassets.tesla.com/tesla-contents/image/upload/f_auto,q_auto/'
VIDEO_BASE = 'https://digitalassets.tesla.com/tesla-contents/video/upload/f_auto,q_auto/'
FONT_BASE = 'https://digitalassets.tesla.com/tesla-design-system/raw/upload/static/fonts/universal-sans-2/web/'

# Names come from the public homepage's <picture>, <img>, <video>, and loaded
# resource URLs observed on 2026-09-28. Avoid fabricating unseen assets.
IMAGES = (
    'Homepage-Promo-Model-Y-L-Family-Desktop-NA.jpg',
    'Homepage-Promo-Model-Y-L-Family-Mobile-NA.jpg',
    'Homepage-Promo-Model-3-Desktop-US.jpg',
    'Homepage-Promo-Model-3-Mobile-US.jpg',
    'Homepage-Promo-Model-Y-L-Seats-Desktop-AU-NZ.jpg',
    'Homepage-Promo-Model-Y-L-Seats-Mobile-AU-NZ.jpg',
    'Homepage-FSD-Card-Desktop-Tablet-Poster.jpg',
    'Homepage-FSD-Card-Mobile-Poster.jpg',
    'Homepage-Card-Model-Y-L-Desktop-US.jpg',
    'Homepage-Card-Model-Y-L-Mobile-US.jpg',
    'Homepage-Card-Model-3-Desktop-US_PR_MX.jpg',
    'Homepage-Card-Model-3-Mobile-US_PR_MX.jpg',
    'Homepage-Vehicle-Card-Model-Y-Desktop-US-Snow.jpg',
    'Homepage-Vehicle-Card-Model-Y-Mobile-US-Snow.jpg',
    'Homepage-Card-Cybertruck-Desktop-US_PR_MX.jpg',
    'Homepage-Card-Cybertruck-Mobile-US_PR_MX.jpg',
    'Homepage-Card-Vehicle-CPO-Desktop.jpg',
    'Homepage-Card-Vehicle-CPO-Mobile.jpg',
    'Homepage-Grid-Current-Offers-All-Devices.png',
    'Homepage-Grid-Inventory-All-Devices.jpg',
    'Homepage-SuperchargerMap-Poster-US.jpg',
    'Homepage-Card-Solar-Panels-Desktop-v2.jpg',
    'Homepage-Card-Solar-Panels-Mobile-v2.jpg',
    'Homepage-Card-Powerwall-Desktop.png',
    'Homepage-Card-Powerwall-Mobile.png',
    'Homepage-Card-Megapack-Desktop-v2.jpg',
    'Homepage-Card-Megapack-Mobile-v2.jpg',
)
VIDEOS = (
    'Homepage-FSD-Card-Desktop.mp4',
    'Homepage-FSD-Card-Mobile.mp4',
)
FONTS = (
    'text/Universal-Sans-Text-Regular.woff2',
    'text/Universal-Sans-Text-Medium.woff2',
    'display/Universal-Sans-Display-Regular.woff2',
    'display/Universal-Sans-Display-Medium.woff2',
)


def download(url: str, name: str) -> dict:
    request = Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                      'AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.tesla.com/',
    })
    with urlopen(request, timeout=90) as response:
        data = response.read()
        content_type = response.headers.get('Content-Type', '')
    if not data or content_type.startswith('text/html'):
        raise ValueError(f'Unexpected response {content_type!r}')
    (DESTINATION / name).write_bytes(data)
    return {'name': name, 'url': url, 'sha256': hashlib.sha256(data).hexdigest(),
            'bytes': len(data), 'content_type': content_type,
            'capture_method': 'official_direct_download'}


def main() -> None:
    DESTINATION.mkdir(exist_ok=True)
    items = ([(IMAGE_BASE + name, name) for name in IMAGES] +
             [(VIDEO_BASE + name, name) for name in VIDEOS] +
             [(FONT_BASE + name, Path(name).name) for name in FONTS])
    captured, failures = [], []
    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = {pool.submit(download, url, name): (url, name)
                   for url, name in items}
        for future in as_completed(futures):
            url, name = futures[future]
            try:
                captured.append(future.result())
            except Exception as error:
                failures.append({'name': name, 'url': url, 'error': str(error)})
    captured.sort(key=lambda item: item['name'])
    failures.sort(key=lambda item: item['name'])
    (ROOT / 'tesla-asset-provenance.json').write_text(
        json.dumps(captured, indent=2) + '\n')
    (ROOT / 'tesla-asset-failures.json').write_text(
        json.dumps(failures, indent=2) + '\n')
    print(f'Saved {len(captured)} public Tesla assets; {len(failures)} failed')
    for failure in failures:
        print(failure['name'] + ': ' + failure['error'][:180])


if __name__ == '__main__':
    main()
