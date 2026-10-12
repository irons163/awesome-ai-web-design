"""Preserve public pageAssets bytes with provenance, excluding tracking resources."""
import concurrent.futures
import hashlib
import json
import re
import shutil
import sys
import urllib.request
from pathlib import Path
from urllib.parse import urlsplit

slug = sys.argv[1]
work = Path('.stitch-work/current-official')
bundle = json.loads((work / f'{slug}-oct10-asset-bundle.json').read_text())
target = work / f'{slug}-assets' / 'oct10'
target.mkdir(parents=True, exist_ok=True)
tracking = re.compile(r'google-analytics\.com|analytics\.google\.com|analytics00\.meride\.tv|tr\.line\.me/tag\.gif|doubleclick|googlead|/pagead/|/collect(?:[/?]|$)|tags\.srv\.|ads\.linkedin|adsct|/pixel|segment\.com|bat\.bing\.com/action|facebook\.com/tr(?:[/?]|$)|connect\.facebook\.net|googletagmanager\.com', re.I)

def extension(data, content_type, url):
    if data.startswith(b'RIFF') and data[8:12] == b'WEBP': return '.webp'
    if data.startswith(b'\x89PNG'): return '.png'
    if data.startswith(b'\xff\xd8'): return '.jpg'
    if data.startswith(b'wOF2'): return '.woff2'
    if b'<svg' in data[:1000]: return '.svg'
    if data[4:8] == b'ftyp': return '.avif' if b'avif' in data[:32] else '.mp4'
    return { 'text/css': '.css', 'font/woff': '.woff', 'font/ttf': '.ttf' }.get(content_type.split(';')[0], Path(urlsplit(url).path).suffix or '.bin')

def preserve(a):
    url = a['url']
    if tracking.search(url): return None
    if 'path' in a:
        data = Path(a['path']).read_bytes()
        content_type = a.get('contentType') or ''
        method = 'pageAssets original bytes'
    else:
        request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'image/webp,image/avif,image/*,*/*;q=0.8'})
        with urllib.request.urlopen(request, timeout=45) as response:
            data = response.read()
            content_type = response.headers.get('Content-Type', '')
        method = 'Unauthenticated HTTPS GET of exactly observed public asset URL after pageAssets CORS failure'
    digest = hashlib.sha256(data).hexdigest()
    output = target / (digest[:20] + extension(data, content_type, url))
    output.write_bytes(data)
    return {'source_url': url, 'path': str(output.relative_to(work)), 'bytes': len(data), 'sha256': digest, 'contentType': content_type, 'acquisition': method}

items = {a['url']: a for a in bundle['assets'] + bundle['failures'] if not tracking.search(a['url'])}
for width in (1280, 390):
    reference = json.loads((work / f'{slug}-oct10-official-{width}-reference.json').read_text())
    observed = [image['src'] for image in reference['images']] + reference['stylesheets']
    for url in observed:
        if url.startswith('https://') and not tracking.search(url):
            items.setdefault(url, {'url': url})
assets, failures = [], []
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    futures = {pool.submit(preserve, a): a for a in items.values()}
    for future, asset in futures.items():
        try:
            result = future.result()
            if result: assets.append(result)
        except Exception as error:
            failures.append({'source_url': asset['url'], 'error': str(error)})
manifest = {'assets': sorted(assets, key=lambda a: a['source_url']), 'failures': failures, 'trackingExcluded': True}
(work / f'{slug}-oct10-assets.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(json.dumps({'slug': slug, 'assets': len(assets), 'bytes': sum(a['bytes'] for a in assets), 'failures': failures}, indent=2))
