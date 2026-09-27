#!/usr/bin/env python3
"""Build a static Warp visual study from the dated public homepage capture."""

import json
import re
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1] / '.stitch-work' / 'current-official'
SOURCE = ROOT / 'warp-source-current.html'
OUTPUT = ROOT / 'warp.html'
ASSETS = ROOT / 'warp-assets'
PROVENANCE = ROOT / 'warp-asset-provenance.json'
BASE = 'https://www.warp.dev'

assets = json.loads(PROVENANCE.read_text())
asset_by_path = {}
for asset in assets:
    local = ASSETS / asset['name']
    if not local.is_file():
        raise FileNotFoundError(local)
    asset_by_path[urlsplit(asset['url']).path] = asset['name']


def local_or_official(path):
    name = asset_by_path.get(path)
    return f'warp-assets/{name}' if name else BASE + path


# Keep the downloaded source and the Stitch exports intact. This derivative
# uses source-backed markup and CSS where the native Stitch screens omit most
# of the observed 7,629px desktop / 11,841px mobile homepage.
page = SOURCE.read_text()
assert 'Open infrastructure for cloud software factories' in page
assert page.count('<h2>') == 8
assert page.count('class="faq-item"') == 9

# Next scripts, analytics and tracking pixels are unnecessary for a gallery
# preview. Replace only the UI state needed to inspect the captured page.
page = re.sub(r'<script\b[^>]*>.*?</script>', '', page, flags=re.I | re.S)
page = re.sub(r'<noscript\b[^>]*>.*?</noscript>', '', page, flags=re.I | re.S)
page = re.sub(r'<link\b[^>]*\brel="(?:preload|modulepreload)"[^>]*\bas="script"[^>]*>',
              '', page, flags=re.I)
page = re.sub(r'<link\b[^>]*\brel="stylesheet"[^>]*>', '', page, flags=re.I)

# Preserve the three original CSS snapshots; the merged derivative rewrites
# observed font URLs to local bytes and leaves unavailable variants at Warp.
styles = []
for name in ('0xorukos79vdq.css', '3jb3shq1k4pin.css', '1jbbthoe8lm6p.css'):
    css = (ASSETS / name).read_text()

    def css_url(match):
        raw = match.group(1).strip(' \"\'')
        if raw.startswith('../media/'):
            path = '/_next/static/immutable/media/' + raw.split('/')[-1]
        elif raw.startswith('/'):
            path = raw
        else:
            return match.group(0)
        target = local_or_official(path)
        # This stylesheet lives inside warp-assets, beside captured fonts.
        if target.startswith('warp-assets/'):
            target = target.removeprefix('warp-assets/')
        return f'url({target})'

    styles.append(re.sub(r'url\(([^)]*)\)', css_url, css))

(ASSETS / 'warp-render.css').write_text('\n'.join(styles))
page = page.replace('</head>', '<link rel="stylesheet" href="warp-assets/warp-render.css"/></head>', 1)

# Root-relative links on the official site should never become paths on the
# collection. Captured images and fonts are served locally when available.
page = re.sub(r'\b(href|src|poster)="(/[^"]*)"',
              lambda m: f'{m.group(1)}="{local_or_official(m.group(2)) if m.group(1) != "href" or m.group(2).startswith(("/img/", "/_next/", "/fonts/")) else BASE + m.group(2)}"',
              page)
page = re.sub(r'url\((/[^)]*)\)',
              lambda m: 'url(' + local_or_official(m.group(1)) + ')', page)

enhancements = r'''<style>
.factories-landing .mobile-menu[hidden]{display:none!important}
.factories-landing .mobile-menu{overflow:auto}
.warp-draft-mobile-body{padding:20px 24px;display:grid;gap:0}
.warp-draft-mobile-body a{border-bottom:1px solid var(--line);padding:16px 2px;color:var(--fg);text-decoration:none;font:600 17px/1.3 var(--mono)}
.warp-draft-mobile-body a:last-child{border-bottom:0}
@media(max-width:860px){.factories-landing .feat-mobile-panel:not([hidden]){display:block}}
</style><script>
const warpRoot = document.querySelector('.factories-landing');
const warpChrome = warpRoot?.querySelector('.chrome-swap');
function syncWarpChrome(){warpChrome?.classList.toggle('scrolled', scrollY > 280)}
addEventListener('scroll', syncWarpChrome, {passive:true});
syncWarpChrome();

const featureButtons = [...document.querySelectorAll('.features .feat-item')];
const desktopPanes = [...document.querySelectorAll('.features .feat-grid > .code-panel > .code-pane')];
featureButtons.forEach((button, index) => button.addEventListener('click', () => {
  featureButtons.forEach((item, itemIndex) => {
    item.classList.toggle('active', itemIndex === index);
    const mobilePanel = item.closest('.feat-item-row')?.querySelector('.feat-mobile-panel');
    if (mobilePanel) mobilePanel.hidden = itemIndex !== index;
  });
  desktopPanes.forEach((pane, paneIndex) => pane.classList.toggle('active', paneIndex === index));
}));

document.querySelectorAll('.faq-q').forEach(button => button.addEventListener('click', () => {
  const item = button.closest('.faq-item');
  const opened = !item.classList.contains('open');
  item.classList.toggle('open', opened);
  button.setAttribute('aria-expanded', String(opened));
  const icon = button.querySelector('.icon');
  if (icon) icon.textContent = opened ? '[-]' : '[+]';
}));

const menu = document.querySelector('.mobile-menu');
const burger = document.querySelector('.nav-burger');
const closeMenu = () => {if (menu) menu.hidden = true; burger?.setAttribute('aria-expanded','false')};
burger?.addEventListener('click', () => {
  const open = menu.hidden;
  menu.hidden = !open;
  burger.setAttribute('aria-expanded', String(open));
});
menu?.querySelector('[data-close-menu]')?.addEventListener('click', closeMenu);
menu?.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
addEventListener('keydown', event => {if (event.key === 'Escape') closeMenu()});

document.querySelectorAll('[command="--copy"][commandfor]').forEach(button => {
  button.addEventListener('click', () => {
    const target = document.getElementById(button.getAttribute('commandfor'));
    if (target) navigator.clipboard?.writeText(target.textContent || '');
  });
});
</script>'''

mobile_menu = '''<div class="mobile-menu" hidden aria-label="Mobile navigation">
<div class="mobile-bar"><span>Warp / menu</span><button type="button" data-close-menu>close [×]</button></div>
<div class="warp-draft-mobile-body">
<a href="https://www.warp.dev/factories">Warp Factories</a>
<a href="https://www.warp.dev/terminal">Warp Terminal</a>
<a href="https://www.warp.dev/agent">Warp Agent</a>
<a href="https://www.warp.dev/enterprise">Enterprise</a>
<a href="https://www.warp.dev/pricing">Pricing</a>
<a href="https://www.warp.dev/factories/request-access">Request early access</a>
</div></div>'''
page = page.replace('<div class="chrome-swap">', mobile_menu + '<div class="chrome-swap">', 1)
page = page.replace('</body>', enhancements + '</body>', 1)

assert page.count('warp-assets/') >= 25
assert '<script src=' not in page
OUTPUT.write_text(page)
print(f'Wrote {OUTPUT} ({len(page)} characters)')
