# Scoped actual visual review

Reference: https://www.tesla.com/

Reviewed preview SHA-256: a58cc012a7358feea5951bb94ea4cb2226b0a2a1222f89634c33d04bea7ebc64

Actual desktop and390px narrow homepage screenshots were compared across complete scroll coverage. Existing screenshot dimensions and current preview hash were rechecked when normalizing this record. This records a completed scoped visual review; accepted=false and official_consistency_claim=false.

- Hero autoplay is not synchronized with the live official rotation. Manual Model Y/Model 3 dot changes were visibly exercised.
- FSD mileage counter is frozen to observed captured values. Official live mileage and network counts continue changing.
- FSD video uses the exact public official source; screenshot video time differs. Playback, network conditions and browser native video controls are not synchronized.
- Map is a source-captured static illustration with fully loaded official tiles and observed markers; zoom, geolocation, find-me and live network backend are not implemented.
- Desktop menu captureBeyondViewport composition paints some official inactive opacity-zero panels on top of the active panel. Local preview explicitly hides inactive panels. This compositor ambiguity prevents an official pixel-equality claim for desktop menu screenshots.
- Mobile root/Vehicles menus, desktop Vehicles hover and Escape, and hero Model 3/Model Y dot controls were exercised. Other menu branches, region chooser and horizontal product/energy carousel states have not all been visually verified.
- Scroll-driven header/chat/sticky transitions and exact animation timing remain scoped differences. Account, chat, demo scheduling, ordering and authenticated/backend services stay on official destinations.
- Hosted deployment and widths/devices beyond the recorded two scopes await root integration and verification.

## Legacy capture binding audit (2026-10-12 Taipei)

Legacy capture records do not contain a capture-time preview SHA-256. Association with the current unchanged preview is supported by preserved completion/build/hash records and the owner visual review, rather than an independently recorded per-capture digest. The 2026-10-12 provenance audit does not backdate hashes or constitute a new browser review.

Current preview SHA-256 `a58cc012a7358feea5951bb94ea4cb2226b0a2a1222f89634c33d04bea7ebc64` matches the preserved pre-audit completion record and build/manifest record. All 13 canonical local viewport rasters and their metadata retain their historical recorded hashes and actual dimensions. The original phase records are unchanged. Exact files, preserved record snapshots, and the audit timestamp are in [tesla-oct12-capture-binding-audit.json](tesla-oct12-capture-binding-audit.json).
