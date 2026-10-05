#!/usr/bin/env python3
"""Build a dated Uber visual study from the observed public DOM, not live services."""
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / '.stitch-work/current-official'
BASE = 'https://www.uber.com/ca/en/'
CDN = 'https://tb-static.uber.com/prod/udam-assets/'
LOGIN = 'https://auth.uber.com/login-redirect?next_url=https://www.uber.com'

ASSETS = {
    'essentials': CDN+'b1902ed8-4af1-421a-beb4-bdc8a5c2e59b.svg',
    'account': CDN+'850e6b6d-a29e-4960-bcab-46de99547d24.svg',
    'reserve': CDN+'5152cc71-a5b0-4fbd-aeb8-bee896efcd48.png',
    'ride': 'https://mobile-content.uber.com/launch-experience/nava-icons-may-2026/light-mode/Sedan-160-temp.png',
    'schedule': 'https://cn-geo1.uber.com/static/mobile-content/launch-experience/nava-icons-may-2026/light-mode/Calendar-351-temp.png',
    'courier': 'https://cn-geo1.uber.com/static/mobile-content/Courier.png',
    'food': 'https://d4p17acsd5wyj.cloudfront.net/shortcuts/restaurants.png',
    'grocery': 'https://d4p17acsd5wyj.cloudfront.net/shortcuts/uber_grocery.png',
    'travel': 'https://cn-geo1.uber.com/image-proc/crop/resizecrop/udam/format=auto/width=1116/height=744/srcb64=aHR0cHM6Ly90Yi1zdGF0aWMudWJlci5jb20vcHJvZC91ZGFtLWFzc2V0cy9hMDU4OGFmZS0wNjFlLTQ3OWQtYjczMC00ZGQ4NzJjZTM4NTIucG5n',
    'driver': 'https://cn-geo1.uber.com/image-proc/crop/resizecrop/udam/format=auto/width=1152/height=1152/srcb64=aHR0cHM6Ly90Yi1zdGF0aWMudWJlci5jb20vcHJvZC91ZGFtLWFzc2V0cy85NjRkZDNkMS05NGU3LTQ4MWUtYjI4Yy0wOGQ1OTM1M2I5ZTAucG5n',
    'business': 'https://cn-geo1.uber.com/image-proc/crop/resizecrop/udam/format=auto/width=1152/height=1152/srcb64=aHR0cHM6Ly90Yi1zdGF0aWMudWJlci5jb20vcHJvZC91ZGFtLWFzc2V0cy83NmJhZjFlYS0zODVhLTQwOGMtODQ2Yi01OTIxMTA4NjE5NmMucG5n',
    'rider_qr': 'https://cn-geo1.uber.com/image-proc/crop/resizecrop/udam/format=auto/width=552/height=552/srcb64=aHR0cHM6Ly90Yi1zdGF0aWMudWJlci5jb20vcHJvZC91ZGFtLWFzc2V0cy9hNTk5ODZhZC0wZDlmLTQzOTYtODUzOS0zODliY2U5N2Y1NzkucG5n',
    'driver_qr': 'https://cn-geo1.uber.com/image-proc/crop/resizecrop/udam/format=auto/width=552/height=552/srcb64=aHR0cHM6Ly90Yi1zdGF0aWMudWJlci5jb20vcHJvZC91ZGFtLWFzc2V0cy9jODQ2NmEyNy1kMzBjLTUxNGEtOTZmMi1lMDlmMThmYWY4MDYucG5n',
    'rider_app': CDN+'e24f1914-1e23-4896-ad77-22e88c37c2f9.svg',
    'driver_app': CDN+'480eb066-2389-442c-b0f7-1cdcaa68a649.svg',
}
SERVICES = [
    ('Ride', 'Go anywhere with Uber. Request a ride, hop in, and go.', 'ride', 'https://m.uber.com/looking/'),
    ('Reserve', 'Reserve your ride in advance so you can relax on the day of your trip.', 'schedule', 'https://m.uber.com/reserve/'),
    ('Courier', 'Uber makes same-day item delivery easier than ever.', 'courier', 'https://m.uber.com/go/connect/pickup'),
    ('Food', 'Order delivery from local restaurants with Uber Eats.', 'food', 'https://www.ubereats.com/'),
    ('Grocery', 'Get groceries delivered to your door with Uber Eats.', 'grocery', 'https://www.ubereats.com/feeds/shop_feed'),
]
FOOTER = {
    'Company': [('About us',BASE+'about/'),('Our offerings',BASE+'about/uber-offerings/'),('Newsroom',BASE+'newsroom/'),('Investors','https://investor.uber.com/'),('Blog',BASE+'blog/'),('Careers','https://jobs.uber.com/en/'),('Uber One',BASE+'uber-one/')],
    'Products': [('Ride',BASE+'ride/'),('Drive',BASE+'drive/'),('Deliver',BASE+'deliver/'),('Eat','https://www.ubereats.com/'),('Uber for Business',BASE+'business/'),('Uber Freight','https://www.uberfreight.com/'),('Gift cards',BASE+'gift-cards/'),('Uber Health','https://www.uberhealth.com/ca/en/'),('Uber Advertising',BASE+'advertising/'),('Merchants','https://merchants.ubereats.com/ca/en/')],
    'Global citizenship': [('Safety',BASE+'safety/'),('Sustainability',BASE+'about/sustainability/')],
    'Travel': [('Reserve','https://m.uber.com/reserve'),('Airports',BASE+'airports/'),('Hotels',BASE+'hotels/'),('Cities',BASE+'r/cities/')],
}

CSS = '''
@font-face{font-family:UberMove;src:url("uber-assets/UberMove-Bold.woff2") format("woff2");font-weight:700;font-display:swap}
@font-face{font-family:UberMove;src:url("uber-assets/UberMove-Regular.woff2") format("woff2");font-weight:400;font-display:swap}
@font-face{font-family:UberMoveText;src:url("uber-assets/UberMoveText-Medium.woff2") format("woff2");font-weight:500;font-display:swap}
@font-face{font-family:UberMoveText;src:url("uber-assets/UberMoveText-Regular.woff2") format("woff2");font-weight:400;font-display:swap}
*{box-sizing:border-box}body{margin:0;color:#000;background:#fff;font-family:UberMoveText,Arial,sans-serif;font-size:16px;line-height:24px}
[hidden]{display:none!important}a{color:inherit;text-decoration:none}button,input,select{font:inherit}button,a,input,select{outline-offset:4px}button{cursor:pointer;border:0}img{display:block;max-width:100%}h1,h2,h3,h4,p{margin:0}h1,h2,h3{font-family:UberMove,Arial,sans-serif;font-weight:700}h1{font-size:52px;line-height:64px}h2{font-size:36px;line-height:44px}h3{font-size:24px;line-height:32px}h4{font-size:18px;line-height:24px;font-weight:500}
.wrap{max-width:1280px;margin:auto;padding-left:64px;padding-right:64px}.header{height:64px;background:#000;color:#fff}.header .wrap{height:64px;display:flex;align-items:center;gap:28px}.wordmark{font-family:UberMove,sans-serif;font-size:24px;line-height:28px;font-weight:400}.header-links,.header-right{display:flex;align-items:center;gap:24px;font-size:14px;font-weight:500}.header-right{margin-left:auto;gap:20px}.header button{background:transparent;color:inherit;padding:8px 0}.header .signup{border-radius:24px;background:#fff;color:#000;padding:10px 16px}.menu-toggle{display:none}.nav-panel{position:absolute;top:64px;right:64px;z-index:10;min-width:220px;background:#fff;color:#000;border:1px solid #ddd;padding:20px;box-shadow:0 8px 30px #0002}.nav-panel a{display:block;padding:8px}.skip{position:absolute;left:20px;top:-100px}.skip:focus{top:8px;z-index:20;background:white;padding:8px}
.hero{padding-top:64px;padding-bottom:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:36px;min-height:523px}.hero-copy{width:459px;max-width:100%}.city{height:24px;display:flex;align-items:center;gap:8px;margin-bottom:8px}.city svg{width:20px;height:20px}.city a{font-size:14px;border-bottom:1px solid #aaa}.hero h1{margin-bottom:16px}.pickup-now{height:48px;display:flex;align-items:center;gap:8px;border-radius:30px;background:#f3f3f3;padding:0 16px;margin-bottom:24px;font-size:16px;font-weight:500}.pickup-now svg{width:20px;height:20px}.route-form{width:396px;max-width:100%;position:relative}.route-fields{position:relative;display:grid;gap:16px}.route-line{position:absolute;top:28px;left:25px;width:1px;height:72px;background:#000;z-index:1}.route-field{display:flex;align-items:center;height:56px;background:#f3f3f3;border-radius:8px;position:relative}.route-field input{background:none;border:0;outline:none;padding:16px 42px 16px 52px;width:100%;height:56px;color:#000}.route-field input::placeholder{color:#5e5e5e;opacity:1}.route-marker{position:absolute;left:21px;top:23px;z-index:2;width:9px;height:9px;background:#000;border:2px solid #fff;box-shadow:0 0 0 1px #000}.route-marker.round{border-radius:50%}.location-link{position:absolute;right:14px;top:16px;line-height:24px}.route-actions{margin-top:16px;display:flex;align-items:center;gap:24px;width:500px;max-width:calc(100vw - 128px)}.cta{display:inline-flex;align-items:center;justify-content:center;white-space:nowrap;border-radius:8px;background:#000;color:#fff;min-height:48px;padding:12px 25px;font-weight:500}.cta:hover{background:#333}.underlined{border-bottom:1px solid #aaa;padding-bottom:5px}.hero-art{position:relative;align-self:start;width:459px;max-width:100%}.hero-art>img{width:100%;aspect-ratio:1}.travel-overlay{position:absolute;left:18px;right:18px;bottom:18px;background:#fff;border-radius:8px;padding:16px;display:flex;align-items:center;justify-content:space-between}.travel-overlay span{font-weight:500}.travel-overlay a{background:#f3f3f3;border-radius:8px;padding:12px 16px;font-weight:500;font-size:14px}
.explore{padding-top:64px;padding-bottom:32px}.explore h2{margin-bottom:29.875px}.service-grid{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px 16px}.service-tile{background:#f3f3f3;border-radius:8px;padding:16px;min-height:166px;display:flex;position:relative}.service-tile .text{padding-right:128px;width:100%}.service-tile strong{font-size:16px;font-weight:500}.service-tile p{font-size:12px;line-height:20px;margin:8px 0 16px}.service-tile .details{display:inline-block;border-radius:24px;background:#fff;padding:8px 12px;font-size:12px;line-height:16px;font-weight:500}.service-tile img{position:absolute;right:16px;top:16px;width:128px;height:128px;object-fit:contain}.service-tile:hover{background:#e8e8e8}
.feature{padding-top:64px;padding-bottom:64px;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:36px;align-items:center}.feature .copy{width:459px;max-width:100%}.feature p{margin-top:24px}.feature .actions{display:flex;align-items:center;gap:24px;flex-wrap:wrap;margin-top:32px}.feature>img{width:100%;aspect-ratio:3/2;object-fit:cover}.feature.driver>img,.feature.business>img{aspect-ratio:1}.feature.driver .copy{margin-left:auto;grid-column:2;grid-row:1}.feature.driver>img{grid-column:1;grid-row:1}.account .copy{padding-top:0}.plan{padding-top:0;padding-bottom:64px}.plan>h2{margin:29.875px 0 36px}.reserve-grid{display:grid;grid-template-columns:2fr 1fr;gap:36px}.reserve-card{border-radius:12px;background:#9cc7d1;background-image:var(--reserve);background-position:right center;background-repeat:no-repeat;background-size:auto 100%;min-height:404px;padding:36px;overflow:hidden}.reserve-content{max-width:360px}.reserve-card h3{font-size:36px;line-height:44px;margin:36px 0}.reserve-card h4{margin:24px 0 8px}.date-row{display:grid;grid-template-columns:1fr 1fr;gap:8px}.date-row label{font-size:12px;line-height:20px}.date-row input{width:100%;height:48px;margin-top:4px;border:0;border-radius:8px;background:#fff;padding:12px;font-size:14px}.reserve-card .cta{width:100%;margin-top:16px}.benefits{border:1px solid #eee;border-radius:12px;padding:12px}.benefits h3{font-size:20px;line-height:28px;margin-bottom:20px}.benefits ul{margin:0;padding:0;list-style:none}.benefits li{display:flex;gap:24px;align-items:center;padding:16px 0;border-bottom:1px solid #eee}.benefits img{height:24px;width:24px;flex-shrink:0}.benefits p{font-size:16px;line-height:24px}.benefits .underlined{display:inline-block;margin-top:16px;color:#6b6b6b}.city-choice{margin-top:32px;background:#f3f3f3;border-radius:8px;padding:12px 16px;height:48px;display:inline-flex;align-items:center;gap:12px;font-weight:500}.city-choice svg{width:20px;height:20px}.apps{background:#f6f6f6;padding:64px 0}.apps h2{margin-bottom:36px}.app-grid{display:grid;grid-template-columns:1fr 1fr;gap:36px}.app-card{display:flex;align-items:center;gap:24px;background:#fff;border:1px solid #eee;padding:24px}.app-card .qr{width:150px;height:150px}.app-card .app-icon{display:none}.app-card p{margin-top:0}.app-card .arrow{font-size:28px;margin-left:auto}.app-card h3{font-size:24px;line-height:32px}.footer{background:#000;color:#fff;padding:64px 0 24px;font-size:14px;line-height:20px}.footer .wordmark{display:inline-block;margin-bottom:32px}.help-link{display:block;margin-bottom:40px}.registration{margin-bottom:64px;font-size:14px;line-height:20px}.footer-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:36px}.footer h2{font-family:UberMoveText,sans-serif;font-weight:500;font-size:18px;line-height:24px;margin-bottom:20px}.footer ul{list-style:none;margin:0;padding:0;display:grid;gap:16px}.footer a:hover{color:#aaa}.footer-toolbar{display:flex;align-items:center;justify-content:space-between;margin:64px 0}.social{display:flex;gap:64px}.social svg{width:16px;height:16px}.locale{display:flex;gap:24px}.locale a{display:flex;align-items:center;gap:8px}.store-links{display:flex;gap:12px}.store-links a{display:flex;align-items:center;gap:6px;border:1px solid #777;border-radius:6px;padding:4px 10px;font:14px/16px UberMoveText,sans-serif}.store-links small{font-size:9px;display:block}.legal{display:flex;justify-content:space-between;margin-top:64px;color:#afafaf;font-size:12px}.legal-links{display:flex;gap:32px}
@media(max-width:1023px){.wrap{padding-left:24px;padding-right:24px}.header .wrap{gap:16px}.header-links,.header-right .language,.header-right .help{display:none}.header-right{gap:20px}.menu-toggle{display:block}.nav-panel{left:0;right:0;top:64px;border:0}.hero{display:block;padding-top:48px;min-height:0}.hero-copy{width:100%}.city{margin-bottom:0}.hero h1{font-size:36px;line-height:44px;margin-bottom:32px}.pickup-now,.hero-art{display:none}.route-form{width:100%}.route-actions{margin-top:16px;display:flex;align-items:flex-start;flex-direction:column;gap:16px;width:100%;max-width:none}.route-actions .underlined{margin-top:0;padding-top:0;line-height:24px}.explore{padding-top:80px;padding-bottom:0}.explore h2{font-size:28px;line-height:36px;margin-bottom:24px}.service-grid{grid-template-columns:repeat(6,minmax(0,1fr));gap:24px 16px}.service-grid li{grid-column:span 2}.service-grid li:nth-child(-n+2){grid-column:span 3}.service-tile{min-height:124px;display:flex;align-items:flex-end;justify-content:center;padding:12px}.service-tile .text{padding:0;text-align:center}.service-tile strong{font-size:14px;line-height:20px}.service-tile p,.service-tile .details{display:none}.service-tile img{top:6px;left:50%;right:auto;transform:translateX(-50%);width:80px;height:80px}.service-grid li:nth-child(-n+2) .service-tile{height:124px}.feature{display:flex;flex-direction:column;align-items:stretch;padding-top:64px;padding-bottom:0;gap:48px}.feature .copy{width:100%}.feature h2{font-size:28px;line-height:36px}.feature p{margin-top:24px}.feature .actions{gap:16px;align-items:flex-start;flex-direction:column;margin-top:32px}.feature>img{width:100%}.feature.driver .copy{margin-left:0}.feature.driver>img{order:2}.plan{padding-top:64px;padding-bottom:0}.plan>h2{font-size:28px;line-height:36px;margin:0 0 36px}.reserve-grid{display:flex;flex-direction:column;gap:24px}.reserve-card{padding:24px;min-height:410px;background-size:auto 100%;background-position:75% center}.reserve-content{width:100%;max-width:270px}.reserve-card h3{font-size:28px;line-height:36px;margin:12px 0 32px;max-width:230px}.reserve-card h4{margin-top:24px}.benefits{padding:16px;border:0}.benefits h3{font-size:20px;line-height:28px}.benefits li{gap:24px}.apps{padding:64px 0;margin-top:64px}.apps h2{font-size:28px;line-height:36px;margin-bottom:36px}.app-grid{grid-template-columns:1fr;gap:24px}.app-card{padding:24px;gap:16px;min-height:132px}.app-card .qr,.app-card p{display:none}.app-card .app-icon{display:block;width:84px;height:84px}.app-card h3{font-size:24px;line-height:32px}.footer{padding-top:64px;padding-bottom:24px}.footer .wordmark{margin-bottom:32px}.registration{margin-bottom:64px}.footer-grid{grid-template-columns:1fr;gap:64px}.footer-toolbar{align-items:flex-start;flex-direction:column;gap:48px;margin-top:64px;margin-bottom:48px}.social{width:100%;justify-content:space-between;gap:0}.locale{flex-direction:column;gap:16px}.legal{flex-direction:column;gap:64px;margin-top:64px}.legal-links{gap:24px}
}
'''

# Observed responsive spacing after the original font files have loaded.
CSS += '''
.plan>h2{margin-bottom:29.875px}
.plan{padding-bottom:32px}
.reserve-grid{grid-template-columns:minmax(0,66.666667%) minmax(0,1fr);gap:24px}
.reserve-card{height:404px;min-height:404px}
.reserve-content{position:relative;margin-top:36px}
.reserve-card h3{margin-top:0}
.benefits{align-self:start}.benefits li{padding:12px 0}.benefits li:last-child{border-bottom:0}.benefits .underlined{padding-bottom:0;height:25px;min-height:25px}
.app-card{border:0}
.footer-top{position:relative;height:181.5px;margin-bottom:36px}
.footer-top .wordmark{display:block;width:calc(100% - 396px);height:112px;line-height:112px;margin:0}
.footer-top .help-link{position:absolute;top:115.5px;left:0;font-size:16px;line-height:22.5px;margin:0}
.footer-top .registration{position:absolute;top:0;right:0;width:360px;margin:0}
.footer h2{margin-top:14.9375px}.footer ul{padding-bottom:16px}
@media(max-width:1023px){
.header .signup{padding:8px 12px;font-size:14px;line-height:20px}.header .menu-toggle{font-size:20px;width:24px}
.city{font-size:14px;line-height:20px;font-weight:500}.city svg{width:12px;height:12px}
.route-actions{gap:12px}.route-actions .underlined{height:32px;min-height:32px;padding-top:4px;padding-bottom:3px;line-height:24px}
.explore{padding-top:68px;padding-bottom:20px}.explore h2{margin-bottom:23.234375px}
.service-grid{gap:16px 12px}.service-tile,.service-grid li:nth-child(-n+2) .service-tile{height:96px;min-height:96px;padding:8px}.service-tile img{top:8px;width:56px;height:56px}
.feature{padding-top:40px;padding-bottom:40px;gap:36px}.feature p{margin-top:16px}.feature .actions{gap:12px}.feature .underlined{height:32px;min-height:32px;padding-top:4px;padding-bottom:3px;line-height:24px}
.business .actions .underlined{display:none}
.plan{padding-top:0;padding-bottom:20px}.plan>h2{margin:23.234375px 0}
.reserve-card{height:356px;min-height:356px}.reserve-content{margin-top:28px;max-width:100%}.reserve-card h3{max-width:100%;margin:0 0 28px}.reserve-card h4{margin-top:24px}
.benefits{border:1px solid #eee;border-radius:12px;padding:12px}.benefits li{padding:12px 0}
.apps{padding:40px 0;margin-top:0}.apps h2{margin-bottom:36px}.app-card{padding:16px;min-height:116px}
.app-card{border:1px solid #eee}.app-grid{gap:36px}
.footer{padding-top:40px}.footer-top{height:226.5px}.footer-top .wordmark{width:100%;font-size:20px}.footer-top .registration{top:170.5px;left:0;right:auto;width:100%}.footer-grid{gap:36px}
}
'''

JS = '''
const menu=document.getElementById('nav-panel');
document.querySelectorAll('[data-menu]').forEach(b=>b.addEventListener('click',()=>{const open=menu.hidden;menu.hidden=!open;b.setAttribute('aria-expanded',String(open));}));
document.addEventListener('keydown',e=>{if(e.key==='Escape'){menu.hidden=true;document.querySelectorAll('[data-menu]').forEach(b=>b.setAttribute('aria-expanded','false'));}});
document.querySelector('[data-reserve]').addEventListener('click',()=>document.getElementById('reserve').scrollIntoView({behavior:matchMedia('(prefers-reduced-motion:reduce)').matches?'instant':'smooth'}));
'''


def a(text, url, cls=''):
    return '<a href="'+escape(url,quote=True)+'"'+(' class="'+cls+'"' if cls else '')+'>'+escape(text)+'</a>'


def img(key, alt='', cls=''):
    return '<img src="'+ASSETS[key]+'" alt="'+escape(alt,quote=True)+'"'+(' class="'+cls+'"' if cls else '')+'>'


PIN = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M19.07 2.931a10 10 0 0 0-14.14 14.14L12 24l7.07-6.93a10 10 0 0 0 0-14.14ZM12 12.5a2.5 2.5 0 1 1 0-5 2.5 2.5 0 0 1 0 5Z" fill="currentColor"/></svg>'
DOWN = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m6 9 6 6 6-6" fill="none" stroke="currentColor" stroke-width="2"/></svg>'
CLOCK = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9" fill="currentColor"/><path d="M12 6v6h5" fill="none" stroke="#fff" stroke-width="2"/></svg>'


def main():
    services=''.join('<li><a class="service-tile" href="'+url+'"><div class="text"><strong>'+label+'</strong><p>'+copy+'</p><span class="details">Details</span></div>'+img(key,label)+'</a></li>' for label,copy,key,url in SERVICES)
    footer=''.join('<div><h2>'+title+'</h2><ul>'+''.join('<li>'+a(label,url)+'</li>' for label,url in links)+'</ul></div>' for title,links in FOOTER.items())
    benefits=''.join('<li><img alt="" src="'+CDN+filename+'"><p>'+copy+'</p></li>' for filename,copy in [
        ('e12eddee-f082-49f7-a5fc-22c17977de50.svg','Choose your exact pickup time up to 90 days in advance.'),
        ('30f5ecd4-8ccf-44d0-9976-2833f69df8a9.svg','Extra wait time included to meet your ride.'),
        ('45ebda59-6a0d-41e3-a924-0dbbce078029.svg','Cancel at no charge up to 60 minutes in advance.')])
    apps=''.join('<a class="app-card" href="'+url+'">'+img(key+'_qr','','qr')+img(key+'_app','','app-icon')+'<div><h3>'+title+'</h3><p>Scan to download</p></div><span class="arrow" aria-hidden="true">→</span></a>' for key,title,url in [
        ('rider','Download the Uber app','https://rides.sng.link/Aw5zn/o42y?_dl=uber%3A%2F%2F&_smtype=3&pcn=uber-com-homepage-block'),
        ('driver','Download the Driver app','https://earn.sng.link/A3ir4p/mf0l?_dl=uberdriver%3A%2F%2F&_smtype=3&pcn=uber-com-homepage-block')])
    socials=[('linkedin','https://www.linkedin.com/company/1815218','<path d="M2 6h3v10H2zm1.5-5A1.5 1.5 0 1 0 3.5 4a1.5 1.5 0 0 0 0-3ZM7 6h3v1.5C12 4 16 6 16 10v6h-3v-6c0-2-3-2-3 0v6H7Z"/>'),('youtube','https://www.youtube.com/channel/UCgnxoUwDmmyzeigmmcf0hZA','<path d="M16 4c-.2-1-1-1-2-1H3C1 3 0 4 0 6v6c0 2 1 3 3 3h11c2 0 3-1 3-3V6l-1-2ZM7 12V6l5 3Z"/>'),('instagram','https://instagram.com/uber/','<rect x="1" y="1" width="14" height="14" rx="4" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="8" cy="8" r="3" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="4" r="1"/>'),('twitter','https://twitter.com/uber','<path d="M1 1h4l4 5 4-5h2l-5 7 6 7h-4l-4-5-4 5H1l6-7Z"/>')]
    social=''.join('<a aria-label="'+label+'" href="'+url+'"><svg viewBox="0 0 18 18" fill="currentColor" aria-hidden="true">'+svg+'</svg></a>' for label,url,svg in socials)
    html='''<!doctype html><html lang="en-CA"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Uber · Unofficial visual study</title><style>'''+CSS+'''</style></head><body>
<a class="skip" href="#main">Skip to main content</a><header class="header"><nav class="wrap" aria-label="Main navigation">'''+a('Uber',BASE,'wordmark')+'''<div class="header-links">'''+a('Ride','https://m.uber.com/looking')+a('Earn','https://drivers.uber.com/')+a('Business',BASE+'business/')+a('Uber Eats','https://www.ubereats.com/')+'''<button type="button" data-menu aria-expanded="false">About⌄</button></div><div class="header-right">'''+a('◉ EN',BASE,'language')+a('Help','https://help.uber.com/','help')+a('Log in',LOGIN)+'''<button type="button" class="signup" data-menu aria-expanded="false">Sign up</button><button type="button" class="menu-toggle" aria-label="Menu" data-menu aria-expanded="false">☰</button></div></nav><nav id="nav-panel" class="nav-panel" aria-label="More links" hidden>'''+''.join(a(label,url) for label,url in FOOTER['Company'])+a('Create an account','https://get.uber.com/sign-up')+a('Drive & deliver','https://drivers.uber.com/')+'''</nav></header>
<main id="main"><section class="hero wrap"><div class="hero-copy"><div class="city">'''+PIN+'''<span>Taipei, CA</span>'''+a('Change city',BASE+'r/cities/')+'''</div><h1>Go anywhere with Uber</h1><button class="pickup-now" type="button" data-reserve>'''+CLOCK+'''<span>Pickup now</span>'''+DOWN+'''</button><div class="route-form"><div class="route-fields"><span class="route-line" aria-hidden="true"></span><label class="route-field"><span class="route-marker round" aria-hidden="true"></span><input type="text" placeholder="Pickup location" aria-label="Pickup location" autocomplete="off"><a class="location-link" aria-label="Open pickup location on Uber" href="https://m.uber.com/looking">➤</a></label><label class="route-field"><span class="route-marker" aria-hidden="true"></span><input type="text" placeholder="Dropoff location" aria-label="Dropoff location" autocomplete="off"></label></div><div class="route-actions">'''+a('See prices','https://m.uber.com/looking','cta')+a('Log in to see your recent activity',LOGIN,'underlined')+'''</div></div></div><div class="hero-art">'''+img('essentials','essentials')+'''<div class="travel-overlay"><span>Ready to travel?</span>'''+a('Schedule ahead','https://m.uber.com/reserve')+'''</div></div></section>
<section class="explore wrap"><h2>Explore what you can do with Uber</h2><ul class="service-grid">'''+services+'''</ul></section>
<section class="feature account wrap"><div class="copy"><h2>Log in to see your account details</h2><p>View past trips, tailored suggestions, support resources, and more.</p><div class="actions">'''+a('Log in to your account',LOGIN,'cta')+a('Create an account','https://get.uber.com/sign-up','underlined')+'''</div></div>'''+img('account','signup.svg')+'''</section>
<section class="plan wrap" id="reserve"><h2>Plan for later</h2><div class="reserve-grid"><div class="reserve-card" style="--reserve:url('''+ASSETS['reserve']+''')"><div class="reserve-content"><h3>Get your ride right with Uber Reserve</h3><h4>Choose date and time</h4><div class="date-row"><label>Date<input type="date" aria-label="Select a date"></label><label>Time<input type="time" aria-label="Time"></label></div>'''+a('Next','https://m.uber.com/reserve','cta')+'''</div></div><aside class="benefits"><h3>Benefits</h3><ul>'''+benefits+'''</ul>'''+a('See terms',BASE+'ride/how-it-works/reserve/#see-prices','underlined')+'''</aside></div></section>
<section class="feature city-hub wrap"><div class="copy"><h2>Planning your next getaway?</h2><p>From weekend road trip to international destination, we've got you covered. Explore transport options, points of interest, and more with our new City Hub.</p><a class="city-choice" href="'''+BASE+'''r/cities/">'''+PIN+'''Taipei'''+DOWN+'''</a></div>'''+img('travel','Uber travel')+'''</section>
<section class="feature driver wrap"><div class="copy"><h2>Drive when you want, make what you need</h2><p>Make money on your schedule with deliveries or rides—or both. You can use your own car or choose a rental through Uber.</p><div class="actions">'''+a('Get started','https://drivers.uber.com/','cta')+a('Already have an account? Sign in','https://drivers.uber.com/','underlined')+'''</div></div>'''+img('driver','Drive when you want with Uber')+'''</section>
<section class="feature business wrap"><div class="copy"><h2>The Uber you know, reimagined for business</h2><p>Uber for Business is a platform for managing global rides and meals, and local deliveries, for companies of any size.</p><div class="actions">'''+a('Get started',BASE+'business/getting-started/','cta')+a('Check out our solutions',BASE+'business/','underlined')+'''</div></div>'''+img('business','Uber for Business')+'''</section>
<section class="apps"><div class="wrap"><h2>It’s easier in the apps</h2><div class="app-grid">'''+apps+'''</div></div></section></main>
<footer class="footer"><div class="wrap">'''+a('Uber',BASE,'wordmark')+a('Visit Help Centre','https://help.uber.com/','help-link')+'''<p class="registration">Company's registered name - Uber Formosa Co. Ltd. Taxation registration number - 83118125</p><div class="footer-grid">'''+footer+'''</div><div class="footer-toolbar"><div class="social">'''+social+'''</div><div class="locale">'''+a('◉ English',BASE)+a('Taipei',BASE+'r/cities/')+'''</div></div><div class="store-links"><a href="https://rides.sng.link/Bw5zn/vz1k?_dl=uber%3A%2F%2F&amp;pcn=uber-com-footer" aria-label="Download the Uber app on Google Play">▶<span><small>GET IT ON</small>Google Play</span></a><a href="https://rides.sng.link/Cw5zn/564k?_dl=uber%3A%2F%2F&amp;_smtype=3&amp;pcn=uber-com-footer" aria-label="Download the Uber app on the App Store">●<span><small>Download on the</small>App Store</span></a></div><div class="legal"><p>© 2026 Uber Technologies Inc.</p><div class="legal-links">'''+a('Privacy','https://www.uber.com/legal/document/?name=privacy-notice')+a('Accessibility',BASE+'about/accessibility/')+a('Terms','https://www.uber.com/legal/document/?name=general-terms-of-use')+'''</div></div></div></footer><script>'''+JS+'''</script></body></html>'''
    footer_open='<footer class="footer"><div class="wrap">'
    html=html.replace(footer_open,footer_open+'<div class="footer-top">')
    html=html.replace('<div class="footer-grid">','</div><div class="footer-grid">')
    (ROOT/'uber.html').write_text(html)
    (ROOT/'uber-browser-source.json').write_text(json.dumps({
        'observed_at':'2026-10-05','url':BASE,'method':'read_only_live_browser_dom',
        'geographic_variant':'Taipei, CA; footer Uber Formosa Co. Ltd.',
        'source_http_status':406,'source_html_available':False,
        'assets_observed':ASSETS,'services_observed':SERVICES,'footer_links_observed':FOOTER,
        'service_boundary':'Editable local fields; prices, reservations, accounts and location services open the official service. No account or ride request is submitted by this static study.'
    },ensure_ascii=False,indent=2)+'\n')
    print('Saved Uber source-aligned draft')


if __name__ == '__main__':
    main()
