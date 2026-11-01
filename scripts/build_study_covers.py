"""Derive catalog covers from retained, current-study browser screenshots."""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT/'.stitch-work/current-official'

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--source',default='data/study-covers.json')
    args=parser.parse_args()
    records=json.loads((ROOT/args.source).read_text())['covers']
    expected={r['slug'] for r in json.loads((ROOT/'data/recipes.json').read_text())}
    if {r['slug'] for r in records}!=expected or len(records)!=len(expected):raise ValueError('Expected one cover per current study')
    out=ROOT/'assets/current-previews';out.mkdir(exist_ok=True)
    total=0;replaced=[]
    for record in records:
        for key in ['source','result']:
            path=WORK/record[key]['path'];path.resolve().relative_to(WORK.resolve())
            if digest(path)!=record[key]['sha256']:raise ValueError('Changed source: '+str(path))
        if digest(WORK/(record['brand']+'.html'))!=record['preview_sha256']:raise ValueError('Stale cover source: '+record['brand'])
        source=Image.open(WORK/record['source']['path']).convert('RGB')
        height=round(source.width*9/16)
        canvas=Image.new('RGB',(source.width,height),'white')
        top=record['source'].get('crop_top',0)
        crop=[0,top,source.width,min(source.height,top+height)]
        canvas.paste(source.crop(crop),(0,0))
        canvas=canvas.resize((800,450),Image.Resampling.LANCZOS)
        temporary=out/'cover.tmp.webp';canvas.save(temporary,'WEBP',quality=82,method=6)
        sha=digest(temporary);path=out/(record['slug']+'-'+sha[:16]+'.webp');temporary.replace(path)
        if record.get('image',{}).get('path')!=str(path.relative_to(ROOT)) and record.get('image',{}).get('path'):replaced.append(ROOT/record['image']['path'])
        record['source']['dimensions']=list(source.size)
        record['image']={'path':str(path.relative_to(ROOT)),'sha256':sha,'bytes':path.stat().st_size,'width':800,'height':450,'source_crop':crop}
        total+=path.stat().st_size
    manifest={'method':'Viewport excerpts of actual corrected-study browser rasters, resized to800×450 WebP. Each cover is bound to the current preview and review digests; the source crop is explicit.','count':len(records),'bytes':total,'covers':records}
    (ROOT/'data/study-covers.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    for file in replaced:
        file.resolve().relative_to(out.resolve());file.unlink(missing_ok=True)
    print(json.dumps({'covers':len(records),'bytes':total}))

if __name__=='__main__':main()
