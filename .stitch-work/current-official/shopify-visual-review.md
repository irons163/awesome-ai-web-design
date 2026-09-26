# Shopify Canada reconstruction review

- Current reference: https://www.shopify.com/ca, inspected in the in-app browser at 1280 × 720 on 2026-09-27 (Taipei time).
- Supplementary saved HTML: `shopify-source.html`, observed 2026-09-22. It supplied the below-fold text and link inventory. The current browser showed the same major heading hierarchy, but the hero visibly rotates text and video frames.
- Native Stitch: `shopify-stitch.html` and `shopify-stitch.png`. All five requested official images became generic Stitch placeholders. Stitch also invented an AI product price, 14,200 analyzed orders, a 99.99% uptime claim, unsupported CTA copy, and several historical footer links.
- Refined draft: `shopify.html`. `refine-shopify.py` replaces placeholders with eight saved official assets, restores the current Canada navigation and footer links, replaces fabricated below-fold copy with current browser text, and uses the official sweater/chat poster for the large teal card.

## Directly observed visual reference

The official page had a fixed 72px translucent header, with the white Shopify logo about 90px from the left edge. At the first captured hero frame, “Be the next solo-preneur” appeared as thin white display text over full-bleed documentary video; its accessible fallback read “Be the next AI all-star.” The display type measured 96px. Body copy and two pill actions sat below. The hero image/video occupied roughly 1280 × 878px at this desktop width.

The following near-black section started with a large rounded top edge and four oversized progressive lines about where people shop. Further down, the browser showed three merchant screenshot tiles and a 1100px-wide dark teal Agentic Storefronts panel with ChatGPT/Google/Copilot marks on the left and a sweater/chat-input animation on the right.

## Outstanding acceptance work

- The refined draft itself has not been visually compared to the current official site. The earlier browser security decision rejected opening a local `file://` draft; it must not be reattempted through another browser surface or localhost workaround.
- Hero film playback and rotating headline are approximated by an official still and one captured headline frame.
- Below-fold sections, 390px/768px layouts, navigation menus, video action, and footer interaction still need direct visual and behavioral review.
- Shopify's public page can vary by region, animation frame, and time. This record is specific to the Canada route and observation time.
