// CUA-only capture of actual visible public DOM and its enclosing section.
import fs from 'node:fs/promises';
import crypto from 'node:crypto';
const work='/Users/pchang01/Documents/mygithub/awesome-ai-web-design/.stitch-work/current-official';
export async function activeSection(tab,slug,label,text,levels,width,height){
 const record=await tab.playwright.evaluate(({text,levels})=>{let h=[...document.querySelectorAll('h1,h2,h3')].find(e=>e.textContent.includes(text));if(!h)throw Error('Observed heading unavailable');let e=h;for(let i=0;i<levels;i++)e=e.parentElement;let path=[],n=e;while(n&&n!==document.documentElement){let p=n.parentElement;path.unshift(n.tagName.toLowerCase()+':nth-child('+([...p.children].indexOf(n)+1)+')');n=p;}let html=e.outerHTML;let whole=document.documentElement.outerHTML;return{url:location.href,observed_at:new Date().toISOString(),viewport:{width:innerWidth,height:innerHeight},scrollY,bodyHeight:document.documentElement.scrollHeight,selector:'html>'+path.join('>'),box:e.getBoundingClientRect().toJSON(),htmlParts:Array.from({length:Math.ceil(html.length/60000)},(_,i)=>html.slice(i*60000,(i+1)*60000)),html_length:html.length,documentHtmlParts:Array.from({length:Math.ceil(whole.length/60000)},(_,i)=>whole.slice(i*60000,(i+1)*60000)),images:[...e.querySelectorAll('img')].map(i=>({src:i.currentSrc||i.src,alt:i.alt,naturalWidth:i.naturalWidth,complete:i.complete})),text:e.innerText}}, {text,levels});
 if(record.viewport.width!==width||record.viewport.height!==height)throw Error('Incorrect viewport');
 record.html_sha256=crypto.createHash('sha256').update(record.htmlParts.join('')).digest('hex');
 record.screenshot=`${slug}-oct11-${label}-${width}.jpg`;
 await fs.writeFile(work+'/'+record.screenshot,Buffer.from(await tab.screenshot({fullPage:false})));
 await fs.writeFile(work+`/${slug}-oct11-${label}-${width}-reference.json`,JSON.stringify(record,null,2)+'\n');
 return{label,width,scrollY:record.scrollY,bodyHeight:record.bodyHeight,htmlLength:record.html_length,images:record.images.length};
}
