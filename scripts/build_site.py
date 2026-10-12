#!/usr/bin/env python3
"""Stage public catalog and exact current-study asset dependencies."""
import json
import shutil
from pathlib import Path
from publication import stage_official_content
ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'dist'
DRAFT_SOURCE = ROOT / '.stitch-work/current-official'
OFFICIAL_DRAFTS = tuple('linear' if item['slug'] == 'linear.app' else item['slug']
                        for item in json.loads((ROOT / 'assets/catalog.json').read_text())['designs'])


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
    progress = json.loads((DRAFT_SOURCE / 'progress.json').read_text())
    summary = stage_official_content(ROOT, OUTPUT, progress, catalog['designs'])
    print(json.dumps(summary))
    print(f'Staged public website in {OUTPUT}')


if __name__ == '__main__':
    main()
