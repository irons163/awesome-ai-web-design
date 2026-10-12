# 2026-10-12 目前稿完整補驗 — raycast

目前稿 SHA256：`2564ae11e6519d84a1cac9fdbb0ba923f481cc8650f5ac619cfd02b38e17aaa6`；本次未修改HTML、原生Stitch輸出、原始設計匯出或公開素材。

桌面1280×720共23張、窄版390×844共19張，從頂到頁尾完整實際視窗無缺口；每張當時記錄目前稿SHA、截圖SHA與截圖後URL/捲動守衛，PIL逐檔確認原生尺寸。兩次重新載入的document response bytes均與磁碟稿完全相等。全部42張完整視窗、16張對照圖與2張最新官方頂部對照已逐張檢視。所有DOM圖片載入、字型loaded，無頁面水平溢位。桌面檢視contact sheet使用半尺寸顯示，窄版原尺寸；原始JPEG完全未縮放或裁切。

`currentFullPageCaptureComplete=true`、`currentFullPageComparisonComplete=true`只表示目前SHA已整頁實看並與**原日期官方完整畫面**比較。`freshOfficialFullPageComparisonComplete=false`：最新官方另存完整DOM與一張頂部實拍，不冒充最新完整逐段來源。先前歷史phase及缺capture-time SHA的紀錄完全未改寫。

All23 complete current viewport frames and8 dated-source comparison segments viewed. Header, Clipboard History launcher, extension cards, AI section, community, six technical illustrations, keyboard, footer and restored Subscribe label are visible. Hero WebGL is blank locally; AI Extensions, snippets, hotkeys and SVG frames differ from the moving source.

All19 complete current viewport frames and8 dated-source comparison segments viewed. Final Window Management launcher state differs from source Clipboard History; fixed Granola/Things reply adds26px total height relative to dated source and shifts some sequential-composite sections by about51.5px around changing demo heights. Footer Subscribe is visible in the current complete sequence. No broken-image placeholder or horizontal page overflow observed.

Fresh official desktop top shows the red WebGL hero absent locally; desktop DOM height15992 vs current15991. Fresh narrow top was captured during initial fade/lazy initialization at height14051; its temporarily absent shortcuts section is not evidence of a design removal. Fresh source is top-only, dated full-source evidence remains separately timed.

accepted=false；動畫、UI、服務與最新全頁差異仍依result明列，沒有宣稱全面官方一致。本次沒有付費、登入、提交表單或部署。

當前證據：`raycast-oct12-current-verification.json`、`raycast-oct12-current-visual-review.json`；歷史脈絡保留於`raycast-oct12-evidence-lineage.json`。以下原設計分析與歷史稽核依原日期保留。

---

# Raycast 目前公開首頁設計分析

來源 https://www.raycast.com/，觀察及最後校正2026-10-11。黑色背景、Inter字體、紅色Raycast識別與膠囊固定導覽。保留64px主標 Your shortcut to everything.、最新macOS Tahoe/AppleSilicon下載提示與鍵盤公告。完整新版 Take shortcuts, not detours. 真實啟動器、鍵盤特性、商店擴充套件、AI Agent/Chat/QuickAI/AIExtensions、24位社群人物、Snippets/Quicklinks/Hotkeys、十二工具、社群影片、開發者技術圖及六欄頁尾均來自目前完整渲染DOM/CSS。

原保存來源缺少新版主要內容，因此重新透過 genuine Google Stitch MCP 校正。新原生候選與完整回應獨立保存，未將供應者的技術聲明或虛構客戶採用為官方內容。校正版保存320份公開原素材，並補入實際可見Granola/Things工作流程與正確窄版reel捲動位置。原始native、DESIGN.md/design-md、舊草稿及不同時期官方證據均保留。

桌面23段、窄版19段本機實際視窗截圖，來源桌面23段、窄版20段加一張補缺口截圖；PIL逐一驗證1280×720與390×844真實尺寸。十六張2000px比較圖皆已目視檢查。桌面頁高15991px相同；窄版固定AI示範狀態15973px，比來源15947px長26px。125/112張圖片載入、字型完成、無水平溢位。主內容與資產一致性僅涵蓋上述觀察，WebGL及動態/互動保留差異。

- The public hero WebGL canvas is blank in the static corrected page. The actual narrow source shows the red moving hero, and the desktop source includes red edges in one frame. Canvas export was unsupported by the read-only browser scope; no invented raster substitute was used.
- The narrow launcher is frozen to the captured final Window Management selection, while the source first visible phase showed Clipboard History. Public original images and the final selected reel offset are preserved; auto-advance timing is not equivalent.
- The AI Extensions demo now contains the exact independently captured public Granola/Things workflow, including eight original image nodes. Its fixed reviewed-message state differs from the empty/typing source phase, and the narrow fixed page is26px taller (15973 vs15947). The source capture also changes demo height by25.5px; a supplemental actual viewport fills the coverage gap. Sequential composite offsets can differ by about51.5px around changing demo phases.
- Snippets text, Quick AI typing, key highlights/hotkeys, testimonial selection, extension carousel and illustrated technical SVG animation phases differ. Complete menu, download options, category/tool tabs, keyboard interactions, focus and dynamic demos have not been accepted.
- The Subscribe input label was restored from the public source after the full page comparison. Exact static diff proves only the two responsive submit inputs changed (valueSubscribe and readonly removed); the main phase evidence remains explicitly bound to the pre-label-patchSHA. Final desktop and narrow footer screenshots separately verify the restored Subscribe label at actual1280×720/390×844; those supplements are bound to the finalSHA.
- Account/newsletter services, downloads, other pages, real phone hardware, untested viewport widths and published deployment are outside this review. No forms were submitted.

accepted=false；未宣稱全面官方一致。未購買或升級；帳戶計費未稽核。

## 歷史紀錄：2026-10-12 補拍前的版本綁定稽核

以下「尚未重拍」與false flags只描述當時狀態；後續補拍已完成，請以本文開頭與最新result為準。

完整整頁比較屬4bf651…歷史稿；目前2564ae…僅兩個Subscribe輸入標籤不同，已做精確雙向位元組證明及目前SHA頁尾補驗，未宣稱目前稿整頁逐段重拍。

Full current-SHA D/N page recapture was not performed. Historical full-page screenshots bind to4bf651…; exact two-input normalization proves the remaining bytes unchanged. Final footer-only screenshots bind to2564ae… and verify the changed Subscribe labels.

完整歷史phase JSON未改寫，也沒有補造capture-time SHA。`currentFullPageCaptureComplete=false`、`currentFullPageComparisonComplete=false`；歷史完整觀察與精確未變範圍/局部補驗分開記錄，accepted=false。
