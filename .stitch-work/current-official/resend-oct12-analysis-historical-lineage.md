# Resend 目前公開首頁設計分析

官方來源：https://resend.com/，來源觀察2026-10-10；最後校正畫面2026-10-11（台灣時間）。黑色背景搭配 Domaine 襯線主標與 Favorit 內文，保留 Email for developers、Forward 活動提示、十二個實際客戶商標、十三種語言及九個 Node 框架導覽。開發者體驗、公開編輯器初始白色區域、Contact management、Broadcast analytics、React 程式碼與 ACME 預覽、九張送達功能卡、實際客戶證言、控制台示例與完整頁尾均取自完整官方渲染 DOM/CSS。

與先前保存官方設計相比，主要內容及結構相同，因此重用9月27日 genuine Google Stitch MCP 原生生成；今天的 get_screen 完整回應另存。原候選含有重新詮釋及技術/客戶聲明風險，沒有直接視為通過。原始 HTML、PNG、生成 metadata、分析及 DESIGN.md/design-md 保留。校正版使用63份已觀察的公開原素材，包括五段影片、海報、商標、字型與實際分析圖。

實際1280×720桌面與390×844窄版各17段捲動截圖。PIL確認每段真實像素尺寸及從頂到頁尾無缺口；頁高各12154與14143px，與官方相同。73張本機DOM圖片皆載入，字型載入完成，無水平溢位。逐段檢視七張桌面、八張窄版2000px比較圖。主內容、字體、卡片、程式碼及頁尾位置相合，動態及互動差異如下。

## 尚存差異

- The official desktop capture had the Floor background and Light ray image requests not ready, and its WebGL cube canvas was empty. The preserved public background originals load locally. Desktop WebGL fidelity was not verified.
- The narrow header uses a documented raster-stability CSS correction: its child is raised above the captured backdrop and the before blur layer is removed. The source sequential screenshots show a120px blurred band while the corrected header remains readable. This is an explicit visual difference.
- The narrow cube and four product videos, testimonial marquee offsets, status pulse and dynamic demo IDs/timestamps are frozen or show different frames. React code-pane internal scroll differs in one desktop comparison. Animation/frame/state parity is not claimed.
- Navigation dropdown/hamburger, SDK/framework switching, copy controls, Test-mode and editor demos, React file/view/theme tabs, tooltips and dashboard tabs remain captured initial states. Their complete behavior and keyboard focus were not accepted.
- Authentication, email sending, newsletter/account services, real phone hardware, other viewport widths and final published deployment are outside this review. Inputs are read-only and public service links lead to official pages.

accepted=false；沒有宣稱全面官方一致。沒有購買、付費升級或部署；帳戶計費未稽核。

## 2026-10-12 驗證版本綁定校正

10月10日完整桌面/窄版畫面比較保留為歷史證據；D僅第6–16張原始記錄含目前SHA，前6張與N17張缺capture-time SHA。事後manifest相合不等於當時整頁逐張版本綁定，尚未補完整目前SHA重拍。

Historical desktop/narrow observations and comparisons remain valid dated observations. Only desktop phase indices6–16 originally contain capture-time SHA; desktop0–5 and all narrow phases do not. The later manifest/current file match is posthoc lineage and is not retroactive full-page SHA binding.

完整歷史phase JSON未改寫，也沒有補造capture-time SHA。`currentFullPageCaptureComplete=false`、`currentFullPageComparisonComplete=false`；歷史完整觀察與精確未變範圍/局部補驗分開記錄，accepted=false。
