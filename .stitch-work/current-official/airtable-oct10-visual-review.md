# Airtable — 2026-10-10 畫面比對

狀態：已逐段比對，仍有明確差異；未接受為完整官方一致。

- Current public Airtable homepage inspected on 2026-10-10 at1280x720 and390x844; full source reference length and SHA-256 checked, with complete closed page plus desktop Platform/Solutions/Resources and narrow drawer references.
- Two genuine Google Stitch MCP requests completed; raw provider HTML/PNG exports and complete text/suggestions preserved unchanged. The MOBILE request returned DESKTOP2560 metadata and is explicitly recorded as a mismatch.
- Corrected clone uses current official wording, public stylesheet bytes, Neue Haas font files, original SVG markup and64 observed public asset records with SHA-256. Browser image Accept negotiation restored the transparent customer logo.
- 原先每份官方／本機桌面與窄版各11段實際截圖。10月11日重新檢查覆蓋範圍時，發現舊本機桌面在1440至1457.5px間留有17.5px缺口；已以目前相同檔案的1440px位置實際截圖補齊，沒有修改舊量測或補寫當時未記錄的逐段檔案雜湊。桌面7421px、窄版8510px的完整範圍現在由原紀錄加上補充畫面覆蓋。
- 原44張官方／本機截圖已逐段檢視，補充畫面亦已和原官方同位置截圖實際比對。九個主要標題與頁面幾何是輔助證據，不能推定完整像素或互動一致；補充畫面中的影片時間點仍不同。

## 尚待校正或未驗證

- Original hero and eBay promotional video frame synchronization and occasional desktop capture/compositor blank video frame; video is playing locally but exact rendered capture state remains unaccepted.
- Exact source scroll thresholds, animation timing and narrow chapter-strip horizontal motion. Compact wordmark and basic active-section behavior have been corrected.
- Footer expansion, cookie preferences, complete nested navigation, keyboard/focus and narrow interactions; narrow emulation pointer routing was unreliable and no interaction parity is claimed.
- Tablet/intermediate widths, real mobile hardware, and production-page verification.

完整證據、畫面名稱和驗證尺寸見 `airtable-oct10-result.json`。原始 Stitch 輸出與工作校正稿分開保存，原 DESIGN.md 及三組 AI 指令保留。
