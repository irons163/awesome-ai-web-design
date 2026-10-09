import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {JSDOM,VirtualConsole} from 'jsdom';

const work=path.resolve('.stitch-work/current-official');
const read=name=>JSON.parse(fs.readFileSync(path.join(work,name),'utf8'));
const hash=bytes=>crypto.createHash('sha256').update(bytes).digest('hex');
const parse=html=>new JSDOM(html,{virtualConsole:new VirtualConsole()}).window.document;

function runtime() {
  const templates={desktop:document.getElementById('study-desktop-source'),mobile:document.getElementById('study-mobile-source')};
  const narrow=matchMedia('(max-width:799px)');
  let mode,live=[];
  function install() {
    const next=narrow.matches?'mobile':'desktop';
    if (next===mode) return;
    live.forEach(node=>node.remove());
    const fragment=templates[next].content.cloneNode(true);
    live=[...fragment.childNodes];
    document.body.className=CONFIG.bodyClasses[next];
    document.documentElement.className=CONFIG.htmlClasses[next];
    document.body.insertBefore(fragment,document.getElementById('study-runtime'));
    mode=next;
    document.querySelectorAll('video').forEach(video=>{
      video.muted=true;video.playsInline=true;
      if (video.closest('.simple-hero-banner,.fullwidth-image-signpost')) {
        video.autoplay=true;video.loop=true;video.play().catch(()=>{});
      }
    });
    const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{
      if (!entry.isIntersecting) return;
      const element=entry.target;
      element.classList.add('animate');
      element.classList.add('animate--'+(element.dataset.animation||'fade-in-top'));
      observer.unobserve(element);
    }));
    document.querySelectorAll('[data-animate]').forEach(element=>observer.observe(element));
    if(CONFIG.brand==='pinterest'){
      const list=document.querySelector('.carousel--mode-multi-brand-module-carousel');
      if(list){
        const update=()=>document.querySelectorAll('[data-test-id="carousel-overlay-previous"],[data-test-id="carousel-overlay-next"]').forEach(button=>{
          const previous=button.getAttribute('data-test-id').endsWith('previous');
          const shown=previous?list.scrollLeft>1:list.scrollLeft<list.scrollWidth-list.clientWidth-1;
          button.parentElement.classList.toggle('opacity0_k',!shown);
          button.parentElement.classList.toggle('opacity1_k',shown);
          button.parentElement.style.pointerEvents=shown?'auto':'none';
        });
        list.addEventListener('scroll',update,{passive:true});update();
      }
    }
  }
  function menu(open) {
    const element=document.getElementById('menu');
    if (!element||!CONFIG.menuOpening) return;
    document.documentElement.className=open?CONFIG.menuOpening.htmlClass:CONFIG.htmlClasses[mode];
    document.body.className=open?CONFIG.menuOpening.bodyClass:CONFIG.bodyClasses[mode];
    element.classList.toggle('mm-menu--opened',open);
    element.toggleAttribute('inert',!open);
    document.body.style.overflow=open?'hidden':'';
    const control=document.querySelector('a[href="#menu"]');
    if(control)control.setAttribute('aria-expanded',String(open));
  }
  function carousel(control) {
    const section=control.closest('section');
    const container=section?.querySelector('.swiper');
    if(!container)return;
    const wrapper=container.querySelector('.swiper-wrapper');
    const slides=[...wrapper.children].filter(e=>e.classList.contains('swiper-slide'));
    let index=Number(container.dataset.studyIndex||0);
    if(control.matches('.swiper-pagination-bullet')) {
      index=[...section.querySelectorAll('.swiper-pagination-bullet')].indexOf(control);
    } else index+=control.closest('.swiper-button-prev')?-1:1;
    index=Math.max(0,Math.min(slides.length-1,index));
    container.dataset.studyIndex=index;
    if(section.classList.contains('vertical-carousel')) {
      slides.forEach((slide,i)=>{
        slide.style.opacity=i===index?'1':'0';
        slide.style.pointerEvents=i===index?'auto':'none';
        slide.style.transform='translate3d('+(-i*container.clientWidth)+'px,0,0)';
        slide.classList.toggle('swiper-slide-active',i===index);
        const video=slide.querySelector('video');
        if(video){if(i===index)video.play().catch(()=>{});else video.pause();}
      });
    } else {
      wrapper.style.transform='translate3d('+(-index*(slides[0].getBoundingClientRect().width+16))+'px,0,0)';
    }
    section.querySelectorAll('.swiper-pagination-bullet').forEach((dot,i)=>dot.classList.toggle('swiper-pagination-bullet-active',i===index));
    section.querySelectorAll('.swiper-button-prev').forEach(button=>{button.disabled=index===0;button.classList.toggle('swiper-button-disabled',index===0);});
    section.querySelectorAll('.swiper-button-next').forEach(button=>{button.disabled=index===slides.length-1;button.classList.toggle('swiper-button-disabled',index===slides.length-1);});
  }
  document.addEventListener('click',event=>{
    const control=event.target.closest('a,button');if(!control)return;
    if(CONFIG.brand==='vodafone') {
      if(control.matches('a[href="#menu"]')){event.preventDefault();menu(true);return;}
      if(control.matches('a[href="#page"],.mm-wrapper__blocker,.mm-btn--close')){event.preventDefault();menu(false);return;}
      if(control.closest('#menu')&&control.matches('.mm-btn--next,.mm-btn--prev')) {
        const panel=document.querySelector(control.getAttribute('href'));
        if(panel){
          event.preventDefault();
          const item=control.closest('.mm-listitem--vertical');
          if(item&&item.contains(panel)){
            const opened=item.classList.toggle('mm-listitem--opened');
            item.classList.toggle('hovered',opened);
            control.setAttribute('aria-expanded',String(opened));
          }else document.querySelectorAll('#menu .mm-panel:not(.mm-panels)').forEach(p=>p.classList.toggle('mm-panel--opened',p===panel));
        }return;
      }
      if(control.matches('.action-button')) {
        const video=control.closest('section')?.querySelector('video');
        if(video){
          const sync=()=>{
            control.dataset.studyPaused=String(video.paused);
            control.setAttribute('aria-label',video.paused?'Play the video':'Pause the video');
          };
          if(video.paused)video.play().then(sync).catch(()=>{});else video.pause();
          sync();
        }return;
      }
      const slider=control.closest('.swiper-button-prev,.swiper-button-next,.swiper-pagination-bullet');
      if(slider){event.preventDefault();carousel(slider);return;}
    } else {
      const label=control.getAttribute('aria-label')||control.textContent.trim();
      if(/^(Log in|I already have an account)$/.test(label)){location.assign('https://www.pinterest.com/login/');return;}
      if(/Sign up|Join Pinterest|Continue/.test(label)){location.assign('https://www.pinterest.com/');return;}
      if(/^View (Previous|Next)$/.test(label)) {
        const list=document.querySelector('.carousel--mode-multi-brand-module-carousel');
        if(list){
          const [first,second]=list.children;
          const pitch=second?second.offsetLeft-first.offsetLeft:list.clientWidth;
          const step=pitch>0?Math.ceil(list.clientWidth/pitch)*pitch:list.clientWidth;
          list.scrollBy({left:(label.endsWith('Previous')?-1:1)*step,behavior:'smooth'});
        }return;
      }
    }
  });
  document.addEventListener('submit',event=>{event.preventDefault();location.assign(CONFIG.brand==='pinterest'?'https://www.pinterest.com/':'https://www.vodafone.com/');});
  document.addEventListener('keydown',event=>{if(event.key==='Escape')menu(false);});
  narrow.addEventListener('change',install);
  install();
}

for(const brand of ['vodafone','pinterest']) {
  const native=read(brand+'-stitch-generated.json');
  if(!native.screens?.length)throw new Error('A genuine native Stitch export is required before creating a working draft');
  for(const screen of native.screens)for(const file of screen.exports){
    const bytes=fs.readFileSync(path.join(work,file.path));
    if(bytes.length!==file.bytes||hash(bytes)!==file.sha256)throw new Error('Original native export was modified');
  }
  const assets=new Map();
  const prior=path.join(work,brand+'-asset-provenance.json');
  if(fs.existsSync(prior))for(const a of JSON.parse(fs.readFileSync(prior)).assets||[])if(a.retained)assets.set(a.source_url,a);
  for(const a of read(brand+'-browser-asset-provenance.json').assets)assets.set(a.source_url,a);
  for(const a of assets.values()) {
    const bytes=fs.readFileSync(path.join(work,a.path));
    if(bytes.length!==a.bytes||hash(bytes)!==a.sha256)throw new Error('Original public asset differs from provenance');
  }
  const origin=brand==='vodafone'?'https://www.vodafone.com/':'https://www.pinterest.com/';
  const url=(value,base=origin)=>{
    if(!value||/^(#|data:|mailto:|tel:)/i.test(value))return value;
    if(/^javascript:/i.test(value))return '#';
    const absolute=new URL(value,base).href;
    return assets.get(absolute)?.path||absolute;
  };
  const css=(text,base=origin)=>text.replace(/url\(\s*(['"]?)(.*?)\1\s*\)/g,(match,quote,value)=>/^(data:|#)/i.test(value)?match:'url("'+url(value,base)+'")');
  function localize(document) {
    document.querySelectorAll('base,meta[http-equiv],link:not([rel="stylesheet"]),[id^="codex-browser-"]').forEach(element=>element.remove());
    document.querySelectorAll('style').forEach(element=>element.textContent=css(element.textContent));
    document.querySelectorAll('link[rel="stylesheet"]').forEach(element=>{
      const absolute=new URL(element.getAttribute('href'),origin).href;
      const asset=assets.get(absolute);
      if(asset){const style=document.createElement('style');style.textContent=css(fs.readFileSync(path.join(work,asset.path),'utf8'),absolute);element.replaceWith(style);}
      else element.href=absolute;
    });
    document.querySelectorAll('*').forEach(element=>{
      for(const key of ['src','href','poster'])if(element.hasAttribute(key))element.setAttribute(key,url(element.getAttribute(key)));
      if(element.hasAttribute('style'))element.setAttribute('style',css(element.getAttribute('style')));
      if(element.hasAttribute('srcset'))element.setAttribute('srcset',element.getAttribute('srcset').split(',').map(item=>{const tokens=item.trim().split(/\s+/);tokens[0]=url(tokens[0]);return tokens.join(' ');}).join(', '));
    });
    // The source's JavaScript used data-src for later images. Browser-native
    // lazy loading retains those same original files without its tracker code.
    document.querySelectorAll('img[data-src]:not([src])').forEach(element=>{
      element.setAttribute('src',url(element.getAttribute('data-src')));
      element.loading='lazy';
    });
    document.querySelectorAll('input[type="email"],input[type="password"],input[type="date"]').forEach(element=>{element.readOnly=true;element.autocomplete='off';});
    // Keep Pinterest's own visible Google button; the live account iframe is
    // excluded from the study, so the public overlay supplies its click target.
    document.querySelectorAll('[data-test-id="dweb-google-button-social"]').forEach(element=>{
      element.setAttribute('aria-label','Continue with Google on Pinterest');
      element.style.pointerEvents='auto';
    });
    document.querySelectorAll('form').forEach(element=>{element.removeAttribute('action');element.removeAttribute('method');});
  }
  const documents={},references={};
  for(const mode of ['desktop','mobile']) {
    const reference=read(brand+'-'+mode+'-browser-reference.json');
    const html=reference.htmlParts.join('');
    if(hash(html)!==reference.html_sha256)throw new Error('Rendered source record changed');
    const document=parse(html);localize(document);documents[mode]=document;references[mode]=reference;
  }
  const configuration={brand,bodyClasses:{},htmlClasses:{}};
  for(const mode of ['desktop','mobile']){configuration.bodyClasses[mode]=documents[mode].body.className;configuration.htmlClasses[mode]=documents[mode].documentElement.className;}
  if(brand==='vodafone'){
    const menu=read('vodafone-mobile-menu-reference.json');
    configuration.menuOpening={htmlClass:menu.htmlClass,bodyClass:menu.bodyClass,menuClass:menu.menu.class,pageClass:menu.pageClass};
  }
  const head=documents.desktop.head;
  head.querySelectorAll('meta,title').forEach(node=>node.remove());
  const intro='<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>'+brand+' — dated official-site working study</title>';
  // Changing the original icon-play class also moves the hero button into the
  // text column. Change only its original icon glyph, preserving its geometry.
  const controls=brand==='vodafone'?'<style>.action-button[data-study-paused="true"]::before{content:"\\e91e"}</style>':'';
  const templates=['desktop','mobile'].map(mode=>'<template id="study-'+mode+'-source">'+documents[mode].body.innerHTML+'</template>').join('');
  const script='<script id="study-runtime">const CONFIG='+JSON.stringify(configuration).replace(/</g,'\\u003c')+';('+runtime.toString()+')();</script>';
  const html='<!doctype html><html lang="en"><head>'+intro+head.innerHTML+controls+'</head><body>'+templates+script+'</body></html>';
  fs.writeFileSync(path.join(work,brand+'.html'),html);
  fs.writeFileSync(path.join(work,brand+'-draft-build-record.json'),JSON.stringify({accepted:false,
    native_exports:brand+'-stitch-generated.json',source_references:Object.fromEntries(Object.entries(references).map(([mode,r])=>[mode,{file:brand+'-'+mode+'-browser-reference.json',observed_at:r.observed_at,html_sha256:r.html_sha256}])),
    asset_provenance:brand+'-browser-asset-provenance.json',working_draft:{path:brand+'.html',bytes:Buffer.byteLength(html),sha256:hash(html)},
    method:'Separate source-backed correction of genuine Stitch output. Original native exports and all original media bytes stay unchanged. Rendered comparison and complete behavior acceptance are pending.',
    limitations:brand==='pinterest'?['Narrow reference uses the existing browser and shows bodyWidth800 at390px; real mobile user-agent layout remains unverified.','Original public Google-button SVG and overlay retained, with its live account frame excluded; sign-in/sign-up actions go to the official website and the study does not collect credentials.']:['Exact media frame/timing, all carousels, desktop mega-menus, search, footer accordions, tablet and live publication require review.']},null,2)+'\n');
  console.log(JSON.stringify({brand,bytes:Buffer.byteLength(html),sha256:hash(html),assets:assets.size}));
}
