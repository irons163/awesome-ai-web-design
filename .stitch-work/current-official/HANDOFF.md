# Current official rebuild — 2026-09-23

User target: each brand’s current public official website. All 74 remain unfinished until individually verified. Do not use raw Stitch export existence as fidelity proof.

2 native regenerated examples staged: Spotify and Linear. Neither has passed whole-page and responsive verification. Remaining 72 are not regenerated. 59 public reference source fetches succeeded, but metadata is not a visual review.

## Rebuild commands

```sh
python3 .stitch-work/current-official/refine-spotify.py
python3 .stitch-work/current-official/extend-spotify-tw.py
python3 .stitch-work/current-official/refine-linear.py
python3 .stitch-work/current-official/extend-linear.py
```

Spotify: Taiwan public page observed 2026-09-22T21:23:17Z at 1280×720 and saved in `spotify-tw-browser-reference.json`. All 54 observed card images, labels, destination links and Taiwan footer links are in the Stitch-derived preview. The five section headings match the current Taiwan page y positions within 0.01px (87, 437.789, 742.516, 1073.242, 1376.969). First viewport and footer were visually compared. Remaining: some typography and header icon details, final image loading while scrolling, interactions, and responsive checks. `extend-spotify-ca.py` is an obsolete Canada reference refinement retained for provenance.

Linear: the first viewport hero, observed issue copy and seven official SVG customer marks are staged. The app demo visuals and lower illustrations still differ substantially. Generated fictional metrics/people in feature sections must be replaced with observed official page content. Do not mark finished.

Raw `*-stitch.html` exports, native response JSON and request JSON are preserved separately from refined HTML. Original `spotify.png` and `linear-stitch.png` are raw Stitch screenshots, not screenshots of refined pages; never publish them as refined screenshots.

## Publication blocker

Existing Site project `appgprj_6ab202e80eb08191ab7ab27168509bf0` returns NOT_FOUND. Current Sites account resolved philqq101; production is philqq100. User has been asked to reconnect original account. No replacement Site may be created, and hosting manifest must be preserved.

No product-source integration, commit, source push, or public redeployment occurred in this rebuild. Existing catalog remains the old generated demonstrations. All current work is staged here pending Site source opening and fidelity verification.
