"""Create labelled review overviews from preserved actual browser screenshots."""
from pathlib import Path
from PIL import Image, ImageDraw
import hashlib
import json

work = Path(__file__).resolve().parents[1] / '.stitch-work/current-official'
for brand in ['ibm', 'mongodb', 'intercom', 'superhuman', 'kraken', 'coinbase']:
    pairs = []
    current = hashlib.sha256((work / f'{brand}.html').read_bytes()).hexdigest()
    for mode in ['desktop', 'narrow']:
        panels = []
        for role in ['official', 'local']:
            width = 1280 if mode == 'desktop' else 390
            newest = work / f'{brand}-oct10-{role}-{width}-phases.json'
            phases = role == 'local' and newest.exists()
            frames = json.loads((newest if phases else work / f'{brand}-oct10-{role}-{mode}-slices.json').read_text())
            width, height = frames[0]['viewport']['width'], round(frames[-1]['bodyHeight' if phases else 'height'])
            canvas = Image.new('RGB', (width, height), '#eee')
            covered = 0
            for frame in frames:
                image = Image.open(work / frame['screenshot' if phases else 'file']).convert('RGB')
                y = round(frame['scrollY'])
                overlap = max(0, covered - y)
                if overlap < image.height:
                    canvas.paste(image.crop((0, overlap, image.width, image.height)), (0, y + overlap))
                    covered = max(covered, y + image.height)
            display_width = 384 if mode == 'desktop' else 195
            canvas = canvas.resize((display_width, round(height * display_width / width)))
            panel = Image.new('RGB', (display_width, canvas.height + 54), 'white')
            state = 'source' if role == 'official' else ('current hash' if all(
                x.get('draft_sha256') == current for x in frames) else 'PRIOR REVISION')
            ImageDraw.Draw(panel).text((5, 4), f'{brand} {role} {mode}\nheight {height}; {state}', fill='black')
            panel.paste(canvas, (0, 54))
            panels.append(panel)
        pair = Image.new('RGB', (sum(x.width for x in panels) + 8, max(x.height for x in panels)), '#ccc')
        x = 0
        for panel in panels:
            pair.paste(panel, (x, 0))
            x += panel.width + 8
        pairs.append(pair)
    overview = Image.new('RGB', (sum(x.width for x in pairs) + 12, max(x.height for x in pairs)), '#ddd')
    x = 0
    for pair in pairs:
        overview.paste(pair, (x, 0))
        x += pair.width + 12
    overview.save(work / f'{brand}-oct10-comparison-overview.png')
    print(brand, overview.size)
