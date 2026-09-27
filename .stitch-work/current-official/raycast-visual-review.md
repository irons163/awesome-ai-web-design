# Raycast public homepage reconstruction review · 2026-09-27

Status: **source-backed draft; not visually accepted as identical**.

The current public homepage was inspected in the in-app browser at 1280×720. It has a fixed dense rounded navigation, a nearly black viewport, a live Three.js red diagonal hero, centered 64px Inter heading, a Raycast launcher product scene, then editorial sections for speed, extensions, AI, professional users, automation, community, developers, and download. The captured public wordmark, red feature background, and Linear/Spotify/Slack extension previews have URL and SHA-256 provenance in `raycast-asset-provenance.json`.

Native Google Stitch generated a full page and red Three.js ribbon animation. Its raw HTML and thumbnail are preserved. It also omitted three navigation entries and invented first-viewport placement, app commands, latency statistics, old AI model names, and product claims. The refined draft restores the observed navigation, headings, public URLs, current macOS requirement, observed product UI content, and public assets. The hero uses the site's public red feature artwork as a **static fallback**, because Stitch's ribbon animation is not the site's actual Three.js implementation.

Remaining: visually compare the refined page with the current public desktop page, refine the full-page layout, test tablet and mobile, and inspect interaction behavior. A previous automated browser review rejected opening the local/public draft for this comparison; do not treat the source-backed layout as a pixel match.
