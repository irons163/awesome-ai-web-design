"""Create canonical filename aliases without recapturing or altering source bytes."""
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / '.stitch-work/current-official'
NOW = datetime.now(timezone.utc).isoformat()


def digest(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def alias_string(value):
    for old, new in [('linear-oct10-', 'linear.app-oct10-'),
                     ('linear-assets/', 'linear.app-assets/')]:
        if value.startswith(old):
            return new + value[len(old):]
        absolute = str(ROOT / old)
        if value.startswith(absolute):
            return str(ROOT / new) + value[len(absolute):]
    return value


def alias_data(value):
    if isinstance(value, dict):
        return {alias_string(k): alias_data(v) for k, v in value.items()}
    if isinstance(value, list):
        return [alias_data(v) for v in value]
    return alias_string(value) if isinstance(value, str) else value


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


original_files = sorted(p for p in ROOT.glob('linear-oct10-*') if p.is_file())
original_assets = sorted(p for p in (ROOT / 'linear-assets/oct10').rglob('*') if p.is_file())
original_hashes = {str(p.relative_to(ROOT)): digest(p) for p in original_files + original_assets}
preview = ROOT / 'linear.app.html'
preview_before = digest(preview) if preview.exists() else None
if any(ROOT.glob('linear.app-oct10-*')):
    raise RuntimeError('Canonical alias files already exist; refusing to overwrite evidence')

mapping = []
for source in original_assets + original_files:
    relative = str(source.relative_to(ROOT))
    destination = ROOT / alias_string(relative)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if source.suffix == '.json' and source.name != 'linear-oct10-source-hashes.json':
        write_json(destination, alias_data(json.loads(source.read_text())))
    elif source.suffix == '.md':
        destination.write_text(source.read_text().replace('linear-oct10-', 'linear.app-oct10-')
                               .replace('linear-assets/', 'linear.app-assets/'))
    elif source.name != 'linear-oct10-source-hashes.json':
        shutil.copyfile(source, destination)
    if destination.exists():
        mapping.append({'original': relative, 'alias': str(destination.relative_to(ROOT)),
                        'original_digest': digest(source), 'alias_digest': digest(destination),
                        'byte_identical': source.read_bytes() == destination.read_bytes()})

manifest = json.loads((ROOT / 'linear.app-oct10-assets.json').read_text())
assets_by_url = {a['source_url']: a for a in manifest['assets']}
bundle_path = ROOT / 'linear.app-oct10-asset-bundle.json'
bundle = json.loads(bundle_path.read_text())
for item in bundle['assets']:
    item['original_export_path'] = item['path']
    item['path'] = str(ROOT / assets_by_url[item['url']]['path'])
    assert Path(item['path']).is_file()
bundle['directoryPath'] = str(ROOT / 'linear.app-assets/oct10')
bundle['manifestPath'] = str(bundle_path)
bundle['filename_alias_provenance'] = {
    'alias_created_at': NOW,
    'original_provider_output': 'linear-oct10-asset-bundle.json',
    'note': 'Derived path alias for existing byte-identical original files; provider output remains unchanged in the original filename. This is not a new fetch or observation.'
}
write_json(bundle_path, bundle)

review_path = ROOT / 'linear.app-oct10-source-review.json'
review = json.loads(review_path.read_text())
review['brand'] = 'linear.app'
review['original_source_capture_preview_record'] = {
    'slug': 'linear', 'preview_untouched_sha256': review.pop('preview_untouched_sha256', None),
    'note': 'Retained original research record; it must not be interpreted as a historical capture-time hash of canonical linear.app.html.'
}
review['preview_untouched_sha256'] = preview_before['sha256'] if preview_before else None
review['preview_hash_recorded_at_alias_audit'] = NOW
review['filename_alias'] = {
    'original_prefix': 'linear', 'canonical_prefix': 'linear.app',
    'created_at': NOW, 'new_browser_observation': False,
    'observed_timestamps_preserved': True,
    'original_files_retained': True,
    'all_raster_and_asset_bytes_identical': True,
    'provenance': 'linear.app-oct12-source-alias-provenance.json',
    'note': 'Filename and stored path aliases only. Official URL remains https://linear.app/. No preview HTML was changed; recorded source capture, CSSOM and inspection times are unchanged.'
}
for scope in review['scopes'].values():
    for key in ['phase_metadata', 'reference']:
        record = scope[key]
        record.update(digest(ROOT / record['path']))
write_json(review_path, review)
markdown = ROOT / 'linear.app-oct10-source-review.md'
markdown.write_text(markdown.read_text() + '\nFilename alias provenance: these canonical linear.app filenames refer to the same earlier linear source observations. Original linear files remain retained. Native raster and original asset bytes are unchanged; JSON stored paths and slug metadata are derived aliases. No new capture or observation time is claimed. Alias created at ' + NOW + '.\n')

preview_after = digest(preview) if preview.exists() else None
assert preview_after == preview_before
for relative, original_digest in original_hashes.items():
    assert digest(ROOT / relative) == original_digest, relative
for entry in mapping:
    entry['alias_digest'] = digest(ROOT / entry['alias'])
    entry['byte_identical'] = entry['original_digest'] == entry['alias_digest']
    if entry['original'].endswith(('.jpg', '.png', '.woff2', '.css', '.svg', '.mp4')):
        assert entry['byte_identical'], entry

provenance = {
    'alias_created_at': NOW, 'new_browser_observation': False,
    'source_url': 'https://linear.app/', 'original_prefix': 'linear',
    'canonical_prefix': 'linear.app', 'original_files_unchanged': True,
    'all_native_rasters_and_original_assets_byte_identical': True,
    'source_observed_at': {str(w): json.loads((ROOT / f'linear-oct10-official-{w}-reference.json').read_text())['observed_at'] for w in [1280, 390]},
    'preview_before': preview_before, 'preview_after': preview_after,
    'preview_hash_scope': 'Measured at alias audit only; not a capture-time hash assertion',
    'files': mapping,
}
write_json(ROOT / 'linear.app-oct12-source-alias-provenance.json', provenance)
hashed = {str(p.relative_to(ROOT)): digest(p) for p in sorted(ROOT.glob('linear.app-oct10-*')) if p.is_file() and not p.name.endswith('source-hashes.json')}
hashed.update({str(p.relative_to(ROOT)): digest(p) for p in sorted((ROOT / 'linear.app-assets/oct10').rglob('*')) if p.is_file()})
hashed['linear.app-oct12-source-alias-provenance.json'] = digest(ROOT / 'linear.app-oct12-source-alias-provenance.json')
write_json(ROOT / 'linear.app-oct10-source-hashes.json', hashed)
print(json.dumps({'canonical_prefix': 'linear.app', 'aliased_original_files': len(mapping), 'originals_unchanged': True, 'asset_records': len(manifest['assets']), 'bundle_assets_with_existing_paths': len(bundle['assets']), 'source_observed_at': provenance['source_observed_at'], 'preview_untouched': True}, indent=2))
