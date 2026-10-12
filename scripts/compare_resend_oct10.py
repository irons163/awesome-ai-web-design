from pathlib import Path
import json
from PIL import Image,ImageDraw
w=Path('.stitch-work/current-official');b='resend'
for width,mode in [(1280,'desktop'),(390,'narrow')]:
 phases=json.loads((w/f'{b}-oct10-official-{width}-phases.json').read_text())
 a=Image.new('RGB',(width,int(max(p['bodyHeight'] for p in phases))),'black')
 for p in phases:
  im=Image.open(w/p['screenshot']).convert('RGB');a.paste(im,(0,round(p['scrollY'])))
 a.save(w/f'{b}-oct10-official-{mode}-phase-composite.png')
 cp=json.loads((w/f'{b}-oct10-corrected-final-{width}-phases.json').read_text());c=Image.new('RGB',(width,int(max(p['bodyHeight'] for p in cp))),'black')
 for p in cp:c.paste(Image.open(w/p['screenshot']).convert('RGB'),(0,round(p['scrollY'])))
 c.save(w/f'{b}-oct10-corrected-final-{mode}-phase-composite.png');scale=.5 if mode=='desktop' else 1
 for i,y in enumerate(range(0,max(a.height,c.height),2000)):
  h=min(2000,max(a.height,c.height)-y);o=Image.new('RGB',(round((a.width+c.width)*scale),round(h*scale)+30),'#ddd');d=ImageDraw.Draw(o);d.text((5,6),'Official sequential phase composite',fill='black');d.text((round(a.width*scale)+5,6),'Corrected final sequential phases',fill='black');o.paste(a.crop((0,y,a.width,y+h)).resize((round(a.width*scale),round(h*scale))),(0,30));o.paste(c.crop((0,y,c.width,y+h)).resize((round(c.width*scale),round(h*scale))),(round(a.width*scale),30));o.save(w/f'{b}-oct10-compare-{mode}-{i}.png')
print('Resend actual-render comparison pairs saved')
