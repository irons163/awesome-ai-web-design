import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {JSDOM, VirtualConsole} from 'jsdom';

const work = path.resolve('.stitch-work/current-official');
const target = path.join(work, 'mongodb.html');
const old = fs.readFileSync(target, 'utf8');
const start = old.indexOf('const CONFIG=') + 'const CONFIG='.length;
const end = old.indexOf(';(function runtime', start);
if (start < 13 || end < start) throw new Error('Missing MongoDB source configuration');
const config = JSON.parse(old.slice(start, end));
const url = 'https://images.contentstack.io/v3/assets/blt7151619cb9560896/blta613ba208160715f/645a458e1b8450d92ec4b0a6/compass.svg';
const manifest = JSON.parse(fs.readFileSync(path.join(work, 'mongodb-oct10-assets.json'), 'utf8'));
const asset = manifest.assets.find(a => a.source_url === url);
const sha = s => crypto.createHash('sha256').update(s).digest('hex');
if (!asset || sha(fs.readFileSync(path.join(work, asset.path))) !== asset.sha256) throw new Error('Unpreserved compass SVG');
const changes = [];
for (const width of ['1280', '390']) {
  const source = JSON.parse(fs.readFileSync(path.join(work, `mongodb-oct10-official-${width}-reference.json`), 'utf8'));
  const options = {runScripts: 'outside-only', virtualConsole: new VirtualConsole()};
  const sourceDoc = new JSDOM(source.htmlParts.join(''), options).window.document;
  const image = sourceDoc.querySelector('[data-testid="pathfinder-image-wrapper"] img');
  if (image?.getAttribute('data-src') !== url) throw new Error('Unexpected source CTA image');
  const preview = new JSDOM(config.bodies[width], options).window.document;
  const wrapper = preview.querySelector('[data-testid="pathfinder-image-wrapper"] [automation-testid="flora-SingleImage-Ratio"]');
  if (!wrapper || wrapper.children.length || wrapper.textContent) throw new Error('CTA wrapper no longer empty');
  const restored = preview.importNode(image, true);
  restored.src = asset.path;
  restored.loading = 'eager';
  restored.classList.remove('lazyload');
  restored.removeAttribute('data-src');
  restored.removeAttribute('data-sizes');
  wrapper.append(restored);
  config.bodies[width] = preview.body.innerHTML;
  changes.push({width: Number(width), restored_source_image: url,
    local_asset: asset, source_markup: image.outerHTML, corrected_markup: restored.outerHTML,
    original_responsive_wrapper_preserved: true});
}
const corrected = old.slice(0, start) + JSON.stringify(config).replace(/</g, '\u003c') + old.slice(end);
const backup = path.join(work, 'mongodb-oct10-pre-cta-image-fix.html');
if (!fs.existsSync(backup)) fs.writeFileSync(backup, old);
fs.writeFileSync(target, corrected);
fs.writeFileSync(path.join(work, 'mongodb-oct10-cta-image-correction.json'), JSON.stringify({
  brand: 'mongodb', accepted: false, previous_sha256: sha(old), corrected_sha256: sha(corrected),
  reason: 'Actual official desktop lower-page raster shows this original compass illustration, but the preview had removed it because the initial top-of-page currentSrc was empty. Restore the observed source data-src asset; keep original hidden narrow wrapper.',
  changes, actual_render_after_correction_verified: false,
  remaining: ['Fresh desktop and390px narrow screenshots bound to corrected hash.', 'Announcement/customer/marquee phases and interactions remain unverified.']
}, null, 2) + '\n');
console.log(JSON.stringify({brand: 'mongodb', sha256: sha(corrected), changes: changes.length, accepted: false}));
