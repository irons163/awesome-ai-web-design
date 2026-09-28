#!/usr/bin/env python3
"""Build a dated MiniMax public-homepage study with observed first-party media."""

from __future__ import annotations

from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / '.stitch-work' / 'current-official'
A = 'minimax-assets/'
V = 'https://file.cdn.minimax.io/public/'

SLIDES = (
    {
        'key': 'm3', 'title': 'MiniMax M3',
        'title_asset': 'minimax-home-hero-title-m3-20260922.svg',
        'desktop_bg': 'minimax-home-hero-m3-20260923-v2-background-poster.jpg',
        'mobile_bg': 'minimax-home-mobile-stage-m3.webp',
        'video': 'minimax-home-hero-m3-20260923-v2-hq.mp4',
        'features': (
            ('minimax-home-m3-feature-1.webp', 'Frontier Coding / Agentic', 'Production-grade engineering, beyond code generation'),
            ('minimax-home-m3-feature-2.webp', 'MSA · 1M Context', 'Novel sparse attention that truly scales context'),
            ('minimax-home-m3-feature-3.webp', 'Multimodal', 'Step 0 joint training · interleaved'),
        ),
        'description': 'A frontier coding & agentic model built on a novel attention architecture (MSA) with 1M context',
        'actions': (
            ('API & Token Plan', 'https://platform.minimax.io/subscribe/token-plan'),
            ('Try in MiniMax Code', 'https://code.minimax.io/'),
            ('Learn More', 'https://www.minimax.io/models/text/m3'),
        ),
    },
    {
        'key': 'h3', 'title': 'MiniMax H3',
        'title_asset': 'minimax-home-hero-title-h3-20260922.svg',
        'desktop_bg': 'minimax-home-hero-h3-20260923-v2-background-poster.jpg',
        'mobile_bg': 'minimax-home-mobile-stage-h3-20260923-v1.webp',
        'video': 'minimax-home-hero-h3-20260923-v2-hq.mp4',
        'feature_video': 'minimax-home-hero-h3-feature-20260921-220444-faststart.mp4',
        'feature_poster': 'minimax-home-hero-h3-feature-poster-20260921-220444-1p3s.jpg',
        'description': 'An open-weight, general-purpose, omni-modal generation model',
        'actions': (
            ('API', 'https://platform.minimax.io/docs/api-reference/video-generation-v2-create'),
            ('Try in MiniMax Design', 'https://design.minimax.io/'),
            ('Learn More', 'https://www.minimax.io/blog/minimax-h3'),
        ),
    },
    {
        'key': 'code', 'title': 'MiniMax Code',
        'title_asset': 'minimax-home-hero-title-code-20260922.svg',
        'desktop_bg': 'minimax-home-hero-code-20260923-v3-background-poster.jpg',
        'mobile_bg': 'minimax-home-mobile-stage-code-20260923-v1.webp',
        'video': 'minimax-home-hero-code-20260923-v3-hq.mp4',
        'features': (
            ('minimax-home-code-feature-1.webp', 'Build Your Own Agent Team', 'The right Agents team up automatically to tackle any task, simple or complex.'),
            ('minimax-home-code-feature-2.webp', 'All-in-One Multimodal Creation', 'Understands images, video, and audio. Creates visuals, scripts, and voiceovers — in one seamless flow.'),
            ('minimax-home-code-feature-3.webp', 'Coding & Work Modes', 'Coding Mode keeps your code tools handy. Work Mode focuses on delivery. Switch instantly.'),
        ),
        'description': 'The coding harness built for MiniMax models',
        'actions': (
            ('Desktop', 'https://code.minimax.io/download'),
            ('Try Code Now', 'https://code.minimax.io/'),
            ('Learn More', 'https://www.minimax.io/blog/minimax-agent-team-long-running-1779893953'),
        ),
    },
    {
        'key': 'design', 'title': 'MiniMax Design',
        'title_asset': 'minimax-home-hero-title-design-20260922.svg',
        'desktop_bg': 'minimax-home-hero-design-20260923-v2-background-poster.jpg',
        'mobile_bg': 'minimax-home-mobile-stage-design-20260923-v1.webp',
        'video': 'minimax-home-hero-design-20260923-v2-hq.mp4',
        'features': (
            ('minimax-home-design-feature-1.webp', 'Agent-Driven Workflow', 'Input your goal. Agents autonomously plan, execute, and deliver the final output.'),
            ('minimax-home-design-feature-2.webp', 'Built for Commercial Creation', 'Create ads, e-commerce assets, brand campaigns, and post-production content.'),
            ('minimax-home-design-feature-3.webp', 'Open & Flexible Integration', 'Connect local assets, deploy privately, and scale through APIs.'),
        ),
        'description': 'AI Agent Platform for Commercial Content Creation',
        'actions': (
            ('Try Now', 'https://design.minimax.io/'),
            ('MiniMax Design Membership', 'https://design.minimax.io/media-plan/subscribe'),
        ),
    },
)

RESEARCH = (
    ('MiniMax Music 3.0', 'Music Generation', 'Open Weights',
     'MiniMax Music 3.0: Next-Generation Open-Weights, Production-Ready & Versatile Music Model',
     '2026-08-13', '30222ea1-9b1b-4cb1-aea9-9d6976bb2a66.png',
     'https://www.minimax.io/blog/minimax-music-3-0-next-generation-open-weights-production-ready-versatile-music-model'),
    ('AI', 'H3', 'Multimodal · Video Generation',
     'MiniMax H3: An Open Model Breaking the Boundaries Between Tasks and Modalities',
     '2026-07-31', 'e5727d3f-3d6e-455c-9ddc-1300c1a131ba.jpg',
     'https://www.minimax.io/blog/minimax-h3'),
    ('AI', 'M3', '',
     'MaxProof: Scaling Mathematical Proof with Generative-Verifier RL and Evolutionary Search',
     '2026-06-09', 'f96a4df0-8f46-4a13-aba2-925b65c5dfd8.png',
     'https://www.minimax.io/blog/minimax-maxproof-math-proof-evolution'),
    ('AI', 'M3', 'Frontier Model · MSA',
     'MiniMax M3: Frontier Coding, 1M Context, Native Multimodality — All in One Model',
     '2026-06-01', '5e2cae31-96fc-403c-aa5d-738d56d52d22.png',
     'https://www.minimax.io/blog/minimax-m3'),
)

FOOTER = (
    ('Model', (
        ('MiniMax M3', 'https://www.minimax.io/blog/minimax-m3'),
        ('MiniMax M2.7', 'https://www.minimax.io/news/minimax-m27-en'),
        ('MiniMax M2.5', 'https://www.minimax.io/news/minimax-m25'),
        ('MiniMax H3', 'https://www.minimax.io/blog/minimax-h3'),
        ('MiniMax Speech 2.8', 'https://www.minimax.io/news/minimax-speech-28'),
        ('MiniMax Music 3.0', 'https://www.minimax.io/blog/minimax-music-3-0-next-generation-open-weights-production-ready-versatile-music-model'),
    )),
    ('Product', (
        ('MiniMax Code', 'https://code.minimax.io/'),
        ('MiniMax Design', 'https://design.minimax.io/'),
        ('Audio', 'https://www.minimax.io/audio'),
        ('Talkie', 'https://www.talkie-ai.com/'),
    )),
    ('API', (
        ('Developer Docs', 'https://platform.minimax.io/docs/guides/models-intro'),
        ('Token Plan', 'https://platform.minimax.io/subscribe/token-plan'),
        ('Pricing', 'https://platform.minimax.io/docs/pricing/overview'),
        ('Console Login', 'https://platform.minimax.io/user-center/basic-information'),
        ('Status', 'https://status.minimax.io/'),
    )),
    ('Company', (
        ('About Us', 'https://www.minimax.io/about'),
        ('News', 'https://www.minimax.io/news'),
        ('Investor Relations', 'https://ir.minimax.io/'),
        ('Careers', 'https://www.minimax.io/careers'),
    )),
)


def link(label: str, href: str, cls: str = '') -> str:
    return f'<a class="{cls}" href="{escape(href, quote=True)}">{escape(label)}</a>'


def feature_rows(features: tuple) -> str:
    return '<div class="feature-rows">' + ''.join(
        '<div class="feature-row"><img src="' + A + icon + '" alt=""><h2>' + escape(title) +
        '</h2><p>' + escape(body) + '</p></div>'
        for icon, title, body in features) + '</div>'


def hero_slide(index: int, slide: dict) -> str:
    feature = (feature_rows(slide['features']) if 'features' in slide else
               '<div class="h3-video-box"><video id="h3-feature-video" playsinline preload="metadata" poster="' +
               A + slide['feature_poster'] + '"><source src="' + V + slide['feature_video'] +
               '" type="video/mp4"></video><button type="button" id="h3-play" aria-label="Play MiniMax H3 video">▶</button></div>')
    actions = ''.join(link(text, href, 'outline-btn') for text, href in slide['actions'])
    return (f'<article class="hero-slide" data-index="{index}"{" hidden" if index else ""}>'
            f'<img class="hero-title" src="{A}{slide["title_asset"]}" alt="{escape(slide["title"], quote=True)}">'
            + feature + f'<p class="hero-description">{escape(slide["description"])}</p>'
            + f'<div class="hero-actions">{actions}</div></article>')


def model_card(title: str, subtitle: str, slug: str, href: str, first: bool = False) -> str:
    return ('<a class="model-card' + (' lead' if first else '') + '" href="' + escape(href, quote=True) + '">'
            '<div class="model-art"><img class="model-base" src="' + A + f'minimax-home-model-card-{slug}-poster.webp' + '" alt="">'
            '<img class="model-overlay" src="' + A + f'minimax-home-model-card-{slug}-overlay.webp' + '" alt=""></div>'
            '<div class="model-caption"><h3>' + escape(title) + '</h3><p>' + escape(subtitle) + '</p></div></a>')


def research() -> str:
    cards = []
    for a, b, c, title, date, image, url in RESEARCH:
        tags = ''.join('<span>' + escape(t) + '</span>' for t in (a, b, *([c] if c else [])))
        cards.append('<a class="research-card" href="' + escape(url, quote=True) + '"><div class="research-copy">'
                     '<div class="tags">' + tags + '</div><h3>' + escape(title) + '</h3>'
                     '<div class="research-meta">' + date + ' <span>Learn More ›</span></div></div>'
                     '<img src="' + A + image + '" alt="" loading="lazy"></a>')
    return ('<section class="research" id="latest-research"><h2>Latest Research</h2>'
            '<p class="section-subtitle">Cutting-edge Tech · Model Capabilities · Engineering Practice</p>'
            '<div class="research-grid">' + ''.join(cards) + '</div>'
            + link('View All ›', 'https://www.minimax.io/blog', 'view-all') + '</section>')


def footer() -> str:
    columns = ''.join('<div class="footer-col"><h3>' + escape(group) + '</h3>' +
                      ''.join(link(text, href) for text, href in items) + '</div>'
                      for group, items in FOOTER)
    socials = (
        ('X', 'https://x.com/MiniMax_AI'),
        ('in', 'https://www.linkedin.com/company/minimax-ai/'),
        ('✉', 'mailto:api@minimax.io'),
        ('GitHub', 'https://github.com/MiniMax-AI'),
        ('HF', 'https://huggingface.co/MiniMaxAI'),
        ('Discord', 'https://www.minimax.io/discord'),
    )
    return ('<footer class="site-footer"><div class="footer-inner"><div class="footer-brand">'
            '<img src="' + A + '9c54bf6a-d5af-4a67-ab91-07a3236d4ab3.png" alt="MiniMax · Intelligence with Everyone">'
            '<div class="socials">' + ''.join(link(t, u) for t, u in socials) + '</div></div>'
            '<div class="footer-columns">' + columns + '</div>'
            '<p class="copyright">© 2026 MiniMax © MAX CIPHER PTE. LTD.</p></div></footer>')


def main() -> None:
    styles = '''
@font-face{font-family:Outfit;src:url('minimax-assets/Outfit-VariableFont_wght.ttf') format('truetype');font-weight:100 900;font-display:swap}
@font-face{font-family:DMSans;src:url('minimax-assets/DMSans-Regular.ttf') format('truetype');font-weight:400;font-display:swap}
@font-face{font-family:DMSans;src:url('minimax-assets/DMSans-Medium.ttf') format('truetype');font-weight:500;font-display:swap}
@font-face{font-family:DMSans;src:url('minimax-assets/DMSans-Bold.ttf') format('truetype');font-weight:700;font-display:swap}
@font-face{font-family:LibreBaskerville;src:url('minimax-assets/LibreBaskerville-Regular.otf') format('opentype');font-weight:400;font-display:swap}
@font-face{font-family:LibreBaskerville;src:url('minimax-assets/LibreBaskerville-Bold.otf') format('opentype');font-weight:700;font-display:swap}
:root{--ink:#181e25}*{box-sizing:border-box}html,body{margin:0}html{scroll-behavior:smooth}body{color:var(--ink);background:#fff;font:16px/1.5 DMSans,Arial,sans-serif}img,video{display:block;max-width:100%}a{color:inherit;text-decoration:none}a:hover{text-decoration:underline}button{font:inherit;cursor:pointer}a:focus-visible,button:focus-visible,summary:focus-visible{outline:2px solid #f56276;outline-offset:3px}
.stage{position:relative;background-size:100% 100%;background-position:center top;background-repeat:no-repeat}.stage[data-slide="0"]{background-image:url('minimax-assets/minimax-home-hero-m3-20260923-v2-background-poster.jpg')}.stage[data-slide="1"]{background-image:url('minimax-assets/minimax-home-hero-h3-20260923-v2-background-poster.jpg')}.stage[data-slide="2"]{background-image:url('minimax-assets/minimax-home-hero-code-20260923-v3-background-poster.jpg')}.stage[data-slide="3"]{background-image:url('minimax-assets/minimax-home-hero-design-20260923-v2-background-poster.jpg')}
.site-header{height:76px;position:fixed;z-index:40;top:0;left:0;right:0;display:flex;align-items:center;gap:48px;padding:0 5%;color:#fff;transition:background .2s,color .2s}.site-header.scrolled{background:#fffc;color:var(--ink);backdrop-filter:blur(12px)}.logo-white,.logo-black{width:128px;height:auto}.logo-black{display:none}.site-header.scrolled .logo-white{display:none}.site-header.scrolled .logo-black{display:block}.desktop-nav{display:flex;gap:36px;margin-right:auto;align-items:center;font:16px Outfit,Arial,sans-serif}.desktop-nav>a,.nav-group>summary{cursor:pointer;list-style:none}.nav-group>summary::-webkit-details-marker{display:none}.nav-group{position:relative}.nav-pop{position:absolute;top:33px;left:-20px;width:230px;padding:18px;background:#fff;color:#181e25;border-radius:12px;box-shadow:0 12px 40px #0003;display:grid;gap:10px;font-size:14px}.header-actions{display:flex;gap:12px}.header-actions a{min-width:140px;min-height:40px;border:1px solid #fff;border-radius:999px;display:grid;place-items:center}.header-actions a:last-child{background:#080808;border-color:#080808;color:#fff}.site-header.scrolled .header-actions a:first-child{background:#181e25;color:#fff;border-color:#181e25}.site-header.scrolled .header-actions a:last-child{background:#f4f5f7;color:#181e25;border-color:#f4f5f7}.hamburger{display:none}.mobile-menu{display:none}
.hero{height:900px;position:relative;overflow:hidden;color:#fff}.hero-motion{position:absolute;inset:0 0 auto;width:100%;height:900px;object-fit:cover;opacity:.8;mask-image:linear-gradient(#000 66%,transparent 100%)}.hero-motion[hidden]{display:none}.hero-slide{position:relative;z-index:2;height:100%;padding:80px 24px 0;text-align:center}.hero-slide[hidden]{display:none}.hero-title{height:72px;width:auto;max-width:80%;margin:0 auto}.feature-rows{width:620px;max-width:100%;margin:26px auto 0;display:grid;gap:12px}.feature-row{min-height:105px;display:grid;grid-template-columns:80px 215px 1fr;align-items:center;gap:18px;text-align:left;padding:12px 20px;background:#fff;color:#111;border:8px solid #ffffff55;border-radius:18px;box-shadow:0 9px 24px #0002}.feature-row img{width:70px;height:70px;object-fit:contain}.feature-row h2{font:600 24px/1.1 Outfit,Arial,sans-serif;margin:0}.feature-row p{color:#747474;margin:0;font:16px/1.35 DMSans,Arial,sans-serif}.hero-description{font:700 17px/1.35 LibreBaskerville,Georgia,serif;max-width:640px;margin:31px auto 24px}.hero-actions{display:flex;justify-content:center;gap:20px}.outline-btn{min-width:180px;min-height:46px;border:1px solid #fff;border-radius:10px;display:grid;place-items:center;padding:0 16px;color:#fff}.outline-btn:hover{background:#ffffff24;text-decoration:none}.h3-video-box{width:640px;height:360px;max-width:100%;position:relative;margin:25px auto 0;padding:7px;border-radius:18px;background:#ffffff66}.h3-video-box video{width:100%;height:100%;object-fit:cover;border-radius:11px}.h3-video-box button{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:64px;height:64px;border:0;border-radius:50%;background:#0009;color:#fff;font-size:26px}.h3-video-box.playing button{display:none}.carousel-bars{position:absolute;z-index:5;left:50%;bottom:80px;transform:translateX(-50%);display:flex;gap:6px}.carousel-bars button{width:64px;height:5px;padding:0;border:0;border-radius:99px;background:#ffffff55}.carousel-bars button.active{background:#fff}
.models{height:586px;padding:48px max(24px,calc((100% - 1062px)/2)) 0;text-align:center;color:#fff}.models h2,.research h2{font:600 40px/1.1 Outfit,Arial,sans-serif;margin:0}.section-subtitle{font:700 16px/1.45 LibreBaskerville,Georgia,serif;margin:12px 0 54px}.model-grid{display:grid;grid-template-columns:1.5fr 1fr 1fr;gap:24px;text-align:left}.model-card{background:#fff;color:#181e25;border:8px solid #ffffff77;border-radius:24px;box-shadow:0 5px 20px #0001;overflow:hidden;padding:14px}.model-art{height:232px;position:relative;border-radius:12px;overflow:hidden}.model-art img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}.model-caption h3{font:600 24px/1.25 Outfit,Arial,sans-serif;margin:20px 0 2px}.model-caption p{margin:0;color:#777;font-size:14px}
.research{margin:60px auto 0;max-width:1240px;height:530px;text-align:center}.research .section-subtitle{margin:12px 0 48px;color:#8c8c8c}.research-grid{display:grid;grid-template-columns:1fr 1fr;gap:55px 24px;text-align:left}.research-card{height:125px;display:flex;align-items:flex-start;justify-content:space-between;gap:24px}.research-copy{min-width:0;flex:1}.tags{display:flex;gap:6px;flex-wrap:wrap}.tags span{background:#f5f5f5;color:#777;border-radius:999px;padding:3px 10px;font:13px LibreBaskerville,Georgia,serif;white-space:nowrap}.research-card h3{font:600 20px/1.16 Outfit,Arial,sans-serif;margin:14px 0 8px}.research-card img{width:120px;height:120px;border-radius:12px;object-fit:cover;flex:none}.research-meta{font-size:13px;color:#a2a2a2}.research-meta span{margin-left:8px}.view-all{display:inline-grid;place-items:center;padding:8px 22px;border:1px solid #ddd;border-radius:999px;color:#999;margin-top:50px;font-size:13px}
.about{max-width:1226px;height:436px;margin:64px auto 0}.about-heading{display:grid;grid-template-columns:1fr 1fr;align-items:end;gap:24px}.about h2{font:600 60px/1 Outfit,Arial,sans-serif;margin:0}.about-tagline{font:700 30px/1.18 LibreBaskerville,Georgia,serif;margin:0}.about-label{display:inline-block;background:#f3f3f3;border-radius:999px;padding:3px 14px;margin:20px 0 12px;font:13px LibreBaskerville,Georgia,serif}.about p{font:14px/1.65 DMSans,Arial,sans-serif;color:#86909c;margin:0 0 16px}.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:18px}.stats strong{display:block;font:700 24px/1.1 LibreBaskerville,Georgia,serif}.stats span{color:#86909c;font-size:13px}
.site-footer{background:#000;color:#fff;min-height:687px;padding:72px 5% 34px}.footer-brand img{width:200px;height:auto}.socials{display:flex;gap:25px;margin-top:22px;color:#878787;font-weight:700}.footer-columns{display:grid;grid-template-columns:repeat(4,1fr);max-width:650px;gap:30px;margin-top:60px}.footer-col{display:grid;align-content:start;gap:13px}.footer-col h3{font:600 16px Outfit,Arial,sans-serif;margin:0 0 10px}.footer-col a{font-size:13px;color:#a2a2a2}.copyright{font-size:12px;color:#777;margin-top:55px}
@media(max-width:1000px){.desktop-nav{gap:15px}.site-header{gap:25px}.header-actions a{min-width:100px}}
@media(max-width:767px){.stage[data-slide="0"]{background-image:url('minimax-assets/minimax-home-mobile-stage-m3.webp')}.stage[data-slide="1"]{background-image:url('minimax-assets/minimax-home-mobile-stage-h3-20260923-v1.webp')}.stage[data-slide="2"]{background-image:url('minimax-assets/minimax-home-mobile-stage-code-20260923-v1.webp')}.stage[data-slide="3"]{background-image:url('minimax-assets/minimax-home-mobile-stage-design-20260923-v1.webp')}.site-header{height:50px;padding:0 16px;gap:0}.logo-white,.logo-black{width:105px}.desktop-nav,.header-actions{display:none}.hamburger{display:block;margin-left:auto;border:0;background:transparent;color:inherit;font-size:25px;line-height:1}.mobile-menu.open{display:block;position:fixed;z-index:60;inset:0;background:#fff;color:#181e25;overflow-y:auto;padding:0 16px 30px}.mobile-menu-head{height:50px;display:flex;justify-content:space-between;align-items:center}.mobile-menu-head img{width:105px}.mobile-menu-head button{border:0;background:none;font-size:26px}.mobile-menu details,.mobile-menu .menu-link{display:block;border-bottom:1px solid #eee;padding:15px 0;font:600 18px Outfit,Arial,sans-serif}.mobile-menu summary{list-style:none;cursor:pointer}.mobile-menu summary:after{content:'›';float:right}.mobile-menu details[open] summary:after{content:'⌄'}.mobile-menu details a{display:block;font:16px DMSans,Arial,sans-serif;padding:12px 24px}.mobile-menu small{display:block;color:#999;font-size:12px;padding-top:18px}.mobile-menu .menu-login{display:inline-block;margin-top:25px;background:#111;color:#fff;border-radius:999px;padding:9px 30px}.hero{height:742px}.hero-motion{display:none}.hero-slide{padding:75px 16px 0}.hero-title{height:60px;max-width:100%}.feature-rows{width:100%;margin:17px 0 0;gap:12px}.feature-row{min-height:94px;grid-template-columns:71px 1fr;gap:8px;padding:7px 8px;border-width:6px;border-radius:14px}.feature-row img{width:65px;height:65px}.feature-row h2{font-size:20px;line-height:1.1}.feature-row p{grid-column:2;font-size:14px;line-height:1.25;margin-top:-16px}.hero-description{font-size:18px;line-height:1.25;margin:34px auto 38px;max-width:340px}.hero-actions{display:block;padding:0 15px}.hero-actions .outline-btn{display:none;width:100%;min-height:47px;margin:0}.hero-actions .outline-btn:first-child{display:grid}.carousel-bars{bottom:37px}.carousel-bars button{width:25px;height:5px}.h3-video-box{width:100%;height:306px;margin:25px auto 0}.h3-video-box button{width:50px;height:50px;font-size:20px}.hero-slide:has(.h3-video-box) .hero-description{margin:24px auto 22px;font-size:16px}.models{height:710px;padding:28px 20px 0}.models h2,.research h2{font-size:24px}.section-subtitle{font-size:16px;line-height:1.2;margin:12px 0 70px}.model-grid{grid-template-columns:1fr 1fr;gap:24px 16px}.model-card{padding:8px;border-width:5px;border-radius:22px}.model-card.lead{grid-column:1/3}.model-card.lead .model-art{height:204px}.model-art{height:143px;border-radius:9px}.model-caption h3{font-size:18px;line-height:1.1;margin:12px 2px 2px}.model-card.lead .model-caption h3{font-size:24px}.model-caption p{font-size:12px;margin:0 2px}.research{margin:50px 16px 0;height:807px}.research .section-subtitle{margin:10px auto 48px;max-width:350px}.research-grid{display:block}.research-card{height:168px;gap:16px;padding:0 8px}.research-card img{width:100px;height:100px;border-radius:9px}.research-card h3{font-size:15.5px;line-height:1.18;margin:12px 0 5px}.research-meta{font-size:11px}.research-meta span{margin-left:6px}.tags span{font-size:10px;padding:2px 7px}.view-all{margin-top:8px}.about{margin:50px 24px 0;height:775px;text-align:center}.about-heading{display:block}.about h2{font-size:60px}.about-tagline{font-size:28px;margin:6px 0 0}.about-label{margin:35px auto 22px}.about p{text-align:justify;line-height:1.65;margin-bottom:30px}.stats{grid-template-columns:1fr 1fr;text-align:left;margin-top:22px;gap:28px}.stats strong{font-size:20px}.stats span{font-size:12px}.site-footer{min-height:960px;padding:74px 24px 32px}.footer-columns{grid-template-columns:1fr 1fr;margin-top:45px;gap:38px}.footer-col a{font-size:12px}.copyright{margin-top:48px}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
'''
    header = ('<header class="site-header" id="site-header"><a href="https://www.minimax.io/" aria-label="MiniMax home">'
              '<img class="logo-white" src="' + A + 'minimax-horizontal-white.webp" alt="MiniMax"><img class="logo-black" src="' + A + 'minimax-horizontal-brand-black.webp" alt="MiniMax"></a>'
              '<nav class="desktop-nav" aria-label="Main navigation"><details class="nav-group"><summary>Models</summary><div class="nav-pop">'
              + link('MiniMax M3', 'https://www.minimax.io/models/text/m3') + link('MiniMax M2.7', 'https://www.minimax.io/models/text/m27') +
              link('MiniMax H3', 'https://www.minimax.io/blog/minimax-h3') + link('MiniMax Speech 2.8', 'https://www.minimax.io/news/minimax-speech-28') + '</div></details>'
              '<details class="nav-group"><summary>Product</summary><div class="nav-pop">' + link('MiniMax Code', 'https://code.minimax.io/') + link('MiniMax Design', 'https://design.minimax.io/') +
              link('Audio', 'https://www.minimax.io/audio') + link('Talkie', 'https://www.talkie-ai.com/') + '</div></details>'
              + link('API', 'https://platform.minimax.io/docs/guides/models-intro') + link('Token Plan', 'https://platform.minimax.io/subscribe/token-plan') +
              link('Research', '#latest-research') + link('Company', '#about') + '</nav>'
              '<div class="header-actions">' + link('Contact Us', 'https://platform.minimax.io/contact-us') + link('Login', 'https://platform.minimax.io/user-center/basic-information') + '</div>'
              '<button class="hamburger" id="open-menu" type="button" aria-label="Open menu">☰</button></header>')
    menu = ('<aside class="mobile-menu" id="mobile-menu" aria-label="MiniMax mobile menu"><div class="mobile-menu-head"><img src="' + A + 'minimax-horizontal-brand-black.webp" alt="MiniMax">'
            '<button id="close-menu" type="button" aria-label="Close menu">×</button></div>'
            '<details open><summary>Models</summary><small>LLM</small>' + link('MiniMax M3  NEW', 'https://www.minimax.io/models/text/m3') + link('MiniMax M2.7', 'https://www.minimax.io/models/text/m27') + link('MiniMax M2.5', 'https://www.minimax.io/models/text') +
            '<small>VIDEO</small>' + link('MiniMax H3  NEW', 'https://www.minimax.io/blog/minimax-h3') + '<small>SPEECH & MUSIC</small>' +
            link('MiniMax Speech 2.8  NEW', 'https://www.minimax.io/news/minimax-speech-28') + link('MiniMax Music 3.0  NEW', 'https://www.minimax.io/blog/minimax-music-3-0-next-generation-open-weights-production-ready-versatile-music-model') + '</details>'
            '<details><summary>Product</summary>' + link('MiniMax Code', 'https://code.minimax.io/') + link('MiniMax Design', 'https://design.minimax.io/') + link('Audio', 'https://www.minimax.io/audio') + link('Talkie', 'https://www.talkie-ai.com/') + '</details>'
            + link('API', 'https://platform.minimax.io/docs/guides/models-intro', 'menu-link') + link('Token Plan', 'https://platform.minimax.io/subscribe/token-plan', 'menu-link') +
            link('Research', '#latest-research', 'menu-link') + link('Company', '#about', 'menu-link') + link('Login', 'https://platform.minimax.io/user-center/basic-information', 'menu-login') + '</aside>')
    motions = ''.join(f'<video class="hero-motion" data-video-index="{i}" autoplay muted loop playsinline preload="none" poster="{A}{slide["desktop_bg"]}"{" hidden" if i else ""}><source src="{V}{slide["video"]}" type="video/mp4"></video>'
                      for i, slide in enumerate(SLIDES))
    bars = '<div class="carousel-bars" aria-label="Hero campaigns">' + ''.join(
        f'<button type="button" data-show="{i}" class="{"active" if i == 0 else ""}" aria-label="Show {escape(s["title"], quote=True)}"></button>'
        for i, s in enumerate(SLIDES)) + '</div>'
    models = ('<section class="models" id="models-highlight"><h2>Flagship Models</h2>'
              '<p class="section-subtitle">MiniMax’s latest featured models — Language / Video / Speech &amp; Music</p>'
              '<div class="model-grid">' + model_card('Introducing MiniMax M3', 'Top Coding · 1M Context · Multimodal', 'm3', 'https://platform.minimax.io/docs/guides/text-generation', True) +
              model_card('MiniMax H3', 'Video Generation', 'h3', 'https://platform.minimax.io/docs/guides/video-generation') +
              model_card('MiniMax Speech 2.8', 'Speech', 'speech', 'https://platform.minimax.io/docs/guides/speech-voice-clone') + '</div></section>')
    about = ('<section class="about" id="about"><div class="about-heading"><h2>MiniMax</h2><p class="about-tagline">A World-Leading General AI Technology Company</p></div>'
             '<span class="about-label">About Us</span><p>Founded in early 2022, MiniMax is driven by the mission to ‘co-create intelligence with everyone,’ dedicated to advancing the frontiers of AI and achieving Artificial General Intelligence (AGI). MiniMax has independently developed a series of multimodal foundation models with powerful code and Agent capabilities, as well as ultra-long context processing, capable of understanding, generating, and integrating multiple modalities including text, audio, image, video, and music.</p>'
             '<p>Building on these proprietary models, MiniMax has launched a suite of AI-native products worldwide, including MiniMax Code, MiniMax Design, MiniMax Audio, Talkie, and an open platform for enterprises and developers — delivering cutting-edge intelligent experiences to users around the globe.</p>'
             '<div class="stats"><div><strong>230+</strong><span>Countries &amp; Regions Served</span></div><div><strong>300M+</strong><span>Global Individual Users</span></div><div><strong>2M+</strong><span>Enterprise Clients &amp; Developers</span></div><div><strong>100+</strong><span>Enterprise Coverage Countries</span></div></div></section>')
    script = '''<script>
(() => {
  const stage=document.getElementById('stage');
  const slides=[...document.querySelectorAll('.hero-slide')];
  const videos=[...document.querySelectorAll('.hero-motion')];
  const bars=[...document.querySelectorAll('[data-show]')];
  let active=0,timer;
  function show(index){
    active=(index+slides.length)%slides.length;
    stage.dataset.slide=String(active);
    slides.forEach((node,i)=>node.hidden=i!==active);
    videos.forEach((node,i)=>{node.hidden=i!==active;node.pause();if(i===active&&innerWidth>767&&!matchMedia('(prefers-reduced-motion: reduce)').matches)node.play().catch(()=>{});});
    bars.forEach((node,i)=>node.classList.toggle('active',i===active));
  }
  function schedule(){clearInterval(timer);if(!matchMedia('(prefers-reduced-motion: reduce)').matches)timer=setInterval(()=>show(active+1),8000)}
  bars.forEach(b=>b.addEventListener('click',()=>{show(Number(b.dataset.show));schedule()}));
  document.addEventListener('visibilitychange',()=>{if(document.hidden){clearInterval(timer);videos.forEach(v=>v.pause())}else{show(active);schedule()}});
  show(0);schedule();
  const head=document.getElementById('site-header');
  function headerState(){head.classList.toggle('scrolled',scrollY>30)}
  document.addEventListener('scroll',headerState,{passive:true});headerState();
  const menu=document.getElementById('mobile-menu');
  function toggleMenu(open){menu.classList.toggle('open',open);document.body.style.overflow=open?'hidden':''}
  document.getElementById('open-menu').addEventListener('click',()=>toggleMenu(true));
  document.getElementById('close-menu').addEventListener('click',()=>toggleMenu(false));
  menu.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>toggleMenu(false)));
  document.addEventListener('keydown',e=>{if(e.key==='Escape')toggleMenu(false)});
  const play=document.getElementById('h3-play'),clip=document.getElementById('h3-feature-video');
  play.addEventListener('click',()=>{clip.controls=true;clip.play().then(()=>play.parentElement.classList.add('playing')).catch(()=>{})});
  clip.addEventListener('pause',()=>play.parentElement.classList.remove('playing'));
})();
</script>'''
    html = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>MiniMax · 2026-09-28 Homepage Study</title><meta name="description" content="Dated study of MiniMax public homepage using observed official content and assets.">'
            '<style>' + styles + '</style></head><body><div class="stage" id="stage" data-slide="0">' + header + menu +
            '<section class="hero" aria-label="MiniMax campaigns">' + motions + ''.join(hero_slide(i, s) for i, s in enumerate(SLIDES)) + bars + '</section>' + models + '</div>' +
            research() + about + footer() + script + '</body></html>\n')
    target = ROOT / 'minimax.html'
    target.write_text(html)
    print(f'Wrote {target} ({target.stat().st_size} bytes)')


if __name__ == '__main__':
    main()
