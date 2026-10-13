# Validation

The collection is checked locally before publication. This revision replaces the previous token specimens with individual Google Stitch generations over MCP.

## Official study review — October 13, 2026

The current publication metadata has 74 studies with scoped desktop/narrow raster comparisons. None is marked accepted or claimed identical to the current official site. The six latest records bind the exact current preview SHA-256, original full-page JPEGs, viewport measurements, reviewed comparison sheets, and remaining differences in `.stitch-work/current-official/*-oct13-result.json`.

The Verge and WIRED now load checksum-verified preserved images instead of allowing remote image variants to override them. Vodafone's static study displays the final content reveal state; animation timing remains unverified. Pinterest's official page became readable on the latest direct attempt, allowing complete 1280×720 and 390×844 raster review. Its current Traditional Chinese hero and new seasonal mosaic differ from the retained English Halloween draft. At 390px the official document overflows to 800px, while the draft uses a separate stacked adaptation. Both full rasters and visible-viewport evidence are retained; this is not physical mobile or interaction acceptance. Live news, theme, media frames, advertising, and source layout changes are documented in each study's public review note. Original Stitch exports and the 74 design analyses / 222 task prompts remain preserved.

## Automated checks

Large official images, videos, fonts, and catalog screenshots use their original same-origin paths. The Vinext Worker streams only allowlisted files from verified immutable GitHub commits. Both staging entry points check source sizes and SHA-256 before removing large files from the deployment bundle; no HTML, CSS, JavaScript, JSON, or inline SVG bytes are rewritten. The publication manifest binds equal source/published hashes. Each relative dependency must resolve to a bundled file or a verified Worker media route. `pnpm run test:media` checks streaming, byte ranges, HEAD, conditional caching, upstream failures, and rejection of unlisted paths without forwarding visitor credentials. Compressed and expanded archives are checked against the actual 256 MiB hosting limits. Use `pnpm run dev` for the full Worker preview; the staging-only `/dist/` directory requires those routes.

Run `python3 scripts/rewrite_prompts.py`, `python3 scripts/build.py`, then `python3 -m unittest discover -s tests -v`. The collection checks cover:

- All 74 designs have their analysis, rewritten task prompts, README, original Stitch HTML export, generation prompt, and provenance record.
- All 222 task prompts are distinct and include their corresponding design context.
- Removing upstream AI instructions preserves the surrounding design analysis.
- Every preview has a distinct Stitch screen ID and HTML checksum. Exported HTML, screenshots, thumbnails, and generation prompts match their SHA-256 records.
- Full screenshots retain desktop resolution; old alternate-theme specimens are absent.
- Catalog document hashes, byte counts, categories, and color values match the files.
- Catalog and README links resolve; the collection has no paid-access routes.
- The hosted catalog uses same-origin routes backed by immutable GitHub media, while local exports and the complete ZIP retain all original image files. Hosted HTML, prompts, and provenance remain local assets.
- The complete ZIP contains the same exported files, design documents, and MIT notices.

`node --check assets/app.js` verifies JavaScript syntax. Rebuilding must leave tracked generated collection files unchanged. The catalog UI remains plain JavaScript; the hosting Worker uses the supplied Vinext starter and Sites build integration.

## Browser checks

The local catalog is checked in the Codex in-app browser:

The same-origin Worker preview loaded all 157 preserved The Verge image elements and all 70 local WIRED image elements, with fonts loaded. All six Bugatti videos decoded at 1920×1080; an actual 1024-byte range request returned 206 and matched the original video bytes. Pinterest's captured draft loaded all 35 images at both review sizes. These checks cover the selected preserved assets; independent third-party advertising/tracking endpoints and full product interactions remain outside that claim.

- Search and category filters display the matching designs.
- Detail views show actual Stitch screenshots and switch to the exported HTML.
- Claude, Spotify, and retro designs have visibly distinct page structures.
- Screenshot previews and HTML download links are accompanied by the actual generation prompt and provenance JSON.
- Escape dismisses the detail dialog.
- The mobile catalog and detail layout fit a 390-pixel viewport without horizontal overflow.

## Scope

These are static generated UI examples, not official brand websites or working product backends. Their illustrative forms and links are not end-to-end product features. The HTML exports are preserved as supplied by Stitch and may depend on external fonts, Tailwind, and image hosts. Screenshots and catalog thumbnails are preserved in the repository and ZIP. The hosted catalog streams those same files through same-origin routes from an immutable GitHub commit. The embedded HTML uses a sandbox without same-origin access.

The checks do not certify every generated demo's accessibility, business logic, responsive behavior, external assets, or compatibility with every browser. The design analyses remain based on the pinned upstream revision, rather than a new audit of every live brand website.
