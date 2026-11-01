#!/usr/bin/env python3
"""Record and integrate the reviewed Canva full-page study."""
from pathlib import Path
import hashlib
import json
import shutil
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
WORK=ROOT/'.stitch-work/current-official'
REVIEW=ROOT/'.test-artifacts/canva-full-2026-11-01'
SLUG='canva'
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def sha(b):return hashlib.sha256(b).hexdigest()

def main():
    lockpath=ROOT/'data/zh-TW/source-lock.json';locks=read(lockpath);lock=locks[SLUG]
    original=WORK/'canva.html'; assert sha(original.read_bytes())==lock['preview_sha256']
    data=(REVIEW/'canva.html').read_bytes();shot=REVIEW/'canva-1280.png'
    assert len(data)>100000 and shot.is_file() and Image.open(shot).size==(1280,720)
    newsha=sha(data); original.write_bytes(data)
    source=WORK/'canva-nov01-browser-desktop.png';shutil.copyfile(shot,source)
    analysis=WORK/'canva-nov01-analysis.md'
    analysis.write_text('''# Canva 官網首頁觀察

參考日期：2026-11-01，觀察繁體中文公開首頁。

首頁由紫藍青綠漸層、置中標題與兩排浮動圖片開始；往下依序是可切換的 AI、簡報、社交、影片及印刷分類，三欄不等寬功能卡、雙欄 Visual Suite 介紹、雙排範本、創意生態系統、漸層行動區及多欄頁尾。

本次參考公開首頁順序重製整頁，並使用已記錄來源的部分官網圖片。桌面首屏與主要章節經瀏覽器人工查看，並測試分類切換及窄版基本排版。內容、圖示、頁尾、動畫、載入時機和部分互動仍與官網不同；並未進行逐像素驗收。
''')
    remain=['依 2026-11-01 的 Canva 繁體中文公開首頁觀察，已重製主要區塊順序；部分圖像來自官網且版權屬原權利人。',
            '工具分頁可切換本機內容；部分連結開啟 Canva 官方網站。範本載入與播放、官網導覽、動畫、登入和服務未完整重現。',
            '已於 1280 及 390 像素檢查主要區塊與分類互動，未逐像素驗證全頁，其他尺寸與真實裝置未完整驗證。']
    resultpath=WORK/'canva-nov01-result.json';result=read(resultpath)
    result.update(preview_sha256=newsha,remaining_differences=remain);write(resultpath,result)
    lock['preview_sha256']=newsha;lock['source_documents']['analysis']['sha256']=sha(analysis.read_bytes())
    lock['remaining_sha256']=sha(json.dumps(remain,ensure_ascii=False,separators=(',',':')).encode())
    folder=ROOT/'design-md/canva';(folder/'preview.html').write_bytes(data);shutil.copyfile(shot,folder/'preview.png')
    im=Image.open(shot).convert('RGB');im.resize((640,400),Image.Resampling.LANCZOS).save(folder/'thumbnail.webp','WEBP',quality=85)
    stitchpath=folder/'STITCH.json';stitch=read(stitchpath)
    change='依官網公開首頁人工重製主要區塊與本機工具分頁；保留部分官網圖片，未重現全部互動。'
    if change not in stitch['changes']:stitch['changes'].append(change)
    stitch['scope']='人工重製的非官方 Canva 首頁參考，包含原權利人的部分圖片；視覺及互動仍有差異，非 Stitch 原始輸出。'
    stitch['width']=1280;stitch['height']=720
    stitch['files']={name:sha((folder/name).read_bytes()) for name in ('STITCH-PROMPT.md','preview.html','preview.png','thumbnail.webp')};write(stitchpath,stitch)
    coverpath=ROOT/'data/study-covers.json';covers=read(coverpath);c=next(x for x in covers['covers'] if x['slug']==SLUG)
    temp=ROOT/'assets/current-previews/canva-full-tmp.webp';im.resize((800,450),Image.Resampling.LANCZOS).save(temp,'WEBP',quality=82,method=6)
    cover_sha=sha(temp.read_bytes());cover=temp.with_name('canva-'+cover_sha[:16]+'.webp');temp.replace(cover)
    c.update(preview_sha256=newsha,result=dict(path=resultpath.name,sha256=sha(resultpath.read_bytes())),source=dict(path=source.name,sha256=sha(source.read_bytes()),method='本機瀏覽器截取重製後的 Canva 首頁。',observed_at='2026-11-01',dimensions=[1280,720]),image=dict(path=str(cover.relative_to(ROOT)),sha256=cover_sha,bytes=cover.stat().st_size,width=800,height=450,source_crop=[0,0,1280,720]))
    covers['bytes']=sum(x['image']['bytes'] for x in covers['covers']);write(coverpath,covers)
    contractpath=ROOT/'data/implementation/component-contracts.json';contracts=read(contractpath)
    contracts[SLUG]=['漸層首屏、五種工具分類、不等寬功能卡、產品介紹、雙排範本、生態系統與頁尾','工具分頁支援點擊及方向鍵；功能連結前往原站，範本僅供預覽。'];write(contractpath,contracts)
    recipepath=ROOT/'data/recipes.json';recipes=read(recipepath);entry=next(x for x in recipes if x['slug']==SLUG)
    entry.update(brief='製作視覺創作工具首頁，依序呈現漸層主視覺、工具分類與不等寬功能卡、產品介紹、範本展示、生態系統和頁尾。',component='工具分類分頁與不等寬功能卡，支援鍵盤切換並提供清楚狀態')
    write(recipepath,recipes);write(lockpath,locks)
    print('Canva full-page study integrated:',newsha)

if __name__=='__main__':main()
