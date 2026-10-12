"""Contact sheets of assigned actual source phases; no acceptance inference."""
from pathlib import Path
from PIL import Image, ImageDraw
import json
import hashlib
import sys

WORK = Path(__file__).resolve().parents[1] / '.stitch-work/current-official'
allowed = {'clickhouse', 'cohere', 'mintlify', 'elevenlabs', 'miro', 'opencode.ai', 'voltagent', 'posthog'}
brands = ['posthog']
assert set(brands) <= allowed
for brand in brands:
    out = {'brand': brand, 'accepted': False, 'official_consistency_claim': False,
           'purpose': 'Derived diagnostic overview of every retained actual official browser phase; does not assert a local match.', 'modes': {}}
    for width in (1280, 390):
        records_name = f'{brand}-oct10-official-{width}-phases.json'
        if not (WORK / records_name).exists(): continue
        records = json.loads((WORK / records_name).read_text())
        thumb_w = 384 if width == 1280 else 195
        thumb_h = round(records[0]['viewport']['height'] * thumb_w / width)
        outputs = []
        for start in range(0, len(records), 8):
            canvas = Image.new('RGB', (thumb_w * 4, (thumb_h + 34) * 2), 'white')
            draw = ImageDraw.Draw(canvas)
            for offset, record in enumerate(records[start:start + 8]):
                x = offset % 4 * thumb_w
                y = offset // 4 * (thumb_h + 34)
                name = record.get('screenshot') or f'{brand}-oct10-official-{width}-phase-{start + offset}.png'
                im = Image.open(WORK / name).convert('RGB')
                im.thumbnail((thumb_w, thumb_h))
                canvas.paste(im, (x, y + 34))
                draw.text((x + 4, y + 3), f"{brand} official{width} #{start + offset}\nregion={record['coverage']['offset']}", fill='black')
            name = f'{brand}-oct10-official-{width}-complete-contact-{start}.jpg'
            canvas.save(WORK / name, quality=96)
            outputs.append({'path': name, 'sha256': hashlib.sha256((WORK / name).read_bytes()).hexdigest()})
        out['modes'][str(width)] = {'phase_records': records_name, 'phases': len(records),
                                  'coordinate_space': 'element_scroll', 'region_extent': records[-1]['coverage']['extent'], 'contact_sheets': outputs}
    (WORK / f'{brand}-oct10-official-complete-contact-sheets.json').write_text(json.dumps(out, indent=2) + '\n')
    print(brand, {k: v['phases'] for k, v in out['modes'].items()})
