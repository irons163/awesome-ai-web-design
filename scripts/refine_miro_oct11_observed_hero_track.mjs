import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {JSDOM,VirtualConsole} from 'jsdom';

const work=path.resolve('.stitch-work/current-official');
const file=path.join(work,'miro.html');
const original=fs.readFileSync(file,'utf8');
if(original.includes('id="miro-observed-hero-track"')) throw new Error('Correction already installed');
const hash=value=>crypto.createHash('sha256').update(value).digest('hex');
const read=name=>JSON.parse(fs.readFileSync(path.join(work,name),'utf8'));
const start=original.indexOf('const CONFIG=')+13;
const end=original.indexOf(';(function runtime',start);
const config=JSON.parse(original.slice(start,end));
const assets=new Map(read('miro-oct10-assets.json').assets.map(asset=>[asset.source_url,asset]));
const sourceRecords=[];
for(const width of [1280,390]){
  const name=`miro-oct11-active-hero-${width}-reference.json`,record=read(name),html=record.htmlParts.join('');
  if(html.length!==record.html_length||hash(html)!==record.html_sha256||record.scrollY!==0||html.includes('[Truncated]')) throw new Error('Incomplete active hero');
  const source=new JSDOM(html,{url:record.url,virtualConsole:new VirtualConsole()}).window.document;
  const current=new JSDOM(config.bodies[width],{virtualConsole:new VirtualConsole()}).window.document;
  if(source.images.length!==record.images.length) throw new Error('Observed active hero image order changed');
  [...source.images].forEach((image,index)=>{
    const observed=record.images[index];
    if(image.alt!==observed.alt) throw new Error('Observed active hero image alt changed');
    if(!observed.src){image.remove();return;}
    if(observed.src.startsWith('data:')) image.src=observed.src;
    else {
      const asset=assets.get(observed.src);
      if(!asset) throw new Error('Missing exact active hero asset: '+observed.src);
      image.src=asset.path;
    }
    image.removeAttribute('srcset');image.removeAttribute('sizes');image.loading='eager';
  });
  source.querySelectorAll('script,iframe,link,style,picture source').forEach(node=>node.remove());
  for(const node of source.querySelectorAll('*')){
    for(const attribute of [...node.attributes]) if(/^on/i.test(attribute.name)) node.removeAttribute(attribute.name);
    if(node.hasAttribute('href')&&!node.getAttribute('href').startsWith('#')) node.setAttribute('href',new URL(node.getAttribute('href'),record.url).href);
    if(node.hasAttribute('style')) node.setAttribute('style',node.getAttribute('style').replace(/url\(\s*(['"]?)(.*?)\1\s*\)/g,(all,q,url)=>`url("${assets.get(new URL(url,record.url).href)?.path||url}")`));
  }
  source.querySelectorAll('form').forEach(node=>{node.removeAttribute('action');node.removeAttribute('method');});
  source.querySelectorAll('input').forEach(node=>{node.value='';node.readOnly=true;});
  const oldHero=current.querySelector('.framer-zzhgth');
  const hero=source.body.firstElementChild;
  if(!oldHero||!hero.classList.contains('framer-zzhgth')||!hero.textContent.includes('Human collaboration at the speed of AI')) throw new Error('Hero structure changed');
  oldHero.replaceWith(current.importNode(hero,true));
  config.bodies[width]=current.body.innerHTML;
  sourceRecords.push({name,observed_at:record.observed_at,scrollY:record.scrollY,bodyHeight:record.bodyHeight,html_sha256:record.html_sha256,images:record.images.length});
}
const active=read('miro-oct11-active-desktop-track-reference.json');
const track2880=active.elements.find(element=>element.selector==='.framer-66a86y');
if(!track2880) throw new Error('Missing exact observed card track geometry');
const frames=read('miro-oct10-official-1280-phases.json');
const samples=frames.filter(frame=>frame.scrollY<=2160).map(frame=>{
  const heading=frame.headings.find(heading=>heading.text==='Experience the Innovation Workspace');
  return {scrollY:frame.scrollY,trackX:heading.box.x+374,basis:'Canonical initial title/card separation; active card track becomes visible near this interval.'};
});
samples.push({scrollY:2880,trackX:track2880.box.x,basis:'Actual active2880 card track box'});
for(const scrollY of [3600,4320]){
  const name=`miro-oct11-active-track-${scrollY}-styles.json`,record=read(name);
  const track=record.nodes.find(node=>node.cls==='framer-66a86y');
  if(record.scrollY!==scrollY||!track) throw new Error('Missing observed scroll phase');
  samples.push({scrollY,trackX:track.box.x,basis:name,observed_at:record.observed_at});
}
config.studyTrack.trackSamples=samples;

function observedTrackRuntime(){
  let activeNode,mode,pending=false;
  function update(){
    pending=false;
    if(matchMedia('(max-width:767px)').matches){activeNode=null;mode=null;return;}
    let node=document.querySelector('.framer-1e4zp5x');if(!node)return;
    const desired=scrollY<CONFIG.studyTrack.finalPhaseFrom?'active':'final';
    if(node!==activeNode||desired!==mode){
      const template=document.createElement('template');
      template.innerHTML=CONFIG.studyTrack[desired==='active'?'activeHTML':'finalHTML'];
      const next=template.content.firstElementChild;node.replaceWith(next);node=next;activeNode=next;mode=desired;
    }
    const overlay=document.querySelector('.framer-b5l8z1>.framer-1fic3hf');
    if(overlay){overlay.style.opacity=desired==='active'?'0':'1';overlay.style.pointerEvents=desired==='active'?'none':'';}
    if(desired!=='active')return;
    const samples=CONFIG.studyTrack.trackSamples;
    let target=samples.at(-1).trackX;
    for(let i=1;i<samples.length;i++)if(scrollY<=samples[i].scrollY){
      const a=samples[i-1],b=samples[i],ratio=Math.max(0,Math.min(1,(scrollY-a.scrollY)/(b.scrollY-a.scrollY)));
      target=a.trackX+(b.trackX-a.trackX)*ratio;break;
    }
    const scroller=node.querySelector('.framer-xn4vzc'),track=node.querySelector('.framer-66a86y');
    const current=new DOMMatrixReadOnly(getComputedStyle(scroller).transform).m41;
    scroller.style.transform=`translateX(${current+target-track.getBoundingClientRect().left}px)`;
  }
  function queue(){if(!pending){pending=true;requestAnimationFrame(update);}}
  addEventListener('scroll',queue,{passive:true});addEventListener('resize',queue);update();
}
let corrected=original.slice(0,start)+JSON.stringify(config).replace(/</g,'\\u003c')+original.slice(end);
corrected=corrected.replace(/<script id="miro-study-track">[\s\S]*?<\/script>/,`<script id="miro-observed-hero-track">(${observedTrackRuntime.toString()})();</script>`);
if(corrected===original||corrected.includes('id="miro-study-track"'))throw new Error('Previous projection not replaced');
const backup=path.join(work,'miro-oct11-pre-observed-hero-track.html');
if(!fs.existsSync(backup))fs.writeFileSync(backup,original);
fs.writeFileSync(file,corrected);
fs.writeFileSync(path.join(work,'miro-oct11-observed-hero-track-correction.json'),JSON.stringify({
  accepted:false,official_consistency_claim:false,previous_sha256:hash(original),corrected_sha256:hash(corrected),
  hero_sources:sourceRecords,card_track_samples:samples,
  method:'Replace original hero with exact observed active DOM/ancestors and genuine localized source images; project desktop card track using measured track boxes, not only heading position.',
  actual_render_after_correction_verified:false,
  limits:['Fresh settled3600/4320 source phases differ slightly from canonical first-pass spring timing; both originals retained.',
    'Interpolation between measured card track positions and the transition to final AI platform phase remain static projections, not validated Framer spring fidelity.',
    'Hero original canvas/video/icon motion and all UI/service behavior remain unverified.',
    'Current-hash full desktop/narrow actual raster proof is required after this correction.']
},null,2)+'\n');
console.log(JSON.stringify({brand:'miro',bytes:Buffer.byteLength(corrected),sha256:hash(corrected),accepted:false}));
