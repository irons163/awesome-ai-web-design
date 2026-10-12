from pathlib import Path
import json, hashlib
from PIL import Image,ImageDraw
w=Path('.stitch-work/current-official');b='ollama';checks=[]
for mode,width,height in [('desktop',1280,720),('narrow',390,844)]:
    a=json.loads((w/f'{b}-oct10-official-{width}-phases.json').read_text())
    c=json.loads((w/f'{b}-oct10-corrected-native-{width}-phases.json').read_text())
    assert len(a)==len(c)==2
    for phases in [a,c]:
        assert phases[0]['scrollY']==0 and phases[-1]['scrollY']+height==phases[-1]['bodyHeight']
        assert phases[1]['scrollY']<=height
        assert all(Image.open(w/p['screenshot']).size==(width,height) for p in phases)
    for i,(x,y) in enumerate(zip(a,c)):
        assert x['scrollY']==y['scrollY'] and x['bodyHeight']==y['bodyHeight']
        out=Image.new('RGB',(width*2,height+28),'#eee');d=ImageDraw.Draw(out)
        d.text((6,7),'Official current public page',fill='black');d.text((width+6,7),'Corrected actual local page',fill='black')
        out.paste(Image.open(w/x['screenshot']),(0,28));out.paste(Image.open(w/y['screenshot']),(width,28))
        out.save(w/f'{b}-oct10-compare-{mode}-{i}.png')
    checks.append({'mode':mode,'viewport':[width,height],'sourcePhases':2,'previewPhases':2,'fullSequentialCoverage':True,'sourceHeight':a[-1]['bodyHeight'],'previewHeight':c[-1]['bodyHeight'],'scrollYs':[p['scrollY']for p in a]})
im1=Image.open(w/f'{b}-oct10-official-narrow-menu.jpg');im2=Image.open(w/f'{b}-oct10-corrected-narrow-menu.jpg');assert im1.size==im2.size==(390,844)
out=Image.new('RGB',(780,872),'#eee');d=ImageDraw.Draw(out);d.text((6,7),'Official open menu',fill='black');d.text((396,7),'Corrected open menu',fill='black');out.paste(im1,(0,28));out.paste(im2,(390,28));out.save(w/f'{b}-oct10-compare-narrow-menu.png')
(w/f'{b}-oct10-native-coverage.json').write_text(json.dumps({'checks':checks,'screenshotMethod':'Native JPEG viewport screenshots, PIL actual dimensions guarded; observed scroll offsets cover entire page.','previewSha256':hashlib.sha256((w/f'{b}.html').read_bytes()).hexdigest()},indent=2)+'\n')
print(json.dumps(checks))
