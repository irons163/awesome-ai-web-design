import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';
import {setTimeout as delay} from 'node:timers/promises';
import test from 'node:test';
import {JSDOM} from 'jsdom';

const read = file => readFileSync(new URL('../'+file,import.meta.url),'utf8');
const html=read('index.html'),app=read('assets/app.js'),catalog=JSON.parse(read('assets/catalog.json')),usage=JSON.parse(read('data/usage.json'));
const published=existsSync(new URL('../dist/client/official-progress.html',import.meta.url))?'dist/client/':'dist/';
const key='awesome-ai-web-design:favorites:v1';
async function until(predicate){for(let i=0;i<40;i++){if(predicate())return;await delay(5);}assert.fail('Catalog did not reach expected state');}
async function fixture(t,{hash='',favorites='[]',catalogFailure=false,progressFailure=false,blockedStorage=false,clipboardFailure=false,fallbackCopy=false,documentResponse,catalogData=catalog}={}){
 const dom=new JSDOM(html,{url:'https://catalog.test/'+hash,runScripts:'outside-only'});
 t.after(async()=>{await delay(0);dom.window.close();});
 const w=dom.window,q=s=>w.document.querySelector(s);let fail=catalogFailure;
 w.HTMLDialogElement.prototype.showModal=function(){this.setAttribute('open','');};
 w.HTMLDialogElement.prototype.close=function(){this.removeAttribute('open');};
 w.localStorage.setItem(key,favorites);
 if(blockedStorage)w.Storage.prototype.setItem=function(){throw new Error('Storage unavailable');};
 const copied=[];
 Object.defineProperty(w.navigator,'clipboard',{value:fallbackCopy?undefined:{writeText:async text=>{if(clipboardFailure)throw new Error('Denied');copied.push(text);}}});
 w.document.execCommand=()=>false;
 w.fetch=async file=>{
  if(file==='assets/catalog.json')return {ok:!fail,json:async()=>structuredClone(catalogData)};
  if(file==='official-progress.html')return {ok:!progressFailure,text:async()=>read(published+'official-progress.html')};
  if(file.startsWith('official-drafts/'))return documentResponse?documentResponse(file):{ok:true,text:async()=>read(published+file)};
  throw new Error('Unexpected file '+file);
 };
 w.eval(app);
 await until(()=>catalogFailure?!q('#load-error').hidden:q('#catalog').children.length===catalogData.designs.length);
 return {w,q,copied,recover(){fail=false;},slugs(){return [...w.document.querySelectorAll('[data-design]')].map(n=>n.dataset.design);},input(value){q('#search').value=value;q('#search').dispatchEvent(new w.Event('input',{bubbles:true}));}};
}

test('visible collection counts follow the catalog instead of a fixed total',async t=>{
 const subset={...catalog,count:1,designs:[catalog.designs[0]]};
 const ui=await fixture(t,{catalogData:subset});
 const counters=[...ui.w.document.querySelectorAll('[data-design-count]')];
 assert.ok(counters.length>=5);
 assert.ok(counters.every(element=>element.textContent==='1'));
 assert.equal(ui.q('#stitch-count').textContent,'1 套免費設計參考');
 assert.equal(ui.q('#result-count').textContent,'1 套設計');
});

test('search, category and mode filters combine and clearing an empty result resets them all',async t=>{
 const ui=await fixture(t);ui.input('  STRIPE  ');assert.deepEqual(ui.slugs(),['stripe']);
 ui.input('支付');assert.ok(ui.slugs().includes('stripe'));
 ui.q('#search').value='';ui.q('[data-category="Fintech & Crypto"]').click();
 ui.q('#mode').value='dark';ui.q('#mode').dispatchEvent(new ui.w.Event('change'));
 const expected=catalog.designs.filter(d=>d.category==='Fintech & Crypto'&&d.mode==='dark').map(d=>d.slug).sort();
 assert.deepEqual(ui.slugs().sort(),expected);assert.ok(expected.includes('binance'));
 ui.input('不存在的設計xyz');assert.equal(ui.q('#empty').hidden,false);
 ui.q('#clear-filters').click();assert.equal(ui.slugs().length,catalog.designs.length);assert.equal(ui.q('#mode').value,'all');assert.equal(ui.q('#search').value,'');
 assert.equal(ui.q('[data-category="all"]').getAttribute('aria-pressed'),'true');
});

test('favorites persist, filter correctly, synchronize tabs and return focus when a favorite is removed',async t=>{
 const ui=await fixture(t,{favorites:JSON.stringify(['stripe','obsolete',3])});
 assert.equal(ui.q('#saved-count').textContent,'1');ui.q('[data-save="linear.app"]').click();
 assert.deepEqual(JSON.parse(ui.w.localStorage.getItem(key)).sort(),['linear.app','stripe']);
 ui.q('#favorites-filter').click();assert.deepEqual(ui.slugs().sort(),['linear.app','stripe']);
 ui.q('[data-save="stripe"]').click();assert.deepEqual(ui.slugs(),['linear.app']);assert.equal(ui.w.document.activeElement.id,'favorites-filter');
 ui.w.dispatchEvent(new ui.w.StorageEvent('storage',{key,newValue:'["starbucks"]'}));assert.deepEqual(ui.slugs(),['starbucks']);
 ui.w.dispatchEvent(new ui.w.StorageEvent('storage',{key:null,newValue:null}));assert.equal(ui.slugs().length,0);assert.equal(ui.q('#empty').hidden,false);
});

test('blocked storage keeps this-session favorites usable and clearly reports that they were not saved',async t=>{
 const ui=await fixture(t,{favorites:'invalid JSON',blockedStorage:true});ui.q('[data-save="stripe"]').click();
 assert.equal(ui.q('#saved-count').textContent,'1');assert.match(ui.q('#toast').textContent,/無法保存/);ui.q('#favorites-filter').click();assert.deepEqual(ui.slugs(),['stripe']);
});

test('catalog fetch failure offers a working retry without a false empty-results state',async t=>{
 const ui=await fixture(t,{catalogFailure:true});assert.equal(ui.q('#empty').hidden,true);ui.recover();ui.q('#retry').click();
 await until(()=>ui.q('#catalog').children.length===catalog.designs.length);assert.equal(ui.q('#load-error').hidden,true);
});

test('keyboard search, tabs, Escape close and return focus follow the visible controls',async t=>{
 const ui=await fixture(t);ui.w.document.dispatchEvent(new ui.w.KeyboardEvent('keydown',{key:'/'}));assert.equal(ui.w.document.activeElement.id,'search');
 const trigger=ui.q('a[aria-label="查看 Stripe 設計"]');trigger.focus();ui.w.location.hash='#/design/stripe';
 await until(()=>ui.q('#design-dialog').open);assert.equal(ui.w.document.activeElement.id,'close-dialog');
 ui.q('#tab-preview').dispatchEvent(new ui.w.KeyboardEvent('keydown',{key:'End',bubbles:true,cancelable:true}));
 assert.equal(ui.q('#tab-document').getAttribute('aria-selected'),'true');assert.equal(ui.w.document.activeElement.id,'tab-document');
 ui.q('#tab-document').dispatchEvent(new ui.w.KeyboardEvent('keydown',{key:'ArrowLeft',bubbles:true,cancelable:true}));assert.equal(ui.w.document.activeElement.id,'tab-prompts');
 ui.q('#tab-prompts').dispatchEvent(new ui.w.KeyboardEvent('keydown',{key:'Home',bubbles:true,cancelable:true}));assert.equal(ui.w.document.activeElement.id,'tab-preview');
 ui.q('#tab-preview').dispatchEvent(new ui.w.KeyboardEvent('keydown',{key:'ArrowRight',bubbles:true,cancelable:true}));assert.equal(ui.w.document.activeElement.id,'tab-prompts');
 ui.q('#design-dialog').dispatchEvent(new ui.w.Event('cancel',{cancelable:true}));assert.equal(ui.q('#design-dialog').open,false);assert.equal(ui.w.document.activeElement,trigger);assert.equal(ui.w.location.hash,'#collection');
});

for(const hash of ['#/design/unknown-design','#/design/%E0%A4%A']){
 test('invalid shared link recovers to the collection: '+hash,async t=>{
  const ui=await fixture(t,{hash});assert.equal(ui.q('#design-dialog').open,false);assert.equal(ui.w.location.hash,'#collection');assert.match(ui.q('#toast').textContent,/找不到|格式有誤/);assert.equal(ui.slugs().length,catalog.designs.length);
 });
}

for(const fallbackCopy of [false,true]){
 test('clipboard '+(fallbackCopy?'fallback failure':'permission denial')+' does not report false success or leave an invisible input',async t=>{
  const ui=await fixture(t,{hash:'#/design/stripe',clipboardFailure:true,fallbackCopy});
  await until(()=>ui.q('#download-design').hasAttribute('href'));ui.q('#tab-document').click();await until(()=>!ui.q('#copy-document').disabled);
  ui.q('#copy-document').click();await until(()=>ui.q('#toast').textContent.includes('剪貼簿'));
  assert.doesNotMatch(ui.q('#toast').textContent,/已複製/);assert.equal(ui.copied.length,0);assert.equal(ui.w.document.querySelectorAll('textarea').length,0);
 });
}

test('all entries support preview, current specs, copy and implementation-pack links through the actual app',async t=>{
 const ui=await fixture(t);await until(()=>ui.q('.official-drafts-count').textContent.includes(String(catalog.designs.length)));
 for(const item of catalog.designs){
  ui.w.location.hash='#/design/'+encodeURIComponent(item.slug);await until(()=>ui.q('#detail-title').textContent===item.name);
  assert.equal(ui.q('#current-preview-image').hidden,false,item.slug);assert.match(ui.q('#open-preview').getAttribute('href'),/official-drafts\/.+\.html$/);
  ui.q('#tab-document').click();await until(()=>!ui.q('#copy-document').disabled);const design=ui.q('#document-text').textContent;
  assert.ok(design.includes('## 色彩角色'),item.slug);ui.q('#copy-document').click();await until(()=>ui.copied.at(-1)===design);
  ui.q('#tab-prompts').click();await until(()=>!ui.q('#copy-current-prompt').disabled);const prompt=ui.q('#current-prompt-text').textContent;
  assert.equal(ui.q('#individual-downloads').open,false,item.slug);
  assert.equal(ui.q('#start-prompt').textContent,usage.start_prompt,item.slug);
  assert.equal(ui.q('#copy-start-prompt').disabled,false,item.slug);
  ui.q('#download-usage').open=true;ui.q('#copy-start-prompt').click();await until(()=>ui.copied.at(-1)===usage.start_prompt);
  await until(()=>!ui.q('#copy-full-reference').disabled);
  ui.q('#copy-full-reference').click();await until(()=>ui.copied.at(-1)===ui.q('#combined-reference-text').textContent);
  const combined=ui.copied.at(-1);
  assert.ok(combined.startsWith('# '+item.name+' 網站製作參考\n'),item.slug);
  assert.ok(combined.includes(usage.copy_intro),item.slug);
  assert.ok(combined.includes(design.trimEnd()),item.slug);
  assert.ok(combined.includes(prompt.trimEnd()),item.slug);
  assert.equal(ui.q('#download-simple-pack').getAttribute('href'),'assets/design-packs/'+encodeURIComponent(item.slug)+'-simple.zip');
  ui.q('#individual-downloads').open=true;
  assert.ok(prompt.includes('我的產品名稱'),item.slug);ui.q('#copy-current-prompt').click();await until(()=>ui.copied.at(-1)===prompt);
  assert.equal(ui.q('#download-implementation-pack').getAttribute('href'),'assets/design-packs/'+encodeURIComponent(item.slug)+'.zip');
  assert.equal(ui.q('#download-implementation-pack').hidden,false);
 }
});

test('two equivalent entry points stay in the header while the complete pack is in advanced options',async t=>{
 const ui=await fixture(t,{hash:'#/design/figma'});
 await until(()=>!ui.q('#download-simple-pack').hidden);
 const pack=ui.q('#download-simple-pack');
 assert.equal(ui.w.document.querySelectorAll('#download-simple-pack').length,1);
 assert.equal(ui.w.document.querySelectorAll('#copy-full-reference').length,1);
 assert.equal(pack.closest('[role="tabpanel"]'),null);
 assert.equal(pack.getAttribute('aria-label'),'下載 Figma 簡易包');
 assert.equal(pack.getAttribute('download'),'figma-simple.zip');
 for(const name of ['preview','document','prompts']){
  ui.q('#tab-'+name).click();assert.equal(pack.hidden,false);
 }
 assert.equal(ui.q('#individual-downloads').open,false);
 for(const selector of ['#download-implementation-pack','#download-design','#download-prompts'])assert.equal(ui.q(selector).closest('details').id,'individual-downloads');
 ui.q('#tab-preview').click();
 pack.addEventListener('click',e=>e.preventDefault(),{once:true});pack.click();
 assert.equal(ui.q('#tab-prompts').getAttribute('aria-selected'),'true');
 assert.equal(ui.q('#usage-content').hidden,false);
 assert.equal(ui.q('#download-usage').open,true);
 assert.equal(ui.q('#panel-prompts').querySelectorAll('.usage-method').length,2);
});

test('unavailable source metadata cannot advertise a working download or starter copy',async t=>{
 const ui=await fixture(t,{hash:'#/design/figma',progressFailure:true});
 await until(()=>ui.q('#pack-status').textContent.includes('無法載入'));
 assert.equal(ui.q('#download-implementation-pack').hidden,true);
 assert.equal(ui.q('#download-implementation-pack').hasAttribute('href'),false);
 assert.equal(ui.q('#usage-content').hidden,true);
 assert.equal(ui.q('#copy-start-prompt').disabled,true);
 assert.equal(ui.q('#download-simple-pack').hidden,true);
 assert.equal(ui.q('#download-simple-pack').hasAttribute('href'),false);
 assert.equal(ui.q('#copy-full-reference').disabled,true);
 assert.equal(ui.q('#download-design').hidden,true);
 assert.equal(ui.q('#download-prompts').hidden,true);
});

for(const fallbackCopy of [false,true]){
 test('complete-copy failure leaves both full documents selectable: '+(fallbackCopy?'fallback':'clipboard denial'),async t=>{
  const ui=await fixture(t,{hash:'#/design/stripe',clipboardFailure:true,fallbackCopy});
  await until(()=>!ui.q('#copy-full-reference').disabled);ui.q('#copy-full-reference').click();
  await until(()=>ui.q('#copy-reference-details').open);
  assert.equal(ui.copied.length,0);
  assert.equal(ui.q('#tab-prompts').getAttribute('aria-selected'),'true');
  assert.equal(ui.w.document.activeElement.id,'combined-reference-text');
  assert.ok(ui.q('#combined-reference-text').textContent.includes('## 色彩角色'));
  assert.ok(ui.q('#combined-reference-text').textContent.includes('# Stripe AI 實作指令'));
  assert.match(ui.q('#toast').textContent,/剪貼簿/);
  assert.equal(ui.w.document.querySelectorAll('textarea').length,0);
 });
}

test('a failed combined-copy fetch can retry and never copies only one document',async t=>{
 let fail=true;
 const ui=await fixture(t,{hash:'#/design/figma',documentResponse:file=>({ok:!fail,text:async()=>read(published+file)})});
 await until(()=>ui.q('#copy-full-reference').textContent==='重新載入複製內容');
 assert.equal(ui.q('#download-simple-pack').hidden,false);
 assert.equal(ui.q('#combined-reference-text').textContent,'');assert.equal(ui.copied.length,0);
 fail=false;ui.q('#copy-full-reference').click();
 await until(()=>ui.q('#copy-full-reference').textContent==='一次複製給 AI');
 assert.equal(ui.copied.length,0);ui.q('#copy-full-reference').click();
 await until(()=>ui.copied.length===1);
 assert.ok(ui.copied[0].includes('## DESIGN.md｜完整設計規格'));
 assert.ok(ui.copied[0].includes('## PROMPTS.md｜完整 AI 實作指令'));
});

test('starter copy failure keeps a selectable command and reports no false success',async t=>{
 const ui=await fixture(t,{hash:'#/design/figma',clipboardFailure:true});
 await until(()=>!ui.q('#copy-start-prompt').disabled);ui.q('#tab-prompts').click();ui.q('#download-usage').open=true;
 ui.q('#copy-start-prompt').click();await until(()=>ui.q('#toast').textContent.includes('剪貼簿'));
 assert.equal(ui.copied.length,0);assert.equal(ui.q('#start-prompt').textContent,usage.start_prompt);
 assert.equal(ui.w.document.querySelectorAll('textarea').length,0);
});
