import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {JSDOM, VirtualConsole} from 'jsdom';

const capture = path.resolve(process.argv[2] || '/private/tmp/official-browser-vercel-airbnb-oct10');
const work = path.resolve('.stitch-work/current-official');
const origin = 'https://vercel.com/';
const hash = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const read = name => JSON.parse(fs.readFileSync(path.join(capture, name), 'utf8'));
const write = (name, value) => fs.writeFileSync(path.join(work, name), JSON.stringify(value, null, 2) + '\n');
const parse = html => new JSDOM(html, {virtualConsole:new VirtualConsole()}).window.document;
const allowed = value => /^(data:image\/|https:\/\/(?:vercel\.com|[a-z0-9.-]+\.public\.blob\.vercel-storage\.com)\/)/i.test(value);
const cleanLink = value => {
  const url = new URL(value, origin);
  for (const key of ['tid','gclid','fbclid','li_fat_id','_ga']) url.searchParams.delete(key);
  return url.href;
};
function sanitize(html) {
  const document = parse(html);
  document.querySelectorAll('script,noscript,iframe,object,embed,template,input[type="hidden"],[id^="codex-browser-"]').forEach(e=>e.remove());
  document.querySelectorAll('meta:not([charset]):not([name="viewport"]),link:not([rel="stylesheet"]):not([as="font"])').forEach(e=>e.remove());
  document.querySelectorAll('input,textarea').forEach(e=>{e.removeAttribute('value');if(e.tagName==='TEXTAREA')e.textContent='';});
  document.querySelectorAll('img[src]').forEach(e=>{if(!allowed(new URL(e.getAttribute('src'),origin).href))e.remove();});
  document.querySelectorAll('img:not([src])').forEach(e=>e.remove());
  document.querySelectorAll('*').forEach(e=>[...e.attributes].forEach(a=>{
    if(/^on|nonce|token|csrf|data-(?:cdp|gtm|sentry|zone|prefetch)/i.test(a.name)) e.removeAttribute(a.name);
    else if(a.name==='href'&&!a.value.startsWith('#'))e.setAttribute('href',cleanLink(a.value));
  }));
  const walker=document.createTreeWalker(document,128),comments=[];
  while(walker.nextNode())comments.push(walker.currentNode);
  comments.forEach(e=>e.remove());
  return '<!doctype html>'+document.documentElement.outerHTML;
}
function extension(bytes,kind) {
  const start=bytes.subarray(0,4).toString();
  if(kind==='stylesheet'){if(/^\s*</.test(bytes.toString()))throw new Error('HTML instead of original CSS');return '.css';}
  if(kind==='font'){if(start==='wOF2')return '.woff2';if(start==='wOFF')return '.woff';throw new Error('Invalid original font');}
  if(bytes[0]===255&&bytes[1]===216)return '.jpg';
  if(bytes.subarray(1,4).toString()==='PNG')return '.png';
  if(start==='RIFF')return '.webp';
  if(bytes.subarray(4,8).toString()==='ftyp')return '.avif';
  if(/<svg[\s>]/i.test(bytes.subarray(0,2000).toString()))return '.svg';
  throw new Error('Invalid original image');
}
fs.mkdirSync(path.join(work,'vercel-assets'),{recursive:true});
const references={},screenshots=[],assets=[],failures=[],required=new Set();
const variants=['desktop','mobile','desktop-products-menu','desktop-resources-menu','mobile-menu','mobile-products-menu','mobile-resources-menu'];
for(const variant of variants) {
  const raw=read('vercel-'+variant+'-complete-raw-private.json');
  if(raw.htmlParts.join('').length!==raw.htmlLength||raw.reference_url!==origin)throw new Error('Incomplete or wrong public reference: '+variant);
  const html=sanitize(raw.htmlParts.join('')),document=parse(html);
  if(!document.querySelector('h1')?.textContent.includes('Agentic Infrastructure'))throw new Error('Wrong current homepage');
  raw.htmlParts=html.match(/[\s\S]{1,40000}/g)||[];raw.htmlLength=html.length;raw.html_sha256=hash(html);
  raw.images=raw.images.filter(i=>allowed(i.src));
  raw.links=raw.links.map(l=>({...l,href:cleanLink(l.href)}));
  raw.controls=raw.controls.map(c=>({...c,html:parse(sanitize('<body>'+c.html+'</body>')).body.innerHTML}));
  raw.method='Dated public rendered DOM, computed typography, native screenshots and original visual resources. Scripts, embedded frames, entered values, comments, token and telemetry attributes removed offline. No cookies, storage or private account APIs read.';
  raw.limitations=['Narrow captures use a desktop user agent. Content-visibility and motion can change offscreen layout; only recorded visible states are comparison evidence. CSSOM access returned null; original stylesheet response bytes are retained instead.'];
  for(const i of raw.images)if(!i.src.startsWith('data:'))required.add(i.src);
  for(const e of document.querySelectorAll('link[rel="stylesheet"][href]'))required.add(new URL(e.getAttribute('href'),origin).href);
  for(const e of document.querySelectorAll('[style]'))for(const m of e.getAttribute('style').matchAll(/url\(\s*["']?([^"')]+)["']?\s*\)/g)){
    const url=new URL(m[1],origin).href;if(allowed(url)&&!url.startsWith('data:'))required.add(url);
  }
  const file='vercel-'+variant+'-browser-reference.json';write(file,raw);
  references[variant]={file,observed_at:raw.observed_at,viewport:raw.viewport,html_sha256:raw.html_sha256,bodyHeight:raw.bodyHeight,bodyWidth:raw.bodyWidth};
  for(const frame of (['desktop','mobile'].includes(variant)?['first','full']:['first'])){
    const name='vercel-'+variant+'-'+frame+'.jpg',bytes=fs.readFileSync(path.join(capture,name));
    fs.writeFileSync(path.join(work,name),bytes);screenshots.push({path:name,bytes:bytes.length,sha256:hash(bytes),method:'Original native browser JPEG, unchanged.'});
  }
}
const summaries=[];
for(const variant of ['desktop','mobile']){
  const bundle=read('vercel-'+variant+'-asset-bundle-private.json');summaries.push({variant,...bundle.summary});
  for(const a of bundle.assets){
    if(!allowed(a.url)||a.url.startsWith('data:')||assets.some(x=>x.source_url===a.url))continue;
    const bytes=fs.readFileSync(a.path),sha256=hash(bytes),relative='vercel-assets/'+hash(a.url).slice(0,16)+'-'+sha256.slice(0,8)+extension(bytes,a.kind);
    fs.writeFileSync(path.join(work,relative),bytes);
    assets.push({source_url:a.url,path:relative,kind:a.kind,bytes:bytes.length,sha256,content_type:a.contentType,method:'Native pageAssets bundle; original response bytes unchanged.'});
  }
  for(const failure of bundle.failures)if(allowed(failure.url))failures.push(failure);
  const phases=read('vercel-'+variant+'-scroll-phases.json');write('vercel-'+variant+'-scroll-phases.json',phases);
}
for(const url of [...required].filter(url=>!assets.some(a=>a.source_url===url))){
  if(!/^https:\/\/(?:[a-z0-9.-]+\.public\.blob\.vercel-storage\.com\/[^?]+|vercel\.com\/vc-ap-vercel-marketing\/_next\/static\/immutable\/media\/[^?]+)\.webp$/.test(url))throw new Error('Unobserved resource acquisition path');
  const temporary=path.join(capture,'vercel-original-'+hash(url).slice(0,16));
  if(!fs.existsSync(temporary))execFileSync('curl',['--fail','--silent','--show-error','--compressed','--max-time','30','--output',temporary,url]);
  const bytes=fs.readFileSync(temporary),sha256=hash(bytes),relative='vercel-assets/'+hash(url).slice(0,16)+'-'+sha256.slice(0,8)+extension(bytes,'image');
  fs.writeFileSync(path.join(work,relative),bytes);
  assets.push({source_url:url,path:relative,kind:'image',bytes:bytes.length,sha256,method:'Exact public image URL observed in rendered source DOM; unauthenticated original response bytes unchanged. This inactive resource was not fetched by native pageAssets.'});
}
const missing=[...required].filter(url=>!assets.some(a=>a.source_url===url));
if(missing.length)throw new Error('Required observed resources missing: '+JSON.stringify(missing));
assets.sort((a,b)=>a.path.localeCompare(b.path));
write('vercel-browser-asset-provenance.json',{references,assets,failures,native_summaries:summaries,method:'Only observed public original visual files. No image redrawing, resizing or recompression. Inline original SVG/data images remain in the sanitized DOM.'});
write('vercel-reference.json',{accepted:false,references,screenshots,asset_provenance:'vercel-browser-asset-provenance.json',scope:'Dated desktop and narrow desktop-browser reference, including actual products/resources navigation. Motion, complete interaction, true phones/tablet and production pixel comparison remain separate acceptance tasks.'});
console.log(JSON.stringify({assets:assets.length,bytes:assets.reduce((n,a)=>n+a.bytes,0),references:variants.length,missing}));
