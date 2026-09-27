#!/usr/bin/env python3
"""Replace invented Stitch details with the observed Supabase public homepage.

The untouched Stitch HTML and screenshot are saved beside this script. The
result is a dated reconstruction draft, not a visually accepted replica.
"""
from html import escape
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
raw = (ROOT / 'supabase-stitch.html').read_text()
for text in ('Build in a weekend', 'Scale to millions', 'Postgres Database',
             'Stay productive and manage your app without leaving the dashboard'):
    assert text in raw
assert 'stitch-placeholder' in raw
assets = ROOT / 'supabase-assets'
logo = (assets / 'logo.svg').read_text()
examples = json.loads((ROOT / 'supabase-framework-examples.json').read_text())
assert len(examples) == 6


def a(text: str, url: str, css: str = '') -> str:
    return f'<a class="{css}" href="{escape(url, quote=True)}">{escape(text)}</a>'


def img(name: str, alt: str, css: str = '') -> str:
    assert (assets / name).is_file(), name
    return f'<img class="{css}" src="supabase-assets/{name}" alt="{escape(alt, quote=True)}" loading="lazy">'


nav = [('Product', 'https://supabase.com/features'),
       ('Developers', 'https://supabase.com/docs'),
       ('Solutions', 'https://supabase.com/solutions'),
       ('Pricing', 'https://supabase.com/pricing'),
       ('Docs', 'https://supabase.com/docs'),
       ('Blog', 'https://supabase.com/blog')]
header = '<div class="announcement"><span aria-hidden="true">〈〈〈〈〈〈〈〈</span>Supabase Select 2026 is coming October 2 <b>·</b> ' + a('Apply to attend ↗', 'https://select.supabase.com/') + '<span aria-hidden="true">〉〉〉〉〉〉〉〉</span></div>'
header += '<header class="site-nav"><div class="nav-inner"><a class="brand" href="https://supabase.com/">' + logo + '</a><nav aria-label="Main navigation">'
header += ''.join(a(label + (' ⌄' if label in ('Product', 'Developers', 'Solutions') else ''), url) for label, url in nav)
header += '</nav><div class="nav-right">' + a('◉ 110.7K', 'https://github.com/supabase/supabase', 'stars') + a('Sign in', 'https://supabase.com/dashboard', 'sign-in') + a('Start your project', 'https://supabase.com/dashboard/sign-up', 'green-btn') + '</div></div></header>'

hero = '''<main><section class="hero container"><div class="hero-columns"><div><h1>Build in a weekend<br><span>Scale to millions</span></h1><div class="hero-actions">'''
hero += a('Start your project', 'https://supabase.com/dashboard/sign-up', 'green-btn')
hero += a('Request a demo', 'https://supabase.com/contact/sales', 'dark-btn')
hero += '''</div></div><p>Start your project with a Postgres database. Add Authentication, Data APIs, Edge Functions, Realtime Data, Storage, and Vector embeddings.</p></div></section>'''

products = [
    ('Postgres Database', 'Every project is a full Postgres database, the world\'s most trusted relational database.', 'https://supabase.com/database', 'database-dark.png', 'database'),
    ('Authentication', 'Add user sign ups and logins, securing your data with Row Level Security.', 'https://supabase.com/auth', 'auth.svg', 'auth'),
    ('Edge Functions', 'Easily write custom code without deploying or scaling servers.', 'https://supabase.com/edge-functions', 'edge-functions-dark.svg', 'edge'),
    ('Storage', 'Store, organize, and serve large files, from videos to images.', 'https://supabase.com/storage', '', 'storage'),
    ('Realtime', 'Build multiplayer experiences with real-time data synchronization.', 'https://supabase.com/realtime', 'realtime-dark.svg', 'realtime'),
    ('Vector', 'Integrate your favorite ML-models to store, index and search vector embeddings.', 'https://supabase.com/modules/vector', 'vector-dark.svg', 'vector'),
    ('Data APIs', 'Instant ready-to-use REST APIs.', 'https://supabase.com/docs/guides/api', 'data-apis-dark.svg', 'data-apis'),
]
cards = '<section class="products container" aria-label="Supabase products"><div class="product-grid">'
for name, copy, url, art, kind in products:
    cards += f'<a class="product-card {kind}" href="{url}"><div class="product-copy"><h2>{escape(name)}</h2><p>{escape(copy)}</p>'
    if kind == 'database':
        cards += '<ul><li>100% portable</li><li>Built-in Auth with RLS</li><li>Easy to extend</li></ul>'
    if kind == 'vector':
        cards += '<small>OpenAI &nbsp; Hugging Face</small>'
    cards += '</div>'
    if kind == 'storage':
        cards += '<div class="storage-art" aria-hidden="true">' + ''.join('<span>▤</span>' for _ in range(12)) + '</div>'
    elif art:
        cards += img(art, f'Supabase {name} official illustration', 'product-art')
    cards += '</a>'
cards += '</div><p class="integrated">Use one or all. <strong>Best of breed products.</strong> Integrated as a platform.</p></section>'

customer_names = [
    ('Lovable', 'lovable'), ('Mozilla', 'mozilla'), ('PwC', 'pwc'),
    ('Figma', 'figma'), ('v0', 'v0'), ('Bolt', 'bolt'), ('GitHub', 'github'),
    ('BetaShares', 'betashares'), ('Mobbin', 'mobbin'), ('Resend', 'resend'),
    ('LangChain', 'langchain'), ('1Password', '1password'),
]
social = '<section class="social"><div class="container"><p>Trusted by fast-growing companies worldwide</p><div class="social-grid">' + ''.join(img('customer-' + file + '.svg', name) for name, file in customer_names) + '</div></div></section>'

dashboard = '''<section class="dashboard container"><h2><span>Stay productive and manage your app</span><br>without leaving the dashboard</h2><div class="dashboard-tabs" role="tablist" aria-label="Dashboard examples">'''
for i, (label, key) in enumerate((('Table Editor', 'table-editor'), ('SQL Editor', 'sql-editor'), ('RLS Policies', 'rls'))):
    dashboard += f'<button type="button" role="tab" data-dashboard="{key}" aria-selected="{str(i == 0).lower()}">{label}</button>'
dashboard += '''</div><div class="dashboard-window"><div class="window-dots"><i></i><i></i><i></i></div><video id="dashboard-video" autoplay muted loop playsinline preload="metadata" poster="supabase-assets/supabase-table-editor.png"><source src="supabase-assets/supabase-table-editor.webm" type="video/webm"></video></div></section>'''
for key in ('table-editor', 'sql-editor', 'rls'):
    for ext in ('png', 'webm'):
        assert (assets / f'supabase-{key}.{ext}').is_file()

framework = '<section class="framework container"><h2>Use Supabase with<br><span id="framework-name">React</span></h2><div class="framework-panel"><div class="framework-tabs" role="tablist" aria-label="Framework">'
for i, item in enumerate(examples):
    framework += f'<button type="button" role="tab" data-framework="{i}" aria-label="{escape(item["name"], quote=True)}" aria-selected="{str(i == 0).lower()}">{escape(item["name"])}</button>'
framework += '</div><pre><code id="framework-code">' + escape(examples[0]['code']) + '</code></pre><div class="framework-docs"><a id="framework-docs" href="' + escape(examples[0]['docs'], quote=True) + '">Read docs for React ↗</a></div></div></section>'

templates = [
    ('Stripe Subscriptions Starter', 'The all-in-one subscription starter kit for high-performance SaaS applications, powered by Stripe, Supabase, and Vercel.', 'https://github.com/supabase-community/nextjs-subscription-payments', 'stripe'),
    ('Next.js Starter', 'A Next.js App Router template configured with cookie-based auth using Supabase, TypeScript and Tailwind CSS.', 'https://github.com/vercel/next.js/tree/canary/examples/with-supabase', 'nextjs'),
    ('AI Chatbot', 'An open-source AI chatbot app template built with Next.js, the Vercel AI SDK, OpenAI, and Supabase.', 'https://github.com/supabase-community/vercel-ai-chatbot', 'openai'),
    ('LangChain + Next.js Starter', 'Starter template and example use-cases for LangChain projects in Next.js, including chat, agents, and retrieval.', 'https://github.com/langchain-ai/langchain-nextjs-template', 'langchain'),
    ('Flutter User Management', 'Get started with Supabase and Flutter by building a user management app with auth, file storage, and database.', 'https://github.com/supabase/supabase/tree/master/examples/user-management/flutter-user-management', 'flutter'),
    ('Expo React Native Starter', 'An extended version of create-t3-turbo implementing authentication on both the web and mobile applications.', 'https://github.com/supabase-community/create-t3-turbo', 'expo'),
]
template_html = '<section class="templates container"><div class="section-heading"><h2>Kickstart your next project<br><span>with production ready templates</span></h2>' + a('View all examples', 'https://supabase.com/docs/guides/examples') + '</div><div class="template-grid">'
for i, (name, copy, url, icon) in enumerate(templates):
    template_html += f'<a href="{url}" class="template-card {"large" if i < 2 else ""}">'
    template_html += img('template-' + icon + '.svg', icon)
    template_html += f'<h3>{escape(name)}</h3><p>{escape(copy)}</p>'
    if i < 2:
        template_html += '<div class="template-window" aria-hidden="true"><span></span><span></span><span></span><div></div></div>'
    template_html += '</a>'
template_html += '</div></section>'

stories = [
    ('Lovable', 'Powering millions of AI-generated apps with a complete Supabase backend.', 'Lovable is about unlocking creativity for anyone. Only 1% of the population knows how to code. Lovable has unlocked that ability for the other 99%.', 'Bryan Byrne, Product Manager, Lovable', 'https://supabase.com/customers/lovable', 'story-lovable.svg', 'lovable'),
    ('eXp Realty', 'Empowering 2,000+ employees to build production software with AI.', "The thing that makes everything possible, all of our rapid development now and AI-generated or assisted development, is Supabase. That's the giant whose shoulders we can stand on.", 'Seth Siegler, Chief Innovation Officer, eXp Realty', 'https://supabase.com/customers/exprealty', 'story-exprealty.svg', 'exprealty'),
    ('Phoenix Energy', 'Migrated critical infrastructure from MongoDB with zero downtime.', 'We needed a system that could handle serious performance and security requirements — without slowing down our developers. Supabase has given us both.', 'Kris Woods, CTO, Phoenix Energy', 'https://supabase.com/customers/phoenix-energy', 'story-phoenix.svg', 'phoenix'),
    ('Chatbase', 'Scaled from zero to $10M ARR on a single Postgres-backed platform.', "Instead of splitting things out as we go, we try to consolidate things more as we do. The technology itself works better when you have things that are closely tied together. That's why we're on Supabase.", 'Yasser Elsaid, Founder and CEO, Chatbase', 'https://supabase.com/customers/chatbase', 'story-chatbase.svg', 'chatbase'),
    ('Rally', 'From first line of code to fully licensed fintech in three months.', "We could not have built this company without Supabase. If I had to go and build all these components myself, we wouldn't even have launched.", 'Thiago Peres, Founder & CTO, Rally', 'https://supabase.com/customers/rally', 'story-rally.svg', 'rally'),
]
story_html = '<section class="stories container"><div class="section-heading"><h2>How industry leaders<br><span>are building with Supabase</span></h2>' + a('More customer stories', 'https://supabase.com/customers') + '</div><div class="story-grid" id="story-grid">'
for i, (name, summary, quote, author, url, icon, css) in enumerate(stories):
    story_html += f'<div class="story-card {css} {"active" if i == 0 else ""}" role="button" tabindex="0" aria-label="{escape(name, quote=True)}" aria-expanded="{str(i == 0).lower()}">'
    story_html += img(icon, name)
    story_html += f'<div class="story-text"><h3>{escape(name)}</h3><p>{escape(summary)}</p><blockquote>{escape(quote)}</blockquote><small>{escape(author)}</small>{a("Read the story →", url)}</div></div>'
story_html += '</div></section>'

community = '<section class="community"><div class="container"><h2>Join the community</h2><p>Discover what our community has to say about their Supabase experience.</p>' + a('Join us on Discord', 'https://discord.supabase.com/', 'dark-btn') + '</div></section>'
opensource = '<section class="opensource container"><h2>Open source from day one</h2><p>Supabase is built in the open because we believe great developer tools should be transparent, inspectable, and owned by the community. Read, contribute, self-host. You\'re never locked in, and always in control.</p>' + a('View on GitHub', 'https://github.com/supabase', 'dark-btn') + '</section>'
closing = '<section class="closing"><h2>Build in a weekend, <span>scale to millions</span></h2><div>' + a('Start your project', 'https://supabase.com/dashboard/sign-up', 'green-btn') + a('Request a demo', 'https://supabase.com/contact/sales', 'dark-btn') + '</div></section></main>'

footer_groups = {
    'Product': [('Pricing', 'https://supabase.com/pricing'), ('Database', 'https://supabase.com/database'), ('Auth', 'https://supabase.com/auth'), ('Functions', 'https://supabase.com/edge-functions'), ('Realtime', 'https://supabase.com/realtime'), ('Storage', 'https://supabase.com/storage'), ('Vector', 'https://supabase.com/modules/vector')],
    'Solutions': [('AI Builders', 'https://supabase.com/solutions/ai-builders'), ('No Code', 'https://supabase.com/solutions/no-code'), ('Developers', 'https://supabase.com/solutions/developers'), ('Startups', 'https://supabase.com/solutions/startups'), ('Enterprise', 'https://supabase.com/solutions/enterprise')],
    'Resources': [('Blog', 'https://supabase.com/blog'), ('Support', 'https://supabase.com/support'), ('System Status', 'https://status.supabase.com/'), ('Brand Assets', 'https://supabase.com/brand-assets'), ('Security & Compliance', 'https://supabase.com/security')],
    'Developers': [('Documentation', 'https://supabase.com/docs'), ('Supabase Library', 'https://supabase.com/library'), ('Changelog', 'https://supabase.com/changelog'), ('RSS', 'https://supabase.com/rss.xml')],
    'Community': [('Events & Webinars', 'https://supabase.com/events'), ('Contributing', 'https://github.com/supabase/supabase/blob/master/CONTRIBUTING.md'), ('Open Source', 'https://supabase.com/open-source')],
    'Company': [('Company', 'https://supabase.com/company'), ('Careers', 'https://supabase.com/careers'), ('Legal Hub', 'https://supabase.com/legal'), ('Privacy Policy', 'https://supabase.com/privacy'), ('Contact Us', 'https://supabase.com/contact-us')],
}
footer = '<footer class="footer"><div class="container"><div class="footer-security"><strong>We protect your data.</strong>' + a('More on Security', 'https://supabase.com/security') + '<span>SOC2 Type 2 Certified · HIPAA Compliant · ISO 27001 Certified</span></div><div class="footer-main"><div class="footer-brand">' + logo + '<p>© Supabase Inc</p></div>'
footer += ''.join('<div><h3>' + escape(group) + '</h3>' + ''.join(a(label, url) for label, url in links) + '</div>' for group, links in footer_groups.items())
footer += '</div></div></footer>'

style = '''<style>
:root{color-scheme:dark}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#121312;color:#eee;font-family:Inter,Arial,sans-serif;font-size:14px}button{font:inherit;cursor:pointer}a{color:inherit}.container{max-width:1088px;margin-left:auto;margin-right:auto}.announcement{height:55px;display:flex;align-items:center;justify-content:center;gap:10px;background:#0b0e0d;color:#e0e0e0;border-bottom:1px solid #252726;position:relative;overflow:hidden}.announcement>a{color:#9dc2ad;text-underline-offset:4px}.announcement>b{color:#777}.announcement>span{position:absolute;color:#26332c;white-space:nowrap;letter-spacing:4px;font-size:22px}.announcement>span:first-child{left:0}.announcement>span:last-child{right:0}.site-nav{height:64px;position:sticky;top:0;z-index:20;background:#121312f5;border-bottom:1px solid #262826;backdrop-filter:blur(8px)}.nav-inner{max-width:1088px;height:100%;margin:auto;display:flex;align-items:center;gap:40px}.brand{flex:none}.brand svg{width:124px;height:24px;display:block}.site-nav nav,.nav-right{display:flex;align-items:center;gap:24px}.site-nav nav a,.nav-right a{text-decoration:none;font-size:14px;white-space:nowrap;color:#dedede}.site-nav nav a:hover,.nav-right a:hover{color:#fff}.nav-right{margin-left:auto;gap:10px}.nav-right .stars{margin-right:6px;color:#aaa}.sign-in,.dark-btn{background:#1b1d1b;border:1px solid #343736;border-radius:7px;text-decoration:none;display:inline-flex;align-items:center;justify-content:center}.nav-right .sign-in{padding:5px 11px;font-size:12px}.green-btn{background:#327954;border:1px solid #41865f;color:#fff!important;border-radius:7px;text-decoration:none;display:inline-flex;align-items:center;justify-content:center;font-size:13px}.nav-right .green-btn{padding:5px 12px;font-size:12px}.hero{padding-top:162px}.hero-columns{display:grid;grid-template-columns:1fr 1fr;gap:16px}.hero h1{margin:0;font:400 46px/46px Manrope,Inter,sans-serif;letter-spacing:-.04em;color:#e8e8e8}.hero h1 span{color:oklch(.76 .15 157.5)}.hero p{margin:24px 0 0;color:#999;font-size:16px;line-height:24px;max-width:430px}.hero-actions{display:flex;gap:8px;margin-top:32px}.hero-actions a{min-height:38px;padding:0 15px}.hero-actions .dark-btn{color:#eee}.products{margin-top:64px}.product-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}.product-card{height:400px;position:relative;display:block;border:1px solid #2c2e2c;border-radius:12px;background:#1a1b1a;overflow:hidden;text-decoration:none;color:#eee;padding:26px 24px}.product-card:hover{border-color:#565b56}.product-card.database{grid-column:span 2}.product-copy{position:relative;z-index:2}.product-card h2{font-size:16px;font-weight:500;margin:6px 0 19px}.product-card p{color:#aaa;font-size:15px;line-height:20px;margin:0;max-width:280px}.product-card.database p{max-width:245px}.product-card ul{list-style:none;padding:0;margin:185px 0 0;color:#d3d3d3;font-size:13px}.product-card li{margin:9px 0}.product-card li:before{content:'✓';margin-right:8px}.product-card small{display:block;margin-top:170px;color:#c7c7c7}.product-art{position:absolute;bottom:0;left:0;width:100%;max-height:220px;object-fit:contain;object-position:bottom;opacity:.7}.database .product-art{left:auto;right:-25px;width:58%;max-height:320px;opacity:.34;filter:grayscale(1)}.auth .product-art,.edge .product-art{max-height:190px}.storage-art{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;position:absolute;bottom:14px;left:10px;right:10px}.storage-art span{height:62px;border:1px solid #272b29;background:#131514;border-radius:10px;text-align:center;padding-top:18px;color:#8c9690;font-size:20px}.realtime .product-art,.vector .product-art,.data-apis .product-art{max-height:225px}.integrated{text-align:center;color:#929292;font-size:20px;margin:20px 0 80px}.integrated strong{color:#d5d5d5;font-weight:400}.social{border-top:1px solid #272a27;border-bottom:1px solid #272a27;padding:60px 0 70px}.social p{text-align:center;color:#888;font-size:14px;margin:0 0 42px}.social-grid{display:grid;grid-template-columns:repeat(6,1fr);gap:32px 36px;align-items:center;justify-items:center}.social-grid img{max-width:100%;height:43px;object-fit:contain;opacity:.6}.dashboard{padding:90px 0 100px}.dashboard h2,.framework h2,.section-heading h2,.community h2,.opensource h2,.closing h2{font:400 34px/1.16 Manrope,Inter,sans-serif;letter-spacing:-.025em;margin:0}.dashboard h2{color:#858585}.dashboard h2 span{color:#e9e9e9}.dashboard-tabs{display:flex;gap:8px;margin:33px 0}.dashboard-tabs button{border:1px solid #282b28;background:#151615;border-radius:28px;color:#aaa;padding:9px 26px}.dashboard-tabs button[aria-selected=true]{border-color:#e4e4e4;color:#eee}.dashboard-window{padding:8px;border:1px solid #2a2d2a;border-radius:16px;background:#151615;overflow:hidden}.window-dots{height:25px;display:flex;align-items:center;gap:8px;padding-left:14px}.window-dots i{height:7px;width:7px;border-radius:50%;background:#343636}.dashboard video{display:block;width:100%;aspect-ratio:16/9;border-radius:8px;object-fit:cover}.framework{border-top:1px solid #272a27;border-bottom:1px solid #272a27;padding:85px 0;display:grid;grid-template-columns:1fr 1fr;gap:0}.framework h2{color:#888}.framework h2 span{color:#eee}.framework-panel{border:1px solid #2c2e2c;border-radius:8px;overflow:hidden;min-height:450px}.framework-tabs{display:grid;grid-template-columns:repeat(6,1fr);border-bottom:1px solid #2c2e2c}.framework-tabs button{height:58px;background:#151615;color:#aaa;border:0;border-right:1px solid #2c2e2c;font-size:12px}.framework-tabs button[aria-selected=true]{background:#232523;color:#eee}.framework pre{margin:0;padding:28px 24px;min-height:330px;overflow:auto;color:#cfcfcf;font:13px/1.7 'JetBrains Mono',monospace}.framework-docs{text-align:right;padding:10px 16px}.framework-docs a{display:inline-block;background:#1f211f;border:1px solid #2c2e2c;border-radius:18px;padding:8px 12px;text-decoration:none;color:#aaa;font-size:12px}.templates{padding:95px 0}.section-heading{display:flex;align-items:flex-end;justify-content:space-between;margin-bottom:54px}.section-heading h2{color:#888}.section-heading h2 span{color:#eee}.section-heading>a{color:#bbb;text-underline-offset:3px}.template-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}.template-card{position:relative;min-height:178px;border:1px solid #2b2e2b;border-radius:10px;background:#191b19;padding:22px 24px;text-decoration:none;overflow:hidden}.template-card.large{grid-column:span 2;height:330px}.template-card img{height:22px;max-width:80px;object-fit:contain}.template-card h3{font-size:15px;font-weight:500;margin:14px 0 8px}.template-card p{font-size:13px;line-height:1.4;color:#a1a1a1;margin:0}.template-window{position:absolute;left:24px;right:24px;bottom:-40px;height:170px;background:#121312;border:1px solid #333;border-radius:12px;padding:14px}.template-window span{display:inline-block;height:8px;width:8px;background:#353535;border-radius:50%;margin-right:5px}.template-window div{height:90px;background:repeating-linear-gradient(90deg,#1c1d1c 0 36px,#222 36px 42px);margin-top:20px}.stories{padding:95px 0;border-top:1px solid #272a27}.story-grid{display:grid;grid-template-columns:6fr .7fr .7fr .7fr .7fr;gap:8px;height:480px}.story-card{border-radius:8px;border:1px solid #ffffff20;padding:30px;overflow:hidden;cursor:pointer;color:white;min-width:0}.story-card>img{height:42px;max-width:70px;object-fit:contain}.story-card.lovable{background:linear-gradient(#fd49a8,#fa2733 40%,#ff8f1b)}.story-card.exprealty{background:#0c0f24}.story-card.phoenix{background:#002533}.story-card.chatbase{background:#000}.story-card.rally{background:linear-gradient(130deg,#484ece,#1e2dc4)}.story-card .story-text{display:none}.story-card.active .story-text{display:block}.story-card h3{font-size:15px;font-weight:500;margin:32px 0 6px}.story-card p{font-size:13px;color:#ffffffb0}.story-card blockquote{font-size:20px;line-height:1.35;margin:100px 0 15px;max-width:610px}.story-card small{display:block;color:#ffffffa8}.story-card a{display:inline-block;margin-top:26px;font-size:13px;color:#fff}.community{text-align:center;padding:90px 0 160px;border-top:1px solid #272a27}.community p{color:#999;font-size:16px}.community a{margin-top:15px;padding:10px 16px}.opensource{padding:100px 0;border-top:1px solid #272a27;border-bottom:1px solid #272a27}.opensource p{max-width:560px;color:#999;font-size:15px;line-height:1.5}.opensource a{margin-top:15px;padding:9px 14px}.closing{text-align:center;padding:120px 0}.closing h2{color:#888}.closing h2 span{color:#eee}.closing>div{display:flex;justify-content:center;gap:10px;margin-top:32px}.closing a{padding:10px 15px}.footer{border-top:1px solid #272a27;background:#101110;color:#999}.footer-security{padding:45px 0;border-bottom:1px solid #2a2d2a;display:flex;gap:20px;align-items:center}.footer-security strong{font-weight:500;color:#eee}.footer-security span{margin-left:auto}.footer-main{padding:55px 0;display:grid;grid-template-columns:1.6fr repeat(6,1fr);gap:22px}.footer-brand svg{width:124px;height:24px}.footer-brand p{margin-top:70px}.footer-main h3{font-size:13px;color:#ddd;font-weight:500;margin:0 0 15px}.footer-main a{display:block;text-decoration:none;color:#999;font-size:12px;line-height:2.25}.footer-main a:hover{text-decoration:underline}
@media(max-width:1160px){.container,.nav-inner{margin-left:24px;margin-right:24px}.site-nav nav,.nav-right{gap:12px}.nav-inner{gap:20px}}@media(max-width:850px){.site-nav nav{display:none}.nav-right{margin-left:auto}.hero{padding-top:100px}.product-grid{grid-template-columns:repeat(2,1fr)}.product-card.database{grid-column:span 2}.social-grid{grid-template-columns:repeat(4,1fr)}.template-grid{grid-template-columns:repeat(2,1fr)}.framework{grid-template-columns:1fr;gap:30px}.footer-main{grid-template-columns:repeat(3,1fr)}}@media(max-width:600px){.announcement{font-size:11px;text-align:center}.announcement>span{display:none}.nav-right .stars,.nav-right .sign-in{display:none}.hero{padding-top:70px}.hero-columns{grid-template-columns:1fr}.hero h1{font-size:38px;line-height:1.1}.hero p{margin-top:28px}.products{margin-top:50px}.product-grid{grid-template-columns:1fr}.product-card,.product-card.database{grid-column:auto;height:320px}.product-card.database{height:360px}.product-card ul{margin-top:120px}.product-card small{margin-top:100px}.social-grid{grid-template-columns:repeat(3,1fr)}.social-grid img{height:28px}.dashboard h2,.framework h2,.section-heading h2,.community h2,.opensource h2,.closing h2{font-size:29px}.dashboard-tabs button{padding:8px 12px;font-size:12px}.template-grid{grid-template-columns:1fr}.template-card.large{grid-column:auto}.story-grid{display:flex;flex-direction:column;height:auto}.story-card{min-height:65px}.story-card.active{min-height:470px}.story-card blockquote{margin-top:50px}.footer-security{display:block}.footer-security span{display:block;margin-top:18px}.footer-main{grid-template-columns:repeat(2,1fr)}}
</style>'''
style = style.replace('</style>', '''
.product-art{inset:auto 0 0;width:100%;height:100%;max-height:none;object-fit:cover;opacity:1}
.database .product-art{left:auto;right:0;width:256px;height:100%;max-height:none;object-fit:contain;opacity:1;filter:none}
.auth .product-art,.edge .product-art,.realtime .product-art,.data-apis .product-art{max-height:none}
.vector .product-art{left:auto;right:-30px;width:325px;height:358px;max-height:none;object-fit:contain}
</style>''')

scripts = '''<script>
for(const tab of document.querySelectorAll('[data-dashboard]'))tab.addEventListener('click',()=>{document.querySelectorAll('[data-dashboard]').forEach(x=>x.setAttribute('aria-selected',String(x===tab)));const key=tab.dataset.dashboard;const video=document.getElementById('dashboard-video');video.poster=`supabase-assets/supabase-${key}.png`;video.querySelector('source').src=`supabase-assets/supabase-${key}.webm`;video.load();video.play().catch(()=>{});});
const frameworkExamples=FRAMEWORK_EXAMPLES;
for(const tab of document.querySelectorAll('[data-framework]'))tab.addEventListener('click',()=>{document.querySelectorAll('[data-framework]').forEach(x=>x.setAttribute('aria-selected',String(x===tab)));const item=frameworkExamples[Number(tab.dataset.framework)];document.getElementById('framework-name').textContent=item.name;document.getElementById('framework-code').textContent=item.code;const docs=document.getElementById('framework-docs');docs.href=item.docs;docs.textContent=`Read docs for ${item.name} ↗`;});
const storyGrid=document.getElementById('story-grid');const storyCards=[...storyGrid.querySelectorAll('.story-card')];function showStory(card){storyCards.forEach(x=>{x.classList.toggle('active',x===card);x.setAttribute('aria-expanded',String(x===card))});storyGrid.style.gridTemplateColumns=storyCards.map(x=>x===card?'6fr':'.7fr').join(' ')}for(const card of storyCards){card.addEventListener('click',()=>showStory(card));card.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();showStory(card)}})}
</script>'''
scripts = scripts.replace('FRAMEWORK_EXAMPLES', json.dumps(examples, ensure_ascii=False).replace('</', '<\\/'))

head = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Supabase | The Postgres Development Platform</title><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&amp;family=Manrope:wght@400;500;600&amp;family=JetBrains+Mono:wght@400;500&amp;display=swap" rel="stylesheet">'''
html = head + style + '</head><body>' + header + hero + cards + social + dashboard + framework + template_html + story_html + community + opensource + closing + footer + scripts + '</body></html>\n'
assert 'stitch-placeholder' not in html and 'href="#"' not in html
for invented in ('Alex Rivera', 'Elena Rostova', 'Marcus Vance', 'S3 compatible API',
                 'WebSockets', 'PostgREST', 'Start building immediately without entering credit card information'):
    assert invented not in html
for title in ('Postgres Database', 'Stay productive and manage your app',
              'Use Supabase with', 'Open source from day one'):
    assert title in html
(ROOT / 'supabase.html').write_text(html)
print('Wrote Supabase current-reference draft:', len(html), 'characters')
