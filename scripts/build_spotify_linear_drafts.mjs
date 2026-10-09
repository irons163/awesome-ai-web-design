import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {JSDOM, VirtualConsole} from 'jsdom';

const work = path.resolve('.stitch-work/current-official');
const read = name => JSON.parse(fs.readFileSync(path.join(work, name), 'utf8'));
const hash = value => crypto.createHash('sha256').update(value).digest('hex');
const parse = html => new JSDOM(html, {virtualConsole: new VirtualConsole()}).window.document;

function runtime() {
  const narrow = matchMedia('(max-width:799px)');
  let mode, live = [];
  const rootAttributes = element => [...element.attributes].map(a => a.name);
  function applyAttributes(element, attributes) {
    rootAttributes(element).forEach(name => element.removeAttribute(name));
    Object.entries(attributes).forEach(([name, value]) => element.setAttribute(name, value));
  }
  function install() {
    const next = narrow.matches ? 'mobile' : 'desktop';
    if (next === mode) return;
    live.forEach(node => node.remove());
    applyAttributes(document.documentElement, CONFIG.attributes[next].html);
    applyAttributes(document.body, CONFIG.attributes[next].body);
    const fragment = document.getElementById('study-' + next + '-source').content.cloneNode(true);
    live = [...fragment.childNodes];
    document.body.insertBefore(fragment, document.getElementById('study-runtime'));
    mode = next;
    if (CONFIG.brand === 'spotify') document.querySelectorAll('img[data-testid="card-image"]').forEach(image => {
      const ready = () => {
        if (!image.naturalWidth) return;
        // This is the original source's decoded-image state and fade-in class.
        image.dataset.imageStatus = 'loaded';
        image.classList.add('xMLEqLC2MvHjIHuD0xxf');
      };
      if (image.complete) ready(); else image.addEventListener('load', ready, {once: true});
    });
    document.querySelectorAll('video').forEach(video => {video.muted = true; video.playsInline = true;});
  }
  function mobileMenu(open) {
    const menu = document.querySelector('[data-study-mobile-menu]');
    const trigger = document.querySelector('button.TZTsQG_mobileMenuTrigger');
    if (!menu || !trigger) return;
    menu.hidden = !open;
    menu.toggleAttribute('data-open', open);
    trigger.toggleAttribute('data-popup-open', open);
    trigger.setAttribute('aria-expanded', String(open));
    trigger.setAttribute('aria-label', open ? 'Close site navigation' : 'Open site navigation');
    document.body.style.overflow = open ? 'hidden' : '';
    document.querySelectorAll('main').forEach(main => main.inert = open);
    if (open) menu.querySelector('a')?.focus();
    else trigger.focus();
  }
  function desktopMenu(name, restoreFocus = false) {
    document.querySelectorAll('[data-study-desktop-menu]').forEach(menu => {
      const active = menu.dataset.studyDesktopMenu === name;
      menu.hidden = !active;
      const trigger = [...document.querySelectorAll('button.TZTsQG_trigger')].find(button => button.textContent.trim().toLowerCase() === menu.dataset.studyDesktopMenu);
      trigger?.setAttribute('aria-expanded', String(active));
      trigger?.toggleAttribute('data-popup-open', active);
      trigger?.toggleAttribute('data-pressed', active);
      if (!active && restoreFocus && menu.contains(document.activeElement)) trigger?.focus();
    });
  }
  document.addEventListener('click', event => {
    const button = event.target.closest('button,[role="button"]');
    if (!button) {
      if (!event.target.closest('[data-study-desktop-menu]')) desktopMenu(null);
      return;
    }
    if (CONFIG.brand === 'linear') {
      if (button.matches('.TZTsQG_mobileMenuTrigger')) {
        mobileMenu(button.getAttribute('aria-expanded') !== 'true');
      } else if (button.matches('.TZTsQG_trigger')) {
        desktopMenu(button.getAttribute('aria-expanded') === 'true' ? null : button.textContent.trim().toLowerCase());
      }
      return;
    }
    const label = button.getAttribute('aria-label') || button.textContent.trim();
    const card = button.closest('.Card');
    if (card) {
      const destination = card.querySelector('a[href]');
      if (destination) location.assign(destination.href);
    } else if (/^Home$/i.test(label)) location.assign('https://open.spotify.com/');
    else if (/^Search$/i.test(label)) document.querySelector('input[role="combobox"]')?.focus();
    else if (/^Premium$/i.test(label)) location.assign('https://www.spotify.com/tw/premium/');
    else if (/^Support$/i.test(label)) location.assign('https://support.spotify.com/');
    else if (/^Download$/i.test(label)) location.assign('https://open.spotify.com/download');
    else if (/^Log in$/i.test(label)) location.assign('https://accounts.spotify.com/login');
    else if (/^Sign up( free)?$/i.test(label)) location.assign('https://www.spotify.com/signup/');
    else if (/^Create playlist$|^Browse podcasts$/.test(label)) location.assign('https://open.spotify.com/');
    else if (/^Install App$/i.test(label)) location.assign('https://www.spotify.com/download/');
  });
  document.addEventListener('submit', event => {
    event.preventDefault();
    if (CONFIG.brand === 'spotify') {
      const search = event.target.querySelector('input[role="combobox"],input[type="search"]');
      location.assign(search?.value.trim() ? 'https://open.spotify.com/search/' + encodeURIComponent(search.value.trim()) : 'https://open.spotify.com/');
    } else location.assign('https://linear.app/');
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape') {mobileMenu(false); desktopMenu(null, true);}
    const menu = document.querySelector('[data-study-mobile-menu]:not([hidden])');
    if (event.key === 'Tab' && menu) {
      const controls = [document.querySelector('button.TZTsQG_mobileMenuTrigger'), ...menu.querySelectorAll('a[href]')];
      const index = controls.indexOf(document.activeElement);
      if ((!event.shiftKey && index === controls.length - 1) || (event.shiftKey && index === 0)) {
        event.preventDefault(); controls[event.shiftKey ? controls.length - 1 : 0].focus();
      }
    }
  });
  narrow.addEventListener('change', install);
  install();
}

for (const brand of ['spotify', 'linear']) {
  const native = read(brand + '-stitch-oct10-generated.json');
  if (!native.screens?.length) throw new Error('A genuine new Stitch generation is required');
  for (const screen of native.screens) for (const file of screen.exports) {
    const bytes = fs.readFileSync(path.join(work, file.path));
    if (bytes.length !== file.bytes || hash(bytes) !== file.sha256) throw new Error('Native export differs from its recorded original');
  }
  const assets = new Map(read(brand + '-browser-asset-provenance.json').assets.map(a => [a.source_url, a]));
  for (const asset of assets.values()) {
    const bytes = fs.readFileSync(path.join(work, asset.path));
    if (bytes.length !== asset.bytes || hash(bytes) !== asset.sha256) throw new Error('Original asset differs: ' + asset.path);
  }
  const origin = brand === 'spotify' ? 'https://open.spotify.com/' : 'https://linear.app/';
  const used = new Set();
  const url = (value, base = origin) => {
    if (!value || /^(#|data:|mailto:|tel:)/i.test(value)) return value;
    if (/^javascript:/i.test(value)) return '#';
    const absolute = new URL(value, base).href;
    const asset = assets.get(absolute);
    if (asset) {used.add(asset.path); return asset.path;}
    return absolute;
  };
  const css = (value, base = origin) => value.replace(/url\(\s*(['"]?)(.*?)\1\s*\)/g,
    (match, quote, value) => /^(data:|#)/i.test(value) ? match : 'url("' + url(value, base) + '")');
  function localize(document) {
    document.querySelectorAll('base,meta[http-equiv],link:not([rel="stylesheet"]),.grecaptcha-badge,[id^="codex-browser-"]').forEach(e => e.remove());
    document.querySelectorAll('*').forEach(element => {
      for (const name of ['src', 'href', 'poster']) if (element.hasAttribute(name)) element.setAttribute(name, url(element.getAttribute(name)));
      if (element.hasAttribute('style')) element.setAttribute('style', css(element.getAttribute('style')));
      const srcset = element.getAttribute('srcset');
      if (srcset && !srcset.startsWith('data:')) element.setAttribute('srcset', srcset.split(/,\s*(?=(?:https?:|\/))/).map(item => {
        const tokens = item.trim().split(/\s+/); tokens[0] = url(tokens[0]); return tokens.join(' ');
      }).join(', '));
    });
    document.querySelectorAll('input[type="email"],input[type="password"]').forEach(input => {input.readOnly = true; input.autocomplete = 'off';});
    // A source snapshot has no application lazy-loader. Load its unchanged
    // original images eagerly so every shelf and the full-page proof can render.
    document.querySelectorAll('img').forEach(image => image.setAttribute('loading', 'eager'));
    document.querySelectorAll('form').forEach(form => {form.removeAttribute('action'); form.removeAttribute('method');});
  }
  const documents = {}, references = {}, styles = [];
  const attributes = element => Object.fromEntries([...element.attributes].map(a => [a.name, a.value]));
  const configuration = {brand, attributes: {}};
  for (const variant of ['desktop', 'mobile']) {
    const reference = read(brand + '-' + variant + '-browser-reference.json');
    const html = reference.htmlParts.join('');
    if (hash(html) !== reference.html_sha256) throw new Error('Source reference changed');
    const document = parse(html);
    const nodes = [...document.querySelectorAll('style,link[rel="stylesheet"]')];
    if (nodes.length !== reference.stylesheets.length) throw new Error('Stylesheet order is incomplete');
    const media = variant === 'desktop' ? '(min-width:800px)' : '(max-width:799px)';
    nodes.forEach((node, index) => {
      const sheet = reference.stylesheets[index];
      let text, base = origin;
      if (node.tagName === 'LINK') {
        base = new URL(node.getAttribute('href'), origin).href;
        if (base !== sheet.href) throw new Error('Stylesheet order mismatch');
        const asset = assets.get(base);
        if (!asset && !sheet.parts) throw new Error('Missing active stylesheet: ' + base);
        text = asset ? fs.readFileSync(path.join(work, asset.path), 'utf8') : sheet.parts.join('');
      } else {
        // CSS-in-JS inserts rules through CSSOM; outerHTML alone loses them.
        text = node.textContent || sheet.parts?.join('') || '';
      }
      if (text) styles.push('<style media="' + media + '">' + css(text, base).replace(/<\/style/gi, '<\\/style') + '</style>');
      node.remove();
    });
    localize(document);
    if (brand === 'linear' && variant === 'mobile') {
      const menu = read('linear-mobile-menu-reference.json');
      for (const sheet of menu.inline_css) if (sheet) styles.push('<style media="' + media + '">' + css(sheet).replace(/<\/style/gi, '<\\/style') + '</style>');
      const fragment = parse(menu.popup_html).body.firstElementChild;
      if (!fragment?.matches('.TZTsQG_mobileMenuContent')) throw new Error('Missing observed mobile menu');
      fragment.hidden = true; fragment.removeAttribute('data-open'); fragment.setAttribute('data-study-mobile-menu', '');
      const menuDocument = parse(fragment.outerHTML); localize(menuDocument);
      document.body.insertAdjacentHTML('beforeend', menuDocument.body.innerHTML);
      const trigger = document.querySelector('button.TZTsQG_mobileMenuTrigger');
      trigger.setAttribute('aria-controls', fragment.id);
      trigger.setAttribute('aria-expanded', 'false'); trigger.removeAttribute('data-popup-open');
      trigger.setAttribute('aria-label', 'Open site navigation');
    }
    if (brand === 'linear' && variant === 'desktop') {
      for (const name of ['product', 'resources']) {
        const menu = read('linear-desktop-' + name + '-menu-reference.json');
        for (const sheet of menu.inline_css) if (sheet) styles.push('<style media="' + media + '">' + css(sheet).replace(/<\/style/gi, '<\\/style') + '</style>');
        const fragment = parse(menu.portal_html);
        fragment.querySelectorAll('[data-base-ui-focus-guard]').forEach(e => e.remove());
        localize(fragment);
        const portal = fragment.body.firstElementChild;
        portal.hidden = true; portal.setAttribute('data-study-desktop-menu', name);
        document.body.insertAdjacentHTML('beforeend', portal.outerHTML);
        const trigger = [...document.querySelectorAll('button.TZTsQG_trigger')].find(e => e.textContent.trim().toLowerCase() === name);
        trigger.setAttribute('aria-controls', portal.querySelector('.TZTsQG_popup').id);
        trigger.setAttribute('aria-expanded', 'false'); trigger.removeAttribute('data-popup-open');
      }
    }
    configuration.attributes[variant] = {html: attributes(document.documentElement), body: attributes(document.body)};
    documents[variant] = document;
    references[variant] = {file: brand + '-' + variant + '-browser-reference.json', observed_at: reference.observed_at, html_sha256: reference.html_sha256};
  }
  const templates = ['desktop', 'mobile'].map(variant => '<template id="study-' + variant + '-source">' + documents[variant].body.innerHTML + '</template>').join('');
  const script = '<script id="study-runtime">const CONFIG=' + JSON.stringify(configuration).replace(/</g, '\\u003c') + ';(' + runtime.toString() + ')();</script>';
  const html = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>' + brand + ' — dated official-site working study</title>' + styles.join('') + '<style>[data-study-mobile-menu][hidden],[data-study-desktop-menu][hidden]{display:none!important}</style></head><body>' + templates + script + '</body></html>';
  fs.writeFileSync(path.join(work, brand + '.html'), html);
  fs.writeFileSync(path.join(work, brand + '-draft-build-record.json'), JSON.stringify({accepted: false,
    native_exports: brand + '-stitch-oct10-generated.json', source_references: references,
    asset_provenance: brand + '-browser-asset-provenance.json', asset_paths: [...used].sort(),
    working_draft: {path: brand + '.html', bytes: Buffer.byteLength(html), sha256: hash(html)},
    method: 'Working correction after an independently prompted native Stitch generation. Dated sanitized public source DOM, CSS/CSSOM, original vector marks, fonts and images retained; desktop and narrow source states switch at 800px. Native generation exports remain separate and unchanged.',
    limitations: brand === 'spotify' ? ['Narrow reference uses a desktop user agent and clips the desktop player; genuine phone behavior is not accepted.', 'Accounts, playback, changing recommendations and server search remain on Spotify.'] : ['The captured product demonstration is a dated visual state, not a working Linear account.', 'Scroll animation timing and complete interaction parity remain unaccepted.'],
  }, null, 2) + '\n');
  console.log(JSON.stringify({brand, bytes: Buffer.byteLength(html), retainedAssets: used.size, accepted: false}));
}
