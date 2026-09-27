#!/usr/bin/env python3
"""Save first-party assets for a dated Wise Canada homepage study."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1] / '.stitch-work' / 'current-official'
SOURCE = ROOT / 'wise-source-current.html'
ASSETS = ROOT / 'wise-assets'
PROVENANCE = ROOT / 'wise-asset-provenance.json'
FAILURES = ROOT / 'wise-asset-failures.json'
BASE = 'https://wise.com/'
EXTENSIONS = {'.css', '.png', '.jpg', '.jpeg', '.webp', '.svg',
              '.woff', '.woff2', '.mp4', '.webm', '.avif'}


def official_asset(value: str, base: str = BASE) -> str | None:
    value = html.unescape(value.strip().strip("\"'"))
    if not value or value.startswith(('data:', '#')):
        return None
    url = urljoin(base, value)
    parsed = urlparse(url)
    if parsed.scheme != 'https' or parsed.netloc != 'wise.com':
        return None
    if parsed.path.startswith('/visit/pixel'):
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
    parsed = urlparse(url)
    digest = hashlib.sha256(url.encode()).hexdigest()[:10]
    return digest + '-' + Path(parsed.path).name


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
            'Accept-Language': 'en-CA,en;q=0.9',
        })
        with urlopen(request, timeout=45) as response:
            data = response.read()
        method = 'official_direct_download'
    if not data:
        raise ValueError('empty asset')
    destination.write_bytes(data)
    return {
        'url': url,
        'name': name,
        'sha256': hashlib.sha256(data).hexdigest(),
        'bytes': len(data),
        'capture_method': method,
    }


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
                   if official_asset(asset['url'])}

    urls = source_urls(SOURCE.read_text())
    urls.update(bundled)
    # First capture the source CSS, then discover its font/image dependencies.
    stylesheets = sorted(url for url in urls if urlparse(url).path.endswith('.css'))
    results = []
    failures = []
    for url in stylesheets:
        try:
            item = capture(url, bundled.get(url))
            results.append(item)
            urls.update(css_urls((ASSETS / item['name']).read_text(errors='replace'), url))
        except Exception as error:
            failures.append({'url': url, 'error': str(error)})

    complete = set(stylesheets) - {item['url'] for item in failures}
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = {pool.submit(capture, url, bundled.get(url)): url
                   for url in sorted(urls - complete)}
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
    print(f'Saved {len(results)} official assets; {len(failures)} failures')
    for failure in failures:
        print(failure['url'], failure['error'][:140])


if __name__ == '__main__':
    main()
