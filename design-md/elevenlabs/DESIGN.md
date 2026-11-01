---
version: zh-TW-2026-10-15
language: zh-TW
name: "ElevenLabs"
description: "乾淨石色、聲音波形與細膩的文字層次。"

colors:
  primary: "#292524"
  primary-active: "#0c0a09"
  ink: "#0c0a09"
  body: "#4e4e4e"
  body-strong: "#292524"
  muted: "#777169"
  muted-soft: "#a8a29e"
  hairline: "#e7e5e4"
  hairline-soft: "#f0efed"
  hairline-strong: "#d6d3d1"
  canvas: "#f5f5f5"
  canvas-soft: "#fafafa"
  canvas-deep: "#0c0a09"
  surface-card: "#ffffff"
  surface-strong: "#f0efed"
  surface-dark: "#0c0a09"
  surface-dark-elevated: "#1c1917"
  on-primary: "#ffffff"
  on-dark: "#ffffff"
  on-dark-soft: "#a8a29e"
  gradient-mint: "#a7e5d3"
  gradient-peach: "#f4c5a8"
  gradient-lavender: "#c8b8e0"
  gradient-sky: "#a8c8e8"
  gradient-rose: "#e8b8c4"
  semantic-error: "#dc2626"
  semantic-success: "#16a34a"

typography:
  display-mega:
    fontFamily: "'Waldenburg', 'Times New Roman', serif"
    fontSize: 64px
    fontWeight: 300
    lineHeight: 1.05
    letterSpacing: -1.92px
  display-xl:
    fontFamily: "'Waldenburg', serif"
    fontSize: 48px
    fontWeight: 300
    lineHeight: 1.08
    letterSpacing: -0.96px
  display-lg:
    fontFamily: "'Waldenburg', serif"
    fontSize: 36px
    fontWeight: 300
    lineHeight: 1.17
    letterSpacing: -0.36px
  display-md:
    fontFamily: "'Waldenburg', serif"
    fontSize: 32px
    fontWeight: 300
    lineHeight: 1.13
    letterSpacing: -0.32px
  display-sm:
    fontFamily: "'Waldenburg', serif"
    fontSize: 24px
    fontWeight: 300
    lineHeight: 1.2
    letterSpacing: 0
  title-md:
    fontFamily: "'Inter', sans-serif"
    fontSize: 20px
    fontWeight: 500
    lineHeight: 1.35
    letterSpacing: 0
  title-sm:
    fontFamily: "'Inter', sans-serif"
    fontSize: 18px
    fontWeight: 500
    lineHeight: 1.44
    letterSpacing: 0.18px
  body-md:
    fontFamily: "'Inter', sans-serif"
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: 0.16px
  body-strong:
    fontFamily: "'Inter', sans-serif"
    fontSize: 16px
    fontWeight: 500
    lineHeight: 1.5
    letterSpacing: 0.16px
  body-sm:
    fontFamily: "'Inter', sans-serif"
    fontSize: 15px
    fontWeight: 400
    lineHeight: 1.47
    letterSpacing: 0.15px
  caption:
    fontFamily: "'Inter', sans-serif"
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: 0
  caption-uppercase:
    fontFamily: "'Inter', sans-serif"
    fontSize: 12px
    fontWeight: 600
    lineHeight: 1.4
    letterSpacing: 0.96px
    textTransform: uppercase
  button:
    fontFamily: "'Inter', sans-serif"
    fontSize: 15px
    fontWeight: 500
    lineHeight: 1.0
    letterSpacing: 0
  nav-link:
    fontFamily: "'Inter', sans-serif"
    fontSize: 15px
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: 0

rounded:
  none: 0px
  xs: 4px
  sm: 6px
  md: 8px
  lg: 12px
  xl: 16px
  xxl: 24px
  pill: 9999px
  full: 9999px

spacing:
  xxs: 4px
  xs: 8px
  sm: 12px
  base: 16px
  md: 20px
  lg: 24px
  xl: 32px
  xxl: 48px
  section: 96px

components:
  top-nav:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.nav-link}"
    height: 64px
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.button}"
    rounded: "{rounded.pill}"
    padding: 10px 20px
    height: 40px
  button-primary-active:
    backgroundColor: "{colors.primary-active}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.pill}"
  button-outline:
    backgroundColor: transparent
    textColor: "{colors.ink}"
    typography: "{typography.button}"
    rounded: "{rounded.pill}"
    padding: 9px 19px
    height: 40px
  button-tertiary-text:
    backgroundColor: transparent
    textColor: "{colors.ink}"
    typography: "{typography.button}"
  hero-band:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.display-mega}"
    padding: 96px
  gradient-orb-card:
    backgroundColor: "{colors.canvas-soft}"
    textColor: "{colors.ink}"
    rounded: "{rounded.xxl}"
    padding: 32px
  feature-card:
    backgroundColor: "{colors.surface-card}"
    textColor: "{colors.ink}"
    typography: "{typography.title-md}"
    rounded: "{rounded.xl}"
    padding: 24px
  product-card-stack:
    backgroundColor: "{colors.surface-card}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.xl}"
    padding: 0
  voice-row:
    backgroundColor: transparent
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    padding: 12px 0
  voice-icon-circular:
    backgroundColor: "{colors.surface-strong}"
    rounded: "{rounded.full}"
    size: 32px
  pricing-tier-card:
    backgroundColor: "{colors.surface-card}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.xl}"
    padding: 32px
  pricing-tier-featured:
    backgroundColor: "{colors.surface-dark}"
    textColor: "{colors.on-dark}"
    typography: "{typography.body-md}"
    rounded: "{rounded.xl}"
    padding: 32px
  text-input:
    backgroundColor: "{colors.surface-card}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: 12px 16px
    height: 44px
  badge-pill:
    backgroundColor: "{colors.surface-strong}"
    textColor: "{colors.ink}"
    typography: "{typography.caption-uppercase}"
    rounded: "{rounded.pill}"
    padding: 4px 10px
  cta-band:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.display-lg}"
    padding: 96px
  testimonial-card:
    backgroundColor: "{colors.surface-card}"
    textColor: "{colors.body}"
    typography: "{typography.body-md}"
    rounded: "{rounded.xl}"
    padding: 32px
  audio-waveform-card:
    backgroundColor: "{colors.surface-card}"
    textColor: "{colors.ink}"
    rounded: "{rounded.xl}"
    padding: 24px
  footer:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.body}"
    typography: "{typography.body-sm}"
    padding: 64px 48px
  footer-link:
    backgroundColor: transparent
    textColor: "{colors.body}"
    typography: "{typography.body-sm}"
---

# ElevenLabs 延伸設計規格

語言：繁體中文（台灣用語，zh-TW）。在地化更新：2026-11-01。

## 來源與規格層次

這份規格將較早保存的品牌設計資料重新整理為可實作的繁體中文文件。來源設定中的色碼、字級、字重、行高、間距、圓角與元件識別字保留，供開發工具讀取；敘述與操作指令改用台灣用語。這些延伸設定不等同於目前日期限定首頁的逐項實測值，若兩者不同，依下方的日期限定觀察及對應預覽判讀。

- 原始資料版本：`1a783491c9539c3153c2fc96c16d59131e024f4e`。
- 原始 DESIGN.md 摘要：`f49ae1dae448f75a2c3129e93e5dfe19e4a437ff2c876cb8bb60f2917d163fc1`。
- 目前首頁參考日期：2026-10-10。
- 目前公開來源：https://elevenlabs.io/。
- 目前預覽：`official-drafts/elevenlabs.html`。
- 台灣繁體中文規格與指令是本次重新產出的內容；來源截圖及原生生成紀錄保留原貌。

## 整體視覺方向

乾淨石色、聲音波形與細膩的文字層次。

製作音訊專案工作區，包含逐字稿、聲音選擇與精簡的波形播放器。版面明亮、操作清楚；播放、暫停、已播放時間與文字狀態都必須可辨識，不只依賴動畫。

先建立主要內容、輔助資訊與操作之間的層級，再套用色彩及裝飾。品牌色應有明確用途；主要操作、選取、錯誤及停用狀態要能分辨。避免將多套參考風格混在同一頁，也不要僅替換通用卡片的顏色。

## 色彩、字型與繁體中文排版

上方來源設定保留原始色彩角色與數值。主要品牌色用於最重要的操作；背景、內容表面、主要文字、次要文字與分隔線各自維持一致用途。資訊不能只依賴顏色，狀態須同時有文字或圖示標示。

原字型名稱可作為拉丁字母參考。繁體中文字型優先使用可取得的 `Noto Sans TC`、`PingFang TC`、`Microsoft JhengHei`，最後才使用 `sans-serif`。原字型未涵蓋中文時必須提供替代，不以缺字或圖片文字呈現正文。專有字型無法取得時，記錄替代字型與可能的字寬差異。

中文標題以語意分段，避免為模仿英文大寫字距而拉散中文字。內文行高、欄寬與段落間距以可讀性為準；英文型號、網址、程式碼及長連結可以換行或在自己的區域捲動，不可撐開整份文件。價格、規格及比較欄位保持數字與單位對齊。

| 字級 | 字重 | 行高 | 字距 |
| --- | --- | --- | --- |
| 64px | 300 | 1.05 | -1.92px |
| 48px | 300 | 1.08 | -0.96px |
| 36px | 300 | 1.17 | -0.36px |
| 32px | 300 | 1.13 | -0.32px |
| 24px | 300 | 1.2 | 0 |
| 20px | 500 | 1.35 | 0 |
| 18px | 500 | 1.44 | 0.18px |
| 16px | 400 | 1.5 | 0.16px |
| 16px | 500 | 1.5 | 0.16px |
| 15px | 400 | 1.47 | 0.15px |
| 14px | 400 | 1.5 | 0 |
| 12px | 600 | 1.4 | 0.96px |
| 15px | 500 | 1.0 | 0 |
| 15px | 500 | 1.4 | 0 |

## 版面與元件結構

此參考可先實作：音訊預覽卡片，包含播放控制項與可展開的逐字稿。

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

- `#f5f5f5`
- `#292524`
- `0 4px 16px rgba(0, 0, 0, 0.04)`

## 日期限定首頁觀察

來源：https://elevenlabs.io/。原始取樣時間保留於 UTC 紀錄，oct10 工作檔名不表示所有檢查都在 10 月 10 日完成。

現行首頁為白／灰白、細格線與小交點，搭配精簡黑字、按鈕及淺色圓角卡。Elevenv4 公告下方主標「讓科技融入生活」，首屏 Creative／Agents／API 展示含彩色球體、語音範例、播放控制與產品分頁。

下方保留 ElevenCreative／ElevenAgents、創作編輯與 Music／SFX／Voices／Image & Video、代理程式的全通路／分析／測試／防護／工作流、三種 API 程式碼、影響力、研究時間線至 Elevenv4／Dubbingv2／Musicv2、安全三卡、Flows／Government／Expressive Mode 更新及完整頁尾。

已新送原生 Stitch，再依目前來源圖片、CSSOM 與完整內容校正。390px 原站有水平溢位與橫向卡列，不能把來源本身標成無溢位；音訊、API 與研究動態並未呼叫外部付費服務來假裝可用。

保留原有 DESIGN.md、PROMPTS.md、STITCH-PROMPT.md；本檔為目前官網的日期限定補充。研究頁免費瀏覽、無付費執行時依賴，未執行購買或訂閱。

驗證範圍為匿名公開首頁、1280×720 與 390×844、DPR 1、桌面 UA。實體手機、其他地區、完整互動與部署尚未驗證；accepted=false，不宣稱與官方一致。

## 已知差異與驗證範圍

- 官網窄版截圖本身有文件溢位；水平卡片列及溢位原因須依實際影像判讀，不可自動宣稱完全沒有溢位。
- 音訊播放與合成、Creative／Agents／API 分頁、研究畫布、精確時間階段及註冊、API 服務尚未驗證。
- 官網與本機窄版皆因卡片及程式碼列產生水平溢位，不宣稱零溢位。
- 安全性雕塑、文字與動態圖像的時間階段有些微差異；音訊合成與播放、分頁、導覽、輪播及服務尚未驗證。
- 原始比對未涵蓋其他寬度、實體裝置、地區、完整互動及動態，以及正式部署。

以上限制沿用原參考日期的比對紀錄。本次繁體中文整理不會把未驗證的影片、動畫、服務或尺寸改標為已通過；目前預覽仍未宣稱與官方完全一致。
<!-- Original AI instructions: awesome-ai-web-design -->

## 來源與使用範圍

資料來源與適用授權集中於專案根目錄的 ATTRIBUTION.md 與 LICENSE。品牌名稱僅用於識別參考來源，並非官方授權或服務。下方 AI 指令由本專案獨立撰寫；若既有互動備註與無障礙要求衝突，以此處的可用性檢查為準。

## 重新撰寫的 AI 任務指令

語言：繁體中文（台灣用語，zh-TW）。將 DESIGN.md 放入專案，再選擇下方任務。這些指令由本專案重新撰寫；請把示範內容替換為自己的產品需求。

## 建立新頁面

```text
先閱讀隨附的 DESIGN.md，以 ElevenLabs 的設計語言作為介面參考。請完成以下可操作頁面：製作音訊專案工作區，包含逐字稿、聲音選擇與精簡的波形播放器。版面明亮、操作清楚；播放、暫停、已播放時間與文字狀態都必須可辨識，不只依賴動畫。

使用我的產品名稱、內容與資料格式，優先沿用專案現有元件及技術。開始製作樣式前，先將色彩、字體、間距與圓角整理為可重複使用的設計變數。指定字型無法取得時，使用可用的系統字型或開源字型，並說明替代方式。介面文案、按鈕、提示、錯誤訊息、圖片替代文字、註解與交付說明，一律使用繁體中文（台灣用語）。使用「專案、元件、資料、建立、預設、載入、登入、連結、儲存、影片」等台灣用語。保留品牌名稱、檔名、網址、API 識別字與可執行程式碼；HTML 語言設為 zh-Hant-TW。

讓互動元件可實際操作，並將狀態提供給輔助科技。具備可見的鍵盤焦點、清楚的欄位標示、減少動態效果，以及至少 44px 的觸控區域。參考視覺與可用性衝突時，作最小幅度的無障礙調整並記錄原因。在 390px、768px、1440px 寬度檢查版面，涵蓋繁體中文長標題、長內容、空白及錯誤狀態。金額、數量與日期依資料本身的幣別、單位及時區呈現，以 zh-TW 格式顯示，不擅自換算。最後交付完成的檔案、實際驗證結果與仍待確認的假設，不把未檢查項目宣稱為通過。
```

## 製作元件

```text
先閱讀隨附的 DESIGN.md，以 ElevenLabs 的設計語言作為介面參考。請製作音訊預覽卡片，包含播放控制項與可展開的逐字稿。沿用現有元件慣例，放入精簡且符合實際情境的範例。比例與資訊層級應來自參考規格，不能只替通用卡片換色。依需求支援預設、焦點、停用、載入與錯誤狀態。使用有意義的示範資料，讓每個可見操作都有明確結果。

使用我的產品名稱、內容與資料格式，優先沿用專案現有元件及技術。開始製作樣式前，先將色彩、字體、間距與圓角整理為可重複使用的設計變數。指定字型無法取得時，使用可用的系統字型或開源字型，並說明替代方式。介面文案、按鈕、提示、錯誤訊息、圖片替代文字、註解與交付說明，一律使用繁體中文（台灣用語）。使用「專案、元件、資料、建立、預設、載入、登入、連結、儲存、影片」等台灣用語。保留品牌名稱、檔名、網址、API 識別字與可執行程式碼；HTML 語言設為 zh-Hant-TW。

讓互動元件可實際操作，並將狀態提供給輔助科技。具備可見的鍵盤焦點、清楚的欄位標示、減少動態效果，以及至少 44px 的觸控區域。參考視覺與可用性衝突時，作最小幅度的無障礙調整並記錄原因。在 390px、768px、1440px 寬度檢查版面，涵蓋繁體中文長標題、長內容、空白及錯誤狀態。金額、數量與日期依資料本身的幣別、單位及時區呈現，以 zh-TW 格式顯示，不擅自換算。最後交付完成的檔案、實際驗證結果與仍待確認的假設，不把未檢查項目宣稱為通過。
```

## 改造既有介面

```text
先閱讀隨附的 DESIGN.md，以 ElevenLabs 的設計語言作為介面參考。重新設計選定頁面，同時保留路由、資料、行為與使用者可理解的意義。先確認頁面層級，再找出最少且可重複使用的設計變數與元件調整。以下構圖作為視覺方向，依現有頁面調整：製作音訊專案工作區，包含逐字稿、聲音選擇與精簡的波形播放器。版面明亮、操作清楚；播放、暫停、已播放時間與文字狀態都必須可辨識，不只依賴動畫。

使用我的產品名稱、內容與資料格式，優先沿用專案現有元件及技術。開始製作樣式前，先將色彩、字體、間距與圓角整理為可重複使用的設計變數。指定字型無法取得時，使用可用的系統字型或開源字型，並說明替代方式。介面文案、按鈕、提示、錯誤訊息、圖片替代文字、註解與交付說明，一律使用繁體中文（台灣用語）。使用「專案、元件、資料、建立、預設、載入、登入、連結、儲存、影片」等台灣用語。保留品牌名稱、檔名、網址、API 識別字與可執行程式碼；HTML 語言設為 zh-Hant-TW。依完整元件群組套用變更，檢查其他頁面是否受影響，並說明調整前後的主要差異。

讓互動元件可實際操作，並將狀態提供給輔助科技。具備可見的鍵盤焦點、清楚的欄位標示、減少動態效果，以及至少 44px 的觸控區域。參考視覺與可用性衝突時，作最小幅度的無障礙調整並記錄原因。在 390px、768px、1440px 寬度檢查版面，涵蓋繁體中文長標題、長內容、空白及錯誤狀態。金額、數量與日期依資料本身的幣別、單位及時區呈現，以 zh-TW 格式顯示，不擅自換算。最後交付完成的檔案、實際驗證結果與仍待確認的假設，不把未檢查項目宣稱為通過。
```

## 逐次調整流程

1. 先指出一個可實際觀察的問題，例如層級不清或內容遭裁切。
2. 在 DESIGN.md 找到對應設計變數或元件規則，提出範圍明確的調整。
3. 套用調整，保留無關的路由與資料行為。
4. 檢查鍵盤焦點、窄版排版，以及代表性的內容與錯誤狀態。
5. 用繁體中文說明結果，以及刻意偏離參考外觀的原因。
