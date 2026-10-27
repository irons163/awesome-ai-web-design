# 來源、致謝與改寫說明

本專案為獨立的免費設計參考集，設計分析改寫自 **VoltAgent/awesome-design-md**。

- 上游專案：https://github.com/VoltAgent/awesome-design-md
- 匯入版本：`f6961238d5cddcf8042a74a70fc400ec67181abb`
- 匯入日期：2026-09-22。
- 原始著作權：Copyright (c) 2026 VoltAgent。
- 授權：MIT；原始授權與著作權聲明完整保留於 [LICENSE](LICENSE)。
- 上游檔案路徑與 SHA-256 保留於原始碼的 `data/upstream.json`。

## 本次繁體中文整理

74 份延伸設計規格、222 則任務指令、日期限定的主要規格與指令、介面文案及已知差異，於 2026-10-20 重新產出為繁體中文（台灣用語）。原先上游的代理提示及逐次調整章節，由本專案獨立撰寫的任務指令取代；不把上游設計資料宣稱為本專案原創。

目錄介面、中文摘要、AI 指令、通用工作流程、預覽整合、建置程式、說明及測試，由 Awesome AI Web Design 貢獻者製作，同樣採 MIT 授權。延伸規格保留來源設定中的技術值；目前首頁研究另依各品牌參考日期及範圍判讀，兩者不混作同一天的實際量測。

## 預覽與原始生成紀錄

Google Stitch 原始預覽來自實際 MCP 生成；各 `STITCH.json` 記錄專案、畫面識別字及未修改匯出的檔案雜湊。原始 `STITCH-PROMPT.md` 保留當時送出的指令；重新撰寫的 `STITCH-PROMPT.zh-TW.md` 是中文生成參考，沒有宣稱已再次送交生成服務。

網站主要預覽則依保存的公開官網資料、DOM、樣式、字型、圖片與影片校正，與原生生成稿分開保存。本次文字在地化沒有改寫原始預覽、截圖或媒體，也不把生成服務的精確度宣稱當成視覺驗證。

原始完整改寫歷程可由版本 `1a783491c9539c3153c2fc96c16d59131e024f4e` 的來源紀錄溯源；目前每頁的日期、預覽摘要與限制則以 [全部參考紀錄](official-progress.html) 為準。曾出現的生成錯誤、下載失敗、行動版請求回傳桌面稿、影片與動畫差異，仍保留在來源紀錄，不因中文整理而改標為驗收通過。

## 品牌與第三方素材

品牌名稱、商標、字型、圖片及影片屬各自權利人。這些參考素材不因本專案的程式與文字採 MIT 授權，就一併成為 MIT 授權素材。個別素材保留來源網址、檔案大小及 SHA-256；資料包中的 Markdown 用於說明設計，不包含完整官網媒體或品牌服務。

部分預覽使用固定版本 hls.js 1.7.3 精簡播放器，採 Apache-2.0 授權；套件授權及完整性紀錄隨原始資源保留。原始網站連結、外部服務及受原權利人管理的內容，維持各自目的地。

## 74 份日期限定研究的來源

以下日期是既有公開首頁觀察日期，不是本次中文整理時重新檢查官網的日期。每頁限制說明以繁體中文提供；實際比較只涵蓋原紀錄的尺寸與狀態，未宣稱完整互動、所有裝置或品牌後端服務一致。

| 品牌 | 參考日期 | 來源與範圍 |
| --- | --- | --- |
| Airbnb | 2026-10-10 | [公開來源](https://www.airbnb.ca/?locale=en) · [比對紀錄](official-progress.html#airbnb) |
| Airtable | 2026-10-10 | [公開來源](https://www.airtable.com/) · [比對紀錄](official-progress.html#airtable) |
| Apple | 2026-10-10 | [公開來源](https://www.apple.com/) · [比對紀錄](official-progress.html#apple) |
| Binance | 2026-10-11 | [公開來源](https://www.binance.com/en) · [比對紀錄](official-progress.html#binance) |
| BMW | 2026-10-10 | [公開來源](https://www.bmw.com.tw/zh/index.html) · [比對紀錄](official-progress.html#bmw) |
| BMW M | 2026-10-10 | [公開來源](https://www.bmw-m.com/en/index.html) · [比對紀錄](official-progress.html#bmw-m) |
| Bugatti | 2026-10-11 | [公開來源](https://www.bugatti.com/) · [比對紀錄](official-progress.html#bugatti) |
| Cal.com | 2026-10-10 | [公開來源](https://cal.com/) · [比對紀錄](official-progress.html#cal) |
| Claude | 2026-10-12 | [公開來源](https://claude.com/index.html) · [比對紀錄](official-progress.html#claude) |
| Clay | 2026-10-10 | [公開來源](https://clay.global/) · [比對紀錄](official-progress.html#clay) |
| ClickHouse | 2026-10-11 | [公開來源](https://clickhouse.com/) · [比對紀錄](official-progress.html#clickhouse) |
| Cohere | 2026-10-10 | [公開來源](https://cohere.com/) · [比對紀錄](official-progress.html#cohere) |
| Coinbase | 2026-10-10 | [公開來源](https://www.coinbase.com/en-ca) · [比對紀錄](official-progress.html#coinbase) |
| Composio | 2026-10-10 | [公開來源](https://composio.dev/) · [比對紀錄](official-progress.html#composio) |
| Cursor | 2026-10-10 | [公開來源](https://cursor.com/) · [比對紀錄](official-progress.html#cursor) |
| Dell (1996) | 2026-10-13 | [公開來源](https://www.dell.com/zh-tw) · [比對紀錄](official-progress.html#dell-1996) |
| ElevenLabs | 2026-10-10 | [公開來源](https://elevenlabs.io/) · [比對紀錄](official-progress.html#elevenlabs) |
| Expo | 2026-10-10 | [公開來源](https://expo.dev/) · [比對紀錄](official-progress.html#expo) |
| Ferrari | 2026-10-11 | [公開來源](https://www.ferrari.com/en-US) · [比對紀錄](official-progress.html#ferrari) |
| Figma | 2026-10-12 | [公開來源](https://www.figma.com/) · [比對紀錄](official-progress.html#figma) |
| Framer | 2026-10-12 | [公開來源](https://www.framer.com/) · [比對紀錄](official-progress.html#framer) |
| HashiCorp | 2026-10-11 | [公開來源](https://www.hashicorp.com/en) · [比對紀錄](official-progress.html#hashicorp) |
| HP | 2026-10-11 | [公開來源](https://www.hp.com/ca-en/home.html) · [比對紀錄](official-progress.html#hp) |
| IBM | 2026-10-10 | [公開來源](https://www.ibm.com/ca-en) · [比對紀錄](official-progress.html#ibm) |
| Intercom | 2026-10-10 | [公開來源](https://www.intercom.com/) · [比對紀錄](official-progress.html#intercom) |
| Kraken | 2026-10-10 | [公開來源](https://www.kraken.com/ca) · [比對紀錄](official-progress.html#kraken) |
| Lamborghini | 2026-10-11 | [公開來源](https://www.lamborghini.com/en-en) · [比對紀錄](official-progress.html#lamborghini) |
| Linear | 2026-10-12 | [公開來源](https://linear.app/) · [比對紀錄](official-progress.html#linear.app) |
| Lovable | 2026-10-11 | [公開來源](https://lovable.dev/) · [比對紀錄](official-progress.html#lovable) |
| Mastercard | 2026-10-11 | [公開來源](https://www.mastercard.com/tw/zh.html) · [比對紀錄](official-progress.html#mastercard) |
| Meta | 2026-10-11 | [公開來源](https://www.meta.com/ca/) · [比對紀錄](official-progress.html#meta) |
| MiniMax | 2026-10-11 | [公開來源](https://www.minimax.io/) · [比對紀錄](official-progress.html#minimax) |
| Mintlify | 2026-10-10 | [公開來源](https://www.mintlify.com/) · [比對紀錄](official-progress.html#mintlify) |
| Miro | 2026-10-10 | [公開來源](https://miro.com/) · [比對紀錄](official-progress.html#miro) |
| Mistral AI | 2026-10-10 | [公開來源](https://mistral.ai/) · [比對紀錄](official-progress.html#mistral.ai) |
| MongoDB | 2026-10-10 | [公開來源](https://www.mongodb.com/zh-tw) · [比對紀錄](official-progress.html#mongodb) |
| Nike | 2026-10-11 | [公開來源](https://www.nike.com/ca/) · [比對紀錄](official-progress.html#nike) |
| Nintendo (2001) | 2026-10-13 | [公開來源](https://www.nintendo.com/en-ca/) · [比對紀錄](official-progress.html#nintendo-2001) |
| Notion | 2026-10-12 | [公開來源](https://www.notion.com/) · [比對紀錄](official-progress.html#notion) |
| NVIDIA | 2026-10-11 | [公開來源](https://www.nvidia.com/en-us/) · [比對紀錄](official-progress.html#nvidia) |
| Ollama | 2026-10-11 | [公開來源](https://ollama.com/) · [比對紀錄](official-progress.html#ollama) |
| OpenCode | 2026-10-10 | [公開來源](https://opencode.ai/) · [比對紀錄](official-progress.html#opencode.ai) |
| Pinterest | 2026-10-13 | [公開來源](https://www.pinterest.com/) · [比對紀錄](official-progress.html#pinterest) |
| PlayStation | 2026-10-11 | [公開來源](https://www.playstation.com/fr-ca/) · [比對紀錄](official-progress.html#playstation) |
| PostHog | 2026-10-10 | [公開來源](https://posthog.com/) · [比對紀錄](official-progress.html#posthog) |
| Raycast | 2026-10-12 | [公開來源](https://www.raycast.com/) · [比對紀錄](official-progress.html#raycast) |
| Renault | 2026-10-11 | [公開來源](https://www.renaultgroup.com/) · [比對紀錄](official-progress.html#renault) |
| Replicate | 2026-10-10 | [公開來源](https://replicate.com/) · [比對紀錄](official-progress.html#replicate) |
| Resend | 2026-10-12 | [公開來源](https://resend.com/) · [比對紀錄](official-progress.html#resend) |
| Revolut | 2026-10-11 | [公開來源](https://www.revolut.com/) · [比對紀錄](official-progress.html#revolut) |
| Runway | 2026-10-11 | [公開來源](https://runway.com/) · [比對紀錄](official-progress.html#runwayml) |
| Sanity | 2026-10-11 | [公開來源](https://www.sanity.io/) · [比對紀錄](official-progress.html#sanity) |
| Sentry | 2026-10-11 | [公開來源](https://sentry.io/welcome/) · [比對紀錄](official-progress.html#sentry) |
| Shopify | 2026-10-10 | [公開來源](https://www.shopify.com/ca) · [比對紀錄](official-progress.html#shopify) |
| Slack | 2026-10-11 | [公開來源](https://slack.com/) · [比對紀錄](official-progress.html#slack) |
| SpaceX | 2026-10-11 | [公開來源](https://www.spacex.com/) · [比對紀錄](official-progress.html#spacex) |
| Spotify | 2026-10-12 | [公開來源](https://open.spotify.com/) · [比對紀錄](official-progress.html#spotify) |
| Starbucks | 2026-10-10 | [公開來源](https://www.starbucks.com/) · [比對紀錄](official-progress.html#starbucks) |
| Stripe | 2026-10-10 | [公開來源](https://stripe.com/en-ca) · [比對紀錄](official-progress.html#stripe) |
| Supabase | 2026-10-12 | [公開來源](https://supabase.com/) · [比對紀錄](official-progress.html#supabase) |
| Superhuman | 2026-10-10 | [公開來源](https://superhuman.com/) · [比對紀錄](official-progress.html#superhuman) |
| Tesla | 2026-10-10 | [公開來源](https://www.tesla.com/) · [比對紀錄](official-progress.html#tesla) |
| The Verge | 2026-10-13 | [公開來源](https://www.theverge.com/) · [比對紀錄](official-progress.html#theverge) |
| Together AI | 2026-10-10 | [公開來源](https://www.together.ai/) · [比對紀錄](official-progress.html#together.ai) |
| Uber | 2026-10-11 | [公開來源](https://www.uber.com/ca/en/) · [比對紀錄](official-progress.html#uber) |
| Vercel | 2026-10-12 | [公開來源](https://vercel.com/) · [比對紀錄](official-progress.html#vercel) |
| Vodafone | 2026-10-13 | [公開來源](https://www.vodafone.com/) · [比對紀錄](official-progress.html#vodafone) |
| VoltAgent | 2026-10-11 | [公開來源](https://voltagent.dev/) · [比對紀錄](official-progress.html#voltagent) |
| Warp | 2026-10-12 | [公開來源](https://www.warp.dev/) · [比對紀錄](official-progress.html#warp) |
| Webflow | 2026-10-11 | [公開來源](https://webflow.com/) · [比對紀錄](official-progress.html#webflow) |
| WIRED | 2026-10-13 | [公開來源](https://www.wired.com/) · [比對紀錄](official-progress.html#wired) |
| Wise | 2026-10-11 | [公開來源](https://wise.com/) · [比對紀錄](official-progress.html#wise) |
| xAI | 2026-10-11 | [公開來源](https://x.ai/) · [比對紀錄](official-progress.html#x.ai) |
| Zapier | 2026-10-11 | [公開來源](https://zapier.com/) · [比對紀錄](official-progress.html#zapier) |
