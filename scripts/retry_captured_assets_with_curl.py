"""Retry observed public asset timeouts over ordinary HTTPS; never retry denials."""
import concurrent.futures
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlsplit

slug = sys.argv[1]
timeout_seconds = sys.argv[2] if len(sys.argv) > 2 else '30'
work = Path(__file__).resolve().parents[1] / '.stitch-work/current-official'
path = work / f'{slug}-oct10-assets.json'
manifest = json.loads(path.read_text())
known = {x['source_url'] for x in manifest['assets']}
denied = {x['source_url'] for x in manifest['failures'] if re.search(r'\b(?:403|404|429)\b', x['error'])}
tracking = re.compile(r'google-analytics\.com|analytics\.google\.com|tr\.line\.me/tag\.gif|doubleclick|googlead|/pagead/|/collect(?:[/?]|$)|tags\.srv\.|ads\.linkedin|adsct|/pixel|segment\.com|bat\.bing\.com/action|facebook\.com/tr(?:[/?]|$)|connect\.facebook\.net|googletagmanager\.com', re.I)
urls = {x['source_url'] for x in manifest['failures']} - denied
for width in (1280, 390):
    reference = json.loads((work / f'{slug}-oct10-official-{width}-reference.json').read_text())
    urls.update(x['src'] for x in reference['images'])
    urls.update(reference['stylesheets'])
    phases_path = work / f'{slug}-oct10-official-{width}-phases.json'
    if phases_path.exists():
        for phase in json.loads(phases_path.read_text()):
            for media in phase.get('visibleMedia', []):
                if media.get('tag') == 'VIDEO':
                    urls.update(value for value in (media.get('src'), media.get('poster')) if value)
urls = sorted(url for url in urls if url.startswith('https://') and url not in known | denied and not tracking.search(url))

def acquire(url):
    with tempfile.TemporaryDirectory() as temp:
        dest = Path(temp) / 'asset'
        run = subprocess.run(['curl', '--silent', '--show-error', '--fail', '--location', '--max-time', timeout_seconds,
                              '--output', str(dest), '--write-out', '%{http_code}\n%{content_type}', url], capture_output=True, text=True)
        status, _, content_type = run.stdout.partition('\n')
        if run.returncode:
            return {'source_url': url, 'error': f'Ordinary HTTPS curl exit{run.returncode}, HTTP{status or "unavailable"}'}
        data = dest.read_bytes()
        if data.startswith(b'RIFF') and data[8:12] == b'WEBP': ext = '.webp'
        elif data.startswith(b'\x89PNG'): ext = '.png'
        elif data.startswith(b'\xff\xd8'): ext = '.jpg'
        elif data.startswith(b'wOF2'): ext = '.woff2'
        elif data.startswith(b'wOFF'): ext = '.woff'
        elif b'<svg' in data[:1000]: ext = '.svg'
        elif data[4:8] == b'ftyp': ext = '.avif' if b'avif' in data[:32] else '.mp4'
        else: ext = '.css' if content_type.startswith('text/css') else Path(urlsplit(url).path).suffix or '.bin'
        digest = hashlib.sha256(data).hexdigest()
        relative = f'{slug}-assets/oct10/{digest[:20]}{ext}'
        (work / relative).write_bytes(data)
        return {'source_url': url, 'path': relative, 'bytes': len(data), 'sha256': digest, 'contentType': content_type,
                'acquisition': 'Ordinary unauthenticated HTTPS curl of exactly observed public asset URL after transfer timeout or newly settled source media; no denial bypass.'}

recovered, failures = [], [x for x in manifest['failures'] if x['source_url'] in denied]
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    for result in pool.map(acquire, urls):
        (recovered if 'path' in result else failures).append(result)
manifest.setdefault('previous_transfer_failures', []).extend(manifest['failures'])
manifest['assets'].extend(recovered)
manifest['assets'].sort(key=lambda x: x['source_url'])
manifest['failures'] = failures
path.write_text(json.dumps(manifest, indent=2) + '\n')
print(json.dumps({'slug': slug, 'recovered': len(recovered), 'assets': len(manifest['assets']),
                  'bytes': sum(x['bytes'] for x in manifest['assets']), 'remaining_failures': len(failures)}))
