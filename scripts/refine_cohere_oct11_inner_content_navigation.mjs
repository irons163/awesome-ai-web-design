import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {JSDOM, VirtualConsole} from 'jsdom';

const work=path.resolve('.stitch-work/current-official');
const file=path.join(work,'cohere.html');
const original=fs.readFileSync(file,'utf8');
const hash=value=>crypto.createHash('sha256').update(value).digest('hex');
const read=name=>JSON.parse(fs.readFileSync(path.join(work,name),'utf8'));
const start=original.indexOf('const CONFIG=')+13;
const end=original.indexOf(';(function runtime',start);
const config=JSON.parse(original.slice(start,end));
if(config.observedStack.innerTextSamples) throw new Error('Inner correction already installed');
const document=new JSDOM(config.bodies[1280],{virtualConsole:new VirtualConsole()}).window.document;
const cards=[...document.querySelectorAll('[class*="pin-spacer-stacking"]')].map(node=>node.firstElementChild);
const labels=cards.map(node=>node.querySelector('h3').textContent.trim());
const inner=cards.map(node=>node.querySelector('.left-text-container'));
const endTranslations=inner.map(node=>Number(/translate\(0px, (-?[\d.]+)px\)/.exec(node.style.transform)?.[1]||0));
if(cards.length!==3||JSON.stringify(endTranslations)!=='[-110.195,-110.195,0]') throw new Error('Unexpected canonical inner structure');
const source=read('cohere-reduced-oct10-official-1280-phases.json');
const previous=read('cohere-oct10-local-1280-phases.json');
if(previous.some(frame=>frame.draft_sha256!==hash(original))) throw new Error('Calibration must describe the current prior candidate');
const calibration=[];
config.observedStack.innerTextSamples=[{scrollY:0,translations:[0,0,0]}];
for(const scrollY of [2160,2880]){
  const official=source.find(frame=>frame.scrollY===scrollY);
  const local=previous.find(frame=>frame.scrollY===scrollY);
  const scales=config.observedStack.scaleSamples.find(frame=>frame.scrollY===scrollY).scales;
  const translations=labels.map((label,index)=>{
    const a=official.headings.find(heading=>heading.text===label);
    const b=local.headings.find(heading=>heading.text===label);
    if(!a||!b) throw new Error('Missing measured original heading');
    const value=endTranslations[index]+(a.box.y-b.box.y)/scales[index];
    calibration.push({scrollY,label,source_y:a.box.y,previous_y:b.box.y,scale:scales[index],end_translation:endTranslations[index],projected_translation:value});
    return value;
  });
  config.observedStack.innerTextSamples.push({scrollY,translations});
}
config.observedStack.innerEndTranslations=endTranslations;
inner.forEach(node=>node.style.transform='translate3d(0,0,0)');
config.bodies[1280]=document.body.innerHTML;

function observedStackRuntime(){
  let pending=false;
  function valueAt(samples,key,index,y){
    let value=samples.at(-1)[key][index];
    for(let i=1;i<samples.length;i++) if(y<=samples[i].scrollY){
      const a=samples[i-1],b=samples[i];
      const ratio=Math.max(0,Math.min(1,(y-a.scrollY)/(b.scrollY-a.scrollY)));
      value=a[key][index]+(b[key][index]-a[key][index])*ratio;break;
    }
    return value;
  }
  function update(){
    pending=false;
    const stack=CONFIG.observedStack;
    if(matchMedia('(max-width:767px)').matches){
      const nav=[...document.querySelectorAll('nav')].find(node=>node.classList.contains('lg:hidden'));
      const banner=[...document.querySelectorAll('div.relative.z-nav')].find(node=>node.textContent.includes('Introducing North 2'));
      if(nav){
        if(scrollY<1){nav.style.top=`${banner?.getBoundingClientRect().height||80}px`;nav.style.transform='translateY(0)';}
        else{nav.style.removeProperty('top');nav.style.removeProperty('transform');}
      }
      return;
    }
    const nav=[...document.querySelectorAll('nav')].find(node=>node.classList.contains('lg:block'));
    if(nav) nav.style.top=`${Math.max(0,stack.announcementHeight-scrollY)}px`;
    const spacers=[...document.querySelectorAll('[class*="pin-spacer-stacking"]')];
    spacers.forEach((spacer,index)=>{
      const card=spacer.firstElementChild;
      const naturalTop=spacer.getBoundingClientRect().top+scrollY;
      const shift=Math.max(0,Math.min(stack.maxShifts[index],scrollY+stack.topOffsets[index]-naturalTop));
      const endY=Math.max(2881,naturalTop+stack.maxShifts[index]-stack.topOffsets[index]);
      const scaleSamples=[...stack.scaleSamples,{scrollY:endY,scales:stack.endScales}];
      const scale=valueAt(scaleSamples,'scales',index,scrollY);
      card.style.transform=`translate3d(0,${shift}px,0) scale(${scale})`;
      const textSamples=[...stack.innerTextSamples,{scrollY:endY,translations:stack.innerEndTranslations}];
      const translation=valueAt(textSamples,'translations',index,scrollY);
      card.querySelector('.left-text-container').style.transform=`translate3d(0,${translation}px,0)`;
    });
  }
  function queue(){if(!pending){pending=true;requestAnimationFrame(update);}}
  addEventListener('scroll',queue,{passive:true});addEventListener('resize',queue);update();
}

let corrected=original.slice(0,start)+JSON.stringify(config).replace(/</g,'\\u003c')+original.slice(end);
const runtime=/<script id="cohere-observed-stack">[\s\S]*?<\/script>/;
if(!runtime.test(corrected)) throw new Error('Missing prior bounded projection');
corrected=corrected.replace(runtime,`<script id="cohere-observed-stack">(${observedStackRuntime.toString()})();</script>`);
const backup=path.join(work,'cohere-oct11-pre-inner-content-navigation.html');
if(!fs.existsSync(backup)) fs.writeFileSync(backup,original);
fs.writeFileSync(file,corrected);
fs.writeFileSync(path.join(work,'cohere-oct11-inner-content-navigation-correction.json'),JSON.stringify({
  accepted:false,official_consistency_claim:false,previous_sha256:hash(original),corrected_sha256:hash(corrected),
  source_mode:'Official prefers-reduced-motion:reduce,1280×720 and390×844 desktop UA',
  canonical_reference:'cohere-reduced-oct10-official-1280-phases.json',
  prior_current_hash_capture:'cohere-oct10-local-1280-phases.json',
  fresh_inner_sources:['cohere-oct11-reduced-active-product-2160-settled-1280-reference.json','cohere-oct11-reduced-active-product-2880-1280-reference.json'],
  inner_content:{original_end_translations:endTranslations,samples:config.observedStack.innerTextSamples,calibration,
    method:'Remove captured final inner translateY and project actual canonical2160/2880 heading samples on original text containers. Fresh active ancestor styles confirm this independent inner motion exists; no copy or artwork replaced.'},
  narrow_navigation:{method:'At scroll0 show the original60px logo/hamburger nav below the actual80px announcement; after scrolling retain the captured original hidden class.',source:read('cohere-reduced-oct10-official-390-phases.json')[0].screenshot},
  actual_render_after_correction_verified:false,
  limits:['Between-sample inner/card transforms and nav hide timing are bounded static projections; exact GSAP timing remains unverified.',
    'Canonical and fresh active source phases differ by load/animation time and80px overall page height; both original references are retained.',
    'Rive/video and logo carousel phases are not synchronized; current-hash full desktop/narrow raster QA is required.']
},null,2)+'\n');
console.log(JSON.stringify({brand:'cohere',bytes:Buffer.byteLength(corrected),sha256:hash(corrected),text_samples:config.observedStack.innerTextSamples,accepted:false}));
