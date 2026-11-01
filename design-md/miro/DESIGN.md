---
version: zh-TW-2026-10-15
language: zh-TW
name: "Miro"
description: "明亮黃色與便箋色彩，讓協作空間有秩序。"

colors:
  primary: "#1c1c1e"
  on-primary: "#ffffff"
  brand-yellow: "#ffd02f"
  brand-yellow-deep: "#fcb900"
  yellow-light: "#fff4c4"
  yellow-dark: "#746019"
  brand-blue: "#4262ff"
  blue-450: "#5b76fe"
  blue-pressed: "#2a41b6"
  brand-coral: "#ff9999"
  coral-light: "#ffc6c6"
  coral-dark: "#600000"
  brand-rose: "#ffd8f4"
  rose-light: "#fde0f0"
  brand-pink: "#fde0f0"
  brand-teal: "#0fbcb0"
  teal-light: "#c3faf5"
  moss-dark: "#187574"
  brand-orange-light: "#ffe6cd"
  brand-red: "#fbd4d4"
  brand-red-dark: "#e3c5c5"
  success-accent: "#00b473"
  canvas: "#ffffff"
  surface: "#f7f8fa"
  surface-soft: "#fafbfc"
  surface-yellow: "#fff8e0"
  surface-pricing-featured: "#f5f3ff"
  hairline: "#e0e2e8"
  hairline-soft: "#eef0f3"
  hairline-strong: "#c7cad5"
  ink-deep: "#050038"
  ink: "#1c1c1e"
  charcoal: "#2c2c34"
  slate: "#555a6a"
  steel: "#6b6f7e"
  stone: "#8e91a0"
  muted: "#a5a8b5"
  on-dark: "#ffffff"
  on-dark-muted: "#a5a8b5"
  footer-bg: "#1c1c1e"

typography:
  hero-display:
    fontFamily: Roobert PRO
    fontSize: 80px
    fontWeight: 500
    lineHeight: 1.05
    letterSpacing: -2px
  display-lg:
    fontFamily: Roobert PRO
    fontSize: 60px
    fontWeight: 500
    lineHeight: 1.10
    letterSpacing: -1.5px
  heading-1:
    fontFamily: Roobert PRO
    fontSize: 48px
    fontWeight: 500
    lineHeight: 1.15
    letterSpacing: -1px
  heading-2:
    fontFamily: Roobert PRO
    fontSize: 36px
    fontWeight: 500
    lineHeight: 1.20
    letterSpacing: -0.5px
  heading-3:
    fontFamily: Roobert PRO
    fontSize: 28px
    fontWeight: 500
    lineHeight: 1.25
  heading-4:
    fontFamily: Roobert PRO
    fontSize: 22px
    fontWeight: 500
    lineHeight: 1.30
  heading-5:
    fontFamily: Roobert PRO
    fontSize: 18px
    fontWeight: 500
    lineHeight: 1.40
  subtitle:
    fontFamily: Roobert PRO
    fontSize: 18px
    fontWeight: 400
    lineHeight: 1.50
  body-md:
    fontFamily: Roobert PRO
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.50
  body-md-medium:
    fontFamily: Roobert PRO
    fontSize: 16px
    fontWeight: 500
    lineHeight: 1.50
  body-sm:
    fontFamily: Roobert PRO
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.50
  body-sm-medium:
    fontFamily: Roobert PRO
    fontSize: 14px
    fontWeight: 500
    lineHeight: 1.50
  caption:
    fontFamily: Roobert PRO
    fontSize: 13px
    fontWeight: 400
    lineHeight: 1.40
  caption-bold:
    fontFamily: Roobert PRO
    fontSize: 13px
    fontWeight: 600
    lineHeight: 1.40
  micro:
    fontFamily: Roobert PRO
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1.40
  micro-uppercase:
    fontFamily: Roobert PRO
    fontSize: 11px
    fontWeight: 600
    lineHeight: 1.40
    letterSpacing: 0.5px
  button-md:
    fontFamily: Roobert PRO
    fontSize: 14px
    fontWeight: 500
    lineHeight: 1.30
  stat-display:
    fontFamily: Roobert PRO
    fontSize: 64px
    fontWeight: 500
    lineHeight: 1.10
    letterSpacing: -1.5px

rounded:
  xs: 4px
  sm: 6px
  md: 8px
  lg: 12px
  xl: 16px
  xxl: 20px
  xxxl: 28px
  feature: 32px
  full: 9999px

spacing:
  xxs: 4px
  xs: 8px
  sm: 12px
  md: 16px
  lg: 20px
  xl: 24px
  xxl: 32px
  xxxl: 40px
  section-sm: 48px
  section: 64px
  section-lg: 96px
  hero: 120px

components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.button-md}"
    rounded: "{rounded.full}"
    padding: "12px 24px"
  button-primary-pressed:
    backgroundColor: "{colors.charcoal}"
    textColor: "{colors.on-primary}"
  button-primary-disabled:
    backgroundColor: "{colors.hairline}"
    textColor: "{colors.muted}"
  button-yellow:
    backgroundColor: "{colors.brand-yellow}"
    textColor: "{colors.primary}"
    typography: "{typography.button-md}"
    rounded: "{rounded.full}"
    padding: "12px 24px"
  button-blue:
    backgroundColor: "{colors.brand-blue}"
    textColor: "{colors.on-primary}"
    typography: "{typography.button-md}"
    rounded: "{rounded.full}"
    padding: "12px 24px"
  button-secondary:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    typography: "{typography.button-md}"
    rounded: "{rounded.full}"
    padding: "12px 24px"
    border: "1px solid {colors.hairline-strong}"
  button-on-dark:
    backgroundColor: "{colors.on-dark}"
    textColor: "{colors.primary}"
    typography: "{typography.button-md}"
    rounded: "{rounded.full}"
    padding: "12px 24px"
  button-ghost:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    typography: "{typography.button-md}"
    rounded: "{rounded.md}"
    padding: "8px 12px"
  button-link:
    backgroundColor: "transparent"
    textColor: "{colors.brand-blue}"
    typography: "{typography.body-sm-medium}"
    padding: "0"
  button-icon-circular:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    rounded: "{rounded.full}"
    size: 36px
    border: "1px solid {colors.hairline}"
  card-base:
    backgroundColor: "{colors.canvas}"
    rounded: "{rounded.xl}"
    padding: "{spacing.xl}"
    border: "1px solid {colors.hairline-soft}"
  card-feature:
    backgroundColor: "{colors.canvas}"
    rounded: "{rounded.xxxl}"
    padding: "{spacing.xxl}"
    border: "1px solid {colors.hairline-soft}"
  card-feature-yellow:
    backgroundColor: "{colors.brand-yellow}"
    textColor: "{colors.primary}"
    rounded: "{rounded.xxxl}"
    padding: "{spacing.xxl}"
  card-feature-coral:
    backgroundColor: "{colors.coral-light}"
    textColor: "{colors.primary}"
    rounded: "{rounded.xxxl}"
    padding: "{spacing.xxl}"
  card-feature-teal:
    backgroundColor: "{colors.teal-light}"
    textColor: "{colors.primary}"
    rounded: "{rounded.xxxl}"
    padding: "{spacing.xxl}"
  card-feature-rose:
    backgroundColor: "{colors.rose-light}"
    textColor: "{colors.primary}"
    rounded: "{rounded.xxxl}"
    padding: "{spacing.xxl}"
  card-customer-story:
    backgroundColor: "{colors.canvas}"
    rounded: "{rounded.xxxl}"
    padding: "0"
    border: "1px solid {colors.hairline-soft}"
  card-stat:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    typography: "{typography.stat-display}"
    padding: "{spacing.lg}"
  pricing-card:
    backgroundColor: "{colors.canvas}"
    rounded: "{rounded.xl}"
    padding: "{spacing.xxl}"
    border: "1px solid {colors.hairline}"
  pricing-card-featured:
    backgroundColor: "{colors.surface-pricing-featured}"
    rounded: "{rounded.xl}"
    padding: "{spacing.xxl}"
    border: "2px solid {colors.brand-blue}"
  pricing-card-enterprise:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.xl}"
    padding: "{spacing.xxl}"
  text-input:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: "{spacing.sm} {spacing.md}"
    border: "1px solid {colors.hairline-strong}"
    height: 44px
  text-input-focused:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    border: "2px solid {colors.brand-blue}"
  search-pill:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.steel}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.md}"
    padding: "{spacing.xs} {spacing.md}"
    height: 40px
    border: "1px solid {colors.hairline}"
  filter-dropdown:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.body-sm-medium}"
    rounded: "{rounded.full}"
    padding: "{spacing.xs} {spacing.md}"
    border: "1px solid {colors.hairline-strong}"
  pill-tab:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.steel}"
    typography: "{typography.body-sm-medium}"
    rounded: "{rounded.full}"
    padding: "{spacing.xs} {spacing.md}"
    border: "1px solid {colors.hairline}"
  pill-tab-active:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.full}"
    border: "1px solid {colors.primary}"
  toggle-monthly-yearly:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.full}"
    padding: "4px"
  badge-promo:
    backgroundColor: "{colors.brand-yellow}"
    textColor: "{colors.primary}"
    typography: "{typography.caption-bold}"
    rounded: "{rounded.full}"
    padding: "4px 10px"
  badge-tag-yellow:
    backgroundColor: "{colors.surface-yellow}"
    textColor: "{colors.yellow-dark}"
    typography: "{typography.caption-bold}"
    rounded: "{rounded.full}"
    padding: "4px 10px"
  badge-tag-purple:
    backgroundColor: "{colors.surface-pricing-featured}"
    textColor: "{colors.brand-blue}"
    typography: "{typography.caption-bold}"
    rounded: "{rounded.full}"
    padding: "4px 10px"
  badge-tag-coral:
    backgroundColor: "{colors.coral-light}"
    textColor: "{colors.coral-dark}"
    typography: "{typography.caption-bold}"
    rounded: "{rounded.full}"
    padding: "4px 10px"
  badge-success:
    backgroundColor: "{colors.success-accent}"
    textColor: "{colors.on-primary}"
    typography: "{typography.caption-bold}"
    rounded: "{rounded.full}"
    padding: "4px 10px"
  badge-discount:
    backgroundColor: "{colors.brand-yellow}"
    textColor: "{colors.primary}"
    typography: "{typography.caption-bold}"
    rounded: "{rounded.sm}"
    padding: "2px 6px"
  promo-banner:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.body-sm-medium}"
    padding: "{spacing.sm} {spacing.md}"
  comparison-table:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.md}"
    border: "1px solid {colors.hairline}"
  comparison-row:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    padding: "{spacing.md} {spacing.lg}"
    border: "0 0 1px {colors.hairline-soft} solid"
  template-card:
    backgroundColor: "{colors.canvas}"
    rounded: "{rounded.xl}"
    padding: "{spacing.md}"
    border: "1px solid {colors.hairline}"
  whiteboard-mockup:
    backgroundColor: "{colors.canvas}"
    rounded: "{rounded.xl}"
    padding: "0"
    border: "1px solid {colors.hairline-soft}"
    shadow: "rgba(5, 0, 56, 0.08) 0px 12px 32px -4px"
  faq-accordion-item:
    backgroundColor: "{colors.canvas}"
    rounded: "{rounded.md}"
    padding: "{spacing.xl}"
    border: "0 0 1px {colors.hairline} solid"
  logo-wall-item:
    backgroundColor: "transparent"
    textColor: "{colors.steel}"
    typography: "{typography.body-md-medium}"
    padding: "{spacing.lg}"
  hero-band-marketing:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.hero-display}"
    rounded: "0"
    padding: "{spacing.hero}"
  cta-banner-dark:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.feature}"
    padding: "{spacing.section}"
  industry-tile:
    backgroundColor: "{colors.canvas}"
    rounded: "{rounded.xl}"
    padding: "{spacing.xl}"
    border: "1px solid {colors.hairline-soft}"
  capterra-badge:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.caption}"
    rounded: "{rounded.md}"
    padding: "{spacing.sm} {spacing.md}"
    border: "1px solid {colors.hairline}"
  footer-region:
    backgroundColor: "{colors.footer-bg}"
    textColor: "{colors.on-dark}"
    typography: "{typography.body-sm}"
    padding: "{spacing.section} {spacing.xxl}"
  footer-link:
    backgroundColor: "transparent"
    textColor: "{colors.on-dark-muted}"
    typography: "{typography.body-sm}"
    padding: "{spacing.xxs} 0"
  app-store-badge:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.primary}"
    typography: "{typography.caption-bold}"
    rounded: "{rounded.md}"
    padding: "{spacing.sm} {spacing.md}"
---

# Miro 延伸設計規格

語言：繁體中文（台灣用語，zh-TW）。在地化更新：2026-11-01。

## 來源與規格層次

這份規格將較早保存的品牌設計資料重新整理為可實作的繁體中文文件。來源設定中的色碼、字級、字重、行高、間距、圓角與元件識別字保留，供開發工具讀取；敘述與操作指令改用台灣用語。這些延伸設定不等同於目前日期限定首頁的逐項實測值，若兩者不同，依下方的日期限定觀察及對應預覽判讀。

- 原始資料版本：`1a783491c9539c3153c2fc96c16d59131e024f4e`。
- 原始 DESIGN.md 摘要：`93849d046658d7f21556671761012bc2b757c9d0e681937339dc6634df2cb4f2`。
- 目前首頁參考日期：2026-10-10。
- 目前公開來源：https://miro.com/。
- 目前預覽：`official-drafts/miro.html`。
- 台灣繁體中文規格與指令是本次重新產出的內容；來源截圖及原生生成紀錄保留原貌。

## 整體視覺方向

明亮黃色與便箋色彩，讓協作空間有秩序。

製作工作坊白板總覽，包含範本卡片、參與者狀態與小型畫布預覽。黃色建立工作空間識別，便利貼顏色依意義分組，不隨機分配。

先建立主要內容、輔助資訊與操作之間的層級，再套用色彩及裝飾。品牌色應有明確用途；主要操作、選取、錯誤及停用狀態要能分辨。避免將多套參考風格混在同一頁，也不要僅替換通用卡片的顏色。

## 色彩、字型與繁體中文排版

上方來源設定保留原始色彩角色與數值。主要品牌色用於最重要的操作；背景、內容表面、主要文字、次要文字與分隔線各自維持一致用途。資訊不能只依賴顏色，狀態須同時有文字或圖示標示。

原字型名稱可作為拉丁字母參考。繁體中文字型優先使用可取得的 `Noto Sans TC`、`PingFang TC`、`Microsoft JhengHei`，最後才使用 `sans-serif`。原字型未涵蓋中文時必須提供替代，不以缺字或圖片文字呈現正文。專有字型無法取得時，記錄替代字型與可能的字寬差異。

中文標題以語意分段，避免為模仿英文大寫字距而拉散中文字。內文行高、欄寬與段落間距以可讀性為準；英文型號、網址、程式碼及長連結可以換行或在自己的區域捲動，不可撐開整份文件。價格、規格及比較欄位保持數字與單位對齊。

| 字級 | 字重 | 行高 | 字距 |
| --- | --- | --- | --- |
| 80px | 500 | 1.05 | -2px |
| 60px | 500 | 1.10 | -1.5px |
| 48px | 500 | 1.15 | -1px |
| 36px | 500 | 1.20 | -0.5px |
| 28px | 500 | 1.25 | 0 |
| 22px | 500 | 1.30 | 0 |
| 18px | 500 | 1.40 | 0 |
| 18px | 400 | 1.50 | 0 |
| 16px | 400 | 1.50 | 0 |
| 16px | 500 | 1.50 | 0 |
| 14px | 400 | 1.50 | 0 |
| 14px | 500 | 1.50 | 0 |
| 13px | 400 | 1.40 | 0 |
| 13px | 600 | 1.40 | 0 |
| 12px | 500 | 1.40 | 0 |
| 11px | 600 | 1.40 | 0.5px |
| 14px | 500 | 1.30 | 0 |
| 64px | 500 | 1.10 | -1.5px |

## 版面與元件結構

此參考可先實作：工作坊範本卡片，包含預覽筆記、所需時間與開始操作。

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

- `rgba(5, 0, 56, 0.04) 0px 1px 2px 0px`
- `rgba(5, 0, 56, 0.06) 0px 4px 12px 0px`
- `rgba(5, 0, 56, 0.08) 0px 12px 32px -4px`
- `rgba(5, 0, 56, 0.12) 0px 16px 48px -8px`
- `12px 24px`
- `1px solid {colors.hairline-strong}`
- `8px 12px`
- `1px solid {colors.hairline}`
- `1px solid {colors.hairline-soft}`
- `2px solid {colors.brand-blue}`
- `4px`
- `4px 10px`
- `2px 6px`

## 日期限定首頁觀察

來源：https://miro.com/。原始取樣時間保留於 UTC 紀錄，oct10 工作檔名不表示所有檢查都在 10 月 10 日完成。

現行首頁使用灰白留白、黃色 Miro 標誌、淡藍 CTA、細框圓角圖卡。「讓人類協作跟上 AI 的速度」置中，搭配 email／Get Started Free、真正的研究／流程／圖表截圖與品牌列。

下方是 Research／Roadmap & Planning／Diagrams／Workshops、從點子順暢走向成果、PepsiCo／ASOS／KW 當日案例、100M+／250+／6,000+、Innovation Workspace 六卡、團隊協作的 AI 平台、六張入門資源與深色完整頁尾。

已另送原生 Stitch 並改回來源原始圖與三段公開影片。Framer 同時保留多種響應式 DOM，不能將重複標題當成三套可見內容；桌面部分圖形顯示過渡留白，窄版則可見原圖，需以實際截圖辨認。

首屏新增桌面與窄版真正顯示時的完整 hero 原始 DOM，保留裝飾圖祖先，避免頁尾擷取的退出 transform 讓 Customer Feedback／Flow Process 蓋住標題與表單。桌面六張功能卡依實際 track box 的 2880／3600／4320 捲動位置投影，不再以標題位置推測全部卡片；相位之間的 Framer spring 與收尾切換仍未驗證。

root 已實際查看目前雜湊的桌面／窄版各 11 段及全部 6 張比較圖；桌面 3600／4320 的 Formats／Blueprints／Security／Integrations 另直接比對真正 active 官網圖。首屏大標與 CTA 均完整露出，頁高 7703／8910px 相同，無可見壞圖、溢位或覆蓋缺口；桌面仍保留 7 個幾何診斷差異，不能把主要畫面已比對改稱完全一致。

保留原有 DESIGN.md、PROMPTS.md、STITCH-PROMPT.md；本檔為目前官網的日期限定補充。研究頁免費瀏覽、無付費執行時依賴，未執行購買或訂閱。

驗證範圍為匿名公開首頁、1280×720 與 390×844、DPR 1、桌面 UA。實體手機、其他地區、完整互動與部署尚未驗證；accepted=false，不宣稱與官方一致。

## 已知差異與驗證範圍

- Framer 響應式變體會重複產生 DOM 標題，再以 CSS 控制實際顯示；DOM 標題總數無法證明隱藏、顯示中的桌面圖像，以及畫布、影片階段。
- 啟用中的主視覺祖先樣式與桌面卡片軌道量測補充正式第一輪紀錄。重新穩定的 3600／4320 彈簧動畫階段與正式影像略有差異；插值與最終轉場仍為靜態推算，不代表精確動畫一致。
- 桌面保留 7 個正式標題幾何差異：3 個進場動畫的垂直位移各 40px，以及 4 個離屏第 0 階段 AI 平台標題差異；窄版差異為 0。早期桌面延遲載入空白保留為歷史資料，重新取得的啟用來源支援已還原區段。
- Brie 游標與本機覆蓋層的垂直位置、PepsiCo 案例影片、輪播與商標時間階段不同；選單、產品分頁、表單、註冊後端及實際團隊、代理服務尚未驗證。
- 桌面有 3 個標題因進場動畫相差 40px，以及 4 個離屏第 0 階段 AI 平台標題差異，共 7 個；窄版為 0。幾何診斷不代表像素或動畫一致。
- 桌面最終第 5／6 階段的實際本機影像，已與新取得的官網 3600／4320 啟用影像直接比較，確認格式、藍圖、安全性及整合區。早期正式桌面延遲載入空白保留，另以實際啟用參考補充。
- Brie 游標與本機覆蓋層的垂直位置、PepsiCo 案例影片、輪播及商標動態階段不同；精確彈簧與插值時間尚未驗證。
- 選單、分頁、表單、註冊後端及實際團隊、代理服務尚未驗證。
- 原始比對未涵蓋其他寬度、實體裝置、地區、完整互動及動態，以及正式部署。

以上限制沿用原參考日期的比對紀錄。本次繁體中文整理不會把未驗證的影片、動畫、服務或尺寸改標為已通過；目前預覽仍未宣稱與官方完全一致。
<!-- Original AI instructions: awesome-ai-web-design -->

## 來源與使用範圍

資料來源與適用授權集中於專案根目錄的 ATTRIBUTION.md 與 LICENSE。品牌名稱僅用於識別參考來源，並非官方授權或服務。下方 AI 指令由本專案獨立撰寫；若既有互動備註與無障礙要求衝突，以此處的可用性檢查為準。

## 重新撰寫的 AI 任務指令

語言：繁體中文（台灣用語，zh-TW）。將 DESIGN.md 放入專案，再選擇下方任務。這些指令由本專案重新撰寫；請把示範內容替換為自己的產品需求。

## 建立新頁面

```text
先閱讀隨附的 DESIGN.md，以 Miro 的設計語言作為介面參考。請完成以下可操作頁面：製作工作坊白板總覽，包含範本卡片、參與者狀態與小型畫布預覽。黃色建立工作空間識別，便利貼顏色依意義分組，不隨機分配。

使用我的產品名稱、內容與資料格式，優先沿用專案現有元件及技術。開始製作樣式前，先將色彩、字體、間距與圓角整理為可重複使用的設計變數。指定字型無法取得時，使用可用的系統字型或開源字型，並說明替代方式。介面文案、按鈕、提示、錯誤訊息、圖片替代文字、註解與交付說明，一律使用繁體中文（台灣用語）。使用「專案、元件、資料、建立、預設、載入、登入、連結、儲存、影片」等台灣用語。保留品牌名稱、檔名、網址、API 識別字與可執行程式碼；HTML 語言設為 zh-Hant-TW。

讓互動元件可實際操作，並將狀態提供給輔助科技。具備可見的鍵盤焦點、清楚的欄位標示、減少動態效果，以及至少 44px 的觸控區域。參考視覺與可用性衝突時，作最小幅度的無障礙調整並記錄原因。在 390px、768px、1440px 寬度檢查版面，涵蓋繁體中文長標題、長內容、空白及錯誤狀態。金額、數量與日期依資料本身的幣別、單位及時區呈現，以 zh-TW 格式顯示，不擅自換算。最後交付完成的檔案、實際驗證結果與仍待確認的假設，不把未檢查項目宣稱為通過。
```

## 製作元件

```text
先閱讀隨附的 DESIGN.md，以 Miro 的設計語言作為介面參考。請製作工作坊範本卡片，包含預覽筆記、所需時間與開始操作。沿用現有元件慣例，放入精簡且符合實際情境的範例。比例與資訊層級應來自參考規格，不能只替通用卡片換色。依需求支援預設、焦點、停用、載入與錯誤狀態。使用有意義的示範資料，讓每個可見操作都有明確結果。

使用我的產品名稱、內容與資料格式，優先沿用專案現有元件及技術。開始製作樣式前，先將色彩、字體、間距與圓角整理為可重複使用的設計變數。指定字型無法取得時，使用可用的系統字型或開源字型，並說明替代方式。介面文案、按鈕、提示、錯誤訊息、圖片替代文字、註解與交付說明，一律使用繁體中文（台灣用語）。使用「專案、元件、資料、建立、預設、載入、登入、連結、儲存、影片」等台灣用語。保留品牌名稱、檔名、網址、API 識別字與可執行程式碼；HTML 語言設為 zh-Hant-TW。

讓互動元件可實際操作，並將狀態提供給輔助科技。具備可見的鍵盤焦點、清楚的欄位標示、減少動態效果，以及至少 44px 的觸控區域。參考視覺與可用性衝突時，作最小幅度的無障礙調整並記錄原因。在 390px、768px、1440px 寬度檢查版面，涵蓋繁體中文長標題、長內容、空白及錯誤狀態。金額、數量與日期依資料本身的幣別、單位及時區呈現，以 zh-TW 格式顯示，不擅自換算。最後交付完成的檔案、實際驗證結果與仍待確認的假設，不把未檢查項目宣稱為通過。
```

## 改造既有介面

```text
先閱讀隨附的 DESIGN.md，以 Miro 的設計語言作為介面參考。重新設計選定頁面，同時保留路由、資料、行為與使用者可理解的意義。先確認頁面層級，再找出最少且可重複使用的設計變數與元件調整。以下構圖作為視覺方向，依現有頁面調整：製作工作坊白板總覽，包含範本卡片、參與者狀態與小型畫布預覽。黃色建立工作空間識別，便利貼顏色依意義分組，不隨機分配。

使用我的產品名稱、內容與資料格式，優先沿用專案現有元件及技術。開始製作樣式前，先將色彩、字體、間距與圓角整理為可重複使用的設計變數。指定字型無法取得時，使用可用的系統字型或開源字型，並說明替代方式。介面文案、按鈕、提示、錯誤訊息、圖片替代文字、註解與交付說明，一律使用繁體中文（台灣用語）。使用「專案、元件、資料、建立、預設、載入、登入、連結、儲存、影片」等台灣用語。保留品牌名稱、檔名、網址、API 識別字與可執行程式碼；HTML 語言設為 zh-Hant-TW。依完整元件群組套用變更，檢查其他頁面是否受影響，並說明調整前後的主要差異。

讓互動元件可實際操作，並將狀態提供給輔助科技。具備可見的鍵盤焦點、清楚的欄位標示、減少動態效果，以及至少 44px 的觸控區域。參考視覺與可用性衝突時，作最小幅度的無障礙調整並記錄原因。在 390px、768px、1440px 寬度檢查版面，涵蓋繁體中文長標題、長內容、空白及錯誤狀態。金額、數量與日期依資料本身的幣別、單位及時區呈現，以 zh-TW 格式顯示，不擅自換算。最後交付完成的檔案、實際驗證結果與仍待確認的假設，不把未檢查項目宣稱為通過。
```

## 逐次調整流程

1. 先指出一個可實際觀察的問題，例如層級不清或內容遭裁切。
2. 在 DESIGN.md 找到對應設計變數或元件規則，提出範圍明確的調整。
3. 套用調整，保留無關的路由與資料行為。
4. 檢查鍵盤焦點、窄版排版，以及代表性的內容與錯誤狀態。
5. 用繁體中文說明結果，以及刻意偏離參考外觀的原因。
