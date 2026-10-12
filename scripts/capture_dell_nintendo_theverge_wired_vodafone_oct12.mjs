// Invoke exclusively inside the documented CUA REPL. All browser actions use its supported API.
import fs from 'node:fs/promises';
import crypto from 'node:crypto';
const work='/Users/pchang01/Documents/mygithub/awesome-ai-web-design/.stitch-work/current-official';
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const allowed=new Set(['dell-1996','nintendo-2001','theverge','wired','vodafone']);
function dimensions(bytes){
 if(bytes.subarray(0,8).equals(Buffer.from([137,80,78,71,13,10,26,10])))return{width:bytes.readUInt32BE(16),height:bytes.readUInt32BE(20),format:'png'};
 if(bytes[0]!==255||bytes[1]!==216)throw new Error('Unknown native raster format');
 let p=2;while(p<bytes.length){if(bytes[p]!==255){p++;continue;}while(bytes[p]===255)p++;const m=bytes[p++];if(m===217||m===218)break;if(m===1||(m>=208&&m<=215))continue;const n=bytes.readUInt16BE(p);if([192,193,194,195,197,198,199,201,202,203,205,206,207].includes(m))return{width:bytes.readUInt16BE(p+5),height:bytes.readUInt16BE(p+3),format:'jpg'};p+=n;}
 throw new Error('JPEG native dimensions unavailable');
}
function validateBrand(brand){if(!allowed.has(brand))throw new Error('Outside owned source research scope');}
export async function preserveHistory(brand){
 validateBrand(brand);const dir=work+'/'+brand+'-oct12-private-source-history';await fs.mkdir(dir,{recursive:true});
 let inventory;try{return JSON.parse(await fs.readFile(dir+'/manifest.json','utf8'));}catch{}
 const names=(await fs.readdir(work)).filter(n=>n.startsWith(brand+'-')&&!n.includes('-oct12-')&&!n.includes('-oct10-')&&(/reference|browser-export|source(?:\.|-)|official/.test(n)));
 const files=[];for(const n of names){const src=work+'/'+n;if(!(await fs.stat(src)).isFile())continue;const b=await fs.readFile(src);await fs.writeFile(dir+'/'+n,b);files.push({original:n,privateCopy:brand+'-oct12-private-source-history/'+n,bytes:b.length,sha256:hash(b)});}
 inventory={observedAt:new Date().toISOString(),brand,privateResearchOnly:true,originalsUnmodified:true,files};await fs.writeFile(dir+'/manifest.json',JSON.stringify(inventory,null,2)+'\n');return{brand,files:files.length};
}
export async function reloadAndRecord(tab,cdp,brand,width,height,expectedURL){
 validateBrand(brand);await cdp.send('Network.enable',{});const before=(await cdp.readEvents({methods:['Network.responseReceived']})).cursor;
 await tab.reload();await tab.playwright.domSnapshot();let after=before,documentEvent;
 for(let i=0;i<8;i++){const events=await cdp.readEvents({afterSequence:after,methods:['Network.responseReceived'],limit:1000});for(const e of events.events)if(e.params?.type==='Document'&&e.params?.response?.url===expectedURL)documentEvent=e.params;after=events.cursor;if(!events.hasMore)break;}
 const state=await tab.playwright.evaluate(()=>({url:location.href,width:innerWidth,height:innerHeight,bodyHeight:document.documentElement.scrollHeight,title:document.title}));
 const record={observedAt:new Date().toISOString(),url:expectedURL,viewport:{width,height},state,status:documentEvent?.response?.status??null,statusProvenance:documentEvent?'CUA supported CDP Network.responseReceived':'Response event unavailable; rendered page alone is not an HTTP status assertion',requestId:documentEvent?.requestId};
 await fs.writeFile(work+'/'+brand+'-oct10-official-'+width+'-response.json',JSON.stringify(record,null,2)+'\n');
 if([403,404,429].includes(record.status))throw new Error('Restricted HTTP response '+record.status+'; do not retry or change URL');
 if(state.url!==expectedURL||state.width!==width||state.height!==height)throw new Error('Official URL/viewport changed');
 if(documentEvent){try{const response=await cdp.send('Network.getResponseBody',{requestId:documentEvent.requestId});const bytes=Buffer.from(response.body,response.base64Encoded?'base64':'utf8');const name=brand+'-oct10-official-'+width+'-response.html';await fs.writeFile(work+'/'+name,bytes);record.documentResponse={file:name,bytes:bytes.length,sha256:hash(bytes)};}catch(e){record.responseBodyLimitation=String(e.message).slice(0,400);}await fs.writeFile(work+'/'+brand+'-oct10-official-'+width+'-response.json',JSON.stringify(record,null,2)+'\n');}
 return record;
}
export async function reference(tab,brand,width,height,expectedURL){
 const r=await tab.playwright.evaluate(()=>{const html=document.documentElement.outerHTML;const styles=[...document.querySelectorAll('style')];return{url:location.href,observed_at:new Date().toISOString(),viewport:{width:innerWidth,height:innerHeight,dpr:devicePixelRatio},scrollY,bodyHeight:document.documentElement.scrollHeight,bodyWidth:document.documentElement.scrollWidth,title:document.title,language:document.documentElement.lang,fontStatus:document.fonts.status,htmlParts:Array.from({length:Math.ceil(html.length/80000)},(_,i)=>html.slice(i*80000,(i+1)*80000)),html_length:html.length,images:[...document.images].map(e=>({alt:e.alt,src:e.currentSrc||e.src,srcset:e.srcset,complete:e.complete,naturalWidth:e.naturalWidth,naturalHeight:e.naturalHeight})),media:[...document.querySelectorAll('video,source')].map(e=>({tag:e.tagName,src:e.currentSrc||e.src||'',poster:e.poster||'',type:e.type||''})),stylesheets:[...document.querySelectorAll('link[rel="stylesheet"]')].map(e=>e.href),cssom:[...document.styleSheets].map((s,stylesheetIndex)=>{const styleIndex=styles.indexOf(s.ownerNode);try{const text=[...s.cssRules].map(r=>r.cssText).join('\n');return{stylesheetIndex,styleIndex,href:s.href||'',disabled:s.disabled,ruleCount:s.cssRules.length,cssParts:Array.from({length:Math.ceil(text.length/80000)},(_,i)=>text.slice(i*80000,(i+1)*80000)),css_length:text.length}}catch(e){return{stylesheetIndex,styleIndex,href:s.href||'',error:e.name+': '+e.message}}})};});
 if(r.url!==expectedURL||r.viewport.width!==width||r.viewport.height!==height)throw new Error('Reference URL/viewport mismatch');const html=r.htmlParts.join('');if(html.length!==r.html_length||!html.endsWith('</html>')||!html.includes('</body>'))throw new Error('Incomplete DOM export');r.html_sha256=hash(html);
 for(const s of r.cssom)if(s.cssParts){const css=s.cssParts.join('');if(css.length!==s.css_length)throw new Error('Incomplete CSSOM export');s.sha256=hash(css);}
 r.inlineStyleRules=r.cssom.filter(s=>s.styleIndex>=0&&s.cssParts).map(s=>({index:s.styleIndex,cssParts:s.cssParts,sha256:s.sha256}));
 const prefix=brand+'-oct10-official-'+width;await fs.writeFile(work+'/'+prefix+'-reference.json',JSON.stringify(r,null,2)+'\n');await fs.writeFile(work+'/'+prefix+'-rendered-source.html',html);return{brand,width,htmlLength:r.html_length,htmlSha256:r.html_sha256,cssSheets:r.cssom.length,accessibleCSS:r.cssom.filter(s=>s.cssParts).length,images:r.images.length,unreadyImages:r.images.filter(i=>!i.complete||!i.naturalWidth).length};
}
export async function capture(tab,cdp,brand,width,height,expectedURL,{reset=false,maxPhases=5}={}){
 validateBrand(brand);const prefix=brand+'-oct10-official-'+width;let phases=[];if(!reset){try{phases=JSON.parse(await fs.readFile(work+'/'+prefix+'-phases.json','utf8'));}catch{}}
 async function wheel(delta){await cdp.send('Input.dispatchMouseEvent',{type:'mouseWheel',x:width-30,y:height-60,deltaX:0,deltaY:delta});await tab.playwright.domSnapshot();}
 const start=await tab.playwright.evaluate(()=>({y:scrollY,height:document.documentElement.scrollHeight}));if(reset&&start.y)await wheel(-start.y);
 if(!reset&&phases.length){const last=phases.at(-1);if(Math.abs(start.y-last.scrollY)>1)throw new Error('Source resume offset changed');const remaining=start.height-height-start.y;if(remaining>1)await wheel(Math.min(height,remaining));}
 let done=false;const began=Date.now();for(let count=0;count<maxPhases;count++){
  const m=await tab.playwright.evaluate(()=>({url:location.href,observed_at:new Date().toISOString(),viewport:{width:innerWidth,height:innerHeight,dpr:devicePixelRatio},scrollY,bodyHeight:document.documentElement.scrollHeight,bodyWidth:document.documentElement.scrollWidth,fontStatus:document.fonts.status,prefersReducedMotion:matchMedia('(prefers-reduced-motion:reduce)').matches,headings:[...document.querySelectorAll('h1,h2,h3')].map(e=>{const b=e.getBoundingClientRect(),s=getComputedStyle(e);return{text:e.innerText.trim()||e.textContent.trim(),box:{x:b.x,y:b.y+scrollY,width:b.width,height:b.height},font:s.fontFamily,size:s.fontSize,lineHeight:s.lineHeight,weight:s.fontWeight,visible:b.height>0&&b.bottom>0&&b.top<innerHeight}}),visibleMedia:[...document.querySelectorAll('img,video,canvas')].filter(e=>{const b=e.getBoundingClientRect(),s=getComputedStyle(e);return b.width>1&&b.height>1&&Math.min(b.right,innerWidth)-Math.max(b.left,0)>1&&Math.min(b.bottom,innerHeight)-Math.max(b.top,0)>1&&s.display!=='none'&&s.visibility!=='hidden'&&s.opacity!=='0'}).map(e=>{const b=e.getBoundingClientRect();return{tag:e.tagName,src:e.currentSrc||e.src||'',poster:e.poster||'',alt:e.alt||'',loaded:e.tagName==='IMG'?e.complete&&!!e.naturalWidth:null,box:{x:b.x,y:b.y+scrollY,width:b.width,height:b.height}}})}));
  if(m.url!==expectedURL||m.viewport.width!==width||m.viewport.height!==height||(!phases.length&&Math.abs(m.scrollY)>1))throw new Error('Wrong official source viewport/URL/top');
  const bytes=Buffer.from(await tab.screenshot({fullPage:false})),raster=dimensions(bytes);const name=prefix+'-phase-'+phases.length+'.'+raster.format;await fs.writeFile(work+'/'+name,bytes);
  const guard=await tab.playwright.evaluate(()=>({url:location.href,width:innerWidth,height:innerHeight,scrollY,bodyHeight:document.documentElement.scrollHeight}));
  if(raster.width!==width||raster.height!==height){await fs.writeFile(work+'/'+prefix+'-rejected-raster.json',JSON.stringify({observedAt:new Date().toISOString(),file:name,raster,requested:{width,height},state:m,guard,acceptedAsEvidence:false},null,2)+'\n');throw new Error('Native raster dimensions do not match requested full viewport');}
  if(guard.url!==expectedURL||guard.width!==width||guard.height!==height||Math.abs(guard.scrollY-m.scrollY)>1||Math.abs(guard.bodyHeight-m.bodyHeight)>1)throw new Error('Source layout/offset changed during screenshot; original retained but not a valid phase');
  m.screenshot=name;m.screenshot_format=raster.format;m.screenshotSha256=hash(bytes);m.nativeRasterDimensions=raster;m.postScreenshotGuard=guard;phases.push(m);await fs.writeFile(work+'/'+prefix+'-phases.json',JSON.stringify(phases,null,2)+'\n');
  const remaining=m.bodyHeight-height-m.scrollY;if(remaining<=1){done=true;break;}if(count===maxPhases-1||Date.now()-began>35000)break;await wheel(Math.min(height,remaining));
 }
 let exported;if(done)exported=await reference(tab,brand,width,height,expectedURL);return{brand,width,done,phases:phases.length,scrollY:phases.at(-1)?.scrollY,bodyHeight:phases.at(-1)?.bodyHeight,noOverflow:phases.every(p=>p.bodyWidth<=width),unreadyVisibleImages:phases.reduce((n,p)=>n+p.visibleMedia.filter(m=>m.tag==='IMG'&&!m.loaded).length,0),exported};
}
