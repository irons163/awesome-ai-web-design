---
version: zh-TW-2026-10-15
language: zh-TW
name: "PostHog"
description: "暖灰與黃色細節，兼顧密集資訊和趣味。"

colors:
  primary: "#f7a501"
  primary-pressed: "#dd9001"
  primary-active: "#b17816"
  on-primary: "#23251d"
  ink: "#23251d"
  body: "#4d4f46"
  charcoal: "#33342d"
  mute: "#6c6e63"
  ash: "#9b9c92"
  stone: "#b6b7af"
  hairline: "#bfc1b7"
  hairline-soft: "#dcdfd2"
  on-dark: "#ffffff"
  canvas: "#eeefe9"
  surface-soft: "#e5e7e0"
  surface-card: "#ffffff"
  surface-doc: "#fcfcfa"
  surface-dark: "#23251d"
  link-blue: "#1d4ed8"
  link-teal: "#1078a3"
  accent-blue: "#2c84e0"
  accent-blue-soft: "#dceaf6"
  accent-red: "#cd4239"
  accent-red-soft: "#f7d6d3"
  accent-green: "#2c8c66"
  accent-green-soft: "#d9eddf"
  accent-purple: "#7c44a6"
  accent-purple-soft: "#e7d8ee"
  focus-ring: "rgba(59,130,246,0.5)"

typography:
  display-xl:
    fontFamily: IBM Plex Sans Variable
    fontSize: 36px
    fontWeight: 700
    lineHeight: 1.5
    letterSpacing: 0
  display-lg:
    fontFamily: IBM Plex Sans Variable
    fontSize: 24px
    fontWeight: 800
    lineHeight: 1.33
    letterSpacing: -0.6px
  heading-lg:
    fontFamily: IBM Plex Sans Variable
    fontSize: 21px
    fontWeight: 700
    lineHeight: 1.4
    letterSpacing: -0.5px
  heading-md:
    fontFamily: IBM Plex Sans Variable
    fontSize: 20px
    fontWeight: 700
    lineHeight: 1.4
    letterSpacing: 0
  heading-sm:
    fontFamily: IBM Plex Sans Variable
    fontSize: 18px
    fontWeight: 700
    lineHeight: 1.5
    letterSpacing: 0
    textTransform: uppercase
  heading-sm-mixed:
    fontFamily: IBM Plex Sans Variable
    fontSize: 18px
    fontWeight: 600
    lineHeight: 1.56
    letterSpacing: 0
  body-md:
    fontFamily: IBM Plex Sans Variable
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: 0
  body-strong:
    fontFamily: IBM Plex Sans Variable
    fontSize: 16px
    fontWeight: 600
    lineHeight: 1.5
    letterSpacing: 0
  body-sm:
    fontFamily: IBM Plex Sans Variable
    fontSize: 15px
    fontWeight: 400
    lineHeight: 1.71
    letterSpacing: 0
  body-sm-strong:
    fontFamily: IBM Plex Sans Variable
    fontSize: 15px
    fontWeight: 600
    lineHeight: 1.71
    letterSpacing: 0
  body-xs:
    fontFamily: IBM Plex Sans Variable
    fontSize: 14px
    fontWeight: 500
    lineHeight: 1.43
    letterSpacing: 0
  caption-md:
    fontFamily: IBM Plex Sans Variable
    fontSize: 14px
    fontWeight: 700
    lineHeight: 1.71
    letterSpacing: 0
  caption-sm:
    fontFamily: IBM Plex Sans Variable
    fontSize: 13px
    fontWeight: 500
    lineHeight: 1.5
    letterSpacing: 0
  caption-xs:
    fontFamily: IBM Plex Sans Variable
    fontSize: 12px
    fontWeight: 600
    lineHeight: 1.33
    letterSpacing: 0
    textTransform: uppercase
  utility-xs:
    fontFamily: IBM Plex Sans Variable
    fontSize: 12px
    fontWeight: 700
    lineHeight: 1.33
    letterSpacing: 0
    textTransform: uppercase
  link-md:
    fontFamily: IBM Plex Sans Variable
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: 0
  button-md:
    fontFamily: IBM Plex Sans Variable
    fontSize: 14px
    fontWeight: 700
    lineHeight: 1.5
    letterSpacing: 0
  button-sm:
    fontFamily: IBM Plex Sans Variable
    fontSize: 13px
    fontWeight: 500
    lineHeight: 1
    letterSpacing: 0
  code-sm:
    fontFamily: ui-monospace
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.43
    letterSpacing: 0
  code-xs:
    fontFamily: Source Code Pro
    fontSize: 14px
    fontWeight: 500
    lineHeight: 1.43
    letterSpacing: 0

rounded:
  none: 0px
  xs: 2px
  sm: 4px
  md: 6px
  lg: 8px
  full: 9999px

spacing:
  xxs: 2px
  xs: 4px
  sm: 8px
  md: 12px
  lg: 16px
  xl: 24px
  xxl: 32px
  section: 80px

components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.button-md}"
    rounded: "{rounded.md}"
    padding: 8px 16px
    height: 40px
  button-primary-pressed:
    backgroundColor: "{colors.primary-pressed}"
    textColor: "{colors.on-primary}"
    typography: "{typography.button-md}"
    rounded: "{rounded.md}"
  button-secondary:
    backgroundColor: "{colors.surface-soft}"
    textColor: "{colors.ink}"
    typography: "{typography.button-md}"
    rounded: "{rounded.md}"
    padding: 8px 16px
    height: 40px
  button-tertiary:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    typography: "{typography.button-md}"
    rounded: "{rounded.md}"
    padding: 8px 12px
  button-disabled:
    backgroundColor: "{colors.surface-soft}"
    textColor: "{colors.ash}"
    rounded: "{rounded.md}"
  text-input:
    backgroundColor: "{colors.surface-card}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: 8px 12px
    height: 36px
  text-input-focused:
    backgroundColor: "{colors.surface-card}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
  search-input:
    backgroundColor: "{colors.surface-card}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: 8px 12px
    height: 36px
  product-card:
    backgroundColor: "{colors.surface-card}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: 24px
  doc-card:
    backgroundColor: "{colors.surface-doc}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: 24px
  feature-tile:
    backgroundColor: "{colors.surface-card}"
    textColor: "{colors.ink}"
    typography: "{typography.heading-sm-mixed}"
    rounded: "{rounded.md}"
    padding: 20px
  pricing-tier-card:
    backgroundColor: "{colors.surface-card}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: 32px
  hedgehog-mascot-card:
    backgroundColor: "{colors.surface-card}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: 24px
  product-tab:
    backgroundColor: "transparent"
    textColor: "{colors.body}"
    typography: "{typography.body-strong}"
    rounded: "{rounded.md}"
    padding: 8px 12px
  product-tab-active:
    backgroundColor: "{colors.surface-card}"
    textColor: "{colors.ink}"
    typography: "{typography.body-strong}"
    rounded: "{rounded.md}"
  pill-tab:
    backgroundColor: "transparent"
    textColor: "{colors.body}"
    typography: "{typography.button-sm}"
    rounded: "{rounded.full}"
    padding: 6px 14px
  pill-tab-active:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.on-dark}"
    typography: "{typography.button-sm}"
    rounded: "{rounded.full}"
  badge-uppercase:
    backgroundColor: "transparent"
    textColor: "{colors.body}"
    typography: "{typography.utility-xs}"
    rounded: "{rounded.none}"
  badge-promo:
    backgroundColor: "{colors.accent-blue-soft}"
    textColor: "{colors.link-blue}"
    typography: "{typography.caption-xs}"
    rounded: "{rounded.full}"
    padding: 2px 8px
  banner-tip-blue:
    backgroundColor: "{colors.accent-blue-soft}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: 16px 20px
  banner-tip-green:
    backgroundColor: "{colors.accent-green-soft}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: 16px 20px
  banner-tip-red:
    backgroundColor: "{colors.accent-red-soft}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: 16px 20px
  banner-tip-purple:
    backgroundColor: "{colors.accent-purple-soft}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: 16px 20px
  code-block:
    backgroundColor: "{colors.surface-dark}"
    textColor: "{colors.on-dark}"
    typography: "{typography.code-sm}"
    rounded: "{rounded.md}"
    padding: 16px 20px
  inline-code:
    backgroundColor: "{colors.surface-soft}"
    textColor: "{colors.ink}"
    typography: "{typography.code-xs}"
    rounded: "{rounded.xs}"
    padding: 2px 6px
  primary-nav:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.body-strong}"
    rounded: "{rounded.none}"
    height: 56px
  sub-nav-strip:
    backgroundColor: "{colors.surface-soft}"
    textColor: "{colors.body}"
    typography: "{typography.body-xs}"
    rounded: "{rounded.none}"
    height: 40px
  doc-sidebar:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.body}"
    typography: "{typography.body-xs}"
    rounded: "{rounded.none}"
    width: 240px
  footer-section:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.body}"
    typography: "{typography.body-xs}"
    rounded: "{rounded.none}"
    padding: 32px 24px
  link-inline:
    textColor: "{colors.link-teal}"
    typography: "{typography.link-md}"
---

# PostHog 延伸設計規格

語言：繁體中文（台灣用語，zh-TW）。在地化更新：2026-11-01。

## 來源與規格層次

這份規格將較早保存的品牌設計資料重新整理為可實作的繁體中文文件。來源設定中的色碼、字級、字重、行高、間距、圓角與元件識別字保留，供開發工具讀取；敘述與操作指令改用台灣用語。這些延伸設定不等同於目前日期限定首頁的逐項實測值，若兩者不同，依下方的日期限定觀察及對應預覽判讀。

- 原始資料版本：`1a783491c9539c3153c2fc96c16d59131e024f4e`。
- 原始 DESIGN.md 摘要：`396e31064702c79b9b9dbbebb9b7b9a06d9453298c79dc5fedff5178305ee4a3`。
- 目前首頁參考日期：2026-10-10。
- 目前公開來源：https://posthog.com/。
- 目前預覽：`official-drafts/posthog.html`。
- 台灣繁體中文規格與指令是本次重新產出的內容；來源截圖及原生生成紀錄保留原貌。

## 整體視覺方向

暖灰與黃色細節，兼顧密集資訊和趣味。

製作產品分析總覽，包含精簡洞察卡片、事件表格與友善的初次使用提示。內容緊湊且對齊，黃色用於操作重點，不重製吉祥物圖像。

先建立主要內容、輔助資訊與操作之間的層級，再套用色彩及裝飾。品牌色應有明確用途；主要操作、選取、錯誤及停用狀態要能分辨。避免將多套參考風格混在同一頁，也不要僅替換通用卡片的顏色。

## 色彩、字型與繁體中文排版

上方來源設定保留原始色彩角色與數值。主要品牌色用於最重要的操作；背景、內容表面、主要文字、次要文字與分隔線各自維持一致用途。資訊不能只依賴顏色，狀態須同時有文字或圖示標示。

原字型名稱可作為拉丁字母參考。繁體中文字型優先使用可取得的 `Noto Sans TC`、`PingFang TC`、`Microsoft JhengHei`，最後才使用 `sans-serif`。原字型未涵蓋中文時必須提供替代，不以缺字或圖片文字呈現正文。專有字型無法取得時，記錄替代字型與可能的字寬差異。

中文標題以語意分段，避免為模仿英文大寫字距而拉散中文字。內文行高、欄寬與段落間距以可讀性為準；英文型號、網址、程式碼及長連結可以換行或在自己的區域捲動，不可撐開整份文件。價格、規格及比較欄位保持數字與單位對齊。

| 字級 | 字重 | 行高 | 字距 |
| --- | --- | --- | --- |
| 36px | 700 | 1.5 | 0 |
| 24px | 800 | 1.33 | -0.6px |
| 21px | 700 | 1.4 | -0.5px |
| 20px | 700 | 1.4 | 0 |
| 18px | 700 | 1.5 | 0 (uppercase) |
| 18px | 600 | 1.56 | 0 |
| 16px | 400 | 1.5 | 0 |
| 16px | 600 | 1.5 | 0 |
| 15px | 400 | 1.71 | 0 |
| 15px | 600 | 1.71 | 0 |
| 14px | 500 | 1.43 | 0 |
| 14px | 700 | 1.71 | 0 |
| 13px | 500 | 1.5 | 0 |
| 12px | 600 | 1.33 | 0 (uppercase) |
| 12px | 700 | 1.33 | 0 (uppercase) |
| 16px | 400 | 1.5 | 0 |
| 14px | 700 | 1.5 | 0 |
| 13px | 500 | 1 | 0 |
| 14px | 400 | 1.43 | 0 |
| 14px | 500 | 1.43 | 0 |

## 版面與元件結構

此參考可先實作：事件洞察卡片，包含示範趨勢、日期區間與沒有資料的說明。

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

- `#eeefe9`
- `#4d4f46`
- `#23251d`
- `#f7a501`
- `#dd9001`
- `#b17816`
- `#e5e7e0`
- `#ffffff`
- `#fcfcfa`
- `#bfc1b7`
- `#dcdfd2`
- `#33342d`
- `#6c6e63`
- `#9b9c92`
- `#b6b7af`
- `#1d4ed8`
- `#1078a3`
- `#2c84e0`
- `#dceaf6`
- `#cd4239`
- `#f7d6d3`
- `#2c8c66`
- `#d9eddf`
- `#7c44a6`
- `#e7d8ee`
- `rgba(59,130,246,0.5)`
- `6px 6px 0 0`
- `8px 16px`
- `40px`
- `8px 12px`
- `6px 14px`
- `2px 8px`
- `36px`
- `16px 20px`
- `2px 6px`
- `56px`
- `240px`
- `32px 24px`
- `width: auto; max-width: 100%`

## 日期限定首頁觀察

來源：https://posthog.com/。原始取樣時間保留於 UTC 紀錄，oct10 工作檔名不表示所有檢查都在 10 月 10 日完成。

現行 PostHog 為綠色草地插畫桌面、周圍 app 圖示、頂部功能列與淡綠應用程式視窗。RoundHog 黑字、橘黃按鈕及紫色頁籤構成「產品的情境資訊層」首頁；不能換成通用紫色 SaaS 模板。

視窗內依序有免費 setup 卡、Ask PostHog anything／讓 AI 代理掌握產品情境／Ship with PostHog、Social proof、彩色客戶 logo、All your data、Usage-based pricing 表、Why PostHog、Bedtime reading、Shameless CTA，以及復古軟體盒 PostHog Web 廣告。setup 的 97% 與定價文內的 98% 原文矛盾分別保留。

主要內容在 .app-scroll-viewport 內捲動；桌面內容 extent 4679／可見 629，窄版 extent 7725／可見 787，不能以 bodyHeight 720／844 判定全頁。早期 JPEG 窄版實際只有 390×219，已排除作完整證據；重新以明確 clip 取得 390×844 原始 PNG 後才可檢查。

保留原有 DESIGN.md、PROMPTS.md、STITCH-PROMPT.md；本檔為目前官網的日期限定補充。研究頁免費瀏覽、無付費執行時依賴，未執行購買或訂閱。

驗證範圍為匿名公開首頁、1280×720 與 390×844、DPR 1、桌面 UA。實體手機、其他地區、完整互動與部署尚未驗證；accepted=false，不宣稱與官方一致。

## 已知差異與驗證範圍

- 覆蓋檢查須使用元素捲動的 offsets／extent／visible_extent，而非文件 bodyHeight；已被取代的 390×219 JPEG 不是完整窄版證據。
- 分頁、工具列與視窗操作、選單、雲端區域、MCP 安裝、即時計數及註冊帳戶服務尚未驗證。
- 作業系統視窗控制與導覽、Ask／Give／Ship 分頁、暫停及輪播、美國與歐洲雲端選擇、註冊、安裝及服務未進行互動測試。
- 來源的 97% 免費設定文案與 98% 定價文案互相矛盾，依觀察保留，未自行統一數字。
- 原始比對未涵蓋其他寬度、實體裝置、地區、完整互動及動態，以及正式部署。

以上限制沿用原參考日期的比對紀錄。本次繁體中文整理不會把未驗證的影片、動畫、服務或尺寸改標為已通過；目前預覽仍未宣稱與官方完全一致。
<!-- Original AI instructions: awesome-ai-web-design -->

## 來源與使用範圍

資料來源與適用授權集中於專案根目錄的 ATTRIBUTION.md 與 LICENSE。品牌名稱僅用於識別參考來源，並非官方授權或服務。下方 AI 指令由本專案獨立撰寫；若既有互動備註與無障礙要求衝突，以此處的可用性檢查為準。

## 重新撰寫的 AI 任務指令

語言：繁體中文（台灣用語，zh-TW）。將 DESIGN.md 放入專案，再選擇下方任務。這些指令由本專案重新撰寫；請把示範內容替換為自己的產品需求。

## 建立新頁面

```text
先閱讀隨附的 DESIGN.md，以 PostHog 的設計語言作為介面參考。請完成以下可操作頁面：製作產品分析總覽，包含精簡洞察卡片、事件表格與友善的初次使用提示。內容緊湊且對齊，黃色用於操作重點，不重製吉祥物圖像。

使用我的產品名稱、內容與資料格式，優先沿用專案現有元件及技術。開始製作樣式前，先將色彩、字體、間距與圓角整理為可重複使用的設計變數。指定字型無法取得時，使用可用的系統字型或開源字型，並說明替代方式。介面文案、按鈕、提示、錯誤訊息、圖片替代文字、註解與交付說明，一律使用繁體中文（台灣用語）。使用「專案、元件、資料、建立、預設、載入、登入、連結、儲存、影片」等台灣用語。保留品牌名稱、檔名、網址、API 識別字與可執行程式碼；HTML 語言設為 zh-Hant-TW。

讓互動元件可實際操作，並將狀態提供給輔助科技。具備可見的鍵盤焦點、清楚的欄位標示、減少動態效果，以及至少 44px 的觸控區域。參考視覺與可用性衝突時，作最小幅度的無障礙調整並記錄原因。在 390px、768px、1440px 寬度檢查版面，涵蓋繁體中文長標題、長內容、空白及錯誤狀態。金額、數量與日期依資料本身的幣別、單位及時區呈現，以 zh-TW 格式顯示，不擅自換算。最後交付完成的檔案、實際驗證結果與仍待確認的假設，不把未檢查項目宣稱為通過。
```

## 製作元件

```text
先閱讀隨附的 DESIGN.md，以 PostHog 的設計語言作為介面參考。請製作事件洞察卡片，包含示範趨勢、日期區間與沒有資料的說明。沿用現有元件慣例，放入精簡且符合實際情境的範例。比例與資訊層級應來自參考規格，不能只替通用卡片換色。依需求支援預設、焦點、停用、載入與錯誤狀態。使用有意義的示範資料，讓每個可見操作都有明確結果。

使用我的產品名稱、內容與資料格式，優先沿用專案現有元件及技術。開始製作樣式前，先將色彩、字體、間距與圓角整理為可重複使用的設計變數。指定字型無法取得時，使用可用的系統字型或開源字型，並說明替代方式。介面文案、按鈕、提示、錯誤訊息、圖片替代文字、註解與交付說明，一律使用繁體中文（台灣用語）。使用「專案、元件、資料、建立、預設、載入、登入、連結、儲存、影片」等台灣用語。保留品牌名稱、檔名、網址、API 識別字與可執行程式碼；HTML 語言設為 zh-Hant-TW。

讓互動元件可實際操作，並將狀態提供給輔助科技。具備可見的鍵盤焦點、清楚的欄位標示、減少動態效果，以及至少 44px 的觸控區域。參考視覺與可用性衝突時，作最小幅度的無障礙調整並記錄原因。在 390px、768px、1440px 寬度檢查版面，涵蓋繁體中文長標題、長內容、空白及錯誤狀態。金額、數量與日期依資料本身的幣別、單位及時區呈現，以 zh-TW 格式顯示，不擅自換算。最後交付完成的檔案、實際驗證結果與仍待確認的假設，不把未檢查項目宣稱為通過。
```

## 改造既有介面

```text
先閱讀隨附的 DESIGN.md，以 PostHog 的設計語言作為介面參考。重新設計選定頁面，同時保留路由、資料、行為與使用者可理解的意義。先確認頁面層級，再找出最少且可重複使用的設計變數與元件調整。以下構圖作為視覺方向，依現有頁面調整：製作產品分析總覽，包含精簡洞察卡片、事件表格與友善的初次使用提示。內容緊湊且對齊，黃色用於操作重點，不重製吉祥物圖像。

使用我的產品名稱、內容與資料格式，優先沿用專案現有元件及技術。開始製作樣式前，先將色彩、字體、間距與圓角整理為可重複使用的設計變數。指定字型無法取得時，使用可用的系統字型或開源字型，並說明替代方式。介面文案、按鈕、提示、錯誤訊息、圖片替代文字、註解與交付說明，一律使用繁體中文（台灣用語）。使用「專案、元件、資料、建立、預設、載入、登入、連結、儲存、影片」等台灣用語。保留品牌名稱、檔名、網址、API 識別字與可執行程式碼；HTML 語言設為 zh-Hant-TW。依完整元件群組套用變更，檢查其他頁面是否受影響，並說明調整前後的主要差異。

讓互動元件可實際操作，並將狀態提供給輔助科技。具備可見的鍵盤焦點、清楚的欄位標示、減少動態效果，以及至少 44px 的觸控區域。參考視覺與可用性衝突時，作最小幅度的無障礙調整並記錄原因。在 390px、768px、1440px 寬度檢查版面，涵蓋繁體中文長標題、長內容、空白及錯誤狀態。金額、數量與日期依資料本身的幣別、單位及時區呈現，以 zh-TW 格式顯示，不擅自換算。最後交付完成的檔案、實際驗證結果與仍待確認的假設，不把未檢查項目宣稱為通過。
```

## 逐次調整流程

1. 先指出一個可實際觀察的問題，例如層級不清或內容遭裁切。
2. 在 DESIGN.md 找到對應設計變數或元件規則，提出範圍明確的調整。
3. 套用調整，保留無關的路由與資料行為。
4. 檢查鍵盤焦點、窄版排版，以及代表性的內容與錯誤狀態。
5. 用繁體中文說明結果，以及刻意偏離參考外觀的原因。
