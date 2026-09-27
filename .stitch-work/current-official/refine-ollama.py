#!/usr/bin/env python3
"""Refine the native Stitch output against observed Ollama public content.

This builds a dated draft, not a visually accepted replica.
"""
from html import escape
from pathlib import Path

root = Path(__file__).resolve().parent
raw = (root / 'ollama-stitch.html').read_text()
for phrase in ('Run open models', 'Get more usage', 'Reliably fast'):
    assert phrase in raw, phrase
assets = root / 'ollama-assets'
logos = ('apple', 'nike', 'microsoft', 'meta', 'nasa', 'netflix', 'nvidia',
         'adobe', 'ibm', 'bmw', 'mercedes', 'intel', 'volvo', 'salesforce',
         'databricks', 'intuit', 'mit', 'walmart', 'visa')
for name in (*[f'{x}.svg' for x in logos], 'ollama.png', 'hero-poster.jpg',
             'claude.png', 'codex-app.png', 'opencode.png', 'openclaw.svg',
             'hermes.png', 'vscode.svg', 'pi.svg', 'n8n.png',
             'openai.svg', 'anthropic.svg', 'kimi.svg', 'deepseek.svg'):
    assert (assets / name).is_file(), name
template = (root / 'ollama-refined-template.html').read_text()
logo_html = ''.join(
    f'<img src="ollama-assets/{name}.svg" alt="{escape(name.title())}" loading="lazy">'
    for name in logos
)
assert '{{LOGOS}}' in template
html = template.replace('{{LOGOS}}', logo_html)
for phrase in ('Run open models.', 'Get more usage.', 'Frontier open models',
               'Your data stays yours', 'Predictable pricing'):
    assert phrase in html, phrase
for invention in ('Lorem ipsum', 'example@', '99.9% uptime'):
    assert invention not in html, invention
(root / 'ollama.html').write_text(html)
print('Wrote ollama.html from Stitch-derived, source-corrected template')
