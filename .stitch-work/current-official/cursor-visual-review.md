# Cursor public homepage reconstruction review · 2026-09-27

Status: **source-backed draft; not visually accepted as identical**.

The live Cursor homepage was observed at 1280×720. Its first viewport uses a 52px fixed header, #14120b background, CursorGothic typography, 26px two-line left-aligned heading, two 43px CTA pills, and a large product demo on Cursor's publicly served painted landscape. The live page's section titles and vertical positions, customer names, changelog headlines, article titles and URLs, current footer groups and links were recorded.

Google Stitch generated the raw desktop screen; the original HTML and screenshot are preserved in `cursor-stitch.html` and `cursor-stitch.png`. The generation matched the dark palette and broad section order but inserted fabricated telemetry, compiler and agent statistics, fictional testimonial quotes, arbitrary product UI copy, articles and incorrect routes. The refined `cursor.html` uses local public Cursor fonts, the official inline wordmark and wallpaper, a dated observed first-screen demo state, observed copy, public links, and no invented testimonials or metrics. It also replaces the generated feature visuals with source-backed simplified static UI and marks itself as a reconstruction draft in the publishing pipeline.

Remaining: visually compare the refined rendering with the current official desktop homepage; match the live rotating/interactive demo, exact brand logo tile art and feature visuals; compare tablet and mobile layouts and interactions; then independently verify the full page before acceptance. The refined file is **not** an exact visual match. A previous automatic browser review rejected opening local/public drafts for browser comparison, so no rendered comparison is claimed.
