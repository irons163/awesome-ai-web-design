// Public study navigation; source templates and exact official links only.
(()=>{let closed='',state=null,bodyStyle=null,wordObserver;
function updateAnchors(){const anchors=[...document.querySelectorAll('a.js-anchor[data-id]')];let current=anchors[0];for(const a of anchors){const section=document.getElementById(a.dataset.id);if(section&&section.getBoundingClientRect().top<200)current=a;}if(current){anchors.forEach(a=>a.setAttribute('data-active',String(a===current)));const label=current.closest('mistral-atom-spoiler')?.querySelector('.js-spoiler-trigger button p');if(label)label.textContent=current.textContent.trim();}}
function setup(){closed=document.querySelector('header')?.outerHTML||'';bodyStyle=document.body.getAttribute('style');state=null;wordObserver?.disconnect();wordObserver=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.style.transform='translate(0%, 0%)';wordObserver.unobserve(entry.target);}}),{threshold:0});document.querySelectorAll('[data-string-slide]').forEach(e=>wordObserver.observe(e));updateAnchors();}
function close(){if(closed)document.querySelector('header').outerHTML=closed;if(bodyStyle===null)document.body.removeAttribute('style');else document.body.setAttribute('style',bodyStyle);state=null;}
function show(name){const v=CONFIG.menus[name];if(!v)return;document.querySelector('header').outerHTML=v.html;document.body.style.overflow='hidden';state=name;}
document.addEventListener('mistral-study-ready',setup);setup();
document.addEventListener('keydown',e=>{if(e.key==='Escape')close();});
document.addEventListener('scroll',updateAnchors,{passive:true});
document.addEventListener('click',e=>{const trigger=e.target.closest('.js-spoiler-trigger');if(trigger){const spoiler=trigger.closest('mistral-atom-spoiler');const panel=spoiler?.querySelector('.js-spoiler-content');if(panel){const opened=spoiler.getAttribute('data-open')==='true';spoiler.setAttribute('data-open',String(!opened));panel.style.height=opened?'0px':'auto';return;}}
const b=e.target.closest('button');if(!b)return;
if(b.id==='mobile-menu-button'){e.preventDefault();state?close():show('root');return;}
if(b.closest('#mobile-nav-panel')){const text=b.textContent.trim();if(text==='Research'){e.preventDefault();show('research');return;}const destination={'Sovereign AI':'https://mistral.ai/sovereign-ai/','Cloud':'https://mistral.ai/cloud/inference/','Customers':'https://mistral.ai/customers/','Company':'https://mistral.ai/about/'}[text];if(destination){e.preventDefault();location.assign(destination);return;}if(b.getAttribute('aria-label')?.toLowerCase().includes('back')){show('root');return;}}
});})();
