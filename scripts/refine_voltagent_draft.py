#!/usr/bin/env python3
"""Build a dated VoltAgent draft from the inspected public homepage snapshot.

The original Stitch outputs and downloaded reference files remain untouched.
This static derivative uses the official section markup and media to correct
the generated draft while desktop/mobile visual acceptance is still pending.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / '.stitch-work' / 'current-official'
ASSETS = ROOT / 'voltagent-assets'
SOURCE = ROOT / 'voltagent-source-current.html'
OUTPUT = ROOT / 'voltagent.html'

TAB_IMAGES = {
    'framework': 'framework.png',
    'observability': 'dashboard.png',
    'evals': 'evals.png',
    'triggers-actions': 'trigger.png',
    'rag': 'rag-features.png',
    'monitoring': 'monitoring.png',
    'prompts': 'prompts.png',
    'guardrails': 'guardrails.png',
    'deployment': 'deployment-4.png',
}

for name in ('styles.44e054ea.css', *TAB_IMAGES.values()):
    if not (ASSETS / name).is_file():
        raise FileNotFoundError(ASSETS / name)

page = SOURCE.read_text()
assert page.count('data-tab-id=') == len(TAB_IMAGES)
assert page.count('https://cdn.voltagent.dev/website/feature-showcase/framework.png') == 2

# Hydrating this Docusaurus export would restore its own routing and analytics
# inside the collection. Keep its dated visual markup and add just the controls
# that a static single-page draft can support.
page = re.sub(r'<script\b[^>]*>.*?</script>', '', page, flags=re.S | re.I)
page = re.sub(r'<link\b(?=[^>]*\brel="(?:canonical|alternate|search|preconnect)")[^>]*>', '', page, flags=re.I)
page = page.replace(' data-has-hydrated="false"', ' data-theme="dark"')
page = page.replace('href="/assets/css/styles.44e054ea.css"',
                    'href="voltagent-assets/styles.44e054ea.css"')
page = page.replace('href="/img/favicon.ico"',
                    'href="https://voltagent.dev/img/favicon.ico"')
page = page.replace('https://cdn.voltagent.dev/website/feature-showcase/framework.png',
                    'voltagent-assets/framework.png')
page = re.sub(r'(<a\b[^>]*?\bhref=")/([^"]*)"',
              lambda m: m.group(1) + 'https://voltagent.dev/' + m.group(2) + '"',
              page, flags=re.S | re.I)

# Four hero elements are initially invisible until the removed React animation
# runs. Preserve their final layout classes and render their observed end state.
assert page.count('opacity-0 translate-y-4') == 4
page = page.replace('opacity-0 translate-y-4', 'opacity-100 translate-y-0')

def mark_tab(match):
    tag = match.group(0)
    tab_id = match.group(1)
    return tag[:-1] + (' role="tab" aria-selected="true" data-draft-active="true">'
                       if tab_id == 'framework' else
                       ' role="tab" aria-selected="false" data-draft-active="false">')

page, tab_count = re.subn(r'<button\s+data-tab-id="([^"]+)"[^>]*>', mark_tab, page)
assert tab_count == len(TAB_IMAGES)

enhancements = r'''<style>
[data-tab-id][data-draft-active="true"]{background:#101010!important;color:#2fd6a1!important;border-bottom:2px solid #2fd6a1!important}
[data-tab-id][data-draft-active="false"]{background:transparent!important;color:#eee!important;border-bottom:2px solid transparent!important}
#draft-voltagent-mobile-menu[hidden]{display:none!important}
#draft-voltagent-mobile-menu{position:fixed;inset:var(--draft-menu-top,88px) 0 0;z-index:1000;background:#090a0c;overflow:auto;padding:24px 20px 64px;border-top:1px solid #303331}
#draft-voltagent-mobile-menu a{display:block;color:#e9e9e9;text-decoration:none;padding:16px 10px;border-bottom:1px solid #272b2a;font:500 16px/1.3 Inter,system-ui,sans-serif}
#draft-voltagent-mobile-menu a:hover{color:#2fd6a1}
@media(min-width:997px){#draft-voltagent-mobile-menu{display:none!important}}
</style><nav id="draft-voltagent-mobile-menu" aria-label="Mobile" hidden>
<a href="https://voltagent.dev/voltops-llm-observability/">Products</a>
<a href="https://voltagent.dev/docs/">Documentation</a>
<a href="https://voltagent.dev/docs/quick-start/">Recipes &amp; Guides</a>
<a href="https://voltagent.dev/pricing/">Pricing</a>
<a href="https://voltagent.dev/use-cases/">Use Cases</a>
<a href="https://voltagent.dev/blog/">Resources</a>
<a href="https://console.voltagent.dev/">Log in to VoltOps</a>
<a href="https://discord.gg/voltagent">Discord Community</a>
</nav><script>
const tabImages = TAB_IMAGES_JSON;
const tabs = [...document.querySelectorAll('[data-tab-id]')];
tabs.forEach(tab => tab.addEventListener('click', () => {
  const id = tab.getAttribute('data-tab-id');
  tabs.forEach(button => {
    const selected = button === tab;
    button.dataset.draftActive = String(selected);
    button.setAttribute('aria-selected', String(selected));
  });
  document.querySelectorAll('img[src^="voltagent-assets/"]').forEach(image => {
    image.src = 'voltagent-assets/' + tabImages[id];
    image.alt = id + ' preview';
  });
}));
document.querySelector('.announcementBarClose_gvF7')?.addEventListener('click', () => {
  document.querySelector('.announcementBar_mb4j')?.remove();
});
document.querySelector('button[aria-label="Copy npm command to clipboard"]')?.addEventListener('click', () => {
  navigator.clipboard?.writeText('npm create voltagent-app@latest');
});
const menuButton = document.querySelector('.menuButton_nZcG');
const menu = document.getElementById('draft-voltagent-mobile-menu');
menuButton?.setAttribute('aria-expanded', 'false');
menuButton?.setAttribute('aria-controls', menu.id);
function toggleMenu(open) {
  menu.hidden = !open;
  menuButton.setAttribute('aria-expanded', String(open));
  menuButton.setAttribute('aria-label', open ? 'Close menu' : 'Toggle menu');
  menu.style.setProperty('--draft-menu-top', document.querySelector('.navbar_UaH_').getBoundingClientRect().bottom + 'px');
  document.body.style.overflow = open ? 'hidden' : '';
}
menuButton?.addEventListener('click', () => toggleMenu(menu.hidden));
menu.querySelectorAll('a').forEach(link => link.addEventListener('click', () => toggleMenu(false)));
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && !menu.hidden) toggleMenu(false);
});
</script>'''.replace('TAB_IMAGES_JSON', json.dumps(TAB_IMAGES, separators=(',', ':')))
page = page.replace('</body>', enhancements + '</body>', 1)
assert page.count('voltagent-assets/styles.44e054ea.css') == 1
assert page.count('voltagent-assets/framework.png') == 2
OUTPUT.write_text(page)
print(f'Wrote {OUTPUT} ({len(page)} characters)')
