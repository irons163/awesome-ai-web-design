---
version: zh-TW-2026-10-15
language: zh-TW
name: "Superhuman"
description: "深紫與暖白的輕盈對比，聚焦鍵盤效率。"

colors:
  primary: "#1b1938"
  primary-deep: "#0e0c1f"
  on-primary: "#ffffff"
  ink: "#292827"
  ink-mute: "#73706d"
  ink-faint: "#9a9794"
  canvas: "#ffffff"
  canvas-soft: "#fafaf8"
  surface-violet-soft: "#c9b4fa"
  surface-teal-deep: "#0e3030"
  surface-teal-mid: "#155555"
  hairline: "#e8e4dd"
  hairline-dark: "#3f3a52"
  on-dark-mute: "#bcbac9"
  on-dark-faint: "#5a5772"

typography:
  display-xxl:
    fontFamily: "'Super Sans VF', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
    fontSize: 64px
    fontWeight: 540
    lineHeight: 0.96
    letterSpacing: 0
  display-xl:
    fontFamily: "'Super Sans VF', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
    fontSize: 48px
    fontWeight: 460
    lineHeight: 0.96
    letterSpacing: -1.32px
  display-lg:
    fontFamily: "'Super Sans VF', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
    fontSize: 28px
    fontWeight: 540
    lineHeight: 1.14
    letterSpacing: -0.63px
  display-md:
    fontFamily: "'Super Sans VF', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
    fontSize: 22px
    fontWeight: 460
    lineHeight: 1.1
    letterSpacing: -0.315px
  heading-lg:
    fontFamily: "'Super Sans VF', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
    fontSize: 20px
    fontWeight: 460
    lineHeight: 1.2
    letterSpacing: -0.4px
  body-lg:
    fontFamily: "'Super Sans VF', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
    fontSize: 18px
    fontWeight: 540
    lineHeight: 1.5
    letterSpacing: -0.135px
  body-md:
    fontFamily: "'Super Sans VF', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
    fontSize: 16px
    fontWeight: 460
    lineHeight: 1.5
    letterSpacing: 0
  body-strong:
    fontFamily: "'Super Sans VF', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
    fontSize: 18.72px
    fontWeight: 700
    lineHeight: 1.5
    letterSpacing: 0
  button-md:
    fontFamily: "'Super Sans VF', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
    fontSize: 16px
    fontWeight: 700
    lineHeight: 1.0
    letterSpacing: 0
  button-cap:
    fontFamily: "'Super Sans VF', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
    fontSize: 14px
    fontWeight: 600
    lineHeight: 1.0
    letterSpacing: 0
  caption:
    fontFamily: "'Super Sans VF', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
    fontSize: 14px
    fontWeight: 460
    lineHeight: 1.4
    letterSpacing: 0
  micro:
    fontFamily: "'Super Sans VF', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
    fontSize: 12px
    fontWeight: 540
    lineHeight: 1.4
    letterSpacing: 0

rounded:
  xs: 4px
  sm: 6px
  md: 8px
  lg: 12px
  xl: 16px
  full: 9999px

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
  button-primary-dark:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.button-md}"
    rounded: "{rounded.md}"
    padding: 12px 20px
  button-primary-dark-pressed:
    backgroundColor: "{colors.primary-deep}"
    textColor: "{colors.on-primary}"
    typography: "{typography.button-md}"
    rounded: "{rounded.md}"
    padding: 12px 20px
  button-on-dark-pill:
    backgroundColor: "{colors.surface-violet-soft}"
    textColor: "{colors.primary}"
    typography: "{typography.button-md}"
    rounded: "{rounded.full}"
    padding: 12px 20px
  button-secondary-outline:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.button-md}"
    rounded: "{rounded.md}"
    padding: 12px 20px
  button-on-teal:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.surface-teal-deep}"
    typography: "{typography.button-md}"
    rounded: "{rounded.md}"
    padding: 12px 20px
  text-input:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.sm}"
    padding: 10px 12px
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
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.body-md}"
    rounded: "{rounded.lg}"
    padding: 32px
  card-teal-band:
    backgroundColor: "{colors.surface-teal-deep}"
    textColor: "{colors.on-primary}"
    typography: "{typography.body-lg}"
    rounded: "{rounded.lg}"
    padding: 64px
  card-feature-row:
    backgroundColor: "{colors.canvas-soft}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: 24px
  pill-tab-light:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.button-cap}"
    rounded: "{rounded.full}"
    padding: 8px 16px
  nav-bar-dark:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.body-md}"
    rounded: "{rounded.xs}"
    padding: 16px 24px
  nav-bar-light:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.xs}"
    padding: 16px 24px
  link-on-light:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
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

# Superhuman 延伸設計規格

語言：繁體中文（台灣用語，zh-TW）。在地化更新：2026-10-20。

## 來源與規格層次

這份規格將較早保存的品牌設計資料重新整理為可實作的繁體中文文件。來源設定中的色碼、字級、字重、行高、間距、圓角與元件識別字保留，供開發工具讀取；敘述與操作指令改用台灣用語。這些延伸設定不等同於目前日期限定首頁的逐項實測值，若兩者不同，依下方的日期限定觀察及對應預覽判讀。

- 原始資料版本：`1a783491c9539c3153c2fc96c16d59131e024f4e`。
- 原始 DESIGN.md 摘要：`738def8a9cdfe200c62c62d8f383f8395efa488d5366c99dbe7d8fb3afd667f7`。
- 目前首頁參考日期：2026-10-10。
- 目前公開來源：https://superhuman.com/。
- 目前預覽：`official-drafts/superhuman.html`。
- 台灣繁體中文規格與指令是本次重新產出的內容；來源截圖及原生生成紀錄保留原貌。

## 整體視覺方向

深紫與暖白的輕盈對比，聚焦鍵盤效率。

製作郵件效率工具概念頁，包含簡潔收件匣、展開的閱讀面板與可見快捷鍵。暖色中性閱讀區與深紫色外框交替，以清楚選取與快速掃讀為優先。

先建立主要內容、輔助資訊與操作之間的層級，再套用色彩及裝飾。品牌色應有明確用途；主要操作、選取、錯誤及停用狀態要能分辨。避免將多套參考風格混在同一頁，也不要僅替換通用卡片的顏色。

## 色彩、字型與繁體中文排版

上方來源設定保留原始色彩角色與數值。主要品牌色用於最重要的操作；背景、內容表面、主要文字、次要文字與分隔線各自維持一致用途。資訊不能只依賴顏色，狀態須同時有文字或圖示標示。

原字型名稱可作為拉丁字母參考。繁體中文字型優先使用可取得的 `Noto Sans TC`、`PingFang TC`、`Microsoft JhengHei`，最後才使用 `sans-serif`。原字型未涵蓋中文時必須提供替代，不以缺字或圖片文字呈現正文。專有字型無法取得時，記錄替代字型與可能的字寬差異。

中文標題以語意分段，避免為模仿英文大寫字距而拉散中文字。內文行高、欄寬與段落間距以可讀性為準；英文型號、網址、程式碼及長連結可以換行或在自己的區域捲動，不可撐開整份文件。價格、規格及比較欄位保持數字與單位對齊。

| 字級 | 字重 | 行高 | 字距 |
| --- | --- | --- | --- |
| 64px | 540 | 0.96 | 0 |
| 48px | 460 | 0.96 | -1.32px |
| 28px | 540 | 1.14 | -0.63px |
| 22px | 460 | 1.1 | -0.315px |
| 20px | 460 | 1.2 | -0.4px |
| 18px | 540 | 1.5 | -0.135px |
| 16px | 460 | 1.5 | 0 |
| 18.72px | 700 | 1.5 | 0 |
| 16px | 700 | 1.0 | 0 |
| 14px | 600 | 1.0 | 0 |
| 14px | 460 | 1.4 | 0 |
| 12px | 540 | 1.4 | 0 |

## 版面與元件結構

此參考可先實作：收件匣資料列，包含已讀未讀、寄件者、主旨與快捷鍵提示。

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

- `#1b1938`
- `#ffffff`
- `#292827`
- `#0e3030`
- `#0e0c1f`
- `#c9b4fa`
- `#155555`
- `#fafaf8`
- `#e8e4dd`
- `#3f3a52`
- `#73706d`
- `#9a9794`
- `box-shadow: 0 1px 3px rgba(0,0,0,0.08)`
- `box-shadow: 0 8px 24px rgba(0,0,0,0.12)`

## 日期限定首頁觀察

取樣來源：https://superhuman.com/。匿名可讀的英文公開頁面。

現行官網為白色導覽與淡紫公告、深色發光 Mail 首屏：「使用 Superhuman Mail，每週節省 4 小時以上」、左側文案／右側真實 Mail 示範，搭配 Mail、Go、Docs 切換。

下方依序有品牌列、Go 助理、Grammarly／Email Assistant／Daily Briefs、客戶見證、Mail 排程、Docs、企業方案、彩色 CTA 與密集深色頁尾。

桌面首屏與全頁高度已對照實際官網取樣；窄版在排程與 Docs 等區塊仍有間距差異，且影片畫格會隨播放時間改變。

原有 DESIGN.md、PROMPTS.md 與 STITCH-PROMPT.md 保留；本檔為日期限定補充。研究頁免費瀏覽，未開啟付費方案或交易；不對外部生成服務的帳戶計費狀態作保證。

驗證範圍為匿名公開首頁、1280×720 與390×844、DPR1、桌面 UA。未完成實體手機、其他地區、完整互動或服務驗證；目前 accepted=false，不宣稱與官方一致。

## 已知差異與驗證範圍

- 最新桌面整頁高 7320px，與取樣來源相同；窄版穩定後為 10308px，來源為 10530px。下方郵件、排程、Docs 及企業區的間距、狀態仍有可見差異。
- 公開 Mail 影片曾確認載入及播放，但遠端影片可用性、精確畫格與轉場時間未固定，也未完整驗證。
- 產品分頁轉場、展開導覽與帳戶流程尚未驗證。

以上限制沿用原參考日期的比對紀錄。本次繁體中文整理不會把未驗證的影片、動畫、服務或尺寸改標為已通過；目前預覽仍未宣稱與官方完全一致。
<!-- Original AI instructions: awesome-ai-web-design -->

## 來源與使用範圍

設計資料改寫自採 MIT 授權的 VoltAgent/awesome-design-md，詳見 LICENSE 與 ATTRIBUTION.md。品牌名稱僅用於識別參考來源，並非官方授權或服務。下方 AI 指令由本專案獨立撰寫；若既有互動備註與無障礙要求衝突，以此處的可用性檢查為準。

## 重新撰寫的 AI 任務指令

語言：繁體中文（台灣用語，zh-TW）。將 DESIGN.md 放入專案，再選擇下方任務。這些指令由本專案重新撰寫；請把示範內容替換為自己的產品需求。

## 建立新頁面

```text
先閱讀隨附的 DESIGN.md，以 Superhuman 的設計語言作為介面參考。請完成以下可操作頁面：製作郵件效率工具概念頁，包含簡潔收件匣、展開的閱讀面板與可見快捷鍵。暖色中性閱讀區與深紫色外框交替，以清楚選取與快速掃讀為優先。

使用我的產品名稱、內容與資料格式，優先沿用專案現有元件及技術。開始製作樣式前，先將色彩、字體、間距與圓角整理為可重複使用的設計變數。指定字型無法取得時，使用可用的系統字型或開源字型，並說明替代方式。介面文案、按鈕、提示、錯誤訊息、圖片替代文字、註解與交付說明，一律使用繁體中文（台灣用語）。使用「專案、元件、資料、建立、預設、載入、登入、連結、儲存、影片」等台灣用語。保留品牌名稱、檔名、網址、API 識別字與可執行程式碼；HTML 語言設為 zh-Hant-TW。

讓互動元件可實際操作，並將狀態提供給輔助科技。具備可見的鍵盤焦點、清楚的欄位標示、減少動態效果，以及至少 44px 的觸控區域。參考視覺與可用性衝突時，作最小幅度的無障礙調整並記錄原因。在 390px、768px、1440px 寬度檢查版面，涵蓋繁體中文長標題、長內容、空白及錯誤狀態。金額、數量與日期依資料本身的幣別、單位及時區呈現，以 zh-TW 格式顯示，不擅自換算。最後交付完成的檔案、實際驗證結果與仍待確認的假設，不把未檢查項目宣稱為通過。
```

## 製作元件

```text
先閱讀隨附的 DESIGN.md，以 Superhuman 的設計語言作為介面參考。請製作收件匣資料列，包含已讀未讀、寄件者、主旨與快捷鍵提示。沿用現有元件慣例，放入精簡且符合實際情境的範例。比例與資訊層級應來自參考規格，不能只替通用卡片換色。依需求支援預設、焦點、停用、載入與錯誤狀態。使用有意義的示範資料，讓每個可見操作都有明確結果。

使用我的產品名稱、內容與資料格式，優先沿用專案現有元件及技術。開始製作樣式前，先將色彩、字體、間距與圓角整理為可重複使用的設計變數。指定字型無法取得時，使用可用的系統字型或開源字型，並說明替代方式。介面文案、按鈕、提示、錯誤訊息、圖片替代文字、註解與交付說明，一律使用繁體中文（台灣用語）。使用「專案、元件、資料、建立、預設、載入、登入、連結、儲存、影片」等台灣用語。保留品牌名稱、檔名、網址、API 識別字與可執行程式碼；HTML 語言設為 zh-Hant-TW。

讓互動元件可實際操作，並將狀態提供給輔助科技。具備可見的鍵盤焦點、清楚的欄位標示、減少動態效果，以及至少 44px 的觸控區域。參考視覺與可用性衝突時，作最小幅度的無障礙調整並記錄原因。在 390px、768px、1440px 寬度檢查版面，涵蓋繁體中文長標題、長內容、空白及錯誤狀態。金額、數量與日期依資料本身的幣別、單位及時區呈現，以 zh-TW 格式顯示，不擅自換算。最後交付完成的檔案、實際驗證結果與仍待確認的假設，不把未檢查項目宣稱為通過。
```

## 改造既有介面

```text
先閱讀隨附的 DESIGN.md，以 Superhuman 的設計語言作為介面參考。重新設計選定頁面，同時保留路由、資料、行為與使用者可理解的意義。先確認頁面層級，再找出最少且可重複使用的設計變數與元件調整。以下構圖作為視覺方向，依現有頁面調整：製作郵件效率工具概念頁，包含簡潔收件匣、展開的閱讀面板與可見快捷鍵。暖色中性閱讀區與深紫色外框交替，以清楚選取與快速掃讀為優先。

使用我的產品名稱、內容與資料格式，優先沿用專案現有元件及技術。開始製作樣式前，先將色彩、字體、間距與圓角整理為可重複使用的設計變數。指定字型無法取得時，使用可用的系統字型或開源字型，並說明替代方式。介面文案、按鈕、提示、錯誤訊息、圖片替代文字、註解與交付說明，一律使用繁體中文（台灣用語）。使用「專案、元件、資料、建立、預設、載入、登入、連結、儲存、影片」等台灣用語。保留品牌名稱、檔名、網址、API 識別字與可執行程式碼；HTML 語言設為 zh-Hant-TW。依完整元件群組套用變更，檢查其他頁面是否受影響，並說明調整前後的主要差異。

讓互動元件可實際操作，並將狀態提供給輔助科技。具備可見的鍵盤焦點、清楚的欄位標示、減少動態效果，以及至少 44px 的觸控區域。參考視覺與可用性衝突時，作最小幅度的無障礙調整並記錄原因。在 390px、768px、1440px 寬度檢查版面，涵蓋繁體中文長標題、長內容、空白及錯誤狀態。金額、數量與日期依資料本身的幣別、單位及時區呈現，以 zh-TW 格式顯示，不擅自換算。最後交付完成的檔案、實際驗證結果與仍待確認的假設，不把未檢查項目宣稱為通過。
```

## 逐次調整流程

1. 先指出一個可實際觀察的問題，例如層級不清或內容遭裁切。
2. 在 DESIGN.md 找到對應設計變數或元件規則，提出範圍明確的調整。
3. 套用調整，保留無關的路由與資料行為。
4. 檢查鍵盤焦點、窄版排版，以及代表性的內容與錯誤狀態。
5. 用繁體中文說明結果，以及刻意偏離參考外觀的原因。
