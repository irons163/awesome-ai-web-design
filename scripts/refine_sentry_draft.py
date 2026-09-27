#!/usr/bin/env python3
"""Prepare a dated Sentry homepage snapshot for static review hosting."""

from __future__ import annotations

import hashlib
import json
import os
import re
from html import unescape
from pathlib import Path
from urllib.parse import urlsplit

from capture_sentry_assets import public_asset


ROOT = Path(__file__).resolve().parents[1] / '.stitch-work' / 'current-official'
SOURCE = ROOT / 'sentry-source-current.html'
DESTINATION = ROOT / 'sentry.html'
ASSETS = ROOT / 'sentry-assets'
BASE = 'https://sentry.io/'


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    provenance = json.loads((ROOT / 'sentry-asset-provenance.json').read_text())
    assets = {item['url']: item for item in provenance}
    css_derivatives = []
    css_replacements = {}
    for url, item in assets.items():
        if not item['path'].endswith('.css'):
            continue
        original = ASSETS / item['path']
        local = original.with_name(original.stem + '.local.css')
        css = original.read_text(errors='replace')

        def rewrite_css_url(match: re.Match[str]) -> str:
            value = unescape(match.group(1).strip().strip('"\''))
            resolved = public_asset(value, url)
            if not resolved:
                return match.group(0)
            if resolved in assets:
                relative = os.path.relpath(ASSETS / assets[resolved]['path'],
                                           local.parent)
                return f'url({relative})'
            return f'url({resolved})'

        css = re.sub(r'url\(\s*([^)]+)\s*\)', rewrite_css_url, css)
        local.write_text(css)
        path = local.relative_to(ROOT).as_posix()
        css_replacements[url] = path
        css_derivatives.append({
            'source_url': url,
            'source_sha256': item['sha256'],
            'local_path': path,
            'local_sha256': sha256(local),
        })

    html = SOURCE.read_text()
    # The original inline scripts include telemetry, OAuth sign-up handling,
    # runtime module imports and a newsletter form. This copy is visual only.
    html = re.sub(r'<script\b[^>]*>.*?</script>', '', html, flags=re.I | re.S)
    html = re.sub(r'<noscript\b[^>]*>.*?</noscript>', '', html,
                  flags=re.I | re.S)
    html = re.sub(r'<link\b[^>]*\brel="preconnect"[^>]*>', '', html,
                  flags=re.I)
    for url, item in sorted(assets.items(), key=lambda pair: -len(pair[0])):
        local = css_replacements.get(url, 'sentry-assets/' + item['path'])
        relative_url = urlsplit(url).path
        if urlsplit(url).query:
            relative_url += '?' + urlsplit(url).query
        for original in (url, relative_url):
            html = html.replace(original, local)
            html = html.replace(original.replace('&', '&amp;'), local)

    # Internal navigation in a standalone catalog draft must open the actual
    # Sentry site; remaining static media also uses Sentry's public origin.
    html = re.sub(r'(<a\b[^>]*\bhref=")(/[^" ]*)(")',
                  lambda m: m.group(1) +
                  (m.group(2) if m.group(2).startswith('//') else
                   BASE.rstrip('/') + m.group(2)) + m.group(3),
                  html, flags=re.I)
    html = re.sub(r'(<form\b[^>]*\baction=")(/[^" ]*)(")',
                  lambda m: m.group(1) + BASE.rstrip('/') +
                  m.group(2) + m.group(3), html, flags=re.I)
    html = re.sub(r'((?:src|poster|data-src)=")(/[^" ]*)(")',
                  lambda m: m.group(1) +
                  (m.group(2) if m.group(2).startswith('//') else
                   BASE.rstrip('/') + m.group(2)) + m.group(3),
                  html, flags=re.I)

    # Sentry's server-rendered mobile menu and tab classes already include
    # their original styling. Restore only local disclosure behavior.
    behavior = '''<style>
[data-menu-dropdown].draft-open{display:block!important}
</style><script>
(() => {
  const mobileButton = document.getElementById('menu-toggle-button');
  const mobileMenu = document.getElementById('mobileMenu');
  mobileButton?.addEventListener('click', () => {
    const open = !mobileMenu.classList.contains('nav-expanded');
    mobileMenu.classList.toggle('nav-expanded', open);
    mobileButton.setAttribute('aria-expanded', String(open));
  });
  for (const button of document.querySelectorAll('button[id^="trigger-"][aria-controls]')) {
    button.addEventListener('click', () => {
      const next = button.getAttribute('aria-expanded') !== 'true';
      button.setAttribute('aria-expanded', String(next));
    });
  }
  const dropdowns = [...document.querySelectorAll('button[data-menu-trigger]')];
  for (const button of dropdowns) {
    button.addEventListener('click', () => {
      const menu = document.querySelector('[data-menu-dropdown="' + button.dataset.menuTrigger + '"]');
      const next = !menu?.classList.contains('draft-open');
      for (const other of dropdowns) {
        other.setAttribute('aria-expanded', 'false');
        document.querySelector('[data-menu-dropdown="' + other.dataset.menuTrigger + '"]')?.classList.remove('draft-open');
      }
      menu?.classList.toggle('draft-open', next);
      button.setAttribute('aria-expanded', String(next));
    });
  }
  for (const root of document.querySelectorAll('[id^="tabbed-"]')) {
    root.addEventListener('click', event => {
      const button = event.target.closest('.tab-button');
      if (!button || !root.contains(button)) return;
      const id = button.dataset.tab;
      root.querySelectorAll('.tab-item.active,[class*="tab-img-"].active').forEach(el => el.classList.remove('active'));
      button.closest('.tab-item')?.classList.add('active');
      root.querySelectorAll('.tab-img-' + id).forEach(el => el.classList.add('active'));
    });
  }
  document.getElementById('mkto_1942')?.addEventListener('submit', event => {
    event.preventDefault();
    window.location.assign('https://sentry.io/welcome/');
  });
})();
</script>'''
    html = html.replace('</body>', behavior + '</body>', 1)
    DESTINATION.write_text(html)
    (ROOT / 'sentry-local-css.json').write_text(
        json.dumps(css_derivatives, indent=2) + '\n')
    print(f'Wrote {DESTINATION.name}; {len(assets)} official public assets; '
          f'{len(css_derivatives)} CSS derivatives')


if __name__ == '__main__':
    main()
