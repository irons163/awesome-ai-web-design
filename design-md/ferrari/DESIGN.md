---
version: zh-TW-2026-10-15
language: zh-TW
name: "Ferrari"
description: "黑白光影與克制的紅色，帶出速度感。"

colors:
  primary: "#da291c"
  primary-active: "#b01e0a"
  primary-hover: "#9d2211"
  ink: "#ffffff"
  body: "#969696"
  body-strong: "#ffffff"
  body-on-light: "#181818"
  muted: "#666666"
  muted-soft: "#8f8f8f"
  hairline: "#303030"
  hairline-on-light: "#d2d2d2"
  hairline-soft: "#ebebeb"
  canvas: "#181818"
  canvas-elevated: "#303030"
  canvas-light: "#ffffff"
  surface-card: "#303030"
  surface-soft-light: "#f7f7f7"
  surface-strong-light: "#ebebeb"
  on-primary: "#ffffff"
  on-dark: "#ffffff"
  on-light: "#181818"
  accent-yellow-hypersail: "#fff200"
  accent-yellow: "#f6e500"
  semantic-info: "#4c98b9"
  semantic-success: "#03904a"
  semantic-warning: "#f13a2c"

typography:
  display-mega:
    fontFamily: "'FerrariSans', -apple-system, system-ui, sans-serif"
    fontSize: 80px
    fontWeight: 500
    lineHeight: 1.05
    letterSpacing: -1.6px
  display-xl:
    fontFamily: "'FerrariSans', sans-serif"
    fontSize: 56px
    fontWeight: 500
    lineHeight: 1.1
    letterSpacing: -1.12px
  display-lg:
    fontFamily: "'FerrariSans', sans-serif"
    fontSize: 36px
    fontWeight: 500
    lineHeight: 1.2
    letterSpacing: -0.36px
  display-md:
    fontFamily: "'FerrariSans', sans-serif"
    fontSize: 26px
    fontWeight: 500
    lineHeight: 1.5
    letterSpacing: 0.195px
  title-md:
    fontFamily: "'FerrariSans', sans-serif"
    fontSize: 18px
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: 0
  title-sm:
    fontFamily: "'FerrariSans', sans-serif"
    fontSize: 16px
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: 0.08px
  body-md:
    fontFamily: "'FerrariSans', sans-serif"
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: 0
  body-sm:
    fontFamily: "'FerrariSans', sans-serif"
    fontSize: 13px
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: 0
  caption:
    fontFamily: "'FerrariSans', sans-serif"
    fontSize: 12px
    fontWeight: 400
    lineHeight: 1.4
    letterSpacing: 0
  caption-uppercase:
    fontFamily: "'FerrariSans', sans-serif"
    fontSize: 11px
    fontWeight: 600
    lineHeight: 1.4
    letterSpacing: 1.1px
    textTransform: uppercase
  button:
    fontFamily: "'FerrariSans', sans-serif"
    fontSize: 14px
    fontWeight: 700
    lineHeight: 1.0
    letterSpacing: 1.4px
    textTransform: uppercase
  nav-link:
    fontFamily: "'FerrariSans', sans-serif"
    fontSize: 13px
    fontWeight: 600
    lineHeight: 1.4
    letterSpacing: 0.65px
    textTransform: uppercase
  number-display:
    fontFamily: "'FerrariSans', sans-serif"
    fontSize: 80px
    fontWeight: 700
    lineHeight: 1.0
    letterSpacing: -1.6px

rounded:
  none: 0px
  xs: 2px
  sm: 4px
  md: 6px
  lg: 8px
  xl: 12px
  full: 9999px

spacing:
  xxxs: 4px
  xxs: 8px
  xs: 16px
  sm: 24px
  md: 32px
  lg: 48px
  xl: 64px
  xxl: 96px
  super: 128px

components:
  top-nav-on-dark:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.nav-link}"
    height: 64px
  top-nav-on-light:
    backgroundColor: "{colors.canvas-light}"
    textColor: "{colors.body-on-light}"
    typography: "{typography.nav-link}"
    height: 64px
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.button}"
    rounded: "{rounded.none}"
    padding: 14px 32px
    height: 48px
  button-primary-active:
    backgroundColor: "{colors.primary-active}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.none}"
  button-outline-on-dark:
    backgroundColor: transparent
    textColor: "{colors.ink}"
    typography: "{typography.button}"
    rounded: "{rounded.none}"
    padding: 13px 31px
    height: 48px
  button-outline-on-light:
    backgroundColor: transparent
    textColor: "{colors.body-on-light}"
    typography: "{typography.button}"
    rounded: "{rounded.none}"
    padding: 13px 31px
    height: 48px
  button-tertiary-text:
    backgroundColor: transparent
    textColor: "{colors.ink}"
    typography: "{typography.button}"
  hero-band-cinema:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.display-mega}"
    padding: 0
  hero-band-light:
    backgroundColor: "{colors.canvas-light}"
    textColor: "{colors.body-on-light}"
    typography: "{typography.display-xl}"
    padding: 96px
  feature-card-photo:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.title-md}"
    rounded: "{rounded.none}"
    padding: 0
  feature-card-light:
    backgroundColor: "{colors.canvas-light}"
    textColor: "{colors.body-on-light}"
    typography: "{typography.title-md}"
    rounded: "{rounded.none}"
    padding: 32px
  livery-band:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.ink}"
    typography: "{typography.display-lg}"
    padding: 96px
  preowned-listing-card:
    backgroundColor: "{colors.canvas-light}"
    textColor: "{colors.body-on-light}"
    typography: "{typography.body-md}"
    rounded: "{rounded.none}"
    padding: 24px
  spec-cell:
    backgroundColor: transparent
    textColor: "{colors.ink}"
    typography: "{typography.number-display}"
    padding: 24px 0
  race-position-cell:
    backgroundColor: transparent
    textColor: "{colors.primary}"
    typography: "{typography.number-display}"
  race-calendar-row:
    backgroundColor: transparent
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    padding: 16px 0
  driver-card:
    backgroundColor: "{colors.canvas-elevated}"
    textColor: "{colors.ink}"
    typography: "{typography.title-md}"
    rounded: "{rounded.none}"
    padding: 24px
  text-input-on-dark:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.sm}"
    padding: 14px 16px
    height: 48px
  text-input-on-light:
    backgroundColor: "{colors.canvas-light}"
    textColor: "{colors.body-on-light}"
    typography: "{typography.body-md}"
    rounded: "{rounded.sm}"
    padding: 14px 16px
    height: 48px
  badge-pill:
    backgroundColor: "{colors.canvas-elevated}"
    textColor: "{colors.ink}"
    typography: "{typography.caption-uppercase}"
    rounded: "{rounded.full}"
    padding: 4px 12px
  cta-band-dark:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.display-lg}"
    padding: 96px
  newsletter-input-band:
    backgroundColor: "{colors.canvas-elevated}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.sm}"
    padding: 32px
  footer-dark:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.body}"
    typography: "{typography.body-sm}"
    padding: 64px 48px
  footer-link:
    backgroundColor: transparent
    textColor: "{colors.body}"
    typography: "{typography.body-sm}"
---

# Ferrari 延伸設計規格

語言：繁體中文（台灣用語，zh-TW）。在地化更新：2026-10-20。

## 來源與規格層次

這份規格將較早保存的品牌設計資料重新整理為可實作的繁體中文文件。來源設定中的色碼、字級、字重、行高、間距、圓角與元件識別字保留，供開發工具讀取；敘述與操作指令改用台灣用語。這些延伸設定不等同於目前日期限定首頁的逐項實測值，若兩者不同，依下方的日期限定觀察及對應預覽判讀。

- 原始資料版本：`1a783491c9539c3153c2fc96c16d59131e024f4e`。
- 原始 DESIGN.md 摘要：`5e74de5d39ca9cec9ea8a2383af5e139efd6bde1c4b899466d44a71c8677c8ec`。
- 目前首頁參考日期：2026-10-11。
- 目前公開來源：https://www.ferrari.com/en-US。
- 目前預覽：`official-drafts/ferrari.html`。
- 台灣繁體中文規格與指令是本次重新產出的內容；來源截圖及原生生成紀錄保留原貌。

## 整體視覺方向

黑白光影與克制的紅色，帶出速度感。

製作車款專題頁，讓深淺故事章節交錯，並提供精簡的車款摘要。紅色只用於明確重點，透過有力的圖片裁切與章節標題建立閱讀節奏。

先建立主要內容、輔助資訊與操作之間的層級，再套用色彩及裝飾。品牌色應有明確用途；主要操作、選取、錯誤及停用狀態要能分辨。避免將多套參考風格混在同一頁，也不要僅替換通用卡片的顏色。

## 色彩、字型與繁體中文排版

上方來源設定保留原始色彩角色與數值。主要品牌色用於最重要的操作；背景、內容表面、主要文字、次要文字與分隔線各自維持一致用途。資訊不能只依賴顏色，狀態須同時有文字或圖示標示。

原字型名稱可作為拉丁字母參考。繁體中文字型優先使用可取得的 `Noto Sans TC`、`PingFang TC`、`Microsoft JhengHei`，最後才使用 `sans-serif`。原字型未涵蓋中文時必須提供替代，不以缺字或圖片文字呈現正文。專有字型無法取得時，記錄替代字型與可能的字寬差異。

中文標題以語意分段，避免為模仿英文大寫字距而拉散中文字。內文行高、欄寬與段落間距以可讀性為準；英文型號、網址、程式碼及長連結可以換行或在自己的區域捲動，不可撐開整份文件。價格、規格及比較欄位保持數字與單位對齊。

| 字級 | 字重 | 行高 | 字距 |
| --- | --- | --- | --- |
| 80px | 500 | 1.05 | -1.6px |
| 56px | 500 | 1.1 | -1.12px |
| 36px | 500 | 1.2 | -0.36px |
| 26px | 500 | 1.5 | 0.195px |
| 18px | 700 | 1.2 | 0 |
| 16px | 500 | 1.4 | 0.08px |
| 14px | 400 | 1.5 | 0 |
| 13px | 400 | 1.5 | 0 |
| 12px | 400 | 1.4 | 0 |
| 11px | 600 | 1.4 | 1.1px |
| 14px | 700 | 1.0 | 1.4px (uppercase) |
| 13px | 600 | 1.4 | 0.65px (uppercase) |
| 80px | 700 | 1.0 | -1.6px |

## 版面與元件結構

此參考可先實作：車款故事面板，包含圖片說明與可使用鍵盤展開的規格資訊。

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

- `#181818`
- `#da291c`
- `0 4px 8px rgba(0,0,0,0.1)`
- `linear-gradient(180deg, #a00c01, #da291c 64%)`
- `linear-gradient(180deg, #3c3c3c, #030303 64%)`

## 日期限定首頁觀察

來源為 https://www.ferrari.com/en-US 。沿用 oct10 檔名前綴；最新來源與實際畫面觀察時間為2026-10-11T23:08Z之後，臺北時間2026-10-12。新聞第一則已更新為「Charles 在濱海灣登上頒獎台」，舊 qualifying 報導不再留在目前稿件。新聞第二則 Barcelona 為本預覽的選定靜態狀態。

官方首頁以滿版影片、透明黑色導航與白色新聞區形成對比。Scuderia Ferrari HP 首屏佔完整視窗；三封面指示器與四則新聞輪播皆有原始資料。六張照片卡在1280px形成兩欄，在390px依序堆疊。Sketch Body 沒有 Magazine 小標。灰色 Newsletter 區接黑色五類頁尾，窄版呈閉合列；完整社群、公司法律文字、隱私連結、國別與 Shell 標記均保留。

真正的兩次 Google Stitch 桌面修改與未改動輸出已保存。首次生成含與來源不同的字型、影像、EN-US工具、01/04索引與 Sketch Body 小標，因此再以完整公開 DOM、220個開放 shadow roots、64份 adopted CSS 與實際公開素材逐項校正。保留正常CSS瀏覽器200回應的原始 Ferrari 字型；不載入追蹤與服務腳本。

目前 SHA 的稿件重新載入後，桌面1280×720與窄版390×844各有7張真正視窗截圖，連續覆蓋4337與5258px。每張核對實際檔案尺寸、網址、捲動位置、頁高與擷取時稿件雜湊。兩版19張DOM圖片全部載入，沒有橫向溢出。首屏、六卡與Newsletter共8個主要標題的文字及邊界差值皆為0。補充同一 Barcelona 新聞狀態的兩版實拍，以及官方窄版動畫完成後再走一次的7張完整實拍；所有比較圖已實際開啟檢視。

完整官方第一趟窄版截圖仍保留尚未出現的動畫卡與輪播過渡，第二趟真實截圖可見全部照片。預覽採原始公開影片海報與動畫終態，不重現HLS影格、入場/輪播時序、Play、Menu、Search、Subscribe、頁尾展開或外部服務。桌面額外新聞實拍的官方導航仍顯示，本地向下捲動狀態已收起，兩者差異亦保留。7個未使用的替代/CJK字型網址405仍記錄，不能宣稱所有取得嘗試成功。

## 已知差異與驗證範圍

- 第一張主視覺使用原始公開靜態海報，與官網 HLS 影片的畫格可見不同；播放及封面控制尚未實作。其他封面保留在來源範本中，但其啟用後畫面尚未驗收。
- 官網新聞自動輪播；首次完整桌面拍攝顯示第 3 則，首次窄版拍攝跨越新聞及顯示動畫。另存的兩種寬度 Barcelona 來源截圖及第二次完整窄版拍攝，顯示預覽選用的第 2 則。自動輪播、導覽按鈕與轉場時間仍有差異。
- 官網進場及幕簾動畫在預覽中固定為最終靜態狀態。第一次窄版官網拍攝包含尚未顯示的卡片，原始影像保留；第二次另存的 7 張 390×844 來源截圖顯示全部 6 張卡片。未宣稱畫格時間或動畫一致。
- 桌面向下捲動時以簡單門檻隱藏頁首；另選的 Barcelona 官網桌面畫面仍有頁首，本機向下畫面則隱藏。完整上下捲動導覽、滑鼠移入選單、搜尋、訂閱、頁尾與社群摺疊、鍵盤焦點、隱私及無障礙服務尚未實作或驗收。
- 7 個未使用的替代、中字重及中日韓字型網址回傳 405。所需 Body-Font 取自正常瀏覽器 CSS 的 200 回應，兩份主要 FerrariSans 一般與中字重字型已保存；兩種寬度的已觀察圖片皆可載入。其他語言與替代字型尚未驗收。
- 兩份新的 Stitch 桌面編輯稿分別保留，先前行動版與原始設計資料仍可溯源。390px 為使用桌面瀏覽器識別的 CSS 窄版，並非真實手機；原始比對未涵蓋其他寬度、路由、帳戶、車款設定器、購買服務及正式部署。

以上限制沿用原參考日期的比對紀錄。本次繁體中文整理不會把未驗證的影片、動畫、服務或尺寸改標為已通過；目前預覽仍未宣稱與官方完全一致。
<!-- Original AI instructions: awesome-ai-web-design -->

## 來源與使用範圍

設計資料改寫自採 MIT 授權的 VoltAgent/awesome-design-md，詳見 LICENSE 與 ATTRIBUTION.md。品牌名稱僅用於識別參考來源，並非官方授權或服務。下方 AI 指令由本專案獨立撰寫；若既有互動備註與無障礙要求衝突，以此處的可用性檢查為準。

## 重新撰寫的 AI 任務指令

語言：繁體中文（台灣用語，zh-TW）。將 DESIGN.md 放入專案，再選擇下方任務。這些指令由本專案重新撰寫；請把示範內容替換為自己的產品需求。

## 建立新頁面

```text
先閱讀隨附的 DESIGN.md，以 Ferrari 的設計語言作為介面參考。請完成以下可操作頁面：製作車款專題頁，讓深淺故事章節交錯，並提供精簡的車款摘要。紅色只用於明確重點，透過有力的圖片裁切與章節標題建立閱讀節奏。

使用我的產品名稱、內容與資料格式，優先沿用專案現有元件及技術。開始製作樣式前，先將色彩、字體、間距與圓角整理為可重複使用的設計變數。指定字型無法取得時，使用可用的系統字型或開源字型，並說明替代方式。介面文案、按鈕、提示、錯誤訊息、圖片替代文字、註解與交付說明，一律使用繁體中文（台灣用語）。使用「專案、元件、資料、建立、預設、載入、登入、連結、儲存、影片」等台灣用語。保留品牌名稱、檔名、網址、API 識別字與可執行程式碼；HTML 語言設為 zh-Hant-TW。

讓互動元件可實際操作，並將狀態提供給輔助科技。具備可見的鍵盤焦點、清楚的欄位標示、減少動態效果，以及至少 44px 的觸控區域。參考視覺與可用性衝突時，作最小幅度的無障礙調整並記錄原因。在 390px、768px、1440px 寬度檢查版面，涵蓋繁體中文長標題、長內容、空白及錯誤狀態。金額、數量與日期依資料本身的幣別、單位及時區呈現，以 zh-TW 格式顯示，不擅自換算。最後交付完成的檔案、實際驗證結果與仍待確認的假設，不把未檢查項目宣稱為通過。
```

## 製作元件

```text
先閱讀隨附的 DESIGN.md，以 Ferrari 的設計語言作為介面參考。請製作車款故事面板，包含圖片說明與可使用鍵盤展開的規格資訊。沿用現有元件慣例，放入精簡且符合實際情境的範例。比例與資訊層級應來自參考規格，不能只替通用卡片換色。依需求支援預設、焦點、停用、載入與錯誤狀態。使用有意義的示範資料，讓每個可見操作都有明確結果。

使用我的產品名稱、內容與資料格式，優先沿用專案現有元件及技術。開始製作樣式前，先將色彩、字體、間距與圓角整理為可重複使用的設計變數。指定字型無法取得時，使用可用的系統字型或開源字型，並說明替代方式。介面文案、按鈕、提示、錯誤訊息、圖片替代文字、註解與交付說明，一律使用繁體中文（台灣用語）。使用「專案、元件、資料、建立、預設、載入、登入、連結、儲存、影片」等台灣用語。保留品牌名稱、檔名、網址、API 識別字與可執行程式碼；HTML 語言設為 zh-Hant-TW。

讓互動元件可實際操作，並將狀態提供給輔助科技。具備可見的鍵盤焦點、清楚的欄位標示、減少動態效果，以及至少 44px 的觸控區域。參考視覺與可用性衝突時，作最小幅度的無障礙調整並記錄原因。在 390px、768px、1440px 寬度檢查版面，涵蓋繁體中文長標題、長內容、空白及錯誤狀態。金額、數量與日期依資料本身的幣別、單位及時區呈現，以 zh-TW 格式顯示，不擅自換算。最後交付完成的檔案、實際驗證結果與仍待確認的假設，不把未檢查項目宣稱為通過。
```

## 改造既有介面

```text
先閱讀隨附的 DESIGN.md，以 Ferrari 的設計語言作為介面參考。重新設計選定頁面，同時保留路由、資料、行為與使用者可理解的意義。先確認頁面層級，再找出最少且可重複使用的設計變數與元件調整。以下構圖作為視覺方向，依現有頁面調整：製作車款專題頁，讓深淺故事章節交錯，並提供精簡的車款摘要。紅色只用於明確重點，透過有力的圖片裁切與章節標題建立閱讀節奏。

使用我的產品名稱、內容與資料格式，優先沿用專案現有元件及技術。開始製作樣式前，先將色彩、字體、間距與圓角整理為可重複使用的設計變數。指定字型無法取得時，使用可用的系統字型或開源字型，並說明替代方式。介面文案、按鈕、提示、錯誤訊息、圖片替代文字、註解與交付說明，一律使用繁體中文（台灣用語）。使用「專案、元件、資料、建立、預設、載入、登入、連結、儲存、影片」等台灣用語。保留品牌名稱、檔名、網址、API 識別字與可執行程式碼；HTML 語言設為 zh-Hant-TW。依完整元件群組套用變更，檢查其他頁面是否受影響，並說明調整前後的主要差異。

讓互動元件可實際操作，並將狀態提供給輔助科技。具備可見的鍵盤焦點、清楚的欄位標示、減少動態效果，以及至少 44px 的觸控區域。參考視覺與可用性衝突時，作最小幅度的無障礙調整並記錄原因。在 390px、768px、1440px 寬度檢查版面，涵蓋繁體中文長標題、長內容、空白及錯誤狀態。金額、數量與日期依資料本身的幣別、單位及時區呈現，以 zh-TW 格式顯示，不擅自換算。最後交付完成的檔案、實際驗證結果與仍待確認的假設，不把未檢查項目宣稱為通過。
```

## 逐次調整流程

1. 先指出一個可實際觀察的問題，例如層級不清或內容遭裁切。
2. 在 DESIGN.md 找到對應設計變數或元件規則，提出範圍明確的調整。
3. 套用調整，保留無關的路由與資料行為。
4. 檢查鍵盤焦點、窄版排版，以及代表性的內容與錯誤狀態。
5. 用繁體中文說明結果，以及刻意偏離參考外觀的原因。
