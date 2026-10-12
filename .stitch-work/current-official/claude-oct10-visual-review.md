# Claude｜實際畫面校正與驗證

**已比對主要靜態畫面，仍有差異；accepted=false，不宣稱與官方一致。**

官方來源：https://claude.com/index.html。重製檔 SHA-256：`d98af541665c9625abdfdefe55473188bd520e2143a090b2a937d314eaec0b59`。

主代理已實際檢視全部 5 張桌面／窄版對照圖，以及本次原生 Stitch 圖。真實 PNG/JPEG 尺寸已檢查，完整取樣對應目前檔案；相同頁高與幾何量測不代表完全一致。窄版為桌面 UA 的 390px 響應式測試。

| 實際取樣 | 頁高 | 分段數 | 全頁覆蓋 |
|---|---:|---:|---|
| official_desktop | 4013 | 6 | 是 |
| official_narrow | 6946 | 9 | 是 |
| local_desktop | 4013 | 6 | 是 |
| local_narrow | 6946 | 9 | 是 |

Stitch真正回傳MOBILE780×12362，原生稿虛構Cowork介面、方案排列與簡化頁尾，與校正版獨立保存。原生PNG不是瀏覽器驗證。

官方來源影片src及currentSrc空、readyState0，原生畫面確實呈灰色槽；本機保留同樣空槽，沒有猜測影片URL或假稱播放器可用。

FAQ、Explore plans等官方取樣標題處於暗色進場影格，本機完整顯示，仍有可見明暗／揭露差異。成效卡、滑入、輪播、游標及陰影影格沒有同步。兩版標題幾何相同不代表官方一致。

D6／N9目前原生畫面完整覆蓋、無可見缺圖或橫向溢出，實際載入HTML與磁碟逐位元組相同。根選單、桌面下拉、FAQ展開、方案切換、語言、Ask Claude與所有Google／email登入／註冊結果未驗證；沒有提交任何服務操作。

390px是桌面UA響應式測試，非實機。原分析與原指令保留，研究頁免費瀏覽、未啟用付費方案或交易；不推定供應商使用量帳單。accepted=false、official_consistency_claim=false，待全74頁整合後更新既有站。
