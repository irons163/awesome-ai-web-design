// Invoke only inside CUA REPL. Normal reload/input, readonly DOM, native screenshot.
import fs from 'node:fs/promises';
import crypto from 'node:crypto';
const work='/Users/pchang01/Documents/mygithub/awesome-ai-web-design/.stitch-work/current-official';
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
export async function reloadAndBind(tab,cdp,brand,width,height){
 const url='http://127.0.0.1:4173/.stitch-work/current-official/'+brand+'.html';
 const current=await fs.readFile(work+'/'+brand+'.html'),sha=hash(current);
 await cdp.send('Network.enable',{});
 const cursor=(await cdp.readEvents({methods:['Network.responseReceived']})).cursor;
 await tab.reload();await tab.playwright.domSnapshot();
 let after=cursor,documentEvent;
 for(let page=0;page<5;page++){
  const events=await cdp.readEvents({afterSequence:after,methods:['Network.responseReceived'],limit:1000});
  for(const e of events.events)if(e.params.type==='Document'&&e.params.response.url===url)documentEvent=e.params;
  after=events.cursor;if(!events.hasMore)break;
 }
 if(!documentEvent)throw new Error('No exact local document response observed');
 const response=await cdp.send('Network.getResponseBody',{requestId:documentEvent.requestId});
 const bytes=Buffer.from(response.body,response.base64Encoded?'base64':'utf8');
 if(hash(bytes)!==sha)throw new Error('Loaded document bytes do not match current preview file');
 const state=await tab.playwright.evaluate(()=>({url:location.href,width:innerWidth,height:innerHeight,bodyHeight:document.documentElement.scrollHeight,fontStatus:document.fonts.status,allImages:document.images.length,pendingImages:[...document.images].filter(e=>!e.complete).length,headings:[...document.querySelectorAll('h1,h2,h3')].map(e=>e.innerText.trim())}));
 if(state.url!==url||state.width!==width||state.height!==height)throw new Error('Reloaded document URL/viewport mismatch');
 const record={observedAt:new Date().toISOString(),url,width,height,requestId:documentEvent.requestId,status:documentEvent.response.status,fromDiskCache:documentEvent.response.fromDiskCache||false,documentBytes:bytes.length,documentResponseSha256:hash(bytes),currentFileSha256:sha,exactByteEquality:bytes.equals(current),state};
 await fs.writeFile(work+'/'+brand+'-oct12-current-'+width+'-loaded-response.json',JSON.stringify(record,null,2)+'\n');
 return{sha,bytes:bytes.length,exactByteEquality:true,state};
}
export async function capture(tab,cdp,brand,width,height,{reset=false,maxPhases=6}={}){
 const prefix=brand+'-oct12-current-'+width,url='http://127.0.0.1:4173/.stitch-work/current-official/'+brand+'.html';
 const sha=hash(await fs.readFile(work+'/'+brand+'.html'));
 let phases=[];if(!reset){try{phases=JSON.parse(await fs.readFile(work+'/'+prefix+'-phases.json','utf8'))}catch{}}
 async function wheel(d){await cdp.send('Input.dispatchMouseEvent',{type:'mouseWheel',x:width-30,y:height-60,deltaX:0,deltaY:d});await tab.playwright.domSnapshot();}
 const start=await tab.playwright.evaluate(()=>({y:scrollY,height:document.documentElement.scrollHeight}));
 if(reset&&start.y)await wheel(-start.y);
 if(!reset&&phases.length){const last=phases.at(-1);if(Math.abs(start.y-last.scrollY)>1)throw new Error('Resume scroll offset changed');const remaining=last.bodyHeight-height-last.scrollY;if(remaining>1)await wheel(Math.min(height,remaining));}
 let done=false;
 for(let i=0;i<maxPhases;i++){
  const m=await tab.playwright.evaluate(()=>({url:location.href,observed_at:new Date().toISOString(),viewport:{width:innerWidth,height:innerHeight,dpr:devicePixelRatio},scrollY,bodyHeight:document.documentElement.scrollHeight,bodyWidth:document.documentElement.scrollWidth,fontStatus:document.fonts.status,headings:[...document.querySelectorAll('h1,h2,h3')].map(e=>{const b=e.getBoundingClientRect(),s=getComputedStyle(e);return{text:e.innerText.trim(),box:{x:b.x,y:b.y+scrollY,width:b.width,height:b.height},font:s.fontFamily,size:s.fontSize,lineHeight:s.lineHeight,visible:b.height>0&&b.bottom>0&&b.top<innerHeight}}),images:[...document.images].map(e=>{const b=e.getBoundingClientRect();return{src:e.currentSrc||e.src,alt:e.alt,loaded:e.complete&&!!e.naturalWidth,visible:b.width>0&&b.height>0&&b.bottom>0&&b.top<innerHeight}})}));
  if(m.url!==url||m.viewport.width!==width||m.viewport.height!==height||(!phases.length&&m.scrollY!==0))throw new Error('Wrong current page or viewport/top offset');
  if(hash(await fs.readFile(work+'/'+brand+'.html'))!==sha)throw new Error('Preview changed during capture');
  m.draft_sha256=sha;
  const bytes=Buffer.from(await tab.screenshot({fullPage:false}));
  const guard=await tab.playwright.evaluate(()=>({url:location.href,width:innerWidth,height:innerHeight,scrollY,bodyHeight:document.documentElement.scrollHeight}));
  if(guard.url!==url||guard.width!==width||guard.height!==height||Math.abs(guard.scrollY-m.scrollY)>1||Math.abs(guard.bodyHeight-m.bodyHeight)>1)throw new Error('Native screenshot layout changed');
  if(hash(await fs.readFile(work+'/'+brand+'.html'))!==sha)throw new Error('Preview changed after screenshot');
  const format=bytes[0]===0xff&&bytes[1]===0xd8?'jpg':'png';m.screenshot=prefix+'-phase-'+phases.length+'.'+format;m.screenshot_format=format;m.screenshotSha256=hash(bytes);m.postScreenshotGuard=guard;
  await fs.writeFile(work+'/'+m.screenshot,bytes);phases.push(m);await fs.writeFile(work+'/'+prefix+'-phases.json',JSON.stringify(phases,null,2)+'\n');
  const remaining=m.bodyHeight-height-m.scrollY;if(remaining<=1){done=true;break}if(i===maxPhases-1)break;await wheel(Math.min(height,remaining));
 }
 return{brand,width,done,phases:phases.length,y:phases.at(-1).scrollY,bodyHeight:phases.at(-1).bodyHeight,captureSha256:sha,images:phases.at(-1).images.length,imagesNotReady:phases.at(-1).images.filter(e=>!e.loaded).length,noOverflow:phases.every(p=>p.bodyWidth===width)};
}
export async function observeOfficialTop(tab,brand,width,height,expectedURL){
 await tab.playwright.domSnapshot();
 const r=await tab.playwright.evaluate(()=>{const html=document.documentElement.outerHTML;return{url:location.href,observed_at:new Date().toISOString(),viewport:{width:innerWidth,height:innerHeight,dpr:devicePixelRatio},scrollY,bodyHeight:document.documentElement.scrollHeight,bodyWidth:document.documentElement.scrollWidth,fontStatus:document.fonts.status,htmlParts:Array.from({length:Math.ceil(html.length/80000)},(_,i)=>html.slice(i*80000,(i+1)*80000)),html_length:html.length,headings:[...document.querySelectorAll('h1,h2,h3')].map(e=>{const b=e.getBoundingClientRect();return{text:e.innerText.trim()||e.textContent.trim(),box:{x:b.x,y:b.y+scrollY,width:b.width,height:b.height}}}),images:[...document.images].map(e=>({src:e.currentSrc||e.src,alt:e.alt,complete:e.complete,naturalWidth:e.naturalWidth})),stylesheets:[...document.querySelectorAll('link[rel="stylesheet"]')].map(e=>e.href)};});
 if(r.url!==expectedURL||r.viewport.width!==width||r.viewport.height!==height||Math.abs(r.scrollY)>2)throw new Error('Fresh source top URL/viewport mismatch');
 const html=r.htmlParts.join('');if(html.length!==r.html_length||!html.endsWith('</html>'))throw new Error('Truncated fresh public source');r.html_sha256=hash(html);
 const bytes=Buffer.from(await tab.screenshot({fullPage:false}));
 const guard=await tab.playwright.evaluate(()=>({url:location.href,width:innerWidth,height:innerHeight,scrollY,bodyHeight:document.documentElement.scrollHeight}));
 if(guard.url!==r.url||guard.width!==width||guard.height!==height||Math.abs(guard.scrollY-r.scrollY)>1||guard.bodyHeight!==r.bodyHeight)throw new Error('Fresh source top screenshot changed');
 const ext=bytes[0]===0xff&&bytes[1]===0xd8?'jpg':'png';r.screenshot=brand+'-oct12-official-'+width+'-top.'+ext;r.screenshotSha256=hash(bytes);r.postScreenshotGuard=guard;r.scope='Fresh current source full DOM and one actual top viewport only; not a new complete official-page traversal.';
 await fs.writeFile(work+'/'+r.screenshot,bytes);await fs.writeFile(work+'/'+brand+'-oct12-official-'+width+'-reference.json',JSON.stringify(r,null,2)+'\n');return{url:r.url,width,height,bodyHeight:r.bodyHeight,htmlSha256:r.html_sha256,headings:r.headings.map(h=>h.text),screenshot:r.screenshot,observed_at:r.observed_at,scope:r.scope};
}
