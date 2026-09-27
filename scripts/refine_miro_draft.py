#!/usr/bin/env python3
"""Build a dated Miro draft from the observed homepage and its public assets."""

from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / '.stitch-work' / 'current-official'
ASSETS = ROOT / 'miro-assets'


def asset(name):
    if not (ASSETS / name).is_file():
        raise FileNotFoundError(name)
    return 'miro-assets/' + name


def image(name, alt='', extra=''):
    return f'<img src="{asset(name)}" alt="{escape(alt, quote=True)}" {extra}>'


def link(label, href):
    return f'<a href="{escape(href, quote=True)}">{escape(label)}</a>'


case_studies = [
    ('PepsiCo', '3.6x', 'faster time to market', 'uIRqtTqzgtqaVuWSUgkiU6DGgI.jpeg', 'https://miro.com/customer-stories/'),
    ('ASOS', '50%', 'shorter planning process', 'GHMgTmbz8qR7eeU8e7Oo86AVxIQ.jpeg', 'https://miro.com/customer-stories/'),
    ('Keller Williams', '2x', 'faster time to market', 'ydQ4lfokqxcCYfp2CxNAzOzCc.jpeg', 'https://miro.com/customer-stories/'),
]
stories_html = ''.join(
    f'<a class="story" href="{href}">{image(file, company, "loading=lazy")}'
    f'<span class="story-shade"></span><span class="story-content"><span class="story-brand">{company}</span>'
    f'<span class="story-metric">{metric}</span><span class="story-label">{label}</span>'
    f'<span class="story-link">Read customer story ↗</span></span></a>'
    for company, metric, label, file, href in case_studies
)

features = [
    ('AI', 'Bring team and artificial intelligence together', 'qktnranaPpFcKWyM60NJD9VvI.png', 'https://miro.com/ai/ai-overview/'),
    ('Intelligent Canvas', 'Discover, define and deliver as one team on one canvas', 'Yuc5oFlUGxrhIlp7DDzijhyh3k.png', 'https://miro.com/product/'),
    ('Formats', 'Move work forward with formats you know', 'jEBfMRQ9CEbwCHlIsSZ8arK5Jt0.png', 'https://miro.com/product/'),
    ('Blueprints', 'Build workflows once, use them again and again', 'UE6PN5AkKpZr9wiHr9XmecEwBe8.png', 'https://miro.com/blueprints/'),
    ('Enterprise Security & Scale', 'Your data is secured. Period.', 't6nXozqt1IQNpt1ZoXulrivOM.png', 'https://miro.com/enterprise/'),
    ('Integrations', 'Connect Miro to 250+ of your top tools', 'wIqLXdrx2cUUItCcoSjzFjBMQ.png', 'https://miro.com/integrations/'),
]
features_html = ''.join(
    f'<a class="feature" href="{href}"><div class="feature-text"><h3>{escape(title)}</h3>'
    f'<p>{escape(body)}</p><span>Explore {escape(title)} ↗</span></div>'
    f'{image(file, title, "loading=lazy")}</a>'
    for title, body, file, href in features
)

resources = [
    ('Pricing', 'Select a plan', 'nDl7hMgk3lz5P8pMtAuj1ud7Hy8.png', 'https://miro.com/pricing/'),
    ('Templates', 'Get started fast', '9UpWE0ntDpz31gYdqHX0PnWoZo.png', 'https://miro.com/templates/'),
    ('Solution Partners', 'Explore the network', 'aWqMa3w2fGAiOiCaAifW1vI5iZ0.png', 'https://miro.com/find-a-partner/'),
    ('Community', 'Connect with Miro users', 'jE9EEchZdIvXR2nxDldppRlf4UQ.png', 'https://community.miro.com/'),
    ('Blog', 'Dive in to ways of working', '54fgARxfE1yaO0U194V6yowtGTQ.png', 'https://miro.com/blog/'),
    ('Academy', 'Get started with Miro', '3aN9meKGAp4IQCF4QoQfjFiK0c.png', 'https://academy.miro.com/'),
]
resources_html = ''.join(
    f'<a class="resource" href="{href}"><div class="resource-text"><span>{escape(kind)} ↗</span>'
    f'<h3>{escape(title)}</h3></div>{image(file, title, "loading=lazy")}</a>'
    for kind, title, file, href in resources
)

footer_columns = [
    ('Product', [('Apps & Integrations', '/integrations/'), ('Templates', '/templates/'),
                 ('Miro Developer Platform', 'https://developers.miro.com/'), ('Miro for Devices', '/apps/'),
                 ('Enterprise Guard', '/products/enterprise-guard/'), ('Accessibility', '/accessibility/'),
                 ('Changelog', '/changelog/')]),
    ('Solutions', [('AI Platform', '/ai/ai-overview/'), ('Product Acceleration', '/solutions/product-acceleration/'),
                   ('Business Acceleration', '/solutions/business-acceleration/'), ('Platform and Capabilities', '/products/platform-overview/')]),
    ('Tools', [('Agile Tools', '/agile/'), ('Graphs', '/graphs/'), ('Online Sticky Notes', '/online-sticky-notes/'),
               ('Customer Journey Mapping', '/customer-journey-map/'), ('Wireframe', '/wireframe/'),
               ('Kanban Board', '/kanban/'), ('AI Prototype Generator', '/ai/prototype-ai/'),
               ('AI Wireframe Generator', '/ai/wireframe/'), ('AI Diagram Generator', '/ai/diagram-ai/')]),
    ('Resources', [('Customer Stories', '/customers/'), ('Miro Academy', 'https://academy.miro.com/'),
                   ('Help Center', 'https://help.miro.com/hc/en-us'), ('Blog', '/blog/'), ('Status', 'https://status.miro.com/'),
                   ('Miro Community', '/community/'), ('Miro Events', 'https://community.miro.com/events'),
                   ('Solution Partners', '/partners/solution-partners/'), ('Miro Security', 'https://trust.miro.com/')]),
    ('Company', [('About Us', '/about/'), ('Careers 🚀', '/careers/'), ('Miro in the News', '/newsroom/')]),
    ('Plans & Pricing', [('Pricing', '/pricing/'), ('Business', '/business-plan/'), ('Enterprise', '/enterprise/'),
                         ('Consultants', '/consultants-agencies/'), ('Education', '/education-whiteboard/'),
                         ('Startups', '/startups/'), ('NPOs', '/npo/'), ('Contact sales →', '/contact/sales/')]),
]
footer_html = ''.join(
    f'<nav aria-label="{escape(title)}"><h3>{escape(title)}</h3>'
    + ''.join(link(label, path if path.startswith('https:') else 'https://miro.com' + path)
              for label, path in entries) + '</nav>'
    for title, entries in footer_columns
)

css = r'''
@font-face{font-family:Roobert;src:url("miro-assets/IWIJ9TEwVer0sH7Pi9PuwiGLfPI.woff2") format("woff2");font-style:normal;font-weight:500;font-display:swap}
@font-face{font-family:RoobertSemi;src:url("miro-assets/ynxJLpJmNmhxBFJOqRq8uP2oWE.woff2") format("woff2");font-style:normal;font-weight:600;font-display:swap}
:root{--ink:#1c1c1e;--blue:#3859ff;--muted:#555a6a;--line:#e9e9ef;--cream:#f7f7fa}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;color:var(--ink);background:white;font:16px/1.5 Roobert,Arial,sans-serif}a{color:inherit;text-decoration:none}a:hover{text-decoration:underline}button,input{font:inherit}button{cursor:pointer}h1,h2,h3,p{margin-top:0}h1,h2,h3{font-family:Roobert,Arial,sans-serif;font-weight:500;letter-spacing:-.025em}img{display:block;max-width:100%}.wrap{width:min(calc(100% - 64px),1152px);margin:0 auto}.primary{display:inline-flex;align-items:center;justify-content:center;background:linear-gradient(#6075ff,#3b54ee);color:white;border:1px solid #4961f5;border-radius:8px;box-shadow:0 1px 2px #344bd437;min-height:48px;padding:0 20px;font-family:RoobertSemi,Roobert,Arial,sans-serif;font-size:16px}.primary:hover{text-decoration:none;background:#3859ff}.outline{display:inline-flex;align-items:center;justify-content:center;border:1px solid #d7d7dc;border-radius:8px;min-height:42px;padding:0 14px;box-shadow:0 1px 3px #0001;font-family:RoobertSemi,Roobert,Arial,sans-serif}.outline:hover{text-decoration:none;background:#f7f7fa}.text-link{display:inline-flex;color:#3859ff;font-family:RoobertSemi,Roobert,Arial,sans-serif}
.header{height:72px;position:sticky;top:0;z-index:100;display:flex;align-items:center;gap:32px;padding:0 16px;background:#fff;border-bottom:1px solid #e8e8e8;box-shadow:0 1px 2px #0001}.brand{display:flex;align-items:center;gap:7px;flex:none;font-family:RoobertSemi,Roobert,Arial,sans-serif;font-size:32px;line-height:1;letter-spacing:-.06em}.brand img{width:40px;height:40px}.main-nav{display:flex;gap:30px;align-items:center;font-size:16px;white-space:nowrap}.main-nav a{display:flex;align-items:center;gap:7px}.chev{width:7px;height:7px;border-right:1.5px solid;border-bottom:1.5px solid;transform:rotate(45deg) translateY(-3px)}.header-actions{margin-left:auto;display:flex;gap:12px;align-items:center;white-space:nowrap}.header-actions>a:first-child{padding:8px 12px}.header-actions .primary{min-height:40px}.mobile-nav{display:none}
.hero{position:relative;overflow:hidden;text-align:center;padding:47px 0 0;background:radial-gradient(ellipse 50% 33% at 49% 73%,#dcd5ff88,transparent 75%),radial-gradient(ellipse 30% 20% at 75% 75%,#ffe8c599,transparent 80%),radial-gradient(circle at 1px 1px,#d9d9df 1px,transparent 1.5px);background-size:auto,auto,20px 20px}.hero h1{font-size:48px;line-height:1.02;max-width:560px;margin:0 auto 24px;letter-spacing:-.035em}.hero-intro{font-size:20px;line-height:1.25;color:#555a6a;max-width:545px;margin:0 auto 28px}.hero-form{width:280px;margin:0 auto}.hero-form input{display:block;width:100%;height:48px;border:1px solid #dddfe8;background:#fff;border-radius:8px;padding:0 16px;outline-color:var(--blue)}.hero-form .primary{width:100%;margin-top:16px}.hero-form small{display:block;margin:9px auto 0;color:#666b79;font-size:14px}.hero-board{position:relative;width:min(768px,calc(100% - 32px));height:470px;margin:80px auto 0;text-align:left}.board-chip{position:absolute;top:0;left:1px;border-radius:7px;background:white;padding:4px 8px;box-shadow:0 2px 12px #0002;font-size:11px}.board-window{position:absolute;inset:40px 0 0;background:#fff;border:1px solid #e7e7ed;border-radius:14px 14px 0 0;box-shadow:0 8px 42px #22254a22;overflow:hidden}.board-top{height:42px;display:flex;align-items:center;justify-content:space-between;background:#f7f8fa;border-bottom:1px solid #eee;color:#565b66;font-size:10px;padding:0 18px}.board-body{display:grid;grid-template-columns:217px 1fr;height:388px}.board-side{border-right:1px solid #eee;padding:18px 10px}.board-side span{display:block;height:26px;border:1px solid #e9ebef;border-radius:4px;margin-bottom:8px;background:linear-gradient(90deg,#e9e9ed 65%,transparent 65%)}.board-grid{position:relative;display:grid;grid-template-columns:repeat(7,1fr);grid-template-rows:40px 1fr;background:repeating-linear-gradient(90deg,#fff 0,#fff calc(14.285% - 1px),#eff0f4 calc(14.285% - 1px),#eff0f4 14.285%)}.board-grid b{font-size:10px;font-weight:400;text-align:center;padding-top:12px;color:#777b87}.timeline{position:absolute;height:23px;border-radius:5px;border:1px solid #d68f91;background:#eeb2b4b8;top:88px;left:23%;width:64%}.timeline.two{top:127px;left:9%;width:32%;background:#c6bafb;border-color:#ab97f3}.timeline.three{top:165px;left:43%;width:42%;background:#bfe5d1;border-color:#9ad2b1}.timeline.four{top:205px;left:10%;width:72%;background:#ffe3a7;border-color:#e7bd6b}.timeline.five{top:244px;left:28%;width:49%;background:#c6d4ff;border-color:#abc0f7}
.trusted{padding:75px 0 115px;text-align:center}.trusted p{color:#6d7180;font-size:15px}.logos{display:flex;align-items:center;justify-content:space-around;gap:35px;flex-wrap:wrap;margin:55px auto 0;max-width:1030px;font-family:RoobertSemi,Roobert,Arial,sans-serif;font-size:22px;letter-spacing:-.05em;color:#343946}.logos span:nth-child(3){font-style:italic;font-size:29px}.logos span:nth-child(4){letter-spacing:0;font-size:18px}.logos span:nth-child(6){font-size:20px}
.research{padding:10px 0 125px}.research-tabs{display:grid;grid-template-columns:repeat(4,1fr);border-bottom:1px solid #e5e7ed}.research-tabs a{text-align:left;background:none;border:0;border-bottom:5px solid transparent;padding:0 0 23px;font:500 21px Roobert,Arial,sans-serif;color:#9295a0}.research-tabs a[aria-current=true]{color:#1c1c1e;border-bottom-color:#ffdb39}.research-grid{display:grid;grid-template-columns:48% 52%;gap:0;align-items:center;padding-top:70px}.research-copy{max-width:445px}.research-copy h2{font-size:40px;line-height:1.1;margin-bottom:25px}.research-copy p{font-size:16px;color:#555a6a;line-height:1.55}.research-copy .text-link{margin-top:16px}.research-art{border-radius:18px;overflow:hidden;background:#f8f8fa;min-height:300px;display:grid;place-items:center}.research-art img{width:100%;height:100%;object-fit:cover}
.stories{background:#f7f7fa;padding:96px 0 86px}.stories-head{max-width:820px;margin:0 auto 50px;text-align:center}.stories h2{font-size:48px;line-height:1.04;margin-bottom:18px}.stories-head p{font-size:19px;color:#555a6a}.story-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.story{height:590px;border-radius:20px;overflow:hidden;position:relative;color:white;background:#343946}.story>img{width:100%;height:100%;object-fit:cover}.story-shade{position:absolute;inset:0;background:linear-gradient(#0006,transparent 47%,#000a)}.story-content{position:absolute;inset:24px;display:flex;flex-direction:column}.story-brand{font:600 28px RoobertSemi,Arial,sans-serif}.story-metric{font:500 67px/1 Roobert,Arial,sans-serif;margin-top:auto}.story-label{font-size:19px}.story-link{font-size:15px;margin-top:28px}.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:30px;padding-top:90px;text-align:center}.stats strong{display:block;font:500 54px/1 Roobert,Arial,sans-serif}.stats span{display:block;margin-top:10px;color:#555a6a}
.flow{padding:110px 0 50px;text-align:center}.flow h2{font-size:45px;margin-bottom:30px}.flow img{max-width:780px;margin:auto}.experience{padding:55px 0 130px;overflow:hidden}.section-head{display:flex;align-items:end;justify-content:space-between;gap:30px;margin-bottom:40px}.section-head h2{font-size:48px;line-height:1.05;max-width:700px;margin:0}.carousel-controls{display:flex;gap:12px}.carousel-controls button{width:40px;height:40px;border:0;border-radius:50%;background:white;box-shadow:0 2px 8px #0002;font-size:22px}.carousel{display:flex;gap:16px;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;padding-bottom:8px}.carousel::-webkit-scrollbar{display:none}.feature{scroll-snap-align:start;flex:0 0 380px;display:flex;flex-direction:column;border:1px solid #e9e9ee;border-radius:20px;overflow:hidden;background:#f9f9fb;min-height:530px}.feature:hover{text-decoration:none}.feature-text{padding:28px}.feature h3{font-size:30px;margin:0 0 10px}.feature p{color:#555a6a;font-size:16px;min-height:53px}.feature span{font-size:15px;color:#3859ff}.feature img{width:100%;height:300px;object-fit:contain;margin-top:auto;background:#fff}
.ai-platform{padding:80px 0 110px;text-align:center;background:#f8f8fb}.ai-platform h2{font-size:48px;margin:0 auto 16px}.ai-platform p{font-size:20px;color:#555a6a;max-width:640px;margin:0 auto 24px}.ai-platform>div>img{width:min(900px,100%);margin:55px auto 0;border-radius:17px;box-shadow:0 18px 45px #292d3d16}
.resources{padding:110px 0 140px;overflow:hidden}.resources h2{font-size:48px;margin:0 0 40px}.resource{scroll-snap-align:start;flex:0 0 320px;display:flex;flex-direction:column;border:1px solid #e8e9ee;border-radius:20px;overflow:hidden;height:370px;background:#fff}.resource:hover{text-decoration:none}.resource-text{padding:24px 24px 0}.resource-text span{color:#666a78;font-size:14px}.resource h3{font-size:27px;margin:12px 0}.resource img{width:100%;height:230px;object-fit:contain;margin-top:auto}.resources .carousel-controls{justify-content:flex-end;margin-top:25px}
.footer{background:#1c1c1e;color:#f8f8f8;padding:52px 0 35px}.footer-columns{display:grid;grid-template-columns:repeat(6,1fr);gap:25px}.footer h3{font:600 18px RoobertSemi,Arial,sans-serif;margin:0 0 16px}.footer nav a{display:block;font-size:14px;line-height:1.4;margin-bottom:10px;color:#e5e5e7}.footer nav a:hover{color:white}.footer-bottom{border-top:1px solid #4d4d50;margin-top:80px;padding-top:25px;display:flex;justify-content:space-between;gap:25px;color:#cbcbce;font-size:13px}
@media(max-width:900px){.header{gap:12px}.main-nav{gap:15px;font-size:14px}.header-actions{gap:4px}.header-actions>a:first-child{display:none}.hero h1{font-size:43px}.story-grid{gap:10px}.story{height:450px}.story-metric{font-size:50px}.footer-columns{grid-template-columns:repeat(3,1fr)}}
@media(max-width:680px){.wrap{width:min(calc(100% - 32px),1152px)}.header{height:64px}.brand{font-size:27px}.brand img{width:35px;height:35px}.main-nav,.header-actions .outline{display:none}.header-actions .primary{font-size:14px;min-height:36px;padding:0 11px}.mobile-nav{display:inline-flex;border:0;background:none;font-size:24px;padding:0 4px}.mobile-menu{display:none;position:fixed;top:64px;left:0;right:0;background:white;padding:18px 24px;box-shadow:0 10px 20px #0002;z-index:99}.mobile-menu.open{display:grid;gap:16px}.hero{padding-top:55px}.hero h1{font-size:38px;padding:0 15px}.hero-intro{font-size:17px;padding:0 16px}.hero-board{margin-top:65px;height:340px;width:calc(100% - 22px)}.board-window{height:320px}.board-body{grid-template-columns:28% 72%;height:278px}.board-grid b{font-size:8px}.trusted{padding:50px 0 75px}.logos{gap:18px;margin-top:32px}.logos span{font-size:18px!important}.research{padding-bottom:85px}.research-tabs a{font-size:15px;padding-bottom:15px}.research-grid{grid-template-columns:1fr;padding-top:48px}.research-copy h2{font-size:34px}.research-art{margin-top:28px}.stories{padding:70px 0}.stories h2,.section-head h2,.ai-platform h2,.resources h2{font-size:35px}.stories-head p,.ai-platform p{font-size:17px}.story-grid{display:flex;overflow-x:auto;scroll-snap-type:x mandatory}.story{flex:0 0 78vw;height:460px;scroll-snap-align:start}.stats{gap:10px;padding-top:65px}.stats strong{font-size:35px}.stats span{font-size:12px}.flow{padding:80px 0 30px}.flow h2{font-size:33px}.section-head{align-items:center}.feature{flex-basis:82vw;min-height:460px}.feature img{height:260px}.experience{padding-bottom:85px}.ai-platform{padding:70px 0 80px}.resources{padding:80px 0 95px}.resource{flex-basis:78vw}.footer-columns{grid-template-columns:repeat(2,1fr);gap:30px}.footer-bottom{margin-top:45px;flex-direction:column}}
'''

page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Miro — Current Official Homepage Draft</title><style>{css}</style></head><body>
<header class="header"><a class="brand" href="https://miro.com/">{image('6FBG66PBxjV2QFaDfIdUi5mi9A.png','')}<span>miro</span></a><nav class="main-nav" aria-label="Main navigation"><a href="https://miro.com/product/">Product <span class="chev"></span></a><a href="https://miro.com/use-cases/">Use Cases <span class="chev"></span></a><a href="https://miro.com/solutions/">Solutions <span class="chev"></span></a><a href="https://miro.com/resources/">Resources <span class="chev"></span></a><a href="https://miro.com/pricing/">Pricing</a></nav><div class="header-actions"><a href="https://miro.com/login/">Login</a><a class="outline" href="https://miro.com/contact/sales/">Contact sales</a><a class="primary" href="https://miro.com/signup/">Get started free</a><button class="mobile-nav" type="button" aria-label="Open menu" aria-expanded="false">☰</button></div></header><nav class="mobile-menu" aria-label="Mobile navigation"><a href="https://miro.com/product/">Product</a><a href="https://miro.com/use-cases/">Use Cases</a><a href="https://miro.com/solutions/">Solutions</a><a href="https://miro.com/resources/">Resources</a><a href="https://miro.com/pricing/">Pricing</a><a href="https://miro.com/contact/sales/">Contact sales</a></nav>
<main><section class="hero"><h1>Human collaboration<br>at the speed of AI</h1><p class="hero-intro">Where your team and AI think, plan, and build together, in a workspace that works the way you do.</p><form class="hero-form" action="https://miro.com/signup/" method="get"><input aria-label="Work email" type="email" name="email" placeholder="Enter your work email" required><button class="primary" type="submit">Get started free</button><small>No credit card needed.</small></form><div class="hero-board" aria-label="Illustration of a Miro roadmap board"><span class="board-chip">✳ Q3 Product Release</span><div class="board-window"><div class="board-top"><span>‹ &nbsp;▦ &nbsp;›</span><span>September &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; October</span><span>⋮</span></div><div class="board-body"><div class="board-side"><span></span><span></span><span></span><span></span><span></span></div><div class="board-grid"><b>2</b><b>9</b><b>16</b><b>23</b><b>30</b><b>7</b><b>14</b><i class="timeline"></i><i class="timeline two"></i><i class="timeline three"></i><i class="timeline four"></i><i class="timeline five"></i></div></div></div></div></section>
<section class="trusted wrap"><p>Trusted by teams at the world's leading companies</p><div class="logos" aria-label="Customer names"><span>SONY</span><span>PayPal</span><span>Ubisoft</span><span>workday</span><span>Deloitte.</span><span>salesforce</span></div></section>
<section class="research wrap"><div class="research-tabs" aria-label="Miro use cases"><a href="#research-heading" aria-current="true">Research</a><a href="https://miro.com/roadmap/">Roadmaps</a><a href="https://miro.com/capabilities/diagrams/">Diagrams</a><a href="https://miro.com/meetings-and-workshops/">Workshops</a></div><div class="research-grid"><div class="research-copy"><h2 id="research-heading">Turn research into a shared direction</h2><p id="research-body">Pull outputs from Claude, NotebookLM, or any research tool into one canvas. Your team reviews the findings together, surfaces what matters, and commits to a direction — then flow the insights back out to your roadmap, specs, or next AI prompt.</p><a id="research-link" class="text-link" href="https://miro.com/solutions/research/">Explore research ↗</a></div><div class="research-art">{image('TUnQ4cxR4MCJxGldUuwR6dA.png','Miro research workflow canvas','loading=lazy')}</div></div></section>
<section class="stories"><div class="wrap"><div class="stories-head"><h2>The only thing more important than moving fast is moving the needle</h2><p>See how over 250,000 companies are getting great done in Miro.</p></div><div class="story-grid">{stories_html}</div><div class="stats"><div><strong>100M+</strong><span>people collaborating on Miro</span></div><div><strong>250+</strong><span>apps and integrations</span></div><div><strong>6,000+</strong><span>templates</span></div></div></div></section>
<section class="flow wrap"><h2>Flow from idea to outcome in seconds</h2>{image('Yuc5oFlUGxrhIlp7DDzijhyh3k.png','Discover, define and deliver as one team','loading=lazy')}</section>
<section class="experience wrap"><div class="section-head"><h2>Experience the Innovation Workspace</h2><div class="carousel-controls"><button type="button" data-scroll="features" data-direction="-1" aria-label="Previous feature">‹</button><button type="button" data-scroll="features" data-direction="1" aria-label="Next feature">›</button></div></div><div class="carousel" id="features">{features_html}</div></section>
<section class="ai-platform"><div class="wrap"><h2>The AI platform for teamwork</h2><p>Move beyond individual AI productivity to team and cross-team collaboration with AI.</p><a class="primary" href="https://miro.com/ai/ai-overview/">Explore Miro AI ↗</a>{image('qktnranaPpFcKWyM60NJD9VvI.png','Miro AI canvas for teamwork','loading=lazy')}</div></section>
<section class="resources wrap"><h2>Need help getting started?</h2><div class="carousel" id="resources">{resources_html}</div><div class="carousel-controls"><button type="button" data-scroll="resources" data-direction="-1" aria-label="Previous resource">‹</button><button type="button" data-scroll="resources" data-direction="1" aria-label="Next resource">›</button></div></section></main>
<footer class="footer"><div class="wrap"><div class="footer-columns">{footer_html}</div><div class="footer-bottom"><span>© 2026 Miro</span><span>{link('Privacy Policy','https://miro.com/privacy-policy/')} &nbsp; {link('Terms of Service','https://miro.com/terms-of-service/')}</span></div></div></footer>
<script>
document.querySelector('.mobile-nav').addEventListener('click',function(){{const menu=document.querySelector('.mobile-menu');const open=menu.classList.toggle('open');this.setAttribute('aria-expanded',String(open));}});
document.querySelectorAll('[data-scroll]').forEach(button=>button.addEventListener('click',()=>{{document.getElementById(button.dataset.scroll).scrollBy({{left:Number(button.dataset.direction)*395,behavior:'smooth'}});}}));
</script></body></html>'''

(ROOT / 'miro.html').write_text(page)
print(f'Wrote {ROOT / "miro.html"} ({len(page)} characters)')
