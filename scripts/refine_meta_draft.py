#!/usr/bin/env python3
"""Refine genuine Stitch seeds with dated rendered Meta Canada source observations."""
import hashlib
import json
import re
from html import escape
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / '.stitch-work/current-official'
ASSETS = json.loads((WORK/'meta-asset-provenance.json').read_text())['assets']
ORIGIN = 'https://www.meta.com'

def by_url(url):
 rows=[r for r in ASSETS if r['source_url']==url]
 if len(rows)!=1: raise ValueError('Missing or ambiguous source: '+url)
 return rows[0]['path']

def media(mid):
 rows=[r for r in ASSETS if parse_qs(urlsplit(r['source_url']).query).get('media_id')==[mid]]
 if len(rows)!=1: raise ValueError('Missing or ambiguous media: '+mid)
 return rows[0]['path']

def pic(desktop,mobile,alt,cls):
 return '<picture><source media="(max-width:767px)" srcset="'+media(mobile)+'"><img class="'+cls+'" src="'+media(desktop)+'" alt="'+escape(alt,quote=True)+'"></picture>'

def link(text,url):
 if url.startswith('/'): url=ORIGIN+url
 return '<a href="'+escape(url,quote=True)+'">'+escape(text)+'</a>'

def svg(path):
 return '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path fill-rule="evenodd" clip-rule="evenodd" d="'+path+'"></path></svg>'

# Exact line paths observed in the rendered official DOM, not generator vectors.
ICONS={
 'close':'M5.707 4.293a1 1 0 1 0-1.414 1.414L10.586 12l-6.293 6.293a1 1 0 1 0 1.414 1.414L12 13.414l6.293 6.293a1 1 0 0 0 1.414-1.414L13.414 12l6.293-6.293a1 1 0 0 0-1.414-1.414L12 10.586 5.707 4.293z',
 'search':'M16.618 18.032a9 9 0 1 1 1.414-1.414l3.675 3.675a1 1 0 0 1-1.414 1.414l-3.675-3.675zM18 11a7 7 0 1 1-14 0 7 7 0 0 1 14 0z',
 'bag':'M10 5a2 2 0 1 1 4 0v1h-4V5zM8 8v2a1 1 0 1 0 2 0V8h4v2a1 1 0 1 0 2 0V8h.624a1 1 0 0 1 .973.771l.34 1.442A40.001 40.001 0 0 1 19 19.375V20a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1v-.625c0-3.085.357-6.16 1.063-9.162l.34-1.442A1 1 0 0 1 7.376 8H8zm0-2V5a4 4 0 1 1 8 0v1h.624a3 3 0 0 1 2.92 2.313l.34 1.442A41.995 41.995 0 0 1 21 19.375V20a3 3 0 0 1-3 3H6a3 3 0 0 1-3-3v-.625a42 42 0 0 1 1.116-9.62l.34-1.442A3 3 0 0 1 7.376 6H8z',
 'account':'M17 6A5 5 0 1 1 7 6a5 5 0 0 1 10 0zm-2 0a3 3 0 1 1-6 0 3 3 0 0 1 6 0zM21 19.801v-1.134C21 14.222 16.5 12 12 12s-9 2.222-9 6.667V19.8c0 1.255.79 2.36 2.022 2.6 1.495.292 3.822.6 6.978.6 3.156 0 5.483-.308 6.979-.6 1.231-.24 2.021-1.345 2.021-2.6zm-2-1.134V19.8a.781.781 0 0 1-.142.472.411.411 0 0 1-.262.165c-1.372.268-3.57.562-6.596.562-3.026 0-5.224-.294-6.596-.562a.411.411 0 0 1-.262-.165A.781.781 0 0 1 5 19.8v-1.134c0-1.435.684-2.521 1.912-3.33C8.2 14.49 10.042 14 12 14c1.958 0 3.8.49 5.088 1.337 1.228.809 1.912 1.895 1.912 3.33z',
 'globe':'M12 23c6.075 0 11-4.925 11-11S18.075 1 12 1 1 5.925 1 12s4.925 11 11 11zm.83-2.473c-.36.381-.641.473-.83.473-.189 0-.47-.091-.83-.473-.363-.384-.736-.992-1.07-1.827-.417-1.043-.743-2.361-.929-3.856.904.102 1.853.156 2.829.156.976 0 1.925-.054 2.829-.156-.186 1.495-.512 2.813-.929 3.856-.334.835-.707 1.444-1.07 1.827zm2.156-7.717c-.933.123-1.937.19-2.986.19-1.049 0-2.053-.067-2.987-.19A24.277 24.277 0 0 1 9 12c0-2.667.434-5.035 1.1-6.7.334-.835.707-1.443 1.07-1.827.36-.381.641-.473.83-.473.189 0 .47.091.83.473.363.384.736.992 1.07 1.827.666 1.665 1.1 4.033 1.1 6.7 0 .273-.005.544-.014.81zm1.891 1.706c-.185 1.87-.575 3.563-1.12 4.926-.128.32-.267.627-.416.918a9.009 9.009 0 0 0 5.603-7.35c-.598.372-1.3.692-2.071.959a16.62 16.62 0 0 1-1.996.547zm3.986-4.088c-.123.203-.344.446-.71.707-.47.337-1.12.662-1.935.944-.379.132-.788.252-1.222.359C17 12.292 17 12.146 17 12c0-2.856-.461-5.488-1.243-7.442-.128-.32-.267-.627-.416-.918a9.014 9.014 0 0 1 5.522 6.788zm-13.86 2.01A26.392 26.392 0 0 1 7 12c0-2.856.461-5.488 1.243-7.442.128-.32.267-.627.416-.918a9.014 9.014 0 0 0-5.522 6.788l.019.03c.36.56 1.33 1.22 2.97 1.735.28.088.572.17.878.245zm-3.947.573A9.009 9.009 0 0 0 8.66 20.36c-.15-.29-.288-.598-.416-.918-.545-1.363-.935-3.057-1.12-4.926a17.221 17.221 0 0 1-1.596-.415c-.908-.285-1.758-.647-2.47-1.09z',
 'delivery':'M17 7v1h2a3 3 0 0 1 3 3v4a3 3 0 0 1-3 3h-.17a3.001 3.001 0 0 1-5.66 0H9.83a3.001 3.001 0 0 1-5.701-.128A3.001 3.001 0 0 1 2 15V7a3 3 0 0 1 3-3h9a3 3 0 0 1 3 3zM4.292 15.706A.997.997 0 0 1 4 15V7a1 1 0 0 1 1-1h9a1 1 0 0 1 1 1v7.17A3.009 3.009 0 0 0 13.17 16H9.83a3.001 3.001 0 0 0-5.538-.293zM17 14.17A3.009 3.009 0 0 1 18.83 16H19a1 1 0 0 0 1-1v-4a1 1 0 0 0-1-1h-2v4.17zM7 18a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm9 0a1 1 0 1 0 0-2 1 1 0 0 0 0 2z',
 'returns':'M12 3a9 9 0 1 1-9 9 1 1 0 1 0-2 0c0 6.075 4.925 11 11 11s11-4.925 11-11S18.075 1 12 1c-2.659 0-5.099.944-7 2.514V2a1 1 0 0 0-2 0v4a1 1 0 0 0 1 1h4a1 1 0 0 0 0-2H6.343A8.959 8.959 0 0 1 12 3zm-1.548 7.35c0-.286.097-.446.253-.56.188-.139.54-.263 1.12-.263h.117c.625 0 1.146.132 1.732.475a.75.75 0 0 0 .757-1.296 4.78 4.78 0 0 0-1.641-.61.82.82 0 0 0 .002-.053V7.25a.75.75 0 0 0-1.5 0v.805c-.556.06-1.065.224-1.476.526-.57.42-.864 1.045-.864 1.769 0 .669.261 1.237.758 1.641.463.378 1.074.566 1.715.65l1.028.136.007.001c.54.06.823.193.964.316.11.097.201.245.201.565 0 .204-.083.39-.293.547-.226.168-.631.321-1.268.321h-.134c-.705 0-1.283-.198-1.854-.627a.75.75 0 0 0-.902 1.199c.65.488 1.343.784 2.118.887v.764a.75.75 0 1 0 1.5 0v-.776c.556-.085 1.045-.273 1.437-.566.571-.426.896-1.049.896-1.749 0-.66-.213-1.256-.713-1.693-.467-.41-1.098-.6-1.777-.678l-1.014-.134c-.504-.066-.804-.195-.964-.326-.128-.104-.205-.235-.205-.478z',
 'warranty':'M5 6.18a15.03 15.03 0 0 1 14 0V9.94a10 10 0 0 1-5.144 8.741L12 19.712l-1.856-1.032A10 10 0 0 1 5 9.94V6.18zm-2-.345c0-.516.28-.99.73-1.24a17.03 17.03 0 0 1 16.54 0c.45.25.73.724.73 1.24v4.104a12 12 0 0 1-6.172 10.49L12.97 21.46a2 2 0 0 1-1.942 0L9.172 20.43A12 12 0 0 1 3 9.939V5.835zm9 3.46c1.2-2.334 4-1.167 4 .777 0 1.945-2 4.15-4 4.928-2-.778-4-2.983-4-4.928 0-1.944 2.72-3.11 4-.777z',
}

GROUPS={
 'Meta Store': [('Meta Glasses','/ca/ai-glasses/meta-glasses/'),('Ray-Ban Meta glasses','/ca/ai-glasses/ray-ban-meta/'),('Oakley Meta glasses','/ca/ai-glasses/oakley-meta/'),('Meta Ray-Ban Display','/ca/ai-glasses/meta-ray-ban-display/'),('Compare glasses','/ca/ai-glasses/compare/'),('AI glasses accessories','/ca/ai-glasses/accessories/'),('AI glasses guides','/ca/ai-glasses/learn/'),('Meta Lab','/ca/meta-lab/'),('Meta Quest','/ca/quest/'),('Meta Quest accessories','/ca/quest/shop-all/accessories/'),('Apps and games','/experiences/'),('Meta Quest gift cards','/ca/quest/gift-cards/'),('Refurbished Meta Quest 3','/ca/refurbished/quest-3/'),('Refurbished Meta Quest 3S','/ca/refurbished/quest-3s/'),('Refurbished Ray-Ban Meta glasses','/ca/refurbished/ai-glasses/'),('More from Ray-Ban','https://rayban.com/'),('Blog','/blog/')],
 'Store support and legal':[('Meta Help Center','/help/'),('Order status','/order/find/'),('Returns','/returns/'),('Find a product demo','/demo/'),('Find a store','/ca/retailers/'),('Legal','/ca/legal/'),('Terms of sale','/ca/legal/terms-of-sale/'),('Meta Quest safety center','/ca/quest/safety-center/')],
 'Community':[('Creators','https://creator.oculus.com/'),('Developers','https://developers.meta.com/horizon/'),('Businesses','https://www.facebook.com/business/ads/'),('Non-profits','https://www.facebook.com/government-nonprofits/best-practices/nonprofits/'),('Download SDKs','https://developers.meta.com/horizon/downloads/unity/'),('Made for Meta partner program','/ca/made-for-meta/'),('VR for Good','/community/vr-for-good/')],
 'Our actions':[('Data and privacy','/actions/protecting-privacy-and-security/'),('Responsible business practices','/actions/responsible-business-practices/'),('Accessibility','/ca/accessibility/'),('Elections','/actions/preparing-for-elections-with-meta/')],
 'About us':[('About Meta','/about/'),('Company Info','/about/company-info/'),('Careers','https://metacareers.com/'),('Media gallery','/media-gallery/'),('Brand resources','/brand/resources/'),('For investors','https://investor.atmeta.com/home/default.aspx'),('Newsroom','https://about.fb.com/news/')],
 'Site terms and policies':[('Community standards','https://transparency.meta.com/policies/community-standards/'),('Privacy policy','/ca/legal/privacy-policy/'),('Terms','https://www.facebook.com/terms.php/'),('Cookie policy','https://www.facebook.com/privacy/policies/cookies/')],
 'App support':[('Facebook Help Center','https://www.facebook.com/help?ref=about.facebook.com'),('Messenger Help Center','https://www.facebook.com/help/messenger-app/?ref=about.facebook.com'),('Instagram Help Center','https://help.instagram.com/'),('WhatsApp Help Center','https://faq.whatsapp.com/'),('Workplace Help Center','https://www.facebook.com/help/work?ref=about.facebook.com'),('Meta Verified','/meta-verified/'),('Meta Account (Single Login)','/account/')],
}

def footer_group(name):
 return '<details class="official-footer-group" open><summary>'+escape(name)+'</summary><ul>'+''.join('<li>'+link(t,u)+'</li>' for t,u in GROUPS[name])+'</ul></details>'

def main():
 for device in ('desktop','mobile'):
  if not (WORK/f'meta-{device}-stitch.html').is_file(): raise ValueError('Missing native Stitch seed')
 html=(WORK/'meta-desktop-stitch.html').read_text()
 for row in json.loads((WORK/'meta-stitch-downloads.json').read_text()):
  data=(WORK/row['path']).read_bytes()
  if len(data)!=row['bytes'] or hashlib.sha256(data).hexdigest()!=row['sha256']:raise ValueError('Native export changed')
 for row in ASSETS:
  data=(WORK/row['path']).read_bytes()
  if len(data)!=row['bytes'] or hashlib.sha256(data).hexdigest()!=row['sha256']:raise ValueError('Captured original changed')
 dark=by_url('https://static.xx.fbcdn.net/rsrc.php/y9/r/tL_v571NdZ0.svg');light=by_url('https://static.xx.fbcdn.net/rsrc.php/y3/r/y6QsbGgc866.svg')
 logo='<a class="meta-logo-link" href="https://www.meta.com/ca/" aria-label="Meta home"><img class="logo-dark" src="'+dark+'" alt="Meta"><img class="logo-light" src="'+light+'" alt="Meta"></a>'
 nav=''.join(link(t,u).replace('<a ','<a class="nav-item" ',1) for t,u in [('AI glasses','/ca/ai-glasses/'),('Meta Quest','/ca/quest/'),('Meta VR Glasses','/ca/vr-glasses/')])+'<span class="nav-spacer"></span>'+''.join(link(t,u).replace('<a ','<a class="nav-item nav-extra" ',1) for t,u in [('Explore Meta','/about/'),('Support','/help/')])
 hamburger='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M2 4h20M2 12h20M2 20h20"></path></svg>'
 actions='<div class="nav-actions">'+link('','/ca/').replace('<a ','<a aria-label="Search Meta Store on official website" class="nav-icon-btn" ',1).replace('</a>',svg(ICONS['search'])+'</a>')+'<a class="region-indicator" href="https://www.meta.com/ca/" aria-label="Change shipping country and language on official website">'+svg(ICONS['globe'])+'<span>CA</span></a><a class="nav-icon-btn" href="https://www.meta.com/bag/" aria-label="View bag items">'+svg(ICONS['bag'])+'</a><a class="nav-icon-btn" href="https://www.meta.com/account/" aria-label="Log In on official website">'+svg(ICONS['account'])+'</a></div>'
 header='<header class="meta-header"><button class="mobile-menu-button" type="button" aria-label="Open mobile navigation menu" aria-controls="mobile-navigation" aria-expanded="false">'+hamburger+'</button>'+logo+'<nav class="nav-center" aria-label="Main Navigation">'+nav+'</nav>'+actions+'</header>'
 html,n=re.subn(r'<header\b[^>]*>.*?</header>',lambda _:header,html,count=1,flags=re.S);assert n==1
 notice='<div id="region-notice"><div>Did we select the right country/region? <strong>Canada</strong></div><button id="dismiss-region" class="dismiss-btn" aria-label="Dismiss the banner">'+svg(ICONS['close'])+'</button></div>'
 html,n=re.subn(r'<div id="region-notice">.*?</div>',lambda _:notice,html,count=1,flags=re.S);assert n==1
 products=[('1827369085125592','1785594222681010','Meta Glasses by LISA'),('4104975809796115','1617413229969463','Ray-Ban Meta'),('2913871422324522','1476175607896980','Ray-Ban Meta Audio'),('954863517662877','954863517662877','Meta VR Glasses'),('1369273198705222','1369273198705222','Hand holding Muse Charm, with Muse on its display'),('1547194663656162','2195054354368471','Oakley Meta'),('1467356825221356','945715694601950','Meta Ray-Ban Display'),('1639626233993472','1746818216319556','Meta Quest 3S')]
 iterator=iter(products)
 html,n=re.subn(r'<img\b[^>]*class="panel-bg-img"[^>]*>',lambda _:pic(*next(iterator),'panel-bg-img'),html);assert n==8
 categories=[('2230808311202778','1776006623643465','Oakley Meta Vanguard and Ray-Ban Meta Wayfarer AI Glasses'),('1015520448179716','28463428633322724','Meta VR Glasses'),('1640876397643578','1603834474428318','Meta Quest 3S headset')]
 iterator=iter(categories)
 html,n=re.subn(r'<img\b[^>]*alt="(?:AI glasses lineup|Meta VR Glasses lineup|Meta Quest headset lineup)"[^>]*>',lambda _:pic(*next(iterator),'category-image'),html);assert n==3
 html=html.replace('class="category-item" href="https://www.meta.com/ca/ai-glasses/"','class="category-item" href="https://www.meta.com/ca/ai-glasses/shop-all/"')
 html=html.replace('<h2 class="category-heading">','<h1 class="category-heading">').replace('from the Meta Store</h2>','from the Meta Store</h1>')
 html=html.replace('class="panel-title"','class="panel-title"').replace('<h3 class="panel-title">','<h2 class="panel-title">')
 html=re.sub(r'(<h2 class="panel-title">[^<]*)</h3>',r'\1</h2>',html)
 html=html.replace('<div class="hero-headline-1">','<div class="hero-headline-1" aria-hidden="true">').replace('<div class="hero-headline-2">','<div class="hero-headline-2" aria-hidden="true">')
 html=html.replace('<!-- Hero Subhead and CTAs -->','<h2 class="sr-only">Meet the all-new Meta Glasses</h2><div class="hero-mobile-title" aria-hidden="true">Meet the all-new Meta Glasses</div><!-- Hero Subhead and CTAs -->')
 html=html.replace('aria-label="Hero Showcase"','aria-label="Meet the all-new Meta Glasses"')
 html=html.replace('loop="" ','')
 html=html.replace('id="hero-video"','id="hero-video" data-desktop-poster="'+media('28586977950985699')+'" data-mobile-poster="'+media('1019512193865523')+'"')
 html=re.sub(r'poster="https://lookaside[^\"]*"','poster="'+media('28586977950985699')+'"',html,count=1)
 for r in ASSETS:
  html=html.replace(r['source_url'],r['path']).replace(escape(r['source_url'],quote=True),r['path'])
 news=[next(r for r in ASSETS if '818599021_' in r['source_url']),next(r for r in ASSETS if '790425514_' in r['source_url'])]
 iterator=iter(news)
 html,n=re.subn(r'<img\b[^>]*class="article-img"[^>]*>',lambda _:'<img class="article-img" src="'+next(iterator)['path']+'" alt="">',html);assert n==2
 iterator=iter(('delivery','returns','warranty'))
 html,n=re.subn(r'(<div class="benefit-icon">)\s*<svg\b.*?</svg>',lambda m:m[1]+svg(ICONS[next(iterator)]),html,flags=re.S);assert n==3
 newsletter='<div class="official-newsletter"><p class="official-newsletter-title">Get news and updates from Meta</p><div><div class="official-newsletter-fields"><input type="email" aria-label="Email" placeholder="Email" autocomplete="off"><button type="button" disabled>Sign up</button></div><div class="official-newsletter-notes"><p>By signing up you agree to receive updates and marketing messages (e.g. email, social, etc.) from Meta about Meta’s existing and future products and services.</p><p>You may withdraw your consent and unsubscribe at any time by clicking the unsubscribe link included in our messages.</p><p>Your subscription is subject to '+link('Terms','https://www.facebook.com/terms/')+' and '+link('Privacy Policy','https://www.facebook.com/privacy/policy/')+'.</p></div></div></div>'
 social=[]
 for substring,label,url in [('425860105_','Facebook','https://facebook.com/Meta'),('708050048_','Threads','https://threads.net/@meta'),('425804778_','Instagram','https://instagram.com/meta/'),('426747931_','X','https://twitter.com/Meta'),('425519002_','YouTube','https://youtube.com/meta')]:
  asset=next(r for r in ASSETS if substring in r['source_url']);social.append('<a href="'+url+'" aria-label="'+label+'"><img src="'+asset['path']+'" alt=""></a>')
 brand='<div class="official-footer-brand"><img src="'+dark+'" alt="Meta"><div class="official-socials">'+''.join(social)+'</div></div>'
 columns=[['Meta Store','Store support and legal'],['Community','Our actions'],['About us','Site terms and policies','App support']]
 groups='<div class="official-footer-grid">'+brand+''.join('<div>'+''.join(footer_group(n) for n in names)+'</div>' for names in columns)+'</div>'
 legal='<div class="official-legal"><p>Parents: '+link('Important Guidance & Safety Warnings','/ca/quest/parent-info/')+' for children’s use.</p><p>For additional details on our AI Glasses and Meta Quest products and services, please visit the product pages and review the related '+link('legal disclosures','/ca/legal/disclosures/')+'. See details for our '+link('current promotions','/ca/legal/promotional-terms/')+'.</p><p>OPTIONAL FINANCING is subject to eligibility and lender terms. For details on current financing offers, see '+link('current offers','/ca/legal/promotional-terms/')+' and '+link('Financing Disclosures','/ca/legal/disclosures/')+'.</p><p>†DISNEY+<br>PG-13 for extended sequences of sci-fi violence and action.<br>Content rating may differ in your country. Disney+ subscription required. Must be 18+ to subscribe. © 2026 Disney and its related entities. © 2026 &amp; ™ Lucasfilm Ltd. All rights reserved. Availability of 3D playback on Disney+ varies by region. Some titles shown may not be available in 3D in your country.</p><p>††NBA<br>Select NBA games only. Availability varies by region. Subscription may be required.</p><p>MUSE CHARM<br>Muse Charm requires you to sign up for Muse. Download the Muse app here: '+link('https://muse.ai/','https://muse.ai/')+'</p><p>©2026 Meta.</p></div>'
 footer='<footer class="meta-footer">'+newsletter+groups+'<div class="official-footer-bottom"><p class="official-country">'+svg(ICONS['globe'])+'Canada (English)</p>'+legal+'</div></footer>'
 html,n=re.subn(r'<footer\b.*?</footer>',lambda _:footer,html,count=1,flags=re.S);assert n==1
 explore=[('Meta Glasses','/ca/ai-glasses/meta-glasses/'),('Ray-Ban Meta','/ca/ai-glasses/ray-ban-meta/'),('Ray-Ban Meta Audio','/ca/ai-glasses/ray-ban-meta-audio/'),('Meta Ray-Ban Display','/ca/ai-glasses/meta-ray-ban-display/'),('Oakley Meta','/ca/ai-glasses/oakley-meta/'),('About AI glasses','/ca/ai-glasses/'),('Compare glasses','/ca/ai-glasses/compare/')]
 shop=[('Shop all glasses','/ca/ai-glasses/shop-all/'),('Accessories','/ca/ai-glasses/accessories/'),('Certified refurbished','/ca/refurbished/ai-glasses/'),('Prescription','/ca/ai-glasses/prescription/')]
 drawer='<aside id="mobile-navigation" class="mobile-drawer" role="dialog" aria-modal="true" aria-label="Mobile menu" hidden><div class="drawer-top"><a href="https://www.meta.com/ca/" aria-label="Meta home"><img src="'+dark+'" alt="Meta"></a><button class="drawer-close" aria-label="Close the menu">'+svg(ICONS['close'])+'</button></div><nav class="drawer-links"><details><summary>AI glasses</summary><div class="drawer-submenu"><h3>Explore</h3>'+''.join(link(*r) for r in explore)+'<h3>Shop</h3>'+''.join(link(*r) for r in shop)+'</div></details>'+link('Meta Quest','/ca/quest/')+link('Meta VR Glasses','/ca/vr-glasses/')+'</nav><div class="drawer-bottom"><p>Canada (English)</p>'+link('Explore Meta','/about/')+link('Support','/help/')+'</div></aside>'
 html=re.sub(r'<script\b.*?</script>', '',html,flags=re.S)
 html=html.replace('</body>',drawer+'<script>'+ (ROOT/'scripts/meta-current-official.js').read_text()+'</script></body>')
 css=(ROOT/'scripts/meta-current-official.css').read_text()
 html=html.replace('</head>','<meta name="robots" content="noindex"><style>'+css+'</style></head>')
 html=html.replace('viewbox=','viewBox=')
 if 'stitch-placeholder' in html or 'fidelity-study@' in html: raise ValueError('Uncorrected native placeholder')
 (WORK/'meta.html').write_text(html)
 print(json.dumps({'native_seed':'meta-desktop-stitch.html','native_mobile_seed_preserved':True,'official_assets':len(ASSETS),'draft_bytes':len(html.encode())}))

if __name__=='__main__':main()
