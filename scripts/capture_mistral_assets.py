#!/usr/bin/env python3
"""Capture public assets referenced by a dated Mistral homepage snapshot."""

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
SOURCE = ROOT / 'mistral.ai-source-current.html'
ASSETS = ROOT / 'mistral.ai-assets'
PROVENANCE = ROOT / 'mistral.ai-asset-provenance.json'
FAILURES = ROOT / 'mistral.ai-asset-failures.json'
BASE = 'https://mistral.ai/'
PREFIXES = ('/_astro/', '/cms-media/', '/fonts/', '/images/')
SUFFIXES = {'.css', '.webp', '.svg', '.png', '.jpg', '.jpeg', '.gif',
            '.avif', '.woff', '.woff2', '.ttf', '.mp4', '.webm'}


def normalized_url(value: str, base: str = BASE) -> str | None:
    value = unescape(value.strip().strip('"\''))
    if not value or value.startswith(('data:', '#')):
        return None
    url = urljoin(base, value)
    parsed = urlparse(url)
    if parsed.scheme != 'https' or parsed.netloc != 'mistral.ai':
        return None
    if not parsed.path.startswith(PREFIXES):
        return None
    if Path(parsed.path).suffix.lower() not in SUFFIXES:
        return None
    return url


class SourceAssets(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.urls: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        values = []
        if tag in ('img', 'source', 'video'):
            values.extend(attr.get(key) for key in ('src', 'poster') if attr.get(key))
            if attr.get('srcset'):
                values.extend(item.strip().split()[0]
                              for item in attr['srcset'].split(','))
        if tag == 'link' and attr.get('rel') in ('stylesheet', 'icon', 'preload'):
            values.append(attr.get('href'))
        if attr.get('style'):
            values.extend(re.findall(r'url\(\s*([^)]+)\s*\)', attr['style']))
        for value in values:
            url = normalized_url(value)
            if url:
                self.urls.add(url)


def capture(url: str) -> dict:
    parsed = urlparse(url)
    relative = Path(parsed.path.lstrip('/'))
    destination = ASSETS / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    request = Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                      'AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': BASE,
    })
    with urlopen(request, timeout=90) as response:
        data = response.read()
        content_type = response.headers.get('Content-Type', '')
    if not data or content_type.startswith('text/html'):
        raise ValueError(f'Unexpected response {content_type!r}')
    destination.write_bytes(data)
    return {'url': url, 'path': relative.as_posix(),
            'sha256': hashlib.sha256(data).hexdigest(),
            'bytes': len(data), 'content_type': content_type,
            'capture_method': 'official_direct_download'}


def main() -> None:
    parser = SourceAssets()
    parser.feed(SOURCE.read_text())
    urls = set(parser.urls)
    captured: list[dict] = []
    failures: list[dict] = []
    css_urls = sorted(url for url in urls if urlparse(url).path.endswith('.css'))
    for url in css_urls:
        try:
            item = capture(url)
            captured.append(item)
            css = (ASSETS / item['path']).read_text(errors='replace')
            for value in re.findall(r'url\(\s*([^)]+)\s*\)', css):
                asset_url = normalized_url(value, url)
                if asset_url:
                    urls.add(asset_url)
        except Exception as error:
            failures.append({'url': url, 'error': str(error)})
    done = {item['url'] for item in captured}
    with ThreadPoolExecutor(max_workers=10) as pool:
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
    print(f'Saved {len(captured)} Mistral assets; {len(failures)} failures')
    for item in failures:
        print(item['url'], item['error'][:160])


if __name__ == '__main__':
    main()
