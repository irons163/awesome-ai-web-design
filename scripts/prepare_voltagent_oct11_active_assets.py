"""Preserve only newly observed exact image URLs; do not retry known404."""
from pathlib import Path
import concurrent.futures
import hashlib
import json
import urllib.request

work = Path('.stitch-work/current-official')
target = work / 'voltagent-assets/oct10'
manifest_path = work / 'voltagent-oct10-assets.json'
manifest = json.loads(manifest_path.read_text())
known = {asset['source_url'] for asset in manifest['assets'] + manifest['failures']}
urls = {image['src'] for width in [1280, 390]
        for image in json.loads((work / f'voltagent-oct11-testimonials-active-{width}-reference.json').read_text())['images']}

def preserve(url):
    assert url.startswith(('https://cdn.voltagent.dev/', 'https://img.youtube.com/'))
    with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=40) as response:
        data, content_type = response.read(), response.headers.get('Content-Type', '')
    digest = hashlib.sha256(data).hexdigest()
    suffix = '.png' if data.startswith(b'\x89PNG') else '.jpg' if data.startswith(b'\xff\xd8') else '.webp' if data.startswith(b'RIFF') else None
    assert suffix, 'Unexpected original image bytes'
    relative = 'voltagent-assets/oct10/' + digest[:20] + suffix
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
(work / 'voltagent-oct11-active-additional-assets.json').write_text(json.dumps({'added': added, 'new_failures': failures,
    'known_failure_not_retried': 'https://pbs.twimg.com/profile_images/2088056226089160704/DgHVP6vH_normal.jpg'}, indent=2) + '\n')
print(json.dumps({'added': len(added), 'new_failures': failures, 'total_assets': len(manifest['assets'])}))
