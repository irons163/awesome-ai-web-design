# Shopify：目前公開首頁設計分析

官方來源：https://www.shopify.com/ca，觀察日期2026-10-10。

保留深色首頁、72px 半透明導覽、96px 桌面／48px 窄版主標、四類商家真實照片、Agentic Storefronts、目前 Show up everywhere 三張插畫、跨境地圖、三組創業者照片、紫色 Sidekick、App 拼貼、開發者圖層、綠色 Checkout、地球截圖替代、Capital 引言、三步驟照片與完整頁尾。

Shopify 最終桌面高度10958px、390px窄版11531px，均與目前官方捕捉狀態相同。最新官方產品段是 Show up everywhere. Without going anywhere.；已移除舊文案與 Courses 頁尾。商家類別、窄版選單與產品次選單、返回、Escape、創業者頁點已操作檢查。

完整官方頁面先以分段DOM保存，原生Google Stitch重新生成的結果與供應商說法保留。接著以今天官方的完整渲染DOM/CSS、字型與公開照片修正具體頁面；舊草稿及原生生成未被覆寫。

實際於1440×1000及390×844 CSS像素、DPR1、相同桌面UA逐段捲動、截圖與比較；390px是響應式窄版證據，並非真實手機硬體測試。兩尺寸均無水平溢位，已觀察的本地圖片皆載入，字型完成載入。已逐段檢視全部比較圖；影片時間、轉場及部分互動不同，不能推論全面官方一致。

## 仍有差異

- The official streamed hero and rotating headline are represented by the actual official poster and a captured headline phase (store they line up for); streamed animation and the changing headline are not reproduced.
- The live WebGL globe uses dated official screenshot crops with provenance and soft edge masking. Rotation, surrounding starfield and changing animated commerce factoids are not recreated.
- Merchant categories and country/product illustrations retain captured initial phases; manual category selection and entrepreneur dots operate, but official automatic cycling, swipe/drag and timing are not fully reproduced.
- Desktop menu wrappers explicitly hide when closed and menu-only GPU transitions are disabled to avoid a reproducible retained paint artifact. Endpoint layout is scoped evidence; transition timing and every hover/focus state remain unverified.
- Why we build Shopify and testimonial modal video flows, country picker parity, cookie vendor and account/checkout/store services are outside verified scope. Privacy opens an educational local dialog.
- Public video media remain external URLs and show different frames in comparisons. Real mobile hardware, other widths and final published deployment have not been verified.

驗收維持accepted=false。沒有採購、付費升級或部署；後續整合與正式網站驗證由主代理執行。
