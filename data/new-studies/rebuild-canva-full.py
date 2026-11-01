#!/usr/bin/env python3
"""Rebuild Canva's public homepage study from the observed 2026-11-01 layout.

The study is a local, non-official reference. It uses recorded third-party
media; source URLs and hashes are recorded in the accompanying manifest.
"""
from pathlib import Path
import base64
import html
import json

ROOT=Path(__file__).resolve().parents[2]
ASSETS=ROOT/'data/new-studies/media/reference-2026-11-01/canva-full-optimized'
OUT=ROOT/'.test-artifacts/canva-full-2026-11-01'
MANIFEST=json.loads((ASSETS/'manifest.json').read_text())['assets']
BY_NAME={r['name']:r for r in MANIFEST}

def image(name):
    r=BY_NAME[name]
    return 'data:image/webp;base64,'+base64.b64encode((ASSETS/r['derived_path']).read_bytes()).decode()

def e(value): return html.escape(value,quote=True)

DATA={
 'AI':[
  ('使用「魔法圖層」將影像轉換為可編輯的版面配置','探索魔法圖層','ai-magic-layers-2-3_zh-TW.png','https://www.canva.com/zh_tw/magic-layers/'),
  ('使用魔法橡皮擦清理照片','探索魔法橡皮擦','ai-magic-eraser-1-3_zh-TW.png','https://www.canva.com/features/magic-eraser/'),
  ('按一下即可移除影像背景','探索背景移除工具','social-bgremover-1-3_zh-TW.png','https://www.canva.com/features/background-remover/'),
  ('使用魔法文案工具提升寫作品質','探索魔法文案工具','ai-magic-write-2-3_zh-TW.png','https://www.canva.com/magic-write/')],
 '簡報':[
  ('製作引人入勝且能激發靈感的簡報','探索簡報設計工具','presentations-2-3_zh-TW.png','https://www.canva.com/presentations/'),
  ('尋找你的完美簡報範本','探索範本','presentations-templates-1-3_zh-TW.png','https://www.canva.com/presentations/templates/'),
  ('使用品牌工具組維持一致的品牌形象','探索品牌工具組','presentations-brand-kit-1-3_zh-TW.png','https://www.canva.com/zh_tw/pro/brand-kit/'),
  ('運用動畫讓簡報栩栩如生','探索動畫','presentations-animations-2-3_zh-TW.png','https://www.canva.com/zh_tw/pro/animator/')],
 '社交':[
  ('使用熱門範本，輕鬆製作你的下一部影片','探索系列','social-templates-2-3_zh-TW.png','https://www.canva.com/mobile-videos/templates/'),
  ('按一下即可移除影像背景','探索背景移除工具','social-bgremover-1-3_zh-TW.png','https://www.canva.com/features/background-remover/'),
  ('使用 Image Upscaler 將任何照片銳化','探索影像增強','social-upscale-1-3_zh-TW.png','https://www.canva.com/features/image-upscaler/'),
  ('即時調整設計尺寸，適用於任何管道','探索魔法尺寸調整工具','social-resize-2-3_zh-TW.png','https://www.canva.com/zh_tw/pro/magic-resize/')],
 '影片':[
  ('使用影片編輯器，輕鬆將片段轉換為內容','探索影片編輯器','video-editor-2-3_zh-TW.png','https://www.canva.com/video-editor/'),
  ('所有影片範本匯聚一處','探索影片範本','video-marketplace-1-3_zh-TW.png','https://www.canva.com/videos/'),
  ('適合各種專案的工作室品質圖庫影片','探索圖庫影片','video-marketplace-1-3_zh-TW.png','https://www.canva.com/collection/stock-videos/'),
  ('透過 AI 輔助字幕，提升互動率','探索輔助字幕','video-captions-2-3_zh-TW.png','https://www.canva.com/features/add-subtitles-to-video/')],
 '印刷中心':[
  ('透過印刷中心將構想化為高品質印刷品','探索印刷中心','print-shop-2-3_zh-TW.png','https://www.canva.com/zh_tw/print/'),
  ('即時調整設計尺寸，適用於任何印製規格','探索魔法尺寸調整工具','print-resize-1-3_zh-TW.png','https://www.canva.com/zh_tw/pro/magic-resize/'),
  ('為各種場合設計及印刷邀請卡','探索邀請卡','print-invitations-1-3_zh-TW.png','https://www.canva.com/invitations/'),
  ('為印刷品打造高品質影像','探索 AI 圖片產生器','print-ai-image-2-3_zh-TW.png','https://www.canva.com/ai-image-generator/')],
}
TEMPLATES=['320w-DdnGEoTqAD0.jpg','320w-5D9okURd7wk.jpg','283w-XWAIQYBg_WQ.jpg','400w-F5c3ShTpzrM.jpg','283w-E0i4b0TlIdg.jpg','283w-Qy2NA7jtQh0.jpg','800w-QZ4BFHwXVhQ.jpg','283w-KOTx4YgypwE.jpg','283w-WqzuA0JEcvU.jpg']

CSS='''<style>
.cvf-main{background:#fff;color:#0d1216;font-family:"Noto Sans TC","PingFang TC",system-ui,sans-serif}.cvf-main *{box-sizing:border-box}
.cvf-container{width:min(100% - 96px,1360px);margin:0 auto}.cvf-title{text-align:center;font-weight:400;font-size:48px;line-height:1.16;letter-spacing:-.02em;margin:0 0 30px}.cvf-tools{padding:120px 0 80px}.cvf-tabs-wrap{display:flex;justify-content:center;position:sticky;top:16px;z-index:20;margin:0 auto 32px;pointer-events:none}.cvf-tabs{display:flex;gap:3px;align-items:center;padding:5px;background:#fff;border-radius:999px;box-shadow:0 3px 12px #0e131c26;pointer-events:auto;max-width:100%;overflow:auto;scrollbar-width:none}.cvf-tab{border:0;background:transparent;padding:10px 15px;border-radius:999px;font-size:14px;font-weight:700;white-space:nowrap;cursor:pointer;color:#14151b}.cvf-tab[aria-selected=true]{background:linear-gradient(120deg,#54c0c2,#7736f4);color:#fff}.cvf-tab-icon{font-size:22px;margin-right:9px;color:#a239e5}.cvf-tab[aria-selected=true] .cvf-tab-icon{color:#fff}
.cvf-cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}.cvf-card{border-radius:24px;overflow:hidden;display:flex;flex-direction:column;min-width:0;height:406px;color:white;position:relative}.cvf-card:nth-child(1),.cvf-card:nth-child(4){grid-column:span 2}.cvf-card:nth-child(1){background:linear-gradient(#c100be,#d636e5 39%,#edd5ff)}.cvf-card:nth-child(2){background:linear-gradient(#eb4266,#f68c38)}.cvf-card:nth-child(3){background:#f7d9dc;color:#171519}.cvf-card:nth-child(4){background:linear-gradient(#3987ca,#afe4ed)}.cvf-copy{padding:24px 24px 0}.cvf-copy h3{font-size:24px;line-height:1.25;font-weight:600;margin:0 0 16px;max-width:90%}.cvf-link{display:inline-flex;align-items:center;justify-content:center;min-height:40px;padding:0 18px;background:#fff;color:#171519;border-radius:10px;text-decoration:none!important;font-size:14px;font-weight:700;box-shadow:0 3px 3px #0002}.cvf-card img{width:100%;min-height:0;flex:1;object-fit:contain;object-position:bottom center;margin-top:12px}.cvf-suite{padding:80px 0}.cvf-two{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}.cvf-large{height:580px;position:relative;overflow:hidden;border-radius:24px;background:linear-gradient(#7f2cff,#4cb4bf,#d0edff);color:#fff}.cvf-large:nth-child(2){background:linear-gradient(#facda8,#f28b50)}.cvf-large .cvf-copy{padding:32px}.cvf-large h3{font-size:32px;margin:0 0 8px}.cvf-large p{font-size:14px;margin:0 0 16px}.cvf-large img{width:100%;height:76%;object-fit:contain;object-position:bottom;position:absolute;bottom:0}.cvf-template{padding:80px 0 100px;text-align:center}.cvf-template-actions{display:flex;justify-content:center;gap:12px;margin-top:-8px;margin-bottom:48px}.cvf-purple{background:#8338ec;color:white}.cvf-template-track{display:grid;grid-auto-flow:column;grid-auto-columns:242px;grid-template-rows:repeat(2,304px);gap:24px;overflow-x:auto;text-align:left;padding:0 48px 16px;scroll-snap-type:x proximity}.cvf-template-track img{width:100%;height:304px;object-fit:cover;border-radius:12px;border:1px solid #e6e6eb;scroll-snap-align:start}.cvf-ecosystem{padding:80px 0 120px}.cvf-ecosystem .cvf-card:nth-child(1){background:linear-gradient(#215ba0,#70bde5)}.cvf-ecosystem .cvf-card:nth-child(2){background:linear-gradient(#3028b1,#6d77ec)}.cvf-ecosystem .cvf-card:nth-child(3){background:linear-gradient(#398247,#78bb24);color:white}.cvf-ecosystem .cvf-card:nth-child(4){background:linear-gradient(#ef4762,#f68d42)}.cvf-cta{height:570px;display:flex;align-items:center;justify-content:center;flex-direction:column;background:linear-gradient(105deg,#56c2c3,#5333ed,#7b27e8);color:white;text-align:center;padding:30px}.cvf-cta h2{font-size:56px;font-weight:400;line-height:1.2;margin:0 0 32px}.cvf-footer{background:#fff;color:#20242c;padding:72px 48px 100px}.cvf-footer-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:40px;max-width:1360px;margin:auto}.cvf-footer h3{font-size:18px;margin:0 0 20px}.cvf-footer a{display:block;font-size:14px;margin:10px 0;color:#3a4149;text-decoration:none}.cvf-footer-bottom{max-width:1360px;margin:70px auto 0;padding-top:24px;border-top:1px solid #ddd;font-size:14px}
@media(max-width:767px){.cvf-container{width:calc(100% - 32px)}.cvf-title{font-size:32px}.cvf-tools{padding:72px 0 32px}.cvf-tabs-wrap{justify-content:flex-start}.cvf-tabs{max-width:100%}.cvf-tab{font-size:13px;padding:8px 11px}.cvf-tab-icon{font-size:18px;margin-right:4px}.cvf-cards{grid-template-columns:1fr;gap:12px}.cvf-card:nth-child(n){grid-column:span 1;height:360px}.cvf-copy h3{font-size:20px}.cvf-suite,.cvf-template,.cvf-ecosystem{padding:56px 0}.cvf-two{grid-template-columns:1fr}.cvf-large{height:480px}.cvf-large h3{font-size:26px}.cvf-template-track{padding-inline:16px;grid-auto-columns:190px;grid-template-rows:repeat(2,240px);gap:12px}.cvf-template-track img{height:240px}.cvf-cta{height:360px}.cvf-cta h2{font-size:38px}.cvf-footer{padding:48px 20px 100px}.cvf-footer-grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:28px}}
</style>'''

def a(url,label,cls='cvf-link'):
    return f'<a class="{cls}" href="{e(url)}" target="_blank" rel="noopener noreferrer">{e(label)} ↗</a>'

def cards(rows):
    return ''.join(f'<article class="cvf-card"><div class="cvf-copy"><h3>{e(title)}</h3>{a(url,button)}</div><img loading="lazy" src="{image(pic)}" alt="{e(title)} 的參考圖片"></article>' for title,button,pic,url in rows)

def main():
    OUT.mkdir(exist_ok=True)
    original=(ROOT/'.test-artifacts/direct-reference-2026-11-01/candidates/canva.html').read_text()
    assert '<div id="s2-more"' in original
    prefix=original.split('<div id="s2-more"',1)[0]
    prefix=prefix.replace('</head>',CSS+'</head>',1)
    tabs=''.join(f'<button type="button" role="tab" id="cvf-tab-{i}" aria-controls="cvf-panel-{i}" class="cvf-tab" aria-selected="{str(i==0).lower()}" tabindex="{0 if i==0 else -1}" data-cvf-tab="{i}"><span class="cvf-tab-icon" aria-hidden="true">{icon}</span>{e(name)}</button>' for i,(name,icon) in enumerate(zip(DATA,['✦','◉','♥','▶','▣'])))
    panels=''.join(f'<div role="tabpanel" id="cvf-panel-{i}" aria-labelledby="cvf-tab-{i}" {"" if i==0 else "hidden"}><div class="cvf-cards">{cards(rows)}</div></div>' for i,rows in enumerate(DATA.values()))
    suite=[('認識 Visual Suite','在同一處管理工作流程，讓創作與協作更加順暢。','探索 Visual Suite','visual-suite.png','https://www.canva.com/zh_tw/visual-suite/'),('提升簡報影響力','運用視覺元素、協作工具和 AI，為簡報帶來新風貌。','嘗試設計簡報','presentations_spotlight_clone_zh_tw.png','https://www.canva.com/presentations/')]
    suite_html=''.join(f'<article class="cvf-large"><div class="cvf-copy"><h3>{e(t)}</h3><p>{e(desc)}</p>{a(url,label)}</div><img loading="lazy" src="{image(pic)}" alt="{e(t)} 的參考圖片"></article>' for t,desc,label,pic,url in suite)
    template_order=[0,5,1,6,2,7,3,8,4]
    templates=''.join(f'<img loading="lazy" src="{image(TEMPLATES[i])}" alt="設計範本參考 {i+1}">' for i in template_order)
    eco=[('與 Pingu 一起滑進歡樂與混亂','開始設計','pingu_2-3.png','https://www.canva.com/p/mattel/collections/AaEueKyWFl0DZmHF_yJ5ig'),('適合大型組織的端到端平台','探索 Canva Enterprise','mobile_enterprise_zh_tw.png','https://www.canva.com/enterprise/'),('將 Canva 與你最愛的應用程式搭配使用','探索應用程式','apps-mobile.png','https://www.canva.com/zh_tw/apps/'),('專為有遠大抱負的小型企業打造','探索 Canva 商業版','desktop_business_zh_tw.png','https://www.canva.com/zh_tw/canva-business/')]
    footer_groups={'產品':[('視覺套件','https://www.canva.com/zh_tw/visual-suite/'),('Canva AI','https://www.canva.com/zh_tw/canva-ai/'),('品牌管理','https://www.canva.com/zh_tw/solutions/brand-management-tools/'),('社群媒體','https://www.canva.com/zh_tw/social-media/'),('功能','https://www.canva.com/zh_tw/features/'),('印刷品','https://www.canva.com/zh_tw/print/'),('應用程式','https://www.canva.com/zh_tw/apps/')], '方案':[('定價','https://www.canva.com/zh_tw/pricing/'),('Canva Pro','https://www.canva.com/zh_tw/pro/'),('商業版','https://www.canva.com/zh_tw/canva-business/'),('企業版','https://www.canva.com/zh_tw/enterprise/'),('教育版','https://www.canva.com/zh_tw/education/'),('校園版','https://www.canva.com/zh_tw/higher-education/')], '關於':[('關於 Canva','https://www.canva.com/about/'),('活動','https://www.canva.com/zh_tw/events/'),('工作機會','https://lifeatcanva.com/en'),('社會影響力','https://www.canva.com/zh_tw/step-two/'),('永續發展','https://www.canva.com/zh_tw/sustainability/')], '需要協助？':[('說明中心','https://www.canva.com/zh_tw/help/'),('安全防護','https://www.canva.com/zh_tw/security/'),('信任中心','https://www.canva.com/zh_tw/trust/'),('無障礙操作','https://www.canva.com/accessibility/'),('Design School','https://www.canva.com/design-school/')]}
    foot=''.join('<div><h3>'+e(k)+'</h3>'+''.join(a(url,label,'') for label,url in values)+'</div>' for k,values in footer_groups.items())
    body=f'''<main class="cvf-main"><section class="cvf-tools"><div class="cvf-container"><h2 class="cvf-title">助你打造最佳作品的工具</h2><div class="cvf-tabs-wrap"><div role="tablist" aria-label="工具分類" class="cvf-tabs">{tabs}</div></div>{panels}</div></section><section class="cvf-suite"><div class="cvf-container"><h2 class="cvf-title">所有工具。盡在一處。</h2><div class="cvf-two">{suite_html}</div></div></section><section class="cvf-template" id="templates"><h2 class="cvf-title">五花八門的範本</h2><div class="cvf-template-actions">{a('https://www.canva.com/zh_tw/signup/','免費開始設計','cvf-link cvf-purple')}{a('https://www.canva.com/zh_tw/templates/','瀏覽所有範本')}</div><div class="cvf-template-track" tabindex="0" aria-label="設計範本，可水平捲動">{templates}</div></section><section class="cvf-ecosystem"><div class="cvf-container"><h2 class="cvf-title">解鎖 Canva 的創意生態系統</h2><div class="cvf-cards">{cards(eco)}</div></div></section><section class="cvf-cta"><h2>開始使用 <em>Canva</em> 進行設計</h2>{a('https://www.canva.com/zh_tw/signup/','立即開始免費使用')}</section></main><footer class="cvf-footer"><div class="cvf-footer-grid">{foot}</div><div class="cvf-footer-bottom">繁體中文（台灣）　 ·　非官方設計參考，品牌及圖片屬各自權利人。　{a('https://www.canva.com/zh_tw/','前往 Canva 官網','')}</div></footer><script>(function(){{const tabs=[...document.querySelectorAll('[data-cvf-tab]')];function select(i){{tabs.forEach((t,n)=>{{t.setAttribute('aria-selected',String(n===i));t.tabIndex=n===i?0:-1;document.getElementById('cvf-panel-'+n).hidden=n!==i;}})}}tabs.forEach((t,i)=>{{t.addEventListener('click',()=>select(i));t.addEventListener('keydown',e=>{{if(e.key==='ArrowRight'||e.key==='ArrowLeft'){{e.preventDefault();let n=(i+(e.key==='ArrowRight'?1:-1)+tabs.length)%tabs.length;select(n);tabs[n].focus()}}}})}})}})();</script></body></html>'''
    (OUT/'canva.html').write_text(prefix+body)
    print('Canva full-page candidate prepared:', OUT/'canva.html')

if __name__=='__main__':main()
