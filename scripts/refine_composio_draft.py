#!/usr/bin/env python3
"""Refine the Stitch Composio screen using the dated public-site reference."""

import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / '.stitch-work' / 'current-official'
ASSETS = ROOT / 'composio-assets'


def asset(name):
    if not (ASSETS / name).is_file():
        raise FileNotFoundError(name)
    return 'composio-assets/' + name


trusted = [
    ('Glean', 'customers-logos-glean.svg'),
    ('Zoom', 'customers-logos-zoom.webp'),
    ('AWS', 'customers-logos-aws.svg'),
    ('Google', 'customers-logos-google-wordmark.svg'),
    ('Wix', 'customers-logos-wix-real.svg'),
    ('Browser Use', 'customers-logos-browseruse-trim2.webp'),
    ('Emergent', 'customers-logos-emergent.svg'),
    ('Island', 'customers-logos-island-wordmark.svg'),
    ('Athena', 'customers-logos-athena-wordmark.svg'),
    ('Sarvam', 'customers-logos-sarvam.svg'),
    ('Hostinger', 'customers-logos-hostinger-wordmark.svg'),
    ('Arizona State University', 'customers-logos-asu-wordmark.webp'),
    ('Pelago Health', 'customers-logos-logo-pelago-black.png'),
    ('ClickFunnels', 'customers-logos-clickfunnels-wordmark.svg'),
]
trusted_html = ''.join(
    f'<img src="{asset(file)}" alt="{escape(name)}" loading="lazy">'
    for name, file in trusted
)

features = [
    {
        'label': 'NO CONTEXT BLOAT', 'title': 'The right actions, without the context bloat',
        'body': 'Every action your AI knows about takes up context. Composio searches the full catalogue and loads only what your task needs, then suggests a plan and adds guardrails.',
        'points': ['Match actions & tools to what the user wants', 'Plan the steps before execution', 'Catch common issues before tool calls run'],
        'bg': 'images-tool-calls-bg.webp',
        'visual': '<div class="terminal"><div class="terminal-search">⌕ &nbsp; list sentry errors and create linear... <small>3 found</small></div><div class="terminal-line"><b>◈</b> SENTRY_LIST_ISSUES <em>MATCH</em></div><div class="terminal-line"><b>◈</b> SENTRY_GET_EVENT <em>MATCH</em></div><div class="terminal-line"><b>◈</b> LINEAR_CREATE_ISSUE <em>MATCH</em></div><div class="terminal-plan">PLAN <span>WARNINGS</span><br>1 &nbsp;Fetch all open Sentry issues<br>2 &nbsp;Classify severity in sandbox<br>3 &nbsp;Create Linear issues for P0s</div></div>',
    },
    {
        'label': 'BETTER EVERY TIME', 'title': 'Works today, works better next time',
        'body': 'Real-world agent behavior helps Composio refine how apps and actions are selected, structured, and executed over time.',
        'points': ['Fewer failed requests over time', 'Account-level tuning for how your agents work', 'Stable integrations, optimized for agent execution'],
        'bg': 'images-constant-evolution-bg.webp',
        'visual': '<div class="terminal"><div class="terminal-search">✉ &nbsp; GMAIL_SEND_EMAIL <small>v2.1.3</small></div><div class="terminal-line error">400 &nbsp; Invalid recipient format: display name not allowed in "to" field</div><div class="terminal-line success">↻ &nbsp; COMPOSIO ADAPTED THE REQUEST</div><div class="terminal-line">Retrying with verified email address...</div></div>',
    },
    {
        'label': 'ONE-CLICK CONNECTIONS', 'title': 'One click to connect, whenever you need it',
        'body': 'Connect apps from your Composio dashboard or sign in when your AI needs one. Either way, it’s a quick, one-time secure sign-in per app.',
        'points': ['OAuth flows managed end to end', 'Connections initiated inside the workflow', 'Granular scopes for each connected account'],
        'bg': 'images-end-user-auth-bg.webp',
        'visual': '<div class="terminal auth-window"><strong>Connect your tools</strong><p>Give your agent permission to work across the apps you use.</p><div>◉ &nbsp; Google Sheets <span>CONNECTED</span></div><div>◈ &nbsp; Instagram <span>CONNECT ↗</span></div><div>◉ &nbsp; Gmail <span>CONNECTED</span></div></div>',
    },
    {
        'label': 'AGENT RUNTIME', 'title': 'A workspace for multi-step work',
        'body': 'When a task needs more than one action, Composio gives your AI a remote runtime for code, actions, files, and intermediate results, with each execution in its own isolated sandbox.',
        'points': ['Chain tools and model calls programmatically', 'Keep large responses out of the context window', 'Give every execution its own isolated sandbox'],
        'bg': 'images-dynamic-sandbox.webp',
        'visual': '<div class="terminal code"><span>FETCH & TRIAGE ERRORS</span> &nbsp; sandbox · py 3.11<br><br>issues = run_composio_tool(<br>&nbsp; "SENTRY_LIST_ISSUES", status="unresolved"<br>)<br>ranked = invoke_llm(issues)<br>for error in ranked["P0"]:<br>&nbsp; run_composio_tool("LINEAR_CREATE_ISSUE")</div>',
    },
]
features_html = ''.join(
    f'<article class="feature-row" id="feature-{i}"><div class="feature-visual" style="background-image:url({asset(f["bg"])})">{f["visual"]}</div>'
    f'<div class="feature-copy"><span class="feature-number">0{i}</span><h3>{escape(f["title"])}</h3><p>{escape(f["body"])}</p>'
    f'<ul>{"".join("<li>" + escape(p) + "</li>" for p in f["points"])}</ul></div></article>'
    for i, f in enumerate(features, 1)
)
tabs_html = ''.join(
    f'<a href="#feature-{i}"><span>0{i}</span>{escape(f["label"])}</a>'
    for i, f in enumerate(features, 1)
)

use_cases = [
    ('Email and calendar', 'https://composio.dev/product/composio-for-everyday-ai-users',
     ['Show me today’s meetings and the emails that need a reply',
      'Draft replies to the emails that need a response',
      'Find a free hour next week for a meeting with Sarah and send her an invite'],
     ['Gmail', 'Google Calendar', 'Outlook', 'Slack']),
    ('Docs and files', 'https://composio.dev/for-you',
     ['Find the notes from Monday’s planning meeting in Google Drive',
      'Pull out the decisions and next steps from our meeting notes in Google Docs',
      'Add the action items from our meeting notes to the tracker in Google Sheets'],
     ['Google Drive', 'Google Sheets', 'Google Docs']),
    ('Development', 'https://composio.dev/product/composio-for-engineering-devops',
     ['Summarize what changed in the repo since the last release',
      'Show this week’s new signups from Supabase',
      'Fix this Linear issue and open a pull request for review'],
     ['GitHub', 'Supabase', 'Linear', 'Vercel']),
    ('Social media', 'https://composio.dev/product/composio-for-content-media',
     ['Show my top-performing Instagram posts and YouTube videos this week',
      'Find unanswered questions in my Instagram comments and DMs',
      'Post this week’s announcement to Instagram, Facebook and LinkedIn'],
     ['Instagram', 'Facebook', 'LinkedIn', 'YouTube']),
    ('Ads and SEO', 'https://composio.dev/product/composio-for-marketing-growth',
     ['Show my top Google search terms and landing pages this month',
      'Compare cost per lead across my Google and Meta ad campaigns',
      'Pause Google Ads keywords that spent over $100 with no leads this month'],
     ['Google Search Console', 'Google Analytics', 'Google Ads', 'Meta Ads']),
    ('Sales and CRM', 'https://composio.dev/product/composio-for-sales-revenue',
     ['Find the deals that haven’t moved forward in two weeks',
      'Draft follow-up emails in Gmail for my stalled HubSpot deals',
      'Add the new leads from my inbox to HubSpot'],
     ['HubSpot', 'Salesforce', 'Gmail']),
]
use_cases_html = ''.join(
    f'<article class="case-card"><h3><a href="{escape(url)}">{escape(title)} <span>↗</span></a></h3>'
    f'<ul>{"".join("<li>" + escape(p) + "</li>" for p in prompts)}</ul>'
    f'<p class="case-apps">{"".join("<span>" + escape(app) + "</span>" for app in apps)}</p></article>'
    for title, url, prompts, apps in use_cases
)

developer_features = [
    ('Managed Auth', 'OAuth, API keys, token refresh, lifecycle management. We handle all of it so you never think about auth again.', 'https://docs.composio.dev/docs/authentication'),
    ('Triggers', 'Bidirectional communication with your apps to keep your agents informed.', 'https://docs.composio.dev/docs/triggers'),
    ('Context Aware Sessions', 'Every session carries full context — sandbox state, files, progress. Your agent never starts from scratch.', 'https://docs.composio.dev/docs/users-and-sessions'),
    ('Model & Framework Agnostic', 'No lock-in. Swap models based on cost, capability, or use case. Your tools and auth carry over, zero rework.', 'https://docs.composio.dev/docs/providers'),
]
developer_html = ''.join(
    f'<article><h4>{escape(title)}</h4><p>{escape(body)}</p><a href="{escape(url)}">READ THE DOCS</a></article>'
    for title, body, url in developer_features
)

faqs = json.loads((ROOT / 'composio-browser-faq.json').read_text())
assert len(faqs) == 11
faq_html = ''.join(
    f'<details><summary>{escape(item["question"])}<span>+</span></summary>'
    + ''.join(f'<p>{escape(block)}</p>' for block in item['blocks'])
    + '</details>'
    for item in faqs
)

footer_columns = [
    ('PRODUCTS', [('COMPOSIO FOR YOU','/for-you'),('DEVELOPER PLATFORM','/developers'),('ENTERPRISE','/enterprise'),('MCP GATEWAY','/mcp-gateway'),('CLI','/cli'),('PRICING','/pricing')]),
    ('RESOURCES', [('DOCS','https://docs.composio.dev/'),('BLOG','/blog'),('CUSTOMERS','/customers'),('TOOLKITS','/toolkits'),('ARTICLES','/content'),('AUTH GUIDES','/auth'),('CASE STUDIES','/case-studies'),('STARTUPS','/startups'),('PARTNERSHIPS','/partnerships')]),
    ('SOLUTIONS', [('OFFICE WORK','/product/composio-for-everyday-ai-users'),('SALES','/product/composio-for-sales-revenue'),('MARKETING','/product/composio-for-marketing-growth'),('PRODUCT & DESIGN','/product/composio-for-product-design'),('CUSTOMER SUPPORT','/product/composio-for-customer-support'),('ENGINEERING','/product/composio-for-engineering-devops'),('ALL USE CASES','/use-cases')]),
    ('FOR AGENTS', [('CLAUDE','/claude'),('CODEX','/codex'),('OPENCLAW','/claw'),('CURSOR','/cursor'),('HERMES AGENT','/hermes')]),
    ('COMPANY', [('CAREERS','https://jobs.ashbyhq.com/composio'),('TRUST','https://trust.composio.dev/'),('CONTACT US','/contact'),('SUPPORT','/support'),('TERMS','/terms'),('PRIVACY POLICY','/privacy')]),
]
footer_html = ''.join(
    f'<nav aria-label="{escape(title)}"><strong>{escape(title)}</strong>'
    + ''.join(f'<a href="{escape(href if href.startswith("http") else "https://composio.dev"+href)}">{escape(label)}</a>' for label, href in links)
    + '</nav>' for title, links in footer_columns
)

css = r'''
@font-face{font-family:Geist;src:url("composio-assets/0b78ff376f6b9734-s.p.woff2") format("woff2");font-weight:100 900;font-display:swap}
@font-face{font-family:JetBrains;src:url("composio-assets/bb3ef058b751a6ad-s.p.woff2") format("woff2");font-weight:100 800;font-display:swap}
:root{--dark:#0f0f0f;--light:#f6f6f6;--blue:#0007cd;--grey:#909090;--line:#313131}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;font:16px/1.4 Geist,Arial,sans-serif;color:var(--dark);background:var(--dark)}a{color:inherit;text-decoration:none}a:hover{text-decoration:underline}button{font:inherit;cursor:pointer}img{max-width:100%;display:block}h1,h2,h3,h4,p{margin-top:0}h1,h2,h3{font-weight:500;letter-spacing:-.035em}.container{width:min(calc(100% - 40px),1240px);margin:auto}.mono{font:500 12px/1.4 JetBrains,monospace;letter-spacing:.015em}.eyebrow{display:table;margin:0 auto 34px;border:1px solid #c4c4c4;padding:7px 10px;font:500 12px JetBrains,monospace;letter-spacing:.01em}.button{display:inline-flex;align-items:center;justify-content:center;min-height:45px;padding:0 23px;font:500 13px JetBrains,monospace;white-space:nowrap}.button.white{background:#fff;color:#111}.button.outline{border:1px solid #535353;color:#aaa}.button.black{background:#111;color:#fff}
.announcement{height:36px;background:#0007cd;color:#fff;display:flex;align-items:center;justify-content:center;text-align:center;padding:0 12px;font-size:14px}.announcement a{display:block}.announcement span{font:500 12px JetBrains,monospace;margin-left:12px}.header{height:82px;background:#0f0f0f;color:#fff;position:sticky;top:0;z-index:100;padding:16px 20px}.header-inner{height:53px;border:1px solid #333;background:#1e1e1e;display:flex;align-items:center;gap:30px;padding:0 9px}.brand img{width:130px;height:auto}.nav{display:flex;gap:35px;align-items:center;margin:auto;font:500 13px JetBrains,monospace}.nav details{position:relative}.nav summary{list-style:none;cursor:pointer}.nav summary::-webkit-details-marker{display:none}.nav summary:after{content:"⌄";margin-left:7px;color:#aaa}.nav-menu{display:none;position:absolute;top:29px;left:-10px;min-width:170px;padding:15px;background:#1e1e1e;border:1px solid #444;box-shadow:0 15px 30px #0008}.nav details[open] .nav-menu{display:grid;gap:12px}.header-actions{display:flex;align-items:center;gap:8px}.header-actions a{font:500 12px JetBrains,monospace;padding:8px}.header-actions .login{border:1px solid #555}.header-actions .signup{background:#fff;color:#111}.mobile-menu{display:none}
.hero{height:764px;background:#0f0f0f;color:white;position:relative;overflow:hidden;text-align:center;padding:98px 20px 0}.hero>*{position:relative;z-index:1}.works{display:inline-flex;align-items:center;gap:13px;height:32px;padding:0 12px;border:1px solid #303030;color:#aaa;font:500 11px JetBrains,monospace;letter-spacing:.02em}.works .marks{border-left:1px solid #444;padding-left:12px;display:flex;gap:10px;color:white;font-size:14px}.hero h1{font-size:68px;line-height:1.05;max-width:820px;margin:35px auto 24px;letter-spacing:-.042em}.hero h1 mark{background:#0007cd;color:#fff;padding:0 9px;white-space:nowrap}.hero-subtitle{font-size:18px;line-height:1.45;color:#929292;max-width:660px;margin:0 auto}.hero-subtitle a{text-decoration:underline;text-underline-offset:3px}.hero-actions{display:flex;justify-content:center;gap:12px;margin:42px 0 16px}.hero .free-note{font-size:14px;color:#888}.hero .trusted-label{font:500 11px JetBrains,monospace;letter-spacing:.04em;color:#777;margin:89px 0 25px}.trusted-logos{display:flex;align-items:center;justify-content:center;gap:42px;max-width:1140px;overflow:hidden;margin:auto;height:45px;opacity:.55}.trusted-logos img{width:auto;height:28px;max-width:110px;object-fit:contain;filter:grayscale(1) brightness(2)}.trusted-link{display:inline-block;color:#888;font:500 11px JetBrains,monospace;margin-top:23px}.glitch{position:absolute!important;z-index:0!important;top:230px;width:210px;height:350px;opacity:.8;filter:blur(1px);background:repeating-linear-gradient(180deg,transparent 0 6px,#1714df 7px 8px,#2222ff 9px 11px,transparent 12px 17px);mask-image:linear-gradient(90deg,#000,transparent)}.glitch.left{left:-65px;clip-path:polygon(0 20%,35% 15%,55% 18%,55% 32%,90% 31%,90% 52%,40% 55%,40% 75%,0 80%)}.glitch.right{right:-55px;transform:scaleX(-1);clip-path:polygon(0 10%,22% 10%,22% 32%,80% 30%,80% 50%,45% 55%,45% 87%,0 90%)}.glitch:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent,#1434ff7a,transparent);filter:blur(14px)}
.how{height:1018px;background:var(--light);padding:79px 20px 0;text-align:center;overflow:hidden}.how h2,.advantage h2,.for-you h2,.developer h2,.security h2{font-size:48px;line-height:1.08}.how h2{margin:0 0 20px}.how>p{color:#555;font-size:18px;margin:0 auto}.how-visual{display:grid;grid-template-columns:340px 250px 340px;justify-content:center;align-items:start;gap:34px;margin:73px auto 0;height:580px}.phone{height:600px;border:7px solid #111;border-radius:50px;background:#fbfaf8;text-align:left;box-shadow:0 0 0 2px #5f5f5f,0 13px 20px #0002;overflow:hidden;padding:16px;position:relative}.phone:before{content:"";position:absolute;top:10px;left:calc(50% - 49px);width:98px;height:27px;border-radius:20px;background:#050505}.phone-status{height:42px;display:flex;justify-content:space-between;padding:0 10px;font-size:13px;font-weight:700}.phone .bubble{background:#efefec;border-radius:15px;padding:12px;font-size:13px;margin:15px 0}.phone .agent{display:flex;gap:10px;margin-top:23px}.agent img{width:40px;height:40px}.agent .message{background:#fff;border:1px solid #e4e4e4;border-radius:12px;padding:10px;font-size:12px}.phone-sheet{background:white}.phone-sheet .sheet-head{font-size:13px;font-weight:700;border-bottom:1px solid #ddd;padding:15px 5px}.phone-sheet .sheet-grid{margin-top:25px;display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:#ddd}.sheet-grid span{background:#fff;padding:11px 3px;font-size:9px}.sheet-grid span:nth-child(-n+4){background:#dfeee4;font-weight:700}.connection{padding-top:90px}.connection img{width:154px;margin:0 auto 24px}.connection .steps{background:white;border:1px solid #ddd;border-radius:10px;text-align:left;padding:14px 16px;color:#666;font-size:12px;line-height:2.4}.connection .steps div+div{border-top:1px solid #eee}.connection .steps span{float:right;color:#00a675}.connection p{margin-top:37px;font-size:15px}.connection .tool-names{font:500 12px JetBrains,monospace;color:#555}
.advantage{background:#0f0f0f;color:#fff;padding:140px 20px 105px;min-height:2162px}.advantage .eyebrow{border-color:#333;color:#aaa}.advantage h2{text-align:center;margin:0 auto 20px}.advantage-intro{max-width:730px;margin:0 auto 70px;text-align:center;color:#aaa;font-size:18px}.advantage-content{display:grid;grid-template-columns:225px minmax(0,1fr);gap:60px;max-width:1240px;margin:auto}.feature-tabs{align-self:start;position:sticky;top:104px;border:1px solid #333}.feature-tabs a{display:flex;align-items:center;gap:18px;border-bottom:1px solid #333;padding:12px 13px;font:500 12px JetBrains,monospace;min-height:45px}.feature-tabs a:last-child{border:0}.feature-tabs a:first-child{border-color:#0007cd}.feature-tabs span{color:#888}.feature-tabs a:first-child span{background:#0007cd;color:white;padding:3px}.feature-rows{min-width:0}.feature-row{height:414px;display:grid;grid-template-columns:61% 39%;border:1px solid #303030;border-bottom:0;scroll-margin-top:105px}.feature-row:last-child{border-bottom:1px solid #303030}.feature-visual{background-size:cover;background-position:center;display:grid;place-items:center;overflow:hidden}.terminal{background:#111;color:#d3d3d3;border:1px solid #303030;box-shadow:0 20px 35px #0008;width:75%;max-width:360px;padding:12px;text-align:left;font:10px/1.5 JetBrains,monospace}.terminal-search{border:1px solid #333;padding:8px;color:#777}.terminal-search small{float:right}.terminal-line{border:1px solid #262626;margin-top:6px;padding:9px;color:#aaa}.terminal-line b{color:#b878ea}.terminal-line em{float:right;color:#9b9bd8;font-style:normal;font-size:8px}.terminal-plan{border-top:1px solid #333;margin-top:14px;padding-top:10px;color:#aaa}.terminal-plan span{color:#b58d46;margin-left:45px}.terminal .error{color:#ce6868}.terminal .success{color:#4080ff}.terminal.auth-window{font:13px Geist,Arial;padding:22px}.auth-window strong{font-size:21px}.auth-window p{font-size:13px;color:#aaa}.auth-window div{padding:9px;border-top:1px solid #444}.auth-window span{float:right;color:#85a5ff;font-size:10px}.terminal.code{font:10px/1.7 JetBrains,monospace;color:#c9c9dd}.terminal.code span{color:#aaa}.feature-copy{padding:30px;display:flex;flex-direction:column}.feature-number{font:500 12px JetBrains,monospace;color:#aaa;background:#252525;align-self:start;padding:5px}.feature-copy h3{font-size:29px;line-height:1.1;margin:13px 0 15px}.feature-copy p{font-size:14px;line-height:1.3;margin:0 0 auto}.feature-copy ul{margin:16px 0 0;padding:0;list-style:none}.feature-copy li{font-size:13px;border-left:2px solid #aaa;padding:6px 0 6px 16px;margin:3px 0}
.for-you{background:var(--light);padding:125px 20px 100px;text-align:center}.for-you .eyebrow{margin-bottom:35px}.for-you h2{margin-bottom:18px}.for-you>p{font-size:17px;color:#555}.case-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:65px auto 35px}.case-card{background:#fff;border:1px solid #e3e3e3;text-align:left;min-height:330px;padding:19px 20px;display:flex;flex-direction:column}.case-card h3{font-size:25px;letter-spacing:-.02em;margin:0 0 15px}.case-card h3 span{float:right;color:#999;font-size:18px}.case-card ul{list-style:none;padding:0;margin:0}.case-card li{background:#fafafa;border:1px solid #e5e5e5;padding:12px;margin-bottom:7px;font-size:14px;line-height:1.3}.case-apps{display:flex;flex-wrap:wrap;gap:9px;color:#6d6d6d;font:500 10px JetBrains,monospace;margin:auto 0 0;padding-top:22px}.for-you .case-actions{display:flex;justify-content:center;gap:10px}.for-you small{display:block;color:#777;margin:15px}
.developer{background:#0f0f0f;color:#fff;padding:128px 20px 105px}.developer .eyebrow{border-color:#444;color:#aaa}.developer h2{text-align:center;margin:0 0 20px}.developer>p{text-align:center;color:#aaa;font-size:17px;margin-bottom:65px}.dev-platform{display:grid;grid-template-columns:35% 65%;min-height:395px;border:1px solid #343434}.dev-copy{padding:40px}.dev-copy h3{font:500 25px Geist,Arial;margin:0 0 20px}.dev-copy p{color:#aaa;line-height:1.5;margin-bottom:25px}.dev-copy pre{font:12px JetBrains,monospace;color:#8db8ff}.dev-copy .button{margin-top:25px}.dev-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;padding:14px}.dev-grid article{background:#1d1d1d;border:1px solid #303030;padding:17px;min-height:155px}.dev-grid article b{display:block;font-size:13px}.dev-grid article p{font:12px JetBrains,monospace;color:#7f7f7f;margin-top:58px}.developer h3.out-of-box{text-align:center;font-size:24px;margin:70px 0 30px}.dev-features{display:grid;grid-template-columns:repeat(4,1fr);border:1px solid #333}.dev-features article{padding:20px;min-height:216px;border-right:1px solid #333;display:flex;flex-direction:column}.dev-features article:last-child{border:0}.dev-features h4{font-size:20px;margin:0 0 12px}.dev-features p{font-size:14px;line-height:1.5}.dev-features a{background:#282828;color:#aaa;align-self:start;margin-top:auto;font:500 12px JetBrains,monospace;padding:7px 8px}
.security{background:#f6f6f6;padding:110px 20px 90px;min-height:725px;text-align:center}.security h2{margin:0 0 50px}.security-content{display:grid;grid-template-columns:41% 59%;min-height:420px;border:1px solid #dedede;text-align:left}.security-art{background:#f6f6f6 url("composio-assets/images-security-holographic.webp") center/contain no-repeat;border-right:1px solid #ddd}.security-copy{padding:0 32px;display:flex;flex-direction:column}.security-copy details{border-bottom:1px solid #ddd;padding:18px 0}.security-copy summary{list-style:none;font-size:24px;cursor:pointer}.security-copy summary::-webkit-details-marker{display:none}.security-copy summary span{float:right}.security-copy details p{font-size:17px;color:#555;margin:8px 0 0}.security-copy>a{align-self:start;margin:auto 0 22px;background:#e1e1e1;padding:9px;font:500 12px JetBrains,monospace}
.faq{background:#0f0f0f;color:#fff;padding:110px 20px 95px}.faq-wrap{display:grid;grid-template-columns:40% 60%;gap:30px}.faq .eyebrow{margin:0 0 20px;border-color:#333;color:#aaa}.faq h2{font-size:48px}.faq-list{border-top:1px solid #343434}.faq-list details{border-bottom:1px solid #343434}.faq-list summary{list-style:none;padding:23px 0;font-size:17px;cursor:pointer}.faq-list summary::-webkit-details-marker{display:none}.faq-list summary span{float:right}.faq-list p{color:#aaa;max-width:650px}.faq-list p a{text-decoration:underline}
.final-cta{background:#f6f6f6;text-align:center;padding:95px 20px}.final-cta h2{font-size:43px;margin-bottom:25px}
.footer{background:#0f0f0f;color:#fff;padding:70px 20px 25px}.footer-top{display:grid;grid-template-columns:1.5fr repeat(5,1fr);gap:20px}.footer-brand img{width:115px}.footer nav{display:grid;align-content:start;gap:11px}.footer nav strong{font:500 12px JetBrains,monospace;margin-bottom:10px}.footer nav a{font:500 11px JetBrains,monospace;color:#999}.footer-bottom{margin-top:75px;border-top:1px solid #333;padding-top:24px;color:#888;font-size:12px}
@media(max-width:1000px){.nav{gap:12px;font-size:11px}.hero h1{font-size:58px}.how-visual{grid-template-columns:29% 22% 29%;gap:3%}.advantage-content{grid-template-columns:160px minmax(0,1fr);gap:20px}.feature-copy{padding:20px}.feature-copy h3{font-size:25px}.footer-top{grid-template-columns:repeat(3,1fr)}.footer-brand{grid-column:1/-1}}
@media(max-width:720px){.header{height:70px;padding:8px}.header-inner{height:54px}.brand img{width:115px}.mobile-menu{display:block;margin-left:auto;color:white;background:none;border:0;font-size:24px}.nav{display:none;position:absolute;top:66px;left:8px;right:8px;background:#1e1e1e;border:1px solid #444;padding:17px;flex-direction:column;align-items:start;font-size:13px}.header.open .nav{display:flex}.header-actions{gap:5px}.header-actions .login{display:none}.header-actions a{padding:7px;font-size:10px}.announcement{font-size:11px}.announcement span{font-size:10px}.hero{height:690px;padding-top:100px}.works{font-size:9px;gap:6px}.works .marks{gap:5px;font-size:10px}.hero h1{font-size:clamp(43px,9vw,66px);margin-top:35px}.hero-subtitle{font-size:16px}.hero-actions{margin-top:28px}.hero .trusted-label{margin-top:70px}.trusted-logos{gap:23px}.glitch{opacity:.4}.how{height:auto;padding:75px 15px 70px}.how h2,.advantage h2,.for-you h2,.developer h2,.security h2{font-size:36px}.how-visual{display:flex;gap:12px;height:450px;overflow:hidden;margin-top:55px}.phone{flex:0 0 180px;height:430px;border-radius:30px;padding:8px}.connection{flex:0 0 120px;padding-top:50px}.connection img{width:110px}.connection .steps{font-size:8px;padding:6px}.connection p{font-size:11px}.advantage{padding:80px 15px}.advantage-content{display:block}.feature-tabs{position:static;display:grid;grid-template-columns:repeat(2,1fr);margin-bottom:25px}.feature-tabs a{font-size:9px;min-height:55px}.feature-row{height:auto;display:block;margin-bottom:20px;border:1px solid #333}.feature-visual{height:290px}.feature-copy{min-height:330px}.feature-copy p{margin-bottom:20px}.for-you{padding:75px 15px}.case-grid{grid-template-columns:1fr;margin-top:40px}.case-card{min-height:290px}.developer{padding:80px 15px}.dev-platform{display:block}.dev-grid{grid-template-columns:repeat(2,1fr)}.dev-features{grid-template-columns:repeat(2,1fr)}.dev-features article:nth-child(2){border-right:0}.dev-features article:nth-child(-n+2){border-bottom:1px solid #333}.security{padding:80px 15px}.security-content{display:block}.security-art{height:330px;border-right:0;border-bottom:1px solid #ddd}.security-copy{min-height:355px}.faq{padding:75px 15px}.faq-wrap{display:block}.faq-list{margin-top:45px}.final-cta h2{font-size:34px}.footer-top{grid-template-columns:repeat(2,1fr)}.footer nav strong{font-size:11px}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
'''

page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex"><title>Composio — source-backed homepage draft</title><meta name="description" content="Dated reconstruction draft of the public Composio homepage observed 2026-09-27."><style>{css}</style></head><body>
<div class="announcement"><a href="https://chatgpt.com/plugins/plugin_asdk_app_6a58503580c08191b78cc5bdaf4eba6e">Composio is now live in the ChatGPT Plugins Directory. <span>TRY IT OUT ↗</span></a></div>
<header class="header" id="header"><div class="header-inner"><a class="brand" href="https://composio.dev/" aria-label="Composio home"><img src="{asset('logos-composio-full-white.svg')}" alt="Composio"></a><button class="mobile-menu" type="button" aria-label="Toggle menu" aria-expanded="false" onclick="const h=document.getElementById('header');h.classList.toggle('open');this.setAttribute('aria-expanded',h.classList.contains('open'))">☰</button><nav class="nav" aria-label="Primary"><details><summary>PRODUCTS</summary><div class="nav-menu"><a href="https://composio.dev/for-you">COMPOSIO FOR YOU</a><a href="https://composio.dev/developers">DEVELOPER PLATFORM</a><a href="https://composio.dev/enterprise">ENTERPRISE</a><a href="https://composio.dev/mcp-gateway">MCP GATEWAY</a></div></details><details><summary>SOLUTIONS</summary><div class="nav-menu"><a href="https://composio.dev/use-cases">ALL USE CASES</a><a href="https://composio.dev/product/composio-for-engineering-devops">ENGINEERING</a><a href="https://composio.dev/product/composio-for-marketing-growth">MARKETING</a></div></details><details><summary>RESOURCES</summary><div class="nav-menu"><a href="https://docs.composio.dev/">DOCS</a><a href="https://composio.dev/blog">BLOG</a><a href="https://composio.dev/customers">CUSTOMERS</a><a href="https://composio.dev/toolkits">TOOLKITS</a></div></details><a href="https://composio.dev/developers">DEVELOPERS</a></nav><div class="header-actions"><a class="login" href="https://login.composio.dev/">LOG IN</a><a class="signup" href="https://dashboard.composio.dev/login">GET STARTED – FREE</a></div></div></header>
<main><section class="hero"><div class="glitch left" aria-hidden="true"></div><div class="glitch right" aria-hidden="true"></div><a class="works" href="https://composio.dev/works-with"><span>WORKS WITH</span><span class="marks">◎ &nbsp; ◉ &nbsp; ✳ &nbsp; ● &nbsp; ▲ &nbsp; ⬡</span><span>→</span></a><h1>Give your AI secure access<br>to 1,500+ apps <mark>in minutes</mark></h1><p class="hero-subtitle">Connect Claude, ChatGPT, Hermes, or your own harness to <a href="https://composio.dev/toolkits">almost any app</a>.<br>Then watch it go from chatting to doing.</p><div class="hero-actions"><a class="button white" href="https://dashboard.composio.dev/login?cta_placement=hero-cta">GET STARTED FOR FREE</a><a class="button outline" href="https://composio.dev/contact">GET A DEMO</a></div><p class="free-note">100,000 free actions included every month.</p><p class="trusted-label">TRUSTED BY</p><div class="trusted-logos">{trusted_html}</div><a class="trusted-link" href="https://composio.dev/customers">READ THEIR STORIES →</a></section>
<section class="how" id="how-it-works"><span class="eyebrow">HOW IT WORKS</span><h2>Composio turns your AI into a doer</h2><p>Composio sits between your AI and your apps, turning your requests into actions.</p><div class="how-visual"><div class="phone"><div class="phone-status">9:41 <span>▴ ▰</span></div><div class="bubble">Save yesterday’s Instagram stats to my sheet.</div><div class="agent"><img src="{asset('images-clients-claude.svg')}" alt="Claude"><div class="message">I’ll get your Instagram performance and add it to Google Sheets.</div></div></div><div class="connection"><img src="{asset('logos-composio-full-black.svg')}" alt="Composio"><div class="steps"><div>◎ &nbsp; Connect to Instagram <span>✓</span></div><div>◎ &nbsp; Read yesterday’s post stats <span>✓</span></div><div>◉ &nbsp; Connect to Google Sheets <span>✓</span></div><div>◉ &nbsp; Add rows to the sheet <span>✓</span></div></div><p>We work with the AI tools you already use</p><div class="tool-names">Claude &nbsp; ChatGPT &nbsp; Codex</div></div><div class="phone phone-sheet"><div class="phone-status">9:41 <span>▴ ▰</span></div><div class="sheet-head">‹ &nbsp; Instagram performance</div><div class="sheet-grid"><span>Post</span><span>Views</span><span>Likes</span><span>Comments</span><span>May 12</span><span>12.4k</span><span>1.3k</span><span>96</span><span>May 11</span><span>8.7k</span><span>842</span><span>47</span></div></div></div></section>
<section class="advantage"><span class="eyebrow">THE COMPOSIO ADVANTAGE</span><h2>Everything between the ask and the result, handled</h2><p class="advantage-intro">Give your AI & agent a task. Composio finds the right actions across 1,500+ apps, connects each app in a click, and keeps connections working as those apps change.</p><div class="advantage-content"><nav class="feature-tabs" aria-label="Composio advantages">{tabs_html}</nav><div class="feature-rows">{features_html}</div></div></section>
<section class="for-you"><span class="eyebrow">COMPOSIO FOR YOU</span><h2>Composio helps AI take action 100M+ times a week</h2><p>Explore everyday tasks your AI can take off your hands with Composio.</p><div class="case-grid container">{use_cases_html}</div><div class="case-actions"><a class="button black" href="https://dashboard.composio.dev/login">PUT YOUR AI TO WORK</a><a class="button" href="https://composio.dev/for-you">LEARN MORE</a></div><small>Illustrative examples.</small></section>
<section class="developer"><span class="eyebrow">FOR DEVELOPERS</span><h2>Build agents on battle-tested infrastructure</h2><p>Connect your agents to the apps your users rely on without maintaining every integration yourself.</p><div class="dev-platform container"><div class="dev-copy"><h3>Composio PLATFORM</h3><p>Implement in minutes. Ship working integrations in just five lines of code.</p><pre>tools = session.tools()
agent = Agent(
  name="Assistant",
  tools=tools,
)</pre><a class="button white" href="https://dashboard.composio.dev/login">TRY FOR FREE</a> <a class="button outline" href="https://docs.composio.dev/">READ THE DOCS</a></div><div class="dev-grid"><article><b>Support Agent</b><p>Resolved GH-482</p></article><article><b>Email Agent</b><p>Labeled 3 emails</p></article><article><b>Slack Agent</b><p>Summarized #engineering</p></article><article><b>SQL Agent</b><p>Ran analytics query</p></article><article><b>Code Review Agent</b><p>Reviewed PR #127</p></article><article><b>Research Agent</b><p>Found 12 sources</p></article></div></div><h3 class="out-of-box">What you get out of the box</h3><div class="dev-features container">{developer_html}</div></section>
<section class="security"><span class="eyebrow">SAFETY & SECURITY</span><h2>Secure by default, at every layer</h2><div class="security-content container"><div class="security-art" role="img" aria-label="Holographic security illustration"></div><div class="security-copy"><details open><summary>Team controls <span>−</span></summary><p>Fine grained data access controls</p></details><details><summary>SOC2 & ISO 27001:2022 <span>+</span></summary><p>Security and compliance at every layer.</p></details><details><summary>Bring your own cloud <span>+</span></summary><p>Deploy with the control your organization needs.</p></details><a href="https://trust.composio.dev/">LEARN MORE ABOUT OUR SECURITY</a></div></div></section>
<section class="faq"><div class="faq-wrap container"><div><span class="eyebrow">FAQ</span><h2>Frequently asked<br>questions</h2></div><div class="faq-list">{faq_html}</div></div></section><section class="final-cta"><h2>Connect your AI to 1,500+ apps for free</h2><a class="button black" href="https://dashboard.composio.dev/login">TRY COMPOSIO NOW</a></section></main>
<footer class="footer"><div class="footer-top container"><div class="footer-brand"><a href="https://composio.dev/"><img src="{asset('logos-composio-full-white.svg')}" alt="Composio"></a></div>{footer_html}</div><div class="footer-bottom container">© Composio 2026 &nbsp; · &nbsp; <a href="https://x.com/composio">X</a> &nbsp; <a href="https://www.linkedin.com/company/composiohq/">LinkedIn</a> &nbsp; <a href="https://github.com/composiohq/composio/">GitHub</a> &nbsp; <a href="https://dub.composio.dev/discord">Discord</a></div></footer></body></html>'''

(ROOT / 'composio.html').write_text(page)
print(f'Wrote {ROOT / "composio.html"} ({len(page)} characters)')
