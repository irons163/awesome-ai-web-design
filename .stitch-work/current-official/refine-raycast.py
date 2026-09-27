#!/usr/bin/env python3
"""Build the Raycast dated draft from the preserved native Stitch screen.

The official site's live Three.js hero and responsive page still require
visual comparison. This output is not a pixel-accepted replica.
"""
from pathlib import Path

root = Path(__file__).resolve().parent
raw = (root / 'raycast-stitch.html').read_text()
for phrase in ('Your shortcut to everything.', 'Take shortcuts, not detours.',
               'There’s an extension for that.', 'Meet your new virtual assistant'):
    assert phrase in raw, phrase
assets = root / 'raycast-assets'
for name in ('raycast-wordmark.svg', 'feature-background.webp', 'favicon.png',
             'linear-icon.webp', 'linear-preview.webp', 'spotify-icon.webp',
             'spotify-preview.webp', 'slack-icon.webp', 'slack-preview.webp'):
    assert (assets / name).is_file(), name
template = (root / 'raycast-refined-template.html').read_text()
for phrase in ('Your shortcut to everything.', 'Take shortcuts, not detours.',
               'It’s not about saving time.', 'There’s an extension for that.',
               'Take the short way.'):
    assert phrase in template, phrase
for invention in ('v1.75', 'macOS 12+', '0ms latency overhead',
                  'Claude 3.5 Sonnet', 'GPT-4o', 'Lorem ipsum', 'href="#"'):
    assert invention not in template, invention
(root / 'raycast.html').write_text(template)
print('Wrote Raycast dated draft from Stitch screen and observed public assets')
