#!/usr/bin/env python3
"""Capture first-party assets referenced by a dated Sentry homepage snapshot."""

from __future__ import annotations

import hashlib
import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1] / '.stitch-work' / 'current-official'
SOURCE = ROOT / 'sentry-source-current.html'
ASSETS = ROOT / 'sentry-assets'
PROVENANCE = ROOT / 'sentry-asset-provenance.json'
FAILURES = ROOT / 'sentry-asset-failures.json'
BASE = 'https://sentry.io/welcome/'
SUFFIXES = {'.css', '.jpg', '.jpeg', '.png', '.webp', '.gif', '.svg',
            '.woff', '.woff2', '.otf', '.ttf', '.avif', '.ico'}
MAX_BYTES = 30 * 1024 * 1024


def public_asset(value: str, base: str = BASE) -> str | None:
    value = unescape(value.strip().strip('"\''))
    if not value or value.startswith(('data:', '#', 'blob:')):
        return None
    url = urljoin(base, value)
    parsed = urlparse(url)
    if parsed.scheme != 'https' or parsed.netloc != 'sentry.io':
        return None
    if parsed.path == '/_vercel/image':
        return url
    if Path(parsed.path).suffix.lower() not in SUFFIXES:
        return None
    return url


class SourceAssets(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.urls: set[str] = set()
        self.in_style = False

    def add(self, value: str, base: str = BASE) -> None:
        asset = public_asset(value, base)
        if asset:
            self.urls.add(asset)

    def handle_starttag(self, tag: str,
                        attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        if tag == 'style':
            self.in_style = True
        if tag in ('img', 'source', 'video'):
            for key in ('src', 'poster', 'data-src', 'data-poster'):
                if attr.get(key):
                    self.add(attr[key])
            for key in ('srcset', 'data-srcset'):
                if attr.get(key):
                    for candidate in attr[key].split(','):
                        self.add(candidate.strip().split()[0])
        if tag == 'link' and attr.get('rel') in (
                'stylesheet', 'icon', 'preload', 'apple-touch-icon'):
            if attr.get('href'):
                self.add(attr['href'])
        if attr.get('style'):
            self.add_css(attr['style'])

    def handle_endtag(self, tag: str) -> None:
        if tag == 'style':
            self.in_style = False

    def handle_data(self, data: str) -> None:
        if self.in_style:
            self.add_css(data)

    def add_css(self, css: str, base: str = BASE) -> None:
        for value in re.findall(r'url\(\s*([^)]+)\s*\)', css):
            self.add(value, base)


def local_path(url: str) -> Path:
    parsed = urlparse(url)
    suffix = ('.webp' if parsed.path == '/_vercel/image'
              else Path(parsed.path).suffix.lower())
    digest = hashlib.sha256(url.encode()).hexdigest()[:20]
    return Path(parsed.netloc) / (digest + suffix)


def capture(url: str) -> dict:
    relative = local_path(url)
    destination = ASSETS / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    request = Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                      'AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': BASE,
    })
    with urlopen(request, timeout=90) as response:
        content_type = response.headers.get('Content-Type', '')
        final_url = response.url
        if content_type.startswith('text/html'):
            raise ValueError('Unexpected HTML response')
        data = response.read(MAX_BYTES + 1)
    if not data or len(data) > MAX_BYTES:
        raise ValueError('Empty or oversized asset')
    destination.write_bytes(data)
    return {
        'url': url,
        'path': relative.as_posix(),
        'sha256': hashlib.sha256(data).hexdigest(),
        'bytes': len(data),
        'content_type': content_type,
        'final_url': final_url,
        'capture_method': 'public_website_asset_download',
    }


def main() -> None:
    parser = SourceAssets()
    parser.feed(SOURCE.read_text())
    urls = set(parser.urls)
    captured: list[dict] = []
    failures: list[dict] = []
    for url in sorted(x for x in urls if urlparse(x).path.endswith('.css')):
        try:
            item = capture(url)
            captured.append(item)
            parser.add_css((ASSETS / item['path']).read_text(errors='replace'), url)
        except Exception as error:
            failures.append({'url': url, 'error': str(error)})
    urls.update(parser.urls)
    done = {item['url'] for item in captured}
    with ThreadPoolExecutor(max_workers=12) as pool:
        futures = {pool.submit(capture, url): url for url in sorted(urls - done)}
        for future in as_completed(futures):
            url = futures[future]
            try:
                captured.append(future.result())
            except Exception as error:
                failures.append({'url': url, 'error': str(error)})
    captured.sort(key=lambda item: item['url'])
    failures.sort(key=lambda item: item['url'])
    PROVENANCE.write_text(json.dumps(captured, indent=2) + '\n')
    FAILURES.write_text(json.dumps(failures, indent=2) + '\n')
    print(f'Saved {len(captured)} Sentry public assets; '
          f'{len(failures)} failures; '
          f'{sum(item["bytes"] for item in captured) / (1024 * 1024):.1f} MiB')
    for item in failures:
        print(item['url'], item['error'][:150])


if __name__ == '__main__':
    main()
