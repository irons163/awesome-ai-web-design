# PostHog｜2026-10-11 公開官網設計分析

來源：https://posthog.com/。原始取樣時間保留於 UTC 紀錄，oct10 工作檔名不表示所有檢查都在 10 月 10 日完成。

現行 PostHog 為綠色草地插畫桌面、周圍 app 圖示、頂部功能列與淡綠應用程式視窗。RoundHog 黑字、橘黃按鈕及紫色頁籤構成「Your product’s context layer」首頁；不能換成通用紫色 SaaS 模板。

視窗內依序有免費 setup 卡、Ask PostHog anything／Give agents product context／Ship with PostHog、Social proof、彩色客戶 logo、All your data、Usage-based pricing 表、Why PostHog、Bedtime reading、Shameless CTA，以及復古軟體盒 PostHog Web 廣告。setup 的 97% 與定價文內的 98% 原文矛盾分別保留。

主要內容在 .app-scroll-viewport 內捲動；桌面內容 extent 4679／可見 629，窄版 extent 7725／可見 787，不能以 bodyHeight 720／844 判定全頁。早期 JPEG 窄版實際只有 390×219，已排除作完整證據；重新以明確 clip 取得 390×844 原始 PNG 後才可檢查。

保留原有 DESIGN.md、PROMPTS.md、STITCH-PROMPT.md；本檔為目前官網的日期限定補充。研究頁免費瀏覽、無付費執行時依賴，未執行購買或訂閱。

驗證範圍為匿名公開首頁、1280×720 與 390×844、DPR 1、桌面 UA。實體手機、其他地區、完整互動與部署尚未驗證；accepted=false，不宣稱與官方一致。
