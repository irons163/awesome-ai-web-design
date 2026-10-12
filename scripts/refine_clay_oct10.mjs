// Clay Global: observed static hero phase and scroll header behavior.
import fs from 'node:fs';
const file='.stitch-work/current-official/clay.html';
let html=fs.readFileSync(file,'utf8');
function correction(){
  function install(){
    const header=document.querySelector('header');if(!header)return;
    const updateHeader=()=>{
      const h=document.querySelector('header');if(!h)return;
      h.className='Header_Header__wKE8N Header_Header_white__e_hFz';
      h.style.setProperty('background-color','transparent','important');
      h.style.setProperty('transform',scrollY>100?'translateY(-110%)':'none','important');
      h.querySelectorAll('[class*="inverted"]').forEach(e=>{e.className=e.className.split(' ').filter(c=>!c.includes('inverted')).join(' ');});
      h.querySelectorAll('[class*="Header_ContactLink"]').forEach(e=>{e.style.background='#17191f';e.style.color='#fff';});
      h.querySelectorAll('img').forEach(e=>e.style.setProperty('filter','brightness(0)','important'));
    };
    updateHeader();document.addEventListener('scroll',updateHeader,{passive:true,capture:true});
    if(innerWidth>=768){
      const hero=document.querySelector('[class*="HomeHero_TopWrapper"]');
      if(hero){const stage=hero.querySelector('[class*="HomeHero_StageWrapper"]');if(stage)stage.style.visibility='hidden';
        const image=document.createElement('img');image.src='clay-assets/oct10/observed-hero-3d-phase.png';image.alt='Observed static phase of Clay Global 3D homepage artwork';image.style.cssText='position:absolute;left:calc(50% + 120px);top:100px;width:470px;height:600px;object-fit:contain;pointer-events:none;';hero.style.position='relative';hero.append(image);}
    }
    const fintech=document.querySelector('[class*="IndustriesPreview_GlobalLink"]');
    if(fintech){fintech.style.position='relative';fintech.style.backgroundColor='#17191f';const art=document.createElement('img');art.src='clay-assets/oct10/observed-fintech-3d-region.png';art.alt='Observed static region of Clay fintech artwork';art.style.cssText='position:absolute;right:0;top:0;height:100%;width:'+(innerWidth>=768?'40%':'55%')+';object-fit:cover;z-index:1;pointer-events:none;';fintech.append(art);const content=fintech.querySelector('[class*="CryptoPreview__container"]');if(content){content.style.position='relative';content.style.zIndex='2';content.style.background='transparent';}}
  }
  install();matchMedia('(max-width:767px)').addEventListener('change',()=>requestAnimationFrame(install));
}
html=html.replace(/<script id="clay-current-corrections">[\s\S]*?<\/script>/g,'');
html=html.replace('</body>','<script id="clay-current-corrections">('+correction.toString()+')();</script></body>');
fs.writeFileSync(file,html);
console.log('Clay current static phase and header correction installed');
