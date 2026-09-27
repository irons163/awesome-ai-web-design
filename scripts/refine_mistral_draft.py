#!/usr/bin/env python3
"""Make a dated, source-backed static Mistral visual draft."""

from __future__ import annotations

import hashlib
import json
import os
import re
from html import unescape
from pathlib import Path
from urllib.parse import urljoin, urlparse


ROOT = Path(__file__).resolve().parents[1] / '.stitch-work' / 'current-official'
SOURCE = ROOT / 'mistral.ai-source-current.html'
DESTINATION = ROOT / 'mistral.ai.html'
ASSETS = ROOT / 'mistral.ai-assets'
BASE = 'https://mistral.ai/'

MENU_SCRIPT = '''<script>
(() => {
  const button = document.querySelector('#mobile-menu-button');
  const panel = document.querySelector('#mobile-nav-panel');
  if (!button || !panel) return;
  const subpanels = [...panel.querySelectorAll('[data-mobile-subpanel]')];
  function closeSubpanels() {
    subpanels.forEach(item => { item.style.transform = 'translateX(100%)'; });
  }
  function setOpen(open) {
    panel.style.transform = open ? 'translateX(0)' : 'translateX(100%)';
    button.setAttribute('aria-expanded', String(open));
    if (!open) closeSubpanels();
  }
  button.setAttribute('aria-expanded', 'false');
  button.addEventListener('click', () => setOpen(button.getAttribute('aria-expanded') !== 'true'));
  panel.querySelectorAll('[data-mobile-nav-index]').forEach(item => {
    item.addEventListener('click', () => {
      closeSubpanels();
      const target = panel.querySelector('[data-mobile-subpanel="' + item.dataset.mobileNavIndex + '"]');
      if (target) target.style.transform = 'translateX(0)';
    });
  });
  subpanels.forEach(item => {
    const back = document.createElement('button');
    back.type = 'button';
    back.textContent = '← Menu';
    back.setAttribute('aria-label', 'Back to menu');
    back.style.cssText = 'display:block;width:100%;text-align:left;padding:16px;border-bottom:1px solid #333;background:#101013;color:#fafaf4';
    back.addEventListener('click', closeSubpanels);
    item.prepend(back);
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape') setOpen(false);
  });
})();
</script>'''


def main() -> None:
    provenance = json.loads((ROOT / 'mistral.ai-asset-provenance.json').read_text())
    assets = {item['url']: item for item in provenance}
    css_derivatives = []
    css_replacements = {}
    for url, item in assets.items():
        if not item['path'].endswith('.css'):
            continue
        original = ASSETS / item['path']
        local = original.with_name(original.stem + '.local.css')
        stylesheet = original.read_text(errors='replace')

        def rewrite_css_url(match: re.Match) -> str:
            value = unescape(match.group(1).strip().strip('"\''))
            resolved = urljoin(url, value)
            asset = assets.get(resolved)
            if asset is None:
                return match.group(0)
            relative = os.path.relpath(ASSETS / asset['path'], local.parent)
            return 'url(' + relative + ')'

        stylesheet = re.sub(r'url\(\s*([^)]+)\s*\)', rewrite_css_url,
                            stylesheet)
        local.write_text(stylesheet)
        path = local.relative_to(ROOT).as_posix()
        css_replacements[url] = path
        css_derivatives.append({
            'source_url': url,
            'source_sha256': item['sha256'],
            'local_path': path,
            'local_sha256': hashlib.sha256(local.read_bytes()).hexdigest(),
        })

    html = SOURCE.read_text()
    # Keep the official server-rendered page and its CSS, while removing
    # analytics, consent injection, Netlify telemetry and the original runtime.
    html = re.sub(r'<script\b[^>]*>.*?</script>', '', html,
                  flags=re.I | re.S)
    html = re.sub(r'<noscript>\s*<iframe\b[^>]*googletagmanager[^>]*>\s*</iframe>\s*</noscript>',
                  '', html, flags=re.I | re.S)
    html = re.sub(r'<iframe\b[^>]*googletagmanager[^>]*>\s*</iframe>',
                  '', html, flags=re.I | re.S)
    html = re.sub(r'<link\b[^>]*href="https://www\.googletagmanager\.com"[^>]*>',
                  '', html, flags=re.I)
    # Both absolute and same-origin root-relative references occur in the
    # snapshot. Replace longest forms first so query strings do not remain.
    replacements = []
    for url, item in assets.items():
        parsed = urlparse(url)
        local = css_replacements.get(url,
                                     'mistral.ai-assets/' + item['path'])
        replacements.append((url, local))
        replacements.append((parsed.path + ('?' + parsed.query if parsed.query else ''), local))
    for old, new in sorted(set(replacements), key=lambda pair: -len(pair[0])):
        for variant in (old, old.replace('&', '&amp;')):
            if variant.startswith('/'):
                # A localized path still contains the original slash-prefixed
                # fragment. Avoid rewriting that fragment a second time.
                html = re.sub(r'(?<!mistral\.ai-assets)' + re.escape(variant),
                              lambda _match: new, html)
            else:
                html = html.replace(variant, new)
    # Catalog, CTA and footer links should lead to the real official page,
    # not broken routes under this collection's static host.
    html = re.sub(r'(<a\b[^>]*\bhref=")(/[^\"]*)(")',
                  lambda match: match.group(1) + BASE.rstrip('/') +
                  match.group(2) + match.group(3), html, flags=re.I)
    html = html.replace('href="javascript:openAxeptioCookies()"',
                        'href="https://mistral.ai/"')
    html = html.replace('</body>', MENU_SCRIPT + '</body>', 1)
    DESTINATION.write_text(html)
    (ROOT / 'mistral.ai-local-css.json').write_text(
        json.dumps(css_derivatives, indent=2) + '\n')
    print(f'Wrote {DESTINATION.name}; {len(assets)} localized official assets; '
          f'{len(css_derivatives)} CSS derivatives')


if __name__ == '__main__':
    main()
