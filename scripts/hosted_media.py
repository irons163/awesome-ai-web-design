"""Keep large original media at an immutable GitHub commit via static redirects."""
import hashlib
import json
import re
import shutil
from pathlib import Path
from urllib.parse import quote

MEDIA = {'.mp4', '.webm', '.png', '.jpg', '.jpeg', '.webp', '.avif', '.gif', '.woff', '.woff2', '.ttf', '.otf'}


def compact_hosted_media(root, output):
    config_path = root / 'data/hosted-official-media.json'
    config = json.loads(config_path.read_text())
    base = config['base_url']
    match = re.fullmatch(r'https://raw\.githubusercontent\.com/[^/]+/[^/]+/([a-f0-9]{40})/\.stitch-work/current-official/', base)
    if not match or match[1] != config['source_commit']:
        raise ValueError('Official media requires an immutable GitHub commit')
    work = root / '.stitch-work/current-official'
    selected, seen = [], set()
    for asset in config['assets']:
        name = asset['path']
        relative = Path(name)
        if relative.is_absolute() or '..' in relative.parts or '\\' in name or relative.suffix.lower() not in MEDIA or name in seen:
            raise ValueError('Invalid hosted media path: ' + name)
        seen.add(name)
        source = work / relative
        source.resolve().relative_to(work.resolve())
        data = source.read_bytes()
        if len(data) != asset['bytes'] or hashlib.sha256(data).hexdigest() != asset['sha256']:
            raise ValueError('Hosted original media changed: ' + name)
        staged = output / 'official-drafts' / relative
        if not staged.is_file():
            continue
        if hashlib.sha256(staged.read_bytes()).hexdigest() != asset['sha256']:
            raise ValueError('Staged media differs: ' + name)
        rule = '/official-drafts/' + quote(name, safe='/') + ' ' + base + quote(name, safe='/') + ' 302'
        if len(rule) > 1000:
            raise ValueError('Media redirect exceeds the hosting limit')
        selected.append((staged, rule, asset['bytes']))
    if len(selected) > 2000:
        raise ValueError('Too many static media redirects')
    for file, _, _ in selected:
        file.unlink()
    (output / '_redirects').write_text('\n'.join(sorted(rule for _, rule, _ in selected)) + '\n')
    shutil.copy2(config_path, output / 'assets/official-media-hosting.json')
    total = sum(p.stat().st_size for p in output.rglob('*') if p.is_file())
    if total > config['max_bundle_bytes']:
        raise ValueError('Static deployment exceeds its uploadable size budget')
    return dict(hosted_media_count=len(selected), hosted_media_bytes=sum(size for _, _, size in selected), bundled_static_bytes=total)
