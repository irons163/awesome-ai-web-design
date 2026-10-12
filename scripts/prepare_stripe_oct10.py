#!/usr/bin/env python3
"""Preserve discovered Stripe assets and make an auditable static refinement.

The genuine Oct 10 Stitch export stays byte-for-byte unchanged. This refinement
uses the current public rendered DOM to correct observed omissions and geometry;
it is not accepted as live-site parity, particularly for WebGL and interactions.
"""
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote
from urllib.request import Request, urlopen
from concurrent.futures import ThreadPoolExecutor
import hashlib, json, re, html
from official_html_tree import Tree, Node, fragment

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / '.stitch-work/current-official'
ASSETS = WORK / 'stripe-oct10-assets'
ASSETS.mkdir(exist_ok=True)
BASE = 'https://stripe.com/en-ca'
bundle = json.loads((WORK / 'stripe-oct10-assets-local.json').read_text())
asset_map = {a['url']: a['local'] for a in bundle}
if (WORK/'stripe-oct10-local-asset-map.json').exists():
    asset_map.update(json.loads((WORK/'stripe-oct10-local-asset-map.json').read_text()))
source = (WORK / 'stripe-oct10-source-rendered-loaded.html').read_text()
assert len(source) > 300000 and '</body>' in source and source.endswith('</html>')
tree = Tree(source).root
body = tree.find(lambda n: n.tag == 'body')
assert body

def strip(node):
    node.children = [x for x in node.children if x.tag not in {'script', 'iframe', 'noscript', 'link'}]
    for x in node.children:
        for k in list(x.attrs):
            if k.startswith('data-analytics') or k.startswith('on'):
                del x.attrs[k]
        strip(x)
strip(body)

css_by_url = {a['url']:a for a in bundle if a['kind']=='stylesheet'}
source_css_order = list(dict.fromkeys(n.attrs['href'] for n in tree.walk() if n.tag=='link' and n.attrs.get('rel')=='stylesheet'))
css_assets = [css_by_url[u] for u in source_css_order if u in css_by_url]
css_sources = [(a['url'], (WORK / a['local']).read_text()) for a in css_assets]
urls = set()

def public_asset(url):
    return urlparse(url).hostname in {'b.stripecdn.com','images.stripeassets.com','assets.stripeassets.com','videos.stripeassets.com'}

def remember(value, base=BASE):
    u = urljoin(base, html.unescape(value.strip()))
    if public_asset(u): urls.add(u)
    return u

supplement_sources=[]
for filename in ['stripe-oct10-reference-dialog-templates.json','stripe-oct10-reference-customer-templates.json','stripe-oct10-reference-mobile-menu-templates.json']:
    if (WORK/filename).exists():
        supplement_sources.extend(Tree(markup).root for markup in json.loads((WORK/filename).read_text()).values())
for n in [node for root in [body,*supplement_sources] for node in root.walk()]:
    for k in ['src', 'poster']:
        if n.attrs.get(k): remember(n.attrs[k])
    if n.attrs.get('srcset'):
        for part in n.attrs['srcset'].split(','):
            if part.strip(): remember(part.strip().split()[0])
    if n.attrs.get('style'):
        for u in re.findall(r'url\([\'\"]?([^\)\'\"]+)',n.attrs['style']): remember(u)
for base, css in css_sources:
    for u in re.findall(r'url\([\'\"]?([^\)\'\"]+)',css):
        if not u.startswith(('data:', '#')): remember(u,base)

def download(u):
    if u in asset_map and (WORK / asset_map[u]).exists():
        return {'url':u,'local':asset_map[u],'existing':True}
    path = unquote(urlparse(u).path)
    ext = Path(path).suffix.lower()
    if ext not in {'.woff2','.woff','.png','.jpg','.jpeg','.webp','.svg','.gif','.mp4','.ico'}: ext = '.bin'
    name = hashlib.sha256(u.encode()).hexdigest()[:18] + ext
    local = 'stripe-oct10-assets/' + name
    try:
        data=urlopen(Request(u,headers={'User-Agent':'Mozilla/5.0','Referer':BASE}),timeout=35).read()
        (WORK/local).write_bytes(data)
        return {'url':u,'local':local,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
    except Exception as exc:
        return {'url':u,'error':str(exc)}

with ThreadPoolExecutor(max_workers=8) as pool:
    downloads=list(pool.map(download,sorted(urls)))
for item in downloads:
    if 'local' in item: asset_map[item['url']]=item['local']
(WORK/'stripe-oct10-asset-downloads.json').write_text(json.dumps(downloads,indent=2))

def local_url(u, base=BASE, css=False):
    target = urljoin(base, html.unescape(u))
    found = asset_map.get(target)
    return ('./'+Path(found).name if css else found) if found else target

def rewrite_markup(node):
    for n in node.walk():
        for key in ['src','poster']:
            if n.attrs.get(key): n.attrs[key]=local_url(n.attrs[key])
        if n.attrs.get('srcset'):
            n.attrs['srcset']=', '.join(local_url(p.strip().split()[0]) + (' '+ ' '.join(p.strip().split()[1:]) if len(p.strip().split())>1 else '') for p in n.attrs['srcset'].split(',') if p.strip())
        if n.attrs.get('href') and not n.attrs['href'].startswith(('#','mailto:','tel:','data:')):
            n.attrs['href']=urljoin(BASE,n.attrs['href'])
        if n.attrs.get('style'):
            n.attrs['style']=re.sub(r'url\([\'\"]?([^\)\'\"]+)[\'\"]?\)',lambda m:'url("'+local_url(m[1])+'")',n.attrs['style'])
        if n.tag=='img': n.attrs['loading']='eager'

rewrite_markup(body)
css_files=[]
for origin,css in css_sources:
    rewritten=re.sub(r'url\([\'\"]?([^\)\'\"]+)[\'\"]?\)',lambda m:m[0] if m[1].startswith(('data:','#')) else 'url("'+local_url(m[1],origin,True)+'")',css)
    name='local-'+hashlib.sha256(origin.encode()).hexdigest()[:12]+'.css'
    (ASSETS/name).write_text(rewritten)
    css_files.append('stripe-oct10-assets/'+name)

# Force official static fallbacks after removing live executable bundles.
for n in body.walk():
    classes=n.attrs.get('class','').split()
    if 'single-wave--drawn' in classes:
        n.attrs['class']=' '.join(x for x in classes if x!='single-wave--drawn')
    if n.tag=='canvas':
        n.attrs['data-static-unimplemented']='true'
    if n.attrs.get('aria-label')=='Canada. Choose your country':
        n.attrs['title']='Locale selection opens the official Stripe country selector.'

header=body.find(lambda n:n.tag=='header')
header.attrs['data-stripe-static-header']='true'

# Decorative product demos are genuine public reference captures, not substitute
# marketing text. Preserve their original screenshots and crop coordinates.
art=json.loads((WORK/'stripe-oct10-artwork-capture-manifest.json').read_text())
for key in ['payments','billing','agentic-commerce','issuing','crypto','connect']:
    card=body.find(lambda n:n.attrs.get('aria-labelledby')=='bento-card-title-'+key)
    inner=card.find(lambda n:'modular-solutions-bento-card__inner' in n.attrs.get('class','').split())
    inner.children=fragment('<picture class="stripe-frozen-art"><source media="(max-width:639px)" srcset="'+art['narrow'][key]['file']+'"><img src="'+art['desktop'][key]['file']+'" alt="Observed Stripe '+key.replace('-',' ')+' product illustration, captured 2026-10-10"></picture>')
    inner.attrs['data-capture-crop-top']='120'
for cls,key in [('data-viz','commerce-graphic'),('developers-wave-animation','developers-wave')]:
    region=body.find(lambda n:cls in n.attrs.get('class','').split())
    region.children=fragment('<img class="stripe-static-graphic" src="'+art['desktop'][key]['file']+'" alt="" aria-hidden="true">')
events_canvas=body.find(lambda n:'squeezy-carousel__canvas' in n.attrs.get('class','').split())
events_canvas.tag='img'
events_canvas.attrs['src']=art['desktop']['events-graphic']['file']
events_canvas.attrs['alt']='Stripe news and event artwork captured from the public official homepage.'
events_canvas.attrs.pop('data-static-unimplemented',None)

customers={}
for name,markup in json.loads((WORK/'stripe-oct10-reference-customer-templates.json').read_text()).items():
    ct=Tree(markup).root
    rewrite_markup(ct)
    strip(ct)
    customers[name]=ct.render()
customer_region=body.find(lambda n:'customer-stories' in n.attrs.get('class','').split())
customer_region.children=fragment(customers['Hertz'])[0].children
mobile_source=Tree((WORK/'stripe-oct10-source-mobile-rendered.html').read_text()).root
mobile_customers=mobile_source.find(lambda n:'customer-stories' in n.attrs.get('class','').split())
strip(mobile_customers)
rewrite_markup(mobile_customers)

menus=json.loads((WORK/'stripe-oct10-reference-menu-templates.json').read_text())
for name,item in menus.items():
    mt=Tree(item['popup']).root
    rewrite_markup(mt)
    menus[name]=mt.render()

mobile_menus={}
for name,markup in json.loads((WORK/'stripe-oct10-reference-mobile-menu-templates.json').read_text()).items():
    mm=Tree(markup).root
    rewrite_markup(mm)
    strip(mm)
    mobile_menus[name]=mm.render()
dialogs={}
for name,markup in json.loads((WORK/'stripe-oct10-reference-dialog-templates.json').read_text()).items():
    dt=Tree(markup).root
    rewrite_markup(dt)
    strip(dt)
    dialogs[name]=dt.render()

metadata={'provider':'Google Stitch','transport':'MCP','screen':'projects/11029026435952069219/screens/7fd99dcea465427b81fd712649f844f2','reference_url':BASE,'observed_date':'2026-10-10','refinement':'Current official DOM/CSS/assets correct original Stitch geometry and omitted sections; animations remain static and not accepted as official parity.'}
head='<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Stripe — current official reconstruction draft</title><meta name="description" content="Educational Stripe homepage reconstruction, with current official reference and Google Stitch generation provenance. Not the official Stripe website.">'+''.join('<link rel="stylesheet" href="'+f+'">' for f in css_files)+'<link rel="stylesheet" href="stripe-oct10-refinements.css"></head>'
data='<script type="application/json" id="stripe-provenance">'+json.dumps(metadata).replace('<','\\u003c')+'</script><script type="application/json" id="stripe-menu-templates">'+json.dumps({'desktop':menus,'mobile':mobile_menus,'customers':customers,'mobileCustomers':mobile_customers.render(),'dialogs':dialogs}).replace('<','\\u003c')+'</script><script src="stripe-oct10-interactions.js" defer></script>'
body.children.extend(fragment(data))
out='<!doctype html>\n<html lang="en-CA">'+head+body.render()+'</html>\n'
(WORK/'stripe.html').write_text(out)
(WORK/'stripe-oct10-local-asset-map.json').write_text(json.dumps(asset_map,indent=2))
print(json.dumps({'html_bytes':len(out.encode()),'asset_urls':len(urls),'download_success':sum('local' in a for a in downloads),'failures':[x for x in downloads if 'error' in x],'css_files':css_files,'mobile_menu_bytes':sum(map(len,mobile_menus.values()))},indent=2))
