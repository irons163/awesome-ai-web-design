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
const assets = new Map(manifest.assets.map(a => [a.source_url, a]));
for (const a of assets.values()) if (hash(fs.readFileSync(path.join(work, a.path))) !== a.sha256) throw new Error('Changed original public asset');
const tracking = /analytics|doubleclick|googlead|\/pagead\/|\/collect(?:[/?]|$)|tags\.srv\.|ads\.linkedin|adsct|\/pixel|segment\.com|bat\.bing\.com\/action|facebook\.com\/tr(?:[/?]|$)|connect\.facebook\.net|googletagmanager\.com/i;
function local(value, base = officialURL) {
  if (!value || /^(?:data:|#|mailto:|tel:)/.test(value) || value.startsWith(`${slug}-assets/`)) return value;
  if (/^javascript:/i.test(value)) return '#';
  const url = new URL(value, base);
  url.searchParams.delete('_gl');
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
  const document = new JSDOM(html, {runScripts: 'outside-only', virtualConsole: new VirtualConsole()}).window.document;
  const capturedStyles = [...document.querySelectorAll('style')];
  for (const record of r.inlineStyleRules || []) {
    if (record.cssText && capturedStyles[record.index]) capturedStyles[record.index].textContent = record.cssText;
  }
  document.querySelectorAll('noscript').forEach(e => e.remove());
  const images = [...document.images];
  if (images.length !== r.images.length || images.some((e, i) => e.alt !== r.images[i].alt)) throw new Error('Observed source image order differs');
  images.forEach((e, i) => {
    const source = r.images[i].src;
    if (!source) { e.remove(); return; }
    if (!/^(data:|blob:)/.test(source) && !tracking.test(source) && !assets.has(source)) throw new Error('Unpreserved observed image: ' + source);
    if (tracking.test(source)) { e.remove(); return; }
    e.src = local(source); e.removeAttribute('srcset'); e.removeAttribute('sizes'); e.loading = 'eager';
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
  document.querySelectorAll('form').forEach(e => {e.removeAttribute('action'); e.removeAttribute('method');});
  document.querySelectorAll('input').forEach(e => {e.value = ''; e.readOnly = true;});
  // A source-captured public map preserves the actually observed markers.
  const map=document.querySelector('.charging-map-component__map');
  if(map) map.innerHTML='<img src="tesla-oct10-map-'+width+'.png" alt="" style="display:block;width:100%;height:100%;object-fit:cover">';
  const hero=document.querySelector('.tcl-flex-module-carousel--homepage_hero_carousel');
  if(hero) {
    [...hero.querySelectorAll('.tcl-flex-module-carousel__slides > .tcl-flex-module-carousel__slide')].forEach((s,i)=>s.classList.toggle('tcl-flex-module-carousel__slide--active',i===0));
    hero.querySelectorAll('[aria-label="Tab List"]').forEach(n=>[...n.querySelectorAll('[role="tab"]')].forEach((t,i)=>t.setAttribute('aria-selected',String(i===0))));
  }
  config.attributes[width] = {html: Object.fromEntries([...document.documentElement.attributes].map(a => [a.name, a.value])), body: Object.fromEntries([...document.body.attributes].map(a => [a.name, a.value]))};
  config.bodies[width] = document.body.innerHTML;
}
function safeMenu(html){
  const d=new JSDOM(html,{virtualConsole:new VirtualConsole()}).window.document;
  d.querySelectorAll('script,iframe,base,link').forEach(e=>e.remove());
  for(const e of d.querySelectorAll('*')){
    for(const a of [...e.attributes]) if(/^on/i.test(a.name))e.removeAttribute(a.name);
    for(const a of ['src','href','poster','xlink:href']) if(e.hasAttribute(a))e.setAttribute(a,local(e.getAttribute(a)));
    if(e.hasAttribute('srcset')) e.removeAttribute('srcset');
    if(e.hasAttribute('style'))e.setAttribute('style',css(e.getAttribute('style'),officialURL));
  }
  return d.body.innerHTML;
}
config.menus={mobile:{},desktop:{}};
for(const [type,file] of [['mobile','tesla-oct10-mobile-menu-templates.json'],['desktop','tesla-oct10-desktop-menu-templates.json']]){
  for(const [name,value] of Object.entries(read(file))) config.menus[type][name]={html:safeMenu(typeof value==='string'?value:value.html),bodyClass:value.bodyClass||null};
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
    document.dispatchEvent(new CustomEvent("tesla-study-ready"));
    const mediaObserver = new IntersectionObserver(entries => entries.forEach(entry => {
      const video = entry.target;
      if (entry.isIntersecting) video.play().catch(() => {}); else video.pause();
    }));
    document.querySelectorAll('video').forEach(v => {v.muted = true; v.loop = true; v.preload = 'auto'; v.load(); mediaObserver.observe(v);});
  }
  document.addEventListener('submit', e => {e.preventDefault(); location.assign(OFFICIAL_URL);});
  media.addEventListener('change', install); install();
}
const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>${slug} — dated unofficial homepage study</title><script src="tesla-oct10-interactions.js" defer></script><style>${[...styles].join('\n').replace(/<\/style/gi, '<\\/style')}/* Public source computed footer padding: 92px at 390px, including the 68px fixed bottom bar. */
@media(max-width:599px){.tcl-page__shell .tcl-footer.tds-footer{padding-bottom:92px!important}}
/* Source desktop React state marks exactly one panel active. */
@media(min-width:768px){.dx-mega-menu-panel-content:not(.active){visibility:hidden!important;opacity:0!important;pointer-events:none!important}}
</style></head><body><script id="study-runtime">const OFFICIAL_URL=${JSON.stringify(officialURL)};const CONFIG=${JSON.stringify(config).replace(/</g, '\\u003c')};(${runtime.toString()})();</script></body></html>`;
const old = path.join(work, `${slug}-pre-oct10-draft.html`);
if (!fs.existsSync(old)) fs.copyFileSync(path.join(work, `${slug}.html`), old);
fs.writeFileSync(path.join(work, `${slug}.html`), html);
fs.writeFileSync(path.join(work, `${slug}-oct10-build-record.json`), JSON.stringify({accepted: false, method: 'Current rendered public DOM/CSS/original assets corrected after genuine native Stitch generation, which is preserved separately.', references, assets: manifest.assets, html: {bytes: Buffer.byteLength(html), sha256: hash(html)}, remaining: ['Actual rendered desktop/narrow visual review', 'Interactive and animated states, real devices and other widths', 'Published deployment verification']}, null, 2) + '\n');
console.log(JSON.stringify({slug, bytes: Buffer.byteLength(html), assets: assets.size, accepted: false}));
