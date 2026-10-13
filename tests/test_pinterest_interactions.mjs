import assert from 'node:assert/strict';
import fs from 'node:fs';
import test from 'node:test';
import {JSDOM,VirtualConsole} from 'jsdom';

const html=fs.readFileSync(new URL('../.stitch-work/current-official/pinterest.html',import.meta.url),'utf8');

function fixture(t) {
  const dom=new JSDOM(html,{runScripts:'outside-only',url:'https://study.test/',virtualConsole:new VirtualConsole()});
  t.after(()=>dom.window.close());
  const {window}=dom;
  let narrow=false,change;
  window.matchMedia=()=>({get matches(){return narrow;},addEventListener(_event,listener){change=listener;}});
  window.IntersectionObserver=class {observe(){} unobserve(){}};
  let offset=0;
  const isList=element=>element.matches('.carousel--mode-multi-brand-module-carousel');
  Object.defineProperties(window.HTMLElement.prototype,{
    clientWidth:{get(){return isList(this)?1140:0;}},
    scrollWidth:{get(){return isList(this)?2890:0;}},
    scrollLeft:{get(){return isList(this)?offset:0;}},
    offsetLeft:{get(){return this.parentElement&&isList(this.parentElement)?[...this.parentElement.children].indexOf(this)*289:0;}}
  });
  function move(element,next){offset=Math.max(0,Math.min(1750,next));element.dispatchEvent(new window.Event('scroll'));}
  window.HTMLElement.prototype.scrollBy=function({left}){move(this,offset+left);};
  window.HTMLElement.prototype.scrollTo=function({left}){move(this,left);};
  window.eval(window.document.querySelector('#study-runtime').textContent);
  const query=selector=>window.document.querySelector(selector);
  const list=()=>query('.carousel--mode-multi-brand-module-carousel');
  return {window,query,list,get offset(){return offset;},resize(){narrow=!narrow;offset=0;change();}};
}

test('localized carousel buttons advance, clamp at the end, and return to the start',t=>{
  const ui=fixture(t);
  const previous=ui.query('[data-test-id="carousel-overlay-previous"]');
  const next=ui.query('[data-test-id="carousel-overlay-next"]');
  assert.equal(previous.disabled,true);
  assert.match(next.getAttribute('aria-label'),/下一個/);
  next.click();assert.equal(ui.offset,1156);assert.equal(previous.disabled,false);
  next.click();assert.equal(ui.offset,1750);assert.equal(next.disabled,true);
  previous.click();previous.click();assert.equal(ui.offset,0);assert.equal(previous.disabled,true);
});

test('carousel keyboard navigation supports both directions and endpoints',t=>{
  const ui=fixture(t);
  const press=key=>ui.list().dispatchEvent(new ui.window.KeyboardEvent('keydown',{key,cancelable:true,bubbles:true}));
  assert.equal(ui.list().tabIndex,0);
  press('ArrowRight');assert.equal(ui.offset,1156);
  press('ArrowLeft');assert.equal(ui.offset,0);
  press('End');assert.equal(ui.offset,1750);
  press('Home');assert.equal(ui.offset,0);
});

test('switching viewport templates preserves working carousel controls and read-only account fields',t=>{
  const ui=fixture(t);
  for(let pass=0;pass<2;pass++){
    ui.resize();
    ui.query('[data-test-id="carousel-overlay-next"]').click();
    assert.equal(ui.offset,1156);
    for(const field of ui.window.document.querySelectorAll('input[type="email"],input[type="password"],input[type="date"]'))assert.equal(field.readOnly,true);
    assert.equal(ui.query('iframe'),null);
    assert.match(ui.window.document.documentElement.lang,/^zh(?:-|$)/);
  }
});
