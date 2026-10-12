# ClickHouse｜2026-10-11 畫面校正紀錄

來源：https://clickhouse.com/。目前重製檔 SHA-256：`3c5e9e082010d6cedd5415c1c49baf85313769c6577c73d9c1115552f652f55b`。

**accepted=false；不宣稱與官方一致。** 已完成新原生 Stitch 編輯與具體來源校正；實際畫面證據與未完成項目分別記錄。

| 取樣 | 座標範圍 | 實際影像數 | 完整範圍 | 目前重製檔 |
|---|---|---:|---|---|
| official_desktop | document_scroll：9819px | 14 | 是 | 官網來源 |
| local_desktop | document_scroll：9819px | 14 | 是 | 是 |
| official_narrow | document_scroll：12542px | 15 | 是 | 官網來源 |
| local_narrow | document_scroll：12542px | 15 | 是 | 是 |

已逐段查看對應目前檔案的所有本機截圖；仍須遵守下列可見差異與限制。

- Canonical desktop reference was freshly warmed and recaptured in14 complete phases; earlier blank/load phases are retained separately under clickhouse-oct11-official-1280-before-warm-*. The invalid333px desktop diagnostic is excluded from current visual evidence.
- Marquees, counters, row/column chart GIF phases and FAQ left-side motion differ by time. Navigation, filters, FAQ, video controls and actual services remain unverified. Counts and customer wording are dated samples.
- The actual public newsletter iframe was reconstructed from saved DOM/computed styles. Hidden tracking fields, scripts and submit action are removed; button type=button. Subscription, validation and backend are not implemented or verified.
- Optional stylesheet3jrdzpyzqpmrl.css and a separate2c55 Cyrillic font subset returned ordinaryHTTP403 and were not retried or fetched by another route. Original external Latin Inter remains; the English form does not use that Cyrillic subset. Complete external CSS/offline font fidelity is unverified.
- Latest official desktop was freshly warmed and fully recaptured; original before-warm phases and invalid333px diagnostic remain historical, excluded from current whole-page proof.
- Marquee/counter/row-column chart GIF timing and FAQ left-side motion differ; nav/filter/FAQ/video/service behavior remains unverified.
- Newsletter form uses actual public iframe DOM and observed computed styles, with hidden tracking fields/scripts/action removed and a non-submitting button. Subscription/validation/backend unimplemented and unverified.
- Original external Latin Inter declaration remains. Optional stylesheet and separate Cyrillic subset ordinary403 failures were preserved without retry or alternate route; offline font fidelity remains unverified.
- Other widths, physical devices, regions, complete interaction/motion and the published deployment are unverified.

量測為輔助診斷，零壞圖候選或頁高相同不代表像素、文字、版面、動畫或服務完全一致。
