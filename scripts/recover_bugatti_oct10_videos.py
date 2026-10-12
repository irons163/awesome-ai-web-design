from pathlib import Path
import json,urllib.request,hashlib,concurrent.futures
w=Path('.stitch-work/current-official');p=w/'bugatti-oct10-assets.json';m=json.loads(p.read_text());(w/'bugatti-oct10-assets-initial-failures.json').write_text(json.dumps(m['failures'],indent=2)+'\n')
def recover(f):
 u=f['source_url'];req=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0','Accept':'*/*'})
 with urllib.request.urlopen(req,timeout=150)as r:
  expected=int(r.headers.get('Content-Length','0'));ct=r.headers.get('Content-Type','');pieces=[]
  while True:
   b=r.read(256*1024)
   if not b:break
   pieces.append(b)
 data=b''.join(pieces)
 if expected and len(data)!=expected:raise ValueError('Incomplete public video bytes')
 sha=hashlib.sha256(data).hexdigest();dest=w/'bugatti-assets'/'oct10'/(sha[:20]+'.mp4');dest.write_bytes(data)
 return dict(source_url=u,path=str(dest.relative_to(w)),bytes=len(data),sha256=sha,contentType=ct,acquisition='Chunked unauthenticated GET of exact current CUA-observed public video URL after initial timeout/incomplete transfer; no altered URL or access bypass')
remaining=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:
 fs={pool.submit(recover,f):f for f in m['failures']}
 for future,f in fs.items():
  try:m['assets'].append(future.result())
  except Exception as e:remaining.append({'source_url':f['source_url'],'error':str(e)})
m['failures']=remaining;m['assets'].sort(key=lambda a:a['source_url']);p.write_text(json.dumps(m,indent=2)+'\n')
print(json.dumps({'assets':len(m['assets']),'bytes':sum(a['bytes']for a in m['assets']),'remainingFailureCount':len(remaining)}))
