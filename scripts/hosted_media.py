"""Preserve published HTML bytes and serve allowlisted media through the Worker."""
import hashlib
import json
import re
import shutil
from pathlib import Path

MEDIA = {'.mp4', '.webm', '.png', '.jpg', '.jpeg', '.webp', '.avif', '.gif', '.svg', '.woff', '.woff2', '.ttf', '.otf'}
TEXT = {'.html', '.css', '.js', '.mjs', '.json'}


def validated_media(source_root, output, config):
    selected, seen = [], set()
    for asset in config['assets']:
        name = asset['path']
        relative = Path(name)
        if relative.is_absolute() or any(x in ('', '.', '..') for x in name.split('/')) or '\\' in name or relative.suffix.lower() not in MEDIA or name in seen:
            raise ValueError('Invalid hosted media path: ' + name)
        seen.add(name)
        source = source_root / relative
        source.resolve().relative_to(source_root.resolve())
        data = source.read_bytes()
        if len(data) != asset['bytes'] or hashlib.sha256(data).hexdigest() != asset['sha256']:
            raise ValueError('Hosted original media changed: ' + name)
        staged = output / relative
        if not staged.is_file():
            continue
        if hashlib.sha256(staged.read_bytes()).hexdigest() != asset['sha256']:
            raise ValueError('Staged media differs: ' + name)
        selected.append((name, staged, asset['bytes']))
    return selected


def compact_catalog_media(root, output, catalog):
    config_path = root / 'data/hosting-assets.json'
    config = json.loads(config_path.read_text())
    if not re.fullmatch(r'https://raw\.githubusercontent\.com/[^/]+/[^/]+/[a-f0-9]{40}/', config['image_base_url']):
        raise ValueError('Catalog media requires an immutable GitHub commit')
    expected = sorted(item['preview'][key] for item in catalog['designs'] if item['preview']['status'] == 'generated' for key in ('image', 'thumbnail'))
    if expected != sorted(item['path'] for item in config['assets']):
        raise ValueError('Catalog media allowlist differs from the published collection')
    selected = validated_media(root, output, config)
    for _, file, _ in selected:
        file.unlink()
    shutil.copy2(config_path, output / 'assets/catalog-media-hosting.json')


def compact_hosted_media(root, output):
    config_path = root / 'data/hosted-official-media.json'
    config = json.loads(config_path.read_text())
    match = re.fullmatch(r'https://raw\.githubusercontent\.com/[^/]+/[^/]+/([a-f0-9]{40})/\.stitch-work/current-official/', config['base_url'])
    if not match or match[1] != config['source_commit']:
        raise ValueError('Official media requires an immutable GitHub commit')
    work = root / '.stitch-work/current-official'
    drafts = output / 'official-drafts'
    selected = validated_media(work, drafts, config)
    proof = {}
    for file in sorted(drafts.rglob('*')):
        if not file.is_file() or file.suffix.lower() not in TEXT:
            continue
        relative = file.relative_to(drafts).as_posix()
        original = file.read_bytes()
        if original != (work / relative).read_bytes():
            raise ValueError('Staged text differs from preserved source: ' + relative)
        checksum = hashlib.sha256(original).hexdigest()
        proof[relative] = dict(source_sha256=checksum, published_sha256=checksum, replacements=[])
    for _, file, _ in selected:
        file.unlink()
    (output / '_redirects').unlink(missing_ok=True)
    shutil.copy2(config_path, output / 'assets/official-media-hosting.json')
    publication = dict(transport='same_origin_immutable_proxy', source_commit=config['source_commit'], files=proof)
    (output / 'assets/official-media-publication.json').write_text(json.dumps(publication, ensure_ascii=False, separators=(',', ':')) + '\n')
    studies_path = output / 'assets/official-studies.json'
    if studies_path.is_file():
        studies = json.loads(studies_path.read_text())
        studies['media_publication'] = 'assets/official-media-publication.json'
        for study in studies['studies']:
            study['published_preview_sha256'] = hashlib.sha256((output / study['preview']).read_bytes()).hexdigest()
        studies_path.write_text(json.dumps(studies, ensure_ascii=False, separators=(',', ':')) + '\n')
    total = sum(p.stat().st_size for p in output.rglob('*') if p.is_file())
    if total > config['max_bundle_bytes']:
        raise ValueError('Static deployment exceeds its uploadable size budget')
    return dict(hosted_media_count=len(selected), hosted_media_bytes=sum(size for _, _, size in selected), bundled_static_bytes=total, transported_reference_count=0)
