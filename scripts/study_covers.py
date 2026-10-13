"""Validate that public covers depict the current study, never an older export."""
import hashlib
import json
from pathlib import Path

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def covers_for(root,catalog):
    manifest=json.loads((root/'data/study-covers.json').read_text())
    covers={row['slug']:row for row in manifest['covers']}
    if len(covers)!=len(manifest['covers']) or set(covers)!={row['slug'] for row in catalog}:raise ValueError('Current cover inventory differs from catalog')
    return covers

def cover_for(root,record,brand,current):
    if record['brand']!=brand or record['preview_sha256']!=current:raise ValueError('Stale current-study cover: '+brand)
    work=root/'.stitch-work/current-official'
    for key in ['source','result']:
        file=work/record[key]['path'];file.resolve().relative_to(work.resolve())
        if digest(file)!=record[key]['sha256']:raise ValueError('Changed cover evidence: '+brand)
    image=record['image'];file=root/image['path'];file.resolve().relative_to((root/'assets/current-previews').resolve())
    if digest(file)!=image['sha256'] or file.stat().st_size!=image['bytes']:raise ValueError('Changed cover image: '+brand)
    return dict(src=image['path'],width=image['width'],height=image['height'],sha256=image['sha256'],preview_sha256=current)
