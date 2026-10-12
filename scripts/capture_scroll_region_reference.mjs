// Run only inside CUA REPL with documented tab/CDP handles. This captures an
// actual nested scrolling region; document dimensions are kept separate.
import fs from 'node:fs/promises';
import crypto from 'node:crypto';
const work='/Users/pchang01/Documents/mygithub/awesome-ai-web-design/.stitch-work/current-official';
export async function captureRegion(tab,cdp,slug,side,width,height,expectedURL,selector,{reset=false,maxPhases=6}={}){
  const prefix=work+'/'+slug+'-oct10-'+side+'-'+width;
  await cdp.send('Page.bringToFront',{});
  await cdp.send('Emulation.setDeviceMetricsOverride',{width,height,deviceScaleFactor:1,mobile:false});
  const region=()=>tab.playwright.evaluate(selector=>{const e=document.querySelector(selector),b=e.getBoundingClientRect();return{selector,scrollTop:e.scrollTop,scrollHeight:e.scrollHeight,clientHeight:e.clientHeight,box:b.toJSON()}},selector);
  async function wheel(delta){
    const before=await region();
    await cdp.send('Input.dispatchMouseEvent',{type:'mouseWheel',x:before.box.x+12,y:Math.min(height-100,before.box.y+200),deltaX:0,deltaY:delta});
    for(let i=0;i<4;i++){await tab.playwright.domSnapshot();if(Math.abs((await region()).scrollTop-before.scrollTop)>0.5)return true;}
    return false;
  }
  let frames=[];
  if(!reset){try{frames=JSON.parse(await fs.readFile(prefix+'-phases.json','utf8'));}catch{}}
  let start=await region();
  if(reset&&start.scrollTop>0)await wheel(-start.scrollTop);
  if(reset&&Math.abs((await region()).scrollTop)>2)throw new Error('Nested scroll region has not reached its initial position.');
  if(!reset&&frames.length){const previous=frames.at(-1).coverage;if(Math.abs(start.scrollTop-previous.offset)<2&&previous.extent-previous.visible_extent-previous.offset>1)await wheel(Math.min(previous.visible_extent-32,previous.extent-previous.visible_extent-previous.offset));}
  const hash=side==='local'?crypto.createHash('sha256').update(await fs.readFile(work+'/'+slug+'.html')).digest('hex'):undefined;
  let done=false;
  const began=Date.now();
  for(let i=0;i<maxPhases;i++){
    const m=await tab.playwright.evaluate(selector=>{
      const pane=document.querySelector(selector),r=pane.getBoundingClientRect();
      return{url:location.href,observed_at:new Date().toISOString(),viewport:{width:innerWidth,height:innerHeight},scrollY,bodyHeight:document.documentElement.scrollHeight,bodyWidth:document.documentElement.scrollWidth,
        coverage:{coordinate_space:'element_scroll',selector,offset:pane.scrollTop,extent:pane.scrollHeight,visible_extent:pane.clientHeight},region:{selector,scrollTop:pane.scrollTop,scrollHeight:pane.scrollHeight,clientHeight:pane.clientHeight,box:r.toJSON()},
        headings:[...pane.querySelectorAll('h1,h2,h3')].map(e=>{const b=e.getBoundingClientRect(),s=getComputedStyle(e);return{text:e.innerText?.trim()||e.textContent.trim(),box:{x:b.x,y:b.y+scrollY,width:b.width,height:b.height},regionBox:{x:b.x-r.x,y:b.y-r.y+pane.scrollTop,width:b.width,height:b.height},font:s.fontFamily,size:s.fontSize,weight:s.fontWeight,lineHeight:s.lineHeight,color:s.color,visible:b.height>0&&b.bottom>r.top&&b.top<r.bottom}}),
        brokenVisibleImages:[...document.images].filter(e=>{const b=e.getBoundingClientRect();return b.width>0&&b.height>0&&b.bottom>r.top&&b.top<r.bottom&&e.complete&&!e.naturalWidth}).map(e=>({src:e.currentSrc||e.src,alt:e.alt})),
        visibleMedia:[...pane.querySelectorAll('img,video,canvas')].filter(e=>{const b=e.getBoundingClientRect(),s=getComputedStyle(e);return b.width>0&&b.height>0&&b.bottom>r.top&&b.top<r.bottom&&s.visibility!=='hidden'&&s.display!=='none'}).map(e=>{const b=e.getBoundingClientRect();return{tag:e.tagName,src:e.currentSrc||e.src||'',poster:e.poster||'',alt:e.alt||'',box:{x:b.x,y:b.y,width:b.width,height:b.height},html:(e.closest('picture')||e.parentElement).outerHTML.slice(0,60000)}})};
    },selector);
    if(m.url!==expectedURL||m.viewport.width!==width)throw new Error('Unexpected nested reference URL or width.');
    if(hash)m.draft_sha256=hash;
    // Explicit CSS viewport clip avoids a native-window thumbnail and the
    // host's device-pixel ratio. Document scroll is always zero for this pane.
    const shot=await cdp.send('Page.captureScreenshot',{format:'png',captureBeyondViewport:false,fromSurface:true,clip:{x:0,y:0,width,height,scale:1}});
    const bytes=Buffer.from(shot.data,'base64');
    m.capture_method='CDP explicit CSS viewport clip; element scroll stays separate from document scroll';
    const ext=bytes[0]===0xff&&bytes[1]===0xd8?'jpg':'png';
    m.screenshot=slug+'-oct10-'+side+'-'+width+'-phase-'+frames.length+'.'+ext;
    m.screenshot_format=ext;
    await fs.writeFile(work+'/'+m.screenshot,bytes);frames.push(m);
    await fs.writeFile(prefix+'-phases.json',JSON.stringify(frames,null,2)+'\n');
    const c=m.coverage,remaining=c.extent-c.visible_extent-c.offset;
    if(remaining<=1){done=true;break;}
    if(i===maxPhases-1||Date.now()-began>35000)break;
    if(!await wheel(Math.min(c.visible_extent-32,remaining)))break;
  }
  if(done){
    const r=await tab.playwright.evaluate(()=>{const html=document.documentElement.outerHTML;return{url:location.href,observed_at:new Date().toISOString(),viewport:{width:innerWidth,height:innerHeight},scrollY,htmlParts:Array.from({length:Math.ceil(html.length/80000)},(_,i)=>html.slice(i*80000,(i+1)*80000)),html_length:html.length,images:[...document.images].map(e=>({alt:e.alt,src:e.currentSrc||e.src,complete:e.complete,naturalWidth:e.naturalWidth})),stylesheets:[...document.querySelectorAll('link[rel="stylesheet"]')].map(e=>e.href),inlineStyleRules:[...document.styleSheets].map(s=>{const index=[...document.querySelectorAll('style')].indexOf(s.ownerNode);if(index<0||s.ownerNode.textContent.trim())return null;try{const text=[...s.cssRules].map(r=>r.cssText).join('\n');return{index,cssParts:Array.from({length:Math.ceil(text.length/80000)},(_,i)=>text.slice(i*80000,(i+1)*80000))}}catch{return null}}).filter(Boolean)}});
    r.html_sha256=crypto.createHash('sha256').update(r.htmlParts.join('')).digest('hex');
    r.coverage=frames.at(-1).coverage;
    await fs.writeFile(prefix+'-reference.json',JSON.stringify(r,null,2)+'\n');
  }
  return{side,width,done,phases:frames.length,coverage:frames.at(-1)?.coverage,brokenVisibleImages:frames.reduce((n,p)=>n+p.brokenVisibleImages.length,0),overflow:frames.some(p=>p.bodyWidth>width)};
}
