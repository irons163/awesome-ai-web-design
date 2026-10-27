# 可獨立使用的實作規格

這裡提供 74 組繁體中文實作方向，補足主要下載文件曾經缺少明確數值、依賴未附延伸文件及未提供品牌圖片的問題。它用來建立自己的前端介面，不是原官網原始碼或像素還原保證。

- `brand-directions.json`：逐品牌角色色碼、構圖類型及設計方向。
- `component-contracts.json`：逐品牌核心元件的必要欄位與行為。
- `specs.json`：產出的完整值、值的依據及素材清單。
- `scripts/implementation_specs.py`：讀取保存的來源樣式，產出主要 `DESIGN.md`、`PROMPTS.md` 及 4 份補充檔；不發起網路或 AI 生成請求。

來源色碼以檔案路徑、SHA-256 及 CSS 片段追溯。只要值出現在來源宣告，就會保留出處；色彩角色仍由本規格指定，不冒充瀏覽器量測結果。其他色碼、字型、尺寸、斷點與元件行為清楚標記為實作建議。舊版生成紀錄與比對統計保留於開發紀錄，不混入使用者的 AI 任務。

每份 `DESIGN.md` 自帶所有必要數值與 CSS。`TOKENS.json` 便於工具讀取，`starter.css` 與主要文件內 CSS 相同；`ASSETS.md`、`ASSETS.json` 說明素材未提供及缺少時的無圖做法。建議圖片路徑不代表檔案存在；無外部圖片、專有字型及後端時，仍能實作本機文字版原型。

重新產出與檢查：

```sh
python3 scripts/localize_zh_tw.py
python3 scripts/build.py
python3 -m unittest discover -s tests -v
node scripts/build_site.mjs --output public
node --test tests/test_catalog_workflows.mjs tests/test_media_proxy.mjs tests/test_pinterest_interactions.mjs tests/test_preview_routing.mjs
```

測試檢查 74 份必要值、來源雜湊、文字用語及 75 個 ZIP 的解壓內容；不代表 74 種介面都已由不同模型生成並驗收。2026-10-20 另以 Starbucks、Stripe、Linear 三類凍結下載包實作前端範例並操作測試，屬同一助理的整合驗證，並非獨立盲測。

目錄色票與明暗模式也由目前實作規格的角色色碼產出，避免沿用歷史分析的分類。所有下載 ZIP 均含 `LICENSE`、`ATTRIBUTION.md`，完整包有 448 個檔案，單品牌包有 10 個檔案。目錄操作測試涵蓋搜尋與複合篩選、收藏與跨分頁同步、儲存失敗、剪貼簿拒絕、錯誤連結、鍵盤操作，以及全部 74 組規格／指令的實際複製流程。
