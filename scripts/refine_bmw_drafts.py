#!/usr/bin/env python3
"""Correct native Stitch candidates against dated official BMW source markup.

Native exports remain unchanged. The displayed studies use the observed source
hierarchy and CSS, with locally authored navigation and carousel behavior.
"""
import json
import re
from pathlib import Path
from urllib.parse import urljoin
from official_html_tree import Tree, fragment

ROOT = Path(__file__).resolve().parents[1] / '.stitch-work/current-official'
BASES = {'bmw': 'https://www.bmw.com.tw/zh/index.html',
         'bmw-m': 'https://www.bmw-m.com/en/index.html'}
COMMON = '''[hidden]{display:none!important}:focus-visible{outline:2px solid #3466cc;outline-offset:3px}
@media(prefers-reduced-motion:reduce){*,*:before,*:after{animation:none!important;scroll-behavior:auto!important;transition:none!important}}
'''
BMW_CSS = '''
.cmp-globalnavigation__flyout:not([data-draft-open]){display:none!important}
.cmp-globalnavigation__flyout[data-draft-open]{display:block;opacity:1}
.cmp-globalnavigation__flyout-layer[data-draft-layer]{display:flex}
.cmp-globalnavigation__flyout-layer[data-draft-layer] .cmp-globalnavigation__flyout-wrapper{opacity:1;transform:scaleY(1)}
.cmp-mybmw-flyout-login-url{display:none!important}
.draft-mybmw{padding:32px;background:white;color:#262626}
@media(min-width:1024px){.cmp-globalnavigation__navigation-mobile{display:none!important}}
@media(max-width:1023px){
.cmp-globalnavigation--open .cmp-globalnavigation__primary,.cmp-globalnavigation--open .cmp-globalnavigation__navigation-mobile{left:0}
.cmp-globalnavigation--open .cmp-globalnavigation__navigation-mobile{background:#fff;border-color:#bbb}
.cmp-globalnavigation--open .cmp-globalnavigation__navigation-mobile .cmp-globalnavigation__interaction{color:#262626}
.cmp-globalnavigation--open .cmp-globalnavigation__navigation-mobile .cmp-globalnavigation__logo-image--white{display:none}
.cmp-globalnavigation--open .cmp-globalnavigation__navigation-mobile .cmp-globalnavigation__logo-image--grey{display:block}
.cmp-globalnavigation__flyout-layer[data-draft-layer]{left:0}
}
'''
M_CSS = '''
.pw-m-swiper-carousel:not([data-draft-hero]){overflow:hidden}
.pw-m-swiper-carousel__scroll-wrapper{transition:transform .35s ease}
.pw-m-header__submenu[hidden]{display:none!important}
.pw-m-header__nav[data-draft-open]{display:block;visibility:visible;opacity:1;transform:none}
.pw-m-header__slogan{pointer-events:none}
'''
BMW_JS = '''
const navigation=document.querySelector('.cmp-globalnavigation');
const layer=document.querySelector('.cmp-globalnavigation__flyout-layer');
const triggers=[...document.querySelectorAll('button[data-button-id]')];
function closeNavigation(){navigation.classList.remove('cmp-globalnavigation--open');layer?.removeAttribute('data-draft-layer');document.querySelectorAll('[data-flyout-id]').forEach(e=>e.removeAttribute('data-draft-open'));triggers.forEach(b=>{b.setAttribute('aria-expanded','false');b.setAttribute('aria-pressed','false');});}
triggers.forEach(button=>{button.setAttribute('aria-expanded','false');button.addEventListener('click',()=>{const id=button.dataset.buttonId,flyout=[...document.querySelectorAll('[data-flyout-id]')].find(e=>e.dataset.flyoutId===id),open=button.getAttribute('aria-expanded')!=='true';closeNavigation();if(open&&flyout){navigation.classList.add('cmp-globalnavigation--open');layer.setAttribute('data-draft-layer','');flyout.setAttribute('data-draft-open','');button.setAttribute('aria-expanded','true');button.setAttribute('aria-pressed','true');}});});
document.querySelectorAll('.cmp-globalnavigation__interaction--toggle-open').forEach(b=>{b.setAttribute('aria-expanded','false');b.addEventListener('click',()=>{navigation.classList.add('cmp-globalnavigation--open');b.setAttribute('aria-expanded','true');});});
document.querySelectorAll('.cmp-globalnavigation__interaction--toggle-close,.cmp-globalnavigation__header-back').forEach(b=>b.addEventListener('click',closeNavigation));
document.addEventListener('keydown',e=>{if(e.key==='Escape')closeNavigation();});
document.querySelectorAll('footer .cmp-list__title--collapsable-mobile').forEach(title=>{const list=title.nextElementSibling;title.setAttribute('role','button');title.tabIndex=0;title.setAttribute('aria-expanded','false');title.setAttribute('aria-controls',list.id);function toggle(){if(!matchMedia('(max-width:767px)').matches)return;const open=title.getAttribute('aria-expanded')!=='true';title.setAttribute('aria-expanded',String(open));title.classList.toggle('cmp-list__title--expanded',open);list.style.maxHeight=open?list.scrollHeight+'px':'';}title.addEventListener('click',toggle);title.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();toggle();}});});
'''
M_JS = '''
const header=document.querySelector('.pw-m-header'),burger=document.querySelector('.pw-m-header__burger-button'),nav=document.querySelector('.pw-m-header__nav');
header.classList.add('pw-m-header--initialized');
function closeMenu(){nav.removeAttribute('data-draft-open');header.classList.remove('pw-m-header--mobile-open','pw-m-header--search-active');document.querySelector('.pw-m-header__search-button').setAttribute('aria-expanded','false');burger.setAttribute('aria-expanded','false');document.querySelector('.pw-m-header__icon-menu').style.display='';document.querySelector('.pw-m-header__icon-close').style.display='none';document.querySelectorAll('.pw-m-header__submenu').forEach(e=>e.hidden=true);document.querySelectorAll('.pw-m-header__menu-link[role=button]').forEach(e=>e.setAttribute('aria-expanded','false'));}
burger.addEventListener('click',()=>{const open=burger.getAttribute('aria-expanded')!=='true';closeMenu();if(open){nav.setAttribute('data-draft-open','');header.classList.add('pw-m-header--mobile-open');burger.setAttribute('aria-expanded','true');document.querySelector('.pw-m-header__icon-menu').style.display='none';document.querySelector('.pw-m-header__icon-close').style.display='';}});
document.querySelectorAll('.pw-m-header__menu-link[role=button]').forEach(button=>{function toggle(){const submenu=button.parentElement.querySelector('.pw-m-header__submenu'),open=submenu.hidden;document.querySelectorAll('.pw-m-header__submenu').forEach(e=>e.hidden=true);document.querySelectorAll('.pw-m-header__menu-link[role=button]').forEach(e=>e.setAttribute('aria-expanded','false'));submenu.hidden=!open;button.setAttribute('aria-expanded',String(open));submenu.querySelectorAll('a').forEach(e=>e.tabIndex=open?0:-1);}button.addEventListener('click',toggle);button.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();toggle();}});});
document.addEventListener('keydown',e=>{if(e.key==='Escape')closeMenu();});
const searchForm=document.querySelector('.pw-m-header__search-form'),searchInput=searchForm.querySelector('input'),searchButton=searchForm.querySelector('button');
function search(){if(searchInput.value.trim())location.href=searchForm.action+'#'+encodeURIComponent(searchInput.value.trim());}
searchForm.addEventListener('submit',event=>{event.preventDefault();search();});
searchButton.addEventListener('click',()=>{if(matchMedia('(max-width:1023px)').matches){search();return;}const open=searchButton.getAttribute('aria-expanded')!=='true';searchButton.setAttribute('aria-expanded',String(open));header.classList.toggle('pw-m-header--search-active',open);if(open)searchInput.focus();});
document.querySelectorAll('.pw-m-swiper-carousel').forEach(carousel=>{
 carousel.classList.add('swiper','swiper-initialized','swiper-horizontal');
 const wrapper=carousel.querySelector('.pw-m-swiper-carousel__scroll-wrapper');wrapper.classList.add('swiper-wrapper');
 const slides=[...wrapper.children].filter(e=>e.classList.contains('pw-m-swiper-carousel__slide'));
 slides.forEach(e=>e.classList.add('swiper-slide'));
 const hero=!!carousel.closest('.pw-m-stage-hero-teaser'),focus=!!carousel.closest('.pw-m-focus-teaser');
 if(hero)carousel.dataset.draftHero='';
 let index=0;
 function update(){const step=slides[1]?slides[1].offsetLeft-slides[0].offsetLeft:slides[0].offsetWidth;
  const max=Math.max(0,wrapper.scrollWidth-carousel.clientWidth);const offset=Math.min(index*step,max);wrapper.style.transform='translate3d('+(-offset)+'px,0,0)';
  const previous=carousel.querySelector('.swiper-button-prev'),next=carousel.querySelector('.swiper-button-next');if(previous)previous.disabled=index===0;if(next)next.disabled=offset>=max;
  slides.forEach((slide,i)=>slide.classList.toggle('swiper-slide-active',i===index));
 }
 carousel.querySelector('.swiper-button-prev')?.addEventListener('click',()=>{index=Math.max(0,index-1);update();});
 carousel.querySelector('.swiper-button-next')?.addEventListener('click',()=>{index=Math.min(slides.length-1,index+1);update();});
 carousel.tabIndex=0;carousel.addEventListener('keydown',e=>{if(!['ArrowLeft','ArrowRight','Home','End'].includes(e.key))return;e.preventDefault();index=e.key==='Home'?0:e.key==='End'?slides.length-1:Math.max(0,Math.min(slides.length-1,index+(e.key==='ArrowRight'?1:-1)));update();});
 window.addEventListener('resize',update);update();
});
const mediaObserver=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting&&!matchMedia('(prefers-reduced-motion:reduce)').matches){entry.target.play().catch(()=>{});}else entry.target.pause();}));
document.querySelectorAll('video').forEach(video=>{video.muted=true;video.loop=true;video.playsInline=true;video.preload='none';video.removeAttribute('autoplay');mediaObserver.observe(video);});
'''


def refine(brand):
    # A source correction is recorded separately from the untouched AI candidate.
    if not (ROOT / (brand + '-desktop-native.html')).exists():
        raise FileNotFoundError('Preserve the native desktop export before refining ' + brand)
    base = BASES[brand]
    records = json.loads((ROOT / (brand + '-asset-provenance.json')).read_text())['assets']
    assets = {a['source_url']:a['path'] for a in records}
    styles = {}
    for asset in records:
        if not asset['path'].endswith('.css'):
            continue
        original = (ROOT / asset['path']).read_text()
        def css_url(match):
            value = match.group(1).strip().strip('\'"')
            if value.startswith(('data:', '#')):
                return match.group(0)
            absolute = urljoin(asset['source_url'], value)
            local = assets.get(absolute)
            return 'url("' + (Path(local).name if local else absolute) + '")'
        local = asset['path'].replace('source-', 'display-')
        (ROOT / local).write_text(re.sub(r'url\(([^)]+)\)', css_url, original))
        styles[asset['source_url']] = local
    tree = Tree((ROOT / (brand + '-source-current.html')).read_text())
    def clean(node):
        node.children = [c for c in node.children if c.tag not in ('script','iframe','noscript','tracking','dialog')
                         and 'epaasnotavailablebanner' not in c.attrs.get('class','').replace('-','')]
        node.attrs = {k:v for k,v in node.attrs.items() if not k.startswith(('on','data-tracking','data-track'))}
        for child in node.children:
            clean(child)
    clean(tree.root)
    for node in tree.root.walk():
        if node.tag == 'link':
            if node.attrs.get('rel') == 'stylesheet':
                url = urljoin(base,node.attrs['href'])
                node.attrs['href'] = styles.get(url,url)
            elif node.attrs.get('as') == 'script' or node.attrs.get('rel') in ('manifest','preconnect','dns-prefetch'):
                node.attrs.pop('href',None)
        for attr in ['src','href','poster','xlink:href','data-src','action']:
            value = node.attrs.get(attr)
            if not value or value.startswith(('#','data:','mailto:','tel:')):
                continue
            if attr == 'href' and value in styles.values():
                continue
            node.attrs[attr] = assets.get(urljoin(base,value),urljoin(base,value))
        for attr in ['srcset','data-srcset']:
            if node.attrs.get(attr):
                # BMW's Scene7 URLs contain escaped commas, not unescaped lists.
                node.attrs[attr] = ', '.join(urljoin(base,item.strip().split(' ')[0]) +
                                          (' ' + item.strip().split(' ',1)[1] if ' ' in item.strip() else '')
                                          for item in node.attrs[attr].split(','))
        if node.tag == 'source' and node.attrs.get('data-src'):
            node.attrs['src'] = node.attrs.pop('data-src')
        if node.tag == 'source' and node.attrs.get('data-srcset'):
            node.attrs['srcset'] = node.attrs.pop('data-srcset')
        if node.tag == 'img' and node.attrs.get('data-src'):
            node.attrs['src'] = node.attrs.pop('data-src')
        if node.tag == 'use' and node.attrs.get('href','').startswith('#'):
            pass
    head = tree.root.find(lambda n:n.tag=='head')
    head.find(lambda n:n.tag=='title').children = fragment(('BMW Taiwan' if brand=='bmw' else 'BMW M') + ' · Unofficial visual study')
    for node in head.walk():
        if node.tag=='meta' and node.attrs.get('http-equiv','').lower()=='content-security-policy':
            node.attrs.pop('content',None)
    head.children += fragment('<meta name="robots" content="noindex"><style>' + COMMON + (BMW_CSS if brand=='bmw' else M_CSS) + '</style>')
    body = tree.root.find(lambda n:n.tag=='body')
    if brand=='bmw':
        account=body.find(lambda n:'cmp-mybmwflyout' in n.attrs.get('class','').split())
        if account:
            account.children=fragment('<div class="draft-mybmw"><h3>MyBMW</h3><a href="https://www.bmw.com.tw/zh/my-bmw.html">前往 BMW 官方 MyBMW</a></div>')
    body.children += fragment('<script>' + (BMW_JS if brand=='bmw' else M_JS) + '</script>')
    (ROOT / (brand + '.html')).write_text('<!doctype html>' + tree.root.render())
    print('Saved source-corrected draft: ' + brand)


if __name__ == '__main__':
    import sys
    for brand in sys.argv[1:] or BASES:
        refine(brand)
