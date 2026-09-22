# Validation

Verified locally on 2026-09-22.

## Automated checks

Run `python3 -m unittest discover -s tests -v` after building. Coverage includes:

- Every imported public design is present with a design document, task prompts, README, and both previews.
- All generated task prompts are present in both DESIGN.md and PROMPTS.md; each prompt contains its specific brand context.
- Original prompt and iteration sections are removed without discarding following analysis sections.
- Catalog hashes and byte counts match the served design documents.
- Generated HTML and README local links resolve.
- Download archive integrity, complete documents, previews, and MIT notices.
- Preview accent foreground colors meet a 4.5:1 calculated contrast ratio.

`node --check assets/app.js` also passes. The application has no installed JavaScript dependencies.

## Browser checks

Using the Codex in-app browser against the local server:

- Catalog renders 74 items; Claude search produces one result.
- Automotive category produces 7 results; dark reference filter produces 17 results.
- Unknown search produces an empty state; clearing filters restores 74 results.
- Saving Claude persists through reload; removing it from the saved-only list shows the empty state.
- Claude detail opens from its hash URL; all three prompt panels are present.
- Copied task prompt and full document were checked against the browser clipboard.
- Light/dark preview switching updates the iframe target.
- Preview project form displays a confirmation containing the entered project name.
- Single Markdown and complete ZIP links both trigger browser download events.
- Tab navigation responds to arrow keys; Escape dismisses the detail dialog.
- Main page width equals viewport width at 390, 768, and 1440 pixels.
- Desktop catalog, mobile catalog, and mobile detail were visually inspected.

## Scope

This verifies the local implementation, not a public deployment or every browser engine. Brand analyses are preserved from the pinned upstream revision and have not all been checked against live brand sites. Previews are token specimens and alternate themes are interpretations, as labeled in the UI.
