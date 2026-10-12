"""Publishable study records from root-reviewed, hash-bound raster evidence.

This only packages explicitly configured findings. Geometry and file existence
never invent visual acceptance; the reviewer must supply an actually viewed
contact-sheet list. Raw browser DOM/network bundles remain private work files.
"""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / '.stitch-work/current-official'


def read(name):
    return json.loads((WORK / name).read_text())


def hashed(name):
    data = (WORK / name).read_bytes()
    return {'path': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def finalize(config):
    slug = config['brand']
    stem = slug + '-oct10-'
    preview = hashed(slug + '.html')
    if config.get('ready_to_finalize') is False:
        raise ValueError('Research-only draft is not ready for finalization: ' + slug)
    if config.get('expected_final_preview_sha256') and config['expected_final_preview_sha256'] != preview['sha256']:
        raise ValueError('Configured final preview hash differs: ' + slug)
    if not config.get('root_viewed_native_png'):
        raise ValueError('Native original has not been actually viewed: ' + slug)
    evidence = {}
    for role in ['official', 'local']:
        for width, label in [(1280, 'desktop'), (390, 'narrow')]:
            prefix = stem + role + '-' + str(width)
            frames = read(prefix + '-phases.json')
            intervals = []
            for frame in frames:
                viewport = frame['viewport']
                with Image.open(WORK / frame['screenshot']) as image:
                    mapped = frame.get('actual_raster_dimensions', {})
                    scale = image.width / viewport['width']
                    proportional = (config.get('allow_documented_proportional_rasters') is True
                                    and frame.get('raster_mapping') == 'proportional_full_viewport'
                                    and (mapped.get('width'), mapped.get('height')) == image.size
                                    and 0.9 <= scale <= 1
                                    and abs(image.height - viewport['height'] * scale) <= 1)
                    if image.size != (viewport['width'], viewport['height']) and not proportional:
                        raise ValueError('Wrong actual viewport raster: ' + frame['screenshot'])
                coverage = frame.get('coverage', {})
                offset = coverage.get('offset', frame['scrollY'])
                extent = coverage.get('extent', frame['bodyHeight'])
                visible = coverage.get('visible_extent', viewport['height'])
                intervals.append((max(0, offset), min(extent, offset + visible)))
            end, gaps = 0, []
            for start, stop in sorted(intervals):
                if start > end + 1:
                    gaps.append([end, start])
                end = max(end, stop)
            height = frames[-1].get('coverage', {}).get('extent', frames[-1]['bodyHeight'])
            if end < height - 1:
                gaps.append([end, height])
            current = role == 'local' and all(f.get('draft_sha256') == preview['sha256'] for f in frames)
            evidence[role + '_' + label] = {
                'measurement': prefix + '-reference.json', 'phases': prefix + '-phases.json',
                'viewport': frames[0]['viewport'], 'settled_page_height': height,
                'coverage_coordinate_space': frames[-1].get('coverage', {}).get('coordinate_space', 'document_scroll'),
                'screenshots': len(frames), 'whole_page_covered': not gaps,
                'uncovered_intervals': gaps,
                'actual_raster_dimensions_checked': True,
                'actual_raster_dimensions': [dict(t) for t in sorted({tuple(sorted(f.get('actual_raster_dimensions', f['viewport']).items())) for f in frames})],
                'raster_mapping': sorted({f.get('raster_mapping', 'exact') for f in frames}),
                'observed_at': [frames[0]['observed_at'], frames[-1]['observed_at']],
                'rect_based_visible_broken_candidates': max(len(f['brokenVisibleImages']) for f in frames),
                'horizontal_overflow_observed': any(f['bodyWidth'] > width for f in frames),
                'screenshot_files': [f['screenshot'] for f in frames],
                'proves_latest_draft': current if role == 'local' else None,
                'draft_sha256_at_capture': preview['sha256'] if current else None,
            }
    full_latest = all(evidence['local_' + mode]['whole_page_covered'] and evidence['local_' + mode]['proves_latest_draft'] for mode in ['desktop', 'narrow'])
    if not full_latest:
        raise ValueError('Latest HTML does not have complete actual raster evidence: ' + slug)
    comparison = read(stem + 'layout-comparison.json')
    expected_sheets = [s for item in comparison.values() for s in item['diagnosticContactSheets']]
    if set(expected_sheets) != set(config['root_viewed_contact_sheets']):
        raise ValueError('Actual review declaration does not cover current contact sheets: ' + slug)
    response = read(stem + 'stitch-response.json')['structuredContent']
    screens = [s for c in response['outputComponents'] for s in c.get('design', {}).get('screens', [])]
    native_files = [stem + 'reproduction-prompt.md']
    native_files += [stem + f'stitch-raw-{i}.{suffix}' for i in range(len(screens)) for suffix in ['html', 'png']]
    native = {
        'project': 'projects/' + response['projectId'],
        'current_screens': ['projects/' + response['projectId'] + '/screens/' + s['id'] for s in screens],
        'original_exports_preserved': True,
        'native_screen_metadata': [{'id': s['id'], 'device_type': s.get('deviceType'), 'width': s.get('width'), 'height': s.get('height')} for s in screens],
        'original_exports': native_files[1:], 'exact_native_prompt': native_files[0],
        'native_image_actually_viewed_by_root': config['root_viewed_native_png'],
        'provider_image_is_not_browser_QA': True,
    }
    originals = []
    for name in ['DESIGN.md', 'PROMPTS.md', 'README.md', 'STITCH-PROMPT.md']:
        path = 'design-md/' + config.get('catalog_slug', slug) + '/' + name
        f = ROOT / path
        if not f.is_file():
            continue
        old = subprocess.run(['git', 'show', 'HEAD:' + path], cwd=ROOT, capture_output=True)
        originals.append({'path': path, 'sha256': hashlib.sha256(f.read_bytes()).hexdigest(), 'unchanged_from_HEAD': old.returncode == 0 and old.stdout == f.read_bytes()})
    analysis_name, prompt_name, review_name = [stem + x for x in ['design-analysis.md', 'rewritten-prompts.md', 'visual-review.md']]
    declaration = '**已比對主要靜態畫面，仍有差異；accepted=false，不宣稱與官方一致。**'
    (WORK / analysis_name).write_text('# ' + config['label'] + '｜目前公開官方網站設計分析\n\n' + config['analysis_zh'].strip() + '\n\n' + declaration + '\n\n既有設計分析及原始指令保留。本次官方來源、真實 Google Stitch MCP 原始輸出、校正檔與實際瀏覽器畫面分開記錄。研究頁面免費瀏覽，沒有啟動付費方案或交易。\n', encoding='utf8')
    prompt = (WORK / native_files[0]).read_text().strip()
    (WORK / prompt_name).write_text('# ' + config['label'] + '｜重寫 AI 指令與實際生成紀錄\n\n以下為本次實際送交 Google Stitch MCP 的完整原始指令，逐字保留；供應商輸出不能替代畫面驗證。\n\n```text\n' + prompt + '\n```\n\n後續校正指令：\n\n' + config['correction_prompt'].strip() + '\n', encoding='utf8')
    rows = ['| 實際取樣 | 頁高 | 分段數 | 全頁覆蓋 |', '|---|---:|---:|---|']
    for key, item in evidence.items():
        rows.append(f'| {key} | {item["settled_page_height"]} | {item["screenshots"]} | {"是" if item["whole_page_covered"] else "否"} |')
    limits = config['remaining_differences_and_limits']
    (WORK / review_name).write_text('# ' + config['label'] + '｜實際畫面校正與驗證\n\n' + declaration + '\n\n官方來源：' + config['reference_url'] + '。重製檔 SHA-256：`' + preview['sha256'] + '`。\n\n主代理已實際檢視全部 ' + str(len(expected_sheets)) + ' 張桌面／窄版對照圖，以及本次原生 Stitch 圖。真實 PNG/JPEG 尺寸已檢查，完整取樣對應目前檔案；相同頁高與幾何量測不代表完全一致。窄版為桌面 UA 的 390px 響應式測試。\n\n' + '\n'.join(rows) + '\n\n' + '\n\n'.join(limits) + '\n', encoding='utf8')
    source = (WORK / (slug + '.html')).read_text()
    required = sorted(set(re.findall(re.escape(slug) + r'-assets/[A-Za-z0-9_./%+-]+', source)))
    missing = [name for name in required if not (WORK / name).is_file()]
    if missing:
        raise ValueError('Missing referenced local assets: ' + repr(missing))
    # Only the selected public files below may be copied. Raw DOM, captured
    # cookies/tracking, failed transfer bundles and provider responses stay local.
    private = [stem + role + '-' + str(width) + '-reference.json' for role in ['official', 'local'] for width in [1280, 390]]
    private += [stem + 'asset-bundle.json', stem + 'stitch-response.json']
    private += config.get('private_work_files', [])
    public_manifest = {
        'brand': slug, 'accepted': False, 'official_consistency_claim': False,
        'preview': preview, 'study_text': [analysis_name, prompt_name, review_name],
        'runtime_required_assets': required, 'missing_required_assets': [],
        'native_original_exports': native['original_exports'],
        'evidence_phases': [e['phases'] for e in evidence.values()],
        'private_work_files_do_not_stage': private,
        'publication_instructions': 'Only explicit study/evidence files, native original exports and referenced local assets. Never recursively copy raw browser DOM, bundles or host application screenshots.',
    }
    manifest_name = stem + 'publication-manifest.json'
    (WORK / manifest_name).write_text(json.dumps(public_manifest, ensure_ascii=False, indent=2) + '\n')
    names = {slug + '.html', *required, *native_files, analysis_name, prompt_name, review_name, manifest_name, stem + 'layout-comparison.json'}
    for item in evidence.values():
        names.update([item['phases'], *item['screenshot_files']])
    names.update(expected_sheets)
    hashes = [hashed(name) for name in sorted(names)]
    provenance_name = stem + 'provenance.json'
    provenance = {'brand': slug, 'reference_url': config['reference_url'], 'native_stitch': native,
                  'current_preview': preview, 'browser_evidence': evidence,
                  'original_analysis_and_prompts': originals,
                  'root_actually_viewed_contact_sheets': config['root_viewed_contact_sheets'],
                  'visual_inspection_owner': 'root', 'hashes': hashes,
                  'static_derivatives': config.get('static_derivatives', []),
                  'private_raw_retention': private}
    (WORK / provenance_name).write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + '\n')
    asset_manifest = read(stem + 'assets.json')
    result = {
        'brand': slug, 'observed_at': evidence['official_desktop']['observed_at'][0],
        'accepted': False, 'official_consistency_claim': False, 'status': 'in_visual_review',
        'reference_url': config['reference_url'], 'preview': slug + '.html',
        'preview_sha256': preview['sha256'], 'native_stitch': native,
        'scope': {'desktop': {'width': 1280, 'height': 720}, 'narrow': {'width': 390, 'height': 844, 'mobile': False}, 'public_anonymous': True, 'service_actions_performed': False},
        'method': 'Genuine native Stitch, original official assets and source correction, then actual root review of the final hash-bound raster evidence.',
        'evidence': evidence, 'layout_comparison': stem + 'layout-comparison.json',
        'root_actual_review': config['root_viewed_contact_sheets'], 'visual_inspection_owner': 'root',
        'latest_draft_actual_render_checked': True,
        'latest_draft_full_desktop_and_narrow_coverage': True,
        'latest_draft_raster_dimensions_valid': True,
        'public_assets': {'manifest': stem + 'assets.json', 'count': len(asset_manifest['assets']), 'failed_transfers': len(asset_manifest['failures'])},
        'remaining_differences_and_limits': limits,
        'cost': {'external_purchase_or_paid_plan_started': False, 'study_access_free': True, 'provider_usage_billing_not_asserted': True},
        'current_supplements': {'design_analysis': analysis_name, 'rewritten_prompts': prompt_name, 'visual_review': review_name, 'provenance': provenance_name, 'publication_manifest': manifest_name},
        'design_analysis_and_original_prompts': originals,
        'hashes': hashes + [hashed(provenance_name)],
    }
    (WORK / (stem + 'result.json')).write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'brand': slug, 'sha256': preview['sha256'], 'latest_full_both': True, 'accepted': False, 'public_assets': len(required)}))


if __name__ == '__main__':
    for path in sys.argv[1:]:
        finalize(json.loads(Path(path).read_text()))
