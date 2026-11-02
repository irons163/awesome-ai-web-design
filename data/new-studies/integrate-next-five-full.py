#!/usr/bin/env python3
"""Record reviewed, non-official full-page studies and provenance."""
from pathlib import Path
from PIL import Image
import hashlib,json,shutil
R=Path(__file__).resolve().parents[2];W=R/'.stitch-work/current-official';V=R/'.test-artifacts/next-five-full-2026-11-01'
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def sha(b):return hashlib.sha256(b).hexdigest()
DATA={
'wikipedia':('Wikipedia','置中名稱、地球與多語言入口、搜尋、更多語言、基金會、相關專案與頁尾','地球與語言入口、搜尋及相關專案'),
'amazon':('Amazon','深色導覽與搜尋、活動主視覺、商品分類格線、推薦提示與多欄頁尾','深色搜尋導覽、橫向活動圖與商品分類卡'),
'discord':('Discord','漸層主視覺、群組聊天、直播分享、加入聊天、揪團、共同活動、跨裝置與頁尾','深藍紫主視覺與六組交錯圓角圖文'),
'duolingo':('Duolingo','學習主視覺、語言列、免費學習、教學、學習動力、個人化、應用程式、Super、英語測驗與頁尾','綠色操作、橫向課程與交錯學習插圖'),
'ikea':('IKEA','搜尋導覽、活動圖磚、系列推薦、服務與安全資訊、會員優惠、佈置靈感與頁尾','不等寬活動圖磚、系列推薦與服務資訊')}

def main():
 lockpath=R/'data/zh-TW/source-lock.json';locks=read(lockpath);coverpath=R/'data/study-covers.json';covers=read(coverpath);cp=R/'data/implementation/component-contracts.json';contracts=read(cp);rp=R/'data/recipes.json';recipes=read(rp)
 for slug,(name,sections,brief) in DATA.items():
  lock=locks[slug]; original=W/(slug+'.html');assert sha(original.read_bytes())==lock['preview_sha256'],slug
  data=(V/(slug+'.html')).read_bytes();shot=V/(slug+'-1280.png');assert len(data)>25000 and Image.open(shot).size==(1280,720)
  newsha=sha(data);original.write_bytes(data);source=W/(slug+'-nov01-browser-desktop.png');shutil.copyfile(shot,source)
  analysis=W/(slug+'-nov01-analysis.md');analysis.write_text(f'# {name} 官網首頁觀察\n\n參考日期：2026-11-01，依公開首頁的主要區塊順序觀察。\n\n往下依序可見：{sections}。本次以人工方式重新製作主要版面，並使用部分已記錄來源的官網素材。\n\n預覽為設計研究而非官方網站。文字、商品、圖片、頁尾、互動及內容數量仍有差異，尤其官網動態或個人化內容會改變；未逐像素比對完整頁面，也未重現登入、購物或付款等真實服務。\n')
  remain=[f'依 2026-11-01 的 {name} 公開首頁觀察，重製往下捲動的主要區塊；部分圖片來自原站，權利屬原權利人。','部分官網的動態內容、圖片、文字、頁尾、導覽與服務未重現，部分連結會開啟官網。','已檢查 1280 與 390 像素的排版及部分示範互動；未逐像素驗證所有內容與真實裝置。']
  resultpath=W/(slug+'-nov01-result.json');result=read(resultpath);result.update(preview_sha256=newsha,remaining_differences=remain);write(resultpath,result)
  lock['preview_sha256']=newsha;lock['source_documents']['analysis']['sha256']=sha(analysis.read_bytes());lock['remaining_sha256']=sha(json.dumps(remain,ensure_ascii=False,separators=(',',':')).encode())
  folder=R/'design-md'/slug;(folder/'preview.html').write_bytes(data);shutil.copyfile(shot,folder/'preview.png');im=Image.open(shot).convert('RGB');im.resize((640,400),Image.Resampling.LANCZOS).save(folder/'thumbnail.webp','WEBP',quality=85)
  sp=folder/'STITCH.json';stitch=read(sp);change='依官網公開首頁人工重製主要區塊；部分圖片屬原權利人，互動與動態內容未完全重現。'
  if change not in stitch['changes']:stitch['changes'].append(change)
  stitch['scope']=f'人工重製的非官方 {name} 首頁參考，包含原權利人的部分圖片；視覺及互動仍有差異，非 Stitch 原始輸出。';stitch['width']=1280;stitch['height']=720;stitch['files']={n:sha((folder/n).read_bytes()) for n in ('STITCH-PROMPT.md','preview.html','preview.png','thumbnail.webp')};write(sp,stitch)
  c=next(x for x in covers['covers'] if x['slug']==slug);tmp=R/'assets/current-previews'/(slug+'-full-tmp.webp');im.resize((800,450),Image.Resampling.LANCZOS).save(tmp,'WEBP',quality=82,method=6);h=sha(tmp.read_bytes());cover=tmp.with_name(slug+'-'+h[:16]+'.webp');tmp.replace(cover)
  c.update(preview_sha256=newsha,result=dict(path=resultpath.name,sha256=sha(resultpath.read_bytes())),source=dict(path=source.name,sha256=sha(source.read_bytes()),method=f'本機瀏覽器截取重製後的 {name} 首頁。',observed_at='2026-11-01',dimensions=[1280,720]),image=dict(path=str(cover.relative_to(R)),sha256=h,bytes=cover.stat().st_size,width=800,height=450,source_crop=[0,0,1280,720]))
  contracts[slug]=[brief,'主要連結前往原站；示範頁不提供真實帳戶、購物或付款服務。']
  entry=next(x for x in recipes if x['slug']==slug);entry.update(brief=f'製作{name}風格的參考首頁，依序呈現{sections}。',component=brief)
  print(slug,newsha)
 covers['bytes']=sum(x['image']['bytes'] for x in covers['covers']);write(coverpath,covers);write(cp,contracts);write(rp,recipes);write(lockpath,locks)
if __name__=='__main__':main()
