#!/usr/bin/env python3
"""Build a static Wise Canada homepage study from a dated public capture."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urljoin, urlparse


ROOT = Path(__file__).resolve().parents[1] / '.stitch-work' / 'current-official'
SOURCE = ROOT / 'wise-source-current.html'
OUTPUT = ROOT / 'wise.html'
ASSETS = ROOT / 'wise-assets'
PROVENANCE = ROOT / 'wise-asset-provenance.json'

assets = json.loads(PROVENANCE.read_text())
asset_by_url = {item['url']: item['name'] for item in assets}
for item in assets:
    path = ASSETS / item['name']
    if not path.is_file():
        raise FileNotFoundError(path)
    if hashlib.sha256(path.read_bytes()).hexdigest() != item['sha256']:
        raise ValueError(f'Asset changed: {path}')

source = SOURCE.read_text()
assert 'Wise Canada' in source
assert 'The chequing account for home and abroad' in source
assert 'The account that moves with you' in source
assert 'Safe at every step' in source
assert 'One smart app, 60 million downloads' in source

# Keep the server-rendered page and its exact stylesheet ordering. Strip
# hydration, analytics and pixels: this is a dated static visual reference.
page = re.sub(r'<script\b[^>]*>.*?</script>', '', source, flags=re.I | re.S)
page = re.sub(r'<noscript\b[^>]*>.*?</noscript>', '', page, flags=re.I | re.S)
page = re.sub(r'<iframe\b[^>]*>.*?</iframe>', '', page, flags=re.I | re.S)
page = re.sub(r'<link\b(?=[^>]*\brel="(?:preconnect|dns-prefetch|preload)")[^>]*>',
              '', page, flags=re.I)

css_urls = [urljoin('https://wise.com/', href)
            for href in re.findall(
                r'<link\b(?=[^>]*\brel="stylesheet")[^>]*\bhref="([^"]+)"[^>]*>',
                source, flags=re.I)]
assert len(css_urls) == 6, css_urls
css_parts = []
for css_url in css_urls:
    original = (ASSETS / asset_by_url[css_url]).read_text(errors='replace')

    def localize_css(match):
        raw = match.group(1).strip().strip('"\'')
        absolute = urljoin(css_url, raw)
        if absolute in asset_by_url:
            return 'url(' + asset_by_url[absolute] + ')'
        return match.group(0)

    css_parts.append(re.sub(r'url\(\s*([^)]+)\s*\)', localize_css, original, flags=re.I))
(ASSETS / 'wise-render.css').write_text('\n'.join(css_parts))
page = re.sub(r'<link\b(?=[^>]*\brel="stylesheet")[^>]*>', '', page, flags=re.I)
page = page.replace('</head>',
                    '<link rel="stylesheet" href="wise-assets/wise-render.css"/></head>', 1)

# Source media may use absolute wise.com URLs or root-relative Next paths.
# Localize both spellings before rewriting navigation links.
for url, name in sorted(asset_by_url.items(), key=lambda item: -len(item[0])):
    local = 'wise-assets/' + name
    page = page.replace(url, local)
    path = urlparse(url).path
    if path.startswith('/static-assets/') or path.startswith('/web-art/'):
        page = page.replace(path, local)
page = re.sub(
    r'\b(href|action)="/(?!/)([^"]*)"',
    lambda match: f'{match.group(1)}="https://wise.com/{match.group(2)}"',
    page)

# The source calculator requires Wise's live service. Display the observed
# Canadian values as a read-only sample instead of implying live rates.
page = re.sub(
    r'<input\b[^>]*>',
    lambda match: match.group(0)[:-2] +
    ' readonly="" title="Dated static sample, not a live rate"/>',
    page, flags=re.I)

enhancements = '''<style>
/* Static source capture: reveal content formerly activated by Next.js. */
[class*="SimpleMotion_fadeIn--start"],
[class*="SimpleMotion_slideUp--start"],
[class*="SimpleMotion_scaleIn--start"]{
  opacity:1!important;visibility:visible!important;transform:none!important;
}
.eds-carousel__container{overflow-x:auto!important;scroll-snap-type:x mandatory}
.eds-carousel__slide{
  transform:none!important;opacity:1!important;visibility:visible!important;
  scroll-snap-align:start
}
#wise-study-nav{display:none}
#wise-study-nav[data-open="true"]{
  display:flex;position:fixed;inset:0;z-index:99999;background:#b4e887;
  color:#172b05;flex-direction:column;padding:24px;gap:22px;overflow:auto
}
#wise-study-nav a{color:inherit;font:700 28px/1.2 Inter,Arial,sans-serif;text-decoration:none}
#wise-study-nav button{align-self:flex-end;background:none;border:0;
  color:inherit;font:700 36px/1 Arial,sans-serif}
@media(min-width:769px){#wise-study-nav[data-open="true"]{display:none}}
</style>
<nav id="wise-study-nav" aria-label="Wise mobile navigation" aria-hidden="true">
  <button type="button" aria-label="Close navigation menu">&times;</button>
  <a href="https://wise.com/">Personal</a>
  <a href="https://wise.com/ca/business/">Business</a>
  <a href="https://wise.com/platform/">Platform</a>
  <a href="https://wise.com/help/">Help</a>
  <a href="https://wise.com/login/">Log in</a>
</nav>
<script>
const bannerClose=document.querySelector('.eds-banner__close');
bannerClose?.addEventListener('click',()=>bannerClose.closest('.eds-banner')?.remove());
const navTrigger=document.querySelector('[data-testid="mobile-nav-trigger"]');
const nav=document.getElementById('wise-study-nav');
function closeWiseNav(){
  nav?.setAttribute('data-open','false');
  nav?.setAttribute('aria-hidden','true');
  navTrigger?.setAttribute('aria-expanded','false');
  document.body.style.overflow='';
}
navTrigger?.addEventListener('click',()=>{
  const opened=nav?.getAttribute('data-open')!=='true';
  nav?.setAttribute('data-open',String(opened));
  nav?.setAttribute('aria-hidden',String(!opened));
  navTrigger?.setAttribute('aria-expanded',String(opened));
  document.body.style.overflow=opened?'hidden':'';
});
nav?.querySelector('button')?.addEventListener('click',closeWiseNav);
nav?.querySelectorAll('a').forEach(link=>link.addEventListener('click',closeWiseNav));
document.addEventListener('keydown',event=>{if(event.key==='Escape')closeWiseNav()});
document.querySelectorAll('.eds-carousel').forEach(carousel=>{
  const track=carousel.querySelector('.eds-carousel__container');
  carousel.querySelectorAll('button[aria-label="Previous"],button[aria-label="Next"]')
    .forEach(button=>{
      button.removeAttribute('disabled');
      button.setAttribute('aria-disabled','false');
      button.addEventListener('click',()=>track?.scrollBy({
        left:(button.getAttribute('aria-label')==='Next'?1:-1)*Math.max(280,track.clientWidth*.65),
        behavior:'smooth'
      }));
    });
});
</script>'''
page = page.replace('</body>', enhancements + '</body>', 1)

assert 'Wise Canada' in page
assert page.count('wise-assets/') >= 100
assert len(re.findall(r'<script\b', page, flags=re.I)) == 1
assert '<iframe' not in page
OUTPUT.write_text(page)
print(f'Wrote {OUTPUT} ({len(page)} characters, {len(assets)} verified assets)')
