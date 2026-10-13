"""Publish immutable original media without depending on host redirect support."""
import hashlib
import json
import posixpath
import re
import shutil
from pathlib import Path
from urllib.parse import quote

MEDIA = {'.mp4', '.webm', '.png', '.jpg', '.jpeg', '.webp', '.avif', '.gif', '.woff', '.woff2', '.ttf', '.otf'}
TEXT = {'.html', '.css', '.js', '.mjs', '.json'}


def transport_references(names, parent, base):
    if not names:
        return {}, re.compile(rb'(?!)')
    references = {}
    for name in names:
        relative = posixpath.relpath(name, parent or '.')
        variants = {relative, quote(relative, safe='/'), '/official-drafts/' + quote(name, safe='/')}
        if not relative.startswith('../'):
            variants.update('./' + item for item in tuple(variants) if not item.startswith('/'))
        target = base + quote(name, safe='/')
        for value in variants:
            references[value.encode()] = (target.encode(), name)
            if '/' in value:
                references[value.replace('/', '\\/').encode()] = (target.replace('/', '\\/').encode(), name)
    pattern = re.compile(rb'(?<![A-Za-z0-9_./:\-])(?:\\?/)?[A-Za-z0-9_.%\-]+(?:(?:\\?/)[A-Za-z0-9_.%\-]+)*(?=$|[?#&\s"\'<>()\\,;])')
    return references, pattern


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
        selected.append((name, staged, asset['bytes']))
    names = [name for name, _, _ in selected]
    cache, pending, proof = {}, [], {}
    drafts = output / 'official-drafts'
    for file in sorted(drafts.rglob('*')):
        if not file.is_file() or file.suffix.lower() not in TEXT:
            continue
        relative = file.relative_to(drafts).as_posix()
        parent = posixpath.dirname(relative)
        if parent not in cache:
            cache[parent] = transport_references(names, parent, base)
        references, pattern = cache[parent]
        original = file.read_bytes()
        edits = [(m, references[m[0]]) for m in pattern.finditer(original) if m[0] in references]
        if not edits:
            continue
        if original != (work / relative).read_bytes():
            raise ValueError('Staged text differs from preserved source: ' + relative)
        chunks, cursor, records = [], 0, []
        for found, (replacement, asset_name) in edits:
            chunks.extend((original[cursor:found.start()], replacement))
            records.append([found.start(), found.end(), found[0].decode(), asset_name])
            cursor = found.end()
        chunks.append(original[cursor:])
        published = b''.join(chunks)
        proof[relative] = dict(source_sha256=hashlib.sha256(original).hexdigest(), published_sha256=hashlib.sha256(published).hexdigest(), replacements=records)
        pending.append((file, published))
    for file, data in pending:
        file.write_bytes(data)
    for _, file, _ in selected:
        file.unlink()
    (output / '_redirects').unlink(missing_ok=True)
    shutil.copy2(config_path, output / 'assets/official-media-hosting.json')
    publication = dict(transport='absolute_immutable_urls', source_commit=config['source_commit'], files=proof)
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
    return dict(hosted_media_count=len(selected), hosted_media_bytes=sum(size for _, _, size in selected), bundled_static_bytes=total, transported_reference_count=sum(len(p['replacements']) for p in proof.values()))
