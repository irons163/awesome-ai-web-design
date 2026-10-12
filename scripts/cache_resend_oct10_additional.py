import json,hashlib,re,urllib.request,concurrent.futures
from pathlib import Path
from urllib.parse import urljoin,urlsplit
w=Path('.stitch-work/current-official');p=w/'resend-oct10-assets.json';m=json.loads(p.read_text());known={a['source_url'] for a in m['assets']};urls={a['source_url'] for a in m['failures']}
for a in m['assets']:
 if a.get('contentType','').startswith('text/css') or a['path'].endswith('.css'):
  text=(w/a['path']).read_text()
  for u in re.findall(r'url\(\s*[\'"]?(.*?)[\'"]?\s*\)',text):
   if not u.startswith(('data:','#')):urls.add(urljoin(a['source_url'],u))
def get(u):
 with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=45) as r:data=r.read();ct=r.headers.get('Content-Type','')
 h=hashlib.sha256(data).hexdigest();ext='.woff2' if data[:4]==b'wOF2' else '.svg' if b'<svg' in data[:1000] else Path(urlsplit(u).path).suffix or '.bin';q=w/'resend-assets'/'oct10'/(h[:20]+ext);q.write_bytes(data)
 return dict(source_url=u,path=str(q.relative_to(w)),bytes=len(data),sha256=h,contentType=ct,acquisition='Unauthenticated GET of exactly observed public CSS url() or one retry of observed asset URL')
fail=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
 futures={ex.submit(get,u):u for u in urls-known}
 for f,u in futures.items():
  try:m['assets'].append(f.result())
  except Exception as e:fail.append(dict(source_url=u,error=str(e)))
m['failures']=fail;p.write_text(json.dumps(m,indent=2)+'\n');print(json.dumps(dict(assets=len(m['assets']),failures=fail)))
