import fs from 'node:fs';
import {execFileSync} from 'node:child_process';
let s=fs.readFileSync('scripts/build_captured_homepage.mjs','utf8');
s=s.replace('const styles = new Set();',`config.menu = read('replicate-oct10-official-mobile-menu.json').header;
const styles = new Set();`);
s=s.replace('current = width;','current = width; document.dispatchEvent(new Event("replicate-study-ready"));');
s=s.replace("document.querySelectorAll('picture source').forEach(e => e.remove());", `document.querySelectorAll('picture source').forEach(e => e.remove());
  const media = new Map();
  for (const capture of read('replicate-oct10-visible-media.json')) for (const item of capture.items) {
    const score = item.images.filter(i=>i.naturalWidth>0).length + item.videos.filter(v=>v.src).length;
    if (!media.has(item.href) || media.get(item.href).score < score) media.set(item.href,{...item,score});
  }
  for(const anchor of document.querySelectorAll('a[href]')) {
    const item=media.get(new URL(anchor.getAttribute('href'),officialURL).href), slot=anchor.querySelector('div.absolute.inset-0');
    if(item&&slot)slot.innerHTML=item.slotHTML;
  }
  const drone=read('replicate-oct10-drone-media.json').find(x=>x.visible);
  for(const span of document.querySelectorAll('span'))if(span.textContent==='drone-art') {
    const card=span.closest('div.p-4')?.parentElement?.parentElement;
    const slot=card?.querySelector('div.absolute.inset-0');if(slot&&drone)slot.innerHTML=drone.outer;
  }
  document.querySelectorAll('img').forEach(e=>{e.src=local(e.getAttribute('src'));e.loading='eager';e.removeAttribute('srcset');e.removeAttribute('sizes');});`);
s=s.replace('</head><body>', '<style>[data-paper-shader]:not(style){background-image:radial-gradient(circle,rgba(0,0,0,.9) .65px,transparent .9px);background-size:3px 3px;}[data-paper-shader] canvas{display:none!important}.goo-canvas{background-size:cover;background-position:center}</style></head><body>');
s=s.replace('</script></body></html>', '</script><script src="replicate-oct10-interactions.js" defer></script></body></html>');
fs.writeFileSync('scripts/replicate-oct10-captured-builder.mjs',s);
execFileSync(process.execPath,['scripts/replicate-oct10-captured-builder.mjs','replicate','https://replicate.com/'],{stdio:'inherit'});
