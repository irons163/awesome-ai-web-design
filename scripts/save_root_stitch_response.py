"""Retain one completed real provider response and an explicit export list."""
import json
from pathlib import Path
import re
import sys

slug = sys.argv[1]
assert re.fullmatch(r'[a-z0-9.-]+', slug)
response = json.loads(sys.argv[2])
work = Path(__file__).resolve().parents[1] / '.stitch-work/current-official'
target = work / f'{slug}-oct10-stitch-response.json'
backup = work / f'{slug}-oct12-before-native.private.json'
if target.exists() and not backup.exists():
    backup.write_bytes(target.read_bytes())
target.write_text(json.dumps(response, ensure_ascii=False, indent=2) + '\n')
screens = [s for c in response['structuredContent']['outputComponents'] for s in c.get('design', {}).get('screens', [])]
downloads = []
for index, screen in enumerate(screens):
    for key, suffix in [('htmlCode', 'html'), ('screenshot', 'png')]:
        url = screen.get(key, {}).get('downloadUrl')
        if url:
            downloads.append({'url': url + ('=s0' if key == 'screenshot' and '=s0' not in url else ''), 'path': f'{slug}-oct10-stitch-raw-{index}.{suffix}'})
manifest = work / f'{slug}-oct12-export-downloads.private.json'
manifest.write_text(json.dumps(downloads, indent=2) + '\n')
print(json.dumps({'brand': slug, 'screens': len(screens), 'downloads': len(downloads), 'download_manifest': str(manifest)}))
