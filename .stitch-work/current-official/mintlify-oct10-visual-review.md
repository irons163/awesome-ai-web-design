# Mintlify｜2026-10-11 畫面校正紀錄

來源：https://www.mintlify.com/。目前重製檔 SHA-256：`13fbd9656db4274d733a85445bf0f2a748202461c19fdf104473e990a3da1443`。

**accepted=false；不宣稱與官方一致。** 已完成新原生 Stitch 編輯與具體來源校正；實際畫面證據與未完成項目分別記錄。

| 取樣 | 座標範圍 | 實際影像數 | 完整範圍 | 目前重製檔 |
|---|---|---:|---|---|
| official_desktop | document_scroll：8457px | 12 | 是 | 官網來源 |
| local_desktop | document_scroll：8457px | 12 | 是 | 是 |
| official_narrow | document_scroll：12555px | 15 | 是 | 官網來源 |
| local_narrow | document_scroll：12555px | 15 | 是 | 是 |

已逐段查看對應目前檔案的所有本機截圖；仍須遵守下列可見差異與限制。

- Thirteen actual initial-visible canvas bitmap phases per width (indices0..9,12..14) are preserved and displayed on original canvas boxes. Hidden horizontal customer-card slots10/11 remain unseen;26 static bitmap phases do not prove live canvas animation parity.
- Latest updates uses original WebP images. Initial decoded-but-unpainted black frames are preserved privately as mintlify-oct11-first-paint-* diagnostics; unchanged current HTML was fully recaptured after warming and the actual images then inspected. Cold first-paint timing is unverified.
- Frozen canvas wave, desktop brand/logo rotation, live counters/agent statistics and testimonial phases differ by time. Menus, carousels, Ask assistant, forms, Google sign-in, tabs and backend remain unverified; no paid account backend is used.
- Actual frozen canvas wave phase, desktop brand/logo rotation, live counters/agent statistics and testimonial phases are not synchronized.
- Hidden horizontal canvas slots10/11 were not observed; the13 actual bitmap phases per width do not establish live animation parity.
- Latest updates original WebP images are complete in the warmed no-reload full desktop/narrow captures. Earlier decoded-but-unpainted black frames/phaseJSON are retained privately as first-paint diagnostics and excluded from current proof. Cold first-paint timing remains unverified.
- Menus, carousels, Ask assistant, forms, sign-in and backend are unverified.
- Other widths, physical devices, regions, complete interaction/motion and the published deployment are unverified.

量測為輔助診斷，零壞圖候選或頁高相同不代表像素、文字、版面、動畫或服務完全一致。
