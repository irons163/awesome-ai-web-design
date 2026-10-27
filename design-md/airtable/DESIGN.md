---
version: zh-TW-2026-10-15
language: zh-TW
name: "Airtable"
description: "彩色分區，把複雜資訊整理清楚。"

colors:
  primary: "#181d26"
  primary-active: "#0d1218"
  ink: "#181d26"
  body: "#333840"
  muted: "#41454d"
  hairline: "#dddddd"
  border-strong: "#9297a0"
  canvas: "#ffffff"
  surface-soft: "#f8fafc"
  surface-strong: "#e0e2e6"
  surface-dark: "#181d26"
  surface-dark-elevated: "#1d1f25"
  signature-coral: "#aa2d00"
  signature-forest: "#0a2e0e"
  signature-cream: "#f5e9d4"
  signature-peach: "#fcab79"
  signature-mint: "#a8d8c4"
  signature-yellow: "#f4d35e"
  signature-mustard: "#d9a441"
  on-primary: "#ffffff"
  on-dark: "#ffffff"
  link: "#1b61c9"
  link-active: "#1a3866"
  info: "#254fad"
  info-border: "#458fff"
  success: "#006400"
  success-border: "#39bf45"
  pricing-ink: "#1d1f25"

typography:
  display-xl:
    fontFamily: "Haas Groot Disp, Haas, sans-serif"
    fontSize: 48px
    fontWeight: 500
    lineHeight: 1.1
    letterSpacing: 0
  display-lg:
    fontFamily: "Haas Groot Disp, Haas, sans-serif"
    fontSize: 40px
    fontWeight: 400
    lineHeight: 1.2
    letterSpacing: 0
  display-md:
    fontFamily: "Haas Groot Disp, Haas, sans-serif"
    fontSize: 32px
    fontWeight: 400
    lineHeight: 1.2
    letterSpacing: 0
  title-lg:
    fontFamily: "Haas, sans-serif"
    fontSize: 24px
    fontWeight: 400
    lineHeight: 1.35
    letterSpacing: 0.12px
  title-md:
    fontFamily: "Haas Groot Disp, Haas, sans-serif"
    fontSize: 20px
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: 0
  title-sm:
    fontFamily: "Haas, sans-serif"
    fontSize: 18px
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: 0
  label-md:
    fontFamily: "Haas, sans-serif"
    fontSize: 16px
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: 0
  button:
    fontFamily: "Haas, sans-serif"
    fontSize: 16px
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: 0
  body-md:
    fontFamily: "Haas, sans-serif"
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.25
    letterSpacing: 0
  caption:
    fontFamily: "Haas, sans-serif"
    fontSize: 14px
    fontWeight: 500
    lineHeight: 1.35
    letterSpacing: 0.16px
  legal:
    fontFamily: "Haas, sans-serif"
    fontSize: 13.12px
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: 0
  pricing-display:
    fontFamily: "Inter Display, system-ui, sans-serif"
    fontSize: 44.8px
    fontWeight: 475
    lineHeight: 1.1
    letterSpacing: 0
  pricing-section:
    fontFamily: "Inter Display, system-ui, sans-serif"
    fontSize: 28px
    fontWeight: 475
    lineHeight: 1.2
    letterSpacing: 0
  pricing-card-title:
    fontFamily: "Inter Display, system-ui, sans-serif"
    fontSize: 20px
    fontWeight: 475
    lineHeight: 1.3
    letterSpacing: 0

rounded:
  xs: 2px
  sm: 6px
  md: 10px
  lg: 12px
  pill: 9999px
  full: 9999px

spacing:
  xxs: 4px
  xs: 8px
  sm: 12px
  md: 16px
  lg: 24px
  xl: 32px
  xxl: 48px
  section: 96px

components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.button}"
    rounded: "{rounded.lg}"
    padding: 16px 24px
  button-primary-active:
    backgroundColor: "{colors.primary-active}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.lg}"
  button-secondary:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.button}"
    rounded: "{rounded.lg}"
    padding: 16px 24px
  button-secondary-on-dark:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.button}"
    rounded: "{rounded.lg}"
    padding: 16px 24px
  button-legal:
    backgroundColor: "{colors.link}"
    textColor: "{colors.on-primary}"
    typography: "{typography.legal}"
    rounded: "{rounded.xs}"
    padding: 12px 10px
  button-icon-circular:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    rounded: "{rounded.full}"
    size: 40px
  button-pricing-pill:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.pricing-ink}"
    typography: "{typography.button}"
    rounded: "{rounded.pill}"
    padding: 12px 24px
  text-link:
    backgroundColor: transparent
    textColor: "{colors.link}"
    typography: "{typography.body-md}"
  top-nav:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    height: 64px
  hero-band:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.display-lg}"
    padding: 96px
  signature-coral-card:
    backgroundColor: "{colors.signature-coral}"
    textColor: "{colors.on-primary}"
    typography: "{typography.display-md}"
    rounded: "{rounded.lg}"
    padding: 48px
  signature-forest-card:
    backgroundColor: "{colors.signature-forest}"
    textColor: "{colors.on-primary}"
    typography: "{typography.display-md}"
    rounded: "{rounded.lg}"
    padding: 48px
  hero-card-dark:
    backgroundColor: "{colors.surface-dark}"
    textColor: "{colors.on-dark}"
    typography: "{typography.display-md}"
    rounded: "{rounded.lg}"
    padding: 48px
  feature-card-tabbed:
    backgroundColor: "{colors.surface-soft}"
    textColor: "{colors.ink}"
    typography: "{typography.title-lg}"
    rounded: "{rounded.lg}"
    padding: 32px
  cream-callout-card:
    backgroundColor: "{colors.signature-cream}"
    textColor: "{colors.ink}"
    typography: "{typography.title-lg}"
    rounded: "{rounded.md}"
    padding: 24px
  demo-grid-card:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.label-md}"
    rounded: "{rounded.md}"
    padding: 16px
  logo-strip:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.muted}"
    typography: "{typography.body-md}"
    padding: 32px
  article-card:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.title-sm}"
    rounded: "{rounded.md}"
    padding: 16px
  topic-filter-rail:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.body}"
    typography: "{typography.body-md}"
    width: 240px
  text-input:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.sm}"
    padding: 12px 16px
    height: 44px
  text-input-focus:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
  pricing-tier-card:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.pricing-ink}"
    typography: "{typography.pricing-card-title}"
    rounded: "{rounded.md}"
    padding: 32px
  pricing-tier-card-featured:
    backgroundColor: "{colors.surface-soft}"
    textColor: "{colors.pricing-ink}"
    typography: "{typography.pricing-card-title}"
    rounded: "{rounded.md}"
    padding: 32px
  pricing-comparison-row:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.body}"
    typography: "{typography.body-md}"
    padding: 12px
  cta-band-light:
    backgroundColor: "{colors.surface-strong}"
    textColor: "{colors.ink}"
    typography: "{typography.display-md}"
    rounded: "{rounded.lg}"
    padding: 48px
  footer:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.body}"
    typography: "{typography.body-md}"
    padding: 64px
---

# Airtable 延伸設計規格

語言：繁體中文（台灣用語，zh-TW）。在地化更新：2026-10-20。

## 來源與規格層次

這份規格將較早保存的品牌設計資料重新整理為可實作的繁體中文文件。來源設定中的色碼、字級、字重、行高、間距、圓角與元件識別字保留，供開發工具讀取；敘述與操作指令改用台灣用語。這些延伸設定不等同於目前日期限定首頁的逐項實測值，若兩者不同，依下方的日期限定觀察及對應預覽判讀。

- 原始資料版本：`1a783491c9539c3153c2fc96c16d59131e024f4e`。
- 原始 DESIGN.md 摘要：`47cb6c71bc045459a5d1feb4e8b264ede2f2ebb01a3092be537fe7588370ffb3`。
- 目前首頁參考日期：2026-10-10。
- 目前公開來源：https://www.airtable.com/。
- 目前預覽：`official-drafts/airtable.html`。
- 台灣繁體中文規格與指令是本次重新產出的內容；來源截圖及原生生成紀錄保留原貌。

## 整體視覺方向

彩色分區，把複雜資訊整理清楚。

製作團隊規劃工作區，包含檢視切換、分組資料，以及可編輯的側邊詳細資料面板。使用分類色協助辨識，不要把每個儲存格都做成標籤；內容增加時仍須維持欄位對齊。

先建立主要內容、輔助資訊與操作之間的層級，再套用色彩及裝飾。品牌色應有明確用途；主要操作、選取、錯誤及停用狀態要能分辨。避免將多套參考風格混在同一頁，也不要僅替換通用卡片的顏色。

## 色彩、字型與繁體中文排版

上方來源設定保留原始色彩角色與數值。主要品牌色用於最重要的操作；背景、內容表面、主要文字、次要文字與分隔線各自維持一致用途。資訊不能只依賴顏色，狀態須同時有文字或圖示標示。

原字型名稱可作為拉丁字母參考。繁體中文字型優先使用可取得的 `Noto Sans TC`、`PingFang TC`、`Microsoft JhengHei`，最後才使用 `sans-serif`。原字型未涵蓋中文時必須提供替代，不以缺字或圖片文字呈現正文。專有字型無法取得時，記錄替代字型與可能的字寬差異。

中文標題以語意分段，避免為模仿英文大寫字距而拉散中文字。內文行高、欄寬與段落間距以可讀性為準；英文型號、網址、程式碼及長連結可以換行或在自己的區域捲動，不可撐開整份文件。價格、規格及比較欄位保持數字與單位對齊。

| 字級 | 字重 | 行高 | 字距 |
| --- | --- | --- | --- |
| 48px | 500 | 1.1 | 0 |
| 40px | 400 | 1.2 | 0 |
| 32px | 400 | 1.2 | 0 |
| 24px | 400 | 1.35 | 0.12px |
| 20px | 400 | 1.5 | 0 |
| 18px | 500 | 1.4 | 0 |
| 16px | 500 | 1.4 | 0 |
| 16px | 500 | 1.4 | 0 |
| 14px | 400 | 1.25 | 0 |
| 14px | 500 | 1.35 | 0.16px |
| 13.12px | 600 | 1.2 | 0 |
| 44.8px | 475 | 1.1 | 0 |
| 28px | 475 | 1.2 | 0 |
| 20px | 475 | 1.3 | 0 |

## 版面與元件結構

此參考可先實作：資料詳細資訊面板，包含清楚的欄位標示與儲存狀態。

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

- `--theme_button-background-primary: #1b61c9`

## 日期限定首頁觀察

參考：https://www.airtable.com/；觀察日期2026-10-10。原有 DESIGN.md 保留，此文件補充目前版本。

白色版面以黑色品牌、Neue Haas 字型與留白建立企業工具的秩序。上方淺藍公告列42px，桌面導覽80px；桌面主標題40/48px、窄版32/40px，兩個 CTA 在窄版垂直排列。

主要章節順序為工作流程影片、客戶標誌、四種能力、四色 AI Plays、三篇資源、eBay 客戶故事、註冊及頁尾。能力卡依序採磚紅、白色、淺藍與米色。桌面左側有固定章節導覽，窄版改為可水平捲動的列。

複製時須保留真實官方圖片、原始 SVG 與字型。不可用虛構資料表或自製圖示代替影片內容，也不可把文字座標相同等同完整一致。影片、選單狀態和互動差異列在相鄰驗證紀錄。

## 已知差異與驗證範圍

- 原始主視覺與 eBay 宣傳影片的畫格尚未同步；桌面截圖偶爾出現合成器造成的空白畫格。本機影片可播放，但截圖中的確切狀態尚未驗收。
- 捲動觸發位置、動畫時間及窄版章節列的水平移動仍有差異；精簡商標與基本章節標示已校正。
- 頁尾展開、Cookie 偏好設定、完整巢狀導覽、鍵盤焦點與窄版互動尚未完整驗證；窄版模擬的指標事件不穩定，因此不宣稱互動一致。
- 平板與中間寬度、真實行動裝置尚未驗證；原始比對未涵蓋正式頁面。

以上限制沿用原參考日期的比對紀錄。本次繁體中文整理不會把未驗證的影片、動畫、服務或尺寸改標為已通過；目前預覽仍未宣稱與官方完全一致。
<!-- Original AI instructions: awesome-ai-web-design -->

## 來源與使用範圍

設計資料改寫自採 MIT 授權的 VoltAgent/awesome-design-md，詳見 LICENSE 與 ATTRIBUTION.md。品牌名稱僅用於識別參考來源，並非官方授權或服務。下方 AI 指令由本專案獨立撰寫；若既有互動備註與無障礙要求衝突，以此處的可用性檢查為準。

## 重新撰寫的 AI 任務指令

語言：繁體中文（台灣用語，zh-TW）。將 DESIGN.md 放入專案，再選擇下方任務。這些指令由本專案重新撰寫；請把示範內容替換為自己的產品需求。

## 建立新頁面

```text
先閱讀隨附的 DESIGN.md，以 Airtable 的設計語言作為介面參考。請完成以下可操作頁面：製作團隊規劃工作區，包含檢視切換、分組資料，以及可編輯的側邊詳細資料面板。使用分類色協助辨識，不要把每個儲存格都做成標籤；內容增加時仍須維持欄位對齊。

使用我的產品名稱、內容與資料格式，優先沿用專案現有元件及技術。開始製作樣式前，先將色彩、字體、間距與圓角整理為可重複使用的設計變數。指定字型無法取得時，使用可用的系統字型或開源字型，並說明替代方式。介面文案、按鈕、提示、錯誤訊息、圖片替代文字、註解與交付說明，一律使用繁體中文（台灣用語）。使用「專案、元件、資料、建立、預設、載入、登入、連結、儲存、影片」等台灣用語。保留品牌名稱、檔名、網址、API 識別字與可執行程式碼；HTML 語言設為 zh-Hant-TW。

讓互動元件可實際操作，並將狀態提供給輔助科技。具備可見的鍵盤焦點、清楚的欄位標示、減少動態效果，以及至少 44px 的觸控區域。參考視覺與可用性衝突時，作最小幅度的無障礙調整並記錄原因。在 390px、768px、1440px 寬度檢查版面，涵蓋繁體中文長標題、長內容、空白及錯誤狀態。金額、數量與日期依資料本身的幣別、單位及時區呈現，以 zh-TW 格式顯示，不擅自換算。最後交付完成的檔案、實際驗證結果與仍待確認的假設，不把未檢查項目宣稱為通過。
```

## 製作元件

```text
先閱讀隨附的 DESIGN.md，以 Airtable 的設計語言作為介面參考。請製作資料詳細資訊面板，包含清楚的欄位標示與儲存狀態。沿用現有元件慣例，放入精簡且符合實際情境的範例。比例與資訊層級應來自參考規格，不能只替通用卡片換色。依需求支援預設、焦點、停用、載入與錯誤狀態。使用有意義的示範資料，讓每個可見操作都有明確結果。

使用我的產品名稱、內容與資料格式，優先沿用專案現有元件及技術。開始製作樣式前，先將色彩、字體、間距與圓角整理為可重複使用的設計變數。指定字型無法取得時，使用可用的系統字型或開源字型，並說明替代方式。介面文案、按鈕、提示、錯誤訊息、圖片替代文字、註解與交付說明，一律使用繁體中文（台灣用語）。使用「專案、元件、資料、建立、預設、載入、登入、連結、儲存、影片」等台灣用語。保留品牌名稱、檔名、網址、API 識別字與可執行程式碼；HTML 語言設為 zh-Hant-TW。

讓互動元件可實際操作，並將狀態提供給輔助科技。具備可見的鍵盤焦點、清楚的欄位標示、減少動態效果，以及至少 44px 的觸控區域。參考視覺與可用性衝突時，作最小幅度的無障礙調整並記錄原因。在 390px、768px、1440px 寬度檢查版面，涵蓋繁體中文長標題、長內容、空白及錯誤狀態。金額、數量與日期依資料本身的幣別、單位及時區呈現，以 zh-TW 格式顯示，不擅自換算。最後交付完成的檔案、實際驗證結果與仍待確認的假設，不把未檢查項目宣稱為通過。
```

## 改造既有介面

```text
先閱讀隨附的 DESIGN.md，以 Airtable 的設計語言作為介面參考。重新設計選定頁面，同時保留路由、資料、行為與使用者可理解的意義。先確認頁面層級，再找出最少且可重複使用的設計變數與元件調整。以下構圖作為視覺方向，依現有頁面調整：製作團隊規劃工作區，包含檢視切換、分組資料，以及可編輯的側邊詳細資料面板。使用分類色協助辨識，不要把每個儲存格都做成標籤；內容增加時仍須維持欄位對齊。

使用我的產品名稱、內容與資料格式，優先沿用專案現有元件及技術。開始製作樣式前，先將色彩、字體、間距與圓角整理為可重複使用的設計變數。指定字型無法取得時，使用可用的系統字型或開源字型，並說明替代方式。介面文案、按鈕、提示、錯誤訊息、圖片替代文字、註解與交付說明，一律使用繁體中文（台灣用語）。使用「專案、元件、資料、建立、預設、載入、登入、連結、儲存、影片」等台灣用語。保留品牌名稱、檔名、網址、API 識別字與可執行程式碼；HTML 語言設為 zh-Hant-TW。依完整元件群組套用變更，檢查其他頁面是否受影響，並說明調整前後的主要差異。

讓互動元件可實際操作，並將狀態提供給輔助科技。具備可見的鍵盤焦點、清楚的欄位標示、減少動態效果，以及至少 44px 的觸控區域。參考視覺與可用性衝突時，作最小幅度的無障礙調整並記錄原因。在 390px、768px、1440px 寬度檢查版面，涵蓋繁體中文長標題、長內容、空白及錯誤狀態。金額、數量與日期依資料本身的幣別、單位及時區呈現，以 zh-TW 格式顯示，不擅自換算。最後交付完成的檔案、實際驗證結果與仍待確認的假設，不把未檢查項目宣稱為通過。
```

## 逐次調整流程

1. 先指出一個可實際觀察的問題，例如層級不清或內容遭裁切。
2. 在 DESIGN.md 找到對應設計變數或元件規則，提出範圍明確的調整。
3. 套用調整，保留無關的路由與資料行為。
4. 檢查鍵盤焦點、窄版排版，以及代表性的內容與錯誤狀態。
5. 用繁體中文說明結果，以及刻意偏離參考外觀的原因。
