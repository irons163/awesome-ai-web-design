---
version: zh-TW-2026-10-15
language: zh-TW
name: "Stripe"
description: "深藍字色、靛紫操作與輕盈的漸層空間。"

colors:
  primary: "#533afd"
  primary-deep: "#4434d4"
  primary-press: "#2e2b8c"
  primary-soft: "#665efd"
  primary-bg-subdued-hover: "#b9b9f9"
  brand-dark-900: "#1c1e54"
  ink: "#0d253d"
  ink-secondary: "#273951"
  ink-mute: "#64748d"
  ink-mute-2: "#61718a"
  on-primary: "#ffffff"
  canvas: "#ffffff"
  canvas-soft: "#f6f9fc"
  canvas-cream: "#f5e9d4"
  hairline: "#e3e8ee"
  hairline-input: "#a8c3de"
  ruby: "#ea2261"
  magenta: "#f96bee"
  lemon: "#9b6829"
  shadow-blue: "#003770"

typography:
  display-xxl:
    fontFamily: "sohne-var, 'SF Pro Display', system-ui, -apple-system, sans-serif"
    fontSize: 56px
    fontWeight: 300
    lineHeight: 1.03
    letterSpacing: -1.4px
    fontFeature: ss01
  display-xl:
    fontFamily: "sohne-var, 'SF Pro Display', system-ui, -apple-system, sans-serif"
    fontSize: 48px
    fontWeight: 300
    lineHeight: 1.15
    letterSpacing: -0.96px
    fontFeature: ss01
  display-lg:
    fontFamily: "sohne-var, 'SF Pro Display', system-ui, -apple-system, sans-serif"
    fontSize: 32px
    fontWeight: 300
    lineHeight: 1.1
    letterSpacing: -0.64px
    fontFeature: ss01
  display-md:
    fontFamily: "sohne-var, 'SF Pro Display', system-ui, -apple-system, sans-serif"
    fontSize: 26px
    fontWeight: 300
    lineHeight: 1.12
    letterSpacing: -0.26px
    fontFeature: ss01
  heading-lg:
    fontFamily: "sohne-var, 'SF Pro Display', system-ui, -apple-system, sans-serif"
    fontSize: 22px
    fontWeight: 300
    lineHeight: 1.1
    letterSpacing: -0.22px
    fontFeature: ss01
  heading-md:
    fontFamily: "sohne-var, 'SF Pro Display', system-ui, -apple-system, sans-serif"
    fontSize: 20px
    fontWeight: 300
    lineHeight: 1.4
    letterSpacing: -0.2px
    fontFeature: ss01
  heading-sm:
    fontFamily: "sohne-var, 'SF Pro Display', system-ui, -apple-system, sans-serif"
    fontSize: 18px
    fontWeight: 300
    lineHeight: 1.4
    letterSpacing: 0
    fontFeature: ss01
  body-lg:
    fontFamily: "sohne-var, 'SF Pro Display', system-ui, -apple-system, sans-serif"
    fontSize: 16px
    fontWeight: 300
    lineHeight: 1.4
    letterSpacing: 0
    fontFeature: ss01
  body-md:
    fontFamily: "sohne-var, 'SF Pro Display', system-ui, -apple-system, sans-serif"
    fontSize: 15px
    fontWeight: 300
    lineHeight: 1.4
    letterSpacing: 0
    fontFeature: ss01
  body-tabular:
    fontFamily: "sohne-var, 'SF Pro Display', system-ui, -apple-system, sans-serif"
    fontSize: 14px
    fontWeight: 300
    lineHeight: 1.4
    letterSpacing: -0.42px
    fontFeature: tnum
  button-md:
    fontFamily: "sohne-var, 'SF Pro Display', system-ui, -apple-system, sans-serif"
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.0
    letterSpacing: 0
    fontFeature: ss01
  button-sm:
    fontFamily: "sohne-var, 'SF Pro Display', system-ui, -apple-system, sans-serif"
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.0
    letterSpacing: 0
    fontFeature: ss01
  caption:
    fontFamily: "sohne-var, 'SF Pro Display', system-ui, -apple-system, sans-serif"
    fontSize: 13px
    fontWeight: 400
    lineHeight: 1.4
    letterSpacing: -0.39px
    fontFeature: tnum
  micro:
    fontFamily: "sohne-var, 'SF Pro Display', system-ui, -apple-system, sans-serif"
    fontSize: 11px
    fontWeight: 300
    lineHeight: 1.4
    letterSpacing: 0
    fontFeature: ss01
  micro-cap:
    fontFamily: "sohne-var, 'SF Pro Display', system-ui, -apple-system, sans-serif"
    fontSize: 10px
    fontWeight: 400
    lineHeight: 1.15
    letterSpacing: 0.1px
    fontFeature: ss01

rounded:
  xs: 4px
  sm: 6px
  md: 8px
  lg: 12px
  xl: 16px
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
    typography: "{typography.button-md}"
    rounded: "{rounded.pill}"
    padding: 8px 16px
  button-primary-pill-pressed:
    backgroundColor: "{colors.primary-press}"
    textColor: "{colors.on-primary}"
    typography: "{typography.button-md}"
    rounded: "{rounded.pill}"
    padding: 8px 16px
  button-secondary:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.primary}"
    typography: "{typography.button-md}"
    rounded: "{rounded.pill}"
    padding: 8px 16px
  button-on-dark:
    backgroundColor: "{colors.brand-dark-900}"
    textColor: "{colors.on-primary}"
    typography: "{typography.button-md}"
    rounded: "{rounded.pill}"
    padding: 8px 16px
  text-input:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.sm}"
    padding: 8px 12px
  text-input-focused:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.sm}"
    padding: 8px 12px
  card-feature-light:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.lg}"
    padding: 32px
  card-pricing:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.lg}"
    padding: 32px
  card-pricing-featured:
    backgroundColor: "{colors.brand-dark-900}"
    textColor: "{colors.on-primary}"
    typography: "{typography.body-md}"
    rounded: "{rounded.lg}"
    padding: 32px
  card-cream-band:
    backgroundColor: "{colors.canvas-cream}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.lg}"
    padding: 32px
  card-dashboard-mockup:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.body-tabular}"
    rounded: "{rounded.lg}"
    padding: 24px
  pill-tag-soft:
    backgroundColor: "{colors.primary-bg-subdued-hover}"
    textColor: "{colors.primary-deep}"
    typography: "{typography.micro-cap}"
    rounded: "{rounded.pill}"
    padding: 4px 8px
  nav-bar-on-mesh:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.xs}"
    padding: 16px 24px
  link-on-light:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.primary}"
    typography: "{typography.body-md}"
    rounded: "{rounded.xs}"
    padding: 0px
  footer-light:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink-mute}"
    typography: "{typography.caption}"
    rounded: "{rounded.xs}"
    padding: 64px 24px
---

# Stripe 延伸設計規格

語言：繁體中文（台灣用語，zh-TW）。在地化更新：2026-11-01。

## 來源與規格層次

這份規格將較早保存的品牌設計資料重新整理為可實作的繁體中文文件。來源設定中的色碼、字級、字重、行高、間距、圓角與元件識別字保留，供開發工具讀取；敘述與操作指令改用台灣用語。這些延伸設定不等同於目前日期限定首頁的逐項實測值，若兩者不同，依下方的日期限定觀察及對應預覽判讀。

- 原始資料版本：`1a783491c9539c3153c2fc96c16d59131e024f4e`。
- 原始 DESIGN.md 摘要：`a8a4375382af9019d7ddba27315d79f785d1d0c9c603cc82ae42fd83ba9ecac7`。
- 目前首頁參考日期：2026-10-10。
- 目前公開來源：https://stripe.com/en-ca。
- 目前預覽：`official-drafts/stripe.html`。
- 台灣繁體中文規格與指令是本次重新產出的內容；來源截圖及原生生成紀錄保留原貌。

## 整體視覺方向

深藍字色、靛紫操作與輕盈的漸層空間。

製作支付基礎架構介紹頁，採輕字重大標題、節制的漸層頁首與實用交易示範。數字對齊並標為範例，以乾淨白色區段讓技術說明容易閱讀。

先建立主要內容、輔助資訊與操作之間的層級，再套用色彩及裝飾。品牌色應有明確用途；主要操作、選取、錯誤及停用狀態要能分辨。避免將多套參考風格混在同一頁，也不要僅替換通用卡片的顏色。

## 色彩、字型與繁體中文排版

上方來源設定保留原始色彩角色與數值。主要品牌色用於最重要的操作；背景、內容表面、主要文字、次要文字與分隔線各自維持一致用途。資訊不能只依賴顏色，狀態須同時有文字或圖示標示。

原字型名稱可作為拉丁字母參考。繁體中文字型優先使用可取得的 `Noto Sans TC`、`PingFang TC`、`Microsoft JhengHei`，最後才使用 `sans-serif`。原字型未涵蓋中文時必須提供替代，不以缺字或圖片文字呈現正文。專有字型無法取得時，記錄替代字型與可能的字寬差異。

中文標題以語意分段，避免為模仿英文大寫字距而拉散中文字。內文行高、欄寬與段落間距以可讀性為準；英文型號、網址、程式碼及長連結可以換行或在自己的區域捲動，不可撐開整份文件。價格、規格及比較欄位保持數字與單位對齊。

| 字級 | 字重 | 行高 | 字距 |
| --- | --- | --- | --- |
| 56px | 300 | 1.03 | -1.4px |
| 48px | 300 | 1.15 | -0.96px |
| 32px | 300 | 1.1 | -0.64px |
| 26px | 300 | 1.12 | -0.26px |
| 22px | 300 | 1.1 | -0.22px |
| 20px | 300 | 1.4 | -0.2px |
| 18px | 300 | 1.4 | 0 |
| 16px | 300 | 1.4 | 0 |
| 15px | 300 | 1.4 | 0 |
| 14px | 300 | 1.4 | -0.42px |
| 16px | 400 | 1.0 | 0 |
| 14px | 400 | 1.0 | 0 |
| 13px | 400 | 1.4 | -0.39px |
| 11px | 300 | 1.4 | 0 |
| 10px | 400 | 1.15 | 0.1px |

## 版面與元件結構

此參考可先實作：示範交易摘要，包含幣別、狀態與可展開的交易明細。

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

- `#533afd`
- `#0d253d`
- `8px 16px`
- `#4434d4`
- `#2e2b8c`
- `#665efd`
- `#b9b9f9`
- `#1c1e54`
- `#ea2261`
- `#f96bee`
- `#9b6829`
- `#ffffff`
- `#f6f9fc`
- `#f5e9d4`
- `#e3e8ee`
- `#a8c3de`
- `#273951`
- `#64748d`
- `#61718a`
- `letter-spacing: -1.4px`
- `box-shadow: rgba(0,55,112,0.08) 0 1px 3px`
- `box-shadow: rgba(0,55,112,0.08) 0 8px 24px, rgba(0,55,112,0.04) 0 2px 6px`
- `4px 8px`

## 日期限定首頁觀察

支付基礎架構首頁以白色背景、深黑藍文字與薰衣草紫、粉橘色波形建立主視覺。原始 Stripe Sohne 字型採輕字重；1440×1000 參考中的導覽高 76px、置中內容寬 1232px，主要操作色為 #5336f5，按鈕為約 4px 圓角矩形。這是日期限定首頁觀察，與較早延伸規格中的膠囊按鈕不可混用。

主視覺以左側連續文字與右上斜向波形構成，沒有右側支付儀表板。主要文字在 1440px 畫面約由 x=208、y=235 起始，內容最寬約 960px；標題與接續灰色說明使用相同 48px 字級、300 字重、55.2px 行高，形成連續閱讀，而非大標題搭配小段落。背景 GDP 數字屬動態觀察值，不可捏造固定比例。

內容依序為商業模式解決方案、Stripe Sessions、全球商務基礎、企業與各規模客戶、新創公司、SaaS 平台、開發者整合、最新消息、開始使用與完整多欄頁尾。產品區使用真實終端機、結帳、訂閱、發卡及平台插圖，不以空白圖示卡片替代。

來源展示數字包含 135+ 種幣別與付款方式、2025 年 US$1.9tn 付款量、99.999% 歷史服務可用率、200m+ 筆有效訂閱，以及開發者區每日 500m+ 次 API 請求、每秒 10k+ 次 API 請求、每分鐘 150k+ 筆交易。這些只代表參考日期的官網版面內容，並非本網站即時查核或服務承諾。

窄版採單欄連續標題、波形背景與 16px 側邊留白。完整桌面導覽及六個對話框有操作紀錄，但動畫波形、部分輪播、國家選擇及帳戶後端仍有限制，須連同已知差異閱讀。

## 已知差異與驗證範圍

- 主視覺 WebGL 波形、產品結帳幣別與畫面、發卡及加密資產、商標跑馬燈、支付調度商標與開發者波形，皆固定於來源已觀察階段；動畫時間與即時 GDP 計數器未與後續官網畫格同步。
- 產品插圖使用保存的官網裝飾圖原始截圖區域。開發者波形裁切不含語意標題及統計覆蓋文字，並依版面伸縮，因此曲線幾何與即時畫布不同。
- 統計主題依來源觀察採桌面黃昏、窄版夜間。官網可能在尺寸切換後保留主題及摺疊狀態；驗收證據使用獨立重新載入的桌面初始狀態。時段及圖表控制未重現 WebGL 變化。
- 平台示範固定為來源最後可見狀態；官網進場時可能只顯示漸層，未宣稱時間一致。
- 新聞輪播可切換文字，但仍保留第一張固定插圖。新創輪播、客戶引言分頁、國家選擇與帳戶後端尚未完整重現互動。
- 1280×720 桌面選單與全部 6 個對話框已開關操作，窄版主選單、產品導覽及 Escape 也已測試。其他選單分支、鍵盤焦點與全部外部目的地尚未完整驗收。
- 早期截圖紀錄沒有拍攝當下的預覽 SHA-256；與目前未變更預覽的關聯，來自保留的完成、建置、雜湊紀錄及人工檢視，並非每張截圖各自記錄的摘要。2026-10-12 來源稽核未回填較早雜湊，也不代表新的瀏覽器檢查。

以上限制沿用原參考日期的比對紀錄。本次繁體中文整理不會把未驗證的影片、動畫、服務或尺寸改標為已通過；目前預覽仍未宣稱與官方完全一致。
<!-- Original AI instructions: awesome-ai-web-design -->

## 來源與使用範圍

資料來源與適用授權集中於專案根目錄的 ATTRIBUTION.md 與 LICENSE。品牌名稱僅用於識別參考來源，並非官方授權或服務。下方 AI 指令由本專案獨立撰寫；若既有互動備註與無障礙要求衝突，以此處的可用性檢查為準。

## 重新撰寫的 AI 任務指令

語言：繁體中文（台灣用語，zh-TW）。將 DESIGN.md 放入專案，再選擇下方任務。這些指令由本專案重新撰寫；請把示範內容替換為自己的產品需求。

## 建立新頁面

```text
先閱讀隨附的 DESIGN.md，以 Stripe 的設計語言作為介面參考。請完成以下可操作頁面：製作支付基礎架構介紹頁，採輕字重大標題、節制的漸層頁首與實用交易示範。數字對齊並標為範例，以乾淨白色區段讓技術說明容易閱讀。

使用我的產品名稱、內容與資料格式，優先沿用專案現有元件及技術。開始製作樣式前，先將色彩、字體、間距與圓角整理為可重複使用的設計變數。指定字型無法取得時，使用可用的系統字型或開源字型，並說明替代方式。介面文案、按鈕、提示、錯誤訊息、圖片替代文字、註解與交付說明，一律使用繁體中文（台灣用語）。使用「專案、元件、資料、建立、預設、載入、登入、連結、儲存、影片」等台灣用語。保留品牌名稱、檔名、網址、API 識別字與可執行程式碼；HTML 語言設為 zh-Hant-TW。

讓互動元件可實際操作，並將狀態提供給輔助科技。具備可見的鍵盤焦點、清楚的欄位標示、減少動態效果，以及至少 44px 的觸控區域。參考視覺與可用性衝突時，作最小幅度的無障礙調整並記錄原因。在 390px、768px、1440px 寬度檢查版面，涵蓋繁體中文長標題、長內容、空白及錯誤狀態。金額、數量與日期依資料本身的幣別、單位及時區呈現，以 zh-TW 格式顯示，不擅自換算。最後交付完成的檔案、實際驗證結果與仍待確認的假設，不把未檢查項目宣稱為通過。
```

## 製作元件

```text
先閱讀隨附的 DESIGN.md，以 Stripe 的設計語言作為介面參考。請製作示範交易摘要，包含幣別、狀態與可展開的交易明細。沿用現有元件慣例，放入精簡且符合實際情境的範例。比例與資訊層級應來自參考規格，不能只替通用卡片換色。依需求支援預設、焦點、停用、載入與錯誤狀態。使用有意義的示範資料，讓每個可見操作都有明確結果。

使用我的產品名稱、內容與資料格式，優先沿用專案現有元件及技術。開始製作樣式前，先將色彩、字體、間距與圓角整理為可重複使用的設計變數。指定字型無法取得時，使用可用的系統字型或開源字型，並說明替代方式。介面文案、按鈕、提示、錯誤訊息、圖片替代文字、註解與交付說明，一律使用繁體中文（台灣用語）。使用「專案、元件、資料、建立、預設、載入、登入、連結、儲存、影片」等台灣用語。保留品牌名稱、檔名、網址、API 識別字與可執行程式碼；HTML 語言設為 zh-Hant-TW。

讓互動元件可實際操作，並將狀態提供給輔助科技。具備可見的鍵盤焦點、清楚的欄位標示、減少動態效果，以及至少 44px 的觸控區域。參考視覺與可用性衝突時，作最小幅度的無障礙調整並記錄原因。在 390px、768px、1440px 寬度檢查版面，涵蓋繁體中文長標題、長內容、空白及錯誤狀態。金額、數量與日期依資料本身的幣別、單位及時區呈現，以 zh-TW 格式顯示，不擅自換算。最後交付完成的檔案、實際驗證結果與仍待確認的假設，不把未檢查項目宣稱為通過。
```

## 改造既有介面

```text
先閱讀隨附的 DESIGN.md，以 Stripe 的設計語言作為介面參考。重新設計選定頁面，同時保留路由、資料、行為與使用者可理解的意義。先確認頁面層級，再找出最少且可重複使用的設計變數與元件調整。以下構圖作為視覺方向，依現有頁面調整：製作支付基礎架構介紹頁，採輕字重大標題、節制的漸層頁首與實用交易示範。數字對齊並標為範例，以乾淨白色區段讓技術說明容易閱讀。

使用我的產品名稱、內容與資料格式，優先沿用專案現有元件及技術。開始製作樣式前，先將色彩、字體、間距與圓角整理為可重複使用的設計變數。指定字型無法取得時，使用可用的系統字型或開源字型，並說明替代方式。介面文案、按鈕、提示、錯誤訊息、圖片替代文字、註解與交付說明，一律使用繁體中文（台灣用語）。使用「專案、元件、資料、建立、預設、載入、登入、連結、儲存、影片」等台灣用語。保留品牌名稱、檔名、網址、API 識別字與可執行程式碼；HTML 語言設為 zh-Hant-TW。依完整元件群組套用變更，檢查其他頁面是否受影響，並說明調整前後的主要差異。

讓互動元件可實際操作，並將狀態提供給輔助科技。具備可見的鍵盤焦點、清楚的欄位標示、減少動態效果，以及至少 44px 的觸控區域。參考視覺與可用性衝突時，作最小幅度的無障礙調整並記錄原因。在 390px、768px、1440px 寬度檢查版面，涵蓋繁體中文長標題、長內容、空白及錯誤狀態。金額、數量與日期依資料本身的幣別、單位及時區呈現，以 zh-TW 格式顯示，不擅自換算。最後交付完成的檔案、實際驗證結果與仍待確認的假設，不把未檢查項目宣稱為通過。
```

## 逐次調整流程

1. 先指出一個可實際觀察的問題，例如層級不清或內容遭裁切。
2. 在 DESIGN.md 找到對應設計變數或元件規則，提出範圍明確的調整。
3. 套用調整，保留無關的路由與資料行為。
4. 檢查鍵盤焦點、窄版排版，以及代表性的內容與錯誤狀態。
5. 用繁體中文說明結果，以及刻意偏離參考外觀的原因。
