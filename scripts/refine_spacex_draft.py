#!/usr/bin/env python3
"""Build a dated SpaceX home-page study from observed first-party content/media."""

from __future__ import annotations

from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / '.stitch-work' / 'current-official'
ASSET = 'spacex-assets/'
VIDEO = 'https://sxcontent9668.azureedge.us/cms-assets/assets/'

SECTIONS = (
    {
        'id': 'mars', 'side': 'left', 'title': 'MAKING LIFE MULTIPLANETARY',
        'copy': 'SpaceX was founded under the belief that a future where humanity is out exploring the stars is fundamentally more exciting than one where we are not.',
        'button': 'EXPLORE', 'href': 'https://www.spacex.com/humanspaceflight/mars',
        'desktop': 'Mars_Web_8fafe15a48.jpg', 'mobile': 'Mars_Mobile_9924bba7c2.jpg',
        'video': 'Mars_Rotation_Web_HB_d96299f9de.mp4',
    },
    {
        'id': 'starship', 'side': 'right', 'title': 'REVOLUTIONIZING SPACE TECHNOLOGY',
        'copy': 'SpaceX’s Starship spacecraft and Super Heavy rocket is a fully reusable transportation system designed to carry both crew and cargo to Earth orbit, the Moon, Mars, and beyond.',
        'button': 'LEARN MORE', 'href': 'https://www.spacex.com/vehicles/starship',
        'desktop': 'Revolutionizing_Space_Tech_Desktop_ec67ad03c2.jpg',
        'mobile': 'Revolutionizing_Space_Tech_Mobile_45093b17b7.jpg',
    },
    {
        'id': 'launch', 'side': 'left', 'title': 'WORLD’S LEADING LAUNCH SERVICE PROVIDER',
        'copy': 'SpaceX leads the world in launches with its reliable, reusable rockets and is developing the fully and rapidly reusable rockets necessary to transform humanity’s ability to access space into something as routine as air travel.',
        'button': 'RESERVE YOUR RIDE', 'href': 'https://www.spacex.com/rideshare',
        'desktop': 'Leading_Launch_Service_Desktop_06a98ac534.jpg',
        'mobile': 'Leading_Launch_Service_Mobile_02_41fdea4331.jpg',
        'video': 'Space_X_Falcon_Heavy_UAS_Landing_DESKTOP_compress_b4568daf9c_5e2026727a.mp4',
    },
    {
        'id': 'human', 'side': 'right', 'title': 'ADVANCING HUMAN SPACEFLIGHT',
        'copy': 'Since returning human spaceflight capabilities to the United States in 2020, SpaceX is helping build a new era where not just hundreds of people, but thousands and ultimately millions will be able to explore space.',
        'button': 'JOIN A MISSION', 'href': 'https://www.spacex.com/humanspaceflight',
        'desktop': 'Advancing_Human_Spaceflight_Desktop_61c8ba1c67.jpg',
        'mobile': 'Advancing_Human_Spaceflight_Mobile_af242fde31.jpg',
    },
    {
        'id': 'starlink', 'side': 'left', 'title': 'DELIVERING HIGH-SPEED INTERNET FROM SPACE',
        'copy': 'Starlink is the world’s most advanced satellite constellation in low-Earth orbit, delivering reliable broadband internet capable of supporting streaming, online gaming, video calls, and more.',
        'button': 'ORDER NOW', 'href': 'https://www.starlink.com/',
        'desktop': 'Delivering_Highspeed_Desktop_d50314640c.jpg',
        'mobile': 'Delivering_Highspeed_Mobile_86f0698604.jpg',
        'video': 'Starlink_12_10_20250428_Deploy_website_DESKTOP_14fe7e072c.mp4',
    },
    {
        'id': 'compute', 'side': 'right', 'title': 'DEVELOPING ORBITAL AI COMPUTE',
        'copy': 'SpaceX is the only vertical integrated company capable of developing a truly scalable solution for the future of AI.',
        'button': 'STARMIND', 'href': 'https://www.spacex.com/spacexai/starmind',
        'desktop': 'home_hero_ba20d17dfc.webp', 'mobile': 'home_hero_ba20d17dfc.webp',
    },
)

NAV = (
    ('VEHICLES', (
        ('Starship', 'https://www.spacex.com/vehicles/starship'),
        ('Dragon', 'https://www.spacex.com/vehicles/dragon'),
        ('Falcon 9', 'https://www.spacex.com/vehicles/falcon-9'),
        ('Falcon Heavy', 'https://www.spacex.com/vehicles/falcon-heavy'),
    )),
    ('HUMAN SPACEFLIGHT', (
        ('Overview', 'https://www.spacex.com/humanspaceflight/overview'),
        ('Space Station', 'https://www.spacex.com/humanspaceflight/iss'),
        ('Earth Orbit', 'https://www.spacex.com/humanspaceflight/earth'),
        ('The Moon', 'https://www.spacex.com/humanspaceflight/moon'),
        ('Mars & Beyond', 'https://www.spacex.com/humanspaceflight/mars'),
    )),
    ('STARLINK', 'https://www.starlink.com/'),
    ('STARSHIELD', 'https://www.spacex.com/starshield'),
    ('SPACEXAI', (
        ('AI Satellite', 'https://www.spacex.com/spacexai/starmind'),
        ('Grok', 'https://x.ai/'), ('Grokipedia', 'https://grokipedia.com/'),
        ('X', 'https://x.com/'),
    )),
    ('TERAFAB', 'https://terafab.ai/'),
    ('COMPANY', (
        ('Mission', 'https://www.spacex.com/mission'),
        ('Careers', 'https://www.spacex.com/careers'),
        ('Sites', 'https://www.spacex.com/sites'),
        ('Updates', 'https://www.spacex.com/updates'),
        ('Content', 'https://www.spacex.com/content'),
        ('Investor Relations', 'https://ir.spacex.com/'),
    )),
    ('SHOP', (
        ('SpaceX Shop', 'https://shop.spacex.com/'),
        ('xAI Shop', 'https://shop.x.com/'),
    )),
)


def link(text: str, href: str, css_class: str = '') -> str:
    return (f'<a class="{css_class}" href="{escape(href, quote=True)}">'
            f'{escape(text)}</a>')


def media(desktop: str, mobile: str, video: str | None = None) -> str:
    visual = ('<picture class="background-picture"><source media="(max-width:767px)" srcset="'
              + ASSET + mobile + '"><img src="' + ASSET + desktop + '" alt="" loading="lazy"></picture>')
    if video:
        visual += ('<video class="background-video" muted loop playsinline preload="none" poster="'
                   + ASSET + desktop + '" data-mobile-poster="' + ASSET + mobile + '">'
                   '<source src="' + VIDEO + video + '" type="video/mp4"></video>')
    return visual


def panel(item: dict) -> str:
    return (f'<section class="panel panel-{item["id"]} {item["side"]}" id="{item["id"]}">'
            + media(item['desktop'], item['mobile'], item.get('video'))
            + '<div class="panel-shade"></div><div class="panel-content">'
            + f'<h2>{escape(item["title"])}</h2><p>{escape(item["copy"])}</p>'
            + link(item['button'] + '　→', item['href'], 'outline-button')
            + '</div></section>')


def header() -> str:
    nav = []
    for title, value in NAV:
        if isinstance(value, str):
            nav.append(link(title, value, 'nav-link'))
        else:
            nav.append('<details class="nav-group"><summary>' + title + '</summary><div class="submenu">'
                       + ''.join(link(label, href) for label, href in value) + '</div></details>')
    upcoming = ('<details class="upcoming"><summary>UPCOMING LAUNCHES <span>⌄</span></summary>'
                '<div class="upcoming-list"><a href="https://www.spacex.com/launches/starship-flight-14">'
                '<img src="' + ASSET + '20260511_Wet_Dress_Actual_4_600x600_2efaf3e3dc.jpg" alt="">'
                '<span>Starship Flight 14<small>September 28, 2026 · 20:15 Taiwan Time</small></span><b>→</b></a>'
                '<a href="https://www.spacex.com/launches"><img src="' + ASSET + 'crew_12_MOBILE_template1_f0071d661e.jpg" alt="">'
                '<span>Crew-13 Mission<small>October 1, 2026 · 23:10 Taiwan Time</small></span><b>→</b></a>'
                + link('ALL UPCOMING LAUNCHES', 'https://www.spacex.com/launches', 'all-launches') + '</div></details>')
    return ('<header class="site-header" id="site-header"><a class="brand" href="https://www.spacex.com/" aria-label="SpaceX home">'
            '<img src="' + ASSET + 'spacex-wordmark.svg" alt="SpaceX"></a>'
            '<nav class="primary-nav" id="primary-nav" aria-label="SpaceX navigation">'
            + ''.join(nav) + upcoming + '</nav>'
            '<button id="menu-toggle" class="menu-toggle" type="button" aria-label="Open navigation" aria-expanded="false">'
            '<span></span><span></span><span></span></button></header>')


def footer() -> str:
    items = (
        ('CAREERS', 'https://www.spacex.com/careers'),
        ('UPDATES', 'https://www.spacex.com/updates'),
        ('PRIVACY POLICY', 'https://www.spacex.com/assets/media/privacy_policy_spacex.pdf'),
        ('SUPPLIERS', 'https://www.spacex.com/supplier'),
        ('INVESTORS', 'https://ir.spacex.com/'),
    )
    return ('<footer class="site-footer"><div class="footer-links">'
            + ''.join(link(text, href) for text, href in items)
            + '</div><span>© 2026 SPACEX</span>'
            + link('𝕏', 'https://x.com/SpaceX', 'social-x') + '</footer>')


def main() -> None:
    style = '''
@font-face{font-family:DDIN;src:url('spacex-assets/D-DIN.e58c68e58b09fc0e.woff2') format('woff2');font-style:normal;font-weight:400;font-display:swap}
@font-face{font-family:DDIN;src:url('spacex-assets/D-DIN-Bold.9a5ce67e997fd030.woff2') format('woff2');font-style:normal;font-weight:700;font-display:swap}
@font-face{font-family:RobotoMono;src:url('spacex-assets/RobotoMono.19b5beb679797c73.ttf') format('truetype');font-style:normal;font-weight:400;font-display:swap}
*{box-sizing:border-box}html{scroll-behavior:smooth}html,body{margin:0;background:#000;color:#f0f0fa}body{font:16px/1.5 DDIN,Arial,sans-serif}a{color:inherit;text-decoration:none}a:hover{text-decoration:underline}button,summary{cursor:pointer}a:focus-visible,button:focus-visible,summary:focus-visible{outline:2px solid #fff;outline-offset:4px}img,video{display:block;max-width:100%}
.site-header{height:76px;position:fixed;top:0;left:0;right:0;z-index:30;display:flex;align-items:center;gap:30px;padding:0 40px;color:#f0f0fa;background:linear-gradient(#0009,#0000);font:700 13px/1 DDIN,Arial,sans-serif;letter-spacing:.09em}.brand{width:147px;flex:none}.brand img{width:147px;height:19px}.primary-nav{display:flex;align-items:center;gap:27px;min-width:0;flex:1}.primary-nav>a,.nav-group>summary{white-space:nowrap}.nav-group{position:relative}.nav-group>summary{list-style:none}.nav-group>summary::-webkit-details-marker{display:none}.submenu{display:none;position:absolute;top:28px;left:-16px;width:max-content;min-width:180px;background:#111e;padding:12px 0;flex-direction:column;border:1px solid #ffffff44}.nav-group[open] .submenu{display:flex}.submenu a{padding:12px 18px;text-transform:uppercase}.submenu a:hover{background:#ffffff22}.upcoming{position:relative;margin-left:auto;min-width:200px}.upcoming summary{height:34px;border:1px solid #ffffff5d;border-radius:4px;padding:0 10px;display:flex;align-items:center;justify-content:space-between;font-size:10px;list-style:none;white-space:nowrap}.upcoming summary::-webkit-details-marker{display:none}.upcoming-list{display:none;position:absolute;right:0;top:40px;width:330px;background:#080808;border:1px solid #ffffff35;padding:16px;box-shadow:0 12px 28px #0008}.upcoming[open] .upcoming-list{display:block}.upcoming-list>a:not(.all-launches){display:flex;align-items:center;gap:10px;padding:12px 0;border-bottom:1px solid #333;font-size:13px;letter-spacing:0;text-transform:none}.upcoming-list img{width:54px;height:54px;object-fit:cover;border-radius:5px}.upcoming-list small{display:block;color:#bbb;font-size:10px;font-weight:400;margin-top:5px}.upcoming-list b{font-size:18px;margin-left:auto}.all-launches{display:block;text-align:center;padding:18px 0 5px;font-size:11px}.menu-toggle{display:none}
.hero,.panel{position:relative;overflow:hidden;background:#000}.hero{height:100vh;height:100svh;min-height:650px}.panel{height:max(100vh,73.52vw);min-height:720px}.background-picture,.background-video,.background-picture img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}.background-video{max-width:none}.background-picture img{max-width:none}.hero>.background-video{z-index:1}.hero::after{content:'';position:absolute;z-index:2;inset:0;background:linear-gradient(0deg,#000e 0%,#0005 21%,transparent 55%,#0002 100%);pointer-events:none}.hero-content{position:absolute;z-index:3;left:60px;bottom:108px;width:min(640px,calc(100% - 120px))}.countdown{font:400 14px/1.4 RobotoMono,monospace;letter-spacing:.03em}.hero h1{font:700 60px/.9 DDIN,Arial,sans-serif;text-transform:uppercase;margin:0 0 50px;letter-spacing:.01em}.outline-button{display:inline-flex;align-items:center;justify-content:center;min-width:104px;height:50px;border:1px solid #ffffff85;border-radius:3px;padding:0 20px;font:400 12px/1 DDIN,Arial,sans-serif;white-space:nowrap;transition:background .2s,color .2s}.outline-button:hover{background:#fff;color:#000;text-decoration:none}
.panel-shade{position:absolute;z-index:2;inset:0;pointer-events:none}.panel.left .panel-shade{background:linear-gradient(90deg,#0009 0%,#0006 24%,transparent 63%)}.panel.right .panel-shade{background:linear-gradient(270deg,#0009 0%,#0004 35%,transparent 70%)}.panel-content{position:absolute;z-index:3;top:122px;width:450px}.panel.left .panel-content{left:max(40px,calc((100% - 1080px)/2))}.panel.right .panel-content{right:max(40px,calc((100% - 1080px)/2))}.panel h2{font:700 48px/1.25 DDIN,Arial,sans-serif;text-transform:uppercase;margin:0;max-width:450px}.panel.left h2{line-height:1;max-width:405px}.panel p{font:400 16px/24px DDIN,Arial,sans-serif;max-width:416px;margin:16px 0 30px}.panel-mars .panel-content{top:273px}.panel-mars h2{font-size:80px;line-height:.95}.panel-starlink .panel-content{top:315px}.panel-launch h2,.panel-starlink h2{line-height:1}.panel .outline-button{margin-top:0}
.site-footer{min-height:72px;background:#000;padding:18px 35px;display:flex;align-items:center;justify-content:flex-end;gap:40px;font-size:11px}.footer-links{display:flex;gap:20px}.site-footer span{color:#aaa}.social-x{display:grid;place-items:center;border-radius:50%;background:#101010;width:44px;height:44px;font-size:22px}
@media(max-width:1200px) and (min-width:768px){.site-header{gap:16px;padding:0 24px}.primary-nav{gap:14px;font-size:11px}.brand,.brand img{width:130px}.upcoming{min-width:170px}.panel-content{width:40%}.panel.right .panel-content{right:5%}.panel.left .panel-content{left:5%}}
@media(max-width:767px){.site-header{height:64px;padding:0 16px;gap:0;background:linear-gradient(#0008,#0000)}.brand,.brand img{width:120px}.brand img{height:auto}.menu-toggle{display:flex;flex-direction:column;justify-content:center;gap:5px;width:24px;height:40px;border:0;background:transparent;margin-left:auto;padding:0}.menu-toggle span{width:24px;height:1px;background:#fff;transition:transform .2s,opacity .2s}body.nav-open .site-header{background:#000}body.nav-open .menu-toggle span:nth-child(1){transform:translateY(6px) rotate(45deg)}body.nav-open .menu-toggle span:nth-child(2){opacity:0}body.nav-open .menu-toggle span:nth-child(3){transform:translateY(-6px) rotate(-45deg)}.primary-nav{display:none;position:fixed;inset:0;z-index:-1;background:#000;overflow-y:auto;padding:75px 16px 25px;flex-direction:column;align-items:stretch;gap:0;font-size:18px;letter-spacing:.045em}body.nav-open .primary-nav{display:flex}.primary-nav>a,.nav-group>summary{display:block;padding:15px 0}.nav-group>summary:after{content:'⌄';margin-left:5px;font-size:14px}.submenu{position:static;display:none;width:100%;background:transparent;border:0;box-shadow:none;padding:0 0 10px 18px}.nav-group[open] .submenu{display:flex}.submenu a{padding:8px 0;font-size:14px}.upcoming{margin:24px 0 0;min-width:0}.upcoming summary{border:0;padding:0;height:44px;font-size:18px;justify-content:flex-start;gap:4px}.upcoming-list{position:static;display:block;border:0;padding:0;box-shadow:none;width:100%;background:transparent}.upcoming-list>a:not(.all-launches){padding:14px 0;font-size:14px}.upcoming-list img{width:64px;height:64px}.upcoming-list small{font-size:11px}.hero{height:100svh;min-height:700px}.hero::after{background:linear-gradient(0deg,#000f 0%,#0006 23%,transparent 60%,#0002 100%)}.hero-content{left:16px;bottom:42px;width:calc(100% - 32px)}.hero h1{font-size:60px;line-height:.9;max-width:350px;margin:0 0 50px}.countdown{font-size:13px}.panel{height:100svh;min-height:700px}.panel-content,.panel.left .panel-content,.panel.right .panel-content{left:20px;right:20px;top:auto;bottom:30px;width:auto}.panel h2,.panel.left h2,.panel-mars h2{font-size:38px;line-height:.98;max-width:350px}.panel p{font-size:16px;line-height:25px;margin:10px 0 18px;max-width:355px}.panel-shade,.panel.left .panel-shade,.panel.right .panel-shade{background:linear-gradient(0deg,#000d 0%,#0008 28%,transparent 72%)}.panel .background-video{display:none}.panel-mars{margin-bottom:376px}.site-footer{height:132px;min-height:0;padding:15px 16px;display:flex;flex-direction:column;gap:10px;justify-content:center}.footer-links{flex-wrap:wrap;justify-content:center;gap:10px;font-size:10px}.site-footer span{font-size:10px}.social-x{display:none}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}.background-video{display:none}}
'''
    hero = ('<section class="hero" id="hero">'
            + media('starship-flight-14-poster.jpg', 'starship-flight-14-poster.jpg',
                    '20260924_FL_14_Wet_Dress_15_cf0c5812e6.mp4')
            + '<div class="hero-content"><div class="countdown" id="countdown" aria-label="Time from scheduled Starship Flight 14 launch">T-08:42:29</div>'
              '<h1>STARSHIP FLIGHT 14</h1>'
            + link('WATCH　→', 'https://www.spacex.com/launches/starship-flight-14', 'outline-button')
            + '</div></section>')
    script = '''<script>
(() => {
  const toggle=document.getElementById('menu-toggle');
  const nav=document.getElementById('primary-nav');
  function menu(open){document.body.classList.toggle('nav-open',open);toggle.setAttribute('aria-expanded',String(open));toggle.setAttribute('aria-label',open?'Close navigation':'Open navigation');document.body.style.overflow=open?'hidden':''}
  toggle.addEventListener('click',()=>menu(!document.body.classList.contains('nav-open')));
  nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>menu(false)));
  document.addEventListener('keydown',e=>{if(e.key==='Escape')menu(false)});
  const launch=Date.parse('2026-09-28T12:15:00Z');
  const clock=document.getElementById('countdown');
  function tick(){const difference=Math.floor((launch-Date.now())/1000),seconds=Math.abs(difference);const h=Math.floor(seconds/3600),m=Math.floor(seconds/60)%60,s=seconds%60;clock.textContent=`T${difference>=0?'-':'+'}${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`}
  tick();setInterval(tick,1000);
  const videos=[...document.querySelectorAll('.background-video')];
  function posters(){videos.forEach(v=>{const next=innerWidth<768?v.dataset.mobilePoster:v.previousElementSibling.querySelector('img').getAttribute('src');if(v.getAttribute('poster')!==next)v.setAttribute('poster',next)})}
  posters();addEventListener('resize',posters,{passive:true});
  if(!matchMedia('(prefers-reduced-motion: reduce)').matches){
    const watcher=new IntersectionObserver(entries=>entries.forEach(entry=>{const v=entry.target;if(entry.isIntersecting){v.play().catch(()=>{})}else v.pause()}),{threshold:.05});
    videos.forEach(v=>watcher.observe(v));
  }
})();
</script>'''
    html = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>SpaceX · 2026-09-28 Homepage Study</title>'
            '<meta name="description" content="Dated unofficial study of the SpaceX public homepage.">'
            '<style>' + style + '</style></head><body>'
            + header() + '<main>' + hero + ''.join(panel(item) for item in SECTIONS)
            + '</main>' + footer() + script + '</body></html>\n')
    target = ROOT / 'spacex.html'
    target.write_text(html)
    print(f'Wrote {target} ({target.stat().st_size} bytes)')


if __name__ == '__main__':
    main()
