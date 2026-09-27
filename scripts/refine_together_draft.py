#!/usr/bin/env python3
"""Localize a dated Together AI homepage without its tracking scripts."""

from __future__ import annotations

import hashlib
import json
import os
import re
from html import unescape
from pathlib import Path

from capture_together_assets import official_asset


ROOT = Path(__file__).resolve().parents[1] / '.stitch-work' / 'current-official'
SOURCE = ROOT / 'together.ai-source-current.html'
DESTINATION = ROOT / 'together.ai.html'
ASSETS = ROOT / 'together.ai-assets'
BASE = 'https://www.together.ai/'


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    provenance = json.loads((ROOT / 'together.ai-asset-provenance.json').read_text())
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
            value = unescape(match.group(1).strip().strip('\"\''))
            resolved = official_asset(value, url)
            if not resolved or resolved not in assets:
                return match.group(0)
            relative = os.path.relpath(ASSETS / assets[resolved]['path'],
                                       local.parent)
            return f'url({relative})'

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

    def keep_nontracking_script(match: re.Match[str]) -> str:
        tag = match.group(0)
        attrs, body = match.group(1), match.group(2)
        lowered = (attrs + body).lower()
        if any(term in lowered for term in (
            'app.termly.io', 'cdn.amplitude.com', 'window.amplitude',
            'googletagmanager.com', 'intellimize',
            'cb_debug', 'consent-bridge', '_linkedin_partner_id',
            'window.lintrk', 'wf.onvariationrecorded',
            'cdn.jsdelivr.net/gh/tomasmrazek92/together@',
        )):
            return ''
        return tag

    html = re.sub(r'<script\b([^>]*)>(.*?)</script>', keep_nontracking_script,
                  html, flags=re.I | re.S)
    html = re.sub(r'<noscript>\s*<iframe\b[^>]*googletagmanager[^>]*>'
                  r'\s*</iframe>\s*</noscript>', '', html, flags=re.I | re.S)
    html = re.sub(r'<iframe\b[^>]*googletagmanager[^>]*>\s*</iframe>',
                  '', html, flags=re.I | re.S)
    html = re.sub(r'<img\b[^>]*src="https://px\.ads\.linkedin\.com/'
                  r'[^"]*"[^>]*>', '', html, flags=re.I)
    html = re.sub(r'<img\b[^>]*src="https://cdn\.prod\.website-files'
                  r'\.com/plugins/Basic/assets/placeholder\.60f9b1840c'
                  r'\.svg"[^>]*>', '', html, flags=re.I)
    html = re.sub(r'<link\b[^>]*\brel="prefetch"[^>]*>', '', html, flags=re.I)
    html = re.sub(r'<link\b[^>]*\brel="preconnect"[^>]*>', '', html, flags=re.I)

    for url, item in sorted(assets.items(), key=lambda pair: -len(pair[0])):
        local = css_replacements.get(url, 'together.ai-assets/' + item['path'])
        html = html.replace(url, local).replace(url.replace('&', '&amp;'), local)

    # Relative navigation should lead to the actual brand site, rather than
    # nonexistent paths on this collection's hosting domain.
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
    DESTINATION.write_text(html)
    (ROOT / 'together.ai-local-css.json').write_text(
        json.dumps(css_derivatives, indent=2) + '\n')
    print(f'Wrote {DESTINATION.name}; {len(assets)} official assets; '
          f'{len(css_derivatives)} CSS derivatives')


if __name__ == '__main__':
    main()
