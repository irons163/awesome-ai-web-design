import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {JSDOM, VirtualConsole} from 'jsdom';

const capture = path.resolve(process.argv[2] || '/private/tmp/official-browser-claude-notion-oct10');
const work = path.resolve('.stitch-work/current-official');
const hash = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const read = name => JSON.parse(fs.readFileSync(path.join(capture, name), 'utf8'));
const write = (name, value) => fs.writeFileSync(path.join(work, name), JSON.stringify(value, null, 2) + '\n');
const parse = html => new JSDOM(html, {virtualConsole: new VirtualConsole()}).window.document;
const visualURL = value => /^(data:image\/|https:\/\/(?:[^/]*\.)?(?:website-files\.com|notion\.com|ctfassets\.net|anthropic\.com|claude\.com|jsdelivr\.net|googleapis\.com|gstatic\.com)\/)/i.test(value);

function sanitize(html) {
  const document = parse(html.replace(/<noscript\b[^>]*>[\s\S]*?<\/noscript\s*>/gi, ''));
  document.querySelectorAll('script,iframe,object,embed,template,input[type="hidden"],[id^="codex-browser-"]').forEach(e => e.remove());
  document.querySelectorAll('link[as="script"],link[as="fetch"],link[rel="prefetch"],meta[http-equiv="refresh"]').forEach(e => e.remove());
  document.querySelectorAll('input,textarea').forEach(e => {e.removeAttribute('value'); if(e.tagName === 'TEXTAREA') e.textContent = '';});
  document.querySelectorAll('img[src]').forEach(e => {if (!visualURL(new URL(e.getAttribute('src'), 'https://www.notion.com/').href)) e.remove();});
  document.querySelectorAll('*').forEach(e => [...e.attributes].forEach(a => {
    if (/^on|nonce|token|csrf/i.test(a.name)) e.removeAttribute(a.name);
    if (a.name === 'href' && /[?&](tid|gclid|fbclid|li_fat_id)=/.test(a.value)) {
      const url = new URL(a.value, 'https://www.notion.com/');
      for(const key of ['tid','gclid','fbclid','li_fat_id']) url.searchParams.delete(key);
      e.setAttribute(a.name, url.href);
    }
  }));
  const walker = document.createTreeWalker(document, 128), comments = [];
  while(walker.nextNode()) comments.push(walker.currentNode);
  comments.forEach(e => e.remove());
  return '<!doctype html>' + document.documentElement.outerHTML;
}

for(const brand of ['claude','notion']) {
  fs.mkdirSync(path.join(work, brand + '-assets'), {recursive:true});
  const references = {}, required = new Map(), assets = [], failures = [];
  for(const variant of ['desktop','mobile']) {
    const raw = read(`${brand}-${variant}-complete-raw-private.json`);
    const original = raw.htmlParts.join('');
    if(original.length !== raw.htmlLength || raw.viewport.width !== (variant === 'desktop' ? 1280 : 390)) throw new Error('Incomplete capture: ' + brand + '/' + variant);
    for(const sheet of raw.stylesheets) if(sheet.parts && sheet.parts.join('').length !== sheet.textLength) throw new Error('Incomplete CSSOM');
    const html = sanitize(original), document = parse(html);
    const marker = brand === 'claude' ? 'Think fast' : 'Where teams and agents';
    if(!document.body.textContent.includes(marker)) throw new Error('Wrong public page');
    const add = (value, kind) => {if(value && visualURL(value) && !value.startsWith('data:')) required.set(value,kind);};
    for(const link of document.querySelectorAll('link[rel="stylesheet"][href]')) add(new URL(link.getAttribute('href'),raw.reference_url).href,'stylesheet');
    for(const link of document.querySelectorAll('link[as="font"][href]')) add(new URL(link.getAttribute('href'),raw.reference_url).href,'font');
    for(const image of raw.images) add(image.src,'image');
    raw.images = raw.images.filter(image=>visualURL(image.src));
    for(const video of raw.videos) for(const url of video.sources) add(url,'video');
    raw.htmlParts = html.match(/[\s\S]{1,50000}/g) || [];
    raw.htmlLength = html.length; raw.html_sha256 = hash(html);
    raw.links = raw.links.map(link => {const url = new URL(link.href,raw.reference_url); for(const key of ['tid','gclid','fbclid','li_fat_id']) url.searchParams.delete(key); return {...link,href:url.href};});
    raw.controls = raw.controls.map(control => ({...control,html:sanitize('<body>' + control.html + '</body>').replace(/^.*?<body[^>]*>|<\/body>.*$/gs,'')}));
    raw.method = 'Dated rendered public DOM/CSS and original screenshots, with desktop user agent at both viewport sizes. Scripts, frames, comments, entered values, token attributes and telemetry images excluded offline. No cookies, storage or private account APIs were read.';
    raw.limitations = brand === 'claude' ? ['Root homepage redirected to Claude login in this browser. The search-discovered official /index.html marketing page is the actual captured reference.','The official hero video had an empty src and readyState 0 at both sizes; no replacement video was invented.'] : ['Rotating hero wording, logo marquee and video frame are time dependent; the captures preserve dated states.'];
    const file = `${brand}-${variant}-browser-reference.json`; write(file,raw);
    references[variant] = {file,observed_at:raw.observed_at,viewport:raw.viewport,html_sha256:raw.html_sha256,bodyHeight:raw.bodyHeight,bodyWidth:raw.bodyWidth};
  }
  function retain(asset,method) {
    if(assets.some(a=>a.source_url === asset.url)) return;
    const bytes = fs.readFileSync(asset.path), sha256 = hash(bytes);
    const extension = path.extname(asset.path) || (asset.kind === 'stylesheet' ? '.css' : '.bin');
    const relative = `${brand}-assets/${hash(asset.url).slice(0,16)}-${sha256.slice(0,8)}${extension}`;
    if(fs.existsSync(path.join(work,relative)) && hash(fs.readFileSync(path.join(work,relative))) !== sha256) throw new Error('Asset collision');
    fs.copyFileSync(asset.path,path.join(work,relative));
    assets.push({source_url:asset.url,path:relative,kind:asset.kind,content_type:asset.contentType,bytes:bytes.length,sha256,method});
  }
  const nativeSummaries = [];
  let omittedTelemetryFailures = 0;
  for(const variant of ['desktop','mobile']) {
    const bundle = read(`${brand}-${variant}-asset-bundle.json`);
    for(const asset of read(`${brand}-${variant}-asset-inventory.json`).assets) {
      if(asset.kind === 'font' && visualURL(asset.url)) required.set(asset.url,'font');
    }
    nativeSummaries.push({variant,...bundle.summary});
    for(const asset of bundle.assets) if(visualURL(asset.url) && !asset.url.startsWith('data:')) retain(asset,'Native pageAssets bundle; original bytes unchanged.');
    for(const failure of bundle.failures) {
      if(visualURL(failure.url)) failures.push({...failure,reason:failure.reason.slice(0,1000)});
      else omittedTelemetryFailures++;
    }
  }
  for(const [url,kind] of required) {
    if(assets.some(a=>a.source_url === url)) continue;
    const extension = {stylesheet:'.css',font:'.woff2',video:'.mp4',image:'.bin'}[kind];
    const temporary = path.join(capture,brand + '-original-' + hash(url).slice(0,16) + extension);
    try {
      const previous = brand === 'notion' ? JSON.parse(fs.readFileSync(path.join(work,'notion-asset-provenance.json'))) : {};
      const cached = Object.entries(previous).find(([name,source])=>source === url && fs.existsSync(path.join(work,'notion-assets',name)));
      if(cached) {
        retain({url,path:path.join(work,'notion-assets',cached[0]),kind,contentType:null},'Current public URL matches the previously retained original asset URL exactly; original bytes reused, current native acquisition failure retained separately.');
        continue;
      }
      const partial = temporary + '.partial';
      if(!fs.existsSync(temporary)) {
        execFileSync('curl',['--fail','--silent','--show-error','--compressed','--location','--max-time','45',url,'--output',partial]);
        fs.renameSync(partial,temporary);
      }
      const bytes = fs.readFileSync(temporary);
      if(kind === 'font' && bytes.subarray(0,4).toString() !== 'wOF2') throw new Error('Invalid WOFF2');
      if(kind === 'video' && bytes.subarray(4,8).toString() !== 'ftyp') throw new Error('Invalid MP4');
      if(kind === 'stylesheet' && /^\s*</.test(bytes.toString())) throw new Error('HTML instead of CSS');
      let file = temporary;
      if(kind === 'image') {
        const ext = bytes[0] === 255 && bytes[1] === 216 ? '.jpg' : bytes.subarray(1,4).toString() === 'PNG' ? '.png' : bytes.subarray(0,4).toString() === 'RIFF' ? '.webp' : /<svg[\s>]/i.test(bytes.subarray(0,1000).toString()) ? '.svg' : null;
        if(!ext) throw new Error('Unsupported image signature'); file += ext; fs.copyFileSync(temporary,file);
      }
      retain({url,path:file,kind,contentType:null},'Observed public visual URL; unauthenticated HTTPS download, original decoded response bytes unchanged.');
    } catch(error) {failures.push({url,method:'Supplementary observed visual download',reason:String(error.message).slice(0,1000)});}
  }
  write(brand + '-browser-asset-provenance.json',{references,assets,failures,native_summaries:nativeSummaries,omitted_telemetry_failures:omittedTelemetryFailures,method:'Original public visual assets only. Telemetry URLs and pixels excluded. No redrawing, resizing or recompression.'});
  const screenshots = [];
  for(const variant of ['desktop','mobile']) for(const frame of ['first','full','footer']) {
    const name = `${brand}-${variant}-${frame}.jpg`, original = path.join(capture,name);
    if(!fs.existsSync(original)) continue;
    const bytes = fs.readFileSync(original); fs.copyFileSync(original,path.join(work,name));
    screenshots.push({path:name,bytes:bytes.length,sha256:hash(bytes),method:'Original browser JPEG unchanged.'});
  }
  write(brand + '-reference.json',{accepted:false,references,screenshots,asset_provenance:brand + '-browser-asset-provenance.json',scope:'Dated public desktop and narrow desktop-browser reference. Complete interaction, true phone and rendered public deployment remain separate acceptance tasks.'});
  for(const variant of ['mobile-menu','mobile-resources-menu','desktop-product-menu','desktop-resources-menu']) {
    const file = path.join(capture,`${brand}-${variant}-complete-raw-private.json`);
    if(!fs.existsSync(file)) continue;
    const raw = read(path.basename(file));
    if(raw.htmlParts.join('').length !== raw.htmlLength) throw new Error('Incomplete menu capture');
    const cleaned = sanitize(raw.htmlParts.join(''));
    raw.htmlParts = cleaned.match(/[\s\S]{1,50000}/g)||[]; raw.htmlLength=cleaned.length; raw.html_sha256=hash(cleaned);
    raw.images=raw.images.filter(image=>visualURL(image.src));
    delete raw.controls; delete raw.links;
    raw.method='Dated official open navigation DOM and CSSOM, sanitized offline; public visual state only.';
    write(`${brand}-${variant}-browser-reference.json`,raw);
    fs.copyFileSync(path.join(capture,`${brand}-${variant}-first.jpg`),path.join(work,`${brand}-${variant}.jpg`));
  }
  console.log(JSON.stringify({brand,assets:assets.length,bytes:assets.reduce((n,a)=>n+a.bytes,0),visualFailures:failures.length}));
}
const controls = read('notion-video-controls.json');
controls.pause = parse(sanitize(controls.pause)).body.innerHTML;
controls.play = parse(sanitize(controls.play)).body.innerHTML;
write('notion-video-controls.json',controls);
