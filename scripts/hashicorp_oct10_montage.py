from PIL import Image,ImageDraw
from pathlib import Path
import json
p=Path('.stitch-work/current-official')
for w in (1280,390):
 a=p/f'hashicorp-oct10-official-{w}-phases.json';b=p/f'hashicorp-oct10-local-{w}-phases.json'
 if not b.exists():continue
 aa=json.loads(a.read_text());bb=json.loads(b.read_text());tw=640 if w==1280 else 390
 for start in range(0,min(len(aa),len(bb)),4):
  ims=[]
  for x,y in zip(aa[start:start+4],bb[start:start+4]):
   row=[]
   for side,z in [('official',x),('local',y)]:
    im=Image.open(p/z['screenshot']);im=im.resize((tw,round(im.height*tw/im.width)));tile=Image.new('RGB',(tw,im.height+24),'#ddd');tile.paste(im,(0,24));ImageDraw.Draw(tile).text((4,4),f'{side}:phase{z.get("phase","?")} y{z["scrollY"]}',fill='black');row.append(tile)
   joined=Image.new('RGB',(tw*2,max(z.height for z in row)),'white');joined.paste(row[0]);joined.paste(row[1],(tw,0));ims.append(joined)
  out=Image.new('RGB',(tw*2,sum(z.height for z in ims)), 'white');top=0
  for im in ims:out.paste(im,(0,top));top+=im.height
  out.save(p/f'hashicorp-oct10-comparison-{w}-{start//4}.jpg',quality=90)
