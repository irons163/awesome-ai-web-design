#!/usr/bin/env python3
"""Integrate reviewed first-screen revisions while preserving Stitch provenance."""
import hashlib
import json
import shutil
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / '.stitch-work/current-official'
REVIEW = ROOT / '.test-artifacts/direct-reference-2026-11-01/candidates'
SLUGS = ('canva', 'linkedin', 'paypal', 'etsy', 'khan-academy')
OBS = {
 'canva':'白色字的淡紫導覽下方，以紫藍綠漸層包住置中標題、操作及漂浮素材。',
 'linkedin':'白底導覽搭配藍色按鈕；首屏左側是標題與垂直排列的膠囊操作，右側是大型人物插畫。',
 'paypal':'白色導覽後接淺藍色首屏，上方是個人與公司切換，中間為黑色大標，下面放白色圓角圖片卡。',
 'etsy':'橘色品牌字旁排列大型膠囊搜尋，分類導覽下方是左寬右窄的圖片主題磚。',
 'khan-academy':'白色導覽中央為識別；首屏左側是學習主題大標與說明，右側垂直排列學生、家長和教師三張卡。',
}
CONTRACTS = {
 'canva':['置中標題、主要按鈕、浮動素材與範本分類','按鈕前往下方示範範本；不提供真實編輯服務。'],
 'linkedin':['職涯介紹標題、膠囊按鈕、大型插畫及示範主題','按鈕前往本機示範內容；沒有帳戶登入或真實職缺。'],
 'paypal':['個人及公司切換、置中標題、圓角圖片卡','切換頁首標題；示範不提供付款、轉帳或金融服務。'],
 'etsy':['分類導覽、膠囊搜尋、主題磚、示範搜尋及收藏','入口前往本機示範資料；不提供真實購物。'],
 'khan-academy':['置中識別、學習標題、學生家長教師入口及示範課程','角色入口前往示範課程；不建立帳號。'],
}

def sha(data): return hashlib.sha256(data).hexdigest()
def read(path): return json.loads(path.read_text())
def write(path, data): path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')

def main():
    locks_path=ROOT/'data/zh-TW/source-lock.json'
    covers_path=ROOT/'data/study-covers.json'
    directions_path=ROOT/'data/implementation/brand-directions.json'
    contracts_path=ROOT/'data/implementation/component-contracts.json'
    locks, covers, directions, contracts = (read(p) for p in (locks_path,covers_path,directions_path,contracts_path))
    for slug in SLUGS:
        html=(REVIEW/f'{slug}.html').read_bytes()
        shot=REVIEW/f'{slug}-1280.png'
        assert html.startswith(b'<!') and shot.is_file()
        old=locks[slug]['preview_sha256']
        assert sha((WORK/f'{slug}.html').read_bytes()) == old, slug
        preview_sha=sha(html)
        (WORK/f'{slug}.html').write_bytes(html)
        source=WORK/f'{slug}-nov01-browser-desktop.png'
        shutil.copyfile(shot,source)
        analysis=WORK/f'{slug}-nov01-analysis.md'
        analysis.write_text(f'# {locks[slug]["name"]} 參考觀察\n\n參考日期：2026-11-01。\n\n{OBS[slug]}\n\n首屏依公開首頁重新製作；Canva、LinkedIn、PayPal、Etsy 使用公開來源圖片或標誌，文字部分以繁體中文表達。延伸互動是另外設計的示範。尚未逐像素或逐項比對，無法保證與官網完全相同。\n')
        remain=['首屏以 2026-11-01 所見的公開首頁為參考重新製作；部分圖片和標誌來自原官網，部分文字、插畫和互動為自行設計。',
                '下方保留獨立設計的互動示範，與官網內容不同；不提供真實帳戶、購物、付款或其他品牌服務。',
                '已在 390 及 1280 像素檢查基本顯示，並對照 1280 像素首屏；其他尺寸、整頁與全部互動尚未完整比對，未進行逐像素驗證。']
        result_path=WORK/f'{slug}-nov01-result.json'; result=read(result_path)
        result['preview_sha256']=preview_sha;result['remaining_differences']=remain;write(result_path,result)
        locks[slug]['preview_sha256']=preview_sha
        locks[slug]['source_documents']['analysis']['sha256']=sha(analysis.read_bytes())
        locks[slug]['remaining_sha256']=sha(json.dumps(remain,ensure_ascii=False,separators=(',',':')).encode())
        folder=ROOT/'design-md'/slug
        (folder/'preview.html').write_bytes(html);shutil.copyfile(shot,folder/'preview.png')
        im=Image.open(shot).convert('RGB');im.resize((640,400),Image.Resampling.LANCZOS).save(folder/'thumbnail.webp','WEBP',quality=85)
        stitch=read(folder/'STITCH.json')
        stitch['changes'].append('再度依 1280 像素官網畫面重製首屏；部分使用公開來源圖片與標誌，非 Stitch 原始輸出；下方延伸互動為獨立示範。')
        stitch['scope']='首屏為人工重製的設計參考，部分使用原官網素材；非 Stitch 原始輸出或品牌官方網站。下方內容不同，整頁尚未驗收。'
        stitch['width']=1280;stitch['height']=720
        stitch['files']={name:sha((folder/name).read_bytes()) for name in ('STITCH-PROMPT.md','preview.html','preview.png','thumbnail.webp')}
        write(folder/'STITCH.json',stitch)
        cover_data=next(x for x in covers['covers'] if x['slug']==slug)
        tmp=ROOT/'assets/current-previews'/f'{slug}-revision-tmp.webp'
        im.crop((0,0,1280,720)).resize((800,450),Image.Resampling.LANCZOS).save(tmp,'WEBP',quality=82,method=6)
        cover_sha=sha(tmp.read_bytes());cover=tmp.with_name(f'{slug}-{cover_sha[:16]}.webp');tmp.replace(cover)
        cover_data.update(preview_sha256=preview_sha,
            result=dict(path=result_path.name,sha256=sha(result_path.read_bytes())),
            source=dict(path=source.name,sha256=sha(source.read_bytes()),method='本機瀏覽器截取人工重製的首屏。',observed_at='2026-11-01',dimensions=[1280,720]),
            image=dict(path=str(cover.relative_to(ROOT)),sha256=cover_sha,bytes=cover.stat().st_size,width=800,height=450,source_crop=[0,0,1280,720]))
        contracts[slug]=CONTRACTS[slug]
        print(slug,'updated')
    directions['paypal'][-1]='淺藍首屏、個人／公司切換、置中黑色大標與白色圓角圖片卡。'
    directions['khan-academy'][0]='#5149d6'
    covers['bytes']=sum(x['image']['bytes'] for x in covers['covers'])
    for path,data in ((locks_path,locks),(covers_path,covers),(directions_path,directions),(contracts_path,contracts)):write(path,data)

if __name__=='__main__': main()
