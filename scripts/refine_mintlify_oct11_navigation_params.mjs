import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {JSDOM, VirtualConsole} from 'jsdom';
const work = path.resolve('.stitch-work/current-official');
const target = path.join(work, 'mintlify.html');
const original = fs.readFileSync(target, 'utf8');
const start = original.indexOf('const CONFIG=') + 13;
const end = original.indexOf(';(function runtime', start);
const config = JSON.parse(original.slice(start, end));
const changes = [];
for (const width of [1280, 390]) {
  const document = new JSDOM(config.bodies[width], {virtualConsole: new VirtualConsole()}).window.document;
  for (const node of document.querySelectorAll('a[href]')) {
    const prior = node.getAttribute('href');
    if (!prior.startsWith('https://')) continue;
    const url = new URL(prior), removed = [...url.searchParams.keys()].filter(key => key === 'ajs_aid' || key === '_gl' || key.startsWith('utm_'));
    if (!removed.length) continue;
    removed.forEach(key => url.searchParams.delete(key));
    node.setAttribute('href', url.href);
    changes.push({width, text: node.textContent.trim(), original_url: prior, corrected_url: url.href, removed_keys: removed});
  }
  config.bodies[width] = document.body.innerHTML;
}
const corrected = original.slice(0, start) + JSON.stringify(config).replace(/</g, '\\u003c') + original.slice(end);
fs.writeFileSync(target, corrected);
const hash = value => crypto.createHash('sha256').update(value).digest('hex');
fs.writeFileSync(path.join(work, 'mintlify-oct11-navigation-correction.json'), JSON.stringify({
  accepted: false, official_consistency_claim: false, previous_sha256: hash(original), corrected_sha256: hash(corrected),
  changes, rule: 'Remove only actually observed ajs_aid/_gl/utm_* navigation query parameters. No destination/path or original bitmap changes.',
  actual_render_after_correction_verified: false
}, null, 2) + '\n');
console.log(JSON.stringify({brand:'mintlify',bytes:Buffer.byteLength(corrected),sha256:hash(corrected),navigation_changes:changes.length}));
