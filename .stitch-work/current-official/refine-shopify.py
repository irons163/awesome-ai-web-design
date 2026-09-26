#!/usr/bin/env python3
"""Remove invented Stitch content and pin current Shopify CA page references.

Native Stitch HTML/screenshot remain unchanged. The refined draft is not an
accepted visual match to the current official desktop or mobile site.
"""
from html import escape
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent
html = (ROOT / 'shopify-stitch.html').read_text()
reference = json.loads((ROOT / 'shopify-browser-reference.json').read_text())
assert reference['url'] == 'https://www.shopify.com/ca'


def once(old: str, new: str) -> None:
    global html
    assert html.count(old) == 1, old[:90]
    html = html.replace(old, new, 1)


def section(start: str, end: str, replacement: str) -> None:
    global html
    assert html.count(start) == 1 and html.count(end) == 1, (start, end)
    a = html.index(start)
    b = html.index(end, a)
    html = html[:a] + replacement + html[b:]


def link(label: str, url: str) -> str:
    return f'<a href="{escape(url, quote=True)}">{escape(label)}</a>'


signup = ('https://admin.shopify.com/signup?locale=en-CA&language=en&'
          'signup_page=https%3A%2F%2Fwww.shopify.com%2Fca&'
          'signup_types%5B%5D=paid_trial_experience')
logo = 'shopify-assets/logo.svg'
photos = ('shopify-assets/hero-poster.png', 'shopify-assets/steve-madden.jpg',
          'shopify-assets/ornot.jpg', 'shopify-assets/glossier.jpg')
placeholder = 'https://www.gstatic.com/labs-code/stitch/stitch-placeholder-300x300.svg'
for asset in (logo, *photos):
    assert (ROOT / asset).is_file()
    assert placeholder in html
    html = html.replace(placeholder, asset, 1)
assert placeholder not in html
for name in ('ai-chatgpt.svg', 'ai-google.png', 'ai-copilot.svg', 'ai-card.png'):
    assert (ROOT / 'shopify-assets' / name).is_file()

header = '''<!-- Live-reference header, 1280×720 browser observation on 2026-09-27 -->
<header class="shopify-header"><nav class="shopify-nav" aria-label="Main navigation">
<a class="shopify-logo" href="https://www.shopify.com/ca"><img src="shopify-assets/logo.svg" alt="Shopify"></a>
<div class="shopify-nav-left"><details><summary>Why Shopify <span aria-hidden="true">⌄</span></summary><div class="shopify-menu">
<a href="https://www.shopify.com/ca/start">Get started fast</a><a href="https://www.shopify.com/ca/sell">Switch to Shopify</a><a href="https://www.shopify.com/ca/enterprise">Trusted by enterprise brands</a><a href="https://www.shopify.com/ca/checkout">World's best checkout</a><a href="https://www.shopify.com/ca/sidekick">Sidekick</a>
</div></details><details><summary>Products <span aria-hidden="true">⌄</span></summary><div class="shopify-menu">
<a href="https://www.shopify.com/ca/website/builder">Website Builder</a><a href="https://www.shopify.com/ca/online">Online</a><a href="https://www.shopify.com/ca/pos">Point of Sale</a><a href="https://www.shopify.com/ca/shop">Shop App</a><a href="https://apps.shopify.com/">App Store</a>
</div></details><a href="https://www.shopify.com/ca/pricing">Pricing</a><a href="https://www.shopify.com/ca/enterprise">Enterprise</a></div>
<div class="shopify-nav-right"><a href="https://www.shopify.com/login?ui_locales=en-CA">Log in</a><a class="shopify-signup" href="''' + escape(signup, quote=True) + '''">Start for free</a></div>
</nav></header>
'''
section('<!-- TOP TRANSLUCENT HEADER (72px high, overlaying hero) -->',
        '<!-- FIRST VIEWPORT: DOCUMENTARY MERCHANT FILM HERO (~880px height at desktop) -->', header)

# The official hero headline rotates. Keep a captured visible frame and the
# accessible fallback; the motion itself remains a pending fidelity task.
once('<h1 class="hero-headline font-light tracking-tight text-white mb-6">',
     '<h1 class="hero-headline font-light tracking-tight text-white mb-6" aria-label="Be the next AI all-star">')
once('<span class="sr-only">AI all-star</span>', '')
assert 'https://www.shopify.com/ca/free-trial' in html
html = html.replace('https://www.shopify.com/ca/free-trial', escape(signup, quote=True))
assert 'https://www.shopify.com/ca/about' in html
html = html.replace('https://www.shopify.com/ca/about', 'https://www.shopify.com/ca')
once('<div class="grid grid-cols-1 md:grid-cols-3 gap-6 items-stretch">',
     '<div class="merchant-grid grid grid-cols-1 md:grid-cols-3 gap-6 items-stretch">')
for unsupported in ('Footwear &amp; Fashion', 'Cycling Apparel', 'Beauty &amp; Skincare'):
    html, n = re.subn(r'<span class="text-xs text-white/40">' + unsupported + r'</span>', '', html, count=1)
    assert n == 1, unsupported

ai = '''<!-- Official source-backed Agentic Storefronts panel -->
<section class="shopify-ai-wrap"><div class="shopify-ai-panel"><div class="shopify-ai-copy">
<div class="shopify-ai-logos"><span><img src="shopify-assets/ai-chatgpt.svg" alt="ChatGPT"></span><span><img src="shopify-assets/ai-google.png" alt="Google"></span><span><img src="shopify-assets/ai-copilot.svg" alt="Copilot"></span></div>
<div><h2>Your brand has entered the chat</h2><p>Get discovered across AI channels. Shoppers check out right in the chat. You don’t lift a finger. All powered by <a href="https://www.shopify.com/ca/agentic-storefronts">Agentic Storefronts</a>.</p></div>
</div><div class="shopify-ai-art"><img src="shopify-assets/ai-card.png" alt="A sweater with an AI shopping chat input, from Shopify's homepage"></div></div></section>
'''
section('<!-- BROAD DARK TEAL/GREEN ROUNDED FEATURE PANEL: AGENTIC STOREFRONTS -->',
        '<!-- SOURCE-BACKED SECTION 1: SELL MORE IN MORE PLACES -->', ai)

def editorial(title: str, body: str, extra: str = '', kind: str = '') -> str:
    return f'<section class="shopify-editorial {kind}"><div class="shopify-editorial-inner"><h2>{escape(title)}</h2><p>{body}</p>{extra}</div></section>\n'


features = '<div class="shopify-feature-list">' + ''.join(
    f'<article><h3>{escape(title)}</h3><p>{copy}</p></article>' for title, copy in [
        ('Get a stunning store', 'That’s built to sell. Design fast with AI. Pick a prebuilt theme. Or go totally custom.'),
        ('Sell on every channel', 'Put your products where shoppers search, shop, and scroll with <a href="https://www.shopify.com/ca/channels">multichannel integration</a>.'),
        ('Sell face to face', 'Sell in person and keep online and in-store sales in sync with <a href="https://www.shopify.com/ca/pos">Shopify POS</a>.'),
        ('Sell to 250M+ shoppers with Shop', 'Automatically show up on the <a href="https://www.shopify.com/ca/shop">Shop app</a>. Reach millions of pre-verified shoppers.'),
    ]) + '</div>'
sections = editorial('Sell more in more places', '', features)
sections += editorial('Grow around the world',
    'Take the complexity out of international selling with <a href="https://www.shopify.com/ca/international">Shopify Markets</a>. Deliver products faster and more affordably with <a href="https://www.shopify.com/ca/shipping">built-in shipping tools</a>.')
stories = '<div class="shopify-feature-list">' + ''.join(
    f'<article><h3>{escape(title)}</h3><p>{copy}</p></article>' for title, copy in [
        ('Get started fast', 'Jackie Prince launched Guests on Earth out of her home. Now it’s a $4M+ business.'),
        ('Grow as big as you want', 'Our Place grew from a one-product shop into a cookware empire.'),
        ('Raise the bar', 'Iconic toymaker Mattel sells direct to shoppers all around the world. All powered by Shopify.'),
    ]) + '</div>'
sections += editorial('For anyone from entrepreneurs to enterprise', '', stories)
sections += editorial('Meet your secret weapon, Sidekick',
    'Spot opportunities for growth and automate tedious tasks with <a href="https://www.shopify.com/ca/sidekick">Sidekick</a>. Built right into your Shopify admin.',
    '<p class="shopify-small-title">Your very own commerce AI</p>', 'sidekick')
sections += editorial('Customize everything with apps',
    'The Shopify App Store has <a href="https://apps.shopify.com/">21,000+ commerce apps</a> for whatever specialized features your business might need.')
sections += editorial('Hyperdriven by AI. Commerce to the core.',
    'Shopify’s <a href="https://www.shopify.com/ca/ucp">Universal Commerce Protocol</a> and <a href="https://shopify.dev/">APIs, tools, and primitives</a> give devs the power to build agentic commerce experiences that businesses are looking for.')
sections += editorial('There’s no better place for you to build', '', kind='shopify-build')
sections += editorial('The world’s best-converting checkout',
    '<a href="https://www.shopify.com/ca/checkout">Shopify Checkout</a> with <a href="https://www.shopify.com/ca/shop-pay">Shop Pay</a> converts up to 50% higher than guest checkout and exposes your brand to hundreds of millions of buyers.',
    '<div class="shopify-stats"><strong>15% <span>higher conversions</span></strong><strong>250M+ <span>high-intent shoppers</span></strong></div>', 'shopify-checkout')
sections += editorial('Rock steady. Blazing fast.', 'Your Shopify store runs strong, even during your most epic product drops.')
sections += editorial('Shopify is here to help',
    'If your business needs a boost, <a href="https://www.shopify.com/ca/capital">Shopify Capital</a> is here to lend a hand.')
sections += editorial('Build fast on Shopify', '',
    '<ol class="shopify-steps"><li>Add your first product</li><li>Customize your store</li><li>Set up payments</li></ol><a class="shopify-final-cta" href="' + escape(signup, quote=True) + '">Take your shot</a>', 'shopify-last')
section('<!-- SOURCE-BACKED SECTION 1: SELL MORE IN MORE PLACES -->',
        '<!-- ACTUAL FOOTER: SHOPIFY, ECOSYSTEM, RESOURCES AND SUPPORT, REGIONAL CANADA | ENGLISH, LEGAL -->',
        sections + '</main>\n')

footer_groups = {
    'Shopify': [('What is Shopify?', 'https://www.shopify.com/ca/blog/what-is-shopify'), ('Shopify Editions', 'https://www.shopify.com/editions'), ('Careers', 'https://www.shopify.com/careers'), ('Investors', 'https://www.shopify.com/investors'), ('Newsroom', 'https://www.shopify.com/news'), ('Sustainability', 'https://www.shopify.com/ca/climate')],
    'Ecosystem': [('Developer Docs', 'https://shopify.dev/docs'), ('Theme Store', 'https://themes.shopify.com/'), ('App Store', 'https://apps.shopify.com/'), ('Partners', 'https://www.shopify.com/ca/partners'), ('Affiliates', 'https://www.shopify.com/ca/affiliates')],
    'Resources': [('Blog', 'https://www.shopify.com/ca/blog'), ('Compare Shopify', 'https://www.shopify.com/ca/compare'), ('Guides', 'https://www.shopify.com/ca/blog/topics/guides'), ('Courses', 'https://www.shopifyacademy.com/'), ('Free Tools', 'https://www.shopify.com/ca/tools'), ('Changelog', 'https://changelog.shopify.com/')],
    'Support': [('Shopify Help Center', 'https://help.shopify.com/en'), ('Community Forum', 'https://community.shopify.com/'), ('Hire a Partner', 'https://www.shopify.com/ca/partners/directory'), ('Service Status', 'https://www.shopifystatus.com/')],
}
groups = ''.join('<section><h3>' + escape(title) + '</h3>' + ''.join(link(label, url) for label, url in rows) + '</section>'
                 for title, rows in footer_groups.items())
legal = [('Terms of Service', 'https://www.shopify.com/ca/legal/terms'), ('Legal', 'https://www.shopify.com/ca/legal'), ('Privacy Policy', 'https://www.shopify.com/ca/legal/privacy'), ('Sitemap', 'https://www.shopify.com/ca/sitemap'), ('Your Privacy Choices', 'https://privacy.shopify.com/en')]
new_footer = '<footer class="shopify-footer"><div class="shopify-footer-inner"><nav aria-label="Shopify footer" class="shopify-footer-grid">' + groups + '</nav><p>Canada | English</p><nav aria-label="Legal" class="shopify-legal">' + ''.join(link(*pair) for pair in legal) + '</nav></div></footer>'
html, n = re.subn(r'<footer\b.*?</footer>', lambda _: new_footer, html, count=1, flags=re.S)
assert n == 1

css = '''<style>
.shopify-header{position:fixed;inset:0 0 auto;z-index:50;height:72px;background:#0005;backdrop-filter:blur(8px);color:white}.shopify-nav{height:100%;max-width:1100px;margin:auto;display:flex;align-items:center;gap:32px}.shopify-logo img{height:36px;width:auto}.shopify-nav-left,.shopify-nav-right{display:flex;align-items:center;gap:30px}.shopify-nav-right{margin-left:auto}.shopify-nav a,.shopify-nav summary{color:white;font-size:15px;cursor:pointer;text-decoration:none}.shopify-nav details{position:relative}.shopify-nav summary{list-style:none}.shopify-nav summary::-webkit-details-marker{display:none}.shopify-nav summary span{margin-left:4px}.shopify-menu{position:absolute;top:38px;left:-20px;width:260px;padding:14px 18px;background:#061517;border:1px solid #29403b;border-radius:14px;box-shadow:0 20px 40px #0007;display:grid;gap:10px}.shopify-menu a{display:block;font-size:14px}.shopify-nav .shopify-signup,.shopify-final-cta{display:inline-block;padding:13px 22px;border-radius:40px;background:#fff;color:#080808;font-weight:600}.shopify-signup:hover,.shopify-final-cta:hover{background:#eee}
body>section>.relative.z-10{max-width:1100px;padding-left:0;padding-right:0}
.merchant-grid{grid-template-columns:2.3fr 1fr 2.3fr;gap:16px}.merchant-grid>div>div:first-child{height:331px;aspect-ratio:auto;border:0;border-radius:8px}.merchant-grid img{object-fit:cover}.merchant-grid .text-sm{font-family:inherit}
.shopify-ai-wrap{max-width:1100px;margin:0 auto 110px}.shopify-ai-panel{min-height:460px;display:grid;grid-template-columns:1fr 1fr;background:linear-gradient(290deg,#061a1c 58%,#0d3a2d);border:1px solid #ffffff12;border-radius:18px;overflow:hidden}.shopify-ai-copy{padding:40px;display:flex;flex-direction:column;justify-content:space-between}.shopify-ai-logos{display:flex;align-items:center;padding-left:12px}.shopify-ai-logos span{width:56px;height:56px;border-radius:50%;background:white;border:1px solid #ddd;display:grid;place-items:center;margin-left:-12px;box-shadow:0 3px 12px #0004}.shopify-ai-logos img{width:28px;height:28px;object-fit:contain}.shopify-ai-copy h2{font-size:clamp(36px,4.4vw,56px);line-height:1.07;font-weight:300;letter-spacing:-.03em;max-width:470px;margin:0 0 20px}.shopify-ai-copy p{font-size:18px;line-height:1.4;color:#aab8b7;max-width:480px}.shopify-ai-copy a,.shopify-editorial a{color:inherit;text-decoration:underline}.shopify-ai-art{display:flex;align-items:center;justify-content:center;overflow:hidden}.shopify-ai-art img{width:100%;max-width:520px;mix-blend-mode:screen}
.shopify-editorial{padding:100px 24px;background:#02090b;border-top:1px solid #ffffff16}.shopify-editorial-inner{max-width:1100px;margin:auto}.shopify-editorial h2{font-size:clamp(40px,5vw,64px);font-weight:300;line-height:1.08;letter-spacing:-.035em;max-width:900px;margin:0 0 32px}.shopify-editorial p{font-size:20px;line-height:1.5;color:#aab8b7;max-width:730px;margin:0 0 20px}.shopify-feature-list{display:grid;grid-template-columns:repeat(2,1fr);gap:0 32px;margin-top:48px}.shopify-feature-list article{padding:25px 0;border-top:1px solid #ffffff36}.shopify-feature-list h3{font-size:25px;font-weight:350;margin:0 0 12px}.shopify-feature-list p{font-size:17px}.shopify-editorial.sidekick{background:linear-gradient(#2c007f,#000a1d)}.shopify-editorial.shopify-build{text-align:center}.shopify-build h2{margin:auto}.shopify-editorial.shopify-checkout{background:#082420}.shopify-stats{display:flex;gap:60px;margin-top:45px}.shopify-stats strong{font-size:48px;font-weight:350}.shopify-stats span{display:block;font-size:14px;color:#adbfbb;font-weight:400}.shopify-steps{counter-reset:steps;display:grid;grid-template-columns:repeat(3,1fr);gap:24px;list-style:none;padding:0;margin:48px 0}.shopify-steps li{border-top:1px solid #ffffff55;padding-top:18px}.shopify-steps li:before{counter-increment:steps;content:'0' counter(steps);display:block;font-size:13px;color:#aaa;margin-bottom:14px}.shopify-editorial.shopify-last{text-align:center}.shopify-last h2{margin-left:auto;margin-right:auto}.shopify-last .shopify-final-cta{color:#070707;text-decoration:none}
.shopify-footer{padding:70px 24px 40px;background:#010506;color:#bbb}.shopify-footer-inner{max-width:1100px;margin:auto}.shopify-footer-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:28px;padding-bottom:60px}.shopify-footer-grid h3{font-size:16px;font-weight:500;color:#fff;margin:0 0 18px}.shopify-footer-grid a{display:block;font-size:14px;color:#bbb;line-height:2;text-decoration:none}.shopify-footer-grid a:hover,.shopify-legal a:hover{text-decoration:underline}.shopify-footer p{border-top:1px solid #ffffff30;padding-top:30px}.shopify-legal{display:flex;flex-wrap:wrap;gap:18px}.shopify-legal a{font-size:13px;color:#aaa}
@media(max-width:1150px){.shopify-nav,body>section>.relative.z-10,.shopify-ai-wrap{margin-left:24px;margin-right:24px}}
@media(max-width:800px){.shopify-nav-left{display:none}.shopify-ai-panel{grid-template-columns:1fr}.shopify-ai-art{height:300px}.merchant-grid{grid-template-columns:repeat(3,1fr)}.merchant-grid>div>div:first-child{height:220px}.shopify-footer-grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:600px){.shopify-nav-right>a:first-child{display:none}.shopify-ai-copy{min-height:360px}.merchant-grid{grid-template-columns:1fr}.merchant-grid>div>div:first-child{height:280px}.shopify-feature-list,.shopify-steps{grid-template-columns:1fr}.shopify-stats{display:block}.shopify-footer-grid{grid-template-columns:1fr}body>section>.relative.z-10{padding-left:0;padding-right:0}}
</style>'''
once('</head>', css + '</head>')

for invented in ('$148 CAD', '14,200 orders', '99.99% uptime',
                 'No credit card required', 'https://www.shopify.com/ca/free-trial'):
    assert invented not in html, invented
for asset in (logo, *photos, 'shopify-assets/ai-card.png'):
    assert asset in html, asset
for title in reference['below_first_viewport']['section_headings']:
    assert title.replace('\u00a0', ' ') in html, title
assert html.count('</main>') == 1
(ROOT / 'shopify.html').write_text(html)
print('Wrote current-reference Shopify draft:', len(html), 'characters')
