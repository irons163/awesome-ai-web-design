/* Dated public interface study. Values are snapshots; account actions use official links. */
(() => {
 const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
 const branch=()=>$('.study-'+(matchMedia('(max-width:767px)').matches?'mobile':'desktop'));
 const minus=$('svg',$('template[data-study-minus]').content).innerHTML;
 for(const trigger of $$('.study-faq-trigger')){
  const answer=$('.study-faq-answer',trigger.parentElement),svg=$('svg',trigger),closed=svg?.innerHTML;
  const toggle=()=>{const open=trigger.getAttribute('aria-expanded')!=='true';trigger.setAttribute('aria-expanded',String(open));answer.classList.toggle('hidden',!open);answer.classList.toggle('block',open);trigger.parentElement.classList.toggle('active',open);trigger.parentElement.classList.toggle('bg-Vessel',open);if(svg)svg.innerHTML=open?minus:closed;};
  trigger.addEventListener('click',toggle);trigger.addEventListener('keydown',e=>{if(['Enter',' '].includes(e.key)){e.preventDefault();toggle();}});
 }
 for(const group of $$('.study-footer-group')){
  const heading=$('h3',group),list=$('ul',group),svg=$('svg',heading),closed=svg?.innerHTML;
  const toggle=()=>{if(matchMedia('(max-width:767px)').matches){const open=!group.classList.contains('study-footer-open');group.classList.toggle('study-footer-open',open);heading.setAttribute('aria-expanded',String(open));list.classList.toggle('active',open);list.style.display=open?'block':'';if(svg)svg.innerHTML=open?minus:closed;}};
  heading.addEventListener('click',toggle);heading.addEventListener('keydown',e=>{if(['Enter',' '].includes(e.key)){e.preventDefault();toggle();}});
 }
 for(const market of $$('.study-market')){
  const tabs=$$('[data-study-market-tab]',market),panels=$$('[role=tabpanel]',market),original=panels.map(p=>p.cloneNode(true));
  if(!tabs.length||!panels.length)continue;
  const activeClasses=tabs[0].className.split(/\s+/).filter(c=>!tabs[1].className.split(/\s+/).includes(c));
  const select=(label)=>{
   const mode=market.closest('[data-study-branch]').dataset.studyBranch;
   const template=$$('template[data-study-market-template]').find(t=>t.dataset.studyMarketTemplate===mode+':'+label);
   const current=$$('[role=tabpanel]',market);
   const host=current[0].parentElement;current.forEach(p=>p.remove());
   const replacement=label==='Popular'?original[0].cloneNode(true):template?.content.firstElementChild.cloneNode(true);
   if(replacement){replacement.setAttribute('aria-hidden','false');replacement.style.display='';replacement.id=original[0].id;replacement.setAttribute('aria-labelledby',tabs.find(t=>t.dataset.studyMarketTab===label).id);host.append(replacement);}
   tabs.forEach(t=>{const active=t.dataset.studyMarketTab===label;t.setAttribute('aria-selected',String(active));t.tabIndex=active?0:-1;activeClasses.forEach(c=>t.classList.toggle(c,active));});
  };
  tabs.forEach((tab,i)=>{tab.addEventListener('click',()=>select(tab.dataset.studyMarketTab));tab.addEventListener('keydown',e=>{if(['ArrowLeft','ArrowRight','Home','End'].includes(e.key)){e.preventDefault();const index=e.key==='Home'?0:e.key==='End'?tabs.length-1:(i+(e.key==='ArrowRight'?1:-1)+tabs.length)%tabs.length;select(tabs[index].dataset.studyMarketTab);tabs[index].focus();}});});
 }
 document.addEventListener('click',e=>{
  const tab=e.target.closest('[data-study-download-tab]');if(!tab)return;
  const wanted=tab.dataset.studyDownloadTab,template=$$('template[data-study-download-template]').find(t=>t.dataset.studyDownloadTemplate===wanted);
  const app=$('.study-app',branch()),parent=app.firstElementChild,section=parent.children[3];
  if(template&&section)section.replaceWith(template.content.firstElementChild.cloneNode(true));
 });
 const notice=$('#cm-banner-sdk'),preferences=$('#onetrust-pc-sdk'),mask=$('.onetrust-pc-dark-filter');
 const hideCookies=()=>{if(notice)notice.style.display='none';if(preferences)preferences.style.display='none';if(mask)mask.style.display='none';$('.study-cookie-dialog')?.remove();document.body.style.overflow='';};
 const manage=()=>{
  if(!$('style[data-study-cookie-loaded]')){const style=$('template[data-study-cookie-styles]').content.firstElementChild.cloneNode(true);style.setAttribute('data-study-cookie-loaded','');document.head.append(style);}
  hideCookies();closeMenus();const dialog=$('template[data-study-cookie-manager]').content.firstElementChild.cloneNode(true);dialog.classList.add('study-cookie-dialog');document.body.append(dialog);document.body.style.overflow='hidden';
  const originals=new Map($$('.manageCookieModal-accordionItem',dialog).map(n=>[$('.manageCookieModal-categoryTitle',n).textContent,n.cloneNode(true)]));
  const switchChoice=n=>{const checked=n.getAttribute('aria-checked')!=='true';n.setAttribute('aria-checked',String(checked));n.classList.toggle('checked',checked);};
  const toggleCategory=row=>{const owner=row.closest('.manageCookieModal-accordionItem'),label=$('.manageCookieModal-categoryTitle',row).textContent,open=row.getAttribute('aria-expanded')!=='true',template=$$('template[data-study-cookie-category]').find(t=>t.dataset.studyCookieCategory===label),checked=$('[role=switch]',owner)?.getAttribute('aria-checked')==='true';const replacement=open?template.content.firstElementChild.cloneNode(true):originals.get(label).cloneNode(true);const choice=$('[role=switch]',replacement);if(choice){choice.setAttribute('aria-checked',String(checked));choice.classList.toggle('checked',checked);}owner.replaceWith(replacement);};
  dialog.addEventListener('click',e=>{const choice=e.target.closest('[role=switch]');if(choice){switchChoice(choice);return;}const row=e.target.closest('.manageCookieModal-categoryRow');if(row)toggleCategory(row);});
  dialog.addEventListener('keydown',e=>{if(!['Enter',' '].includes(e.key))return;const choice=e.target.closest('[role=switch]'),row=e.target.closest('.manageCookieModal-categoryRow');if(choice||row){e.preventDefault();if(choice)switchChoice(choice);else toggleCategory(row);}});
  const close=$('.bn-modal-header-next',dialog);close.tabIndex=0;close.addEventListener('click',hideCookies);close.addEventListener('keydown',e=>{if(['Enter',' '].includes(e.key))hideCookies();});
  for(const button of $$('button',dialog))button.addEventListener('click',()=>{try{localStorage.setItem('binance-study-cookie-choice',button.textContent.includes('Reject')?'rejected':'saved');}catch{}hideCookies();});
 };
 try{if(notice){notice.style.display=localStorage.getItem('binance-study-cookie-choice')?'none':'flex';notice.style.visibility='visible';notice.style.opacity='1';}}catch{}
 for(const button of $$('button',notice||document.createElement('div'))){button.addEventListener('click',()=>{if(/Manage/i.test(button.textContent))manage();else{try{localStorage.setItem('binance-study-cookie-choice',/Reject/i.test(button.textContent)?'rejected':'accepted');}catch{}hideCookies();}});}
 for(const element of $$('a,button,span'))if(element.textContent.trim()==='Cookie Preferences')element.addEventListener('click',e=>{e.preventDefault();manage();});
 for(const button of $$('button',preferences||document.createElement('div'))){if(/Reject|Confirm|Close|Save|Allow|Accept/i.test(button.textContent+' '+button.getAttribute('aria-label')))button.addEventListener('click',()=>{try{localStorage.setItem('binance-study-cookie-choice','saved');}catch{}hideCookies();});}
 const closeMenus=()=>{for(const owner of $$('.header-menu-item-active')){owner.classList.remove('header-menu-item-active');$('.header-menu-subgrid',owner)?.remove();}$('.study-mobile-drawer')?.remove();document.body.style.overflow='';};
 for(const template of $$('template[data-study-desktop-menu]')){
  const control=$('#desktop-'+template.dataset.studyDesktopMenu),owner=control?.parentElement;if(!owner)continue;
  control.setAttribute('role','button');control.setAttribute('aria-expanded','false');control.tabIndex=0;
  const show=()=>{closeMenus();owner.append(template.content.firstElementChild.cloneNode(true));owner.classList.add('header-menu-item-active');control.setAttribute('aria-expanded','true');};
  control.addEventListener('click',show);
  owner.addEventListener('mouseenter',show);owner.addEventListener('mouseleave',()=>{owner.classList.remove('header-menu-item-active');$('.header-menu-subgrid',owner)?.remove();control.setAttribute('aria-expanded','false');});
  control.addEventListener('keydown',e=>{if(['Enter',' '].includes(e.key)){e.preventDefault();show();}});
 }
 const showMobileMenu=()=>{
  closeMenus();const menu=$('template[data-study-mobile-menu]').content.firstElementChild.cloneNode(true);menu.classList.add('study-mobile-drawer');document.body.append(menu);document.body.style.overflow='hidden';
  const close=$('.header-nav-bar .close-btn-size',menu);close.setAttribute('role','button');close.setAttribute('aria-label','Close Menu');close.tabIndex=0;close.addEventListener('click',closeMenus);close.addEventListener('keydown',e=>{if(['Enter',' '].includes(e.key))closeMenus();});
  for(const item of $$('.header-rightnav-subitem',menu)){const trigger=$('.header-rightnav-subview',item),list=$('.header-nav-subgroup',item);trigger.setAttribute('role','button');trigger.setAttribute('aria-label',$('.header-nav-subtitle_text',trigger).textContent);trigger.setAttribute('aria-expanded','false');trigger.tabIndex=0;const toggle=()=>{const open=trigger.getAttribute('aria-expanded')!=='true';trigger.setAttribute('aria-expanded',String(open));list.style.height=open?'auto':'0px';};trigger.addEventListener('click',toggle);trigger.addEventListener('keydown',e=>{if(['Enter',' '].includes(e.key)){e.preventDefault();toggle();}});}
  for(const item of $$('.header-nav-itemnosub',menu)){const text=item.textContent.trim();if(text==='Download'||text==='24/7 Chat Support'){item.setAttribute('role','link');item.tabIndex=0;const visit=()=>open(text==='Download'?'https://www.binance.com/en/download':'https://www.binance.com/en/chat','_blank','noopener');item.addEventListener('click',visit);item.addEventListener('keydown',e=>{if(e.key==='Enter')visit();});}}
 };
 for(const control of $$('.header-menu-right-pickup')){control.setAttribute('role','button');control.setAttribute('aria-label','Open Menu');control.tabIndex=0;control.addEventListener('click',showMobileMenu);control.addEventListener('keydown',e=>{if(['Enter',' '].includes(e.key)){e.preventDefault();showMobileMenu();}});}
 for(const chat of $$('[id*="chat"]'))if(chat.id==='pre-chat-container')chat.addEventListener('click',()=>open('https://www.binance.com/en/chat?sourceEntry=4','_blank','noopener'));
 addEventListener('keydown',e=>{if(e.key==='Escape'){closeMenus();hideCookies();}});
})();
