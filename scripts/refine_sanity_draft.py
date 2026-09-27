#!/usr/bin/env python3
"""Prepare a dated Sanity homepage snapshot for static review hosting."""

from __future__ import annotations

import hashlib
import json
import os
import re
from html import unescape
from pathlib import Path

from capture_sanity_assets import public_asset


ROOT = Path(__file__).resolve().parents[1] / '.stitch-work' / 'current-official'
SOURCE = ROOT / 'sanity-source-current.html'
DESTINATION = ROOT / 'sanity.html'
ASSETS = ROOT / 'sanity-assets'
BASE = 'https://www.sanity.io/'
HOSTED_SUFFIXES = {'.css', '.woff', '.woff2', '.ttf', '.svg', '.webp'}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    provenance = json.loads((ROOT / 'sanity-asset-provenance.json').read_text())
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
            if (not resolved or resolved not in assets or
                    Path(assets[resolved]['path']).suffix not in HOSTED_SUFFIXES):
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
    # Astro hydration bundles are restricted to Sanity's own origin. Removing
    # them also avoids analytics and consent scripts on this read-only copy.
    html = re.sub(r'<script\b[^>]*>.*?</script>', '', html, flags=re.I | re.S)
    html = re.sub(r'<noscript>.*?</noscript>', '', html, flags=re.I | re.S)
    html = re.sub(r'<link\b[^>]*\brel="preconnect"[^>]*>', '', html,
                  flags=re.I)
    for url, item in sorted(assets.items(), key=lambda pair: -len(pair[0])):
        if Path(item['path']).suffix not in HOSTED_SUFFIXES:
            continue
        local = css_replacements.get(url, 'sanity-assets/' + item['path'])
        html = html.replace(url, local).replace(url.replace('&', '&amp;'), local)
        if url.startswith(BASE):
            relative_url = url[len(BASE) - 1:]
            html = html.replace(relative_url, local)
            html = html.replace(relative_url.replace('&', '&amp;'), local)

    # Enable the actual responsive public hero video in the static snapshot.
    # Other official breakpoint variants remain on Sanity's public CDN.
    html = html.replace('data-lazy-video loop muted playsinline preload="none"',
                        'autoplay loop muted playsinline preload="metadata"')
    html = re.sub(r'(<source\b[^>]*?)\bdata-src=', r'\1src=', html,
                  flags=re.I)

    # The navigation is normally hydrated by Astro, so provide a small static
    # equivalent of its observed mobile disclosure without third-party code.
    mobile_menu = '''<dialog id="mobile-menu" class="sanity-official-menu">
      <div class="sanity-menu-head"><strong>Sanity</strong><button type="button" data-menu-back hidden aria-label="Back">‹</button><span data-menu-title hidden></span><button type="button" data-close-menu aria-label="Close menu">×</button></div>
      <nav aria-label="Mobile navigation"><div class="sanity-menu-main"><button type="button" data-open-panel="products">Products <span>›</span></button><button type="button" data-open-panel="solutions">Solutions <span>›</span></button><button type="button" data-open-panel="resources">Resources <span>›</span></button><a href="https://www.sanity.io/docs">Docs</a><a href="https://www.sanity.io/enterprise">Enterprise</a><a href="https://www.sanity.io/pricing">Pricing</a><a href="https://www.sanity.io/entry">Login</a></div>
      <div class="sanity-menu-panel" data-panel="products" hidden><small>CONTENT OPERATIONS</small><a href="https://www.sanity.io/studio">Studio</a><a href="https://www.sanity.io/content-agent">Content Agent</a><a href="https://www.sanity.io/app-sdk">App SDK</a><a href="https://www.sanity.io/media-library">Media Library</a><a href="https://www.sanity.io/content-releases">Content Releases</a><a href="https://www.sanity.io/agent-actions">Agent API</a><small>CONTENT BACKEND</small><a href="https://www.sanity.io/content-lake">Content Lake</a><a href="https://www.sanity.io/context">Sanity Context</a><a href="https://www.sanity.io/mcp">MCP Server</a><a href="https://www.sanity.io/functions">Functions</a><a href="https://www.sanity.io/live-cdn">Live CDN</a></div>
      <div class="sanity-menu-panel" data-panel="solutions" hidden><small>BY INDUSTRY</small><a href="https://www.sanity.io/ecommerce">E-commerce &amp; Retail</a><a href="https://www.sanity.io/media">Media &amp; Publishing</a><a href="https://www.sanity.io/marketing">SaaS</a><small>BY TEAM</small><a href="https://www.sanity.io/developers">Developers</a><a href="https://www.sanity.io/content-editors">Content Editors</a><a href="https://www.sanity.io/product-owners">Product Owners</a><a href="https://www.sanity.io/business-leaders">Business Leaders</a></div>
      <div class="sanity-menu-panel" data-panel="resources" hidden><small>BUILD AND SHARE</small><a href="https://snty.link/101">Sanity 101</a><a href="https://www.sanity.io/learn">Sanity Learn</a><a href="https://www.sanity.io/pioneers">Pioneers</a><a href="https://www.sanity.io/exchange/frameworks">Frameworks</a><a href="https://www.sanity.io/templates">Templates</a><a href="https://www.sanity.io/plugins">Tools and plugins</a><a href="https://www.sanity.io/recipes">Schemas and snippets</a><a href="https://snty.link/community">Join our community</a><small>INSIGHT</small><a href="https://www.sanity.io/blog">Company blog</a><a href="https://www.sanity.io/engineering">Engineering</a><a href="https://www.sanity.io/events">Events &amp; Webinars</a><a href="https://www.sanity.io/customers">Customer stories</a><a href="https://www.sanity.io/blog?category=guide">Guides</a><a href="https://www.sanity.io/use-cases">Use Cases</a></div></nav>
      <div class="sanity-menu-actions"><a href="https://www.sanity.io/get-started">Get started</a><a href="https://www.sanity.io/contact/sales">Contact sales</a></div>
    </dialog>'''
    if '<dialog id="mobile-menu"></dialog>' not in html:
        raise ValueError('Expected mobile dialog was not found')
    html = html.replace('<dialog id="mobile-menu"></dialog>', mobile_menu)
    menu_style = '''<style>
    .sanity-official-menu{position:fixed;inset:0;width:100vw;height:100dvh;max-width:none;max-height:none;margin:0;padding:0 24px 24px;background:#0b0b0b;color:#fff;border:0;box-sizing:border-box;z-index:999999}
    .sanity-official-menu::backdrop{background:#0b0b0b}
    .sanity-menu-head{height:66px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #353535}
    .sanity-menu-head strong{font:700 30px Georgia,serif;letter-spacing:-2px}
    .sanity-menu-head [data-menu-title]{margin-right:auto;text-transform:uppercase;font:14px monospace}
    .sanity-menu-head button{border:0;border-radius:50%;background:#242424;color:white;width:36px;height:36px;font:24px/1 sans-serif;cursor:pointer}
    .sanity-menu-head [data-menu-back]{margin-right:16px}
    .sanity-official-menu nav{height:calc(100dvh - 150px);overflow:auto;padding-top:16px}
    .sanity-official-menu nav a,.sanity-official-menu nav button{display:flex;width:100%;justify-content:space-between;color:white;text-decoration:none;font:24px/1.4 Arial,sans-serif;padding:8px 0;border:0;background:none;text-align:left;cursor:pointer}
    .sanity-menu-panel small{display:block;color:#aaa;margin-top:12px;font:11px/1.5 monospace;letter-spacing:.06em}
    .sanity-menu-panel a{font-size:20px!important}
    .sanity-official-menu [hidden]{display:none!important}
    .sanity-menu-actions{position:absolute;bottom:24px;left:12px;right:12px;display:flex;gap:8px}
    .sanity-menu-actions a{flex:1;border-radius:999px;padding:13px 8px;text-align:center;text-decoration:none;text-transform:uppercase;font:12px/1.2 monospace;background:#ff5500;color:#0b0b0b}
    .sanity-menu-actions a+a{background:white}
    </style>'''
    html = html.replace('</head>', menu_style + '</head>')
    menu_script = '''<script>
    (()=>{const open=document.querySelector('button[aria-controls="mobile-menu"]');const dialog=document.getElementById('mobile-menu');if(!open||!dialog)return;const main=dialog.querySelector('.sanity-menu-main'),back=dialog.querySelector('[data-menu-back]'),title=dialog.querySelector('[data-menu-title]'),logo=dialog.querySelector('strong');const reset=()=>{main.hidden=false;back.hidden=true;title.hidden=true;logo.hidden=false;for(const p of dialog.querySelectorAll('[data-panel]'))p.hidden=true};open.addEventListener('click',()=>{reset();dialog.showModal()});dialog.querySelector('[data-close-menu]').addEventListener('click',()=>dialog.close());back.addEventListener('click',reset);for(const button of dialog.querySelectorAll('[data-open-panel]'))button.addEventListener('click',()=>{main.hidden=true;back.hidden=false;title.hidden=false;logo.hidden=true;title.textContent=button.textContent.trim();dialog.querySelector('[data-panel="'+button.dataset.openPanel+'"]').hidden=false});})();
    </script>'''
    html = html.replace('</body>', menu_script + '</body>')

    # Relative navigation must reach the actual brand site, not this catalog.
    html = re.sub(r'(<a\b[^>]*\bhref=")(/[^"]*)(")',
                  lambda m: m.group(1) +
                  (m.group(2) if m.group(2).startswith('//') else
                   BASE.rstrip('/') + m.group(2)) + m.group(3),
                  html, flags=re.I)
    html = re.sub(r'(<form\b[^>]*\baction=")(/[^"]*)(")',
                  lambda m: m.group(1) + BASE.rstrip('/') +
                  m.group(2) + m.group(3), html, flags=re.I)
    # Uncaptured root-relative icons and media can still load from Sanity.
    html = re.sub(r'((?:src|poster|href)=")(/[^"]*)(")',
                  lambda m: m.group(1) +
                  (m.group(2) if m.group(2).startswith('//') else
                   BASE.rstrip('/') + m.group(2)) + m.group(3),
                  html, flags=re.I)
    DESTINATION.write_text(html)
    (ROOT / 'sanity-local-css.json').write_text(
        json.dumps(css_derivatives, indent=2) + '\n')
    print(f'Wrote {DESTINATION.name}; {len(assets)} public assets; '
          f'{len(css_derivatives)} CSS derivatives')


if __name__ == '__main__':
    main()
