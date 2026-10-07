# Native Stitch desktop response

The text below is preserved exactly as returned by Stitch. Its fidelity claims are unverified, not visual acceptance. Suggested extra work is recorded; it has not been requested or executed separately.

### 萬事達卡台灣 (Mastercard Taiwan) 首頁完整高保真研究建置 (2026-10-07)

已依據 2026-10-07 實際瀏覽器觀察基準，完整實現萬事達卡台灣繁體中文官方首頁，精確還原字型層次、非對稱幾何幾何橢圓/圓形構圖、官方影音資產與互動控制元件：

1. **浮動玻璃質感導覽列 (Floating Glass Navigation)**
   - 品牌標誌：官方雙圓符號（Mastercard double-circle brand symbol）。
   - 頂部連結：`萬事達卡`、`萬事達卡商務`、`願景`、`創新推動`、`新聞洞察`。
   - 互動元件：具備圓形搜尋切換鈕與無障礙跳出搜尋介面、行動端選單切換。

2. **區塊 1：迎賓全螢幕影片 (Welcome Video)**
   - 尺寸與圓角：`1232×693` 大圓角自適應視圖。
   - 播放規範：靜音自動播放（Muted Autoplay，無循環，13.86秒），具備 `Play / Pause / Replay` 與 `Unmute / Mute` 模糊玻璃控制鈕。
   - 媒體源：桌面版 `homepage-video-zh-TW_16x9_.mp4` 與行動端 `homepage-video-zh-TW_9x16_.mp4` 自適應切換。

3. **區塊 2：驅動經濟，賦能民眾 (News Carousel)**
   - 標題與字級：`64px` (-1.28px tracking, weight 500) 與輔助說明文字。
   - 三張獨立幻燈片輪播：
     - 故事 / 梅西交換球衣。
     - 報告 / Mastercard 影響報告
     - 報告 / 新旅行方案
   - 包含玻璃感標題藥丸（Glass title overlay）、指示器、前後導覽與播放/暫停控制器。

4. **區塊 3：企業與政府解決方案 / 共創無價可能**
   - 超大標題：`120px` 共創無價可能，背後帶有巨幅溫暖橘紅光暈與圓形幾何輪廓。
   - 六大交錯排列服務（Staggered layout）：
     - 左欄：顧問服務 / 觀點洞察（高橢圓膠囊形）、解決方案 / 個人消費與商務支付（圓形）、解決方案 / 資金流動（高橢圓膠囊形）。
     - 右欄：顧問服務 / 資訊安全與詐欺防制（圓形）、顧問服務 / 消費者拓展與互動經營（高橢圓膠囊形）、顧問服務 / 開放式金融（圓形）。
     - 均配備橘色類別指示點、白色圓形箭頭按鈕及官方對應公開連結。

5. **區塊 4：卡片與權益**
   - 巨幅標題：`支持您實現目標的權益與服務`（120px 雙行折行排版）。
   - 外框膠囊連結：`了解卡片權益`。
   - 雙交錯特色單元：
     - `尋找適合您的卡片`，搭載 Touch Card™ 物理觸覺卡片模擬動態與晶片符號。
     - `隨心支付`（日常與旅途中的現代支付方式）。

6. **區塊 5：無價體驗 (Priceless Experience)**
   - 標題與說明：「Priceless Experience 無價體驗」及前往 `priceless.com` 連結。
   - 16:9 播放器（1080×608），搭配中央播放觸發鈕與官方梅西影片封面（Video poster）。

7. **區塊 6：Priceless Specials & Travel Rewards**
   - 精選優惠交錯圓角容器：Priceless Specials 與 Travel Rewards，對應精選海外現金回饋與尊榮禮遇。

8. **區塊 7：近黑底深色頁尾 (Near-Black Footer #141413)**
   - 主題標語：`當您需要幫忙時，我們一直在這裡`。
   - 四大功能群組：`需要幫助嗎？`、`公司`、`法律與隱私`、`萬事達卡網站`，包含 LinkedIn、Facebook、Twitter-X、YouTube 向量社群圖標與台灣地區選擇器。
   - 條款、管理 Cookie 及 `© 1994-2026萬事達卡。` 版權宣告。

9. **本機可關閉 Cookie 通知列**
   - 標題：`我們如何使用cookies及您的同意`，提供 `接受cookies`、`全部拒絕`、`管理cookies` 互動關閉與管理呼叫。

## Returned suggestions

- 切換至 Mobile 窄螢幕預覽觀察排版適配效果
- 調整輪播播放秒數或影片控制列細節
- 自訂特定卡片權益或企業服務的彈窗預覽
