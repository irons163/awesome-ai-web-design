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
EVIDENCE = ROOT / '.test-artifacts/five-new-designs-2026-11-01'
REVIEW = EVIDENCE / 'review-previews'
DATE = '2026-11-01'
PROJECTS = {'google':'11802698461431083906', 'youtube':'8916368574112371506',
            'netflix':'4042150818544829071', 'github':'7340037193447218715',
            'microsoft':'12260637069137934999'}
SCREENS = {'github':'930b874c990542c68f9e5789282aba9a'}
DIRECTIONS = {
    'google':['#a8c7fa','#22242a','#e8eaf2','#303134','search-home','深灰背景、置中識別與膠囊搜尋框，保留充足留白與精簡導覽。'],
    'youtube':['#ff0033','#0f0f0f','#f1f1f1','#272727','video-results','深色搜尋介面、精簡導覽、水平篩選標籤與影音結果清單。'],
    'netflix':['#e50914','#000000','#ffffff','#232323','streaming','深黑背景、紅色主要操作、置中大標與可瀏覽的內容卡。'],
    'github':['#1f883d','#ffffff','#1f2328','#f6f8fa','collaboration','白底綠色操作、置中標題與帶分頁的程式碼示範面板。'],
    'microsoft':['#0067b8','#ffffff','#0e1726','#f2f2f2','product-catalog','白色精簡導覽、藍色操作、產品圖文主視覺與規格卡片。'],
}
CONTRACTS = {
    'google':['查詢文字、建議詞、清除操作、搜尋結果與空白狀態','輸入時顯示本機建議；可清除、用鍵盤選取並送出，無結果時提供清楚提示，不連接真實搜尋服務。'],
    'youtube':['縮圖、影片標題、頻道、時間長度、分類與搜尋條件','搜尋與分類同步更新可見結果與數量；無結果時提供清除篩選，不假裝播放真實影片。'],
    'netflix':['內容標題、原創示意圖、簡介、分類與問答','片單可水平瀏覽、問答可展開與收合；操作只提供本機示範，不要求個資或執行註冊付款。'],
    'github':['檔案名稱、程式碼內容、作用中分頁與複製狀態','切換分頁更新實際程式碼；複製成功或失敗提供正確回饋，不執行未驗證的安裝指令。'],
    'microsoft':['產品名稱、分類、重點規格、示範價格與詳細資料','分類與搜尋同步更新可見產品及數量；詳細規格可展開，價格和購物功能均標示為範例。'],
}


def read(path): return json.loads(path.read_text())
def write(path, data): path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
def digest(data): return hashlib.sha256(data if isinstance(data, bytes) else data.encode()).hexdigest()


def main():
    recipes_path = ROOT / 'data/recipes.json'
    recipes = read(recipes_path)
    briefs = read(ROOT / 'data/new-studies/briefs-2026-11-01.json')['studies']
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
                      changes=['公開預覽依真實 Stitch 輸出調整，移除不實聯絡資料與可能誤導的安裝指令。',
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
