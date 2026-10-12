"""Preserve exact observed public demo/poster bytes; no service/account action."""
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlsplit
from datetime import datetime, timezone
import hashlib
import json

WORK = Path(__file__).resolve().parents[1] / '.stitch-work/current-official'
brand = 'opencode.ai'
name = f'{brand}-oct10-assets.json'
manifest = json.loads((WORK / name).read_text())
known = {a['source_url'] for a in manifest['assets']}
observed = set()
for width in [1280, 390]:
    phases = json.loads((WORK / f'{brand}-oct10-official-{width}-phases.json').read_text())
    for phase in phases:
        for media in phase.get('visibleMedia', []):
            if media.get('tag') == 'VIDEO':
                observed.update(media[k] for k in ['src', 'poster'] if media.get(k))
records = []
for url in sorted(observed):
    assert urlsplit(url).scheme == 'https' and urlsplit(url).hostname == 'opencode.ai'
    if url in known:
        continue
    try:
        with urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=60) as response:
            data = response.read()
            content_type = response.headers.get('Content-Type', '')
            assert response.status == 200 and data
        suffix = '.png' if data.startswith(b'\x89PNG') else '.mp4' if data[4:8] == b'ftyp' else None
        assert suffix, 'Unexpected observed-media format'
        sha = hashlib.sha256(data).hexdigest()
        path = f'{brand}-assets/oct10/{sha[:20]}{suffix}'
        (WORK / path).write_bytes(data)
        item = {'source_url': url, 'path': path, 'bytes': len(data), 'sha256': sha,
                'contentType': content_type,
                'acquisition': 'Unauthenticated HTTPS GET of exact public video/poster URL observed in actual browser phases',
                'downloaded_at': datetime.now(timezone.utc).isoformat()}
        manifest['assets'].append(item)
        records.append(item)
    except Exception as error:
        item = {'source_url': url, 'error': str(error)}
        manifest['failures'].append(item)
        records.append(item)
manifest['assets'].sort(key=lambda a: a['source_url'])
(WORK / name).write_text(json.dumps(manifest, indent=2) + '\n')
(WORK / f'{brand}-oct10-observed-video-provenance.json').write_text(json.dumps({
    'brand': brand, 'accepted': False, 'records': records,
    'scope': 'Original observed media bytes only. Playback, timing and demo interactions remain unverified.'
}, indent=2) + '\n')
print(json.dumps({'brand': brand, 'saved': len([a for a in records if 'path' in a]),
                  'failures': [a for a in records if 'error' in a]}))
