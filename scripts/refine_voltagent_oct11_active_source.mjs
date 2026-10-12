import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {JSDOM, VirtualConsole} from 'jsdom';

const work = path.resolve('.stitch-work/current-official');
const target = path.join(work, 'voltagent.html');
const original = fs.readFileSync(target, 'utf8');
const start = original.indexOf('const CONFIG=') + 'const CONFIG='.length;
const end = original.indexOf(';(function runtime', start);
if (start < 13 || end < start) throw new Error('Missing source-corrected templates');
const config = JSON.parse(original.slice(start, end));
const hash = value => crypto.createHash('sha256').update(value).digest('hex');
const manifest = JSON.parse(fs.readFileSync(path.join(work, 'voltagent-oct10-assets.json'), 'utf8'));
const assets = new Map(manifest.assets.map(asset => [asset.source_url, asset]));
const unavailable = 'https://pbs.twimg.com/profile_images/2088056226089160704/DgHVP6vH_normal.jpg';
const changes = [], missing = [];
function local(value) {
  if (!value || /^(?:data:|#|mailto:|tel:|voltagent-assets\/)/.test(value)) return value;
  if (/^javascript:/i.test(value)) return '#';
  const url = new URL(value, 'https://voltagent.dev/').href;
  return assets.get(url)?.path || url;
}
function fragment(name) {
  const record = JSON.parse(fs.readFileSync(path.join(work, name), 'utf8'));
  const html = record.htmlParts.join('');
  if (record.url !== 'https://voltagent.dev/' || html.length !== record.html_length || hash(html) !== record.html_sha256) throw new Error('Incomplete active source');
  const document = new JSDOM(`<body>${html}</body>`, {virtualConsole: new VirtualConsole()}).window.document;
  const images = [...document.images];
  if (images.length !== record.images.length || images.some((image, index) => image.alt !== record.images[index].alt)) throw new Error('Active source image order changed');
  images.forEach((image, index) => {
    const source = record.images[index].src;
    if (!assets.has(source) && !/^(?:data:|blob:)/.test(source)) {
      const failure = manifest.failures.find(asset => asset.source_url === source);
      if (source !== unavailable || !/404/.test(failure?.error || '')) throw new Error('Unpreserved active image: ' + source);
      missing.push({reference: name, alt: image.alt, source_url: source, error: failure.error, source_natural_width: record.images[index].naturalWidth});
    }
    image.src = local(source); image.removeAttribute('srcset'); image.removeAttribute('sizes'); image.loading = 'eager';
  });
  document.querySelectorAll('script,iframe,base,meta,link,noscript,picture source').forEach(node => node.remove());
  for (const node of document.querySelectorAll('*')) {
    for (const attribute of [...node.attributes]) if (/^on/i.test(attribute.name) || /^data-airgap/.test(attribute.name)) node.removeAttribute(attribute.name);
    for (const attribute of ['src', 'href', 'poster', 'xlink:href']) if (node.hasAttribute(attribute)) node.setAttribute(attribute, local(node.getAttribute(attribute)));
    if (node.hasAttribute('style')) node.setAttribute('style', node.getAttribute('style').replace(/url\(\s*(['"]?)(.*?)\1\s*\)/g, (_, quote, value) => `url("${local(value)}")`));
  }
  document.querySelectorAll('form').forEach(node => {node.removeAttribute('action'); node.removeAttribute('method');});
  document.querySelectorAll('input').forEach(node => {node.value = ''; node.readOnly = true;});
  if (document.body.children.length !== 1) throw new Error('Expected one exact source wrapper');
  changes.push({reference: name, html_sha256: record.html_sha256, observed_at: record.observed_at, source_selector: record.selector, scrollY: record.scrollY, source_body_height: record.bodyHeight ?? null, images: images.length});
  return document.body.firstElementChild;
}
for (const width of [1280, 390]) {
  const document = new JSDOM(config.bodies[width], {virtualConsole: new VirtualConsole()}).window.document;
  if (width === 1280) {
    const currentMain = document.querySelector('main');
    if (!currentMain) throw new Error('Main slot missing');
    const main = fragment('voltagent-oct11-hero-settled-1280-reference.json');
    if (main.tagName !== 'MAIN' || !main.textContent.includes('AI Agent Engineering')) throw new Error('Unexpected settled main');
    currentMain.replaceWith(main);
  }
  // Removed style nodes alter nth-child positions in the sanitized template.
  // The exact visible heading and its four-level source wrapper are stable.
  const heading = [...document.querySelectorAll('h2')].find(node => node.textContent === 'What are they saying?');
  const current = heading?.parentElement?.parentElement?.parentElement?.parentElement;
  if (current?.tagName !== 'DIV' || !current.classList.contains('relative') || !current.parentElement?.parentElement?.matches('main')) throw new Error('Testimonials slot changed');
  const active = fragment(`voltagent-oct11-testimonials-active-${width}-reference.json`);
  if (!active.textContent.includes('What are they saying?') || active.querySelectorAll('img').length !== 62) throw new Error('Incomplete active testimonials');
  current.replaceWith(active);
  config.bodies[width] = document.body.innerHTML;
}
const corrected = original.slice(0, start) + JSON.stringify(config).replace(/</g, '\\u003c') + original.slice(end);
const backup = path.join(work, 'voltagent-oct11-pre-active-source.html');
if (!fs.existsSync(backup)) fs.writeFileSync(backup, original);
fs.writeFileSync(target, corrected);
fs.writeFileSync(path.join(work, 'voltagent-oct11-active-source-correction.json'), JSON.stringify({
  brand: 'voltagent', accepted: false, official_consistency_claim: false,
  previous_sha256: hash(original), corrected_sha256: hash(corrected), changes, unavailable_images: missing,
  actual_render_after_correction_verified: false,
  limits: ['Current public settled desktop hero and actual mounted desktop/narrow testimonials are preserved as captured phases.',
    'Source desktop body height changed from9729 to9755 when active content mounted; these are different observed phases.',
    'The Seth Rose Twitter avatar is genuinely404 in the current source and remains unavailable; no invented replacement.',
    'Marquee/diagram/reveal timing, controls and services remain unverified. Current-hash local raster proof is required.']
}, null, 2) + '\n');
console.log(JSON.stringify({brand: 'voltagent', bytes: Buffer.byteLength(corrected), sha256: hash(corrected), captured_fragments: changes.length, source_unavailable_image_occurrences: missing.length, accepted: false}));
