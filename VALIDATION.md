# Validation

The collection is checked locally before publication. This revision replaces the previous token specimens with individual Google Stitch generations over MCP.

## Automated checks

Run `python3 scripts/rewrite_prompts.py`, `python3 scripts/build.py`, then `python3 -m unittest discover -s tests -v`. The eight checks cover:

- All 74 designs have their analysis, rewritten task prompts, README, original Stitch HTML export, generation prompt, and provenance record.
- All 222 task prompts are distinct and include their corresponding design context.
- Removing upstream AI instructions preserves the surrounding design analysis.
- Every preview has a distinct Stitch screen ID and HTML checksum. Exported HTML, screenshots, thumbnails, and generation prompts match their SHA-256 records.
- Full screenshots retain desktop resolution; old alternate-theme specimens are absent.
- Catalog document hashes, byte counts, categories, and color values match the files.
- Catalog and README links resolve; the collection has no paid-access routes.
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

These are static generated UI examples, not official brand websites or working product backends. Their illustrative forms and links are not end-to-end product features. The HTML exports are preserved as supplied by Stitch and may depend on external fonts, Tailwind, and image hosts. Screenshots and catalog thumbnails are stored locally. The embedded HTML uses a sandbox without same-origin access.

The checks do not certify every generated demo's accessibility, business logic, responsive behavior, external assets, or compatibility with every browser. The design analyses remain based on the pinned upstream revision, rather than a new audit of every live brand website.
