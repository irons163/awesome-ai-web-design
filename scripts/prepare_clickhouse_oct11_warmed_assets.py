"""Preserve only newly observed exact image URLs; do not retry known404."""
from pathlib import Path
import concurrent.futures
import hashlib
import json
import urllib.request

work = Path('.stitch-work/current-official')
target = work / 'clickhouse-assets/oct10'
manifest_path = work / 'clickhouse-oct10-assets.json'
manifest = json.loads(manifest_path.read_text())
known = {asset['source_url'] for asset in manifest['assets'] + manifest['failures']}
references = [json.loads((work / f'clickhouse-oct10-official-{width}-reference.json').read_text()) for width in [1280,390]]
urls = {image['src'] for r in references for image in r['images']} | {url for r in references for url in r['stylesheets']}

def preserve(url):
    assert url.startswith(('https://clickhouse.com/',))
    with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=40) as response:
        data, content_type = response.read(), response.headers.get('Content-Type', '')
    digest = hashlib.sha256(data).hexdigest()
    suffix = '.png' if data.startswith(b'\x89PNG') else '.jpg' if data.startswith(b'\xff\xd8') else '.webp' if data.startswith(b'RIFF') else '.css' if 'text/css' in content_type else '.svg' if b'<svg' in data[:1000] else None
    assert suffix, 'Unexpected original image bytes'
    relative = 'clickhouse-assets/oct10/' + digest[:20] + suffix
    (work / relative).write_bytes(data)
    return {'source_url': url, 'path': relative, 'bytes': len(data), 'sha256': digest, 'contentType': content_type,
            'acquisition': 'Unauthenticated HTTPS GET of exactly observed current active testimonial image URL; no known failure retried.'}

added, failures = [], []
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
    futures = {pool.submit(preserve, url): url for url in sorted(urls - known)}
    for future, url in futures.items():
        try:
            added.append(future.result())
        except Exception as error:
            failures.append({'source_url': url, 'error': str(error)})
manifest['assets'].extend(added)
manifest['assets'].sort(key=lambda item: item['source_url'])
manifest['failures'].extend(failures)
manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')
(work / 'clickhouse-oct11-warmed-additional-assets.json').write_text(json.dumps({'added': added, 'new_failures': failures,
    'known_failure_not_retried': None}, indent=2) + '\n')
print(json.dumps({'added': len(added), 'new_failures': failures, 'total_assets': len(manifest['assets'])}))
