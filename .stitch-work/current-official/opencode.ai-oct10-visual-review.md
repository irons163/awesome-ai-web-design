# OpenCode｜2026-10-11 畫面校正紀錄

來源：https://opencode.ai/。目前重製檔 SHA-256：`b4bf44470a8930a975313a2eb647d23ecd3b2abf0708f3907205c5a4011c90e4`。

**accepted=false；不宣稱與官方一致。** 已完成新原生 Stitch 編輯與具體來源校正；實際畫面證據與未完成項目分別記錄。

| 取樣 | 座標範圍 | 實際影像數 | 完整範圍 | 目前重製檔 |
|---|---|---:|---|---|
| official_desktop | document_scroll：4209px | 6 | 是 | 官網來源 |
| local_desktop | document_scroll：4209px | 6 | 是 | 是 |
| official_narrow | document_scroll：4326px | 6 | 是 | 官網來源 |
| local_narrow | document_scroll：4326px | 6 | 是 | 是 |

已逐段查看對應目前檔案的所有本機截圖；仍須遵守下列可見差異與限制。

- Source height changed from3314 to4209 during loading. Later source metrics/text are dated samples, not live GitHub/provider guarantees.
- Original demo/poster bytes are preserved; exact playback, copy/install tabs, FAQ, newsletter, desktop downloads and coding-agent services are unverified.
- Original terminal video plays a different local phase from the source blank/faint-logo phase; exact video timing remains unverified.
- Navigation, FAQ, install tabs, code copy, newsletter, downloads and services remain unverified.
- Other widths, physical devices, regions, complete interaction/motion and the published deployment are unverified.

量測為輔助診斷，零壞圖候選或頁高相同不代表像素、文字、版面、動畫或服務完全一致。
