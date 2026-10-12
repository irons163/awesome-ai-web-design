import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {JSDOM, VirtualConsole} from 'jsdom';
const work = path.resolve('.stitch-work/current-official');
const file = path.join(work, 'miro.html');
const original = fs.readFileSync(file, 'utf8');
if (original.includes('id="miro-study-track"')) throw new Error('Correction already installed');
const start = original.indexOf('const CONFIG=') + 13;
const end = original.indexOf(';(function runtime', start);
const config = JSON.parse(original.slice(start, end));
const hash = value => crypto.createHash('sha256').update(value).digest('hex');
const manifest = JSON.parse(fs.readFileSync(path.join(work, 'miro-oct10-assets.json')));
const assets = new Map(manifest.assets.map(asset => [asset.source_url, asset]));
const activeRecord = JSON.parse(fs.readFileSync(path.join(work, 'miro-oct11-active-desktop-track-reference.json')));
const active = activeRecord.elements.find(element => element.selector === '.framer-1e4zp5x');
const activeHTML = active.htmlParts.join('');
if (activeHTML.includes('[Truncated]') || !activeHTML.endsWith('</div>') || activeRecord.viewport.width !== 1280) throw new Error('Incomplete active desktop track');
const observed = [];
for (const width of [1280, 390]) {
  const document = new JSDOM(config.bodies[width], {virtualConsole: new VirtualConsole()}).window.document;
  const hero = document.querySelector('.framer-1lut5gu');
  if (!hero?.textContent.includes('Human collaboration at the speed of AI')) throw new Error('Hero structure changed');
  observed.push({width, selector: '.framer-1lut5gu', previous_style: hero.getAttribute('style'), corrected: 'opacity:1;transform:none', basis: 'Official phase0 actual visible headline/support/email/CTA; end DOM captured offscreen exit state.'});
  hero.style.opacity = '1'; hero.style.transform = 'none';
  if (width === 1280) {
    const oldTrack = document.querySelector('.framer-1e4zp5x');
    const source = new JSDOM(activeHTML, {url: 'https://miro.com/', virtualConsole: new VirtualConsole()}).window.document;
    for (const image of source.images) {
      const asset = assets.get(image.src);
      if (!asset) throw new Error('Missing observed active source image: ' + image.src);
      image.src = asset.path; image.removeAttribute('srcset'); image.removeAttribute('sizes'); image.loading = 'eager';
    }
    source.querySelectorAll('script,iframe,link,picture source').forEach(node => node.remove());
    for (const node of source.querySelectorAll('*')) {
      for (const attribute of [...node.attributes]) if (/^on/i.test(attribute.name)) node.removeAttribute(attribute.name);
      if (node.hasAttribute('href') && !node.getAttribute('href').startsWith('#')) node.setAttribute('href', new URL(node.getAttribute('href'), 'https://miro.com/').href);
    }
    const frames = JSON.parse(fs.readFileSync(path.join(work, 'miro-oct10-official-1280-phases.json')));
    const samples = frames.filter(frame => frame.scrollY <= 4320).map(frame => {
      const heading = frame.headings.find(heading => heading.text === 'Experience the Innovation Workspace');
      return {scrollY: frame.scrollY, titleX: heading.box.x, translateX: heading.box.x + 3440};
    });
    config.studyTrack = {activeHTML: source.body.firstElementChild.outerHTML, finalHTML: oldTrack.outerHTML,
      samples, finalPhaseFrom: 4680, active_record: 'miro-oct11-active-desktop-track-reference.json'};
  }
  config.bodies[width] = document.body.innerHTML;
}
function trackRuntime() {
  let activeNode, mode, pending = false;
  function update() {
    pending = false;
    if (matchMedia('(max-width:767px)').matches) {activeNode = null; mode = null; return;}
    let node = document.querySelector('.framer-1e4zp5x');
    if (!node) return;
    const desired = scrollY < CONFIG.studyTrack.finalPhaseFrom ? 'active' : 'final';
    if (node !== activeNode || desired !== mode) {
      const template = document.createElement('template');
      template.innerHTML = CONFIG.studyTrack[desired === 'active' ? 'activeHTML' : 'finalHTML'];
      const next = template.content.firstElementChild; node.replaceWith(next);
      node = next; activeNode = next; mode = desired;
    }
    const overlay = document.querySelector('.framer-b5l8z1>.framer-1fic3hf');
    if (overlay) {overlay.style.opacity = desired === 'active' ? '0' : '1'; overlay.style.pointerEvents = desired === 'active' ? 'none' : '';}
    if (desired !== 'active') return;
    const samples = CONFIG.studyTrack.samples;
    let value = samples.at(-1).translateX;
    for (let i = 1; i < samples.length; i++) if (scrollY <= samples[i].scrollY) {
      const a = samples[i-1], b = samples[i];
      const ratio = Math.max(0, Math.min(1, (scrollY-a.scrollY)/(b.scrollY-a.scrollY)));
      value = a.translateX + (b.translateX-a.translateX)*ratio; break;
    }
    node.querySelector('.framer-xn4vzc').style.transform = `translateX(${value}px)`;
  }
  function queue() {if (!pending) {pending = true; requestAnimationFrame(update);}}
  addEventListener('scroll', queue, {passive:true}); addEventListener('resize', queue); update();
}
let corrected = original.slice(0, start) + JSON.stringify(config).replace(/</g, '\\u003c') + original.slice(end);
corrected = corrected.replace('</body>', `<script id="miro-study-track">(${trackRuntime.toString()})();</script></body>`);
const backup = path.join(work, 'miro-oct11-pre-visible-source.html');
if (!fs.existsSync(backup)) fs.writeFileSync(backup, original);
fs.writeFileSync(file, corrected);
fs.writeFileSync(path.join(work, 'miro-oct11-visible-source-correction.json'), JSON.stringify({
  accepted:false,official_consistency_claim:false,previous_sha256:hash(original),corrected_sha256:hash(corrected),hero:observed,
  active_source: {file:'miro-oct11-active-desktop-track-reference.json',observed_at:activeRecord.observed_at,scrollY:activeRecord.scrollY,html_sha256:hash(activeHTML)},
  desktop_track: {samples:config.studyTrack.samples,base_title_x:-3440,final_phase_from:4680,
    method:'Original seven observed images/six cards and captured active wrapper; translateX interpolates actual source title positions. Captured final overlay phase follows after the last observed card phase.'},
  actual_render_after_correction_verified:false,
  limits:['This projects observed scroll phases; Framer spring timing and exact between-sample transforms are unverified.',
    'The change from card track to AI platform uses a static phase boundary; source transition/motion fidelity is not claimed.',
    'Current-hash actual full desktop/narrow screenshots are required; no replacement graphics invented.']
},null,2)+'\n');
console.log(JSON.stringify({brand:'miro',bytes:Buffer.byteLength(corrected),sha256:hash(corrected),accepted:false}));
