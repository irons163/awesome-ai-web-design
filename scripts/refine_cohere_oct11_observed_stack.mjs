import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {JSDOM, VirtualConsole} from 'jsdom';

const work=path.resolve('.stitch-work/current-official');
const file=path.join(work,'cohere.html');
const original=fs.readFileSync(file,'utf8');
if(original.includes('id="cohere-observed-stack"')) throw new Error('Correction already installed');
const hash=value=>crypto.createHash('sha256').update(value).digest('hex');
const read=name=>JSON.parse(fs.readFileSync(path.join(work,name),'utf8'));
const start=original.indexOf('const CONFIG=')+13;
const end=original.indexOf(';(function runtime',start);
const config=JSON.parse(original.slice(start,end));
const styles2160=read('cohere-oct11-reduced-active-product-2160-styles.json');
const styles2880=read('cohere-oct11-reduced-active-product-2880-styles.json');
const top=read('cohere-oct11-reduced-top-announcement-1280-reference.json');
const activeNames=['cohere-oct11-reduced-active-product-2160-settled-1280-reference.json',
  'cohere-oct11-reduced-active-product-2880-1280-reference.json'];
const sourceRecords=activeNames.map(name=>({name,record:read(name)}));
for(const {record} of sourceRecords) {
  const html=record.htmlParts.join('');
  if(html.length!==record.html_length||hash(html)!==record.html_sha256||html.includes('[Truncated]')) throw new Error('Incomplete active source');
}
const document=new JSDOM(config.bodies[1280],{virtualConsole:new VirtualConsole()}).window.document;
const cards=[...document.querySelectorAll('[class*="pin-spacer-stacking"]')];
if(cards.length!==3) throw new Error('Expected exactly three desktop pin spacers');
const originalStyles=cards.map(spacer=>spacer.firstElementChild.getAttribute('style'));
const scales=rows=>rows.map(row=>Number(/matrix\(([^,]+)/.exec(row.childTransform)?.[1]||1));
const maxShifts=originalStyles.map(style=>Number(/translate\(0px, ([\d.]+)px\)/.exec(style)?.[1]||0));
if(JSON.stringify(maxShifts)!=='[1017,513,9]') throw new Error('Canonical end state changed');
config.observedStack={maxShifts,originalStyles,topOffsets:[115.375,180.375,245.375],
  scaleSamples:[{scrollY:0,scales:[1,1,1]},{scrollY:2160,scales:scales(styles2160)},
    {scrollY:2880,scales:scales(styles2880)}],endScales:[0.975,0.9875,1],announcementHeight:48};
cards.forEach(spacer=>{
  const card=spacer.firstElementChild;
  card.style.transform='translate3d(0,0,0)';
  card.style.position='relative';card.style.left='0px';card.style.top='0px';
});
config.bodies[1280]=document.body.innerHTML;

function observedStackRuntime(){
  let pending=false;
  function update(){
    pending=false;
    if(matchMedia('(max-width:767px)').matches) return;
    const stack=CONFIG.observedStack;
    const nav=[...document.querySelectorAll('nav')].find(node=>node.classList.contains('lg:block'));
    if(nav) nav.style.top=`${Math.max(0,stack.announcementHeight-scrollY)}px`;
    const spacers=[...document.querySelectorAll('[class*="pin-spacer-stacking"]')];
    spacers.forEach((spacer,index)=>{
      const card=spacer.firstElementChild;
      const naturalTop=spacer.getBoundingClientRect().top+scrollY;
      const shift=Math.max(0,Math.min(stack.maxShifts[index],scrollY+stack.topOffsets[index]-naturalTop));
      const samples=[...stack.scaleSamples,{scrollY:Math.max(2881,naturalTop+stack.maxShifts[index]-stack.topOffsets[index]),scales:stack.endScales}];
      let scale=samples.at(-1).scales[index];
      for(let i=1;i<samples.length;i++) if(scrollY<=samples[i].scrollY){
        const a=samples[i-1],b=samples[i];
        const ratio=Math.max(0,Math.min(1,(scrollY-a.scrollY)/(b.scrollY-a.scrollY)));
        scale=a.scales[index]+(b.scales[index]-a.scales[index])*ratio;break;
      }
      card.style.transform=`translate3d(0,${shift}px,0) scale(${scale})`;
    });
  }
  function queue(){if(!pending){pending=true;requestAnimationFrame(update);}}
  addEventListener('scroll',queue,{passive:true});addEventListener('resize',queue);update();
}
let corrected=original.slice(0,start)+JSON.stringify(config).replace(/</g,'\\u003c')+original.slice(end);
corrected=corrected.replace('</body>',`<script id="cohere-observed-stack">(${observedStackRuntime.toString()})();</script></body>`);
const backup=path.join(work,'cohere-oct11-pre-observed-stack.html');
if(!fs.existsSync(backup)) fs.writeFileSync(backup,original);
fs.writeFileSync(file,corrected);
fs.writeFileSync(path.join(work,'cohere-oct11-observed-stack-correction.json'),JSON.stringify({
  accepted:false,official_consistency_claim:false,previous_sha256:hash(original),corrected_sha256:hash(corrected),
  source_mode:'Official prefers-reduced-motion:reduce,1280×720 desktop UA',
  canonical_full_reference_preserved:['cohere-reduced-oct10-official-1280-reference.json','cohere-reduced-oct10-official-1280-phases.json'],
  fresh_active_sources:sourceRecords.map(({name,record})=>({name,observed_at:record.observed_at,scrollY:record.scrollY,bodyHeight:record.bodyHeight,html_sha256:record.html_sha256})),
  announcement:{source:'cohere-oct11-reduced-top-announcement-1280-reference.json',observed_at:top.observed_at,height:48,
    correction:'Restore observed desktop nav position below announcement at scroll0, then top0 after announcement leaves viewport; narrow template unchanged.'},
  stack:{maxShifts,topOffsets:config.observedStack.topOffsets,scaleSamples:config.observedStack.scaleSamples,
    method:'Restore original three card contents and spacer dimensions; pin projection uses actual source fixed top offsets and observed2160/2880 scales, with canonical final travel limits.'},
  actual_render_after_correction_verified:false,
  limits:['Fresh active source body8867 differs from canonical full source8947; original full evidence remains canonical and unmodified.',
    'Projection between observed scroll samples and GSAP timing remains unverified. Last-card top increment65 is inferred from the first two observed offsets and canonical travel.',
    'Official normal no-preference mode remains blank in this environment and unverified; this study explicitly uses reduced-motion mode.',
    'Current hash requires fresh full desktop/narrow actual raster review; account, menu and services remain unverified.']
},null,2)+'\n');
console.log(JSON.stringify({brand:'cohere',bytes:Buffer.byteLength(corrected),sha256:hash(corrected),accepted:false}));
