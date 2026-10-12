// Run only inside the documented CUA REPL, with its tab and cdp handles.
import fs from 'node:fs/promises';
import crypto from 'node:crypto';
const work='/Users/pchang01/Documents/mygithub/awesome-ai-web-design/.stitch-work/current-official';
export async function capture(tab,cdp,slug,side,width,height,expectedURL,{reset=false,maxPhases=6,settleAfterScroll,scrollBy,screenshot}={}){
  const prefix=work+'/'+slug+'-oct10-'+side+'-'+width;
  await cdp.send('Emulation.setDeviceMetricsOverride',{width,height,deviceScaleFactor:1,mobile:false});
  await cdp.send('Page.bringToFront',{});
  if(reset)await tab.playwright.domSnapshot();
  async function wheel(delta){
    const before=await tab.playwright.evaluate(()=>scrollY);
    if(scrollBy)await scrollBy(delta);
    else await cdp.send('Input.dispatchMouseEvent',{type:'mouseWheel',x:Math.min(width-50,1000),y:height-80,deltaX:0,deltaY:delta});
    if(settleAfterScroll)await settleAfterScroll();
    for(let observations=0;observations<4;observations++){
      await tab.playwright.domSnapshot();
      const after=await tab.playwright.evaluate(()=>scrollY);
      if(Math.abs(after-before)>0.5)return true;
    }
    return false;
  }
  let phases=[];
  if(!reset){try{phases=JSON.parse(await fs.readFile(prefix+'-phases.json','utf8'));}catch{}}
  const start=await tab.playwright.evaluate(()=>({scrollY}));
  await cdp.send('Input.dispatchMouseEvent',{type:'mouseMoved',x:width-10,y:height-10});
  if(reset&&start.scrollY>0)await wheel(-start.scrollY);
  if(reset){const top=await tab.playwright.evaluate(()=>({scrollY}));if(Math.abs(top.scrollY)>2)throw new Error('Top viewport has not settled; no complete-coverage claim may be made.');}
  if(!reset&&phases.length){const last=phases.at(-1);const remaining=last.bodyHeight-height-last.scrollY;if(remaining>1&&Math.abs(start.scrollY-last.scrollY)<2){if(!await wheel(Math.min(height,remaining)))return{side,width,done:false,phases:phases.length,pendingScroll:true};}}
  let done=false;
  const draft_sha256=side==='local'?crypto.createHash('sha256').update(await fs.readFile(work+'/'+slug+'.html')).digest('hex'):undefined;
  let browser_build_fingerprint;
  if(side==='local'){
    const current=await fs.readFile(work+'/'+slug+'.html','utf8');
    const expected=current.match(/<meta name="study-build-fingerprint" content="([a-f0-9]+)">/)?.[1];
    browser_build_fingerprint=await tab.playwright.evaluate(()=>document.querySelector('meta[name="study-build-fingerprint"]')?.content);
    if(!expected||expected!==browser_build_fingerprint)throw new Error('Browser preview is stale or differs from the current build fingerprint');
  }
  const began=Date.now();
  for(let count=0;count<maxPhases;count++){
    const m=await tab.playwright.evaluate(()=>({url:location.href,observed_at:new Date().toISOString(),viewport:{width:innerWidth,height:innerHeight},scrollY,bodyHeight:document.documentElement.scrollHeight,bodyWidth:document.documentElement.scrollWidth,headings:[...document.querySelectorAll('h1,h2,h3')].map(e=>{const b=e.getBoundingClientRect(),s=getComputedStyle(e);return{text:e.innerText?.trim()||e.textContent.trim(),box:{x:b.x,y:b.y+scrollY,width:b.width,height:b.height},font:s.fontFamily,size:s.fontSize,weight:s.fontWeight,lineHeight:s.lineHeight,color:s.color,visible:b.height>0&&b.bottom>0&&b.top<innerHeight}}),brokenVisibleImages:[...document.images].filter(e=>{const b=e.getBoundingClientRect(),s=getComputedStyle(e);return !!(e.currentSrc||e.getAttribute('src'))&&b.width>0&&b.height>0&&b.bottom>0&&b.top<innerHeight&&b.right>0&&b.left<innerWidth&&s.visibility!=='hidden'&&s.display!=='none'&&e.complete&&!e.naturalWidth}).map(e=>({src:e.currentSrc||e.src,alt:e.alt}))}));
    m.prefers_reduced_motion=await tab.playwright.evaluate(()=>matchMedia('(prefers-reduced-motion:reduce)').matches);
    if(m.url!==expectedURL||m.viewport.width!==width||m.viewport.height!==height)throw new Error('Unexpected reference URL or viewport');
    if(draft_sha256){m.draft_sha256=draft_sha256;m.browser_build_fingerprint=browser_build_fingerprint;}
    if(side==='official')m.visibleMedia=await tab.playwright.evaluate(()=>[...document.querySelectorAll('img,video,canvas')].filter(e=>{const b=e.getBoundingClientRect(),s=getComputedStyle(e);return b.width>0&&b.height>0&&b.bottom>0&&b.top<innerHeight&&s.visibility!=='hidden'&&s.display!=='none'}).map(e=>{const b=e.getBoundingClientRect();const path=[];let n=e;while(n&&n!==document.documentElement){const p=n.parentElement;if(!p)break;path.unshift(n.tagName.toLowerCase()+':nth-child('+([...p.children].indexOf(n)+1)+')');n=p;}return{tag:e.tagName,selector:'html>'+path.join('>'),src:e.currentSrc||e.src||'',poster:e.poster||'',alt:e.alt||'',box:{x:b.x,y:b.y+scrollY,width:b.width,height:b.height},html:(e.closest('picture')||e.parentElement).outerHTML.slice(0,60000)}}));
    const shot=screenshot?await screenshot():await cdp.send('Page.captureScreenshot',{format:'png',captureBeyondViewport:true,fromSurface:true,clip:{x:0,y:m.scrollY,width,height,scale:1}});
    const bytes=screenshot?Buffer.from(shot):Buffer.from(shot.data,'base64');
    const format=bytes[0]===0xff&&bytes[1]===0xd8?'jpg':'png';
    const name=slug+'-oct10-'+side+'-'+width+'-phase-'+phases.length+'.'+format;
    await fs.writeFile(work+'/'+name,bytes);m.screenshot=name;m.screenshot_format=format;phases.push(m);
    await fs.writeFile(prefix+'-phases.json',JSON.stringify(phases,null,2)+'\n');
    const remaining=m.bodyHeight-height-m.scrollY;
    if(remaining<=1){done=true;break;}
    if(count===maxPhases-1||Date.now()-began>35000)break;
    if(!await wheel(Math.min(height,remaining)))break;
  }
  if(done){
    const r=await tab.playwright.evaluate(()=>{const html=document.documentElement.outerHTML;return{url:location.href,observed_at:new Date().toISOString(),viewport:{width:innerWidth,height:innerHeight},scrollY,htmlParts:Array.from({length:Math.ceil(html.length/80000)},(_,i)=>html.slice(i*80000,(i+1)*80000)),html_length:html.length,images:[...document.images].map(e=>({alt:e.alt,src:e.currentSrc||e.src,complete:e.complete,naturalWidth:e.naturalWidth})),stylesheets:[...document.querySelectorAll('link[rel="stylesheet"]')].map(e=>e.href),inlineStyleRules:[...document.styleSheets].map(s=>{const index=[...document.querySelectorAll('style')].indexOf(s.ownerNode);if(index<0||s.ownerNode.textContent.trim())return null;try{const text=[...s.cssRules].map(r=>r.cssText).join('\n');return{index,cssParts:Array.from({length:Math.ceil(text.length/80000)},(_,i)=>text.slice(i*80000,(i+1)*80000))}}catch{return null}}).filter(Boolean)}});
    r.html_sha256=crypto.createHash('sha256').update(r.htmlParts.join('')).digest('hex');
    await fs.writeFile(prefix+'-reference.json',JSON.stringify(r,null,2)+'\n');
  }
  return{side,width,done,phases:phases.length,scrollY:phases.at(-1)?.scrollY,bodyHeight:phases.at(-1)?.bodyHeight,brokenVisibleImages:phases.reduce((n,p)=>n+p.brokenVisibleImages.length,0),overflow:phases.some(p=>p.bodyWidth>width)};
}
