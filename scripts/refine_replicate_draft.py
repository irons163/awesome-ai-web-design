#!/usr/bin/env python3
"""Make a dated static Replicate draft from public server-rendered markup."""

from __future__ import annotations

import hashlib
import json
import os
import re
from html import unescape
from pathlib import Path

from capture_replicate_assets import official_asset


ROOT = Path(__file__).resolve().parents[1] / '.stitch-work' / 'current-official'
SOURCE = ROOT / 'replicate-source-current.html'
DESTINATION = ROOT / 'replicate.html'
ASSETS = ROOT / 'replicate-assets'
BASE = 'https://replicate.com/'

INTERACTIONS = '''<script>
(() => {
  const menuButton = document.querySelector('.v2-header-mobile-nav button');
  const mobilePanel = document.querySelector('.v2-header-mobile-nav-disclosure');
  if (menuButton && mobilePanel) {
    function showMenu(open) {
      mobilePanel.hidden = !open;
      mobilePanel.style.display = open ? '' : 'none';
      menuButton.setAttribute('aria-expanded', String(open));
    }
    menuButton.addEventListener('click', () => showMenu(menuButton.getAttribute('aria-expanded') !== 'true'));
    mobilePanel.querySelectorAll('a').forEach(link => link.addEventListener('click', () => showMenu(false)));
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape') showMenu(false);
    });
  }
  const dismiss = document.querySelector('.v2-banner-close-button');
  dismiss?.addEventListener('click', () => {
    document.querySelector('.v2-banner')?.remove();
    document.querySelector('.v2-header')?.setAttribute('data-has-banner', 'false');
  });
  const snippet = document.querySelector('#code-snippet');
  snippet?.querySelectorAll('[role="tab"]').forEach(tab => {
    tab.addEventListener('click', () => {
      snippet.querySelectorAll('[role="tab"]').forEach(item => {
        item.setAttribute('aria-selected', String(item === tab));
      });
      snippet.querySelectorAll('[role="tabpanel"]').forEach(panel => {
        const open = panel.getAttribute('aria-labelledby') === tab.id;
        panel.hidden = !open;
        panel.style.display = open ? '' : 'none';
        panel.setAttribute('data-open', String(open));
      });
    });
  });
})();
</script>'''


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    provenance = json.loads((ROOT / 'replicate-asset-provenance.json').read_text())
    assets = {item['url']: item for item in provenance}
    stylesheets = []
    replacements = {}
    for url, item in assets.items():
        if not item['path'].endswith('.css'):
            continue
        original = ASSETS / item['path']
        local = original.with_name(original.stem + '.local.css')
        css = original.read_text(errors='replace')

        def rewrite_css_url(match: re.Match[str]) -> str:
            value = unescape(match.group(1).strip().strip('"\''))
            resolved = official_asset(value, url)
            if not resolved or resolved not in assets:
                return match.group(0)
            relative = os.path.relpath(ASSETS / assets[resolved]['path'], local.parent)
            return f'url({relative})'

        css = re.sub(r'url\(\s*([^)]+)\s*\)', rewrite_css_url, css)
        local.write_text(css)
        relative = local.relative_to(ROOT).as_posix()
        replacements[url] = relative
        stylesheets.append({
            'source_url': url,
            'source_sha256': item['sha256'],
            'local_path': relative,
            'local_sha256': sha256(local),
        })

    html = SOURCE.read_text()
    # The public page is server-rendered. Its React Router hydration and
    # streaming scripts would fetch private app state on this static host.
    html = re.sub(r'<script\b[^>]*>.*?</script>', '', html, flags=re.I | re.S)
    html = re.sub(r'<link\b[^>]*rel="modulepreload"[^>]*>', '', html, flags=re.I)
    html = re.sub(r'<link\b[^>]*rel="preconnect"[^>]*>', '', html, flags=re.I)
    html = html.replace('<html lang="en" class="">', '<html lang="en" class="dark">', 1)
    for url, item in sorted(assets.items(), key=lambda pair: -len(pair[0])):
        local = replacements.get(url, 'replicate-assets/' + item['path'])
        html = html.replace(url, local).replace(url.replace('&', '&amp;'), local)
    # React's inline SVG data URIs contain literal url(%23gradient) calls.
    # Encode the parentheses within the data URI without changing its SVG.
    html = re.sub(r'url\(%23([^)]+)\)', r'url%28%23\1%29', html)
    # Absolute official links remain live. Root-relative links should also
    # resolve to the real brand site instead of this collection's static host.
    html = re.sub(
        r'(<a\b[^>]*\bhref=")(/[^"]*)(")',
        lambda match: match.group(1) +
        (match.group(2) if match.group(2).startswith('//') else
         BASE.rstrip('/') + match.group(2)) + match.group(3),
        html, flags=re.I,
    )
    html = re.sub(
        r'(<form\b[^>]*\baction=")(/[^"]*)(")',
        lambda match: match.group(1) + BASE.rstrip('/') +
        match.group(2) + match.group(3),
        html, flags=re.I,
    )
    html = html.replace('</body>', INTERACTIONS + '</body>', 1)
    DESTINATION.write_text(html)
    (ROOT / 'replicate-local-css.json').write_text(
        json.dumps(stylesheets, indent=2) + '\n')
    print(f'Wrote {DESTINATION.name}; {len(assets)} official assets; '
          f'{len(stylesheets)} local CSS derivatives')


if __name__ == '__main__':
    main()
