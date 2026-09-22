# Awesome AI Web Design

**74 套設計參考、222 則重新撰寫的 AI 指令，全部免費。**

[開啟免費設計集](https://awesome-ai-web-design.philqq100.chatgpt.site) · [GitHub 原始碼](https://github.com/irons163/awesome-ai-web-design)

把喜歡的 `DESIGN.md` 放進專案，再選擇對應的 prompt，讓 AI 依照一致的色彩、字級、間距與元件規格實作介面。沒有帳號、訂閱、付費下載或廣告。設計分析保留原始深度，AI 操作指令全部重新撰寫。

這是以 [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) 為基礎的獨立免費版本，不是原作者的官方網站。保留原始 MIT 授權與來源，詳見 [ATTRIBUTION.md](ATTRIBUTION.md)。

## 立即使用

1. 在下方目錄選一套設計，將其 `DESIGN.md` 複製到你的專案根目錄。
2. 開啟同資料夾的 `PROMPTS.md`，挑選「建立新頁面」、「製作元件」或「改造既有介面」。
3. 把需求與選好的指令交給能讀取專案檔案的 AI 開發工具。

例如：

```text
先讀取專案根目錄的 DESIGN.md，將它作為這次介面的視覺規格。
我要做一個可以搜尋、篩選與收藏文章的閱讀清單。
沿用目前技術架構，先建立共用的色彩與字級 token，再實作完整的操作流程。
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

從 ZIP 解壓後可直接啟動伺服器。網站的完整下載包由 GitHub Releases 提供；`python3 scripts/build.py` 可在本機重建同名 ZIP，ZIP 不會將自己遞迴封裝在內。

開啟 **http://127.0.0.1:4173**。可搜尋品牌或關鍵字、依領域和明暗模式篩選、收藏設計、比較 Stitch 生成頁面、閱讀全文、複製指令，以及下載單一檔案或全部 ZIP。收藏只儲存在目前瀏覽器。

網站預覽由 Google Stitch MCP 依各份設計分析與專屬情境實際生成，保留原始 HTML 與截圖，不是品牌原站截圖。每份範例附有生成指令、Stitch project/screen ID 與檔案 SHA-256。HTML 是靜態介面範例，可能使用 Google Fonts、Tailwind CDN 或 Stitch 匯出的外部圖片，部分操作與資料僅供展示。直接開 `index.html` 時瀏覽器可能阻擋讀取資料；請使用上述本機伺服器。

## 開發與驗證

```sh
python3 scripts/rewrite_prompts.py
python3 scripts/build.py
python3 -m unittest discover -s tests -v
```

有 Node.js 的環境也可使用 `npm run dev`、`npm run build`、`npm test`；它們呼叫相同的 Python 指令，不需 `npm install`。

- `design-md/<slug>/DESIGN.md`：完整設計分析，加上全新 AI 指令。
- `design-md/<slug>/PROMPTS.md`：三種任務指令與迭代流程。
- `design-md/<slug>/preview.html`：Stitch 匯出的原始 HTML。
- `design-md/<slug>/preview.png`：Stitch 原始生成截圖。
- `design-md/<slug>/STITCH-PROMPT.md` / `STITCH.json`：生成指令與可追溯的來源紀錄。
- `data/recipes.json`：本專案撰寫的品牌情境與元件需求。
- `data/upstream.json`：匯入版本、每份原始文件的 SHA-256。
- `assets/catalog.json`：由設計檔案與情境資料產生的網站目錄。
- `assets/all-designs.zip`：建置產出的完整下載包，包含設計、prompt、HTML、原始截圖、網站原始碼與授權；不提交二進位 ZIP，發布到 GitHub Releases。

修改情境後先執行 `rewrite_prompts.py`；再執行 `build.py` 更新目錄和下載包。`build.py` 只驗證並封裝既有 Stitch 匯出，不會產生、重繪或覆蓋預覽，也不會發起 AI 請求。要更新範例，需在 Stitch 重新生成並透過 `scripts/import_stitch.py` 匯入 MCP 結果。金鑰只供生成工具使用，不會放入網站或下載包。一般檢查流程由 `.github/workflows/check.yml` 提供。

## 網站發布

網站採純靜態部署。執行 `python3 scripts/build.py` 更新資料與下載包，再執行 `python3 scripts/build_site.py` 將可公開的網站檔案整理到 `dist/`。正式網站由 Sites 託管；GitHub 儲存庫保存完整原始碼。 完整 ZIP 需由同一份來源 commit 建置，並以 `all-designs.zip` 檔名上傳至 GitHub Releases；網站使用最新 Release 的固定下載連結。`dist/` 不包含這個大型 ZIP。

## 免費與來源

本專案的所有內容均直接開放下載，沒有付費牆、私有訂製入口或支付整合。MIT 授權仍允許使用者將內容用於商業專案；「免費提供」不等於限制下游商用。

色彩和字體資料是匯入版本的分析紀錄，尚未逐一重新查核所有品牌當前網站。品牌名稱、商標與專有字體屬於各自權利人，下載包不包含品牌商標或專有字體檔案。無障礙要求優先於匯入分析中過小的觸控目標或缺少焦點狀態的建議。

## 設計目錄

<!-- COLLECTION:START -->

### AI 與模型 / AI & LLM Platforms

| 設計 | 特色 | 檔案 |
| --- | --- | --- |
| [Claude](design-md/claude/README.md) | 奶油色、陶土色與襯線標題的溫暖節奏。 | [DESIGN.md](design-md/claude/DESIGN.md) · [Prompts](design-md/claude/PROMPTS.md) |
| [Cohere](design-md/cohere/README.md) | 中性閱讀面搭配低彩度產品色塊。 | [DESIGN.md](design-md/cohere/DESIGN.md) · [Prompts](design-md/cohere/PROMPTS.md) |
| [ElevenLabs](design-md/elevenlabs/README.md) | 乾淨石色、聲音波形與細膩的文字層次。 | [DESIGN.md](design-md/elevenlabs/DESIGN.md) · [Prompts](design-md/elevenlabs/PROMPTS.md) |
| [MiniMax](design-md/minimax/README.md) | 多產品色彩配合輕量網格，保持技術可讀性。 | [DESIGN.md](design-md/minimax/DESIGN.md) · [Prompts](design-md/minimax/PROMPTS.md) |
| [Mistral AI](design-md/mistral.ai/README.md) | 暖黃與橙色像素節奏，帶出開放技術感。 | [DESIGN.md](design-md/mistral.ai/DESIGN.md) · [Prompts](design-md/mistral.ai/PROMPTS.md) |
| [Ollama](design-md/ollama/README.md) | 單色、終端機範例與直白的內容結構。 | [DESIGN.md](design-md/ollama/DESIGN.md) · [Prompts](design-md/ollama/PROMPTS.md) |
| [OpenCode](design-md/opencode.ai/README.md) | 暖灰紙面搭配深色終端機，保持工具感。 | [DESIGN.md](design-md/opencode.ai/DESIGN.md) · [Prompts](design-md/opencode.ai/PROMPTS.md) |
| [Replicate](design-md/replicate/README.md) | 輕量白底、模型範例與可閱讀的程式碼。 | [DESIGN.md](design-md/replicate/DESIGN.md) · [Prompts](design-md/replicate/PROMPTS.md) |
| [Runway](design-md/runwayml/README.md) | 電影式暗場搭配白色閱讀區，讓作品成為焦點。 | [DESIGN.md](design-md/runwayml/DESIGN.md) · [Prompts](design-md/runwayml/PROMPTS.md) |
| [Together AI](design-md/together.ai/README.md) | 黑白結構與柔和色塊，整理多層技術內容。 | [DESIGN.md](design-md/together.ai/DESIGN.md) · [Prompts](design-md/together.ai/PROMPTS.md) |
| [VoltAgent](design-md/voltagent/README.md) | 終端機式黑底與翡翠色，讓代理工作流可見。 | [DESIGN.md](design-md/voltagent/DESIGN.md) · [Prompts](design-md/voltagent/PROMPTS.md) |
| [xAI](design-md/x.ai/README.md) | 克制黑白與寬闊留白，保持技術敘事的焦點。 | [DESIGN.md](design-md/x.ai/DESIGN.md) · [Prompts](design-md/x.ai/PROMPTS.md) |

### 開發工具 / Developer Tools & IDEs

| 設計 | 特色 | 檔案 |
| --- | --- | --- |
| [Cursor](design-md/cursor/README.md) | 暖灰紙感與精簡編輯器，呈現開發細節。 | [DESIGN.md](design-md/cursor/DESIGN.md) · [Prompts](design-md/cursor/PROMPTS.md) |
| [Expo](design-md/expo/README.md) | 清爽中性色與藍色重點，聚焦開發流程。 | [DESIGN.md](design-md/expo/DESIGN.md) · [Prompts](design-md/expo/PROMPTS.md) |
| [Lovable](design-md/lovable/README.md) | 奶油色、柔和邊框與深色操作按鈕。 | [DESIGN.md](design-md/lovable/DESIGN.md) · [Prompts](design-md/lovable/PROMPTS.md) |
| [Raycast](design-md/raycast/README.md) | 黑色指令視窗與細膩的強調色，快速而直接。 | [DESIGN.md](design-md/raycast/DESIGN.md) · [Prompts](design-md/raycast/PROMPTS.md) |
| [Superhuman](design-md/superhuman/README.md) | 深紫與暖白的輕盈對比，聚焦鍵盤效率。 | [DESIGN.md](design-md/superhuman/DESIGN.md) · [Prompts](design-md/superhuman/PROMPTS.md) |
| [Vercel](design-md/vercel/README.md) | 黑白幾何與細線網格，凸顯產品精度。 | [DESIGN.md](design-md/vercel/DESIGN.md) · [Prompts](design-md/vercel/PROMPTS.md) |
| [Warp](design-md/warp/README.md) | 暖灰終端機與區塊式指令，兼顧工具感與閱讀。 | [DESIGN.md](design-md/warp/DESIGN.md) · [Prompts](design-md/warp/PROMPTS.md) |

### 後端與資料 / Backend, Database & DevOps

| 設計 | 特色 | 檔案 |
| --- | --- | --- |
| [ClickHouse](design-md/clickhouse/README.md) | 近黑底色與明亮黃色，清楚展示技術。 | [DESIGN.md](design-md/clickhouse/DESIGN.md) · [Prompts](design-md/clickhouse/PROMPTS.md) |
| [Composio](design-md/composio/README.md) | 黑色介面與電藍色訊號，凸顯整合流程。 | [DESIGN.md](design-md/composio/DESIGN.md) · [Prompts](design-md/composio/PROMPTS.md) |
| [HashiCorp](design-md/hashicorp/README.md) | 規律黑白網格，承載多產品技術資訊。 | [DESIGN.md](design-md/hashicorp/DESIGN.md) · [Prompts](design-md/hashicorp/PROMPTS.md) |
| [MongoDB](design-md/mongodb/README.md) | 深青綠與鮮綠色，連接資料與開發者體驗。 | [DESIGN.md](design-md/mongodb/DESIGN.md) · [Prompts](design-md/mongodb/PROMPTS.md) |
| [PostHog](design-md/posthog/README.md) | 暖灰與黃色細節，兼顧密集資訊和趣味。 | [DESIGN.md](design-md/posthog/DESIGN.md) · [Prompts](design-md/posthog/PROMPTS.md) |
| [Sanity](design-md/sanity/README.md) | 大字級、近黑底與珊瑚紅，清楚呈現內容工作流。 | [DESIGN.md](design-md/sanity/DESIGN.md) · [Prompts](design-md/sanity/PROMPTS.md) |
| [Sentry](design-md/sentry/README.md) | 紫黑底與亮色狀態，協助快速定位問題。 | [DESIGN.md](design-md/sentry/DESIGN.md) · [Prompts](design-md/sentry/PROMPTS.md) |
| [Supabase](design-md/supabase/README.md) | 炭黑面板與翡翠綠，呈現實際開發工作。 | [DESIGN.md](design-md/supabase/DESIGN.md) · [Prompts](design-md/supabase/PROMPTS.md) |

### 生產力工具 / Productivity & SaaS

| 設計 | 特色 | 檔案 |
| --- | --- | --- |
| [Cal.com](design-md/cal/README.md) | 中性色與清楚的表單層級，專注排程。 | [DESIGN.md](design-md/cal/DESIGN.md) · [Prompts](design-md/cal/PROMPTS.md) |
| [Intercom](design-md/intercom/README.md) | 暖白底與橙色訊號，讓對話更有親和力。 | [DESIGN.md](design-md/intercom/DESIGN.md) · [Prompts](design-md/intercom/PROMPTS.md) |
| [Linear](design-md/linear.app/README.md) | 近黑分層與薰衣草色，精準呈現產品資訊。 | [DESIGN.md](design-md/linear.app/DESIGN.md) · [Prompts](design-md/linear.app/PROMPTS.md) |
| [Mintlify](design-md/mintlify/README.md) | 綠色點綴與閱讀導向的文件結構。 | [DESIGN.md](design-md/mintlify/DESIGN.md) · [Prompts](design-md/mintlify/PROMPTS.md) |
| [Notion](design-md/notion/README.md) | 文件式結構與柔和色面，讓知識容易整理。 | [DESIGN.md](design-md/notion/DESIGN.md) · [Prompts](design-md/notion/PROMPTS.md) |
| [Resend](design-md/resend/README.md) | 近黑底色、單色字級與精簡開發者介面。 | [DESIGN.md](design-md/resend/DESIGN.md) · [Prompts](design-md/resend/PROMPTS.md) |
| [Slack](design-md/slack/README.md) | 茄紫色配合奶油底與圓角按鈕，突出協作。 | [DESIGN.md](design-md/slack/DESIGN.md) · [Prompts](design-md/slack/PROMPTS.md) |
| [Zapier](design-md/zapier/README.md) | 暖白與亮橙色，將自動化步驟排列清楚。 | [DESIGN.md](design-md/zapier/DESIGN.md) · [Prompts](design-md/zapier/PROMPTS.md) |

### 設計與創作 / Design & Creative Tools

| 設計 | 特色 | 檔案 |
| --- | --- | --- |
| [Airtable](design-md/airtable/README.md) | 彩色分區，把複雜資訊整理清楚。 | [DESIGN.md](design-md/airtable/DESIGN.md) · [Prompts](design-md/airtable/PROMPTS.md) |
| [Clay](design-md/clay/README.md) | 柔和暖色與不規則構圖，保留創作空間。 | [DESIGN.md](design-md/clay/DESIGN.md) · [Prompts](design-md/clay/PROMPTS.md) |
| [Figma](design-md/figma/README.md) | 大膽色塊、俐落黑線與充滿活力的構圖。 | [DESIGN.md](design-md/figma/DESIGN.md) · [Prompts](design-md/figma/PROMPTS.md) |
| [Framer](design-md/framer/README.md) | 深色展示舞台與電藍色，突出作品品質。 | [DESIGN.md](design-md/framer/DESIGN.md) · [Prompts](design-md/framer/PROMPTS.md) |
| [Miro](design-md/miro/README.md) | 明亮黃色與便箋色彩，讓協作空間有秩序。 | [DESIGN.md](design-md/miro/DESIGN.md) · [Prompts](design-md/miro/PROMPTS.md) |
| [Webflow](design-md/webflow/README.md) | 大膽黑白區塊與亮藍色，配合精準版面結構。 | [DESIGN.md](design-md/webflow/DESIGN.md) · [Prompts](design-md/webflow/PROMPTS.md) |

### 金融科技 / Fintech & Crypto

| 設計 | 特色 | 檔案 |
| --- | --- | --- |
| [Binance](design-md/binance/README.md) | 深色底與黃色重點，資訊一眼可辨。 | [DESIGN.md](design-md/binance/DESIGN.md) · [Prompts](design-md/binance/PROMPTS.md) |
| [Coinbase](design-md/coinbase/README.md) | 白底與鮮明藍色，建立有秩序的閱讀體驗。 | [DESIGN.md](design-md/coinbase/DESIGN.md) · [Prompts](design-md/coinbase/PROMPTS.md) |
| [Kraken](design-md/kraken/README.md) | 紫色按鈕與冷灰中性色，保持清楚可信。 | [DESIGN.md](design-md/kraken/DESIGN.md) · [Prompts](design-md/kraken/PROMPTS.md) |
| [Mastercard](design-md/mastercard/README.md) | 溫暖米色與圓弧構圖，讓內容輕鬆流動。 | [DESIGN.md](design-md/mastercard/DESIGN.md) · [Prompts](design-md/mastercard/PROMPTS.md) |
| [Revolut](design-md/revolut/README.md) | 俐落字級與深淺卡片，整理多種金融資訊。 | [DESIGN.md](design-md/revolut/DESIGN.md) · [Prompts](design-md/revolut/PROMPTS.md) |
| [Stripe](design-md/stripe/README.md) | 深藍字色、靛紫操作與輕盈的漸層空間。 | [DESIGN.md](design-md/stripe/DESIGN.md) · [Prompts](design-md/stripe/PROMPTS.md) |
| [Wise](design-md/wise/README.md) | 鮮綠色與深綠字色，讓數字和步驟清晰可讀。 | [DESIGN.md](design-md/wise/DESIGN.md) · [Prompts](design-md/wise/PROMPTS.md) |

### 電商與零售 / E-commerce & Retail

| 設計 | 特色 | 檔案 |
| --- | --- | --- |
| [Airbnb](design-md/airbnb/README.md) | 珊瑚紅與圓角，讓探索成為主角。 | [DESIGN.md](design-md/airbnb/DESIGN.md) · [Prompts](design-md/airbnb/PROMPTS.md) |
| [Meta](design-md/meta/README.md) | 大幅影像與藍色操作，建立明確產品層次。 | [DESIGN.md](design-md/meta/DESIGN.md) · [Prompts](design-md/meta/PROMPTS.md) |
| [Nike](design-md/nike/README.md) | 巨大標題、黑白對比與影像優先的編排。 | [DESIGN.md](design-md/nike/DESIGN.md) · [Prompts](design-md/nike/PROMPTS.md) |
| [Shopify](design-md/shopify/README.md) | 黑色與柔綠色面，讓商業展示保有呼吸感。 | [DESIGN.md](design-md/shopify/DESIGN.md) · [Prompts](design-md/shopify/PROMPTS.md) |
| [Starbucks](design-md/starbucks/README.md) | 多層綠色與暖奶油底，呈現親切日常感。 | [DESIGN.md](design-md/starbucks/DESIGN.md) · [Prompts](design-md/starbucks/PROMPTS.md) |

### 媒體與科技 / Media & Consumer Tech

| 設計 | 特色 | 檔案 |
| --- | --- | --- |
| [Apple](design-md/apple/README.md) | 大幅留白，讓產品與文字自己說話。 | [DESIGN.md](design-md/apple/DESIGN.md) · [Prompts](design-md/apple/PROMPTS.md) |
| [HP](design-md/hp/README.md) | 白色版面與電藍色，配合俐落幾何切角。 | [DESIGN.md](design-md/hp/DESIGN.md) · [Prompts](design-md/hp/PROMPTS.md) |
| [IBM](design-md/ibm/README.md) | 嚴謹網格、方角元件與清楚的藍色層級。 | [DESIGN.md](design-md/ibm/DESIGN.md) · [Prompts](design-md/ibm/PROMPTS.md) |
| [NVIDIA](design-md/nvidia/README.md) | 黑色與鮮綠色構成高對比的技術舞台。 | [DESIGN.md](design-md/nvidia/DESIGN.md) · [Prompts](design-md/nvidia/PROMPTS.md) |
| [Pinterest](design-md/pinterest/README.md) | 紅色操作與瀑布流，讓視覺收藏容易瀏覽。 | [DESIGN.md](design-md/pinterest/DESIGN.md) · [Prompts](design-md/pinterest/PROMPTS.md) |
| [PlayStation](design-md/playstation/README.md) | 藍色訊號配合深淺章節，營造遊戲展示感。 | [DESIGN.md](design-md/playstation/DESIGN.md) · [Prompts](design-md/playstation/PROMPTS.md) |
| [SpaceX](design-md/spacex/README.md) | 黑白全幅敘事，以影像與大字級建立張力。 | [DESIGN.md](design-md/spacex/DESIGN.md) · [Prompts](design-md/spacex/PROMPTS.md) |
| [Spotify](design-md/spotify/README.md) | 深色分層與鮮綠色操作，配合封面主導的編排。 | [DESIGN.md](design-md/spotify/DESIGN.md) · [Prompts](design-md/spotify/PROMPTS.md) |
| [The Verge](design-md/theverge/README.md) | 酸綠與紫色交錯，搭配有力的編輯字級。 | [DESIGN.md](design-md/theverge/DESIGN.md) · [Prompts](design-md/theverge/PROMPTS.md) |
| [Uber](design-md/uber/README.md) | 純黑與白色、粗體字級與直接的操作流程。 | [DESIGN.md](design-md/uber/DESIGN.md) · [Prompts](design-md/uber/PROMPTS.md) |
| [Vodafone](design-md/vodafone/README.md) | 紅色章節與大字標題，清楚傳達服務。 | [DESIGN.md](design-md/vodafone/DESIGN.md) · [Prompts](design-md/vodafone/PROMPTS.md) |
| [WIRED](design-md/wired/README.md) | 報紙式密度、襯線標題與精簡藍色連結。 | [DESIGN.md](design-md/wired/DESIGN.md) · [Prompts](design-md/wired/PROMPTS.md) |

### 汽車 / Automotive

| 設計 | 特色 | 檔案 |
| --- | --- | --- |
| [BMW](design-md/bmw/README.md) | 精準網格搭配深淺交錯的產品敘事。 | [DESIGN.md](design-md/bmw/DESIGN.md) · [Prompts](design-md/bmw/PROMPTS.md) |
| [BMW M](design-md/bmw-m/README.md) | 黑色舞台、緊密字級與少量賽車色彩。 | [DESIGN.md](design-md/bmw-m/DESIGN.md) · [Prompts](design-md/bmw-m/PROMPTS.md) |
| [Bugatti](design-md/bugatti/README.md) | 近乎純黑的畫布，搭配雕塑般的比例。 | [DESIGN.md](design-md/bugatti/DESIGN.md) · [Prompts](design-md/bugatti/PROMPTS.md) |
| [Ferrari](design-md/ferrari/README.md) | 黑白光影與克制的紅色，帶出速度感。 | [DESIGN.md](design-md/ferrari/DESIGN.md) · [Prompts](design-md/ferrari/PROMPTS.md) |
| [Lamborghini](design-md/lamborghini/README.md) | 純黑、大寫字級與金色細節，凝聚視線。 | [DESIGN.md](design-md/lamborghini/DESIGN.md) · [Prompts](design-md/lamborghini/PROMPTS.md) |
| [Renault](design-md/renault/README.md) | 俐落方角與明亮色帶，形成大膽的章節感。 | [DESIGN.md](design-md/renault/DESIGN.md) · [Prompts](design-md/renault/PROMPTS.md) |
| [Tesla](design-md/tesla/README.md) | 全幅視覺與極少元件，留下清楚的行動路徑。 | [DESIGN.md](design-md/tesla/DESIGN.md) · [Prompts](design-md/tesla/PROMPTS.md) |

### 復古網頁 / Retro Web · DESIGN.md Nostalgia

| 設計 | 特色 | 檔案 |
| --- | --- | --- |
| [Dell (1996)](design-md/dell-1996/README.md) | 色塊與復古排版，重現早期網頁型錄感。 | [DESIGN.md](design-md/dell-1996/DESIGN.md) · [Prompts](design-md/dell-1996/PROMPTS.md) |
| [Nintendo (2001)](design-md/nintendo-2001/README.md) | 金屬框、琥珀色導覽與遊戲盒式的懷舊編排。 | [DESIGN.md](design-md/nintendo-2001/DESIGN.md) · [Prompts](design-md/nintendo-2001/PROMPTS.md) |

<!-- COLLECTION:END -->

## 參與貢獻

歡迎新增設計分析、修正資料或改善 prompt。請閱讀 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 授權

[MIT](LICENSE)。原始設計分析 © 2026 VoltAgent；新指令、程式與預覽 © 2026 Awesome AI Web Design contributors。
