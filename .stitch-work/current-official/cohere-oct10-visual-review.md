# Cohere｜2026-10-11 畫面校正紀錄

來源：https://cohere.com/。目前重製檔 SHA-256：`e963788d73e8b4807ce6dd9f26e7bcbdf2c7c4531bf71d30f358bd51be502492`。

**accepted=false；不宣稱與官方一致。** 已完成新原生 Stitch 編輯與具體來源校正；實際畫面證據與未完成項目分別記錄。

| 取樣 | 座標範圍 | 實際影像數 | 完整範圍 | 目前重製檔 |
|---|---|---:|---|---|
| official_desktop | document_scroll：8947px | 13 | 是 | 官網來源 |
| local_desktop | document_scroll：8947px | 13 | 是 | 是 |
| official_narrow | document_scroll：10516px | 13 | 是 | 官網來源 |
| local_narrow | document_scroll：10516px | 13 | 是 | 是 |

已逐段查看對應目前檔案的所有本機截圖；仍須遵守下列可見差異與限制。

- Readable static reference is the actual official prefers-reduced-motion: reduce mode (D8947/N10516). Normal no-preference hero/headline reveals remained blank; those original captures are retained and normal animation parity remains unverified.
- Desktop stacked-card and announcement correction uses fresh actual2160/2880 active styles; fresh source body8867 differs from canonical8947. Canonical full evidence is retained. Between-sample timing and inferred65px last-card pin increment remain unverified.
- Independent inner-text translation is projected from actual canonical2160/2880 heading samples, with fresh active ancestor styles retained. Narrow scroll0 original logo/hamburger nav is restored below the80px announcement; nav-hide timing, Rive/video and logo carousel phases remain unverified.
- North video and logo carousel phases differ. Menus, industry/customer selections, industry/footer accordion behavior, forms, demo/sign-in and backend services are unverified.
- Official reference is actual prefers-reduced-motion:reduce; ordinary local browser uses an explicitly applied static visible source-CSS branch. This does not verify the default official motion mode; original no-preference blank captures remain retained.
- Desktop card/inner-text projections and narrow nav restoration are verified only at the actual sampled viewport/scroll phases. Between-sample GSAP/nav timing and fresh-active versus canonical page-height differences remain explicit.
- North video and logo carousel phases differ; menus, industry/customer selections, industry/footer accordions, forms, sign-in/demo/backend services remain unverified.
- Other widths, physical devices, regions, complete interaction/motion and the published deployment are unverified.

量測為輔助診斷，零壞圖候選或頁高相同不代表像素、文字、版面、動畫或服務完全一致。
