// Dated static canvas phase and observed header behavior for Composio's public study.
import fs from 'node:fs';
const file='.stitch-work/current-official/composio.html';
let html=fs.readFileSync(file,'utf8');
function correction(){
  function mount(){
    const header=document.querySelector('header');
    if(!header)return;
    const topClass="fixed top-0 left-0 z-50 flex w-full flex-col items-center overflow-visible border-b p-2 transition-[background-color,border-color,color,translate] duration-300 md:top-4 md:left-1/2 md:w-[calc(100%-2rem)] md:max-w-page md:-translate-x-1/2 md:border md:px-2 md:py-[8px]";
    function update(){
      const announcement=document.querySelector('[aria-label="Announcement"]');
      const offset=Math.max(0,(announcement?.getBoundingClientRect().bottom||0));
      const point=document.elementsFromPoint(innerWidth/2,120).find(e=>e.closest('main')&&!e.closest('header'));
      const section=point?.closest('section');
      const dark=section?.classList.contains('dark')??true;
      header.className=topClass+(scrollY<10?' border-transparent bg-transparent dark text-white':dark?' dark text-white':' text-black');
      header.style.transform='translateY('+offset+'px)';
      header.style.backgroundColor=scrollY<10?'transparent':dark?'#0f0f0f':'#f6f6f6';
      header.style.borderColor=scrollY<10?'transparent':dark?'#333':'#ddd';
      header.style.color=dark?'#fff':'#0f0f0f';
      header.querySelectorAll('.text-white').forEach(e=>{e.style.color=dark?'#fff':'#0f0f0f';});
      const logos=[...header.querySelectorAll('a[aria-label="Composio home"] img')];
      logos.forEach((e,i)=>{e.classList.toggle('hidden',i!==(dark?0:1));e.classList.toggle('block',i===(dark?0:1));e.style.display=i===(dark?0:1)?'block':'none';});
    }
    if(innerWidth>=768){
      const canvas=document.querySelector('canvas');
      if(canvas){
        const phase=document.createElement('div');phase.className='observed-webgl-static-phase';
        phase.style.cssText='position:absolute;inset:0;pointer-events:none;background-image:url("composio-assets/oct10/observed-hero-left.png"),url("composio-assets/oct10/observed-hero-right.png");background-position:left 84px,right 84px;background-size:245px 762px;background-repeat:no-repeat;';
        canvas.parentElement.style.position='relative';canvas.parentElement.append(phase);
      }
    }
    update();window.addEventListener('scroll',update,{passive:true});
  }
  mount();matchMedia('(max-width:767px)').addEventListener('change',()=>requestAnimationFrame(mount));
}
html=html.replace('</body>','<script id="composio-current-corrections">('+correction.toString()+')();</script></body>');
fs.writeFileSync(file,html);
console.log('Composio observed static WebGL phase and header correction installed');
