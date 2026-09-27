#!/usr/bin/env python3
"""Build a source-backed Mintlify draft from the dated native Stitch screen.

The original Stitch exports remain untouched. The live website was observed on
2026-09-28. This is still a visual-review draft, not an accepted replica.
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / '.stitch-work' / 'current-official'
ASSETS = WORK / 'mintlify-assets'
BASE = 'https://www.mintlify.com'


def official(path: str) -> str:
    return path if path.startswith('https://') else BASE + path


def link(path: str, label: str, css_class: str = '') -> str:
    return (f'<a class="{css_class}" href="{html.escape(official(path), quote=True)}">'
            f'{html.escape(label)}<span aria-hidden="true"> ↗</span></a>')


def wordmark() -> str:
    svg = (ASSETS / 'cee64add09c6539f.svg').read_text()
    return svg.replace('var(--color-text-main)', '#f7f8f7')


def filaments(prefix: str, count: int, width: int, height: int) -> str:
    """Restrained thin curves reconstructed from the official canvas."""
    paths = []
    for i in range(count):
        if prefix == 'hero':
            x0, y0 = -140 + 18 * i, 922 + 3 * i
            x1, y1 = 740 + 8 * i, 344 - 2 * i
            x2, y2 = 1290, 95 + 7 * i
            d = (f'M{x0} {y0} C{540 + i * 5} {y0 - 75},'
                 f'{x1 - 60} {y1 + 75},{x1} {y1} '
                 f'S{1130 + i * 3} {y2 + 85},{x2} {y2}')
        else:
            d = (f'M{-90 + i * 14} {height - 30 + i * 2} '
                 f'C{width * .38:.0f} {height * .38 + i * 5:.0f},'
                 f'{width * .62:.0f} {height * .76 - i * 4:.0f},'
                 f'{width + 45} {25 + i * 7}')
        color = '#9bcf37' if i % 5 == 0 else '#25c99a'
        paths.append(f'<path d="{d}" stroke="{color}" stroke-opacity="{.34 + (i % 4) * .1:.2f}" stroke-width=".7"/>')
    return (f'<svg class="filaments {prefix}-filaments" viewBox="0 0 {width} {height}" '
            'preserveAspectRatio="none" fill="none" aria-hidden="true">'
            + ''.join(paths) + '</svg>')


def header() -> str:
    menus = {
        'Products': [('/docs', 'Documentation'), ('/search-index', 'Index'), ('/score', 'Agent score')],
        'Solutions': [('/startups', 'Startups'), ('/enterprise', 'Enterprise'), ('/switch', 'Switch to Mintlify')],
        'Resources': [('/customers', 'Customers'), ('/blog', 'Blog'), ('/guides/introduction', 'Guides')],
    }
    nav = ''.join('<details class="nav-menu"><summary>' + name + '</summary><div class="menu-panel">'
                  + ''.join(link(path, text) for path, text in entries) + '</div></details>'
                  for name, entries in menus.items())
    return f'''<aside class="report-bar"><a href="{BASE}/state-of-knowledge/2026">
      <span class="report-chip">▥&nbsp; Featured report</span><span>The 2026 State of Knowledge Report</span>
      <span class="report-read">Read the research&nbsp; ›</span></a></aside>
<header class="top-nav"><div class="nav-inner">
  <a class="wordmark" href="{BASE}/" aria-label="Mintlify official website">{wordmark()}</a>
  <nav aria-label="Primary navigation">{nav}<a href="{BASE}/pricing">Pricing</a></nav>
  <div class="nav-actions"><a class="sign-in" href="https://app.mintlify.com">Sign in</a>
    <a class="button white" href="{BASE}/contact/sales">Contact sales</a></div>
</div></header>'''


def hero() -> str:
    return f'''<section class="hero" aria-labelledby="hero-title">
  {filaments('hero', 27, 1280, 995)}
  <div class="hero-copy"><div class="traffic-chip"><span>Agent traffic</span><strong>68.8%</strong><span aria-hidden="true">›</span></div>
    <h1 id="hero-title">The knowledge<br>infrastructure<br>agents build on</h1>
    <p>Self-updating documentation for startups,<br class="desktop-only"> enterprises, and agents.</p>
    <div class="hero-actions"><a class="button white" href="https://app.mintlify.com/signup">Get started <span aria-hidden="true">›</span></a>
      <a class="button ghost" href="https://app.mintlify.com/api/auth/google/discovery"><b class="google-g">G</b>Sign up with Google</a></div>
  </div>
  <img class="docs-preview" src="mintlify-assets/3ff34f45c36d44db.svg"
    width="1080" height="656" alt="Mintlify dark documentation preview showing API Reference and the Quickstart Guide">
</section>'''


def logo_grid() -> str:
    logos = [
        ('Microsoft', '<span class="microsoft-mark"><i></i><i></i><i></i><i></i></span><b>Microsoft</b>'),
        ('Anthropic', '<img src="mintlify-assets/71d89fce50605060.svg" alt="Anthropic">'),
        ('Amazon', '<img src="mintlify-assets/39dfbe732951e147.svg" alt="Amazon">'),
        ('Coinbase', '<b class="coinbase-word">coinbase</b>'),
        ('Cognition', '<img src="mintlify-assets/da778c0690940ce4.svg" alt="Cognition">'),
        ('Solana', '<img src="mintlify-assets/c852f85ab15aab1b.svg" alt="Solana">'),
        ('AT&amp;T', '<img src="mintlify-assets/e35ad5544f9af52d.svg" alt="AT&amp;T">'),
        ('Rivian', '<b class="rivian-word">RIVIAN</b>'),
    ]
    cells = ''.join(f'<div class="logo-cell" aria-label="{name}">{image}</div>' for name, image in logos)
    stats = [
        ('Pages read', '10,759,862'), ('Search requests', '131,135'),
        ('API requests', '22,105'), ('Feedback provided', '3,105'),
        ('Content updates', '21,841'),
    ]
    ticker = ''.join(f'<span><small>{label}</small><strong>{value}</strong></span>' for label, value in stats)
    return f'''<section class="customers-logos" aria-label="Customer logos and observed agent activity">
  <div class="logo-inner"><div class="logo-intro"><h2>Join 20,000+ of the world's most ambitious companies building for agents.</h2>
    <a class="button white" href="{BASE}/customers">Read customer stories <span aria-hidden="true">›</span></a></div>
    <div class="logo-grid">{cells}</div></div>
  <div class="stats-strip"><div class="stats-inner"><b>Agents at work today</b><div class="stats-values">{ticker}</div></div></div>
</section>'''


def bento() -> str:
    paths = filaments('card', 12, 695, 330)
    ui_lines = '<i></i><i></i><i></i><i></i>'
    return f'''<section class="bento section-shell" aria-labelledby="bento-title">
  <div class="section-inner"><div class="section-head bento-head"><h2 id="bento-title">One platform for your<br>entire knowledge stack.<br><span>Agents that keep work moving 24/7.</span></h2>
    <a class="button white" href="https://app.mintlify.com/signup">Get started <span aria-hidden="true">›</span></a></div>
  <div class="bento-grid">
    <article class="feature-card feature-wide">{paths}<div class="art-window"><span>mintlify</span><i></i><i></i><i></i></div><h3>Agent-native platform</h3></article>
    <article class="feature-card feature-narrow"><div class="update-art"><span class="update-dot"></span>{ui_lines}</div>{filaments('card', 8, 340, 340)}<h3>Self-updating knowledge</h3></article>
    <article class="feature-card"><div class="access-art"><div><i></i><i></i><small>Editor</small></div><div class="active"><i></i><i></i><small>Admin</small></div><div><i></i><i></i><small>Collaborator</small></div></div><h3>Control who has access</h3></article>
    <article class="feature-card"><div class="systems-art">{filaments('card', 10, 340, 320)}<span>✳</span><span>▲</span><span>◎</span></div><h3>Connect with your systems</h3></article>
    <article class="feature-card"><div class="collab-art"><div class="file-tabs"><span>▣&nbsp; Guide.md</span><span>LLMS.txt</span><span>MCP</span><span>Skill.md</span></div><div class="file-lines">{ui_lines}<em>Agent 130</em><em>User 007</em></div></div><h3>Collaborate with your team &amp; agents</h3></article>
    <article class="feature-card feature-full"><div class="config-art"><div class="config-sidebar"><i></i><i></i><i></i><i></i></div><div class="config-screen"><span>Configuration</span><i></i><i></i><i></i><i></i></div></div>{filaments('card', 13, 1052, 360)}<h3>Build on top of your existing setup</h3></article>
  </div></div>
</section>'''


def enterprise() -> str:
    stories = [
        ('Anthropic', 'See how Anthropic accelerates AI adoption with Mintlify',
         'anthropic-sf.webp', '/customers/anthropic', '2M', 'Monthly active developers', '4+', 'Products serviced', 'anthropic'),
        ('Coinbase', 'How Coinbase became agent-ready with Mintlify',
         'coinbase-ipo.webp', '/customers/coinbase', '+50x', 'Faster deployment time', '12+', 'Products serviced', 'coinbase'),
        ('HubSpot', 'How HubSpot powers next-gen developer experience with Mintlify',
         'hubspot-conference.webp', '/customers/hubspot', '3x', 'Faster build times', '50%', 'Reduction in engineering resources', 'hubspot'),
        ('AT&T', 'See how AT&T modernized their knowledge infrastructure with Mintlify',
         'att-photo.webp', '/customers/att', '50K+', 'Monthly active users', '4+', 'Products serviced', 'att'),
    ]
    cards = ''.join(f'''<a class="story-card {theme}" href="{BASE}{path}">
      <div class="story-copy"><span class="story-brand">{html.escape(brand)}</span><h3>{html.escape(title)}</h3>
        <div class="story-metrics"><div><strong>{first}</strong><small>{html.escape(first_label)}</small></div>
          <div><strong>{second}</strong><small>{html.escape(second_label)}</small></div></div>
        <span class="story-read">Read the story <span aria-hidden="true">›</span></span></div>
      <img src="mintlify-assets/{image}" alt="{html.escape(brand)} customer story photograph" loading="lazy"></a>'''
                    for brand, title, image, path, first, first_label, second, second_label, theme in stories)
    return f'''<section class="enterprise section-shell" aria-labelledby="enterprise-title"><div class="section-inner">
      <div class="section-head enterprise-head"><h2 id="enterprise-title">Powering businesses of all sizes.<br><span>Run your business on a reliable platform that adapts to your needs.</span></h2>
        <div class="head-actions"><button class="arrow" type="button" data-slide="previous" aria-label="Previous customer story">‹</button>
          <button class="arrow" type="button" data-slide="next" aria-label="Next customer story">›</button>
          <a class="button white" href="{BASE}/enterprise">For enterprises <span aria-hidden="true">›</span></a></div></div>
      <div class="story-track" id="story-track" tabindex="0" aria-label="Enterprise customer stories">{cards}</div>
    </div></section>'''


def scale() -> str:
    return f'''<section class="scale section-shell" aria-labelledby="scale-title"><div class="section-inner">
      <div class="section-head"><h2 id="scale-title">Built to scale with the agent web.<br><span>Built for scale with enterprise-grade reliability and performance.</span></h2>
        <a class="button white" href="{BASE}/enterprise">For enterprises <span aria-hidden="true">›</span></a></div>
      <div class="scale-art" aria-hidden="true">{filaments('card', 26, 1052, 410)}</div>
      <div class="scale-metrics"><div><strong>300M+</strong><span>visitors in the past year</span></div>
        <div><strong>2B+</strong><span>agents in the past year</span></div>
        <div><strong>99.99%</strong><span>uptime across all services</span></div></div>
    </div></section>'''


def startups() -> str:
    stories = [
        ('Lovable', '5d1d69bded27a71f.webp', '/customers/lovable',
         'Lovable builds its AI-native coding platform and developer experience on top of Mintlify.'),
        ('Kalshi', 'd3c5f87d90d5a90a.webp', '/customers/kalshi',
         'Kalshi powers its developer documentation with Mintlify.'),
        ('Decagon', '09c00b59eb5ad1b5.webp', '/customers/decagon',
         'Decagon ships sleek, AI-native documentation built on Mintlify.'),
        ('Replit', 'e4eb840e14c0eb73.webp', '/customers/replit',
         'Learn how Replit uses Mintlify to turn documentation into a fast, collaborative, and accessible experience.'),
    ]
    cards = ''.join(f'''<a class="startup-card" href="{BASE}{path}"><img src="mintlify-assets/{image}"
         alt="{brand} customer story visual" loading="lazy"><span class="startup-copy"><b>{brand}</b>
         <span>{html.escape(description)}</span><small>Read {brand}'s story&nbsp; ›</small></span></a>'''
                    for brand, image, path, description in stories)
    return f'''<section class="startups section-shell" aria-labelledby="startups-title"><div class="section-inner">
      <div class="section-head startups-head"><h2 id="startups-title">Enabling the next generation of startups.<br>
        <span>Powering a quarter of the last YC batch to 40% of the Forbes AI 50.</span></h2>
        <a class="button white" href="{BASE}/startups">For startups <span aria-hidden="true">›</span></a></div>
      <div class="startup-track">{cards}</div>
    </div></section>'''


def testimonials() -> str:
    quotes = [
        ('Brian Armstrong', 'Co-founder & CEO, Coinbase', 'Yes shout out to Mintlify, great product, worth checking out'),
        ('Guillermo Rauch', 'CEO, Vercel', 'Was wondering how docs.x.com was built because it was so fast & delightful. It’s Mintlify'),
        ('HubSpot', 'Product Manager of Developer Growth', 'Delivering a best-in-class developer experience is non-negotiable for us. That’s why moving our documentation to Mintlify was the obvious choice.'),
        ('Abe Duran', 'Developer Support, Zapier', 'Honestly, we have found it very, very helpful. If I’m honest with you, it’s been one of the best decisions we have taken and we have made in a long time.'),
        ('Dominic Macias', 'Legal Counsel, Axiom', 'Since we adopted Mintlify last year at Axiom, I’ve been more and more delighted with that decision… our customers are getting real value from the AI chat responses.'),
        ('Daksh Gupta', 'CEO, Greptile', 'The idea that devs hate updating docs will be completely lost on the next gen that have always used Mintlify'),
    ]
    cards = ''.join(f'''<blockquote class="quote-card"><div><b>{html.escape(name)}</b><small>{html.escape(role)}</small></div>
        <p>{html.escape(quote)}</p></blockquote>''' for name, role, quote in quotes)
    return f'''<section class="testimonials section-shell" aria-labelledby="testimonials-title"><div class="section-inner">
      <div class="section-head"><h2 id="testimonials-title">Trusted by teams building for agents.</h2>
        <a class="button white" href="{BASE}/wall-of-love">Read more <span aria-hidden="true">›</span></a></div>
      <div class="quote-grid">{cards}</div>
    </div></section>'''


def updates() -> str:
    articles = [
        ('Announcements', 'Aug 6, 2026', 'Introducing Mintlify Index',
         'ee53b059c899c31d.webp', '/blog/mintlify-index'),
        ('AI Trends', 'Jul 29, 2026', 'The state of docs traffic: a 2026 midyear report',
         '5611860d8e36d1dc.webp', '/blog/state-of-docs-traffic'),
        ('Agent Score', 'Apr 27, 2026', 'Can agents read your docs?',
         'd1a4ec1fcebc4175.webp', '/score'),
    ]
    cards = ''.join(f'''<a class="update-card" href="{BASE}{path}"><img src="mintlify-assets/{image}"
      alt="{html.escape(title)} article graphic" loading="lazy"><span class="update-meta">{category}&nbsp; · &nbsp;{date}</span>
      <h3>{html.escape(title)}</h3></a>''' for category, date, title, image, path in articles)
    return f'''<section class="updates section-shell" aria-labelledby="updates-title"><div class="section-inner">
      <div class="section-head"><h2 id="updates-title">Latest updates</h2>
        <a class="button white" href="{BASE}/blog">All posts <span aria-hidden="true">›</span></a></div>
      <div class="update-grid">{cards}</div>
    </div></section>'''


def closing() -> str:
    return f'''<section class="closing section-shell"><div class="section-inner closing-inner">
      <h2>The knowledge platform built for agents</h2><div class="closing-actions">
        <a class="button ghost" href="{BASE}/contact/sales">Talk to sales</a>
        <a class="button white" href="https://app.mintlify.com/signup">Get started <span aria-hidden="true">›</span></a>
      </div></div></section>'''


def footer() -> str:
    columns = [
        ('Explore', [('/startups', 'Startups'), ('/enterprise', 'Enterprise'), ('/build-vs-buy', 'Build vs Buy'),
                     ('/switch', 'Switch'), ('/oss-program', 'OSS program'), ('/desktop', 'Download')]),
        ('Resources', [('https://learn.mintlify.com/', 'Learn'), ('/customers', 'Customers'), ('/blog', 'Blog'),
                       ('/pricing', 'Pricing'), ('/guides/introduction', 'Guides'),
                       ('https://github.com/orgs/mintlify/discussions/categories/feature-requests', 'Feature requests'),
                       ('/library', 'Library'), ('/search-index', 'Index'), ('/wiki', 'Convert from code'), ('/score', 'Agent score')]),
        ('Documentation', [('/docs', 'Getting started'), ('/docs/api/introduction', 'API reference'),
                           ('/docs/components', 'Components'), ('/docs/changelog', 'Changelog')]),
        ('Company', [('/careers', 'Careers'), ('/events', 'Events'), ('/wall-of-love', 'Wall of love'), ('/roadmap', 'Roadmap')]),
        ('Legal', [('/legal/privacy', 'Privacy policy'), ('/security/responsible-disclosure', 'Responsible disclosure'),
                   ('/legal/terms', 'Terms of service'), ('https://security.mintlify.com', 'Security'),
                   ('https://mintlify.typeform.com/to/Bxa77EKc', 'DSR/DSAR')]),
    ]
    cols = ''.join(f'<div><h3>{title}</h3>' + ''.join(f'<a href="{official(path)}">{html.escape(label)}</a>'
                    for path, label in entries) + '</div>' for title, entries in columns)
    return f'''<footer class="footer"><div class="footer-inner"><div class="footer-top">
      <a href="{BASE}/" aria-label="Mintlify official website">{wordmark()}</a>
      <a class="status" href="https://status.mintlify.com/"><span></span>All systems normal</a>
      </div><div class="footer-columns">{cols}</div>
      <div class="footer-bottom"><span>© 2026 Mintlify, Inc.</span>
        <div><a href="https://x.com/mintlify">X</a><a href="https://github.com/mintlify">GitHub</a>
          <a href="https://discord.gg/mintlify">Discord</a></div></div>
    </div></footer>'''


def main() -> None:
    native = (WORK / 'mintlify-stitch-revised.html').read_text()
    required = ['<!-- HERO SECTION -->', '<!-- ASYMMETRIC SIX-CARD BENTO SECTION -->',
                '<!-- ENTERPRISE CUSTOMER STORY CAROUSEL -->',
                '<!-- TRUSTED BY TEAMS BUILDING FOR AGENTS -->', '<!-- DENSE DARK FOOTER -->']
    for marker in required:
        if marker not in native:
            raise ValueError(f'Native Stitch export changed: {marker}')
    style = (ROOT / 'scripts' / 'mintlify_draft_style.css').read_text()
    body = '\n'.join([header(), '<main>', hero(), logo_grid(), bento(), enterprise(), scale(),
                      startups(), testimonials(), updates(), closing(), '</main>', footer()])
    document = f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Mintlify current-official visual reconstruction draft, observed 2026-09-28.">
<title>Mintlify — The Knowledge Platform Built for Agents · Draft</title>
<style>{style}</style></head><body>{body}
<script>
for (const button of document.querySelectorAll('[data-slide]')) {{
  button.addEventListener('click', () => document.getElementById('story-track').scrollBy({{
    left: button.dataset.slide === 'next' ? 840 : -840, behavior: 'smooth'
  }}));
}}
</script></body></html>'''
    (WORK / 'mintlify.html').write_text(document)
    reference = {
        'brand': 'mintlify', 'reference_url': BASE + '/', 'observed_at': '2026-09-28',
        'desktop_reference': {'viewport': [1280, 720], 'page_height': 8497,
                              'hero_heading_xy': [96, 235], 'docs_preview_xy': [511, 456],
                              'bento_heading_y': 1745, 'enterprise_heading_y': 3405,
                              'scale_heading_y': 4269, 'startups_heading_y': 5122,
                              'testimonials_heading_y': 6028, 'updates_heading_y': 6911,
                              'closing_heading_y': 7687},
        'stitch_project': 'projects/8946735483530910971',
        'stitch_design_system': 'assets/15743058118121698181',
        'stitch_initial_screen': 'projects/8946735483530910971/screens/ed7ae5118b734f2284e1741f0ac11212',
        'stitch_revised_screen': 'projects/8946735483530910971/screens/0ddde24254034ea0b7e882dec56bd209',
        'reference_files': ['mintlify-source-2026.html', 'mintlify-asset-provenance.json',
                            'mintlify-stitch.html', 'mintlify-stitch-revised.html'],
        'review_status': 'in_visual_review',
        'known_differences': [
            'The official green line art is canvas animation; the draft uses static SVG curves.',
            'The official activity values update live; the draft shows a dated static snapshot.',
            'The original Stitch export invented endorsements and product details; verified copy and assets replaced them.',
            'Desktop and mobile rendered comparisons remain pending; this draft is not visually accepted.',
        ],
    }
    (WORK / 'mintlify-reference.json').write_text(json.dumps(reference, ensure_ascii=False, indent=2) + '\n')
    print('Built Mintlify current-official draft (still pending visual review).')


if __name__ == '__main__':
    main()
