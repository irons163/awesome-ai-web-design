from pathlib import Path
import concurrent.futures,json,hashlib,re,urllib.request
from urllib.parse import urlsplit
from html import unescape
w=Path('.stitch-work/current-official');b='runwayml';target=w/(b+'-assets')/'oct10';target.mkdir(parents=True,exist_ok=True)
inv=json.loads((w/f'{b}-oct10-asset-inventory.json').read_text())
items={a['url']:a for a in inv['assets'] if a['kind'] in ['font','image','stylesheet','video'] and not re.search(r'google-analytics|analytics\.google|doubleclick|googlead|/collect(?:[/?]|$)|ads\.linkedin|/pixel|segment\.com|bat\.bing|facebook\.com/tr|googletagmanager',a['url'],re.I)}
for width in [1280,390]:
 p=w/f'{b}-oct10-official-{width}-reference.json'
 if not p.exists():continue
 r=json.loads(p.read_text());h=''.join(r['htmlParts'])
 background_urls=[]
 for style in re.findall(r'style="([^"]*)"',h):
  background_urls.extend(re.findall(r'url\([\s\'"]*(https://[^\s)\'"]+)',unescape(style)))
 for url in [i['src'] for i in r['images']]+r['stylesheets']+re.findall(r'poster="(https:[^"]+)"',h)+background_urls:
  if url.startswith('https://'):items.setdefault(url,{'url':url,'kind':'image'})
previous=w/f'{b}-oct10-assets.json';existing=json.loads(previous.read_text())['assets']if previous.exists()else[];byurl={a['source_url']:a for a in existing}
def preserve(a):
 url=a['url']
 if url in byurl and (w/byurl[url]['path']).exists():return byurl[url]
 req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0','Accept':'image/webp,image/avif,image/*,*/*;q=0.8'})
 with urllib.request.urlopen(req,timeout=45)as res:data=res.read();ct=res.headers.get('Content-Type','')
 ext=Path(urlsplit(url).path).suffix or '.bin'
 if data.startswith(b'RIFF')and data[8:12]==b'WEBP':ext='.webp'
 elif data.startswith(b'\x89PNG'):ext='.png'
 elif data.startswith(b'\xff\xd8'):ext='.jpg'
 elif data.startswith(b'wOF2'):ext='.woff2'
 elif b'<svg'in data[:1000]:ext='.svg'
 elif data[4:8]==b'ftyp':ext='.avif'if b'avif'in data[:32]else'.mp4'
 digest=hashlib.sha256(data).hexdigest();p=target/(digest[:20]+ext);p.write_bytes(data)
 return dict(source_url=url,path=str(p.relative_to(w)),bytes=len(data),sha256=digest,contentType=ct,acquisition='Unauthenticated HTTPS GET of exact current CUA-observed public asset URL; original pageAssets bundle timed out, no source-page access bypass')
assets=[];failures=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:
 futures={pool.submit(preserve,a):a for a in items.values()}
 for f,a in futures.items():
  try:assets.append(f.result())
  except Exception as e:failures.append(dict(source_url=a['url'],error=str(e)))
(w/f'{b}-oct10-assets.json').write_text(json.dumps(dict(assets=sorted(assets,key=lambda a:a['source_url']),failures=failures,trackingExcluded=True,sourceInventory=f'{b}-oct10-asset-inventory.json'),indent=2)+'\n')
print(json.dumps(dict(brand=b,assets=len(assets),bytes=sum(a['bytes']for a in assets),failures=len(failures))))
