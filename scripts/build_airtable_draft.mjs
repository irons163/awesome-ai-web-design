import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {JSDOM, VirtualConsole} from 'jsdom';

const work=path.resolve('.stitch-work/current-official');
const origin='https://www.airtable.com/';
const read=name=>JSON.parse(fs.readFileSync(path.join(work,name),'utf8'));
const hash=bytes=>crypto.createHash('sha256').update(bytes).digest('hex');
const parse=html=>new JSDOM(html,{virtualConsole:new VirtualConsole()}).window.document;
const provider=read('airtable-stitch-oct10-response.json');
const response=provider.structuredContent||JSON.parse(provider.content.find(x=>x.type==='text').text);
const screens=response.outputComponents.flatMap(x=>x.design?.screens||[]);
if(!screens.length)throw new Error('Current official-targeted native Stitch generation required');
const exports=['airtable-stitch-oct10-desktop-0.html','airtable-stitch-oct10-desktop-0.png'].map(name=>{
  const bytes=fs.readFileSync(path.join(work,name));return{path:name,bytes:bytes.length,sha256:hash(bytes)};
});
const assetRecord=read('airtable-oct10-assets.json');
const assets=new Map(assetRecord.assets.map(a=>[a.source_url,a]));
for(const a of assets.values())if(hash(fs.readFileSync(path.join(work,a.path)))!==a.sha256)throw new Error('Original public asset changed');
const used=new Set();
const observedLogos=new Map(read('airtable-oct10-logo-observations.json').flatMap(r=>r.images).filter(i=>!i.src.startsWith('data:')).map(i=>[i.alt,i.src]));
function url(value,base=origin){
  if(!value||/^(?:data:|#|mailto:|tel:)/i.test(value))return value;
  if(/^javascript:/i.test(value))return '#';
  const absolute=new URL(value,base).href,a=assets.get(absolute);
  if(a){used.add(a.path);return a.path;}return absolute;
}
const css=(text,base=origin)=>text.replace(/url\(\s*(['"]?)(.*?)\1\s*\)/g,(match,quote,value)=>/^(data:|#)/i.test(value)?match:'url("'+url(value,base)+'")');
const references={};
function source(state){
  const filename='airtable-oct10-'+state+'-reference.json';
  const r=read(filename),html=(r.htmlParts||[]).join('');
  if(r.url!==origin||html.length!==r.html_length||!html.endsWith('</html>')||hash(html)!==r.html_sha256)throw new Error('Incomplete or wrong source reference: '+state);
  references[state]={file:filename,observed_at:r.observed_at,viewport:r.viewport,html_sha256:r.html_sha256};
  return{record:r,document:parse(html)};
}
function sanitize(document,reference){
  const lazyFallbacks=new Map();
  document.querySelectorAll('img').forEach(e=>{
    const fallback=e.nextElementSibling?.tagName==='NOSCRIPT'?e.nextElementSibling.querySelector('img'):null;
    if(fallback)lazyFallbacks.set(e,fallback.getAttribute('src'));
  });
  // JSDOM parses noscript fallback images as elements; the live browser does
  // not. Remove them before matching the observed image order.
  document.querySelectorAll('script,noscript,iframe,base,meta[http-equiv],link:not([rel="stylesheet"]),[id^="q-"]').forEach(e=>e.remove());
  document.querySelectorAll('*').forEach(e=>{
    for(const a of [...e.attributes])if(/^on/i.test(a.name)||/^data-airgap/i.test(a.name))e.removeAttribute(a.name);
    for(const name of ['src','href','poster'])if(e.hasAttribute(name))e.setAttribute(name,url(e.getAttribute(name)));
    if(e.hasAttribute('style'))e.setAttribute('style',css(e.getAttribute('style')));
  });
  const images=[...document.querySelectorAll('img')];
  if(reference&&(images.length!==reference.images.length||images.some((e,i)=>e.alt!==reference.images[i].alt)))throw new Error('Observed image order differs');
  images.forEach((e,i)=>{
    if(reference?.images[i]){
      const selected=reference.images[i].src;
      e.src=url(selected.startsWith('data:')?(observedLogos.get(e.alt)||lazyFallbacks.get(e)||selected):selected);
    }
    e.removeAttribute('srcset');e.removeAttribute('sizes');e.loading='eager';
  });
  document.querySelectorAll('picture source').forEach(e=>e.removeAttribute('srcset'));
  document.querySelectorAll('video').forEach(e=>{e.muted=true;e.setAttribute('muted','');e.setAttribute('playsinline','');});
  document.querySelectorAll('form').forEach(e=>{e.removeAttribute('action');e.removeAttribute('method');});
  document.querySelectorAll('input[type="email"],input[type="password"]').forEach(e=>{e.readOnly=true;e.autocomplete='off';});
  return document;
}
const styles=[],documents={},configuration={origin,attributes:{},headers:{desktop:{},narrow:{}}};
const attrs=e=>Object.fromEntries([...e.attributes].map(a=>[a.name,a.value]));
for(const variant of ['desktop','narrow']){
  const {record,document}=source(variant);
  for(const node of document.querySelectorAll('style,link[rel="stylesheet"]')){
    if(variant==='desktop'){
      const base=node.tagName==='LINK'?new URL(node.getAttribute('href'),origin).href:origin;
      if(node.tagName==='STYLE')styles.push(css(node.textContent));
      else if(base.startsWith(origin+'_next/')){
        const a=assets.get(base);if(!a)throw new Error('Missing public stylesheet: '+base);
        styles.push(css(fs.readFileSync(path.join(work,a.path),'utf8'),base));
      }
    }
    node.remove();
  }
  sanitize(document,record);documents[variant]=document;
  configuration.attributes[variant]={html:attrs(document.documentElement),body:attrs(document.body)};
  configuration.headers[variant].closed=document.querySelector('header').outerHTML;
  const states=variant==='desktop'?['platform','solutions','resources']:['menu','menu-platform','menu-solutions','menu-resources'];
  for(const state of states){
    const s=source(variant+'-'+state),d=sanitize(s.document,s.record);
    configuration.headers[variant][state]=d.querySelector('header').outerHTML;
  }
}
function runtime(){
  const narrow=matchMedia('(max-width:1023px)');let variant,live=[],state='closed';
  const fragment=html=>{const t=document.createElement('template');t.innerHTML=html;return t.content;};
  const mediaObserver=new IntersectionObserver(entries=>entries.forEach(({target,isIntersecting})=>{
    if(isIntersecting)target.play().catch(()=>{});else target.pause();
  }));
  function scrollState(){
    const mark=document.querySelector('#nav-brand [data-wordmark-collapsed]');
    if(mark){const collapsed=scrollY>50&&state==='closed';mark.dataset.wordmarkCollapsed=String(collapsed);mark.style.opacity=collapsed?'0':'1';mark.style.width=collapsed?'0px':'98px';}
    const links=[...document.querySelectorAll('[data-section-id]')];
    const panels=[...document.querySelectorAll('[class*="textMediaCard"]')].filter(e=>!e.parentElement.closest('[class*="textMediaCard"]'));
    if(links.length===4&&panels.length===4){
      let active=0;panels.forEach((e,i)=>{if(e.getBoundingClientRect().top<innerHeight/2)active=i;});
      links.forEach((e,i)=>e.classList.toggle('index-module-scss-module__sqRZBa__active',i===active));
      if(narrow.matches){const wrap=links[0].parentElement;const e=links[active];wrap.scrollLeft=e.offsetLeft-24;}
    }
  }
  function header(next){
    if(!CONFIG.headers[variant][next]){location.assign(CONFIG.origin);return;}
    document.querySelector('header').replaceWith(fragment(CONFIG.headers[variant][next]));state=next;
    document.body.style.overflow=variant==='narrow'&&state!=='closed'?'hidden':'';scrollState();
  }
  function install(){
    const next=narrow.matches?'narrow':'desktop';if(next===variant)return;
    live.forEach(e=>e.remove());
    for(const [node,values]of [[document.documentElement,CONFIG.attributes[next].html],[document.body,CONFIG.attributes[next].body]]){
      for(const a of [...node.attributes])node.removeAttribute(a.name);
      for(const[k,v]of Object.entries(values))node.setAttribute(k,v);
    }
    const content=document.getElementById('study-'+next).content.cloneNode(true);live=[...content.childNodes];
    document.body.insertBefore(content,document.getElementById('study-runtime'));variant=next;state='closed';
    mediaObserver.disconnect();document.querySelectorAll('video').forEach(v=>{v.muted=true;v.loop=true;v.autoplay=true;mediaObserver.observe(v);});scrollState();
  }
  document.addEventListener('click',event=>{
    const b=event.target.closest('button');if(!b)return;
    const name=b.getAttribute('aria-label')||b.textContent.trim();
    if(name==='Open side menu'){header('menu');return;}
    if(['Close side menu','Press escape to close menu'].includes(name)){header('closed');return;}
    if(name==='Go back to previous menu options'){header('menu');return;}
    if(['Platform','Solutions','Resources'].includes(name)&&b.closest('header')){
      const next=(variant==='narrow'?'menu-':'')+name.toLowerCase();header(state===next?(variant==='narrow'?'menu':'closed'):next);return;
    }
    if(name==='Close promo banner'){b.parentElement.remove();return;}
    if(name==='Pause video'||name==='Play video'){
      const v=b.closest('figure')?.querySelector('video');if(v){v.paused?v.play():v.pause();b.setAttribute('aria-label',v.paused?'Play video':'Pause video');}return;
    }
    if(b.closest('header')){location.assign(CONFIG.origin);return;}
  });
  document.addEventListener('keydown',event=>{if(event.key==='Escape'&&state!=='closed')header('closed');});
  document.addEventListener('submit',event=>{event.preventDefault();location.assign(CONFIG.origin);});
  document.addEventListener('scroll',scrollState,{passive:true});
  narrow.addEventListener('change',install);install();
}
const stylesheet=styles.join('\n');
const body=['desktop','narrow'].map(v=>'<template id="study-'+v+'">'+documents[v].body.innerHTML+'</template>').join('');
const html='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Airtable — dated unofficial homepage study</title><style>'+stylesheet.replace(/<\/style/gi,'<\\/style')+'</style></head><body>'+body+'<script id="study-runtime">const CONFIG='+JSON.stringify(configuration).replace(/</g,'\\u003c')+';('+runtime.toString()+')();</script></body></html>';
fs.writeFileSync(path.join(work,'airtable.html'),html);
fs.writeFileSync(path.join(work,'airtable-oct10-build-record.json'),JSON.stringify({accepted:false,method:'Genuine current-source-targeted Stitch generation followed by source correction. Native exports are retained separately and unchanged. Original observed public DOM, stylesheet bytes, images and fonts are used for corrected working draft; account/product destinations remain official.',screens:screens.map(s=>({name:s.name,deviceType:s.deviceType})),exports,references,assets:[...used],html:{path:'airtable.html',bytes:Buffer.byteLength(html),sha256:hash(html)},remaining:['Rendered desktop/narrow full-page comparison','Resources narrow submenu','All nested product/feature menus, footer expansion, animation/video synchronization and intermediate widths','Production screen verification']},null,2)+'\n');
console.log(JSON.stringify({bytes:Buffer.byteLength(html),assets:used.size,sourceReferences:Object.keys(references).length,accepted:false}));
