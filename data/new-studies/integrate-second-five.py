#!/usr/bin/env python3
"""Integrate the five reviewed Stitch web exports and their source evidence."""
import hashlib
import json
import re
import shutil
import zipfile
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / '.stitch-work/current-official'
EVIDENCE = ROOT / '.test-artifacts/five-more-designs-2026-11-01'
REVIEW = EVIDENCE / 'review-previews'
DATE = '2026-11-01'
PROJECTS = {'wikipedia':'14294780808015204309', 'amazon':'7793494073016662871',
            'discord':'14110822146277849317', 'duolingo':'5838844978517462087',
            'ikea':'5357435934024460494'}
SCREENS = {}
DIRECTIONS = {
    'wikipedia':['#4168c6','#101418','#e6e9ee','#202832','knowledge-portal','深色入口、置中圓形識別、對稱語言清單與下方搜尋。'],
    'amazon':['#f3a847','#ffffff','#131921','#f3f4f4','marketplace','深色雙層搜尋導覽、三個主題色塊與商品卡片。'],
    'discord':['#5865f2','#11131c','#ffffff','#27265e','community','深色藍紫漸層、大標題與聊天室互動示意。'],
    'duolingo':['#58cc02','#ffffff','#262c30','#f5f5f5','learning','白色留白、綠色立體按鈕與原創書本星星插畫。'],
    'ikea':['#39684e','#ffffff','#111111','#f5f5f5','home-inspiration','白底精簡導覽、灰色搜尋欄與比例不等的居家靈感磚。'],
}
CONTRACTS = {
    'wikipedia':['搜尋文字、語言選擇、結果清單與空結果','輸入時篩選本機示範條目，可清除文字並切換語言，不連接真實百科。'],
    'amazon':['商品名稱、分類、示範價格、篩選條件與清單數量','搜尋及分類更新可見卡片；加入清單後顯示數量，沒有真實訂單或付款。'],
    'discord':['頻道名稱、本機訊息、輸入欄位與展開狀態','切換頻道可查看範例對話；輸入文字以純文字顯示，訊息不發送到伺服器。'],
    'duolingo':['題目、選項、選取狀態與答案回饋','選擇答案後可檢查並看到結果；僅一題本機示範，不建立學習帳戶。'],
    'ikea':['商品名稱、分類、示範價格、收藏狀態與搜尋條件','分類與搜尋更新商品；收藏按鈕與計數同步，沒有真實購物或配送服務。'],
}


def read(path): return json.loads(path.read_text())
def write(path, data): path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
def digest(data): return hashlib.sha256(data if isinstance(data, bytes) else data.encode()).hexdigest()


def main():
    recipes_path = ROOT / 'data/recipes.json'
    recipes = read(recipes_path)
    briefs = read(ROOT / 'data/new-studies/briefs-second-five-2026-11-01.json')['studies']
    if {b['slug'] for b in briefs} & {r['slug'] for r in recipes}:
        raise ValueError('At least one new design already exists; do not overwrite it')
    paths = {'styles': ROOT/'data/zh-TW/design-sources.json', 'locks': ROOT/'data/zh-TW/source-lock.json',
             'directions': ROOT/'data/implementation/brand-directions.json',
             'contracts': ROOT/'data/implementation/component-contracts.json',
             'progress': WORK/'progress.json', 'covers': ROOT/'data/study-covers.json'}
    data = {key:read(path) for key,path in paths.items()}
    for brief in briefs:
        slug, name = brief['slug'], brief['name']
        archive_path = EVIDENCE / f'{slug}-stitch.zip'
        preview = (REVIEW / f'{slug}.html').read_bytes()
        screenshot = REVIEW / f'{slug}-1440-final.png'
        if not archive_path.is_file() or not screenshot.is_file() or not preview.startswith(b'<!'):
            raise ValueError('Missing reviewed export or screenshot: '+slug)
        with zipfile.ZipFile(archive_path) as archive:
            original_html = archive.read('code.html')
            original_design = archive.read('DESIGN.md')
            original_screen = archive.read('screen.png')
        folder = ROOT / 'design-md' / slug
        if folder.exists(): raise ValueError('Refusing to replace existing folder: '+slug)
        folder.mkdir()
        (folder/'preview.html').write_bytes(preview)
        (folder/'STITCH-PROMPT.md').write_text(brief['stitch_prompt'])
        shutil.copy2(screenshot, folder/'preview.png')
        im = Image.open(screenshot).convert('RGB')
        im.resize((640, 400), Image.Resampling.LANCZOS).save(folder/'thumbnail.webp', 'WEBP', quality=85)
        record = dict(provider='Google Stitch', transport='web', status='generated', project_id=PROJECTS[slug],
                      screen_id=SCREENS.get(slug), screen_name=(f'projects/{PROJECTS[slug]}/screens/{SCREENS[slug]}' if slug in SCREENS else None),
                      title=name+' 風格設計示範', width=1440, height=900, screenshot='preview.png', thumbnail='thumbnail.webp',
                      local_assets=True, preview_is_modified=True, original_export_sha256=digest(archive_path.read_bytes()),
                      original_html_sha256=digest(original_html), original_screen_sha256=digest(original_screen),
                      original_design_sha256=digest(original_design), observed_at=DATE,
                      changes=['公開預覽依 Stitch 輸出調整，移除未經驗證的服務與效能敘述，並以純文字處理聊天輸入。',
                               '使用本機樣式、向量替代圖示與圖片，補上示範說明並修正窄版溢出。',
                               '公開截圖取自調整後的本機瀏覽器，並非 Stitch 原始匯出截圖。'],
                      scope='生成的原創範例，並非品牌官方網站；尚未完成全面互動或視覺一致性驗收。')
        record['files']={name:digest((folder/name).read_bytes()) for name in ('STITCH-PROMPT.md','preview.html','preview.png','thumbnail.webp')}
        write(folder/'STITCH.json',record)

        (WORK/f'{slug}.html').write_bytes(preview)
        current = digest(preview)
        analysis_name, prompt_name = f'{slug}-nov01-analysis.md', f'{slug}-nov01-prompt.md'
        (WORK/analysis_name).write_text(f'# {name} 參考觀察\n\n參考日期：{DATE}。\n\n{brief["observation"]}\n\n這是公開頁面的有限觀察，尺寸與完整互動尚未全面比對；設計方向不代表官方授權。\n')
        (WORK/prompt_name).write_text(f'# {name} 生成請求\n\n{brief["stitch_prompt"]}\n')
        remaining = ['這是根據公開頁面方向產生的原創示範，與品牌官網不同；尚未逐一比對完整頁面及所有互動。',
                     '主要預覽經人工修改及重新截圖，與 Stitch 原始匯出不同；真實帳戶、購物、付款、影片或搜尋後端未串接。',
                     '已在 390 與 1440 像素檢查基本排版和代表性操作；其他尺寸、裝置與全部鍵盤路徑尚未完整驗證。']
        result_name = f'{slug}-nov01-result.json'
        write(WORK/result_name, dict(preview_sha256=current, observed_at=DATE, reference_url=brief['reference_url'],
                                      status='draft_unverified', remaining_differences=remaining,
                                      designAnalysis=analysis_name, rewrittenPrompt=prompt_name))
        paths_by_kind = {'analysis':analysis_name, 'prompts':prompt_name}
        source_docs = {kind:dict(path='official-drafts/'+filename,sha256=digest((WORK/filename).read_bytes()))
                       for kind,filename in paths_by_kind.items()}
        data['locks'][slug] = dict(name=name,file=slug,date=DATE,reference_url=brief['reference_url'],
            preview_sha256=current,study={kind:'official-drafts/'+filename for kind,filename in paths_by_kind.items()},
            source_documents=source_docs,remaining_sha256=digest(json.dumps(remaining,ensure_ascii=False,separators=(',',':'))))
        data['progress'][slug] = dict(status='draft_unverified',reference_url=brief['reference_url'],observed_at=DATE,preview=slug+'.html')
        fm = original_design.decode().split('---',2)[1]
        colors = re.search(r'(?ms)^colors:\s*\n(?:[ \t]+.*\n)+', fm)
        if not colors: raise ValueError('Missing Stitch color tokens: '+slug)
        data['styles'][slug] = dict(source_git_ref='Google Stitch 網頁專案 '+PROJECTS[slug],source_sha256=digest(original_design),
                                    tokens=colors.group(0).rstrip(),inline_values=brief['suggested_palette'],type_tables=[])
        data['directions'][slug], data['contracts'][slug] = DIRECTIONS[slug], CONTRACTS[slug]
        source_name = f'{slug}-nov01-browser-desktop.png'
        shutil.copy2(screenshot,WORK/source_name)
        crop = im.crop((0,0,1440,810)).resize((800,450),Image.Resampling.LANCZOS)
        temp = ROOT/'assets/current-previews'/f'{slug}-tmp.webp'
        crop.save(temp,'WEBP',quality=82,method=6)
        cover_sha = digest(temp.read_bytes())
        cover = temp.with_name(f'{slug}-{cover_sha[:16]}.webp')
        temp.replace(cover)
        data['covers']['covers'].append(dict(slug=slug,brand=slug,preview_sha256=current,
            result=dict(path=result_name,sha256=digest((WORK/result_name).read_bytes())),
            source=dict(path=source_name,sha256=digest((WORK/source_name).read_bytes()),method='本機瀏覽器檢查調整後的預覽。',observed_at=DATE,dimensions=[1440,900]),
            image=dict(path=str(cover.relative_to(ROOT)),sha256=cover_sha,bytes=cover.stat().st_size,width=800,height=450,source_crop=[0,0,1440,810])))
        recipes.append({key:brief[key] for key in ('slug','name','category','description','brief','component')})
        print('Integrated local evidence for',slug)
    data['covers']['count']=len(data['covers']['covers'])
    data['covers']['bytes']=sum(item['image']['bytes'] for item in data['covers']['covers'])
    for key,path in paths.items():write(path,data[key])
    write(recipes_path,recipes)


if __name__ == '__main__':main()
