#!/usr/bin/env python3
"""Add an independently recreated reference first screen to five Stitch studies.

The retained Stitch material below remains available as supplementary demo content.
Original exports stay untouched; this is not an official site or a pixel comparison.
"""
from pathlib import Path
import base64
import re

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / '.test-artifacts/five-fourth-designs-2026-11-01/review-previews'
OUT = ROOT / '.test-artifacts/five-homepage-revision-2026-11-01/review-previews'

CSS = r'''<style>
.s2-old-head{display:none!important}.s2-page main{padding-top:0!important}.s2-page main>div>section:first-of-type{display:none!important}
.s2-page main{max-width:none!important;margin:0!important;padding-left:0!important;padding-right:0!important}
.s2-page{font-family:system-ui,-apple-system,"Noto Sans TC",sans-serif;color:#191919}.s2-page *{box-sizing:border-box}
.s2-label{background:#252c29;color:white;text-align:center;font-size:13px;padding:9px 12px;line-height:1.4}
.s2-nav{display:flex;align-items:center;gap:28px;padding:0 max(24px,calc((100vw - 1200px)/2));height:78px;background:#fff}
.s2-brand{font-size:25px;font-weight:800;white-space:nowrap}.s2-links{display:flex;align-items:center;gap:28px;font-size:14px;font-weight:600;flex:1}.s2-actions{display:flex;align-items:center;gap:14px;white-space:nowrap}.s2-button{display:inline-flex;justify-content:center;align-items:center;min-height:42px;padding:0 23px;border-radius:999px;border:1px solid currentColor;font-size:14px;font-weight:700;text-decoration:none!important;background:transparent;color:inherit;cursor:pointer}.s2-button.s2-filled{background:#151515;color:white;border-color:#151515}.s2-sub{font-size:13px;color:#505968}
.s2-canva .s2-nav{background:#a67cf0;color:white;max-width:none;padding:0 32px}.s2-canva .s2-brand{font-family:Georgia,serif;font-style:italic;font-size:30px}.s2-canva .s2-links{justify-content:center}.s2-canva .s2-button{border-radius:8px;min-height:36px;padding:0 14px}.s2-canva .s2-filled{background:white;color:#191919;border-color:white}
.s2-canva-hero{min-height:690px;text-align:center;padding:72px 24px 48px;background:linear-gradient(180deg,#6d28eb 0%,#5438d8 30%,#4cbdc2 73%,#ecf8fa 100%);color:#fff;overflow:hidden}.s2-canva-hero h1{font-size:clamp(35px,5vw,66px);font-weight:500;line-height:1.18;margin:0 auto 20px;letter-spacing:-.04em}.s2-canva-hero p{font-size:18px;margin:0 0 28px}.s2-canva-hero .s2-button{background:#fff;color:#171717;border:0;border-radius:8px;min-width:190px}.s2-tiles{display:flex;align-items:center;justify-content:center;gap:40px;flex-wrap:wrap;max-width:820px;margin:72px auto 0}.s2-tile{width:92px;height:92px;display:grid;place-items:center;border-radius:22px;color:white;font:bold 46px Georgia,serif;box-shadow:0 8px 20px #322a8655;transform:rotate(-7deg)}.s2-tile:nth-child(even){transform:rotate(7deg)}
.s2-li .s2-brand{color:#0a66c2}.s2-li .s2-links{justify-content:flex-end;color:#626262}.s2-li .s2-button{color:#0a66c2}.s2-li .s2-filled{color:white;background:#0a66c2;border-color:#0a66c2}
.s2-li-hero{max-width:1200px;margin:auto;min-height:610px;padding:62px 0 40px;display:grid;grid-template-columns:1fr 1fr;gap:28px;align-items:start}.s2-li-copy h1{font-size:clamp(38px,4vw,52px);font-weight:400;line-height:1.2;margin:0 0 28px}.s2-li-copy p{font-size:14px;color:#666;line-height:1.6;max-width:400px;text-align:center}.s2-li-choices{display:grid;gap:12px;max-width:400px}.s2-li-choices .s2-button{width:100%;min-height:46px}.s2-li-art{width:100%;max-height:520px}
.s2-pay .s2-brand{color:#003087;font-size:28px;font-style:italic}.s2-pay-hero{background:#81c9f5;text-align:center;min-height:850px;padding:56px 24px 90px}.s2-toggle{display:inline-flex;background:#ffffff5e;border-radius:999px;padding:4px;margin-bottom:56px}.s2-toggle button{padding:13px 30px;border:0;border-radius:999px;background:transparent;cursor:pointer;font-weight:700;color:#222}.s2-toggle button[aria-pressed=true]{background:#fff}.s2-pay-hero h1{font-size:clamp(48px,7vw,84px);line-height:1.12;letter-spacing:-.05em;max-width:650px;margin:0 auto 50px;color:#000}.s2-pay-card{background:#fff;border-radius:40px 40px 0 0;padding:28px 16px 16px;max-width:550px;margin:auto;color:#000}.s2-pay-card strong{display:block;font-size:48px;font-weight:900;letter-spacing:-.05em;margin-bottom:20px}.s2-photo{display:block;width:100%;height:300px;object-fit:cover;border-radius:9px;background:#d5e2e8}
.s2-etsy{background:#faf9f6}.s2-etsy .s2-nav{max-width:none;padding:0 36px;gap:24px}.s2-etsy .s2-brand{font-family:Georgia,serif;color:#d75d25;font-weight:400;font-size:41px}.s2-search{flex:1;border:2px solid #25232a;border-radius:999px;display:flex;align-items:center;min-width:0;height:48px;padding-left:20px;background:#fff;color:#717171;font-size:14px}.s2-search b{margin-left:auto;background:#e87337;color:#fff;border-radius:999px;width:40px;height:40px;display:grid;place-items:center;font-size:20px}.s2-etsy-subnav{display:flex;justify-content:center;gap:48px;border-bottom:1px solid #dedbd5;padding:10px;font-size:13px;font-weight:600}.s2-etsy-hero{display:grid;grid-template-columns:2fr 1fr;gap:28px;padding:24px 36px 48px;max-width:1400px;margin:auto}.s2-etsy-main{display:grid;grid-template-columns:1.15fr 1fr;background:#d6e2f1;border-radius:12px;overflow:hidden;min-height:400px}.s2-etsy-copy{display:flex;align-items:center;justify-content:center;flex-direction:column;text-align:center;padding:32px}.s2-etsy-copy h1{font-family:Georgia,serif;font-size:clamp(30px,3.5vw,52px);font-weight:400;line-height:1.1;margin:0 0 24px}.s2-etsy-main .s2-photo{height:100%;border-radius:0}.s2-etsy-side{border-radius:12px;overflow:hidden;background:linear-gradient(155deg,#d8b79d,#626759);display:flex;align-items:end;padding:28px;color:#fff;min-height:400px}.s2-etsy-side strong{font-size:25px;max-width:250px;line-height:1.2;text-shadow:0 2px 8px #222}
.s2-khan{background:#fff}.s2-khan .s2-nav{border-bottom:1px solid #ddd;position:relative}.s2-khan .s2-brand{position:absolute;left:50%;transform:translateX(-50%);font-size:20px;color:#202329}.s2-khan .s2-links{gap:24px}.s2-khan .s2-filled{background:#5149d6;border-color:#5149d6;color:white;border-radius:7px}.s2-khan-hero{max-width:1120px;margin:auto;display:grid;grid-template-columns:1fr 1fr;gap:80px;padding:84px 0 90px;min-height:600px}.s2-khan-hero h1{font-size:clamp(38px,4vw,54px);line-height:1.04;letter-spacing:-.045em;margin:0 0 28px;max-width:430px}.s2-khan-hero p{font-size:18px;line-height:1.55;max-width:440px}.s2-khan-roles h2{font-size:20px;margin:0 0 10px}.s2-role{display:flex;align-items:center;justify-content:space-between;border:1px solid #c8c8ce;background:#fff;border-radius:8px;padding:18px 16px;margin:0 0 16px;min-height:95px;box-shadow:0 2px 2px #0001;text-decoration:none!important;color:#1d1d22}.s2-role small{display:block;font-size:14px;font-weight:400;color:#555}.s2-role span{color:#5149d6}
@media(max-width:767px){.s2-nav{height:64px;padding:0 20px!important;gap:12px}.s2-links,.s2-actions .s2-optional,.s2-etsy-subnav{display:none!important}.s2-actions{margin-left:auto}.s2-brand{font-size:22px}.s2-canva-hero{padding-top:62px;min-height:620px}.s2-tiles{gap:15px;margin-top:56px}.s2-tile{width:66px;height:66px;font-size:32px}.s2-li-hero{grid-template-columns:1fr;padding:48px 24px 20px;gap:12px}.s2-li-art{max-height:330px}.s2-pay-hero{padding-top:38px;min-height:710px}.s2-toggle{margin-bottom:42px}.s2-pay-card{border-radius:28px 28px 0 0}.s2-pay-card strong{font-size:36px}.s2-photo{height:240px}.s2-etsy .s2-nav{gap:12px}.s2-etsy .s2-brand{font-size:31px}.s2-search{font-size:12px;padding-left:12px}.s2-etsy-hero{padding:16px;grid-template-columns:1fr;gap:14px}.s2-etsy-main{min-height:330px}.s2-etsy-copy{padding:16px}.s2-etsy-copy h1{font-size:29px}.s2-etsy-side{min-height:180px}.s2-khan .s2-brand{position:static;transform:none;font-size:17px}.s2-khan-hero{grid-template-columns:1fr;gap:28px;padding:48px 24px 60px}.s2-khan-hero h1{font-size:38px}.s2-khan-hero p{font-size:16px}}
</style>'''

LABEL = '<div class="s2-label" role="note">非官方設計參考 · 主視覺依公開首頁重新繪製，示範內容不提供真實服務</div>'

ART = '''<svg class="s2-li-art" viewBox="0 0 600 500" role="img" aria-label="原創職涯插圖"><rect x="12" y="16" width="575" height="462" rx="200" fill="#eaf1f1"/><rect x="360" y="30" width="145" height="310" fill="#eee1c9"/><path d="M365 120h140M365 220h140" stroke="#fff" stroke-width="12"/><rect x="400" y="70" width="32" height="45" fill="#bd7761"/><circle cx="460" cy="80" r="28" fill="#8baa98"/><rect x="385" y="160" width="25" height="60" fill="#8fa999"/><rect x="420" y="156" width="30" height="64" fill="#cba18b"/><path d="M60 350h460v18H60z" fill="#cbb99a"/><path d="M140 300h140l40 90H125z" fill="#e5d9c7"/><path d="M200 245l70-45 75 90 25 110h-65l-37-74-56 10z" fill="#315d61"/><circle cx="274" cy="187" r="42" fill="#b77353"/><path d="M235 180c5-52 70-62 85-18l-8 27-14-18-54 12z" fill="#243c3f"/><path d="M160 217h110l20 72H178z" fill="#596f76"/><path d="M155 290h155" stroke="#243c3f" stroke-width="8"/><path d="M306 400l-60 40m80-40 30 40" stroke="#283c3e" stroke-width="12" stroke-linecap="round"/></svg>'''

def nav(brand, links, actions, style):
    return f'<nav class="s2-nav"><div class="s2-brand">{brand}</div><div class="s2-links">{links}</div><div class="s2-actions">{actions}</div></nav>'

def button(label, target, filled=False, extra=''):
    return f'<a class="s2-button {"s2-filled" if filled else ""} {extra}" href="{target}">{label}</a>'

def photo(name):
    path=OUT/f'{name}.webp'
    return 'data:image/webp;base64,'+base64.b64encode(path.read_bytes()).decode() if path.exists() else ''

def hero(slug):
    if slug == 'canva':
        n=nav('Canva 風格研究','<span>設計</span><span>產品</span><span>方案</span><span>教育</span>',button('瀏覽範本','#templates',True),'canva')
        tiles=''.join(f'<div class="s2-tile" style="background:{c}">{v}</div>' for c,v in [('#7eace3','T'),('#f78bac','✦'),('#fb5990','♥'),('#6c46dc','♫'),('#62cfc8','◉'),('#facf49','✳'),('#5399ea','C')])
        return f'<div class="s2-canva">{LABEL}{n}<section class="s2-canva-hero"><h1>讓每個想法，變成作品。</h1><p>為簡報、社群貼文和影片找到創意起點。</p>{button("瀏覽設計範例","#templates",True)}<div class="s2-tiles" aria-hidden="true">{tiles}</div></section></div>'
    if slug == 'linkedin':
        n=nav('LinkedIn 風格研究','<span>熱門內容</span><span>會員</span><span>學習</span><span>職涯</span>',button('探索內容','#explorerSection',False,'s2-optional')+button('瀏覽主題','#explorerSection',True),'li')
        return f'<div class="s2-li">{LABEL}{n}<section class="s2-li-hero"><div class="s2-li-copy"><h1>讓專業交流，<br>成為新的可能。</h1><div class="s2-li-choices">{button("探索職涯主題","#explorerSection",True)}{button("瀏覽社群靈感","#explorerSection")}</div><p>以公開首頁的版面作為設計參考。此處使用虛構內容，不提供登入或徵才服務。</p></div>{ART}</section></div>'
    if slug == 'paypal':
        n=nav('PayPal 風格研究','<span>個人</span><span>商業</span><span>開發者</span>',button('了解示範','#s2-more',False,'s2-optional')+button('查看內容','#s2-more',True),'pay')
        return f'''<div class="s2-pay">{LABEL}{n}<section class="s2-pay-hero"><div class="s2-toggle" role="group" aria-label="選擇參考情境"><button type="button" aria-pressed="true" data-s2-mode="personal">個人</button><button type="button" aria-pressed="false" data-s2-mode="business">公司</button></div><h1 id="s2-pay-title">讓每次付款<br>更簡單</h1><div class="s2-pay-card"><strong>PayPal 風格研究</strong><img class="s2-photo" src="{photo('paypal-hero')}" alt="朋友一起查看手機的原創示意圖"></div></section></div>'''
    if slug == 'etsy':
        n='<nav class="s2-nav"><div class="s2-brand">Etsy</div><span class="s2-optional">☰ 分類</span><a class="s2-search" href="#inspirationHub" aria-label="前往手作靈感搜尋">搜尋手作靈感與商品 <b>⌕</b></a><a class="s2-optional" href="#inspirationHub">探索</a><span aria-hidden="true">♡</span></nav>'
        return f'<div class="s2-etsy">{LABEL}{n}<div class="s2-etsy-subnav"><span>禮物靈感</span><span>居家生活</span><span>手作飾品</span><span>古董選物</span><span>特別企劃</span></div><section class="s2-etsy-hero"><div class="s2-etsy-main"><div class="s2-etsy-copy"><h1>發現與眾不同的手作靈感</h1>{button("探索作品","#inspirationHub",True)}</div><img class="s2-photo" src="{photo("etsy-hero")}" alt="手工布藝的原創示意圖"></div><div class="s2-etsy-side"><strong>為日常挑選<br>獨特的小美好 ↗</strong></div></section></div>'
    n=nav('◆ Khan Academy 風格研究','<span>探索課程 ▾</span><span>⌕ 搜尋</span>',button('課程總覽','#featured-courses',False,'s2-optional')+button('開始探索','#featured-courses',True),'khan')
    return f'<div class="s2-khan">{LABEL}{n}<section class="s2-khan-hero"><div><h1>讓每個學習目標，<br><em>慢慢實現。</em></h1><p>用適合自己的步調練習、理解與成長。這是一個以學習首頁版面為參考的示範。</p><p aria-hidden="true" style="font-size:70px;color:#5550ce;margin-top:45px">✦ ◌ ✳</p></div><div class="s2-khan-roles"><h2>從這裡開始</h2><a class="s2-role" href="#featured-courses"><b>學生<small>依自己的步調學習</small></b><span>›</span></a><a class="s2-role" href="#featured-courses"><b>家長<small>陪伴孩子探索知識</small></b><span>›</span></a><a class="s2-role" href="#featured-courses"><b>教師<small>為課堂尋找學習素材</small></b><span>›</span></a><p class="s2-sub">選擇角色，瀏覽下方的示範課程。</p></div></section></div>'

def main():
    OUT.mkdir(exist_ok=True)
    for slug in ('canva','linkedin','paypal','etsy','khan-academy'):
        html=(EVIDENCE/f'{slug}.html').read_text()
        html=html.replace('</head>',CSS+'</head>',1)
        html=html.replace('<body class="', '<body class="s2-page ', 1)
        html=re.sub(r'<header\b[^>]*>', lambda m:m.group().replace('<header ','<header hidden data-s2-original ',1),html,count=1)
        html=html.replace('</head>', '<style>header[data-s2-original]{display:none!important}</style></head>',1)
        html=re.sub(r'(<main\b[^>]*>)',hero(slug)+r'<div id="s2-more" style="padding:18px 24px;text-align:center;background:#f4f3ef;color:#50564e;font:14px/1.5 system-ui,sans-serif">以下為延伸互動示範，內容與官網不同。</div>\1',html,count=1)
        if slug=='paypal':
            html=html.replace('</body>', '''<script>document.querySelectorAll('[data-s2-mode]').forEach(b=>b.addEventListener('click',()=>{document.querySelectorAll('[data-s2-mode]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));document.getElementById('s2-pay-title').innerHTML=b.dataset.s2Mode==='personal'?'讓每次付款<br>更簡單':'讓商業收付款<br>更有彈性';}));</script></body>''',1)
        (OUT/f'{slug}.html').write_text(html)
        print(slug,'prepared')

if __name__=='__main__': main()
