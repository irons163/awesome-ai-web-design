"""Normalize five already reviewed records without rewriting historical captures.

Their original review records contain the preview digest, but older phase files
do not. Preserve that distinction and bind the unchanged preview through the
original result, instead of inventing a per-phase digest after the fact.
"""
from pathlib import Path
import hashlib
import json
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / '.stitch-work/current-official'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def file_record(name):
    data = (WORK / name).read_bytes()
    return {'path': name, 'bytes': len(data), 'sha256': digest(data)}


def save(name, value):
    (WORK / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


plan = json.loads((ROOT / '.stitch-work/publication-plan.json').read_text())
for slug in ['airtable', 'cal', 'cursor', 'apple', 'composio']:
    result_name = slug + '-oct10-result.json'
    original_name = slug + '-oct11-pre-normalization-result.private.json'
    original = WORK / original_name
    if not original.exists():
        original.write_bytes((WORK / result_name).read_bytes())
    record = json.loads(original.read_text())
    preview = file_record(slug + '.html')
    prior_digest = record.get('previewSha256') or record.get('files', {}).get(slug + '.html', {}).get('sha256')
    if prior_digest != preview['sha256']:
        raise ValueError('Historical reviewed preview bytes changed: ' + slug)
    evidence = {}
    for role in ['official', 'local']:
        for width, height, label in [(1280, 720, 'desktop'), (390, 844, 'narrow')]:
            suffix = label if slug == 'airtable' else str(width)
            prefix = slug + '-oct10-' + role + '-' + suffix
            phase_name = prefix + '-phases.json'
            phases = json.loads((WORK / phase_name).read_text())
            intervals, screenshots = [], []
            for index, phase in enumerate(phases):
                name = phase.get('screenshot', prefix + '-phase-' + str(index) + '.png')
                with Image.open(WORK / name) as raster:
                    if raster.size != (width, height):
                        raise ValueError('Historical raster dimensions differ: ' + name)
                extent = phase.get('bodyHeight', phase.get('height'))
                offset = phase['scrollY']
                intervals.append((max(0, offset), min(extent, offset + height)))
                screenshots.append(name)
            end, gaps = 0, []
            for start, stop in sorted(intervals):
                if start > end + 1:
                    gaps.append([end, start])
                end = max(end, stop)
            extent = phases[-1].get('bodyHeight', phases[-1].get('height'))
            if end < extent - 1:
                gaps.append([end, extent])
            historical_gaps = list(gaps)
            supplement_name = None
            if gaps and slug == 'airtable' and role == 'local' and width == 1280:
                supplement_name = 'airtable-oct11-local-desktop-coverage-supplement.json'
                supplement = json.loads((WORK / supplement_name).read_text())
                if supplement['draft_sha256'] != preview['sha256'] or supplement['viewport'] != {'width': width, 'height': height}:
                    raise ValueError('Airtable supplemental frame is not bound to current preview')
                with Image.open(WORK / supplement['screenshot']) as raster:
                    if raster.size != (width, height):
                        raise ValueError('Airtable supplemental raster has wrong dimensions')
                start = supplement['scrollY']
                if not all(start <= a and start + height >= b for a, b in gaps):
                    raise ValueError('Airtable supplemental frame does not cover the historical gap')
                screenshots.append(supplement['screenshot'])
                gaps = []
            if gaps:
                raise ValueError('Historical coverage gaps: ' + phase_name + repr(gaps))
            evidence[role + '_' + label] = {
                'phase_records': phase_name, 'screenshots': screenshots,
                'viewport': {'width': width, 'height': height},
                'settled_page_height': extent, 'whole_page_covered': True,
                'coverage_gaps': [], 'actual_raster_dimensions_checked': True,
                'historical_coverage_gaps': historical_gaps,
                'current_hash_bound_gap_supplement': supplement_name,
                'per_phase_preview_digest_recorded': False,
                'preview_binding': 'Unchanged bytes match the preserved original root review result; no retroactive per-phase digest was added.' if role == 'local' else None,
            }
    if slug == 'airtable':
        contacts = sorted(p.name for p in WORK.glob('airtable-oct10-compare-*.jpg'))
    else:
        contacts = [name for item in record['checks'].values() for name in item['diagnosticContactSheets']]
    if not contacts or any(not (WORK / name).is_file() for name in contacts):
        raise ValueError('Missing previously reviewed contact sheets: ' + slug)
    analysis = record['designAnalysis']
    review = record.get('review') or record.get('recordUpdates', {}).get('review')
    native_prompt = record['rewrittenPrompt']
    rewritten = slug + '-oct10-rewritten-prompts.md'
    text = '# ' + slug + '｜重寫 AI 指令與實際生成紀錄\n\n以下原始輸入曾實際送交 Google Stitch MCP，逐字保留；後續校正與原生輸出分開記錄。\n\n```text\n' + (WORK / native_prompt).read_text().strip() + '\n```\n'
    if slug == 'cal':
        text += '\n原始生成輸入把內文字型寫為 Matter，並把窄版 Cédric 範例誤當桌面範例。這些是當時實際輸入的錯誤，未改寫歷史紀錄；以下為依實際畫面修正、尚未再次送交生成的指令。\n\n' + (WORK / 'cal-oct11-corrected-reproduction-prompt.md').read_text()
    else:
        text += '\n後續校正應依相鄰的當前設計分析與實際畫面紀錄，保留公開原始圖片、SVG、字型與完整段落；動畫定格、未測互動及其他尺寸需如實列出，不能由供應商完成訊息推定與官方一致。\n'
    (WORK / rewritten).write_text(text)
    limits = record.get('remainingDifferences') or record.get('remaining') or []
    if slug == 'cal':
        limits = [*limits, 'The exact original Stitch prompt contains the disclosed Matter/body-font and desktop-booking-example errors; the separate corrected prompt was not re-sent to the provider.']
    row = next(item for item in plan['studies'] if item['brand'] == slug)
    if row['preview_sha256'] != preview['sha256']:
        raise ValueError('Publication dependency plan is stale: ' + slug)
    texts = [analysis, rewritten, review]
    allowed = sorted({slug + '.html', *row['assets'], *texts})
    for name in allowed:
        if not (WORK / name).is_file():
            raise ValueError('Missing explicit publication dependency: ' + name)
    provenance_name = slug + '-oct10-provenance.json'
    provenance = {
        'brand': slug, 'current_preview': preview,
        'historical_review_record': file_record(original_name),
        'unchanged_preview_matches_historical_root_review': True,
        'historical_phase_records_not_modified': True,
        'root_actually_viewed_contact_sheets_in_prior_review': contacts,
        'browser_evidence': evidence,
        'selected_public_files': [file_record(name) for name in allowed],
        'native_prompt_unchanged': file_record(native_prompt),
    }
    save(provenance_name, provenance)
    manifest_name = slug + '-oct10-publication-manifest.json'
    save(manifest_name, {
        'brand': slug, 'accepted': False, 'official_consistency_claim': False,
        'preview': preview, 'study_text': texts,
        'runtime_required_assets': row['assets'], 'publish_allowlist': allowed,
        'private_work_files_do_not_stage': [original_name, provenance_name],
        'publication_instructions': 'Use only the exact allowlist. Raw DOM/network/captured state and native provider responses remain private work files.',
    })
    record.update({
        'brand': slug, 'accepted': False, 'official_consistency_claim': False,
        'preview': slug + '.html', 'preview_sha256': preview['sha256'],
        'status': 'visually_compared_with_scoped_differences',
        'reference_url': record.get('officialURL') or record.get('recordUpdates', {}).get('reference_url'),
        'latest_draft_actual_render_checked': True,
        'latest_draft_full_desktop_and_narrow_coverage': True,
        'actual_raster_inspection_bound_to_current_preview': True,
        'actual_raster_inspection_binding_method': 'Preserved historical root result digest matches current unchanged preview; phase records did not originally record draft hashes.',
        'evidence': evidence, 'root_actual_review': contacts,
        'rewrittenPrompt': rewritten, 'remaining_differences_and_limits': limits,
        'current_supplements': {'design_analysis': analysis, 'rewritten_prompts': rewritten, 'visual_review': review, 'provenance': provenance_name, 'publication_manifest': manifest_name},
    })
    save(result_name, record)
    print(json.dumps({'brand': slug, 'preview_sha256': preview['sha256'], 'historical_digest_chain_preserved': True, 'contact_sheets': len(contacts), 'accepted': False}))
