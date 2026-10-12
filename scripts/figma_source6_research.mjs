// Source-only research helper. Invoke browser operations only through CUA handles.
import fs from 'node:fs/promises';
import crypto from 'node:crypto';
const base='/Users/pchang01/Documents/mygithub/awesome-ai-web-design/.stitch-work/current-official';
const digest=data=>crypto.createHash('sha256').update(data).digest('hex');
export async function nativeScreenshot(tab,width,height){
  const bytes=Buffer.from(await tab.screenshot({fullPage:false}));
  let size;
  if(bytes[0]===0x89&&bytes[1]===0x50)size=[bytes.readUInt32BE(16),bytes.readUInt32BE(20)];
  else{let p=2;while(p<bytes.length){if(bytes[p]!==255){p++;continue;}const m=bytes[p+1],n=bytes.readUInt16BE(p+2);if([192,193,194,195,197,198,199,201,202,203,205,206,207].includes(m)){size=[bytes.readUInt16BE(p+7),bytes.readUInt16BE(p+5)];break;}p+=2+n;}}
  if(!size||size[0]!==width||size[1]!==height)throw new Error('Actual native raster size '+JSON.stringify(size)+' differs from '+width+'×'+height);
  return bytes;
}
export async function enrich(tab,slug,width){
  const path=base+'/'+slug+'-oct10-official-'+width+'-reference.json';
  const extra=await tab.playwright.evaluate(()=>({title:document.title,document_language:document.documentElement.lang,cssomStylesheets:[...document.styleSheets].map((s,i)=>{let text='',error=null;try{text=[...s.cssRules].map(r=>r.cssText).join('\n');}catch(e){error=String(e);}return{index:i,href:s.href||null,ownerTag:s.ownerNode?.tagName||null,readable:error===null,error,css_length:text.length,cssParts:Array.from({length:Math.ceil(text.length/80000)},(_,n)=>text.slice(n*80000,(n+1)*80000))};}),videos:[...document.querySelectorAll('video')].map(e=>({src:e.currentSrc||e.src,poster:e.poster,autoplay:e.autoplay,loop:e.loop,muted:e.muted,readyState:e.readyState})),canvases:[...document.querySelectorAll('canvas')].map(e=>({width:e.width,height:e.height,cssWidth:e.getBoundingClientRect().width,cssHeight:e.getBoundingClientRect().height})),bodyTextParts:(()=>{const text=document.body.innerText;return Array.from({length:Math.ceil(text.length/80000)},(_,n)=>text.slice(n*80000,(n+1)*80000));})()}));
  for(const s of extra.cssomStylesheets)s.css_sha256=digest(s.cssParts.join(''));
  const ref=JSON.parse(await fs.readFile(path,'utf8'));
  Object.assign(ref,extra,{cssom_observed_at:new Date().toISOString(),source_research_only:true});
  await fs.writeFile(path,JSON.stringify(ref,null,2)+'\n');
  return{width,title:extra.title,language:extra.document_language,cssom:extra.cssomStylesheets.length,cssom_unreadable:extra.cssomStylesheets.filter(x=>!x.readable).length,videos:extra.videos.length,canvases:extra.canvases.length};
}
export async function topSnapshot(tab,cdp,viewport,slug,url,width,height){
  await viewport.set({width,height});
  await cdp.send('Emulation.setDeviceMetricsOverride',{width,height,deviceScaleFactor:1,mobile:false});
  await cdp.send('Page.bringToFront',{});
  const before=await tab.playwright.evaluate(()=>scrollY);
  if(before>0)await cdp.send('Input.dispatchMouseEvent',{type:'mouseWheel',x:4,y:Math.min(height-80,400),deltaX:0,deltaY:-before});
  await tab.playwright.domSnapshot();
  const r=await tab.playwright.evaluate(()=>{const html=document.documentElement.outerHTML;return{url:location.href,observed_at:new Date().toISOString(),viewport:{width:innerWidth,height:innerHeight},scrollY,bodyHeight:document.documentElement.scrollHeight,htmlParts:Array.from({length:Math.ceil(html.length/80000)},(_,i)=>html.slice(i*80000,(i+1)*80000)),html_length:html.length,images:[...document.images].map(e=>({alt:e.alt,src:e.currentSrc||e.src,complete:e.complete,naturalWidth:e.naturalWidth})),stylesheets:[...document.querySelectorAll('link[rel="stylesheet"]')].map(e=>e.href)};});
  if(r.url!==url||r.viewport.width!==width||r.viewport.height!==height||Math.abs(r.scrollY)>1)throw new Error('Source top URL/viewport/scroll guard failed');
  const bytes=await nativeScreenshot(tab,width,height);
  r.html_sha256=digest(r.htmlParts.join(''));
  const name=slug+'-oct10-official-'+width+'-top';
  r.screenshot=name+'.jpg';r.screenshot_sha256=digest(bytes);r.source_research_only=true;
  await fs.writeFile(base+'/'+name+'.jpg',bytes);
  await fs.writeFile(base+'/'+name+'-reference.json',JSON.stringify(r,null,2)+'\n');
  return{width,scrollY:r.scrollY,bodyHeight:r.bodyHeight,html_length:r.html_length,screenshot:r.screenshot};
}
export async function inventory(tab,slug,width){
  const capability=await tab.capabilities.get('pageAssets');
  const data=await capability.list();
  await fs.writeFile(base+'/'+slug+'-oct10-asset-inventory-'+width+'.json',JSON.stringify(data,null,2)+'\n');
  return data;
}
export async function bundle(tab,slug,inventory){
  const capability=await tab.capabilities.get('pageAssets');
  const data=await capability.bundle({inventoryId:inventory.id,kinds:['image','font','stylesheet','video']});
  await fs.writeFile(base+'/'+slug+'-oct10-asset-inventory.json',JSON.stringify(inventory,null,2)+'\n');
  await fs.writeFile(base+'/'+slug+'-oct10-asset-bundle.json',JSON.stringify(data,null,2)+'\n');
  return data.summary;
}
