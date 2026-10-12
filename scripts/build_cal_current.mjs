import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {JSDOM,VirtualConsole} from 'jsdom';

const work=path.resolve('.stitch-work/current-official');
const read=n=>JSON.parse(fs.readFileSync(path.join(work,n),'utf8'));
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const provenance=read('cal-oct10-assets.json');
const assets=new Map(provenance.assets.map(a=>[a.source_url,a]));
for(const a of assets.values())if(hash(fs.readFileSync(path.join(work,a.path)))!==a.sha256)throw new Error('Public asset hash differs');
const refs={};
function local(value,base='https://cal.com/'){
  if(value?.startsWith('cal-assets/'))return value;
  if(!value||/^(?:data:|#|mailto:|tel:)/.test(value))return value;
  if(/^javascript:/i.test(value))return '#';
  const u=new URL(value,base);u.searchParams.delete('_gl');return assets.get(u.href)?.path||u.href;
}
const css=(text,base)=>text.replace(/url\(\s*(['"]?)(.*?)\1\s*\)/g,(all,q,u)=>'url("'+local(u,base)+'")');
const configuration={attributes:{},bodies:{},shadows:{}};
const styles=[];
for(const width of [1280,390]){
  const r=read('cal-oct10-official-'+width+'-reference.json'),html=r.htmlParts.join('');
  if(r.url!=='https://cal.com/'||html.length!==r.html_length||hash(html)!==r.html_sha256||!html.endsWith('</html>'))throw new Error('Invalid complete reference');
  refs[width]={url:r.url,observed_at:r.observed_at,viewport:r.viewport,html_sha256:r.html_sha256};
  const d=new JSDOM(html,{virtualConsole:new VirtualConsole()}).window.document;
  d.querySelectorAll('noscript').forEach(e=>e.remove());
  const imgs=[...d.images];
  if(imgs.length!==r.images.length||imgs.some((e,i)=>e.alt!==r.images[i].alt))throw new Error('Observed image order differs');
  imgs.forEach((e,i)=>{e.src=local(r.images[i].src);e.removeAttribute('srcset');e.removeAttribute('sizes');e.loading='eager';});
  // Some rendered Framer gradient declarations serialize as empty inline values.
  // Restore only the gradients directly observed on these exact public classes.
  for(const b of read('cal-oct10-observed-backgrounds.json')[width].filter(b=>b.backgroundImage.startsWith('linear-gradient('))){
    for(const e of d.querySelectorAll('[style*="background-image:"]'))if(e.className===b.class&&e.getAttribute('data-framer-name')===b.name)e.setAttribute('style',e.getAttribute('style').replace(/background-image:\s*;/,'background-image:'+b.backgroundImage+';'));
  }
  for(const e of [...d.querySelectorAll('style,link[rel="stylesheet"]')]){
    if(width===1280){if(e.tagName==='STYLE')styles.push(css(e.textContent,'https://cal.com/'));else{const a=assets.get(e.href);if(!a)throw new Error('Missing source stylesheet '+e.href);styles.push(css(fs.readFileSync(path.join(work,a.path),'utf8'),a.source_url));}}e.remove();
  }
  d.querySelectorAll('script,iframe,base,meta[http-equiv],link,[id^="q-"],[id^="codex-browser-"],img[src*="adsct"],img[src*="analytics"],img[src*="pixel"]').forEach(e=>e.remove());
  d.querySelectorAll('*').forEach(e=>{
    for(const a of [...e.attributes])if(/^on/i.test(a.name)||/^data-airgap/.test(a.name))e.removeAttribute(a.name);
    for(const a of ['src','href','poster','xlink:href'])if(e.hasAttribute(a))e.setAttribute(a,local(e.getAttribute(a)));
    if(e.hasAttribute('style'))e.setAttribute('style',css(e.getAttribute('style'),'https://cal.com/'));
  });
  d.querySelectorAll('form').forEach(e=>{e.removeAttribute('action');e.removeAttribute('method');});
  d.querySelectorAll('input').forEach(e=>{e.value='';e.readOnly=true;});
  configuration.attributes[width]={html:Object.fromEntries([...d.documentElement.attributes].map(a=>[a.name,a.value])),body:Object.fromEntries([...d.body.attributes].map(a=>[a.name,a.value]))};
  configuration.bodies[width]=d.body.innerHTML;
  configuration.shadows[width]=read('cal-oct10-official-'+width+'-shadow.json').map(r=>{
    const fragment=new JSDOM('<body>'+r.htmlParts.join('')+'</body>',{virtualConsole:new VirtualConsole()}).window.document;
    fragment.querySelectorAll('script,iframe').forEach(e=>e.remove());
    fragment.querySelectorAll('*').forEach(e=>{for(const a of [...e.attributes])if(/^on/i.test(a.name))e.removeAttribute(a.name);for(const a of ['src','href'])if(e.hasAttribute(a))e.setAttribute(a,local(e.getAttribute(a)));if(e.tagName==='STYLE')e.textContent=css(e.textContent,'https://cal.com/');if(e.hasAttribute('style'))e.setAttribute('style',css(e.getAttribute('style'),'https://cal.com/'));});
    return fragment.body.innerHTML;
  });
}
function runtime(){
  let current,live=[];const media=matchMedia('(max-width:809px)');
  function install(){const width=media.matches?'390':'1280';if(width===current)return;live.forEach(n=>n.remove());for(const[node,values]of [[document.documentElement,CONFIG.attributes[width].html],[document.body,CONFIG.attributes[width].body]]){for(const a of [...node.attributes])node.removeAttribute(a.name);for(const[k,v]of Object.entries(values))node.setAttribute(k,v);}const t=document.createElement('template');t.innerHTML=CONFIG.bodies[width];live=[...t.content.childNodes];document.body.insertBefore(t.content,document.getElementById('study-runtime'));document.querySelectorAll('.senja-embed').forEach((e,i)=>{if(CONFIG.shadows[width][i])e.attachShadow({mode:'open'}).innerHTML=CONFIG.shadows[width][i];});current=width;}
  document.addEventListener('submit',e=>{e.preventDefault();location.assign('https://cal.com/');});media.addEventListener('change',install);install();
}
const html='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Cal.com — dated unofficial homepage study</title><style>'+styles.join('\n').replace(/<\/style/gi,'<\\/style')+'</style></head><body><script id="study-runtime">const CONFIG='+JSON.stringify(configuration).replace(/</g,'\\u003c')+';('+runtime.toString()+')();</script></body></html>';
const old=path.join(work,'cal-sept27-draft.html');if(!fs.existsSync(old))fs.copyFileSync(path.join(work,'cal.html'),old);
fs.writeFileSync(path.join(work,'cal.html'),html);
fs.writeFileSync(path.join(work,'cal-oct10-build-record.json'),JSON.stringify({accepted:false,method:'Genuine Stitch correction retained separately; working public-page draft corrected using current rendered source DOM, original public CSS, SVGs, fonts and images. Provider output is not source evidence.',references:refs,assets:provenance.assets,html:{bytes:Buffer.byteLength(html),sha256:hash(html)},remaining:['Rendered official/local comparison','Booking-demo animation, FAQ/nav/language/carousel states, real devices and intermediate widths','Native current Stitch response/export completion and production verification']},null,2)+'\n');
console.log(JSON.stringify({bytes:Buffer.byteLength(html),assets:assets.size,accepted:false}));
