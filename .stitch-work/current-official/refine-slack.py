#!/usr/bin/env python3
"""Correct the native Stitch screen against the observed public Slack homepage.

The Stitch export and screenshot are retained unchanged. This produces a dated
draft; desktop and mobile visual acceptance remain separate work.
"""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
html = (ROOT / 'slack-stitch.html').read_text()


def replace_once(old: str, new: str) -> None:
    global html
    assert html.count(old) == 1, old[:100]
    html = html.replace(old, new, 1)


def replace_between(start: str, end: str, new: str) -> None:
    global html
    assert html.count(start) == 1 and html.count(end) == 1, (start, end)
    a = html.index(start)
    b = html.index(end, a)
    html = html[:a] + new + html[b:]


def link(label: str, href: str) -> str:
    return f'<a href="{escape(href, quote=True)}">{escape(label)}</a>'


asset_dir = ROOT / 'slack-assets'
assets = (
    'logo.png', 'logo-gm.png', 'logo-openai.png', 'logo-target.png',
    'logo-paramount.png', 'logo-stripe.png', 'logo-ibm.png',
    'hero-slackbot.jpg', 'hero-slackbot.mp4', 'hero-plan.jpg', 'hero-plan.mp4',
    'hero-projects.jpg', 'hero-projects.mp4', 'hero-clients.jpg',
    'hero-clients.mp4', 'hero-tasks.jpg', 'hero-tasks.mp4',
    'ai-github.jpg', 'ai-slackbot.jpg', 'ai-summary.jpg', 'ai-claude.jpg',
    'ai-huddles.jpg', 'ai-agentforce.jpg', 'pillar-knowledge.png',
    'pillar-people.png', 'pillar-process.png', 'pillar-platform.png',
    'avant-garde.woff2', 'salesforce-sans.woff2',
    'salesforce-sans-bold.woff2', 'salesforce-sans-semibold.woff2',
)
for asset in assets:
    assert (asset_dir / asset).is_file(), asset

replace_once('<title>Slack: Where work happens</title>',
             '<title>Slack | AI Work Platform &amp; Productivity Tools</title>')
assert 'href="https://slack.com/blog/news/"' in html
html = html.replace('href="https://slack.com/blog/news/"',
                    'href="https://slack.com/blog/news/ai-powered-interface-for-work"', 1)

nav = '''<!-- Navigation reconstructed from the live public desktop page -->
<header class="slack-nav" aria-label="Primary navigation"><div class="slack-nav-inner">
<a class="slack-wordmark" href="https://slack.com/"><img src="slack-assets/logo.png" width="101" height="38" alt="Slack from Salesforce"></a>
<nav class="slack-menu" aria-label="Main navigation"><details><summary>Features <span>⌄</span></summary><div class="slack-menu-panel"><a href="https://slack.com/features">See all features</a><a href="https://slack.com/features/slackbot">Slackbot</a><a href="https://slack.com/features/channels">Channels</a><a href="https://slack.com/features/workflow-automation">Workflow Builder</a></div></details><details><summary>Solutions <span>⌄</span></summary><div class="slack-menu-panel"><a href="https://slack.com/solutions">See all solutions</a><a href="https://slack.com/solutions/engineering">Engineering</a><a href="https://slack.com/solutions/sales">Sales</a></div></details><a href="https://slack.com/enterprise">Enterprise</a><details><summary>Resources <span>⌄</span></summary><div class="slack-menu-panel"><a href="https://slack.com/resources">Resources Library</a><a href="https://slack.com/blog">Slack Blog</a><a href="https://slack.com/customer-stories">Customer Stories</a></div></details><a href="https://slack.com/pricing">Pricing</a></nav>
<div class="slack-nav-actions"><button class="slack-search" type="button" aria-label="Search" title="Search"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="m15.5 15.5 6 6" fill="none" stroke="currentColor" stroke-width="2"/></svg></button><a class="slack-signin" href="https://slack.com/signin">Sign in</a><a class="slack-btn slack-btn-outline" href="https://slack.com/contact-sales">REQUEST A DEMO</a><a class="slack-btn slack-btn-solid" href="https://slack.com/get-started">GET STARTED</a></div>
</div></header>
'''
replace_between('<!-- 2. Main Navigation Header (80px) -->',
                '<!-- 3. Hero Section (White background, centered typography) -->', nav)

logos = [('GM', 'logo-gm.png'), ('OpenAI', 'logo-openai.png'),
         ('Target', 'logo-target.png'), ('Paramount', 'logo-paramount.png'),
         ('Stripe', 'logo-stripe.png'), ('IBM', 'logo-ibm.png')]
proof = '<div class="slack-trust"><span>Trusted by top teams</span>' + ''.join(
    f'<img src="slack-assets/{file}" alt="{label} Logo" loading="lazy">'
    for label, file in logos) + '</div>\n'
replace_between('<!-- Social Proof / Logos -->',
                '<!-- 800px genuine Slack app video / poster visual -->', proof)

hero_tabs = [('Ask Slackbot', 'slackbot'), ('Plan launches', 'plan'),
             ('Run projects', 'projects'), ('Chat with clients', 'clients'),
             ('Automate tasks', 'tasks')]
hero_media = '''<div class="slack-hero-media"><video id="slack-hero-video" autoplay muted loop playsinline preload="metadata" poster="slack-assets/hero-slackbot.jpg"><source src="slack-assets/hero-slackbot.mp4" type="video/mp4">Your browser does not support video.</video></div><div class="slack-hero-tabs" role="tablist" aria-label="Slack examples">'''
hero_media += ''.join(
    f'<button type="button" role="tab" data-hero="{key}" aria-selected="{str(i == 0).lower()}">{escape(label)}</button>'
    for i, (label, key) in enumerate(hero_tabs)) + '</div>\n'
replace_between('<!-- 800px genuine Slack app video / poster visual -->',
                '</section>\n<!-- 4. Dark Aubergine #4a154b AI & Agents Section -->', hero_media)

ai_items = [
    ('Review code with Github Copilot', 'ai-github.jpg'),
    ('Update deals just by asking Slackbot', 'ai-slackbot.jpg'),
    ('Summarize a conversation you missed', 'ai-summary.jpg'),
    ('Get fast answers with Claude', 'ai-claude.jpg'),
    ('Turn on AI note-taking in huddles', 'ai-huddles.jpg'),
    ('Lookup customer data in Agentforce', 'ai-agentforce.jpg'),
]
ai = '''<!-- Live-reference AI section with official stills -->
<section class="slack-ai"><div class="slack-ai-intro"><h2>Reimagine what’s possible with AI and agents.</h2><p>AI in Slack doesn’t make you think, it helps you do. It summarizes and searches based on actual conversations, and with it, makes every app and agent more helpful and contextually aware than ever.</p></div><div class="slack-ai-content"><div class="slack-ai-list" role="tablist" aria-label="AI examples">'''
ai += ''.join(
    f'<button type="button" role="tab" data-ai="{file}" aria-selected="{str(i == 0).lower()}">{escape(label)}' +
    (' <span class="slack-new">NEW</span>' if i == 1 else '') + '</button>'
    for i, (label, file) in enumerate(ai_items))
ai += '</div><img id="slack-ai-image" src="slack-assets/ai-github.jpg" alt="Slack with Github Copilot"></div></section>\n'
replace_between('<!-- 4. Dark Aubergine #4a154b AI & Agents Section -->',
                '<!-- 5. "What\'s new in Slack" Cards Section -->', ai)

news = [
    ('Slack Code', 'Coding agents can now work with your whole team, not just you.'),
    ('Slackbot Deep Research', 'Slackbot can now dig deep on open-ended questions, not just quick ones.'),
    ('Salesforce approvals in Slack', 'Salesforce approvals can now be routed straight into Slack.'),
    ('Slackbot Big Mode', 'Slackbot just got a full-screen workspace built for deeper work.'),
    ('Slackbot Skill Sets', 'Slackbot skills can now travel together, not one at a time.'),
]
below = '''<section class="slack-news"><div class="slack-section-head"><h2>What’s new in Slack</h2><a href="https://slack.com/whats-new">See all updates ↗</a></div><div class="slack-news-grid">'''
below += ''.join(
    '<a href="https://slack.com/whats-new"><small>NEW FEATURE</small><h3>' +
    escape(title) + '</h3><p>' + escape(body) + '</p><span aria-hidden="true">↗</span></a>'
    for title, body in news) + '</div></section>\n'

pillars = [
    ('Knowledge', 'Give everyone instant context.',
     'Get access to every file, decision, and conversation, so you can build on past work instead of recreating it.',
     'Meet Slackbot: Your personal agent for work.',
     "Slackbot isn't just any AI. It's AI that knows you and your team. It coordinates work across your apps and agents so one conversation gets work done.",
     'pillar-knowledge.png', 'https://slack.com/features/slackbot'),
    ('People', 'Let your people connect like people.',
     "Slack’s conversational UI makes collaborating more approachable, whether you're working with a colleague or an agent.",
     'It all starts with a channel.',
     'Channels are flexible, transparent spaces for working with your team, AI assistants, and agents.',
     'pillar-people.png', 'https://slack.com/features/channels'),
    ('Process', 'Manage all your work from one place.',
     'Automate daily stand-ups, project updates, and approvals so your team can focus on growth instead of guesswork.',
     'Anyone can automate in Slack.',
     'By click or by code, Slack makes it easy for anyone to build time-saving automations of their own.',
     'pillar-process.png', 'https://slack.com/features/workflow-automation'),
    ('Platform', 'Secure. Scaleable. Silo-free.',
     'Our flexible, open platform is purpose-built for bringing the best agents and AI to every business, and can be tailored to fit however your teams work best.',
     'From Atlassian to Zoom. Google Drive. ChatGPT. Vercel. Box. Asana. Workday.',
     'You name it, it works in Slack.',
     'pillar-platform.png', 'https://slack.com/marketplace'),
]
below += '<div class="slack-pillar-nav" aria-label="Slack capabilities">' + ''.join(
    f'<a href="#slack-{name.lower()}">{name}</a>' for name, *_ in pillars) + '</div>\n'
for name, heading, intro, subhead, body, image, url in pillars:
    below += (f'<section class="slack-pillar" id="slack-{name.lower()}"><div class="slack-pillar-inner"><div class="slack-pillar-copy"><span class="slack-kicker">{name}</span><h2>{escape(heading)}</h2><p>{escape(intro)}</p><div class="slack-pillar-feature"><h3>{escape(subhead)}</h3><p>{escape(body)}</p><a href="{url}">Learn more ↗</a></div></div><img src="slack-assets/{image}" alt="Slack {name.lower()} product interface" loading="lazy"></div></section>\n')

below += '''<section class="slack-customers"><h2>The most innovative companies run their business in Slack.</h2><div><a href="https://www.youtube.com/embed/SyuBcwa0bqQ">OpenAI ↗</a><a href="https://www.youtube.com/embed/o2c2_EGP8w4">Box ↗</a><a href="https://www.youtube.com/embed/EOTqujB8_R4">Caraway ↗</a><a href="https://www.youtube.com/embed/8NjVIWfje1o">Rivian ↗</a></div></section>
<section class="slack-metrics"><h2>We’re in the business of growing businesses.</h2><div><article><strong>90%</strong><p>of users say Slack helps them stay more connected</p></article><article><strong>43</strong><p>The average number of apps used by teams in Slack</p></article><article><strong>87%</strong><p>of users say Slack helps them collaborate more efficiently</p></article></div><h2>Millions of people love to work in Slack.</h2><div><article><strong>700M</strong><p>Messages sent daily</p></article><article><strong>4M</strong><p>Slack Connect users working directly with external teams each week</p></article><article><strong>3M</strong><p>Daily Workflows</p></article><article><strong>1.7M</strong><p>Apps actively used each week</p></article></div><p class="slack-metric-note">Source: Slack’s public 2026 homepage; figures use its FY25 usage data and customer surveys.</p></section>
<section class="slack-final"><h2>See all you can accomplish in Slack.</h2><div><a class="slack-btn slack-btn-solid" href="https://slack.com/get-started">GET STARTED</a><a class="slack-btn slack-btn-outline" href="https://slack.com/contact-sales">REQUEST A DEMO</a></div></section>
'''
replace_between('<!-- 5. "What\'s new in Slack" Cards Section -->', '</main>', below)

footer_groups = {
    'PRODUCT': [('Watch Demo', 'https://slack.com/demo'), ('Pricing', 'https://slack.com/pricing'), ('Paid vs. Free', 'https://slack.com/pricing/paid-vs-free'), ('Accessibility', 'https://slack.com/accessibility'), ('Featured Releases', 'https://slack.com/innovations'), ('Changelog', 'https://slack.com/changelog')],
    'WHY SLACK?': [('Slack vs. Email', 'https://slack.com/compare/slack-vs-email'), ('Slack vs. Teams', 'https://slack.com/compare/slack-vs-teams'), ('Enterprise', 'https://slack.com/enterprise'), ('Small Business', 'https://slack.com/solutions/small-business'), ('Productivity', 'https://slack.com/engage-users')],
    'FEATURES': [('Channels', 'https://slack.com/features/channels'), ('Slack Connect', 'https://slack.com/connect'), ('Workflow Builder', 'https://slack.com/features/workflow-automation'), ('Messaging', 'https://slack.com/features/team-chat'), ('Huddles', 'https://slack.com/features/huddles'), ('Canvas', 'https://slack.com/features/canvas'), ('Slack AI', 'https://slack.com/features/ai')],
    'SOLUTIONS': [('Engineering', 'https://slack.com/solutions/engineering'), ('IT', 'https://slack.com/solutions/information-technology'), ('Customer Service', 'https://slack.com/solutions/customer-service'), ('Sales', 'https://slack.com/solutions/sales'), ('Project Management', 'https://slack.com/solutions/project-management'), ('Marketing', 'https://slack.com/solutions/marketing')],
    'RESOURCES': [('Help Center', 'https://slack.com/help'), ('What’s New', 'https://slack.com/innovations'), ('Resources Library', 'https://slack.com/resources'), ('Slack Blog', 'https://slack.com/blog'), ('Community', 'https://slack.com/community'), ('Customer Stories', 'https://slack.com/customer-stories')],
    'COMPANY': [('About Us', 'https://slack.com/about'), ('News', 'https://slack.com/blog/news'), ('Media Kit', 'https://slack.com/media-kit'), ('Careers', 'https://slack.com/careers'), ('Contact Us', 'https://slack.com/help')],
}
footer = '<footer class="slack-footer"><div class="slack-footer-inner"><a href="https://slack.com/"><img src="slack-assets/logo.png" alt="Slack"></a><div class="slack-footer-grid">'
footer += ''.join('<div><h3>' + title + '</h3>' + ''.join(link(*item) for item in items) + '</div>' for title, items in footer_groups.items())
footer += '</div><div class="slack-footer-bottom"><div>' + ' '.join(link(*item) for item in [
    ('Privacy', 'https://slack.com/trust/privacy/privacy-policy'),
    ('Terms', 'https://slack.com/legal'),
    ('Your Privacy Choices', 'https://www.salesforce.com/form/other/privacy-request/')]) + '</div><span>©2026 Slack Technologies, LLC, a Salesforce company. All rights reserved.</span></div></div></footer>'
replace_between('<!-- 8. Real Official Slack Footer -->', '</body>', footer)

css = '''<style>
@font-face{font-family:Salesforce-Sans;src:url('slack-assets/salesforce-sans.woff2') format('woff2');font-weight:400;font-display:swap}@font-face{font-family:Salesforce-Sans;src:url('slack-assets/salesforce-sans-semibold.woff2') format('woff2');font-weight:600;font-display:swap}@font-face{font-family:Salesforce-Sans;src:url('slack-assets/salesforce-sans-bold.woff2') format('woff2');font-weight:700;font-display:swap}@font-face{font-family:Salesforce-Avant-Garde;src:url('slack-assets/avant-garde.woff2') format('woff2');font-weight:700;font-display:swap}
html{scroll-behavior:smooth}body{font-family:Salesforce-Sans,Arial,sans-serif;color:#000}h1,h2{font-family:Salesforce-Avant-Garde,Arial,sans-serif}a{color:inherit}.slack-nav{height:80px;background:#fff;position:sticky;top:0;z-index:60}.slack-nav-inner{height:100%;max-width:1180px;margin:auto;display:flex;align-items:center;gap:38px}.slack-wordmark{flex:none}.slack-wordmark img{width:101px;height:38px;object-fit:contain}.slack-menu,.slack-nav-actions{display:flex;align-items:center;gap:30px}.slack-menu a,.slack-menu summary,.slack-signin{font-size:15px;font-weight:600;text-decoration:none;white-space:nowrap;cursor:pointer}.slack-menu details{position:relative}.slack-menu summary{list-style:none}.slack-menu summary::-webkit-details-marker{display:none}.slack-menu summary span{font-size:15px}.slack-menu-panel{position:absolute;top:35px;left:-22px;background:#fff;border:1px solid #eee;border-radius:8px;box-shadow:0 10px 28px #0002;width:230px;padding:15px;display:grid;gap:12px}.slack-menu-panel a{font-size:14px}.slack-nav-actions{margin-left:auto;gap:20px}.slack-search svg{width:20px;height:20px}.slack-btn{display:inline-flex;justify-content:center;align-items:center;min-height:42px;padding:0 15px;font-size:13px;font-weight:700;letter-spacing:.03em;text-decoration:none;border-radius:4px;white-space:nowrap}.slack-btn-outline{border:1px solid #611f69;color:#611f69}.slack-btn-solid{background:#611f69;color:#fff}.slack-btn-solid:hover{background:#4a154b}.slack-btn-outline:hover{background:#f4ede4}
main>section:first-child{padding-top:62px;padding-bottom:66px;max-width:none}main>section:first-child h1{font-size:64px;line-height:1.12;letter-spacing:-.02em;font-weight:700;max-width:900px;color:#000}main>section:first-child>p{margin-top:16px;font-size:18px;color:#000;line-height:1.45}main>section:first-child>div.mt-8{margin-top:18px;gap:8px}main>section:first-child>div.mt-8 a{height:57px;min-width:179px;display:inline-flex;align-items:center;justify-content:center;padding:0 26px;font-size:13px;letter-spacing:.03em;font-weight:700;box-shadow:none;border-width:1px}.slack-trust{display:flex;align-items:center;justify-content:center;gap:34px;margin-top:35px;min-height:38px}.slack-trust span{font-size:12px;color:#777;margin-right:-11px}.slack-trust img{height:27px;width:auto;object-fit:contain;max-width:74px}.slack-trust img:nth-of-type(1){height:34px}.slack-trust img:nth-of-type(3){height:34px}.slack-trust img:nth-of-type(4){height:32px}.slack-hero-media{margin:45px auto 0;max-width:800px;border-radius:7px;overflow:hidden}.slack-hero-media video{width:100%;display:block;aspect-ratio:1.46;object-fit:cover}.slack-hero-tabs{display:flex;flex-wrap:wrap;justify-content:center;gap:8px;margin-top:24px}.slack-hero-tabs button{padding:10px 18px;border-radius:28px;background:#f4ede4;font-size:14px;color:#1d1c1d}.slack-hero-tabs button[aria-selected=true]{background:#611f69;color:#fff}
.slack-ai{background:#4a154b;color:#fff;padding:90px 24px 120px}.slack-ai-intro{text-align:center;max-width:840px;margin:0 auto 66px}.slack-ai h2{font-size:58px;line-height:1.1;font-weight:700;max-width:850px;margin:0 auto}.slack-ai-intro p{font-size:18px;line-height:1.3;margin:36px auto 0;max-width:700px}.slack-ai-content{max-width:940px;margin:auto;display:grid;grid-template-columns:40% 60%;align-items:center;gap:25px}.slack-ai-list{display:grid;gap:15px}.slack-ai-list button{color:#fff;text-align:left;font-size:22px;line-height:1.2;padding:7px 0;background:none}.slack-ai-list button[aria-selected=true]{font-weight:700}.slack-ai-list button:hover{text-decoration:underline}.slack-new{display:inline-block;background:#e8f5ff;color:#28587c;font-size:11px;border-radius:20px;padding:3px 12px;margin-left:8px;vertical-align:middle}.slack-ai-content img{width:100%;border-radius:12px}
.slack-news,.slack-customers,.slack-metrics{padding:85px max(24px,calc((100vw - 1100px)/2))}.slack-news{background:#fff}.slack-section-head{display:flex;align-items:flex-end;justify-content:space-between;gap:24px;margin-bottom:36px}.slack-section-head h2,.slack-customers h2,.slack-metrics h2{font-size:42px;line-height:1.15;max-width:840px}.slack-section-head a{color:#611f69;font-weight:700}.slack-news-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:14px}.slack-news-grid>a{display:flex;flex-direction:column;min-height:252px;background:#f4ede4;padding:24px 18px;text-decoration:none}.slack-news-grid small{color:#611f69;font-size:11px;font-weight:700}.slack-news-grid h3{font-size:19px;line-height:1.2;margin:24px 0 10px;font-weight:700}.slack-news-grid p{font-size:14px;line-height:1.35}.slack-news-grid span{margin-top:auto;color:#611f69;font-size:23px}.slack-pillar-nav{display:flex;justify-content:center;gap:50px;border-bottom:1px solid #ddd;background:white;padding:20px}.slack-pillar-nav a{font-weight:700;text-decoration:none}.slack-pillar{padding:85px 24px;background:#f4ede4}.slack-pillar:nth-of-type(even){background:#fff}.slack-pillar-inner{max-width:1100px;margin:auto;display:grid;grid-template-columns:1fr 1fr;align-items:center;gap:60px}.slack-pillar-copy{max-width:480px}.slack-kicker{font-size:14px;font-weight:700;color:#611f69}.slack-pillar h2{font-size:48px;line-height:1.12;margin:22px 0}.slack-pillar-copy>p{font-size:19px;line-height:1.45}.slack-pillar-feature{border-top:1px solid #aaa;margin-top:40px;padding-top:25px}.slack-pillar-feature h3{font-size:22px;font-weight:700}.slack-pillar-feature p{font-size:16px;margin-top:9px}.slack-pillar-feature a{display:inline-block;color:#611f69;font-weight:700;margin-top:15px}.slack-pillar img{width:100%;object-fit:contain}.slack-customers{background:#4a154b;color:#fff}.slack-customers div{display:grid;grid-template-columns:repeat(4,1fr);gap:15px;margin-top:35px}.slack-customers a{background:#ffffff18;border:1px solid #ffffff50;padding:32px 20px;font-size:24px;font-weight:700;text-decoration:none}.slack-metrics{text-align:center}.slack-metrics h2{margin:15px auto 40px}.slack-metrics>div{display:flex;justify-content:center;gap:70px;margin:0 auto 85px;max-width:1100px}.slack-metrics article{flex:1}.slack-metrics strong{display:block;font-size:48px;color:#611f69}.slack-metrics article p{font-size:15px}.slack-metric-note{font-size:12px;color:#666}.slack-final{background:#f4ede4;text-align:center;padding:80px 24px}.slack-final h2{font-size:42px}.slack-final>div{display:flex;justify-content:center;gap:12px;margin-top:25px}.slack-footer{background:#fff;padding:60px 24px 40px}.slack-footer-inner{max-width:1120px;margin:auto}.slack-footer img{width:101px;height:38px}.slack-footer-grid{display:grid;grid-template-columns:repeat(6,1fr);gap:20px;margin:35px 0 50px}.slack-footer-grid h3{font-size:12px;font-weight:700;margin-bottom:18px}.slack-footer-grid a{display:block;color:#454545;font-size:13px;line-height:2;text-decoration:none}.slack-footer-grid a:hover{text-decoration:underline}.slack-footer-bottom{border-top:1px solid #ddd;padding-top:22px;display:flex;justify-content:space-between;gap:24px;font-size:12px;color:#555}.slack-footer-bottom div{display:flex;gap:18px}.slack-footer-bottom a{text-decoration:none}
@media(max-width:1160px){.slack-nav-inner{padding:0 24px;gap:22px}.slack-menu,.slack-nav-actions{gap:16px}.slack-news-grid{grid-template-columns:repeat(3,1fr)}}@media(max-width:900px){.slack-menu{display:none}.slack-nav-actions{margin-left:auto}.slack-ai-content{grid-template-columns:1fr}.slack-ai-list{grid-template-columns:repeat(2,1fr)}.slack-pillar-inner{gap:25px}.slack-footer-grid{grid-template-columns:repeat(3,1fr)}}@media(max-width:650px){.slack-nav{height:68px}.slack-nav-actions .slack-search,.slack-signin,.slack-btn-outline{display:none}.slack-nav-inner{padding:0 16px}main>section:first-child{padding-top:45px}main>section:first-child h1{font-size:42px}main>section:first-child>p{font-size:16px}.slack-trust{gap:15px;flex-wrap:wrap;margin-top:30px}.slack-trust span{flex-basis:100%}.slack-trust img{height:22px}.slack-hero-media{margin-top:35px}.slack-ai{padding:70px 22px}.slack-ai h2{font-size:40px}.slack-ai-intro p{font-size:16px}.slack-ai-list{grid-template-columns:1fr}.slack-ai-list button{font-size:18px}.slack-section-head h2,.slack-customers h2,.slack-metrics h2,.slack-final h2{font-size:32px}.slack-news-grid{grid-template-columns:1fr 1fr}.slack-pillar-nav{gap:15px;flex-wrap:wrap}.slack-pillar-inner{grid-template-columns:1fr}.slack-pillar h2{font-size:39px}.slack-customers div{grid-template-columns:1fr 1fr}.slack-metrics>div{display:grid;grid-template-columns:1fr 1fr;gap:20px}.slack-footer-grid{grid-template-columns:repeat(2,1fr)}.slack-footer-bottom{display:block}.slack-footer-bottom div{flex-wrap:wrap;margin-bottom:12px}}
</style>'''
replace_once('</head>', css + '</head>')

js = '''<script>
const heroVideo=document.getElementById('slack-hero-video');
for(const tab of document.querySelectorAll('[data-hero]'))tab.addEventListener('click',()=>{for(const other of document.querySelectorAll('[data-hero]'))other.setAttribute('aria-selected',String(other===tab));const key=tab.dataset.hero;heroVideo.poster=`slack-assets/hero-${key}.jpg`;heroVideo.querySelector('source').src=`slack-assets/hero-${key}.mp4`;heroVideo.load();heroVideo.play().catch(()=>{});});
const aiImage=document.getElementById('slack-ai-image');
for(const tab of document.querySelectorAll('[data-ai]'))tab.addEventListener('click',()=>{for(const other of document.querySelectorAll('[data-ai]'))other.setAttribute('aria-selected',String(other===tab));aiImage.src='slack-assets/'+tab.dataset.ai;aiImage.alt=tab.textContent.trim();});
</script>'''
replace_once('</body>', js + '</body>')

assert 'stitch-placeholder' not in html
assert 'href="#"' not in html
for invented in ('Connect your codebase directly', 'Conduct multi-source syntheses',
                 'Equip your personal AI agent with custom API triggers',
                 'A modern foundation for every team'):
    assert invented not in html
for key in ('All your people and AI agents working together.',
            'Reimagine what’s possible with AI and agents.',
            'What’s new in Slack', 'Give everyone instant context.'):
    assert key in html
assert html.count('</main>') == 1 and html.count('</footer>') == 1
(ROOT / 'slack.html').write_text(html)
print('Wrote live-reference Slack draft:', len(html), 'characters')
