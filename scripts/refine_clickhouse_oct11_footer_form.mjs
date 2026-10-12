// Restore the observed public form appearance without tracking or submission.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {JSDOM, VirtualConsole} from 'jsdom';
const work = path.resolve('.stitch-work/current-official');
const file = path.join(work, 'clickhouse.html');
const original = fs.readFileSync(file, 'utf8');
const hash = b => crypto.createHash('sha256').update(b).digest('hex');
const start = original.indexOf('const CONFIG=') + 13;
const end = original.indexOf(';(function runtime', start);
if (start < 13 || end < start) throw new Error('Unexpected draft structure');
const config = JSON.parse(original.slice(start, end));
const reference = JSON.parse(fs.readFileSync(path.join(work, 'clickhouse-oct11-footer-form-reference.json')));
const manifest = JSON.parse(fs.readFileSync(path.join(work, 'clickhouse-oct10-assets.json')));
const assets = new Map(manifest.assets.map(a => [a.source_url, a]));
const source = new JSDOM(reference.htmlParts.join(''), {url:reference.url, virtualConsole:new VirtualConsole()}).window.document;
const computed = JSON.parse(fs.readFileSync(path.join(work, 'clickhouse-oct11-footer-form-computed-styles.json')));
if (source.querySelector('input[type="email"]')?.placeholder !== 'Email address' ||
    source.querySelector('button')?.textContent.trim() !== 'Sign up') throw new Error('Observed form structure changed');
function css(text, base) {
  return text.replace(/url\(\s*(['"]?)(.*?)\1\s*\)/g, (_,q,value) => {
    if (/^(data:|#)/.test(value)) return `url("${value}")`;
    const url = new URL(value,base).href;
    const asset = assets.get(url);
    if (!asset) throw new Error('Unpreserved exact form asset: '+url);
    return `url("${asset.path}")`;
  });
}
// One optional form CSS URL returned a genuine HTTP 403. Do not retry it or
// fetch it through another channel. The already-visible computed values and
// preserved Latin Inter declaration provide a disclosed static study.
const fontCSS = (original.slice(0,original.indexOf('</head>')).match(/@font-face\s*\{[^{}]*\}/g)||[])
  .filter(rule=>/font-family:Inter;/.test(rule) && /unicode-range:U\+\?\?/.test(rule)).join('\n');
if (!fontCSS) throw new Error('Previously observed official Latin Inter declaration required');
source.head.innerHTML = '';
const fontStyle = source.createElement('style');fontStyle.textContent = fontCSS;
source.head.append(fontStyle);
source.querySelectorAll('script,iframe,link,meta,base,input[type="hidden"],[id^="codex-browser-"]').forEach(e=>e.remove());
const form = source.querySelector('form');
for (const child of [...form.children]) if (!child.querySelector('input[type="email"],button')) child.remove();
for (const node of [source.body,...source.body.querySelectorAll('*')]) {
  const match = computed.nodes.find(n=>n.tag===node.tagName && n.id===node.id && n.cls===node.className);
  if (!match) throw new Error('Missing observed rendered style for '+node.tagName+'.'+node.className);
  for (const [property,value] of Object.entries(match.style)) node.style.setProperty(property,value);
  if (node.tagName!=='BUTTON' && !node.classList.contains('mktoButtonRow') && !node.classList.contains('mktoButtonWrap')) node.style.width='100%';
}
const row = form.querySelector('.mktoFormRow');row.style.flex='1 1 0';row.style.minWidth='0';row.style.width='auto';row.style.alignSelf='center';
form.querySelector('.mktoButtonRow').style.flex='0 0 auto';
for (const node of source.querySelectorAll('*')) {
  for (const a of [...node.attributes]) if (/^on/i.test(a.name) || /^data-/i.test(a.name)) node.removeAttribute(a.name);
}
source.querySelectorAll('form').forEach(e=>{e.removeAttribute('action');e.removeAttribute('method');});
source.querySelectorAll('input').forEach(e=>{e.value='';e.removeAttribute('name');});
source.querySelectorAll('button').forEach(e=>{e.type='button';e.removeAttribute('name');});
const frameHTML = '<!doctype html>'+source.documentElement.outerHTML;
const changes = [];
for (const width of [1280,390]) {
  const doc = new JSDOM(config.bodies[width],{virtualConsole:new VirtualConsole()}).window.document;
  const paragraph = [...doc.querySelectorAll('p')].find(e=>e.textContent.startsWith('Stay informed on feature releases'));
  if (!paragraph) throw new Error('Observed newsletter parent missing');
  const parent = paragraph.parentElement;
  if (parent.parentElement.querySelector('iframe')) throw new Error('Form already restored');
  const frame = doc.createElement('iframe');
  frame.title = 'Newsletter email form — visual study';
  frame.height='50';frame.setAttribute('scrolling','no');frame.setAttribute('sandbox','');
  frame.className='w-full bg-transparent! transition-opacity opacity-100';
  frame.setAttribute('srcdoc',frameHTML);
  parent.after(frame);
  changes.push({width,height:50,method:'Sanitized actual public iframe DOM, original external Latin Inter declaration and observed computed styles; no hidden fields, tracking scripts or submission.'});
  config.bodies[width]=doc.body.innerHTML;
}
const corrected=original.slice(0,start)+JSON.stringify(config).replace(/</g,'\\u003c')+original.slice(end);
const backup=path.join(work,'clickhouse-oct11-pre-footer-form.html');
if(!fs.existsSync(backup))fs.writeFileSync(backup,original);
fs.writeFileSync(file,corrected);
fs.writeFileSync(path.join(work,'clickhouse-oct11-footer-form-correction.json'),JSON.stringify({
  accepted:false,official_consistency_claim:false,previous_sha256:hash(original),corrected_sha256:hash(corrected),
  frame_reference:'clickhouse-oct11-footer-form-reference.json',frame_observed_at:reference.observed_at,
  computed_style_reference:'clickhouse-oct11-footer-form-computed-styles.json',
  unavailable_stylesheet:reference.styles[0],unavailable_reason:'Ordinary request returned HTTP 403; no retry or alternate download route.',
  public_frame_sha256:hash(frameHTML),changes,actual_render_after_correction_verified:false,
  limits:['Newsletter submission, validation and backend are not implemented or verified.','Static form styles use observed computed values because one external CSS file returned HTTP 403; complete source CSS fidelity is not claimed.','Latin Inter remains an original external font URL, as in the surrounding study. A separate Cyrillic subset returned HTTP 403 and is not used by this English form; it was not retried. Offline font fidelity is unverified.','Actual desktop/narrow raster QA required after correction.']
},null,2)+'\n');
console.log(JSON.stringify({brand:'clickhouse',bytes:Buffer.byteLength(corrected),sha256:hash(corrected),accepted:false}));
