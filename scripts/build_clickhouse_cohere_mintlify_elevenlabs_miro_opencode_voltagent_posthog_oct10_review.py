"""Hash-bound actual source/local comparison sheets, including internal scroll."""
from pathlib import Path
from PIL import Image, ImageDraw
import hashlib
import json
import sys

WORK = Path(__file__).resolve().parents[1] / '.stitch-work/current-official'
ALLOWED = {'clickhouse', 'cohere', 'mintlify', 'elevenlabs', 'miro', 'opencode.ai', 'voltagent', 'posthog'}
brands = sys.argv[1:] or sorted(ALLOWED)
assert set(brands) <= ALLOWED


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def position(frame):
    return frame['coverage']['offset'] if frame.get('coverage', {}).get('coordinate_space') == 'element_scroll' else frame['scrollY']


def extent(frame):
    return frame['coverage']['extent'] if frame.get('coverage', {}).get('coordinate_space') == 'element_scroll' else frame['bodyHeight']


def gaps(frames):
    total, covered, missing = extent(frames[-1]), 0, []
    for frame in sorted(frames, key=position):
        start = max(0, position(frame))
        visible = frame['coverage']['visible_extent'] if 'coverage' in frame else frame['viewport']['height']
        if start > covered + 1:
            missing.append([covered, start])
        covered = max(covered, min(total, start + visible))
    if covered < total - 1:
        missing.append([covered, total])
    return missing


for brand in brands:
    current = sha(WORK / f'{brand}.html')
    out = {'brand': brand, 'preview_sha256': current, 'accepted': False, 'official_consistency_claim': False,
           'pairing_note': 'Every current local phase is paired to the nearest actual official offset. Actual offsets are labelled. Equal extents/zero broken-image candidates do not imply pixel or motion parity.',
           'modes': {}}
    for width, height, mode in [(1280, 720, 'desktop'), (390, 844, 'narrow')]:
        local_name = f'{brand}-oct10-local-{width}-phases.json'
        source_name = f'cohere-reduced-oct10-official-{width}-phases.json' if brand == 'cohere' else f'{brand}-oct10-official-{width}-phases.json'
        if not (WORK / local_name).exists():
            continue
        source = json.loads((WORK / source_name).read_text())
        local = json.loads((WORK / local_name).read_text())
        assert all(f.get('draft_sha256') == current for f in local), (brand, width, 'stale local capture')
        assert all(Image.open(WORK / f['screenshot']).size == (width, height) for f in source + local), (brand, width, 'incorrect physical capture dimensions')
        nested = local[0].get('coverage', {}).get('coordinate_space') == 'element_scroll'
        assert nested == (source[0].get('coverage', {}).get('coordinate_space') == 'element_scroll')
        pairs = []
        for index, frame in enumerate(local):
            official_index = min(range(len(source)), key=lambda n: abs(position(source[n]) - position(frame)))
            pairs.append({'local_index': index, 'official_index': official_index,
                          'local_offset': position(frame), 'official_offset': position(source[official_index]),
                          'offset_delta': position(frame) - position(source[official_index]),
                          'local_screenshot': frame['screenshot'], 'official_screenshot': source[official_index]['screenshot']})
        thumb_width = 512 if width == 1280 else 390
        thumb_height = round(height * thumb_width / width)
        per_sheet = 4 if width == 1280 else 2
        columns = 2 if width == 1280 else 1
        rows = (per_sheet + columns - 1) // columns
        sheets = []
        for start in range(0, len(pairs), per_sheet):
            canvas = Image.new('RGB', (thumb_width * 2 * columns, (thumb_height + 38) * rows), 'white')
            draw = ImageDraw.Draw(canvas)
            for offset, pair in enumerate(pairs[start:start + per_sheet]):
                x = offset % columns * thumb_width * 2
                y = offset // columns * (thumb_height + 38)
                for side in ['official', 'local']:
                    sx = x + (thumb_width if side == 'local' else 0)
                    im = Image.open(WORK / pair[f'{side}_screenshot']).convert('RGB')
                    im.thumbnail((thumb_width, thumb_height))
                    canvas.paste(im, (sx, y + 38))
                    label = f"{brand} {side} #{pair[f'{side}_index']} offset={pair[f'{side}_offset']}"
                    detail = f'CURRENT {current[:12]}' if side == 'local' else 'Actual source; nearest offset'
                    draw.text((sx + 4, y + 4), label + '\n' + detail, fill='black')
            name = f'{brand}-oct10-latest-{width}-review-{current[:8]}-{start}.jpg'
            canvas.save(WORK / name, quality=96)
            sheets.append(name)
        out['modes'][mode] = {
            'source_records': source_name, 'local_records': local_name,
            'coordinate_space': 'element_scroll' if nested else 'document_scroll',
            'source_extent': extent(source[-1]), 'local_extent': extent(local[-1]),
            'extent_delta': extent(local[-1]) - extent(source[-1]),
            'source_phases': len(source), 'local_phases': len(local),
            'coverage_gaps': gaps(local), 'all_local_phases_bound_to_current_hash': True,
            'visible_broken_image_candidates': max(len(f.get('brokenVisibleImages', [])) for f in local),
            'horizontal_document_overflow_observed': any(f['bodyWidth'] > width for f in local),
            'pairs': pairs, 'diagnostic_contact_sheets': sheets,
        }
    files = sorted({name for mode in out['modes'].values()
                    for name in [mode['source_records'], mode['local_records'], *mode['diagnostic_contact_sheets'],
                                 *[p[k] for p in mode['pairs'] for k in ['official_screenshot', 'local_screenshot'] if k in p]]})
    out['hashes'] = [{'path': name, 'sha256': sha(WORK / name)} for name in files]
    (WORK / f'{brand}-oct10-latest-layout-review.json').write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps({'brand': brand, 'preview_sha256': current,
                      'modes': {mode: {k: value for k, value in data.items() if k not in ['pairs', 'diagnostic_contact_sheets']}
                                for mode, data in out['modes'].items()}}))
