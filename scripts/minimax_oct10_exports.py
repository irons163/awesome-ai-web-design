import concurrent.futures,hashlib,json,urllib.request
from pathlib import Path
p=Path('.stitch-work/current-official');records=json.loads((p/'minimax-oct10-native-export-urls.json').read_text())
def get(x):
 s,ext,u=x
 with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=90) as f:b=f.read();ct=f.headers.get('Content-Type','')
 out=p/('minimax-oct10-native-'+s['screen']+'.'+ext);out.write_bytes(b);return dict(screen=s['screen'],device=s['device'],path=out.name,source_url=u,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),content_type=ct)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:r=list(pool.map(get,[(s,e,s[e]) for s in records for e in ('html','png')]))
(p/'minimax-oct10-native-exports.json').write_text(json.dumps(r,indent=2)+'\n');print([(a['path'],a['bytes']) for a in r])
req=json.loads((p/'minimax-oct10-native-request.json').read_text());(p/'minimax-oct10-prompt.md').write_text('# MiniMax current official reconstruction prompt\n\nReference: https://www.minimax.io/\nObserved:2026-10-11. Genuine Google Stitch MCP edit request, both original outputs and provider response retained.\n\n'+req['prompt']+'\n\nCorrect the native result against current complete desktop/narrow official DOM, original public assets and full-page actual raster captures. Preserve original DESIGN.md and provider exports. The native export is unaccepted until this source-backed correction is reviewed. Avoid claims of exact animation/service parity.\n')
