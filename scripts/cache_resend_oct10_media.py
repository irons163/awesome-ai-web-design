import json,hashlib,urllib.request,concurrent.futures
from pathlib import Path
from urllib.parse import urljoin,urlsplit
from html.parser import HTMLParser
w=Path('.stitch-work/current-official');p=w/'resend-oct10-assets.json';m=json.loads(p.read_text());known={a['source_url'] for a in m['assets']};urls=set()
class P(HTMLParser):
 def handle_starttag(self,t,a):
  a=dict(a)
  if t in ['video','source']:
   for k in ['src','poster']:
    if a.get(k):urls.add(urljoin('https://resend.com/',a[k]))
for width in [1280,390]:P().feed(''.join(json.loads((w/f'resend-oct10-official-{width}-reference.json').read_text())['htmlParts']))
def get(u):
 with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=45) as r:data=r.read();ct=r.headers.get('Content-Type','')
 h=hashlib.sha256(data).hexdigest();q=w/'resend-assets'/'oct10'/(h[:20]+Path(urlsplit(u).path).suffix);q.write_bytes(data)
 return dict(source_url=u,path=str(q.relative_to(w)),bytes=len(data),sha256=h,contentType=ct,acquisition='Unauthenticated GET of exact current rendered public video src/poster URL')
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
 for f,u in [(ex.submit(get,u),u) for u in urls-known]:
  try:m['assets'].append(f.result())
  except Exception as e:m['failures'].append(dict(source_url=u,error=str(e)))
p.write_text(json.dumps(m,indent=2)+'\n');print(json.dumps(dict(assets=len(m['assets']),failures=m['failures'])))
