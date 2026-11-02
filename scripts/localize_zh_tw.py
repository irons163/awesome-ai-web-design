#!/usr/bin/env python3
"""Regenerate Taiwan Chinese documents from reviewed copy and locked source evidence."""
import hashlib
import json
import re
from pathlib import Path
from publication import result_for, study_status
from rewrite_prompts import main as rewrite_prompts
from implementation_specs import build_profile, documents as implementation_documents, VERSION as IMPLEMENTATION_VERSION

ROOT = Path(__file__).resolve().parents[1]
LOCALE = ROOT / 'data/zh-TW'
WORK = ROOT / '.stitch-work/current-official'
UPDATED = IMPLEMENTATION_VERSION


def read(path):
    return json.loads(path.read_text())


def sha(value):
    return hashlib.sha256(value if isinstance(value, bytes) else value.encode()).hexdigest()


def normalize(text):
    substitutions = {
        '预覽': '預覽', '視頻': '影片', '用戶': '使用者', '數據': '資料',
        '默認': '預設', '加載': '載入', '鼠標': '滑鼠', '點擊': '按一下',
        '服務器': '伺服器', '組件': '元件', '鏈接': '連結', '登錄': '登入',
        '信息': '資訊', '屏幕': '畫面', '字體': '字型', '支持': '支援',
        'genuine Google Stitch MCP': '原生 Google Stitch MCP',
        'genuine GoogleStitch': '原生 Google Stitch', 'fullPNG': '完整 PNG 截圖',
        'rawHTML': '原始 HTML', 'full-page': '完整頁面',
        'Canada English explicitly selected through public country/language UI; /ca origin.': '透過公開國家與語言介面明確選擇加拿大英文版，來源位於 /ca。',
        'Official / redirected to /zh-tw while visible homepage content remained English.': '官網根目錄重新導向 /zh-tw，但實際可見首頁仍為英文。',
        'Brainstorm in Claude, build in Cowork': '在 Claude 發想，在 Cowork 實作',
        'global branding and UX design agency': '全球品牌與使用者體驗設計公司',
        'The Future of Finance is Intelligent': '金融的未來，由智慧驅動',
        'Tipalti Redesign Wins Design Awards and Features': 'Tipalti 改版獲得設計獎項與專題報導',
        'Complete Guide to Buttons in Web Design for': '網頁設計按鈕完整指南：',
        'Clay Global Shows Up Strong at The Webby Awards': 'Clay Global 在威比獎表現亮眼',
        'Give your AI secure access to': '讓你的 AI 安全存取',
        'Charles on the podium at Marina Bay': 'Charles 在濱海灣登上頒獎台',
        'Framer is the design agent for every step from idea to launch': 'Framer 是陪你從點子走到上線的設計代理',
        'Own your digital future, on your terms': '依你的方式，掌握數位未來',
        'complete system for AI and human customer service': '整合 AI 與真人客服的完整系統',
        'Own the power of your money': '掌握資金的力量',
        'The product development system for teams and agents': '為團隊與 AI 代理打造的產品開發系統',
        'Human collaboration at the speed of AI': '讓人類協作跟上 AI 的速度',
        'EVERY WORKLOAD. ANY CLOUD. ONE PLATFORM.': '各種工作負載，各種雲端，整合於單一平台。',
        'The open source AI coding agent': '開放原始碼的 AI 程式代理',
        'Show up everywhere. Without going anywhere.': '無須四處奔波，也能處處被看見。',
        'Building Real-World Intelligence': '打造真實世界的智慧',
        'Turn your website into a growth engine': '將網站化為成長引擎',
        'THE INTERNATIONAL ACCOUNT THAT SAVES YOU MONEY': '幫你省錢的國際帳戶',
        'Welcome to automation in the agentic era': '迎接 AI 代理時代的自動化',
        'Save4+hours each week with Superhuman Mail': '使用 Superhuman Mail，每週節省 4 小時以上',
        'Public anonymous English page.': '匿名可讀的英文公開頁面。',
        'Taichung City this weekend': '本週末的台中市',
        'Inspiration for future getaways': '下一趟旅程的靈感',
        'Think fast, built faster': '快速思考，更快完成',
        'The leading database for AI': '專為 AI 打造的領先資料庫',
        'Start free cloud trial': '開始免費雲端試用',
        'Your AI. Your rules.': '你的 AI，由你決定。',
        'Buy. Sell. Trade. Trust.': '買入、賣出、交易，值得信賴。',
        'Earn more on USDC': '透過 USDC 獲取更多收益',
        'Bringing technology to life': '讓科技融入生活',
        'Talk to our team': '聯絡我們的團隊',
        'Building blocks for agentic workflows': 'AI 代理工作流程的建構元件',
        'Infrastructure for your apps': '應用程式的基礎架構',
        'Build beautiful native apps': '打造美觀的原生應用程式',
        'The full-stack creative canvas': '全方位創作畫布',
        'chat overlays may differ.': '聊天覆蓋層可能不同。',
        'THE QUANTUM OF DRIVING': '駕馭的全新境界',
        'new species of product tool': '全新類型的產品工具',
        'Build review and ship': '建置、審閱與發布',
        'Meet the all-new Meta Glasses': '認識全新 Meta Glasses',
        'Meta Glasses by LISA': 'LISA 演繹 Meta Glasses',
        'The intelligent documentation platform': '智慧文件平台',
        'Flow from idea to outcome': '從點子順暢走向成果',
        'AI platform for teamwork': '團隊協作的 AI 平台',
        'Where teams and agents': '讓團隊與 AI 代理',
        'AI where your team works': '在團隊工作的地方使用 AI',
        'New Beginning for Windows PCs': 'Windows 電腦的新開始',
        'GTC Washington, D.C. Nov.': 'GTC 華盛頓特區，11 月',
        'Your product’s context layer': '產品的情境資訊層',
        'Give agents product context': '讓 AI 代理掌握產品情境',
        'How Runway is Used': 'Runway 使用方式',
        'Popular albums and singles': '熱門專輯與單曲',
        'AI Agent Engineering Platform': 'AI 代理工程平台',
        'Build for what’s next': '打造下一個可能',
        'Send more,pay even less': '匯得更多，費用更少',
        'Go from AI to ROI': '讓 AI 創造投資報酬',
    }
    for source, target in substitutions.items():
        text = text.replace(source, target)
    return text


def observation(text, override=None):
    if override:
        return normalize(override)
    lines = text.splitlines()
    if lines and lines[0].startswith('#'):
        lines.pop(0)
    kept = []
    for line in lines:
        if (re.match(r'^-\s+[A-Za-z]', line) or re.match(r'^#{1,4}\s*仍有差異', line)
                or re.match(r'^(?:accepted=false|驗收維持|沒有採購|沒有購買)', line)):
            break
        kept.append(line)
    result = normalize('\n'.join(kept).strip())
    if len(re.findall(r'[\u4e00-\u9fff]', result)) < 20:
        raise ValueError('Missing reviewed Chinese observation')
    return result


LANGUAGE = ('介面文案、按鈕、提示、錯誤訊息、圖片替代文字、設計規格與交付說明，'
            '一律使用繁體中文（台灣用語）。保留品牌名稱、字型名稱、檔名、網址、'
            'API 識別字與可執行程式碼。HTML 使用 zh-Hant-TW；數字與日期以 zh-TW 格式呈現，'
            '幣別及時區依原資料標示，不擅自換算。')

TYPE_HEADERS = {'Role': '用途', 'Font': '字型', 'Size': '字級', 'Weight': '字重',
                'Line Height': '行高', 'Letter Spacing': '字距', 'Notes': '備註'}
TYPE_ROLES = {'Hero Title': '主視覺標題', 'Display Hero': '主視覺大標題',
              'Section Heading': '區段標題', 'Section Title': '區段標題',
              'Sub-heading': '次標題', 'Feature Title': '功能標題',
              'Body': '內文', 'Body Text': '內文', 'Body Medium': '內文中字重',
              'Body Bold': '內文粗體', 'Button': '按鈕', 'Button Label': '按鈕文字',
              'Caption': '補充說明', 'Small': '小型文字', 'Micro': '微型文字',
              'Nav Item': '導覽項目', 'Product Name': '產品名稱', 'Promo Text': '活動文字',
              'Category Label': '分類標示', 'Badge': '狀態標籤', 'Sub-link': '次要連結'}


def typography_tables(blocks):
    result = []
    for block in blocks:
        rows = [[v.strip() for v in line.strip('|').split('|')] for line in block.splitlines()]
        headings = rows[0]
        indexes = [i for i, h in enumerate(headings) if h in TYPE_HEADERS and h != 'Notes']
        if not indexes:
            continue
        result += ['| ' + ' | '.join(TYPE_HEADERS[headings[i]] for i in indexes) + ' |',
                   '| ' + ' | '.join('---' for _ in indexes) + ' |']
        for row in rows[2:]:
            cells = []
            for i in indexes:
                value = row[i] if i < len(row) else '—'
                if headings[i] == 'Role':
                    value = TYPE_ROLES.get(value, '`' + re.sub(r'\s+', '-', value.lower()) + '`')
                value = value.replace('(est.)', '（估計）').replace('(tight)', '（緊密）').replace('(normal)', '（一般）')
                cells.append(value)
            result.append('| ' + ' | '.join(cells) + ' |')
        result.append('')
    return '\n'.join(result)


def extended_design(entry, source, current, observed, limits):
    name = entry['name']
    header = ('---\nversion: zh-TW-2026-10-15\nlanguage: zh-TW\nname: '
              + json.dumps(name, ensure_ascii=False) + '\ndescription: '
              + json.dumps(entry['description'], ensure_ascii=False) + '\n\n' + source['tokens'] + '\n---\n')
    values = '\n'.join('- `' + value + '`' for value in source['inline_values'])
    table = typography_tables(source['type_tables'])
    return header + normalize(f'''
# {name} 延伸設計規格

語言：繁體中文（台灣用語，zh-TW）。在地化更新：{UPDATED}。

## 來源與規格層次

這份規格將較早保存的品牌設計資料重新整理為可實作的繁體中文文件。來源設定中的色碼、字級、字重、行高、間距、圓角與元件識別字保留，供開發工具讀取；敘述與操作指令改用台灣用語。這些延伸設定不等同於目前日期限定首頁的逐項實測值，若兩者不同，依下方的日期限定觀察及對應預覽判讀。

- 原始資料版本：`{source['source_git_ref']}`。
- 原始 DESIGN.md 摘要：`{source['source_sha256']}`。
- 目前首頁參考日期：{current['date']}。
- 目前公開來源：{current['reference_url']}。
- 目前預覽：`official-drafts/{current['file']}.html`。
- 台灣繁體中文規格與指令是本次重新產出的內容；來源截圖及原生生成紀錄保留原貌。

## 整體視覺方向

{entry['description']}

{entry['brief']}

先建立主要內容、輔助資訊與操作之間的層級，再套用色彩及裝飾。品牌色應有明確用途；主要操作、選取、錯誤及停用狀態要能分辨。避免將多套參考風格混在同一頁，也不要僅替換通用卡片的顏色。

## 色彩、字型與繁體中文排版

上方來源設定保留原始色彩角色與數值。主要品牌色用於最重要的操作；背景、內容表面、主要文字、次要文字與分隔線各自維持一致用途。資訊不能只依賴顏色，狀態須同時有文字或圖示標示。

原字型名稱可作為拉丁字母參考。繁體中文字型優先使用可取得的 `Noto Sans TC`、`PingFang TC`、`Microsoft JhengHei`，最後才使用 `sans-serif`。原字型未涵蓋中文時必須提供替代，不以缺字或圖片文字呈現正文。專有字型無法取得時，記錄替代字型與可能的字寬差異。

中文標題以語意分段，避免為模仿英文大寫字距而拉散中文字。內文行高、欄寬與段落間距以可讀性為準；英文型號、網址、程式碼及長連結可以換行或在自己的區域捲動，不可撐開整份文件。價格、規格及比較欄位保持數字與單位對齊。

{table}
## 版面與元件結構

此參考可先實作：{entry['component']}。

先辨識導覽、主要內容、次要內容與頁尾，再依來源設定安排容器寬度、格線、間距及圓角。相同層級使用同一組設計變數；元件內距與區段留白分開管理。表單標示放在欄位旁，補充說明及驗證訊息與對應欄位保持連結。

桌面多欄在窄版依內容順序堆疊；保留必要的篩選與主要操作，不將無法容納的文字裁切掉。資料表、程式碼或水平內容列可在自己的容器內捲動，使用者仍應能辨識後續內容。不同尺寸採同一份有意義的閱讀順序。

## 操作與狀態

| 狀態 | 實作要求 |
| --- | --- |
| 預設 | 顯示操作名稱、目前內容與必要說明。 |
| 滑鼠移入與焦點 | 重點清楚且不只靠色彩；鍵盤焦點可見。 |
| 已選取 | 同時呈現視覺狀態與 aria-selected 或 aria-pressed。 |
| 停用 | 說明無法操作的原因，避免只有降低透明度。 |
| 載入 | 呈現文字進度或等待狀態，避免重複送出。 |
| 空白與錯誤 | 清楚說明原因，提供可行的修正或重試方式。 |

所有可見按鈕都應產生可理解的結果。範例資料要明確標示，不能讓讀者誤以為連上真實帳戶、付款、訂單或模型後端。需要外部服務的操作應提供對應目的地或說明，不偽造成功結果。

## 圖片、動態與無障礙

圖片保留長寬比例與主要構圖，補上有用途的替代文字；純裝飾圖不重複朗讀。影片提供可理解的海報及播放狀態，資訊不能只在動態畫面中出現。尊重減少動態效果設定，避免閃爍與阻礙閱讀的自動移動。

導覽、表單、分頁、對話框與展開控制須支援鍵盤。互動元素使用語意標記，觸控區域建議至少 44px；焦點不可被固定頁首遮住。驗證長中文標題、混合中英文、空內容及載入失敗，並在 390px、768px、1440px 檢查排版。這些是新專案的實作建議，不是原官網通過無障礙檢測的宣稱。

## 來源中的技術值補充

以下保留原始資料中的 CSS 值與數值片段。程式碼屬性及識別字維持原文；實際角色應與上方來源設定及對應元件一起閱讀，不單獨套用沒有語境的數值。

{values or '額外數值以開頭的來源設定為準。'}

## 日期限定首頁觀察

{observed}

## 已知差異與驗證範圍

{chr(10).join('- ' + v for v in limits)}

以上限制沿用原參考日期的比對紀錄。本次繁體中文整理不會把未驗證的影片、動畫、服務或尺寸改標為已通過；目前預覽仍未宣稱與官方完全一致。
''')


def review_document(entry, current, limits):
    name, date, url = entry['name'], current['date'], current['reference_url']
    limit_text = '\n'.join('- ' + value for value in limits)
    review = f'''# {name} 畫面比對紀錄

語言：繁體中文（台灣用語，zh-TW）。整理日期：{UPDATED}。原始參考日期：{date}。

公開來源：{url}

預覽：`official-drafts/{current['file']}.html`

預覽 SHA-256：`{current['preview_sha256']}`

## 比對範圍

這份紀錄將原日期已知差異重新整理為繁體中文，沒有變更原始圖片、影片、預覽或拍攝證據，也沒有新增原先未執行的驗證。比對狀態仍為「已比對主要畫面，仍有差異」，不是完整官方一致驗收。

## 已知差異

{limit_text}

## 判讀方式

原始紀錄提及的未部署、未測服務或未測裝置，指當時的官網畫面比較範圍；不應直接視為目前網站連線狀態。文字在地化與正式網站可用性可另行檢查，但不會擴大原始視覺驗收結論。品牌名稱、素材、技術識別字與來源網址保留供溯源。
'''
    return normalize(review)


def attribution(locks):
    rows = '\n'.join(
        f'| {row["name"]} | {row["date"]} | [公開來源]({row["reference_url"]}) · '
        f'[比對紀錄](official-progress.html#{slug}) |'
        for slug, row in sorted(locks.items()))
    return f'''# 授權與資料來源

Awesome AI Web Design 由 [PhilForge](https://philforge.com/) 製作與維護，免費提供繁體中文設計參考、AI 實作指令、可操作預覽與下載工具。

## 本專案製作的內容

目錄介面、中文摘要、重新撰寫的 AI 指令、通用工作流程、實作規格、預覽整合、建置程式、說明及測試，由 Awesome AI Web Design 貢獻者製作，採 [MIT 授權](LICENSE)。

{len(locks)} 份延伸設計規格、{len(locks) * 3} 則任務指令、日期限定的主要規格與指令、介面文案及已知差異，於 {UPDATED} 重新產出為繁體中文（台灣用語）。主要規格會標示實作依據；每個品牌的觀察日期與比較範圍以[參考來源](https://webdesign.zero2codex.dev/reference-sources.html)及[全部參考紀錄](official-progress.html)為準。

## 預覽與原始生成紀錄

Google Stitch 預覽來自實際 MCP 或網頁版生成；各 `STITCH.json` 記錄可取得的專案與畫面識別字及檔案雜湊。網頁版新增的設計經人工調整並重新截圖，修改範圍及原始匯出的摘要記錄於個別生成紀錄。`STITCH-PROMPT.md` 保留當時送出的指令；重新撰寫的 `STITCH-PROMPT.zh-TW.md` 是中文生成參考，沒有宣稱已再次送交生成服務。

既有網站主要預覽依保存的公開官網資料、DOM、樣式、字型、圖片與影片校正，與原生生成稿分開保存。新增設計採明確標示的生成示範，不把生成服務的精確度宣稱當成視覺驗證。

原始完整改寫歷程可由版本 `1a783491c9539c3153c2fc96c16d59131e024f4e` 的來源紀錄溯源；目前每頁的日期、預覽摘要與限制則以 [全部參考紀錄](official-progress.html) 為準。曾出現的生成錯誤、下載失敗、行動版請求回傳桌面稿、影片與動畫差異，仍保留在來源紀錄，不因中文整理而改標為驗收通過。

## 品牌與第三方素材

品牌名稱、商標、字型、圖片及影片屬各自權利人。這些參考素材不因本專案的程式與文字採 MIT 授權，就一併成為 MIT 授權素材。個別素材保留來源網址、檔案大小及 SHA-256；資料包中的 Markdown 用於說明設計，不包含完整官網媒體或品牌服務。

Google、YouTube、Netflix、GitHub、Microsoft、Wikipedia、Amazon、Discord、Duolingo、IKEA、Adobe、BBC、Twitch、Zoom、Booking.com、Canva、LinkedIn、PayPal、Etsy 與 Khan Academy 的參考預覽含各網站公開頁面的圖片或標誌，用來對照該次觀察的版面。這些素材及商標屬於各自權利人，不適用本專案的 MIT 授權；來源與雜湊記錄於原始碼 `data/new-studies/media/reference-2026-11-01/`。簡易包與實作包不包含這些圖片。

部分預覽使用固定版本 hls.js 1.7.3 精簡播放器，採 Apache-2.0 授權；套件授權及完整性紀錄隨原始資源保留。原始網站連結、外部服務及受原權利人管理的內容，維持各自目的地。

## 歷史匯入資料與授權

早期匯入的設計分析仍有部分來源設定與技術值沿用於延伸規格，相關來源與授權集中記錄於此。

- 資料來源：[VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md)。
- 匯入版本：`f6961238d5cddcf8042a74a70fc400ec67181abb`；匯入日期：2026-09-22。
- 原始著作權：Copyright (c) 2026 VoltAgent；MIT 著作權與授權條文保留於 [LICENSE](LICENSE)。
- 原始檔案路徑與 SHA-256 記錄於原始碼的 `data/upstream.json`。

## {len(locks)} 份日期限定研究的來源

以下日期是既有公開首頁觀察日期，不是本次中文整理時重新檢查官網的日期。每頁限制說明以繁體中文提供；實際比較只涵蓋原紀錄的尺寸與狀態，未宣稱完整互動、所有裝置或品牌後端服務一致。

| 品牌 | 參考日期 | 來源與範圍 |
| --- | --- | --- |
{rows}
'''


def main():
    recipes = read(ROOT / 'data/recipes.json')
    styles, locks = read(LOCALE / 'design-sources.json'), read(LOCALE / 'source-lock.json')
    translated_limits, overrides = read(LOCALE / 'limit-copy.json'), read(LOCALE / 'analysis-copy.json')
    progress = read(WORK / 'progress.json')
    directions = read(ROOT / 'data/implementation/brand-directions.json')
    assert set(directions) == {entry['slug'] for entry in recipes}, 'Incomplete implementation directions'
    output = {}
    implementation_profiles = {}
    for entry in recipes:
        for key in ('description', 'brief', 'component'):
            entry[key] = normalize(entry[key])
        slug = entry['slug']
        lock = locks[slug]
        assert sha((WORK / (lock['file'] + '.html')).read_bytes()) == lock['preview_sha256'], slug
        for source in lock['source_documents'].values():
            assert sha((WORK / Path(source['path']).name).read_bytes()) == source['sha256'], source['path']
        _, record = result_for(WORK, lock['file'], lock['preview_sha256'])
        status = study_status(WORK, lock['file'], entry, progress[slug], record,
                              lock['preview_sha256'], [Path(p).name for p in lock['study'].values()])
        remaining = status['remaining_differences']
        assert sha(json.dumps(remaining, ensure_ascii=False, separators=(',', ':'))) == lock['remaining_sha256'], slug
        limits = [normalize(translated_limits.get(slug, {}).get(str(i), v)) for i, v in enumerate(remaining)]
        if not all(re.search(r'[\u4e00-\u9fff]', v) for v in limits):
            raise ValueError('Untranslated limitation: ' + slug)
        original = (WORK / Path(lock['study']['analysis']).name).read_text()
        observed = observation(original, overrides.get(slug))
        (ROOT / 'design-md' / slug / 'DESIGN.md').write_text(extended_design(entry, styles[slug], lock, observed, limits))
        historical_review = review_document(entry, lock, limits)
        profile = build_profile(ROOT, entry, lock, directions[slug])
        documents, implementation = implementation_documents(entry=entry, lock=lock, profile=profile, review=historical_review)
        implementation_profiles[slug] = dict(profile=implementation['profile'], assets=implementation['assets'])
        output[slug] = dict(source_preview_sha256=lock['preview_sha256'], source_documents=lock['source_documents'],
                            remaining_source_sha256=lock['remaining_sha256'], remaining_differences=limits,
                            documents={kind: documents[kind] for kind in lock['study']},
                            implementation_files={name:dict(path=f'implementation/{slug}/{name}',text=text)
                                                  for name,text in implementation['files'].items()})
    assert len(output) == len(recipes) and set(output) == {entry['slug'] for entry in recipes}
    (ROOT / 'data/recipes.json').write_text(json.dumps(recipes, ensure_ascii=False, indent=2) + '\n')
    (LOCALE / 'studies.json').write_text(json.dumps(dict(locale='zh-TW', updated=UPDATED, studies=output), ensure_ascii=False, indent=2) + '\n')
    (ROOT / 'data/implementation/specs.json').write_text(json.dumps(dict(version=IMPLEMENTATION_VERSION, profiles=implementation_profiles), ensure_ascii=False, indent=2) + '\n')
    (ROOT / 'ATTRIBUTION.md').write_text(attribution(locks))
    rewrite_prompts()
    print(f'Regenerated {len(output)} Chinese design documents and current study document sets.')


if __name__ == '__main__':
    main()
