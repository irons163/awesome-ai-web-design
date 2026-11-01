# Awesome AI Web Design

**94 套品牌設計參考，附繁體中文設計規格、AI 指令與 CSS 起始檔。**

[開啟網站](https://webdesign.zero2codex.dev/) · [下載 94 套合集](https://webdesign.zero2codex.dev/assets/design-references.zip) · [參考來源](https://webdesign.zero2codex.dev/reference-sources.html)

選一套喜歡的設計，下載只含 `DESIGN.md` 與 `PROMPTS.md` 的簡易包，或按「一次複製給 AI」取得兩份完整內容。選一種方式，補上自己的需求就能開始。介面說明、主要設計規格與 AI 指令皆使用繁體中文（台灣用語）；品牌名稱、程式碼與原始預覽保留原文。

所有設計與下載免費開放，不需帳號、訂閱或 API 金鑰，沒有付費牆與廣告。

## 可以做什麼

- **找設計**：搜尋品牌與關鍵字，搭配 10 種領域分類及明暗模式篩選。
- **看預覽**：開啟品牌詳情，查看介面、設計規格、AI 指令與參考日期。
- **開始實作**：取得角色色碼、字級、間距、版面斷點、元件欄位與互動行為，搭配 CSS 起始檔建立介面。
- **下載或直接複製**：簡易包只含兩份核心文件；複製版把完整規格與指令合在一起，不需要下載或上傳檔案。含 CSS 等補充檔案的完整包與單份下載放在進階選項；另提供 94 套合集供批次收藏。
- **收藏設計**：收藏儲存在目前瀏覽器，重新整理後仍保留，並在同網域的分頁間同步。

網站支援桌面與手機瀏覽。收藏不會同步至其他裝置；品牌預覽中的部分互動使用示範資料。

## 怎麼使用

1. 開啟[網站](https://webdesign.zero2codex.dev/)，搜尋品牌或使用篩選，挑一套設計。
2. 選一種方式取得內容：
   - **不下載**：按「一次複製給 AI」，把完整設計規格與指令貼進 AI 對話，填入自己的需求後送出。
   - **保留檔案**：按「下載簡易包」並解壓縮，將兩份文件放入專案的 `design-reference/`，再依「開始使用」的說明複製開工指令。
3. 依產品需求實作，並檢查手機版、鍵盤操作與主要功能。

例如，將下列指令交給能讀取專案檔案的 AI 開發工具：

```text
請先讀取 design-reference/DESIGN.md 與 design-reference/PROMPTS.md。

我要做一個繁體中文的閱讀清單網站，功能包含文章搜尋、分類篩選與收藏。
請沿用專案現有的技術架構，依設計規格建立色彩、字級、間距與共用元件。
只使用這兩份核心文件即可開始；缺少素材時依 DESIGN.md 採用無圖版做法。

使用我的產品名稱與內容，先完成可在本機操作的前端原型。
收藏先儲存在瀏覽器，並處理空清單、搜尋無結果、鍵盤焦點與手機版。
完成後說明變更檔案、實際驗證結果與需要我補充的資料。
```

資料包提供製作前端介面的依據。實際結果需要依產品需求調整與測試；登入、付款或資料庫等服務另依專案需求串接，規格不保證與品牌官網像素相同。

## 簡易包與完整包

**簡易包只有 `DESIGN.md` 與 `PROMPTS.md` 兩份文件，足以開始製作網站介面。**「一次複製給 AI」包含相同的兩份完整內容，另附可填寫需求的說明，原文提到的隨附文件已直接放在複製內容中。簡易 ZIP 的中繼資料保留授權與來源聲明。

需要樣式起始檔或設計數值時，再到進階選項下載完整包。完整包共 10 個檔案；補充檔案依需要使用：

| 檔案 | 用途 |
| --- | --- |
| `DESIGN.md` | 完整視覺規格、元件行為、響應式條件與必要 CSS，可獨立閱讀。 |
| `PROMPTS.md` | 可填入產品需求的繁體中文 AI 實作指令。 |
| `TOKENS.json` | 色彩、字級、間距等設計數值，供工具讀取。 |
| `starter.css` | 與主要規格一致的 CSS 起始檔。 |
| `ASSETS.md`、`ASSETS.json` | 素材需求、建議路徑與缺少圖片時的做法。 |
| `README.md`、`SOURCES.json` | 使用說明、參考日期與來源依據。 |
| `LICENSE`、`ATTRIBUTION.md` | 授權與來源聲明。 |

[94 套合集](https://webdesign.zero2codex.dev/assets/design-references.zip) 共 568 個檔案：94 組主要規格、指令、設計數值、CSS 與兩份素材說明，加上共用說明、來源清單、授權及致謝。資料包未附品牌商標、專有字型或完整官網媒體；規格提供系統字型與無圖版做法。

原始碼另保留 94 份延伸設計分析、282 則任務指令，以及 Google Stitch 生成紀錄；近期新增的公開預覽經修正並重新截圖。網站主要分頁與下載包採用目前的實作規格；延伸分析與生成預覽可供深入研究。

## 來源與授權

Awesome AI Web Design 由 [PhilForge](https://philforge.com/) 製作與維護，提供繁體中文設計規格、重新撰寫的 AI 實作指令、可操作預覽與下載工具。

設計數值依保存的參考資料與實作建議整理，主要規格會標示依據。每個品牌的觀察日期與範圍見[參考來源](https://webdesign.zero2codex.dev/reference-sources.html)；各套 Stitch 生成資訊、原始輸出摘要與公開預覽的調整紀錄，請見對應的 `STITCH.json`。

程式與文字依 [MIT](LICENSE) 授權提供。第三方資料的適用授權及歷史來源集中於 [授權與資料來源](ATTRIBUTION.md)。品牌名稱、商標、字型、圖片與影片的權利屬各自權利人；使用時請保留適用的授權與來源聲明。

## 設計目錄

以下為原始碼中的延伸分析與任務指令。使用目前的主要規格與實作包，請至[網站設計目錄](https://webdesign.zero2codex.dev/)。

<details>
<summary>展開全部 94 套設計</summary>

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
| [GitHub](design-md/github/README.md) | 清楚的開發工具版面，白底搭配綠色操作與程式面板。 | [設計規格](design-md/github/DESIGN.md) · [AI 指令](design-md/github/PROMPTS.md) |

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
| [Discord](design-md/discord/README.md) | 藍紫漸層、活潑標題與聊天介面，呈現社群氛圍。 | [設計規格](design-md/discord/DESIGN.md) · [AI 指令](design-md/discord/PROMPTS.md) |
| [Duolingo](design-md/duolingo/README.md) | 鮮綠按鈕、圓潤插畫與留白，讓學習入口輕鬆易懂。 | [設計規格](design-md/duolingo/DESIGN.md) · [AI 指令](design-md/duolingo/PROMPTS.md) |
| [Zoom](design-md/zoom/README.md) | 深藍漸層、大型標題與產品卡，傳達團隊協作的流暢感。 | [設計規格](design-md/zoom/DESIGN.md) · [AI 指令](design-md/zoom/PROMPTS.md) |
| [LinkedIn](design-md/linkedin/README.md) | 白底藍色操作與親切插畫，呈現職涯社群與主題探索。 | [設計規格](design-md/linkedin/DESIGN.md) · [AI 指令](design-md/linkedin/PROMPTS.md) |
| [Khan Academy](design-md/khan-academy/README.md) | 清楚的雙欄入口與角色選擇卡，讓不同學習需求容易開始。 | [設計規格](design-md/khan-academy/DESIGN.md) · [AI 指令](design-md/khan-academy/PROMPTS.md) |

### 設計與創作

| 設計 | 特色 | 檔案 |
| --- | --- | --- |
| [Airtable](design-md/airtable/README.md) | 彩色分區，把複雜資訊整理清楚。 | [設計規格](design-md/airtable/DESIGN.md) · [AI 指令](design-md/airtable/PROMPTS.md) |
| [Clay](design-md/clay/README.md) | 柔和暖色與不規則構圖，保留創作空間。 | [設計規格](design-md/clay/DESIGN.md) · [AI 指令](design-md/clay/PROMPTS.md) |
| [Figma](design-md/figma/README.md) | 大膽色塊、俐落黑線與充滿活力的構圖。 | [設計規格](design-md/figma/DESIGN.md) · [AI 指令](design-md/figma/PROMPTS.md) |
| [Framer](design-md/framer/README.md) | 深色展示舞台與電藍色，突出作品品質。 | [設計規格](design-md/framer/DESIGN.md) · [AI 指令](design-md/framer/PROMPTS.md) |
| [Miro](design-md/miro/README.md) | 明亮黃色與便箋色彩，讓協作空間有秩序。 | [設計規格](design-md/miro/DESIGN.md) · [AI 指令](design-md/miro/PROMPTS.md) |
| [Webflow](design-md/webflow/README.md) | 大膽黑白區塊與亮藍色，配合精準版面結構。 | [設計規格](design-md/webflow/DESIGN.md) · [AI 指令](design-md/webflow/PROMPTS.md) |
| [Adobe](design-md/adobe/README.md) | 深色主視覺與鮮明產品卡，呈現創意工具的多樣性。 | [設計規格](design-md/adobe/DESIGN.md) · [AI 指令](design-md/adobe/PROMPTS.md) |
| [Canva](design-md/canva/README.md) | 明亮漸層、置中標題與多彩圖形，帶出輕鬆創作感。 | [設計規格](design-md/canva/DESIGN.md) · [AI 指令](design-md/canva/PROMPTS.md) |

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
| [PayPal](design-md/paypal/README.md) | 清爽淺藍主視覺與黑色大標，突顯簡單直接的服務入口。 | [設計規格](design-md/paypal/DESIGN.md) · [AI 指令](design-md/paypal/PROMPTS.md) |

### 電商與零售

| 設計 | 特色 | 檔案 |
| --- | --- | --- |
| [Airbnb](design-md/airbnb/README.md) | 珊瑚紅與圓角，讓探索成為主角。 | [設計規格](design-md/airbnb/DESIGN.md) · [AI 指令](design-md/airbnb/PROMPTS.md) |
| [Meta](design-md/meta/README.md) | 大幅影像與藍色操作，建立明確產品層次。 | [設計規格](design-md/meta/DESIGN.md) · [AI 指令](design-md/meta/PROMPTS.md) |
| [Nike](design-md/nike/README.md) | 巨大標題、黑白對比與影像優先的編排。 | [設計規格](design-md/nike/DESIGN.md) · [AI 指令](design-md/nike/PROMPTS.md) |
| [Shopify](design-md/shopify/README.md) | 黑色與柔綠色面，讓商業展示保有呼吸感。 | [設計規格](design-md/shopify/DESIGN.md) · [AI 指令](design-md/shopify/PROMPTS.md) |
| [Starbucks](design-md/starbucks/README.md) | 深淺綠色、白底與交錯區塊，呈現親切日常感。 | [設計規格](design-md/starbucks/DESIGN.md) · [AI 指令](design-md/starbucks/PROMPTS.md) |
| [Amazon](design-md/amazon/README.md) | 深色搜尋導覽與豐富卡片，讓大量商品容易瀏覽。 | [設計規格](design-md/amazon/DESIGN.md) · [AI 指令](design-md/amazon/PROMPTS.md) |
| [IKEA](design-md/ikea/README.md) | 明亮留白、藍色重點與居家圖片磚，整理生活靈感。 | [設計規格](design-md/ikea/DESIGN.md) · [AI 指令](design-md/ikea/PROMPTS.md) |
| [Booking.com](design-md/booking/README.md) | 深藍主視覺與醒目搜尋列，讓旅行探索從目的地開始。 | [設計規格](design-md/booking/DESIGN.md) · [AI 指令](design-md/booking/PROMPTS.md) |
| [Etsy](design-md/etsy/README.md) | 暖白底、橘色搜尋與手作主題卡，讓商品探索更有溫度。 | [設計規格](design-md/etsy/DESIGN.md) · [AI 指令](design-md/etsy/PROMPTS.md) |

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
| [Google](design-md/google/README.md) | 深色留白與置中搜尋，讓主要操作一眼可見。 | [設計規格](design-md/google/DESIGN.md) · [AI 指令](design-md/google/PROMPTS.md) |
| [YouTube](design-md/youtube/README.md) | 深色影音介面，清楚排列搜尋、分類與內容卡片。 | [設計規格](design-md/youtube/DESIGN.md) · [AI 指令](design-md/youtube/PROMPTS.md) |
| [Netflix](design-md/netflix/README.md) | 深色電影感版面，搭配強烈紅色與大幅主視覺。 | [設計規格](design-md/netflix/DESIGN.md) · [AI 指令](design-md/netflix/PROMPTS.md) |
| [Microsoft](design-md/microsoft/README.md) | 乾淨的產品型錄，以藍色操作與寬幅圖文區塊引導。 | [設計規格](design-md/microsoft/DESIGN.md) · [AI 指令](design-md/microsoft/PROMPTS.md) |
| [Wikipedia](design-md/wikipedia/README.md) | 置中百科入口，對稱語言清單與簡潔搜尋。 | [設計規格](design-md/wikipedia/DESIGN.md) · [AI 指令](design-md/wikipedia/PROMPTS.md) |
| [BBC](design-md/bbc/README.md) | 黑白編輯網格與清晰標題，整理多層次的文章內容。 | [設計規格](design-md/bbc/DESIGN.md) · [AI 指令](design-md/bbc/PROMPTS.md) |
| [Twitch](design-md/twitch/README.md) | 深色介面搭配紫色重點，突出直播內容與頻道瀏覽。 | [設計規格](design-md/twitch/DESIGN.md) · [AI 指令](design-md/twitch/PROMPTS.md) |

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

</details>

## 參與貢獻

歡迎新增設計分析、修正資料或改善 AI 指令。請先閱讀 [CONTRIBUTING.md](CONTRIBUTING.md)，並附上來源與實際驗證結果。
