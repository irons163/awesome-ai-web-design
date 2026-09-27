#!/usr/bin/env python3
"""Save the public assets observed in MongoDB's dated official homepage."""

from __future__ import annotations

import hashlib
import html
import json
import re
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1] / '.stitch-work' / 'current-official'
SOURCE = html.unescape((ROOT / 'mongodb-source-current.html').read_text())
ASSET_DIR = ROOT / 'mongodb-assets'
ASSET_DIR.mkdir(exist_ok=True)

SELECT = {
    'logo-white.svg': 'kuyj3d95v5vbmm2f4-horizontal_white.svg',
    'hero-dashboard.avif': 'mjkd9svc9ucaifrlh-000_(1).avif',
    'factory.svg': 'mjitnh3p1wtg5vuzi-Factory.svg',
    'mercor.svg': 'mjreusu45oymixan9-Mercor-32.svg',
    'hugging-face.svg': 'mjreqoppok0lcyvlg-Hugging_face-32.svg',
    'fireworks.svg': 'mjitnsb5c6dvgfxoa-Fireworks.svg',
    'anthropic.svg': 'mjitmdkze5ktd1o5s-Anthropic.svg',
    'coinbase.svg': 'mfe3zm6fqtnmg53st-Coinbase_Wordmark_White.svg',
    'atlas-learning.svg': 'General_EDUCATION_Books_Spot.svg',
    'build-ai.svg': 'General_INDUSTRIES_AI(2)_Thumbnail.svg',
    'voyage-ai.svg': 'General_TECHNOLOGY_Database_Spot.svg',
    'vector-search.svg': 'lpr2w95dde50v1evs-vs_static_2.svg',
    'victorias-secret.svg': 'homepage_hero_vs_static.svg',
    'ecosystem-confluent.svg': 'kzpulv998d4x9q545-logo-confluent.svg',
    'ecosystem-databricks.svg': 'databricks.svg',
    'ecosystem-aws.svg': 'lgwpl72akptbke7gp-AWS_logo_RGB_1.svg',
    'ecosystem-google.svg': 'google_cloud.svg',
    'ecosystem-azure.png': 'Microsoft-Azure-Logo.png',
    'ecosystem-cohere.svg': 'cohere.svg',
    'compass.svg': 'compass.svg',
}
FONTS = {
    'Sohne-Regular.woff2': 'https://static.mongodb.com/com/fonts/Sohne-Regular.woff2',
    'Sohne-Medium.woff2': 'https://static.mongodb.com/com/fonts/Sohne-Medium.woff2',
    'Sohne-Condensed-Regular.woff2': 'https://static.mongodb.com/com/fonts/Sohne-Condensed-Regular.woff2',
    'Sohne-Condensed-Bold.woff2': 'https://static.mongodb.com/com/fonts/Sohne-Condensed-Bold.woff2',
}
HERO = ('https://images.contentstack.io/v3/assets/blt7151619cb9560896/'
        'blt4199f2368c0410cd/6a68e1835f2918727313a463/'
        'mjkd9svc9ucaifrlh-000_(1).avif')
BROWSER_OBSERVED = {
    'mjitnh3p1wtg5vuzi-Factory.svg': 'bltb1ed6164c7b30462/6a68c8d61fc2ba05af35961b',
    'mjreusu45oymixan9-Mercor-32.svg': 'bltbd2e0ca8b2811a15/6a68c8cd2aaf504f47a13623',
    'mjreqoppok0lcyvlg-Hugging_face-32.svg': 'blt3e41f57b592d4584/6a68c8cdaacc0d229c0b1341',
    'mjitnsb5c6dvgfxoa-Fireworks.svg': 'bltddd6e486b1d6b1d9/6a68c8cd8cde668cc4c49791',
    'mjitmdkze5ktd1o5s-Anthropic.svg': 'bltf526b527a876eb6a/6a68c8cd8e0e24262b71735a',
    'mfe3zm6fqtnmg53st-Coinbase_Wordmark_White.svg': 'blt0a9a06e739c2f22c/6a68c8cd879300891b6aac0a',
}


def source_url(filename: str) -> str:
    if filename == 'mjkd9svc9ucaifrlh-000_(1).avif':
        return HERO
    if filename in BROWSER_OBSERVED:
        return ('https://images.contentstack.io/v3/assets/blt7151619cb9560896/'
                + BROWSER_OBSERVED[filename] + '/' + filename)
    if filename == 'kuyj3d95v5vbmm2f4-horizontal_white.svg':
        return ('https://webimages.mongodb.com/_com_assets/cms/' + filename)
    matches = []
    for url in re.findall(r'https://images\.contentstack\.io/[^\s"\'<>]+', SOURCE):
        url = url.rstrip(');,')
        path = urllib.parse.urlsplit(url).path
        if path.endswith('/' + filename):
            matches.append(url)
    matches = sorted(set(matches), key=len)
    if len(matches) != 1:
        raise ValueError(f'Expected one official URL for {filename}: {matches}')
    return matches[0]


def main() -> None:
    results = []
    for name, filename in SELECT.items():
        url = source_url(filename)
        results.append((name, url))
    results.extend(FONTS.items())
    provenance = []
    for name, url in results:
        request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(request, timeout=45) as response:
            data = response.read()
            assert response.status == 200 and len(data) > 100, (name, response.status)
        (ASSET_DIR / name).write_bytes(data)
        provenance.append({
            'url': url,
            'path': f'mongodb-assets/{name}',
            'sha256': hashlib.sha256(data).hexdigest(),
            'bytes': len(data),
            'capture_method': 'public_website_asset_download',
            'observed_at': datetime.now(ZoneInfo('Asia/Taipei')).isoformat(),
        })
        print(name, len(data))
    (ROOT / 'mongodb-asset-provenance.json').write_text(
        json.dumps(provenance, indent=2) + '\n')


if __name__ == '__main__':
    main()
