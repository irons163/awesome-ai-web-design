import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {JSDOM,VirtualConsole} from 'jsdom';

const capture = path.resolve(process.argv[2] || '/private/tmp/official-browser-oct9');
const output = path.resolve('.stitch-work/current-official');
const hash = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const chunks = text => text.match(/[\s\S]{1,60000}/g) || [];
const read = name => JSON.parse(fs.readFileSync(path.join(capture, name), 'utf8'));

function sanitize(html) {
  // JavaScript is enabled in the reference browser. Removing inert noscript
  // blocks before parsing avoids JSDOM relocating their head content to body.
  html = html.replace(/<noscript\b[^>]*>[\s\S]*?<\/noscript\s*>/gi,'');
  const dom = new JSDOM(html,{virtualConsole:new VirtualConsole()});
  const document = dom.window.document;
  document.querySelectorAll('script,iframe,object,embed,template,input[type="hidden"],[id^="codex-browser-"]').forEach(node => node.remove());
  document.querySelectorAll('input,textarea').forEach(node => {
    node.removeAttribute('value');
    if (node.tagName === 'TEXTAREA') node.textContent = '';
  });
  document.querySelectorAll('*').forEach(node => [...node.attributes].forEach(attribute => {
    if (/^on|nonce|token|csrf/i.test(attribute.name)) node.removeAttribute(attribute.name);
  }));
  const walker = document.createTreeWalker(document, 128);
  const comments = [];
  while (walker.nextNode()) comments.push(walker.currentNode);
  comments.forEach(node => node.remove());
  return dom.serialize();
}

function retainAsset(brand, asset, method) {
  const bytes = fs.readFileSync(asset.path);
  const sha256 = hash(bytes);
  const extension = path.extname(asset.path) || path.extname(new URL(asset.url).pathname) || '.bin';
  const relative = `${brand}-assets/${hash(asset.url).slice(0, 16)}-${sha256.slice(0, 8)}${extension}`;
  const destination = path.join(output, relative);
  if (fs.existsSync(destination)) {
    if (hash(fs.readFileSync(destination)) !== sha256) throw new Error('Original asset collision');
  } else {
    fs.copyFileSync(asset.path, destination);
  }
  return {source_url:asset.url,kind:asset.kind,content_type:asset.contentType,
    path:relative,bytes:bytes.length,sha256,retained:true,method};
}

for (const brand of ['vodafone', 'pinterest']) {
  fs.mkdirSync(path.join(output, `${brand}-assets`), {recursive:true});
  const references = {};
  for (const [variant, width] of [['desktop',1280],['mobile',390]]) {
    const raw = read(`${brand}-${variant}-complete-raw-private.json`);
    const html = raw.htmlParts.join('');
    if (html.length !== raw.htmlLength || raw.viewport.width !== width || raw.bodyHeight < 1500) {
      throw new Error(`${brand}/${variant}: incomplete or wrong-viewport capture`);
    }
    for (const sheet of raw.stylesheets) {
      if (sheet.parts && sheet.parts.join('').length !== sheet.textLength) throw new Error('Incomplete CSS capture');
    }
    const cleaned = sanitize(html);
    const dom = new JSDOM(cleaned,{virtualConsole:new VirtualConsole()});
    const marker = brand === 'vodafone' ? 'EVERYONE.' : 'Conjure your best Halloween';
    if (!dom.window.document.body.textContent.includes(marker)) throw new Error('Missing observed public homepage');
    raw.htmlParts = chunks(cleaned);
    raw.htmlLength = cleaned.length;
    raw.html_sha256 = hash(cleaned);
    raw.method = 'Complete rendered public DOM/CSS serialization, split before transport and sanitized offline. This is not an original HTTP response or proof of visual acceptance.';
    raw.sanitization = 'Scripts, inert noscript blocks, frames, embedded objects, templates, browser-tool overlay roots, comments, hidden inputs, entered field values, inline events and nonce/CSRF/token attributes excluded. No cookies, browser storage or private account APIs were read.';
    if (brand === 'pinterest' && variant === 'mobile') raw.viewport_limit = '390×844 narrow viewport in the existing browser, not a mobile user-agent emulation. The observed public page has bodyWidth800; do not invent a different mobile layout from this capture.';
    const filename = `${brand}-${variant}-browser-reference.json`;
    fs.writeFileSync(path.join(output, filename), JSON.stringify(raw,null,2)+'\n');
    references[variant] = {file:filename,observed_at:raw.observed_at,viewport:raw.viewport,
      bodyHeight:raw.bodyHeight,bodyWidth:raw.bodyWidth,html_sha256:raw.html_sha256};
  }
  const bundle = read(`${brand}-browser-asset-bundle.json`);
  const assets = bundle.assets.map(asset => retainAsset(brand,asset,'Native pageAssets bundle; original file bytes retained unchanged.'));
  if (brand === 'pinterest') {
    const record = JSON.parse(fs.readFileSync(path.join(output,references.desktop.file),'utf8'));
    const css = record.stylesheets.filter(sheet=>sheet.parts).map(sheet=>sheet.parts.join('')).join('\n');
    const urls = [...new Set([...css.matchAll(/https:\/\/s\.pinimg\.com\/[^"'\s)]+\.woff2/g)].map(match=>match[0]))];
    if (urls.length !== 4) throw new Error(`Expected four observed Pin Sans files; found${urls.length}`);
    for (const [index,url] of urls.entries()) {
      const temporary = path.join(capture,`pinterest-font-${index}.woff2`);
      execFileSync('curl',['--fail','--silent','--show-error','--compressed','--location','--max-time','60',url,'--output',temporary]);
      if (fs.readFileSync(temporary).subarray(0,4).toString() !== 'wOF2') throw new Error('Invalid original font');
      assets.push(retainAsset(brand,{url,path:temporary,kind:'font',contentType:'font/woff2'},'Observed font-face URL; ordinary unauthenticated HTTPS200; HTTP content encoding decoded by curl; original decoded body bytes and WOFF2 signature checked.'));
    }
  }
  const provenance = {reference_url:references.desktop.file,observed_at:references.desktop.observed_at,
    method:'Native browser asset bundle, with explicit supplementary observed Pin Sans font downloads. No original asset was redrawn or resized.',
    assets,failures:bundle.failures,summary:bundle.summary};
  fs.writeFileSync(path.join(output,`${brand}-browser-asset-provenance.json`),JSON.stringify(provenance,null,2)+'\n');
  const screenshots = [];
  for (const variant of ['desktop','mobile']) for (const frame of ['first','full']) {
    const name = `${brand}-${variant}-${frame}.jpg`;
    const source = path.join(capture,name);
    if (!fs.existsSync(source)) continue;
    const bytes = fs.readFileSync(source);
    if (bytes[0] !== 0xff || bytes[1] !== 0xd8) throw new Error('Expected unmodified browser JPEG');
    fs.copyFileSync(source,path.join(output,name));
    screenshots.push({path:name,bytes:bytes.length,sha256:hash(bytes),method:'Unmodified browser screenshot; video frames and animated/lazy sections may differ by capture time.'});
  }
  fs.writeFileSync(path.join(output,`${brand}-reference.json`),JSON.stringify({reference_url:brand==='vodafone'?'https://www.vodafone.com/':'https://www.pinterest.com/',
    accepted:false,references,screenshots,asset_provenance:`${brand}-browser-asset-provenance.json`,
    scope:'Dated public desktop and narrow-viewport source references only. Local draft and live public deployment still require separate comparison.'},null,2)+'\n');
  console.log(JSON.stringify({brand,references,assets:assets.length,assetBytes:assets.reduce((sum,a)=>sum+a.bytes,0),failures:bundle.failures.length}));
}
