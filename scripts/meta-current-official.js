(() => {
 const header=document.querySelector('.meta-header'),notice=document.getElementById('region-notice');
 const video=document.getElementById('hero-video'),toggle=document.getElementById('video-toggle-btn');
 const drawer=document.getElementById('mobile-navigation'),menu=document.querySelector('.mobile-menu-button'),close=document.querySelector('.drawer-close');
 const small=matchMedia('(max-width:767px)');
 function updateHeader(){header.classList.toggle('scrolled',scrollY>20);}
 addEventListener('scroll',updateHeader,{passive:true});updateHeader();
 document.getElementById('dismiss-region').addEventListener('click',()=>{notice.classList.add('dismissed');header.classList.add('notice-dismissed');});
 function updateVideo(){const paused=video.paused;toggle.setAttribute('aria-label',paused?'Play video':'Pause video');document.getElementById('pause-icon').style.display=paused?'none':'block';document.getElementById('play-icon').style.display=paused?'block':'none';}
 toggle.addEventListener('click',()=>{if(video.paused)video.play().catch(updateVideo);else video.pause();});
 video.addEventListener('play',updateVideo);video.addEventListener('pause',updateVideo);video.addEventListener('ended',updateVideo);
 function updatePoster(){video.poster=small.matches?video.dataset.mobilePoster:video.dataset.desktopPoster;}
 updatePoster();small.addEventListener('change',updatePoster);updateVideo();
 if(matchMedia('(prefers-reduced-motion:reduce)').matches)video.pause();
 function setMenu(open){drawer.hidden=!open;menu.setAttribute('aria-expanded',String(open));document.body.style.overflow=open?'hidden':'';for(const node of [header,notice,document.querySelector('main'),document.querySelector('footer')])node.inert=open;if(open)close.focus();else menu.focus();}
 menu.addEventListener('click',()=>setMenu(true));close.addEventListener('click',()=>setMenu(false));
 document.addEventListener('keydown',event=>{if(drawer.hidden)return;if(event.key==='Escape'){event.preventDefault();setMenu(false);}else if(event.key==='Tab'){const nodes=[...drawer.querySelectorAll('button,a,summary')].filter(e=>e.getClientRects().length);const first=nodes[0],last=nodes.at(-1);if(event.shiftKey&&document.activeElement===first){event.preventDefault();last.focus();}else if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first.focus();}}});
 function updateFooters(){document.querySelectorAll('.official-footer-group').forEach((e,i)=>{e.open=!small.matches||i===0;});if(!small.matches&&!drawer.hidden)setMenu(false);}
 small.addEventListener('change',updateFooters);updateFooters();
 document.querySelectorAll('.official-footer-group summary').forEach(s=>s.addEventListener('click',event=>{if(!small.matches)event.preventDefault();}));
})();
