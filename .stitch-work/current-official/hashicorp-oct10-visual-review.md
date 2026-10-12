# HashiCorp visual review

Final preview SHA256: `23f47928855b5d0aa34c3fa48e8f844769a1ae9d42fb5d24181f5bf9fd144f54`.

Owner inspected all8 final comparison montages and official/local root-menu rasters. Canonical desktop13+ narrow14 segments per side cover8653/11578px with actual1280x720/390x844 originals. Eleven positive-size headings match text and geometry. Footer29px desktop/55px narrow error was fixed by excluding two runtime-disabled Marketo stylesheets, captured in stylesheet-states.json. Initial white-gap/lazy-paint and later333px cropped-compositor diagnostics are excluded; final official desktop was captured in a fresh tab after all sections loaded. Main text, illustrations, crops and section/footer geometry visually agree within the recorded scope. Current SVG sprite429 causes visible absent arrows/product/social/menu icons; these are explicitly unmatched. Root menu opens and closes, with source white navigation preserved and missing icon differences retained.

Coverage and actual original raster dimensions are recorded in the result JSON. CSS viewport coverage and raster pixel resolution are separate measurements. Uniformly scaled originals are retained unaltered; comparison montages may normalize viewing widths. Cropped or stale compositor diagnostics are excluded.

Remaining differences and limits:

- Current public SVG sprite returnsHTTP429, leaving native arrows, HCP badge, lifecycle/product glyphs, language/social icons and hamburger/close glyphs absent; these are visible unmatched differences. Four unused nested-menu decorative icon URLs also429.
- Desktop customer-logo marquee time phase differs; exact native animation timing and transitions are unverified.
- Only default Accelerate and What is new tab states and root mobile menu were visually compared; alternate tabs, desktop dropdowns, nested mobile panels, language/cookie/form behavior are not implemented or fully reviewed.
- Signup is a visual read-only study; account, subscription, sales and authenticated services remain official destinations.
- Only1280x720 and390x844 desktop-UA responsive viewports reviewed. Other widths, physical phones and final public deployment remain outside this owner review.
