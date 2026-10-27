import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';
import {setTimeout as delay} from 'node:timers/promises';
import test from 'node:test';
import {JSDOM} from 'jsdom';

const read = file => readFileSync(new URL('../'+file,import.meta.url),'utf8');
const html=read('index.html'),app=read('assets/app.js'),catalog=JSON.parse(read('assets/catalog.json'));
const published=existsSync(new URL('../dist/client/official-progress.html',import.meta.url))?'dist/client/':'dist/';
const key='awesome-ai-web-design:favorites:v1';
async function until(predicate){for(let i=0;i<40;i++){if(predicate())return;await delay(5);}assert.fail('Catalog did not reach expected state');}
async function fixture(t,{hash='',favorites='[]',catalogFailure=false,blockedStorage=false,clipboardFailure=false,fallbackCopy=false}={}){
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
  if(file==='assets/catalog.json')return {ok:!fail,json:async()=>structuredClone(catalog)};
  if(file==='official-progress.html')return {ok:true,text:async()=>read(published+'official-progress.html')};
  if(file.startsWith('official-drafts/'))return {ok:true,text:async()=>read(published+file)};
  throw new Error('Unexpected file '+file);
 };
 w.eval(app);
 await until(()=>catalogFailure?!q('#load-error').hidden:q('#catalog').children.length===74);
 return {w,q,copied,recover(){fail=false;},slugs(){return [...w.document.querySelectorAll('[data-design]')].map(n=>n.dataset.design);},input(value){q('#search').value=value;q('#search').dispatchEvent(new w.Event('input',{bubbles:true}));}};
}

test('search, category and mode filters combine and clearing an empty result resets them all',async t=>{
 const ui=await fixture(t);ui.input('  STRIPE  ');assert.deepEqual(ui.slugs(),['stripe']);
 ui.input('支付');assert.ok(ui.slugs().includes('stripe'));
 ui.q('#search').value='';ui.q('[data-category="Fintech & Crypto"]').click();
 ui.q('#mode').value='dark';ui.q('#mode').dispatchEvent(new ui.w.Event('change'));
 const expected=catalog.designs.filter(d=>d.category==='Fintech & Crypto'&&d.mode==='dark').map(d=>d.slug).sort();
 assert.deepEqual(ui.slugs().sort(),expected);assert.ok(expected.includes('binance'));
 ui.input('不存在的設計xyz');assert.equal(ui.q('#empty').hidden,false);
 ui.q('#clear-filters').click();assert.equal(ui.slugs().length,74);assert.equal(ui.q('#mode').value,'all');assert.equal(ui.q('#search').value,'');
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
 await until(()=>ui.q('#catalog').children.length===74);assert.equal(ui.q('#load-error').hidden,true);
});

test('keyboard search, tabs, Escape close and return focus follow the visible controls',async t=>{
 const ui=await fixture(t);ui.w.document.dispatchEvent(new ui.w.KeyboardEvent('keydown',{key:'/'}));assert.equal(ui.w.document.activeElement.id,'search');
 const trigger=ui.q('a[aria-label="查看 Stripe 設計"]');trigger.focus();ui.w.location.hash='#/design/stripe';
 await until(()=>ui.q('#design-dialog').open);assert.equal(ui.w.document.activeElement.id,'close-dialog');
 ui.q('#tab-preview').dispatchEvent(new ui.w.KeyboardEvent('keydown',{key:'End',bubbles:true,cancelable:true}));
 assert.equal(ui.q('#tab-prompts').getAttribute('aria-selected'),'true');assert.equal(ui.w.document.activeElement.id,'tab-prompts');
 ui.q('#tab-prompts').dispatchEvent(new ui.w.KeyboardEvent('keydown',{key:'ArrowRight',bubbles:true,cancelable:true}));assert.equal(ui.q('#tab-preview').tabIndex,0);
 ui.q('#design-dialog').dispatchEvent(new ui.w.Event('cancel',{cancelable:true}));assert.equal(ui.q('#design-dialog').open,false);assert.equal(ui.w.document.activeElement,trigger);assert.equal(ui.w.location.hash,'#collection');
});

for(const hash of ['#/design/unknown-design','#/design/%E0%A4%A']){
 test('invalid shared link recovers to the collection: '+hash,async t=>{
  const ui=await fixture(t,{hash});assert.equal(ui.q('#design-dialog').open,false);assert.equal(ui.w.location.hash,'#collection');assert.match(ui.q('#toast').textContent,/找不到|格式有誤/);assert.equal(ui.slugs().length,74);
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

test('all 74 entries support preview, current specs, copy and implementation-pack links through the actual app',async t=>{
 const ui=await fixture(t);await until(()=>ui.q('.official-drafts-count').textContent.includes('74'));
 for(const item of catalog.designs){
  ui.w.location.hash='#/design/'+encodeURIComponent(item.slug);await until(()=>ui.q('#detail-title').textContent===item.name);
  assert.equal(ui.q('#current-preview-image').hidden,false,item.slug);assert.match(ui.q('#open-preview').getAttribute('href'),/official-drafts\/.+\.html$/);
  ui.q('#tab-document').click();await until(()=>!ui.q('#copy-document').disabled);const design=ui.q('#document-text').textContent;
  assert.ok(design.includes('## 色彩角色'),item.slug);ui.q('#copy-document').click();await until(()=>ui.copied.at(-1)===design);
  ui.q('#tab-prompts').click();await until(()=>!ui.q('#copy-current-prompt').disabled);const prompt=ui.q('#current-prompt-text').textContent;
  assert.ok(prompt.includes('我的產品名稱'),item.slug);ui.q('#copy-current-prompt').click();await until(()=>ui.copied.at(-1)===prompt);
  assert.equal(ui.q('#download-implementation-pack').getAttribute('href'),'assets/design-packs/'+encodeURIComponent(item.slug)+'.zip');
  assert.equal(ui.q('#download-implementation-pack').hidden,false);
 }
});
