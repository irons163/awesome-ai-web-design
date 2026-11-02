#!/usr/bin/env python3
"""Record reviewed, non-official full-page studies and provenance."""
from pathlib import Path
from PIL import Image
import hashlib,json,shutil
R=Path(__file__).resolve().parents[2];W=R/'.stitch-work/current-official';V=R/'.test-artifacts/five-latest-full-2026-11-01'
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def sha(b):return hashlib.sha256(b).hexdigest()
DATA={
'google':('Google','精簡導覽、置中品牌與搜尋、搜尋按鈕及頁尾','置中搜尋與精簡深色導覽'),
'youtube':('YouTube','搜尋導覽、側欄、分類列、影音結果與 Shorts 區塊','深色搜尋結果、16:9 影片縮圖與文字'),
'netflix':('Netflix','背景主視覺、熱門排行、服務特色、常見問題與頁尾','暗色海報主視覺與紅色按鈕、熱門海報及問答'),
'github':('GitHub','主視覺、產品示範、社群動態、平台、功能、企業、客戶故事與頁尾','白底大標、綠色操作與開發工具卡'),
'microsoft':('Microsoft','主視覺輪播、快速連結、Xbox 商品、Edge 橫幅、商務產品與頁尾','淺底雙欄主視覺、四欄產品卡與藍色操作')}


def main():
 lockpath=R/'data/zh-TW/source-lock.json';locks=read(lockpath);coverpath=R/'data/study-covers.json';covers=read(coverpath);cp=R/'data/implementation/component-contracts.json';contracts=read(cp);rp=R/'data/recipes.json';recipes=read(rp)
 for slug,(name,sections,brief) in DATA.items():
  page='搜尋結果頁' if slug=='youtube' else '首頁'
  lock=locks[slug]; original=W/(slug+'.html');assert sha(original.read_bytes())==lock['preview_sha256'],slug
  data=(V/(slug+'.html')).read_bytes();shot=V/(slug+'-1280.png');assert len(data)>8000 and Image.open(shot).size==(1280,720)
  newsha=sha(data);original.write_bytes(data);source=W/(slug+'-nov01-browser-desktop.png');shutil.copyfile(shot,source)
  analysis=W/(slug+'-nov01-analysis.md');analysis.write_text(f'# {name} 官網{page}觀察\n\n參考日期：2026-11-01，依公開{page}的主要區塊順序觀察。\n\n往下依序可見：{sections}。本次以人工方式重新製作主要版面，並使用部分已記錄來源的官網素材。\n\n預覽為設計研究而非官方網站。文字、商品、圖片、頁尾、互動及內容數量仍有差異，尤其官網動態或個人化內容會改變；未逐像素比對完整頁面，也未重現登入、購物或付款等真實服務。\n')
  remain=[f'依 2026-11-01 的 {name} 公開{page}觀察，重製往下捲動的主要區塊；部分圖片來自原站，權利屬原權利人。','部分官網的動態內容、圖片、文字、頁尾、導覽與服務未重現，部分連結會開啟官網。','已檢查 1280 與 390 像素的排版及部分示範互動；未逐像素驗證所有內容與真實裝置。']
  if slug=='youtube':remain.append('範例採用 2026-11-01 的 design 搜尋結果；結果、影片與 Shorts 會隨時間變動，短片圖片與內容以示意呈現。')
  if slug=='google':remain.append('官網搜尋首頁本身為短頁，沒有新增長頁內容。')
  resultpath=W/(slug+'-nov01-result.json');result=read(resultpath);result.update(preview_sha256=newsha,remaining_differences=remain);write(resultpath,result)
  lock['preview_sha256']=newsha;lock['source_documents']['analysis']['sha256']=sha(analysis.read_bytes());lock['remaining_sha256']=sha(json.dumps(remain,ensure_ascii=False,separators=(',',':')).encode())
  folder=R/'design-md'/slug;(folder/'preview.html').write_bytes(data);shutil.copyfile(shot,folder/'preview.png');im=Image.open(shot).convert('RGB');im.resize((640,400),Image.Resampling.LANCZOS).save(folder/'thumbnail.webp','WEBP',quality=85)
  sp=folder/'STITCH.json';stitch=read(sp);change='依官網公開首頁人工重製主要區塊；部分圖片屬原權利人，互動與動態內容未完全重現。'
  if change not in stitch['changes']:stitch['changes'].append(change)
  stitch['scope']=f'人工重製的非官方 {name} {page}參考，包含原權利人的部分圖片；視覺及互動仍有差異，非 Stitch 原始輸出。';stitch['width']=1280;stitch['height']=720;stitch['files']={n:sha((folder/n).read_bytes()) for n in ('STITCH-PROMPT.md','preview.html','preview.png','thumbnail.webp')};write(sp,stitch)
  c=next(x for x in covers['covers'] if x['slug']==slug);tmp=R/'assets/current-previews'/(slug+'-full-tmp.webp');im.resize((800,450),Image.Resampling.LANCZOS).save(tmp,'WEBP',quality=82,method=6);h=sha(tmp.read_bytes());cover=tmp.with_name(slug+'-'+h[:16]+'.webp');tmp.replace(cover)
  c.update(preview_sha256=newsha,result=dict(path=resultpath.name,sha256=sha(resultpath.read_bytes())),source=dict(path=source.name,sha256=sha(source.read_bytes()),method=f'本機瀏覽器截取重製後的 {name} {page}。',observed_at='2026-11-01',dimensions=[1280,720]),image=dict(path=str(cover.relative_to(R)),sha256=h,bytes=cover.stat().st_size,width=800,height=450,source_crop=[0,0,1280,720]))
  contracts[slug]=[brief,'主要連結前往原站；示範頁不提供真實帳戶、購物或付款服務。']
  entry=next(x for x in recipes if x['slug']==slug);entry.update(brief=f'製作{name}風格的參考{page}，依序呈現{sections}。',component=brief)
  print(slug,newsha)
 covers['bytes']=sum(x['image']['bytes'] for x in covers['covers']);write(coverpath,covers);write(cp,contracts);write(rp,recipes);write(lockpath,locks)
if __name__=='__main__':main()
