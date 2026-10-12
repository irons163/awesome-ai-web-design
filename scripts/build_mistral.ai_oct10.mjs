// Current public Mistral source correction after retained native Stitch edit.
import fs from 'node:fs';
import {spawnSync} from 'node:child_process';
let source=fs.readFileSync('scripts/build_captured_homepage.mjs','utf8');
source=source.replace('function runtime() {',`function safeHeader(html){
const d=new JSDOM(html,{virtualConsole:new VirtualConsole(),runScripts:'outside-only'}).window.document;
d.querySelectorAll('script,iframe,base,link').forEach(e=>e.remove());
for(const e of d.querySelectorAll('*')){for(const a of [...e.attributes])if(/^on/i.test(a.name))e.removeAttribute(a.name);for(const a of ['src','href','poster','xlink:href'])if(e.hasAttribute(a))e.setAttribute(a,local(e.getAttribute(a)));if(e.hasAttribute('srcset'))e.removeAttribute('srcset');}
return d.body.innerHTML;
}
config.menus={};
for(const name of ['root','research']){const value=read('mistral.ai-oct10-header-mobile-'+name+'.json');config.menus[name]={...value,html:safeHeader(value.html)};}
function runtime() {`);
source=source.replace('current = width;','current = width;\n    document.dispatchEvent(new CustomEvent("mistral-study-ready"));');
source=source.replace('</title><style>','</title><script src="mistral.ai-oct10-interactions.js" defer></script><style>');
fs.writeFileSync('scripts/mistral.ai-oct10-captured-builder.mjs',source);
const r=spawnSync(process.execPath,['scripts/mistral.ai-oct10-captured-builder.mjs','mistral.ai','https://mistral.ai/','767'],{stdio:'inherit'});process.exitCode=r.status;
