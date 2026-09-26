# Slack official homepage reconstruction review

- Current reference: https://slack.com/, observed in the in-app browser at 1280 × 720 on 2026-09-27 (Taipei time). The saved `slack-source.html` is a separate 2026-09-22 snapshot.
- Native Google Stitch output: `slack-stitch.html` and `slack-stitch.png`, screen `projects/17824255204710655771/screens/7f6a2c8e0176450789d97b372cc05b5e`.
- Stitch got the high-level page hierarchy but used a generic placeholder for the Slack logo and the AI interface. It rendered the real hero video URL but offered static tabs. The news cards, product copy, footer links and several details were invented or inactive.
- `refine-slack.py` keeps the native output for traceability and writes `slack.html`. It replaces the placeholders with official assets saved from the live page, uses the actual Slack typefaces, restores current public copy and links, switches between five real hero videos and six official AI stills, and removes unsupported product descriptions. The additional Knowledge/People/Process/Platform sections use source-backed text and images.

## Directly observed desktop reference

The first viewport has a 48px pale lavender announcement, an 80px white navigation, and a centered 64px black headline around x198/y190. The subtitle and two square-ish actions follow. Six monochrome customer marks sit above the first real Slack application video, which begins around x240/y553 and is about 800px wide. The next large section is deep aubergine, with a centered white heading and six actions beside a Slack interface image.

## Outstanding acceptance work

- The refined draft has **not** been visually compared to the official page. A previous automatic browser safety decision rejected opening a local `file://` draft, and this work did not retry through localhost, another browser, or the public deployment. Do not call this pixel identical.
- Full-page spacing, animation timing, all five news carousel states, AI video playback, navigation/search behaviors, and 390px/768px layouts still need direct visual and behavioral comparison.
- The official homepage can vary with region, time and animation frame. This draft is explicitly dated.
