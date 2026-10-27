---
version: zh-TW-2026-10-15
language: zh-TW
name: "Shopify"
description: "黑色與柔綠色面，讓商業展示保有呼吸感。"

colors:
  primary: "#000000"
  ink: "#000000"
  on-primary: "#ffffff"
  on-dark: "#ffffff"
  canvas-night: "#000000"
  canvas-night-elevated: "#0a0a0a"
  canvas-light: "#ffffff"
  canvas-cream: "#fbfbf5"
  surface-elevated-dark: "#1e2c31"
  shade-30: "#d4d4d8"
  shade-40: "#a1a1aa"
  shade-50: "#71717a"
  shade-60: "#52525b"
  shade-70: "#3f3f46"
  hairline-light: "#e4e4e7"
  hairline-dark: "#1e2c31"
  aloe-10: "#c1fbd4"
  pistachio-10: "#d4f9e0"
  link-cool-1: "#9dabad"
  link-cool-2: "#9797a2"
  link-cool-3: "#bdbdca"
  link-mint: "#99b3ad"

typography:
  display-xxl:
    fontFamily: "NeueHaasGrotesk Display, Helvetica, Arial, sans-serif"
    fontSize: 96px
    fontWeight: 330
    lineHeight: 1.0
    letterSpacing: 2.4px
    fontFeature: ss03
  display-xl:
    fontFamily: "NeueHaasGrotesk Display, Helvetica, Arial, sans-serif"
    fontSize: 70px
    fontWeight: 330
    lineHeight: 1.0
    letterSpacing: 0
    fontFeature: ss03
  display-lg:
    fontFamily: "NeueHaasGrotesk Display, Helvetica, Arial, sans-serif"
    fontSize: 55px
    fontWeight: 330
    lineHeight: 1.16
    letterSpacing: 0
    fontFeature: ss03
  display-md:
    fontFamily: "NeueHaasGrotesk Display, Helvetica, Arial, sans-serif"
    fontSize: 48px
    fontWeight: 330
    lineHeight: 1.14
    letterSpacing: 0
    fontFeature: ss03
  heading-xl:
    fontFamily: "NeueHaasGrotesk Display, Helvetica, Arial, sans-serif"
    fontSize: 28px
    fontWeight: 500
    lineHeight: 1.28
    letterSpacing: 0.42px
    fontFeature: ss03
  heading-lg:
    fontFamily: "NeueHaasGrotesk Display, Helvetica, Arial, sans-serif"
    fontSize: 24px
    fontWeight: 400
    lineHeight: 1.14
    letterSpacing: 0.36px
    fontFeature: ss03
  heading-md:
    fontFamily: "NeueHaasGrotesk Display, Helvetica, Arial, sans-serif"
    fontSize: 20px
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: 0.3px
    fontFeature: ss03
  heading-sm:
    fontFamily: "NeueHaasGrotesk Display, Helvetica, Arial, sans-serif"
    fontSize: 18px
    fontWeight: 500
    lineHeight: 1.25
    letterSpacing: 0.72px
    fontFeature: ss03
  body-lg:
    fontFamily: "Inter Variable, Inter, Helvetica, Arial, sans-serif"
    fontSize: 18px
    fontWeight: 550
    lineHeight: 1.56
    letterSpacing: 0
    fontFeature: ss03
  body-md:
    fontFamily: "Inter Variable, Inter, Helvetica, Arial, sans-serif"
    fontSize: 16px
    fontWeight: 420
    lineHeight: 1.5
    letterSpacing: 0
    fontFeature: ss03
  body-strong:
    fontFamily: "Inter Variable, Inter, Helvetica, Arial, sans-serif"
    fontSize: 16px
    fontWeight: 550
    lineHeight: 1.5
    letterSpacing: 0
    fontFeature: ss03
  caption:
    fontFamily: "Inter Variable, Inter, Helvetica, Arial, sans-serif"
    fontSize: 14px
    fontWeight: 500
    lineHeight: 1.49
    letterSpacing: 0.28px
    fontFeature: ss03
  micro:
    fontFamily: "Inter Variable, Inter, Helvetica, Arial, sans-serif"
    fontSize: 13px
    fontWeight: 500
    lineHeight: 1.5
    letterSpacing: -0.13px
    fontFeature: ss03
  eyebrow-cap:
    fontFamily: "Inter Variable, Inter, Helvetica, Arial, sans-serif"
    fontSize: 12px
    fontWeight: 400
    lineHeight: 1.2
    letterSpacing: 0.72px
    fontFeature: ss03
  code:
    fontFamily: "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace"
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: 0
    fontFeature: ss03

rounded:
  xs: 4px
  sm: 5px
  md: 8px
  lg: 12px
  xl: 20px
  pill: 9999px

spacing:
  xxs: 2px
  xs: 4px
  sm: 8px
  md: 12px
  lg: 16px
  xl: 24px
  xxl: 32px
  huge: 64px

components:
  button-primary-pill:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.body-md}"
    rounded: "{rounded.pill}"
    padding: 12px 24px
  button-primary-pill-pressed:
    backgroundColor: "{colors.shade-70}"
    textColor: "{colors.on-primary}"
    typography: "{typography.body-md}"
    rounded: "{rounded.pill}"
    padding: 12px 24px
  button-outline-on-dark:
    backgroundColor: "{colors.canvas-night}"
    textColor: "{colors.on-primary}"
    typography: "{typography.body-md}"
    rounded: "{rounded.pill}"
    padding: 12px 26px
  button-outline-on-light:
    backgroundColor: "{colors.canvas-light}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.pill}"
    padding: 12px 24px
  button-aloe-pill:
    backgroundColor: "{colors.aloe-10}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.pill}"
    padding: 12px 24px
  text-input:
    backgroundColor: "{colors.canvas-light}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: 10px 12px
  card-pricing:
    backgroundColor: "{colors.canvas-light}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.lg}"
    padding: 32px
  card-pricing-featured:
    backgroundColor: "{colors.aloe-10}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.lg}"
    padding: 32px
  card-feature-cinematic:
    backgroundColor: "{colors.canvas-night-elevated}"
    textColor: "{colors.on-primary}"
    typography: "{typography.body-lg}"
    rounded: "{rounded.lg}"
    padding: 32px
  card-pistachio-band:
    backgroundColor: "{colors.pistachio-10}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.lg}"
    padding: 32px
  card-photo-frame:
    backgroundColor: "{colors.canvas-night}"
    textColor: "{colors.on-primary}"
    typography: "{typography.body-md}"
    rounded: "{rounded.xl}"
    padding: 0px
  pill-tag-mint:
    backgroundColor: "{colors.aloe-10}"
    textColor: "{colors.ink}"
    typography: "{typography.eyebrow-cap}"
    rounded: "{rounded.pill}"
    padding: 4px 12px
  pill-tag-shade:
    backgroundColor: "{colors.shade-30}"
    textColor: "{colors.ink}"
    typography: "{typography.eyebrow-cap}"
    rounded: "{rounded.pill}"
    padding: 4px 12px
  nav-bar-light:
    backgroundColor: "{colors.canvas-light}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.xs}"
    padding: 16px 24px
  nav-bar-dark:
    backgroundColor: "{colors.canvas-night}"
    textColor: "{colors.on-primary}"
    typography: "{typography.body-md}"
    rounded: "{rounded.xs}"
    padding: 16px 24px
  link-on-dark:
    backgroundColor: "{colors.canvas-night}"
    textColor: "{colors.on-primary}"
    typography: "{typography.body-md}"
    rounded: "{rounded.xs}"
    padding: 0px
  footer-dark:
    backgroundColor: "{colors.canvas-night}"
    textColor: "{colors.on-primary}"
    typography: "{typography.caption}"
    rounded: "{rounded.xs}"
    padding: 64px 24px
  footer-light:
    backgroundColor: "{colors.canvas-light}"
    textColor: "{colors.ink}"
    typography: "{typography.caption}"
    rounded: "{rounded.xs}"
    padding: 64px 24px
---

# Shopify 延伸設計規格

語言：繁體中文（台灣用語，zh-TW）。在地化更新：2026-10-20。

## 來源與規格層次

這份規格將較早保存的品牌設計資料重新整理為可實作的繁體中文文件。來源設定中的色碼、字級、字重、行高、間距、圓角與元件識別字保留，供開發工具讀取；敘述與操作指令改用台灣用語。這些延伸設定不等同於目前日期限定首頁的逐項實測值，若兩者不同，依下方的日期限定觀察及對應預覽判讀。

- 原始資料版本：`1a783491c9539c3153c2fc96c16d59131e024f4e`。
- 原始 DESIGN.md 摘要：`773cf7d74a51b48c6ebcf23f4968c236649be21033d351c59d969f0f288c100d`。
- 目前首頁參考日期：2026-10-10。
- 目前公開來源：https://www.shopify.com/ca。
- 目前預覽：`official-drafts/shopify.html`。
- 台灣繁體中文規格與指令是本次重新產出的內容；來源截圖及原生生成紀錄保留原貌。

## 整體視覺方向

黑色與柔綠色面，讓商業展示保有呼吸感。

製作商店工具總覽，包含深色介紹、簡潔商家案例與商品管理預覽。使用輕字重的大標題並節制運用綠色，以清楚標示的示範商品呈現實用操作。

先建立主要內容、輔助資訊與操作之間的層級，再套用色彩及裝飾。品牌色應有明確用途；主要操作、選取、錯誤及停用狀態要能分辨。避免將多套參考風格混在同一頁，也不要僅替換通用卡片的顏色。

## 色彩、字型與繁體中文排版

上方來源設定保留原始色彩角色與數值。主要品牌色用於最重要的操作；背景、內容表面、主要文字、次要文字與分隔線各自維持一致用途。資訊不能只依賴顏色，狀態須同時有文字或圖示標示。

原字型名稱可作為拉丁字母參考。繁體中文字型優先使用可取得的 `Noto Sans TC`、`PingFang TC`、`Microsoft JhengHei`，最後才使用 `sans-serif`。原字型未涵蓋中文時必須提供替代，不以缺字或圖片文字呈現正文。專有字型無法取得時，記錄替代字型與可能的字寬差異。

中文標題以語意分段，避免為模仿英文大寫字距而拉散中文字。內文行高、欄寬與段落間距以可讀性為準；英文型號、網址、程式碼及長連結可以換行或在自己的區域捲動，不可撐開整份文件。價格、規格及比較欄位保持數字與單位對齊。

| 字級 | 字重 | 行高 | 字距 |
| --- | --- | --- | --- |
| 96px | 330 | 1.0 | 2.4px |
| 70px | 330 | 1.0 | 0 |
| 55px | 330 | 1.16 | 0 |
| 48px | 330 | 1.14 | 0 |
| 28px | 500 | 1.28 | 0.42px |
| 24px | 400 | 1.14 | 0.36px |
| 20px | 500 | 1.4 | 0.3px |
| 18px | 500 | 1.25 | 0.72px |
| 18px | 550 | 1.56 | 0 |
| 16px | 420 | 1.5 | 0 |
| 16px | 550 | 1.5 | 0 |
| 14px | 500 | 1.49 | 0.28px |
| 13px | 500 | 1.5 | -0.13px |
| 12px | 400 | 1.2 | 0.72px |
| 16px | 400 | 1.5 | 0 |

## 版面與元件結構

此參考可先實作：商品管理卡片，包含庫存狀態與可編輯的發布狀態。

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

- `#000000`
- `#c1fbd4`
- `#d4f9e0`
- `#9dabad`
- `#9797a2`
- `#bdbdca`
- `#99b3ad`
- `#0a0a0a`
- `#1e2c31`
- `#ffffff`
- `#fbfbf5`
- `#e4e4e7`
- `#d4d4d8`
- `#a1a1aa`
- `#71717a`
- `#52525b`
- `#3f3f46`
- `0 1px 2px rgba(255,255,255,0.05), inset 0 1px 0 rgba(255,255,255,0.04)`
- `0 0 0 1px rgba(255,255,255,0.08), 0 1px 3px rgba(0,0,0,0.3), 0 5px 10px rgba(0,0,0,0.2)`
- `0 8px 8px rgba(0,0,0,0.1), 0 4px 4px rgba(0,0,0,0.1), 0 2px 2px rgba(0,0,0,0.1), 0 0 0 1px rgba(0,0,0,0.1)`
- `0 25px 50px -12px rgba(0,0,0,0.25)`

## 日期限定首頁觀察

官方來源：https://www.shopify.com/ca，觀察日期2026-10-10。

保留深色首頁、72px 半透明導覽、96px 桌面／48px 窄版主標、四類商家真實照片、Agentic Storefronts、目前 Show up everywhere 三張插畫、跨境地圖、三組創業者照片、紫色 Sidekick、App 拼貼、開發者圖層、綠色 Checkout、地球截圖替代、Capital 引言、三步驟照片與完整頁尾。

Shopify 最終桌面高度10958px、390px窄版11531px，均與目前官方捕捉狀態相同。最新官方產品段是 無須四處奔波，也能處處被看見。；已移除舊文案與 Courses 頁尾。商家類別、窄版選單與產品次選單、返回、Escape、創業者頁點已操作檢查。

完整官方頁面先以分段DOM保存，原生Google Stitch重新生成的結果與供應商說法保留。接著以今天官方的完整渲染DOM/CSS、字型與公開照片修正具體頁面；舊草稿及原生生成未被覆寫。

實際於1440×1000及390×844 CSS像素、DPR1、相同桌面UA逐段捲動、截圖與比較；390px是響應式窄版證據，並非真實手機硬體測試。兩尺寸均無水平溢位，已觀察的本地圖片皆載入，字型完成載入。已逐段檢視全部比較圖；影片時間、轉場及部分互動不同，不能推論全面官方一致。

## 已知差異與驗證範圍

- 官網串流主視覺與輪替標題，以實際官方海報及擷取的一個標題階段呈現；串流動畫與變動標題尚未重現。
- 即時 WebGL 地球以具來源紀錄的原日期官網區域截圖及柔邊遮罩替代；旋轉、周圍星空與變動的商務資料尚未重現。
- 商家分類、國家與商品插圖保留初始階段。手動分類選擇及創業者圓點可操作，但官網自動輪替、滑動、拖曳與時間尚未完整重現。
- 桌面選單關閉時明確隱藏外框，並停用選單專用 GPU 轉場，以避免可重現的殘留繪製。端點版面有範圍限定的證據；轉場時間及全部滑鼠移入、焦點狀態仍未驗證。
- 品牌故事及客戶引言影片對話框、國家選擇、Cookie 服務及帳戶、結帳、商店服務不在已驗證範圍。隱私操作開啟本機教學對話框。
- 公開影片仍使用外部網址，比較時畫格不同；真實手機與其他寬度尚未驗證，原始比對也未涵蓋最終公開部署。

以上限制沿用原參考日期的比對紀錄。本次繁體中文整理不會把未驗證的影片、動畫、服務或尺寸改標為已通過；目前預覽仍未宣稱與官方完全一致。
<!-- Original AI instructions: awesome-ai-web-design -->

## 來源與使用範圍

設計資料改寫自採 MIT 授權的 VoltAgent/awesome-design-md，詳見 LICENSE 與 ATTRIBUTION.md。品牌名稱僅用於識別參考來源，並非官方授權或服務。下方 AI 指令由本專案獨立撰寫；若既有互動備註與無障礙要求衝突，以此處的可用性檢查為準。

## 重新撰寫的 AI 任務指令

語言：繁體中文（台灣用語，zh-TW）。將 DESIGN.md 放入專案，再選擇下方任務。這些指令由本專案重新撰寫；請把示範內容替換為自己的產品需求。

## 建立新頁面

```text
先閱讀隨附的 DESIGN.md，以 Shopify 的設計語言作為介面參考。請完成以下可操作頁面：製作商店工具總覽，包含深色介紹、簡潔商家案例與商品管理預覽。使用輕字重的大標題並節制運用綠色，以清楚標示的示範商品呈現實用操作。

使用我的產品名稱、內容與資料格式，優先沿用專案現有元件及技術。開始製作樣式前，先將色彩、字體、間距與圓角整理為可重複使用的設計變數。指定字型無法取得時，使用可用的系統字型或開源字型，並說明替代方式。介面文案、按鈕、提示、錯誤訊息、圖片替代文字、註解與交付說明，一律使用繁體中文（台灣用語）。使用「專案、元件、資料、建立、預設、載入、登入、連結、儲存、影片」等台灣用語。保留品牌名稱、檔名、網址、API 識別字與可執行程式碼；HTML 語言設為 zh-Hant-TW。

讓互動元件可實際操作，並將狀態提供給輔助科技。具備可見的鍵盤焦點、清楚的欄位標示、減少動態效果，以及至少 44px 的觸控區域。參考視覺與可用性衝突時，作最小幅度的無障礙調整並記錄原因。在 390px、768px、1440px 寬度檢查版面，涵蓋繁體中文長標題、長內容、空白及錯誤狀態。金額、數量與日期依資料本身的幣別、單位及時區呈現，以 zh-TW 格式顯示，不擅自換算。最後交付完成的檔案、實際驗證結果與仍待確認的假設，不把未檢查項目宣稱為通過。
```

## 製作元件

```text
先閱讀隨附的 DESIGN.md，以 Shopify 的設計語言作為介面參考。請製作商品管理卡片，包含庫存狀態與可編輯的發布狀態。沿用現有元件慣例，放入精簡且符合實際情境的範例。比例與資訊層級應來自參考規格，不能只替通用卡片換色。依需求支援預設、焦點、停用、載入與錯誤狀態。使用有意義的示範資料，讓每個可見操作都有明確結果。

使用我的產品名稱、內容與資料格式，優先沿用專案現有元件及技術。開始製作樣式前，先將色彩、字體、間距與圓角整理為可重複使用的設計變數。指定字型無法取得時，使用可用的系統字型或開源字型，並說明替代方式。介面文案、按鈕、提示、錯誤訊息、圖片替代文字、註解與交付說明，一律使用繁體中文（台灣用語）。使用「專案、元件、資料、建立、預設、載入、登入、連結、儲存、影片」等台灣用語。保留品牌名稱、檔名、網址、API 識別字與可執行程式碼；HTML 語言設為 zh-Hant-TW。

讓互動元件可實際操作，並將狀態提供給輔助科技。具備可見的鍵盤焦點、清楚的欄位標示、減少動態效果，以及至少 44px 的觸控區域。參考視覺與可用性衝突時，作最小幅度的無障礙調整並記錄原因。在 390px、768px、1440px 寬度檢查版面，涵蓋繁體中文長標題、長內容、空白及錯誤狀態。金額、數量與日期依資料本身的幣別、單位及時區呈現，以 zh-TW 格式顯示，不擅自換算。最後交付完成的檔案、實際驗證結果與仍待確認的假設，不把未檢查項目宣稱為通過。
```

## 改造既有介面

```text
先閱讀隨附的 DESIGN.md，以 Shopify 的設計語言作為介面參考。重新設計選定頁面，同時保留路由、資料、行為與使用者可理解的意義。先確認頁面層級，再找出最少且可重複使用的設計變數與元件調整。以下構圖作為視覺方向，依現有頁面調整：製作商店工具總覽，包含深色介紹、簡潔商家案例與商品管理預覽。使用輕字重的大標題並節制運用綠色，以清楚標示的示範商品呈現實用操作。

使用我的產品名稱、內容與資料格式，優先沿用專案現有元件及技術。開始製作樣式前，先將色彩、字體、間距與圓角整理為可重複使用的設計變數。指定字型無法取得時，使用可用的系統字型或開源字型，並說明替代方式。介面文案、按鈕、提示、錯誤訊息、圖片替代文字、註解與交付說明，一律使用繁體中文（台灣用語）。使用「專案、元件、資料、建立、預設、載入、登入、連結、儲存、影片」等台灣用語。保留品牌名稱、檔名、網址、API 識別字與可執行程式碼；HTML 語言設為 zh-Hant-TW。依完整元件群組套用變更，檢查其他頁面是否受影響，並說明調整前後的主要差異。

讓互動元件可實際操作，並將狀態提供給輔助科技。具備可見的鍵盤焦點、清楚的欄位標示、減少動態效果，以及至少 44px 的觸控區域。參考視覺與可用性衝突時，作最小幅度的無障礙調整並記錄原因。在 390px、768px、1440px 寬度檢查版面，涵蓋繁體中文長標題、長內容、空白及錯誤狀態。金額、數量與日期依資料本身的幣別、單位及時區呈現，以 zh-TW 格式顯示，不擅自換算。最後交付完成的檔案、實際驗證結果與仍待確認的假設，不把未檢查項目宣稱為通過。
```

## 逐次調整流程

1. 先指出一個可實際觀察的問題，例如層級不清或內容遭裁切。
2. 在 DESIGN.md 找到對應設計變數或元件規則，提出範圍明確的調整。
3. 套用調整，保留無關的路由與資料行為。
4. 檢查鍵盤焦點、窄版排版，以及代表性的內容與錯誤狀態。
5. 用繁體中文說明結果，以及刻意偏離參考外觀的原因。
