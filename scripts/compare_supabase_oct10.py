from pathlib import Path
from PIL import Image,ImageDraw
w=Path('.stitch-work/current-official');b='supabase'
for mode in ['desktop','narrow']:
 a=Image.open(w/f'{b}-oct10-official-{mode}.png').convert('RGB');c=Image.open(w/f'{b}-oct10-corrected-{mode}.png').convert('RGB');scale=.5 if mode=='desktop' else 1
 for i,y in enumerate(range(0,max(a.height,c.height),2000)):
  h=min(2000,max(a.height,c.height)-y);o=Image.new('RGB',(round((a.width+c.width)*scale),round(h*scale)+30),'#ddd');d=ImageDraw.Draw(o);d.text((5,6),'Official public capture',fill='black');d.text((round(a.width*scale)+5,6),'Corrected local render',fill='black');o.paste(a.crop((0,y,a.width,y+h)).resize((round(a.width*scale),round(h*scale))),(0,30));o.paste(c.crop((0,y,c.width,y+h)).resize((round(c.width*scale),round(h*scale))),(round(a.width*scale),30));o.save(w/f'{b}-oct10-compare-{mode}-{i}.png')
print('Supabase pairs refreshed')
