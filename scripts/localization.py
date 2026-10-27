"""Publish reviewed Chinese text without mutating captured preview evidence."""
import hashlib
import json
from pathlib import Path


def digest(value):
    return hashlib.sha256(value if isinstance(value, bytes) else value.encode()).hexdigest()


def load_localizations(root, catalog):
    data = json.loads((root / 'data/zh-TW/studies.json').read_text())
    if data.get('locale') != 'zh-TW' or set(data['studies']) != {item['slug'] for item in catalog}:
        raise ValueError('Incomplete Taiwan Chinese publication')
    return data


def localize_study(root, destination, status, data):
    row = data['studies'][status['slug']]
    if row['source_preview_sha256'] != status['preview_sha256']:
        raise ValueError('Chinese text is bound to another preview: ' + status['slug'])
    remaining = json.dumps(status['remaining_differences'], ensure_ascii=False, separators=(',', ':'))
    if digest(remaining) != row['remaining_source_sha256']:
        raise ValueError('Chinese limitations require review: ' + status['slug'])
    if set(row['documents']) != set(status['study']):
        raise ValueError('Chinese document coverage differs: ' + status['slug'])
    status['document_sha256'] = {}
    for kind, relative in status['study'].items():
        source = row['source_documents'][kind]
        if relative != source['path'] or not relative.startswith('official-drafts/') or Path(relative).name != relative.split('/', 1)[1]:
            raise ValueError('Unsafe or stale Chinese document path')
        original = root / '.stitch-work/current-official' / Path(relative).name
        if digest(original.read_bytes()) != source['sha256']:
            raise ValueError('Chinese document source changed: ' + relative)
        target = destination / Path(relative).name
        if not target.is_file() or digest(target.read_bytes()) != source['sha256']:
            raise ValueError('Unexpected document before localization: ' + relative)
        text = row['documents'][kind]
        if '繁體中文（台灣用語，zh-TW）' not in text:
            raise ValueError('Missing Taiwan Chinese document')
        target.write_text(text)
        status['document_sha256'][kind] = digest(text)
    status['remaining_differences'] = row['remaining_differences']
    status['document_language'] = 'zh-TW'
    status['localized_at'] = data['updated']
    if row.get('implementation_files'):
        status['implementation_files'] = {}
        for name, file in row['implementation_files'].items():
            relative = file['path']
            if name not in ('TOKENS.json', 'ASSETS.json', 'ASSETS.md', 'starter.css') or relative != f'implementation/{status["slug"]}/{name}':
                raise ValueError('Unsafe implementation companion path')
            target = destination.parent / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(file['text'])
            status['implementation_files'][name] = dict(path=relative,sha256=digest(file['text']))
        status['implementation_version'] = data['updated']
