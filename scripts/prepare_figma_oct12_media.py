"""Preserve exact publicly embedded Vimeo thumbnails and losslessly remux media.

Player documents were read once at their actual observed iframe URLs. Signed
transport/configuration details stay in private files and are never published.
No authentication, bypass token, guessed URL, transcoding or failed-URL retry.
"""
import concurrent.futures
import hashlib
import json
import re
import subprocess
import urllib.parse
import urllib.request
from pathlib import Path

work = Path('.stitch-work/current-official')
records = json.loads((work / 'figma-oct12-vimeo-configs.private.json').read_text())

def get(url):
    request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.figma.com/'})
    with urllib.request.urlopen(request, timeout=45) as response:
        return response.read()

def preserve(record):
    config = record['config']
    video = config['video']
    result = {'vimeo_src': record['vimeo_src'], 'video_id': video['id'], 'title': video['title'],
              'official_embed_permission': video['embed_permission'], 'duration': video['duration'],
              'player_document_sha256': record['sha256'], 'accepted': False}
    try:
        thumbnail_url = video['thumbnail_url']
        data = get(thumbnail_url)
        filename = f'figma-assets/vimeo-{video["id"]}-thumbnail.jpg'
        (work / filename).write_bytes(data)
        result['thumbnail'] = {'source_url': thumbnail_url, 'path': filename, 'bytes': len(data),
                               'sha256': hashlib.sha256(data).hexdigest(), 'method': 'unchanged public embed thumbnail'}
    except Exception as error:
        result['thumbnail_error'] = str(error)
    try:
        hls = config['request']['files']['hls']
        master_url = hls['cdns'][hls['default_cdn']]['url']
        master = get(master_url).decode()
        variants = []
        lines = master.splitlines()
        for i, line in enumerate(lines):
            if line.startswith('#EXT-X-STREAM-INF:'):
                match = re.search(r'RESOLUTION=(\d+)x(\d+)', line)
                if match:
                    variants.append((int(match[2]), int(match[1]), urllib.parse.urljoin(master_url, lines[i + 1])))
        if not variants:
            raise ValueError('No actually listed HLS resolution')
        eligible = [v for v in variants if v[0] >= 720]
        height, width, variant_url = min(eligible) if eligible else max(variants)
        filename = f'figma-assets/vimeo-{video["id"]}-{height}p.mp4'
        command = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-nostdin', '-y',
                   '-headers', 'Referer: https://www.figma.com/\r\n', '-i', variant_url,
                   '-map', '0:v:0', '-an', '-c', 'copy', '-movflags', '+faststart', str(work / filename)]
        completed = subprocess.run(command, capture_output=True, timeout=120)
        (work / f'figma-oct12-vimeo-{video["id"]}-transfer.private.log').write_bytes(completed.stderr)
        if completed.returncode:
            raise ValueError(f'Public HLS remux failed with exit {completed.returncode}; no retry')
        data = (work / filename).read_bytes()
        result['media'] = {'source_url': record['vimeo_src'], 'path': filename, 'bytes': len(data),
                           'sha256': hashlib.sha256(data).hexdigest(), 'dimensions': [width, height],
                           'method': 'lossless video-only container remux of actually listed public HLS variant; not unchanged container bytes',
                           'master_playlist_sha256': hashlib.sha256(master.encode()).hexdigest()}
    except Exception as error:
        result['media_error'] = str(error)
    print(json.dumps({'video_id': video['id'], 'thumbnail': 'thumbnail' in result,
                      'media_bytes': result.get('media', {}).get('bytes'),
                      'errors': {k: v for k, v in result.items() if k.endswith('_error')}}), flush=True)
    return result

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    results = list(executor.map(preserve, records))
(work / 'figma-oct12-public-embedded-media.json').write_text(json.dumps({
    'accepted': False, 'method': 'Observed public embeds only; failed transfers are not retried.',
    'records': results}, indent=2) + '\n')
