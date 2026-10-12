"""Pair retained Chrome source rasters with current root IAB rasters for review.

Scroll positions differ. Nearest source phases are labelled with their actual
positions; these contact sheets are not pixel-match evidence.
"""
from pathlib import Path
from PIL import Image, ImageDraw
import hashlib
import json
import sys

WORK = Path(__file__).resolve().parents[1] / '.stitch-work/current-official'
BRANDS = sys.argv[1:] or ['mongodb', 'kraken', 'coinbase']
assert set(BRANDS) <= {'mongodb', 'kraken', 'coinbase'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def gaps(frames):
    height = frames[-1]['bodyHeight']
    end = 0
    missing = []
    for frame in sorted(frames, key=lambda x: x['scrollY']):
        start = max(0, frame['scrollY'])
        if start > end + 1:
            missing.append([end, start])
        end = max(end, min(height, start + frame['viewport']['height']))
    if end < height - 1:
        missing.append([end, height])
    return missing


for brand in BRANDS:
    current = sha(WORK / f'{brand}.html')
    out = {'brand': brand, 'preview_sha256': current, 'accepted': False,
           'official_consistency_claim': False,
           'pairing_note': 'Each latest local phase is paired with the nearest retained official raster. Labelled scroll deltas and time/UA/browser differences prevent a pixel-equality claim.',
           'modes': {}}
    for mode, width in [('desktop', 1280), ('narrow', 390)]:
        source_name = f'{brand}-oct10-official-{mode}-slices.json'
        local_name = f'{brand}-oct10-local-{width}-phases.json'
        if not (WORK / local_name).exists():
            continue
        source = json.loads((WORK / source_name).read_text())
        local = json.loads((WORK / local_name).read_text())
        assert all(x.get('draft_sha256') == current for x in local), (brand, mode, 'stale hash')
        pairs = []
        for i, frame in enumerate(local):
            j = min(range(len(source)), key=lambda n: abs(source[n]['scrollY'] - frame['scrollY']))
            pairs.append({'local_index': i, 'official_index': j,
                          'local_scroll_y': frame['scrollY'], 'official_scroll_y': source[j]['scrollY'],
                          'scroll_delta': frame['scrollY'] - source[j]['scrollY'],
                          'local_screenshot': frame['screenshot'], 'official_screenshot': source[j]['file']})
        thumb_w = 512 if width == 1280 else 390
        thumb_h = round(local[0]['viewport']['height'] * thumb_w / width)
        per_sheet = 4 if width == 1280 else 2
        cols = 2 if width == 1280 else 1
        rows = (per_sheet + cols - 1) // cols
        sheets = []
        for old in WORK.glob(f'{brand}-oct10-latest-{width}-review-*.jpg'):
            old.unlink()
        for start in range(0, len(pairs), per_sheet):
            canvas = Image.new('RGB', (thumb_w * 2 * cols, (thumb_h + 38) * rows), 'white')
            draw = ImageDraw.Draw(canvas)
            for offset, pair in enumerate(pairs[start:start + per_sheet]):
                x = (offset % cols) * thumb_w * 2
                y = (offset // cols) * (thumb_h + 38)
                for side in ['official', 'local']:
                    sx = x + (thumb_w if side == 'local' else 0)
                    im = Image.open(WORK / pair[f'{side}_screenshot']).convert('RGB')
                    im.thumbnail((thumb_w, thumb_h))
                    canvas.paste(im, (sx, y + 38))
                    draw.text((sx + 4, y + 4), f"{brand} {side} #{pair[f'{side}_index']} y={pair[f'{side}_scroll_y']}\n" +
                              ('CURRENT hash' if side == 'local' else 'Retained actual source; nearest position'), fill='black')
            name = f'{brand}-oct10-latest-{width}-review-{start}.jpg'
            canvas.save(WORK / name, quality=95)
            sheets.append(name)
        # Include every official source phase in separate ordered sheets, so
        # nearest-neighbour pairing cannot silently omit any retained source.
        source_sheets = []
        for start in range(0, len(source), per_sheet):
            canvas = Image.new('RGB', (thumb_w * per_sheet, thumb_h + 38), 'white')
            draw = ImageDraw.Draw(canvas)
            for offset, frame in enumerate(source[start:start + per_sheet]):
                im = Image.open(WORK / frame['file']).convert('RGB')
                im.thumbnail((thumb_w, thumb_h))
                canvas.paste(im, (offset * thumb_w, 38))
                draw.text((offset * thumb_w + 4, 4), f"{brand} official #{start + offset}\ny={frame['scrollY']}", fill='black')
            name = f'{brand}-oct10-source-{width}-review-{start}.jpg'
            canvas.save(WORK / name, quality=95)
            source_sheets.append(name)
        out['modes'][mode] = {
            'source_records': source_name, 'local_records': local_name,
            'source_height': source[-1]['height'], 'local_height': local[-1]['bodyHeight'],
            'height_delta': local[-1]['bodyHeight'] - source[-1]['height'],
            'source_phases': len(source), 'local_phases': len(local),
            'uncovered_document_y_intervals': gaps(local),
            'all_phases_bound_to_current_hash': True,
            'visible_broken_image_candidates': sum(len(x['brokenVisibleImages']) for x in local),
            'horizontal_overflow_observed': any(x['bodyWidth'] > width for x in local),
            'pairs': pairs, 'diagnostic_contact_sheets': sheets,
            'all_official_phase_contact_sheets': source_sheets,
        }
    files = sorted({f for m in out['modes'].values()
                    for f in [m['source_records'], m['local_records'], *m['diagnostic_contact_sheets'],
                              *m['all_official_phase_contact_sheets']]})
    out['hashes'] = [{'path': name, 'sha256': sha(WORK / name)} for name in files]
    (WORK / f'{brand}-oct10-latest-layout-review.json').write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps({'brand': brand, 'sha256': current, 'modes': {mode: {k: v for k, v in m.items()
          if k not in ['pairs', 'diagnostic_contact_sheets', 'all_official_phase_contact_sheets']}
          for mode, m in out['modes'].items()}}))
