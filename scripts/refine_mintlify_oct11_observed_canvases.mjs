import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {JSDOM, VirtualConsole} from 'jsdom';

const work = path.resolve('.stitch-work/current-official');
const target = path.join(work, 'mintlify.html');
const original = fs.readFileSync(target, 'utf8');
const start = original.indexOf('const CONFIG=') + 'const CONFIG='.length;
const end = original.indexOf(';(function runtime', start);
if (start < 13 || end < start) throw new Error('Missing source-corrected templates');
const config = JSON.parse(original.slice(start, end));
const hash = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const changes = [];
const observed = [];
for (const width of [1280, 390]) {
  const records = JSON.parse(fs.readFileSync(path.join(work, `mintlify-oct11-observed-canvases-${width}.json`), 'utf8'));
  const indices = records.map(record => record.index).sort((a, b) => a - b);
  if (JSON.stringify(indices) !== JSON.stringify([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 13, 14])) throw new Error('Expected13 observed canvases, not all15');
  const doc = new JSDOM(config.bodies[width], {virtualConsole: new VirtualConsole()}).window.document;
  const canvases = [...doc.querySelectorAll('canvas')];
  if (canvases.length !== 15) throw new Error('Canvas structure changed');
  for (const record of records) {
    if (record.error || record.url !== 'https://www.mintlify.com/') throw new Error('Unusable source bitmap');
    const bytes = fs.readFileSync(path.join(work, record.path));
    if (bytes.length !== record.bytes || hash(bytes) !== record.sha256) throw new Error('Changed original observed bitmap');
    // Body child indices changed when official scripts were excluded. The
    // stable main/footer subtree and original canvas index must both agree.
    const anchor = record.selector.match(/>(main|footer):nth-child\(\d+\)>(.*)$/);
    if (!anchor) throw new Error('Unexpected captured selector');
    const selector = `${anchor[1]}>${anchor[2]}`;
    const node = doc.querySelector(selector);
    if (node !== canvases[record.index]) throw new Error('Observed bitmap mapped to a different canvas');
    const priorStyle = node.getAttribute('style');
    // Display original read-only captured pixels on the original canvas box.
    // Retaining the element preserves source tag selectors and sizing rules.
    node.style.backgroundImage = `url("${record.path}")`;
    node.style.backgroundSize = '100% 100%';
    node.style.backgroundPosition = 'center';
    node.style.backgroundRepeat = 'no-repeat';
    node.setAttribute('data-study-static-canvas', String(record.index));
    changes.push({width, index: record.index, source_selector: record.selector, local_selector: selector,
      path: record.path, sha256: record.sha256, original_inline_style: priorStyle,
      method: 'Original actual public canvas pixels displayed as a static CSS background on the original canvas element; source dimensions/class/style retained.'});
    observed.push({...record, previous_attempts: undefined});
  }
  config.bodies[width] = doc.body.innerHTML;
}
const corrected = original.slice(0, start) + JSON.stringify(config).replace(/</g, '\\u003c') + original.slice(end);
const backup = path.join(work, 'mintlify-oct11-pre-observed-canvases.html');
if (!fs.existsSync(backup)) fs.writeFileSync(backup, original);
fs.writeFileSync(target, corrected);
fs.writeFileSync(path.join(work, 'mintlify-oct11-static-canvas-correction.json'), JSON.stringify({
  brand: 'mintlify', accepted: false, official_consistency_claim: false,
  previous_sha256: hash(original), corrected_sha256: hash(corrected),
  source_records: [1280, 390].map(width => `mintlify-oct11-observed-canvases-${width}.json`),
  observed_count_per_width: 13, total_canvas_slots_per_width: 15,
  unseen_horizontal_card_indices: [10, 11], changes, observed,
  actual_render_after_correction_verified: false,
  limits: ['These26 saved actual bitmap phases do not recreate live canvas motion or synchronized phases.',
    'Canvas slots10/11 were not visible in the captured horizontal customer cards; no pixels invented and they remain unverified.',
    'Current-hash desktop/narrow actual full-page screenshots and raster review are still required.']
}, null, 2) + '\n');
console.log(JSON.stringify({brand: 'mintlify', bytes: Buffer.byteLength(corrected), sha256: hash(corrected), static_bitmaps: changes.length, accepted: false}));
