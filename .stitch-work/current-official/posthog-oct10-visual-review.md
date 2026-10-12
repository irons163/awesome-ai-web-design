# PostHog｜2026-10-11 畫面校正紀錄

來源：https://posthog.com/。目前重製檔 SHA-256：`65695ac21e4566ade46bc412e6a9297d3bf52f9edafde242fc4eb5bf0bca9560`。

**accepted=false；不宣稱與官方一致。** 已完成新原生 Stitch 編輯與具體來源校正；實際畫面證據與未完成項目分別記錄。

| 取樣 | 座標範圍 | 實際影像數 | 完整範圍 | 目前重製檔 |
|---|---|---:|---|---|
| official_desktop | element_scroll：4679px | 8 | 是 | 官網來源 |
| local_desktop | element_scroll：4679px | 8 | 是 | 是 |
| official_narrow | element_scroll：7725px | 11 | 是 | 官網來源 |
| local_narrow | element_scroll：7725px | 11 | 是 | 是 |

已逐段查看對應目前檔案的所有本機截圖；仍須遵守下列可見差異與限制。

- Coverage must use element-scroll offsets/extent/visible_extent, not document bodyHeight. Superseded390x219 JPEGs are not complete narrow evidence.
- Tabs, dock/window actions, menus, cloud choices, MCP install actions, live counts and signup/account services remain unverified.
- OS window controls/navigation, Ask/Give/Ship tabs, Pause/carousels, US/EU cloud selection, signup/install and services were not interaction-tested.
- Actual source97% free setup wording and98% pricing wording contradiction is retained, not normalized.
- Other widths, physical devices, regions, complete interaction/motion and the published deployment are unverified.

量測為輔助診斷，零壞圖候選或頁高相同不代表像素、文字、版面、動畫或服務完全一致。
