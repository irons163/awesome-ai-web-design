# Wise 目前公開首頁設計分析

來源 https://wise.com/，觀察與最後校正2026-10-11。網址目前實際提供 Taiwan 英文版：台灣旗EN、Personal/Platform導覽、全萊姆綠首屏、極粗緊字距大寫 THE INTERNATIONAL ACCOUNT THAT SAVES YOU MONEY，兩顆膠囊CTA。桌面三張大型圓角卡為 Get paid in22currencies、Low-cost international transfers、Send more,pay even less；窄版先排列轉帳卡再兩張。當日USD/EUR匯率與費用完整保留為唯讀畫面範例，沒有沿用舊加拿大促銷、CAD利息或服務宣稱。

白底依序是匯率透明堆疊卡、全球用戶指標、Everyday照片、兩張生活攝影、銀行平台、三項安全視覺、Trustpilot客戶引言、綠色地球使命區、動態彩色app下載區、公開速度/支援附註、國家覆蓋與完整法律頁尾。延續 Wise 原始字型、照片、圖示、國旗、插畫、影片及密集的留白節奏。

新版地區與內容不同，因此透過 genuine Google Stitch MCP 新增桌面校正屏幕，完整回應及原始輸出獨立保存；原加拿大設計、DESIGN.md與design-md不變。以完整官方DOM/CSS和202份公開原素材校正具體頁面。實際比較找出並修正首屏導覽隱藏、平台卡淡入後消失、窄版地球圖失去picture來源尺寸遮住標題三項問題；現在窄版地球為官方觀察到的200×150。移除兩個cookie設定追蹤節點及所有追蹤iframe，原始失敗紀錄保留，沒有重試繞過。頁尾12px空白用無追蹤空間保留。

來源與最後成品均完整拍攝1280×720桌面21段、390×844窄版18段；全部8張桌面與8張窄版比較圖目視檢查，PIL真實影像尺寸與捲動無缺段覆蓋確認。最終頁高14703/14690與來源相合，144張DOM圖片均載入、字型完成、無水平溢位。早期總高度估計會因content-visibility離屏排版而變化；證據以實際逐段畫面和最終幾何為準。Everyday照片動畫遮罩仍有白色缺口，因此沒有接受官方一致。

- The Everyday Everywhere scroll/zoom photograph retains source CSS animation and captured motion state, without the full official scroll controller. Its crop/scale, large white text and reveal mask differ; the narrow final comparison contains a white reveal gap through part of that photo. Exact motion and this reveal state remain unresolved, not accepted as official parity.
- The account illustration cycles currencies; source narrow screenshot catches transitional EUR/GBP overlap while the local screenshot shows a settled GBP frame. The built-in-security video frame and play/pause icon also differ; local playback state controls are not fully reproduced.
- The abstract app-download background and moving flag strip appear at different animation phases. The platform card is held in its revealed state; its entry animation is not reproduced. Header hides after64px locally; exact official threshold/up-scroll behavior was not accepted.
- Currency selection, rate/fee calculation, discount modal, country-category radio switching, reviews carousel, desktop/mobile menus, full keyboard/focus parity and service flows were not accepted. The144 loaded image count excludes two cookie-setter tracking nodes; the12px blank footer baseline space left by three zero-size tracking iframes is reproduced without iframes.
- Only the current Taiwan-region English variant actually served at https://wise.com/ was reviewed. Previous Canada sources/native remain preserved. Dated financial/rating/support examples are visual content, not live quotes or financial guidance; no signup, transfers, payments or external form submissions were performed.
- Fresh genuine Stitch correction is DESKTOP only; no new native MOBILE correction. Other regions/routes/widths, real phone hardware and published deployment are outside this review.

accepted=false。沒有購買、付費升級或部署；帳戶計費未稽核。
