#!/usr/bin/env python3
"""Build a static Webflow study from a dated public homepage capture."""

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / '.stitch-work' / 'current-official'
SOURCE = ROOT / 'webflow-source-current.html'
OUTPUT = ROOT / 'webflow.html'
ASSETS = ROOT / 'webflow-assets'
PROVENANCE = ROOT / 'webflow-asset-provenance.json'

assets = json.loads(PROVENANCE.read_text())
for asset in assets:
    if not (ASSETS / asset['name']).is_file():
        raise FileNotFoundError(ASSETS / asset['name'])

page = SOURCE.read_text()
assert 'Build for what’s next' in page
assert 'Where modern teams and agents run the web' in page
assert '300,000+ brands move' in page

# Preserve the official source, the exact downloaded assets, and the native
# Stitch screens separately. This derivative hosts a dated visual study.
# Remove the analytics/experimentation runtime and tracking pixels, while
# retaining the server-rendered page, original Webflow styles and media.
page = re.sub(r'<script\b[^>]*>.*?</script>', '', page, flags=re.I | re.S)
page = re.sub(r'<noscript\b[^>]*>.*?</noscript>', '', page, flags=re.I | re.S)
page = re.sub(r'<style>\.anti-flicker.*?</style>', '', page, flags=re.I | re.S)

css_urls = [
    'https://cdn.prod.website-files.com/686294e263eb7e215bd232f7/css/marketing-main.webflow.shared.ba5f7055f.min.css',
    'https://cdn.prod.website-files.com/686294e263eb7e215bd232f7/css/marketing-main.webflow.686294e363eb7e215bd2334b.5781ef409.opt.min.css',
]
for url in css_urls:
    page = re.sub(r'<link\b(?=[^>]*\bhref="' + re.escape(url) + r'")[^>]*>',
                  '', page, flags=re.I)

asset_by_url = {item['url']: item['name'] for item in assets}
styles = []
for url in css_urls:
    original = (ASSETS / asset_by_url[url]).read_text()
    for asset_url, name in sorted(asset_by_url.items(), key=lambda item: -len(item[0])):
        original = original.replace(asset_url, name)
    styles.append(original)
(ASSETS / 'webflow-render.css').write_text('\n'.join(styles))
page = page.replace('</head>', '<link rel="stylesheet" href="webflow-assets/webflow-render.css"/></head>', 1)

for url, name in sorted(asset_by_url.items(), key=lambda item: -len(item[0])):
    page = page.replace(url, 'webflow-assets/' + name)

# Links to other pages should still go to the real Webflow site. Relative
# static assets are already handled by the exact URL replacement above.
page = re.sub(r'\b(href|src|poster)="/([^"]*)"',
              lambda match: f'{match.group(1)}="https://webflow.com/{match.group(2)}"',
              page)
page = re.sub(r'\bhref="(?!https?:|mailto:|tel:|#|/|webflow-assets/)([^"]+)"',
              lambda match: f'href="https://webflow.com/{match.group(1)}"',
              page)

enhancements = '''<style>
/* The original page needs its Webflow runtime for responsive menus, sliders,
   and entrance effects. Keep the dated capture readable without that runtime. */
html,body{background:#080808}
[data-animation-css]{animation:none!important;opacity:1!important;visibility:visible!important}
.anti-flicker{visibility:visible!important;opacity:1!important}
@media(max-width:991px){
  .nav-menu[data-nav-menu-open]{display:block!important;position:fixed!important;top:68px;bottom:0;left:0;right:0;z-index:9998;overflow:auto;background:#080808}
  .nav-menu_btn.w--open{z-index:9999}
}
/* Without Swiper hydration, keep the observed customer cards inspectable. */
#customers .slider_element{overflow-x:auto;scroll-snap-type:x mandatory}
#customers .swiper-wrapper.w-dyn-items{display:flex}
#customers .swiper-wrapper.w-dyn-items>.w-dyn-item{flex:0 0 min(38vw,520px);scroll-snap-align:start}
@media(max-width:767px){#customers .swiper-wrapper.w-dyn-items>.w-dyn-item{flex-basis:86vw}}
</style><script>
const menuButton = document.querySelector('.nav-menu_btn');
const menu = document.querySelector('.nav-menu.w-nav-menu');
function closeWebflowMenu(){
  menuButton?.classList.remove('w--open');
  menuButton?.setAttribute('aria-expanded','false');
  menu?.removeAttribute('data-nav-menu-open');
  document.body.style.overflow='';
}
menuButton?.setAttribute('role','button');
menuButton?.setAttribute('tabindex','0');
menuButton?.setAttribute('aria-label','Open menu');
menuButton?.setAttribute('aria-expanded','false');
menuButton?.addEventListener('click', () => {
  const opened = !menuButton.classList.contains('w--open');
  menuButton.classList.toggle('w--open', opened);
  menuButton.setAttribute('aria-expanded', String(opened));
  if (opened) menu?.setAttribute('data-nav-menu-open','');
  else menu?.removeAttribute('data-nav-menu-open');
  document.body.style.overflow=opened?'hidden':'';
});
menuButton?.addEventListener('keydown', event => {
  if (event.key==='Enter' || event.key===' ') {event.preventDefault();menuButton.click()}
});
document.addEventListener('keydown', event => {if (event.key==='Escape') closeWebflowMenu()});
menu?.querySelectorAll('a').forEach(link => link.addEventListener('click',closeWebflowMenu));
menu?.querySelectorAll('[data-dropdown="toggle"]').forEach(button => {
  button.addEventListener('click', () => {
    const wrapper=button.closest('[data-dropdown="wrap"]');
    const open=!wrapper?.classList.contains('cc-open-mode');
    wrapper?.classList.toggle('cc-open-mode',open);
    wrapper?.querySelector('[data-dropdown="content"]')?.classList.toggle('cc-open-mode',open);
    button.setAttribute('aria-expanded',String(open));
  });
});
const customerSlider=document.querySelector('#customers .slider_element');
document.querySelectorAll('#customers [data-slider="previous"], #customers [data-slider="next"]').forEach(button => {
  const direction=button.getAttribute('data-slider')==='next'?1:-1;
  button.setAttribute('aria-label',direction===1?'Next customer story':'Previous customer story');
  button.addEventListener('click',()=>customerSlider?.scrollBy({left:direction*customerSlider.clientWidth*.8,behavior:'smooth'}));
});
document.querySelectorAll('[data-dropdown="close"]').forEach(button => button.addEventListener('click', () => {
  const wrapper=button.closest('[data-dropdown="wrap"]');
  wrapper?.classList.remove('cc-open-mode');
  wrapper?.querySelector('[data-dropdown="content"]')?.classList.remove('cc-open-mode');
  wrapper?.querySelector('[data-dropdown="toggle"]')?.setAttribute('aria-expanded','false');
}));
</script>'''
page = page.replace('</body>', enhancements + '</body>', 1)

assert '<script src=' not in page
assert page.count('webflow-assets/') > 100
assert page.count('<img') >= 100
OUTPUT.write_text(page)
print(f'Wrote {OUTPUT} ({len(page)} characters)')
