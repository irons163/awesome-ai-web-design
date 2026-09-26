#!/usr/bin/env python3
"""Stage only public website files for static hosting, after build.py."""
import json
import re
import shutil
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'dist'
OFFICIAL_DRAFTS = ('spotify', 'linear', 'claude', 'notion', 'figma', 'framer', 'vercel')
DRAFT_SOURCE = ROOT / '.stitch-work' / 'current-official'


class AssetReferences(HTMLParser):
    def __init__(self):
        super().__init__()
        self.values = []

    def handle_starttag(self, _tag, attributes):
        for name, value in attributes:
            if name in ('src', 'href', 'poster') and value:
                self.values.append(value)


def stage_official_drafts():
    destination = OUTPUT / 'official-drafts'
    destination.mkdir()
    source_root = DRAFT_SOURCE.resolve()
    for name in OFFICIAL_DRAFTS:
        source = DRAFT_SOURCE / f'{name}.html'
        html = source.read_text()
        references = AssetReferences()
        references.feed(html)
        references.values.extend(re.findall(r'url\(([^)]+)\)', html))
        for value in references.values:
            value = value.strip(' \t\n\r\'"')
            if value.startswith(('https:', 'http:', 'data:', 'mailto:', '#', '/')):
                continue
            relative = Path(urlsplit(value).path)
            asset = (DRAFT_SOURCE / relative).resolve()
            asset.relative_to(source_root)
            if not asset.is_file():
                raise FileNotFoundError(f'Missing {name} draft asset: {relative}')
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(asset, target)
        badge = ('<div class="official-draft-badge" role="note">'
                 '<strong>官網重製草稿 · 尚未視覺驗收</strong>'
                 '<span>非品牌官方網站，內容是特定日期的參考快照。</span>'
                 '<a href="../#official-drafts">返回設計集 ↗</a></div>')
        style = '''<meta name="robots" content="noindex"><style>
.official-draft-badge{position:fixed;right:16px;bottom:16px;z-index:2147483647;max-width:min(340px,calc(100vw - 32px));padding:12px 16px;background:#fffdf7;color:#20211f;border:1px solid #d5d3ca;border-radius:9px;box-shadow:0 8px 34px #0004;font:12px/1.5 system-ui,sans-serif;display:grid;gap:3px}
.official-draft-badge strong{font-size:13px}.official-draft-badge span{color:#555}.official-draft-badge a{color:#a53d22;text-decoration:underline}
</style>'''
        html = html.replace('</head>', style + '</head>', 1)
        match = re.search(r'<body\b[^>]*>', html, re.I)
        if match is None:
            raise ValueError(f'Draft has no body: {source}')
        html = html[:match.end()] + badge + html[match.end():]
        (destination / f'{name}.html').write_text(html)


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
    stage_official_drafts()
    print(f'Staged public website in {OUTPUT}')


if __name__ == '__main__':
    main()
