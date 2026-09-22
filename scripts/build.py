#!/usr/bin/env python3
"""Build the static catalog, token specimens, index, and deterministic ZIP."""
import hashlib
import html
import json
import re
import zipfile
from pathlib import Path
from rewrite_prompts import make_prompts

ROOT = Path(__file__).resolve().parents[1]
CATEGORY_LABELS = {
    'AI & LLM Platforms':'AI 與模型', 'Developer Tools & IDEs':'開發工具',
    'Backend, Database & DevOps':'後端與資料', 'Productivity & SaaS':'生產力工具',
    'Design & Creative Tools':'設計與創作', 'Fintech & Crypto':'金融科技',
    'E-commerce & Retail':'電商與零售', 'Media & Consumer Tech':'媒體與科技',
    'Automotive':'汽車', 'Retro Web · DESIGN.md Nostalgia':'復古網頁',
}
# These files express tokens in prose instead of YAML. Values are taken from their analysis.
PROSE = {
    'kraken':('#7132f5','#ffffff','#101114'), 'lamborghini':('#FFC000','#000000','#FFFFFF'),
    'lovable':('#1c1c1c','#f7f4ed','#1c1c1c'), 'mastercard':('#CF4500','#F3F0EE','#141413'),
    'runwayml':('#000000','#ffffff','#000000'), 'sanity':('#f36458','#0b0b0b','#ededed'),
    'spotify':('#1ed760','#121212','#ffffff'), 'starbucks':('#00754A','#f2f0eb','#1E3932'),
    'tesla':('#3E6AE1','#FFFFFF','#171A20'), 'theverge':('#3cffd0','#131313','#ffffff'),
}


def rgb(value):
    return tuple(int(value[i:i+2],16)/255 for i in (1,3,5))


def luminance(value):
    return sum(w*(v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4) for w,v in zip((.2126,.7152,.0722),rgb(value)))


def contrast_ink(value):
    light = (1.05)/(luminance(value)+.05)
    dark = (luminance(value)+.05)/.05
    return '#ffffff' if light>dark else '#000000'


def mix(a,b,amount):
    return '#'+''.join(f'{round(x*(1-amount)*255+y*amount*255):02x}' for x,y in zip(rgb(a),rgb(b)))


def metadata(entry, text):
    match = re.search(r'^colors:\n(.*?)(?=^\S|\Z)',text,re.M|re.S)
    tokens = dict(re.findall(r'^  ([\w-]+):\s*[\"\']?(#[\da-fA-F]{6})',match[1],re.M)) if match else {}
    all_colors = list(dict.fromkeys(c.lower() for c in re.findall(r'#[\da-fA-F]{6}\b',text)))
    primary, canvas, ink = PROSE.get(entry['slug'],(
        tokens.get('primary',tokens.get('accent',all_colors[0])),
        tokens.get('canvas',tokens.get('background','#ffffff')),
        tokens.get('ink',tokens.get('text-primary','#171717')),
    ))
    font = re.search(r'fontFamily:\s*[\"\']?([^\n]+)',text)
    display_font = font[1].strip('\"\' ') if font else 'system-ui, sans-serif'
    # The specimen ships no proprietary font assets; use an explicit system fallback.
    serif = any(t in display_font.lower() for t in ('copernicus','tiempos','georgia','serif')) and 'sans-serif' not in display_font.lower()
    family = 'Georgia, serif' if serif or entry['slug']=='wired' else 'system-ui, sans-serif'
    colors = list(dict.fromkeys([primary.lower(),canvas.lower(),ink.lower()]+all_colors))[:6]
    return dict(entry, categoryLabel=CATEGORY_LABELS[entry['category']],primary=primary,canvas=canvas,ink=ink,
                colors=colors, mode='dark' if luminance(canvas)<.25 else 'light', font=display_font,previewFont=family,
                prompts=make_prompts(entry),bytes=len(text.encode()),sha256=hashlib.sha256(text.encode()).hexdigest())


def preview(entry, mode):
    name = html.escape(entry['name'])
    native = entry['mode']==mode
    canvas = entry['canvas'] if native else ('#111215' if mode=='dark' else '#fafaf8')
    ink = contrast_ink(canvas)
    panel = mix(canvas,ink,.045)
    muted = mix(canvas,ink,.64)
    border = mix(canvas,ink,.18)
    accent = entry['primary']
    # Retain the documented swatch; select readable foregrounds for interactive samples.
    styles = f'--canvas:{canvas};--panel:{panel};--ink:{ink};--muted:{muted};--border:{border};--accent:{accent};--on-accent:{contrast_ink(accent)};--display:{entry["previewFont"]}'
    swatches = ''.join(f'<div class="swatch"><span style="background:{color}"></span><code>{color}</code></div>' for color in entry['colors'])
    return f'''<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{name} · {mode} token preview</title><link rel="stylesheet" href="../../assets/preview.css"></head>
<body style="{styles}"><main class="specimen"><header class="specimen-header"><a target="_top" href="../../index.html#/design/{entry['slug']}">← 回到設計集</a><span>{mode.upper()} / TOKEN SPECIMEN</span></header>
<section class="sample-hero"><p class="eyebrow">{name} · DESIGN REFERENCE</p><h1>Good design.<br>Clear direction.</h1><p>把色彩、文字與元件放在一起，找到適合你的設計語言。</p><div class="actions"><a class="primary" href="DESIGN.md" download>下載 DESIGN.md ↗</a><a class="secondary" href="PROMPTS.md" download>取得 AI 指令</a></div></section>
<section class="palette"><h2>01 / Color palette</h2><div class="swatches">{swatches}</div></section>
<section class="samples"><article class="sample-card"><p class="eyebrow">02 / TYPOGRAPHY</p><h2>A little more<br>room to think.</h2><p>以清楚的層級引導閱讀，讓每段文字都有合適的位置。</p><small>系統替代字體示意 · {html.escape(entry['font'])}</small></article>
<form class="sample-card" id="sample-form"><p class="eyebrow">03 / COMPONENTS</p><h2>Make it yours.</h2><label for="project">專案名稱</label><input id="project" name="project" placeholder="我的下一個作品" required maxlength="100"><button class="primary" type="submit">儲存示範設定 →</button><p id="sample-status" role="status">這是本機互動示範，資料不會送出。</p></form></section>
<footer>設計 token 示意，非品牌網站截圖。{'此模式沿用參考底色。' if native else '此模式為本專案延伸配色。'}<br>視覺分析：VoltAgent（MIT）；預覽：Awesome AI Web Design。</footer></main><script src="../../assets/preview.js"></script></body></html>'''


def main():
    entries=[]
    for recipe in json.loads((ROOT/'data/recipes.json').read_text()):
        path=ROOT/'design-md'/recipe['slug']
        entry=metadata(recipe,(path/'DESIGN.md').read_text())
        entries.append(entry)
        (path/'preview.html').write_text(preview(entry,'light'))
        (path/'preview-dark.html').write_text(preview(entry,'dark'))
    catalog={'version':1,'count':len(entries),'promptCount':len(entries)*3,'categories':CATEGORY_LABELS,'designs':entries}
    (ROOT/'assets/catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,separators=(',',':'))+'\n')
    readme=(ROOT/'README.md').read_text()
    collection=''
    for category,label in CATEGORY_LABELS.items():
        collection+=f'\n### {label} / {category}\n\n| 設計 | 特色 | 檔案 |\n| --- | --- | --- |\n'
        for entry in entries:
            if entry['category']==category:
                slug=entry['slug']
                collection+=f"| [{entry['name']}](design-md/{slug}/README.md) | {entry['description']} | [DESIGN.md](design-md/{slug}/DESIGN.md) · [Prompts](design-md/{slug}/PROMPTS.md) |\n"
    readme=re.sub(r'<!-- COLLECTION:START -->.*?<!-- COLLECTION:END -->','<!-- COLLECTION:START -->\n'+collection+'\n<!-- COLLECTION:END -->',readme,flags=re.S)
    (ROOT/'README.md').write_text(readme)
    paths=sorted(p for p in (ROOT/'design-md').rglob('*') if p.is_file())
    paths += [ROOT/p for p in ['LICENSE','ATTRIBUTION.md','README.md','assets/preview.css','assets/preview.js']]
    paths += sorted((ROOT/'prompts').glob('*.md'))
    paths += [ROOT/p for p in ['index.html','assets/style.css','assets/app.js','assets/catalog.json','assets/favicon.svg','package.json','CONTRIBUTING.md','.gitignore']]
    paths += sorted((ROOT/'scripts').glob('*.py')) + sorted((ROOT/'data').glob('*.json')) + sorted((ROOT/'tests').glob('*.py'))
    paths += sorted(p for p in (ROOT/'.github').rglob('*') if p.is_file())
    with zipfile.ZipFile(ROOT/'assets/all-designs.zip','w',zipfile.ZIP_DEFLATED) as archive:
        for path in paths:
            info=zipfile.ZipInfo(str(path.relative_to(ROOT)),date_time=(2026,9,22,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            archive.writestr(info,path.read_bytes())
    print(f'Built {len(entries)} designs, {len(entries)*2} previews, and all-designs.zip.')

if __name__=='__main__':
    main()
