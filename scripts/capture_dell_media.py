#!/usr/bin/env python3
"""Retain observed public video bytes; never query the player API or stores."""
import hashlib
import json
import urllib.request
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / '.stitch-work/current-official'
DEST = WORK / 'dell-1996-assets'
REFERENCE = json.loads((WORK / 'dell-1996-interactions-browser-export.json').read_text())['media']


def main():
    rows, failures = [], []
    resources = REFERENCE['resources']
    # The observed 6-second background has two downloaded renditions. Keep
    # the 1280×720 path already played by the public page, not a guessed URL.
    selected = [r['url'] for r in resources if 'cf-images.' in r['url']]
    selected += [r['url'] for r in resources if 'ca31751e-979c-474f-b029-e7ca043acfba' in r['url'] and ('master.m3u8' in r['url'] or '28b570c9-292b-4d83-bef2-253cfcfbe6ae' in r['url'])]
    for url in dict.fromkeys(selected):
        host = urlsplit(url).hostname
        if host not in {'cf-images.us-east-1.prod.boltdns.net', 'manifest.prod.boltdns.net', 'fastly-signed-us-east-1-prod.brightcovecdn.com'}:
            raise ValueError('Unexpected observed resource host')
        suffix = Path(urlsplit(url).path).suffix
        if suffix not in {'.jpg', '.m3u8', '.ts'}:
            raise ValueError('Unexpected observed resource type')
        target = DEST / (hashlib.sha256(url.encode()).hexdigest()[:12] + suffix)
        try:
            with urllib.request.urlopen(url, timeout=20) as response:
                if response.status != 200:
                    raise ValueError('Unsuccessful public media response')
                content_type = response.headers.get_content_type()
                data = response.read()
            if suffix == '.jpg' and not data.startswith(b'\xff\xd8\xff'):
                raise ValueError('Invalid original JPEG signature')
            if suffix == '.m3u8' and not data.startswith(b'#EXTM3U'):
                raise ValueError('Invalid original HLS signature')
            if suffix == '.ts' and not (data[:1] == b'G' and data[188:189] == b'G'):
                raise ValueError('Invalid original MPEG-TS signature')
            target.write_bytes(data)
            rows.append({'source_url': url, 'path': str(target.relative_to(WORK)),
                         'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
                         'content_type': content_type, 'kind': 'image' if suffix == '.jpg' else 'video',
                         'method': 'Already observed public video/poster resource; ordinary unauthenticated HTTPS returned HTTP 200; original format signature checked.'})
        except Exception as error:
            failures.append({'url': url, 'reason': str(error)})
    segment = next((r for r in rows if r['path'].endswith('.ts')), None)
    rendition = next((r for r in rows if r['path'].endswith('.m3u8') and '/28b570c9-' in r['source_url']), None)
    local_manifest = None
    if segment and rendition:
        original = (WORK / rendition['path']).read_text()
        source_lines = [line for line in original.splitlines() if line and not line.startswith('#')]
        if len(source_lines) != 1:
            raise ValueError('The observed clip has more than one segment; no incomplete local playback.')
        local_manifest = 'dell-1996-assets/deloitte-background.m3u8'
        (WORK / local_manifest).write_text('\n'.join(Path(segment['path']).name if line in source_lines else line for line in original.splitlines()) + '\n')
    result = {'reference_url': REFERENCE['reference_url'], 'observed_at': REFERENCE['observed_at'],
              'assets': rows, 'failures': failures, 'local_background_manifest': local_manifest,
              'note': 'Native original manifests and MPEG-TS bytes stay unchanged. The separately named local playlist only points to the captured original segment. Public signed origins may expire; local background bytes do not require a player API token. The full 95-second popup video is not reproduced.'}
    (WORK / 'dell-1996-media-provenance.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'assets': len(rows), 'bytes': sum(r['bytes'] for r in rows), 'failures': len(failures), 'background': bool(local_manifest)}))


if __name__ == '__main__':
    main()
