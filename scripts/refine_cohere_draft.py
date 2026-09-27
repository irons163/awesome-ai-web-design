#!/usr/bin/env python3
"""Build a dated Cohere draft from the observed public-page copy and media."""

import html
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1] / '.stitch-work' / 'current-official'
DATA = json.loads((ROOT / 'cohere-browser-data.json').read_text())
ASSETS = ROOT / 'cohere-assets'


def escape(value):
    return html.escape(str(value), quote=True)


def image(alt=None, y=None, starts=None):
    for item in DATA['images']:
        if alt is not None and item['alt'] != alt:
            continue
        if y is not None and item['y'] != y:
            continue
        if starts is not None and starts not in item['src']:
            continue
        return item['src']
    raise LookupError((alt, y, starts))


def link(starts):
    for item in DATA['links']:
        if item['text'].startswith(starts):
            return item['href']
    raise LookupError(starts)


def local_logo(item):
    name = Path(urlsplit(item['src']).path).name
    if not (ASSETS / name).is_file():
        raise FileNotFoundError(name)
    return f'cohere-assets/{name}'


logos = []
for item in DATA['images']:
    if item['y'] == 1222 and item['alt'] and item['alt'] not in {x['alt'] for x in logos}:
        logos.append(item)
assert len(logos) == 18, len(logos)
logo_imgs = ''.join(f'<img src="{escape(local_logo(x))}" alt="{escape(x["alt"])}">' for x in logos)

stories = [x for x in DATA['images'] if x['y'] == 5143 and x['alt'] == 'Image for Context']
news_images = [x for x in DATA['images'] if x['y'] == 6482 and not x['alt']]
badges = [x for x in DATA['images'] if x['y'] == 7316 and x['alt']]
assert len(stories) == len(news_images) == 3 and len(badges) == 5

hero = image('Hero featured graphic', 546)
campaign_left = image('Section image', 1366)
campaign_right = next(x['src'] for x in DATA['images'] if x['alt'] == 'Section image' and x['y'] == 1366 and x['src'] != campaign_left)
industry = image('', 4263)
industry_images = {
    'Financial services': industry,
    'Public Sector': 'https://cdn.sanity.io/images/rjtqmwfu/web3-prod/c420a62b7752d73b35714a94949222f0ee18dab2-1360x1500.png?auto=format&fit=max&q=80&w=1360',
    'Technology': 'https://cdn.sanity.io/images/rjtqmwfu/web3-prod/4d33a32908efdf438ab7d2e2984433783f44910a-1360x1500.png?auto=format&fit=max&q=80&w=1360',
    'Energy and utilities': 'https://cdn.sanity.io/images/rjtqmwfu/web3-prod/7ad29239cefeedd5e8eb85db77afcdd36941fe16-1360x1500.png?auto=format&fit=max&q=80&w=1360',
}
model_art = image('Featured Image', 2738)
vault_art = image('Featured Image', 3300)
nvidia = image('Jensen Huang', 5805)
north_bg = 'https://cdn.sanity.io/images/rjtqmwfu/web3-prod/d81699dc83d68fd4334dedc2ff209e3b6c2c52b2-2720x1152.png?auto=format&w=1600&q=80&fit=crop'
vault_bg = 'https://cdn.sanity.io/images/rjtqmwfu/web3-prod/698c3dce8af14ea10681a34aadd1d21496ba27af-2720x1200.png?auto=format&w=1600&q=80&fit=crop'

story_meta = [
    ('How CoreWeave used Cohere North to transform its customer support in 90 days', 'https://cohere.com/customer-stories/coreweave'),
    ('Integrating Cohere into Draftwise boosted the quality of search results by 30%', 'https://cohere.com/customer-stories/draftwise'),
    ('Fujitsu launches Takane AI model in partnership with Cohere', 'https://cohere.com/customer-stories/fujitsu'),
]
story_cards = ''.join(
    f'<a class="story-card" href="{escape(href)}"><img src="{escape(stories[i]["src"])}" alt="{escape(title)}">'
    f'<span class="story-category">TECHNOLOGY</span><h3>{escape(title)}</h3><span class="story-read">Read more <b>→</b></span></a>'
    for i, (title, href) in enumerate(story_meta)
)

news_meta = [
    ('Cohere and Aleph Alpha sign agreement to become the first transatlantic sovereign AI solution', 'https://cohere.com/blog/cohere-and-aleph-alpha-sign-agreement', ['Company News', 'Sovereign AI'], '9月 16, 2026'),
    ('Cohere and OpenText partner to bring trusted agentic AI to governments and regulated industries', 'https://cohere.com/blog/cohere-and-open-text-partner-to-bring-trusted-ai', ['Partner', 'Company News'], '9月 16, 2026'),
    ('Who Gets to Define the Rules for AI?', 'https://cohere.com/blog/who-gets-to-define-the-rules-for-ai', ['Company News'], '9月 14, 2026'),
]
news_cards = ''.join(
    f'<article class="news-card"><a href="{escape(href)}"><img src="{escape(news_images[i]["src"])}" alt="{escape(title)}"></a>'
    f'<div class="news-tags">{"".join(f"<span>{escape(tag)}</span>" for tag in tags)}</div>'
    f'<h3><a href="{escape(href)}">{escape(title)}</a></h3><time>{escape(date)}</time></article>'
    for i, (title, href, tags, date) in enumerate(news_meta)
)

badge_imgs = ''.join(f'<a href="{escape("https://www.aicpa.org/soc4so" if x["alt"] == "SOC2" else "https://trustcenter.cohere.com/")}"><img src="{escape(x["src"])}" alt="{escape("ISO 27001" if x["alt"] == "ISO" else x["alt"])}"></a>' for x in badges)

css = r'''
@font-face{font-family:CohereText;src:url('cohere-assets/CohereText-Regular.2hnqq9npo38r1.woff2') format('woff2');font-display:swap}
@font-face{font-family:Unica;src:url('cohere-assets/Unica77CohereWeb-Regular.08nli527722ku.woff2') format('woff2');font-weight:400;font-display:swap}
@font-face{font-family:Unica;src:url('cohere-assets/Unica77CohereWeb-Medium.2d_f6bxov-n_b.woff2') format('woff2');font-weight:500 600;font-display:swap}
@font-face{font-family:Unica;src:url('cohere-assets/Unica77CohereWeb-Bold.0ifnon1g78mmk.woff2') format('woff2');font-weight:700 900;font-display:swap}
:root{--black:#19191e;--green:#152717;--stone:#f0eee9;--ink:#222;--side:40px}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#fff;color:var(--ink);font:17px/1.42 Unica,Arial,sans-serif}img{max-width:100%;display:block}a{color:inherit;text-decoration:none}a:hover{text-decoration:underline}button{font:inherit;cursor:pointer}.container{width:min(calc(100% - 80px),1200px);margin:auto}h1,h2,h3,p{margin-top:0}h1,h2,h3{font-weight:400}h2{font-size:48px;line-height:1.12}h3{font-size:28px;line-height:1.16}.pill{display:inline-flex;align-items:center;justify-content:center;border-radius:999px;min-height:52px;padding:0 28px;white-space:nowrap}.pill.dark{background:var(--black);color:#fff}.pill.white{background:#fff;color:#111}.pill.outline{border:1px solid #1c1c1c;background:transparent;color:#111}
body>.announcement{height:48px;background:#000;color:#fff;text-align:center;display:flex;align-items:center;justify-content:center;padding:0 48px;font-size:15px;position:relative}.announcement a{text-decoration:underline;text-underline-offset:5px;margin-left:7px}.announcement button{position:absolute;right:10px;top:0;width:40px;height:48px;color:#fff;border:0;background:none;font-size:21px}.header{height:60px;background:#fff;position:sticky;top:0;z-index:100;display:flex;align-items:center;padding:0 var(--side);gap:50px}.brand{flex:none}.brand img{width:118px;height:20px}.nav{display:flex;align-items:center;gap:30px;font-size:15px}.nav details{position:relative}.nav summary{list-style:none;cursor:pointer}.nav summary::-webkit-details-marker{display:none}.nav-menu{display:none;position:absolute;top:32px;left:-16px;min-width:190px;background:#fff;border:1px solid #ddd;border-radius:8px;padding:12px;box-shadow:0 16px 30px #0002}.nav details[open] .nav-menu{display:grid;gap:10px}.header-right{margin-left:auto;display:flex;align-items:center;gap:22px;font-size:15px}.header-right .pill{min-height:36px;padding:0 19px;font-size:14px}.mobile-toggle{display:none;border:0;background:none;font-size:26px;color:#111}
.hero{height:438px;text-align:center;padding-top:100px}.hero h1{font:400 96px/1 CohereText,'Space Grotesk',Arial,sans-serif;letter-spacing:-.025em;margin:0}.hero p{font-size:19px;line-height:1.35;max-width:700px;margin:17px auto 0}.hero-art-wrap{height:575px;padding:0 var(--side) 80px}.hero-art-wrap img{width:100%;height:494px;object-fit:cover;border-radius:12px}.trusted{height:245px;overflow:hidden;padding:31px 0}.trusted p{text-align:center;margin:0 0 42px;font-size:16px}.logo-ticker{display:flex;gap:8px;align-items:center;width:max-content;animation:logos 36s linear infinite}.logo-ticker img{width:148px;height:52px;object-fit:contain;flex:none}@keyframes logos{to{transform:translateX(-50%)}}
.empowerment{height:520px;position:relative;overflow:hidden;display:flex}.empowerment img{width:50%;height:100%;object-fit:cover}.empowerment::after{content:'';position:absolute;inset:0;background:linear-gradient(90deg,#071e0a77,transparent 63%)}.empowerment-content{position:absolute;z-index:1;left:var(--side);top:170px;color:#fff;max-width:550px}.empowerment h2{font-size:60px;line-height:1;max-width:480px;margin:0 0 28px}.empowerment p{font-size:18px;max-width:560px;margin:0 0 24px}
.solutions-intro{height:242px;background:var(--stone);text-align:center;padding-top:136px}.solutions-intro h2{margin:0}.product-stack{min-height:1854px;background:var(--stone);padding:148px var(--side) 115px}.product-panel{height:586px;border-radius:17px;overflow:hidden;position:relative;padding:75px 85px;background-color:#101418;background-size:cover;background-position:center;color:#fff}.product-panel+.product-panel{margin-top:-100px}.product-panel:nth-child(1){z-index:1}.product-panel:nth-child(2){z-index:2;background:#050505}.product-panel:nth-child(3){z-index:3;color:#222}.product-copy{position:relative;z-index:2;max-width:445px}.product-copy .kicker{display:block;font-size:13px;letter-spacing:.035em;margin:0 0 42px}.product-copy h3{font-size:48px;line-height:1.1;margin:0 0 23px}.product-copy p{font-size:17px;line-height:1.5;max-width:440px;margin:0 0 36px}.product-panel:nth-child(2) .product-copy,.product-panel:nth-child(3) .product-copy{max-width:425px}.product-panel:nth-child(2) img,.product-panel:nth-child(3) img{position:absolute;right:0;bottom:0;width:52%;height:82%;object-fit:contain;object-position:right bottom}.product-panel:nth-child(3){background-position:center}.product-panel:nth-child(3) .pill{background:#fff}
.industries-heading{height:282px;text-align:center;padding-top:135px}.industries-heading h2{margin:0}.industries{min-height:709px;display:grid;grid-template-columns:512px 1fr;gap:176px}.industries>img{width:512px;height:565px;object-fit:cover;border-radius:18px}.industry-list{padding-top:0}.industry-list details{border-top:1px solid #444}.industry-list details:last-of-type{border-bottom:1px solid #444}.industry-list summary{font-size:26px;line-height:1.2;list-style:none;cursor:pointer;padding:22px 0}.industry-list summary::-webkit-details-marker{display:none}.industry-list details[open] summary{padding-top:5px}.industry-list details p{font-size:17px;line-height:1.45;max-width:470px;margin:8px 0 25px}.industry-list ul{list-style:none;padding:0;margin:0 0 30px}.industry-list li{margin:10px 0}.industry-list li::before{content:'⊙';display:inline-block;margin-right:10px}.industry-list details a{display:inline-block;margin-bottom:30px}.industry-list>.pill{margin-top:34px}
.stories{min-height:689px;padding:0 0 72px}.stories h2{margin:0 0 56px}.story-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}.story-card{background:#f0eee9;border-radius:20px;min-height:455px;padding:16px;display:flex;flex-direction:column}.story-card img{height:198px;width:100%;object-fit:cover;border-radius:9px}.story-category{font-size:13px;letter-spacing:.02em;margin:20px 0}.story-card h3{font-size:25px;line-height:1.24;margin:0}.story-read{margin-top:auto;display:flex;align-items:center;justify-content:space-between;padding-top:24px}.story-read b{background:white;border-radius:50%;width:45px;height:45px;display:grid;place-items:center;font-size:25px;font-weight:400}
.quote{height:742px;display:grid;grid-template-columns:32% 1fr;gap:30px;padding-top:140px}.quote>img{width:168px;height:32px;object-fit:contain}.quote blockquote{font:400 48px/1.19 Unica,Arial,sans-serif;margin:0}.quote cite{display:block;font-style:normal;font-size:16px;margin-top:30px}.quote cite span{display:block;margin-top:4px}.news{min-height:588px;padding:0 0 72px}.news-heading{display:flex;align-items:center;justify-content:space-between;margin:0 0 33px}.news-heading h2{font-size:32px;margin:0}.news-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}.news-card img{width:100%;height:216px;object-fit:cover;border-radius:9px}.news-tags{display:flex;gap:5px;margin:20px 0 15px}.news-tags span{border:1px solid #222;border-radius:22px;padding:5px 13px;font-size:14px}.news-card h3{font-size:26px;line-height:1.18;min-height:120px;margin:0 0 25px}.news-card time{font:14px Unica,Arial;color:#444}
.security{background:var(--green);color:#f2f4ee;padding:95px 0 62px;text-align:center}.security h2{max-width:1050px;margin:0 auto 23px}.security p{max-width:710px;margin:0 auto 23px}.security a{text-decoration:underline;text-underline-offset:4px}.security-badges{background:var(--green);padding:40px 0 90px}.security-badges .container{display:flex;justify-content:space-around;align-items:center;gap:20px}.security-badges img{width:120px;height:120px;object-fit:contain}.ready{min-height:390px;display:flex;align-items:center;justify-content:space-between}.ready h2{font:400 60px/1.1 CohereText,Arial;margin:0}.footer{border-top:1px solid #ddd;padding:65px 0 40px}.footer-top{display:grid;grid-template-columns:180px repeat(4,1fr);gap:28px}.footer-brand img{width:118px}.footer-nav{display:grid;align-content:start;gap:8px;font-size:14px}.footer-nav strong{margin-bottom:12px;font-weight:500}.footer-nav a{color:#555}.footer-bottom{display:flex;gap:25px;flex-wrap:wrap;border-top:1px solid #ddd;margin-top:65px;padding-top:22px;font-size:13px}.footer-bottom a{color:#555}
@media(max-width:1100px){.header{gap:24px}.nav{gap:15px}.industries{grid-template-columns:45% 1fr;gap:8%}.industries>img{width:100%}.product-panel{padding:65px}.story-card h3{font-size:22px}.quote blockquote{font-size:40px}}
@media(max-width:760px){:root{--side:20px}.container{width:min(calc(100% - 40px),1200px)}body>.announcement{height:auto;min-height:58px;font-size:12px;line-height:1.25}.header{height:66px;padding:0 20px;gap:10px}.mobile-toggle{display:block;margin-left:auto}.nav{display:none;position:absolute;top:66px;left:0;right:0;background:#fff;padding:20px;flex-direction:column;align-items:stretch;border-bottom:1px solid #ddd}.header.open .nav{display:flex}.header-right{margin-left:0}.header-right>a:first-child{display:none}.header-right .pill{padding:0 12px;font-size:12px}.hero{height:390px;padding:90px 20px 0}.hero h1{font-size:clamp(54px,12vw,78px)}.hero p{font-size:17px}.hero-art-wrap{height:auto;padding:0 20px 60px}.hero-art-wrap img{height:auto;aspect-ratio:2.2/1}.trusted{height:210px}.trusted p{margin-bottom:28px}.logo-ticker img{width:120px;height:45px}.empowerment{height:560px}.empowerment img{width:50%}.empowerment-content{top:140px;left:20px;right:20px}.empowerment h2{font-size:45px}.empowerment p{font-size:16px}.solutions-intro{height:195px;padding-top:85px}.solutions-intro h2,.industries-heading h2,.stories h2,.security h2{font-size:36px}.product-stack{padding:35px 20px 65px;min-height:0}.product-panel{height:550px;padding:35px;display:flex;align-items:flex-start}.product-panel+.product-panel{margin-top:20px}.product-copy .kicker{margin-bottom:24px}.product-copy h3{font-size:38px}.product-copy p{font-size:15px}.product-panel:nth-child(2) img,.product-panel:nth-child(3) img{height:45%;width:85%}.industries-heading{height:190px;padding-top:70px}.industries{display:block;min-height:0;padding-bottom:60px}.industries>img{width:100%;height:auto;aspect-ratio:1/1}.industry-list{padding-top:35px}.industry-list summary{font-size:22px}.stories{min-height:0;padding-bottom:70px}.stories h2{margin-bottom:30px}.story-grid{grid-template-columns:1fr}.story-card{min-height:400px}.quote{height:auto;display:block;padding:70px 0 110px}.quote>img{margin-bottom:45px}.quote blockquote{font-size:35px}.news{min-height:0;padding-bottom:70px}.news-grid{grid-template-columns:1fr}.news-card h3{min-height:0}.news-card time{display:block;margin-bottom:30px}.security{padding:75px 0}.security-badges{padding:0 0 70px}.security-badges .container{flex-wrap:wrap}.security-badges img{width:80px;height:80px}.ready{min-height:300px;display:block;padding-top:95px}.ready h2{font-size:45px;margin-bottom:30px}.footer-top{grid-template-columns:repeat(2,1fr)}.footer-brand{grid-column:1/-1}}
@media(max-width:430px){.hero h1{font-size:55px}.empowerment h2{font-size:42px}.product-panel{padding:26px}.product-copy h3{font-size:34px}}
'''

page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Cohere — homepage reconstruction draft</title><meta name="description" content="Dated source-backed reconstruction draft of Cohere's public homepage, observed 2026-09-27."><style>{css}</style></head><body>
<div class="announcement" id="announcement">AI for Empowerment: Your freedom. Your focus. See how AI gives you more time for what truly moves you. <a href="https://cohere.com/ai-for-empowerment">Explore now</a><button type="button" aria-label="Close banner" onclick="document.getElementById('announcement').remove()">×</button></div>
<header class="header" id="header"><a class="brand" href="https://cohere.com/"><img src="cohere-assets/logo.svg" alt="Cohere"></a><button class="mobile-toggle" type="button" aria-label="Open menu" aria-expanded="false" onclick="const h=document.getElementById('header');h.classList.toggle('open');this.setAttribute('aria-expanded',h.classList.contains('open'))">☰</button><nav class="nav" aria-label="Primary"><a href="https://cohere.com/products">Products</a><a href="https://cohere.com/solutions">Solutions</a><details><summary>Resources</summary><div class="nav-menu"><a href="https://cohere.com/blog">Blog</a><a href="https://cohere.com/customer-stories">Customer stories</a><a href="https://cohere.com/developers">Developers</a><a href="https://docs.cohere.com/">Documentation</a></div></details><a href="https://cohere.com/blog">Blog</a><a href="https://cohere.com/research">Research</a><a href="https://cohere.com/about">Company</a></nav><div class="header-right"><a href="https://dashboard.cohere.com/welcome/login">Sign in</a><a class="pill dark" href="https://cohere.com/contact-sales">Request a demo</a></div></header>
<main><section class="hero"><h1>Your AI.<br>Your rules.</h1><p>North by Cohere is a complete agentic enterprise AI platform that you control and deploy on your terms.</p></section><section class="hero-art-wrap"><img src="{escape(hero)}" alt="North by Cohere agent workspace"></section>
<section class="trusted"><p>Trusted by industry leaders and developers worldwide</p><div class="logo-ticker">{logo_imgs}{logo_imgs}</div></section>
<section class="empowerment"><img src="{escape(campaign_left)}" alt=""><img src="{escape(campaign_right)}" alt=""><div class="empowerment-content"><h2>AI for<br>Empowerment</h2><p>Your freedom. Your focus. Cohere keeps it that way. Learn how AI helps you reclaim time for what truly moves you.</p><a class="pill white" href="https://cohere.com/ai-for-empowerment">Explore now</a></div></section>
<section class="solutions-intro"><h2>Purpose-built AI solutions</h2></section><section class="product-stack"><article class="product-panel" style="background-image:url('{escape(north_bg)}')"><div class="product-copy"><span class="kicker">NORTH PLATFORM</span><h3>North</h3><p>A fully ownable agentic platform built to bring peak security, intelligence, cost efficiency, and control together.</p><a class="pill white" href="https://cohere.com/north">Explore North</a></div></article><article class="product-panel"><div class="product-copy"><span class="kicker">COHERE MODELS</span><h3>Our models. Your business.</h3><p>Tools for generative AI, advanced search, and multilingual capabilities—built to keep your enterprise in full control.</p><a class="pill white" href="https://cohere.com/models-overview">Explore models</a></div><img src="{escape(model_art)}" alt="Cohere model artwork"></article><article class="product-panel" style="background-image:url('{escape(vault_bg)}')"><div class="product-copy"><span class="kicker">MODEL VAULT</span><h3>Scalable, secure AI deployment</h3><p>Model Vault provides fully-isolated performance inference with end-to-end encryption.</p><a class="pill white" href="https://cohere.com/solutions/model-vault">Learn more</a></div><img src="{escape(vault_art)}" alt="Model Vault interface"></article></section>
<section class="industries-heading"><h2>Powering progress across industries</h2></section><section class="industries container"><img src="{escape(industry)}" alt="Financial services AI agent interface"><div class="industry-list"><details open><summary>Financial services</summary><p>AI solutions that drive growth, reduce risk, and enhance customer experiences with speed and precision.</p><ul><li>Help investment teams move faster</li><li>Automate routine back-office work</li><li>Streamline customer service operations</li></ul><a href="https://cohere.com/solutions/financial-services">Learn more →</a></details><details><summary>Public Sector</summary><p>Automate workflows, unify systems, and surface real-time insights to serve citizens faster, more securely, and at lower cost.</p><ul><li>Deliver instant answers to constituent questions</li><li>Automate case intake and routing</li><li>Fuse real-time emergency intelligence</li></ul><a href="https://cohere.com/solutions/public-sector">Learn more →</a></details><details><summary>Technology</summary><p>Turn your data into your differentiator, streamline dev workflows, and launch AI experiences at scale with Cohere.</p><ul><li>Unblock engineering with context-aware questions</li><li>Automate release workflows from CI to deployment</li><li>Move faster with a customer insight copilot</li></ul><a href="https://cohere.com/solutions/technology">Learn more →</a></details><details><summary>Energy and utilities</summary><p>Maximize uptime, cut operating costs, and modernize critical infrastructure with AI built for the 24/7 demands of energy and utilities companies.</p><ul><li>Get instant guidance with an operations copilot</li><li>Automate outage triage and customer communications</li><li>Streamline compliance and regulatory reporting</li></ul><a href="https://cohere.com/solutions/energy-and-utilities">Learn more →</a></details><a class="pill outline" href="https://cohere.com/solutions">See all industries</a></div></section>
<section class="stories container"><h2>Why leading teams trust Cohere</h2><div class="story-grid">{story_cards}</div></section><section class="quote container"><img src="{escape(nvidia)}" alt="NVIDIA"><div><blockquote>“The team at Cohere has made foundational contributions to generative AI. Their service will help enterprises around the world harness these capabilities to automate and accelerate.”</blockquote><cite>Jensen Huang<span>Founder and CEO, NVIDIA</span></cite></div></section>
<section class="news container"><div class="news-heading"><h2>The latest news</h2><a href="https://cohere.com/blog">See more on the blog →</a></div><div class="news-grid">{news_cards}</div></section><section class="security"><div class="container"><h2>Industry-leading AI security and data protection</h2><p>Our platform and models meet rigorous standards across security, availability, processing integrity, confidentiality, and privacy.</p><a href="https://cohere.com/security">Learn more →</a></div></section><section class="security-badges"><div class="container">{badge_imgs}</div></section><section class="ready container"><h2>Ready to put AI to work?</h2><a class="pill dark" href="https://cohere.com/contact-sales">Request a demo</a></section></main>
<footer class="footer"><div class="container"><div class="footer-top"><a class="footer-brand" href="https://cohere.com/"><img src="cohere-assets/logo.svg" alt="Cohere"></a><nav class="footer-nav" aria-label="Platforms"><strong>Platforms</strong><a href="https://cohere.com/north">North</a><a href="https://cohere.com/compass">Compass</a><a href="https://cohere.com/products">Product Overview</a><strong>Models</strong><a href="https://cohere.com/command">Command</a><a href="https://cohere.com/transcribe">Transcribe</a><a href="https://cohere.com/embed">Embed</a><a href="https://cohere.com/rerank">Rerank</a><a href="https://cohere.com/models-overview">Models Overview</a></nav><nav class="footer-nav" aria-label="Industries"><strong>Industries</strong><a href="https://cohere.com/solutions/financial-services">Financial Services</a><a href="https://cohere.com/solutions/public-sector">Public Sector</a><a href="https://cohere.com/solutions/technology">Technology</a><a href="https://cohere.com/solutions/energy-and-utilities">Energy and Utilities</a><a href="https://cohere.com/solutions">Solutions Overview</a><strong>Deployment</strong><a href="https://cohere.com/solutions/model-vault">Model Vault</a><a href="https://cohere.com/private-deployments">Private Deployments</a><a href="https://cohere.com/security">Security</a></nav><nav class="footer-nav" aria-label="Resources"><strong>Resources</strong><a href="https://cohere.com/blog">Blog</a><a href="https://cohere.com/customer-stories">Customer Stories</a><a href="https://cohere.com/developers">Developers</a><a href="https://docs.cohere.com/">Documentation</a><a href="https://cohere.com/llmu">LLM University</a><strong>Connect</strong><a href="https://cohere.com/research">Research</a><a href="https://cohere.com/partners">Partners</a><a href="https://cohere.com/events">Events</a></nav><nav class="footer-nav" aria-label="Company"><strong>Company</strong><a href="https://cohere.com/about">About</a><a href="https://cohere.com/careers">Careers</a><a href="https://cohere.com/newsroom">Newsroom</a><strong>Legal</strong><a href="https://cohere.com/legal">Legal Center</a><a href="https://trustcenter.cohere.com/">Trust Center</a><a href="https://cohere.com/privacy">Privacy Policy</a><a href="https://cohere.com/terms-of-use">Terms of Use</a></nav></div><div class="footer-bottom"><span>Cohere © 2026</span><a href="https://www.linkedin.com/company/cohere-ai/">LinkedIn</a><a href="https://x.com/cohere">X</a><a href="https://www.instagram.com/cohere_ai">Instagram</a><a href="https://www.youtube.com/@CohereAI">Youtube</a><a href="mailto:support@cohere.com">Email</a></div></div></footer></body></html>'''

industry_script = '''<script>
const industryImages = ''' + json.dumps(industry_images) + ''';
const industryVisual = document.querySelector('.industries > img');
const industryPanels = [...document.querySelectorAll('.industry-list details')];
for (const panel of industryPanels) {
  panel.addEventListener('toggle', () => {
    if (!panel.open) return;
    for (const other of industryPanels) if (other !== panel) other.open = false;
    const name = panel.querySelector('summary').textContent.trim();
    industryVisual.src = industryImages[name];
    industryVisual.alt = name + ' AI interface';
  });
}
</script>'''
page = page.replace('</body>', industry_script + '</body>')
(ROOT / 'cohere.html').write_text(page)
print(f'Wrote {ROOT / "cohere.html"} ({len(page)} characters)')
