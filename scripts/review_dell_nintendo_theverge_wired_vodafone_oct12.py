"""Preserve source assets and produce whole-viewport review sheets; no browser controls."""
import hashlib,json,re,shutil,sys
from datetime import datetime,timezone
from pathlib import Path
from PIL import Image,ImageDraw

work=Path('/Users/pchang01/Documents/mygithub/awesome-ai-web-design/.stitch-work/current-official')
brand=sys.argv[1]
assert brand in {'dell-1996','nintendo-2001','theverge','wired','vodafone'}
sha=lambda b:hashlib.sha256(b).hexdigest()
track=re.compile(r'google-analytics\.com|analytics\.google\.com|doubleclick|googlead|/pagead/|/collect(?:[/?]|$)|ads\.linkedin|adsct|/pixel|segment\.com|bat\.bing\.com|facebook\.com/tr|connect\.facebook\.net|googletagmanager\.com|metrics\.brightcove\.com|d\.agkn\.com|dell\.com/null',re.I)
out=work/(brand+'-assets')/'oct12-source';out.mkdir(parents=True,exist_ok=True)
assets={};failures={};raw=[];inline={}
bundlepaths=[work/f'{brand}-oct10-official-{width}-asset-bundle.json' for width in (1280,390)]+sorted(work.glob(brand+'-oct12-final-*-asset-bundle.json'))
for bundlepath in bundlepaths:
 if not bundlepath.exists():continue
 b=json.loads(bundlepath.read_text());raw.append({'file':bundlepath.name,'sha256':sha(bundlepath.read_bytes()),'summary':b['summary']})
 for a in b['assets']:
  if not track.search(a['url']):assets[a['url']]=a
 for a in b['failures']:
  if not track.search(a['url']):failures[a['url']]=a
for width in (1280,390):
 invpath=work/f'{brand}-oct10-official-{width}-page-assets.json'
 if not invpath.exists():continue
 inv=json.loads(invpath.read_text())
 for a in inv.get('inlineSvgs',[]):inline[sha(a['markup'].encode())]=a

def extension(data,a):
 if data.startswith(b'RIFF') and data[8:12]==b'WEBP':return '.webp'
 if data.startswith(b'\x89PNG'):return '.png'
 if data.startswith(b'\xff\xd8'):return '.jpg'
 if data.startswith(b'wOF2'):return '.woff2'
 if data.startswith(b'wOFF'):return '.woff'
 if b'<svg' in data[:1000]:return '.svg'
 if data[4:8]==b'ftyp':return '.avif' if b'avif' in data[:32] else '.mp4'
 return {'text/css':'.css','font/ttf':'.ttf','font/otf':'.otf'}.get((a.get('contentType') or '').split(';')[0],Path(a['name']).suffix or '.bin')

preserved=[]
for url,a in sorted(assets.items()):
 p=Path(a['path'])
 if not p.is_file():failures[url]={**a,'reason':'Native pageAssets temporary file unavailable at preservation time'};continue
 data=p.read_bytes();h=sha(data);target=out/(h[:20]+extension(data,a));target.write_bytes(data)
 preserved.append({'source_url':url,'path':str(target.relative_to(work)),'bytes':len(data),'sha256':h,'contentType':a.get('contentType'),'kind':a['kind'],'acquisition':'Original bytes from native CUA pageAssets bundle; not reencoded'})
for h,a in inline.items():
 p=out/(h[:20]+'.svg');p.write_text(a['markup']);preserved.append({'source_url':'inline-svg:'+a['id'],'path':str(p.relative_to(work)),'bytes':len(p.read_bytes()),'sha256':sha(p.read_bytes()),'contentType':'image/svg+xml','kind':'image','acquisition':'Exact observed DOM inline SVG markup'})
unresolved=[{'source_url':u,'reason':a['reason'],'contentType':a.get('contentType'),'retried':False} for u,a in failures.items() if u not in assets]
bundle={'observedAt':datetime.now(timezone.utc).isoformat(),'sourceOnly':True,'trackingExcluded':True,'assets':list(assets.values()),'failures':[a for u,a in failures.items() if u not in assets],'nativeBundles':raw}
(work/f'{brand}-oct10-asset-bundle.json').write_text(json.dumps(bundle,ensure_ascii=False,indent=2)+'\n')
manifest={'observedAt':datetime.now(timezone.utc).isoformat(),'sourceOnly':True,'assets':preserved,'failures':unresolved,'trackingExcluded':True,'nativeBundles':raw,'noHTTPRetryOrAlternateURLs':True}
(work/f'{brand}-oct10-assets.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')

coverage=[];sheets=[];frameRecords=[]
for width,height,label in ((1280,720,'desktop'),(390,844,'narrow')):
 path=work/f'{brand}-oct10-official-{width}-phases.json'
 if not path.exists():continue
 phases=json.loads(path.read_text());end=0;gaps=[];allDimensions=True
 for index,p in enumerate(phases):
  data=(work/p['screenshot']).read_bytes();im=Image.open(work/p['screenshot']);im.load()
  assert im.size==(width,height),(p['screenshot'],im.size)
  assert sha(data)==p['screenshotSha256']
  if p['scrollY']>end+1:gaps.append([end,p['scrollY']])
  end=max(end,p['scrollY']+height)
  frameRecords.append({'file':p['screenshot'],'sha256':sha(data),'actualWidth':im.width,'actualHeight':im.height,'scrollY':p['scrollY'],'observedAt':p['observed_at']})
 per=2 if width==1280 else 4
 for first in range(0,len(phases),per):
  part=phases[first:first+per];columns=1 if width==1280 else len(part);rows=len(part) if width==1280 else 1
  sheet=Image.new('RGB',(columns*width,rows*(height+30)),(235,235,235));draw=ImageDraw.Draw(sheet)
  for k,p in enumerate(part):
   x=0 if width==1280 else k*width;y=k*(height+30) if width==1280 else 0
   draw.text((x+8,y+7),f'{brand} {label} frame {first+k} y={p["scrollY"]} native {width}x{height}',fill=(0,0,0));sheet.paste(Image.open(work/p['screenshot']).convert('RGB'),(x,y+30))
  name=f'{brand}-oct12-source-review-{label}-{first//per}.png';sheet.save(work/name);sheets.append({'file':name,'sha256':sha((work/name).read_bytes()),'frames':[p['screenshot'] for p in part],'allFramesWhole':True,'resized':False})
 terminal=phases[-1]['bodyHeight'];coverage.append({'width':width,'height':height,'phasesFile':path.name,'phasesSha256':sha(path.read_bytes()),'phaseCount':len(phases),'nativeDimensionsAllCorrect':allDimensions,'startsAtTop':abs(phases[0]['scrollY'])<=1,'gaps':gaps,'coverageEnd':end,'finalBodyHeight':terminal,'reachesTerminalFooter':end>=terminal-1,'gapless':not gaps and end>=terminal-1,'noOverflow':all(p['bodyWidth']<=width for p in phases),'unreadyVisibleImageOccurrences':sum(1 for p in phases for a in p['visibleMedia'] if a['tag']=='IMG' and not a['loaded'])})

review={'observedAt':datetime.now(timezone.utc).isoformat(),'brand':brand,'scope':'Anonymous current official source research only; no clone fidelity or completion claim','coverage':coverage,'nativeFrames':frameRecords,'reviewSheets':sheets,'visualReviewComplete':False,'assetsManifest':f'{brand}-oct10-assets.json','assetCount':len(preserved),'assetFailures':len(unresolved),'accepted':False}
(work/f'{brand}-oct12-source-review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'brand':brand,'coverage':coverage,'sheets':[s['file'] for s in sheets],'assets':len(preserved),'failures':len(unresolved)},ensure_ascii=False,indent=2))
