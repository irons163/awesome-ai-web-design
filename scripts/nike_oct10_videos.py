from pathlib import Path
import json, re, hashlib, urllib.request, concurrent.futures, subprocess
from urllib.parse import urljoin

p = Path('.stitch-work/current-official')
folder = p / 'nike-assets/oct10/video-originals'
folder.mkdir(parents=True, exist_ok=True)
sha = lambda b: hashlib.sha256(b).hexdigest()
records = []
derived = []

def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=40) as r:
        return r.read()

for m in json.loads((p / 'nike-oct10-video-manifests.json').read_text()):
    text = (p / m['path']).read_text()
    entries = re.findall(r'RESOLUTION=(\d+)x(\d+)[^\n]*\n([^\n]+)', text)
    target = 1280 if max(int(x[0]) for x in entries) > 1000 else 576
    width, height, url = min(entries, key=lambda x: abs(int(x[0]) - target))
    playlist = get(url)
    playlist_path = folder / (sha(playlist)[:20] + '.m3u8')
    playlist_path.write_bytes(playlist)
    records.append({'source_url': url, 'path': str(playlist_path.relative_to(p)), 'bytes': len(playlist), 'sha256': sha(playlist), 'kind': 'original HLS playlist'})
    lines = playlist.decode().splitlines()
    urls = []
    for line in lines:
        if line.startswith('#EXT-X-MAP:'):
            urls.append(urljoin(url, re.search(r'URI="([^"]+)"', line)[1]))
        elif line and not line.startswith('#'):
            urls.append(urljoin(url, line))
    def save(u):
        b = get(u)
        f = folder / (sha(b)[:20] + Path(u).suffix)
        f.write_bytes(b)
        return u, f, b
    mapping = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for u, f, b in pool.map(save, dict.fromkeys(urls)):
            mapping[u] = f.name
            records.append({'source_url': u, 'path': str(f.relative_to(p)), 'bytes': len(b), 'sha256': sha(b), 'kind': 'original encoded video fragment'})
    localized = []
    for line in lines:
        if line.startswith('#EXT-X-MAP:'):
            old = re.search(r'URI="([^"]+)"', line)[1]
            line = line.replace(old, mapping[urljoin(url, old)])
        elif line and not line.startswith('#'):
            line = mapping[urljoin(url, line)]
        localized.append(line)
    local_playlist = folder / (m['source_url'].rsplit('/', 1)[1] + '-local.m3u8')
    local_playlist.write_text('\n'.join(localized) + '\n')
    video_id = m['source_url'].rsplit('/', 1)[1]
    output = p / ('nike-assets/oct10/' + video_id + '.mp4')
    subprocess.run(['/opt/homebrew/bin/ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-allowed_extensions', 'ALL', '-i', str(local_playlist), '-map', '0:v:0', '-c:v', 'copy', '-an', '-movflags', '+faststart', str(output)], check=True, timeout=60)
    b = output.read_bytes()
    derived.append({'video_id': video_id, 'source_manifest': m['source_url'], 'source_stream': url, 'width': int(width), 'height': int(height), 'path': str(output.relative_to(p)), 'bytes': len(b), 'sha256': sha(b), 'conversion': 'Container remux only with video stream copy; original encoded fragments retained separately. Muted ambient video, audio excluded.'})
    (p / 'nike-oct10-video-provenance.json').write_text(json.dumps({'originals': records, 'derived': derived}, indent=2) + '\n')
    print(video_id, len(b), flush=True)
