// Tesla-only refinements after retained native Stitch edit; originals stay untouched.
import fs from 'node:fs';
import {spawnSync} from 'node:child_process';
const base=fs.readFileSync('scripts/build_captured_homepage.mjs','utf8');
let source=base.replace("  config.attributes[width] =",`  // A source-captured public map preserves the actually observed markers.
  const map=document.querySelector('.charging-map-component__map');
  if(map) map.innerHTML='<img src="tesla-oct10-map-'+width+'.png" alt="" style="display:block;width:100%;height:100%;object-fit:cover">';
  const hero=document.querySelector('.tcl-flex-module-carousel--homepage_hero_carousel');
  if(hero) {
    [...hero.querySelectorAll('.tcl-flex-module-carousel__slides > .tcl-flex-module-carousel__slide')].forEach((s,i)=>s.classList.toggle('tcl-flex-module-carousel__slide--active',i===0));
    hero.querySelectorAll('[aria-label="Tab List"]').forEach(n=>[...n.querySelectorAll('[role="tab"]')].forEach((t,i)=>t.setAttribute('aria-selected',String(i===0))));
  }
  config.attributes[width] =`);
source=source.replace('function runtime() {',`function safeMenu(html){
  const d=new JSDOM(html,{virtualConsole:new VirtualConsole()}).window.document;
  d.querySelectorAll('script,iframe,base,link').forEach(e=>e.remove());
  for(const e of d.querySelectorAll('*')){
    for(const a of [...e.attributes]) if(/^on/i.test(a.name))e.removeAttribute(a.name);
    for(const a of ['src','href','poster','xlink:href']) if(e.hasAttribute(a))e.setAttribute(a,local(e.getAttribute(a)));
    if(e.hasAttribute('srcset')) e.removeAttribute('srcset');
    if(e.hasAttribute('style'))e.setAttribute('style',css(e.getAttribute('style'),officialURL));
  }
  return d.body.innerHTML;
}
config.menus={mobile:{},desktop:{}};
for(const [type,file] of [['mobile','tesla-oct10-mobile-menu-templates.json'],['desktop','tesla-oct10-desktop-menu-templates.json']]){
  for(const [name,value] of Object.entries(read(file))) config.menus[type][name]={html:safeMenu(typeof value==='string'?value:value.html),bodyClass:value.bodyClass||null};
}
function runtime() {`);
source=source.replace('current = width;','current = width;\n    document.dispatchEvent(new CustomEvent("tesla-study-ready"));');
source=source.replace('</title><style>','</title><script src="tesla-oct10-interactions.js" defer></script><style>');
source=source.replace('</style></head>',fs.readFileSync('.stitch-work/current-official/tesla-oct10-refinements.css','utf8')+'</style></head>');
fs.writeFileSync('scripts/tesla-oct10-captured-builder.mjs',source);
const p=spawnSync(process.execPath,['scripts/tesla-oct10-captured-builder.mjs','tesla','https://www.tesla.com/','767'],{stdio:'inherit'});
process.exitCode=p.status;
