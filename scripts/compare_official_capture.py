"""Compare dated, actual viewport captures; contact sheets are diagnostic only."""
import json
import sys
from pathlib import Path
from PIL import Image, ImageDraw

slug = sys.argv[1]
source_slug = sys.argv[2] if len(sys.argv) > 2 else slug
work = Path('.stitch-work/current-official')
result = {}
def position(record):
    return record.get('coverage', {}).get('offset', record.get('scrollY', record.get('y', 0)))

def extent(record):
    return record.get('coverage', {}).get('extent', record['bodyHeight'])

for width in (1280, 390):
    source = json.loads((work / f'{source_slug}-oct10-official-{width}-phases.json').read_text())
    local = json.loads((work / f'{slug}-oct10-local-{width}-phases.json').read_text())
    differences = []
    by_text = {}
    for heading in local[0]['headings']:
        by_text.setdefault(heading['text'], []).append(heading)
    unmatched = []
    for i, a in enumerate(source[0]['headings']):
        matches = by_text.get(a['text'], [])
        if not matches:
            unmatched.append(a['text'])
            continue
        b = matches.pop(0)
        for key in ('text', 'font', 'size', 'weight', 'lineHeight', 'color'):
            if a[key] != b[key]:
                differences.append({'heading': i, 'property': key, 'official': a[key], 'local': b[key]})
        a_box, b_box = a.get('regionBox', a['box']), b.get('regionBox', b['box'])
        for key in ('x', 'y', 'width', 'height'):
            if abs(a_box[key] - b_box[key]) > 0.1:
                differences.append({'heading': i, 'property': key, 'official': a_box[key], 'local': b_box[key]})
    if len(source[0]['headings']) != len(local[0]['headings']):
        differences.append({'property': 'heading_count', 'official': len(source[0]['headings']), 'local': len(local[0]['headings'])})
    thumb_w = 384 if width == 1280 else 195
    thumb_h = round(source[0]['viewport']['height'] * thumb_w / width)
    sheets = []
    # Smooth scrolling can produce repeated phases. Pair actual scroll positions,
    # not ordinal indexes, and show unpaired local coverage at the end.
    used = set()
    pairs = []
    for source_index, record in enumerate(source):
        source_position = position(record)
        candidates = [(abs(position(item) - source_position), index)
                      for index, item in enumerate(local)]
        distance, local_index = min(candidates)
        if distance <= 2:
            used.add(local_index)
            pairs.append((source_index, local_index))
        else:
            pairs.append((source_index, None))
    pairs.extend((None, index) for index in range(len(local)) if index not in used)
    for old in work.glob(f'{slug}-oct10-comparison-{width}-*.jpg'):
        old.unlink()
    for start in range(0, len(pairs), 4):
        sheet = Image.new('RGB', (thumb_w * 4, (thumb_h + 28) * 2), 'white')
        draw = ImageDraw.Draw(sheet)
        for offset in range(4):
            pair_index = start + offset
            if pair_index >= len(pairs):
                continue
            x = (offset % 2) * thumb_w * 2
            y = (offset // 2) * (thumb_h + 28)
            for side_index, (side, records) in enumerate((('official', source), ('local', local))):
                phase = pairs[pair_index][side_index]
                if phase is None:
                    continue
                image_path = work / records[phase].get('screenshot', f'{slug}-oct10-{side}-{width}-phase-{phase}.png')
                image = Image.open(image_path).convert('RGB')
                expected = (records[phase]['viewport']['width'], records[phase]['viewport']['height'])
                mapped = records[phase].get('actual_raster_dimensions', {})
                scale = image.width / expected[0]
                proportional = (records[phase].get('raster_mapping') == 'proportional_full_viewport'
                                and (mapped.get('width'), mapped.get('height')) == image.size
                                and 0.9 <= scale <= 1 and abs(image.height - expected[1] * scale) <= 1)
                if image.size != expected and not proportional:
                    raise ValueError(f'Actual screenshot does not cover declared viewport: {image_path.name}: {image.size} != {expected}')
                image.thumbnail((thumb_w, thumb_h))
                sheet.paste(image, (x + thumb_w * side_index, y + 28))
                draw.text((x + thumb_w * side_index + 4, y + 4), f"{side} phase {phase}, y={position(records[phase])}", fill='black')
        output = work / f'{slug}-oct10-comparison-{width}-{start}.jpg'
        sheet.save(output, quality=94)
        sheets.append(output.name)
    result[str(width)] = {
        'officialHeight': extent(source[-1]), 'localHeight': extent(local[-1]),
        'coverageCoordinateSpace': source[-1].get('coverage', {}).get('coordinate_space', 'document_scroll'),
        'officialDocumentHeight': source[-1]['bodyHeight'], 'localDocumentHeight': local[-1]['bodyHeight'],
        'officialPhases': len(source), 'localPhases': len(local),
        'matchedScrollPositions': sum(a is not None and b is not None for a, b in pairs),
        'unpairedOfficialPhases': [a for a, b in pairs if a is not None and b is None],
        'unpairedLocalPhases': [b for a, b in pairs if a is None and b is not None],
        'headingCount': len(source[0]['headings']), 'headingDifferences': differences,
        'unmatchedOfficialHeadingTexts': unmatched,
        'unmatchedLocalHeadingTexts': [h['text'] for items in by_text.values() for h in items],
        'visibleBrokenImages': sum(len(x['brokenVisibleImages']) for x in local),
        'overflow': any(x['bodyWidth'] > width for x in local),
        'diagnosticContactSheets': sheets,
        'caveat': 'Geometry is supporting evidence only. Inspect actual screenshots before recording any visual conclusion.'
    }
(work / f'{slug}-oct10-layout-comparison.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({width: {k: v for k, v in value.items() if k not in ('headingDifferences', 'caveat', 'unmatchedOfficialHeadingTexts', 'unmatchedLocalHeadingTexts')} | {'headingDifferenceCount': len(value['headingDifferences']), 'unmatchedOfficialCount': len(value['unmatchedOfficialHeadingTexts']), 'unmatchedLocalCount': len(value['unmatchedLocalHeadingTexts'])} for width, value in result.items()}, indent=2))
