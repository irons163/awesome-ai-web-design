# Miro｜2026-10-11 公開官網設計分析

來源：https://miro.com/。原始取樣時間保留於 UTC 紀錄，oct10 工作檔名不表示所有檢查都在 10 月 10 日完成。

現行首頁使用灰白留白、黃色 Miro 標誌、淡藍 CTA、細框圓角圖卡。「Human collaboration at the speed of AI」置中，搭配 email／Get Started Free、真正的研究／流程／圖表截圖與品牌列。

下方是 Research／Roadmap & Planning／Diagrams／Workshops、Flow from idea to outcome、PepsiCo／ASOS／KW 當日案例、100M+／250+／6,000+、Innovation Workspace 六卡、AI platform for teamwork、六張入門資源與深色完整頁尾。

已另送原生 Stitch 並改回來源原始圖與三段公開影片。Framer 同時保留多種響應式 DOM，不能將重複標題當成三套可見內容；桌面部分圖形顯示過渡留白，窄版則可見原圖，需以實際截圖辨認。

首屏新增桌面與窄版真正顯示時的完整 hero 原始 DOM，保留裝飾圖祖先，避免頁尾擷取的退出 transform 讓 Customer Feedback／Flow Process 蓋住標題與表單。桌面六張功能卡依實際 track box 的 2880／3600／4320 捲動位置投影，不再以標題位置推測全部卡片；相位之間的 Framer spring 與收尾切換仍未驗證。

root 已實際查看目前雜湊的桌面／窄版各 11 段及全部 6 張比較圖；桌面 3600／4320 的 Formats／Blueprints／Security／Integrations 另直接比對真正 active 官網圖。首屏大標與 CTA 均完整露出，頁高 7703／8910px 相同，無可見壞圖、溢位或覆蓋缺口；桌面仍保留 7 個幾何診斷差異，不能把主要畫面已比對改稱完全一致。

保留原有 DESIGN.md、PROMPTS.md、STITCH-PROMPT.md；本檔為目前官網的日期限定補充。研究頁免費瀏覽、無付費執行時依賴，未執行購買或訂閱。

驗證範圍為匿名公開首頁、1280×720 與 390×844、DPR 1、桌面 UA。實體手機、其他地區、完整互動與部署尚未驗證；accepted=false，不宣稱與官方一致。
