# spotify — genuine Stitch generation, October 10

這是 Google Stitch 原始回覆與建議，完整保存供查核。下列「忠實」「精準」等敘述是生成工具的自述，並非驗收結果；校正草稿與原始生成檔分開保存。本輪未宣稱與官網完全一致。

Native screen: `projects/17774991018148174598/screens/1ea901ffa37346e7a6dd1610f68f3d00`

Prompt: `spotify-stitch-oct10-desktop-prompt.md`

## Provider output (verbatim)

I have faithfully reconstructed the signed-out Taiwan Spotify desktop web player at 1280×720 based on your exact measured layout, typography specifications, and content inventory:

### Architecture & Precision Layout
1. **Global Navigation Bar (64px)**:
   - Spotify wordmark vector mark, circular Home button, search input with keyboard command indicator (`⌘ShiftL`), and header links (`Premium`, `Support`, `Download`, `Install App`).
   - White pill "Log in" and "Sign up" free buttons directing to the official Spotify authentication services.
2. **Library Panel (x: 8px, y: 64px, w: 320px, h: 574px)**:
   - "Your Library" header with plus action icon.
   - Dual onboarding callouts ("Create your first playlist" and "Let's find some podcasts to follow").
   - Legal links and localized `English` language selection pill button.
3. **Independently Scrolling Main Panel (x: 336px, y: 64px, w: 936px, h: 574px)**:
   - Restrained dark top gradient (`#1e1e1e` fading into `#121212`).
   - Authentic `SpotifyMixUITitle` (24px/700) section headers and `SpotifyMixUI` body font sources.
   - All **5 ordered content shelves** populated with all 54 observed cards, real cover artwork, circular artist crops, and active hover green play pills:
     - **Trending songs**: 20 tracks (G.E.M., ALLDAY PROJECT, Ronghao Li & A-Mei Chang, BIGBANG, Bestards, ADÉLA, etc.)
     - **Popular artists**: 10 artists with circular portrait masks (Jay Chou, Stefanie Sun, Mayday, JOLIN, LBI利比, JJ Lin, Eason Chan, ROSÉ, Eric Chou, Bestards)
     - **Popular albums and singles**: 10 release cards (Ruby, HAPPY BURSTDAY, rosie, 电视剧《难哄》, Übermensch, etc.)
     - **Popular radio**: 10 station cards with real radio metadata
     - **Featured Charts**: Top Songs & Top 50 (Global and Taiwan)
   - Comprehensive footer directory covering Company, Communities, Useful links, Spotify Plans, social icons, and copyright.
4. **Persistent Preview Strip (x: 8px, y: 646px, w: 1264px, h: 66px)**:
   - Exact purple-to-blue gradient (`#af2896` to `#509bf5`) with uppercase eyebrow and "Sign up free" pill CTA.

## Provider suggestions (not accepted automatically)

- Inspect interactive play hover states on album cards
- Test custom scroll behavior on library vs main panels
- Simulate search bar expansion or focus state
