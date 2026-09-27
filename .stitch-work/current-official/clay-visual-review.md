# Clay Global homepage reconstruction review · 2026-09-27

Status: **source-backed draft; not visually accepted as identical**.

The current public global-English homepage was inspected at 1280×720. The live reference has a 108px top navigation, a pale-gray hero with a two-line 64px headline and white 3D satellite, a 1130×636px showreel, two-column service text/accordions, pale client-logo wall, 1130×638px dark Fintech panel, a long asymmetric portfolio, a studio section, dark news and FAQ, and a light contact/footer section. The dated reference file records section positions and wording.

Native Google Stitch generated the initial screen architecture and two SVG graphics. Its raw `clay-stitch.html`, `clay-stitch.png`, and graphics are preserved. Stitch also supplied generic illustrations and invented hero copy. The refined `clay.html` removes those substitutions, uses Clay's publicly served logo and Universal Sans fonts, 14 official case-study images, 20 official client marks, actual news and team media, the current showreel poster, observed copy and links. The two animated 3D scenes are represented by still crops captured from the public official page; they are not interactive 3D reproductions. Asset URLs and SHA-256 hashes are in `clay-asset-provenance.json`.

Remaining: render and compare the refined page with the current official site at desktop and mobile sizes; match 3D animation, showreel playback, client-logo motion, masonry spacing, navigation behavior, news placement and footer details. A previous automatic browser review rejected opening local/public drafts for visual comparison, so no rendered comparison or pixel-perfect claim is made.
