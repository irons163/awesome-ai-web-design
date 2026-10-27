---
version: zh-TW-2026-10-15
language: zh-TW
name: "Meta"
description: "大幅影像與藍色操作，建立明確產品層次。"

colors:
  primary: "#0064e0"
  primary-deep: "#0457cb"
  primary-soft: "#0091ff"
  on-primary: "#ffffff"
  ink-button: "#000000"
  on-ink-button: "#ffffff"
  fb-blue: "#1876f2"
  meta-link: "#385898"
  oculus-purple: "#a121ce"
  success: "#31a24c"
  success-bg: "#24e400"
  attention: "#f2a918"
  warning: "#f7b928"
  warning-bg: "#ffe200"
  critical: "#e41e3f"
  critical-strong: "#f0284a"
  canvas: "#ffffff"
  surface-soft: "#f1f4f7"
  ink-deep: "#0a1317"
  ink: "#1c1e21"
  charcoal: "#444950"
  slate: "#4b4c4f"
  steel: "#5d6c7b"
  stone: "#8595a4"
  hairline: "#ced0d4"
  hairline-soft: "#dee3e9"
  disabled-text: "#bcc0c4"

typography:
  hero-display:
    fontFamily: Optimistic VF
    fontSize: 64px
    fontWeight: 500
    lineHeight: 1.16
    fontFeature: "ss01, ss02"
  display-lg:
    fontFamily: Optimistic VF
    fontSize: 48px
    fontWeight: 500
    lineHeight: 1.17
    fontFeature: "ss01, ss02"
  heading-lg:
    fontFamily: Optimistic VF
    fontSize: 36px
    fontWeight: 500
    lineHeight: 1.28
    fontFeature: "ss01, ss02"
  heading-md:
    fontFamily: Optimistic VF
    fontSize: 28px
    fontWeight: 300
    lineHeight: 1.21
    fontFeature: "ss01, ss02"
  heading-sm:
    fontFamily: Optimistic VF
    fontSize: 24px
    fontWeight: 500
    lineHeight: 1.25
    fontFeature: "ss01, ss02"
  subtitle-lg:
    fontFamily: Optimistic VF
    fontSize: 18px
    fontWeight: 700
    lineHeight: 1.44
  subtitle-md:
    fontFamily: Optimistic VF
    fontSize: 18px
    fontWeight: 400
    lineHeight: 1.44
  body-md-bold:
    fontFamily: Optimistic VF
    fontSize: 16px
    fontWeight: 700
    lineHeight: 1.50
    letterSpacing: -0.16px
  body-md:
    fontFamily: Optimistic VF
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.50
    letterSpacing: -0.16px
  body-sm-bold:
    fontFamily: Optimistic VF
    fontSize: 14px
    fontWeight: 700
    lineHeight: 1.43
    letterSpacing: -0.14px
  body-sm:
    fontFamily: Optimistic VF
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.43
    letterSpacing: -0.14px
  caption-bold:
    fontFamily: Optimistic VF
    fontSize: 12px
    fontWeight: 700
    lineHeight: 1.33
  caption:
    fontFamily: Optimistic VF
    fontSize: 12px
    fontWeight: 400
    lineHeight: 1.33
  button-md:
    fontFamily: Optimistic VF
    fontSize: 14px
    fontWeight: 700
    lineHeight: 1.43
    letterSpacing: -0.14px
  link-md:
    fontFamily: Optimistic VF
    fontSize: 16px
    fontWeight: 700
    lineHeight: 1.50
    letterSpacing: -0.16px

rounded:
  xs: 2px
  sm: 4px
  md: 6px
  lg: 8px
  xl: 16px
  xxl: 24px
  xxxl: 32px
  feature: 40px
  full: 100px
  circle: 9999px

spacing:
  xxs: 4px
  xs: 8px
  sm: 10px
  md: 12px
  base: 16px
  lg: 20px
  xl: 24px
  xxl: 32px
  xxxl: 40px
  section-sm: 48px
  section: 64px
  section-lg: 80px
  hero: 120px

components:
  button-primary:
    backgroundColor: "{colors.ink-button}"
    textColor: "{colors.on-ink-button}"
    typography: "{typography.button-md}"
    rounded: "{rounded.full}"
    padding: "14px 30px"
  button-primary-pressed:
    backgroundColor: "{colors.charcoal}"
    textColor: "{colors.on-ink-button}"
  button-primary-disabled:
    backgroundColor: "{colors.disabled-text}"
    textColor: "{colors.canvas}"
  button-buy-cta:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.button-md}"
    rounded: "{rounded.full}"
    padding: "14px 30px"
  button-buy-cta-pressed:
    backgroundColor: "{colors.primary-deep}"
    textColor: "{colors.on-primary}"
  button-secondary:
    backgroundColor: "transparent"
    textColor: "{colors.ink-deep}"
    typography: "{typography.button-md}"
    rounded: "{rounded.full}"
    padding: "12px 28px"
    border: "2px solid {colors.ink-deep}"
  button-ghost:
    backgroundColor: "transparent"
    textColor: "{colors.ink-deep}"
    typography: "{typography.button-md}"
    rounded: "{rounded.full}"
    padding: "10px 22px"
    border: "2px solid rgba(10, 19, 23, 0.12)"
  button-pill-tab:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.body-sm-bold}"
    rounded: "{rounded.full}"
    padding: "8px 16px"
    border: "1px solid {colors.hairline}"
  button-pill-tab-active:
    backgroundColor: "{colors.ink-deep}"
    textColor: "{colors.canvas}"
  button-icon-circular:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    rounded: "{rounded.circle}"
    size: 40px
  card-product-feature:
    backgroundColor: "{colors.canvas}"
    rounded: "{rounded.xxxl}"
    padding: "{spacing.xxl}"
    border: "1px solid {colors.hairline-soft}"
  card-feature-photo:
    backgroundColor: "{colors.canvas}"
    rounded: "{rounded.xxxl}"
    padding: "0"
    border: "none"
  card-promo-strip:
    backgroundColor: "{colors.ink-deep}"
    textColor: "{colors.canvas}"
    rounded: "{rounded.xxxl}"
    padding: "{spacing.section}"
  card-icon-feature:
    backgroundColor: "{colors.canvas}"
    rounded: "{rounded.xl}"
    padding: "{spacing.xl}"
  card-checkout-summary:
    backgroundColor: "{colors.canvas}"
    rounded: "{rounded.xl}"
    padding: "{spacing.xl}"
    border: "1px solid {colors.hairline-soft}"
    shadow: "rgba(20, 22, 26, 0.3) 0px 1px 4px 0px"
  product-thumbnail:
    backgroundColor: "{colors.surface-soft}"
    rounded: "{rounded.xl}"
    padding: "{spacing.base}"
    aspect-ratio: "1 / 1"
  text-input:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.lg}"
    padding: "{spacing.md}"
    border: "1px solid {colors.hairline}"
    height: 44px
  text-input-focused:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    border: "2px solid {colors.fb-blue}"
  text-input-error:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    border: "1px solid {colors.critical-strong}"
  search-pill:
    backgroundColor: "{colors.surface-soft}"
    textColor: "{colors.steel}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.full}"
    padding: "{spacing.md} {spacing.lg}"
    height: 40px
  radio-option:
    backgroundColor: "{colors.canvas}"
    rounded: "{rounded.lg}"
    padding: "{spacing.lg}"
    border: "1px solid rgba(10, 19, 23, 0.12)"
  radio-option-selected:
    backgroundColor: "{colors.canvas}"
    rounded: "{rounded.lg}"
    border: "2px solid #0143b5"
  color-swatch-circle:
    rounded: "{rounded.circle}"
    size: 32px
    border: "2px solid {colors.canvas}"
  badge-promo-yellow:
    backgroundColor: "{colors.warning}"
    textColor: "{colors.ink-deep}"
    typography: "{typography.caption-bold}"
    rounded: "{rounded.full}"
    padding: "4px 10px"
  badge-attention:
    backgroundColor: "{colors.attention}"
    textColor: "{colors.canvas}"
    typography: "{typography.caption-bold}"
    rounded: "{rounded.full}"
    padding: "4px 10px"
  badge-success:
    backgroundColor: "{colors.success}"
    textColor: "{colors.canvas}"
    typography: "{typography.caption-bold}"
    rounded: "{rounded.full}"
    padding: "4px 10px"
  badge-critical:
    backgroundColor: "{colors.critical}"
    textColor: "{colors.canvas}"
    typography: "{typography.caption-bold}"
    rounded: "{rounded.full}"
    padding: "4px 10px"
  promo-banner:
    backgroundColor: "{colors.ink-deep}"
    textColor: "{colors.canvas}"
    typography: "{typography.body-sm-bold}"
    padding: "{spacing.md} {spacing.xl}"
  faq-accordion-item:
    backgroundColor: "{colors.canvas}"
    rounded: "{rounded.xl}"
    padding: "{spacing.xl}"
    border: "1px solid {colors.hairline-soft}"
  why-buy-tile:
    backgroundColor: "{colors.canvas}"
    rounded: "{rounded.xl}"
    padding: "{spacing.xxl} {spacing.xl}"
    border: "1px solid {colors.hairline-soft}"
  warranty-card:
    backgroundColor: "{colors.surface-soft}"
    rounded: "{rounded.xxl}"
    padding: "{spacing.xxl}"
  footer-region:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.steel}"
    typography: "{typography.body-sm}"
    padding: "{spacing.section} {spacing.xxl}"
    border: "1px solid {colors.hairline-soft}"
  hero-band-marketing:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.canvas}"
    typography: "{typography.hero-display}"
    rounded: "{rounded.xxxl}"
    padding: "{spacing.section-lg}"
  product-gallery-pdp:
    backgroundColor: "{colors.canvas}"
    rounded: "{rounded.xxxl}"
    padding: "{spacing.base}"
  color-sku-picker-row:
    backgroundColor: "{colors.surface-soft}"
    rounded: "{rounded.lg}"
    padding: "{spacing.base}"
  feature-icon-row:
    backgroundColor: "{colors.canvas}"
    rounded: "{rounded.xl}"
    padding: "{spacing.xl}"
    border: "1px solid {colors.hairline-soft}"
  tech-specs-table:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.lg}"
    padding: "{spacing.lg}"
    border: "1px solid {colors.hairline-soft}"
  testimonial-customer-card:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.xl}"
    padding: "{spacing.xxl}"
    border: "1px solid {colors.hairline-soft}"
---

# Meta 延伸設計規格

語言：繁體中文（台灣用語，zh-TW）。在地化更新：2026-10-20。

## 來源與規格層次

這份規格將較早保存的品牌設計資料重新整理為可實作的繁體中文文件。來源設定中的色碼、字級、字重、行高、間距、圓角與元件識別字保留，供開發工具讀取；敘述與操作指令改用台灣用語。這些延伸設定不等同於目前日期限定首頁的逐項實測值，若兩者不同，依下方的日期限定觀察及對應預覽判讀。

- 原始資料版本：`1a783491c9539c3153c2fc96c16d59131e024f4e`。
- 原始 DESIGN.md 摘要：`b6c7fe474746207740a39258d8d01d75073f6769d2fc569868f90941e47ddd78`。
- 目前首頁參考日期：2026-10-11。
- 目前公開來源：https://www.meta.com/ca/。
- 目前預覽：`official-drafts/meta.html`。
- 台灣繁體中文規格與指令是本次重新產出的內容；來源截圖及原生生成紀錄保留原貌。

## 整體視覺方向

大幅影像與藍色操作，建立明確產品層次。

製作連網裝置展示頁，明亮產品區與深色沉浸範例交錯。主要操作維持一致的藍色，提供直接比較功能，不要求使用者捲過所有照片。

先建立主要內容、輔助資訊與操作之間的層級，再套用色彩及裝飾。品牌色應有明確用途；主要操作、選取、錯誤及停用狀態要能分辨。避免將多套參考風格混在同一頁，也不要僅替換通用卡片的顏色。

## 色彩、字型與繁體中文排版

上方來源設定保留原始色彩角色與數值。主要品牌色用於最重要的操作；背景、內容表面、主要文字、次要文字與分隔線各自維持一致用途。資訊不能只依賴顏色，狀態須同時有文字或圖示標示。

原字型名稱可作為拉丁字母參考。繁體中文字型優先使用可取得的 `Noto Sans TC`、`PingFang TC`、`Microsoft JhengHei`，最後才使用 `sans-serif`。原字型未涵蓋中文時必須提供替代，不以缺字或圖片文字呈現正文。專有字型無法取得時，記錄替代字型與可能的字寬差異。

中文標題以語意分段，避免為模仿英文大寫字距而拉散中文字。內文行高、欄寬與段落間距以可讀性為準；英文型號、網址、程式碼及長連結可以換行或在自己的區域捲動，不可撐開整份文件。價格、規格及比較欄位保持數字與單位對齊。

| 字級 | 字重 | 行高 | 字距 |
| --- | --- | --- | --- |
| 64px | 500 | 1.16 | 0 |
| 48px | 500 | 1.17 | 0 |
| 36px | 500 | 1.28 | 0 |
| 28px | 300 | 1.21 | 0 |
| 24px | 500 | 1.25 | 0 |
| 18px | 700 | 1.44 | 0 |
| 18px | 400 | 1.44 | 0 |
| 16px | 400 | 1.50 | -0.16px |
| 16px | 700 | 1.50 | -0.16px |
| 14px | 400 | 1.43 | -0.14px |
| 14px | 700 | 1.43 | -0.14px |
| 12px | 700 | 1.33 | 0 |
| 12px | 400 | 1.33 | 0 |
| 14px | 700 | 1.43 | -0.14px |
| 16px | 700 | 1.50 | -0.16px |

## 版面與元件結構

此參考可先實作：裝置特色選擇器，包含可辨識的選取狀態與圖片說明。

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

- `-0.14px`
- `-0.16px`
- `max-width: 380px`
- `rgba(0, 0, 0, 0.2) 1px 1px 0px 0px`
- `rgba(20, 22, 26, 0.3) 0px 1px 4px 0px`
- `rgba(255, 255, 255, 0.1)`
- `rgba(10, 19, 23, 0.12)`
- `14px 30px`
- `2px solid {colors.ink-deep}`
- `12px 28px`
- `2px solid rgba(10, 19, 23, 0.12)`
- `10px 22px`
- `1px solid {colors.hairline}`
- `8px 16px`
- `1px solid {colors.hairline-soft}`
- `2px solid {colors.fb-blue}`
- `1px solid {colors.critical-strong}`
- `1px solid rgba(10, 19, 23, 0.12)`
- `2px solid #0143b5`
- `2px solid {colors.canvas}`
- `4px 10px`

## 日期限定首頁觀察

2026-10-11 UTC實際觀測加拿大英文公開首頁，使用認識全新 Meta Glasses首屏及LISA 演繹 Meta Glasses、Ray-Ban Meta、Ray-Ban Meta Audio、Meta VR Glasses、Muse Charm、Oakley Meta、Meta Ray-Ban Display、Meta Quest 3S八個商品區塊。Optimistic VF字型、藍色膠囊按鈕、圓角照片卡和白色頁尾構成主要視覺。窄版為單欄商品及橫向類別／服務卡，保留當時Meta Store已展開的頁尾群組。67份原始公開素材共7.8MB，未解決的直接下載失敗為0。桌面6964px共10段、窄版8787px共11段，主代理實看全部6張對照圖，20個h1–h3的文字與幾何量測沒有差異；以role=heading繪製的首屏也以實際截圖檢視，不把缺少h2標籤誤認成缺內容。

**已比對主要靜態畫面，仍有差異；accepted=false，不宣稱與官方一致。**

既有設計分析及原始指令保留。本次官方來源、真實 Google Stitch MCP 原始輸出、校正檔與實際瀏覽器畫面分開記錄。研究頁面免費瀏覽，沒有啟動付費方案或交易。

## 已知差異與驗證範圍

- 這次要求MOBILE但供應商回傳DESKTOP 2560×16646；原生稿照片為大量佔位框，沒有當成官方一致成品。原始檔完整保存，成品是後續按實際來源校正的獨立版本。
- 首屏原始影片的播放時間、人物影格及Play／Pause按鈕狀態與來源取樣不同。窄版首屏導覽背景模糊／透明度和選單背景透出的影片色彩及捲動條有可見差異；導覽過渡時機未同步。
- 桌面第一次來源取樣尚在調整高度，第一段高度6900px，後續6964px，造成17項64.4px標題差異；該批保留為私人診斷，最終桌面已改用穩定6964px全頁取樣，不混算為相同畫面。
- 窄版根選單已實看，X／Escape通過；選單次層、桌面選單、地區／搜尋／影片控制、類別／服務輪播其他狀態、全部頁尾手風琴及Newsletter/購物/帳號/融資服務未驗證。沒有輸入個資或建立帳號、訂閱、購物、融資。
- 390px為桌面UA響應式取樣；官網內容會依時間、地區和載入狀態改變。主要靜態畫面已核對但不宣稱完全一致；正式部署仍未驗證。

以上限制沿用原參考日期的比對紀錄。本次繁體中文整理不會把未驗證的影片、動畫、服務或尺寸改標為已通過；目前預覽仍未宣稱與官方完全一致。
<!-- Original AI instructions: awesome-ai-web-design -->

## 來源與使用範圍

設計資料改寫自採 MIT 授權的 VoltAgent/awesome-design-md，詳見 LICENSE 與 ATTRIBUTION.md。品牌名稱僅用於識別參考來源，並非官方授權或服務。下方 AI 指令由本專案獨立撰寫；若既有互動備註與無障礙要求衝突，以此處的可用性檢查為準。

## 重新撰寫的 AI 任務指令

語言：繁體中文（台灣用語，zh-TW）。將 DESIGN.md 放入專案，再選擇下方任務。這些指令由本專案重新撰寫；請把示範內容替換為自己的產品需求。

## 建立新頁面

```text
先閱讀隨附的 DESIGN.md，以 Meta 的設計語言作為介面參考。請完成以下可操作頁面：製作連網裝置展示頁，明亮產品區與深色沉浸範例交錯。主要操作維持一致的藍色，提供直接比較功能，不要求使用者捲過所有照片。

使用我的產品名稱、內容與資料格式，優先沿用專案現有元件及技術。開始製作樣式前，先將色彩、字體、間距與圓角整理為可重複使用的設計變數。指定字型無法取得時，使用可用的系統字型或開源字型，並說明替代方式。介面文案、按鈕、提示、錯誤訊息、圖片替代文字、註解與交付說明，一律使用繁體中文（台灣用語）。使用「專案、元件、資料、建立、預設、載入、登入、連結、儲存、影片」等台灣用語。保留品牌名稱、檔名、網址、API 識別字與可執行程式碼；HTML 語言設為 zh-Hant-TW。

讓互動元件可實際操作，並將狀態提供給輔助科技。具備可見的鍵盤焦點、清楚的欄位標示、減少動態效果，以及至少 44px 的觸控區域。參考視覺與可用性衝突時，作最小幅度的無障礙調整並記錄原因。在 390px、768px、1440px 寬度檢查版面，涵蓋繁體中文長標題、長內容、空白及錯誤狀態。金額、數量與日期依資料本身的幣別、單位及時區呈現，以 zh-TW 格式顯示，不擅自換算。最後交付完成的檔案、實際驗證結果與仍待確認的假設，不把未檢查項目宣稱為通過。
```

## 製作元件

```text
先閱讀隨附的 DESIGN.md，以 Meta 的設計語言作為介面參考。請製作裝置特色選擇器，包含可辨識的選取狀態與圖片說明。沿用現有元件慣例，放入精簡且符合實際情境的範例。比例與資訊層級應來自參考規格，不能只替通用卡片換色。依需求支援預設、焦點、停用、載入與錯誤狀態。使用有意義的示範資料，讓每個可見操作都有明確結果。

使用我的產品名稱、內容與資料格式，優先沿用專案現有元件及技術。開始製作樣式前，先將色彩、字體、間距與圓角整理為可重複使用的設計變數。指定字型無法取得時，使用可用的系統字型或開源字型，並說明替代方式。介面文案、按鈕、提示、錯誤訊息、圖片替代文字、註解與交付說明，一律使用繁體中文（台灣用語）。使用「專案、元件、資料、建立、預設、載入、登入、連結、儲存、影片」等台灣用語。保留品牌名稱、檔名、網址、API 識別字與可執行程式碼；HTML 語言設為 zh-Hant-TW。

讓互動元件可實際操作，並將狀態提供給輔助科技。具備可見的鍵盤焦點、清楚的欄位標示、減少動態效果，以及至少 44px 的觸控區域。參考視覺與可用性衝突時，作最小幅度的無障礙調整並記錄原因。在 390px、768px、1440px 寬度檢查版面，涵蓋繁體中文長標題、長內容、空白及錯誤狀態。金額、數量與日期依資料本身的幣別、單位及時區呈現，以 zh-TW 格式顯示，不擅自換算。最後交付完成的檔案、實際驗證結果與仍待確認的假設，不把未檢查項目宣稱為通過。
```

## 改造既有介面

```text
先閱讀隨附的 DESIGN.md，以 Meta 的設計語言作為介面參考。重新設計選定頁面，同時保留路由、資料、行為與使用者可理解的意義。先確認頁面層級，再找出最少且可重複使用的設計變數與元件調整。以下構圖作為視覺方向，依現有頁面調整：製作連網裝置展示頁，明亮產品區與深色沉浸範例交錯。主要操作維持一致的藍色，提供直接比較功能，不要求使用者捲過所有照片。

使用我的產品名稱、內容與資料格式，優先沿用專案現有元件及技術。開始製作樣式前，先將色彩、字體、間距與圓角整理為可重複使用的設計變數。指定字型無法取得時，使用可用的系統字型或開源字型，並說明替代方式。介面文案、按鈕、提示、錯誤訊息、圖片替代文字、註解與交付說明，一律使用繁體中文（台灣用語）。使用「專案、元件、資料、建立、預設、載入、登入、連結、儲存、影片」等台灣用語。保留品牌名稱、檔名、網址、API 識別字與可執行程式碼；HTML 語言設為 zh-Hant-TW。依完整元件群組套用變更，檢查其他頁面是否受影響，並說明調整前後的主要差異。

讓互動元件可實際操作，並將狀態提供給輔助科技。具備可見的鍵盤焦點、清楚的欄位標示、減少動態效果，以及至少 44px 的觸控區域。參考視覺與可用性衝突時，作最小幅度的無障礙調整並記錄原因。在 390px、768px、1440px 寬度檢查版面，涵蓋繁體中文長標題、長內容、空白及錯誤狀態。金額、數量與日期依資料本身的幣別、單位及時區呈現，以 zh-TW 格式顯示，不擅自換算。最後交付完成的檔案、實際驗證結果與仍待確認的假設，不把未檢查項目宣稱為通過。
```

## 逐次調整流程

1. 先指出一個可實際觀察的問題，例如層級不清或內容遭裁切。
2. 在 DESIGN.md 找到對應設計變數或元件規則，提出範圍明確的調整。
3. 套用調整，保留無關的路由與資料行為。
4. 檢查鍵盤焦點、窄版排版，以及代表性的內容與錯誤狀態。
5. 用繁體中文說明結果，以及刻意偏離參考外觀的原因。
