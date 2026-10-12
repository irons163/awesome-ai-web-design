# Runway 目前公開首頁設計分析

入口 https://runwayml.com/ 目前轉到 https://runway.com/，觀察2026-10-11。當日新增藍色企業促銷公告，桌面高48px、窄版60.5px；白色64px固定導覽，下接黑底原始影片主視覺。abcNormal 主標 Building Real-World Intelligence 的實測位置，桌面為x58.75/y347.53/520.49×43.89、38.17px字型；窄版為x50.59/y280.11/288.83×64.39、28px字型。

完整順序保留合作品牌SVG列、三平台Creative/Dev/Robotics介紹、平台選擇與Creative使用方式頁籤、模糊流動Research影像與三個研究連結、Runway Ads/Praxis-1/OpenAI Marketplace/Claude Motion四則當日新聞，以及完整黑色多欄頁尾。品牌或產品宣傳文字僅代表當日官方頁面，不代表另行產品查核。

官方平台面板會自動輪播，造成頁高變動。本次透過可見按鈕明確選定 Runway Creative / How Runway is Used，再以每段狀態檢查完整拍攝：來源與成品桌面各7段、窄版各12段，頁高5015/9377px。每張實際影像尺寸、連續捲動覆蓋、前後捲動與頁高一致、成品hash皆驗證；全部3張桌面與5張窄版比較圖逐段目視檢查。16張DOM圖片與字型載入完成、無水平溢位，主標位置和尺寸完全相合。

genuine Google Stitch MCP 新增桌面屏幕，完整指令、回應、原始HTML、未改縮圖和fullPNG分開保留；具體重製再使用完整當日官方DOM/CSS及44份公開原始素材校正。已修正公告被固定導覽遮蓋與Dev區塊原始背景圖漏載；Mux播放器使用原始srcset海報，不以生成圖片替代。舊版與不穩定輪播證據均另外保留，不混作本次完整驗證。

- Official homepage auto-cycles between Creative, Dev and Robotics panels, changing body height. This review explicitly selected Runway Creative / How Runway is Used. Dev/Robotics and other Creative tabs are not accepted; the static preview retains the selected captured state.
- Mux shadow-root video/HLS playback is replaced with the exact observed public srcset poster. Hero, Creative, Robotics and the Creative use-case panel show different motion phases or static posters; Research video frame timing also differs. No frame-by-frame or playback parity is claimed.
- The official narrow top screenshot catches navigation over the blue promotion banner during its transition; the corrected header sits below the visible banner, then sticks at top after scroll. Partner-logo positions and their occlusion by sticky navigation differ in sequential phases. These states are not accepted as exact official parity.
- Navigation menus/mobile drawer, platform/tab switching, cookie/privacy and language controls, full keyboard/focus behavior and account/API/contact service flows are not implemented or accepted by this static source correction. Observed links lead to official destinations; no account or form submission occurred.
- Fresh genuine Stitch edit is DESKTOP only. Prior original desktop/mobile/DESIGN.md/design-md remain preserved. Other widths, real phone hardware, other routes/locales and published deployment are not reviewed.

accepted=false；未付費、未部署、未提交帳戶/表單，帳戶計費未稽核。
