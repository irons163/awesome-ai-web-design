// Small public-preview controls; account, ordering, chat and live network services remain official links.
(()=>{
let closedMenu='',closedBody='',openName=null,suppressHover=false;
const menuNames=['Vehicles','Energy','Charging','Semi','Discover'];
function setup(){closedMenu=document.querySelector('#mega-menu')?.outerHTML||'';closedBody=document.body.className;openName=null;}
function close(){suppressHover=true;const m=document.querySelector('#mega-menu');if(m&&closedMenu)m.outerHTML=closedMenu;document.body.className=closedBody;openName=null;}
function open(name){const mobile=matchMedia('(max-width:767px)').matches;const source=CONFIG.menus[mobile?'mobile':'desktop'][name];if(!source)return;document.querySelector('#mega-menu').outerHTML=source.html;document.body.className=source.bodyClass||closedBody+' tds-modal--is-open tds-site-header-panel--is-open';openName=name;}
function heroSlide(hero,index){const slides=[...hero.querySelectorAll('.tcl-flex-module-carousel__slides > .tcl-flex-module-carousel__slide')];index=(index+slides.length)%slides.length;slides.forEach((s,i)=>s.classList.toggle('tcl-flex-module-carousel__slide--active',i===index));hero.querySelectorAll('[aria-label="Tab List"]').forEach(n=>[...n.querySelectorAll('[role="tab"]')].forEach((t,i)=>t.setAttribute('aria-selected',String(i===index))));}
document.addEventListener('tesla-study-ready',setup);setup();
document.addEventListener('keydown',e=>{if(e.key==='Escape')close();});
document.addEventListener('pointermove',e=>{if(!e.target.closest('#tds-site-header'))suppressHover=false;});
document.addEventListener('pointermove',e=>{if(suppressHover||matchMedia('(max-width:767px)').matches)return;const b=e.target.closest('#tds-site-header button');if(b&&menuNames.includes(b.textContent.trim())&&openName!==b.textContent.trim())open(b.textContent.trim());});
document.addEventListener('click',e=>{
const b=e.target.closest('button,[role="tab"]');
if(!b){if(openName&&!e.target.closest('#mega-menu'))close();return;}
if(b.closest('#mega-menu')){
const name=b.textContent.trim(), label=b.getAttribute('aria-label');
if(label==='Close Panel'){e.preventDefault();close();return;}
if(label==='Back'){e.preventDefault();open('Root');return;}
if(name==='Menu'){e.preventDefault();open('Root');return;}
if(menuNames.includes(name)){e.preventDefault();open(name);return;}
}
const hero=b.closest('.tcl-flex-module-carousel--homepage_hero_carousel');
if(hero){const slides=[...hero.querySelectorAll('.tcl-flex-module-carousel__slides > .tcl-flex-module-carousel__slide')];const i=slides.findIndex(s=>s.classList.contains('tcl-flex-module-carousel__slide--active'));const nav=b.closest('[aria-label="Tab List"]');if(nav)heroSlide(hero,[...nav.querySelectorAll('[role="tab"]')].indexOf(b));else if(b.getAttribute('aria-label')==='Next Slide')heroSlide(hero,i+1);else if(b.getAttribute('aria-label')==='Previous Slide')heroSlide(hero,i-1);return;}
const container=b.closest('.tcl-freeflow-carousel__container');
if(container){const list=container.querySelector('.tcl-freeflow-carousel-container__slides');const slides=[...container.querySelectorAll('.tcl-freeflow-carousel-container__slide-container')];const scroller=[...container.querySelectorAll('*')].find(n=>n.scrollWidth>n.clientWidth+20&&/auto|scroll/.test(getComputedStyle(n).overflowX));if(scroller){const isTab=b.matches('[role="tab"]');const current=Math.round(scroller.scrollLeft/(slides[0]?.getBoundingClientRect().width||1));const dotList=b.closest('[aria-label="Tab List"]');const target=isTab?(dotList?[...dotList.querySelectorAll('[role="tab"]')].indexOf(b):slides.indexOf(b)):current+(b.getAttribute('aria-label')?.includes('Previous')?-1:1);const idx=Math.max(0,Math.min(slides.length-1,target));scroller.scrollTo({left:slides[idx].offsetLeft-slides[0].offsetLeft,behavior:'smooth'});slides.forEach((s,i)=>s.setAttribute('aria-selected',String(i===idx)));}return;}
});
})();
