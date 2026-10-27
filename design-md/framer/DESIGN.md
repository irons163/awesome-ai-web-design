---
version: zh-TW-2026-10-15
language: zh-TW
name: "Framer"
description: "深色展示舞台與電藍色，突出作品品質。"

colors:
  primary: "#ffffff"
  on-primary: "#000000"
  accent-blue: "#0099ff"
  ink: "#ffffff"
  ink-muted: "#999999"
  canvas: "#090909"
  surface-1: "#141414"
  surface-2: "#1c1c1c"
  hairline: "#262626"
  hairline-soft: "#1a1a1a"
  inverse-canvas: "#ffffff"
  inverse-ink: "#000000"
  gradient-magenta: "#d44df0"
  gradient-violet: "#6a4cf5"
  gradient-orange: "#ff7a3d"
  gradient-coral: "#ff5577"
  semantic-success: "#22c55e"

typography:
  display-xxl:
    fontFamily: GT Walsheim Framer Medium
    fontSize: 110px
    fontWeight: 500
    lineHeight: 0.85
    letterSpacing: -5.5px
  display-xl:
    fontFamily: GT Walsheim Medium
    fontSize: 85px
    fontWeight: 500
    lineHeight: 0.95
    letterSpacing: -4.25px
    fontFeature: ss02
  display-lg:
    fontFamily: GT Walsheim Medium
    fontSize: 62px
    fontWeight: 500
    lineHeight: 1.00
    letterSpacing: -3.1px
    fontFeature: ss02
  display-md:
    fontFamily: GT Walsheim Medium
    fontSize: 32px
    fontWeight: 500
    lineHeight: 1.13
    letterSpacing: -1.0px
  headline:
    fontFamily: Inter
    fontSize: 22px
    fontWeight: 700
    lineHeight: 1.20
    letterSpacing: -0.8px
    fontFeature: cv05
  subhead:
    fontFamily: Inter Variable
    fontSize: 24px
    fontWeight: 400
    lineHeight: 1.30
    letterSpacing: -0.01px
    fontFeature: cv11
  body-lg:
    fontFamily: Inter Variable
    fontSize: 18px
    fontWeight: 400
    lineHeight: 1.30
    letterSpacing: -0.18px
    fontFeature: cv11
  body:
    fontFamily: Inter Variable
    fontSize: 15px
    fontWeight: 400
    lineHeight: 1.30
    letterSpacing: -0.15px
    fontFeature: cv11
  body-sm:
    fontFamily: Inter Variable
    fontSize: 14px
    fontWeight: 500
    lineHeight: 1.40
    letterSpacing: -0.14px
    fontFeature: cv11
  caption:
    fontFamily: Inter Variable
    fontSize: 13px
    fontWeight: 500
    lineHeight: 1.20
    letterSpacing: -0.13px
    fontFeature: cv11
  micro:
    fontFamily: Inter Variable
    fontSize: 12px
    fontWeight: 400
    lineHeight: 1.20
    letterSpacing: -0.12px
    fontFeature: cv11
  button:
    fontFamily: Inter Variable
    fontSize: 14px
    fontWeight: 500
    lineHeight: 1.0
    letterSpacing: -0.14px
    fontFeature: cv11

rounded:
  xs: 4px
  sm: 6px
  md: 10px
  lg: 15px
  xl: 20px
  xxl: 30px
  pill: 100px
  full: 9999px

spacing:
  hair: 1px
  xxs: 4px
  xs: 8px
  sm: 12px
  md: 15px
  lg: 20px
  xl: 30px
  xxl: 40px
  section: 96px

components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.button}"
    rounded: "{rounded.pill}"
    padding: 10px 15px
  button-primary-pressed:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.button}"
    rounded: "{rounded.pill}"
  button-secondary:
    backgroundColor: "{colors.surface-1}"
    textColor: "{colors.ink}"
    typography: "{typography.button}"
    rounded: "{rounded.pill}"
    padding: 10px 15px
  button-translucent:
    backgroundColor: "{colors.surface-2}"
    textColor: "{colors.ink}"
    typography: "{typography.button}"
    rounded: "{rounded.xxl}"
    padding: 8px 14px
  button-icon-circular:
    backgroundColor: "{colors.surface-1}"
    textColor: "{colors.ink}"
    typography: "{typography.button}"
    rounded: "{rounded.full}"
    size: 40px
  pricing-tab-default:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink-muted}"
    typography: "{typography.button}"
    rounded: "{rounded.pill}"
    padding: 8px 14px
  pricing-tab-selected:
    backgroundColor: "{colors.surface-2}"
    textColor: "{colors.ink}"
    typography: "{typography.button}"
    rounded: "{rounded.pill}"
    padding: 8px 14px
  text-input:
    backgroundColor: "{colors.surface-1}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.md}"
    padding: 10px 14px
  text-input-focused:
    backgroundColor: "{colors.surface-1}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.md}"
    padding: 10px 14px
  pricing-card:
    backgroundColor: "{colors.surface-1}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.xl}"
    padding: 24px
  pricing-card-featured:
    backgroundColor: "{colors.surface-2}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.xl}"
    padding: 24px
  template-card:
    backgroundColor: "{colors.surface-1}"
    textColor: "{colors.ink}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.lg}"
    padding: 12px
  gradient-spotlight-card:
    backgroundColor: "{colors.gradient-violet}"
    textColor: "{colors.ink}"
    typography: "{typography.subhead}"
    rounded: "{rounded.xl}"
    padding: 32px
  gradient-spotlight-card-magenta:
    backgroundColor: "{colors.gradient-magenta}"
    textColor: "{colors.ink}"
    typography: "{typography.subhead}"
    rounded: "{rounded.xl}"
    padding: 32px
  gradient-spotlight-card-orange:
    backgroundColor: "{colors.gradient-orange}"
    textColor: "{colors.ink}"
    typography: "{typography.subhead}"
    rounded: "{rounded.xl}"
    padding: 32px
  product-mockup-tile:
    backgroundColor: "{colors.surface-1}"
    textColor: "{colors.ink}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.xl}"
    padding: 16px
  feature-row:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.xs}"
  comparison-row:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink-muted}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.xs}"
  top-nav:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.xs}"
    height: 56px
  faq-row:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.md}"
    padding: 24px
  footer:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink-muted}"
    typography: "{typography.caption}"
    rounded: "{rounded.xs}"
    padding: 64px 32px
---

# Framer 延伸設計規格

語言：繁體中文（台灣用語，zh-TW）。在地化更新：2026-10-20。

## 來源與規格層次

這份規格將較早保存的品牌設計資料重新整理為可實作的繁體中文文件。來源設定中的色碼、字級、字重、行高、間距、圓角與元件識別字保留，供開發工具讀取；敘述與操作指令改用台灣用語。這些延伸設定不等同於目前日期限定首頁的逐項實測值，若兩者不同，依下方的日期限定觀察及對應預覽判讀。

- 原始資料版本：`1a783491c9539c3153c2fc96c16d59131e024f4e`。
- 原始 DESIGN.md 摘要：`9fc14fce45e7690fb69bfa156123a71b6a783724f13c777b09dc0e3c1d764e0b`。
- 目前首頁參考日期：2026-10-12。
- 目前公開來源：https://www.framer.com/。
- 目前預覽：`official-drafts/framer.html`。
- 台灣繁體中文規格與指令是本次重新產出的內容；來源截圖及原生生成紀錄保留原貌。

## 整體視覺方向

深色展示舞台與電藍色，突出作品品質。

製作作品集發布頁，包含主要專案預覽、精簡功能介紹與範本圖庫。使用深色外框與藍色操作；所有動態內容都提供資訊等量的靜態替代。

先建立主要內容、輔助資訊與操作之間的層級，再套用色彩及裝飾。品牌色應有明確用途；主要操作、選取、錯誤及停用狀態要能分辨。避免將多套參考風格混在同一頁，也不要僅替換通用卡片的顏色。

## 色彩、字型與繁體中文排版

上方來源設定保留原始色彩角色與數值。主要品牌色用於最重要的操作；背景、內容表面、主要文字、次要文字與分隔線各自維持一致用途。資訊不能只依賴顏色，狀態須同時有文字或圖示標示。

原字型名稱可作為拉丁字母參考。繁體中文字型優先使用可取得的 `Noto Sans TC`、`PingFang TC`、`Microsoft JhengHei`，最後才使用 `sans-serif`。原字型未涵蓋中文時必須提供替代，不以缺字或圖片文字呈現正文。專有字型無法取得時，記錄替代字型與可能的字寬差異。

中文標題以語意分段，避免為模仿英文大寫字距而拉散中文字。內文行高、欄寬與段落間距以可讀性為準；英文型號、網址、程式碼及長連結可以換行或在自己的區域捲動，不可撐開整份文件。價格、規格及比較欄位保持數字與單位對齊。

| 字級 | 字重 | 行高 | 字距 |
| --- | --- | --- | --- |
| 110px | 500 | 0.85 | -5.5px |
| 85px | 500 | 0.95 | -4.25px |
| 62px | 500 | 1.00 | -3.1px |
| 32px | 500 | 1.13 | -1.0px |
| 22px | 700 | 1.20 | -0.8px |
| 24px | 400 | 1.30 | -0.01px |
| 18px | 400 | 1.30 | -0.18px |
| 15px | 400 | 1.30 | -0.15px |
| 14px | 500 | 1.40 | -0.14px |
| 13px | 500 | 1.20 | -0.13px |
| 12px | 400 | 1.20 | -0.12px |
| 14px | 500 | 1.0 | -0.14px |

## 版面與元件結構

此參考可先實作：範本預覽卡片，包含檢視尺寸選擇與單一發布示範操作。

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

- `rgba(255,255,255,0.10)`
- `rgba(0,0,0,0.25)`
- `rgba(0,153,255,0.15)`

## 日期限定首頁觀察

2026-10-12 UTC實際匿名英文首頁採純黑底、白字與GT Walsheim。主標題為Framer 是陪你從點子走到上線的設計代理，首屏包含免費開始、下載程式、New: Skills與代理影片。其後為Design、CMS、Code及外部代理，平台功能格、Shipped with Framer作品、品牌故事、社群、代理輸入框與多欄頁尾。窄版為堆疊功能卡、雙欄頁尾及發光畫布CTA。桌面10741px共15段、窄版10855px共13段，以真1280×720與390×844原生畫面擷取。主代理實看全部8張對照圖，28個位置均有配對；窄版19個標題量測無差異，桌面4項差異仍明列。

**已比對主要靜態畫面，仍有差異；accepted=false，不宣稱與官方一致。**

既有設計分析及原始指令保留。本次官方來源、真實 Google Stitch MCP 原始輸出、校正檔與實際瀏覽器畫面分開記錄。研究頁面免費瀏覽，沒有啟動付費方案或交易。

## 已知差異與驗證範圍

- Stitch實際回傳DESKTOP2560×14098，沒有產生所請求窄版。原生成稿新增作品與統計數字，與校正版分開保留，不能代替瀏覽器畫面驗證。
- 桌面4項標題差異與動態取樣有關。影片進度、代理打字／終端、Logo跑馬燈、懸停及淡入未同步。桌面官方取樣多處作品／社群預覽、窄版若干代理卡仍在空白載入狀態，本機原始圖片完整顯示，存在明顯可見差異。
- 初稿內嵌SVG引號導致CSS解析失敗，35317px的24張舊測試不作驗證證據。修正後全套28張重新擷取、完整覆蓋、目前SHA一致，沒有本機可見缺圖或橫向溢出。
- 窄版根選單已實看，X及Escape通過，載入HTTP文件與磁碟逐位元組相同。桌面下拉、次層選單、作品輪播、播放控制、語言與外部代理／登入／註冊服務未完整驗證；沒有提交服務操作。
- 390px為桌面UA響應式測試，非實機。原分析及指令保留，研究免費瀏覽，沒有啟用付費方案，不推定供應商使用量帳單。accepted=false、official_consistency_claim=false，正式更新待全部74頁整合。

以上限制沿用原參考日期的比對紀錄。本次繁體中文整理不會把未驗證的影片、動畫、服務或尺寸改標為已通過；目前預覽仍未宣稱與官方完全一致。
<!-- Original AI instructions: awesome-ai-web-design -->

## 來源與使用範圍

設計資料改寫自採 MIT 授權的 VoltAgent/awesome-design-md，詳見 LICENSE 與 ATTRIBUTION.md。品牌名稱僅用於識別參考來源，並非官方授權或服務。下方 AI 指令由本專案獨立撰寫；若既有互動備註與無障礙要求衝突，以此處的可用性檢查為準。

## 重新撰寫的 AI 任務指令

語言：繁體中文（台灣用語，zh-TW）。將 DESIGN.md 放入專案，再選擇下方任務。這些指令由本專案重新撰寫；請把示範內容替換為自己的產品需求。

## 建立新頁面

```text
先閱讀隨附的 DESIGN.md，以 Framer 的設計語言作為介面參考。請完成以下可操作頁面：製作作品集發布頁，包含主要專案預覽、精簡功能介紹與範本圖庫。使用深色外框與藍色操作；所有動態內容都提供資訊等量的靜態替代。

使用我的產品名稱、內容與資料格式，優先沿用專案現有元件及技術。開始製作樣式前，先將色彩、字體、間距與圓角整理為可重複使用的設計變數。指定字型無法取得時，使用可用的系統字型或開源字型，並說明替代方式。介面文案、按鈕、提示、錯誤訊息、圖片替代文字、註解與交付說明，一律使用繁體中文（台灣用語）。使用「專案、元件、資料、建立、預設、載入、登入、連結、儲存、影片」等台灣用語。保留品牌名稱、檔名、網址、API 識別字與可執行程式碼；HTML 語言設為 zh-Hant-TW。

讓互動元件可實際操作，並將狀態提供給輔助科技。具備可見的鍵盤焦點、清楚的欄位標示、減少動態效果，以及至少 44px 的觸控區域。參考視覺與可用性衝突時，作最小幅度的無障礙調整並記錄原因。在 390px、768px、1440px 寬度檢查版面，涵蓋繁體中文長標題、長內容、空白及錯誤狀態。金額、數量與日期依資料本身的幣別、單位及時區呈現，以 zh-TW 格式顯示，不擅自換算。最後交付完成的檔案、實際驗證結果與仍待確認的假設，不把未檢查項目宣稱為通過。
```

## 製作元件

```text
先閱讀隨附的 DESIGN.md，以 Framer 的設計語言作為介面參考。請製作範本預覽卡片，包含檢視尺寸選擇與單一發布示範操作。沿用現有元件慣例，放入精簡且符合實際情境的範例。比例與資訊層級應來自參考規格，不能只替通用卡片換色。依需求支援預設、焦點、停用、載入與錯誤狀態。使用有意義的示範資料，讓每個可見操作都有明確結果。

使用我的產品名稱、內容與資料格式，優先沿用專案現有元件及技術。開始製作樣式前，先將色彩、字體、間距與圓角整理為可重複使用的設計變數。指定字型無法取得時，使用可用的系統字型或開源字型，並說明替代方式。介面文案、按鈕、提示、錯誤訊息、圖片替代文字、註解與交付說明，一律使用繁體中文（台灣用語）。使用「專案、元件、資料、建立、預設、載入、登入、連結、儲存、影片」等台灣用語。保留品牌名稱、檔名、網址、API 識別字與可執行程式碼；HTML 語言設為 zh-Hant-TW。

讓互動元件可實際操作，並將狀態提供給輔助科技。具備可見的鍵盤焦點、清楚的欄位標示、減少動態效果，以及至少 44px 的觸控區域。參考視覺與可用性衝突時，作最小幅度的無障礙調整並記錄原因。在 390px、768px、1440px 寬度檢查版面，涵蓋繁體中文長標題、長內容、空白及錯誤狀態。金額、數量與日期依資料本身的幣別、單位及時區呈現，以 zh-TW 格式顯示，不擅自換算。最後交付完成的檔案、實際驗證結果與仍待確認的假設，不把未檢查項目宣稱為通過。
```

## 改造既有介面

```text
先閱讀隨附的 DESIGN.md，以 Framer 的設計語言作為介面參考。重新設計選定頁面，同時保留路由、資料、行為與使用者可理解的意義。先確認頁面層級，再找出最少且可重複使用的設計變數與元件調整。以下構圖作為視覺方向，依現有頁面調整：製作作品集發布頁，包含主要專案預覽、精簡功能介紹與範本圖庫。使用深色外框與藍色操作；所有動態內容都提供資訊等量的靜態替代。

使用我的產品名稱、內容與資料格式，優先沿用專案現有元件及技術。開始製作樣式前，先將色彩、字體、間距與圓角整理為可重複使用的設計變數。指定字型無法取得時，使用可用的系統字型或開源字型，並說明替代方式。介面文案、按鈕、提示、錯誤訊息、圖片替代文字、註解與交付說明，一律使用繁體中文（台灣用語）。使用「專案、元件、資料、建立、預設、載入、登入、連結、儲存、影片」等台灣用語。保留品牌名稱、檔名、網址、API 識別字與可執行程式碼；HTML 語言設為 zh-Hant-TW。依完整元件群組套用變更，檢查其他頁面是否受影響，並說明調整前後的主要差異。

讓互動元件可實際操作，並將狀態提供給輔助科技。具備可見的鍵盤焦點、清楚的欄位標示、減少動態效果，以及至少 44px 的觸控區域。參考視覺與可用性衝突時，作最小幅度的無障礙調整並記錄原因。在 390px、768px、1440px 寬度檢查版面，涵蓋繁體中文長標題、長內容、空白及錯誤狀態。金額、數量與日期依資料本身的幣別、單位及時區呈現，以 zh-TW 格式顯示，不擅自換算。最後交付完成的檔案、實際驗證結果與仍待確認的假設，不把未檢查項目宣稱為通過。
```

## 逐次調整流程

1. 先指出一個可實際觀察的問題，例如層級不清或內容遭裁切。
2. 在 DESIGN.md 找到對應設計變數或元件規則，提出範圍明確的調整。
3. 套用調整，保留無關的路由與資料行為。
4. 檢查鍵盤焦點、窄版排版，以及代表性的內容與錯誤狀態。
5. 用繁體中文說明結果，以及刻意偏離參考外觀的原因。
