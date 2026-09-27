#!/usr/bin/env python3
"""Capture public media and fonts used by a dated Replicate homepage."""

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
SOURCE = ROOT / 'replicate-source-current.html'
ASSETS = ROOT / 'replicate-assets'
PROVENANCE = ROOT / 'replicate-asset-provenance.json'
FAILURES = ROOT / 'replicate-asset-failures.json'
BASE = 'https://replicate.com/'
HOSTS = {'static.replicateassets.com', 'fonts.replicateassets.com',
         'tjzk.replicate.delivery', 'replicate.delivery', 'github.com'}
SUFFIXES = {'.css', '.jpg', '.jpeg', '.png', '.webp', '.gif', '.svg',
            '.woff', '.woff2', '.ttf', '.mp4', '.webm', '.avif'}


def official_asset(value: str, base: str = BASE) -> str | None:
    value = unescape(value.strip().strip('"\''))
    if not value or value.startswith(('data:', '#')):
        return None
    url = urljoin(base, value)
    parsed = urlparse(url)
    if parsed.scheme != 'https' or parsed.netloc not in HOSTS:
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
        if tag == 'link' and attr.get('rel') in ('stylesheet', 'preload', 'icon'):
            values.append(attr.get('href'))
        if attr.get('style'):
            values.extend(re.findall(r'url\(\s*([^)]+)\s*\)', attr['style']))
        for value in values:
            url = official_asset(value)
            if url:
                self.urls.add(url)


def local_path(url: str) -> Path:
    parsed = urlparse(url)
    path = Path(parsed.netloc) / parsed.path.lstrip('/')
    if parsed.query:
        digest = hashlib.sha256(parsed.query.encode()).hexdigest()[:8]
        path = path.with_name(path.stem + '-' + digest + path.suffix)
    return path


def capture(url: str) -> dict:
    path = local_path(url)
    destination = ASSETS / path
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
    return {'url': url, 'path': path.as_posix(),
            'sha256': hashlib.sha256(data).hexdigest(),
            'bytes': len(data), 'content_type': content_type,
            'capture_method': 'official_public_asset_download'}


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
            css = (ASSETS / item['path']).read_text(errors='replace')
            for value in re.findall(r'url\(\s*([^)]+)\s*\)', css):
                asset_url = official_asset(value, url)
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
    print(f'Saved {len(captured)} public Replicate assets; {len(failures)} failures')
    for item in failures:
        print(item['url'], item['error'][:150])


if __name__ == '__main__':
    main()
