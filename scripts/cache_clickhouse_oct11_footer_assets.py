"""Cache only exact public stylesheet URLs observed in the official form frame."""
import hashlib
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

work = Path(__file__).resolve().parents[1] / '.stitch-work/current-official'
target = work / 'clickhouse-oct10-assets.json'
manifest = json.loads(target.read_text())
frame = json.loads((work / 'clickhouse-oct11-footer-form-reference.json').read_text())
known = {item['source_url']: item for item in manifest['assets']}
denied = {item['source_url'] for item in manifest.get('failures', [])
          if re.search(r'\b(?:403|404|429)\b', item.get('error', ''))}
# The optional form CSS returned HTTP 403. Do not retry it or request another
# version. Inspect only the already-preserved Inter font stylesheet and its
# explicitly declared independent font URLs.
queue = [url for url in frame['styles'] if url in known]
added = []
for url in queue:
    if url in denied:
        raise RuntimeError('An observed endpoint denial must not be retried')
    if url in known:
        item = known[url]
        data = (work / item['path']).read_bytes()
    else:
        with urllib.request.urlopen(url, timeout=40) as response:
            data = response.read()
            mime = response.headers.get_content_type()
        suffix = Path(urllib.parse.urlsplit(url).path).suffix
        if not re.fullmatch(r'\.[a-z0-9]{1,8}', suffix):
            raise RuntimeError('Unexpected asset extension')
        relative = 'clickhouse-assets/oct11/' + hashlib.sha256(url.encode()).hexdigest()[:20] + suffix
        path = work / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        item = {'source_url': url, 'path': relative, 'bytes': len(data),
                'sha256': hashlib.sha256(data).hexdigest(), 'mime_type': mime,
                'provenance': 'Exact observed official footer iframe stylesheet or its declared asset URL.'}
        manifest['assets'].append(item)
        known[url] = item
        added.append(item)
    if urllib.parse.urlsplit(url).path.endswith('.css'):
        for match in re.finditer(r'url\(\s*[\'"]?([^\)\'\"]+)', data.decode('utf-8')):
            value = match.group(1).strip()
            if value.startswith(('data:', '#')):
                continue
            dependency = urllib.parse.urljoin(url, value)
            if dependency not in queue:
                queue.append(dependency)
target.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')
(work / 'clickhouse-oct11-footer-asset-downloads.json').write_text(
    json.dumps({'assets': added, 'observed_frame': 'clickhouse-oct11-footer-form-reference.json'}, indent=2) + '\n')
print(json.dumps({'added_assets': len(added), 'added_bytes': sum(a['bytes'] for a in added)}))
