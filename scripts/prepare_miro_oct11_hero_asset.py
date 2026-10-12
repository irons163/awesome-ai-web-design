"""Preserve only additional exact image URLs observed in the active hero."""
from pathlib import Path
import hashlib
import json
import urllib.request

work=Path('.stitch-work/current-official')
file=work/'miro-oct10-assets.json'
manifest=json.loads(file.read_text())
known={item['source_url'] for item in manifest['assets']+manifest.get('failures',[])}
urls={image['src'] for width in [1280,390]
      for image in json.loads((work/f'miro-oct11-active-hero-{width}-reference.json').read_text())['images']
      if image['src'].startswith('https://')}
added=[]
for url in sorted(urls-known):
    assert url.startswith('https://framerusercontent.com/images/'),url
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=40) as response:
        data=response.read(); content_type=response.headers.get('Content-Type','')
    assert b'<svg' in data[:2000] and 'svg' in content_type,content_type
    sha=hashlib.sha256(data).hexdigest()
    relative='miro-assets/oct10/'+sha[:20]+'.svg'
    (work/relative).write_bytes(data)
    added.append(dict(source_url=url,path=relative,bytes=len(data),sha256=sha,contentType=content_type,
        acquisition='Unauthenticated HTTPS GET of exact active-hero observed image URL; no known failure retried.'))
manifest['assets'].extend(added)
manifest['assets'].sort(key=lambda item:item['source_url'])
file.write_text(json.dumps(manifest,indent=2)+'\n')
(work/'miro-oct11-hero-additional-assets.json').write_text(json.dumps({'added':added,'known_failures_not_retried':True},indent=2)+'\n')
print(json.dumps({'added':len(added),'total_assets':len(manifest['assets'])}))
