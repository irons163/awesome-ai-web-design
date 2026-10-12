# Intercom｜2026-10-10 畫面校正紀錄

來源：https://www.intercom.com/。目前重製檔 SHA-256：`aa17a623b32dc9b3cabf91ca0ea9990cc8b34ab6272f4b183e8b10b9872f6548`。

**accepted=false；尚不宣稱與官方一致。** 已透過原生 Google Stitch MCP 編輯並保留完整輸出，再依當日來源具體校正。

| 實際取樣 | 頁高 | 全頁覆蓋 | 對應目前重製檔 |
|---|---:|---|---|
| official_desktop | 9494 | 是 | 官方取樣 |
| official_narrow | 10421 | 是 | 官方取樣 |
| local_desktop | 9492 | 是 | 是 |
| local_narrow | 10419 | 是 | 是 |

Latest full desktop height9492 matches source; narrow10419 vs10421. These measurements do not establish visual consistency: the first desktop Fin panel under “Train and test Fin to handle complex queries” is visibly blank, and captured source HTML contains an empty lazy-media container.

Fresh root IAB active-source inspection also showed an empty Fin pane, zero canvas/video nodes, and preserved actual screenshot/fragment. Complete React payload identifies the two original Rive assets, now saved with URL/byte/hash provenance. Earlier Chrome source raster showed a visible phase; a working original Rive render or directly captured visible phase remains unverified. No substitute was invented.

The source notification/chat iframe overlay is excluded. Inactive tab images and complete=false SVG candidates are not automatically classified as visible broken images; product tabs, accordions, navigation and service states remain unverified.

全頁概覽由已保存的實際瀏覽器分段截圖拼接，只用於比較；部分為較早修訂並有明確標籤。圖片候選數僅為矩形與載入狀態檢查，包含隱藏輪播層，不能當作可見破圖數。導覽連結已保留公開目的地，未提交帳戶、預約、電子報、付款或交易。

本子代理的瀏覽器連線政策載入器失敗；主代理已用可用的 IAB 補拍，是否對應目前檔案以表中雜湊綁定為準。未繞過來源安全限制。
