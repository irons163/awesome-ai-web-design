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
for(const asset of manifest.assets){const u=new URL(asset.source_url);if(u.hash){u.hash='';if(!assets.has(u.href))assets.set(u.href,asset);}}
for (const a of assets.values()) if (hash(fs.readFileSync(path.join(work, a.path))) !== a.sha256) throw new Error('Changed original public asset');
const tracking = /google-analytics\.com|analytics\.google\.com|analytics00\.meride\.tv|tr\.line\.me\/tag\.gif|doubleclick|googlead|\/pagead\/|\/collect(?:[/?]|$)|tags\.srv\.|ads\.linkedin|adsct|\/pixel|segment\.com|bat\.bing\.com\/action|facebook\.com\/tr(?:[/?]|$)|connect\.facebook\.net|googletagmanager\.com/i;
function local(value, base = officialURL) {
  if (!value || /^(?:data:|#|mailto:|tel:)/.test(value) || value.startsWith(`${slug}-assets/`)) return value;
  if (/^javascript:/i.test(value)) return '#';
  const url = new URL(value, base);
  if (url.searchParams.has('_gl')) url.searchParams.delete('_gl');
  if (tracking.test(url.href)) return '';
  const fragment=url.hash; const exact=assets.get(url.href);url.hash='';
  return (exact||assets.get(url.href))?.path ? (exact||assets.get(url.href)).path+fragment : url.href+fragment;
}
const css = (text, base) => text.replace(/url\(\s*(['"]?)(.*?)\1\s*\)/g, (all, q, u) => `url("${local(u, base)}")`);
function stylesheet(asset,seen=new Set()){
 if(seen.has(asset.source_url))return '';seen.add(asset.source_url);
 const text=fs.readFileSync(path.join(work,asset.path),'utf8');
 const expanded=text.replace(/@import\s+(?:url\(\s*)?['"]?([^\s'";)]+)['"]?\s*\)?\s*;/g,(all,u)=>{const source=new URL(u,asset.source_url).href;const child=assets.get(source);if(!child)throw new Error('Unpreserved stylesheet import: '+source);return stylesheet(child,new Set(seen));});
 return css(expanded.replace(/@charset[^;]+;/g,''),asset.source_url);
}
const config = {attributes: {}, bodies: {}, breakpoint: Number(breakpoint)};
const ribbonFont=assets.get('https://www.playstation.com/content/dam/global_pdc/site-furniture/marvels-wolverine/alternategotno1d/AlternateGotNo1D.ttf?v=1');
const styles = new Set([`@font-face{font-family:AlternateGotNo1D;src:url("${ribbonFont.path}") format("truetype");font-weight:400;font-style:normal;font-display:swap}`]);
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
    const bottom=read(`${slug}-oct10-official-${width}-bottom-state-reference.json`);
    const fallback=bottom.images.filter(x=>x.alt===e.alt&&x.src);
    const source = r.images[i].src || (fallback.length===1?fallback[0].src:'');
    if (!source) { e.remove(); return; }
    if (!/^(data:|blob:)/.test(source) && !tracking.test(source) && !assets.has(source)) throw new Error('Unpreserved observed image: ' + source);
    if (tracking.test(source)) { e.remove(); return; }
    e.src = local(source); e.removeAttribute('srcset'); e.removeAttribute('sizes'); e.setAttribute('loading', 'eager');
  });
  // The two captured responsive templates already use each viewport's actual image URL.
  document.querySelectorAll('picture source').forEach(e => e.remove());
  for (const e of [...document.querySelectorAll('style,link[rel="stylesheet"]')]) {
    if(e.tagName.toLowerCase()==='style'&&e.closest('svg'))continue;
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
        styles.add(stylesheet(asset));
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
  document.querySelectorAll('input').forEach(e => {
    const type = (e.getAttribute('type') || 'text').toLowerCase();
    if (!['submit', 'button', 'reset', 'checkbox', 'radio', 'hidden'].includes(type)) {
      e.value = '';
      e.readOnly = true;
    }
  });
  const frozen=read(`${slug}-oct10-frozen-styles-${width}.json`);
  const ribbon=document.querySelector('button[aria-label="Découvrez Wolverine en action — Entrer en mode Rage"]');
  for(const record of frozen.ribbon){let node=ribbon;for(const index of record.path)node=node?.children[index];if(!node)throw new Error('Changed ribbon DOM');node.setAttribute('style',(node.getAttribute('style')||'')+';opacity:'+record.opacity+';transform:'+record.transform+';');}
  const sony=document.querySelector('#sony-bar');sony.style.position='absolute';sony.style.top=width===1280?'0px':'auto';sony.style.bottom=width===1280?'auto':'0px';sony.style.height='36px';sony.style.backgroundColor=frozen.sony.backgroundColor;
  config.attributes[width] = {html: Object.fromEntries([...document.documentElement.attributes].map(a => [a.name, a.value])), body: Object.fromEntries([...document.body.attributes].map(a => [a.name, a.value]))};
  config.bodies[width] = document.body.innerHTML;
}
const menuRecord=read(`${slug}-oct10-official-menu-reference.json`);const menuHTML=menuRecord.htmlParts.join('');
if(menuHTML.length!==menuRecord.length||!menuHTML.endsWith('</section>'))throw new Error('Incomplete root menu');
const menuDocument=new JSDOM(menuHTML,{runScripts:'outside-only',virtualConsole:new VirtualConsole()}).window.document;
menuDocument.querySelectorAll('script,iframe,style,link').forEach(e=>{if(e.tagName.toLowerCase()==='style'&&e.closest('svg'))return;e.remove();});
for(const e of menuDocument.querySelectorAll('*')){
 for(const a of [...e.attributes])if(/^on/i.test(a.name))e.removeAttribute(a.name);
 for(const a of ['src','href','poster','xlink:href'])if(e.hasAttribute(a))e.setAttribute(a,local(e.getAttribute(a)));
 if(e.hasAttribute('style'))e.setAttribute('style',css(e.getAttribute('style'),officialURL));
}
config.openMenuRoot=menuDocument.querySelector('#shared-nav-root').outerHTML;
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
    const mediaObserver = new IntersectionObserver(entries => entries.forEach(entry => {
      const video = entry.target;
      if (entry.isIntersecting) video.play().catch(() => {}); else video.pause();
    }));
    document.querySelectorAll('video').forEach(v => {v.muted = true; v.loop = true; v.preload = 'auto'; v.load(); mediaObserver.observe(v);});
  }
  let closedRoot,menuOpen=false;
  function toggleMenu(force){const root=document.querySelector('#shared-nav-root');if(!root)return;const next=force??!menuOpen;
   if(next&&!menuOpen){closedRoot=root.outerHTML;root.outerHTML=CONFIG.openMenuRoot;menuOpen=true;}
   else if(!next&&menuOpen){root.outerHTML=closedRoot;menuOpen=false;}
  }
  document.addEventListener('click',e=>{if(e.target.closest('.shared-nav-hamburger')){e.preventDefault();toggleMenu();}});
  document.addEventListener('keydown',e=>{if(e.key==='Escape')toggleMenu(false);});
  function syncNavigation(){const root=document.querySelector('#shared-nav-root'),nav=document.querySelector('#shared-nav-container');if(!root||!nav)return;const mobile=matchMedia('(max-width:767px)').matches,threshold=mobile?0:36;
    root.style.minHeight=(mobile?60:64)+'px';const ribbonRoot=document.querySelector('#project-whisky-hpto-micropod-root');if(ribbonRoot){ribbonRoot.style.top=scrollY>threshold?(mobile?60:64)+'px':'0px';ribbonRoot.style.opacity=scrollY>innerHeight*1.5?'0':'1';}if(scrollY>threshold){nav.style.position='fixed';nav.style.left='0px';nav.style.top='0px';}else{nav.style.position='relative';nav.style.left='auto';nav.style.top='auto';}
  }
  document.addEventListener('scroll',syncNavigation,{passive:true});
  document.addEventListener('submit', e => {e.preventDefault(); location.assign(OFFICIAL_URL);});
  media.addEventListener('change', install); install();
}
const buildFingerprint=hash(JSON.stringify({config,styles:[...styles],runtime:runtime.toString()}));
const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><meta name="study-build-fingerprint" content="${buildFingerprint}"><title>${slug} — dated unofficial homepage study</title><style>${[...styles].join('\n').replace(/<\/style/gi, '<\\/style')}</style></head><body><script id="study-runtime">const OFFICIAL_URL=${JSON.stringify(officialURL)};const CONFIG=${JSON.stringify(config).replace(/</g, '\\u003c')};(${runtime.toString()})();</script></body></html>`;
const old = path.join(work, `${slug}-pre-oct10-draft.html`);
if (!fs.existsSync(old)) fs.copyFileSync(path.join(work, `${slug}.html`), old);
fs.writeFileSync(path.join(work, `${slug}.html`), html);
fs.writeFileSync(path.join(work, `${slug}-oct10-build-record.json`), JSON.stringify({accepted: false, method: 'Current rendered public DOM/CSS/original assets corrected after genuine native Stitch generation, which is preserved separately.', references, assets: manifest.assets, html: {bytes: Buffer.byteLength(html), sha256: hash(html)}, remaining: ['Actual rendered desktop/narrow visual review', 'Interactive and animated states, real devices and other widths', 'Published deployment verification']}, null, 2) + '\n');
console.log(JSON.stringify({slug, bytes: Buffer.byteLength(html), assets: assets.size, accepted: false}));
