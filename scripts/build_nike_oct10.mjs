// Source correction after a genuine, separately retained native Stitch generation.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {JSDOM, VirtualConsole} from 'jsdom';

const [slug, officialURL, breakpoint = '767'] = process.argv.slice(2);
if (!/^[a-z0-9.-]+$/.test(slug || '') || !officialURL?.startsWith('https://')) throw new Error('Expected brand slug and exact observed official URL');
const work = path.resolve('.stitch-work/current-official');
const read = n => JSON.parse(fs.readFileSync(path.join(work, n), 'utf8'));
const hash = b => crypto.createHash('sha256').update(b).digest('hex');
const manifest = read(`${slug}-oct10-assets.json`);
const videos = new Map(read('nike-oct10-video-provenance.json').derived.map(v=>[v.video_id,v]));
const assets = new Map(manifest.assets.map(a => [a.source_url, a]));
for (const a of assets.values()) if (hash(fs.readFileSync(path.join(work, a.path))) !== a.sha256) throw new Error('Changed original public asset');
const tracking = /google-analytics\.com|analytics\.google\.com|tr\.line\.me\/tag\.gif|doubleclick|googlead|\/pagead\/|\/collect(?:[/?]|$)|tags\.srv\.|ads\.linkedin|adsct|\/pixel|segment\.com|bat\.bing\.com\/action|facebook\.com\/tr(?:[/?]|$)|connect\.facebook\.net|googletagmanager\.com/i;
function local(value, base = officialURL) {
  if (!value || /^(?:data:|#|mailto:|tel:)/.test(value) || value.startsWith(`${slug}-assets/`)) return value;
  if (/^javascript:/i.test(value)) return '#';
  const url = new URL(value, base);
  if (url.searchParams.has('_gl')) url.searchParams.delete('_gl');
  if (tracking.test(url.href)) return '';
  return assets.get(url.href)?.path || url.href;
}
const css = (text, base) => text.replace(/url\(\s*(['"]?)(.*?)\1\s*\)/g, (all, q, u) => `url("${local(u, base)}")`);
const config = {attributes: {}, bodies: {}, breakpoint: Number(breakpoint)};
const styles = new Set();
const references = {};
for (const width of [1280, 390]) {
  const r = read(`${slug}-oct10-official-${width}-reference.json`);
  const html = r.htmlParts.join('');
  if (r.url !== officialURL || html.length !== r.html_length || hash(html) !== r.html_sha256 || !html.endsWith('</html>')) throw new Error('Incomplete or incorrect current reference');
  references[width] = {url: r.url, observed_at: r.observed_at, viewport: r.viewport, html_sha256: r.html_sha256};
  const parsedHTML = html.replace(/<noscript\b[^>]*>[\s\S]*?<\/noscript>/gi, '');
  const document = new JSDOM(parsedHTML, {runScripts: 'outside-only', virtualConsole: new VirtualConsole()}).window.document;
  const capturedStyles = [...document.querySelectorAll('style')];
  for (const record of r.inlineStyleRules || []) {
    const node = capturedStyles[record.index];
    const text = record.cssParts?.join('') || record.cssText || '';
    if (node && !node.textContent.trim() && text && !text.includes('[Truncated]')) node.textContent = text;
  }
  document.querySelectorAll('noscript').forEach(e => e.remove());
  const images = [...document.images];
  if (images.length !== r.images.length || images.some((e, i) => e.alt !== r.images[i].alt)) throw new Error('Observed source image order differs');
  images.forEach((e, i) => {
    const source = r.images[i].src;
    if (!source) { e.remove(); return; }
    if (!/^(data:|blob:)/.test(source) && !tracking.test(source) && !assets.has(source)) throw new Error('Unpreserved observed image: ' + source);
    if (tracking.test(source)) { e.remove(); return; }
    e.src = local(source); e.removeAttribute('srcset'); e.removeAttribute('sizes'); e.setAttribute('loading', 'eager');
  });
  // The two captured responsive templates already use each viewport's actual image URL.
  document.querySelectorAll('picture source').forEach(e => e.remove());
  for (const e of [...document.querySelectorAll('style,link[rel="stylesheet"]')]) {
    if (e.tagName === 'STYLE') styles.add(css(e.textContent, officialURL));
    else {
      if (!e.getAttribute('href')) { e.remove(); continue; }
      const url = new URL(e.getAttribute('href'), officialURL).href;
      // Third-party sign-in UI is outside the public homepage study; preserve its
      // recorded fetch failure rather than attempt to bypass the endpoint.
      if (url.startsWith('https://accounts.google.com/gsi/')) { e.remove(); continue; }
      if (!tracking.test(url)) {
        const asset = assets.get(url);
        if (!asset) throw new Error('Unpreserved current stylesheet: ' + url);
        styles.add(css(fs.readFileSync(path.join(work, asset.path), 'utf8'), url));
      }
    }
    e.remove();
  }
  document.querySelectorAll('script,iframe,base,meta[http-equiv],link,[id^="codex-browser-"],#__framer-editorbar-container,#__framer-editorbar').forEach(e => e.remove());
  for (const e of document.querySelectorAll('*')) {
    for (const a of [...e.attributes]) if (/^on/i.test(a.name) || /^data-airgap/.test(a.name)) e.removeAttribute(a.name);
    for (const a of ['src', 'href', 'poster', 'xlink:href']) if (e.hasAttribute(a)) e.setAttribute(a, local(e.getAttribute(a)));
    if (e.hasAttribute('style')) e.setAttribute('style', css(e.getAttribute('style'), officialURL));
  }
  document.querySelectorAll('video').forEach(e=>{const id=e.closest('[data-video-id]')?.getAttribute('data-video-id');const v=videos.get(id);if(!v)throw new Error('Unpreserved observed video '+id);e.src=v.path;e.removeAttribute('autoplay');e.muted=true;e.loop=true;e.setAttribute('playsinline','');});
  document.querySelector('[class*="pre-l-header-container"]')?.classList.remove('topbar-hidden');
  document.querySelector('nav[aria-label="secondary"]')?.parentElement.classList.remove('_3Bjkmzl6');
  document.querySelectorAll('form').forEach(e => {e.removeAttribute('action'); e.removeAttribute('method');});
  document.querySelectorAll('input').forEach(e => {
    const type = (e.getAttribute('type') || 'text').toLowerCase();
    if (!['submit', 'button', 'reset', 'checkbox', 'radio', 'hidden'].includes(type)) {
      e.value = '';
      e.readOnly = true;
    }
  });
  config.attributes[width] = {html: Object.fromEntries([...document.documentElement.attributes].map(a => [a.name, a.value])), body: Object.fromEntries([...document.body.attributes].map(a => [a.name, a.value]))};
  config.bodies[width] = document.body.innerHTML;
}
function runtime() {
  let current, live = [];
  const media = matchMedia(`(max-width:${CONFIG.breakpoint}px)`);
  function install() {
    const width = media.matches ? '390' : '1280';
    if (width === current) return;
    live.forEach(n => n.remove());
    for (const [node, values] of [[document.documentElement, CONFIG.attributes[width].html], [document.body, CONFIG.attributes[width].body]]) {
      for (const a of [...node.attributes]) node.removeAttribute(a.name);
      for (const [k, v] of Object.entries(values)) node.setAttribute(k, v);
    }
    const template = document.createElement('template'); template.innerHTML = CONFIG.bodies[width];
    live = [...template.content.childNodes]; document.body.insertBefore(template.content, document.getElementById('study-runtime'));
    current = width;
    const header=document.querySelector('[class*="pre-l-header-container"]');
    const secondary=document.querySelector('nav[aria-label="secondary"]')?.parentElement;
    const secondaryPlaceholder=secondary?.parentElement;
    const secondarySpacer=secondary?.previousElementSibling?.getAttribute('aria-hidden')==='true'?secondary.previousElementSibling:null;
    const scrollStates=()=>{header?.classList.toggle('topbar-hidden',scrollY>36);const fixed=!!secondaryPlaceholder&&secondaryPlaceholder.getBoundingClientRect().top<=0;secondary?.classList.toggle('_3Bjkmzl6',fixed);if(secondarySpacer)secondarySpacer.style.display=fixed?'block':'none';};
    addEventListener('scroll',scrollStates,{passive:true});scrollStates();
    const menu=document.querySelector('[data-testid="mobile-menu-container"]');
    const close=document.querySelector('button[aria-label="Close Menu"]');
    const scrim=document.querySelector('.scrim');
    const toggleMenu=open=>{document.body.classList.toggle('nav-menu-open',open);menu?.classList.toggle('draft-menu-open',open);if(close){close.disabled=!open;close.classList.toggle('disabled',!open);}scrim?.classList.toggle('draft-scrim-open',open);};
    document.querySelector('button[aria-label="menu"]')?.addEventListener('click',()=>toggleMenu(true));
    close?.addEventListener('click',()=>toggleMenu(false));scrim?.addEventListener('click',()=>toggleMenu(false));
    document.addEventListener('keydown',e=>{if(e.key==='Escape')toggleMenu(false);});
    for(const c of document.querySelectorAll('[aria-label="Auto-play carousel"]')){
      const track=c.firstElementChild,slides=[...track.children],dots=[...c.querySelectorAll('[aria-label*="Go to slide"]')];let index=0,timer=null;
      const select=n=>{index=(n+3)%3;track.style.transform='translateX(-'+((index+1)*100)+'%)';track.style.transition='none';slides.forEach((e,i)=>{const selected=i===index+1;e.setAttribute('aria-hidden',String(!selected));if(selected)e.removeAttribute('inert');else e.setAttribute('inert','');});dots.forEach((b,i)=>{b.classList.toggle('Eh9hXxQZ',i===index);b.setAttribute('aria-label',(i===index?'Current slide, ':'')+'Go to slide '+(i+1)+' of 3');});};
      dots.forEach((b,i)=>b.addEventListener('click',()=>select(i)));
      c.querySelector('button[aria-label="Next"]')?.addEventListener('click',()=>select(index+1));c.querySelector('button[aria-label="Previous"]')?.addEventListener('click',()=>select(index-1));
      const pause=c.querySelector('[data-qa="progress-pause-btn"]');pause?.addEventListener('click',()=>{if(timer){clearInterval(timer);timer=null;pause.setAttribute('aria-label','Resume carousel autoplay');}else{timer=setInterval(()=>select(index+1),7000);pause.setAttribute('aria-label','Pause carousel autoplay');}});select(0);
    }

    const mediaObserver = new IntersectionObserver(entries => entries.forEach(entry => {
      const video = entry.target;
      if (entry.isIntersecting) video.play().catch(() => {}); else video.pause();
    }));
    document.querySelectorAll('video').forEach(v => {v.muted = true; v.loop = true; v.preload = 'auto'; v.load(); mediaObserver.observe(v);});
  }
  document.addEventListener('submit', e => {e.preventDefault(); location.assign(OFFICIAL_URL);});
  media.addEventListener('change', install); install();
}
styles.add('.css-p135zs,.css-maogmj{font:var(--podium-cds-typography-960-to-1919-display4)}@media(max-width:959px){.css-p135zs,.css-maogmj{font:var(--podium-cds-typography-320-to-959-display4)}}@media(min-width:1920px){.css-p135zs,.css-maogmj{font:var(--podium-cds-typography-1920-plus-display4)}}');
styles.add('[data-testid="mobile-menu-container"]:not(.draft-menu-open){transform:translateX(100%)!important;visibility:hidden!important}[data-testid="mobile-menu-container"].draft-menu-open{display:flex!important;right:0!important;left:auto!important;transform:translateX(0)!important;visibility:visible!important}.draft-scrim-open{display:block!important;opacity:1!important;visibility:visible!important}');
const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>${slug} — dated unofficial homepage study</title><style>${[...styles].join('\n').replace(/<\/style/gi, '<\\/style')}</style></head><body><script id="study-runtime">const OFFICIAL_URL=${JSON.stringify(officialURL)};const CONFIG=${JSON.stringify(config).replace(/</g, '\\u003c')};(${runtime.toString()})();</script></body></html>`;
const old = path.join(work, `${slug}-pre-oct10-draft.html`);
if (!fs.existsSync(old)) fs.copyFileSync(path.join(work, `${slug}.html`), old);
fs.writeFileSync(path.join(work, `${slug}.html`), html);
fs.writeFileSync(path.join(work, `${slug}-oct10-build-record.json`), JSON.stringify({accepted: false, method: 'Current rendered public DOM/CSS/original assets corrected after genuine native Stitch generation, which is preserved separately.', references, assets: manifest.assets, html: {bytes: Buffer.byteLength(html), sha256: hash(html)}, remaining: ['Actual rendered desktop/narrow visual review', 'Interactive and animated states, real devices and other widths', 'Published deployment verification']}, null, 2) + '\n');
console.log(JSON.stringify({slug, bytes: Buffer.byteLength(html), assets: assets.size, accepted: false}));
