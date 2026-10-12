# Kraken｜2026-10-10 公開官網設計分析

取樣來源：https://www.kraken.com/ca。Canada English explicitly selected through public country/language UI; /ca origin.

本次取樣為加拿大英文 /ca、拒絕非必要 Cookie 並關閉地區提示。淡紫首屏為「Own the power of your money」，下方為 Pro、Kraken、Wallet、Krak 深色產品卡。

後續有代理程式工具、20x 槓桿、日期限定行情表、開戶 CTA、法律說明與現行 Payward 頁尾。390px 取樣為窄版桌面 UA，不是實體手機。

實際截圖查出多個卡片只剩背景：原頁把文字與圖片包在初始 --opacity-start:0 的捲動顯示層。已保留原資產與文字，固定為所記錄的最終 opacity／transform；新版桌面與窄版全頁已實際確認產品文字及圖片恢復。

原有 DESIGN.md、PROMPTS.md 與 STITCH-PROMPT.md 保留；本檔為日期限定補充。研究頁免費瀏覽，未開啟付費方案或交易；不對外部生成服務的帳戶計費狀態作保證。

驗證範圍為匿名公開首頁、1280×720 與390×844、DPR1、桌面 UA。未完成實體手機、其他地區、完整互動或服務驗證；目前 accepted=false，不宣稱與官方一致。
