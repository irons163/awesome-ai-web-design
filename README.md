# Awesome AI Web Design

**74 套設計參考、222 則重新撰寫的 AI 指令，全部免費。**

[開啟免費設計集](https://webdesign.zero2codex.dev) · [GitHub 原始碼](https://github.com/irons163/awesome-ai-web-design)

在網站下載喜歡的設計實作包，把 `DESIGN.md` 與 `PROMPTS.md` 交給 AI，再填入自己的內容與功能需求。74 份主要規格已補齊色碼、字級、間距、響應式條件、元件行為及無圖做法，並區分來源宣告與實作建議。全部使用繁體中文（台灣用語），沒有帳號、訂閱、付費下載或廣告。

這是以 [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) 為基礎的獨立免費版本，不是原作者的官方網站。保留原始 MIT 授權與來源，詳見 [ATTRIBUTION.md](ATTRIBUTION.md)。

## 立即使用

1. 在[網站](https://webdesign.zero2codex.dev/)選一套設計，於「AI 指令」分頁下載「此設計實作包」。
2. 解壓後將主要 `DESIGN.md` 與 `PROMPTS.md` 放進專案，填入自己的產品名稱、內容、功能與資料。也可採用同版本 `starter.css` 與 `TOKENS.json`。
3. 把需求與指令交給能讀取專案檔案的 AI 開發工具；缺少圖片時採用規格內的文字版做法，依 `ASSETS.md` 補充自己的素材。
4. 實際檢查手機版、鍵盤操作及每項主要功能，再依結果修正。規格可用於前端原型，登入、付款及資料庫等服務仍須依需求實作與驗收。

每品牌包有 10 個檔案：上述 6 份文件及數值檔，加上 `README.md`、`SOURCES.json`、`LICENSE`、`ATTRIBUTION.md`。主要 `DESIGN.md` 本身已含必要數值及 CSS，不依賴缺少的延伸檔案，也不保證生成結果與原官網相同。原始碼下方目錄的 `design-md/` 保留歷史延伸分析；目前網站及下載包的主要規格由 `data/implementation/` 與 `data/zh-TW/` 產出。

例如：

```text
先讀取專案根目錄的 DESIGN.md，將它作為這次介面的視覺規格。
我要做一個可以搜尋、篩選與收藏文章的閱讀清單。
沿用目前技術架構，先建立共用的色彩與字級設計變數，再實作完整的操作流程。
使用我的產品名稱和內容；檢查手機版、鍵盤操作與空清單狀態。
完成後列出變更檔案、驗證結果，以及需要我補充的內容。
```

其他工作流程：[從網站建立設計分析](prompts/analyze-website.md) · [依參考實作](prompts/build-interface.md) · [視覺檢查與修正](prompts/review-interface.md)

## 本機展示網站

只需要 Python 3.9 以上，不需安裝套件：

```sh
python3 scripts/serve.py
```

若連接埠已被使用，可改成 `python3 scripts/serve.py --port 4178`。

從完整原始碼 ZIP 解壓後可直接啟動伺服器。網站的「下載全部」是設計實作資料包，共 448 個檔案：74 組規格、AI 指令、數值、CSS、素材說明與清單，加上總說明、來源清單、授權與致謝；不含完整預覽網站或品牌素材。開發用途的完整原始碼包另由 `python3 scripts/build.py` 在本機重建為 `assets/all-designs.zip`，ZIP 不會將自己遞迴封裝在內。

開啟 **http://127.0.0.1:4173**。可搜尋品牌或關鍵字、依領域和明暗模式篩選、收藏設計、比較 Stitch 生成頁面、閱讀全文、複製指令，以及下載單一檔案或全部 ZIP。收藏只儲存在目前瀏覽器。

網站預覽由 Google Stitch MCP 依各份設計分析與專屬情境實際生成，保留原始 HTML 與截圖，不是品牌原站截圖。每份範例附有生成指令、Stitch project/screen ID 與檔案 SHA-256。HTML 是靜態介面範例，可能使用 Google Fonts、Tailwind CDN 或 Stitch 匯出的外部圖片，部分操作與資料僅供展示。直接開 `index.html` 時瀏覽器可能阻擋讀取資料；請使用上述本機伺服器。

品牌詳情頁預設提供官網重製草稿入口與參考日期；沒有可用草稿時會顯示進度。原始 Stitch 截圖和 HTML 可切換查看。各品牌已知差異依參考紀錄判讀，預覽入口的切換不代表已與現行官網一致。

## 開發與驗證

```sh
python3 scripts/localize_zh_tw.py
python3 scripts/build.py
python3 -m unittest discover -s tests -v
```

原始收藏仍可用 `python3 scripts/serve.py` 預覽。目前正式網站使用 VPS 靜態託管，詳見原始碼中的 `deploy/vps/README.md`。原 Sites 託管版本保留 Vinext Worker 建置方式，需 Node.js 22.13 以上及 pnpm 11.25；`pnpm run build` 會保留靜態頁面並加入同源素材路由，`pnpm run dev` 可預覽相同的伺服器行為。

預覽入口的非同步載入、品牌連結及原始範例切換另有 DOM 測試。這套測試使用 jsdom，不是瀏覽器畫面驗收；執行前需安裝開發套件並建置網站：

```bash
pnpm install --frozen-lockfile
pnpm run build
pnpm run test:preview
pnpm run test:catalog
pnpm run test:pinterest
pnpm run test:media
```

- `design-md/<slug>/DESIGN.md`：完整設計分析，加上全新 AI 指令。
- `design-md/<slug>/PROMPTS.md`：三種任務指令與迭代流程。
- `design-md/<slug>/preview.html`：Stitch 匯出的原始 HTML。
- `design-md/<slug>/preview.png`：Stitch 原始生成截圖。
- `design-md/<slug>/STITCH-PROMPT.md` / `STITCH.json`：生成指令與可追溯的來源紀錄。
- `data/recipes.json`：本專案撰寫的品牌情境與元件需求。
- `data/implementation/`：74 組實作方向、元件欄位與行為、完整規格數值及來源依據；詳見該目錄的 `README.md`。
- `data/zh-TW/studies.json`：網站主要規格、AI 指令及同版本實作包內容。
- `data/upstream.json`：匯入版本、每份原始文件的 SHA-256。
- `assets/catalog.json`：由設計檔案與情境資料產生的網站目錄。
- `assets/all-designs.zip`：建置產出的完整下載包，包含設計、AI 指令、HTML、原始截圖、網站原始碼與授權；不提交二進位 ZIP，發布到 GitHub Releases。

修改在地化內容後先執行 `localize_zh_tw.py`；再執行 `build.py` 更新目錄和下載包。`build.py` 只驗證並封裝既有 Stitch 匯出，不會產生、重繪或覆蓋預覽，也不會發起 AI 請求。要更新範例，需在 Stitch 重新生成並透過 `scripts/import_stitch.py` 匯入 MCP 結果。金鑰只供生成工具使用，不會放入網站或下載包。一般檢查流程由 `.github/workflows/check.yml` 提供。

## 網站發布

目前正式網站為 [webdesign.zero2codex.dev](https://webdesign.zero2codex.dev/)，由自有 VPS 與 Caddy 提供 HTTPS；原始預覽素材已還原為同源靜態檔案。以下保留原 Sites 託管的建置方式：Vinext Worker 搭配靜態頁面。執行 `python3 scripts/build.py` 更新資料與下載包，再執行 `pnpm run build`；輸出為 `dist/client/` 與 `dist/server/`。`python3 scripts/build_site.py` 或 `pnpm run build:static` 可單獨檢查靜態檔案整理結果，但移除的大型素材需由 Worker 路由提供。完整 ZIP 需由同一份來源 commit 建置，並以 `all-designs.zip` 檔名上傳至 GitHub Releases；主要下載入口使用本次建置的 assets/design-references.zip，與網站顯示的繁體中文內容一致；大型原始碼包不納入正式靜態部署。首頁截圖與縮圖沿用本地相對網址，Worker 依 `data/hosting-assets.json` 的清單串流取得 GitHub 固定 commit 的原檔。更新 Stitch 圖片時，先推送完整匯出，再更新清單的 commit、位元組數及 SHA-256。下載包與原始收藏的本機預覽仍使用完整本機圖片。

網站另提供逐步製作的官網重製草稿，並在 [74 站進度頁](https://webdesign.zero2codex.dev/official-progress.html) 註明各品牌狀態與參考日期。Google Stitch 的原始生成稿另行保存；公開草稿再依保存的官方頁面資料與素材重製。目前 74 份研究已記錄主要畫面比對與差異，完整互動、所有尺寸及品牌服務仍未全面驗收，不能宣稱與品牌現行官網完全一致。`build_site.py` 僅將草稿 HTML 與實際引用的素材放入 `dist/official-drafts/`；這些品牌素材仍屬原權利人，亦不包含在下載 ZIP 中。

## 免費與來源

原 Sites 託管版本的大型官網圖片、影片與字型由同源 Worker 路由提供，以符合部署大小限制。路由只接受 `data/hosted-official-media.json` 清單內、已驗證的 GitHub 固定 commit 原檔，並支援影片分段讀取；不轉送訪客認證或 Cookie。原始草稿 HTML、CSS、JavaScript 與素材完整保留，發布時不替換其中的相對網址。`assets/official-media-publication.json` 記錄來源與發布檔案雜湊，兩者必須完全相同，包含內嵌 SVG。使用 `pnpm run dev` 預覽完整同源載入行為。

本專案的所有內容均直接開放下載，沒有付費牆、私有訂製入口或支付整合。MIT 授權仍允許使用者將內容用於商業專案；「免費提供」不等於限制下游商用。

色彩和字型資料是匯入版本的分析紀錄，尚未逐一重新查核所有品牌當前網站。品牌名稱、商標與專有字型屬於各自權利人，下載包不包含品牌商標或專有字型檔案。無障礙要求優先於匯入分析中過小的觸控目標或缺少焦點狀態的建議。

## 設計目錄

<!-- COLLECTION:START -->

### AI 與模型

| 設計 | 特色 | 檔案 |
| --- | --- | --- |
| [Claude](design-md/claude/README.md) | 奶油色、陶土色與襯線標題的溫暖節奏。 | [設計規格](design-md/claude/DESIGN.md) · [AI 指令](design-md/claude/PROMPTS.md) |
| [Cohere](design-md/cohere/README.md) | 中性閱讀面搭配低彩度產品色塊。 | [設計規格](design-md/cohere/DESIGN.md) · [AI 指令](design-md/cohere/PROMPTS.md) |
| [ElevenLabs](design-md/elevenlabs/README.md) | 乾淨石色、聲音波形與細膩的文字層次。 | [設計規格](design-md/elevenlabs/DESIGN.md) · [AI 指令](design-md/elevenlabs/PROMPTS.md) |
| [MiniMax](design-md/minimax/README.md) | 多產品色彩配合輕量網格，保持技術可讀性。 | [設計規格](design-md/minimax/DESIGN.md) · [AI 指令](design-md/minimax/PROMPTS.md) |
| [Mistral AI](design-md/mistral.ai/README.md) | 暖黃與橙色像素節奏，帶出開放技術感。 | [設計規格](design-md/mistral.ai/DESIGN.md) · [AI 指令](design-md/mistral.ai/PROMPTS.md) |
| [Ollama](design-md/ollama/README.md) | 單色、終端機範例與直白的內容結構。 | [設計規格](design-md/ollama/DESIGN.md) · [AI 指令](design-md/ollama/PROMPTS.md) |
| [OpenCode](design-md/opencode.ai/README.md) | 暖灰紙面搭配深色終端機，保持工具感。 | [設計規格](design-md/opencode.ai/DESIGN.md) · [AI 指令](design-md/opencode.ai/PROMPTS.md) |
| [Replicate](design-md/replicate/README.md) | 輕量白底、模型範例與可閱讀的程式碼。 | [設計規格](design-md/replicate/DESIGN.md) · [AI 指令](design-md/replicate/PROMPTS.md) |
| [Runway](design-md/runwayml/README.md) | 電影式暗場搭配白色閱讀區，讓作品成為焦點。 | [設計規格](design-md/runwayml/DESIGN.md) · [AI 指令](design-md/runwayml/PROMPTS.md) |
| [Together AI](design-md/together.ai/README.md) | 黑白結構與柔和色塊，整理多層技術內容。 | [設計規格](design-md/together.ai/DESIGN.md) · [AI 指令](design-md/together.ai/PROMPTS.md) |
| [VoltAgent](design-md/voltagent/README.md) | 終端機式黑底與翡翠色，讓代理工作流可見。 | [設計規格](design-md/voltagent/DESIGN.md) · [AI 指令](design-md/voltagent/PROMPTS.md) |
| [xAI](design-md/x.ai/README.md) | 克制黑白與寬闊留白，保持技術敘事的焦點。 | [設計規格](design-md/x.ai/DESIGN.md) · [AI 指令](design-md/x.ai/PROMPTS.md) |

### 開發工具

| 設計 | 特色 | 檔案 |
| --- | --- | --- |
| [Cursor](design-md/cursor/README.md) | 暖灰紙感與精簡編輯器，呈現開發細節。 | [設計規格](design-md/cursor/DESIGN.md) · [AI 指令](design-md/cursor/PROMPTS.md) |
| [Expo](design-md/expo/README.md) | 清爽中性色與藍色重點，聚焦開發流程。 | [設計規格](design-md/expo/DESIGN.md) · [AI 指令](design-md/expo/PROMPTS.md) |
| [Lovable](design-md/lovable/README.md) | 奶油色、柔和邊框與深色操作按鈕。 | [設計規格](design-md/lovable/DESIGN.md) · [AI 指令](design-md/lovable/PROMPTS.md) |
| [Raycast](design-md/raycast/README.md) | 黑色指令視窗與細膩的強調色，快速而直接。 | [設計規格](design-md/raycast/DESIGN.md) · [AI 指令](design-md/raycast/PROMPTS.md) |
| [Superhuman](design-md/superhuman/README.md) | 深紫與暖白的輕盈對比，聚焦鍵盤效率。 | [設計規格](design-md/superhuman/DESIGN.md) · [AI 指令](design-md/superhuman/PROMPTS.md) |
| [Vercel](design-md/vercel/README.md) | 黑白幾何與細線網格，凸顯產品精度。 | [設計規格](design-md/vercel/DESIGN.md) · [AI 指令](design-md/vercel/PROMPTS.md) |
| [Warp](design-md/warp/README.md) | 暖灰終端機與區塊式指令，兼顧工具感與閱讀。 | [設計規格](design-md/warp/DESIGN.md) · [AI 指令](design-md/warp/PROMPTS.md) |

### 後端與資料

| 設計 | 特色 | 檔案 |
| --- | --- | --- |
| [ClickHouse](design-md/clickhouse/README.md) | 近黑底色與明亮黃色，清楚展示技術。 | [設計規格](design-md/clickhouse/DESIGN.md) · [AI 指令](design-md/clickhouse/PROMPTS.md) |
| [Composio](design-md/composio/README.md) | 黑色介面與電藍色訊號，凸顯整合流程。 | [設計規格](design-md/composio/DESIGN.md) · [AI 指令](design-md/composio/PROMPTS.md) |
| [HashiCorp](design-md/hashicorp/README.md) | 規律黑白網格，承載多產品技術資訊。 | [設計規格](design-md/hashicorp/DESIGN.md) · [AI 指令](design-md/hashicorp/PROMPTS.md) |
| [MongoDB](design-md/mongodb/README.md) | 深青綠與鮮綠色，連接資料與開發者體驗。 | [設計規格](design-md/mongodb/DESIGN.md) · [AI 指令](design-md/mongodb/PROMPTS.md) |
| [PostHog](design-md/posthog/README.md) | 暖灰與黃色細節，兼顧密集資訊和趣味。 | [設計規格](design-md/posthog/DESIGN.md) · [AI 指令](design-md/posthog/PROMPTS.md) |
| [Sanity](design-md/sanity/README.md) | 黃白色面、粗體章節與珊瑚紅，整理內容工作流程。 | [設計規格](design-md/sanity/DESIGN.md) · [AI 指令](design-md/sanity/PROMPTS.md) |
| [Sentry](design-md/sentry/README.md) | 紫黑底與亮色狀態，協助快速定位問題。 | [設計規格](design-md/sentry/DESIGN.md) · [AI 指令](design-md/sentry/PROMPTS.md) |
| [Supabase](design-md/supabase/README.md) | 炭黑面板與翡翠綠，呈現實際開發工作。 | [設計規格](design-md/supabase/DESIGN.md) · [AI 指令](design-md/supabase/PROMPTS.md) |

### 生產力工具

| 設計 | 特色 | 檔案 |
| --- | --- | --- |
| [Cal.com](design-md/cal/README.md) | 中性色與清楚的表單層級，專注排程。 | [設計規格](design-md/cal/DESIGN.md) · [AI 指令](design-md/cal/PROMPTS.md) |
| [Intercom](design-md/intercom/README.md) | 暖白底與橙色訊號，讓對話更有親和力。 | [設計規格](design-md/intercom/DESIGN.md) · [AI 指令](design-md/intercom/PROMPTS.md) |
| [Linear](design-md/linear.app/README.md) | 近黑分層與薰衣草色，精準呈現產品資訊。 | [設計規格](design-md/linear.app/DESIGN.md) · [AI 指令](design-md/linear.app/PROMPTS.md) |
| [Mintlify](design-md/mintlify/README.md) | 綠色點綴與閱讀導向的文件結構。 | [設計規格](design-md/mintlify/DESIGN.md) · [AI 指令](design-md/mintlify/PROMPTS.md) |
| [Notion](design-md/notion/README.md) | 文件式結構與柔和色面，讓知識容易整理。 | [設計規格](design-md/notion/DESIGN.md) · [AI 指令](design-md/notion/PROMPTS.md) |
| [Resend](design-md/resend/README.md) | 近黑底色、單色字級與精簡開發者介面。 | [設計規格](design-md/resend/DESIGN.md) · [AI 指令](design-md/resend/PROMPTS.md) |
| [Slack](design-md/slack/README.md) | 茄紫色配合奶油底與圓角按鈕，突出協作。 | [設計規格](design-md/slack/DESIGN.md) · [AI 指令](design-md/slack/PROMPTS.md) |
| [Zapier](design-md/zapier/README.md) | 暖白與亮橙色，將自動化步驟排列清楚。 | [設計規格](design-md/zapier/DESIGN.md) · [AI 指令](design-md/zapier/PROMPTS.md) |

### 設計與創作

| 設計 | 特色 | 檔案 |
| --- | --- | --- |
| [Airtable](design-md/airtable/README.md) | 彩色分區，把複雜資訊整理清楚。 | [設計規格](design-md/airtable/DESIGN.md) · [AI 指令](design-md/airtable/PROMPTS.md) |
| [Clay](design-md/clay/README.md) | 柔和暖色與不規則構圖，保留創作空間。 | [設計規格](design-md/clay/DESIGN.md) · [AI 指令](design-md/clay/PROMPTS.md) |
| [Figma](design-md/figma/README.md) | 大膽色塊、俐落黑線與充滿活力的構圖。 | [設計規格](design-md/figma/DESIGN.md) · [AI 指令](design-md/figma/PROMPTS.md) |
| [Framer](design-md/framer/README.md) | 深色展示舞台與電藍色，突出作品品質。 | [設計規格](design-md/framer/DESIGN.md) · [AI 指令](design-md/framer/PROMPTS.md) |
| [Miro](design-md/miro/README.md) | 明亮黃色與便箋色彩，讓協作空間有秩序。 | [設計規格](design-md/miro/DESIGN.md) · [AI 指令](design-md/miro/PROMPTS.md) |
| [Webflow](design-md/webflow/README.md) | 大膽黑白區塊與亮藍色，配合精準版面結構。 | [設計規格](design-md/webflow/DESIGN.md) · [AI 指令](design-md/webflow/PROMPTS.md) |

### 金融科技

| 設計 | 特色 | 檔案 |
| --- | --- | --- |
| [Binance](design-md/binance/README.md) | 深色底與黃色重點，資訊一眼可辨。 | [設計規格](design-md/binance/DESIGN.md) · [AI 指令](design-md/binance/PROMPTS.md) |
| [Coinbase](design-md/coinbase/README.md) | 白底與鮮明藍色，建立有秩序的閱讀體驗。 | [設計規格](design-md/coinbase/DESIGN.md) · [AI 指令](design-md/coinbase/PROMPTS.md) |
| [Kraken](design-md/kraken/README.md) | 紫色按鈕與冷灰中性色，保持清楚可信。 | [設計規格](design-md/kraken/DESIGN.md) · [AI 指令](design-md/kraken/PROMPTS.md) |
| [Mastercard](design-md/mastercard/README.md) | 溫暖米色與圓弧構圖，讓內容輕鬆流動。 | [設計規格](design-md/mastercard/DESIGN.md) · [AI 指令](design-md/mastercard/PROMPTS.md) |
| [Revolut](design-md/revolut/README.md) | 俐落字級與深淺卡片，整理多種金融資訊。 | [設計規格](design-md/revolut/DESIGN.md) · [AI 指令](design-md/revolut/PROMPTS.md) |
| [Stripe](design-md/stripe/README.md) | 深藍字色、靛紫操作與輕盈的漸層空間。 | [設計規格](design-md/stripe/DESIGN.md) · [AI 指令](design-md/stripe/PROMPTS.md) |
| [Wise](design-md/wise/README.md) | 鮮綠色與深綠字色，讓數字和步驟清晰可讀。 | [設計規格](design-md/wise/DESIGN.md) · [AI 指令](design-md/wise/PROMPTS.md) |

### 電商與零售

| 設計 | 特色 | 檔案 |
| --- | --- | --- |
| [Airbnb](design-md/airbnb/README.md) | 珊瑚紅與圓角，讓探索成為主角。 | [設計規格](design-md/airbnb/DESIGN.md) · [AI 指令](design-md/airbnb/PROMPTS.md) |
| [Meta](design-md/meta/README.md) | 大幅影像與藍色操作，建立明確產品層次。 | [設計規格](design-md/meta/DESIGN.md) · [AI 指令](design-md/meta/PROMPTS.md) |
| [Nike](design-md/nike/README.md) | 巨大標題、黑白對比與影像優先的編排。 | [設計規格](design-md/nike/DESIGN.md) · [AI 指令](design-md/nike/PROMPTS.md) |
| [Shopify](design-md/shopify/README.md) | 黑色與柔綠色面，讓商業展示保有呼吸感。 | [設計規格](design-md/shopify/DESIGN.md) · [AI 指令](design-md/shopify/PROMPTS.md) |
| [Starbucks](design-md/starbucks/README.md) | 深淺綠色、白底與交錯區塊，呈現親切日常感。 | [設計規格](design-md/starbucks/DESIGN.md) · [AI 指令](design-md/starbucks/PROMPTS.md) |

### 媒體與科技

| 設計 | 特色 | 檔案 |
| --- | --- | --- |
| [Apple](design-md/apple/README.md) | 大幅留白，讓產品與文字自己說話。 | [設計規格](design-md/apple/DESIGN.md) · [AI 指令](design-md/apple/PROMPTS.md) |
| [HP](design-md/hp/README.md) | 白色版面與電藍色，配合俐落幾何切角。 | [設計規格](design-md/hp/DESIGN.md) · [AI 指令](design-md/hp/PROMPTS.md) |
| [IBM](design-md/ibm/README.md) | 嚴謹網格、方角元件與清楚的藍色層級。 | [設計規格](design-md/ibm/DESIGN.md) · [AI 指令](design-md/ibm/PROMPTS.md) |
| [NVIDIA](design-md/nvidia/README.md) | 黑色與鮮綠色構成高對比的技術舞台。 | [設計規格](design-md/nvidia/DESIGN.md) · [AI 指令](design-md/nvidia/PROMPTS.md) |
| [Pinterest](design-md/pinterest/README.md) | 紅色操作與瀑布流，讓視覺收藏容易瀏覽。 | [設計規格](design-md/pinterest/DESIGN.md) · [AI 指令](design-md/pinterest/PROMPTS.md) |
| [PlayStation](design-md/playstation/README.md) | 藍色訊號配合深淺章節，營造遊戲展示感。 | [設計規格](design-md/playstation/DESIGN.md) · [AI 指令](design-md/playstation/PROMPTS.md) |
| [SpaceX](design-md/spacex/README.md) | 黑白全幅敘事，以影像與大字級建立張力。 | [設計規格](design-md/spacex/DESIGN.md) · [AI 指令](design-md/spacex/PROMPTS.md) |
| [Spotify](design-md/spotify/README.md) | 深色分層與鮮綠色操作，配合封面主導的編排。 | [設計規格](design-md/spotify/DESIGN.md) · [AI 指令](design-md/spotify/PROMPTS.md) |
| [The Verge](design-md/theverge/README.md) | 酸綠與紫色交錯，搭配有力的編輯字級。 | [設計規格](design-md/theverge/DESIGN.md) · [AI 指令](design-md/theverge/PROMPTS.md) |
| [Uber](design-md/uber/README.md) | 純黑與白色、粗體字級與直接的操作流程。 | [設計規格](design-md/uber/DESIGN.md) · [AI 指令](design-md/uber/PROMPTS.md) |
| [Vodafone](design-md/vodafone/README.md) | 紅色章節與大字標題，清楚傳達服務。 | [設計規格](design-md/vodafone/DESIGN.md) · [AI 指令](design-md/vodafone/PROMPTS.md) |
| [WIRED](design-md/wired/README.md) | 報紙式密度、襯線標題與精簡藍色連結。 | [設計規格](design-md/wired/DESIGN.md) · [AI 指令](design-md/wired/PROMPTS.md) |

### 汽車

| 設計 | 特色 | 檔案 |
| --- | --- | --- |
| [BMW](design-md/bmw/README.md) | 精準網格搭配深淺交錯的產品敘事。 | [設計規格](design-md/bmw/DESIGN.md) · [AI 指令](design-md/bmw/PROMPTS.md) |
| [BMW M](design-md/bmw-m/README.md) | 黑色舞台、緊密字級與少量賽車色彩。 | [設計規格](design-md/bmw-m/DESIGN.md) · [AI 指令](design-md/bmw-m/PROMPTS.md) |
| [Bugatti](design-md/bugatti/README.md) | 近乎純黑的畫布，搭配雕塑般的比例。 | [設計規格](design-md/bugatti/DESIGN.md) · [AI 指令](design-md/bugatti/PROMPTS.md) |
| [Ferrari](design-md/ferrari/README.md) | 黑白光影與克制的紅色，帶出速度感。 | [設計規格](design-md/ferrari/DESIGN.md) · [AI 指令](design-md/ferrari/PROMPTS.md) |
| [Lamborghini](design-md/lamborghini/README.md) | 純黑、大寫字級與金色細節，凝聚視線。 | [設計規格](design-md/lamborghini/DESIGN.md) · [AI 指令](design-md/lamborghini/PROMPTS.md) |
| [Renault](design-md/renault/README.md) | 俐落方角與明亮色帶，形成大膽的章節感。 | [設計規格](design-md/renault/DESIGN.md) · [AI 指令](design-md/renault/PROMPTS.md) |
| [Tesla](design-md/tesla/README.md) | 全幅視覺與極少元件，留下清楚的行動路徑。 | [設計規格](design-md/tesla/DESIGN.md) · [AI 指令](design-md/tesla/PROMPTS.md) |

### 復古網頁

| 設計 | 特色 | 檔案 |
| --- | --- | --- |
| [Dell (1996)](design-md/dell-1996/README.md) | 色塊與復古排版，重現早期網頁型錄感。 | [設計規格](design-md/dell-1996/DESIGN.md) · [AI 指令](design-md/dell-1996/PROMPTS.md) |
| [Nintendo (2001)](design-md/nintendo-2001/README.md) | 金屬框、琥珀色導覽與遊戲盒式的懷舊編排。 | [設計規格](design-md/nintendo-2001/DESIGN.md) · [AI 指令](design-md/nintendo-2001/PROMPTS.md) |

<!-- COLLECTION:END -->

## 參與貢獻

歡迎新增設計分析、修正資料或改善 AI 指令。請閱讀 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 授權

[MIT](LICENSE)。原始設計分析 © 2026 VoltAgent；新指令、程式與預覽 © 2026 Awesome AI Web Design contributors。
