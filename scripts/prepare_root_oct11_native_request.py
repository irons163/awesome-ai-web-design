"""Prepare an exact, reviewable native request from captured public reference data."""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

class VisibleText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
    def handle_data(self, data):
        if data.strip():
            self.parts.append(data.strip())

slug, label, url, project, screen, device = sys.argv[1:7]
work = Path('.stitch-work/current-official')
intro = Path(sys.argv[7]).read_text() if len(sys.argv) > 7 else ''
observed_dates = sorted({frame['observed_at'][:10] for width in [1280, 390]
                         for frame in json.loads((work / f'{slug}-oct10-official-{width}-phases.json').read_text())})
prompt = f'''Reproduce the current public {label} homepage at {url}, actually observed on {', '.join(observed_dates)} UTC, as an unofficial reference study. Preserve the actual locale, content, section order, original brand typography, imagery, colours and footer. Generate the complete {device} page; target 390px wide for MOBILE and 1280px wide for DESKTOP. Implement responsive HTML/CSS with no paid dependencies. Do not invent statistics, offers, photos, copy or customer stories. Do not fake transactions, sign-in, account data or official service outcomes. Native generation is an initial study, not proof of official fidelity. Dynamic timing, other carousel states and service interactions remain unverified.\n\n{intro}\n'''
for width in [1280, 390]:
    ref = json.loads((work / f'{slug}-oct10-official-{width}-reference.json').read_text())
    html = ''.join(ref['htmlParts'])
    section = re.search(r'<main\b[\s\S]*?</main>', html)
    markup = section.group() if section else html
    markup = re.sub(r'<(script|style|noscript)\b[\s\S]*?</\1>', '', markup)
    text = VisibleText()
    text.feed(markup)
    frames = json.loads((work / f'{slug}-oct10-official-{width}-phases.json').read_text())
    prompt += f'\nActual {width}px reference, height {frames[-1]["bodyHeight"]}px. Main copy:\n' + ' '.join(text.parts)[:11000] + '\n'
    headings = [{k: h[k] for k in ['text', 'box', 'font', 'size', 'weight', 'lineHeight']} for h in frames[0]['headings']]
    prompt += '\nMeasured heading hierarchy, positions and type:\n' + json.dumps(headings, ensure_ascii=False) + '\n'
assets = json.loads((work / f'{slug}-oct10-assets.json').read_text())['assets']
tracking = re.compile(r'analytics|collect|doubleclick|googlead|facebook\.com/tr|googletagmanager|/pixel|segment\.com|adsct|scorecard|audience|t\.co/|snapchat|bat\.bing|tags\.srv|tr\.line|posthog|/pagead/|linkedin\.com/(?:px|insight)', re.I)
private_query = re.compile(r'(?:[?&])(?:[^=&]*(?:session|visitor|token|signature|auth|credential)|cid|uid|gclid|fbclid|_gl|af_sub1)=', re.I)
urls = sorted({a['source_url'] for a in assets if a['source_url'].startswith('https://') and not tracking.search(a['source_url']) and not private_query.search(a['source_url'])})
prompt += '\nAlready observed public original asset URLs; use original imagery rather than invented substitutions:\n' + '\n'.join(urls[:180])
request = {'projectId': project, 'selectedScreenIds': [screen], 'deviceType': device, 'prompt': prompt}
(work / f'{slug}-oct10-reproduction-prompt.md').write_text(prompt)
(work / f'{slug}-oct10-stitch-edit-request.json').write_text(json.dumps(request, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(request, ensure_ascii=False))
