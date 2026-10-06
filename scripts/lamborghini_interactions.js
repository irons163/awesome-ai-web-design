/* Local controls for a dated, unofficial visual study. Official services remain external. */
const $ = (selector, root=document) => root.querySelector(selector);
const $$ = (selector, root=document) => [...root.querySelectorAll(selector)];
const origin = 'https://www.lamborghini.com';
const absolute = path => path.startsWith('/') ? origin + path : path;
const escapeText = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const header = $('header');
const menu = $('#burger-menu');
const burger = $('button.burger', header);
const menuStack = [];
const menuTemplate = document.createElement('template');
menuTemplate.innerHTML = sourceReference.initialMenu;
const initialMenu = menuTemplate.content.firstElementChild.innerHTML;

function toggleMenu(open) {
  menu.classList.toggle('open',open);
  menu.setAttribute('aria-hidden',String(!open));
  header.classList.toggle('menu-open',open);
  burger.setAttribute('aria-expanded',String(open));
  burger.setAttribute('aria-label',open?'Close menu':'Open menu');
  $('path',burger).setAttribute('d',open?'M19.354 5.354L18.647 4.646L12 11.293L5.354 4.647L4.646 5.354L11.293 12L4.647 18.646L5.354 19.353L12 12.707L18.646 19.353L19.353 18.646L12.707 12L19.354 5.354Z':'M22 6H2V5H22V6ZM22 18H2V19H22V18ZM22 11.5H2V12.5H22V11.5Z');
  if(open) {
    document.body.style.overflow='hidden';
    $$('a,button',menu).forEach(e=>e.tabIndex=0);
    const first=$$('.burger-menu-link',menu).find(e=>e.getBoundingClientRect().height);
    first?.focus();
  } else {
    document.body.style.overflow='';
    menuStack.length=0;
    $('#burger-content').innerHTML=initialMenu;
    burger.focus();
  }
}
burger.addEventListener('click',()=>toggleMenu(!menu.classList.contains('open')));
menu.setAttribute('aria-hidden','true');
burger.setAttribute('aria-expanded','false');

function menuEntry(item,index) {
  const content='<span>'+escapeText(item.title)+'</span>';
  return '<li class="burger-menu-item">'+(item.children?.length?
    '<button class="burger-menu-link lev-3-toggler" data-child="'+index+'">'+content+'</button>':
    '<a class="burger-menu-link" data-preview="'+index+'" href="'+escapeText(absolute(item.url))+'">'+content+'</a>')+'</li>';
}
function previewMenu(item) {
  const destination=$('.menu-study-preview',menu);
  if(!destination)return;
  const data=item.extended_data;
  const art=data?.images?.[0]?.desktop;
  destination.innerHTML=art?'<img alt="'+escapeText(item.title)+'" src="'+escapeText(absolute(art.url))+'">':'';
  for(const action of data?.callToActions??[]) {
    const label=action.labels?.find(x=>x.key==='title_primary')?.value?.[0];
    if(label&&action.url?.url)destination.innerHTML+='<p><a href="'+escapeText(absolute(action.url.url))+'">'+escapeText(label)+'</a></p>';
  }
}
function renderMenu() {
  const content=$('#burger-content');
  content.innerHTML=initialMenu;
  if(!menuStack.length)return;
  $$('.menu-block',content).forEach(e=>e.classList.remove('active'));
  const current=menuStack.at(-1);
  const block=document.createElement('div');
  block.className='menu-block lev-2 active';
  block.innerHTML='<div class="container"><div class="row"><div class="burger-nav burger-nav-back order-1 col-12 col-lg-6"><button class="back-btn" aria-label="Go back"><svg width="24" height="24" viewBox="0 0 24 24"><path d="M15.646 22.354L5.293 12L15.647 1.646L16.353 2.353L6.707 12L16.353 21.646Z" fill="currentColor"/></svg><span>'+escapeText(current.title)+'</span></button></div><div class="burger-nav burger-nav-overview order-3 order-lg-2 col-12 col-lg-6"><a class="overview btn-secondary btn-medium has-icon css-v977j5" href="'+escapeText(absolute(current.url))+'"><span>overview</span></a></div><div class="burger-menu order-2 order-lg-3 col-12 col-lg-4"><div class="primary primary--lev2 css-9mkdug"><ul>'+current.children.map(menuEntry).join('')+'</ul></div></div><div class="d-none d-md-block order-4 col-12 col-lg-8 menu-study-preview"></div></div></div>';
  content.append(block);
  $('.overview',block).insertAdjacentHTML('beforeend','<svg aria-hidden="true" class="icon light" width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M16.4133 6L15.5553 6.92298L19.6739 11.3473H2V12.6527H19.6739L15.5541 17.077L16.4145 18L22 12L16.4145 6H16.4133Z" fill="currentColor"/></svg>');
  content.scrollTop=0;
  $('.back-btn',block).focus();
}
menu.addEventListener('click',event=>{
  const target=event.target.closest('button');
  if(!target)return;
  if(target.classList.contains('back-btn')){menuStack.pop();renderMenu();return;}
  if(target.hasAttribute('data-child')){menuStack.push(menuStack.at(-1).children[Number(target.dataset.child)]);renderMenu();return;}
  if(target.classList.contains('burger-menu-link')){
    const item=sourceReference.menus.find(x=>x.title.toLowerCase()===target.textContent.trim().toLowerCase());
    if(item?.children?.length){menuStack.push(item);renderMenu();}
  }
});
menu.addEventListener('pointerover',event=>{
  const item=event.target.closest('[data-preview]');
  if(item&&menuStack.length)previewMenu(menuStack.at(-1).children[Number(item.dataset.preview)]);
});
document.addEventListener('keydown',event=>{
  if(event.key==='Escape'&&menu.classList.contains('open')){toggleMenu(false);return;}
  if(event.key==='Tab'&&menu.classList.contains('open')){
    const focusable=[burger,...$$('a,button,[tabindex="0"]',menu).filter(e=>e.getBoundingClientRect().height&&!e.disabled)];
    if(event.shiftKey&&document.activeElement===focusable[0]){event.preventDefault();focusable.at(-1)?.focus();}
    else if(!event.shiftKey&&document.activeElement===focusable.at(-1)){event.preventDefault();focusable[0]?.focus();}
  }
});
addEventListener('scroll',()=>header.classList.toggle('full-bg',scrollY>20),{passive:true});

function selectTab(list,index) {
  const tabs=$$('[role="tab"]',list);
  const group=list.closest('.react-tabs');
  const panels=$$(':scope > [role="tabpanel"]',group);
  tabs.forEach((tab,i)=>{
    tab.classList.toggle('react-tabs__tab--selected',i===index);
    tab.setAttribute('aria-selected',String(i===index));
    tab.tabIndex=i===index?0:-1;
  });
  panels.forEach((panel,i)=>{
    panel.classList.toggle('react-tabs__tab-panel--selected',i===index);
    panel.setAttribute('aria-hidden',String(i!==index));
  });
  const slide=list.closest('#families-gallery .swiper-slide');
  if(slide){
    const family=$$('#families-gallery .swiper-slide').indexOf(slide);
    const model=sourceReference.families[family][index];
    $('.carousel-item__image img',slide).src=model.image;
  }
}
$$('[role="tablist"]').forEach(list=>{
  list.addEventListener('click',event=>{const tab=event.target.closest('[role="tab"]');if(tab)selectTab(list,$$('[role="tab"]',list).indexOf(tab));});
  list.addEventListener('keydown',event=>{
    if(!['ArrowLeft','ArrowRight','Home','End'].includes(event.key))return;
    event.preventDefault();const tabs=$$('[role="tab"]',list),current=tabs.indexOf(document.activeElement);
    const index=event.key==='Home'?0:event.key==='End'?tabs.length-1:(current+(event.key==='ArrowRight'?1:-1)+tabs.length)%tabs.length;
    selectTab(list,index);tabs[index].focus();
  });
});
let familyIndex=0;
const familySlides=$$('#families-gallery .swiper-slide');
function selectFamily(index) {
  familyIndex=Math.max(0,Math.min(familySlides.length-1,index));
  const width=$('#families-gallery .swiper').clientWidth;
  familySlides.forEach((slide,i)=>{slide.style.width=width+'px';slide.classList.toggle('swiper-slide-active',i===familyIndex);});
  $('#families-gallery .swiper-wrapper').style.transform='translateX('+(-familyIndex*width)+'px)';
  $('#families-gallery .swiper-wrapper').style.height=familySlides[familyIndex].offsetHeight+'px';
  const previous=$('#families-gallery .lam-carousel__control--prev'),next=$('#families-gallery .lam-carousel__control--next');
  previous.disabled=familyIndex===0;next.disabled=familyIndex===familySlides.length-1;
  previous.classList.toggle('disabled',previous.disabled);next.classList.toggle('disabled',next.disabled);
  $$('.study-pagination [data-slide]').forEach((e,i)=>{e.setAttribute('aria-current',String(i===familyIndex));e.classList.toggle('swiper-pagination-bullet-active',i===familyIndex);});
  $('#families-gallery .consumption-emissions-section span').innerHTML=sourceReference.families[familyIndex][0].disclaimer;
}
$('#families-gallery .lam-carousel__control--prev')?.addEventListener('click',()=>selectFamily(familyIndex-1));
$('#families-gallery .lam-carousel__control--next')?.addEventListener('click',()=>selectFamily(familyIndex+1));
$$('.study-pagination [data-slide]').forEach(button=>{
  button.addEventListener('click',()=>selectFamily(Number(button.dataset.slide)));
  button.addEventListener('keydown',event=>{if(event.key==='Enter'||event.key===' '){event.preventDefault();selectFamily(Number(button.dataset.slide));}});
});
selectFamily(0);document.fonts.ready.then(()=>selectFamily(familyIndex));
function responsiveControls(){
  const desktop=innerWidth>=992;
  $$('#hero-banner .slide-cta,#families-gallery .carousel-item__children a,#families-gallery .carousel-item__children button,#banner .lam-banner__actions a,#model-chooser .model__actions a,#model-chooser .model__actions button').forEach(cta=>{
    cta.classList.toggle('btn-large',desktop);cta.classList.toggle('btn-medium',!desktop);
  });
  updateChooserScroll();
  selectFamily(familyIndex);
}
const chooserWrapper=$('#model-chooser .react-tabs__tab-list-wrapper');
const chooserList=$('[role="tablist"]',chooserWrapper);
function updateChooserScroll(){
  const scrollable=chooserList.scrollWidth>chooserWrapper.clientWidth+1;
  chooserWrapper.classList.toggle('is-scrollable',scrollable);
  $('.css-1scxgtc',chooserWrapper).style.display=scrollable?'':'none';
  $('.left-arrow',chooserWrapper).classList.toggle('invisible',chooserList.scrollLeft<1);
  $('.right-arrow',chooserWrapper).classList.toggle('invisible',chooserList.scrollLeft+chooserList.clientWidth>=chooserList.scrollWidth-1);
}
$('.left-arrow',chooserWrapper).addEventListener('click',()=>chooserList.scrollBy({left:-chooserList.clientWidth*.7,behavior:'smooth'}));
$('.right-arrow',chooserWrapper).addEventListener('click',()=>chooserList.scrollBy({left:chooserList.clientWidth*.7,behavior:'smooth'}));
chooserList.addEventListener('scroll',updateChooserScroll,{passive:true});
document.fonts.ready.then(updateChooserScroll);
responsiveControls();addEventListener('resize',responsiveControls);

$$('button[data-target^="form-"]').forEach(button=>button.addEventListener('click',()=>{
  location.href=sourceReference.services[button.dataset.target] ?? origin+'/en-en/contact-us';
}));
const film=$('#hero-film');
film.muted=true;
const phone=matchMedia('(max-width:991.98px)');
function loadFilm() {
  const url=phone.matches?sourceReference.mobileVideo:sourceReference.desktopVideo;
  film.poster=phone.matches?'https://medialamborghini-meride-tv.akamaized.net/meride/lamborghini/video/images/folder1/2847/1786627187hero_mobile.jpg':'https://medialamborghini-meride-tv.akamaized.net/meride/lamborghini/video/images/folder1/2846/1786627119hero.jpg';
  if(window.Hls?.isSupported()){
    const player=new Hls({maxBufferLength:12,maxMaxBufferLength:24});
    player.loadSource(url);player.attachMedia(film);
    player.on(Hls.Events.MANIFEST_PARSED,()=>{if(!matchMedia('(prefers-reduced-motion:reduce)').matches)film.play().catch(()=>{});});
  }else{film.src=url;if(!matchMedia('(prefers-reduced-motion:reduce)').matches)film.play().catch(()=>{});}
}
loadFilm();
new IntersectionObserver(entries=>{
  if(entries[0].isIntersecting&&!matchMedia('(prefers-reduced-motion:reduce)').matches)film.play().catch(()=>{});
  else film.pause();
},{threshold:0.15}).observe(film);
if(matchMedia('(prefers-reduced-motion:reduce)').matches)film.pause();
