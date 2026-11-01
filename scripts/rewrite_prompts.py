#!/usr/bin/env python3
"""Rebuild locally authored AI instructions; never downloads upstream content."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKER = '\n<!-- Original AI instructions: awesome-ai-web-design -->'


def make_prompts(entry):
    name = entry['name']
    start = f'先閱讀隨附的 DESIGN.md，以 {name} 的設計語言作為介面參考。'
    guard = ('使用我的產品名稱、內容與資料格式，優先沿用專案現有元件及技術。'
             '開始製作樣式前，先將色彩、字體、間距與圓角整理為可重複使用的設計變數。'
             '指定字型無法取得時，使用可用的系統字型或開源字型，並說明替代方式。'
             '介面文案、按鈕、提示、錯誤訊息、圖片替代文字、註解與交付說明，一律使用繁體中文（台灣用語）。'
             '使用「專案、元件、資料、建立、預設、載入、登入、連結、儲存、影片」等台灣用語。'
             '保留品牌名稱、檔名、網址、API 識別字與可執行程式碼；HTML 語言設為 zh-Hant-TW。')
    quality = ('讓互動元件可實際操作，並將狀態提供給輔助科技。'
               '具備可見的鍵盤焦點、清楚的欄位標示、減少動態效果，以及至少 44px 的觸控區域。'
               '參考視覺與可用性衝突時，作最小幅度的無障礙調整並記錄原因。'
               '在 390px、768px、1440px 寬度檢查版面，涵蓋繁體中文長標題、長內容、空白及錯誤狀態。'
               '金額、數量與日期依資料本身的幣別、單位及時區呈現，以 zh-TW 格式顯示，不擅自換算。'
               '最後交付完成的檔案、實際驗證結果與仍待確認的假設，不把未檢查項目宣稱為通過。')
    return [
        {'id':'build','title':'建立新頁面','text':start + '請完成以下可操作頁面：' + entry['brief'] + '\n\n' + guard + '\n\n' + quality},
        {'id':'component','title':'製作元件','text':start + '請製作' + entry['component'] + '。'
         + '沿用現有元件慣例，放入精簡且符合實際情境的範例。'
         + '比例與資訊層級應來自參考規格，不能只替通用卡片換色。'
         + '依需求支援預設、焦點、停用、載入與錯誤狀態。'
         + '使用有意義的示範資料，讓每個可見操作都有明確結果。\n\n' + guard + '\n\n' + quality},
        {'id':'restyle','title':'改造既有介面','text':start + '重新設計選定頁面，同時保留路由、資料、行為與使用者可理解的意義。'
         + '先確認頁面層級，再找出最少且可重複使用的設計變數與元件調整。'
         + '以下構圖作為視覺方向，依現有頁面調整：'
         + entry['brief'] + '\n\n' + guard
         + '依完整元件群組套用變更，檢查其他頁面是否受影響，並說明調整前後的主要差異。\n\n' + quality}
    ]


def remove_upstream_instructions(text):
    text = text.split(MARKER)[0]
    # Remove whole prompt and iteration sections at their own heading depth.
    lines = text.splitlines(keepends=True)
    kept, skip_level = [], None
    for line in lines:
        heading = re.match(r'^(#{1,6})\s+(.+)', line)
        if heading:
            level, title = len(heading[1]), heading[2]
            if skip_level is not None and level <= skip_level:
                skip_level = None
            if skip_level is None and re.search(r'Agent Prompt Guide|Example (?:Component )?Prompts|Iteration Guide', title, re.I):
                skip_level = level
        if skip_level is None:
            kept.append(line)
    return ''.join(kept).rstrip()


def main():
    for entry in json.loads((ROOT/'data/recipes.json').read_text()):
        folder = ROOT/'design-md'/entry['slug']
        provenance = json.loads((folder/'STITCH.json').read_text())
        web_export = provenance.get('transport') == 'web'
        prompts = make_prompts(entry)
        prompt_doc = f"# {entry['name']} — AI 實作指令\n\n"
        prompt_doc += '語言：繁體中文（台灣用語，zh-TW）。將 DESIGN.md 放入專案，再選擇下方任務。這些指令由本專案重新撰寫；請把示範內容替換為自己的產品需求。\n\n'
        for prompt in prompts:
            prompt_doc += f"## {prompt['title']}\n\n```text\n{prompt['text']}\n```\n\n"
        prompt_doc += ('## 逐次調整流程\n\n'
                       '1. 先指出一個可實際觀察的問題，例如層級不清或內容遭裁切。\n'
                       '2. 在 DESIGN.md 找到對應設計變數或元件規則，提出範圍明確的調整。\n'
                       '3. 套用調整，保留無關的路由與資料行為。\n'
                       '4. 檢查鍵盤焦點、窄版排版，以及代表性的內容與錯誤狀態。\n'
                       '5. 用繁體中文說明結果，以及刻意偏離參考外觀的原因。\n')
        (folder/'PROMPTS.md').write_text(prompt_doc)
        (folder/'STITCH-PROMPT.zh-TW.md').write_text(
            f"# {entry['name']} 生成參考指令\n\n"
            '語言：繁體中文（台灣用語，zh-TW）。這是重新撰寫的生成指令，並非早期實際送出的原始請求。'
            + ('網頁版 Stitch 的實際生成指令保存在 STITCH-PROMPT.md；公開預覽經人工調整。\n\n' if web_export else '來源 HTML、截圖及 STITCH.json 維持原始紀錄；不宣稱已重新呼叫生成服務或產生新截圖。\n\n')
            + '```text\n' + prompts[0]['text'] + '\n\n'
            '產出可操作且具響應式版面的完整頁面。所有新文案使用台灣繁體中文，保留必要品牌與技術識別字。'
            '保留原始輸出及生成紀錄，另存後續調整，不以生成服務的自我宣稱代替實際瀏覽器檢查。\n```\n')
        base = remove_upstream_instructions((folder/'DESIGN.md').read_text())
        notice = '\n\n## 來源與使用範圍\n\n資料來源與適用授權集中於專案根目錄的 ATTRIBUTION.md 與 LICENSE。品牌名稱僅用於識別參考來源，並非官方授權或服務。下方 AI 指令由本專案獨立撰寫；若既有互動備註與無障礙要求衝突，以此處的可用性檢查為準。\n'
        # Idempotent regeneration: the provenance notice belongs to the generated section.
        (folder/'DESIGN.md').write_text(base + MARKER + notice + '\n' + prompt_doc.replace('# '+entry['name']+' — AI 實作指令', '## 重新撰寫的 AI 任務指令', 1))
        preview_label = '調整後的 Stitch 設計預覽' if web_export else '原始 Google Stitch 預覽'
        record_label = '生成紀錄' if web_export else '原始生成紀錄'
        preview_scope = 'Google Stitch 網頁版生成的畫面經人工修改並重新截圖；原始輸出雜湊與修改說明見生成紀錄，這不是品牌官方網站' if web_export else 'Google Stitch 原生 HTML、截圖及生成紀錄保留來源原貌，不是品牌官方網站'
        (folder/'README.md').write_text(f"# {entry['name']}\n\n{entry['description']}\n\n設計規格與 AI 指令已重新產出為繁體中文（台灣用語），可免費使用，無須登入。\n\n- [延伸設計規格](DESIGN.md)\n- [三則 AI 實作指令](PROMPTS.md)\n- [繁體中文生成指令](STITCH-PROMPT.zh-TW.md)\n- [{preview_label}](preview.html)\n- [{record_label}](STITCH.json)\n- [回到總目錄](../../README.md)\n\n規格與 AI 指令由本專案以台灣繁體中文重新整理，資料來源與適用授權見[授權與資料來源](../../ATTRIBUTION.md)及 [LICENSE](../../LICENSE)。{preview_scope}；目前日期限定的參考分析請由網站設計詳情閱讀。\n")
    count = len(json.loads((ROOT/'data/recipes.json').read_text()))
    print(f'Wrote {count * 3} original task prompts across {count} design systems.')

if __name__ == '__main__':
    main()
