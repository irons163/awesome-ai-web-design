#!/usr/bin/env python3
"""Produce a dated Resend draft from the Stitch screen and observed public assets.

The raw Stitch output remains beside this script. This removes unsupported
Stitch inventions; it does not certify desktop or mobile visual equivalence.
"""
from pathlib import Path
import re

root = Path(__file__).resolve().parent
raw = (root / 'resend-stitch.html').read_text()
for phrase in ('Email for', 'Integrate this weekend', 'Beyond expectations'):
    assert phrase in raw, phrase
template = (root / 'resend-refined-template.html').read_text()
visible = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', template))
for phrase in ('Join us at Resend Forward', 'Email for', 'Integrate this weekend',
               'First-class', 'Email reimagined.'):
    assert phrase in visible, phrase
for invention in ('Guillermo Rauch', 'Peer Richelsen', 'Shu Ding',
                  '42,850 developers', '99.8%'):
    assert invention not in template, invention
assets = root / 'resend-assets'
for name in ('logo.svg', 'domaine-regular.woff2', 'favorit-book.woff2',
             'inter-variable.woff2', 'commit-mono.woff2', 'cube.mp4',
             'cube-fallback.jpg', 'bg-hero-1.jpg', 'bg-light.png',
             'integrate-fallback.jpg', 'broadcast-fallback.jpg',
             'react-fallback.jpg', 'control-fallback.jpg',
             'broadcast-email-header.jpg', 'screenshot-zoom-audience.png',
             'screenshot-zoom-analytics.png', 'screenshot-metrics.png'):
    assert (assets / name).is_file(), name
(root / 'resend.html').write_text(template)
print('Wrote resend.html from Stitch-derived, source-corrected template')
