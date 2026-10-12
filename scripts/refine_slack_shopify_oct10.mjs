import fs from 'node:fs/promises';
import {JSDOM,VirtualConsole} from 'jsdom';
const root=new URL('../.stitch-work/current-official/',import.meta.url);
for(const brand of process.argv.slice(2)){
 if(!['slack','shopify'].includes(brand))throw Error('Brand out of bounded scope');
 const official=brand==='slack'?'https://slack.com/':'https://www.shopify.com/ca';
 const source=await fs.readFile(new URL(brand+'-oct10-source.html',root),'utf8');
 const dom=new JSDOM(source,{url:official,virtualConsole:new VirtualConsole()});
 const d=dom.window.document;
 try{await fs.copyFile(new URL(brand+'.html',root),new URL(brand+'-oct10-before.html',root),fs.constants.COPYFILE_EXCL);}catch(e){if(e.code!=='EEXIST')throw e;}
 const removedScripts=d.querySelectorAll('script').length;
 d.querySelectorAll('script,iframe,noscript,link[rel=preload][as=script],link[rel=modulepreload],link[rel=preconnect],link[rel=dns-prefetch],#onetrust-consent-sdk,#onetrust-pc-sdk,#onetrust-banner-sdk').forEach(e=>e.remove());
 d.querySelectorAll('*').forEach(e=>{
  for(const a of [...e.attributes]){
   if(/^on/i.test(a.name)||a.name.startsWith('data-clog')||a.name.startsWith('data-gtm'))e.removeAttribute(a.name);
   else if(['src','href','poster','action','xlink:href'].includes(a.name)&&a.value&&!/^(#|data:|mailto:|tel:|javascript:)/i.test(a.value))e.setAttribute(a.name,new URL(a.value,official).href);
  }
  if(e.hasAttribute('loading'))e.setAttribute('loading','eager');
  if(e.tagName==='IMG'){
   const ds=e.getAttribute('data-src');if(ds&&(!e.getAttribute('src')||e.getAttribute('src').startsWith('data:')))e.src=new URL(ds,official).href;
  }
 });
 d.title=brand==='slack'?'Slack — Current official homepage reconstruction':'Shopify Canada — Current official homepage reconstruction';
 const provenance=d.createComment(` Educational reconstruction. Google Stitch native candidate preserved in ${brand}-oct10-stitch-raw.html and provider metadata. Corrected from complete public rendered official source observed 2026-10-10. No original application/tracking scripts execute. Full fidelity not accepted; see ${brand}-oct10-result.json. `);d.body.prepend(provenance);
 const style=d.createElement('style');style.id='oct10-local-corrections';style.textContent=`html{scroll-behavior:smooth} video{object-fit:cover} [data-local-dialog]{position:fixed;inset:0;z-index:999999;background:#fff;color:#111;padding:32px;overflow:auto} [data-local-dialog] button{float:right} [data-local-close]{cursor:pointer}`;
 if(brand==='slack')style.textContent+=` .c-nav.dismiss-nav{transform:none!important} .c-nav.is-fixed{top:0!important} .swiper-wrapper{transition:transform .35s ease!important} .c-home-whats-new-module__swiper{overflow:hidden} .c-extnav-level__0>.nav_parent.local-open>.c-extnav-level__1{display:block!important;visibility:visible!important;opacity:1!important;pointer-events:auto!important} .c-nav__mobile.local-open{display:block!important;visibility:visible!important;opacity:1!important;transform:none!important} .c-nav__mobile.local-open .c-nav__list{display:block} .c-footer__nav .nav_parent.local-open>ul{display:block!important} .c-bento-sticky-toc{z-index:10} `;
 d.head.append(style);
 const script=d.createElement('script');script.id='oct10-local-front-end';script.textContent=`(()=>{
const brand=${JSON.stringify(brand)};
const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)];
function dialog(title,text){const e=document.createElement('section');e.dataset.localDialog='';e.setAttribute('role','dialog');e.setAttribute('aria-modal','true');e.innerHTML='<button type="button">Close</button><h2></h2><p></p>'; $('h2',e).textContent=title;$('p',e).textContent=text;$('button',e).onclick=()=>e.remove();document.body.append(e);$('button',e).focus();}
function toggleMenu(open){const nav=$('#main_nav');if(!nav)return;nav.classList.toggle('is-hidden',!open);nav.classList.toggle('local-open',open);$('#nav_menu_btn')?.setAttribute('aria-expanded',String(open));document.body.style.overflow=open?'hidden':'';}
$('#nav_menu_btn')?.addEventListener('click',()=>toggleMenu(true));$('#nav_close_btn')?.addEventListener('click',()=>toggleMenu(false));
$$('.dropdown_button').forEach(b=>b.addEventListener('click',()=>{const p=b.parentElement,open=!p.classList.contains('local-open');p.classList.toggle('local-open',open);b.setAttribute('aria-expanded',String(open));}));
$$('[data-target-id]').forEach(b=>b.addEventListener('click',()=>document.getElementById(b.dataset.targetId)?.scrollIntoView({behavior:'smooth',block:'start'})));
$$('button.c-video-control').forEach(b=>b.addEventListener('click',()=>{const vs=$$('video',b.closest('section'));const paused=vs.some(v=>!v.paused);vs.forEach(v=>paused?v.pause():v.play().catch(()=>{}));b.setAttribute('aria-pressed',String(paused));}));
$$('.c-switcher-nav-item__heading-row').forEach(b=>b.addEventListener('click',()=>{const section=b.closest('section');if(!section)return;const bs=$$('.c-switcher-nav-item__heading-row',section),index=bs.indexOf(b);$$('.c-switcher-nav-item',section).forEach((e,i)=>e.classList.toggle('active',i===index));const items=$$('.c-switcher-item',section);items.forEach((e,i)=>e.classList.toggle('is-visible',i===index));const wrapper=$('.swiper-wrapper',section);if(wrapper){const slide=wrapper.children[index];if(slide)wrapper.style.transform='translate3d('+(-slide.offsetLeft)+'px,0,0)';}}));
$$('[data-js-swiper-next],[data-js-swiper-prev]').forEach(b=>b.addEventListener('click',()=>{const wrap=document.getElementById(b.getAttribute('aria-controls'));if(!wrap)return;const step=wrap.children[0]?.getBoundingClientRect().width+48||350;let index=Number(wrap.dataset.localIndex||0)+(b.hasAttribute('data-js-swiper-next')?1:-1);index=Math.max(0,Math.min(wrap.children.length-1,index));wrap.dataset.localIndex=index;wrap.style.transform='translate3d('+(-index*step)+'px,0,0)';}));
$$('#nav_search_btn,.nav_search_btn--m').forEach(b=>b.addEventListener('click',()=>{location.href='https://slack.com/help/search';}));
$('#new_locale_switcher')?.addEventListener('click',()=>{const menu=$('.c-locale-new-menu');if(menu){menu.hidden=false;menu.style.display='block';menu.classList.add('is-open');}});$('#btn_close_locale')?.addEventListener('click',()=>{const menu=$('.c-locale-new-menu');if(menu)menu.style.display='none';});
$$('a').forEach(a=>{if(a.getAttribute('href')==='javascript:void(0)'||a.textContent.trim()==='Your Privacy Choices'||a.textContent.trim()==='Cookie Preferences')a.addEventListener('click',e=>{e.preventDefault();dialog('Privacy choices','This educational reconstruction does not run the original vendor consent or account services.');});});
document.addEventListener('keydown',e=>{if(e.key==='Escape'){toggleMenu(false);$$('[data-local-dialog]').forEach(x=>x.remove());$$('.local-open').forEach(x=>x.classList.remove('local-open'));}});
})();`;
 d.body.append(script);
 await fs.writeFile(new URL(brand+'.html',root),'<!DOCTYPE html>\n'+d.documentElement.outerHTML);
 await fs.writeFile(new URL(brand+'-oct10-correction-provenance.json',root),JSON.stringify({official,observedAt:'2026-10-10',input:brand+'-oct10-source.html',output:brand+'.html',removedScripts,sourceComplete:source.trim().endsWith('</html>'),nativeCandidateRetained:brand+'-oct10-stitch-raw.html',method:'Current native Stitch edit plus explicit source-grounded manual reconstruction from observed public DOM/CSS, public images/fonts/video URLs; original application and tracking scripts removed; local UI controls recreated',fullyVerified:false},null,2));
 console.log(brand,'corrected',d.documentElement.outerHTML.length,'removedScripts',removedScripts);
}
