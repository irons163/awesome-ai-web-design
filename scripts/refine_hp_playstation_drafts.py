#!/usr/bin/env python3
"""Adapt dated HP/PlayStation public snapshots with their original artwork/CSS.

Genuine Stitch exports are kept separately, without modifying their bytes.
First-party large media remains on the official CDN. Original site scripts,
telemetry, embedded applications, and inline event handlers are removed.
"""
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urljoin, urldefrag
from official_html_tree import Tree, Node, fragment

ROOT = Path(__file__).resolve().parents[1]/'.stitch-work/current-official'
BASES = {'hp':'https://www.hp.com/ca-en/home.html',
         'playstation':'https://www.playstation.com/fr-ca/'}

HP_CSS = '''
[hidden]{display:none!important}
hp-generic-carousel-slider{display:block}
hp-generic-carousel-slider .swiper-wrapper{display:flex;transform:none!important}
hp-generic-carousel-slider .swiper-slide{width:100%!important}
hp-generic-carousel-slider .swiper-slide[hidden]{display:none!important}
.draft-pagination{display:flex;justify-content:center;gap:12px;height:16px;align-items:center;position:absolute;bottom:20px;left:0;right:0;z-index:10}
.draft-pagination button{border:0;border-radius:10px;width:5px;height:5px;padding:0;background:#000;cursor:pointer}
.draft-pagination button[aria-selected="true"]{width:54px}
.draft-arrow{position:absolute;top:50%;z-index:5;width:30px;height:30px;background:#888b;color:#fff;border:1px solid #fff;cursor:pointer}
.draft-arrow.prev{left:8px}.draft-arrow.next{right:8px}
hp-generic-carousel-slider{position:relative}
.digitnav__drawer[hidden]{display:none!important}
@media(max-width:767px){hp-generic-carousel-slider .swiper-wrapper{min-height:609.5px}.draft-arrow{top:calc(50% - 24px)}}
digitnav-header .digitnav__drawer:not([hidden]){display:flex;height:auto}
@media(max-width:1023px){digitnav-header.draft-menu-open .digitnav__menu{display:flex;width:100%;left:0;right:0}digitnav-header.draft-menu-open .action-bar .mobile-menu-button{display:none}digitnav-header.draft-menu-open .action-bar .close-menu-button{display:block}}
'''
HP_JS = '''
const carousel=document.querySelector('hp-generic-carousel-slider');
const slides=[...carousel.querySelectorAll('.swiper-wrapper>.swiper-slide')];
const tabs=[...carousel.querySelectorAll('.draft-pagination button')];let current=0;
function choose(index){current=(index+slides.length)%slides.length;slides.forEach((n,i)=>{n.hidden=i!==current;n.setAttribute('aria-hidden',String(i!==current));});tabs.forEach((n,i)=>n.setAttribute('aria-selected',String(i===current)));}
tabs.forEach((b,i)=>b.addEventListener('click',()=>choose(i)));
carousel.querySelector('.prev').addEventListener('click',()=>choose(current-1));
carousel.querySelector('.next').addEventListener('click',()=>choose(current+1));choose(0);
document.querySelectorAll('.digitnav__menu .menu-item').forEach(item=>{
 const triggers=[...item.querySelectorAll('.menu-link,.menu-toggle')],drawer=item.querySelector('.digitnav__drawer');if(!triggers.length||!drawer)return;drawer.hidden=true;
 triggers.forEach(trigger=>trigger.addEventListener('click',e=>{e.preventDefault();const open=drawer.hidden;document.querySelectorAll('.digitnav__drawer').forEach(n=>n.hidden=true);drawer.hidden=!open;triggers.forEach(b=>b.setAttribute('aria-expanded',String(open)));item.classList.toggle('draft-open',open);}));
});
const hpHeader=document.querySelector('digitnav-header');
hpHeader.querySelector('.mobile-menu-button')?.addEventListener('click',()=>{hpHeader.classList.add('draft-menu-open');hpHeader.querySelector('.mobile-menu-button').setAttribute('aria-expanded','true');});
hpHeader.querySelector('.close-menu-button')?.addEventListener('click',()=>{hpHeader.classList.remove('draft-menu-open');hpHeader.querySelector('.mobile-menu-button').setAttribute('aria-expanded','false');});
document.addEventListener('keydown',e=>{if(e.key==='Escape'){document.querySelectorAll('.digitnav__drawer').forEach(n=>n.hidden=true);hpHeader.classList.remove('draft-menu-open');hpHeader.querySelector('.mobile-menu-button').setAttribute('aria-expanded','false');}});
'''

PS_LOGO = '''<svg aria-hidden="true" viewBox="0 0 50 50" width="50" height="50"><path fill="#0070d1" d="M5.8,32.1C4.3,33.1,4.8,35,8,35.9c3.3,1.1,6.9,1.4,10.4,0.8c0.2,0,0.4-0.1,0.5-0.1v-3.4l-3.4,1.1 c-1.3,0.4-2.6,0.5-3.9,0.2c-1-0.3-0.8-0.9,0.4-1.4l6.9-2.4V27l-9.6,3.3C8.1,30.7,6.9,31.3,5.8,32.1z M29,17.1v9.7 c4.1,2,7.3,0,7.3-5.2c0-5.3-1.9-7.7-7.4-9.6C26,11,23,10.1,20,9.5v28.9l7,2.1V16.2c0-1.1,0-1.9,0.8-1.6C28.9,14.9,29,16,29,17.1z M42,29.8c-2.9-1-6-1.4-9-1.1c-1.6,0.1-3.1,0.5-4.5,1l-0.3,0.1v3.9l6.5-2.4c1.3-0.4,2.6-0.5,3.9-0.2c1,0.3,0.8,0.9-0.4,1.4 l-10,3.7V40L42,34.9c1-0.4,1.9-0.9,2.7-1.7C45.4,32.2,45.1,30.8,42,29.8z"/></svg>'''
PS_CSS = '''
@font-face{font-family:AlternateGotNo1D;src:url('playstation-assets/ea589c7b7902f823.ttf') format('truetype');font-display:swap}
[hidden]{display:none!important}
body{padding:0!important}
#shared-nav-root{display:block!important;position:relative!important;inset:auto!important;width:100%!important;height:auto!important;min-height:0!important;padding:0!important;margin:0!important}
#shared-nav-root .draft-sony,#shared-nav-root .draft-ps-nav{width:100%;max-width:none;box-sizing:border-box}
.media-block__img.lazy-loaded img{opacity:1}
.gdk .media-block--image .media-block__img>img{width:100%;max-width:100%}
@media(min-width:768px){.gdk .page-banner__logo{max-height:none!important}.gdk .page-banner__logo .media-block__inner,.gdk .page-banner__logo .media-block__figure,.gdk .page-banner__logo .media-block__img,.gdk .page-banner__logo img{height:auto!important}}
[data-component="featured-hardware-v2"]{grid-template-columns:minmax(0,1fr)!important}
[data-component="featured-hardware-v2"] .slider__slides>.layout__2--c{grid-template-columns:minmax(0,1fr) minmax(0,2fr)!important}
[data-component="featured-hardware-v2"] .slider__slides>.slider__slide>.box{min-width:0}
@media(max-width:767px){[data-component="featured-hardware-v2"] .slider__slides>.layout__2--c{grid-template-columns:minmax(0,1fr)!important}}
#project-whisky-hpto-micropod-data{display:none}
.draft-sony{height:36px;background:#000;display:flex;justify-content:flex-end;align-items:center;padding:0;color:white;font:bold 20px Georgia,serif;letter-spacing:1px}
.draft-sony a{display:flex}.draft-sony .sony-logo{height:36px}
.draft-ps-nav{height:64px;display:flex;align-items:center;gap:14px;padding:0 12px;background:white;position:relative;z-index:20;font:13px sst,Arial,sans-serif}
.draft-ps-links{display:flex;gap:10px;align-items:center}.draft-ps-links button{font:inherit;background:transparent;border:0;padding:0;cursor:pointer}
.draft-ps-account{margin-left:auto;color:white;background:#0070d1;border-radius:24px;padding:2px 8px;font-size:16px;line-height:18px;text-decoration:none}
.draft-ps-search,.draft-ps-menu{background:transparent;border:0;font:24px Arial;padding:0 8px;cursor:pointer}.draft-ps-menu{display:none}
.draft-ps-search{order:9;display:flex;align-items:center}.draft-ps-search svg{width:20px;height:20px;fill:#000}
.draft-ps-brand{flex-shrink:0}
.draft-ps-panel{background:white;padding:24px;position:absolute;top:64px;left:0;right:0;box-shadow:0 10px 14px #0002;display:flex;gap:24px;flex-wrap:wrap}
.draft-ps-panel a{color:#0070d1}
[data-component="hp-hero"] .slider__slides>[hidden]{display:none!important}
[data-component="hp-hero"] .slider__controls{display:flex;justify-content:center;gap:10px;overflow-x:auto;padding:28px max(20px,calc((100% - 886px)/2));scrollbar-width:none}
[data-component="hp-hero"] .slider__control{display:block!important;flex:0 0 118px;cursor:pointer;border-radius:12px;overflow:hidden}
[data-component="hp-hero"] .slider__control.is-selected{outline:3px solid #0070d1;outline-offset:3px}
.draft-row{display:flex;gap:24px;overflow-x:auto;scrollbar-width:none}
.draft-row>.carousel-cell{flex:0 0 32%;min-width:0}
.draft-wolverine{height:64px;display:flex;align-items:center;justify-content:space-between;position:relative;overflow:hidden;background:#feeb37 url('playstation-assets/wolverine-ribbon-bg.webp') center top/cover;font-family:AlternateGotNo1D,Impact,sans-serif;color:#1d1b11}
.draft-wolverine-logo{width:116.355px;height:45px;object-fit:contain;margin-left:21px}
.draft-wolverine-title{position:absolute;left:50%;transform:translateX(-50%);font-size:52px;line-height:.85;text-transform:uppercase;text-align:center;white-space:nowrap}
.draft-wolverine-rage{position:relative;width:281.77px;height:64px;display:flex;align-items:center;justify-content:flex-end;background:url('playstation-assets/wolverine-rage-art.webp') center/100% auto no-repeat;color:#fff;padding-right:20px;box-sizing:border-box}
.draft-wolverine-rage span{font-size:20px;line-height:1;max-width:115px;text-align:center;text-transform:uppercase}
.draft-wolverine-rage small{position:absolute;top:5px;left:38px;font:11px sst,Arial,sans-serif;color:#1d1b11}
.draft-wolverine:hover{filter:brightness(.96)}
@media(max-width:767px){.draft-wolverine-title{width:calc(100% - 251.58912px)!important}.draft-wolverine-rage small{left:calc(8px - (100vw - 94px))!important;top:auto;bottom:2px;color:#1d1b11;font-size:8px!important}}
@media(max-width:767px){.draft-sony{display:none}.draft-ps-nav{height:60px;gap:0;padding:0 8px}.draft-ps-links{display:none}.draft-ps-brand{position:absolute;left:calc(50% - 25px)}.draft-ps-menu{display:block}.draft-ps-account{font-size:14px}.draft-ps-panel{top:60px;flex-direction:column}.draft-ps-search{margin-right:auto;order:0}[data-component="hp-hero"] .slider__controls{justify-content:flex-start;padding:20px;gap:14px}[data-component="hp-hero"] .slider__control{flex-basis:166px}.draft-row>.carousel-cell{flex-basis:84%}.draft-wolverine-logo{width:78px;height:30px;margin-left:12px;transform:translateY(-4px)}.draft-wolverine-title{font-size:24px;width:170px;white-space:normal;line-height:1}.draft-wolverine-rage{width:94px;padding-right:4px;background-size:auto 100%}.draft-wolverine-rage span{font-size:12px;width:52px}.draft-wolverine-rage small{font-size:5px;left:0}}
'''
PS_JS = '''
document.querySelectorAll('[data-component="featured-hardware-v2"] [data-control-id]').forEach(n=>{n.tabIndex=0;n.setAttribute('role','button');n.setAttribute('aria-label',n.textContent.trim()||'Console PS5');});
function sizeHeroLogos(hero){hero.querySelectorAll('.slider__slide:not([hidden]) .page-banner__logo .media-block__inner').forEach(n=>{const logo=n.closest('.page-banner__logo');if(matchMedia('(max-width:767px)').matches){n.style.removeProperty('height');logo.style.removeProperty('height');return;}const picture=n.querySelector('picture');const height=picture?.getBoundingClientRect().height;if(height>0){n.style.setProperty('height',height+'px','important');logo.style.setProperty('height',height+'px','important');}});}
document.querySelectorAll('[data-component="hp-hero"]').forEach(hero=>{
 const slides=[...hero.querySelectorAll('.slider__slides>.slider__slide')],tabs=[...hero.querySelectorAll('[data-control-id]')];
 function choose(i){slides.forEach((n,j)=>{n.hidden=i!==j;n.classList.toggle('display--hidden',i!==j);n.classList.toggle('cmp-carousel__item--active',i===j);n.setAttribute('aria-hidden',String(i!==j));});tabs.forEach((n,j)=>{n.classList.toggle('is-selected',i===j);n.setAttribute('aria-selected',String(i===j));});sizeHeroLogos(hero);}
 tabs.forEach((n,i)=>{n.addEventListener('click',()=>choose(i));n.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();choose(i);}});});choose(0);
 hero.querySelectorAll('.page-banner__logo img').forEach(img=>img.addEventListener('load',()=>sizeHeroLogos(hero)));window.addEventListener('load',()=>sizeHeroLogos(hero));window.addEventListener('resize',()=>sizeHeroLogos(hero));
});
document.querySelectorAll('[data-component="featured-hardware-v2"]').forEach(section=>{const slides=[...section.querySelectorAll('.slider__slides>.slider__slide')],tabs=[...section.querySelectorAll('[data-control-id]')];function choose(i){slides.forEach((n,j)=>{n.hidden=i!==j;n.classList.toggle('display--hidden',i!==j);n.setAttribute('aria-hidden',String(i!==j));});tabs.forEach((n,j)=>{n.classList.toggle('is-selected',i===j);n.setAttribute('aria-selected',String(i===j));});}tabs.forEach((n,i)=>{n.addEventListener('click',()=>choose(i));n.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();choose(i);}});});choose(0);});
const menu=document.querySelector('.draft-ps-panel');
document.querySelectorAll('[data-ps-menu]').forEach(b=>b.addEventListener('click',()=>{const open=menu.hidden;menu.hidden=!open;b.setAttribute('aria-expanded',String(open));}));
document.addEventListener('keydown',e=>{if(e.key==='Escape'){menu.hidden=true;document.querySelectorAll('[data-ps-menu]').forEach(b=>b.setAttribute('aria-expanded','false'));}});
document.querySelectorAll('[data-component="tabs"]').forEach(group=>{const pills=[...group.querySelectorAll('.pills__item')],panels=[...group.querySelectorAll('.tabs__tab-content')];function select(order){pills.forEach(p=>{const active=p.dataset.contentOrder===order;p.classList.toggle('pills__item--active',active);p.setAttribute('aria-selected',String(active));});panels.forEach(p=>{p.hidden=p.dataset.contentOrder!==order;});}pills.forEach(p=>{p.addEventListener('click',()=>select(p.dataset.contentOrder));p.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();select(p.dataset.contentOrder);}});});select('1');});
document.querySelectorAll('button[data-component="footer-nav"][aria-controls]').forEach((b,i)=>{const panel=document.getElementById(b.getAttribute('aria-controls'));if(!panel)return;const mobile=matchMedia('(max-width:767px)').matches;panel.hidden=mobile&&i!==0;b.setAttribute('aria-expanded',String(!panel.hidden));b.addEventListener('click',()=>{const open=b.getAttribute('aria-expanded')!=='true';b.setAttribute('aria-expanded',String(open));panel.hidden=!open;});});
'''


def adapt(brand):
    base=BASES[brand]
    provenance=json.loads((ROOT/(brand+'-asset-provenance.json')).read_text())
    assets=provenance['assets']
    local={a['source_url']:a['path'] for a in assets}
    style_map={}
    derived=[]
    for asset in assets:
        if asset['kind']!='stylesheet':
            continue
        original=ROOT/asset['path']
        target=original.with_suffix('.local.css')
        def css_url(m):
            value=m.group(1).strip().strip('"\'')
            if value.startswith(('data:','#')):
                return m.group(0)
            absolute=urljoin(asset['source_url'],value)
            return 'url("'+(Path(local[absolute]).name if absolute in local else absolute)+'")'
        css=re.sub(r'url\(\s*([^)]+)\s*\)',css_url,original.read_text())
        target.write_text(css)
        style_map[asset['source_url']]=target.relative_to(ROOT).as_posix()
        derived.append({'source_url':asset['source_url'],'source_sha256':asset['sha256'],'path':target.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(target.read_bytes()).hexdigest()})
    (ROOT/(brand+'-local-css.json')).write_text(json.dumps(derived,indent=2)+'\n')
    tree=Tree((ROOT/(brand+'-source-current.html')).read_text())
    def clean(node):
        children=[]
        for child in node.children:
            if child.tag in ('script','iframe','template','hp-modal'):
                continue
            if child.tag=='noscript':
                children.extend(n for n in child.children if n.tag=='img')
            else:
                children.append(child)
        node.children=children
        for name in list(node.attrs):
            if name.startswith('on'):
                del node.attrs[name]
        for child in children:
            clean(child)
    clean(tree.root)
    for n in tree.root.walk():
        if n.attrs.get('style'):
            # Safe unquoted URL tokens avoid quote entities in HTML attributes.
            n.attrs['style']=re.sub(r'''url\(\s*["']([^"'\s()]+)["']\s*\)''',lambda m:'url('+m.group(1)+')',n.attrs['style'])
        if n.tag=='use' and n.attrs.get('xlink:href'):
            n.attrs['href']=n.attrs.pop('xlink:href')
        if n.tag=='img':
            n.attrs['loading']='eager'
            if brand=='playstation':
                n.attrs.pop('itemprop',None)
        if n.tag=='picture':
            if brand=='playstation':
                n.attrs['class']=n.attrs.get('class','')+' lazy-loaded'
                n.attrs['data-loaded']='true'
            images=[c for c in n.children if c.tag=='img']
            if len(images)>1:
                first=images[0]
                n.children=[c for c in n.children if c.tag!='img' or c is first]
            if not images:
                sources=[c for c in n.children if c.tag=='source']
                if sources:
                    n.children.append(Node('img',[('src',sources[-1].attrs.get('srcset','').split(' ')[0]),('alt',n.attrs.get('data-alt',''))]))
            if brand=='playstation':
                for img in [c for c in n.children if c.tag=='img']:
                    img.attrs['alt']=n.attrs.get('data-alt',img.attrs.get('alt',''))
        for data,attr in [('data-src','src'),('data-srcset','srcset')]:
            if n.tag in ('img','source') and n.attrs.get(data):
                n.attrs[attr]=n.attrs[data]
        for name in ('href','src','poster','action'):
            value=n.attrs.get(name)
            if not value or value.startswith(('data:','#','mailto:','tel:')):
                continue
            if value.startswith('javascript:'):
                n.attrs[name]='#'
                continue
            absolute=urljoin(base,value)
            resource,anchor=urldefrag(absolute)
            resolved=style_map.get(resource,local.get(resource,resource))
            n.attrs[name]=resolved+('#'+anchor if anchor else '')
        if n.attrs.get('srcset') and not n.attrs['srcset'].startswith('data:'):
            n.attrs['srcset']=', '.join(urljoin(base,v.strip().split(' ')[0])+(' '+v.strip().split(' ',1)[1] if ' ' in v.strip() else '') for v in n.attrs['srcset'].split(','))
        if n.tag=='link' and n.attrs.get('rel') in ('preconnect','dns-prefetch','preload'):
            n.attrs['rel']='nofollow'
        if brand=='playstation' and n.attrs.get('data-component')=='page-banner':
            n.attrs['class']=n.attrs.get('class','')+' '+n.attrs.get('data-bg-animation','')+' '+n.attrs.get('data-content-animation','')
    head=tree.root.find(lambda n:n.tag=='head')
    body=tree.root.find(lambda n:n.tag=='body')
    title=head.find(lambda n:n.tag=='title')
    title.children=fragment(('HP Canada' if brand=='hp' else 'PlayStation Canada')+' · Unofficial visual study')
    fonts=''.join('<link rel="preload" as="font" crossorigin href="'+a['path']+'">' for a in assets if a['kind']=='font')
    head.children+=fragment('<meta name="robots" content="noindex">'+fonts+'<style>'+ (HP_CSS if brand=='hp' else PS_CSS)+'</style>')
    if brand=='hp':
        carousel=tree.root.find(lambda n:n.tag=='hp-generic-carousel-slider')
        count=len([n for n in carousel.walk() if 'swiper-slide' in n.attrs.get('class','').split()])
        carousel.children+=fragment('<button class="draft-arrow prev" aria-label="Previous slide">←</button><button class="draft-arrow next" aria-label="Next slide">→</button><div class="draft-pagination" role="tablist">'+''.join('<button role="tab" aria-label="Go to slide '+str(i+1)+'"></button>' for i in range(count))+'</div>')
    else:
        nav=tree.root.find(lambda n:n.attrs.get('id')=='shared-nav-root')
        names=['Magasin','PS5','Jeux','PS Plus','Accessoires','Actualités','Assistance']
        links=[('PS5','/fr-ca/ps5/'),('Jeux','/fr-ca/ps5/games/'),('PS Plus','/fr-ca/ps-plus/'),('Accessoires','/fr-ca/accessories/'),('Assistance','/fr-ca/support/')]
        search='<svg aria-hidden="true" viewBox="0 0 50 50"><path d="M8,20.913 C8,14.344 13.344,9 19.913,9 C26.482,9 31.827,14.344 31.827,20.913 C31.827,27.482 26.482,32.827 19.913,32.827 C13.344,32.827 8,27.482 8,20.913 M45.112,43.585 L32.346,30.82 C34.518,28.099 35.827,24.658 35.827,20.913 C35.827,12.139 28.688,5 19.913,5 C11.139,5 4,12.139 4,20.913 C4,29.688 11.139,36.827 19.913,36.827 C23.503,36.827 26.808,35.618 29.474,33.604 L42.284,46.413 C42.674,46.804 43.186,46.999 43.698,46.999 C44.209,46.999 44.721,46.804 45.112,46.413 C45.502,46.023 45.698,45.511 45.698,44.999 C45.698,44.488 45.502,43.976 45.112,43.585"></path></svg>'
        nav.children=fragment('<div class="draft-sony"><a href="https://www.sony.com/" aria-label="Sony"><span class="sony-logo sony-bar__logo"></span></a></div><nav class="draft-ps-nav"><button class="draft-ps-menu" aria-label="Menu" data-ps-menu aria-expanded="false">☰</button><button class="draft-ps-search" aria-label="Rechercher">'+search+'</button><a class="draft-ps-brand" href="https://www.playstation.com/fr-ca/" aria-label="Accueil PlayStation">'+PS_LOGO+'</a><div class="draft-ps-links">'+''.join('<button data-ps-menu aria-expanded="false">'+x+' ⌄</button>' for x in names)+'</div><a class="draft-ps-account" href="https://www.playstation.com/fr-ca/playstation-network/">Connexion</a><div class="draft-ps-panel" hidden>'+''.join('<a href="https://www.playstation.com'+href+'">'+name+'</a>' for name,href in links)+'</div></nav>')
        nav.children+=fragment('<a class="draft-wolverine" href="https://www.playstation.com/fr-ca/games/marvels-wolverine/" aria-label="Découvrez Wolverine en action"><img class="draft-wolverine-logo" src="playstation-assets/wolverine-logo.webp" alt="Marvel’s Wolverine"><span class="draft-wolverine-title">Découvrez Wolverine en action</span><span class="draft-wolverine-rage"><small>© 2026 MARVEL</small><span>Entrer en mode<br>Rage</span></span></a>')
        for n in tree.root.walk():
            if n.attrs.get('data-carousel')=='true' and 'slider__controls' not in n.attrs.get('class',''):
                n.attrs['class']=n.attrs.get('class','')+' draft-row'
    body.children+=fragment('<script>'+(HP_JS if brand=='hp' else PS_JS)+'</script>')
    (ROOT/(brand+'.html')).write_text('<!doctype html>'+tree.root.render())
    print('Saved',brand,'source-calibrated draft')


if __name__=='__main__':
    for brand in BASES:
        adapt(brand)
