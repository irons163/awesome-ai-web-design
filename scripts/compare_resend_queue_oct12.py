from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json,math

w=Path('.stitch-work/current-official')
def hash_file(p):return hashlib.sha256(p.read_bytes()).hexdigest()
official={
 'raycast':'raycast-oct10-official-{mode}-native-phase-composite.png',
 'warp':'warp-oct10-official-{mode}-native-phase-composite.png',
 'resend':'resend-oct10-official-{mode}-phase-composite.png',
 'supabase':'supabase-oct10-official-{mode}.png'
}
for b in official:
 sha=hash_file(w/(b+'.html'));records=[]
 for width,height,mode in [(1280,720,'desktop'),(390,844,'narrow')]:
  phases=json.loads((w/f'{b}-oct12-current-{width}-phases.json').read_text())
  loaded=json.loads((w/f'{b}-oct12-current-{width}-loaded-response.json').read_text())
  assert loaded['exactByteEquality'] and loaded['documentResponseSha256']==loaded['currentFileSha256']==sha
  assert phases[0]['scrollY']==0
  assert all(q['draft_sha256']==sha for q in phases)
  assert all(n['scrollY']<=p['scrollY']+height for p,n in zip(phases,phases[1:]))
  assert phases[-1]['scrollY']+height==phases[-1]['bodyHeight']
  for q in phases:
   assert Image.open(w/q['screenshot']).size==(width,height)
   assert hash_file(w/q['screenshot'])==q['screenshotSha256']
  current=Image.new('RGB',(width,phases[-1]['bodyHeight']),'black')
  for q in phases:current.paste(Image.open(w/q['screenshot']).convert('RGB'),(0,round(q['scrollY'])))
  composite=f'{b}-oct12-current-{mode}-native-phase-composite.png';current.save(w/composite)
  source_file=official[b].format(mode=mode);source=Image.open(w/source_file).convert('RGB')
  assert source.width==width
  comparison=[];scale=.5 if width==1280 else 1
  for i,y in enumerate(range(0,max(source.height,current.height),2000)):
   h=min(2000,max(source.height,current.height)-y);o=Image.new('RGB',(int(width*2*scale),int(h*scale)+42),'#ddd');d=ImageDraw.Draw(o)
   d.text((5,6),'Historical official source (original observation date)',fill='black');d.text((int(width*scale)+5,6),'Current preview actual Oct12 phases / SHA '+sha[:8],fill='black')
   o.paste(source.crop((0,y,width,y+h)).resize((int(width*scale),int(h*scale))),(0,42));o.paste(current.crop((0,y,width,y+h)).resize((int(width*scale),int(h*scale))),(int(width*scale),42))
   n=f'{b}-oct12-compare-{mode}-{i}.png';o.save(w/n);comparison.append(n)
  # Every entire raw current viewport appears in one contact sheet, without
  # composite overlap hiding any frame. Originals retain true native dimensions.
  contacts=[];per=4 if width==1280 else 3
  for batch in range(math.ceil(len(phases)/per)):
   chunk=phases[batch*per:(batch+1)*per]
   if width==1280:cols,rows,sw,sh=2,2,640,360
   else:cols,rows,sw,sh=3,1,390,844
   o=Image.new('RGB',(cols*sw,rows*(sh+28)+38),'#ddd');d=ImageDraw.Draw(o)
   d.text((6,9),f'{b} current SHA {sha[:12]} / ALL complete viewport frames, inspection sheet only',fill='black')
   for j,q in enumerate(chunk):
    x=(j%cols)*sw;y=38+(j//cols)*(sh+28)
    d.text((x+5,y+5),f"phase{batch*per+j} / y{q['scrollY']} / native{width}x{height}",fill='black')
    im=Image.open(w/q['screenshot']).convert('RGB');o.paste(im.resize((sw,sh)),(x,y+28))
   n=f'{b}-oct12-review-{mode}-{batch}.png';o.save(w/n);contacts.append({'file':n,'phaseIndices':list(range(batch*per,batch*per+len(chunk))),'nativeFrames':[q['screenshot']for q in chunk],'meaning':'Derived whole-viewport inspection sheet. Desktop frames displayed at half size, narrow frames unscaled. Actual originals unchanged; this is not a capture raster or device-size claim.'})
  fresh=w/f'{b}-oct12-official-{width}-reference.json';fresh_record=None
  if fresh.exists():
   r=json.loads(fresh.read_text());im=Image.open(w/r['screenshot']);assert im.size==(width,height)
   html=''.join(r['htmlParts']);assert hashlib.sha256(html.encode()).hexdigest()==r['html_sha256']and len(html.encode('utf-16-le'))//2==r['html_length']and html.endswith('</html>')
   pair=Image.new('RGB',(int(width*2*scale),int(height*scale)+42),'#ddd');pd=ImageDraw.Draw(pair);pd.text((5,7),'Fresh official TOP only / '+r['observed_at'],fill='black');pd.text((int(width*scale)+5,7),'Current preview first native frame',fill='black');pair.paste(im.convert('RGB').resize((int(width*scale),int(height*scale))),(0,42));pair.paste(Image.open(w/phases[0]['screenshot']).convert('RGB').resize((int(width*scale),int(height*scale))),(int(width*scale),42));top=f'{b}-oct12-fresh-top-compare-{mode}.png';pair.save(w/top)
   fresh_record={'reference':fresh.name,'screenshot':r['screenshot'],'observedAt':r['observed_at'],'url':r['url'],'htmlSha256':r['html_sha256'],'htmlComplete':True,'actualTopScreenshotDimensions':[width,height],'heightAtTopObservation':r['bodyHeight'],'scrollYAtTopObservation':r['scrollY'],'scope':r['scope'],'comparison':top,'headingTexts':r['headings']}
  records.append({'scope':mode,'width':width,'height':height,'previewSha256':sha,'observedAt':[phases[0]['observed_at'],phases[-1]['observed_at']],'phaseFile':f'{b}-oct12-current-{width}-phases.json','phases':len(phases),'trueNativeScreenshotDimensions':[width,height],'scrollYs':[q['scrollY']for q in phases],'bodyHeight':phases[-1]['bodyHeight'],'completeCoverage':True,'loadedHtmlResponse':f'{b}-oct12-current-{width}-loaded-response.json','loadedResponseExactFileEquality':True,'allImages':len(phases[-1]['images']),'imagesNotReady':sum(not e['loaded']for e in phases[-1]['images']),'fontStatus':phases[-1]['fontStatus'],'noHorizontalOverflow':all(q['bodyWidth']==width for q in phases),'nativePhaseComposite':composite,'historicalOfficialComposite':source_file,'historicalSourceComparisonSegments':comparison,'wholeViewportReviewSheets':contacts,'freshOfficialTop':fresh_record})
 (w/f'{b}-oct12-current-coverage.json').write_text(json.dumps({'brand':b,'previewSha256':sha,'currentCompleteCapture':True,'records':records,'meaning':'Actual current preview complete viewport sequences. Historical official full-page comparison retains its original date. Fresh official records are top observations only. No animation/service/hardware equivalence claim.'},ensure_ascii=False,indent=2)+'\n')
 print(b,'phases',[x['phases']for x in records],'review sheets',[len(x['wholeViewportReviewSheets'])for x in records],'guarded current SHA',sha)
