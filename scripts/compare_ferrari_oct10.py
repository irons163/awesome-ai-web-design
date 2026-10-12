from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
w=Path('.stitch-work/current-official');b='ferrari';records=[]
for width,height,mode,side in [(1280,720,'desktop','official'),(390,844,'narrow','official')]:
 pairs=[]
 for name,phaseSide in [('official',side),('corrected','corrected')]:
  phases=json.loads((w/f'{b}-oct10-{phaseSide}-{width}-phases.json').read_text())
  phases=sorted(phases,key=lambda p:p['scrollY']);ys=[p['scrollY']for p in phases]
  assert ys[0]==0 and all(y<=x+height for x,y in zip(ys,ys[1:]))and ys[-1]+height==phases[-1]['bodyHeight']
  a=Image.new('RGB',(width,int(max(p['bodyHeight']for p in phases))),'black')
  for p in phases:
   im=Image.open(w/p['screenshot']).convert('RGB');assert im.size==(width,height);a.paste(im,(0,round(p['scrollY'])))
  file=f'{b}-oct10-{name}-{mode}-native-phase-composite.png';a.save(w/file);pairs.append(a)
  records.append({'scope':mode,'side':name,'phases':len(phases),'scrollYs':ys,'trueScreenshotDimensions':[width,height],'completeCoverage':True,'composite':file,'compositeMeaning':'Sequential actual viewport screenshots joined at observed document offsets; sticky navigation and animation states repeat naturally. Not a single full-page screenshot.'})
 a,c=pairs;scale=.5 if mode=='desktop'else 1
 for i,y in enumerate(range(0,max(a.height,c.height),2000)):
  h=min(2000,max(a.height,c.height)-y);o=Image.new('RGB',(round((a.width+c.width)*scale),round(h*scale)+30),'#ddd');d=ImageDraw.Draw(o);d.text((5,6),'Official native sequential phases',fill='black');d.text((round(a.width*scale)+5,6),'Corrected native sequential phases',fill='black');o.paste(a.crop((0,y,a.width,y+h)).resize((round(a.width*scale),round(h*scale))),(0,30));o.paste(c.crop((0,y,c.width,y+h)).resize((round(c.width*scale),round(h*scale))),(round(a.width*scale),30));o.save(w/f'{b}-oct10-compare-{mode}-{i}.png')
(w/f'{b}-oct10-native-coverage.json').write_text(json.dumps({'records':records,'previewSha256':hashlib.sha256((w/f'{b}.html').read_bytes()).hexdigest()},indent=2)+'\n')
print('Actual Ferrari native comparisons and dimension/coverage guards saved')
