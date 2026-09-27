#!/usr/bin/env python3
"""Save public Zapier media used by a dated official-homepage study."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import parse_qs, urljoin, urlparse
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1] / '.stitch-work' / 'current-official'
SOURCE = ROOT / 'zapier-source-current.html'
ASSETS = ROOT / 'zapier-assets'
PROVENANCE = ROOT / 'zapier-asset-provenance.json'
FAILURES = ROOT / 'zapier-asset-failures.json'
BASE = 'https://zapier.com/'
EXTENSIONS = {'.css', '.png', '.jpg', '.jpeg', '.webp', '.svg',
              '.woff', '.woff2', '.mp4', '.webm', '.avif', '.gif'}
HOSTS = {'marketing-site.vercel.zapier.com', 'images.ctfassets.net',
         'res.cloudinary.com', 'zapier.com'}


def official_asset(value: str, base: str = BASE) -> str | None:
    value = html.unescape(value.strip().strip("\"'"))
    if not value or value.startswith(('data:', '#')):
        return None
    url = urljoin(base, value)
    parsed = urlparse(url)
    if parsed.scheme != 'https' or parsed.netloc not in HOSTS:
        return None
    if parsed.netloc == 'zapier.com' and parsed.path == '/_next/image':
        origin = parse_qs(parsed.query).get('url', [''])[0]
        return official_asset(origin) if origin else None
    if parsed.netloc == 'zapier.com' and not parsed.path.startswith(
            ('/images/', '/fonts/', '/static/')):
        return None
    if parsed.netloc == 'res.cloudinary.com' and not parsed.path.startswith('/zapier-media/'):
        return None
    if Path(parsed.path).suffix.lower() not in EXTENSIONS:
        return None
    return url


def source_urls(markup: str) -> set[str]:
    result = set()
    for attribute, value in re.findall(
            r'\b(src|srcset|poster|href)="([^"]+)"', markup, re.I):
        values = value.split(',') if attribute.lower() == 'srcset' else [value]
        for item in values:
            url = official_asset(item.split()[0])
            if url:
                result.add(url)
    return result


def css_urls(stylesheet: str, css_url: str) -> set[str]:
    result = set()
    for item in re.findall(r'url\(\s*([^)]+)\s*\)', stylesheet, re.I):
        url = official_asset(item, css_url)
        if url:
            result.add(url)
    return result


def output_name(url: str) -> str:
    digest = hashlib.sha256(url.encode()).hexdigest()[:10]
    return digest + '-' + Path(urlparse(url).path).name


def capture(url: str, browser_copy: Path | None) -> dict:
    name = output_name(url)
    destination = ASSETS / name
    if browser_copy and browser_copy.is_file():
        data = browser_copy.read_bytes()
        method = 'browser_page_assets'
    else:
        request = Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                          'AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        })
        with urlopen(request, timeout=90) as response:
            data = response.read()
        method = 'official_direct_download'
    if not data:
        raise ValueError('empty asset')
    destination.write_bytes(data)
    return {'url': url, 'name': name, 'sha256': hashlib.sha256(data).hexdigest(),
            'bytes': len(data), 'capture_method': method}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--browser-manifest', type=Path)
    args = parser.parse_args()
    ASSETS.mkdir(exist_ok=True)
    bundled = {}
    if args.browser_manifest:
        manifest = json.loads(args.browser_manifest.read_text())
        bundled = {asset['url']: Path(asset['path'])
                   for asset in manifest['assets']
                   if official_asset(asset['url']) == asset['url']}

    urls = source_urls(SOURCE.read_text())
    urls.update(bundled)
    stylesheets = sorted(url for url in urls if urlparse(url).path.endswith('.css'))
    results, failures = [], []
    for url in stylesheets:
        try:
            item = capture(url, bundled.get(url))
            results.append(item)
            urls.update(css_urls((ASSETS / item['name']).read_text(errors='replace'), url))
        except Exception as error:
            failures.append({'url': url, 'error': str(error)})

    done = {item['url'] for item in results}
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = {pool.submit(capture, url, bundled.get(url)): url
                   for url in sorted(urls - done)}
        for future in as_completed(futures):
            url = futures[future]
            try:
                results.append(future.result())
            except Exception as error:
                failures.append({'url': url, 'error': str(error)})

    results.sort(key=lambda asset: asset['url'])
    failures.sort(key=lambda failure: failure['url'])
    PROVENANCE.write_text(json.dumps(results, indent=2) + '\n')
    FAILURES.write_text(json.dumps(failures, indent=2) + '\n')
    print(f'Saved {len(results)} brand-hosted assets; {len(failures)} failures')
    for failure in failures:
        print(failure['url'], failure['error'][:140])


if __name__ == '__main__':
    main()
