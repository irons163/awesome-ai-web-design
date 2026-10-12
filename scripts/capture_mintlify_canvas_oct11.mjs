// CUA-only read of the rendered public page's own existing canvases.
import fs from 'node:fs/promises';
import crypto from 'node:crypto';
const work='/Users/pchang01/Documents/mygithub/awesome-ai-web-design/.stitch-work/current-official';
export async function canvasFrame(tab,cdp,width,height){
 const meta=await tab.playwright.evaluate(()=>({url:location.href,width:innerWidth,height:innerHeight,scrollY,observed_at:new Date().toISOString(),canvases:[...document.querySelectorAll('canvas')].map((e,index)=>{const b=e.getBoundingClientRect();let path=[],n=e;while(n&&n!==document.documentElement){const p=n.parentElement;if(!p)break;path.unshift(n.tagName.toLowerCase()+':nth-child('+([...p.children].indexOf(n)+1)+')');n=p;}return{index,selector:'html>'+path.join('>'),width:e.width,height:e.height,box:b.toJSON(),visible:b.width>0&&b.height>0&&b.bottom>0&&b.top<innerHeight&&b.right>0&&b.left<innerWidth}}).filter(e=>e.visible)}));
 if(meta.url!=='https://www.mintlify.com/'||meta.width!==width||meta.height!==height)throw Error('Unexpected current source');
 const name=`mintlify-oct11-canvas-${width}-y-${Math.round(meta.scrollY)}.jpg`;
 await fs.writeFile(work+'/'+name,Buffer.from(await tab.screenshot({fullPage:false})));
 const file=work+`/mintlify-oct11-observed-canvases-${width}.json`;
 let records=[];try{records=JSON.parse(await fs.readFile(file,'utf8'))}catch{}
 for(const c of meta.canvases){
  if(records.some(r=>r.index===c.index&&r.path))continue;
  let data;try{const result=await cdp.send('Runtime.evaluate',{expression:`document.querySelectorAll('canvas')[${c.index}].toDataURL('image/png')`,returnByValue:true});data=result.result?.value;if(!data?.startsWith('data:image/png'))throw Error(result.exceptionDetails?.text||'No current canvas pixels returned');}catch(e){records.push({...c,url:meta.url,observed_at:meta.observed_at,scrollY:meta.scrollY,screenshot:name,error:String(e)});continue}
  const bytes=Buffer.from(data.split(',')[1],'base64');
  const path=`mintlify-assets/oct10/observed-canvas-${width}-${c.index}.png`;
  await fs.writeFile(work+'/'+path,bytes);
  const previous_attempts=records.filter(r=>r.index===c.index&&r.error);records=records.filter(r=>r.index!==c.index||r.path);
  records.push({...c,url:meta.url,observed_at:meta.observed_at,scrollY:meta.scrollY,screenshot:name,path,bytes:bytes.length,sha256:crypto.createHash('sha256').update(bytes).digest('hex'),method:'Read-only CDP Runtime.evaluate toDataURL of the existing rendered public DOM canvas; static phase only, no motion parity claim.',previous_attempts});
 }
 await fs.writeFile(file,JSON.stringify(records,null,2)+'\n');
 return {width,scrollY:meta.scrollY,captured:records.filter(r=>r.path).length,errors:records.filter(r=>r.error).length};
}
