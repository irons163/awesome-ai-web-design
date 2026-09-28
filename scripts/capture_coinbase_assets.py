#!/usr/bin/env python3
"""Preserve public assets observed in the Coinbase Canada browser reference."""

from __future__ import annotations

import hashlib
import json
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / '.stitch-work' / 'current-official'
ASSETS = ROOT / 'coinbase-assets'
CDN = 'https://images.ctfassets.net/o10es7wu5gm1/'
ICON = 'https://static-assets.coinbase.com/ui-infra/illustration/v1/pictogram/svg/light/'
FONT = 'https://www.coinbase.com/assets/sw-cache/'

URLS = {
    'logo.svg': ICON + 'coinbaseLogoNavigation-4.svg',
    'hero.avif': CDN + '5FRx7D75B5NeGKmnCjBTzc/93f654ac9bfa3abc0c2b28932b4d1e1c/LOLP_EN.png?fm=avif&w=2160&h=2250&q=65',
    'usdc.avif': CDN + 'd7A7x1TYo6WoXucBnBx7R/6220e38396bc3f903ec8010feeb0297a/EN.png?fm=avif&w=2034&h=2016&q=65',
    'canada-phone.svg': CDN + '4clhoHumOzwRIuMvRKNMAL/d8e84a1212141a112cc324aa4a1e0079/Frame_1984077839.svg',
    'video-poster.webp': CDN + '6zEPuFRRebtQhSq16t3ANT/b4120f6788b18555f23c541cfffa3dec/image__13_.png?fm=webp&w=1600&q=72',
    'apy-coins.webp': CDN + 'TTe1gYRhqvp3J2t69vaqJ/98bb12c755a5b8007029949e1cedef33/coins.png?fm=webp&w=1100&q=76',
    'advanced-trade.webp': CDN + '6Ek6ntzQGzeW18LxdsyyzJ/55fcb928e10ceeef11686e2f017cbfdd/visual-spot__2_.png?fm=webp&w=1100&q=76',
    'coinbase-one.webp': CDN + '53cTUbesxc0ggDfD0M4A4s/b48ecca017ffe2dc61f9b572e14b0553/CB1_-_CA.png?fm=webp&w=1100&q=76',
    'worldwide.svg': ICON + 'worldwide-3.svg',
    'safe.svg': ICON + 'safe-3.svg',
    'support.svg': ICON + 'support-5.svg',
    'canada.svg': ICON + 'decentralizedIdentity-3.svg',
    'CoinbaseDisplay-Regular.woff2': FONT + 'a_BDyAm2xz.woff2',
    'CoinbaseDisplay-Medium.woff2': FONT + 'a_Dd_cEDRa.woff2',
    'CoinbaseSans-Regular.woff2': FONT + 'a_BybxolpF.woff2',
    'CoinbaseSans-Medium.woff2': FONT + 'a_CH-aRrrD.woff2',
    'CoinbaseText-Regular.woff2': FONT + 'a_BJ1-X6Dz.woff2',
}


def capture(entry: tuple[str, str]) -> dict:
    filename, url = entry
    request = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/130.0 Safari/537.36',
        'Accept': 'image/avif,image/webp,image/png,image/svg+xml,font/woff2,*/*;q=0.8',
    })
    with urllib.request.urlopen(request, timeout=45) as response:
        data = response.read()
        mime = response.headers.get('Content-Type', '')
        status = response.status
    if status != 200 or not data:
        raise RuntimeError(f'{filename}: HTTP {status}, {len(data)} bytes')
    (ASSETS / filename).write_bytes(data)
    return {'path': 'coinbase-assets/' + filename, 'url': url, 'status': status,
            'content_type': mime, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=6) as pool:
        assets = list(pool.map(capture, URLS.items()))
    record = {
        'reference': 'https://www.coinbase.com/en-ca',
        'observed_at': datetime.now().astimezone().isoformat(),
        'note': 'DOM image sources and public font stylesheet observed in live Coinbase Canada browser; Contentful image transforms preserve first-party source.',
        'assets': assets,
    }
    (ROOT / 'coinbase-asset-provenance.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps({'count': len(assets), 'bytes': sum(a['bytes'] for a in assets),
                      'largest': sorted(((a['path'], a['bytes']) for a in assets), key=lambda x: -x[1])[:6]}))


if __name__ == '__main__':
    main()
