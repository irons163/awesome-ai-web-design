#!/usr/bin/env python3
"""Correct the PostHog Stitch draft with the dated public homepage snapshot."""

import json
import re
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1] / '.stitch-work' / 'current-official'
SOURCE = ROOT / 'posthog-source-current.html'
OUTPUT = ROOT / 'posthog.html'
ASSETS = ROOT / 'posthog-assets'
PROVENANCE = ROOT / 'posthog-asset-provenance.json'

assets = json.loads(PROVENANCE.read_text())
for asset in assets:
    if not (ASSETS / asset['name']).is_file():
        raise FileNotFoundError(ASSETS / asset['name'])

page = SOURCE.read_text()
assert page.count('role="tab"') == 3
assert 'Shameless CTA' in page and 'Social proof' in page

# Gatsby's scripts hydrate the page and navigate within posthog.com. The
# collection hosts a static visual study, so preserve observed markup/CSS and
# supply only locally scoped interactions. The native Stitch exports are saved
# separately and are never overwritten by this source-backed derivative.
page = re.sub(r'<script\b[^>]*>.*?</script>', '', page, flags=re.S | re.I)
page = re.sub(r'<link\b(?=[^>]*\brel="(?:canonical|alternate|sitemap|manifest|llms\.txt)")[^>]*>',
              '', page, flags=re.I)

# Keep the observed external media and font bytes together with the draft.
# Exact URL replacement also catches inline style background images.
for asset in assets:
    local = 'posthog-assets/' + asset['name']
    url = asset['url']
    page = page.replace(url, local)
    if url.startswith('https://posthog.com/'):
        page = page.replace(urlsplit(url).path, local)

# CSS is inlined in the public HTML. Font/image URLs not included in the
# observed media bundle still resolve against the official, dated source.
page = re.sub(r'url\((\s*[\'\"]?)/([^)]*)\)',
              lambda match: 'url(' + match.group(1) +
              'https://posthog.com/' + match.group(2) + ')', page)
page = page.replace('url(&#x27;', "url('").replace('&#x27;)', "')")

# Six wallpaper / decorative images are lazy-loaded by the removed runtime.
# Promote their observed data-src to src so the static page can render them.
def promote_lazy_image(match):
    tag = match.group(0)
    if ' src=' in tag or ' data-src=' not in tag:
        return tag
    source = re.search(r' data-src="([^"]+)"', tag)
    assert source
    return tag[:-1] + ' src="' + source.group(1) + '">'

page = re.sub(r'<img\b[^>]*>', promote_lazy_image, page)

# Links, remaining images and form endpoints belong to PostHog, not to this
# collection's root path. Local assets already have non-root relative URLs.
page = re.sub(r'\b(href|src|action|poster)="/([^"]*)"',
              lambda m: m.group(1) + '="https://posthog.com/' + m.group(2) + '"', page)

enhancements = '''<style>
[role="tab"][data-state="active"]{background:#b335d3!important;color:#fff!important}
[role="tab"][data-state="inactive"]{background:transparent!important;color:inherit!important}
[role="tabpanel"][data-state="inactive"]{visibility:hidden!important;opacity:0!important;pointer-events:none!important}
[role="tabpanel"][data-state="active"]{visibility:visible!important;opacity:1!important;pointer-events:auto!important}
#posthog-draft-menu[hidden]{display:none!important}
#posthog-draft-menu{position:fixed;z-index:1000;top:52px;left:13px;width:181px;padding:8px 5px;background:#f8f8f3;border:1px solid #c9c9bd;border-radius:4px;box-shadow:0 8px 22px #0003;color:#17191a;font:13px/1.2 RoundHog,system-ui,sans-serif}
#posthog-draft-menu a{display:block;padding:5px 10px;color:#17191a;text-decoration:none;border-radius:3px}
#posthog-draft-menu a:hover{background:#e6e8df}
@media(min-width:640px){#posthog-draft-menu{display:none!important}}
</style><nav id="posthog-draft-menu" aria-label="PostHog mobile menu" hidden>
<a href="https://posthog.com/">Home</a>
<a href="https://posthog.com/products">Products</a>
<a href="https://posthog.com/pricing">Pricing</a>
<a href="https://posthog.com/docs">Docs</a>
<a href="https://posthog.com/questions">Community</a>
<a href="https://posthog.com/about">Company</a>
<a href="https://posthog.com/changelog">More</a>
<a href="https://posthog.com/about">About PostHog</a>
</nav><script>
const postTabs = [...document.querySelectorAll('[role="tab"][aria-controls]')];
postTabs.forEach(tab => tab.addEventListener('click', () => {
  postTabs.forEach(item => {
    const selected = item === tab;
    item.dataset.state = selected ? 'active' : 'inactive';
    item.setAttribute('aria-selected', String(selected));
    item.tabIndex = selected ? 0 : -1;
    const panel = document.getElementById(item.getAttribute('aria-controls'));
    if (!panel) return;
    panel.dataset.state = selected ? 'active' : 'inactive';
    panel.inert = !selected;
  });
}));
document.querySelectorAll('button[aria-label="Copy to clipboard"]').forEach(button => {
  button.addEventListener('click', () => {
    navigator.clipboard?.writeText('npx @posthog/wizard self-driving');
  });
});
const cloudButtons = [...document.querySelectorAll('button')].filter(button =>
  /^(US \(Virginia\)|EU \(Frankfurt\))$/.test(button.textContent.trim()));
cloudButtons.forEach(button => button.addEventListener('click', () => {
  cloudButtons.forEach(item => {
    item.style.borderColor = item === button ? 'currentColor' : 'transparent';
    item.setAttribute('aria-pressed', String(item === button));
  });
}));
const mobileMenuTrigger = document.querySelector('#taskbar button[role="menuitem"][aria-haspopup="menu"]');
const mobileMenu = document.getElementById('posthog-draft-menu');
mobileMenuTrigger?.addEventListener('click', event => {
  if (innerWidth >= 640) return;
  event.preventDefault();
  mobileMenu.hidden = !mobileMenu.hidden;
  mobileMenuTrigger.setAttribute('aria-expanded', String(!mobileMenu.hidden));
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape') mobileMenu.hidden = true;
});
mobileMenu?.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
  mobileMenu.hidden = true;
}));
</script>'''
page = page.replace('</body>', enhancements + '</body>', 1)

assert page.count('src="posthog-assets/') >= 10
assert len(re.findall(r'<div\b[^>]*\brole="tabpanel"', page)) == 3
assert page.count('data-src=') == 6
OUTPUT.write_text(page)
print(f'Wrote {OUTPUT} ({len(page)} characters)')
