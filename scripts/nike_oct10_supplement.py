import concurrent.futures,hashlib,json,urllib.request
from pathlib import Path
p=Path('.stitch-work/current-official');m=json.loads((p/'nike-oct10-assets.json').read_text());known={a['source_url'] for a in m['assets']};urls=set()
for w in (1280,390):
 r=json.loads((p/f'nike-oct10-official-{w}-reference.json').read_text())
 urls.update(a['src'] for a in r['images'] if a['src'].startswith('https://static.nike.com/'))
def get(u):
 req=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0','Accept':'image/webp,image/avif,image/*,*/*;q=0.8'})
 with urllib.request.urlopen(req,timeout=45) as f: b=f.read();ct=f.headers.get('Content-Type','')
 h=hashlib.sha256(b).hexdigest();ext='.avif' if b[4:8]==b'ftyp' and b'avif' in b[:32] else '.jpg' if b[:2]==b'\xff\xd8' else '.png' if b[:4]==b'\x89PNG' else '.webp'
 dest=p/'nike-assets'/'oct10'/(h[:20]+ext);dest.write_bytes(b)
 return dict(source_url=u,path=str(dest.relative_to(p)),bytes=len(b),sha256=h,contentType=ct,acquisition='Unauthenticated HTTPS GET of exactly re-observed public image URL after stable viewport capture')
new=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
 for a in pool.map(get,sorted(urls-known)): new.append(a)
m['assets'].extend(new);m['assets'].sort(key=lambda a:a['source_url']);(p/'nike-oct10-assets.json').write_text(json.dumps(m,indent=2)+'\n');(p/'nike-oct10-assets-supplement.json').write_text(json.dumps(new,indent=2)+'\n');print(len(new),sum(a['bytes'] for a in new))
