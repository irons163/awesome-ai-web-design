(() => {
  'use strict';
  const data = JSON.parse(document.getElementById('stripe-menu-templates').textContent);
  const header = document.querySelector('[data-stripe-static-header]');
  const menuHost = document.createElement('div');
  menuHost.className = 'stripe-menu-host';
  document.body.append(menuHost);
  const dialogHost = document.createElement('div');
  dialogHost.className = 'stripe-dialog-host';
  document.body.append(dialogHost);
  let menu = null, dialog = null, restoreFocus = null;
  const narrow = () => matchMedia('(max-width: 1023px)').matches;

  function closeMenu() {
    menuHost.replaceChildren(); menu = null;
    header.querySelectorAll('button[aria-expanded]').forEach(x => x.setAttribute('aria-expanded', 'false'));
    header.querySelectorAll('[data-status]').forEach(x => x.setAttribute('data-status', 'unmounted'));
    header.querySelector('#navigation-menu').classList.remove('hds-navigation-menu--open');
    header.querySelector('.navigation-menu__background')?.classList.remove('navigation-menu__background--mobile-visible');
    document.body.style.overflow = '';
  }
  function openMenu(name) {
    const mobile = narrow();
    if (menu === name) { closeMenu(); return; }
    closeMenu(); menu = name;
    const html = mobile ? data.mobile[name] : data.desktop[name];
    if (!html) { closeMenu(); return; }
    const bounds = header.querySelector('#navigation-menu').getBoundingClientRect();
    const y = bounds.bottom;
    const x = mobile ? 0 : bounds.x;
    const width = mobile ? innerWidth : bounds.width;
    menuHost.innerHTML = `${mobile?'<div data-status="open" data-value="root" class="hds-navigation-menu__overlay" style="position:fixed;overflow:auto;top:'+y+'px"></div>':''}<div class="hds-navigation-menu__positioner" style="--position-x:${x}px;--position-y:${y}px;--available-width:${innerWidth}px;--available-height:${innerHeight-y}px;--anchor-width:${width}px;--anchor-height:${bounds.height}px;--root-height:${bounds.height}px;--root-width:${width}px">${html}</div>`;
    header.querySelector('#navigation-menu').classList.add('hds-navigation-menu--open');
    header.querySelector('.navigation-menu__background')?.classList.toggle('navigation-menu__background--mobile-visible',mobile);
    const trigger = [...header.querySelectorAll('button')].find(x => mobile ? x.getAttribute('aria-label') === 'Toggle navigation menu' : x.textContent.trim() === name);
    if (trigger) trigger.setAttribute('aria-expanded', 'true');
    if (mobile) document.body.style.overflow = 'hidden';
  }
  header.addEventListener('click', e => {
    const button = e.target.closest('button'); if (!button) return;
    if (button.getAttribute('aria-label') === 'Toggle navigation menu') { openMenu('Root'); return; }
    const name = button.textContent.trim();
    if (data.desktop[name]) openMenu(name);
  });
  menuHost.addEventListener('click', e => {
    const button = e.target.closest('button'); if (!button) return;
    e.stopPropagation();
    const name = button.textContent.trim();
    if (name === 'Back') { openMenu('Root'); return; }
    if (data.mobile[name]) openMenu(name);
  });
  document.addEventListener('click', e => {
    if (menu && !header.contains(e.target) && !menuHost.contains(e.target)) closeMenu();
  });

  function closeDialog() {
    dialogHost.replaceChildren();
    document.querySelectorAll('.modular-solutions-bento-card').forEach(x => x.setAttribute('aria-expanded','false'));
    document.querySelector('main').removeAttribute('inert');
    header.removeAttribute('inert');
    document.body.style.overflow = '';
    dialog = null;
    restoreFocus?.focus();
  }
  function openDialog(key, button) {
    closeMenu(); restoreFocus = button; dialog = key;
    dialogHost.innerHTML = data.dialogs[key];
    dialogHost.querySelectorAll('[data-status]').forEach(x => x.setAttribute('data-status','open'));
    dialogHost.querySelectorAll('[data-state]').forEach(x => x.setAttribute('data-state','open'));
    document.querySelector('main').setAttribute('inert','');
    header.setAttribute('inert','');
    document.body.style.overflow = 'hidden';
    button.setAttribute('aria-expanded','true');
    dialogHost.querySelector('[aria-label="Close dialog"]')?.focus();
  }
  document.querySelectorAll('.modular-solutions-bento-card').forEach(button => {
    button.addEventListener('click', () => openDialog(button.getAttribute('aria-labelledby').replace('bento-card-title-',''),button));
  });
  dialogHost.addEventListener('click',e => {
    if(e.target.closest('[aria-label="Close dialog"]') || e.target.classList.contains('hds-dialog__overlay')) closeDialog();
  });
  document.addEventListener('keydown', e => {
    if(e.key === 'Escape') { if(dialog) closeDialog(); else closeMenu(); }
    if(e.key === 'Tab' && dialog) {
      const items = [...dialogHost.querySelectorAll('a[href],button')].filter(x=>x.getClientRects().length);
      const first = items[0], last = items.at(-1);
      if(e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if(!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  });

  const customerBreakpoint=matchMedia('(max-width:639px)');
  function setCustomerLayout(){
    const list=document.querySelector('.customer-stories');
    const wrapper=document.createElement('div');
    wrapper.innerHTML=customerBreakpoint.matches ? data.mobileCustomers : data.customers.Hertz;
    list.replaceChildren(...wrapper.firstElementChild.childNodes);
    if(!customerBreakpoint.matches)list.querySelectorAll('.customer-stories__customer-button').forEach(x=>x.tabIndex=0);
  }
  setCustomerLayout();customerBreakpoint.addEventListener('change',setCustomerLayout);
  const statsSection=document.querySelector('.stats-section');
  const desktopStatsClass=statsSection.className;
  function setStatsTheme(){statsSection.className=customerBreakpoint.matches?'hds-color-mode stats-section stats-section--dark stats-section--time-night section hds-mode--dark':desktopStatsClass;}
  setStatsTheme();customerBreakpoint.addEventListener('change',setStatsTheme);
  const sizeGraphics=()=>document.querySelectorAll('.dom-graphic').forEach(e=>{
    const sourceWidth=parseFloat(e.style.getPropertyValue('--graphic-source-width'));
    if(sourceWidth&&e.getBoundingClientRect().width)e.style.setProperty('--graphic-scale',e.getBoundingClientRect().width/sourceWidth);
  });
  new ResizeObserver(sizeGraphics).observe(document.body);sizeGraphics();
  document.addEventListener('click',e=>{
    const button=e.target.closest('.customer-stories__customer-button');
    if(!button || customerBreakpoint.matches)return;
    const key=button.getAttribute('aria-controls').replace('detail-customer-content-','');
    if(data.customers[key]) {
      const list=document.querySelector('.customer-stories');
      const wrapper=document.createElement('div');wrapper.innerHTML=data.customers[key];
      list.replaceChildren(...wrapper.firstElementChild.childNodes);
      list.querySelectorAll('.customer-stories__customer-button').forEach(x=>x.tabIndex=0);
    }
  });

  const stats=[...document.querySelectorAll('.stats-menu__stat')];
  stats.forEach((button,i)=>button.addEventListener('click',()=>{
    stats.forEach((x,j)=>x.classList.toggle('stats-menu__stat--active',i===j));
    document.querySelector('.stats-section__active-indicator-container')?.style.setProperty('--active-stat-index',i);
  }));
  let slide=0;
  function showSlide(index){
    const slides=[...document.querySelectorAll('.squeezy-carousel__item-details')];
    slide=(index+slides.length)%slides.length;
    slides.forEach((x,i)=>{const active=i===slide;x.setAttribute('aria-hidden',String(!active));x.style.opacity=active?'1':'0';x.style.pointerEvents=active?'auto':'none';x.style.transform=active?'translateX(0)':'translateX(-100%)';x.querySelectorAll('a').forEach(a=>a.tabIndex=active?0:-1)});
  }
  document.querySelector('[aria-label="Next slide"]')?.addEventListener('click',()=>showSlide(slide+1));
  document.querySelector('[aria-label="Previous slide"]')?.addEventListener('click',()=>showSlide(slide-1));

  const bentoBackground=document.querySelector('.modular-solutions-bg');
  const fadeBento=()=>bentoBackground?.style.setProperty('--bg-fade-opacity',Math.min(1,Math.max(0,(scrollY-100)/400)));
  fadeBento();addEventListener('scroll',fadeBento,{passive:true});

})();
