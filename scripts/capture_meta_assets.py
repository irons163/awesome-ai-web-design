#!/usr/bin/env python3
"""Capture public assets observed in the dated rendered Meta Canada homepage."""
import hashlib
import json
import mimetypes
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit, parse_qs
from zoneinfo import ZoneInfo

WORK = Path(__file__).resolve().parents[1] / '.stitch-work/current-official'
BUNDLE = Path('/var/folders/34/yb_61rwx2kd7pc6f1xd7l80w0000gn/T/browser-use/assets/4978d19b-5c02-4a58-958e-c2c59a18326b/manifest.json')
MEDIA = [
 ('1019512193865523','1791312022'), ('1776006623643465','1790089128'),
 ('28463428633322724','1790089128'), ('1603834474428318','1789440710'),
 ('1785594222681010','1791312021'), ('1617413229969463','1791310533'),
 ('1476175607896980','1790732924'), ('954863517662877','1790974189'),
 ('1369273198705222','1791310533'), ('1547194663656162','1781735316'),
 ('2195054354368471','1781735316'), ('1467356825221356','1789761630'),
 ('945715694601950','1789761630'), ('1639626233993472','1791307624'),
 ('1746818216319556','1791307624'),
]
EXTRA = ['https://lookaside.fbsbx.com/elementpath/media/?media_id='+i+'&version='+v+'&transcode_extension=webp' for i,v in MEDIA] + [
 'https://static.xx.fbcdn.net/rsrc.php/yQ/r/-pkMfchyeAZ.woff2',
 'https://static.xx.fbcdn.net/rsrc.php/yf/r/-7pQO6hUGK_.svg',
]

def record(data,url,kind,content_type,method):
 if kind=='stylesheet': ext='.css'
 elif kind=='font': ext='.woff2'
 elif 'svg' in (content_type or '') or urlsplit(url).path.endswith('.svg'): ext='.svg'
 elif 'transcode_extension=webp' in url or 'webp' in (content_type or ''): ext='.webp'
 else: ext=mimetypes.guess_extension((content_type or '').split(';')[0]) or '.asset'
 mid=parse_qs(urlsplit(url).query).get('media_id',[''])[0]
 name=hashlib.sha256(url.encode()).hexdigest()[:12]+('-'+mid if mid else '')+ext
 path=WORK/'meta-assets'/name; path.parent.mkdir(parents=True,exist_ok=True); path.write_bytes(data)
 return {'source_url':url,'path':str(path.relative_to(WORK)),'kind':kind,'content_type':content_type,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'method':method,'observed_at':datetime.now(ZoneInfo('Asia/Taipei')).isoformat()}

def capture(url):
 host=urlsplit(url).hostname
 if host not in ('static.xx.fbcdn.net','lookaside.fbsbx.com'):
  raise ValueError('Unobserved host: '+str(host))
 with tempfile.TemporaryDirectory(prefix='meta-asset-') as folder:
  path=Path(folder)/'resource'
  r=subprocess.run(['curl','--silent','--show-error','--location','--connect-timeout','10','--max-time','25','--output',str(path),'--write-out','%{http_code}|%{content_type}',url],capture_output=True)
  status,_,ctype=r.stdout.decode().partition('|')
  if r.returncode or status!='200': return None,{'source_url':url,'status':status,'error':r.stderr.decode()}
  data=path.read_bytes()
  if not data or data.lstrip().lower().startswith((b'<!doctype html',b'<html')): return None,{'source_url':url,'status':status,'error':'Empty or HTML asset'}
 return record(data,url,'font' if url.endswith('.woff2') else 'image',ctype,'ordinary public HTTP, exact observed asset URL'),None

def main():
 p=WORK/'meta-asset-provenance.json'; evidence=json.loads(p.read_text()) if p.exists() else {'assets':[],'capture_failures':[]}
 rows={r['source_url']:r for r in evidence['assets']}
 if BUNDLE.exists():
  bundle=json.loads(BUNDLE.read_text())
  for a in bundle['assets']:
   rows[a['url']]=record(Path(a['path']).read_bytes(),a['url'],a['kind'],a.get('contentType'),'documented pageAssets bundle; original bytes')
  evidence['browser_bundle_failures']=bundle['failures']
 with ThreadPoolExecutor(max_workers=4) as pool:
  for row,failure in pool.map(capture,[u for u in EXTRA if u not in rows]):
   if row: rows[row['source_url']]=row
   else: evidence['capture_failures'].append(failure)
 evidence['assets']=list(rows.values()); p.write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'assets':len(rows),'bytes':sum(r['bytes'] for r in rows.values()),'failures':evidence['capture_failures']}))

if __name__=='__main__': main()
