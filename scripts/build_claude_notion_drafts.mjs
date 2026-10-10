import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {JSDOM, VirtualConsole} from 'jsdom';

const work = path.resolve('.stitch-work/current-official');
const read = name => JSON.parse(fs.readFileSync(path.join(work, name), 'utf8'));
const hash = value => crypto.createHash('sha256').update(value).digest('hex');
const parse = html => new JSDOM(html, {virtualConsole: new VirtualConsole()}).window.document;

function runtime() {
  const narrow=matchMedia('(max-width:799px)'); let mode,live=[],mobileOpen=false,mobileResourcesOpen=false;
  const setAttrs=(e,attrs)=>{[...e.attributes].forEach(a=>e.removeAttribute(a.name));Object.entries(attrs).forEach(([k,v])=>e.setAttribute(k,v));};
  function install(){const next=narrow.matches?'mobile':'desktop';if(next===mode)return;live.forEach(e=>e.remove());setAttrs(document.documentElement,CONFIG.attributes[next].html);setAttrs(document.body,CONFIG.attributes[next].body);const fragment=document.getElementById('study-'+next+'-source').content.cloneNode(true);live=[...fragment.childNodes];document.body.insertBefore(fragment,document.getElementById('study-runtime'));mode=next;mobileOpen=false;document.querySelectorAll('video').forEach(e=>{e.muted=true;e.playsInline=true;});if(CONFIG.brand==='claude'){const reveal=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.querySelectorAll('.word').forEach(word=>{word.style.opacity='1';word.style.visibility='inherit';});reveal.unobserve(entry.target);}}));document.querySelectorAll('h1,h2,h3,h4').forEach(e=>reveal.observe(e));}}
  function replaceWidget(name,open){const widget=CONFIG.widgets[mode]?.[name];if(!widget)return;const current=document.querySelector(widget.selector);if(!current)return;const template=document.createElement('template');template.innerHTML=open?widget.open:widget.closed;current.replaceWith(template.content);}
  function mobileMenu(open){replaceWidget('mobile-menu',open);mobileOpen=open;mobileResourcesOpen=false;if(CONFIG.brand==='claude')document.body.classList.toggle('is-nav-open',open);document.body.style.overflow=open?'hidden':'';document.querySelectorAll('main').forEach(e=>e.inert=open);}
  function closeDesktop(){if(mode!=='desktop')return;if(CONFIG.brand==='notion')for(const name of ['product','resources'])replaceWidget(name,false);document.querySelectorAll('.w-dropdown-toggle[aria-expanded="true"]').forEach(button=>{button.setAttribute('aria-expanded','false');button.classList.remove('w--open');document.getElementById(button.getAttribute('aria-controls'))?.classList.remove('w--open');});}
  document.addEventListener('click',event=>{
    const button=event.target.closest('button,[role="button"]');
    if(!button){if(!event.target.closest('nav,.nav_component'))closeDesktop();return;}
    const label=button.getAttribute('aria-label')||button.textContent.trim();
    if(button.matches('.nav_btn_wrap')||label==='Toggle main menu'){mobileMenu(!mobileOpen);return;}
    if(CONFIG.brand==='notion'){
      if(mode==='mobile'&&label==='Resources'){mobileResourcesOpen=!mobileResourcesOpen;replaceWidget('resources',mobileResourcesOpen);return;}
      if(button.closest('nav[aria-label="Main"]')&&['Product','Resources'].includes(label)){const open=button.getAttribute('aria-expanded')!=='true';closeDesktop();replaceWidget(label.toLowerCase(),open);return;}
      if(label==='Play'||label==='Pause'){const video=document.querySelector('video');if(!video)return;const replace=state=>{const fragment=document.createElement('template');fragment.innerHTML=CONFIG.videoControls[state];button.replaceWith(fragment.content);};if(video.paused){video.play().then(()=>replace('pause')).catch(()=>{});}else{video.pause();replace('play');}return;}
      if(label==='Cookie settings')location.assign('https://www.notion.com/trust/privacy-policy');
      return;
    }
    if(button.matches('.w-dropdown-toggle')){const open=button.getAttribute('aria-expanded')!=='true';if(mode==='desktop'){closeDesktop();if(label==='Product'){replaceWidget('product',open);return;}}button.setAttribute('aria-expanded',String(open));button.classList.toggle('w--open',open);document.getElementById(button.getAttribute('aria-controls'))?.classList.toggle('w--open',open);return;}
    if(button.matches('[data-tabs="tab"]')){const component=button.closest('[data-tabs="component"]');const buttons=[...component.querySelectorAll('[data-tabs="tab"]')],index=buttons.indexOf(button);buttons.forEach((e,i)=>{e.setAttribute('aria-selected',String(i===index));e.tabIndex=i===index?0:-1;e.classList.toggle('is-active',i===index);});component.querySelectorAll('[data-tabs="panel"]').forEach((e,i)=>{e.hidden=i!==index;e.setAttribute('role','tabpanel');});return;}
    if(button.matches('[data-accordion="toggle"]')){const open=button.getAttribute('aria-expanded')!=='true';button.setAttribute('aria-expanded',String(open));const content=document.getElementById(button.getAttribute('aria-controls'));content.style.display=open?'block':'none';content.style.height=open?'auto':'0px';button.closest('[data-accordion="component"]').classList.toggle('is-opened',open);return;}
    if(label==='Continue with Google')location.assign('https://claude.ai/');
    if(label==='Let’s find out'||label==="Let's find out")location.assign('https://claude.com/pricing');
  });
  document.addEventListener('submit',event=>{event.preventDefault();location.assign(CONFIG.brand==='claude'?'https://claude.ai/':'https://www.notion.com/');});
  document.addEventListener('keydown',event=>{if(event.key==='Escape'){if(mobileOpen)mobileMenu(false);closeDesktop();}if(event.key==='Enter'&&event.target.matches('.w-dropdown-toggle')){event.preventDefault();event.target.click();}if(['ArrowLeft','ArrowRight'].includes(event.key)&&event.target.matches('[data-tabs="tab"]')){const tabs=[...event.target.closest('[data-tabs="component"]').querySelectorAll('[data-tabs="tab"]')];const index=(tabs.indexOf(event.target)+(event.key==='ArrowRight'?1:-1)+tabs.length)%tabs.length;tabs[index].click();tabs[index].focus();event.preventDefault();}});
  narrow.addEventListener('change',install);install();
}

for (const brand of (process.argv.slice(2).length ? process.argv.slice(2) : ['claude', 'notion'])) {
  const native = read(brand + '-stitch-oct10-generated.json');
  if (!native.screens?.length) throw new Error('A genuine new Stitch generation is required');
  for (const screen of native.screens) for (const file of screen.exports) {
    const bytes = fs.readFileSync(path.join(work, file.path));
    if (bytes.length !== file.bytes || hash(bytes) !== file.sha256) throw new Error('Native export differs from its recorded original');
  }
  const assets = new Map(read(brand + '-browser-asset-provenance.json').assets.map(a => [a.source_url, a]));
  for (const asset of assets.values()) {
    const bytes = fs.readFileSync(path.join(work, asset.path));
    if (bytes.length !== asset.bytes || hash(bytes) !== asset.sha256) throw new Error('Original asset differs: ' + asset.path);
  }
  const origin = brand === 'claude' ? 'https://claude.com/index.html' : 'https://www.notion.com/';
  const used = new Set();
  const url = (value, base = origin) => {
    if (!value || /^(#|data:|mailto:|tel:)/i.test(value)) return value;
    if (/^javascript:/i.test(value)) return '#';
    const absolute = new URL(value, base).href;
    const asset = assets.get(absolute);
    if (asset) {used.add(asset.path); return asset.path;}
    return absolute;
  };
  const css = (value, base = origin) => value.replace(/url\(\s*(['"]?)(.*?)\1\s*\)/g,
    (match, quote, value) => /^(data:|#)/i.test(value) ? match : 'url("' + url(value, base) + '")');
  function localize(document) {
    document.querySelectorAll('base,meta[http-equiv],link:not([rel="stylesheet"]),.grecaptcha-badge,[id^="codex-browser-"]').forEach(e => e.remove());
    document.querySelectorAll('*').forEach(element => {
      for (const name of ['src', 'href', 'poster']) if (element.hasAttribute(name)) element.setAttribute(name, url(element.getAttribute(name)));
      if (element.hasAttribute('style')) element.setAttribute('style', css(element.getAttribute('style')));
      const srcset = element.getAttribute('srcset');
      if (srcset && !srcset.startsWith('data:')) element.setAttribute('srcset', srcset.split(/,\s*(?=(?:https?:|\/))/).map(item => {
        const tokens = item.trim().split(/\s+/); tokens[0] = url(tokens[0]); return tokens.join(' ');
      }).join(', '));
    });
    document.querySelectorAll('input[type="email"],input[type="password"]').forEach(input => {input.readOnly = true; input.autocomplete = 'off';});
    // A source snapshot has no application lazy-loader. Load its unchanged
    // original images eagerly so every shelf and the full-page proof can render.
    document.querySelectorAll('img').forEach(image => image.setAttribute('loading', 'eager'));
    document.querySelectorAll('form').forEach(form => {form.removeAttribute('action'); form.removeAttribute('method');});
  }
  const documents = {}, references = {}, styles = [];
  const attributes = element => Object.fromEntries([...element.attributes].map(a => [a.name, a.value]));
  const configuration = {brand, attributes: {}, widgets: {desktop:{},mobile:{}}};
  if(brand==='notion')configuration.videoControls=read('notion-video-controls.json');
  for (const variant of ['desktop', 'mobile']) {
    const reference = read(brand + '-' + variant + '-browser-reference.json');
    const html = reference.htmlParts.join('');
    if (hash(html) !== reference.html_sha256) throw new Error('Source reference changed');
    const document = parse(html);
    const nodes = [...document.querySelectorAll('style,link[rel="stylesheet"]')];
    if (nodes.length !== reference.stylesheets.length) throw new Error('Stylesheet order is incomplete');
    const media = variant === 'desktop' ? '(min-width:800px)' : '(max-width:799px)';
    nodes.forEach((node, index) => {
      const sheet = reference.stylesheets[index];
      let text, base = origin;
      if (node.tagName === 'LINK') {
        base = new URL(node.getAttribute('href'), origin).href;
        if (base !== sheet.href) throw new Error('Stylesheet order mismatch');
        // Google identity UI was removed with its scripts/frames; its stylesheet
        // does not style the public marketing page retained in this study.
        if(base === 'https://accounts.google.com/gsi/style'){node.remove();return;}
        const asset = assets.get(base);
        if (!asset && !sheet.parts) throw new Error('Missing active stylesheet: ' + base);
        text = asset ? fs.readFileSync(path.join(work, asset.path), 'utf8') : sheet.parts.join('');
      } else {
        // CSS-in-JS inserts rules through CSSOM; outerHTML alone loses them.
        text = node.textContent || sheet.parts?.join('') || '';
      }
      if (text) styles.push('<style media="' + media + '">' + css(text, base).replace(/<\/style/gi, '<\\/style') + '</style>');
      node.remove();
    });
    localize(document);
    const sourceImages=reference.images.filter(image=>/^(data:image\/|https:\/\/(?:[^/]*\.)?(?:website-files\.com|notion\.com|ctfassets\.net|anthropic\.com)\/)/i.test(image.src));
    if(document.images.length!==sourceImages.length)throw new Error('Image order differs after sanitization');
    [...document.images].forEach((image,index)=>{image.setAttribute('src',url(sourceImages[index].src));image.removeAttribute('srcset');});
    document.querySelectorAll('picture source').forEach(e=>e.removeAttribute('srcset'));
    for(const name of variant==='mobile'?['mobile-menu','resources']:['product','resources']){
      const filename=brand+'-'+(name==='mobile-menu'?'mobile-menu':variant+'-'+name+'-menu')+'-browser-reference.json';
      if(!fs.existsSync(path.join(work,filename)))continue;
      const state=read(filename);const menuDocument=parse(state.htmlParts.join(''));localize(menuDocument);
      const selector=brand==='claude'?'.nav_component':(variant==='mobile'?'[class*="globalNavigationWrapper"]':'nav[aria-label="Main"] #'+name);
      let closed=document.querySelector(selector);
      if(variant==='mobile'&&name==='resources'){
        const closedDocument=parse(read(brand+'-mobile-menu-browser-reference.json').htmlParts.join(''));localize(closedDocument);closed=closedDocument.querySelector(selector);
      }
      const open=menuDocument.querySelector(selector);
      if(!open||!closed)throw new Error('Missing observed navigation widget: '+filename);
      configuration.widgets[variant][name]={selector,open:open.outerHTML,closed:closed.outerHTML};
      // An opened widget can add CSS-in-JS rules that were absent initially.
      for(const sheet of state.stylesheets.filter(s=>!s.href))if(sheet.parts?.join(''))styles.push('<style media="'+media+'">'+css(sheet.parts.join('')).replace(/<\/style/gi,'<\\/style')+'</style>');
    }
    configuration.attributes[variant] = {html: attributes(document.documentElement), body: attributes(document.body)};
    documents[variant] = document;
    references[variant] = {file: brand + '-' + variant + '-browser-reference.json', observed_at: reference.observed_at, html_sha256: reference.html_sha256};
  }
  const templates = ['desktop', 'mobile'].map(variant => '<template id="study-' + variant + '-source">' + documents[variant].body.innerHTML + '</template>').join('');
  const script = '<script id="study-runtime">const CONFIG=' + JSON.stringify(configuration).replace(/</g, '\\u003c') + ';(' + runtime.toString() + ')();</script>';
  const html = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>' + brand + ' — dated official-site working study</title>' + styles.join('') + '<style>[data-study-mobile-menu][hidden],[data-study-desktop-menu][hidden]{display:none!important}</style></head><body>' + templates + script + '</body></html>';
  fs.writeFileSync(path.join(work, brand + '.html'), html);
  fs.writeFileSync(path.join(work, brand + '-draft-build-record.json'), JSON.stringify({accepted: false,
    native_exports: brand + '-stitch-oct10-generated.json', source_references: references,
    asset_provenance: brand + '-browser-asset-provenance.json', asset_paths: [...used].sort(),
    working_draft: {path: brand + '.html', bytes: Buffer.byteLength(html), sha256: hash(html)},
    method: 'Working correction after an independently prompted native Stitch generation. Dated sanitized public source DOM, CSS/CSSOM, original vector marks, fonts and images retained; desktop and narrow source states switch at 800px. Native generation exports remain separate and unchanged.',
    limitations: brand === 'claude' ? ['The actual reference is the public /index.html marketing entry; the root redirected to login in this browser.', 'The official hero video had an empty source and was not replaced with invented content.', 'Complete interaction, true mobile-user-agent and public rendered comparison remain unaccepted.'] : ['Rotating headline, logo marquee and video phases are dated source states; complete motion parity is unaccepted.', 'Accounts remain on Notion; true mobile-user-agent and public rendered comparison remain unaccepted.'],
  }, null, 2) + '\n');
  console.log(JSON.stringify({brand, bytes: Buffer.byteLength(html), retainedAssets: used.size, accepted: false}));
}
