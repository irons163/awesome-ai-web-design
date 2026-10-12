from pathlib import Path
import concurrent.futures,hashlib,json,re,urllib.request
p=Path('.stitch-work/current-official');m=json.loads((p/'minimax-oct10-assets.json').read_text());known={a['source_url'] for a in m['assets']};urls=set()
for a in m['assets']:
 if a['path'].endswith('.css'):
  for f in re.findall(r'@font-face\{[^}]+\}',(p/a['path']).read_text()):
   if any(x in f for x in ('font-family:Outfit;','font-family:DM Sans;','font-family:Libre Baskerville;')):urls.update(re.findall(r'url\((https://[^)]+)\)',f))
def get(u):
 with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=45) as f:b=f.read();ct=f.headers.get('Content-Type','')
 h=hashlib.sha256(b).hexdigest();out=p/'minimax-assets'/'oct10'/(h[:20]+Path(u).suffix);out.write_bytes(b);return dict(source_url=u,path=str(out.relative_to(p)),bytes=len(b),sha256=h,contentType=ct,acquisition='Unauthenticated GET of exact public font URL in captured current official stylesheet')
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:a=list(pool.map(get,sorted(urls-known)))
m['assets'].extend(a);m['assets'].sort(key=lambda x:x['source_url']);(p/'minimax-oct10-assets.json').write_text(json.dumps(m,indent=2)+'\n');print(len(a),sum(x['bytes'] for x in a))
