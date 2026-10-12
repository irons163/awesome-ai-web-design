import concurrent.futures,hashlib,json,re,urllib.parse,urllib.request
from pathlib import Path
p=Path('.stitch-work/current-official');f=p/'playstation-oct10-assets.json';m=json.loads(f.read_text());known={a['source_url']:a for a in m['assets']};acquired=[];fail=[]
def obtain(item):
 u,reason=item
 if u in known:return known[u]
 try:
  with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=60)as r:b=r.read();ct=r.headers.get('Content-Type','')
  h=hashlib.sha256(b).hexdigest();ext=Path(urllib.parse.urlsplit(u).path).suffix or '.bin';out=p/('playstation-assets/oct10/'+h[:20]+ext);out.write_bytes(b)
  return dict(source_url=u,path=str(out.relative_to(p)),bytes=len(b),sha256=h,contentType=ct,acquisition=reason)
 except Exception as e:fail.append(dict(source_url=u,error=str(e)));return None
queue=[a for a in m['assets']if urllib.parse.urlsplit(a['source_url']).path.endswith('.css')];seen=set()
while queue:
 urls=[]
 for a in queue:
  if a['source_url']in seen:continue
  seen.add(a['source_url']);s=(p/a['path']).read_text(errors='replace')
  for u in re.findall(r'@import\s+(?:url\(\s*)?[\'\"]?([^\s\'\";)]+)',s):urls.append((urllib.parse.urljoin(a['source_url'],u),'Exact @import dependency of observed current official public stylesheet'))
  for b in re.findall(r'@font-face\{([^}]+)\}',s):
   if 'font-family:\'SST\''in b and re.search(r'font-weight:(?:200|300|400|500|700);',b)and 'U+20-FF'in b or 'font-family:\'SST\''in b and re.search(r'font-weight:(?:200|300|400|500|700);',b)and 'U+0104'in b:
    for u in re.findall(r'url\([\'\"]?([^\s\'\")]+)',b):
     if '.woff2'in u:urls.append((urllib.parse.urljoin(a['source_url'],u),'Original Latin/Latin-extended SST font explicitly referenced by current observed public font stylesheet'))
  if 'font-all.css'not in a['source_url']:
   for u in re.findall(r'url\([\'\"]?([^\s\'\")]+)',s):
    if re.search(r'\.(?:woff2?|ttf)(?:[?#]|$)',u):urls.append((urllib.parse.urljoin(a['source_url'],u),'Original font dependency of observed current official public stylesheet'))
 unique={u:r for u,r in urls if u not in known}
 with concurrent.futures.ThreadPoolExecutor(max_workers=6)as pool:got=[a for a in pool.map(obtain,unique.items())if a]
 for a in got:known[a['source_url']]=a;acquired.append(a)
 queue=[a for a in got if urllib.parse.urlsplit(a['source_url']).path.endswith('.css')]
m['assets']=list(known.values());m['failures']+=fail;f.write_text(json.dumps(m,indent=2)+'\n');(p/'playstation-oct10-css-dependency-acquisition.json').write_text(json.dumps({'assets':acquired,'failures':fail},indent=2)+'\n');print(json.dumps({'new':len(acquired),'total':len(known),'failures':fail}))
