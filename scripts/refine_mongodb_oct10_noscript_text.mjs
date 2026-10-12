import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const work = path.resolve('.stitch-work/current-official');
const target = path.join(work, 'mongodb.html');
const old = fs.readFileSync(target, 'utf8');
const start = old.indexOf('const CONFIG=') + 'const CONFIG='.length;
const end = old.indexOf(';(function runtime', start);
if (start < 13 || end < start) throw new Error('Missing MongoDB source configuration');
const config = JSON.parse(old.slice(start, end));
const artefact = '&lt;link rel="stylesheet" href="/_next/static/css/bb04bb8d5f3688d2.css"&gt;';
const changes = [];
for (const width of ['1280', '390']) {
  if (!config.bodies[width].startsWith(artefact + '<div id="__next">')) {
    throw new Error(`Unexpected MongoDB leading body, ${width}; do not strip arbitrary text`);
  }
  config.bodies[width] = config.bodies[width].slice(artefact.length);
  changes.push({width: Number(width), removed_leading_text: artefact,
    reason: 'Retained official HTML places this escaped text inside a head noscript node. Actual official raster has no visible row. Earlier parse displaced the text into the preview body.'});
}
const corrected = old.slice(0, start) + JSON.stringify(config).replace(/</g, '\u003c') + old.slice(end);
const sha = s => crypto.createHash('sha256').update(s).digest('hex');
const backup = path.join(work, 'mongodb-oct10-pre-noscript-text-fix.html');
if (!fs.existsSync(backup)) fs.writeFileSync(backup, old);
fs.writeFileSync(target, corrected);
fs.writeFileSync(path.join(work, 'mongodb-oct10-noscript-text-correction.json'), JSON.stringify({
  brand: 'mongodb', accepted: false, previous_sha256: sha(old), corrected_sha256: sha(corrected),
  source_reference: ['mongodb-oct10-official-1280-reference.json', 'mongodb-oct10-official-390-reference.json'],
  defect_evidence: ['mongodb-oct10-local-1280-phase-0.png', 'mongodb-oct10-local-390-phase-0.png'],
  changes, actual_render_after_correction_verified: false,
  remaining: ['Fresh browser desktop/narrow screenshots bound to this corrected hash.', 'Carousel and announcement timing, navigation and service states are unverified.']
}, null, 2) + '\n');
console.log(JSON.stringify({brand: 'mongodb', sha256: sha(corrected), changes: changes.length, accepted: false}));
