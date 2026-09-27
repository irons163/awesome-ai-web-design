# Supabase official homepage reconstruction review

- Current reference: https://supabase.com/, observed on 2026-09-27 in a 1280 × 720 in-app browser. `supabase-source.html` is a separate 2026-09-22 HTML snapshot.
- Native Google Stitch output: `supabase-stitch.html` and `supabase-stitch.png`, screen `projects/17453614638842022136/screens/bfff0942e8f04f96bdcc6a2db231833e`.
- Stitch got the dark palette and broad section order, but used six image placeholders, a text imitation of the logo, inactive links, fictitious database rows and technical badges absent from the live product cards. Its 1280px minimum viewport width also prevented a responsive layout.
- `refine-supabase.py` writes `supabase.html` from the generated screen and observed public reference. It keeps the native output unchanged for traceability, restores the official inline logo and product illustrations, source-backed copy and links, three genuine dashboard videos, six current framework code examples, 12 official customer marks and the current five-story accordion content. The page remains a dated draft.

## Directly observed desktop reference

At 1280px wide, the official site has a roughly 55px announcement and 64px sticky dark header. A Manrope 46px heading occupies x96/y281 to x632/y373, while the intro copy sits in the right column around x648/y305. The two action buttons begin around y405. The product grid begins at x96/y507, spans 1088px, and gives the Postgres card 538px width, then Authentication and Edge Functions 263px each. A second row has four equal product cards. Later sections include a two-row customer-logo strip, three-tab dashboard video, framework code panel, templates, five customer stories, community, open source, CTA and footer.

## Outstanding acceptance work

- The refined draft has not been visually compared with the official desktop or mobile pages. A previous automatic browser safety decision rejected local and public draft browsing, and this work did not retry through another browser or localhost route. It is not accepted as visually identical.
- Product-card illustration opacity/cropping, announcement decoration, full-page spacing, animations, responsive breakpoints, navigation dropdowns and footer still need direct comparison.
- The community carousel and some decorative template art are simplified; they must be recreated from current official evidence before full acceptance.
