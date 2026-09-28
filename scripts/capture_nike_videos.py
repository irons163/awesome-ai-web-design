#!/usr/bin/env python3
"""Save the six short, public Nike Canada hero clips as browser-friendly MP4s."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import urllib.request
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / '.stitch-work' / 'current-official'
ASSETS = ROOT / 'nike-assets'
API = 'https://api.nike.com/content/asset_video_manifest/v1/'
VIDEOS = {
    'pegasus-desktop.mp4': ('0347f0f7-4392-41e0-8f02-a9aa2e19f95d', 960),
    'pegasus-mobile.mp4': ('09a98dd1-7955-4e29-b415-a98f82c3a382', 640),
    'caitlin-desktop.mp4': ('ec7bb7c8-1dfd-4278-af26-d61b6cc09a51', 960),
    'caitlin-mobile.mp4': ('e0d53538-19c9-4fe9-a908-02ecadcf752c', 640),
    'body-desktop.mp4': ('e429b88e-d6f6-435c-aa11-adaf46d00ab8', 960),
    'body-mobile.mp4': ('07a7a4fd-0926-405d-a978-b49e6f25e4ff', 640),
}


def main() -> None:
    records = []
    for filename, (video_id, preferred_width) in VIDEOS.items():
        manifest_url = API + video_id
        request = urllib.request.Request(manifest_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(request, timeout=40) as response:
            manifest = response.read().decode()
        matches = re.findall(r'RESOLUTION=(\d+)x(\d+)[^\n]*\n(https://assets\.nmp\.nike\.com/video/[^\n]+)', manifest)
        if not matches:
            raise RuntimeError(f'No official stream found for {filename}')
        width, height, stream_url = min(matches, key=lambda row: abs(int(row[0]) - preferred_width))
        target = ASSETS / filename
        subprocess.run([
            'ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
            '-i', stream_url, '-c:v', 'libx264', '-preset', 'medium', '-crf', '30',
            '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '64k',
            '-movflags', '+faststart', str(target),
        ], check=True, timeout=120)
        data = target.read_bytes()
        if not data:
            raise RuntimeError(f'Empty official video: {filename}')
        records.append({
            'path': 'nike-assets/' + filename,
            'manifest_url': manifest_url,
            'stream_url': stream_url,
            'width': int(width), 'height': int(height),
            'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
            'conversion': 'ffmpeg H.264/AAC encode, CRF 30, 64k audio, faststart for compact static hosting',
        })
    (ROOT / 'nike-video-provenance.json').write_text(json.dumps({
        'reference': 'https://www.nike.com/ca/',
        'captured_at': datetime.now().astimezone().isoformat(),
        'videos': records,
    }, indent=2) + '\n')
    print(json.dumps({'count': len(records), 'total_bytes': sum(x['bytes'] for x in records),
                      'videos': [(x['path'], x['bytes']) for x in records]}))


if __name__ == '__main__':
    main()
