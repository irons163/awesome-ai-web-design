import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {JSDOM,VirtualConsole} from 'jsdom';
const work='.stitch-work/current-official';
for(const brand of ['mongodb','intercom','superhuman','kraken','coinbase']) {
 const records=[];
 for(const width of [1280,390]) {
  const file=path.join(work,`${brand}-oct10-official-${width}-reference.json`);
  const raw=fs.readFileSync(file,'utf8');
  const backup=file.replace('.json','-unfiltered.json');
  if(!fs.existsSync(backup))fs.writeFileSync(backup,raw);
  const r=JSON.parse(raw),html=r.htmlParts.join('');
  if(crypto.createHash('sha256').update(html).digest('hex')!==r.html_sha256)throw Error('Raw HTML hash changed');
  const doc=new JSDOM(html,{runScripts:'outside-only',virtualConsole:new VirtualConsole()}).window.document;
  const styles=[...doc.querySelectorAll('style')];
  const before=r.inlineStyleRules||[];
  const kept=before.filter(s=>styles[s.index]&&!styles[s.index].textContent.trim());
  if(kept.some(s=>s.cssText?.includes('[Truncated]')))throw Error('Truncated CSSOM is not an acceptable substitute');
  records.push({width,retained:kept.map(s=>({index:s.index,bytes:Buffer.byteLength(s.cssText||'')})),excluded:before.filter(s=>!kept.includes(s)).map(s=>({index:s.index,bytes:Buffer.byteLength(s.cssText||''),truncated:s.cssText?.includes('[Truncated]')||false,reason:'Complete original style text already preserved in htmlParts; keep original rule spelling/cascade.'}))});
  r.inlineStyleRules=kept;r.style_normalization='Use CSSOM only for empty original style text. Complete original style text remains in raw HTML chunks. Truncated CSSOM excluded.';
  fs.writeFileSync(file,JSON.stringify(r,null,2)+'\n');
 }
 fs.writeFileSync(path.join(work,`${brand}-oct10-style-normalization.json`),JSON.stringify(records,null,2)+'\n');
 console.log(brand,records.map(x=>[x.width,x.retained.length]));
}
