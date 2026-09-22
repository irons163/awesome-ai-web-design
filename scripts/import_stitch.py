#!/usr/bin/env python3
"""Import completed MCP results; keep exported HTML and screenshot bytes unchanged."""
import argparse
import hashlib
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def unpack(result):
    if 'structuredContent' in result:
        return result['structuredContent']
    for block in result.get('content', []):
        if block.get('type') == 'text':
            try:
                return json.loads(block['text'])
            except ValueError:
                pass
    return result


def import_result(work, slug):
    folder = ROOT / 'design-md' / slug
    if (folder / 'STITCH.json').exists():
        return False
    response = unpack(json.loads((work / f'{slug}-generated.json').read_text()))
    screens = [s for component in response.get('outputComponents', [])
               for s in component.get('design', {}).get('screens', [])
               if s.get('htmlCode', {}).get('downloadUrl') and s.get('screenshot', {}).get('downloadUrl')]
    if not screens:
        print(f'{slug}: no completed screen yet')
        return False
    # Stitch can also return SVG logo assets under htmlCode. Select a complete
    # page by its actual export bytes, not by the presence of that field alone.
    for screen in screens:
        with urllib.request.urlopen(screen['htmlCode']['downloadUrl'], timeout=90) as result:
            html_data = result.read()
        if b'<html' in html_data.lower():
            break
    else:
        raise ValueError(f'No complete HTML page in Stitch exports: {slug}')
    request = json.loads((work / f'{slug}-request.json').read_text())
    prompt = request['prompt'].encode()
    (folder / 'STITCH-PROMPT.md').write_bytes(prompt)
    files = {'STITCH-PROMPT.md': digest(prompt)}
    screenshot = 'preview.png'
    for key, name in [('htmlCode', 'preview.html'), ('screenshot', screenshot)]:
        url = screen[key]['downloadUrl']
        if key == 'screenshot' and 'googleusercontent.com/' in url:
            url += '=w' + str(screen.get('width', 1440))
        if key == 'htmlCode':
            data = html_data
        else:
            with urllib.request.urlopen(url, timeout=90) as result:
                data = result.read()
        if key == 'screenshot' and not data.startswith(b'\x89PNG'):
            if data.startswith(b'\xff\xd8'):
                name = screenshot = 'preview.jpg'
            elif data.startswith(b'RIFF'):
                name = screenshot = 'preview.webp'
            else:
                raise ValueError(f'Unsupported screenshot format: {slug}')
        if key == 'htmlCode' and b'<html' not in data.lower():
            raise ValueError(f'Invalid HTML export: {slug}')
        (folder / name).write_bytes(data)
        files[name] = digest(data)
    thumbnail = 'thumbnail.png'
    thumbnail_url = screen['screenshot']['downloadUrl'] + '=w640'
    with urllib.request.urlopen(thumbnail_url, timeout=90) as result:
        thumbnail_data = result.read()
    if thumbnail_data.startswith(b'\xff\xd8'):
        thumbnail = 'thumbnail.jpg'
    elif thumbnail_data.startswith(b'RIFF'):
        thumbnail = 'thumbnail.webp'
    elif not thumbnail_data.startswith(b'\x89PNG'):
        raise ValueError(f'Unsupported thumbnail format: {slug}')
    (folder / thumbnail).write_bytes(thumbnail_data)
    files[thumbnail] = digest(thumbnail_data)
    provenance = {
        'provider': 'Google Stitch', 'transport': 'MCP', 'status': 'generated',
        'project_id': response.get('projectId', request['projectId']),
        'screen_id': screen.get('id') or screen['name'].split('/')[-1],
        'screen_name': screen['name'], 'title': screen.get('title', slug),
        'width': int(screen.get('width', 1440)), 'height': int(screen.get('height', 900)),
        'mode': screen.get('theme', {}).get('colorMode', '').lower(),
        'design_system': request.get('designSystem'),
        'imported_at': datetime.now(timezone.utc).isoformat(),
        'screenshot': screenshot, 'thumbnail': thumbnail, 'files': files,
        'scope': 'Original Stitch HTML and screenshot exports. Static demo, not an official brand website.'
    }
    (folder / 'STITCH.json').write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + '\n')
    (folder / 'preview-dark.html').unlink(missing_ok=True)
    print(f'{slug}: imported {provenance["title"]}')
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('slugs', nargs='*')
    args = parser.parse_args()
    recipes = json.loads((ROOT / 'data/recipes.json').read_text())
    known = {r['slug'] for r in recipes}
    slugs = args.slugs or [r['slug'] for r in recipes]
    for slug in slugs:
        if slug not in known:
            raise ValueError('Unknown design slug')
        if (args.directory / f'{slug}-generated.json').exists():
            import_result(args.directory, slug)


if __name__ == '__main__':
    main()
