import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {JSDOM, VirtualConsole} from 'jsdom';

const capture = path.resolve(process.argv[2] || '/private/tmp/official-browser-figma-framer-oct10');
const work = path.resolve('.stitch-work/current-official');
const brands = process.argv.slice(3).length ? process.argv.slice(3) : ['figma', 'framer'];
const hash = value => crypto.createHash('sha256').update(value).digest('hex');
const read = name => JSON.parse(fs.readFileSync(path.join(capture, name), 'utf8'));
const write = (name, value) => fs.writeFileSync(path.join(work, name), JSON.stringify(value, null, 2) + '\n');
const parse = html => new JSDOM(html, {virtualConsole: new VirtualConsole()}).window.document;
const visualURL = value => /^(data:image\/|https:\/\/(?:[^/]*\.)?(?:figma\.com|sanity\.io|framer\.com|framerusercontent\.com|googleapis\.com|gstatic\.com)\/)/i.test(value);
const tracking = ['tid', 'gclid', 'fbclid', 'li_fat_id', '_ga'];
function cleanLink(value, origin) {
  const url = new URL(value, origin);
  for (const key of tracking) url.searchParams.delete(key);
  return url.href;
}
function sanitize(html, origin, allowedFrames = []) {
  const document = parse(html.replace(/<noscript\b[^>]*>[\s\S]*?<\/noscript\s*>/gi, ''));
  document.querySelectorAll('script,object,embed,template,input[type="hidden"],[id^="codex-browser-"]').forEach(e => e.remove());
  document.querySelectorAll('iframe').forEach(e => {if (!allowedFrames.includes(e.getAttribute('src'))) e.remove();});
  document.querySelectorAll('link[as="script"],link[as="fetch"],link[rel="prefetch"],meta[http-equiv="refresh"]').forEach(e => e.remove());
  document.querySelectorAll('input,textarea').forEach(e => {e.removeAttribute('value'); if (e.tagName === 'TEXTAREA') e.textContent = '';});
  document.querySelectorAll('img[src]').forEach(e => {if (!visualURL(new URL(e.getAttribute('src'), origin).href)) e.remove();});
  document.querySelectorAll('*').forEach(e => [...e.attributes].forEach(a => {
    if (/^on|nonce|token|csrf|data-gtm|data-sentry/i.test(a.name)) e.removeAttribute(a.name);
    if (a.name === 'href' && /[?&](tid|gclid|fbclid|li_fat_id|_ga)=/.test(a.value)) e.setAttribute('href', cleanLink(a.value, origin));
  }));
  const walker = document.createTreeWalker(document, 128), comments = [];
  while (walker.nextNode()) comments.push(walker.currentNode);
  comments.forEach(e => e.remove());
  return '<!doctype html>' + document.documentElement.outerHTML;
}
function extension(bytes, kind) {
  const first = bytes.subarray(0, 4).toString();
  if (kind === 'stylesheet') {
    if (/^\s*</.test(bytes.toString())) throw new Error('HTML instead of CSS');
    return '.css';
  }
  if (kind === 'font') {
    if (first === 'wOF2') return '.woff2';
    if (first === 'wOFF') return '.woff';
    if (first === 'OTTO' || bytes.readUInt32BE(0) === 65536) return '.ttf';
    throw new Error('Invalid original font signature');
  }
  if (kind === 'video') {
    if (bytes.subarray(4, 8).toString() === 'ftyp') return '.mp4';
    if (bytes.subarray(0, 4).equals(Buffer.from([26, 69, 223, 163]))) return '.webm';
    throw new Error('Invalid original video signature');
  }
  if (bytes[0] === 255 && bytes[1] === 216) return '.jpg';
  if (bytes.subarray(1, 4).toString() === 'PNG') return '.png';
  if (first === 'RIFF') return '.webp';
  if (first === 'GIF8') return '.gif';
  if (bytes.subarray(4, 8).toString() === 'ftyp') return '.avif';
  if (/<svg[\s>]/i.test(bytes.subarray(0, 2000).toString())) return '.svg';
  throw new Error('Invalid original image signature');
}

for (const brand of brands) {
  if (!['figma', 'framer'].includes(brand)) throw new Error('Unsupported reference');
  const origin = `https://www.${brand}.com/`;
  const marker = brand === 'figma' ? 'The full-stack creative canvas' : 'Framer is the design agent for every step from idea to launch';
  fs.mkdirSync(path.join(work, brand + '-assets'), {recursive: true});
  const references = {}, assets = [], failures = [], required = new Map(), vimeo = {};
  const add = (value, kind) => {
    if (value && visualURL(value) && !value.startsWith('data:')) required.set(value, kind);
  };
  for (const variant of ['desktop', 'mobile']) {
    const raw = read(`${brand}-${variant}-complete-raw-private.json`);
    const original = raw.htmlParts.join('');
    if (original.length !== raw.htmlLength || raw.viewport.width !== (variant === 'desktop' ? 1280 : 390)) throw new Error('Incomplete browser capture');
    for (const sheet of raw.stylesheets) if (sheet.parts && sheet.parts.join('').length !== sheet.textLength) throw new Error('Incomplete CSSOM');
    const html = sanitize(original, origin), document = parse(html);
    if (!document.body.textContent.includes(marker)) throw new Error('Wrong public homepage');
    for (const node of document.querySelectorAll('link[rel="stylesheet"][href]')) add(new URL(node.getAttribute('href'), origin).href, 'stylesheet');
    for (const node of document.querySelectorAll('link[as="font"][href]')) add(new URL(node.getAttribute('href'), origin).href, 'font');
    for (const sheet of raw.stylesheets) for (const match of (sheet.parts?.join('') || '').matchAll(/url\(\s*["']?([^"')]+\.(?:woff2?|ttf|otf)(?:[^"')]*)?)["']?\s*\)/g)) add(new URL(match[1], sheet.href || origin).href, 'font');
    raw.images = raw.images.filter(image => visualURL(image.src));
    for (const image of raw.images) add(image.src, 'image');
    for (const video of raw.videos) {
      add(video.src, 'video'); add(video.poster, 'image');
      for (const source of video.sources) add(source, 'video');
    }
    if (brand === 'figma') {
      vimeo[variant] = read(`figma-${variant}-vimeo-reference.json`);
      for (const player of vimeo[variant].players) {
        if (player.iframe_src && !/^https:\/\/player\.vimeo\.com\/video\/\d+\?/.test(player.iframe_src)) throw new Error('Unexpected embedded player origin');
        add(player.poster, 'image');
      }
    }
    raw.htmlParts = html.match(/[\s\S]{1,50000}/g) || [];
    raw.htmlLength = html.length; raw.html_sha256 = hash(html);
    raw.links = raw.links.map(link => ({...link, href: cleanLink(link.href, origin)}));
    raw.controls = raw.controls.map(control => ({...control, html: parse(sanitize('<body>' + control.html + '</body>', origin)).body.innerHTML}));
    raw.method = 'Dated rendered public DOM/CSS and original browser screenshots; desktop user agent at both widths. Scripts, frames, comments, entered values, token attributes and telemetry images excluded offline. No cookies, storage or private account APIs read.';
    raw.limitations = ['Motion and lazy-load phases are dated observed states; full interaction and true mobile-user-agent verification remain separate tasks.'];
    const file = `${brand}-${variant}-browser-reference.json`;
    write(file, raw);
    references[variant] = {file, observed_at: raw.observed_at, viewport: raw.viewport, html_sha256: raw.html_sha256, bodyHeight: raw.bodyHeight, bodyWidth: raw.bodyWidth};
  }
  const retain = (asset, method) => {
    if (assets.some(a => a.source_url === asset.url)) return;
    const bytes = fs.readFileSync(asset.path), sha256 = hash(bytes);
    const ext = extension(bytes, asset.kind);
    const relative = `${brand}-assets/${hash(asset.url).slice(0, 16)}-${sha256.slice(0, 8)}${ext}`;
    if (fs.existsSync(path.join(work, relative)) && hash(fs.readFileSync(path.join(work, relative))) !== sha256) throw new Error('Original asset collision');
    fs.writeFileSync(path.join(work, relative), bytes);
    assets.push({source_url: asset.url, path: relative, kind: asset.kind, content_type: asset.contentType || null, bytes: bytes.length, sha256, method});
  };
  const bundle = read(`${brand}-desktop-asset-bundle-private.json`);
  const inventory = read(`${brand}-desktop-asset-inventory-private.json`);
  for (const asset of inventory.assets) if (asset.kind === 'font') add(asset.url, 'font');
  let omittedTelemetryFailures = 0;
  for (const asset of bundle.assets) if (visualURL(asset.url) && !asset.url.startsWith('data:')) retain(asset, 'Native pageAssets bundle; original bytes unchanged.');
  for (const failure of bundle.failures) {
    if (visualURL(failure.url)) failures.push({...failure, reason: failure.reason.slice(0, 1000)});
    else omittedTelemetryFailures++;
  }
  const missing = [...required].filter(([url]) => !assets.some(a => a.source_url === url));
  let position = 0;
  await Promise.all(Array.from({length: Math.min(4, missing.length)}, async () => {
    while (position < missing.length) {
      const [url, kind] = missing[position++];
      const temporary = path.join(capture, brand + '-original-' + hash(url).slice(0, 16));
      try {
        let contentType = null;
        if (!fs.existsSync(temporary)) {
          const legacyFile = path.join(work, brand + '-asset-provenance.json');
          const legacy = fs.existsSync(legacyFile) ? JSON.parse(fs.readFileSync(legacyFile)) : {};
          const cached = Object.entries(legacy).find(([name, source]) => source === url && fs.existsSync(path.join(work, brand + '-assets', name)));
          if (cached) {
            retain({url, kind, path: path.join(work, brand + '-assets', cached[0]), contentType}, 'Current observed public URL exactly matches a previously retained original; original bytes reused and current native acquisition failures retained separately.');
            continue;
          }
          execFileSync('curl', ['--fail', '--silent', '--show-error', '--compressed', '--max-time', '45', '--output', temporary + '.partial', url]);
          const bytes = fs.readFileSync(temporary + '.partial');
          extension(bytes, kind);
          fs.renameSync(temporary + '.partial', temporary);
        }
        retain({url, kind, path: temporary, contentType}, 'Observed public visual URL; unauthenticated HTTPS; original decoded response bytes unchanged.');
      } catch (error) {failures.push({url, method: 'Supplementary observed visual download', reason: String(error.message).slice(0, 1000)});}
    }
  }));
  assets.sort((a, b) => a.path.localeCompare(b.path));
  write(brand + '-browser-asset-provenance.json', {references, assets, failures, native_summaries: [{variant: 'desktop', ...bundle.summary}], omitted_telemetry_failures: omittedTelemetryFailures, method: 'Only original public visual resources. Native failures retained; no redrawing, resizing or recompression.'});
  if (brand === 'figma') write('figma-vimeo-browser-reference.json', {references: vimeo, method: 'Public vimeo-video host and open shadow-root iframe attributes observed in the official rendered page. Hero iframe contained a playing video at readyState 4. Blob URLs are not portable media sources and were not published. No replacement imagery or video invented.'});
  const screenshots = [];
  for (const variant of ['desktop', 'mobile']) for (const frame of ['first', 'full']) {
    const name = `${brand}-${variant}-${frame}.jpg`, bytes = fs.readFileSync(path.join(capture, name));
    fs.writeFileSync(path.join(work, name), bytes);
    screenshots.push({path: name, bytes: bytes.length, sha256: hash(bytes), method: 'Original browser JPEG unchanged.'});
  }
  for (const variant of ['desktop-products-menu', 'mobile-menu', 'mobile-products', 'desktop-platform-menu', 'mobile-platform-menu']) {
    const filename = `${brand}-${variant}-complete-raw-private.json`;
    if (!fs.existsSync(path.join(capture, filename))) continue;
    const raw = read(filename);
    if (raw.htmlParts.join('').length !== raw.htmlLength) throw new Error('Incomplete navigation state');
    const html = sanitize(raw.htmlParts.join(''), origin);
    if (brand === 'framer' && variant === 'desktop-platform-menu' && !parse(html).querySelector('nav')?.textContent.includes('External Agents')) continue;
    raw.htmlParts = html.match(/[\s\S]{1,50000}/g) || []; raw.htmlLength = html.length; raw.html_sha256 = hash(html);
    raw.images = raw.images.filter(image => visualURL(image.src));
    delete raw.controls;
    raw.links = raw.links.map(link => ({...link, href: cleanLink(link.href, origin)}));
    raw.method = 'Dated official navigation state, rendered DOM/CSSOM sanitized offline.';
    write(`${brand}-${variant}-browser-reference.json`, raw);
    fs.copyFileSync(path.join(capture, `${brand}-${variant}-first.jpg`), path.join(work, `${brand}-${variant}.jpg`));
  }
  if (brand === 'figma') {
    const controls = read('figma-video-controls.json');
    for (const state of ['pause', 'play']) controls[state] = parse(sanitize(controls[state], origin)).body.innerHTML;
    write('figma-video-controls.json', controls);
  } else {
    const navigation = read('framer-desktop-platform-navigation-private.json');
    if (!navigation.open || !navigation.html.includes('External Agents')) throw new Error('Verified native desktop platform navigation is required');
    navigation.html = parse(sanitize(navigation.html, origin)).body.innerHTML;
    navigation.html_sha256 = hash(navigation.html);
    write('framer-desktop-platform-navigation-browser-reference.json', navigation);
    fs.copyFileSync(path.join(capture, 'framer-desktop-platform-navigation-first.jpg'), path.join(work, 'framer-desktop-platform-navigation.jpg'));
    const player = read('framer-video-player-browser-reference-private.json');
    if (!/^https:\/\/www\.youtube\.com\/embed\/ueQv69QSsgI\?/.test(player.frame_src)) throw new Error('Unexpected public trailer source');
    player.html = parse(sanitize(player.html, origin, [player.frame_src])).body.innerHTML;
    player.html_sha256 = hash(player.html);
    player.method = 'Actual public YouTube overlay opened by the official 0:36 control; native DOM and matching CSS retained. Only the exact observed public trailer iframe is allowed.';
    write('framer-video-player-browser-reference.json', player);
    fs.copyFileSync(path.join(capture, 'framer-video-player-source-first.jpg'), path.join(work, 'framer-video-player-source-first.jpg'));
  }
  write(brand + '-reference.json', {accepted: false, references, screenshots, asset_provenance: brand + '-browser-asset-provenance.json', scope: 'Dated public desktop and narrow desktop-browser reference. Complete interaction, true phone and rendered public deployment remain separate acceptance tasks.'});
  console.log(JSON.stringify({brand, assets: assets.length, bytes: assets.reduce((n, a) => n + a.bytes, 0), missing_required: missing.filter(([url]) => !assets.some(a => a.source_url === url)).map(([url, kind]) => ({url, kind})), nativeFailures: bundle.failures.length}));
}
