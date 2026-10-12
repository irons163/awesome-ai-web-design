# Webflow 目前公開首頁設計分析

來源 https://webflow.com/，實際觀察與最後校正2026-10-11。黑底、WF Visual Sans Variable 字型與藍色品牌CTA，46px Conf26公告列加68px黏性導覽。主標 Build for what’s next，桌面字級74.8571px、行高77.8514px；窄版置中兩行。依序保留行銷成果拼貼、真實客戶商標、Introducing Source視覺、四項能力、300,000+品牌六張客戶卡、目前新的 Turn your website into a growth engine 六欄表單、Dyson編輯器原圖、Recent updates三張、#MadeinWebflow作品及完整目錄頁尾。成果數字只記錄官方當日公開呈現，未作金融或成效背書。

原保存版本銷售區文案不同，因此使用 genuine Google Stitch MCP 產生新的桌面校正稿，完整回應、原始HTML、原始縮圖及全尺寸PNG均分開保留。供應者自行更改部分數據意思，沒有當作已驗證來源。具體頁面以完整當日官方DOM/CSS及226份公開原素材校正。WebGL空白在實際比較中被找出，已用官方原始作品圖與觀察到的角度/位置恢復為靜態CSS展示；不是以整頁截圖冒充頁面。

1280×720桌面10段及390×844窄版12段，來源與最後校正版均實際逐視窗完整拍攝，PIL實際尺寸與上下覆蓋檢查完成。全部4張桌面及5張窄版比較圖目視檢查。頁高7188/9466完全相合，主標與頁尾位置相合；兩尺寸194張DOM圖片載入、字型完成、無水平溢位。來源20個WebGL-held空src節點由GPU渲染，校正版從記錄的公開held URL恢復圖片；Bing追蹤像素移除。

- The official hero marquee moves continuously. The source-corrected page preserves the captured position, so visible left/right tile positions differ across real screenshot times.
- The WebGL #MadeinWebflow gallery is recreated from its exact recorded public held images and observed DOM transforms as a static CSS fallback. Desktop angles/layout match the recorded visible phase; narrow horizontal position differs as the official gallery moves during scrolling. GPU motion, hover dimming, opening cards and project dialogs are not reproduced or accepted.
- Menus, persona selector, customer carousel controls, video playback/dialogs, cookie UI, full keyboard/focus behavior and other interactive states were not accepted in this main-page visual review. The source capture was made after Reject all cookies; no external forms were submitted.
- The sales form is read-only in the study. Account, contact sales, signup, other routes, real phone hardware, other widths and published deployment are outside this review.
- Fresh native Stitch correction is DESKTOP only. Provider altered some metrics/headings and logo descriptions; source-corrected final page uses actual recorded source content. No new native MOBILE correction is claimed.

accepted=false，未宣稱全面官方一致。沒有購買、付費升級或部署；帳戶計費未稽核。
