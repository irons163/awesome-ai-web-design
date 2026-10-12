# 2026-10-12 目前稿完整補驗 — supabase

目前稿 SHA256：`d5d7298263dc3d75d8ef17224fc43a62efc9cdc92302a712afce3b6786047a15`；本次未修改HTML、原生Stitch輸出、原始設計匯出或公開素材。

桌面1280×720共11張、窄版390×844共12張，從頂到頁尾完整實際視窗無缺口；每張當時記錄目前稿SHA、截圖SHA與截圖後URL/捲動守衛，PIL逐檔確認原生尺寸。兩次重新載入的document response bytes均與磁碟稿完全相等。全部23張完整視窗、9張對照圖與2張最新官方頂部對照已逐張檢視。所有DOM圖片載入、字型loaded，無頁面水平溢位。桌面檢視contact sheet使用半尺寸顯示，窄版原尺寸；原始JPEG完全未縮放或裁切。

`currentFullPageCaptureComplete=true`、`currentFullPageComparisonComplete=true`只表示目前SHA已整頁實看並與**原日期官方完整畫面**比較。`freshOfficialFullPageComparisonComplete=false`：最新官方另存完整DOM與一張頂部實拍，不冒充最新完整逐段來源。先前歷史phase及缺capture-time SHA的紀錄完全未改寫。

All11 complete current viewport frames and4 dated-source comparison segments viewed. Product grid, twelve-logo band, dashboard, React panel, six templates, five customer cards, community,111.2K graphic, CTA, security marks and full footer visible. Dashboard video shows an empty-table frame while source shows populated rows; community carousel positions differ. Repeated sticky headers in the derived sequence composite are capture overlaps, not duplicate page nodes.

All12 complete current viewport frames and5 dated-source comparison segments viewed. Stacked product cards, logos, dashboard, React code, all templates, Lovable open customer card, community, GitHub graphic, security and two-column full footer visible. Local community avatars load where dated source requests were pending. No broken image or horizontal page overflow observed.

Fresh official desktop/narrow top text and hero/card geometry visually align. Fresh desktop page height7691 equals current; fresh narrow top DOM height9807 vs current9819 (+12px). No complete fresh official traversal was performed, so this residual current-source height difference is not represented as exact latest full-page geometry parity.

accepted=false；動畫、UI、服務與最新全頁差異仍依result明列，沒有宣稱全面官方一致。本次沒有付費、登入、提交表單或部署。

當前證據：`supabase-oct12-current-verification.json`、`supabase-oct12-current-visual-review.json`；歷史脈絡保留於`supabase-oct12-evidence-lineage.json`。以下原設計分析與歷史稽核依原日期保留。

---

# Supabase目前公開首頁設計分析 — 2026-10-10

官方來源：https://supabase.com/ 。深灰背景、綠色重點、細邊框卡片與實際Postgres線框插畫，保留目前「Build in a weekend / Scale to millions」標題與完整產品網格。十二個客戶商標、實際Table Editor影片、React程式碼、六張範本、五家客戶展開卡、社群原始內容、111.2K GitHub圖像、完整六欄頁尾及安全標章均以今天官方的完整渲染DOM/CSS與原始公開素材校正。

主要版型與先前保存官方參考相同，因此重用9月27日 genuine Google Stitch MCP原生生成，10月10日透過get_screen重新確認並保存完整回應。原始HTML、PNG、生成紀錄、DESIGN.md/design-md及原分析均保留；沒有把原生候選當成驗證結果。

實際1280×720桌面與390×844窄版逐段捲動並截圖，完整頁面高度各7691、9819px，均與官方相同。最後在指定尺寸重新載入以排除固定導覽繪製殘留，58張DOM圖片皆載入、字型載入完成、無水平溢位。逐一檢視4張桌面及5張窄版2000px比較段；主要文字、格線、商標、範本、客戶卡與頁尾布局相合。影片與社群輪播相位不同、部分官方頭像未載入；這是實測範圍，不能推論全面官方一致。

## 尚有差異

- Actual official/local dashboard videos show different frames and the community column carousel is captured at different offsets. Layout and copy were compared; animation phase/timing parity is not claimed.
- Navigation dropdowns, narrow hamburger, dashboard/framework tab changes, customer-story expansion, theme/privacy controls and keyboard focus behavior remain captured initial UI states; they are not fully wired or accepted as official behavior.
- The current official captures had some community avatar requests not ready. Preserved public originals load locally; this is an explicit screenshot difference, not claimed pixel equality.
- The page is a dated public homepage study. Newsletter input is read-only and forms link out; dashboard, authentication, database/account services, real devices, other widths and final published deployment are outside verified scope.

accepted=false。未採購、付費升級或部署。

## 歷史紀錄：2026-10-12 補拍前的版本綁定稽核

以下「尚未重拍」與false flags只描述當時狀態；後續補拍已完成，請以本文開頭與最新result為準。

10月10日桌面/窄版完整畫面比較保留為歷史證據；D11/N12皆未記capture-time SHA。13:31事後manifest與目前d5d729…相合，舊build353872…差異來源未完整重建；不得宣稱目前SHA已整頁逐張驗證。

Historical D11/N12 observations contain no capture-time SHA. The later13:31 manifest/current d5d729… match is posthoc only; the original build record names353872… instead. The exact change from that build is not reconstructed here, and no current-SHA whole-page comparison is claimed.

完整歷史phase JSON未改寫，也沒有補造capture-time SHA。`currentFullPageCaptureComplete=false`、`currentFullPageComparisonComplete=false`；歷史完整觀察與精確未變範圍/局部補驗分開記錄，accepted=false。
