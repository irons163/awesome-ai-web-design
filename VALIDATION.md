# Validation

The collection is checked locally before publication. This revision replaces the previous token specimens with individual Google Stitch generations over MCP.

## Official study review — October 13, 2026

The current publication metadata has 73 studies with scoped desktop/narrow raster comparisons and one unverified study, Pinterest. None is marked accepted or claimed identical to the current official site. The six new records bind the exact current preview SHA-256, original full-page JPEGs, viewport measurements, reviewed comparison sheets, and remaining differences in `.stitch-work/current-official/*-oct13-result.json`.

The Verge and WIRED now load checksum-verified preserved images instead of allowing remote image variants to override them. Vodafone's static study displays the final content reveal state; animation timing remains unverified. Pinterest's local adaptation fits 320, 390, 768, and 1280px viewports, but repeated official-page loads produced no readable content, so its visual comparison remains unverified. Live news, theme, media frames, advertising, and source layout changes are documented in each study's public review note. Original Stitch exports and the 74 design analyses / 222 task prompts remain preserved.

## Automated checks

Large official images, videos, and fonts use exact static redirects to original bytes at a verified immutable GitHub commit. Both build entry points validate file sizes and SHA-256 before removing those copies from the deployment package; source files and study HTML stay intact. Regression checks reject mutable references or altered media and require an uploadable static bundle. The local `/dist/` preview applies the same redirect rules.

Run `python3 scripts/rewrite_prompts.py`, `python3 scripts/build.py`, then `python3 -m unittest discover -s tests -v`. The collection checks cover:

- All 74 designs have their analysis, rewritten task prompts, README, original Stitch HTML export, generation prompt, and provenance record.
- All 222 task prompts are distinct and include their corresponding design context.
- Removing upstream AI instructions preserves the surrounding design analysis.
- Every preview has a distinct Stitch screen ID and HTML checksum. Exported HTML, screenshots, thumbnails, and generation prompts match their SHA-256 records.
- Full screenshots retain desktop resolution; old alternate-theme specimens are absent.
- Catalog document hashes, byte counts, categories, and color values match the files.
- Catalog and README links resolve; the collection has no paid-access routes.
- The hosted catalog uses immutable GitHub image URLs, while local exports and the complete ZIP retain all original image files. Hosted HTML, prompts, and provenance remain local assets.
- The complete ZIP contains the same exported files, design documents, and MIT notices.

`node --check assets/app.js` verifies JavaScript syntax. Rebuilding must leave tracked generated files unchanged. The catalog has no installed JavaScript dependencies.

## Browser checks

The local catalog is checked in the Codex in-app browser:

- Search and category filters display the matching designs.
- Detail views show actual Stitch screenshots and switch to the exported HTML.
- Claude, Spotify, and retro designs have visibly distinct page structures.
- Screenshot previews and HTML download links are accompanied by the actual generation prompt and provenance JSON.
- Escape dismisses the detail dialog.
- The mobile catalog and detail layout fit a 390-pixel viewport without horizontal overflow.

## Scope

These are static generated UI examples, not official brand websites or working product backends. Their illustrative forms and links are not end-to-end product features. The HTML exports are preserved as supplied by Stitch and may depend on external fonts, Tailwind, and image hosts. Screenshots and catalog thumbnails are preserved in the repository and ZIP. The hosted catalog loads those same files from an immutable GitHub commit. The embedded HTML uses a sandbox without same-origin access.

The checks do not certify every generated demo's accessibility, business logic, responsive behavior, external assets, or compatibility with every browser. The design analyses remain based on the pinned upstream revision, rather than a new audit of every live brand website.
