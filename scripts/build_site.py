#!/usr/bin/env python3
"""Stage only public website files for static hosting, after build.py."""
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'dist'


def main():
    if OUTPUT.is_symlink():
        raise RuntimeError('dist must be a regular build directory')
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir()
    for name in ('index.html', 'README.md', 'ATTRIBUTION.md', 'LICENSE', 'CONTRIBUTING.md'):
        shutil.copy2(ROOT / name, OUTPUT / name)
    for name in ('assets', 'design-md', 'prompts'):
        shutil.copytree(ROOT / name, OUTPUT / name, ignore=shutil.ignore_patterns('all-designs.zip') if name == 'assets' else None)
    # Keep the complete, unchanged exports in GitHub and the downloadable ZIP.
    # Pin hosted images to their source commit so later pushes cannot change them.
    image_base = json.loads((ROOT / 'data/hosting-assets.json').read_text())['image_base_url'].rstrip('/') + '/'
    catalog_path = OUTPUT / 'assets/catalog.json'
    catalog = json.loads(catalog_path.read_text())
    for entry in catalog['designs']:
        preview = entry['preview']
        if preview['status'] != 'generated':
            continue
        for key in ('image', 'thumbnail'):
            relative = preview[key]
            preview[key] = image_base + relative
            (OUTPUT / relative).unlink(missing_ok=True)
    catalog_path.write_text(json.dumps(catalog, ensure_ascii=False, separators=(',', ':')) + '\n')
    print(f'Staged public website in {OUTPUT}')


if __name__ == '__main__':
    main()
