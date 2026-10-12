# NVIDIA visual review

Final preview SHA256: `fb65933b23541f659010abd673e3b0cbf604acaa5cbdd208ec61cd76e7b3182b`.

Owner inspected all seven final comparison montage rasters (11 desktop /13 narrow viewport segments per side) and the actual official/local mobile root menu. Exact native raster dimensions1280×720 and390×844; continuous CSS coverage reaches desktop7233px and narrow10350px in both sides. Current first hero image/copy, GTC band, eight industry rows, current article images/copy, footer and root menu were compared. The narrow official first-frame image has a darker transitional fade than the static local frame. Native provider screen thumbnails were inspected and remain unaccepted; generated ordering/theme differ from the current official first slide.

Coverage and actual original raster dimensions are recorded in the result JSON. CSS viewport coverage and raster pixel resolution are separate measurements. Uniformly scaled originals are retained unaltered; comparison montages may normalize viewing widths. Cropped or stale compositor diagnostics are excluded.

Remaining differences and limits:

- Official six-slide hero autoplays every7s. Local first slide, progress fill and content-row positions are frozen; remaining slide selection, autoplay, transitions and horizontal navigation are not fully implemented/verified.
- The captured narrow official first hero is a darker transition frame; local static image is brighter. Exact transition opacity/time and native scrollbar/focus-ring appearance are not matched.
- Only narrow root menu opening and Escape closing were tested. Nested menus, desktop menus, country selector, search, sign-in, quick links and other interactions remain unverified.
- Official US page showed a Taiwan geolocation recommendation; initial banner was recorded then dismissed. Main evidence retains exact en-us URL without claiming Taiwan/other regional equivalence.
- Native provider output does not reproduce the current first-slide theme/order precisely and stays unaccepted. No account, purchase, subscription, live service, other widths, physical phone or hosted-publication parity is claimed.
