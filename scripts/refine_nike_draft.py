#!/usr/bin/env python3
"""Build a dated Nike Canada study with observed public copy and Nike media."""

from __future__ import annotations

from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / '.stitch-work' / 'current-official'
A = 'nike-assets/'

SLIDES = (
    ('pegasus', 'EVERY. DAY. SPEED.',
     'Pegasus Plus 2 features Air Zoom and ultra-light ZoomX to fuel the road to raceday. Coming soon.',
     (('Explore', 'https://www.nike.com/ca/w/pegasus-running-37v7jz8nexh'),),
     'hero-desktop.webp', 'hero-mobile.webp'),
    ('caitlin', 'CAITLIN CLARK EATS', 'Your lunch from thirty-two feet.',
     (('Explore', 'https://www.nike.com/ca/w/caitlin-clark-b0s81'),),
     None, None),
    ('body', 'BODY OBSESSED',
     'Unapologetically feminine, undeniably strong: a new collection chosen by Olympians who never compromise.',
     (('Shop', 'https://www.nike.com/ca/w/nikeskims-b2asd'),
      ('Explore More', 'https://www.nike.com/ca/nikeskims')),
     'hero-body-desktop.webp', 'hero-body-mobile.webp'),
)

SPORTS = (
    ('Running', 'sport-running.webp', 'sport-running-mobile.webp', 'https://www.nike.com/ca/w/running-shoes-37v7jzy7ok'),
    ('Tennis', 'sport-tennis.webp', 'sport-tennis.webp', 'https://www.nike.com/ca/w/tennis-ed1q'),
    ('Basketball', 'sport-basketball.webp', 'sport-basketball.webp', 'https://www.nike.com/ca/w/basketball-3glsm'),
    ('Training', 'sport-training.webp', 'sport-training.webp', 'https://www.nike.com/ca/w/training-gym-58jto'),
)

MERCH = {
    'Featured': ['Air Force 1', 'Jordan 1', 'Air Max Dn', 'Vomero', 'Metcon', 'Air Max 270', 'Air Max 90', 'Blazer', 'Pegasus'],
    'Shoes': ['All Shoes', 'Jordan Shoes', 'Running Shoes', 'Basketball Shoes', 'Tennis Shoes', 'Training Shoes', 'Custom Shoes', 'Sale Shoes', 'Football Boots'],
    'Clothing': ['All Clothing', 'Tops & T-Shirts', 'Shorts', 'Hoodies & Sweatshirts', 'Joggers & Tracksuit Bottoms', 'Sports Bras', 'Trousers & Tights', 'Socks', 'Yoga', 'NikeLab', 'Plus Size', 'Big & Tall', 'Sale Clothing'],
    'Kids': ['Baby & Toddler Shoes', "Kids' Shoes", "Kids' Basketball Shoes", "Kids' Running Shoes", "Kids' Jordan Shoes", "Kids' Clothing", "Kids' Backpacks", "Kids' Socks", "Kids' Sale"],
}


def icon(name: str) -> str:
    paths = {
        'search': '<circle cx="10.8" cy="10.8" r="6.8"/><path d="m16 16 5 5"/>',
        'heart': '<path d="M20.8 8.5c0 4.6-8.8 10.4-8.8 10.4S3.2 13.1 3.2 8.5a4.7 4.7 0 0 1 8.8-2.2 4.7 4.7 0 0 1 8.8 2.2Z"/>',
        'bag': '<path d="M4.7 8h14.6l1 12H3.7l1-12Z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/>',
        'person': '<circle cx="12" cy="7.5" r="3.2"/><path d="M5.6 20c.2-4.1 2.6-6.3 6.4-6.3s6.2 2.2 6.4 6.3"/>',
        'menu': '<path d="M3 6h18M3 12h18M3 18h18"/>',
        'close': '<path d="M4 4 20 20M20 4 4 20"/>',
        'chevron': '<path d="m7 9 5 5 5-5"/>',
    }
    return '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">' + paths[name] + '</svg>'


def picture(desktop: str, mobile: str, alt: str, cls: str = '') -> str:
    return (f'<picture class="{cls}"><source media="(max-width: 767px)" srcset="{A}{mobile}">'
            f'<img src="{A}{desktop}" alt="{escape(alt, quote=True)}" loading="lazy"></picture>')


def pill(text: str, url: str, light: bool = False) -> str:
    return f'<a class="pill{" pill-light" if light else ""}" href="{escape(url, quote=True)}">{escape(text)}</a>'


def hero() -> str:
    slides = []
    for index, (key, title, body, links, poster_desktop, poster_mobile) in enumerate(SLIDES):
        posters = (f' poster="{A}{poster_desktop}"' if poster_desktop else '',
                   f' poster="{A}{poster_mobile}"' if poster_mobile else '')
        clips = ''.join(
            f'<video class="hero-video {device}" muted autoplay loop playsinline preload="metadata"{poster}>'
            f'<source src="{A}{key}-{device}.mp4" type="video/mp4"></video>'
            for device, poster in zip(('desktop', 'mobile'), posters)
        )
        ctas = ''.join(pill(label, url) for label, url in links)
        slides.append(f'<article class="hero-slide{" active" if index == 0 else ""}" data-slide="{index}"'
                      f'{" hidden" if index else ""}><div class="hero-media">{clips}</div>'
                      f'<div class="hero-copy"><h1>{escape(title)}</h1><p>{escape(body)}</p>'
                      f'<div class="actions">{ctas}</div></div></article>')
    return ('<section class="hero" aria-label="Nike campaigns">' + ''.join(slides) +
            '<div class="hero-controls"><button type="button" id="hero-prev" aria-label="Previous campaign">‹</button>'
            '<span id="hero-count">1 / 3</span><button type="button" id="hero-next" aria-label="Next campaign">›</button>'
            '<button type="button" id="hero-toggle" aria-label="Pause video">Ⅱ</button></div></section>')


def merch() -> str:
    columns = []
    for heading, items in MERCH.items():
        # The public homepage renders these as a merchandising directory.
        # Keep labels exact; the paths lead to the corresponding official Nike search.
        links = ''.join(f'<a href="https://www.nike.com/ca/w?q={escape(item.replace(" ", "+"), quote=True)}">{escape(item)}</a>'
                        for item in items)
        columns.append(f'<details class="merch-group"><summary>{escape(heading)}</summary><div>{links}</div></details>')
    return '<nav class="merch" aria-label="Popular Nike categories">' + ''.join(columns) + '</nav>'


def main() -> None:
    head = '''<!doctype html><html lang="en-CA"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Nike Canada · 2026-09-28 Homepage Study</title><meta name="description" content="Dated visual study of Nike Canada public homepage campaigns, using observed official media and copy."><style>
@font-face{font-family:NikeFutura;src:url('nike-assets/Nike-Futura-ND.woff2') format('woff2');font-display:swap}
@font-face{font-family:HelveticaNow;src:url('nike-assets/HelveticaNowText.woff2') format('woff2');font-display:swap}
@font-face{font-family:HelveticaNow;src:url('nike-assets/HelveticaNowTextMedium.woff2') format('woff2');font-weight:500;font-display:swap}
@font-face{font-family:HelveticaNowDisplay;src:url('nike-assets/HelveticaNowDisplayMedium.woff2') format('woff2');font-display:swap}
:root{--ink:#111;--soft:#f5f5f5}*{box-sizing:border-box}html,body{margin:0}body{background:#fff;color:var(--ink);font:16px/1.5 HelveticaNow,Arial,sans-serif}button,input{font:inherit}button{cursor:pointer}a{color:inherit;text-decoration:none}a:hover{text-decoration:underline}a:focus-visible,button:focus-visible,summary:focus-visible{outline:2px solid #1151ff;outline-offset:3px}img,video{display:block;max-width:100%}.shell{position:sticky;top:0;z-index:30;background:#fff}.utility{height:36px;background:var(--soft);display:flex;justify-content:space-between;align-items:center;padding:0 3.75%;font-size:12px;font-weight:500}.utility .marks,.utility .utility-links{display:flex;align-items:center;gap:20px}.utility .marks img:first-child{width:20px;height:20px}.utility .marks img:last-child{width:28px;height:18px}.utility-links a+a:before{content:'|';color:#777;margin-right:20px}.main-nav{height:60px;display:flex;align-items:center;gap:32px;padding:0 3.75%}.swoosh{display:block;width:64px;flex:none}.swoosh img{width:64px;height:22px}.nav-links{display:flex;align-items:center;gap:24px;margin:auto;font-size:16px;font-weight:500;white-space:nowrap}.nav-actions{display:flex;align-items:center;gap:20px}.search{width:170px;height:40px;border:0;border-radius:999px;background:var(--soft);display:flex;gap:8px;align-items:center;padding:0 14px;color:#777}.search svg{width:23px;height:23px}.icon-btn{width:26px;height:26px;display:grid;place-items:center;padding:0;border:0;background:none}.icon-btn svg{width:24px;height:24px}.mobile-only{display:none}.hero{position:relative}.hero-slide[hidden]{display:none}.hero-media{position:relative;width:100%;height:48.6vw;max-height:622px;background:#111}.hero-video{width:100%;height:100%;object-fit:cover}.hero-video.mobile{display:none}.hero-copy{text-align:center;min-height:329px;padding:36px 24px 72px}.hero-copy h1,.overlaid h2{font:500 clamp(46px,5.94vw,76px)/.98 NikeFutura,Impact,sans-serif;text-transform:uppercase;margin:0}.hero-copy p{margin:16px auto 22px;max-width:700px}.actions{display:flex;justify-content:center;gap:8px}.pill{display:inline-flex;align-items:center;justify-content:center;min-height:40px;padding:0 24px;background:#111;color:#fff;border-radius:999px;font-weight:500;white-space:nowrap}.pill:hover{text-decoration:none;background:#555}.pill-light{background:#fff;color:#111}.pill-light:hover{background:#ddd}.hero-controls{position:absolute;right:40px;top:calc(min(48.6vw,622px) - 54px);display:flex;align-items:center;gap:6px;color:#fff}.hero-controls button{width:32px;height:32px;border:1px solid #fff9;border-radius:50%;background:#1118;color:#fff;font-size:24px;line-height:1}.hero-controls span{font-size:12px;padding:0 4px}.overlaid{position:relative}.overlaid picture,.overlaid picture img{width:100%;height:100%}.overlaid picture img{object-fit:cover}.overlaid:after{content:'';position:absolute;inset:45% 0 0;background:linear-gradient(transparent,#0005);pointer-events:none}.overlaid .overlay-content{position:absolute;z-index:1;bottom:36px;left:24px;right:24px;text-align:center;color:#fff}.overlay-content p{margin:14px auto 20px;max-width:630px}.studio{height:48.7vw;max-height:623px;min-height:400px}.duo{max-width:1088px;margin:83px auto 0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.duo .overlaid{height:407px}.duo .overlaid .overlay-content{text-align:left;left:36px;right:30px;bottom:36px}.duo .overlaid h2{font-size:48px;line-height:1}.duo .light-card:after{background:none}.duo .light-card .overlay-content{color:#111}.duo .light-card .pill{background:#111;color:#fff}.acg{margin-top:142px}.acg-wordmark{height:91px;display:flex;justify-content:center;align-items:center}.acg-wordmark img{height:91px;width:auto;max-width:100%}.acg-media{height:52.1vw;max-height:667px}.acg-media .overlay-content{bottom:32px}.sport{margin:90px auto 0;max-width:1192px;padding:0 0 60px}.sport-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:24px}.sport h2{font:24px/1.2 HelveticaNowDisplay,Arial,sans-serif;margin:0}.rail-controls{display:flex;gap:12px}.rail-controls button{width:40px;height:40px;border:0;border-radius:50%;background:var(--soft);font-size:25px}.sport-rail{display:flex;gap:12px;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none}.sport-rail::-webkit-scrollbar{display:none}.sport-card{width:387px;flex:0 0 387px;position:relative;scroll-snap-align:start}.sport-card picture,.sport-card img{display:block;width:100%;height:516px;object-fit:cover}.sport-card span{position:absolute;left:24px;bottom:24px;background:#fff;border-radius:999px;padding:10px 22px;font-weight:500}.bottom-brand{margin:44px auto 88px;width:342px}.bottom-brand img{width:100%;height:auto}.merch{max-width:1192px;margin:0 auto 72px;display:grid;grid-template-columns:repeat(4,1fr);gap:20px}.merch-group summary{list-style:none;font-size:22px;font-family:HelveticaNowDisplay,Arial,sans-serif;cursor:pointer}.merch-group summary::-webkit-details-marker{display:none}.merch-group>div{display:grid;gap:10px;margin-top:18px;color:#707072}.merch-group a:hover{color:#111}.site-footer{border-top:1px solid #e5e5e5;padding:48px max(24px,calc((100% - 1192px)/2)) 64px;color:#707072}.footer-top{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}.footer-top h3{font-size:14px;font-weight:500;color:#111;margin:0 0 24px}.footer-top a{display:block;margin:14px 0;font-size:14px}.footer-bottom{display:flex;flex-wrap:wrap;gap:22px;margin-top:66px;font-size:12px}.footer-bottom a:hover{color:#111}.menu-scrim,.mobile-menu{display:none}
@media(max-width:1000px){.nav-links{gap:14px;font-size:14px}.main-nav{gap:18px}.search{width:40px;padding:8px}.search span{display:none}.sport,.merch{margin-left:24px;margin-right:24px}}
@media(max-width:767px){.utility,.nav-links,.search,.nav-actions .desktop-only{display:none}.main-nav{height:60px;padding:0 24px;gap:0}.swoosh,.swoosh img{width:64px}.nav-actions{margin-left:auto;gap:18px}.mobile-only{display:grid}.hero-media{height:150vw;max-height:none}.hero-video.desktop{display:none}.hero-video.mobile{display:block}.hero-copy{min-height:296px;padding:48px 24px 68px}.hero-copy h1,.overlaid h2{font-size:40px;line-height:1}.hero-copy p{margin:20px auto 24px;line-height:1.4}.hero-controls{top:calc(150vw - 52px);right:15px}.hero-controls button{width:30px;height:30px}.studio{height:150vw;max-height:none;min-height:0}.studio .overlay-content{bottom:32px}.studio h2{font-size:40px}.duo{display:flex;flex-direction:column;margin:84px 24px 0;gap:8px}.duo .overlaid{height:calc((100vw - 48px)*1.497);max-height:none}.duo .overlaid .overlay-content{left:24px;right:24px;bottom:28px}.duo .overlaid h2{font-size:40px}.acg{margin-top:85px}.acg-wordmark{height:91px}.acg-wordmark img{height:91px}.acg-media{height:150vw;max-height:none}.acg-media .overlay-content{bottom:34px}.acg-media .overlay-content p{max-width:325px}.sport{margin:88px 0 0;padding:0 0 0 24px}.sport-head{padding-right:24px;margin-bottom:26px}.sport h2{font-size:24px}.sport-rail{gap:12px}.sport-card{width:300px;flex-basis:300px}.sport-card picture,.sport-card img{height:400px}.sport-card:last-child{margin-right:24px}.bottom-brand{margin:140px auto 122px;width:342px}.merch{display:block;margin:0 24px 50px}.merch-group{border-bottom:1px solid #e5e5e5}.merch-group summary{padding:14px 0;font-size:18px}.merch-group summary:after{content:'+';float:right}.merch-group[open] summary:after{content:'−'}.merch-group>div{padding:0 0 20px;margin:0;gap:12px}.site-footer{padding:36px 24px 70px}.footer-top{display:block}.footer-top>div{border-bottom:1px solid #e5e5e5;padding:10px 0}.footer-top h3{margin:0 0 10px;font-size:16px}.footer-top a{display:none}.footer-bottom{display:grid;gap:12px;margin-top:32px}.menu-scrim.open{display:block;position:fixed;inset:0;background:#0006;z-index:50}.mobile-menu.open{display:block;position:fixed;z-index:51;top:0;right:0;bottom:0;width:min(320px,calc(100vw - 70px));overflow-y:auto;background:#fff;padding:20px 24px;box-shadow:-8px 0 32px #0002}.mobile-menu .close-row{display:flex;justify-content:flex-end;margin-bottom:20px}.mobile-menu .menu-primary{display:grid;gap:14px;font:24px/1.2 HelveticaNowDisplay,Arial,sans-serif}.mobile-menu details summary{list-style:none;cursor:pointer}.mobile-menu details summary:after{content:'›';float:right}.mobile-menu details[open] summary:after{content:'⌄'}.mobile-menu details a{display:block;font:16px HelveticaNow,Arial,sans-serif;padding:9px 12px}.mobile-menu .member{margin:38px 0 22px;color:#707072}.mobile-menu .member a{color:#111;text-decoration:underline}.menu-actions{display:flex;gap:8px}.menu-actions a{padding:9px 18px;border:1px solid #cacacb;border-radius:999px}.menu-actions a:first-child{background:#111;color:#fff}.menu-secondary{display:grid;gap:20px;margin-top:34px}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
</style></head><body>'''
    utility = ('<div class="utility"><div class="marks"><a href="https://www.nike.com/ca/jordan"><img src="' + A + 'jordan.svg" alt="Jordan"></a>'
               '<a href="https://www.converse.ca/"><img src="' + A + 'converse.svg" alt="Converse"></a></div>'
               '<div class="utility-links"><a href="https://www.nike.com/ca/retail">Find a Store</a><a href="https://www.nike.com/ca/help">Help</a>'
               '<a href="https://www.nike.com/ca/membership">Join Us</a><a href="https://www.nike.com/ca/register">Sign In</a></div></div>')
    nav = ('<header class="shell">' + utility + '<div class="main-nav"><a class="swoosh" href="https://www.nike.com/ca/" aria-label="Nike home"><img src="' + A + 'swoosh.svg" alt="Nike"></a>'
           '<nav class="nav-links" aria-label="Nike categories"><a href="https://www.nike.com/ca/men">Men</a><a href="https://www.nike.com/ca/women">Women</a><a href="https://www.nike.com/ca/kids">Kids</a>'
           '<a href="https://www.nike.com/ca/w/performance-3k7dg">Sport</a><a href="https://www.nike.com/ca/jordan">Jordan</a><a href="https://www.nike.com/ca/nikeskims">NikeSKIMS</a><a href="https://www.nike.com/ca/launch">SNKRS</a></nav>'
           '<div class="nav-actions"><a class="search" href="https://www.nike.com/ca/w" aria-label="Search">' + icon('search') + '<span>Search</span></a>'
           '<a class="icon-btn mobile-only" href="https://www.nike.com/ca/w" aria-label="Search">' + icon('search') + '</a>'
           '<a class="icon-btn mobile-only" href="https://www.nike.com/ca/register" aria-label="Account">' + icon('person') + '</a>'
           '<a class="icon-btn desktop-only" href="https://www.nike.com/ca/favorites" aria-label="Favorites">' + icon('heart') + '</a>'
           '<a class="icon-btn" href="https://www.nike.com/ca/cart" aria-label="Bag">' + icon('bag') + '</a>'
           '<button class="icon-btn mobile-only" id="open-menu" type="button" aria-label="Open menu">' + icon('menu') + '</button></div></div></header>')
    menu = ('<div class="menu-scrim" id="menu-scrim"></div><aside class="mobile-menu" id="mobile-menu" aria-label="Nike mobile menu">'
            '<div class="close-row"><button class="icon-btn" id="close-menu" type="button" aria-label="Close menu">' + icon('close') + '</button></div>'
            '<div class="menu-primary"><details><summary>Men</summary><a href="https://www.nike.com/ca/men">New Arrivals</a><a href="https://www.nike.com/ca/men">Best Sellers</a><a href="https://www.nike.com/ca/men">Nike Tech</a><a href="https://www.nike.com/ca/men">Shoes</a><a href="https://www.nike.com/ca/men">Clothing</a><a href="https://www.nike.com/ca/men">Sport</a><a href="https://www.nike.com/ca/men">Accessories</a><a href="https://www.nike.com/ca/men">Sale</a></details>'
            '<details><summary>Women</summary><a href="https://www.nike.com/ca/women">Shop Women</a></details><details><summary>Kids</summary><a href="https://www.nike.com/ca/kids">Shop Kids</a></details>'
            '<details><summary>Sport</summary><a href="https://www.nike.com/ca/w/performance-3k7dg">Shop Sport</a></details><a href="https://www.nike.com/ca/jordan">Jordan</a><a href="https://www.nike.com/ca/nikeskims">NikeSKIMS</a><a href="https://www.nike.com/ca/launch">SNKRS</a></div>'
            '<p class="member">Become a Nike Member for the best products, inspiration and stories in sport. <a href="https://www.nike.com/ca/membership">Learn more</a></p>'
            '<div class="menu-actions"><a href="https://www.nike.com/ca/membership">Join Us</a><a href="https://www.nike.com/ca/register">Sign In</a></div>'
            '<div class="menu-secondary"><a href="https://www.nike.com/ca/help">Help</a><a href="https://www.nike.com/ca/cart">Bag</a><a href="https://www.nike.com/ca/orders">Orders</a><a href="https://www.nike.com/ca/retail">Find a Store</a></div></aside>')
    studio = ('<section class="studio overlaid" aria-label="Studio Fleece">' + picture('studio-desktop.webp', 'studio-mobile.webp', 'STUDIO FLEECE') +
              '<div class="overlay-content"><h2>STUDIO FLEECE</h2><p>It’s just a sweatsuit until its not</p>' +
              pill('Shop', 'https://www.nike.com/ca/w/fleece-4xh6qz5e1x6znik1', True) + '</div></section>')
    duo = ('<section class="duo" aria-label="Jordan and SNKRS campaigns">'
           '<article class="overlaid light-card">' + picture('jordan-desktop.webp', 'jordan-mobile.webp', 'JORDAN HEAT') +
           '<div class="overlay-content"><h2>JORDAN HEAT</h2><p>Latest drops. Iconic styles.</p>' +
           pill('Shop', 'https://www.nike.com/ca/w/new-jordan-37eefz3n82y') + '</div></article>'
           '<article class="overlaid">' + picture('snkrs-desktop.webp', 'snkrs-mobile.webp', 'SNKRS Radar') +
           '<div class="overlay-content"><h2>SNKRS RADAR</h2><p>Be ready for what’s next.</p>' +
           pill('View Calendar', 'https://www.nike.com/ca/launch/upcoming', True) + '</div></article></section>')
    acg = ('<section class="acg" aria-label="ACG Chamo Camo"><div class="acg-wordmark"><img src="' + A + 'acg-wordmark.webp" alt="All Conditions Gear"></div>'
           '<div class="acg-media overlaid">' + picture('acg-desktop.webp', 'acg-mobile.webp', 'ACG Chamo Camo') +
           '<div class="overlay-content"><h2>ACG CHAMO CAMO</h2><p>A print inspired by the foliage of the Chamonix Valley. Wear it and you’ll disappear just enough.</p>' +
           pill('Shop', 'https://www.nike.com/ca/ACG', True) + '</div></div></section>')
    sports = ('<section class="sport" aria-label="Shop by Sport"><div class="sport-head"><h2>Shop by Sport</h2><div class="rail-controls">'
              '<button id="rail-prev" type="button" aria-label="Previous sport">‹</button><button id="rail-next" type="button" aria-label="Next sport">›</button></div></div>'
              '<div class="sport-rail" id="sport-rail">' + ''.join(
                  f'<a class="sport-card" href="{escape(url, quote=True)}">{picture(desktop, mobile, label)}<span>Shop {escape(label)}</span></a>'
                  for label, desktop, mobile, url in SPORTS) + '</div></section>')
    footer = ('<footer class="site-footer"><div class="footer-top"><div><h3>Resources</h3><a href="https://www.nike.com/ca/retail">Find a Store</a><a href="https://www.nike.com/ca/a/nike-journal">Nike Journal</a><a href="https://www.nike.com/ca/membership">Become a Member</a><a href="https://www.nike.com/ca/help">Feedback</a></div>'
              '<div><h3>Help</h3><a href="https://www.nike.com/ca/help">Get Help</a><a href="https://www.nike.com/ca/orders">Order Status</a><a href="https://www.nike.com/ca/help/a/returns-policy">Returns</a></div>'
              '<div><h3>Company</h3><a href="https://about.nike.com/">About Nike</a><a href="https://jobs.nike.com/">Careers</a></div></div>'
              '<div class="footer-bottom"><span>Canada</span><span>© 2026 Nike, Inc. All rights reserved.</span>'
              '<a href="https://www.nike.com/ca/help/a/terms-of-use">Terms of Use</a><a href="https://www.nike.com/ca/help/a/terms-of-sale">Terms of Sale</a>'
              '<a href="https://www.nike.com/ca/help/a/company-details">Company Details</a><a href="https://www.nike.com/ca/help/a/privacy-policy">Privacy &amp; Cookie Policy</a></div></footer>')
    script = '''<script>
(() => {
  const slides=[...document.querySelectorAll('.hero-slide')];
  let active=0,playing=true;
  function show(index){
    active=(index+slides.length)%slides.length;
    slides.forEach((slide,i)=>{const selected=i===active;slide.hidden=!selected;slide.classList.toggle('active',selected);
      slide.querySelectorAll('video').forEach(video=>{if(selected&&playing){video.play().catch(()=>{});}else video.pause();});});
    document.getElementById('hero-count').textContent=`${active+1} / ${slides.length}`;
  }
  document.getElementById('hero-prev').addEventListener('click',()=>show(active-1));
  document.getElementById('hero-next').addEventListener('click',()=>show(active+1));
  document.getElementById('hero-toggle').addEventListener('click',e=>{playing=!playing;e.currentTarget.textContent=playing?'Ⅱ':'▶';e.currentTarget.setAttribute('aria-label',playing?'Pause video':'Play video');show(active)});
  show(0);
  const menu=document.getElementById('mobile-menu'),scrim=document.getElementById('menu-scrim');
  function toggleMenu(open){menu.classList.toggle('open',open);scrim.classList.toggle('open',open);document.body.style.overflow=open?'hidden':'';}
  document.getElementById('open-menu').addEventListener('click',()=>toggleMenu(true));
  document.getElementById('close-menu').addEventListener('click',()=>toggleMenu(false));
  scrim.addEventListener('click',()=>toggleMenu(false));
  document.addEventListener('keydown',e=>{if(e.key==='Escape')toggleMenu(false)});
  const rail=document.getElementById('sport-rail');
  document.getElementById('rail-prev').addEventListener('click',()=>rail.scrollBy({left:-rail.firstElementChild.clientWidth-12,behavior:'smooth'}));
  document.getElementById('rail-next').addEventListener('click',()=>rail.scrollBy({left:rail.firstElementChild.clientWidth+12,behavior:'smooth'}));
})();
</script>'''
    html = head + nav + menu + '<main>' + hero() + studio + duo + acg + sports + '<div class="bottom-brand"><img src="' + A + 'bottom-wordmark.webp" alt="Nike. Just Do It."></div>' + merch() + '</main>' + footer + script + '</body></html>\n'
    target = ROOT / 'nike.html'
    target.write_text(html)
    print(f'Wrote {target} ({target.stat().st_size} bytes)')


if __name__ == '__main__':
    main()
