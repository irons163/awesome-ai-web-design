# 台灣繁體中文內容

全站說明、設計規格、AI 指令與下載檔案使用繁體中文（台灣用語）。品牌名稱、字型名稱、網址、檔名、API 識別字與程式碼保留原文；官網完整預覽、原始截圖與生成證據保留來源原貌。

- `data/recipes.json`：74 個品牌的中文摘要、頁面需求與元件需求。
- `design-sources.json`：較早設計資料中的原始技術值與來源摘要，不把延伸設定冒充當日量測。
- `source-lock.json`：目前 74 份預覽、原始分析、指令、比對紀錄與限制清單的來源雜湊。
- `analysis-copy.json`：需要人工重新整理的品牌觀察。
- `limit-copy.json`：依品牌與原始序號逐項改寫的差異說明。
- `studies.json`：重新產出的主要規格、AI 指令及比對紀錄，供 Python 與 Node.js 發布流程使用。

用語採「專案、元件、資料、建立、預設、載入、登入、連結、儲存、影片、伺服器、滑鼠、字型」。不改寫程式識別字，也不換算原始幣別或回填觀察日期。

修改文案後依序執行：

```sh
python3 scripts/localize_zh_tw.py
python3 scripts/build.py
node scripts/build_site.mjs --output public
```

產出程式會驗證原始預覽與文字雜湊。若來源更新，須重新檢查譯文並更新來源鎖定；不可略過驗證或把舊譯文配上新畫面。發布只替換說明文件及公開的限制文字，原始官網 HTML 與媒體保持相同位元組。

原始碼 `design-md/` 的 `DESIGN.md` 與 `PROMPTS.md` 保留延伸設計分析與三類任務指令。網站主要規格及指令由 `scripts/implementation_specs.py` 配合 `data/implementation/` 重新產出，寫入 `studies.json`。每份主要規格含完整角色色碼、字級、間距、元件行為、斷點、素材替代及可直接使用的 CSS；不依賴延伸規格。

`studies.json` 另含同版本的 `TOKENS.json`、`starter.css`、`ASSETS.md`、`ASSETS.json`。主要分頁、單份下載、單品牌 ZIP 及全部 ZIP 的檔案內容必須一致。色彩來源只宣稱在保存的來源樣式中出現；其角色、其他推薦值與響應式條件明確標為實作建議，不回填成官網實測。`STITCH-PROMPT.zh-TW.md` 為重新撰寫的中文生成參考，不宣稱已再次送交生成服務。
