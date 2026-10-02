// Extract the observed public renderer module; omit the site's analytics runtime.
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import crypto from 'node:crypto';

const root = path.resolve('.stitch-work/current-official');
const input = path.join(root, 'x.ai-source-scripts/29wm_eob9hm2m.js');
const chunks = [];
// The isolated context only records factories. It has no I/O or browser handles.
vm.runInNewContext(fs.readFileSync(input, 'utf8'), {
  TURBOPACK: { push: chunk => chunks.push(chunk) },
}, { timeout: 1000 });
const factory = chunks.flat().find(item =>
  typeof item === 'function' && item.toString().includes('"OrbRenderer"'));
if (!factory) throw new Error('The observed renderer module was not found');
let body = factory.toString();
body = body.replace(/try\{var t=window;[\s\S]*?\}catch\(e\)\{\}/, '');
if (/e\.(?:i|r|A)\(/.test(body)) throw new Error('Renderer has an unexpected runtime dependency');
const output = `// Derived from the observed x.ai public AgentOrb renderer, 2026-10-03.\n` +
  `// Original GLSL, geometry, and animation math are retained.\n` +
  `const officialOrb = (() => {\nconst exports = {};\n` +
  `(${body})({s(entries){for(let i=0;i<entries.length;i+=3)exports[entries[i]]=entries[i+2];}});\n` +
  `return exports;\n})();\n`;
const target = path.join(root, 'x.ai-assets/official-orb-core.js');
fs.writeFileSync(target, output);
const digest = p => crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const provenance = {
  source_url: 'https://x.ai/_next/static/chunks/29wm_eob9hm2m.js?dpl=7bfd379b826e3fd331eb998b1be06368dfaa2e5c',
  source_path: 'x.ai-source-scripts/29wm_eob9hm2m.js',
  source_sha256: digest(input),
  derived_path: 'x.ai-assets/official-orb-core.js',
  derived_sha256: digest(target),
  changes: ['Extract renderer factory 870084', 'Remove Sentry metadata setup', 'Expose renderer without React, Workers, or Turbopack'],
  voice_parameters_source: 'x.ai-source-scripts/272cyek9z3xog.js',
};
fs.writeFileSync(path.join(root, 'x.ai-orb-provenance.json'), JSON.stringify(provenance, null, 2) + '\n');
console.log('Extracted official x.ai orb core:', fs.statSync(target).size, 'bytes');
