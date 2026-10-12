"""Create labelled contact sheets from saved, unmodified official viewport images."""
from pathlib import Path
import json
import sys
from PIL import Image, ImageDraw

WORK = Path(__file__).resolve().parents[1] / '.stitch-work/current-official'
for slug in sys.argv[1:]:
    output = []
    for width in (1280, 390):
        frames = json.loads((WORK / f'{slug}-oct10-official-{width}-phases.json').read_text())
        tw, th, cols = (640, 360, 2) if width == 1280 else (390, 844, 4)
        for start in range(0, len(frames), 4):
            group = frames[start:start + 4]
            rows = (len(group) + cols - 1) // cols
            sheet = Image.new('RGB', (cols * tw, rows * (th + 30)), '#eeeeee')
            draw = ImageDraw.Draw(sheet)
            for k, frame in enumerate(group):
                image = Image.open(WORK / frame['screenshot']).convert('RGB')
                if image.size != (frame['viewport']['width'], frame['viewport']['height']):
                    raise ValueError(f'Incorrect actual screenshot dimensions: {frame["screenshot"]}: {image.size}')
                image.thumbnail((tw, th))
                x, y = (k % cols) * tw, (k // cols) * (th + 30)
                offset = frame.get('coverage', {}).get('offset', frame['scrollY'])
                axis = 'element-y' if frame.get('coverage', {}).get('coordinate_space') == 'element_scroll' else 'y'
                draw.text((x + 8, y + 8), f'{slug} official {width}px phase{start+k} {axis}={offset}', fill='black')
                sheet.paste(image, (x, y + 30))
            name = f'{slug}-oct11-official-{width}-contact-{start}.jpg'
            sheet.save(WORK / name, quality=90)
            output.append(name)
    (WORK / f'{slug}-oct11-official-contact-sheets.json').write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps({'slug': slug, 'contact_sheets': output}))
