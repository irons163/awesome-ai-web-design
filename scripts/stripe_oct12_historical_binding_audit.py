"""Document legacy capture provenance without inventing capture-time digests."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / '.stitch-work/current-official'
NOW = datetime.now(timezone.utc).isoformat()
LIMIT = (
    'Legacy capture records do not contain a capture-time preview SHA-256. '
    'Association with the current unchanged preview is supported by preserved '
    'completion/build/hash records and the owner visual review, rather than an '
    'independently recorded per-capture digest. The 2026-10-12 provenance audit '
    'does not backdate hashes or constitute a new browser review.'
)


def fingerprint(path):
    data = path.read_bytes()
    return {'path': path.relative_to(BASE).as_posix(), 'bytes': len(data),
            'sha256': hashlib.sha256(data).hexdigest()}


def save_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def preserve(path, target):
    if target.exists():
        raise RuntimeError(f'Preserved snapshot already exists: {target.name}')
    target.write_bytes(path.read_bytes())


def prepare(slug):
    result_path = BASE / f'{slug}-oct10-result.json'
    result = json.loads(result_path.read_text())
    preview = fingerprint(BASE / f'{slug}.html')
    assert preview['sha256'] == result['preview_sha256']
    manifest_path = BASE / result['hash_manifest'] if result.get('hash_manifest') else None
    historic = json.loads(manifest_path.read_text()) if manifest_path else result['hashes']
    historic_map = {x['path']: x for x in historic} if isinstance(historic, list) else historic
    assert historic_map[f'{slug}.html']['sha256'] == preview['sha256']
    if slug == 'stripe':
        captures = []
        for label in ['desktop', 'narrow']:
            record = BASE / f'{slug}-oct10-{label}-segments.json'
            phases = json.loads(record.read_text())
            for phase in phases:
                captures.append((label, record.name, phase['local']))
    elif slug == 'tesla':
        captures = []
        for label, check in result['checks'].items():
            width = check['viewport']['width'] if isinstance(check['viewport'], dict) else check['viewport'][0]
            record = f'{slug}-oct10-local-{width}-render-check.json'
            for phase in check['local_segments']:
                captures.append((label, record, phase))
    else:
        captures = []
        for label, check in result['checks'].items():
            record = check['final_local_phases']
            for phase in json.loads((BASE / record).read_text()):
                captures.append((label, record, phase))
    audit_captures = []
    for label, record, phase in captures:
        assert not any('sha' in k.lower() or 'hash' in k.lower() for k in phase), phase
        shot = phase.get('file', phase.get('screenshot'))
        fp = fingerprint(BASE / shot)
        previous = historic_map.get(shot)
        assert previous and previous['sha256'] == fp['sha256'], shot
        with Image.open(BASE / shot) as image:
            dimensions = list(image.size)
        viewport = phase.get('viewport', {'width': phase.get('width'), 'height': phase.get('height')})
        assert dimensions == [viewport['width'], viewport['height']], (shot, dimensions, viewport)
        audit_captures.append({
            'scope': label, 'record': record, 'screenshot': fp,
            'actual_raster_dimensions': dimensions,
            'recorded_viewport': viewport,
            'recorded_scroll_y': phase.get('scrollY', phase.get('y')),
            'recorded_page_height': phase.get('bodyHeight', phase.get('pageHeight')),
            'recorded_url': phase.get('url'),
            'recorded_capture_timestamp': phase.get('observed_at'),
            'capture_timestamp_available': bool(phase.get('observed_at')),
            'capture_time_preview_sha_available': False,
            'matches_pre_audit_historical_raster_hash': True,
        })
    records = [fingerprint(BASE / x) for x in sorted({p[1] for p in captures})]
    for record in records:
        old = historic_map.get(record['path'])
        record['historical_digest_available'] = bool(old)
        record['matches_historical_digest'] = bool(old and old['sha256'] == record['sha256'])
        assert not old or record['matches_historical_digest'], record['path']
    build = BASE / f'{slug}-oct10-build-record.json'
    build_evidence = None
    if build.exists():
        build_record = json.loads(build.read_text())
        assert build_record['html']['sha256'] == preview['sha256']
        build_evidence = {'artifact': fingerprint(build), 'recorded_html': build_record['html'],
                          'matches_current_preview_bytes': True,
                          'build_hash_timestamp_available': False,
                          'note': 'Source observation timestamps in references are not build-hash timestamps.'}
    return result_path, result, manifest_path, historic, preview, audit_captures, records, build_evidence


prepared = {slug: prepare(slug) for slug in ['stripe', 'tesla', 'mistral.ai']}
for slug, values in prepared.items():
    result_path, result, manifest_path, historic, preview, captures, records, build = values
    before_result = BASE / f'{slug}-oct12-pre-audit-result.json'
    preserve(result_path, before_result)
    before_manifest = None
    if manifest_path:
        before_manifest = BASE / f'{slug}-oct12-pre-audit-hashes.json'
        preserve(manifest_path, before_manifest)
    audit_path = BASE / f'{slug}-oct12-capture-binding-audit.json'
    audit = {
        'brand': slug, 'audit_performed_at': NOW, 'audit_taipei_date': '2026-10-12',
        'accepted': False, 'official_consistency_claim': False,
        'current_preview_checked_at': NOW, 'current_preview': preview,
        'current_equals_pre_audit_result_preview_sha': True,
        'current_equals_preserved_build_or_manifest_preview_sha': True,
        'pre_audit_result': fingerprint(before_result),
        'pre_audit_result_source_observed_at': result['observed_at'],
        'pre_audit_result_normalization_at': result.get('normalized_review_flags_at'),
        'source_observed_at_is_not_capture_hash_timestamp': True,
        'pre_audit_manifest': fingerprint(before_manifest) if before_manifest else
            {'location': before_result.name + '#/hashes',
             'note': 'Stripe preserved its completion hashes inline in its result.'},
        'build_evidence': build,
        'capture_binding_method': 'Preserved completion/build/hash records, unchanged current preview bytes, unchanged raster/metadata bytes, and owner historical visual review.',
        'capture_time_preview_sha_available': False,
        'per_capture_cryptographic_binding_available': False,
        'hash_values_calculated_in_this_audit_are_not_backdated': True,
        'fresh_browser_capture_performed': False,
        'historical_phase_records_modified': False,
        'historical_capture_records': records,
        'historical_local_raster_count': len(captures),
        'historical_local_rasters': captures,
        'interpretation': LIMIT,
        'coverage_reference': result['normalization_evidence']['coverage_and_dimensions_rechecked'],
        'coverage_note': 'Existing measured full-page coverage is retained; this audit rechecks file hashes/dimensions only and adds no visual-equivalence claim.'
    }
    save_json(audit_path, audit)
    review_path = BASE / result['visual_review']
    review_path.write_text(review_path.read_text().rstrip() +
        '\n\n## Legacy capture binding audit (2026-10-12 Taipei)\n\n' + LIMIT +
        f'\n\nCurrent preview SHA-256 `{preview["sha256"]}` matches the preserved pre-audit completion record and build/manifest record. '
        f'All {len(captures)} canonical local viewport rasters and their metadata retain their historical recorded hashes and actual dimensions. '
        f'The original phase records are unchanged. Exact files, preserved record snapshots, and the audit timestamp are in [{audit_path.name}]({audit_path.name}).\n')
    result['historical_capture_binding_audit'] = audit_path.name
    result['capture_time_preview_sha_available'] = False
    result['capture_binding_strength'] = 'historical_report_and_unchanged_bytes_not_capture_time_digest'
    result['capture_binding_limit'] = LIMIT
    result['normalization_evidence']['historical_capture_binding_audit'] = audit_path.name
    result['normalization_evidence']['basis'] = (
        'Existing owner visual review associated with the preserved completion/build/hash records; current preview bytes and historical screenshot/metadata hashes are unchanged. '
        'Legacy captures did not record a per-capture preview SHA. This is an explicitly documented historical association, not a retroactively created capture-time digest or a new browser run.')
    for key in ['remaining', 'remaining_differences', 'remaining_differences_and_limits']:
        if isinstance(result.get(key), list) and LIMIT not in result[key]:
            result[key].append(LIMIT)
    result['accepted'] = False
    result['official_consistency_claim'] = False
    added_files = [audit_path, before_result, review_path]
    if before_manifest:
        added_files.append(before_manifest)
    if not manifest_path:
        for path in added_files:
            fp = fingerprint(path)
            result['hashes'][fp.pop('path')] = fp
    save_json(result_path, result)
    if manifest_path:
        hash_map = {x['path']: x for x in historic} if isinstance(historic, list) else historic
        for path in added_files + [result_path]:
            fp = fingerprint(path)
            if isinstance(historic, list):
                hash_map[fp['path']] = fp
            else:
                name = fp.pop('path')
                hash_map[name] = fp
        save_json(manifest_path, list(sorted(hash_map.values(), key=lambda x: x['path'])) if isinstance(historic, list) else hash_map)
    assert fingerprint(BASE / f'{slug}.html') == preview
    print(slug, len(captures), 'unchanged canonical rasters;', audit_path.name)

status_path = ROOT / 'scripts/stripe_queue_status.json'
status = json.loads(status_path.read_text())
for item in status['brands']:
    slug = item['brand']
    result = json.loads((BASE / f'{slug}-oct10-result.json').read_text())
    preview = fingerprint(BASE / f'{slug}.html')
    assert preview['sha256'] == result['preview_sha256'], slug
    assert result['latest_draft_full_desktop_and_narrow_coverage']
    assert result['actual_raster_inspection_bound_to_current_preview']
    item.update(phase='complete scoped main-page review', html_sha256=preview['sha256'],
                result=f'{slug}-oct10-result.json', accepted=False)
status.update(updated_at=NOW, next_after_hp=[],
              browser_note='All 16 assigned scoped homepage reviews completed. Final Together supplemental tab awaits cleanup; actual raster dimensions verified on every canonical scope.',
              supplemental_source_coverage={'replicate_desktop_4320_5040': 'completed, fresh 2026-10-12 Taipei, explicitly mixed-time',
                                            'together_narrow_top_0_1_5': 'completed, fresh 2026-10-12 Taipei, explicitly mixed-time'},
              historical_capture_binding_audits={slug: f'{slug}-oct12-capture-binding-audit.json' for slug in prepared})
save_json(status_path, status)
print('Queue: all16 complete; no preview files changed.')
