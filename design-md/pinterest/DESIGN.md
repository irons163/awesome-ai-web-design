---
version: zh-TW-2026-10-15
language: zh-TW
name: "Pinterest"
description: "紅色操作與瀑布流，讓視覺收藏容易瀏覽。"

colors:
  primary: "#e60023"
  on-primary: "#ffffff"
  primary-pressed: "#cc001f"
  ink: "#000000"
  ink-soft: "#211922"
  body: "#33332e"
  charcoal: "#262622"
  mute: "#62625b"
  ash: "#91918c"
  stone: "#c8c8c1"
  hairline: "#dadad3"
  hairline-soft: "#e5e5e0"
  on-secondary: "#000000"
  secondary-bg: "#e5e5e0"
  secondary-pressed: "#c8c8c1"
  canvas: "#ffffff"
  surface-soft: "#fbfbf9"
  surface-card: "#f6f6f3"
  surface-elevated: "#ffffff"
  on-dark: "#ffffff"
  on-dark-mute: "rgba(255,255,255,0.7)"
  surface-dark: "#262622"
  focus-outer: "#435ee5"
  focus-inner: "#ffffff"
  accent-pressed-blue: "#617bff"
  accent-purple: "#7e238b"
  accent-purple-deep: "#6845ab"
  success-deep: "#103c25"
  success-pale: "#c7f0da"
  error: "#9e0a0a"
  error-deep: "#cc001f"

typography:
  display-xl:
    fontFamily: Pin Sans
    fontSize: 70px
    fontWeight: 600
    lineHeight: 1.1
    letterSpacing: -1.2px
  display-lg:
    fontFamily: Pin Sans
    fontSize: 44px
    fontWeight: 700
    lineHeight: 1.15
    letterSpacing: -0.8px
  heading-xl:
    fontFamily: Pin Sans
    fontSize: 28px
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: -1.2px
  heading-lg:
    fontFamily: Pin Sans
    fontSize: 22px
    fontWeight: 600
    lineHeight: 1.25
    letterSpacing: 0
  heading-md:
    fontFamily: Pin Sans
    fontSize: 18px
    fontWeight: 600
    lineHeight: 1.3
    letterSpacing: 0
  body-md:
    fontFamily: Pin Sans
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.4
    letterSpacing: 0
  body-strong:
    fontFamily: Pin Sans
    fontSize: 16px
    fontWeight: 600
    lineHeight: 1.4
    letterSpacing: 0
  body-sm:
    fontFamily: Pin Sans
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.4
    letterSpacing: 0
  body-sm-strong:
    fontFamily: Pin Sans
    fontSize: 14px
    fontWeight: 700
    lineHeight: 1.4
    letterSpacing: 0
  caption-md:
    fontFamily: Pin Sans
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1.5
    letterSpacing: 0
  caption-sm:
    fontFamily: Pin Sans
    fontSize: 12px
    fontWeight: 400
    lineHeight: 1.4
    letterSpacing: 0
  link-md:
    fontFamily: Pin Sans
    fontSize: 16px
    fontWeight: 600
    lineHeight: 1.4
    letterSpacing: 0
  button-md:
    fontFamily: Pin Sans
    fontSize: 14px
    fontWeight: 700
    lineHeight: 1
    letterSpacing: 0
  button-sm:
    fontFamily: Pin Sans
    fontSize: 12px
    fontWeight: 700
    lineHeight: 1
    letterSpacing: 0

rounded:
  none: 0px
  sm: 8px
  md: 16px
  lg: 32px
  full: 9999px

spacing:
  xxs: 4px
  xs: 6px
  sm: 8px
  md: 12px
  lg: 16px
  xl: 24px
  xxl: 32px
  section: 64px

components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.button-md}"
    rounded: "{rounded.md}"
    padding: 6px 14px
    height: 40px
  button-primary-pressed:
    backgroundColor: "{colors.primary-pressed}"
    textColor: "{colors.on-primary}"
    typography: "{typography.button-md}"
    rounded: "{rounded.md}"
  button-secondary:
    backgroundColor: "{colors.secondary-bg}"
    textColor: "{colors.on-secondary}"
    typography: "{typography.button-md}"
    rounded: "{rounded.md}"
    padding: 6px 14px
    height: 40px
  button-secondary-pressed:
    backgroundColor: "{colors.secondary-pressed}"
    textColor: "{colors.on-secondary}"
    typography: "{typography.button-md}"
    rounded: "{rounded.md}"
  button-tertiary:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    typography: "{typography.button-md}"
    rounded: "{rounded.md}"
  button-icon-circular:
    backgroundColor: "{colors.surface-card}"
    textColor: "{colors.ink}"
    rounded: "{rounded.full}"
    size: 40px
  button-pill-on-image:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.button-md}"
    rounded: "{rounded.full}"
    padding: 8px 14px
  button-disabled:
    backgroundColor: "{colors.surface-card}"
    textColor: "{colors.ash}"
    rounded: "{rounded.md}"
  search-bar:
    backgroundColor: "{colors.surface-card}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.full}"
    padding: 11px 15px
    height: 48px
  search-bar-focused:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    rounded: "{rounded.full}"
  text-input:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: 11px 15px
    height: 44px
  text-input-focused:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
  pin-card:
    backgroundColor: "{colors.surface-card}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
    padding: 0px
  pin-card-large:
    backgroundColor: "{colors.surface-card}"
    textColor: "{colors.ink}"
    rounded: "{rounded.lg}"
    padding: 0px
  pin-overlay-pill:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.button-sm}"
    rounded: "{rounded.full}"
    padding: 6px 12px
  filter-chip:
    backgroundColor: "{colors.surface-card}"
    textColor: "{colors.ink}"
    typography: "{typography.button-md}"
    rounded: "{rounded.full}"
    padding: 8px 16px
  filter-chip-active:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.on-dark}"
    typography: "{typography.button-md}"
    rounded: "{rounded.full}"
  category-tile:
    backgroundColor: "{colors.surface-card}"
    textColor: "{colors.ink}"
    typography: "{typography.body-strong}"
    rounded: "{rounded.md}"
    padding: 16px
  feature-card:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.heading-xl}"
    rounded: "{rounded.md}"
    padding: 32px
  feature-card-soft:
    backgroundColor: "{colors.surface-card}"
    textColor: "{colors.ink}"
    typography: "{typography.heading-xl}"
    rounded: "{rounded.md}"
    padding: 32px
  modal-card:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.lg}"
    padding: 32px
  hero-cta-strip:
    backgroundColor: "{colors.surface-dark}"
    textColor: "{colors.on-dark}"
    typography: "{typography.heading-xl}"
    rounded: "{rounded.none}"
    padding: 48px 32px
  primary-nav:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.body-strong}"
    rounded: "{rounded.none}"
    height: 64px
  footer-section:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.mute}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.none}"
    padding: 32px 24px
  link-inline:
    textColor: "{colors.ink-soft}"
    typography: "{typography.link-md}"
---

# Pinterest 延伸設計規格

語言：繁體中文（台灣用語，zh-TW）。在地化更新：2026-11-01。

## 來源與規格層次

這份規格將較早保存的品牌設計資料重新整理為可實作的繁體中文文件。來源設定中的色碼、字級、字重、行高、間距、圓角與元件識別字保留，供開發工具讀取；敘述與操作指令改用台灣用語。這些延伸設定不等同於目前日期限定首頁的逐項實測值，若兩者不同，依下方的日期限定觀察及對應預覽判讀。

- 原始資料版本：`1a783491c9539c3153c2fc96c16d59131e024f4e`。
- 原始 DESIGN.md 摘要：`6d5bbad0f676d7a4c8d535fea0da0f52b2be1491ea6afc2c48e706ca8c6ae765`。
- 目前首頁參考日期：2026-10-13。
- 目前公開來源：https://www.pinterest.com/。
- 目前預覽：`official-drafts/pinterest.html`。
- 台灣繁體中文規格與指令是本次重新產出的內容；來源截圖及原生生成紀錄保留原貌。

## 整體視覺方向

紅色操作與瀑布流，讓視覺收藏容易瀏覽。

製作視覺靈感圖版，包含不同高度的圖片卡片、具名稱的主題篩選與儲存至圖版的互動。紅色用於關鍵操作，瀑布流切換為手機版時仍維持閱讀順序。

先建立主要內容、輔助資訊與操作之間的層級，再套用色彩及裝飾。品牌色應有明確用途；主要操作、選取、錯誤及停用狀態要能分辨。避免將多套參考風格混在同一頁，也不要僅替換通用卡片的顏色。

## 色彩、字型與繁體中文排版

上方來源設定保留原始色彩角色與數值。主要品牌色用於最重要的操作；背景、內容表面、主要文字、次要文字與分隔線各自維持一致用途。資訊不能只依賴顏色，狀態須同時有文字或圖示標示。

原字型名稱可作為拉丁字母參考。繁體中文字型優先使用可取得的 `Noto Sans TC`、`PingFang TC`、`Microsoft JhengHei`，最後才使用 `sans-serif`。原字型未涵蓋中文時必須提供替代，不以缺字或圖片文字呈現正文。專有字型無法取得時，記錄替代字型與可能的字寬差異。

中文標題以語意分段，避免為模仿英文大寫字距而拉散中文字。內文行高、欄寬與段落間距以可讀性為準；英文型號、網址、程式碼及長連結可以換行或在自己的區域捲動，不可撐開整份文件。價格、規格及比較欄位保持數字與單位對齊。

| 字級 | 字重 | 行高 | 字距 |
| --- | --- | --- | --- |
| 70px | 600 | 1.1 | -1.2px |
| 44px | 700 | 1.15 | -0.8px |
| 28px | 700 | 1.2 | -1.2px |
| 22px | 600 | 1.25 | 0 |
| 18px | 600 | 1.3 | 0 |
| 16px | 400 | 1.4 | 0 |
| 16px | 600 | 1.4 | 0 |
| 14px | 400 | 1.4 | 0 |
| 14px | 700 | 1.4 | 0 |
| 12px | 500 | 1.5 | 0 |
| 12px | 400 | 1.4 | 0 |
| 16px | 600 | 1.4 | 0 |
| 14px | 700 | 1 | 0 |
| 12px | 700 | 1 | 0 |

## 版面與元件結構

此參考可先實作：靈感卡片，包含可見標題、圖片說明與儲存狀態回饋。

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

- `#e60023`
- `#cc001f`
- `#ffffff`
- `#fbfbf9`
- `#f6f6f3`
- `#e5e5e0`
- `#c8c8c1`
- `#262622`
- `#dadad3`
- `#000000`
- `#211922`
- `#33332e`
- `#62625b`
- `#91918c`
- `#9e0a0a`
- `#103c25`
- `#c7f0da`
- `#435ee5`
- `#617bff`
- `#7e238b`
- `#6845ab`
- `6px 14px`
- `8px 14px`
- `8px 16px`
- `11px 15px`
- `6px 12px`
- `48px 32px`
- `32px 24px`

## 日期限定首頁觀察

參考：https://www.pinterest.com/，本次公開、未登入繁體中文首頁。完整畫面為1280×720與390×844瀏覽器視窗；不等同真實手機驗收。

桌面以80px導覽起始，紅色Pinterest標誌、探索入口、搜尋欄與登入／註冊構成主要操作。生活靈感主視覺採文字與照片拼貼雙欄，白底、黑色大標題與紅色主按鈕維持清楚層級。

接續區塊使用淡米色至白色漸層，先呈現「狂歡萬聖節，從這裡開始」與大型季節拼貼，再接圖版輪播。拼貼為原始官方圖片，不以重新排版的小圖替代；輪播卡片包含三張預覽圖、圖版標題、擁有者與Pin數量。

功能介紹由「將你喜愛的點子化為真實」引入，再以交錯雙欄呈現膚色搜尋、群組圖版與視覺搜尋。圖片維持正方形與大圓角，正文留白較多，紅色操作按鈕置於短說明下方。底部以生活照片拼貼為背景，覆蓋深色遮罩、白色註冊卡片，最後接黑色頁尾。

保留觀察到的Pin Sans字型與系統中文字型替代、原始SVG標誌、圖片、圓角與間距。原始素材以來源網址、位元組數及SHA-256保存；原生Stitch匯出另存，未由工作草稿覆寫。

官網在390px桌面瀏覽器仍保留800px文件並裁切。草稿因此獨立採導覽兩列、主視覺與功能圖文堆疊、完整可讀的表單及頁尾。此調整已公開記錄，不能作為與官網手機版一致的證據。完整差異與驗證範圍見同日期畫面校正紀錄。

## 已知差異與驗證範圍

- 390px 官網保留800px文件並裁切；草稿採390px堆疊、較小主標題、兩列導覽、完整可讀表單與頁尾，屬明確的可用性調整，不能宣稱窄版像素一致。
- 僅保存1280×720、390×844公開未登入首頁的完整畫面；320px、768px只檢查圖片載入與水平溢出。真實行動裝置、行動版使用者代理及其他尺寸尚未驗收。
- 輪播已檢查前進、返回、Home／End及邊界停用；全部中間狀態、觸控拖曳、減少動態偏好、完整鍵盤焦點及輔助技術尚未完整驗收。
- 搜尋、自動完成、登入／註冊、日期／密碼輔助控制與商家帳號流程未重建或驗收；帳號欄位唯讀，主要帳號操作前往官方網站，未嵌入即時帳號框架。
- 桌面主要區塊、文字與版面高度已對齊本次日期參考；不同裝置的字型替代、細微點陣差異、動畫與後續官網內容變動不在完全一致聲明範圍。

以上限制沿用原參考日期的比對紀錄。本次繁體中文整理不會把未驗證的影片、動畫、服務或尺寸改標為已通過；目前預覽仍未宣稱與官方完全一致。
<!-- Original AI instructions: awesome-ai-web-design -->

## 來源與使用範圍

資料來源與適用授權集中於專案根目錄的 ATTRIBUTION.md 與 LICENSE。品牌名稱僅用於識別參考來源，並非官方授權或服務。下方 AI 指令由本專案獨立撰寫；若既有互動備註與無障礙要求衝突，以此處的可用性檢查為準。

## 重新撰寫的 AI 任務指令

語言：繁體中文（台灣用語，zh-TW）。將 DESIGN.md 放入專案，再選擇下方任務。這些指令由本專案重新撰寫；請把示範內容替換為自己的產品需求。

## 建立新頁面

```text
先閱讀隨附的 DESIGN.md，以 Pinterest 的設計語言作為介面參考。請完成以下可操作頁面：製作視覺靈感圖版，包含不同高度的圖片卡片、具名稱的主題篩選與儲存至圖版的互動。紅色用於關鍵操作，瀑布流切換為手機版時仍維持閱讀順序。

使用我的產品名稱、內容與資料格式，優先沿用專案現有元件及技術。開始製作樣式前，先將色彩、字體、間距與圓角整理為可重複使用的設計變數。指定字型無法取得時，使用可用的系統字型或開源字型，並說明替代方式。介面文案、按鈕、提示、錯誤訊息、圖片替代文字、註解與交付說明，一律使用繁體中文（台灣用語）。使用「專案、元件、資料、建立、預設、載入、登入、連結、儲存、影片」等台灣用語。保留品牌名稱、檔名、網址、API 識別字與可執行程式碼；HTML 語言設為 zh-Hant-TW。

讓互動元件可實際操作，並將狀態提供給輔助科技。具備可見的鍵盤焦點、清楚的欄位標示、減少動態效果，以及至少 44px 的觸控區域。參考視覺與可用性衝突時，作最小幅度的無障礙調整並記錄原因。在 390px、768px、1440px 寬度檢查版面，涵蓋繁體中文長標題、長內容、空白及錯誤狀態。金額、數量與日期依資料本身的幣別、單位及時區呈現，以 zh-TW 格式顯示，不擅自換算。最後交付完成的檔案、實際驗證結果與仍待確認的假設，不把未檢查項目宣稱為通過。
```

## 製作元件

```text
先閱讀隨附的 DESIGN.md，以 Pinterest 的設計語言作為介面參考。請製作靈感卡片，包含可見標題、圖片說明與儲存狀態回饋。沿用現有元件慣例，放入精簡且符合實際情境的範例。比例與資訊層級應來自參考規格，不能只替通用卡片換色。依需求支援預設、焦點、停用、載入與錯誤狀態。使用有意義的示範資料，讓每個可見操作都有明確結果。

使用我的產品名稱、內容與資料格式，優先沿用專案現有元件及技術。開始製作樣式前，先將色彩、字體、間距與圓角整理為可重複使用的設計變數。指定字型無法取得時，使用可用的系統字型或開源字型，並說明替代方式。介面文案、按鈕、提示、錯誤訊息、圖片替代文字、註解與交付說明，一律使用繁體中文（台灣用語）。使用「專案、元件、資料、建立、預設、載入、登入、連結、儲存、影片」等台灣用語。保留品牌名稱、檔名、網址、API 識別字與可執行程式碼；HTML 語言設為 zh-Hant-TW。

讓互動元件可實際操作，並將狀態提供給輔助科技。具備可見的鍵盤焦點、清楚的欄位標示、減少動態效果，以及至少 44px 的觸控區域。參考視覺與可用性衝突時，作最小幅度的無障礙調整並記錄原因。在 390px、768px、1440px 寬度檢查版面，涵蓋繁體中文長標題、長內容、空白及錯誤狀態。金額、數量與日期依資料本身的幣別、單位及時區呈現，以 zh-TW 格式顯示，不擅自換算。最後交付完成的檔案、實際驗證結果與仍待確認的假設，不把未檢查項目宣稱為通過。
```

## 改造既有介面

```text
先閱讀隨附的 DESIGN.md，以 Pinterest 的設計語言作為介面參考。重新設計選定頁面，同時保留路由、資料、行為與使用者可理解的意義。先確認頁面層級，再找出最少且可重複使用的設計變數與元件調整。以下構圖作為視覺方向，依現有頁面調整：製作視覺靈感圖版，包含不同高度的圖片卡片、具名稱的主題篩選與儲存至圖版的互動。紅色用於關鍵操作，瀑布流切換為手機版時仍維持閱讀順序。

使用我的產品名稱、內容與資料格式，優先沿用專案現有元件及技術。開始製作樣式前，先將色彩、字體、間距與圓角整理為可重複使用的設計變數。指定字型無法取得時，使用可用的系統字型或開源字型，並說明替代方式。介面文案、按鈕、提示、錯誤訊息、圖片替代文字、註解與交付說明，一律使用繁體中文（台灣用語）。使用「專案、元件、資料、建立、預設、載入、登入、連結、儲存、影片」等台灣用語。保留品牌名稱、檔名、網址、API 識別字與可執行程式碼；HTML 語言設為 zh-Hant-TW。依完整元件群組套用變更，檢查其他頁面是否受影響，並說明調整前後的主要差異。

讓互動元件可實際操作，並將狀態提供給輔助科技。具備可見的鍵盤焦點、清楚的欄位標示、減少動態效果，以及至少 44px 的觸控區域。參考視覺與可用性衝突時，作最小幅度的無障礙調整並記錄原因。在 390px、768px、1440px 寬度檢查版面，涵蓋繁體中文長標題、長內容、空白及錯誤狀態。金額、數量與日期依資料本身的幣別、單位及時區呈現，以 zh-TW 格式顯示，不擅自換算。最後交付完成的檔案、實際驗證結果與仍待確認的假設，不把未檢查項目宣稱為通過。
```

## 逐次調整流程

1. 先指出一個可實際觀察的問題，例如層級不清或內容遭裁切。
2. 在 DESIGN.md 找到對應設計變數或元件規則，提出範圍明確的調整。
3. 套用調整，保留無關的路由與資料行為。
4. 檢查鍵盤焦點、窄版排版，以及代表性的內容與錯誤狀態。
5. 用繁體中文說明結果，以及刻意偏離參考外觀的原因。
