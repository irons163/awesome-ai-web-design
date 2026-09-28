#!/usr/bin/env python3
"""Capture selected media and fonts from the dated official Intercom homepage."""

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
SOURCE = (ROOT / 'intercom-source-current.html').read_text()
ASSETS = ROOT / 'intercom-assets'
ASSETS.mkdir(exist_ok=True)


class Images(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.urls: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == 'img':
            src = dict(attrs).get('src')
            if src:
                self.urls.append(src)


IMAGES = Images()
IMAGES.feed(SOURCE)

SELECT = {
    'hero-shadow.webp': 'Intercom_Hero-Gallery_02.webp',
    'hero-floral.webp': 'Intercom_Hero-Gallery_06.webp',
    'hero-eye.webp': 'Intercom_Hero-Gallery_04.webp',
    'hero-sky.webp': 'Intercom_Hero-Gallery_03.webp',
    'products-backdrop.webp': 'be816b66f5bea05d715c01902b842bd3f672837b-1800x936.webp',
    'products-helpdesk-desktop.webp': '1a76ba43b365bcc495d99bfa395cbdd9d45704aa-6400x2800.webp',
    'products-fin-desktop.webp': '91a60acc31e7e302762bb87994790cbd81d67b25-6400x2800.webp',
    'products-helpdesk-mobile.webp': 'c5522322ef381b2249f1fe193a87be0b86907350-1600x1600.webp',
    'products-fin-mobile.webp': '11389c173c14c6ff71cfe160c183ab19fd2ef23f-1600x1600.webp',
    'helpdesk-illustration.webp': 'Intercom_Helpdesk_illo_v2.webp',
    'helpdesk-inbox.webp': 'e2d5af2f03a2a9cf22ea15fdf8d44f3e6b06e0f3-3714x1677.webp',
    'helpdesk-tickets.webp': 'f90345730b8aeeb67178c7bafb0fffecd722f178-3714x1677.webp',
    'helpdesk-onboarding.webp': 'a78f1e62fff0f7e0b8288a798133c2526f336d14-3714x1677.webp',
    'fin-illustration.webp': 'Intercom_Fin_illo_v2.webp',
    'fin-report.webp': '23daa8a658d81cbda4ec00f0559fb6dba0f4853d-3044x3044.webp',
    'together-illustration.webp': 'Intercom_Complete_illo_v2.webp',
    'together-handoff.webp': '2834cc7c1630e5f250b09d1569f9294e2f390ed7-1616x1612.webp',
    'together-recommendations.webp': '01831fc9b275a0d6947a0d0b756fbc90ad39881a-1612x1612.webp',
    'together-knowledge.webp': 'e36358115db8192727d4b8206fbdd126ac695767-1612x1612.webp',
    'testimonial-anthropic.webp': 'Testimonial_Anthropic.webp',
    'testimonial-glean.webp': 'Testimonial_Glean.webp',
    'testimonial-neo.webp': 'Testimonial_Neo.webp',
    'integrations-grid.webp': 'Intercom_Integrations_Grid.webp',
    'pricing-backdrop.webp': '2c4d4c23cb6427f422f41645141866fe058ba19b-2000x1501.webp',
    'footer-gallery-01.webp': 'IC_Footer_Gallery_01.webp',
    'footer-gallery-02.webp': 'IC_Footer_Gallery_02.webp',
    'footer-gallery-03.webp': 'IC_Footer_Gallery_03.webp',
    'footer-gallery-04.webp': 'IC_Footer_Gallery_04.webp',
    'footer-gallery-05.webp': 'IC_Footer_Gallery_05.webp',
    'footer-gallery-06.webp': 'IC_Footer_Gallery_06.webp',
}

FONTS = {
    'Saans-Regular.woff2': 'Saans_Regular-s.0y32wrc-1quhd.woff2',
    'Saans-Medium.woff2': 'Saans_Medium-s.30fecupmfg4ht.woff2',
    'Serrif-Light.woff2': 'Serrif_Light_subset-s.0xcw-beyjla6z.woff2',
    'Serrif-Regular.woff2': 'Serrif_Regular_subset-s.01dfn90lujsv9.woff2',
}

INLINE_SVGS = {
    'intercom-wordmark.svg': '0 0 620 102',
    'intercom-mark.svg': '0 0 36 37',
    'g2.svg': '0 0 24 25',
}


def original_url(src: str) -> str:
    if src.startswith('/ims-image?'):
        src = urllib.parse.parse_qs(urllib.parse.urlsplit(src).query)['url'][0]
    if src.startswith('/'):
        return 'https://www.intercom.com' + src.split('?', 1)[0]
    if src.startswith('https://cdn.sanity.io/'):
        return src.split('?', 1)[0] + '?w=1280&fm=webp'
    raise ValueError(f'Unexpected official image URL: {src}')


def matching_url(filename: str) -> str:
    urls = sorted({original_url(src) for src in IMAGES.urls
                   if urllib.parse.urlsplit(original_url(src)).path.endswith('/' + filename)})
    if len(urls) != 1:
        raise ValueError(f'Expected one official image for {filename}: {urls}')
    return urls[0]


def main() -> None:
    provenance = []
    for output, filename in SELECT.items():
        url = matching_url(filename)
        with urllib.request.urlopen(urllib.request.Request(
            url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=45) as response:
            data = response.read()
            assert response.status == 200 and response.headers.get_content_type() == 'image/webp'
        (ASSETS / output).write_bytes(data)
        provenance.append({'url': url, 'path': f'intercom-assets/{output}',
                           'sha256': hashlib.sha256(data).hexdigest(),
                           'bytes': len(data), 'capture_method': 'public_website_asset_download',
                           'observed_at': datetime.now(ZoneInfo('Asia/Taipei')).isoformat()})
        print(output, len(data))
    for output, filename in FONTS.items():
        url = f'https://www.intercom.com/_next/static/immutable/media/{filename}'
        with urllib.request.urlopen(urllib.request.Request(
            url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=45) as response:
            data = response.read()
            assert response.status == 200 and len(data) > 100
        (ASSETS / output).write_bytes(data)
        provenance.append({'url': url, 'path': f'intercom-assets/{output}',
                           'sha256': hashlib.sha256(data).hexdigest(),
                           'bytes': len(data), 'capture_method': 'public_website_asset_download',
                           'observed_at': datetime.now(ZoneInfo('Asia/Taipei')).isoformat()})
        print(output, len(data))
    for output, viewbox in INLINE_SVGS.items():
        matches = re.findall(r'<svg[^>]*viewBox="' + re.escape(viewbox)
                             + r'"[^>]*>.*?</svg>', SOURCE)
        if not matches:
            raise ValueError(f'No official inline SVG for {output}')
        data = matches[0].encode()
        (ASSETS / output).write_bytes(data)
        provenance.append({'url': 'https://www.intercom.com/',
                           'source_snapshot': 'intercom-source-current.html',
                           'source_viewbox': viewbox,
                           'path': f'intercom-assets/{output}',
                           'sha256': hashlib.sha256(data).hexdigest(),
                           'bytes': len(data),
                           'capture_method': 'official_html_inline_svg_extraction',
                           'observed_at': datetime.now(ZoneInfo('Asia/Taipei')).isoformat()})
        print(output, len(data))
    logo_dir = ASSETS / 'customer-logos'
    logo_dir.mkdir(exist_ok=True)
    seen = set()
    for label, svg in re.findall(
            r'<div[^>]*role="img" aria-label="([^"]+ logo)"[^>]*>'
            r'(<svg.*?</svg>)</div>', SOURCE):
        if label in seen:
            continue
        seen.add(label)
        slug = re.sub(r'[^a-z0-9]+', '-', label.removesuffix(' logo').lower()).strip('-')
        output = f'customer-logos/{slug}.svg'
        data = svg.encode()
        (ASSETS / output).write_bytes(data)
        provenance.append({'url': 'https://www.intercom.com/',
                           'source_snapshot': 'intercom-source-current.html',
                           'source_label': label, 'path': f'intercom-assets/{output}',
                           'sha256': hashlib.sha256(data).hexdigest(),
                           'bytes': len(data),
                           'capture_method': 'official_html_inline_svg_extraction',
                           'observed_at': datetime.now(ZoneInfo('Asia/Taipei')).isoformat()})
        print(output, len(data))
    (ROOT / 'intercom-asset-provenance.json').write_text(
        json.dumps(provenance, indent=2) + '\n')


if __name__ == '__main__':
    main()
