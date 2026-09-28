#!/usr/bin/env python3
"""Capture selected public media from the observed 2026 Superhuman homepage."""

from __future__ import annotations

import hashlib
import json
import re
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1] / '.stitch-work' / 'current-official'
SOURCE = ROOT / 'superhuman-source-current.html'
ASSETS = ROOT / 'superhuman-assets'
BASE = 'https://superhumanstatic.com'

ASSET_URLS = {
    'hero-background.mp4': f'{BASE}/super-funnel/main/public/videos/v1/shared/hero-background.mp4',
    'hero-person.avif': f'{BASE}/vwfkeyj6n9ac/4ExmcB9B5akcYJaGyy2eKh/cc5cb3ba20a218281b975fb595892a8a/person-4.webp?w=822&fm=avif',
    'mail-fallback.png': f'{BASE}/vwfkeyj6n9ac/6GZdcneKJhk1BOMc4wSVFP/76ff2c85fd93f8171adc15fae2f7df56/mail-fallback.png',
    'grammarly-fallback.png': f'{BASE}/vwfkeyj6n9ac/4Xbsd7oCDAyYCJROHZ80Oo/e8f5b1d2fab4760b806f6413cd256f89/grammarly-fallback.png',
    'docs-fallback.png': f'{BASE}/vwfkeyj6n9ac/aX0n8e13NwFiOnXVCAG8u/eed3b77003f84aa38d0bb4eaf5becc6f/coda-fallback.png',
    'go-fallback.png': f'{BASE}/vwfkeyj6n9ac/2Elaw7EDLXcTtRhFmYlD3c/048b30c77421faf80ce7556320cd98c6/go-fallback.png',
    'manifesto.webp': f'{BASE}/vwfkeyj6n9ac/6dRKs0BhqWbnOdnl43ifjt/0a2f56e8ac1c8cddfe72634f7983b440/homepage-manifesto.webp',
    'tonal-flower.webp': f'{BASE}/vwfkeyj6n9ac/1MZDaABlJ6y5NbSOUUeaTN/0e6ab0d1c98158fb9b6c6a6c2e089734/homepage-tonal-flower.webp',
    'superhuman-icon.svg': f'{BASE}/super-funnel/main/public/images/v4/favicons/superhuman-icon.svg',
    'SuperSans-VF-Upright.woff2': f'{BASE}/s/fonts/v1/SuperSans-VF-Upright.woff2',
    'SuperSans-VF-Italic.woff2': f'{BASE}/s/fonts/v1/SuperSans-VF-Italic.woff2',
    'SuperSerif-VF-Upright.woff2': f'{BASE}/s/fonts/v1/SuperSerif-VF-Upright.woff2',
    'SuperSerif-VF-Italic.woff2': f'{BASE}/s/fonts/v1/SuperSerif-VF-Italic.woff2',
    'SuperSansMono-VF.woff2': f'{BASE}/s/fonts/v1/SuperSansMono-VF.woff2',
    **{
        f'customer-logos/{name}.svg':
        f'{BASE}/super-funnel/main/public/images/v4/trusted-by-logos/trustedby-logo-{name}.svg'
        for name in (
            'openai', 'figma', 'hubspot', 'doordash', 'expensify', 'geico',
            'zoom', 'rivian', 'zapier', 'brex', 'atlassian', 'ted'
        )
    },
}


def add_record(records: list[dict], name: str, data: bytes, url: str,
               method: str = 'public_website_asset_download') -> None:
    target = ASSETS / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    records.append({
        'url': url,
        'path': f'superhuman-assets/{name}',
        'sha256': hashlib.sha256(data).hexdigest(),
        'bytes': len(data),
        'capture_method': method,
        'observed_at': datetime.now(ZoneInfo('Asia/Taipei')).isoformat(),
    })
    print(name, len(data))


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    records: list[dict] = []
    for name, url in ASSET_URLS.items():
        if not url.startswith(BASE + '/'):
            raise ValueError(f'Unexpected host for {name}')
        request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(request, timeout=50) as response:
            data = response.read()
            if response.status != 200 or not data:
                raise ValueError(f'Asset unavailable: {name}')
        add_record(records, name, data, url)
    source = SOURCE.read_text()
    match = re.search(
        r'<symbol id="superhuman-logo" viewBox="([^"]+)" fill="currentColor">'
        r'(.*?)</symbol>', source, flags=re.S
    )
    if not match:
        raise ValueError('Official wordmark symbol missing from captured HTML')
    data = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{match.group(1)}" '
        f'fill="currentColor">{match.group(2)}</svg>'
    ).encode()
    add_record(records, 'superhuman-wordmark.svg', data,
               'https://superhuman.com/', 'official_html_inline_svg_extraction')
    (ROOT / 'superhuman-asset-provenance.json').write_text(
        json.dumps(records, indent=2, ensure_ascii=False) + '\n'
    )
    print('captured', len(records), 'assets')


if __name__ == '__main__':
    main()
