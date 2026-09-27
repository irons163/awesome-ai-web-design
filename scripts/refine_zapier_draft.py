#!/usr/bin/env python3
"""Build a dated static Zapier homepage study from its public SSR markup."""

from __future__ import annotations

import hashlib
import html
import json
import re
from pathlib import Path
from urllib.parse import parse_qs, urljoin, urlparse


ROOT = Path(__file__).resolve().parents[1] / '.stitch-work' / 'current-official'
SOURCE = ROOT / 'zapier-source-current.html'
OUTPUT = ROOT / 'zapier.html'
ASSETS = ROOT / 'zapier-assets'
PROVENANCE = ROOT / 'zapier-asset-provenance.json'

assets = json.loads(PROVENANCE.read_text())
asset_by_url = {item['url']: item['name'] for item in assets}
for item in assets:
    path = ASSETS / item['name']
    if not path.is_file():
        raise FileNotFoundError(path)
    if hashlib.sha256(path.read_bytes()).hexdigest() != item['sha256']:
        raise ValueError(f'Asset changed: {path}')

source = SOURCE.read_text()
assert 'Welcome to automation in the agentic era' in source
assert 'The Fluid Determinism difference' in source
assert 'Go from' in source and 'AI to ROI' in source

# Keep the dated server-rendered layout. Hydration, experiments, analytics
# and tracking are not needed for a public visual reference.
page = re.sub(r'<script\b[^>]*>.*?</script>', '', source, flags=re.I | re.S)
page = re.sub(r'<noscript\b[^>]*>.*?</noscript>', '', page, flags=re.I | re.S)
page = re.sub(r'<link\b(?=[^>]*\brel="(?:preconnect|dns-prefetch)")[^>]*>',
              '', page, flags=re.I)
page = re.sub(r'<link\b(?=[^>]*\bas="script")[^>]*>',
              '', page, flags=re.I)

css_urls = re.findall(
    r'<link\b(?=[^>]*\brel="stylesheet")[^>]*\bhref="([^"]+)"[^>]*>',
    source, flags=re.I)
assert len(css_urls) == 5, css_urls
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
(ASSETS / 'zapier-render.css').write_text('\n'.join(css_parts))
page = re.sub(r'<link\b(?=[^>]*\brel="stylesheet")[^>]*>', '', page, flags=re.I)
page = page.replace('</head>',
                    '<link rel="stylesheet" href="zapier-assets/zapier-render.css"/></head>', 1)

# Next's image optimiser encodes the real Contentful/Cloudinary image URL
# inside the query. Use the saved original image for every responsive size.
def localize_next_image(match):
    relative = html.unescape(match.group(0))
    parsed = urlparse(urljoin('https://zapier.com/', relative))
    origin = parse_qs(parsed.query).get('url', [''])[0]
    if origin in asset_by_url:
        return 'zapier-assets/' + asset_by_url[origin]
    raise KeyError(f'Unsaved Next image: {origin}')


page = re.sub(
    r'/_next/image\?url=[^"\s,]+?(?=(?:\s[12]x|["\s,]))',
    localize_next_image, page, flags=re.I)
for url, name in sorted(asset_by_url.items(), key=lambda item: -len(item[0])):
    local = 'zapier-assets/' + name
    page = page.replace(url, local)
    page = page.replace(url.removeprefix('https:'), local)

# All other navigation continues to the real Zapier service.
page = re.sub(
    r'\b(href|action)="/(?!/)([^"]*)"',
    lambda match: f'{match.group(1)}="https://zapier.com/{match.group(2)}"',
    page)
page = re.sub(
    r'<video\b[^>]*>',
    lambda match: match.group(0)[:-1] + ' autoplay="" preload="metadata">',
    page, flags=re.I)

enhancements = '''<style>
/* The original Next.js client handles disclosures, dialog and carousels. */
.zapier-marketing-ui-panel-hksLsjQG[open]{display:block}
video{object-fit:cover}
@media(prefers-reduced-motion:reduce){video{display:none}}
</style>
<script>
const mobileDialog=document.querySelector('dialog[aria-label="Site navigation"]');
const mobileOpen=document.querySelector('button[aria-label="Open menu"]');
const mobileClose=document.querySelector('button[aria-label="Close menu"]');
mobileOpen?.addEventListener('click',()=>mobileDialog?.showModal());
mobileClose?.addEventListener('click',()=>mobileDialog?.close());
mobileDialog?.addEventListener('click',event=>{
  if(event.target===mobileDialog)mobileDialog.close();
});
document.querySelectorAll('[class*="Accordion_trigger__"]').forEach(button=>{
  button.addEventListener('click',()=>{
    const item=button.closest('[class*="Accordion_item__"]');
    const opened=item?.classList.toggle('Accordion_open__qMas4');
    button.setAttribute('aria-expanded',String(Boolean(opened)));
  });
});
const customerSlides=[...document.querySelectorAll('[class*="CarouselSection_carouselItemGroup__"]')];
let customerIndex=0;
function showCustomer(index){
  if(!customerSlides.length)return;
  customerIndex=(index+customerSlides.length)%customerSlides.length;
  customerSlides.forEach((slide,i)=>{
    const active=i===customerIndex;
    slide.dataset.active=String(active);
    slide.setAttribute('aria-hidden',String(!active));
    if(active)slide.removeAttribute('inert');else slide.setAttribute('inert','');
  });
}
document.querySelector('button[aria-label="Next slide"]')
  ?.addEventListener('click',()=>showCustomer(customerIndex+1));
document.querySelector('button[aria-label="Previous slide"]')
  ?.addEventListener('click',()=>showCustomer(customerIndex-1));
document.querySelectorAll('button[aria-expanded][aria-controls]')
  .forEach(button=>{
    if(button.matches('[class*="Accordion_trigger__"]'))return;
    button.addEventListener('click',()=>{
      const open=button.getAttribute('aria-expanded')!=='true';
      button.setAttribute('aria-expanded',String(open));
      const target=document.getElementById(button.getAttribute('aria-controls'));
      if(target)target.hidden=!open;
    });
  });
</script>'''
page = page.replace('</body>', enhancements + '</body>', 1)

assert page.count('zapier-assets/') >= 40
assert len(re.findall(r'<script\b', page, flags=re.I)) == 1
assert '/_next/image?' not in page
OUTPUT.write_text(page)
print(f'Wrote {OUTPUT} ({len(page)} characters, {len(assets)} verified assets)')
