# VoltAgent｜2026-10-11 公開官網設計分析

來源：https://voltagent.dev/。原始取樣時間保留於 UTC 紀錄，oct10 工作檔名不表示所有檢查都在 10 月 10 日完成。

現行首頁以近黑點陣網格、薄荷綠、細邊程式碼／產品卡構成，頁首有開源公告。10 月 11 日新參照的桌面導覽包含 GitHub 10.8K、Discord 圖示與 Try VoltOps，已保留其完整原始 SVG／導覽內容，首屏及捲動導覽皆完成實際複查；數字僅代表取樣當時。首屏為 The end-to-end／AI Agent Engineering Platform、企業多代理說明、Get Started、npm 指令與右側原始連線圖。初次桌面文字留白，已另以真正顯示的官網桌面相位校正，不將舊留白當成完整首屏。

完整順序為 Core Framework／VoltOps Console、程式碼與 console、公司列、Tool calling／Unified API／Dynamic Prompting／Persistent Memory 四卡、見證、Supervisor agent orchestration、Chain API 工作流、RAG／context 四卡、40+ apps、贊助者、社群三卡及完整頁尾。

已新送原生 Stitch 並以真實來源素材校正。見證在離開區域後會從 DOM 卸載，另保留桌面／窄版可見時的完整 wrapper、62 張圖片元素與真實引言，並追加 9 個原始公開圖檔。Seth Rose 頭像在官網實際也 broken／404，保留原 URL，不製作虛構頭像。

主代理已逐段檢查目前雜湊的桌面 14 段與窄版 14 段，並實際查看全部 8 張對照圖與桌面頁首；9755／11459px 範圍完整、沒有橫向溢位。Seth 頭像在來源與本機各有兩個取樣相位仍破圖，不能寫成零破圖。桌面首屏五個後段標題下移 25.890625px，與來源見證延遲掛載有關；已掛載的 26 個見證 h3 也造成初始 DOM 標題數不同。

保留原有 DESIGN.md、PROMPTS.md、STITCH-PROMPT.md；本檔為目前官網的日期限定補充。研究頁免費瀏覽、無付費執行時依賴，未執行購買或訂閱。

驗證範圍為匿名公開首頁、1280×720 與 390×844、DPR 1、桌面 UA。實體手機、其他地區、完整互動與部署尚未驗證；accepted=false，不宣稱與官方一致。
