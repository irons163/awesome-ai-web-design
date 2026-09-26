#!/usr/bin/env python3
"""Source-ground a native Stitch export against the saved Stripe en-CA HTML.

The 2026-09-22 capture has no accepted visual comparison with the current site.
Keep stripe-stitch.html and its screenshot unchanged for provenance.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
html = (ROOT / 'stripe-stitch.html').read_text()


def once(old: str, new: str) -> None:
    global html
    assert html.count(old) == 1, old[:90]
    html = html.replace(old, new, 1)


def section(start: str, end: str, replacement: str) -> None:
    global html
    assert html.count(start) == 1 and end in html, (start, end)
    a = html.index(start)
    b = html.index(end, a)
    html = html[:a] + replacement + html[b:]


wave = 'https://b.stripecdn.com/mkt-ssr-statics/assets/_next/static/media/wave-fallback-desktop-1x.fba6fa88.webp'
payment = 'https://images.stripeassets.com/fzn2n1nzq965/vYmk6v8n7oDAwbDpwhjV6/846f9b3e214549b8f14e2b8c8cfe9343/payment-bento-background.jpg?w=860&q=80'
connect = 'https://images.stripeassets.com/fzn2n1nzq965/3NcSrMqMgaKe75QNr8wZI8/46d520dfc48c5b9f1c59dcde9460b58c/connect-bento-card-background-image.jpg?w=1232&q=90'
hertz = 'https://images.stripeassets.com/fzn2n1nzq965/24BNV3GGtvCprFLrYovyaa/b2eac20a1d5ec75e4bff3888b998d163/enterprise-accordion-hertz.png?w=296&q=90'

once('<title>Stripe | Financial Infrastructure for the Internet (Canada)</title>',
     '<title>Stripe | Financial Infrastructure to Grow Your Revenue</title>')
match = re.search(r'https://lh3\.googleusercontent\.com/aida-public/[^\']+', html)
assert match, 'Stitch hero image changed'
html = html[:match.start()] + wave + html[match.end():]
once('class="relative overflow-hidden pt-8 pb-32 lg:pt-14 lg:pb-44"',
     'class="stripe-hero relative overflow-hidden pt-8 pb-32 lg:pt-14 lg:pb-44"')
once('</style>', '''@font-face{font-family:StripeSohne;src:url(https://b.stripecdn.com/mkt-ssr-statics/assets/_next/static/media/Sohne.cb178166.woff2) format('woff2');font-display:swap}
body{font-family:StripeSohne,Inter,Arial,sans-serif;color:#0d253d}
.stripe-hero h1{font-weight:300;letter-spacing:-.03em;line-height:1.04}
.stripe-nav{position:relative;z-index:50;background:#fff;border-bottom:1px solid #e6e8ef}.stripe-nav-inner{max-width:1280px;margin:auto;display:flex;align-items:center;justify-content:space-between;gap:28px;padding:18px 24px}.stripe-logo{font-weight:800;font-size:27px;letter-spacing:-.08em;color:#635bff;transform:skewX(-8deg)}.stripe-links,.stripe-actions{display:flex;align-items:center;gap:24px}.stripe-nav a{text-decoration:none;font-size:14px;font-weight:600}.stripe-join{background:#635bff;color:white;padding:8px 15px;border-radius:100px}.stripe-menu{display:none}
.stripe-art{position:relative;min-height:520px;display:flex;align-items:center;justify-content:center}.stripe-art>img{width:min(100%,590px);border-radius:12px;box-shadow:0 20px 55px #272b6540}.stripe-art-card{position:absolute;right:0;bottom:8%;width:250px;background:#fff;border:1px solid #dfe4ef;box-shadow:0 18px 40px #20265a25;padding:18px;border-radius:12px}.stripe-art-card b{display:block;font-size:16px}.stripe-art-card p{font-size:13px;line-height:1.5;margin:8px 0 0}
.stripe-section{padding:100px 24px}.stripe-section-inner{max-width:1280px;margin:auto}.stripe-section h2{font-size:clamp(32px,4vw,56px);font-weight:300;line-height:1.08;letter-spacing:-.035em;max-width:790px;margin:0 0 20px}.stripe-section-intro{font-size:18px;line-height:1.6;max-width:730px;margin:0 0 50px;color:#43546b}.stripe-solutions{background:#f6f9fc}.stripe-solutions-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}.stripe-solution{display:flex;min-height:260px;flex-direction:column;justify-content:space-between;background:white;border:1px solid #e4eaf1;padding:26px;border-radius:12px;overflow:hidden}.stripe-solution h3{font-size:22px;font-weight:400;line-height:1.2;max-width:330px}.stripe-solution a{font-size:14px;color:#635bff;font-weight:600}.stripe-solution img{width:100%;height:165px;object-fit:cover;border-radius:8px;margin-top:20px}.stripe-solution.feature{grid-column:span 2;background:#eceaff}
.stripe-metrics{background:#fff}.stripe-metric-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:28px;border-top:1px solid #d7e0ea;border-bottom:1px solid #d7e0ea;padding:30px 0}.stripe-metric-grid strong{display:block;font-size:clamp(30px,3vw,46px);font-weight:500;letter-spacing:-.04em}.stripe-metric-grid span{display:block;color:#43546b;font-size:14px;line-height:1.4}
.stripe-case{background:#f6f9fc}.stripe-case-card{display:grid;grid-template-columns:1.15fr .85fr;gap:36px;align-items:center;background:white;border:1px solid #e1e7ee;padding:36px;border-radius:12px}.stripe-case-card h3{font-size:32px;font-weight:400;line-height:1.15}.stripe-case-card p{color:#43546b;line-height:1.6}.stripe-case-card img{width:100%;height:350px;object-fit:cover;border-radius:8px}.stripe-case-card a{color:#635bff;font-weight:600}
.stripe-footer{background:#f6f9fc;padding:60px 24px;color:#43546b}.stripe-footer-inner{max-width:1280px;margin:auto;display:grid;grid-template-columns:repeat(5,1fr);gap:24px}.stripe-footer b{display:block;color:#0d253d;margin-bottom:12px}.stripe-footer a{display:block;color:#43546b;font-size:13px;line-height:2;text-decoration:none}.stripe-footer a:hover{text-decoration:underline}.stripe-footer small{grid-column:1/-1;border-top:1px solid #dce5ef;padding-top:24px}
@media(max-width:800px){.stripe-links,.stripe-actions a:not(.stripe-join){display:none}.stripe-menu{display:block}.stripe-art{min-height:390px}.stripe-art-card{right:0;bottom:0;width:190px}.stripe-solutions-grid{grid-template-columns:1fr 1fr}.stripe-solution.feature{grid-column:span 2}.stripe-metric-grid{grid-template-columns:repeat(2,1fr)}.stripe-case-card{grid-template-columns:1fr}.stripe-footer-inner{grid-template-columns:repeat(3,1fr)}}
@media(max-width:560px){.stripe-solutions-grid,.stripe-metric-grid{grid-template-columns:1fr}.stripe-solution.feature{grid-column:span 1}.stripe-footer-inner{grid-template-columns:repeat(2,1fr)}.stripe-art{min-height:340px}.stripe-art-card{width:155px;padding:12px}}
</style>''')

header = '''<header class="stripe-nav"><div class="stripe-nav-inner"><a class="stripe-logo" href="https://stripe.com/en-ca">stripe</a><nav class="stripe-links" aria-label="Main navigation"><a href="https://stripe.com/en-ca/payments">Products</a><a href="https://stripe.com/en-ca/solutions">Solutions</a><a href="https://docs.stripe.com/">Developers</a><a href="https://stripe.com/en-ca/resources">Resources</a><a href="https://stripe.com/en-ca/pricing">Pricing</a></nav><div class="stripe-actions"><a href="https://dashboard.stripe.com/login">Sign in</a><a href="https://stripe.com/en-ca/contact/sales">Contact sales</a><a class="stripe-join" href="https://dashboard.stripe.com/register">Start now →</a></div><span class="stripe-menu" aria-hidden="true">☰</span></div></header>\n'''
section('<!-- TopNavBar (Shared Component JSON Conformance) -->', '<!-- Hero Section -->', header)
section('<!-- Live Ticker Eyebrow -->', '<!-- Main Headline -->',
        '<p class="text-xs font-semibold tracking-wide text-[#0d253d] mb-6">Global GDP running on Stripe:</p>\n')
section('<!-- CTA Buttons -->', '<!-- Hero Layered Graphical UI Showcase (Right) -->',
        '''<div class="flex flex-wrap items-center gap-4"><a class="inline-flex items-center gap-2 px-6 py-3 rounded-full bg-[#0d253d] text-white font-semibold" href="https://dashboard.stripe.com/register">Get started →</a><a class="inline-flex items-center gap-2 px-6 py-3 rounded-full bg-white text-[#0d253d] border border-[#cbd5e1] font-semibold" href="https://dashboard.stripe.com/register">Sign up with Google</a></div></div>\n''')
right = f'''<div class="stripe-art lg:col-span-6"><img src="{payment.replace('&', '&amp;')}" alt="Stripe payments artwork from the saved public homepage"><div class="stripe-art-card"><b>Pro Plan</b><p>Billed monthly</p><p>Tokens · CA$0.01 per 1,000 units</p><p>Usage meter</p></div></div></div>\n'''
section('<!-- Hero Layered Graphical UI Showcase (Right) -->', '</section>', right)

solutions = [
    ('Accept and optimise payments globally – online and in person', 'https://stripe.com/en-ca/payments', payment),
    ('Enable any billing model', 'https://stripe.com/en-ca/billing', ''),
    ('Monetise through agentic commerce', 'https://stripe.com/en-ca', ''),
    ('Create a card issuing programme', 'https://stripe.com/en-ca/issuing', ''),
    ('Access borderless money movement with stablecoins and crypto', 'https://stripe.com/en-ca', ''),
    ('Embed payments in your platform', 'https://stripe.com/en-ca/connect', connect),
]
cards = []
for i, (title, link, image) in enumerate(solutions):
    art = f'<img src="{image.replace("&", "&amp;")}" alt="">' if image else ''
    cards.append(f'<article class="stripe-solution{" feature" if i == 0 else ""}"><h3>{title}</h3>{art}<a href="{link}">Explore →</a></article>')
grid = '''<section class="stripe-section stripe-solutions"><div class="stripe-section-inner"><h2>Flexible solutions for every business model.</h2><p class="stripe-section-intro">Grow your business with a comprehensive set of payments and financial tools⁠ – designed to work individually or together.</p><div class="stripe-solutions-grid">''' + ''.join(cards) + '''</div></div></section>\n'''
section('<!-- Solutions Grid Section -->', '<!-- Enterprise Proof & Metrics Section -->', grid)

metrics = [('135+', 'currencies and payment methods supported'),
           ('US$1.9tn', 'in payments volume processed in 2025'),
           ('99.999%', 'historical uptime for Stripe services'),
           ('200M+', 'active subscriptions managed on Stripe Billing')]
items = ''.join(f'<div><strong>{value}</strong><span>{label}</span></div>' for value, label in metrics)
stats = f'<section class="stripe-section stripe-metrics"><div class="stripe-section-inner"><h2>The backbone of global commerce</h2><div class="stripe-metric-grid">{items}</div></div></section>\n'
section('<!-- Enterprise Proof & Metrics Section -->', '<!-- Customer Story Spotlight Section (Hertz) -->', stats)

case = f'''<section class="stripe-section stripe-case"><div class="stripe-section-inner"><h2>Powering businesses of all sizes.</h2><p class="stripe-section-intro">Run your business on a reliable platform that adapts to your needs.</p><article class="stripe-case-card"><div><p>Stripe for enterprises</p><h3>Hertz unifies commerce with Stripe.</h3><p>160 countries · 11K+ locations globally</p><p>Products used: Payments, Terminal, Connect, Radar and Stripe Sigma</p><a href="https://stripe.com/en-ca/customers/hertz">Read the story →</a></div><img src="{hertz.replace('&', '&amp;')}" alt="Aerial view of a street intersection, as shown on Stripe's Hertz story card"></article></div></section>\n'''
section('<!-- Customer Story Spotlight Section (Hertz) -->', '<!-- Ready to Start CTA Banner -->', case)
section('<!-- Ready to Start CTA Banner -->', '<!-- Footer (Shared Component JSON Conformance) -->', '')

footer = '''<footer class="stripe-footer"><div class="stripe-footer-inner"><div><b>Stripe</b><a href="https://stripe.com/en-ca">Canada (English)</a></div><div><b>Products</b><a href="https://stripe.com/en-ca/payments">Payments</a><a href="https://stripe.com/en-ca/billing">Billing</a><a href="https://stripe.com/en-ca/connect">Connect</a><a href="https://stripe.com/en-ca/issuing">Issuing</a><a href="https://stripe.com/en-ca/terminal">Terminal</a></div><div><b>Developers</b><a href="https://docs.stripe.com/">Documentation</a><a href="https://docs.stripe.com/api">API reference</a></div><div><b>Company</b><a href="https://stripe.com/en-ca/customers">Customers</a><a href="https://stripe.com/en-ca/contact/sales">Contact sales</a></div><div><b>Legal</b><a href="https://stripe.com/en-ca/sitemap">Sitemap</a><a href="https://stripe.com/en-ca/cookie-settings">Cookie settings</a></div><small>© 2026 Stripe, Inc. · Source snapshot: 2026-09-22 · Reconstruction draft</small></div></footer>\n'''
section('<!-- Footer (Shared Component JSON Conformance) -->', '<!-- Micro Interaction Script -->', footer)
section('<!-- Micro Interaction Script -->', '</body>', '')

for fiction in ('1.18%', '+14.2% Boost', '$428,950', 'gpt-5o-agent',
                'bulletproof infrastructure', '100% Unified', 'URBANSPACER'):
    assert fiction not in html, fiction
assert 'Financial infrastructure to grow your revenue.' in html
assert wave in html and payment.replace('&', '&amp;') in html
(ROOT / 'stripe.html').write_text(html)
print('Wrote dated Stripe draft:', len(html), 'characters')
