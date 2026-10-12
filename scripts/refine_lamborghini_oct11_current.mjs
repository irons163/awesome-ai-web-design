import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {JSDOM,VirtualConsole} from 'jsdom';
const work=path.resolve('.stitch-work/current-official');
const file=path.join(work,'lamborghini.html');
const before=fs.readFileSync(file,'utf8');
const start=before.indexOf('const CONFIG=')+13;
const end=before.indexOf(';(function runtime',start);
const config=JSON.parse(before.slice(start,end));
const manifest=JSON.parse(fs.readFileSync(path.join(work,'lamborghini-oct10-assets.json'),'utf8'));
const assets=new Map(manifest.assets.map(a=>[a.source_url,a.path]));
const official='https://www.lamborghini.com/en-en';
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const local=v=>{if(!v||/^(?:data:|#|mailto:|tel:)/.test(v))return v;const u=new URL(v,official).href;return assets.get(u)||u;};
const dom=html=>new JSDOM(html,{virtualConsole:new VirtualConsole()}).window.document;
const video='lamborghini-assets/oct10/observed-hero-hd-remux.mp4';
const bytes=fs.readFileSync(path.join(work,video));
config.menuOpen={};
for(const width of [1280,390]){
  const doc=dom(config.bodies[width]);
  for(const v of doc.querySelectorAll('video')){
    v.querySelectorAll('source').forEach(n=>n.remove());
    v.src=video;v.setAttribute('muted','');v.setAttribute('loop','');v.setAttribute('playsinline','');v.setAttribute('autoplay','');
  }
  config.bodies[width]=doc.body.innerHTML;
  const record=JSON.parse(fs.readFileSync(path.join(work,`lamborghini-oct11-official-menu-${width===1280?'desktop':'narrow'}.json`),'utf8'));
  const menu=dom(record.header).querySelector('header');
  for(const n of [menu,...menu.querySelectorAll('*')]){
    for(const a of [...n.attributes])if(/^on/i.test(a.name))n.removeAttribute(a.name);
    for(const a of ['href','src','poster'])if(n.hasAttribute(a))n.setAttribute(a,local(n.getAttribute(a)));
  }
  menu.querySelectorAll('script,iframe').forEach(n=>n.remove());
  config.menuOpen[width]=menu.innerHTML;
}
const rules=JSON.parse(fs.readFileSync(path.join(work,'lamborghini-oct11-official-menu-styles-private.json'),'utf8')).map(x=>x.text||x.css).join('\n').replace(/url\(\s*(['"]?)(.*?)\1\s*\)/g,(all,q,u)=>`url("${local(u)}")`).replace(/<\/style/gi,'<\\/style');
let output=before.slice(0,start)+JSON.stringify(config).replace(/</g,'\\u003c')+before.slice(end);
output=output.replace('</style>',`\n${rules}</style>`);
const needle='    const mediaObserver = new IntersectionObserver';
if(!output.includes(needle))throw new Error('Expected source-corrected runtime');
output=output.replace(needle,`    const header=document.querySelector('header');
    const closed=header?.innerHTML;
    let opened=false;
    function updateHeader(){header?.classList.toggle('full-bg',opened||scrollY>0);}
    function toggleMenu(next){if(!header)return;opened=next;header.innerHTML=next?CONFIG.menuOpen[width]:closed;document.body.style.overflow=next?'hidden':'';updateHeader();if(next)header.querySelector('button[aria-label="Open menu"]')?.focus();}
    addEventListener('scroll',updateHeader,{passive:true});updateHeader();
    header?.addEventListener('click',e=>{if(e.target.closest('button[aria-label="Open menu"]'))toggleMenu(!opened);});
    document.addEventListener('keydown',e=>{if(e.key==='Escape'&&opened)toggleMenu(false);});
${needle}`);
fs.writeFileSync(file,output);
fs.writeFileSync(path.join(work,'lamborghini-oct11-source-corrections.json'),JSON.stringify({brand:'lamborghini',accepted:false,original_sha256:hash(before),corrected_sha256:hash(output),derived_media:[{path:video,bytes:bytes.length,sha256:hash(bytes),source_url:'https://videolamborghini-meride-tv.akamaized.net/video/folder2/1786627119hero_lamborghini/hd/index.m3u8',method:'Stream-copy remux of exact publicly observed official HLS variant; derivative container, original video frames unchanged',duration_seconds:7,dimensions:[1920,1080]}],menus:'Original observed root desktop/narrow header DOM plus original page CSS; only root open/close and Escape implemented. Nested choices and services remain unverified.',tracking_excluded_host:'analytics00.meride.tv',actual_final_hash_visual_review_pending:true},null,2)+'\n');
console.log(JSON.stringify({bytes:Buffer.byteLength(output),sha256:hash(output),accepted:false}));
