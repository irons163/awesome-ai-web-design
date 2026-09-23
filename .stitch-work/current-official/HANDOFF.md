# Current official rebuild — 2026-09-23

User target: all 74 examples should resemble each brand's current public official website. Preserve design analysis, rewrite AI instructions, and keep the collection free. All 74 remain unfinished until individually verified. Do not use raw Stitch export existence as fidelity proof.

4 native regenerated examples staged: Spotify, Linear, Claude, and Notion. None has passed whole-page and responsive verification. Remaining 70 are not regenerated. 59 public reference source fetches succeeded, but metadata is not a visual review.

## Rebuild commands

```sh
python3 .stitch-work/current-official/refine-spotify.py
python3 .stitch-work/current-official/extend-spotify-tw.py tw
python3 .stitch-work/current-official/extend-spotify-tw.py ca
python3 .stitch-work/current-official/refine-linear.py
python3 .stitch-work/current-official/extend-linear.py
python3 .stitch-work/current-official/refine-claude.py
python3 .stitch-work/current-official/fetch-notion-assets.py
python3 .stitch-work/current-official/refine-notion.py
```

Spotify: Taiwan public page observed 2026-09-22T21:23:17Z at 1280×720 and saved in `spotify-tw-browser-reference.json`. All 54 observed card images, labels, destination links and Taiwan footer links are in the Stitch-derived preview `spotify.html`. The five section headings match the current Taiwan page y positions within 0.01px (87, 437.789, 742.516, 1073.242, 1376.969). First viewport and footer were visually compared. Canada public page observed 2026-09-23T12:27:47Z at 1280×720 and saved in `spotify-ca-browser-reference.json`; `spotify-ca.html` contains its separate 54 cards and Canada footer links. The Canada preview has passed static content checks only, not visual comparison. `refine-spotify.py` writes the common `spotify-base.html`; `extend-spotify-tw.py` now accepts `tw` or `ca` to build both locale variants from that base. These are regional snapshots, not universal live content. Remaining: typography, header icon details, final image loading while scrolling, interactions, and responsive checks. `extend-spotify-ca.py` is an obsolete older Canada refinement retained for provenance.

Linear: the first viewport hero, observed issue copy and seven official SVG customer marks are staged. The app demo visuals and lower illustrations still differ substantially. Generated fictional metrics/people in feature sections must be replaced with observed official page content. Do not mark finished.

Claude: native Stitch project `5880004248551648334`, design system `assets/4820437330963276936`, screen `d7061e8e298c49fe9272e523e04176b1`. Raw export: `claude-stitch.html` and `claude-stitch.png`. Public desktop reference observed 2026-09-23 at 1280×720. Its actual hero uses the captured `claude-official-hero.mp4`, not the fictitious Cowork checklist Stitch generated. `claude-browser-reference.json` contains observed coordinates, plan features, footer links, wordmark and plan pictograms. `refine-claude.py` creates `claude.html`, replacing fictitious content and loading the official Roman fonts. This output has passed static checks only: desktop visual comparison, responsiveness and interactions remain. A new claude.com tab redirected to a different claude.ai login page, so the public experience may vary by cookie/experiment/region. The agent browser's URL policy blocked opening the local file preview; do not retry through another browser URL as a workaround.

Notion: native Stitch project `9159430735492729198`, design system `assets/10627265804314086532`, screen `0de4921291454131b4d9748e7d01b63b`. Public desktop homepage observed 2026-09-23 at 1280×720; `notion-browser-reference.json`, `notion-assets-browser-reference.json`, and `notion-logo-browser-reference.json` save browser-observed details. `notion-stitch.html`/`.png` preserve the raw Google Stitch output. Stitch inserted image placeholders and made-up agent usage counts. `fetch-notion-assets.py` saves the official public hero video, font files, customer logos, feature imagery, case icons and customer portraits with URL provenance. `refine-notion.py` writes `notion.html` with actual media and observed copy. Static audit passed: 24 local media references and 46 links, no missing local files or placeholders. Refined HTML has not been visually checked due the agent browser's local-file URL policy; do not retry the same preview through localhost or another browser path. Responsive fidelity, animations, menu controls, full-page comparison and catalog integration remain. Stitch suggested optional pill-state interactivity, a 390px mobile layout, and use-case preview modals; only the first two reflect obvious source behavior and still need evaluation against the official page.

Raw `*-stitch.html` exports, native response JSON and request JSON are preserved separately from refined HTML. Original `spotify.png`, `linear-stitch.png`, and `claude-stitch.png` are raw Stitch screenshots, not screenshots of refined pages; never publish them as refined screenshots.

## Publication

Existing Site project `appgprj_6ab202e80eb08191ab7ab27168509bf0` for `https://awesome-ai-web-design.philqq100.chatgpt.site/` is accessible again. The official Sites open workflow returned this checkout at commit `4883985f3a6fa98ba295c0ca0198b3f1cbcc7256`. Do not create a replacement Site; preserve the hosting manifest.

No preview integration, source push, or public redeployment occurred in this rebuild. Existing catalog remains the old generated demonstrations. `ATTRIBUTION.md` was updated to distinguish unpublished official-site working assets from the MIT-licensed original collection. The `.stitch-work` directory is ignored by Git; use `git add -f` for a deliberate selection of new files rather than force-adding every fetched source.
