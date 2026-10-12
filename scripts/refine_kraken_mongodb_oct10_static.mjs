import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {JSDOM, VirtualConsole} from 'jsdom';

const root = path.resolve('.stitch-work/current-official');
const sha = text => crypto.createHash('sha256').update(text).digest('hex');
for (const brand of ['mongodb', 'kraken']) {
  const target = path.join(root, `${brand}.html`);
  const original = fs.readFileSync(target, 'utf8');
  const start = original.indexOf('const CONFIG=') + 'const CONFIG='.length;
  const end = original.indexOf(';(function runtime', start);
  if (start < 13 || end < start) throw new Error(`Missing source configuration: ${brand}`);
  const config = JSON.parse(original.slice(start, end));
  const changes = [];
  for (const width of ['1280', '390']) {
    const document = new JSDOM(config.bodies[width], {
      runScripts: 'outside-only', virtualConsole: new VirtualConsole(),
    }).window.document;
    const nodes = brand === 'mongodb'
      ? [...document.querySelectorAll('[data-testid="use-case-carousel"]')]
      : [...document.querySelectorAll('[style]')].filter(e =>
        e.style.getPropertyValue('--opacity-start') && e.style.getPropertyValue('--opacity-end'));
    for (const node of nodes) {
      const before = node.getAttribute('style');
      if (brand === 'mongodb') {
        node.style.opacity = '1';
        node.style.visibility = 'visible';
      } else {
        node.style.setProperty('--opacity-start', node.style.getPropertyValue('--opacity-end'));
        if (node.style.getPropertyValue('--transform-end')) {
          node.style.setProperty('--transform-start', node.style.getPropertyValue('--transform-end'));
        }
      }
      changes.push({width: Number(width), selector: brand === 'mongodb'
        ? '[data-testid="use-case-carousel"]' : '[style*="--opacity-start"]',
      text: node.textContent.replace(/\s+/g, ' ').trim().slice(0, 150), before,
      after: node.getAttribute('style')});
    }
    config.bodies[width] = document.body.innerHTML;
  }
  const corrected = original.slice(0, start) + JSON.stringify(config).replace(/</g, '\\u003c') + original.slice(end);
  const backup = path.join(root, `${brand}-oct10-pre-static-reveal.html`);
  if (!fs.existsSync(backup)) fs.writeFileSync(backup, original);
  fs.writeFileSync(target, corrected);
  const record = {brand, accepted: false,
    reason: 'Actual official/local screenshot comparison found source scroll-reveal content frozen in its hidden initial state.',
    method: 'Preserve the observed original content/assets and show the recorded final visibility/transform phase without running official scripts.',
    previous_sha256: sha(original), corrected_sha256: sha(corrected), changes,
    actual_render_after_correction_verified: false,
    remaining: ['Fresh actual desktop and 390px narrow screenshots of this corrected hash.', 'Carousel/reveal animation timing and interactive state parity are not implemented.']};
  fs.writeFileSync(path.join(root, `${brand}-oct10-static-reveal-correction.json`), JSON.stringify(record, null, 2) + '\n');
  console.log(JSON.stringify({brand, changes: changes.length, sha256: sha(corrected), accepted: false}));
}
