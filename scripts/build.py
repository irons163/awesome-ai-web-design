#!/usr/bin/env python3
"""Build the catalog and ZIP from preserved Stitch exports; never generate mock previews."""
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


def metadata(entry, text, profile):
    # Catalog filters and swatches describe the current downloadable spec.
    # Keep the historical extended document only for its content/hash below.
    current = profile['colors']
    primary, canvas, ink = (current[key] for key in ('accent', 'canvas', 'ink'))
    font = re.search(r'fontFamily:\s*[\"\']?([^\n]+)',text)
    display_font = font[1].strip('\"\' ') if font else 'system-ui, sans-serif'
    # The specimen ships no proprietary font assets; use an explicit system fallback.
    serif = any(t in display_font.lower() for t in ('copernicus','tiempos','georgia','serif')) and 'sans-serif' not in display_font.lower()
    family = 'Georgia, serif' if serif or entry['slug']=='wired' else 'system-ui, sans-serif'
    colors = list(dict.fromkeys(current[key].lower() for key in ('accent','canvas','ink','surface','muted','border')))
    return dict(entry, categoryLabel=CATEGORY_LABELS[entry['category']],primary=primary,canvas=canvas,ink=ink,
                colors=colors, mode='dark' if luminance(canvas)<.25 else 'light', font=display_font,previewFont=family,
                implementationVersion=profile['version'],
                prompts=make_prompts(entry),bytes=len(text.encode()),sha256=hashlib.sha256(text.encode()).hexdigest())


def stitch_preview(path):
    provenance = path / 'STITCH.json'
    if not provenance.exists():
        return {'status': 'pending'}
    data = json.loads(provenance.read_text())
    for name, digest in data['files'].items():
        if hashlib.sha256((path / name).read_bytes()).hexdigest() != digest:
            raise ValueError(f'Stitch export checksum mismatch: {path.name}/{name}')
    return {'status': 'generated', 'provider': 'Google Stitch',
            'image': f"design-md/{path.name}/{data['screenshot']}",
            'thumbnail': f"design-md/{path.name}/{data.get('thumbnail', data['screenshot'])}",
            'html': f"design-md/{path.name}/preview.html",
            'provenance': f"design-md/{path.name}/STITCH.json",
            'prompt': f"design-md/{path.name}/STITCH-PROMPT.zh-TW.md",
            'projectId': data['project_id'], 'screenId': data['screen_id'],
            'title': data['title'], 'width': data['width'], 'height': data['height'],
            **({'localAssets': True, 'modified': True} if data.get('preview_is_modified') else {})}


def main():
    entries=[]
    profiles=json.loads((ROOT/'data/implementation/specs.json').read_text())['profiles']
    recipes=json.loads((ROOT/'data/recipes.json').read_text())
    if set(profiles) != {recipe['slug'] for recipe in recipes}:
        raise ValueError('Current implementation profiles must cover the complete catalog')
    for recipe in recipes:
        path=ROOT/'design-md'/recipe['slug']
        entry=metadata(recipe,(path/'DESIGN.md').read_text(),profiles[recipe['slug']]['profile'])
        entry['preview'] = stitch_preview(path)
        entries.append(entry)
    usage=json.loads((ROOT/'data/usage.json').read_text())
    catalog={'version':3,'locale':'zh-TW','startPrompt':usage['start_prompt'],'copyIntro':usage['copy_intro'],'generatedCount':sum(e['preview']['status']=='generated' for e in entries),'count':len(entries),'promptCount':len(entries)*3,'categories':CATEGORY_LABELS,'designs':entries}
    (ROOT/'assets/catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,separators=(',',':'))+'\n')
    readme=(ROOT/'README.md').read_text()
    collection=''
    for category,label in CATEGORY_LABELS.items():
        collection+=f'\n### {label}\n\n| 設計 | 特色 | 檔案 |\n| --- | --- | --- |\n'
        for entry in entries:
            if entry['category']==category:
                slug=entry['slug']
                collection+=f"| [{entry['name']}](design-md/{slug}/README.md) | {entry['description']} | [設計規格](design-md/{slug}/DESIGN.md) · [AI 指令](design-md/{slug}/PROMPTS.md) |\n"
    readme=re.sub(r'<!-- COLLECTION:START -->.*?<!-- COLLECTION:END -->','<!-- COLLECTION:START -->\n'+collection+'\n<!-- COLLECTION:END -->',readme,flags=re.S)
    (ROOT/'README.md').write_text(readme)
    paths=sorted(p for p in (ROOT/'design-md').rglob('*') if p.is_file())
    paths += [ROOT/p for p in ['LICENSE','ATTRIBUTION.md','README.md','VALIDATION.md']]
    paths += sorted((ROOT/'prompts').glob('*.md'))
    paths += [ROOT/p for p in ['index.html','assets/style.css','assets/app.js','assets/catalog.json','assets/favicon.svg','package.json','CONTRIBUTING.md','.gitignore']]
    paths += sorted((ROOT/'scripts').glob('*.py')) + sorted((ROOT/'data').rglob('*.json')) + sorted((ROOT/'tests').glob('*.py'))
    paths += sorted(p for p in (ROOT/'.github').rglob('*') if p.is_file())
    with zipfile.ZipFile(ROOT/'assets/all-designs.zip','w',zipfile.ZIP_DEFLATED) as archive:
        for path in paths:
            info=zipfile.ZipInfo(str(path.relative_to(ROOT)),date_time=(2026,9,22,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            archive.writestr(info,path.read_bytes())
    print(f"Built {len(entries)} designs, {catalog['generatedCount']} genuine Stitch previews, and all-designs.zip.")

if __name__=='__main__':
    main()
