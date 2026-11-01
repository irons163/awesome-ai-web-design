#!/usr/bin/env python3
"""Prepare review-only first screens using measured reference media.

This is not a publish step. Reference assets and their owners must be accounted
for, and the complete pages remain to be checked before replacing a live study.
"""
from pathlib import Path
import base64
import re

ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/'.test-artifacts/five-homepage-revision-2026-11-01/review-previews'
OUT=ROOT/'.test-artifacts/direct-reference-2026-11-01/candidates'
MEDIA=ROOT/'data/new-studies/media/reference-2026-11-01'

def uri(path,content_type):
    return 'data:'+content_type+';base64,'+base64.b64encode(path.read_bytes()).decode()

canva_ids=['7b6119e9bb7c45c6','fbb988f2e6527f13','60385faf7cddd870','4b976d2c32600129','71479db12fb84b8c','77be32c7b21159f9','f794903ff2aff929','653fa7b4c64ff269','54344c444511e61c']

CSS='''<style>
.s2-page .s2-label{display:none}.s2-canva .s2-nav{height:80px;background:#8936f1;padding:0 48px}.s2-canva .s2-brand{font-size:32px}.s2-canva .s2-links{gap:24px}.s2-canva-hero{height:616px;min-height:616px;padding:49px 24px 0;background:linear-gradient(180deg,#762aec 0%,#512ee7 20%,#3a64be 42%,#63bdc3 62%,#bceaf1 83%,#fbf7ff 100%)}.s2-canva-hero h1{font-size:64px;line-height:1.1;font-weight:400;letter-spacing:0;margin:0 auto 24px}.s2-canva-hero p{margin:0 0 24px;font-size:18px}.s2-canva-hero .s2-button{height:40px;min-height:40px;width:192px;border-radius:7px}.ref-canva-row{display:flex;justify-content:center;gap:32px}.ref-canva-row img{width:144px;height:144px;object-fit:contain}.ref-canva-row:first-child{margin-top:48px}.ref-canva-row+.ref-canva-row{margin-top:-28px}
.s2-li .s2-nav{height:80px}.s2-li .s2-brand{font-family:Arial,sans-serif;font-size:26px}.s2-li-hero{padding:48px 0 36px;min-height:608px;grid-template-columns:1fr 1fr;gap:0}.s2-li-copy h1{font-size:48px;line-height:1.2;margin:0 0 28px;font-weight:400;white-space:nowrap}.s2-li-art{width:700px;max-width:none;height:560px;max-height:none}.s2-li-choices .s2-button{min-height:42px}.s2-li-copy p{font-size:14px}
.s2-pay .s2-nav{height:88px}.s2-pay .s2-brand img{height:46px;width:auto}.s2-pay-hero{padding-top:56px;min-height:850px;background:#81c9f5}.s2-pay-hero h1{font-size:69px;line-height:1.1;font-weight:900;letter-spacing:0;margin:0 auto 50px}.s2-pay-card{padding:24px 16px 16px}.s2-pay-card strong{font-size:48px}.s2-pay-card .s2-photo{height:252px}
.s2-etsy-main .s2-photo,.s2-etsy-side .s2-photo{height:100%;width:100%;object-fit:cover;border-radius:0}.s2-etsy-side{padding:0;position:relative}.s2-etsy-side strong{position:absolute;bottom:24px;left:24px}.s2-etsy-hero{padding-top:24px}
.s2-khan-hero{padding-top:88px}.s2-khan-hero h1{font-size:42px;line-height:1.1;max-width:410px}.s2-khan .s2-nav{height:70px}
@media(max-width:767px){.s2-canva .s2-nav,.s2-li .s2-nav,.s2-pay .s2-nav{height:64px}.s2-canva-hero{height:auto;min-height:560px;padding-top:52px}.s2-canva-hero h1{font-size:38px}.ref-canva-row{gap:6px}.ref-canva-row img{width:min(18vw,100px);height:auto}.ref-canva-row+.ref-canva-row{margin-top:-14px}.s2-li-hero{padding:40px 24px;display:block}.s2-li-copy h1{white-space:normal;font-size:35px}.s2-li-art{width:100%;height:auto}.s2-pay-hero h1{font-size:48px}.s2-pay-hero{padding-top:40px}.s2-pay-card .s2-photo{height:210px}.s2-etsy-side{min-height:220px}.s2-khan-hero{padding-top:48px}}
</style>'''

def main():
    OUT.mkdir(exist_ok=True)
    canva_imgs=[uri(MEDIA/'canva'/f'{n}.png','image/webp' if n=='77be32c7b21159f9' else 'image/png') for n in canva_ids]
    svg=uri(MEDIA/'linkedin/hero.svg','image/svg+xml')
    paypal=uri(MEDIA/'paypal/9db972a0603cb389.jpg','image/webp')
    paypal_logo=uri(MEDIA/'paypal/d8b6288035eb720d.svg','image/svg+xml')
    etsy=uri(MEDIA/'etsy/ff2444285d3efa4c.jpg','image/webp')
    etsy2=uri(MEDIA/'etsy/1e04aeff40bcabac.jpg','image/webp')
    for slug in ['canva','linkedin','paypal','etsy','khan-academy']:
        html=(SRC/f'{slug}.html').read_text()
        html=html.replace('授權：自由互動示範原型','素材與商標權利屬原權利人')
        html=html.replace('</head>',CSS+'</head>',1)
        if slug=='canva':
            html=html.replace('讓每個想法，變成作品。','你今天要設計些什麼呢？').replace('為簡報、社群貼文和影片找到創意起點。','運用創意工具製作社群媒體貼文、影片和簡報等內容。').replace('瀏覽設計範例','開始設計')
            imgs=['<img src="'+u+'" alt="" />' for u in canva_imgs]
            rows='<div class="ref-canva-row">'+''.join(imgs[:4])+'</div><div class="ref-canva-row">'+''.join(imgs[4:])+'</div>'
            html,n=re.subn(r'<div class="s2-tiles" aria-hidden="true">.*?</div></section>',lambda _: '<div aria-hidden="true">'+rows+'</div></section>',html,count=1)
            assert n==1
        if slug=='linkedin':
            html=html.replace('讓專業交流，<br>成為新的可能。','歡迎加入專業人士社群網')
            html,n=re.subn(r'<svg class="s2-li-art".*?</svg>',f'<img class="s2-li-art" src="{svg}" alt="工作場景插畫"/>',html,count=1,flags=re.S);assert n==1
            html=html.replace('探索職涯主題','使用 Google 繼續（示範）').replace('瀏覽社群靈感','用電子郵件登入（示範）')
        if slug=='paypal':
            html=html.replace('PayPal 風格研究</div><div class="s2-links">',f'<img src="{paypal_logo}" alt="PayPal"/></div><div class="s2-links">',1)
            html=html.replace('讓每次付款<br>更簡單','付款和要求<br>付款').replace('<strong>PayPal 風格研究</strong>','<strong>PayPal</strong>')
            html,n=re.subn(r'(<img class="s2-photo" src=")[^"]+(" alt="朋友一起查看手機的原創示意圖">)',lambda m:m[1]+paypal+'" alt="朋友一起查看手機的參考照片">',html,count=1);assert n==1
        if slug=='etsy':
            html,n=re.subn(r'(<img class="s2-photo" src=")[^"]+(" alt="手工布藝的原創示意圖">)',lambda m:m[1]+etsy+'" alt="手作商品參考照片">',html,count=1);assert n==1
            html=html.replace('<div class="s2-etsy-side"><strong>','<div class="s2-etsy-side"><img class="s2-photo" src="'+etsy2+'" alt="節日飾品參考照片"/><strong>')
        if slug=='khan-academy':
            html=html.replace('讓每個學習目標，<br><em>慢慢實現。</em>','把遠大的學習目標，<br><em>化為真實成果。</em>')
        (OUT/f'{slug}.html').write_text(html)
        print(slug,'candidate prepared')

if __name__=='__main__':main()
