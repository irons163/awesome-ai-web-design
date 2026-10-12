# Mintlify｜2026-10-11 公開官網設計分析

來源：https://www.mintlify.com/。原始取樣時間保留於 UTC 紀錄，oct10 工作檔名不表示所有檢查都在 10 月 10 日完成。

現行首頁改為「The intelligent documentation platform」，使用近黑背景、薄荷綠流線、Arizona Flare 襯線標題與小型白色按鈕。左側主文、Agent traffic 標籤、文件介面圖與右下 Ask assistant 為目前來源；舊的 knowledge infrastructure 主標不可沿用。

完整順序為 20,000+ 公司、六張 knowledge stack／24×7 agents 功能卡、Anthropic／Coinbase／HubSpot／AT&T 企業案例、300M+／2B+／99.99% 當日數字、Lovable／Kalshi／Decagon／Replit、新創與見證、三張最新文章、襯線收尾 CTA 及頁尾。窄版保留側邊露出的輪播卡。

本次重新送交原生 Stitch；提供者草稿加入的辦公室照片與通用示範，不能當官網資產。來源校正改回原始文件／品牌圖與字型。流線與多個卡片實際是 canvas，僅複製 DOM 會丟失可見像素，需有原始像素或明確限定的靜態相位證據。

每個尺寸保留 13 個初始可見 canvas 的實際像素作為靜態影格；水平隱藏的顧客卡 10／11 未曾露出，不能宣稱全部 15 個位置完成。Latest updates 三張則是原始 WebP 圖，不是 canvas；初次瀏覽器已有解碼尺寸但仍未繪出的黑畫面另存診斷，未改 HTML，暖機後重新拍攝才確認圖片正常。

root 已實際查看目前雜湊的桌面 12 段、390px 窄版 15 段及全部 7 張新比較圖。頁高 8457／12555px 與來源相同，兩尺寸各 24 個標題幾何無量測差、無可見壞圖或水平溢位；此為暖機後主要靜態畫面的限定比對。

保留原有 DESIGN.md、PROMPTS.md、STITCH-PROMPT.md；本檔為目前官網的日期限定補充。研究頁免費瀏覽、無付費執行時依賴，未執行購買或訂閱。

驗證範圍為匿名公開首頁、1280×720 與 390×844、DPR 1、桌面 UA。實體手機、其他地區、完整互動與部署尚未驗證；accepted=false，不宣稱與官方一致。
