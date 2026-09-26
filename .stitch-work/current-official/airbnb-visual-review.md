# Airbnb Canada draft: partial visual review

The public reference was observed on 2026-09-26 at `https://www.airbnb.ca/?locale=en`. The saved `airbnb-browser-reference.json` and `airbnb-official-full.jpg` are dated evidence, not proof of today's site.

- Source screenshot SHA-256: `51aac762605410274685f7bbb739a188877e8b711a4cf331470f714f3702e57d` (1280 × 5678 JPEG; the original local capture had an incorrect `.png` extension).
- Draft reviewed: `airbnb.html`, SHA-256 `887db01b954d870a70fc7095cd595e5908f12b3e0b11797ad3a21f1b679acfc9`.
- The saved screenshot visually occupies the left 640 pixels of a 1280-pixel canvas at half the draft's apparent scale. For first-screen comparison, crop the left 640 × 360 pixels and enlarge 2×. This normalization is observational; the original capture mechanism did not record a device-pixel or zoom explanation.
- The draft was rendered at 1280 × 720 with all HTTP(S) requests aborted before navigation. It made 54 blocked asset requests, so this review does **not** validate loaded photo or icon pixels. Header, search bar, experience carousel and service carousel align closely in the normalized first screen. Their text and visible hierarchy match.
- Content audit against the saved browser JSON: 96/96 card image URLs, links and titles match; 17/17 category image URLs and labels match; all 16 non-null category links match; 4/4 nav icon URLs match.

Acceptance is **partial first-screen layout review only**. Full-page and responsive visual comparison, rendered images, current official-site comparison, and the pending official-targeted Stitch screen remain outstanding. Do not mark Airbnb complete or pixel-identical.
