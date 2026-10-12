// Restore captured header visibility and freeze the actually observed magazine slides.
import fs from 'node:fs';
const file='.stitch-work/current-official/bmw-m.html';
let html=fs.readFileSync(file,'utf8');
function correction(){
 function install(){
  const header=document.querySelector('.pw-m-header');
  const update=()=>header?.classList.toggle('pw-m-header--hidden',scrollY>100);
  update();document.addEventListener('scroll',update,{passive:true});
  if(innerWidth>=768){
   const heroVideo=document.querySelector('video[id^="pw-a-video-stage"]');
   if(heroVideo){heroVideo.pause();heroVideo.removeAttribute('autoplay');heroVideo.removeAttribute('src');heroVideo.querySelectorAll('source').forEach(e=>e.remove());heroVideo.poster='bmw-m-assets/oct10/observed-hero-video-phase.png';heroVideo.load();heroVideo.dataset.observedStaticPhase='Actual source viewport hero-video crop; animation unverified';}
  }
  const magazine=document.querySelector('[aria-label="MORE FROM BMW M MAGAZINE. "]');
  const track=magazine?.querySelector('.swiper-wrapper');
  if(track){const slides=[...track.children],index=innerWidth<768?2:3;
   track.style.transition='none';track.style.transform=`translate3d(${-slides[index].offsetLeft}px,0,0)`;
   track.dataset.observedStaticPhase=innerWidth<768?'M3 Touring 24H':'Nordschleife / LEGO / Forza';
  }
 }
 install();matchMedia('(max-width:768px)').addEventListener('change',()=>requestAnimationFrame(install));
}
html=html.replace(/<script id="bmw-m-current-corrections">[\s\S]*?<\/script>/g,'');
html=html.replace('</body>','<script id="bmw-m-current-corrections">('+correction.toString()+')();</script></body>');
fs.writeFileSync(file,html);
