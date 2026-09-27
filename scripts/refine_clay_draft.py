#!/usr/bin/env python3
"""Refine the dated Stitch Clay screen with observed public-site content."""
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / '.stitch-work' / 'current-official'
data = json.loads((SOURCE / 'clay-browser-data.json').read_text())

services = data['services'].strip().split('\n\n')
assert len(services) == 13, len(services)
service_pairs = list(zip(services[1::2], services[2::2]))

work_names = [
    'Slack', 'STC Bank', 'Sky', 'Snapchat', 'Joe & The Juice', 'Vantara',
    'Grayscale', 'Discover', 'Marqeta', 'Yahoo! Games', 'Serena & Lily',
    'Tipalti', 'Wealth', 'Art Bridges',
]
work_images = [
    'work-slack.avif', 'work-stc-bank.avif', 'work-sky.avif',
    'work-snapchat.avif', 'work-joe-and-the-juice.avif', 'work-vantara.avif',
    'work-grayscale.avif', 'work-discover.avif', 'work-marqeta.avif',
    'work-yahoo-games.avif', 'work-serena-and-lily.avif', 'work-tipalti.avif',
    'work-wealth.avif', 'work-art-bridges.avif',
]
work_descriptions = [
    'Designing and building Slack’s interactive demo experience',
    'Accelerating the future of digital banking in Saudi Arabia',
    'Branding and visual identity for an innovative DeFi platform',
    'Integrating augmented reality to elevate social commerce',
    'A digital commerce and visual identity for a global chain of coffee shops and juice bars',
    'Website design and development for a landmark animal conservation center',
    'Web redesign for the world’s largest crypto asset manager',
    'Design partnership focused on mobile app innovation',
    'Website and digital branding for a modern card-issuing platform',
    'Website design and development for Yahoo Games',
    'Ecommerce redesign for a leader in luxury home decor',
    'Web redesign for a modern payables automation platform',
    'Designing a self-service digital estate planning platform',
    'Website redesign for a niche nonprofit organization',
]
assert len(data['work']) == len(work_names) == len(work_images)

news_images = ['news-tipalti.avif', 'news-buttons.avif', 'news-webby.avif']
news_titles = [
    'Tipalti Redesign Wins Design Awards and Features',
    'Complete Guide to Buttons in Web Design for 2026',
    'Clay Global Shows Up Strong at The Webby Awards 2026',
]
news_dates = ['Sep 3, 2026', 'Apr 21, 2026', 'May 6, 2026']
news_categories = ['News', 'Web Design', 'News']

questions = [
    'What are your core services as a UX design and branding firm?',
    'What separates Clay from other branding and web design agencies?',
    'Do you work with clients in different timezones?',
    'How much does hiring you for a design project cost?',
    'Do you work with startups?',
    'Can you help us redesign our B2B/enterprise software?',
]
faq_text = data['faq']
faq_answers = []
for index, question in enumerate(questions):
    start = faq_text.index(question) + len(question)
    end = faq_text.index(questions[index + 1]) if index + 1 < len(questions) else len(faq_text)
    faq_answers.append(faq_text[start:end].strip())

def link(label, url, cls=''):
    return f'<a class="{cls}" href="{escape(url, quote=True)}">{escape(label)}</a>'

def work_card(index):
    item = data['work'][index]
    wide = index in (2, 5, 8, 11)
    desc = work_descriptions[index]
    return (
        f'<article class="work-card{" work-card-wide" if wide else ""}">'
        f'<a href="{escape(item["href"], quote=True)}" aria-label="View {escape(work_names[index])} case study">'
        f'<img src="clay-assets/{work_images[index]}" alt="{escape(work_names[index])} project image" loading="lazy"></a>'
        f'<div class="work-meta"><h3>{escape(work_names[index])}</h3>'
        f'<p>{escape(desc)}</p><a href="{escape(item["href"], quote=True)}" class="case-link">View case study ↗</a></div>'
        '</article>'
    )

service_html = ''.join(
    f'<details class="service"><summary>{escape(title)}<span aria-hidden="true">⌄</span></summary>'
    f'<p>{escape(body)}</p></details>' for title, body in service_pairs
)
logos = data['clients'][:10]
logo_files = [
    'logo-meta.avif', 'logo-google.avif', 'logo-discover.avif', 'logo-stripe.png',
    'logo-coca-cola.avif', 'logo-coinbase.png', 'logo-uber.png', 'logo-sony.avif',
    'logo-slack.avif', 'logo-amazon.avif', 'logo-fiverr.avif',
    'logo-credit-karma.png', 'logo-cisco.png', 'logo-adp.avif',
    'logo-ups.avif', 'logo-vmware.avif', 'logo-fossil.png',
    'logo-western-digital.avif', 'logo-toyota.avif', 'logo-samsung.png',
]
logo_html = ''.join(
    f'<img src="clay-assets/{file}" alt="{escape(logo["name"])}" loading="lazy">'
    for logo, file in zip(logos, logo_files[:10])
)
work_html = ''.join(work_card(i) for i in range(14))
news_html = ''.join(
    f'<a class="news-item" href="{escape(data["news"][i]["href"], quote=True)}">'
    f'<img src="clay-assets/{news_images[i]}" alt="" loading="lazy">'
    f'<div><span class="news-category">{news_categories[i]}</span><h3>{escape(news_titles[i])}</h3>'
    f'<small>{news_dates[i]}</small></div><span class="news-arrow" aria-hidden="true">↗</span></a>'
    for i in range(3)
)
faq_html = ''.join(
    f'<details class="faq-item"><summary>{escape(q)}<span aria-hidden="true">⌄</span></summary>'
    f'<p>{escape(answer)}</p></details>' for q, answer in zip(questions, faq_answers)
)

html = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex"><title>Clay Global — Official Homepage Reconstruction Draft</title>
<meta name="description" content="Dated reconstruction draft based on Clay Global's public homepage observed 2026-09-27.">
<style>
@font-face{font-family:Universal;src:url("clay-assets/universal-sans.woff") format("woff");font-display:swap}
@font-face{font-family:Universal;src:url("clay-assets/universal-sans-bold.woff") format("woff");font-weight:700;font-display:swap}
@font-face{font-family:UniversalHeadline;src:url("clay-assets/universal-sans-headlines-bold.woff") format("woff");font-weight:700;font-display:swap}
:root{--ink:#06070a;--gray:#efedf0;--pad:75px}*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:#fff;color:var(--ink);font:18px/1.45 Universal,Arial,sans-serif}
a{color:inherit;text-decoration:none}button{font:inherit}img{max-width:100%;display:block}
.site-header{height:108px;padding:0 75px 0 45px;display:flex;align-items:flex-start;justify-content:space-between;gap:24px;position:sticky;top:0;z-index:10;background:rgba(239,237,240,.96);transition:background .2s}
.site-header.scrolled{background:rgba(255,255,255,.95);backdrop-filter:blur(18px)}
.brand{display:flex;align-items:center;gap:5px;margin-top:33px;flex:none}.brand img:first-child{width:21px;height:40px}.brand img:last-child{width:74px;height:auto}
.primary-nav{display:flex;align-items:center;gap:39px;margin:29px 0 0 auto;font-size:18px;font-weight:700;white-space:nowrap}
.primary-nav a{transition:opacity .2s}.primary-nav a:hover{opacity:.5}.primary-nav .industry::after{content:"⌄";color:#a2a4aa;font-size:18px;margin-left:9px;font-weight:400}
.contact-button{margin-top:29px;background:#171a20;color:#fff;border-radius:30px;padding:12px 22px;font-size:18px;line-height:28px;font-weight:700;white-space:nowrap}
.menu-toggle{display:none}
.hero{height:607px;background:var(--gray);position:relative;overflow:hidden}.hero h1{position:absolute;left:72px;top:151px;margin:0;width:745px;font:700 64px/1.1 UniversalHeadline,Arial,sans-serif;letter-spacing:-.045em;z-index:2}
.hero-art{position:absolute;width:397px;height:488px;object-fit:contain;right:65px;top:22px}
.showreel{padding:0 var(--pad) 125px}.showreel-frame{height:auto;aspect-ratio:1130/636;position:relative;background:#15171c;overflow:hidden}
.showreel-frame video{width:100%;height:100%;object-fit:cover}.showreel-label{position:absolute;right:0;bottom:0;background:#17191e;color:#fff;padding:15px 18px;font-size:20px;cursor:pointer;border:0}
.services{padding:100px var(--pad) 65px;display:grid;grid-template-columns:1.1fr .8fr;gap:14%;min-height:525px}
.services h2{font:400 30px/1.32 Universal,Arial,sans-serif;letter-spacing:-.02em;margin:0;max-width:560px}
.service{margin:0 0 6px}.service summary{list-style:none;cursor:pointer;font:700 30px/1.48 Universal,Arial,sans-serif}.service summary::-webkit-details-marker,.faq-item summary::-webkit-details-marker{display:none}
.service summary span{color:#a4a8b2;font-weight:400;margin-left:10px}.service p{font-size:17px;line-height:1.5;color:#62646a;max-width:390px;margin:5px 0 18px}
.clients{padding:22px var(--pad) 80px;min-height:445px;overflow:hidden}.logo-wall{display:grid;grid-template-columns:repeat(5,1fr);align-items:center;gap:0 24px;height:250px}
.logo-wall img{width:100%;max-width:180px;height:105px;object-fit:contain;opacity:.68}
.text-link{display:inline-block;font-size:20px;border-bottom:1px solid #b9bdc4;padding-bottom:3px}.text-link::after{content:"→";margin-left:12px;color:#b9bdc4}.clients .text-link{display:table;margin:27px auto 0}
.fintech-wrap{padding:0 var(--pad) 0}.fintech{height:638px;background:#17191e;color:#fff;position:relative;overflow:hidden}
.fintech-content{position:relative;z-index:2;height:100%;padding:64px;display:flex;flex-direction:column;align-items:flex-start}.fintech small{font-size:18px;color:#a2a4a9}
.fintech h2{font:700 64px/1.13 UniversalHeadline,Arial,sans-serif;letter-spacing:-.035em;max-width:620px;margin:27px 0 0}
.fintech .text-link{margin-top:auto;margin-bottom:10px}.fintech-visual{position:absolute;right:0;top:74px;width:455px;height:460px;object-fit:cover}
.work{padding:68px var(--pad) 170px}.work-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));column-gap:112px;row-gap:110px;align-items:start}
.work-card:nth-child(even):not(.work-card-wide){margin-top:145px}.work-card img{width:100%;height:auto;aspect-ratio:1/1;object-fit:cover;background:#f2f3f5;transition:transform .35s}
.work-card>a{display:block;overflow:hidden}.work-card>a:hover img{transform:scale(1.025)}.work-card:nth-child(even):not(.work-card-wide) img{aspect-ratio:4/5}
.work-card-wide{grid-column:1/-1;margin:10px 0 15px}.work-card-wide img{aspect-ratio:1130/635}
.work-meta{padding-top:18px}.work-meta h3{font:700 30px/1.2 UniversalHeadline,Arial,sans-serif;margin:0 0 7px}.work-meta p{margin:0;color:#4b4d51;font-size:18px}
.case-link{font-size:14px;border-bottom:1px solid #aaa;display:inline-block;margin-top:12px}.work>.text-link{display:table;margin:120px auto 0}
.about{padding:100px var(--pad) 150px;background:#f7f7f8;overflow:hidden}.about h2{font:700 clamp(48px,6vw,86px)/1.05 UniversalHeadline,Arial,sans-serif;letter-spacing:-.04em;max-width:970px;margin:0 0 46px}
.about-intro{display:grid;grid-template-columns:1fr 1fr;gap:80px;align-items:start}.about-intro p{font-size:30px;line-height:1.3;margin:0;max-width:600px}
.about-images{display:flex;gap:26px;align-items:end;margin:130px -75px 110px}.about-images img{width:calc(33.333% - 18px);height:470px;object-fit:cover}.about-images img:nth-child(2){height:620px}.about-images img:nth-child(3){height:410px}
.about-note{max-width:610px;margin:0 0 25px auto;color:#57595f;font-size:24px;line-height:1.3}
.about>.text-link{margin-left:calc(50% + 40px)}
.dark{background:#17191e;color:#fff}.news{padding:115px var(--pad) 120px;display:grid;grid-template-columns:30% 1fr;gap:7%}.news h2{font:700 56px/1.1 UniversalHeadline,Arial,sans-serif;margin:0}
.news-list{display:grid}.news-item{display:grid;grid-template-columns:34% 1fr 20px;gap:24px;min-height:250px;border-bottom:1px solid #333740;padding:24px 0}.news-item:first-child{padding-top:0}
.news-item img{width:100%;height:185px;object-fit:cover}.news-category{color:#b3b5bb;font-size:14px}.news-item h3{font:700 30px/1.18 UniversalHeadline,Arial,sans-serif;margin:12px 0 40px}.news-item small{color:#a9abb1;font-size:13px}.news-arrow{font-size:24px}
.news .text-link{grid-column:2;margin-top:30px;justify-self:end}
.faq{padding:90px var(--pad) 170px;border-top:1px solid #30343b}.faq h2{font:700 54px/1.12 UniversalHeadline,Arial,sans-serif;margin:0 0 55px}.faq-item{border-bottom:1px solid #333740}
.faq-item summary{padding:23px 0;display:flex;justify-content:space-between;gap:25px;list-style:none;font-size:24px;cursor:pointer}.faq-item summary span{color:#9699a2}.faq-item p{max-width:850px;white-space:pre-line;color:#b8bac0;line-height:1.5;margin:0 0 30px}
.footer{background:#f2f2f4;padding:100px var(--pad) 40px}.footer-top{display:grid;grid-template-columns:1fr 1fr;gap:60px}.footer h2{font:700 clamp(72px,10vw,150px)/.95 UniversalHeadline,Arial,sans-serif;letter-spacing:-.06em;margin:0 0 35px}.footer-contact{font-size:30px}.footer-contact a{display:block}.footer-nav{display:grid;grid-template-columns:repeat(2,1fr);align-content:start;gap:12px;font-size:21px}
.offices{display:grid;grid-template-columns:repeat(3,1fr);gap:38px 60px;margin:145px 0}.offices h3{font-size:18px;margin:0 0 8px}.offices p{font-size:16px;color:#686a70;white-space:pre-line;margin:0}
.footer-bottom{border-top:1px solid #d7d9de;padding-top:22px;display:flex;flex-wrap:wrap;gap:20px;font-size:14px;color:#64666b}.footer-bottom a:hover,.footer-nav a:hover{text-decoration:underline}
@media(max-width:1100px){:root{--pad:45px}.primary-nav{gap:19px;font-size:16px}.site-header{padding-right:45px}.hero h1{font-size:54px;width:58%}.hero-art{width:36%;right:40px}.work-grid{gap:80px 65px}.fintech h2{font-size:56px}}
@media(max-width:760px){:root{--pad:22px}.site-header{height:80px;padding:0 22px;align-items:center}.brand{margin:0}.primary-nav{display:none}.contact-button{margin:0 0 0 auto;font-size:15px;padding:8px 15px}.menu-toggle{display:inline-block;border:0;background:transparent;font-size:26px}.site-header.nav-open{height:auto;flex-wrap:wrap;padding-top:20px;padding-bottom:18px}.site-header.nav-open .primary-nav{display:flex;order:3;width:100%;flex-wrap:wrap;margin:15px 0 0;gap:14px 22px}.hero{height:640px}.hero h1{font-size:clamp(39px,8vw,58px);left:22px;top:65px;width:calc(100% - 44px)}.hero-art{width:min(75vw,360px);height:auto;right:10px;top:255px}.showreel{padding-bottom:65px}.showreel-frame{aspect-ratio:16/10}.showreel-label{font-size:15px;padding:10px}.services{display:block;padding-top:75px}.services h2{font-size:27px;margin-bottom:55px}.service summary{font-size:25px}.clients{padding-top:35px;min-height:0}.logo-wall{grid-template-columns:repeat(3,1fr);height:auto}.logo-wall img{height:80px}.fintech{height:610px}.fintech-content{padding:34px 28px}.fintech h2{font-size:clamp(42px,8vw,60px);max-width:570px}.fintech-visual{width:65%;height:auto;top:auto;bottom:40px;right:0;opacity:.7}.fintech .text-link{position:relative;z-index:3}.work{padding-top:70px;padding-bottom:100px}.work-grid{grid-template-columns:1fr;row-gap:65px}.work-card:nth-child(even):not(.work-card-wide){margin-top:0}.work-card-wide{grid-column:auto}.work-card img,.work-card:nth-child(even):not(.work-card-wide) img,.work-card-wide img{aspect-ratio:4/3}.work-meta h3{font-size:26px}.about{padding-top:75px;padding-bottom:100px}.about h2{font-size:48px}.about-intro{display:block}.about-intro p{font-size:25px;margin-bottom:30px}.about-images{margin:80px -22px;gap:10px}.about-images img{width:calc(33.333% - 7px);height:230px!important}.about-note{font-size:20px}.about>.text-link{margin-left:0}.news{display:block;padding-top:85px}.news h2{font-size:48px;margin-bottom:55px}.news-item{grid-template-columns:38% 1fr 15px;gap:14px;min-height:170px}.news-item img{height:135px}.news-item h3{font-size:22px;margin:6px 0 12px}.faq{padding-top:70px;padding-bottom:110px}.faq h2{font-size:42px}.faq-item summary{font-size:20px}.footer{padding-top:85px}.footer-top{display:block}.footer h2{font-size:76px}.footer-contact{font-size:25px;margin-bottom:55px}.offices{grid-template-columns:repeat(2,1fr);gap:35px 20px;margin:80px 0}.footer-nav{font-size:18px}}
@media(max-width:430px){.hero{height:600px}.hero-art{top:260px;width:82vw}.logo-wall{grid-template-columns:repeat(2,1fr)}.fintech h2{font-size:43px}.fintech-visual{width:80%}.news-item{grid-template-columns:1fr 18px}.news-item img{display:none}.offices{grid-template-columns:1fr 1fr}.footer h2{font-size:65px}}
</style></head><body>
<!-- Google Stitch project 6058475459069348637 generated the initial section architecture; official imagery, content and geometry were refined from the dated live reference. -->
<header class="site-header" id="site-header"><a class="brand" href="https://clay.global/" aria-label="Clay Global home"><img src="clay-assets/clay-logo-left.png" alt=""><img src="clay-assets/clay-logo-right.png" alt="Clay"></a>
<nav class="primary-nav" id="primary-nav" aria-label="Primary"><a href="https://clay.global/work">Work</a><a href="https://clay.global/clients">Clients</a><a href="https://clay.global/services">Services</a><a class="industry" href="https://clay.global/industries">Industries</a><a href="https://clay.global/about">About</a><a href="https://clay.global/blog">Blog</a></nav>
<a class="contact-button" href="https://clay.global/contact">Contact</a><button class="menu-toggle" aria-controls="primary-nav" aria-expanded="false" aria-label="Toggle menu">☰</button></header>
<main>
<section class="hero"><h1>Clay is a global branding<br>and UX design agency</h1><img class="hero-art" src="clay-assets/hero-satellite-observed.png" alt="Clay's white satellite-shaped 3D artwork with purple and orange spheres"></section>
<section class="showreel" aria-label="Clay showreel"><div class="showreel-frame"><video id="showreel" playsinline preload="none" poster="clay-assets/showreel-poster.avif" src="https://cdn.sanity.io/files/r115idoc/production/1f0e5e7efc6e944b7ab0babd354ad6f850296748.mp4#t=0.1"></video><button class="showreel-label" id="showreel-button" type="button">Play Showreel</button></div></section>
<section class="services" id="services"><h2>We build transformative digital experiences for the world's leading brands by blending AI, design, and technology.</h2><div class="service-list">@@SERVICES@@</div></section>
<section class="clients" id="clients"><div class="logo-wall">@@LOGOS@@</div><a class="text-link" href="https://clay.global/clients">View all clients</a></section>
<section class="fintech-wrap"><div class="fintech"><img class="fintech-visual" src="clay-assets/fintech-object-observed.png" alt="Clay's dark 3D fintech sculpture"><div class="fintech-content"><small>Fintech</small><h2>The Future of<br>Finance is Intelligent</h2><a class="text-link" href="https://clay.global/fintech">Explore fintech</a></div></div></section>
<section class="work" id="work"><div class="work-grid">@@WORK@@</div><a class="text-link" href="https://clay.global/work">Explore all work</a></section>
<section class="about" id="about"><h2>We transform companies through design innovation</h2><div class="about-intro"><p>A full-service creative agency designing and building inventive digital experiences across all platforms and brand touchpoints.</p><a class="text-link" href="https://clay.global/services">View our services</a></div>
<div class="about-images"><img src="clay-assets/team-office.jpg" alt="Shelves and plants in Clay's office" loading="lazy"><img src="clay-assets/team-camera.png" alt="Clay team member with a camera" loading="lazy"><img src="clay-assets/team-san-francisco.png" alt="San Francisco city buildings" loading="lazy"></div>
<p class="about-note">Our cross-disciplinary team combines strategy, branding, UX design, and technology for swift, impactful results. Working as one team with our clients, we merge human creativity with AI-driven efficiency to consistently exceed expectations.</p><a class="text-link" href="https://clay.global/about">Get to know us</a></section>
<section class="news dark" id="blog"><h2>Featured News</h2><div class="news-list">@@NEWS@@</div><a class="text-link" href="https://clay.global/blog">Visit blog</a></section>
<section class="faq dark"><h2>FAQ</h2><div>@@FAQ@@</div></section>
</main>
<footer class="footer" id="contact"><div class="footer-top"><div><h2>Let’s Talk</h2><div class="footer-contact"><a href="mailto:hey@clay.global">hey@clay.global</a><a href="tel:+14157966262">+1 415 796 6262</a></div></div><nav class="footer-nav" aria-label="Footer"><a href="https://clay.global/work">Work</a><a href="https://clay.global/clients">Clients</a><a href="https://clay.global/services">Services</a><a href="https://clay.global/industries">Industries</a><a href="https://clay.global/about">About</a><a href="https://clay.global/blog">Blog</a><a href="https://clay.global/contact">Contact</a></nav></div>
<div class="offices"><div><h3>San Francisco</h3><p>300 Broadway,\nSan Francisco, CA 94133</p></div><div><h3>New York</h3><p>148 Lafayette St,\nNew York, NY 10013</p></div><div><h3>Austin</h3><p>600 Congress Ave,\nAustin, TX 78701</p></div><div><h3>Denver</h3><p>1700 Lincoln St 17th fl,\nDenver, CO 80203</p></div><div><h3>Lisbon</h3><p>Av. Alm. Reis 139, 1150-015\nLisbon, Portugal</p></div><div><h3>Belgrade</h3><p>Nušićeva 15, 11000\nBelgrade, Serbia</p></div></div>
<div class="footer-bottom"><span>© 2016–2026 Clay Global, LLC</span><a href="https://clay.global/privacy">Privacy</a><a href="https://clay.global/terms">Terms</a><a href="https://clay.global/sitemap.xml">Sitemap</a><a href="https://www.instagram.com/clayglobal/">Instagram</a><a href="https://www.linkedin.com/company/clay-global/">LinkedIn</a></div></footer>
<script>
const header=document.getElementById('site-header');const menu=document.querySelector('.menu-toggle');
addEventListener('scroll',()=>header.classList.toggle('scrolled',scrollY>40),{passive:true});
menu.addEventListener('click',()=>{const open=header.classList.toggle('nav-open');menu.setAttribute('aria-expanded',String(open));});
const video=document.getElementById('showreel'),play=document.getElementById('showreel-button');
play.addEventListener('click',()=>{video.controls=true;video.play();play.hidden=true});
</script></body></html>'''

for marker, content in {
    '@@SERVICES@@': service_html, '@@LOGOS@@': logo_html, '@@WORK@@': work_html,
    '@@NEWS@@': news_html, '@@FAQ@@': faq_html,
}.items():
    html = html.replace(marker, content)
assert '@@' not in html
(SOURCE / 'clay.html').write_text(html + '\n')
print(f'Wrote Clay draft: {len(work_names)} work items, {len(service_pairs)} services, {len(questions)} FAQs')
