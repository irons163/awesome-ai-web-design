---
version: zh-TW-2026-10-15
language: zh-TW
name: "Webflow"
description: "大膽黑白區塊與亮藍色，配合精準版面結構。"

colors:
  primary: "#080808"
  on-primary: "#ffffff"
  ink: "#080808"
  ink-strong: "#222222"
  body: "#363636"
  body-mid: "#5a5a5a"
  mute: "#898989"
  mute-soft: "#ababab"
  hairline: "#d8d8d8"
  canvas: "#ffffff"
  accent-purple: "#7a3dff"
  accent-pink: "#ed52cb"
  accent-blue: "#3b89ff"
  accent-blue-deep: "#006acc"
  accent-blue-info: "#146ef5"
  accent-orange: "#ff6b00"
  accent-green: "#00d722"
  accent-yellow: "#ffae13"
  accent-red: "#ee1d36"

typography:
  display-xxl:
    fontFamily: WF Visual Sans Variable, Inter, system-ui, -apple-system, sans-serif
    fontSize: 80px
    fontWeight: 600
    lineHeight: 83.2px
    letterSpacing: -0.8px
  display-xl:
    fontFamily: WF Visual Sans Variable, Inter, system-ui, sans-serif
    fontSize: 56px
    fontWeight: 600
    lineHeight: 58.24px
  display-lg:
    fontFamily: WF Visual Sans Variable, Inter, system-ui, sans-serif
    fontSize: 44.8px
    fontWeight: 600
    lineHeight: 46.6px
  display-md:
    fontFamily: WF Visual Sans Variable, Inter, system-ui, sans-serif
    fontSize: 32px
    fontWeight: 500
    lineHeight: 41.6px
  display-sm:
    fontFamily: WF Visual Sans Variable, Inter, system-ui, sans-serif
    fontSize: 24px
    fontWeight: 500
    lineHeight: 31.2px
  display-xs:
    fontFamily: WF Visual Sans Variable, Inter, system-ui, sans-serif
    fontSize: 20px
    fontWeight: 500
    lineHeight: 28px
  eyebrow-uppercase:
    fontFamily: WF Visual Sans Variable, Inter, system-ui, sans-serif
    fontSize: 15px
    fontWeight: 500
    lineHeight: 19.5px
    letterSpacing: 1.5px
  eyebrow-uppercase-sm:
    fontFamily: WF Visual Sans Variable, Inter, system-ui, sans-serif
    fontSize: 12px
    fontWeight: 500
    lineHeight: 12px
    letterSpacing: 0.6px
  body-lg:
    fontFamily: WF Visual Sans Variable, Inter, system-ui, sans-serif
    fontSize: 28.8px
    fontWeight: 400
    lineHeight: 46.08px
    letterSpacing: -0.288px
  body-md:
    fontFamily: WF Visual Sans Variable, Inter, system-ui, sans-serif
    fontSize: 16px
    fontWeight: 400
    lineHeight: 25.6px
    letterSpacing: -0.16px
  body-md-strong:
    fontFamily: WF Visual Sans Variable, Inter, system-ui, sans-serif
    fontSize: 16px
    fontWeight: 500
    lineHeight: 25.6px
    letterSpacing: -0.16px
  body-sm:
    fontFamily: WF Visual Sans Variable, Inter, system-ui, sans-serif
    fontSize: 14px
    fontWeight: 400
    lineHeight: 22.4px
  body-sm-strong:
    fontFamily: WF Visual Sans Variable, Inter, system-ui, sans-serif
    fontSize: 14px
    fontWeight: 500
    lineHeight: 22.4px
  caption:
    fontFamily: WF Visual Sans Variable, Inter, system-ui, sans-serif
    fontSize: 12.8px
    fontWeight: 550
    lineHeight: 15.36px
  caption-mono:
    fontFamily: WFVisualSans-Mono, Inconsolata, ui-monospace, SFMono-Regular, Menlo, monospace
    fontSize: 12px
    fontWeight: 400
    lineHeight: 18px
  button-md:
    fontFamily: WF Visual Sans Variable, Inter, system-ui, sans-serif
    fontSize: 16px
    fontWeight: 500
    lineHeight: 25.6px
    letterSpacing: -0.16px

rounded:
  none: 0px
  xs: 2px
  sm: 4px
  md: 8px
  full: 9999px

spacing:
  xxs: 2px
  xs: 4px
  sm: 8px
  md: 12px
  lg: 16px
  xl: 20px
  2xl: 24px
  3xl: 32px

components:
  nav-bar:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.body-sm-strong}"
    padding: "{spacing.lg} {spacing.3xl}"
  nav-link:
    textColor: "{colors.ink}"
    typography: "{typography.body-sm-strong}"
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.button-md}"
    rounded: "{rounded.sm}"
    padding: "{spacing.md} {spacing.xl}"
  button-secondary:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    borderColor: "{colors.hairline}"
    typography: "{typography.button-md}"
    rounded: "{rounded.sm}"
    padding: "{spacing.md} {spacing.xl}"
  button-text-arrow:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.button-md}"
    padding: "{spacing.xl} 0"
  button-icon-circular:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    rounded: "{rounded.full}"
    padding: "{spacing.sm}"
  text-input:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    borderColor: "{colors.hairline}"
    typography: "{typography.body-md}"
    rounded: "{rounded.sm}"
    padding: "{spacing.md} {spacing.lg}"
  badge-info:
    backgroundColor: "{colors.accent-blue-info}"
    textColor: "{colors.on-primary}"
    typography: "{typography.caption}"
    rounded: "{rounded.sm}"
    padding: "{spacing.xs} {spacing.sm}"
  badge-info-soft:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.accent-blue-info}"
    typography: "{typography.caption}"
    rounded: "{rounded.sm}"
    padding: "{spacing.xs} {spacing.sm}"
  card-feature:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    borderColor: "{colors.hairline}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: "{spacing.3xl}"
  card-feature-dark:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: "{spacing.3xl}"
  card-pricing:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    borderColor: "{colors.hairline}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: "{spacing.3xl}"
  hero-band:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.display-xxl}"
    padding: "{spacing.3xl} {spacing.3xl}"
  hero-band-dark:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.display-xxl}"
    padding: "{spacing.3xl} {spacing.3xl}"
  content-band:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.display-lg}"
    padding: "{spacing.3xl} {spacing.3xl}"
  category-card-purple:
    backgroundColor: "{colors.accent-purple}"
    textColor: "{colors.on-primary}"
    typography: "{typography.display-md}"
    rounded: "{rounded.md}"
    padding: "{spacing.3xl}"
  category-card-blue:
    backgroundColor: "{colors.accent-blue}"
    textColor: "{colors.on-primary}"
    typography: "{typography.display-md}"
    rounded: "{rounded.md}"
    padding: "{spacing.3xl}"
  category-card-orange:
    backgroundColor: "{colors.accent-orange}"
    textColor: "{colors.on-primary}"
    typography: "{typography.display-md}"
    rounded: "{rounded.md}"
    padding: "{spacing.3xl}"
  category-card-green:
    backgroundColor: "{colors.accent-green}"
    textColor: "{colors.primary}"
    typography: "{typography.display-md}"
    rounded: "{rounded.md}"
    padding: "{spacing.3xl}"
  category-card-pink:
    backgroundColor: "{colors.accent-pink}"
    textColor: "{colors.on-primary}"
    typography: "{typography.display-md}"
    rounded: "{rounded.md}"
    padding: "{spacing.3xl}"
  footer:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.body-mid}"
    typography: "{typography.body-sm}"
    padding: "{spacing.3xl} {spacing.3xl}"

  ex-pricing-tier:
    description: "Default Pricing tier card. Re-uses feature-card chrome with brand canvas-soft surface."
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    borderColor: "{colors.hairline}"
    rounded: "{rounded.md}"
    padding: "{spacing.3xl}"
  ex-pricing-tier-featured:
    description: "Featured/highlighted tier — polarity-flipped surface (dark fill + light text in light mode, light fill + dark text in dark mode)."
    backgroundColor: "{colors.ink}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.md}"
    padding: "{spacing.3xl}"
  ex-product-selector:
    description: "What's Included summary card — re-purposed for SaaS / B2B verticals (NOT a literal product gallery)."
    backgroundColor: "{colors.canvas}"
    rounded: "{rounded.md}"
    padding: "{spacing.3xl}"
  ex-cart-drawer:
    description: "Subscription summary — re-purposed for SaaS / B2B (line items per add-on, not literal cart)."
    backgroundColor: "{colors.canvas}"
    rounded: "{rounded.md}"
    padding: "{spacing.2xl}"
    item-divider: "{colors.hairline}"
  ex-app-shell-row:
    description: "Sidebar nav row inside the App Shell example. Active state uses brand primary as the indicator."
    backgroundColor: "{colors.canvas}"
    activeIndicator: "{colors.primary}"
    rounded: "{rounded.sm}"
    padding: "{spacing.md} {spacing.lg}"
  ex-data-table-cell:
    description: "Default data-table th + td chrome. Header uses mono-caps eyebrow typography; body uses body-sm."
    headerBackground: "{colors.canvas}"
    headerTypography: "{typography.caption}"
    bodyTypography: "{typography.body-sm}"
    cellPadding: "{spacing.md} {spacing.lg}"
    rowBorder: "{colors.hairline}"
  ex-auth-form-card:
    description: "Sign-in / sign-up card. Re-uses feature-card chrome with text-input primitives inside."
    backgroundColor: "{colors.canvas}"
    rounded: "{rounded.md}"
    padding: "{spacing.3xl}"
  ex-modal-card:
    description: "Modal dialog surface — same chrome as feature-card with elevated shadow."
    backgroundColor: "{colors.canvas}"
    rounded: "{rounded.md}"
    padding: "{spacing.3xl}"
  ex-empty-state-card:
    description: "Empty-state illustration frame."
    backgroundColor: "{colors.canvas}"
    rounded: "{rounded.md}"
    padding: "{spacing.3xl}"
    captionTypography: "{typography.body-md}"
  ex-toast:
    description: "Toast notification surface — feature-card shape + medium shadow."
    backgroundColor: "{colors.canvas}"
    rounded: "{rounded.md}"
    padding: "{spacing.md} {spacing.lg}"
    typography: "{typography.body-sm}"
---

# Webflow 延伸設計規格

語言：繁體中文（台灣用語，zh-TW）。在地化更新：2026-11-01。

## 來源與規格層次

這份規格將較早保存的品牌設計資料重新整理為可實作的繁體中文文件。來源設定中的色碼、字級、字重、行高、間距、圓角與元件識別字保留，供開發工具讀取；敘述與操作指令改用台灣用語。這些延伸設定不等同於目前日期限定首頁的逐項實測值，若兩者不同，依下方的日期限定觀察及對應預覽判讀。

- 原始資料版本：`1a783491c9539c3153c2fc96c16d59131e024f4e`。
- 原始 DESIGN.md 摘要：`0bd8e7d15828df524290873b2ad6cd6a97c366daffc1b802527e9882e1640395`。
- 目前首頁參考日期：2026-10-11。
- 目前公開來源：https://webflow.com/。
- 目前預覽：`official-drafts/webflow.html`。
- 台灣繁體中文規格與指令是本次重新產出的內容；來源截圖及原生生成紀錄保留原貌。

## 整體視覺方向

大膽黑白區塊與亮藍色，配合精準版面結構。

製作視覺化網站建置工具總覽，包含畫布預覽、元件導覽與精簡發布檢查清單。藍色用於編輯情境與有效操作，清楚區分畫布內容及應用程式控制項。

先建立主要內容、輔助資訊與操作之間的層級，再套用色彩及裝飾。品牌色應有明確用途；主要操作、選取、錯誤及停用狀態要能分辨。避免將多套參考風格混在同一頁，也不要僅替換通用卡片的顏色。

## 色彩、字型與繁體中文排版

上方來源設定保留原始色彩角色與數值。主要品牌色用於最重要的操作；背景、內容表面、主要文字、次要文字與分隔線各自維持一致用途。資訊不能只依賴顏色，狀態須同時有文字或圖示標示。

原字型名稱可作為拉丁字母參考。繁體中文字型優先使用可取得的 `Noto Sans TC`、`PingFang TC`、`Microsoft JhengHei`，最後才使用 `sans-serif`。原字型未涵蓋中文時必須提供替代，不以缺字或圖片文字呈現正文。專有字型無法取得時，記錄替代字型與可能的字寬差異。

中文標題以語意分段，避免為模仿英文大寫字距而拉散中文字。內文行高、欄寬與段落間距以可讀性為準；英文型號、網址、程式碼及長連結可以換行或在自己的區域捲動，不可撐開整份文件。價格、規格及比較欄位保持數字與單位對齊。

| 字級 | 字重 | 行高 | 字距 |
| --- | --- | --- | --- |
| 80px | 600 | 83.2px | -0.8px |
| 56px | 600 | 58.24px | 0 |
| 44.8px | 600 | 46.6px | 0 |
| 32px | 500 | 41.6px | 0 |
| 24px | 500 | 31.2px | 0 |
| 20px | 500 | 28px | 0 |
| 15px | 500 | 19.5px | 1.5px |
| 12px | 500 | 12px | 0.6px |
| 28.8px | 400 | 46.08px | -0.288px |
| 16px | 400 | 25.6px | -0.16px |
| 16px | 500 | 25.6px | -0.16px |
| 14px | 400 | 22.4px | 0 |
| 14px | 500 | 22.4px | 0 |
| 12.8px | 550 | 15.36px | 0 |
| 12px | 400 | 18px | 0 |
| 16px | 500 | 25.6px | -0.16px |

## 版面與元件結構

此參考可先實作：元件導覽資料列，包含巢狀層級、顯示狀態與鍵盤焦點。

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

- `#080808`
- `#7a3dff`
- `#ed52cb`
- `#3b89ff`
- `#ff6b00`
- `#00d722`
- `#006acc`
- `#146ef5`
- `#ffae13`
- `#ee1d36`
- `#ffffff`
- `#d8d8d8`
- `#222222`
- `#363636`
- `#5a5a5a`
- `#898989`
- `#ababab`
- `0 84px 24px rgba(0,0,0,0), 0 54px 22px rgba(0,0,0,0.01), 0 30px 18px rgba(0,0,0,0.04), 0 13px 13px rgba(0,0,0,0.08), 0 3px 7px rgba(0,0,0,0.09)`
- `0 24px 24px rgba(0,0,0,0.26), 0 6px 13px rgba(0,0,0,0.29)`

## 日期限定首頁觀察

來源 https://webflow.com/，實際觀察與最後校正2026-10-11。黑底、WF Visual Sans Variable 字型與藍色品牌CTA，46px Conf26公告列加68px黏性導覽。主標 打造下一個可能，桌面字級74.8571px、行高77.8514px；窄版置中兩行。依序保留行銷成果拼貼、真實客戶商標、Introducing Source視覺、四項能力、300,000+品牌六張客戶卡、目前新的 將網站化為成長引擎 六欄表單、Dyson編輯器原圖、Recent updates三張、#MadeinWebflow作品及完整目錄頁尾。成果數字只記錄官方當日公開呈現，未作金融或成效背書。

原保存版本銷售區文案不同，因此使用 原生 Google Stitch MCP 產生新的桌面校正稿，完整回應、原始HTML、原始縮圖及全尺寸PNG均分開保留。供應者自行更改部分資料意思，沒有當作已驗證來源。具體頁面以完整當日官方DOM/CSS及226份公開原素材校正。WebGL空白在實際比較中被找出，已用官方原始作品圖與觀察到的角度/位置恢復為靜態CSS展示；不是以整頁截圖冒充頁面。

1280×720桌面10段及390×844窄版12段，來源與最後校正版均實際逐視窗完整拍攝，PIL實際尺寸與上下覆蓋檢查完成。全部4張桌面及5張窄版比較圖目視檢查。頁高7188/9466完全相合，主標與頁尾位置相合；兩尺寸194張DOM圖片載入、字型完成、無水平溢位。來源20個WebGL-held空src節點由GPU渲染，校正版從記錄的公開held URL恢復圖片；Bing追蹤像素移除。

## 已知差異與驗證範圍

- 官網主視覺跑馬燈持續移動，依來源校正的頁面保留擷取位置，因此不同截圖時間的左右卡片位置不同。
- WebGL 的 #MadeinWebflow 圖庫，以精確記錄的公開圖片與 DOM 變形重建為靜態 CSS 替代。桌面角度及配置符合已記錄階段；窄版水平位置因官網捲動移動而不同。GPU 動態、滑鼠移入變暗、開啟卡片及專案對話框尚未重現或驗收。
- 選單、使用者類型選擇、客戶輪播、影片播放與對話框、Cookie、完整鍵盤焦點及其他互動狀態，未在主要畫面比對中驗收。來源是在拒絕全部 Cookie 後擷取，未送出外部表單。
- 業務洽詢表單為唯讀；帳戶、聯絡業務、註冊、其他路由、真實手機與其他寬度不在本次範圍，原始比對也未涵蓋正式部署。
- 新 Stitch 修正版僅為桌面。供應者改動部分資料、標題與商標描述；最終校正版使用實際來源紀錄，未宣稱有新原生行動版修正。

以上限制沿用原參考日期的比對紀錄。本次繁體中文整理不會把未驗證的影片、動畫、服務或尺寸改標為已通過；目前預覽仍未宣稱與官方完全一致。
<!-- Original AI instructions: awesome-ai-web-design -->

## 來源與使用範圍

資料來源與適用授權集中於專案根目錄的 ATTRIBUTION.md 與 LICENSE。品牌名稱僅用於識別參考來源，並非官方授權或服務。下方 AI 指令由本專案獨立撰寫；若既有互動備註與無障礙要求衝突，以此處的可用性檢查為準。

## 重新撰寫的 AI 任務指令

語言：繁體中文（台灣用語，zh-TW）。將 DESIGN.md 放入專案，再選擇下方任務。這些指令由本專案重新撰寫；請把示範內容替換為自己的產品需求。

## 建立新頁面

```text
先閱讀隨附的 DESIGN.md，以 Webflow 的設計語言作為介面參考。請完成以下可操作頁面：製作視覺化網站建置工具總覽，包含畫布預覽、元件導覽與精簡發布檢查清單。藍色用於編輯情境與有效操作，清楚區分畫布內容及應用程式控制項。

使用我的產品名稱、內容與資料格式，優先沿用專案現有元件及技術。開始製作樣式前，先將色彩、字體、間距與圓角整理為可重複使用的設計變數。指定字型無法取得時，使用可用的系統字型或開源字型，並說明替代方式。介面文案、按鈕、提示、錯誤訊息、圖片替代文字、註解與交付說明，一律使用繁體中文（台灣用語）。使用「專案、元件、資料、建立、預設、載入、登入、連結、儲存、影片」等台灣用語。保留品牌名稱、檔名、網址、API 識別字與可執行程式碼；HTML 語言設為 zh-Hant-TW。

讓互動元件可實際操作，並將狀態提供給輔助科技。具備可見的鍵盤焦點、清楚的欄位標示、減少動態效果，以及至少 44px 的觸控區域。參考視覺與可用性衝突時，作最小幅度的無障礙調整並記錄原因。在 390px、768px、1440px 寬度檢查版面，涵蓋繁體中文長標題、長內容、空白及錯誤狀態。金額、數量與日期依資料本身的幣別、單位及時區呈現，以 zh-TW 格式顯示，不擅自換算。最後交付完成的檔案、實際驗證結果與仍待確認的假設，不把未檢查項目宣稱為通過。
```

## 製作元件

```text
先閱讀隨附的 DESIGN.md，以 Webflow 的設計語言作為介面參考。請製作元件導覽資料列，包含巢狀層級、顯示狀態與鍵盤焦點。沿用現有元件慣例，放入精簡且符合實際情境的範例。比例與資訊層級應來自參考規格，不能只替通用卡片換色。依需求支援預設、焦點、停用、載入與錯誤狀態。使用有意義的示範資料，讓每個可見操作都有明確結果。

使用我的產品名稱、內容與資料格式，優先沿用專案現有元件及技術。開始製作樣式前，先將色彩、字體、間距與圓角整理為可重複使用的設計變數。指定字型無法取得時，使用可用的系統字型或開源字型，並說明替代方式。介面文案、按鈕、提示、錯誤訊息、圖片替代文字、註解與交付說明，一律使用繁體中文（台灣用語）。使用「專案、元件、資料、建立、預設、載入、登入、連結、儲存、影片」等台灣用語。保留品牌名稱、檔名、網址、API 識別字與可執行程式碼；HTML 語言設為 zh-Hant-TW。

讓互動元件可實際操作，並將狀態提供給輔助科技。具備可見的鍵盤焦點、清楚的欄位標示、減少動態效果，以及至少 44px 的觸控區域。參考視覺與可用性衝突時，作最小幅度的無障礙調整並記錄原因。在 390px、768px、1440px 寬度檢查版面，涵蓋繁體中文長標題、長內容、空白及錯誤狀態。金額、數量與日期依資料本身的幣別、單位及時區呈現，以 zh-TW 格式顯示，不擅自換算。最後交付完成的檔案、實際驗證結果與仍待確認的假設，不把未檢查項目宣稱為通過。
```

## 改造既有介面

```text
先閱讀隨附的 DESIGN.md，以 Webflow 的設計語言作為介面參考。重新設計選定頁面，同時保留路由、資料、行為與使用者可理解的意義。先確認頁面層級，再找出最少且可重複使用的設計變數與元件調整。以下構圖作為視覺方向，依現有頁面調整：製作視覺化網站建置工具總覽，包含畫布預覽、元件導覽與精簡發布檢查清單。藍色用於編輯情境與有效操作，清楚區分畫布內容及應用程式控制項。

使用我的產品名稱、內容與資料格式，優先沿用專案現有元件及技術。開始製作樣式前，先將色彩、字體、間距與圓角整理為可重複使用的設計變數。指定字型無法取得時，使用可用的系統字型或開源字型，並說明替代方式。介面文案、按鈕、提示、錯誤訊息、圖片替代文字、註解與交付說明，一律使用繁體中文（台灣用語）。使用「專案、元件、資料、建立、預設、載入、登入、連結、儲存、影片」等台灣用語。保留品牌名稱、檔名、網址、API 識別字與可執行程式碼；HTML 語言設為 zh-Hant-TW。依完整元件群組套用變更，檢查其他頁面是否受影響，並說明調整前後的主要差異。

讓互動元件可實際操作，並將狀態提供給輔助科技。具備可見的鍵盤焦點、清楚的欄位標示、減少動態效果，以及至少 44px 的觸控區域。參考視覺與可用性衝突時，作最小幅度的無障礙調整並記錄原因。在 390px、768px、1440px 寬度檢查版面，涵蓋繁體中文長標題、長內容、空白及錯誤狀態。金額、數量與日期依資料本身的幣別、單位及時區呈現，以 zh-TW 格式顯示，不擅自換算。最後交付完成的檔案、實際驗證結果與仍待確認的假設，不把未檢查項目宣稱為通過。
```

## 逐次調整流程

1. 先指出一個可實際觀察的問題，例如層級不清或內容遭裁切。
2. 在 DESIGN.md 找到對應設計變數或元件規則，提出範圍明確的調整。
3. 套用調整，保留無關的路由與資料行為。
4. 檢查鍵盤焦點、窄版排版，以及代表性的內容與錯誤狀態。
5. 用繁體中文說明結果，以及刻意偏離參考外觀的原因。
