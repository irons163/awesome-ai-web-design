#!/usr/bin/env python3
"""Adapt the dated public Runway source without its application/telemetry code."""
import json
import re
from html import escape
from pathlib import Path
from urllib.parse import urljoin
from official_html_tree import Tree, Node, fragment

ROOT = Path(__file__).resolve().parents[1] / '.stitch-work/current-official'
BASE = 'https://runway.com/'
CSS = '''
[hidden]{display:none!important}
.next-video-container video{display:block;width:100%;height:100%;object-fit:cover}
.draft-nav-panel{position:fixed;left:0;right:0;top:64px;background:#fff;z-index:60;padding:24px 20px;display:flex;gap:28px;flex-wrap:wrap;box-shadow:0 8px 18px #0002}
.draft-nav-panel a{color:#111;text-decoration:none}
.draft-menu{border:0;background:none;display:none;align-items:center;justify-content:center;color:inherit;padding:0 0 0 16px;cursor:pointer}
@media(max-width:1023px){.draft-menu{display:flex}.draft-nav-panel{flex-direction:column}}
[role=tab][aria-selected=false] span{opacity:.5}
[role=tab][aria-selected=true] span{opacity:1}
'''
JS = '''
const menu=document.querySelector('.draft-nav-panel');
document.querySelectorAll('[data-draft-menu]').forEach(button=>button.addEventListener('click',event=>{event.preventDefault();const open=menu.hidden;menu.hidden=!open;button.setAttribute('aria-expanded',String(open));}));
document.addEventListener('keydown',event=>{if(event.key==='Escape'){menu.hidden=true;document.querySelectorAll('[data-draft-menu]').forEach(b=>b.setAttribute('aria-expanded','false'));}});
const players=new WeakMap();
function ensurePlayback(video){const source=video.dataset.stream||video.getAttribute('src');if(!source||!source.includes('.m3u8')||video.canPlayType('application/vnd.apple.mpegurl')||!window.Hls||!Hls.isSupported()||players.has(video))return;video.dataset.stream=source;video.removeAttribute('src');const player=new Hls({capLevelToPlayerSize:true,maxBufferLength:20,backBufferLength:5});players.set(video,player);player.attachMedia(video);player.loadSource(source);player.on(Hls.Events.MANIFEST_PARSED,()=>{if(!video.closest('[hidden]')&&!matchMedia('(prefers-reduced-motion:reduce)').matches)video.play().catch(()=>{});});player.on(Hls.Events.ERROR,(_,data)=>{if(data.fatal){player.destroy();players.delete(video);const poster=video.parentElement.querySelector('[data-stream-poster]');if(poster)poster.style.visibility='visible';}});}
function playVisible(){document.querySelectorAll('video').forEach(video=>{video.muted=true;const visible=!video.closest('[hidden]');if(!visible||matchMedia('(prefers-reduced-motion:reduce)').matches){video.removeAttribute('autoplay');video.pause();const player=players.get(video);if(player)player.stopLoad();}else{ensurePlayback(video);const player=players.get(video);if(player)player.startLoad();video.play().catch(()=>{});}});}
document.querySelectorAll('video').forEach(video=>video.addEventListener('playing',()=>{const poster=video.parentElement.querySelector('[data-stream-poster]');if(poster)poster.style.visibility='hidden';}));
document.querySelectorAll('[role=tab]').forEach(tab=>{
 tab.addEventListener('click',()=>{const group=tab.closest('[data-platform-view]');group.querySelectorAll('[role=tab]').forEach(t=>{const on=t===tab;t.setAttribute('aria-selected',String(on));t.tabIndex=on?0:-1;const span=t.querySelector('span');if(span)span.style.color=on?'#fff':'#999';});group.querySelectorAll('[role=tabpanel]').forEach(p=>p.hidden=p.id!==tab.getAttribute('aria-controls'));playVisible();});
 tab.addEventListener('keydown',e=>{const keys=['ArrowLeft','ArrowRight','Home','End'];if(!keys.includes(e.key))return;e.preventDefault();const tabs=[...tab.parentElement.querySelectorAll('[role=tab]')],i=tabs.indexOf(tab);const target=e.key==='Home'?0:e.key==='End'?tabs.length-1:(i+(e.key==='ArrowRight'?1:-1)+tabs.length)%tabs.length;tabs[target].focus();tabs[target].click();});
});
document.querySelectorAll('[data-platform]').forEach(button=>button.addEventListener('click',()=>{const platform=button.dataset.platform;document.querySelectorAll('[data-platform-view]').forEach(view=>view.hidden=view.dataset.platformView!==platform);document.querySelectorAll('[data-platform]').forEach(b=>{b.setAttribute('aria-pressed',String(b===button));b.style.opacity=b===button?'1':'.5';});playVisible();}));
playVisible();
'''


def additional_platforms(tree):
    """Static content and media observed after using the official platform controls."""
    panel=tree.root.find(lambda n:n.attrs.get('id')=='creative-panel-how-used')
    card=next(n for n in tree.root.walk() if panel in n.children)
    host=next(n for n in tree.root.walk() if card in n.children)
    view=Node('div',[('data-platform-view','creative')])
    view.children=[card]
    host.children[host.children.index(card)]=view
    for slug,playback in [
        ('agent','fge4i7900DHIgUpB5rnoDMguUjeW6Mf775NtFnafD69I'),
        ('workflows','irfCRYcaqVUDBktKHI21XHi019Sy4JulAMtZiX7xSbYM'),
        ('enterprise','RLVvmVFKaTw3fBoZ8UV2zX74Dz500BSd7dUPQchkczEY'),
        ('models','el3CLGnZ9Qow0219NeHLt8SyDpnLSjcPjy6TJlP5Ubzo'),
    ]:
        poster='https://image.mux.com/'+playback+'/thumbnail.webp?time=0&amp;width=1280'
        stream='https://stream.mux.com/'+playback+'.m3u8?min_resolution=720p'
        card.children+=fragment('<div role="tabpanel" id="creative-panel-'+slug+'" aria-labelledby="creative-tab-'+slug+'" class="overflow-hidden rounded-xl" hidden><div class="relative aspect-video w-full scale-[1.01] grid"><img src="'+poster+'" class="h-full w-full min-h-0 object-cover [grid-area:1/1]" alt="" data-stream-poster><video src="'+stream+'" muted loop playsinline preload="metadata" aria-hidden="true" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover"></video></div></div>')
    devtabs=''.join('<button type="button" role="tab" id="dev-tab-'+slug+'" aria-controls="dev-panel-'+slug+'" aria-selected="'+('true' if slug=='workflows' else 'false')+'" tabindex="'+('0' if slug=='workflows' else '-1')+'" class="cursor-pointer"><span class="rw-h4">'+title+'</span></button>' for slug,title in [('workflows','Workflows'),('recipes','Recipes'),('characters','Characters')])
    media=lambda filename:'<div class="mx-auto w-full max-w-2xl overflow-hidden rounded-xl"><div class="relative aspect-square w-full scale-[1.01]"><video src="https://d3phaj0sisr2ct.cloudfront.net/devportal/landing/'+filename+'" muted loop playsinline preload="metadata" class="absolute inset-0 h-full w-full object-cover"></video></div></div>'
    workflows='<div role="tabpanel" id="dev-panel-workflows" aria-labelledby="dev-tab-workflows"><div class="grid grid-cols-1 md:grid-cols-[1fr_2fr] gap-10 lg:gap-16 mt-10"><div class="flex flex-col"><p class="rw-bodycopy1 text-white/90">Create your own pipelines combining multiple models, modalities and tasks. Trigger Workflows via custom endpoints.</p><ul class="mt-10"><li class="border-t border-white/15 py-4"><span class="rw-bodycopy3 text-white/90">Automate repetitive tasks at scale</span></li><li class="flex items-center justify-between gap-4 border-t border-white/15 py-4"><span class="rw-bodycopy3 text-white/90">Get dedicated support from Runway\'s Technical Artists for Workflow builds</span><span class="whitespace-nowrap rounded-full border border-amber-400/70 px-3 py-1 text-xs text-amber-300">Enterprise</span></li></ul></div>'+media('workflows-flow.mp4')+'</div></div>'
    recipe_data=[
        ('Product Ad','product_ad','product-ad/product-ad-poster.webp','Generate ad videos from a product photo. Ready for social, ecommerce or paid placements.','Video'),
        ('Product UGC','product_ugc','product-ugc/ugc-poster.webp','Generate vertical user-generated content ads from a character photo, product photo, and creative brief.','Video'),
        ('Product Swap','product_swap','product-swap/product-swap-poster-v2.webp','Replace the product in an existing ad video with a new product while preserving camera motion and scene composition.','Video'),
        ('Multi-Shot Video','multi_shot_video','https://d3phaj0sisr2ct.cloudfront.net/devportal/recipes/multi-shot-video-poster.jpg','Generate a multi-cut video from a story prompt or custom shot list with cohesive cinematic pacing.','Video'),
        ('Marketing Stock Image','marketing_stock_image','marketing-stock-image/marketing-poster-2.webp','Generate polished, on-brand marketing stock imagery from a text brief and an optional reference image of brand assets.','Image'),
        ('Product Campaign Image','product_campaign_image','product-campaign-image/product-campaign-poster.webp','Generate four fashion campaign images from a product photo and creative brief.','Image'),
    ]
    recipes=''.join('<a href="https://dev.runwayml.com/recipes/'+slug+'" class="group block rounded-xl bg-white/5 p-3"><div class="overflow-hidden rounded-lg"><img alt="" class="aspect-video w-full object-cover" src="'+(image if image.startswith('https:') else 'https://d3phaj0sisr2ct.cloudfront.net/devportal/playground-examples/'+image)+'"></div><div class="mt-3 flex items-center justify-between gap-3"><h4 class="rw-bodycopy2 text-white">'+title+'</h4><span class="whitespace-nowrap rounded-full bg-white/10 px-2.5 py-0.5 text-xs text-white/70">'+kind+'</span></div><p class="rw-bodycopy3 mt-2 text-darkGray">'+copy+'</p></a>' for title,slug,image,copy,kind in recipe_data)
    recipes='<div role="tabpanel" id="dev-panel-recipes" aria-labelledby="dev-tab-recipes" hidden><div class="mt-10"><div class="flex flex-col gap-4 md:flex-row md:items-start md:justify-between"><p class="rw-bodycopy1 max-w-xl text-white/90">Pre-built endpoints for specific use cases. Get professional-quality assets with one request.</p><a href="https://docs.dev.runwayml.com/recipes/" class="text-sm text-white">View documentation</a></div><div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-8">'+recipes+'</div></div></div>'
    characters='<div role="tabpanel" id="dev-panel-characters" aria-labelledby="dev-tab-characters" hidden><div class="grid grid-cols-1 md:grid-cols-[1fr_2fr] gap-10 lg:gap-16 mt-10"><div class="flex flex-col"><p class="rw-bodycopy1 text-white/90">Build expressive characters with custom voices, knowledge and tools, ready for live interaction directly from your product.</p><div class="mt-8"><a href="https://docs.dev.runwayml.com/characters/quickstart/" class="text-sm text-white">View documentation</a></div></div>'+media('characters-flow.mp4')+'</div></div>'
    host.children+=fragment('<div data-platform-view="dev" hidden><div class="overflow-hidden rounded-2xl bg-offBlack p-8 text-white lg:p-14"><div role="tablist" aria-label="Other ways to build" class="flex flex-wrap items-baseline gap-x-6 gap-y-2">'+devtabs+'</div>'+workflows+recipes+characters+'</div></div>')
    robotics=[
        ('Policy Model','product/robotics/policy-model',"Control your robot with Runway's General World Model. GWM-1 predicts actions from live observations — custom fine-tuned for your specific hardware, environment, and tasks."),
        ('Video Model Licensing','model-licensing','License GWM-1 as the diffusion backbone for training custom policy models. Deploy on your own infrastructure with full control over fine-tuning.'),
        ('Offline Policy Evaluation','product/robotics/policy-evaluation','Submit action sequences and camera observations to simulate policy rollouts in GWM-1. Surface failure modes before deploying to hardware.'),
        ('Data Augmentation','product/robotics/data-augmentation','Transform existing trajectories into new environments, lighting conditions, and object configurations. Expand your training distribution without collecting more data.'),
    ]
    cards=''.join('<a class="group flex flex-col rounded-lg border border-lightGray bg-white p-6 lg:p-8" href="'+urljoin(BASE,url)+'"><h3 class="text-2xl !leading-none mb-3">'+title+'</h3><p class="text-[16px] !leading-tight text-darkText mb-6">'+escape(copy)+'</p><span class="mt-auto inline-flex items-center gap-1.5 text-sm text-offBlack">Learn more →</span></a>' for title,url,copy in robotics)
    host.children+=fragment('<div data-platform-view="robotics" hidden><div class="rounded-2xl border border-black/10 bg-white p-8 lg:p-14"><div class="mb-2 text-sm text-darkGrayAlt">Platform</div><div class="mb-10 flex flex-col lg:mb-14 lg:flex-row lg:gap-16"><div class="mb-4 lg:mb-0 lg:w-4/12"><h2 class="text-[28px] !leading-none tracking-tight md:text-[32px] lg:text-[36px]">A complete toolkit for robot learning.</h2></div><p class="text-[16px] !leading-tight text-darkText lg:w-8/12 lg:text-[18px]">From policy inference and evaluation to synthetic data generation, every component is powered by GWM-1, our state-of-the-art General World Model. Pick the surface you need — we\'ll work with you to fit it to your hardware.</p></div><div class="grid grid-cols-1 md:grid-cols-2 gap-4 lg:gap-6">'+cards+'</div></div></div>')
    for n in tree.root.walk():
        if n.tag=='button':
            text=re.sub('<[^>]*>','',n.render()).strip()
            if text in ['Runway Creative','Runway Dev','Runway Robotics']:
                slug=text.split(' ')[1].lower()
                n.attrs.update({'data-platform':slug,'aria-pressed':'true' if slug=='creative' else 'false'})
        if n.attrs.get('role')=='tab':
            n.attrs['tabindex']='0' if n.attrs.get('aria-selected')=='true' else '-1'


def main():
    provenance=json.loads((ROOT/'runwayml-asset-provenance.json').read_text())
    assets={a['source_url']:a['path'] for a in provenance['assets']}
    tree=Tree((ROOT/'runwayml-source-current.html').read_text())
    def clean(node):
        node.children=[c for c in node.children if c.tag not in ('script','iframe','noscript','template')]
        node.attrs={k:v for k,v in node.attrs.items() if not k.startswith('on')}
        for child in node.children:
            clean(child)
    clean(tree.root)
    additional_platforms(tree)
    streams=json.loads((ROOT/'runwayml-browser-source.json').read_text())['observed_streams']
    inserted=set()
    def add_video(node):
        for child in list(node.children):
            if child.tag=='img':
                values=str(child.attrs)
                playback=next((key for key in streams if key in values),None)
                if playback and playback not in inserted and not any(c.tag=='video' for c in node.children):
                    inserted.add(playback)
                    child.attrs['data-stream-poster']=''
                    video=Node('video',[('src',streams[playback]),('muted',''),('autoplay',''),('loop',''),('playsinline',''),('preload','metadata'),('aria-hidden','true'),('style','position:absolute;inset:0;width:100%;height:100%;object-fit:cover')])
                    node.children.insert(0,video)
            add_video(child)
    add_video(tree.root)
    for n in tree.root.walk():
        if n.tag=='link' and n.attrs.get('as')=='script':
            n.attrs['rel']='nofollow'
            n.attrs.pop('as',None)
            n.attrs.pop('href',None)
        for name in ['src','href','poster']:
            value=n.attrs.get(name)
            if value and not value.startswith(('#','data:','mailto:','tel:')):
                absolute=urljoin(BASE,value)
                n.attrs[name]=assets.get(absolute,absolute)
        if n.attrs.get('srcset') and not n.attrs['srcset'].startswith('data:'):
            n.attrs['srcset']=', '.join(urljoin(BASE,p.strip().split(' ')[0])+(' '+p.strip().split(' ',1)[1] if ' ' in p.strip() else '') for p in n.attrs['srcset'].split(','))
        if n.tag=='style':
            for text in n.children:
                if text.text is None: continue
                def rewrite(m):
                    value=m.group(1).strip().strip('\'"')
                    if value.startswith(('data:','#')): return m.group(0)
                    absolute=urljoin(BASE,value)
                    return 'url("'+assets.get(absolute,absolute)+'")'
                text.text=re.sub(r'url\(([^)]+)\)',rewrite,text.text)
        if n.tag=='mux-video':
            # Native HLS where available; the original poster remains the fallback.
            n.tag='video'
            n.attrs['muted']=''
            if not n.attrs.get('src') and n.attrs.get('playback-id'):
                # Only use the publicly observed stream spelling for these IDs.
                streams=json.loads((ROOT/'runwayml-browser-source.json').read_text())['observed_streams']
                if n.attrs['playback-id'] in streams:
                    n.attrs['src']=streams[n.attrs['playback-id']]
            n.attrs['preload']='metadata'
    head=tree.root.find(lambda n:n.tag=='head')
    head.find(lambda n:n.tag=='title').children=fragment('Runway · Unofficial visual study')
    head.children+=fragment('<meta name="robots" content="noindex"><link rel="license" href="runwayml-assets/hls-LICENSE"><style>'+CSS+'</style>')
    body=tree.root.find(lambda n:n.tag=='body')
    header=body.find(lambda n:n.tag=='header')
    nav=header.find(lambda n:n.tag=='nav')
    for n in nav.walk():
        if n.tag=='a' and n.attrs.get('aria-haspopup'):
            n.attrs['data-draft-menu']=''
    trigger=header.find(lambda n:n.tag=='div' and 'lg:hidden' in n.attrs.get('class',''))
    trigger.tag='button'
    trigger.attrs.update({'type':'button','aria-label':'Menu','aria-expanded':'false','data-draft-menu':''})
    links=[('Creative','product'),('Dev','https://dev.runwayml.com/'),('Robotics','product/robotics'),('Research','research'),('Resources','resources'),('Enterprise','enterprise'),('Pricing','pricing')]
    body.children+=fragment('<nav class="draft-nav-panel" aria-label="Menu" hidden>'+''.join('<a href="'+urljoin(BASE,url)+'">'+label+'</a>' for label,url in links)+'</nav><script src="runwayml-assets/hls.light.min.js"></script><script>'+JS+'</script>')
    (ROOT/'runwayml.html').write_text('<!doctype html>'+tree.root.render())
    print('Saved Runway source-aligned draft')


if __name__=='__main__':
    main()
