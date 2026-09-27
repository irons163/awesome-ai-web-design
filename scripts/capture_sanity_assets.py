#!/usr/bin/env python3
"""Capture the public assets used by a dated Sanity homepage snapshot."""

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
SOURCE = ROOT / 'sanity-source-current.html'
ASSETS = ROOT / 'sanity-assets'
PROVENANCE = ROOT / 'sanity-asset-provenance.json'
FAILURES = ROOT / 'sanity-asset-failures.json'
BASE = 'https://www.sanity.io/'
HOSTS = {'www.sanity.io', 'cdn.sanity.io', 'image.mux.com'}
SUFFIXES = {'.css', '.jpg', '.jpeg', '.png', '.webp', '.gif', '.svg',
            '.woff', '.woff2', '.ttf', '.avif', '.webm'}
MAX_BYTES = 30 * 1024 * 1024
LOCAL_VIDEO_NAMES = {
    'bdd4149e4a4ac0e5d4c52086ba1530cd7236c0de.webm',  # 1200px+
    '0e593dcaf9a76d16011724741f0ec4b3482b9996.webm',  # phone
}


def public_asset(value: str, base: str = BASE) -> str | None:
    value = unescape(value.strip().strip('"\''))
    if not value or value.startswith(('data:', '#')):
        return None
    url = urljoin(base, value)
    parsed = urlparse(url)
    if parsed.scheme != 'https' or parsed.netloc not in HOSTS:
        return None
    suffix = Path(parsed.path).suffix.lower()
    if suffix not in SUFFIXES:
        return None
    if suffix == '.webm' and Path(parsed.path).name not in LOCAL_VIDEO_NAMES:
        return None
    return url


class SourceAssets(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.urls: set[str] = set()

    def add(self, value: str) -> None:
        url = public_asset(value)
        if url:
            self.urls.add(url)

    def handle_starttag(self, tag: str,
                        attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        if tag in ('img', 'source', 'video'):
            for key in ('src', 'poster', 'data-src', 'data-poster-url'):
                if attr.get(key):
                    self.add(attr[key])
            for key in ('srcset', 'data-srcset'):
                if attr.get(key):
                    for candidate in attr[key].split(','):
                        self.add(candidate.strip().split()[0])
        if tag == 'link' and attr.get('rel') in (
            'stylesheet', 'shortcut icon', 'icon', 'apple-touch-icon',
            'preload', 'modulepreload'
        ) and attr.get('href'):
            self.add(attr['href'])
        if attr.get('style'):
            for value in re.findall(r'url\(\s*([^)]+)\s*\)', attr['style']):
                self.add(value)


def local_path(url: str) -> Path:
    parsed = urlparse(url)
    digest = hashlib.sha256(url.encode()).hexdigest()[:20]
    return Path(parsed.netloc) / (digest + Path(parsed.path).suffix.lower())


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
    source = SOURCE.read_text()
    parser.feed(source)
    urls = set(parser.urls)
    # Include image and font URLs embedded in Astro metadata or inline styles.
    for value in re.findall(r'https://(?:cdn\.sanity\.io|image\.mux\.com)/[^\s"\'<>)]*',
                            source):
        url = public_asset(value.rstrip(',;'))
        if url:
            urls.add(url)
    captured: list[dict] = []
    failures: list[dict] = []
    for url in sorted(x for x in urls if urlparse(x).path.endswith('.css')):
        try:
            item = capture(url)
            captured.append(item)
            css = (ASSETS / item['path']).read_text(errors='replace')
            for value in re.findall(r'url\(\s*([^)]+)\s*\)', css):
                nested = public_asset(value, url)
                if nested:
                    urls.add(nested)
        except Exception as error:
            failures.append({'url': url, 'error': str(error)})
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
    print(f'Saved {len(captured)} Sanity public assets; '
          f'{len(failures)} failures; '
          f'{sum(item["bytes"] for item in captured) / (1024 * 1024):.1f} MiB')
    for item in failures:
        print(item['url'], item['error'][:150])


if __name__ == '__main__':
    main()
