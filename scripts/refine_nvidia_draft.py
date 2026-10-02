#!/usr/bin/env python3
"""Adapt NVIDIA's dated public HTML, preserving its own markup and styles.

Native Stitch exports remain unchanged alongside this source-calibrated draft.
Large first-party media stays on NVIDIA's CDN; fonts and CSS are local.
"""
from pathlib import Path
from urllib.parse import urljoin
import hashlib
import json
import re
from official_html_tree import Tree, fragment

ROOT = Path(__file__).resolve().parents[1] / '.stitch-work/current-official'
BASE = 'https://www.nvidia.com/en-us/'

SCRIPT = r'''
const hero=document.querySelector('#home-wmfg-carousel');
const slides=[...hero.querySelectorAll('[data-cmp-hook-carousel="item"]')];
const tabs=[...hero.querySelectorAll('.progressBox')];
let current=0;
function selectSlide(index){
 current=(index+slides.length)%slides.length;
 slides.forEach((s,i)=>{s.classList.toggle('cmp-carousel__item--active',i===current);s.setAttribute('aria-hidden',String(i!==current));});
 const light=tabs[current].dataset.theme.toLowerCase()==='white';
 tabs.forEach((t,i)=>{t.setAttribute('aria-selected',String(i===current));t.querySelector('.progress_filled').style.width=i===current?'100%':'0%';t.querySelectorAll('.progressLabel,.progressDescription').forEach(x=>{x.classList.toggle('black',!light);x.classList.toggle('White',light);});});
}
tabs.forEach((t,i)=>{t.addEventListener('click',()=>selectSlide(i));t.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();selectSlide(i);}else if(e.key==='ArrowRight'){e.preventDefault();selectSlide(current+1);tabs[current].focus();}else if(e.key==='ArrowLeft'){e.preventDefault();selectSlide(current-1);tabs[current].focus();}});});
selectSlide(0);
const toggle=document.querySelector('#menu-toggle');
const mobile=document.querySelector('.mobile-nav');
if(toggle&&mobile){
 const setMenu=open=>{toggle.setAttribute('aria-expanded',String(open));mobile.classList.toggle('meganav-open',open);mobile.querySelector('.mega-menu').classList.toggle('hide',!open);document.body.classList.toggle('draft-menu-open',open);document.body.style.overflow=open?'hidden':'';document.querySelector('#mega-nav-open-menu-icon').classList.toggle('hide',open);document.querySelector('#mega-nav-close-menu-icon').classList.toggle('hide',!open);};
 toggle.addEventListener('click',()=>setMenu(toggle.getAttribute('aria-expanded')!=='true'));
 document.addEventListener('keydown',e=>{if(e.key==='Escape')setMenu(false)});
}
document.querySelectorAll('.accordion-menu .submenu').forEach(panel=>panel.hidden=true);
document.querySelectorAll('.accordion-menu .accordion-btn').forEach(b=>b.addEventListener('click',()=>{const open=b.getAttribute('aria-expanded')!=='true';b.setAttribute('aria-expanded',String(open));const panel=b.nextElementSibling;if(panel){panel.hidden=!open;panel.style.display=open?'block':'none';b.closest('.menu-item').classList.toggle('open',open);}}));
document.querySelectorAll('.cmp-carousel:not(#home-wmfg-carousel)').forEach(row=>{
 const content=row.querySelector('.cmp-carousel__content'),track=row.querySelector('.cmp-carousel__slides');if(!content||!track)return;
 const intro=track.querySelector('[data-cmp-hook-carousel="item"]');
 const layout=()=>{if(innerWidth<768){if(intro.parentElement===track)content.insertBefore(intro,track);}else if(intro.parentElement!==track)track.prepend(intro);};
 layout();addEventListener('resize',layout);
 row.querySelectorAll('[data-cmp-hook-carousel="next"]').forEach(b=>b.addEventListener('click',()=>track.scrollBy({left:innerWidth<768?330:440,behavior:'smooth'})));
 row.querySelectorAll('[data-cmp-hook-carousel="previous"]').forEach(b=>b.addEventListener('click',()=>track.scrollBy({left:innerWidth<768?-330:-440,behavior:'smooth'})));
});
document.querySelectorAll('.cmp-teaser__quick-links').forEach(button=>button.addEventListener('click',()=>{const open=button.getAttribute('aria-expanded')!=='true';button.setAttribute('aria-expanded',String(open));button.parentElement.querySelector('.quick-links-box').classList.toggle('hide',!open)}));
'''

CSS = '''
[hidden]{display:none!important}
#home-wmfg-carousel [aria-hidden="true"]{display:none!important}
#home-wmfg-carousel .cmp-carousel__indicators{display:none}
#home-wmfg-carousel .progress_filled{transition:width .25s}
#home-wmfg-carousel .progressContainer{padding:0 0 10px}
.draft-menu-open #mega-nav{display:block!important;visibility:visible!important;opacity:1!important;position:fixed;inset:45px 0 0;overflow:auto;background:white;z-index:999}
.draft-menu-open #mega-nav .mega-menu{left:0!important;min-height:calc(100dvh - 45px)}
.draft-menu-open .accordion-menu .menu-item.open>.submenu{display:block!important;max-height:none!important;visibility:visible}
body{overflow-x:hidden;padding-top:45px}
.cmp-carousel:not(#home-wmfg-carousel) .cmp-carousel__slides{overflow-x:auto;scrollbar-width:none}
.cmp-carousel:not(#home-wmfg-carousel) .cmp-carousel__slides::-webkit-scrollbar{display:none}
@media(min-width:1024px){.cmp-carousel:not(#home-wmfg-carousel) .cmp-carousel__slides>.cmp-carousel__item{width:410px;flex:0 0 410px}.cmp-carousel:not(#home-wmfg-carousel) .cmp-carousel__slides>.cmp-carousel__item:first-child{width:520px;flex-basis:520px}}
@media(max-width:767px){.cmp-carousel:not(#home-wmfg-carousel) .cmp-carousel__slides>.cmp-carousel__item{width:300px;flex:0 0 300px}.cmp-carousel:not(#home-wmfg-carousel) .cmp-carousel__content>.cmp-carousel__item{width:calc(100% - 30px);margin:0 15px}.cmp-carousel:not(#home-wmfg-carousel) .cmp-carousel__slides>.cmp-carousel__item:first-child{margin-left:15px}}
'''


def main():
    provenance = json.loads((ROOT/'nvidia-asset-provenance.json').read_text())
    assets = provenance['assets']
    local = {a['source_url']: a['path'] for a in assets}
    css_records = []
    styles = {}
    for asset in assets:
        if asset['kind'] != 'stylesheet':
            continue
        source = ROOT/asset['path']
        target = source.with_suffix('.local.css')
        original = source.read_text()
        def css_url(match):
            value = match.group(1).strip().strip('"\'')
            if value.startswith(('data:', '#')):
                return match.group(0)
            url = urljoin(asset['source_url'], value)
            return 'url("'+(Path(local[url]).name if url in local else url)+'")'
        target.write_text(re.sub(r'url\(\s*([^)]+)\s*\)', css_url, original))
        styles[asset['source_url']] = target.relative_to(ROOT).as_posix()
        css_records.append({'source_url':asset['source_url'],'source_sha256':asset['sha256'],
                            'path':target.relative_to(ROOT).as_posix(),
                            'sha256':hashlib.sha256(target.read_bytes()).hexdigest()})
    tree = Tree((ROOT/'nvidia-source-current.html').read_text())
    def clean(node):
        children = []
        for child in node.children:
            if child.tag in ('script','iframe'):
                continue
            if child.tag == 'noscript':
                # AEM's real article images are lazy-loaded from this fallback.
                children.extend(c for c in child.children
                                if c.tag == 'img' and 'cmp-image__image' in c.attrs.get('class',''))
            else:
                children.append(child)
        node.children = children
        for key in list(node.attrs):
            if key.startswith('on'):
                del node.attrs[key]
        for child in node.children:
            clean(child)
    clean(tree.root)
    for node in tree.root.walk():
        classes = node.attrs.get('class', '').split()
        if 'progressDescription' in classes:
            node.attrs['class'] += ' two_row'
        if 'account-icon-loading' in classes:
            node.attrs['class'] = ' '.join(c for c in classes if c != 'account-icon-loading')
        if node.tag == 'picture':
            for child in node.children:
                for device in ('mobile','tablet','laptop','desktop'):
                    value = node.attrs.get('data-srcset-'+device)
                    if value and 'data-source-'+device in child.attrs:
                        child.attrs['srcset'] = value
                if child.tag == 'img':
                    value = node.attrs.get('data-srcset-laptop') or node.attrs.get('data-srcset-desktop') or node.attrs.get('data-srcset-mobile')
                    if value:
                        child.attrs['src'] = value.split(',')[0].strip().split(' ')[0]
        if node.tag == 'img' and node.attrs.get('data-src'):
            node.attrs['src'] = node.attrs.pop('data-src')
        for key in ('href','src','poster','action'):
            value = node.attrs.get(key)
            if not value or value.startswith(('data:', '#', 'mailto:', 'tel:')):
                continue
            url = urljoin(BASE,value)
            node.attrs[key] = styles.get(url,local.get(url,url))
        if 'srcset' in node.attrs:
            value=node.attrs['srcset']
            if not value.startswith('data:'):
                node.attrs['srcset'] = ', '.join(urljoin(BASE,item.strip().split(' ')[0]) +
                     (' '+item.strip().split(' ',1)[1] if ' ' in item.strip() else '')
                     for item in value.split(','))
        if node.tag == 'link' and node.attrs.get('rel') in ('preconnect','dns-prefetch','preload'):
            node.attrs['rel'] = 'nofollow'
    head = tree.root.find(lambda n:n.tag=='head')
    body = tree.root.find(lambda n:n.tag=='body')
    title = head.find(lambda n:n.tag=='title')
    title.children = fragment('NVIDIA · Unofficial visual study')
    fonts = ''.join('<link rel="preload" as="font" type="font/woff2" crossorigin href="'+a['path']+'">'
                    for a in assets if a['kind']=='font')
    head.children += fragment('<meta name="robots" content="noindex">'+fonts+'<style>'+CSS+'</style>')
    body.children += fragment('<script>'+SCRIPT+'</script>')
    output = '<!doctype html>'+tree.root.render()
    (ROOT/'nvidia.html').write_text(output)
    (ROOT/'nvidia-local-css.json').write_text(json.dumps(css_records,indent=2)+'\n')
    print('Saved NVIDIA source-backed draft with',len(assets),'official CSS/font assets')


if __name__ == '__main__':
    main()
