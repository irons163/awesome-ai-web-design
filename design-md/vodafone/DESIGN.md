---
version: zh-TW-2026-10-15
language: zh-TW
name: "Vodafone"
description: "紅色章節與大字標題，清楚傳達服務。"

colors:
  primary: "#e60000"
  on-primary: "#ffffff"
  ink: "#25282b"
  body: "#7e7e7e"
  mute: "#bebebe"
  canvas: "#ffffff"
  canvas-soft: "#f2f2f2"
  on-dark: "#ffffff"

typography:
  display-hero:
    fontFamily: Vodafone, Vodafone Rg, Helvetica Neue, Arial, sans-serif
    fontSize: 144px
    fontWeight: 800
    lineHeight: 114px
    letterSpacing: -1px
  display-xxl:
    fontFamily: Vodafone, Vodafone Rg, Helvetica Neue, Arial, sans-serif
    fontSize: 126px
    fontWeight: 800
    lineHeight: 113px
    letterSpacing: -1px
  display-xl:
    fontFamily: Vodafone, Vodafone Rg, Helvetica Neue, Arial, sans-serif
    fontSize: 90px
    fontWeight: 800
    lineHeight: 84px
  display-lg:
    fontFamily: Vodafone, Vodafone Rg, Helvetica Neue, Arial, sans-serif
    fontSize: 48px
    fontWeight: 300
    lineHeight: 52px
  display-md:
    fontFamily: Vodafone, Vodafone Rg, Helvetica Neue, Arial, sans-serif
    fontSize: 40px
    fontWeight: 300
    lineHeight: 44px
  display-sm:
    fontFamily: Vodafone, Vodafone Rg, Helvetica Neue, Arial, sans-serif
    fontSize: 32px
    fontWeight: 700
    lineHeight: 40px
  display-xs:
    fontFamily: Vodafone, Vodafone Rg, Helvetica Neue, Arial, sans-serif
    fontSize: 24px
    fontWeight: 700
    lineHeight: 24px
  eyebrow-uppercase:
    fontFamily: Vodafone, Vodafone Rg, Helvetica Neue, Arial, sans-serif
    fontSize: 16px
    fontWeight: 800
    lineHeight: 24px
  body-lg:
    fontFamily: Vodafone, Vodafone Rg, Helvetica Neue, Arial, sans-serif
    fontSize: 22px
    fontWeight: 400
    lineHeight: 24px
  body-md:
    fontFamily: Vodafone, Vodafone Rg, Helvetica Neue, Arial, sans-serif
    fontSize: 18px
    fontWeight: 400
    lineHeight: 28px
  body-md-strong:
    fontFamily: Vodafone, Vodafone Rg, Helvetica Neue, Arial, sans-serif
    fontSize: 18px
    fontWeight: 600
    lineHeight: 28px
  body-sm:
    fontFamily: Vodafone, Vodafone Rg, Helvetica Neue, Arial, sans-serif
    fontSize: 16px
    fontWeight: 400
    lineHeight: 20px
  body-sm-strong:
    fontFamily: Vodafone, Vodafone Rg, Helvetica Neue, Arial, sans-serif
    fontSize: 16px
    fontWeight: 700
    lineHeight: 22px
  caption:
    fontFamily: Vodafone, Vodafone Rg, Helvetica Neue, Arial, sans-serif
    fontSize: 14px
    fontWeight: 400
    lineHeight: 16px
  caption-strong:
    fontFamily: Vodafone, Vodafone Rg, Helvetica Neue, Arial, sans-serif
    fontSize: 14px
    fontWeight: 700
    lineHeight: 21px
  caption-uppercase:
    fontFamily: Vodafone, Vodafone Rg, Helvetica Neue, Arial, sans-serif
    fontSize: 12px
    fontWeight: 600
    lineHeight: 16px
    letterSpacing: 0.5691px
  button-md:
    fontFamily: Vodafone, Vodafone Rg, Helvetica Neue, Arial, sans-serif
    fontSize: 18px
    fontWeight: 400
    lineHeight: 28px

rounded:
  none: 0px
  xs: 1px
  sm: 6px
  card: 6px
  pill-md: 32px
  pill-lg: 60px
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
    backgroundColor: "{colors.ink}"
    textColor: "{colors.on-dark}"
    typography: "{typography.body-sm}"
    padding: "{spacing.lg} {spacing.3xl}"
  nav-link:
    textColor: "{colors.on-dark}"
    typography: "{typography.body-sm}"
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    borderColor: "{colors.primary}"
    typography: "{typography.button-md}"
    rounded: "{rounded.pill-lg}"
    padding: "{spacing.md} {spacing.2xl}"
  button-outline-red:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.primary}"
    borderColor: "{colors.primary}"
    typography: "{typography.button-md}"
    rounded: "{rounded.pill-lg}"
    padding: "{spacing.md} {spacing.2xl}"
  button-outline-dark:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    borderColor: "{colors.ink}"
    typography: "{typography.button-md}"
    rounded: "{rounded.pill-lg}"
    padding: "{spacing.md} {spacing.2xl}"
  button-icon-circular:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    borderColor: "{colors.canvas}"
    rounded: "{rounded.full}"
  text-input:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    borderColor: "{colors.ink}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.sm}"
    padding: "{spacing.md} {spacing.lg}"
  badge-chip:
    backgroundColor: "{colors.canvas-soft}"
    textColor: "{colors.ink}"
    typography: "{typography.caption-strong}"
    rounded: "{rounded.pill-md}"
    padding: "{spacing.xs} {spacing.md}"
  card-content:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.card}"
    padding: "{spacing.lg}"
  card-hero:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.display-sm}"
    rounded: "{rounded.card}"
    padding: "{spacing.lg}"
  hero-band-dark:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.on-dark}"
    typography: "{typography.display-hero}"
    padding: "{spacing.3xl} {spacing.3xl}"
  hero-band-red:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.display-xl}"
    padding: "{spacing.3xl} {spacing.3xl}"
  content-band-light:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.display-md}"
    padding: "{spacing.3xl} {spacing.3xl}"
  speechmark-logo-orb:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.sm}"
  divider-on-dark:
    borderColor: "{colors.on-dark}"
  footer:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.on-dark}"
    typography: "{typography.body-sm}"
    padding: "{spacing.3xl} {spacing.3xl}"

  ex-pricing-tier:
    description: "Default tier card. Mirrors card-content chrome with canvas-soft surface and a hairline border."
    backgroundColor: "{colors.canvas-soft}"
    textColor: "{colors.ink}"
    borderColor: "{colors.mute}"
    rounded: "{rounded.card}"
    padding: "{spacing.lg}"
  ex-pricing-tier-featured:
    description: "Featured tier — polarity-flipped to ink with white text and white pill CTA inside."
    backgroundColor: "{colors.ink}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.card}"
    padding: "{spacing.lg}"
  ex-product-selector:
    description: "Tariff-tier picker — repurposed as the brand's plan selector with badge-chip chips inside the frame."
    backgroundColor: "{colors.canvas-soft}"
    rounded: "{rounded.card}"
    padding: "{spacing.lg}"
  ex-cart-drawer:
    description: "Subscription summary — line items per tariff add-on, light hairline dividers."
    backgroundColor: "{colors.canvas}"
    rounded: "{rounded.card}"
    padding: "{spacing.lg}"
    item-divider: "{colors.mute}"
  ex-app-shell-row:
    description: "Sidebar nav row. Active state uses brand primary as a left-edge indicator bar."
    backgroundColor: "{colors.canvas}"
    activeIndicator: "{colors.primary}"
    rounded: "{rounded.sm}"
    padding: "{spacing.md} {spacing.lg}"
  ex-data-table-cell:
    description: "Default data-table cell chrome. Header uses caption-uppercase mono-style eyebrow; body uses body-sm."
    headerBackground: "{colors.canvas-soft}"
    headerTypography: "{typography.caption-uppercase}"
    bodyTypography: "{typography.body-sm}"
    cellPadding: "{spacing.md} {spacing.lg}"
    rowBorder: "{colors.mute}"
  ex-auth-form-card:
    description: "Sign-in / sign-up card. Mirrors card-content chrome with text-input primitives inside."
    backgroundColor: "{colors.canvas-soft}"
    rounded: "{rounded.card}"
    padding: "{spacing.lg}"
  ex-modal-card:
    description: "Modal dialog surface — same chrome as card-content; brand uses scrim, not card shadow."
    backgroundColor: "{colors.canvas}"
    rounded: "{rounded.card}"
    padding: "{spacing.lg}"
  ex-empty-state-card:
    description: "Empty-state illustration frame on canvas-soft with generous interior padding."
    backgroundColor: "{colors.canvas-soft}"
    rounded: "{rounded.card}"
    padding: "{spacing.3xl}"
    captionTypography: "{typography.body-md}"
  ex-toast:
    description: "Toast notification surface — card-content shape with caption-strong body."
    backgroundColor: "{colors.canvas}"
    rounded: "{rounded.sm}"
    padding: "{spacing.md} {spacing.lg}"
    typography: "{typography.body-sm}"
---

# Vodafone 延伸設計規格

語言：繁體中文（台灣用語，zh-TW）。在地化更新：2026-10-20。

## 來源與規格層次

這份規格將較早保存的品牌設計資料重新整理為可實作的繁體中文文件。來源設定中的色碼、字級、字重、行高、間距、圓角與元件識別字保留，供開發工具讀取；敘述與操作指令改用台灣用語。這些延伸設定不等同於目前日期限定首頁的逐項實測值，若兩者不同，依下方的日期限定觀察及對應預覽判讀。

- 原始資料版本：`1a783491c9539c3153c2fc96c16d59131e024f4e`。
- 原始 DESIGN.md 摘要：`1e0bc6dab7a86c6ef361d18ffa22502f0dcc5e8040b7987c79e12d213bd4ef57`。
- 目前首頁參考日期：2026-10-13。
- 目前公開來源：https://www.vodafone.com/。
- 目前預覽：`official-drafts/vodafone.html`。
- 台灣繁體中文規格與指令是本次重新產出的內容；來源截圖及原生生成紀錄保留原貌。

## 整體視覺方向

紅色章節與大字標題，清楚傳達服務。

製作連線服務介紹頁，包含鮮明紅色章節、涵蓋範圍說明與裝置支援格線。內文使用穩定中性背景，以簡短具標示的比較取代密集徽章。

先建立主要內容、輔助資訊與操作之間的層級，再套用色彩及裝飾。品牌色應有明確用途；主要操作、選取、錯誤及停用狀態要能分辨。避免將多套參考風格混在同一頁，也不要僅替換通用卡片的顏色。

## 色彩、字型與繁體中文排版

上方來源設定保留原始色彩角色與數值。主要品牌色用於最重要的操作；背景、內容表面、主要文字、次要文字與分隔線各自維持一致用途。資訊不能只依賴顏色，狀態須同時有文字或圖示標示。

原字型名稱可作為拉丁字母參考。繁體中文字型優先使用可取得的 `Noto Sans TC`、`PingFang TC`、`Microsoft JhengHei`，最後才使用 `sans-serif`。原字型未涵蓋中文時必須提供替代，不以缺字或圖片文字呈現正文。專有字型無法取得時，記錄替代字型與可能的字寬差異。

中文標題以語意分段，避免為模仿英文大寫字距而拉散中文字。內文行高、欄寬與段落間距以可讀性為準；英文型號、網址、程式碼及長連結可以換行或在自己的區域捲動，不可撐開整份文件。價格、規格及比較欄位保持數字與單位對齊。

| 字級 | 字重 | 行高 | 字距 |
| --- | --- | --- | --- |
| 144px | 800 | 114px | -1px |
| 126px | 800 | 113px | -1px |
| 90px | 800 | 84px | 0 |
| 48px | 300 | 52px | 0 |
| 40px | 300 | 44px | 0 |
| 32px | 700 | 40px | 0 |
| 24px | 700 | 24px | 0 |
| 16px | 800 | 24px | 0 |
| 22px | 400 | 24px | 0 |
| 18px | 400 | 28px | 0 |
| 18px | 600 | 28px | 0 |
| 16px | 400 | 20px | 0 |
| 16px | 700 | 22px | 0 |
| 14px | 400 | 16px | 0 |
| 14px | 700 | 21px | 0 |
| 12px | 600 | 16px | 0.57px |
| 18px | 400 | 28px | 0 |

## 版面與元件結構

此參考可先實作：連線特色卡片，包含速度單位、可用範圍說明與詳細資訊切換。

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

- `#e60000`
- `#ffffff`
- `#f2f2f2`
- `#25282b`
- `#7e7e7e`
- `#bebebe`
- `-1px`
- `letter-spacing: -1px`

## 日期限定首頁觀察

參考日期：2026-10-13。來源：https://www.vodafone.com/

依已保存的預覽、畫面量測與同日期比對紀錄整理；文件整理日期為 2026-10-14，未重新擷取官網。

## 版面與層級

這份分析對應目前保存的 Vodafone 公開首頁研究。頁面以品牌導覽、EVERYONE. CONNECTED 大型主視覺、連結主題區、新聞重點、企業／投資資訊和頁尾形成主要順序。

主視覺與 people／businesses／continents／futures 的連結訊息使用大型文字與寬幅圖像。新聞區以重複圖文卡片維持密度，企業或投資資料則以較短資訊群組呈現。

## 視覺規則

品牌紅、黑、白形成主要對比。保存的字型為 Vodafone；1280px 量測中主要文字約 115.4px，News highlights 約 45px，新聞卡片標題約 23.1px。這些數字只適用於已記錄的桌面尺寸，窄版需依自身可讀性規則調整。

使用原始品牌素材與寬幅比例，重點放在大字、空間與圖文關係。目前預覽直接呈現進場動畫結束狀態，以免靜態頁面留下空白；這個安排不代表影片與動畫時序已完成驗收。

## 窄版與使用

既有 390px 研究重新排列導覽、新聞卡片與資訊區，紀錄沒有水平溢出。窄版選單與 Escape 關閉已檢查，但與官網選單外觀的對等性尚未建立。股價、新聞與資料日期是保存時內容；實作時標明資料時間，並讓選單、搜尋及資料載入具有可辨識狀態。

## 已知差異與參考紀錄

- 草稿直接顯示進場動畫的結束狀態；影片影格、播放時序與原站動畫尚未驗收。
- 新聞卡片、股價與資料日期和目前官網不同，草稿中的數字不是即時資料。
- 官網選單開啟外觀的對等性尚未建立；其他選單、搜尋、頁尾折疊、輪播、其他尺寸及正式部署仍待驗收。

比對紀錄：[Vodafone 畫面校正紀錄](vodafone-oct13-visual-review.md)。目前預覽：[Vodafone](vodafone.html)。

## 已知差異與驗證範圍

- 草稿直接顯示進場動畫的結束狀態；影片影格、播放時序與原站動畫尚未驗收。
- 新聞卡片、股價與資料日期和目前官網不同，草稿中的數字不是即時資料。
- 官網選單開啟外觀的對等性尚未建立；其他選單、搜尋、頁尾折疊、輪播、其他尺寸及正式部署仍待驗收。

以上限制沿用原參考日期的比對紀錄。本次繁體中文整理不會把未驗證的影片、動畫、服務或尺寸改標為已通過；目前預覽仍未宣稱與官方完全一致。
<!-- Original AI instructions: awesome-ai-web-design -->

## 來源與使用範圍

設計資料改寫自採 MIT 授權的 VoltAgent/awesome-design-md，詳見 LICENSE 與 ATTRIBUTION.md。品牌名稱僅用於識別參考來源，並非官方授權或服務。下方 AI 指令由本專案獨立撰寫；若既有互動備註與無障礙要求衝突，以此處的可用性檢查為準。

## 重新撰寫的 AI 任務指令

語言：繁體中文（台灣用語，zh-TW）。將 DESIGN.md 放入專案，再選擇下方任務。這些指令由本專案重新撰寫；請把示範內容替換為自己的產品需求。

## 建立新頁面

```text
先閱讀隨附的 DESIGN.md，以 Vodafone 的設計語言作為介面參考。請完成以下可操作頁面：製作連線服務介紹頁，包含鮮明紅色章節、涵蓋範圍說明與裝置支援格線。內文使用穩定中性背景，以簡短具標示的比較取代密集徽章。

使用我的產品名稱、內容與資料格式，優先沿用專案現有元件及技術。開始製作樣式前，先將色彩、字體、間距與圓角整理為可重複使用的設計變數。指定字型無法取得時，使用可用的系統字型或開源字型，並說明替代方式。介面文案、按鈕、提示、錯誤訊息、圖片替代文字、註解與交付說明，一律使用繁體中文（台灣用語）。使用「專案、元件、資料、建立、預設、載入、登入、連結、儲存、影片」等台灣用語。保留品牌名稱、檔名、網址、API 識別字與可執行程式碼；HTML 語言設為 zh-Hant-TW。

讓互動元件可實際操作，並將狀態提供給輔助科技。具備可見的鍵盤焦點、清楚的欄位標示、減少動態效果，以及至少 44px 的觸控區域。參考視覺與可用性衝突時，作最小幅度的無障礙調整並記錄原因。在 390px、768px、1440px 寬度檢查版面，涵蓋繁體中文長標題、長內容、空白及錯誤狀態。金額、數量與日期依資料本身的幣別、單位及時區呈現，以 zh-TW 格式顯示，不擅自換算。最後交付完成的檔案、實際驗證結果與仍待確認的假設，不把未檢查項目宣稱為通過。
```

## 製作元件

```text
先閱讀隨附的 DESIGN.md，以 Vodafone 的設計語言作為介面參考。請製作連線特色卡片，包含速度單位、可用範圍說明與詳細資訊切換。沿用現有元件慣例，放入精簡且符合實際情境的範例。比例與資訊層級應來自參考規格，不能只替通用卡片換色。依需求支援預設、焦點、停用、載入與錯誤狀態。使用有意義的示範資料，讓每個可見操作都有明確結果。

使用我的產品名稱、內容與資料格式，優先沿用專案現有元件及技術。開始製作樣式前，先將色彩、字體、間距與圓角整理為可重複使用的設計變數。指定字型無法取得時，使用可用的系統字型或開源字型，並說明替代方式。介面文案、按鈕、提示、錯誤訊息、圖片替代文字、註解與交付說明，一律使用繁體中文（台灣用語）。使用「專案、元件、資料、建立、預設、載入、登入、連結、儲存、影片」等台灣用語。保留品牌名稱、檔名、網址、API 識別字與可執行程式碼；HTML 語言設為 zh-Hant-TW。

讓互動元件可實際操作，並將狀態提供給輔助科技。具備可見的鍵盤焦點、清楚的欄位標示、減少動態效果，以及至少 44px 的觸控區域。參考視覺與可用性衝突時，作最小幅度的無障礙調整並記錄原因。在 390px、768px、1440px 寬度檢查版面，涵蓋繁體中文長標題、長內容、空白及錯誤狀態。金額、數量與日期依資料本身的幣別、單位及時區呈現，以 zh-TW 格式顯示，不擅自換算。最後交付完成的檔案、實際驗證結果與仍待確認的假設，不把未檢查項目宣稱為通過。
```

## 改造既有介面

```text
先閱讀隨附的 DESIGN.md，以 Vodafone 的設計語言作為介面參考。重新設計選定頁面，同時保留路由、資料、行為與使用者可理解的意義。先確認頁面層級，再找出最少且可重複使用的設計變數與元件調整。以下構圖作為視覺方向，依現有頁面調整：製作連線服務介紹頁，包含鮮明紅色章節、涵蓋範圍說明與裝置支援格線。內文使用穩定中性背景，以簡短具標示的比較取代密集徽章。

使用我的產品名稱、內容與資料格式，優先沿用專案現有元件及技術。開始製作樣式前，先將色彩、字體、間距與圓角整理為可重複使用的設計變數。指定字型無法取得時，使用可用的系統字型或開源字型，並說明替代方式。介面文案、按鈕、提示、錯誤訊息、圖片替代文字、註解與交付說明，一律使用繁體中文（台灣用語）。使用「專案、元件、資料、建立、預設、載入、登入、連結、儲存、影片」等台灣用語。保留品牌名稱、檔名、網址、API 識別字與可執行程式碼；HTML 語言設為 zh-Hant-TW。依完整元件群組套用變更，檢查其他頁面是否受影響，並說明調整前後的主要差異。

讓互動元件可實際操作，並將狀態提供給輔助科技。具備可見的鍵盤焦點、清楚的欄位標示、減少動態效果，以及至少 44px 的觸控區域。參考視覺與可用性衝突時，作最小幅度的無障礙調整並記錄原因。在 390px、768px、1440px 寬度檢查版面，涵蓋繁體中文長標題、長內容、空白及錯誤狀態。金額、數量與日期依資料本身的幣別、單位及時區呈現，以 zh-TW 格式顯示，不擅自換算。最後交付完成的檔案、實際驗證結果與仍待確認的假設，不把未檢查項目宣稱為通過。
```

## 逐次調整流程

1. 先指出一個可實際觀察的問題，例如層級不清或內容遭裁切。
2. 在 DESIGN.md 找到對應設計變數或元件規則，提出範圍明確的調整。
3. 套用調整，保留無關的路由與資料行為。
4. 檢查鍵盤焦點、窄版排版，以及代表性的內容與錯誤狀態。
5. 用繁體中文說明結果，以及刻意偏離參考外觀的原因。
