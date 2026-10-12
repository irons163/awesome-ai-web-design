import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {JSDOM, VirtualConsole} from 'jsdom';

const work=path.resolve('.stitch-work/current-official');
const file=path.join(work,'voltagent.html');
const original=fs.readFileSync(file,'utf8');
const hash=value=>crypto.createHash('sha256').update(value).digest('hex');
const name='voltagent-oct10-official-1280-reference.json';
const source=JSON.parse(fs.readFileSync(path.join(work,name),'utf8'));
const html=source.htmlParts.join('');
if(source.url!=='https://voltagent.dev/'||html.length!==source.html_length||hash(html)!==source.html_sha256||!html.endsWith('</html>')) throw new Error('Incomplete current source');
const dom=html=>new JSDOM(html,{virtualConsole:new VirtualConsole()}).window.document;
const sourceDocument=dom(html);
const nav=sourceDocument.querySelector('nav.navbar_UaH_');
if(!nav||!nav.textContent.includes('10.8K')||!nav.textContent.includes('Try VoltOps')||!nav.querySelector('a[href="https://s.voltagent.dev/discord/"]')) throw new Error('Current header controls not present');
if(nav.querySelector('img,video,canvas,source,iframe,script,link')) throw new Error('Unexpected external source dependency');
for(const node of [nav,...nav.querySelectorAll('*')]){
  for(const attr of [...node.attributes]) if(/^on/i.test(attr.name)) node.removeAttribute(attr.name);
  for(const attr of ['href','xlink:href']) if(node.hasAttribute(attr)){
    const value=node.getAttribute(attr);
    if(/^javascript:/i.test(value)) node.setAttribute(attr,'#');
    else if(!/^(?:#|data:|mailto:|tel:)/.test(value)) node.setAttribute(attr,new URL(value,source.url).href);
  }
}
const start=original.indexOf('const CONFIG=')+13;
const end=original.indexOf(';(function runtime',start);
const config=JSON.parse(original.slice(start,end));
const body=config.bodies[1280];
const priorNav=dom(body).querySelector('nav.navbar_UaH_');
if(!priorNav||!body.includes(priorNav.outerHTML)) throw new Error('Exact original nav slot not available');
const beforeMain=dom(body).querySelector('main').outerHTML;
const narrow=config.bodies[390];
const newNav=nav.outerHTML;
config.bodies[1280]=body.replace(priorNav.outerHTML,newNav);
if(dom(config.bodies[1280]).querySelector('main').outerHTML!==beforeMain||config.bodies[390]!==narrow) throw new Error('Unrelated body content changed');
const corrected=original.slice(0,start)+JSON.stringify(config).replace(/</g,'\\u003c')+original.slice(end);
const backup=path.join(work,'voltagent-oct11-pre-current-navbar.html');
if(!fs.existsSync(backup)) fs.writeFileSync(backup,original);
fs.writeFileSync(file,corrected);
fs.writeFileSync(path.join(work,'voltagent-oct11-current-navbar-correction.json'),JSON.stringify({
  brand:'voltagent',accepted:false,official_consistency_claim:false,
  previous_sha256:hash(original),corrected_sha256:hash(corrected),source:name,
  source_url:source.url,source_observed_at:source.observed_at,source_html_sha256:source.html_sha256,
  source_selector:'nav.navbar_UaH_',source_nav_sha256:hash(sourceDocument.querySelector('nav.navbar_UaH_').outerHTML),
  corrected_nav_sha256:hash(newNav),original_nav_sha256:hash(priorNav.outerHTML),
  method:'Replace only the1280 desktop navbar with the current actually observed original public nav; normalize its original relative navigation links. GitHub10.8K, Discord inlineSVG and Try VoltOps retained. No external assets were needed.',
  narrow_template_bytes_unchanged:true,desktop_main_dom_unchanged:true,additional_assets:[],
  actual_render_after_correction_verified:false,
  limits:['Current source GitHub count is a dated sample, not a live guarantee.',
    'Navigation/menu/GitHub/Discord/VoltOps service interactions remain unverified.',
    'Known original Seth avatar404, virtualized testimonial mount/layout and marquee/diagram phases remain explicit.',
    'Current-hash full desktop/narrow actual raster review remains required.']
},null,2)+'\n');
console.log(JSON.stringify({brand:'voltagent',bytes:Buffer.byteLength(corrected),sha256:hash(corrected),external_assets_added:0,accepted:false}));
