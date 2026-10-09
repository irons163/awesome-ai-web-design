import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { JSDOM, VirtualConsole } from 'jsdom';

const capture = path.resolve(process.argv[2] || '/private/tmp/official-browser-oct10');
const output = path.resolve('.stitch-work/current-official');
const hash = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const chunks = text => text.match(/[\s\S]{1,50000}/g) || [];
const read = name => JSON.parse(fs.readFileSync(path.join(capture, name), 'utf8'));
const write = (name, value) => fs.writeFileSync(path.join(output, name), JSON.stringify(value, null, 2) + '\n');

function sanitize(html) {
  html = html.replace(/<noscript\b[^>]*>[\s\S]*?<\/noscript\s*>/gi, '');
  const dom = new JSDOM(html, { virtualConsole: new VirtualConsole() });
  const document = dom.window.document;
  document.querySelectorAll('script,iframe,object,embed,template,input[type="hidden"],[id^="codex-browser-"]').forEach(node => node.remove());
  document.querySelectorAll('link[as="script"],link[as="fetch"],link[rel="prefetch"],meta[http-equiv="refresh"],img[src*="scorecardresearch.com"]').forEach(node => node.remove());
  document.querySelectorAll('input,textarea').forEach(node => {
    node.removeAttribute('value');
    if (node.tagName === 'TEXTAREA') node.textContent = '';
  });
  document.querySelectorAll('*').forEach(node => [...node.attributes].forEach(attribute => {
    if (/^on|nonce|token|csrf/i.test(attribute.name)) node.removeAttribute(attribute.name);
  }));
  const walker = document.createTreeWalker(document, 128);
  const comments = [];
  while (walker.nextNode()) comments.push(walker.currentNode);
  comments.forEach(node => node.remove());
  return dom.serialize();
}

function retain(brand, asset, method) {
  const bytes = fs.readFileSync(asset.path);
  const sha256 = hash(bytes);
  const extension = path.extname(asset.path) || '.bin';
  const relative = `${brand}-assets/${hash(asset.url).slice(0, 16)}-${sha256.slice(0, 8)}${extension}`;
  const destination = path.join(output, relative);
  if (fs.existsSync(destination) && hash(fs.readFileSync(destination)) !== sha256) {
    throw new Error('Asset collision: ' + relative);
  }
  if (!fs.existsSync(destination)) fs.copyFileSync(asset.path, destination);
  return { source_url: asset.url, path: relative, kind: asset.kind, content_type: asset.contentType, bytes: bytes.length, sha256, method };
}

for (const brand of ['spotify', 'linear']) {
  fs.mkdirSync(path.join(output, `${brand}-assets`), { recursive: true });
  const references = {};
  const fontUrls = new Set();
  const imageUrls = new Set();
  for (const [variant, width] of [['desktop', 1280], ['mobile', 390]]) {
    const raw = read(`${brand}-${variant}-complete-raw-private.json`);
    const original = raw.htmlParts.join('');
    if (original.length !== raw.htmlLength || raw.viewport.width !== width) throw new Error('Incomplete or wrong-viewport ' + brand + '/' + variant);
    for (const sheet of raw.stylesheets) {
      if (sheet.parts && sheet.parts.join('').length !== sheet.textLength) throw new Error('Incomplete stylesheet capture');
    }
    const cleaned = sanitize(original);
    const document = new JSDOM(cleaned, { virtualConsole: new VirtualConsole() }).window.document;
    const marker = brand === 'spotify' ? 'Trending songs' : 'The product development system for teams and agents';
    if (!document.body.textContent.includes(marker)) throw new Error('Missing public homepage content');
    for (const link of document.querySelectorAll('link[as="font"][href]')) fontUrls.add(new URL(link.getAttribute('href'), raw.reference_url).href);
    for (const image of document.querySelectorAll('img[src]')) {
      const url = new URL(image.getAttribute('src'), raw.reference_url);
      if (url.protocol === 'https:') imageUrls.add(url.href);
    }
    raw.htmlParts = chunks(cleaned);
    raw.htmlLength = cleaned.length;
    raw.html_sha256 = hash(cleaned);
    raw.method = 'Rendered signed-out public DOM/CSS, serialized in chunks before transport and sanitized offline. The browser uses its desktop user agent at both viewport sizes.';
    raw.sanitization = 'Scripts, noscript, frames, embedded objects, templates, comments, tool overlays, hidden inputs, entered values, inline handlers, token/nonce/CSRF attributes, script/fetch preloads and telemetry image excluded. Cookies, storage and private account APIs were not read.';
    if (brand === 'spotify') raw.capture_scope = 'Desktop web player with its own scrolling main pane. A full-page screenshot captures the outer window, not every position inside that pane.';
    if (brand === 'spotify' && variant === 'mobile') raw.viewport_limit = '390×844 narrow desktop browser, with observed document width812 and a clipped desktop player; this is not a true mobile-user-agent reference.';
    const filename = `${brand}-${variant}-browser-reference.json`;
    write(filename, raw);
    references[variant] = { file: filename, observed_at: raw.observed_at, viewport: raw.viewport, bodyHeight: raw.bodyHeight, bodyWidth: raw.bodyWidth, html_sha256: raw.html_sha256 };
  }
  const bundle = read(`${brand}-browser-asset-bundle.json`);
  const assets = bundle.assets.map(asset => retain(brand, asset, 'Native pageAssets bundle; original bytes retained unchanged.'));
  const failures = [...bundle.failures];
  for (const asset of bundle.assets.filter(asset => asset.kind === 'stylesheet')) {
    const css = fs.readFileSync(asset.path, 'utf8');
    for (const match of css.matchAll(/url\(\s*["']?([^"'()\s]+\.(?:woff2?|ttf|otf)(?:\?[^"'()\s]*)?)["']?\s*\)/gi)) {
      const url = new URL(match[1], asset.url);
      if (url.protocol === 'https:') fontUrls.add(url.href);
    }
  }
  for (const url of fontUrls) {
    if (assets.some(asset => asset.source_url === url)) continue;
    const temporary = path.join(capture, `${brand}-font-${hash(url).slice(0, 12)}.woff2`);
    try {
      if (!fs.existsSync(temporary) || fs.readFileSync(temporary).subarray(0, 4).toString() !== 'wOF2') {
        execFileSync('curl', ['--fail', '--silent', '--show-error', '--compressed', '--location', '--max-time', '45', url, '--output', temporary]);
      }
      if (fs.readFileSync(temporary).subarray(0, 4).toString() !== 'wOF2') throw new Error('Invalid WOFF2 signature');
      assets.push(retain(brand, { url, path: temporary, kind: 'font', contentType: 'font/woff2' }, 'Observed public font preload; unauthenticated HTTPS download with decoded HTTP content encoding; original WOFF2 bytes retained.'));
    } catch (error) {
      failures.push({ url, reason: String(error.message).slice(0, 1000), method: 'Supplementary public font download' });
    }
  }
  for (const url of imageUrls) {
    if (assets.some(asset => asset.source_url === url)) continue;
    const temporary = path.join(capture, `${brand}-image-${hash(url).slice(0, 12)}.bin`);
    try {
      if (!fs.existsSync(temporary)) execFileSync('curl', ['--fail', '--silent', '--show-error', '--compressed', '--location', '--max-time', '45', url, '--output', temporary]);
      const bytes = fs.readFileSync(temporary);
      const extension = bytes[0] === 0xff && bytes[1] === 0xd8 ? '.jpg' : bytes.subarray(1, 4).toString() === 'PNG' ? '.png' : bytes.subarray(0, 4).toString() === 'RIFF' ? '.webp' : /<svg[\s>]/i.test(bytes.subarray(0, 1000).toString()) ? '.svg' : null;
      if (!extension) throw new Error('Unsupported original image signature');
      const original = temporary + extension;
      fs.copyFileSync(temporary, original);
      assets.push(retain(brand, {url, path: original, kind: 'image', contentType: 'image/' + (extension === '.jpg' ? 'jpeg' : extension === '.svg' ? 'svg+xml' : extension.slice(1))}, 'Observed public img src; unauthenticated HTTPS download; original image bytes retained without resizing or recompression.'));
    } catch (error) {
      failures.push({url, reason: String(error.message).slice(0, 1000), method: 'Supplementary observed public image download'});
    }
  }
  write(`${brand}-browser-asset-provenance.json`, { observed_at: references.desktop.observed_at, references, assets, failures, native_summary: bundle.summary, method: 'Original browser asset bundle plus observed public font preloads. Images, vectors and fonts were not redrawn, resized or substituted.' });
  const screenshots = [];
  for (const variant of ['desktop', 'mobile']) for (const frame of ['first', 'full']) {
    const name = `${brand}-${variant}-${frame}.jpg`;
    const original = path.join(capture, name);
    if (!fs.existsSync(original)) continue;
    const bytes = fs.readFileSync(original);
    if (bytes[0] !== 0xff || bytes[1] !== 0xd8) throw new Error('Expected original browser JPEG');
    fs.copyFileSync(original, path.join(output, name));
    screenshots.push({ path: name, bytes: bytes.length, sha256: hash(bytes), method: 'Original browser screenshot, unchanged. Scroll-dependent animations and loading remain time dependent.' });
  }
  write(`${brand}-reference.json`, { accepted: false, references, screenshots, asset_provenance: `${brand}-browser-asset-provenance.json`, scope: 'Dated public desktop and narrow-viewport reference. Local correction, interactions and rendered public deployment require separate review.' });
  console.log(JSON.stringify({ brand, references, assets: assets.length, bytes: assets.reduce((sum, asset) => sum + asset.bytes, 0), failures: failures.length }));
}

const menu = read('linear-mobile-menu-raw-private.json');
const menuStyles = read('linear-mobile-menu-styles-raw-private.json');
const menuDocument = new JSDOM(sanitize(menuStyles.popup_html), {virtualConsole: new VirtualConsole()}).window.document;
write('linear-mobile-menu-reference.json', {
  observed_at: menuStyles.observed_at, viewport: menu.viewport, controls: menu.controls,
  trigger_open_html: menu.trigger_open_html, popup_html: menuDocument.body.innerHTML,
  popup_box: menu.popup_box, links: menuStyles.links, inline_css: menuStyles.inline_css,
  method: 'Observed public mobile navigation, sanitized offline; no account state, cookies or storage read.',
});
fs.copyFileSync(path.join(capture, 'linear-mobile-menu.jpg'), path.join(output, 'linear-mobile-menu.jpg'));
for (const variant of ['product', 'resources']) {
  const record = read('linear-desktop-' + variant + '-menu-raw-private.json');
  record.portal_html = new JSDOM(sanitize(record.portal_html), {virtualConsole: new VirtualConsole()}).window.document.body.innerHTML;
  record.method = 'Observed public desktop navigation and its CSSOM rules, sanitized offline; no account state read.';
  write('linear-desktop-' + variant + '-menu-reference.json', record);
  fs.copyFileSync(path.join(capture, 'linear-desktop-' + variant + '-menu.jpg'), path.join(output, 'linear-desktop-' + variant + '-menu.jpg'));
}
for (const frame of ['middle', 'footer']) {
  const name = 'spotify-desktop-' + frame + '.jpg';
  if (fs.existsSync(path.join(capture, name))) fs.copyFileSync(path.join(capture, name), path.join(output, name));
}
