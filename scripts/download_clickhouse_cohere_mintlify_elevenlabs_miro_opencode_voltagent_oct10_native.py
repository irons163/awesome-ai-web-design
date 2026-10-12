"""Preserve every fresh provider HTML/screenshot export without alteration."""
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlsplit
from datetime import datetime, timezone
import hashlib
import json
import sys

WORK = Path(__file__).resolve().parents[1] / '.stitch-work/current-official'
allowed = {'clickhouse', 'cohere', 'mintlify', 'elevenlabs', 'miro', 'opencode.ai', 'voltagent', 'posthog'}
brands = sys.argv[1:] or sorted(allowed)
assert set(brands) <= allowed
for brand in brands:
    response_name = f'{brand}-oct10-stitch-current-correction-response.json'
    response_path = WORK / response_name
    if not response_path.exists():
        print(json.dumps({'brand': brand, 'response_pending': True}), flush=True)
        continue
    response = json.loads(response_path.read_text())
    structured = response.get('structuredContent')
    if not structured:
        for content in response.get('content', []):
            if content.get('type') == 'text':
                try: structured = json.loads(content['text']); break
                except (ValueError, TypeError): pass
    screens = [s for c in (structured or {}).get('outputComponents', [])
               for s in c.get('design', {}).get('screens', [])]
    manifest_name = f'{brand}-oct10-native-original-downloads.json'
    old = json.loads((WORK / manifest_name).read_text()) if (WORK / manifest_name).exists() else {}
    saved = []
    for index, screen in enumerate(screens):
        for kind, field, suffix in [('html', 'htmlCode', '.html'), ('screenshot', 'screenshot', '.png')]:
            export = screen.get(field, {})
            url = export.get('downloadUrl')
            if not url: continue
            if urlsplit(url).scheme != 'https' or urlsplit(url).hostname not in {
                'contribution.usercontent.google.com', 'lh3.googleusercontent.com'}:
                raise ValueError('Unexpected provider export origin')
            name = f'{brand}-oct10-stitch-current-{index}{suffix}'
            path = WORK / name
            previous = next((x for x in old.get('exports', []) if x['path'] == name and x['source_url'] == url), None)
            if previous and path.exists() and hashlib.sha256(path.read_bytes()).hexdigest() == previous['sha256']:
                saved.append(previous)
                continue
            with urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=60) as stream:
                data = stream.read()
                content_type = stream.headers.get('Content-Type')
                if stream.status != 200 or not data: raise ValueError('Empty/unavailable provider export')
            path.write_bytes(data)
            saved.append({'path': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
                          'source_url': url, 'response_file': response_name,
                          'provider_file_name': export.get('name'), 'provider_screen_name': screen.get('name'),
                          'kind': kind, 'content_type': content_type, 'downloaded_at': datetime.now(timezone.utc).isoformat(),
                          'original_bytes_unmodified': True})
    manifest = {'brand': brand, 'accepted': False, 'official_consistency_claim': False,
                'response': response_name, 'native_screens': [s.get('name') for s in screens],
                'exports': saved, 'note': 'These are original provider outputs, not browser proof or a claim of official consistency.'}
    (WORK / manifest_name).write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps({'brand': brand, 'native_screens': manifest['native_screens'],
                      'exports': [{k: v for k, v in item.items() if k in ['path', 'bytes', 'sha256']} for item in saved]}), flush=True)
