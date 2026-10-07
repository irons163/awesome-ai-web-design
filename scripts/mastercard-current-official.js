/* Local interactions for the corrected study. No analytics or account services. */
(() => {
 const $ = (s, root=document) => root.querySelector(s);
 const $$ = (s, root=document) => [...root.querySelectorAll(s)];
 $('#livechatIcon').addEventListener('click',()=>open('https://www.mastercard.com/tw/zh/personal/get-support.html','_blank','noopener'));
 const hero = $('#study-hero');
 const videoShell = hero.closest('.video-js');
 const play = $('.vjs-play-control',videoShell);
 const mute = $('.vjs-mute-control',videoShell);
 const mobile = matchMedia('(max-width:600px)');
 function videoSource(){
  const next='https://www.mastercard.com/content/dam/mccom/shared/homepage/videos/translated-welcome-videos/homepage-video-zh-TW_'+(mobile.matches?'9x16':'16x9')+'_.mp4';
  if(hero.getAttribute('src')!==next){hero.src=next;hero.load();hero.play().catch(()=>{});}
 }
 function videoState(){
  const label=hero.ended?'Replay':hero.paused?'Play':'Pause';
  play.title=label;$('.vjs-control-text',play).textContent=label;
  for(const e of [play,videoShell]){e.classList.toggle('vjs-paused',hero.paused);e.classList.toggle('vjs-ended',hero.ended);e.classList.toggle('vjs-playing',!hero.paused);}
  mute.title=hero.muted?'Unmute':'Mute';$('.vjs-control-text',mute).textContent=mute.title;mute.classList.toggle('vjs-vol-0',hero.muted);
 }
 play.addEventListener('click',()=>{if(hero.ended)hero.currentTime=0;if(hero.paused)hero.play().catch(()=>{});else hero.pause();});
 mute.addEventListener('click',()=>{hero.muted=!hero.muted;videoState();});
 for(const event of ['play','pause','ended','volumechange'])hero.addEventListener(event,videoState);
 mobile.addEventListener('change',videoSource);videoSource();videoState();

 const carousel=$('.carousel');
 const swiper=$('.swiper',carousel),track=$('.swiper-wrapper',swiper),slides=$$('.swiper-slide',swiper),tabs=$$('[role="tab"]',swiper);
 let selected=0,timer=null,startX=null;
 function draw(){
  const gap=mobile.matches?8:16,perView=mobile.matches?1.01:1.001;
  const width=Number(((Math.round(swiper.getBoundingClientRect().width)-(perView-1)*gap)/perView).toFixed(mobile.matches?3:2));
  slides.forEach((e,i)=>{e.style.width=width+'px';e.style.marginRight=gap+'px';e.classList.toggle('swiper-slide-active',i===selected);e.classList.toggle('swiper-slide-next',i===selected+1);e.classList.toggle('swiper-slide-prev',i===selected-1);e.setAttribute('aria-hidden',String(i!==selected));e.inert=i!==selected;});
  track.style.transform='translate3d('+(-selected*(width+gap))+'px,0,0)';
  tabs.forEach((e,i)=>{e.classList.toggle('swiper-pagination-bullet-active',i===selected);e.setAttribute('aria-selected',String(i===selected));e.tabIndex=i===selected?0:-1;});
 }
 function select(i){selected=(i+slides.length)%slides.length;draw();}
 function pause(){clearInterval(timer);timer=null;carousel.classList.add('study-paused');}
 function resume(){pause();carousel.classList.remove('study-paused');timer=setInterval(()=>select(selected+1),2500);}
 $('.swiper-button-prev',swiper).addEventListener('click',()=>{pause();select(selected-1);});
 $('.swiper-button-next',swiper).addEventListener('click',()=>{pause();select(selected+1);});
 $('.swiper-button-pause',swiper).addEventListener('click',pause);$('.swiper-button-play',swiper).addEventListener('click',resume);
 tabs.forEach((e,i)=>{e.addEventListener('click',()=>{pause();select(i);});e.addEventListener('keydown',ev=>{if(['ArrowRight','ArrowLeft','Home','End','Enter',' '].includes(ev.key)){ev.preventDefault();pause();select(ev.key==='Home'?0:ev.key==='End'?2:ev.key==='ArrowRight'?selected+1:ev.key==='ArrowLeft'?selected-1:i);tabs[selected].focus();}});});
 swiper.addEventListener('touchstart',e=>{startX=e.changedTouches[0].clientX;},{passive:true});
 swiper.addEventListener('touchend',e=>{const delta=e.changedTouches[0].clientX-startX;if(Math.abs(delta)>45){pause();select(selected+(delta<0?1:-1));}startX=null;},{passive:true});
 addEventListener('resize',draw);draw();pause();

 const footerButtons=$$('[id^="navMenu-"][id$="-button"]');
 function footerState(){const small=matchMedia('(max-width:940px)').matches;$('#footer-secondary-navigation').prepend($(small?'.study-footer-social':'.study-footer-legal'));const social=$('#footer-social-navigation');social.prepend($(small?'.text':'.countryselector',social));footerButtons.forEach(b=>{const expanded=!small;b.setAttribute('aria-expanded',String(expanded));$('#'+b.getAttribute('aria-controls')).setAttribute('aria-hidden',String(!expanded));});}
 footerButtons.forEach(b=>b.addEventListener('click',()=>{if(matchMedia('(max-width:940px)').matches){const expanded=b.getAttribute('aria-expanded')!=='true';b.setAttribute('aria-expanded',String(expanded));$('#'+b.getAttribute('aria-controls')).setAttribute('aria-hidden',String(!expanded));}}));
 matchMedia('(max-width:940px)').addEventListener('change',footerState);footerState();

 const navigation=$('.navigation-bar'),drawer=$('#mobileMenuToggle'),panel=$('#study-navigation'),search=$('#search-content'),searchToggle=$('#search-toggle');
 const menus={
  '1f2ad0e473':[['查看所有卡別','personal/find-a-card'],['萬事達卡信用卡','personal/find-a-card/credit-card'],['萬事達卡Debit簽帳金融卡','personal/find-a-card/debit-card'],['為您實現熱情','personal/find-a-card/passion-cards'],['卡片權益','personal/find-a-card/card-benefits'],['自選支付方式','personal/ways-to-pay'],['感應式支付','personal/ways-to-pay/contactless'],['一鍵支付（Click to Pay）','personal/ways-to-pay/click-to-pay'],['支付密鑰（Payment Passkeys）','personal/ways-to-pay/payment-passkeys'],['安全與保障','personal/protection-and-security'],['支援與聯絡','personal/get-support'],['尋找最近的 ATM','personal/get-support/atm-near-me'],['使用我們的貨幣轉換器','personal/get-support/currency-exchange-rate-converter'],['盡情享受無價體驗','personal/experience-mastercard/priceless'],['我們的多感官品牌','personal/experience-mastercard/multisensory-branding']],
  'e51b865f32':[['消費者支付','business/payments/consumer-payments'],['商業支付','business/payments/commercial-payments'],['資金流動','business/payments/Mastercard%20Move'],['顧問與轉型','business/insights-intelligence/advisors-transformation'],['網路安全與詐騙預防','business/cybersecurity-fraud-prevention'],['客戶拓展與聯繫','business/consumer-acquisition-and-engagement'],['洞察與智能','business/insights-intelligence'],['AI','business/artificial-intelligence'],['金融機構','business/industry-segment/financial-institutions'],['中小企業','business/industry-segment/small-medium-business'],['大型企業','business/industry-segment/large-corporations'],['政府及公共服務','business/industry-segment/public-sector'],['金融科技','business/industry-segment/fintech'],['健康照顧','business/industry-segment/healthcare']],
  '74968c2f23':[['企業影響','for-the-world/corporate-impact'],['賦能民眾','for-the-world/people'],['邁向繁榮之路','for-the-world/prosperity'],['保護地球','for-the-world/planet'],['社區與歸屬感','for-the-world/people/community-belonging'],['社區影響力','for-the-world/people/community-impact'],['Girls4Tech','for-the-world/people/girls4tech'],['關於我們','for-the-world/about-us'],['隱私和資料責任','for-the-world/about-us/mastercard-privacy-and-data-responsibility']],
  '900a6ee2fb':[['開發人員','innovation/build-with-us/mastercard-developers'],['數位實驗室','innovation/build-with-us/digital-labs'],['Start Path','innovation/partner-with-us/start-path'],['Mastercard Engage','business/industry-segment/fintech/program/engage'],['研究與開發','innovation/explore-with-us/research-development'],['體驗中心','innovation/engage-with-us/mastercard-experience-center']],
  'bba1fd377f':[['全球新聞中心','news-and-trends/stories'],['AI','news-and-trends/featured-topic/artificial-intelligence-featured-topic'],['網路安全','news-and-trends/featured-topic/cybersecurity-featured-topic'],['小型企業','news-and-trends/featured-topic/small-business-featured-topic'],['萬事達卡經濟研究所','news-and-trends/insights-report/mastercard-economic-institute'],['新聞稿','news-and-trends/press'],['管理層簡介','news-and-trends/press/executive-bios'],['媒體聯絡人','news-and-trends/press/media-contacts']]
 };
 function closeNavigation(){navigation.classList.remove('study-drawer');drawer.setAttribute('aria-expanded','false');panel.hidden=true;search.hidden=true;searchToggle.setAttribute('aria-expanded','false');$$('.mobile-menu button').forEach(b=>b.setAttribute('aria-expanded','false'));document.body.style.overflow='';}
 drawer.addEventListener('click',()=>{const open=drawer.getAttribute('aria-expanded')!=='true';closeNavigation();navigation.classList.toggle('study-drawer',open);drawer.setAttribute('aria-expanded',String(open));document.body.style.overflow=open?'hidden':'';});
 $$('.mobile-menu button').forEach(b=>b.addEventListener('click',()=>{const open=b.getAttribute('aria-expanded')!=='true';panel.replaceChildren();$$('.mobile-menu button').forEach(n=>n.setAttribute('aria-expanded','false'));b.setAttribute('aria-expanded',String(open));panel.hidden=!open;search.hidden=true;if(open){const title=document.createElement('h2');title.textContent=b.textContent;const list=document.createElement('ul');for(const [text,path]of menus[b.id.slice(8)]){const li=document.createElement('li'),a=document.createElement('a');a.textContent=text;a.href='https://www.mastercard.com/tw/zh/'+path+'.html';li.append(a);list.append(li);}panel.append(title,list);}}));
 searchToggle.addEventListener('click',()=>{const open=search.hidden;closeNavigation();search.hidden=!open;searchToggle.setAttribute('aria-expanded',String(open));if(open)$('#study-search-input').focus();});
 $('#study-search').addEventListener('submit',e=>{e.preventDefault();const query=$('#study-search-input').value.trim().toLocaleLowerCase();const matches=Object.values(menus).flat().filter(([text])=>query&&text.toLocaleLowerCase().includes(query));const out=$('#study-search-result');out.replaceChildren();for(const [text,path]of matches){const a=document.createElement('a');a.textContent=text;a.href='https://www.mastercard.com/tw/zh/'+path+'.html';out.append(a,document.createElement('br'));}if(!matches.length){const a=document.createElement('a');a.textContent='前往 Mastercard';a.href='https://www.mastercard.com/tw/zh.html';out.append(a);}});
 addEventListener('keydown',e=>{if(e.key==='Escape'){const trigger=search.hidden?drawer:searchToggle;closeNavigation();trigger.focus();}});

 const cookieNotice=$('#study-cookies'),cookieSettings=$('#study-cookie-settings');
 let functional=false;
 try{functional=localStorage.getItem('mastercard-study-functional')==='yes';if(!localStorage.getItem('mastercard-study-consent'))cookieNotice.showModal();}catch{cookieNotice.showModal();}
 function consent(value){functional=value;try{localStorage.setItem('mastercard-study-consent','set');localStorage.setItem('mastercard-study-functional',value?'yes':'no');}catch{}cookieNotice.close();cookieSettings.close();}
 function settings(){cookieNotice.close();$('#study-functional').checked=functional;cookieSettings.showModal();}
 $$('[data-cookie]').forEach(b=>b.addEventListener('click',()=>b.dataset.cookie==='manage'?settings():consent(b.dataset.cookie==='accept')));
 $$('.optanon-show-settings').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();settings();}));
 $('#study-save-cookies').addEventListener('click',()=>consent($('#study-functional').checked));
 const countryInput=$('#countrySelectorDropdownCustomInput'),countryMenu=$('#study-country-overflow'),countryOptions=$$('[role="option"]',countryMenu);
 function countryState(open){countryInput.setAttribute('aria-expanded',String(open));countryMenu.classList.toggle('overflow-menu--open',open);countryMenu.classList.toggle('overflow-menu--closed',!open);}
 countryInput.addEventListener('click',()=>countryState(countryInput.getAttribute('aria-expanded')!=='true'));
 countryInput.addEventListener('keydown',e=>{if(['Enter',' ','ArrowDown'].includes(e.key)){e.preventDefault();countryState(true);$('a',countryOptions[0]).focus();}});
 countryOptions.forEach((option,i)=>option.addEventListener('keydown',e=>{if(['ArrowDown','ArrowUp','Home','End'].includes(e.key)){e.preventDefault();const next=e.key==='Home'?0:e.key==='End'?countryOptions.length-1:(i+(e.key==='ArrowDown'?1:-1)+countryOptions.length)%countryOptions.length;$('a',countryOptions[next]).focus();}}));
 addEventListener('click',e=>{if(!e.target.closest('#countrySelectorContainter'))countryState(false);});
 addEventListener('keydown',e=>{if(e.key==='Escape'&&countryInput.getAttribute('aria-expanded')==='true'){countryState(false);countryInput.focus();}});
 $('.youtube-player .vjs-big-play-button').addEventListener('click',()=>{const player=$('.youtube-player');if(!functional){player.classList.add('study-cookie-needed');if(!$('.video-splash-screen',player)){const overlay=document.createElement('div');overlay.className='video-splash-screen';const text=document.createElement('p');text.textContent='Please accept functional cookies to watch this video.';const configure=document.createElement('button');configure.className='made-c-button made-c-button--secondary';configure.textContent='Configure my cookies';configure.addEventListener('click',settings);overlay.append(text,configure);player.append(overlay);}return;}const frame=document.createElement('iframe');frame.src='https://www.youtube.com/embed/eLr4zq0VRoY?autoplay=1';frame.title='Mastercard priceless video';frame.allow='autoplay; encrypted-media; picture-in-picture';frame.allowFullscreen=true;player.replaceChildren(frame);});
})();
