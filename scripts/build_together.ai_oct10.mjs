import fs from 'node:fs';
import crypto from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {JSDOM,VirtualConsole} from 'jsdom';
const work='.stitch-work/current-official/';
const read=n=>JSON.parse(fs.readFileSync(work+n,'utf8'));
const manifest=read('together.ai-oct10-assets.json');
const assets=new Map(manifest.assets.map(a=>[a.source_url,a.path]));
const doc=h=>new JSDOM(h,{runScripts:'outside-only',virtualConsole:new VirtualConsole()}).window.document;
function localize(h){
 const d=doc(h);
 d.querySelectorAll('script,iframe,style').forEach(e=>e.remove());
 d.querySelectorAll('*').forEach(e=>{
   for(const a of [...e.attributes])if(/^on/i.test(a.name))e.removeAttribute(a.name);
   for(const key of ['src','href','poster'])if(e.hasAttribute(key)){
      const value=e.getAttribute(key);if(!value||value.startsWith('#')||value.startsWith('data:'))continue;
      const u=new URL(value,'https://www.together.ai/').href;e.setAttribute(key,assets.get(u)||u);
   }
   if(e.tagName==='IMG'){e.removeAttribute('srcset');e.removeAttribute('sizes');e.loading='eager';}
 });return d.body.innerHTML;
}
let base=fs.readFileSync('scripts/build_captured_homepage.mjs','utf8');
base=base.replace('const source = r.images[i].src;', "const source = r.images[i].src;\n    if (source.includes('/plugins/Basic/assets/placeholder.60f9b1840c.svg')) { e.remove(); return; }");
fs.writeFileSync('scripts/together.ai-oct10-captured-builder.mjs',base);
execFileSync(process.execPath,['scripts/together.ai-oct10-captured-builder.mjs','together.ai','https://www.together.ai/'],{stdio:'inherit'});
const source=doc(read('together.ai-oct10-official-390-reference.json').htmlParts.join(''));
const navClosed=localize(source.querySelector('nav').outerHTML);
const navOpen=localize(read('together.ai-oct10-official-mobile-menu.json').nav);
const tabs={Inference:localize(source.querySelector('[data-tabs="wrap"]').outerHTML),Compute:localize(read('together.ai-oct10-official-compute.json').tabs),'Model shaping':localize(read('together.ai-oct10-official-model-shaping.json').tabs)};
function runtime(){
 let menu=false;
 let announcementOpen=innerWidth>767;
 const announcement=()=>document.documentElement.style.setProperty('--_spacers---announcement-bar',announcementOpen&&innerWidth>767?'2.75em':'0em');
 announcement();
 window.addEventListener('scroll',()=>{if(scrollY>2&&announcementOpen){announcementOpen=false;announcement();}},{passive:true});
 const replace=(selector,markup)=>{const old=document.querySelector(selector);const t=document.createElement('template');t.innerHTML=markup;old?.replaceWith(t.content);};
 function setMenu(open){menu=open;replace('nav',open?MENU_OPEN:MENU_CLOSED);document.body.style.overflow=open?'hidden':'';}
 document.addEventListener('click',e=>{
   const trigger=e.target.closest('[data-nav-menu="trigger"]');
   if(trigger){e.preventDefault();setMenu(!menu);return;}
   const tab=e.target.closest('[data-tabs="menu-item"]');
   if(tab){const key=tab.textContent.trim();if(TABS[key]){e.preventDefault();replace('[data-tabs="wrap"]',TABS[key]);}return;}
 });
 document.addEventListener('keydown',e=>{if(e.key==='Escape'&&menu)setMenu(false);});
 matchMedia('(max-width:767px)').addEventListener('change',()=>{menu=false;document.body.style.overflow='';announcement();});
}
const js=`// Source-observed menu and product-tab states; no official service runtime.\nconst MENU_OPEN=${JSON.stringify(navOpen)};const MENU_CLOSED=${JSON.stringify(navClosed)};const TABS=${JSON.stringify(tabs)};(${runtime.toString()})();\n`;
fs.writeFileSync(work+'together.ai-oct10-interactions.js',js);
let html=fs.readFileSync(work+'together.ai.html','utf8');html=html.replace('</body>','<script src="together.ai-oct10-interactions.js"></script></body>');fs.writeFileSync(work+'together.ai.html',html);
const record=read('together.ai-oct10-build-record.json');record.html={bytes:Buffer.byteLength(html),sha256:crypto.createHash('sha256').update(html).digest('hex')};record.interactions='Captured exact official menu, Compute and Model shaping markup, with local delegated selection controls; only scoped states visually checked.';record.removed_assets=['Hidden Webflow placeholder403; no public visible image removed.'];fs.writeFileSync(work+'together.ai-oct10-build-record.json',JSON.stringify(record,null,2)+'\n');console.log(JSON.stringify(record.html));
