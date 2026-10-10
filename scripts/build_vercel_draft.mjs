import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {JSDOM,VirtualConsole} from 'jsdom';
const work=path.resolve('.stitch-work/current-official'),origin='https://vercel.com/';
const read=name=>JSON.parse(fs.readFileSync(path.join(work,name),'utf8'));
const hash=value=>crypto.createHash('sha256').update(value).digest('hex');
const parse=html=>new JSDOM(html,{virtualConsole:new VirtualConsole()}).window.document;
const native=read('vercel-stitch-oct10-generated.json');
if(!native.screens?.length)throw new Error('Genuine current Stitch generation required');
for(const screen of native.screens)for(const file of screen.exports)if(hash(fs.readFileSync(path.join(work,file.path)))!==file.sha256)throw new Error('Original native export changed');
const mobileNativeFile='vercel-stitch-oct10-mobile-generated.json';
if(fs.existsSync(path.join(work,mobileNativeFile)))for(const screen of read(mobileNativeFile).screens)for(const file of screen.exports)if(hash(fs.readFileSync(path.join(work,file.path)))!==file.sha256)throw new Error('Original mobile-request native export changed');
const provenance=read('vercel-browser-asset-provenance.json'),assets=new Map(provenance.assets.map(a=>[a.source_url,a])),used=new Set();
for(const a of assets.values()){const b=fs.readFileSync(path.join(work,a.path));if(b.length!==a.bytes||hash(b)!==a.sha256)throw new Error('Original public asset changed');}
const url=(value,base=origin)=>{
  if(!value||/^(#|data:|mailto:|tel:)/i.test(value))return value;
  if(/^javascript:/i.test(value))return '#';
  const absolute=new URL(value,base).href,a=assets.get(absolute);if(a){used.add(a.path);return a.path;}return absolute;
};
const css=(value,base=origin)=>value.replace(/url\(\s*(['"]?)(.*?)\1\s*\)/g,(match,quote,value)=>/^(data:|#)/i.test(value)?match:'url("'+url(value,base)+'")');
function localize(document,reference){
  document.querySelectorAll('base,meta[http-equiv],link:not([rel="stylesheet"])').forEach(e=>e.remove());
  document.querySelectorAll('*').forEach(e=>{
    for(const name of ['src','href','poster'])if(e.hasAttribute(name))e.setAttribute(name,url(e.getAttribute(name)));
    if(e.hasAttribute('style'))e.setAttribute('style',css(e.getAttribute('style')));
  });
  if(reference){
    if(document.images.length!==reference.images.length)throw new Error('Image order changed');
    [...document.images].forEach((e,i)=>{e.src=url(reference.images[i].src);e.removeAttribute('srcset');e.loading='eager';});
  } else document.querySelectorAll('img').forEach(e=>e.removeAttribute('srcset'));
  document.querySelectorAll('picture source').forEach(e=>e.removeAttribute('srcset'));
  document.querySelectorAll('input[type="radio"]').forEach(e=>e.name='study-display-theme');
  document.querySelectorAll('input[type="password"],input[type="email"]').forEach(e=>{e.readOnly=true;e.autocomplete='off';});
  document.querySelectorAll('form').forEach(e=>{e.removeAttribute('action');e.removeAttribute('method');});
  // Use the actual public static fallback, not a blank canvas or invented image.
  // The official live WebGL animation remains explicitly outside acceptance.
  document.querySelectorAll('[data-hero-static-fallback]').forEach(e=>e.parentElement.style.opacity='1');
  document.querySelectorAll('canvas').forEach(e=>e.remove());
}
function runtime(){
  const narrow=matchMedia('(max-width:880px)');let mode,live=[],desktopMenu=null,mobileOpen=false;
  const fragment=html=>{const t=document.createElement('template');t.innerHTML=html;return t.content;};
  const attrs=(e,values)=>{for(const a of [...e.attributes])e.removeAttribute(a.name);for(const[k,v]of Object.entries(values))e.setAttribute(k,v);};
  function desktop(name){
    desktopMenu=name;
    const h=document.querySelector('#marketing-header');h.toggleAttribute('data-nav-open',!!name);
    h.querySelectorAll('button[data-nav-id]').forEach(e=>{const open=e.dataset.navId===name;e.setAttribute('aria-expanded',String(open));e.toggleAttribute('data-open',open);e.querySelectorAll('span[aria-hidden]').forEach(s=>s.toggleAttribute('data-open',open));});
    h.querySelectorAll('[id^="nav-panel-"]').forEach(e=>{const open=e.id==='nav-panel-'+name;e.toggleAttribute('data-open',open);e.inert=!open;if(open)e.removeAttribute('aria-hidden');else e.setAttribute('aria-hidden','true');});
  }
  function mobile(open){
    mobileOpen=open;const h=document.querySelector('#marketing-header');h.toggleAttribute('data-mobile-open',open);
    const b=h.querySelector('button[aria-label="Open menu"],button[aria-label="Close menu"]');b.setAttribute('aria-label',open?'Close menu':'Open menu');b.setAttribute('aria-expanded',String(open));b.toggleAttribute('data-open',open);
    const menu=h.querySelector('[aria-label="Navigation menu"]');menu.toggleAttribute('data-open',open);menu.inert=!open;if(open)menu.removeAttribute('aria-hidden');else menu.setAttribute('aria-hidden','true');
    document.querySelector('main').inert=open;document.body.style.overflow=open?'hidden':'';
  }
  function install(){
    const next=narrow.matches?'mobile':'desktop';if(next===mode)return;
    live.forEach(e=>e.remove());attrs(document.documentElement,CONFIG.attributes[next].html);attrs(document.body,CONFIG.attributes[next].body);
    const source=document.getElementById('study-'+next+'-source').content.cloneNode(true);live=[...source.childNodes];document.body.insertBefore(source,document.getElementById('study-runtime'));
    mode=next;desktopMenu=null;mobileOpen=false;
  }
  document.addEventListener('click',event=>{
    const button=event.target.closest('button');if(!button)return;
    const label=button.getAttribute('aria-label')||button.textContent.trim();
    if(label==='Open menu'||label==='Close menu'){mobile(!mobileOpen);return;}
    if(button.dataset.navId){desktop(desktopMenu===button.dataset.navId?null:button.dataset.navId);return;}
    if(['Onboard your agent','Cookie Preferences','View as AI agent','Ask AI','Copy Wordmark','Copy Logo','Download Brand Assets','Open Brand Guidelines in New Tab'].includes(label))location.assign(CONFIG.origin);
  });
  document.addEventListener('pointerout',event=>{const h=document.querySelector('#marketing-header');if(mode==='desktop'&&desktopMenu&&h.contains(event.target)&&!h.contains(event.relatedTarget))desktop(null);});
  document.addEventListener('click',event=>{if(mode==='desktop'&&desktopMenu&&!event.target.closest('#marketing-header'))desktop(null);});
  document.addEventListener('keydown',event=>{if(event.key==='Escape'){if(mobileOpen)mobile(false);if(desktopMenu){const id=desktopMenu;desktop(null);document.querySelector('[data-nav-id="'+id+'"]').focus();}}});
  document.addEventListener('change',event=>{
    if(!event.target.matches('input[name="study-display-theme"]'))return;
    const value=event.target.getAttribute('aria-label'),dark=value==='dark'||(value==='system'&&matchMedia('(prefers-color-scheme:dark)').matches);
    document.documentElement.classList.toggle('dark-theme',dark);document.documentElement.classList.toggle('light-theme',!dark);document.documentElement.style.colorScheme=dark?'dark':'light';document.documentElement.style.backgroundColor=dark?'#000':'#fff';
  });
  document.addEventListener('submit',event=>{event.preventDefault();location.assign(CONFIG.origin);});
  addEventListener('scroll',()=>document.querySelector('#marketing-header')?.toggleAttribute('data-scrolled',scrollY>8),{passive:true});
  narrow.addEventListener('change',install);install();
}
const attributes=e=>Object.fromEntries([...e.attributes].map(a=>[a.name,a.value]));
const configuration={origin,attributes:{}},documents={},references={},styles=[];
for(const variant of ['desktop','mobile']){
  const r=read('vercel-'+variant+'-browser-reference.json'),html=r.htmlParts.join('');if(hash(html)!==r.html_sha256)throw new Error('Current reference changed');
  const document=parse(html);
  for(const node of document.querySelectorAll('style,link[rel="stylesheet"]')){
    if(variant==='desktop'){
      const base=node.tagName==='LINK'?new URL(node.getAttribute('href'),origin).href:origin;
      const a=assets.get(base);if(node.tagName==='LINK'&&!a)throw new Error('Missing exact original stylesheet');
      const text=node.tagName==='LINK'?fs.readFileSync(path.join(work,a.path),'utf8'):node.textContent;
      styles.push(css(text,base));
    }
    node.remove();
  }
  localize(document,r);configuration.attributes[variant]={html:attributes(document.documentElement),body:attributes(document.body)};
  documents[variant]=document;references[variant]={file:'vercel-'+variant+'-browser-reference.json',observed_at:r.observed_at,html_sha256:r.html_sha256};
}
// Keep the required unofficial-study disclosure in the empty compact header
// area so it cannot cover links in the long native mobile navigation drawer.
styles.push('@media(max-width:880px){body.root>.official-draft-badge{top:8px;right:66px;bottom:auto;max-width:calc(100vw - 132px)}}@media(max-width:359px){body.root>.official-draft-badge summary{font-size:11px}}');
const stylesheet=styles.join('\n'),stylesheetName='vercel-rendered.css';fs.writeFileSync(path.join(work,stylesheetName),stylesheet);
const templates=['desktop','mobile'].map(v=>'<template id="study-'+v+'-source">'+documents[v].body.innerHTML+'</template>').join('');
const script='<script id="study-runtime">const CONFIG='+JSON.stringify(configuration).replace(/</g,'\\u003c')+';('+runtime.toString()+')();</script>';
const html='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Vercel — dated official-site working study</title><style>'+stylesheet.replace(/<\/style/gi,'<\\/style')+'</style></head><body>'+templates+script+'</body></html>';
fs.writeFileSync(path.join(work,'vercel.html'),html);
fs.writeFileSync(path.join(work,'vercel-draft-build-record.json'),JSON.stringify({accepted:false,native_exports:'vercel-stitch-oct10-generated.json',native_mobile_exports:fs.existsSync(path.join(work,mobileNativeFile))?mobileNativeFile:null,source_references:references,asset_provenance:'vercel-browser-asset-provenance.json',asset_paths:[...used].sort(),working_draft:{path:'vercel.html',bytes:Buffer.byteLength(html),sha256:hash(html)},working_css:{path:stylesheetName,bytes:Buffer.byteLength(stylesheet),sha256:hash(stylesheet)},method:'Source correction after an independently prompted genuine Stitch generation. Original public rendered DOM, stylesheet response bytes, actual fonts/images and original public static hero fallback retained; native exports remain separate and immutable.',limitations:['Official live WebGL shader is not replayed; its original public static fallback is used.','Content-visibility, full motion, all advanced controls and intermediate widths require further comparison. Account, agent, AI and cookie workflows delegate to the official service.','Narrow source uses a desktop user agent. True phone/tablet and production pixel comparison remain unaccepted.']},null,2)+'\n');
console.log(JSON.stringify({htmlBytes:Buffer.byteLength(html),cssBytes:Buffer.byteLength(stylesheet),assets:used.size,accepted:false}));
