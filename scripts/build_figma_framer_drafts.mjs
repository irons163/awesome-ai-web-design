import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {JSDOM, VirtualConsole} from 'jsdom';

const work = path.resolve('.stitch-work/current-official');
const read = name => JSON.parse(fs.readFileSync(path.join(work, name), 'utf8'));
const hash = value => crypto.createHash('sha256').update(value).digest('hex');
const parse = html => new JSDOM(html, {virtualConsole: new VirtualConsole()}).window.document;
function runtime() {
  const narrow = matchMedia('(max-width:' + (CONFIG.breakpoint - 1) + 'px)');
  let mode, live = [], mobileOpen = false, productOpen = false, trailerOpen = false, bannerObserver;
  const attrs = (e, values) => {for (const a of [...e.attributes]) e.removeAttribute(a.name); for (const [k,v] of Object.entries(values)) e.setAttribute(k,v);};
  const fragment = html => {const t = document.createElement('template'); t.innerHTML = html; return t.content;};
  function replaceNav(html) {document.querySelector('nav').replaceWith(fragment(html));}
  function videoCommand(host, method) {host.querySelector('iframe')?.contentWindow?.postMessage({method}, 'https://player.vimeo.com');}
  function installMedia() {
    if (CONFIG.brand === 'figma') {
      bannerObserver?.disconnect();
      const badge = document.querySelector('.official-draft-badge');
      const banner = document.querySelector('.announcement-banner');
      if (badge && banner) {
        bannerObserver = new ResizeObserver(() => {badge.style.bottom = (banner.getBoundingClientRect().height + 16) + 'px';});
        bannerObserver.observe(banner);
      }
      document.querySelectorAll('[aria-label="Media player"]').forEach(group => {
        const show = visible => {
          group.toggleAttribute('data-controls-visible', visible);
          group.querySelectorAll('.fig-e3oo29').forEach(control => control.toggleAttribute('data-visible', visible));
        };
        group.addEventListener('pointerenter', () => show(true));
        group.addEventListener('pointerleave', () => {if (!group.contains(document.activeElement)) show(false);});
        group.addEventListener('focusin', () => show(true));
        group.addEventListener('focusout', event => {if (!group.contains(event.relatedTarget)) show(false);});
      });
      const observer = new IntersectionObserver(entries => entries.forEach(entry => {entry.target.dataset.studyVisible = String(entry.isIntersecting); videoCommand(entry.target, entry.isIntersecting && entry.target.dataset.studyPaused !== 'true' ? 'play' : 'pause');}));
      document.querySelectorAll('vimeo-video').forEach(e => observer.observe(e));
    } else document.querySelectorAll('video').forEach(e => {e.muted = true; e.playsInline = true;});
  }
  window.addEventListener('message', event => {
    if (event.origin !== 'https://player.vimeo.com') return;
    let data = event.data; try {if (typeof data === 'string') data = JSON.parse(data);} catch {return;}
    if (data?.event !== 'ready') return;
    for (const host of document.querySelectorAll('vimeo-video')) if (host.querySelector('iframe')?.contentWindow === event.source) videoCommand(host, host.dataset.studyVisible === 'true' && host.dataset.studyPaused !== 'true' ? 'play' : 'pause');
  });
  function menu(open, products = false) {
    mobileOpen = open; productOpen = products;
    if (CONFIG.brand === 'figma') {
      document.querySelector('[role="dialog"][aria-label="Navigation Menu"]')?.parentElement.remove();
      if (open) document.body.append(fragment(CONFIG.widgets.mobile[products ? 'products' : 'menu']));
    } else replaceNav(open ? CONFIG.widgets.mobile[products ? 'products' : 'menu'] : CONFIG.widgets.mobile.closed);
    document.body.style.overflow = open ? 'hidden' : '';
    document.querySelectorAll('main').forEach(e => {if (!e.contains(document.querySelector('nav'))) e.inert = open;});
  }
  function desktopMenu(open) {
    productOpen = open;
    if (CONFIG.brand === 'figma') document.querySelector('header').replaceWith(fragment(CONFIG.widgets.desktop[open ? 'products' : 'closed']));
    else replaceNav(CONFIG.widgets.desktop[open ? 'products' : 'closed']);
  }
  function trailer(open) {
    trailerOpen = open;
    let node = document.getElementById('template-overlay');
    if (!node) {node = document.createElement('div'); node.id = 'template-overlay'; document.body.append(node);}
    node.innerHTML = open ? CONFIG.player : '';
    document.body.style.overflow = open ? 'hidden' : '';
  }
  function install() {
    const next = narrow.matches ? 'mobile' : 'desktop'; if (next === mode) return;
    live.forEach(e => e.remove());
    document.querySelector('[role="dialog"][aria-label="Navigation Menu"]')?.parentElement.remove();
    attrs(document.documentElement, CONFIG.attributes[next].html); attrs(document.body, CONFIG.attributes[next].body);
    const content = document.getElementById('study-' + next + '-source').content.cloneNode(true);
    live = [...content.childNodes]; document.body.insertBefore(content, document.getElementById('study-runtime'));
    mode = next; mobileOpen = false; productOpen = false; trailerOpen = false; installMedia();
  }
  document.addEventListener('click', event => {
    if (CONFIG.brand === 'framer' && event.target.closest('#template-overlay .framer-8evocl')) {trailer(false); return;}
    const button = event.target.closest('button,[role="button"],[tabindex="0"]');
    if (!button) return;
    const label = button.getAttribute('aria-label') || button.textContent.trim();
    if (CONFIG.brand === 'figma') {
      if (label === 'Open navigation menu') {menu(true); return;}
      if (label === 'Close navigation menu') {menu(false); return;}
      if (label === 'Products') {if (mode === 'mobile') menu(true, !productOpen); else desktopMenu(!productOpen); return;}
      if (label === 'Pause' || label === 'Play') {
        const host = button.closest('[aria-label="Media player"]')?.querySelector('vimeo-video'); if (!host) return;
        const paused = label === 'Pause'; host.dataset.studyPaused = String(paused); videoCommand(host, paused ? 'pause' : 'play');
        const replacement = fragment(CONFIG.videoControls[paused ? 'play' : 'pause']).firstElementChild;
        attrs(button, Object.fromEntries([...replacement.attributes].map(a => [a.name, a.value])));
        button.innerHTML = replacement.innerHTML; return;
      }
      if (label === 'Dismiss') {bannerObserver?.disconnect(); button.closest('.announcement-banner')?.remove(); document.querySelector('.official-draft-badge')?.style.removeProperty('bottom'); return;}
    } else {
      if (button.matches('[name="Mobile Menu"]')) {menu(!mobileOpen); return;}
      if (label === 'Platform') {if (mode === 'mobile') menu(true, !productOpen); else desktopMenu(!productOpen); return;}
      if (label === '0:36') {trailer(true); return;}
    }
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape') {if (trailerOpen) trailer(false); else if (mobileOpen) menu(false); else if (productOpen) desktopMenu(false);}
    if (event.key === 'Enter' && event.target.matches('[tabindex="0"]:not(a,button)')) {event.preventDefault(); event.target.click();}
  });
  document.addEventListener('submit', event => {event.preventDefault(); location.assign(CONFIG.origin);});
  narrow.addEventListener('change', install); install();
}

for (const brand of (process.argv.slice(2).length ? process.argv.slice(2) : ['figma', 'framer'])) {
  const native = read(brand + '-stitch-oct10-generated.json');
  if (!native.screens?.length) throw new Error('Genuine current Stitch generation required');
  for (const screen of native.screens) for (const file of screen.exports) if (hash(fs.readFileSync(path.join(work, file.path))) !== file.sha256) throw new Error('Original native export changed');
  const provenance = read(brand + '-browser-asset-provenance.json');
  const assets = new Map(provenance.assets.map(a => [a.source_url, a]));
  for (const asset of assets.values()) {const bytes = fs.readFileSync(path.join(work, asset.path)); if (bytes.length !== asset.bytes || hash(bytes) !== asset.sha256) throw new Error('Original visual asset changed');}
  const origin = `https://www.${brand}.com/`, used = new Set(), breakpoint = brand === 'figma' ? 1024 : 810;
  const url = (value, base = origin) => {
    if (!value || /^(#|data:|mailto:|tel:)/i.test(value)) return value;
    if (/^javascript:/i.test(value)) return '#';
    const absolute = new URL(value, base).href, asset = assets.get(absolute);
    if (asset) {used.add(asset.path); return asset.path;}
    return absolute;
  };
  const css = (value, base = origin) => value.replace(/url\(\s*(['"]?)(.*?)\1\s*\)/g, (match, quote, value) => /^(data:|#)/i.test(value) ? match : 'url("' + url(value, base) + '")');
  function localize(document) {
    document.querySelectorAll('base,meta[http-equiv],link:not([rel="stylesheet"])').forEach(e => e.remove());
    document.querySelectorAll('*').forEach(e => {
      for (const name of ['src','href','poster']) if (e.hasAttribute(name)) e.setAttribute(name, url(e.getAttribute(name)));
      if (e.hasAttribute('style')) e.setAttribute('style', css(e.getAttribute('style')));
    });
    document.querySelectorAll('img').forEach(e => {e.setAttribute('loading','eager'); e.removeAttribute('srcset');});
    document.querySelectorAll('picture source').forEach(e => e.removeAttribute('srcset'));
    document.querySelectorAll('input[type="password"],input[type="email"]').forEach(e => {e.readOnly = true; e.autocomplete = 'off';});
    document.querySelectorAll('form').forEach(e => {e.removeAttribute('action'); e.removeAttribute('method');});
  }
  const configuration = {brand, origin, breakpoint, attributes:{}, widgets:{desktop:{},mobile:{}}};
  const styles = [], documents = {}, references = {};
  const attributes = e => Object.fromEntries([...e.attributes].map(a => [a.name,a.value]));
  for (const variant of ['desktop','mobile']) {
    const reference = read(brand + '-' + variant + '-browser-reference.json'), html = reference.htmlParts.join('');
    if (hash(html) !== reference.html_sha256) throw new Error('Reference changed');
    const document = parse(html), nodes = [...document.querySelectorAll('style,link[rel="stylesheet"]')];
    if (nodes.length !== reference.stylesheets.length) throw new Error('Stylesheet order incomplete');
    const media = variant === 'desktop' ? `(min-width:${breakpoint}px)` : `(max-width:${breakpoint-1}px)`;
    nodes.forEach((node, index) => {
      const sheet = reference.stylesheets[index]; let text, base = origin;
      if (node.tagName === 'LINK') {base = new URL(node.getAttribute('href'),origin).href; if (base === 'https://accounts.google.com/gsi/style') {node.remove(); return;} const asset = assets.get(base); if (!asset && !sheet.parts) throw new Error('Missing original stylesheet: ' + base); text = asset ? fs.readFileSync(path.join(work,asset.path),'utf8') : sheet.parts.join('');}
      else text = node.textContent || sheet.parts?.join('') || '';
      if (text) styles.push('<style media="' + media + '">' + css(text,base).replace(/<\/style/gi,'<\\/style') + '</style>');
      node.remove();
    });
    localize(document);
    if (document.images.length !== reference.images.length) throw new Error('Image order differs');
    [...document.images].forEach((e,i) => e.setAttribute('src',url(reference.images[i].src)));
    if (brand === 'figma') {
      const players = read('figma-vimeo-browser-reference.json').references[variant].players;
      document.querySelectorAll('vimeo-video').forEach(host => {
        const player = players.find(p => p.src === host.getAttribute('src'));
        if (!player?.iframe_src) throw new Error('Missing actually observed public player');
        const iframe = document.createElement('iframe');
        for (const [k,v] of player.iframe_attributes) if (!/^data-|^on/i.test(k)) iframe.setAttribute(k,v);
        iframe.style.cssText = 'display:block;width:100%;height:100%;border:0'; host.append(iframe);
      });
    } else {
      const vectors = read('framer-open-navigation-vectors.json');
      for (const vector of vectors.symbols) if (!document.getElementById(vector.id)) {
        const container = document.getElementById('svg-templates');
        if (!container) throw new Error('Missing original zero-sized SVG definition container');
        container.append(...parse(vector.html).body.childNodes);
      }
    }
    configuration.attributes[variant] = {html:attributes(document.documentElement),body:attributes(document.body)};
    const selector = brand === 'figma' ? 'header' : 'nav';
    configuration.widgets[variant].closed = document.querySelector(selector)?.outerHTML;
    if (!configuration.widgets[variant].closed) throw new Error('Missing source navigation');
    const states = variant === 'desktop' ? ['products'] : ['menu','products'];
    for (const name of states) {
      if (brand === 'framer' && variant === 'desktop') {
        const state = read('framer-desktop-platform-navigation-browser-reference.json');
        if (!state.open || hash(state.html) !== state.html_sha256) throw new Error('Native platform state differs');
        for (const sheet of state.stylesheets || []) {
          if (sheet.parts?.join('').length !== sheet.textLength) throw new Error('Incomplete native open-menu stylesheet');
          if (sheet.parts?.join('')) styles.push('<style media="' + media + '">' + css(sheet.parts.join(''), sheet.href || origin).replace(/<\/style/gi,'<\\/style') + '</style>');
        }
        const widget = parse(state.html); localize(widget); configuration.widgets.desktop.products = widget.body.innerHTML; continue;
      }
      const file = brand + '-' + (variant === 'desktop' ? 'desktop-products-menu' : name === 'menu' ? 'mobile-menu' : brand === 'figma' ? 'mobile-products' : 'mobile-platform-menu') + '-browser-reference.json';
      const state = read(file), widget = parse(state.htmlParts.join('')); localize(widget);
      const node = brand === 'figma' && variant === 'mobile' ? widget.querySelector('[role="dialog"][aria-label="Navigation Menu"]')?.parentElement : widget.querySelector(selector);
      if (!node) throw new Error('Missing actual open navigation: ' + file);
      configuration.widgets[variant][name] = node.outerHTML;
      for (const sheet of state.stylesheets.filter(s => !s.href)) if (sheet.parts?.join('')) styles.push('<style media="' + media + '">' + css(sheet.parts.join('')).replace(/<\/style/gi,'<\\/style') + '</style>');
    }
    references[variant] = {file:brand+'-'+variant+'-browser-reference.json',observed_at:reference.observed_at,html_sha256:reference.html_sha256};
    documents[variant] = document;
  }
  if (brand === 'figma') {
    configuration.videoControls = read('figma-video-controls.json');
    const skin = read('figma-media-skin-browser-reference.json');
    const source = skin.shadow_styles.join('\n');
    styles.push('<style>' + source.replace(/:host\(:not\(\[controls\]\)\)/g, 'vimeo-video:not([controls])').replace(/:host/g, 'vimeo-video').replace(/\biframe\s*\{/g, 'vimeo-video > iframe {') + '</style>');
  }
  else {const player = read('framer-video-player-browser-reference.json'); const document = parse(player.html); localize(document); configuration.player = document.getElementById('template-overlay').innerHTML; styles.push('<style>' + css(player.css.join('\n')) + '</style>');}
  const templates = ['desktop','mobile'].map(v => '<template id="study-' + v + '-source">' + documents[v].body.innerHTML + '</template>').join('');
  const script = '<script id="study-runtime">const CONFIG=' + JSON.stringify(configuration).replace(/</g,'\\u003c') + ';(' + runtime.toString() + ')();</script>';
  const html = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>' + brand + ' — dated official-site working study</title>' + styles.join('') + '</head><body>' + templates + script + '</body></html>';
  fs.writeFileSync(path.join(work,brand+'.html'),html);
  fs.writeFileSync(path.join(work,brand+'-draft-build-record.json'),JSON.stringify({accepted:false,native_exports:brand+'-stitch-oct10-generated.json',source_references:references,asset_provenance:brand+'-browser-asset-provenance.json',asset_paths:[...used].sort(),working_draft:{path:brand+'.html',bytes:Buffer.byteLength(html),sha256:hash(html)},method:'Working correction after an independently prompted genuine Stitch generation. Original public source DOM/CSS, fonts, images, media and actually observed navigation/player states retained. Native generation exports remain immutable and separate.',limitations:['Motion phases, full interaction coverage and intermediate widths require further review.','Narrow captures use a desktop user agent; true mobile and rendered production comparison remain unaccepted.']},null,2)+'\n');
  console.log(JSON.stringify({brand,bytes:Buffer.byteLength(html),assets:used.size,accepted:false}));
}
