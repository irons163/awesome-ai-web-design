#!/usr/bin/env python3
"""Calibrate the real Stitch drafts against the observed 2026-10-03 x.ai page.

Uses the official XVF/Geist fonts, utility CSS, photos, wordmark and orb renderer.
The HTTP challenge is retained separately; it is not used as page source.
"""
from pathlib import Path
from urllib.parse import urljoin
from html import escape
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1] / '.stitch-work/current-official'
BASE = 'https://x.ai/'
WRAP = 'mx-auto w-full px-4 lg:px-6 xl:max-w-7xl'
SECTION = WRAP + ' py-16 sm:py-24'
WORDMARK = '''<svg width="205" height="25" viewBox="0 0 1294 158" fill="currentColor" xmlns="http://www.w3.org/2000/svg" aria-label="SpaceXAI"><path fill-rule="evenodd" clip-rule="evenodd" d="M331.027 83.6049C331.027 67.2845 317.318 58.0969 295.467 58.0969H188.967V157.661H218.997V119.471H297.358C319.228 119.471 331.027 111.887 331.027 94.5399V83.6049ZM218.997 101.241H291.846C303.645 101.241 304.96 97.2963 304.96 90.1626V86.2536C304.96 79.2465 303.213 75.4632 290.387 75.4632H219.177L218.997 101.241Z"/><path d="M495.676 157.644H459.882L443.994 135.847H351.382L367.289 118.86H431.636L400.669 76.3459L418.954 53.8642L495.676 157.644Z"/><path d="M115.163 58.0969C131.772 58.0969 141.248 66.2575 144.166 75.4627H33.0911V96.8814H119.235C136.564 97.8902 147.066 105.312 147.066 119.309V135.198C147.066 150.654 137.897 157.643 119.523 157.643H31.632C14.8789 157.643 5.25904 151.374 2.48486 138.944H119.991V116.175H32.6585C16.482 116.265 5.54735 108.825 5.54725 95.7107V79.9662C5.54725 64.9424 16.1759 58.0969 34.6944 58.0969H115.163Z"/><path d="M635.773 58.0788C651.806 58.0789 663.173 63.6274 666.091 75.4447H553.394V138.944H666.091C662.885 152.113 656.021 157.643 636.638 157.643H551.377C536.659 157.643 522.806 151.662 522.806 135.774V79.9481C522.806 64.0597 536.659 58.0789 551.377 58.0788H635.773Z"/><path d="M798.637 108.587H738.037V138.941H841.925V157.64H707.485V91.5281H798.637V108.587Z"/><path d="M843.348 75.4627H707.485V58.0969H843.348V75.4627Z"/><path d="M1291.42 0.485005C1243.91 4.35808 1057.2 27.5063 927.728 157.658H879.684L885.052 152.308C912.145 126.134 1032.03 15.2025 1291.42 0.34082V0.485005Z"/><path d="M1128.81 157.658H1091.16L1016.96 103.651C1023.8 99.3515 1030.68 95.2564 1037.58 91.3564L1128.81 157.658Z"/><path d="M1068.63 157.659H1030.99L1019.58 149.354H955.827C960.315 145.369 964.859 141.5 969.45 137.745H1003.6L985.926 124.891C992.242 120.191 998.628 115.689 1005.07 111.377L1068.63 157.659Z"/><path d="M931.636 58.0739L960.66 79.1672C953.437 83.4208 946.676 87.6309 940.365 91.7495L894.029 58.0558L931.636 58.0739Z"/></svg>'''

CODE = {
    'Python': '''import os
from xai_sdk import Client
from xai_sdk.chat import user

client = Client(
    api_key=os.getenv("XAI_API_KEY")
)

chat = client.chat.create(model="grok-4.7")
chat.append(user("Explain quantum computing"))

response = chat.sample()
print(response.content)''',
    'TypeScript': '''import { xai } from "@ai-sdk/xai";
import { generateText } from "ai";

const { text } = await generateText({
  model: xai.responses("grok-4.7"),
  prompt: "Explain quantum computing",
});

console.log(text);''',
    'TypeScript (OpenAI SDK)': '''import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.XAI_API_KEY,
  baseURL: "https://api.x.ai/v1",
});

const response = await client.chat.completions.create({
  model: "grok-4.7",
  messages: [{ role: "user", content: "Explain quantum computing" }],
});

console.log(response.choices[0].message.content);''',
    'cURL': '''curl https://api.x.ai/v1/chat/completions \\
  -H "Authorization: Bearer $XAI_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
    "model": "grok-4.7",
    "messages": [
      { "role": "user", "content": "Explain quantum computing" }
    ]
  }' '''.rstrip(),
}

GROUPS = [
    ('Products', [('Chat','/grok'),('Build','/build'),('Imagine','/api/imagine'),('Voice','/voice'),('Bot','/bot'),('Grokipedia','https://grokipedia.com')]),
    ('Download', [('Web','https://grok.com'),('iOS','https://apps.apple.com/app/apple-store/id6670324846'),('Android','https://play.google.com/store/apps/details?id=ai.x.grok'),('Grok on X','https://x.com/i/grok')]),
    ('Solutions', [('Business','/grok/business'),('Government','/grok/government'),('Customer Support','/solutions/customer-support'),('Legal','/solutions/legal'),('Security','/solutions/security'),('Use Cases','/grok/use-cases')]),
    ('Grok Bot', [('Overview','/bot'),('Marketplace','/bot/marketplace'),('Guides','/bot/guides'),('Use Cases','/bot/use-cases'),('Changelog','/changelog/bot')]),
    ('Developers', [('API Overview','/api'),('Pricing','/pricing'),('Models','https://docs.x.ai/developers/models'),('Console','https://console.x.ai'),('Changelog','/api/changelog'),('Docs','https://docs.x.ai'),('Status','https://status.x.ai')]),
    ('Enterprise', [('Contact Sales','/contact-sales'),('FAQs','/legal/faq-enterprise'),('BAA','/legal/baa'),('DPA','/legal/data-processing-addendum')]),
    ('Company', [('About','/company'),('Colossus','/colossus'),('Careers','/careers'),('News','/news'),('Contact','/contact')]),
    ('Trust', [('Safety','/safety'),('Security','/security'),('Privacy Portal','/privacy-portal'),('Subprocessors','/legal/subprocessor-list'),('Help Center','https://docs.x.ai/grok/user-guide')]),
    ('Legal', [('Terms','/legal/terms-of-service'),('Enterprise Terms','/legal/terms-of-service-enterprise'),('Privacy','/legal/privacy-policy'),('Cookies','/legal/cookie-policy'),('Acceptable Use Policy','/legal/acceptable-use-policy'),('Brand','/legal/brand-guidelines')]),
    ('Social', [('@SpaceXAI','https://x.com/spacexai'),('@grok','https://x.com/grok'),('Discord','https://discord.com/invite/kqCc86jM55')]),
]

CSS = '''
[hidden]{display:none!important}button,a{touch-action:manipulation}
.xai-header{position:fixed;inset:0 0 auto;z-index:50;background:rgba(255,255,255,.85);backdrop-filter:blur(12px)}
.xai-nav{display:flex;align-items:center;justify-content:space-between;gap:40px;height:64px}
.xai-brand{width:51px;flex-shrink:0}.xai-brand img{width:51px;height:32px}
.xai-nav-links{display:flex;align-items:center;gap:30px;flex:1;font-size:14px}
.xai-nav-links button{white-space:nowrap}.xai-nav-links button::after{content:'⌄';font-size:13px;margin-left:5px}
.xai-actions{display:flex;gap:8px;align-items:center}.xai-actions .pill{font-size:14px;padding:9px 18px}
.pill{display:inline-flex;align-items:center;justify-content:center;font-size:14px;font-weight:500;line-height:20px;padding:12px 20px;border-radius:999px;background:#f0f0ef;white-space:nowrap}
.pill-hero-pt .pill.solid{width:159.2109375px}.pill-hero-pt .pill:not(.solid){width:176.625px}
.pill.solid{background:#0a0a0a;color:white}.pill.small{padding:10px 18px}.try-split{display:flex;border-radius:50px;overflow:hidden;background:#0a0a0a;color:white;font-size:14px}
.try-split>a{padding:9px 16px}.try-split>button{width:36px;border-left:1px solid #ffffff26}
.xai-mobile-toggle{display:none;align-items:center;justify-content:center;width:52px;height:52px;border-radius:50%;background:#f0f0ef}
.menu-bars{width:16px;height:10px;border-top:1.5px solid;border-bottom:1.5px solid}.menu-bars:after{content:'';display:block;border-top:1.5px solid;margin-top:3px}
.xai-menu{position:fixed;inset:64px 0 auto;z-index:60;background:white;border-top:1px solid #eee;padding:30px;max-height:calc(100dvh - 64px);overflow:auto}
.xai-menu .menu-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:40px;max-width:1232px;margin:auto}
.xai-menu h3{font-size:12px;color:#777;margin-bottom:16px}.xai-menu a{display:block;font-size:18px;margin-bottom:12px}
.hero-word{border-bottom:3px solid #c8c8c8;position:relative}.product-label{position:absolute;inset:auto 0 0;z-index:20;display:flex;justify-content:space-between;align-items:end;padding:24px 16px 16px;font-size:14px;font-weight:400}
.product-shade{position:absolute;inset:auto 0 0;height:64px;z-index:10;background:linear-gradient(transparent,hsl(var(--card)) 90%)}
.build-card{--card:0 0% 8%;color:#f3eee7}.build-preview{position:absolute;inset:0;padding:20px;font-family:var(--font-geist-mono);font-size:10.5px;line-height:18px;color:#9d9d9d}
.build-preview .prompt{color:#e2e2e2;margin:8px 0}.build-preview .command{color:#87a6ff}.build-preview .run{color:#cfb47c}.build-preview .done{color:#9ece6a}
.build-preview .task{display:flex;justify-content:space-between;border-left:2px solid #555;margin-top:7px;padding-left:10px}
.imagine-grid{display:grid;grid-template-columns:minmax(0,2fr) minmax(0,1fr);grid-template-rows:repeat(2,minmax(0,1fr));gap:3px;height:100%}.imagine-grid img{width:100%;height:100%;min-height:0;object-fit:cover;border-radius:4px}.imagine-grid img:first-child{grid-row:span 2}
.voice-shell{position:relative;width:218px;height:218px;border-radius:50%;overflow:hidden;clip-path:circle(50% at 50% 50%)}
.voice-shell canvas{width:100%;height:100%;display:block}.voice-chrome{position:absolute;inset:0;border-radius:50%;pointer-events:none;opacity:.35;box-shadow:inset 0 1px 1px #ffffffb3,inset 0 -1px 1px #ffffff73,inset 0 0 0 1px #ffffff38,inset 0 0 13.1px #ffffff2e}
.code-background{background-color:#E04A26;background-image:radial-gradient(circle at 59.815662230565835% 61.935103519200446%,#FF9C6A 0%,transparent 36%),radial-gradient(circle at 38.10742708391736% 56.962326997879266%,#FF7A45 0%,transparent 34%),radial-gradient(circle at 52.962326997879266% 30.305776620824613%,#FFEFE6 0%,transparent 38%),linear-gradient(7.562874804775114deg,#E04A26 0%,#B42A1E 100%)}
.code-window-chrome{background:#fff;color:#24292e}.code-header{display:flex;justify-content:end;height:41px;border-bottom:1px solid #ddd;padding:12px 16px;font-size:12px;line-height:16px;color:#888}
main>section:first-of-type .grid>div{min-width:0}
.code-window-scroll{height:280px;overflow:auto;padding:12px 0}.code-window-scroll pre{padding:0 16px;line-height:19.5px;font-size:13px;font-family:var(--font-geist-mono);white-space:pre}
.code-tabs button[aria-selected=true]{background:#f4f4f4;color:#0a0a0a}.code-tabs button{color:#666}
.number-static{display:inline-block;line-height:1em;padding:.25em 0;font-kerning:none}.footer-group h3{font-size:13px;line-height:19.5px;font-weight:500;margin-bottom:6px;color:#111}.footer-group ul{display:flex;flex-direction:column;gap:4px;font-size:13px;line-height:19.5px;color:#555}.footer-group a:hover{color:#000}
@media(max-width:1023px){.xai-nav{height:84px;gap:16px;padding:16px}.xai-brand{margin-left:8px}.xai-nav-links,.xai-actions{display:none}.xai-mobile-toggle{display:flex}.xai-menu{inset:84px 0 0;max-height:none;padding:24px}.xai-menu .menu-grid{grid-template-columns:1fr 1fr;gap:32px}.voice-shell{width:172px;height:172px}}
@media(min-width:640px) and (max-width:1023px){.voice-shell{width:218px;height:218px}}
'''

SCRIPT = r'''
const menu=document.querySelector('#xai-menu'),toggle=document.querySelector('#xai-mobile-toggle');
function setMenu(open,section){menu.hidden=!open;toggle.setAttribute('aria-expanded',String(open));document.body.style.overflow=open?'hidden':'';if(section)menu.dataset.section=section;}
toggle.addEventListener('click',()=>setMenu(menu.hidden));
document.querySelectorAll('[data-menu]').forEach(b=>b.addEventListener('click',()=>setMenu(menu.hidden,b.dataset.menu)));
document.addEventListener('keydown',e=>{if(e.key==='Escape')setMenu(false)});
const tabs=[...document.querySelectorAll('.code-tabs button')],panels=[...document.querySelectorAll('[data-code-panel]')];
tabs.forEach((t,i)=>t.addEventListener('click',()=>{tabs.forEach((b,j)=>b.setAttribute('aria-selected',String(i===j)));panels.forEach((p,j)=>p.hidden=i!==j)}));
document.querySelector('#copy-code').addEventListener('click',async e=>{try{await navigator.clipboard.writeText(panels.find(p=>!p.hidden).textContent);e.currentTarget.textContent='Copied';setTimeout(()=>document.querySelector('#copy-code').textContent='Copy',1800)}catch{e.currentTarget.textContent='Select code to copy'}});
const metricTargets=[400,200,122];
const metricObserver=new IntersectionObserver(entries=>{entries.forEach(entry=>{if(!entry.isIntersecting)return;const n=entry.target;const i=[...document.querySelectorAll('.number-static')].indexOf(n);n.textContent=metricTargets[i];metricObserver.unobserve(n)})},{threshold:.5});
document.querySelectorAll('.number-static').forEach(n=>metricObserver.observe(n));
const shell=document.querySelector('.voice-shell'),canvas=shell.querySelector('canvas');
const hash=officialOrb.hashSeed('voice-preview');
const rgb=officialOrb.toRGB;
const spec={bg:rgb('#FFFFFF'),anchor:rgb('#131A2E'),accents:['#3B82F6','#8B5CF6','#EC4899'].map(rgb),phase:hash%6283/1000,arch:(hash>>>16)%4,seed:'voice-preview',lens:.4,audioSmooth:0,audioFast:0,spinDir:1,spinVel:0,prevA:0,flipQueued:false,oscSign:1,spin:hash%6283/1000*3.7,lastT:null};
const gl=canvas.getContext('webgl',officialOrb.GL_CONTEXT_OPTS);
if(gl){
 const renderer=new officialOrb.OrbRenderer(canvas,gl);let visible=true,time=0,last=null;
 const resize=()=>{const size=Math.round(shell.clientWidth*Math.min(2,devicePixelRatio||1));canvas.width=size;canvas.height=size;renderer.render(spec,size,time)};
 new ResizeObserver(resize).observe(shell);resize();
 new IntersectionObserver(([entry])=>{visible=entry.isIntersecting;last=null}).observe(shell);
 const reduced=matchMedia('(prefers-reduced-motion:reduce)').matches;
 function frame(now){if(visible){if(last!==null&&!reduced)time+=Math.min(100,now-last)/1000;last=now;renderer.render(spec,canvas.width,time)}requestAnimationFrame(frame)}requestAnimationFrame(frame);
}
'''


def url(value):
    return escape(urljoin(BASE, value), quote=True)


def main():
    prov = json.loads((ROOT/'x.ai-asset-provenance.json').read_text())
    assets = prov['assets']
    local = {a['source_url']:a['path'] for a in assets}
    styles = []
    derived = []
    for a in assets:
        if a['kind'] != 'stylesheet':
            continue
        source = ROOT/a['path']
        target = source.with_suffix('.local.css')
        def css_url(m):
            value = m.group(1).strip().strip('"\'')
            if value.startswith(('data:', '#')):
                return m.group(0)
            absolute = urljoin(a['source_url'], value)
            return 'url("'+(Path(local[absolute]).name if absolute in local else absolute)+'")'
        target.write_text(re.sub(r'url\(\s*([^)]+)\s*\)', css_url, source.read_text()))
        styles.append('<link rel="stylesheet" href="'+target.relative_to(ROOT).as_posix()+'">')
        derived.append({'source_url':a['source_url'],'source_sha256':a['sha256'],'path':target.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(target.read_bytes()).hexdigest()})
    (ROOT/'x.ai-local-css.json').write_text(json.dumps(derived,indent=2)+'\n')
    (ROOT/'x.ai-assets/spacexai-wordmark.svg').write_text(WORDMARK)
    # The header is the same source wordmark cropped to its actual symbol region.
    (ROOT/'x.ai-assets/spacexai-symbol.svg').write_text(WORDMARK.replace('viewBox="0 0 1294 158"','viewBox="879 0 415 158"'))
    brand_provenance = {
        'source_url': 'https://x.ai/',
        'observed_at': '2026-10-03',
        'capture_method': 'Visible official page DOM; inline SVG path geometry retained',
        'assets': [
            {
                'path': 'x.ai-assets/'+name,
                'sha256': hashlib.sha256((ROOT/'x.ai-assets'/name).read_bytes()).hexdigest(),
                'changes': changes,
            }
            for name, changes in [
                ('spacexai-wordmark.svg', ['Standalone SVG with local dimensions and accessible label']),
                ('spacexai-symbol.svg', ['Same wordmark paths; viewBox cropped to the header symbol region']),
            ]
        ],
    }
    (ROOT/'x.ai-brand-provenance.json').write_text(json.dumps(brand_provenance,indent=2)+'\n')
    images = {a['source_url'].split('/')[-1]:a['path'] for a in assets if a['kind']=='image'}
    preload = ''.join('<link rel="preload" as="font" type="font/woff2" crossorigin href="'+a['path']+'">' for a in assets if a['kind']=='font')
    nav = ''.join('<button type="button" data-menu="'+n+'">'+n+'</button>' for n in ['Products','Solutions','Developer','Company'])
    nav += '<a href="https://x.ai/pricing">Pricing</a><a href="https://x.ai/news">News</a>'
    menu = ''.join('<div><h3>'+name.upper()+'</h3>'+''.join('<a href="'+url(href)+'">'+escape(label)+'</a>' for label,href in links)+'</div>' for name,links in GROUPS[:8])
    chat = ''.join('<div class="flex justify-'+('end' if i%2==0 else 'start')+'"><div class="max-w-[82%] rounded-2xl px-3.5 py-2 text-[10.5px] leading-relaxed bg-primary/['+('0.08' if i%2==0 else '0.04')+'] text-primary rounded-b'+('r' if i%2==0 else 'l')+'-md">'+escape(t)+'</div></div>' for i,t in enumerate([
      'Explain quantum entanglement simply','Two particles become linked — measuring one instantly determines the other, regardless of distance.','Why is the sky blue?','Shorter blue wavelengths scatter more off air molecules than longer red ones.','How do black holes form?']))
    label = lambda name:'<div class="product-label"><span>'+name+'</span><span>Explore →</span></div>'
    cardclass = 'bg-card group/card relative flex h-[220px] overflow-hidden rounded-2xl sm:h-[280px] '
    cards = '<a href="https://x.ai/grok" class="'+cardclass+'sm:col-span-2"><div class="relative flex h-full flex-col justify-end gap-2.5 overflow-hidden px-5 pt-3 pb-14">'+chat+'</div><div class="product-shade"></div>'+label('Chat')+'</a>'
    build = '''<div class="build-preview"><div>projects/main | <span class="command">11.60%</span> |</div><div class="prompt">❯ Migrate auth from sessions to JWT.</div><p>Thinking...</p><p><span class="command">▸ read_file</span> src/middleware/auth.ts <span>68 lines</span></p><p><span class="command">▸ grep</span> "session" src/ <span>4 matches</span></p><p><span class="command">▸ read_file</span> src/lib/jwt.ts <span>42 lines</span></p><div class="task"><span>Audit auth middleware</span><span>explore <span class="run">[running]</span></span></div><div class="task"><span>Design token rotation</span><span>general <span class="run">[running]</span></span></div><div class="task"><span>Find session references</span><span>explore <span class="done">[done]</span></span></div><p class="command">◆ Thought for 4.1s</p></div>'''
    cards += '<a href="https://x.ai/build" class="'+cardclass+'sm:col-span-2 build-card">'+build+'<div class="product-shade"></div>'+label('Build')+'</a>'
    cards += '<a href="https://x.ai/bot" class="'+cardclass+'sm:col-span-2"><div class="baby-grok-bot-transcript"></div>'+label('Bot')+'</a>'
    cards += '<a href="https://x.ai/api/imagine" class="'+cardclass+'sm:col-span-3 p-1"><div class="relative flex-1 overflow-hidden rounded-xl"><div class="imagine-grid">'+''.join('<img alt="" src="'+images[n]+'">' for n in ['nav-1-a43d837c.jpg','nav-7-9d816d41.jpg','nav-8-b74b9ad6.jpg'])+'</div><div class="product-label text-white">'+label('Imagine').replace('<div class="product-label">','').removesuffix('</div>')+'</div></div></a>'
    cards += '<a href="https://x.ai/voice" class="'+cardclass+'sm:col-span-3"><div class="flex h-full w-full items-center justify-center"><div class="voice-shell" aria-hidden="true"><canvas></canvas><div class="voice-chrome"></div></div></div><div class="product-shade"></div>'+label('Voice')+'</a>'
    news_data = [
      ('grok-4-7','grok-4-7-og.webp','2026-09-21','Sep 21, 2026','Introducing Grok 4.7',True),
      ('team-bots','team-bots-og-d3e412bc.webp','2026-09-28','Sep 28, 2026','Team Bots: shared AI teammates that learn as they work',True),
      ('grok-bot-customer-support','grok-bot-customer-support-og.webp','2026-09-22','Sep 22, 2026','How SpaceXAI is using Grok Bot to scale customer support',True),
      ('grok-voice-transcribe-2','og-grok-voice-transcribe-2-0.webp','2026-09-18','Sep 18, 2026','Introducing Grok Voice Transcribe 2.0',False),
    ]
    news = ''.join('<a class="group group/card block" href="https://x.ai/news/'+slug+'"><div class="border-primary/[0.06] bg-card relative overflow-hidden border rounded-lg"><div style="aspect-ratio:1200/630" class="relative overflow-hidden"><img src="'+images[img]+'" alt="'+escape(title)+'" class="absolute inset-0 h-full w-full object-cover"></div></div><div class="text-primary flex items-center gap-2 text-xs mt-4">'+('<span class="font-medium">Product</span><span class="text-primary/25">·</span>' if product else '')+'<time datetime="'+iso+'">'+date+'</time></div><h3 class="text-primary mt-2 text-base font-medium leading-snug tracking-tight text-pretty">'+title+' <span class="text-primary/60">↗</span></h3></a>' for slug,img,iso,date,title,product in news_data)
    panels = ''.join('<pre data-code-panel="'+str(i)+'"'+(' hidden' if i else '')+'>'+escape(code)+'</pre>' for i,code in enumerate(CODE.values()))
    tabs = ''.join('<button role="tab" aria-selected="'+str(i==0).lower()+'" class="rounded-full px-3 py-1.5 text-sm font-medium">'+escape(name)+'</button>' for i,name in enumerate(CODE))
    choices = ''
    for title,description,points,cta,href,solid in [
      ('Build on your own','Launch your AI-powered product with:',['Access to all Grok models','Usage-based pricing','Automatically increasing rate limits','Comprehensive documentation and guides'],'Start Building','https://console.x.ai?utm_source=website&utm_medium=referral&utm_campaign=home&utm_content=get-started-start-building',True),
      ('Get extra support','Custom rate limits and hands-on support for your team.',['Dedicated onboarding support','Custom rate limits','Billing via monthly invoices','Single sign-on and audit logging','Data residency options'],'Contact Sales','/contact-sales',False)]:
        choices += '<div class="bg-card flex flex-col rounded-2xl p-8 sm:p-10"><h3 class="font-display text-2xl tracking-tight">'+title+'</h3><p class="text-primary mt-3">'+description+'</p><hr class="border-border my-6"><ul class="space-y-3">'+''.join('<li class="flex items-start gap-3 text-sm"><span aria-hidden="true">✓</span>'+point+'</li>' for point in points)+'</ul><div class="mt-auto pt-8"><a href="'+url(href)+'" class="pill small w-full'+(' solid' if solid else '')+'">'+cta+'</a></div></div>'
    footer_groups = ['<div class="footer-group"><h3>'+name+'</h3><ul>'+''.join('<li><a href="'+url(href)+'">'+escape(label)+'</a></li>' for label,href in links)+'</ul></div>' for name,links in GROUPS]
    footer_columns = ''.join('<div class="flex flex-col gap-10">'+''.join(footer_groups[i:i+2])+'</div>' for i in range(0,10,2))
    html = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>SpaceXAI · Unofficial visual study</title>'''+''.join(styles)+preload+'<style>'+CSS+'</style></head><body class="geistmono_157ca88a-module__-glMDW__variable xvf_14695435-module__Z7Vuyq__variable bg-background text-primary font-sans antialiased">'
    html += '<header class="xai-header"><nav class="'+WRAP+' xai-nav"><a class="xai-brand" aria-label="SpaceXAI Homepage" href="https://x.ai/"><img src="x.ai-assets/spacexai-symbol.svg" alt="SpaceXAI"></a><div class="xai-nav-links">'+nav+'</div><div class="xai-actions"><a class="pill" href="https://x.ai/contact-sales">Contact Sales</a><div class="try-split"><a href="https://grok.com">Try for free</a><button type="button" data-menu="Try for free" aria-label="Try for free options">⌄</button></div></div><button id="xai-mobile-toggle" class="xai-mobile-toggle" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="xai-menu"><span class="menu-bars"></span></button></nav></header><div id="xai-menu" class="xai-menu" hidden><div class="menu-grid">'+menu+'</div></div>'
    html += '<main><div class="pill-hero-pt relative"><div class="'+WRAP+' pb-16 sm:pb-24"><div class="mx-auto mb-12 max-w-3xl text-center sm:mb-20"><div class="mb-6 flex justify-center sm:mb-8"><a aria-label="Meet Grok 4.7, our new model" class="inline-flex items-center gap-2.5 rounded-full py-1.5 pe-1.5 ps-2.5 border-primary/[0.08] border" href="https://x.ai/news/grok-4-7"><span class="bg-sunset/10 text-sunset inline-flex rounded-full px-2 py-[3px] text-[11px] font-medium leading-none">New</span><span class="whitespace-nowrap text-[13px]"><span class="font-medium">Meet Grok 4.7</span><span class="text-primary/20"> · </span>Our new model</span><span class="bg-primary/[0.04] flex size-6 items-center justify-center rounded-full">↗</span></a></div><h1 class="font-display text-4xl font-[450] leading-[1.1] tracking-tight text-balance sm:text-5xl lg:text-6xl">Frontier AI models<br>for everything you <br class="sm:hidden"><span class="hero-word">build</span>.</h1><p class="text-primary mt-5 text-lg leading-relaxed">Reasoning, code, voice, images, and video. <br class="lg:hidden">Trained on the world\'s largest supercluster.</p><div class="mt-9 flex flex-wrap justify-center gap-3"><a class="pill solid" href="https://console.x.ai?utm_source=website&amp;utm_medium=referral&amp;utm_campaign=home&amp;utm_content=hero-get-api-access">Get API Access ›</a><a class="pill" href="https://docs.x.ai">View Documentation</a></div></div><div class="grid gap-3 sm:grid-cols-6">'+cards+'</div></div></div>'
    html += '<section><div class="'+SECTION+'"><div class="grid gap-12 lg:grid-cols-2 lg:items-center lg:gap-24"><div><p class="text-primary/60 text-sm font-medium">For developers</p><h2 class="font-display mt-4 text-4xl tracking-tight sm:text-5xl">One API.<br>Every modality.</h2><p class="text-primary mt-4 max-w-md leading-relaxed">Text, code, voice, images, and video — all through a single unified API. Start building in seconds.</p><div class="mt-8 flex gap-3"><a href="https://console.x.ai" class="pill small solid">Get API Key</a><a href="https://docs.x.ai" class="pill small">Read Docs</a></div><div class="mt-8 flex flex-wrap gap-6 text-xs">'+''.join('<div><p class="text-primary text-sm font-medium tabular-nums">'+escape(value)+'</p><p class="text-primary/30 mt-0.5">'+name+'</p></div>' for value,name in [('1M+','API calls per day'),('<200ms','Median latency'),('5+','Model families')])+'</div></div><div class="relative"><div class="relative p-8 sm:p-10 lg:p-12 overflow-hidden code-background"><div class="code-window-chrome relative overflow-hidden rounded-xl"><div class="code-header"><button id="copy-code" type="button" aria-label="Copy code">Copy</button></div><div class="code-window-scroll minimal-scrollbar">'+panels+'</div></div></div><div class="code-tabs relative mt-5 flex flex-wrap items-center gap-x-1 gap-y-2" role="tablist" aria-label="Code language">'+tabs+'</div></div></div></div></section>'
    html += '<section><div class="'+WRAP+' py-4 sm:py-6"><dl class="divide-primary/10 border-primary/10 grid gap-y-8 border-y py-8 sm:grid-cols-3 sm:gap-x-10 sm:divide-x sm:py-10 [&amp;>div:not(:first-child)]:sm:pl-10">'+''.join('<div><dd class="m-0"><div class="font-display text-primary whitespace-nowrap text-4xl tracking-tight sm:text-5xl"><span class="number-static">'+n+'</span>'+suffix+'</div></dd><dt class="text-primary/60 text-sm font-medium mt-2">'+label+'</dt></div>' for n,suffix,label in [('300','M+','queries processed daily'),('150','K','GPUs in <a href="https://x.ai/colossus">Colossus</a>'),('90','','<a href="https://x.ai/colossus">days to build Colossus</a>')])+'</dl></div></section>'
    html += '<section><div class="'+SECTION+'"><div class="mb-10 flex items-end justify-between"><h2 class="font-display text-2xl tracking-tight sm:text-3xl">Latest news</h2><a href="https://x.ai/news" class="text-sm font-medium">All posts ↗</a></div><div class="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">'+news+'</div></div></section>'
    html += '<section><div class="'+SECTION+' border-border border-t"><h2 class="font-display mb-10 text-center text-2xl tracking-tight sm:text-3xl">Choose how to get started</h2><div class="grid gap-6 md:grid-cols-2">'+choices+'</div></div></section></main>'
    html += '<footer><div class="'+WRAP+' border-border border-t pb-16 pt-10 max-lg:px-6"><div class="flex flex-col gap-10 lg:flex-row lg:gap-16"><div class="flex shrink-0 flex-col lg:w-[280px]"><img src="x.ai-assets/spacexai-wordmark.svg" alt="SpaceXAI" class="h-4 w-auto self-start"><p class="text-primary/40 mt-6 text-xs">© 2026 SpaceXAI LLC</p><a class="text-primary/30 mt-2 text-xs" href="https://grok.com">Built with Grok</a></div><div class="border-primary/[0.1] hidden border-l border-dashed lg:block"></div><div class="grid grid-cols-2 gap-x-8 gap-y-8 md:grid-cols-3 md:gap-x-12 lg:ml-auto lg:grid-cols-5 lg:gap-x-14 lg:gap-y-10">'+footer_columns+'</div></div></div></footer><script src="x.ai-assets/official-orb-core.js"></script><script>'+SCRIPT+'</script></body></html>'
    (ROOT/'x.ai.html').write_text(html)
    print('Saved SpaceXAI draft with official fonts, photographs, utility styles, and orb renderer')


if __name__ == '__main__':
    main()
