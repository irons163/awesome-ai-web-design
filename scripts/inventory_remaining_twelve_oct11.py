"""Read-only source/native inventory for the next root-owned browser queue."""
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import urlsplit
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / '.stitch-work/current-official'
BRANDS = ['lamborghini', 'renault', 'revolut', 'meta', 'mastercard', 'binance',
          'dell-1996', 'nintendo-2001', 'theverge', 'wired', 'pinterest', 'vodafone']
GAPS = {
    'lamborghini': ['No saved non-native viewport raster files in current-official; earlier geometry/video/menu checks are not a complete current screenshot review.', 'Mobile native generation needed one device correction; use corrected MOBILE screen, not the earlier mobile-request DESKTOP.'],
    'renault': ['42 retained assets coexist with22ordinary capture failures, including HTTP403; inspect already-retained actual visible assets and record failures without changing origins or bypassing denial.', 'Earlier desktop/narrow geometry checks do not establish current full-page raster coverage.'],
    'revolut': ['Requested MOBILE output remains DESKTOP; no genuine corresponding mobile canvas is established.', 'Large salary-panel scroll transform uses an observed end state/approximate trigger; current active section references required.'],
    'meta': ['Requested MOBILE output remains DESKTOP; no genuine corresponding mobile canvas is established.', 'Hero character/video timing and navigation are earlier scoped observations; current Canadian public homepage must be freshly inspected.'],
    'mastercard': ['Keep Taiwan zh-Hant reference scope explicit; do not substitute a different country page silently.', 'Cookie preference/embed consent, carousel and custom footer-chevron glyph are unresolved earlier limits.'],
    'binance': ['Initial MOBILE request returned DESKTOP, then actual MOBILE correction exists; retain both and use corrected screen metadata.', 'Remote BinanceNova font and live financial value/marquee/counter states require current visual checks; do not treat old values as live quotes.'],
    'dell-1996': ['Legacy catalog label remains preserved, but current reconstruction scope is Dell Taiwan current public homepage, not a1996 archive.', 'Three hero/seven showcase states and actual media phase need current main-page sampling; do not operate purchase/account services.'],
    'nintendo-2001': ['Legacy catalog label remains preserved, but current scope is Nintendo Canada current public homepage, not a2001 archive.', 'No genuine earlier official390px source; local mobile iframe/adaptation is explicitly not official mobile evidence.'],
    'theverge': ['No genuine earlier official390px source: direct narrow load failed without established cause, and local mobile iframe is not official evidence.', 'Earlier desktop has16px height/shelf difference; dated editorial feed and variable ads require fresh references.'],
    'wired': ['No independent earlier official narrow reference and no retained local screenshot file/hash: capture submission timed out.', 'Raw asset manifests include analytics pixels; keep raw manifests private and verify actual publication dependency membership before source reuse.'],
    'pinterest': ['Earlier390px desktop-UA browser retained800px content clipped at390; this is not a verified responsive390px homepage.', 'Only genuine DESKTOP Stitch output exists; exact mobile generation and real responsive/source behavior remain unresolved.'],
    'vodafone': ['Existing DESKTOP screen came from MOBILE request; one correction produced actual MOBILE, but dedicated desktop layout generation/correction remains an earlier stated gap.', 'Four earlier narrow carousel-heading offsets remain; original media and main-page states need fresh current actual review.'],
}


def read(file):
    return json.loads(file.read_text())


def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


cache = {}
def digest(name):
    if name not in cache:
        file = WORK / name
        cache[name] = dict(path=name, exists=file.is_file())
        if file.is_file():
            data = file.read_bytes()
            cache[name].update(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
    return dict(cache[name])


def local_name(row):
    name = row.get('path') or row.get('local') or row.get('local_path')
    if not isinstance(name, str):
        return None
    file = Path(name)
    if file.is_absolute():
        try:
            return str(file.relative_to(WORK))
        except ValueError:
            return None
    return name.removeprefix('.stitch-work/current-official/')


def failure_summary(row):
    url = row.get('url') or row.get('source_url') or ''
    parts = urlsplit(url)
    reason = str(row.get('reason') or row.get('error') or '')
    status = row.get('status') or row.get('http_status')
    if status == 403 or 'HTTP 403' in reason:
        category = 'ordinary_http_403_recorded_do_not_bypass'
    elif 'TypeError: Failed to fetch' in reason:
        category = 'browser_asset_fetch_failure_not_itself_proof_of_server_denial'
    else:
        category = 'other_recorded_capture_failure'
    return dict(origin=parts.scheme + '://' + parts.netloc if parts.netloc else '', path=parts.path,
                query_omitted=True, status=status, category=category)


progress = read(WORK / 'progress.json')
catalog = {item['slug']: item for item in read(ROOT / 'assets/catalog.json')['designs']}
plan = {item['brand']: item for item in read(ROOT / '.stitch-work/publication-plan.json')['studies']}
records = []
for brand in BRANDS:
    item = progress[brand]
    review_file = WORK / (item.get('review') or brand + '-review.json')
    review = read(review_file) if review_file.exists() else {}
    project = item.get('stitch_project') or review.get('native_stitch', {}).get('project')
    native_files = [file for file in WORK.glob(brand + '-*.json')
                    if any(term in file.name for term in ['stitch', 'native-export', 'provenance'])
                    and not any(term in file.name for term in ['asset-bundle', 'browser-export', 'reference'])]
    metadata, screen_ids, native_exports = {}, set(), {}
    for file in native_files:
        data = read(file)
        metadata[file.name] = digest(file.name)
        text = file.read_text()
        screen_ids.update(re.findall(r'projects/\d+/screens/[A-Za-z0-9_-]+', text))
        for row in walk(data):
            screen = row.get('name') or row.get('screen')
            device = row.get('deviceType') or row.get('device_type')
            if isinstance(screen, str) and '/screens/' in screen and device:
                metadata.setdefault('screen_metadata', {})[screen] = dict(
                    device_type=device, width=row.get('width'), height=row.get('height'),
                    metadata_dimensions=row.get('metadata_dimensions') or row.get('export_dimensions'))
            name = local_name(row)
            if not name or not name.startswith(brand + '-') or Path(name).suffix not in ['.html', '.png']:
                continue
            if not any(term in name for term in ['native', 'stitch']):
                continue
            native_exports[name] = dict(**digest(name), recorded_sha256=row.get('sha256'))
            if row.get('sha256'):
                native_exports[name]['recorded_hash_matches'] = native_exports[name].get('sha256') == row['sha256']
    for file in WORK.glob(brand + '-*'):
        if file.is_file() and file.suffix in ['.html', '.png'] and any(term in file.name for term in ['native', 'stitch']):
            native_exports.setdefault(file.name, digest(file.name))
    project_ids = set(re.findall(r'projects/(\d+)', project or ''))
    if project_ids:
        screen_ids = {name for name in screen_ids if name.split('/')[1] in project_ids}
    assets, failure_rows, asset_manifests, tracker_rows = {}, [], [], []
    for file in WORK.glob(brand + '-*provenance.json'):
        data = read(file)
        if not isinstance(data, dict) or not isinstance(data.get('assets'), list):
            continue
        asset_manifests.append(digest(file.name))
        for row in data['assets']:
            name = local_name(row)
            if not name:
                continue
            result = dict(**digest(name), recorded_sha256=row.get('sha256'), manifest=file.name)
            if row.get('sha256'):
                result['recorded_hash_matches'] = result.get('sha256') == row['sha256']
            assets[name] = result
            url = row.get('source_url') or row.get('source') or ''
            host = urlsplit(url).netloc
            if any(term in host for term in ['analytics.', 'doubleclick.', 'googletagmanager.', 'facebook.com', 'bat.bing.']):
                tracker_rows.append(dict(path=name, origin_host=host, referenced_by_current_publication=name in plan.get(brand, {}).get('assets', [])))
        for key in ['capture_failures', 'browser_bundle_failures', 'failures']:
            for row in data.get(key, []):
                failure_rows.append(dict(manifest=file.name, **failure_summary(row)))
    actual_rasters = [digest(file.name) for file in WORK.glob(brand + '-*') if file.is_file()
                      and file.suffix in ['.png', '.jpg'] and not any(term in file.name for term in ['native', 'stitch'])]
    current_phases = [file.name for file in WORK.glob(brand + '-oct1*-*phases.json')]
    browser_records = [digest(file.name) for file in WORK.glob(brand + '-*.json')
                       if any(term in file.name for term in ['browser-reference', 'browser-export'])]
    records.append(dict(
        brand=brand, official_reference_url=item.get('reference_url'), previous_observed_at=item.get('observed_at'),
        current_preview=digest(brand + '.html'), previous_progress_status=item.get('status'),
        existing_official_specific_project=project, known_official_specific_screens=sorted(screen_ids),
        primary_desktop_screen=item.get('native_screen'),
        primary_mobile_screen=item.get('native_mobile_screen'),
        actual_mobile_screen_candidates=[name for name, value in metadata.get('screen_metadata', {}).items() if value['device_type'] == 'MOBILE'],
        desktop_screen_candidates=[name for name, value in metadata.get('screen_metadata', {}).items() if value['device_type'] == 'DESKTOP'],
        original_inspired_catalog_project='projects/' + catalog[brand]['preview']['projectId'],
        original_inspired_catalog_screen=catalog[brand]['preview']['screenId'],
        original_catalog_is_not_current_official_reference=True,
        native_export_files=list(native_exports.values()), native_metadata=metadata,
        asset_manifests=asset_manifests, retained_asset_count=len(assets),
        retained_asset_files=list(assets.values()),
        recorded_capture_failures=failure_rows,
        tracking_pixel_records=tracker_rows,
        existing_browser_records=browser_records, saved_non_native_rasters=actual_rasters,
        current_full_phase_records=current_phases,
        old_review_file=digest(review_file.name) if review_file.exists() else None,
        old_remaining_limits=item.get('remaining') or review.get('remaining') or [],
        immediate_gaps=GAPS[brand] + ['Fresh current official desktop/narrow reference, corresponding actual local full-page raster review and current-preview digest binding are required; prior geometry/native/provider output does not suffice.'],
        stale_policy_notes_are_historical_only=True, fresh_network_or_browser_checks_performed=False,
        preview_modified=False, accepted=False, official_consistency_claim=False,
    ))
result = dict(recorded_at_utc=datetime.now(timezone.utc).isoformat(), scope='Read-only on-disk inventory, not current browser verification.',
              count=len(records), native_generation_performed=False, preview_modified=False,
              public_release_performed=False, commit_performed=False, records=records)
target = ROOT / '.stitch-work/remaining-twelve-oct11-inventory.json'
target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
lines = ['# 下一批12頁｜既有原生專案與檔案缺口', '',
         '此檔僅整理磁碟現有紀錄，沒有發出生成、造訪官網、修改預覽、提交或發布。較早的官網取樣不代表10月11日仍相同；舊政策錯誤不代表目前仍被擋。原始74個靈感專案與下列官網專案分開保存。', '',
         '| 品牌 | 既有官網 project | 舊取樣日期 | 原生匯出檔 | 獨立素材／失敗列 | 實際非原生圖 |', '|---|---|---|---:|---:|---:|']
for record in records:
    lines.append(f'| {record["brand"]} | {record["existing_official_specific_project"]} | {record["previous_observed_at"]} | {len(record["native_export_files"])} | {record["retained_asset_count"]}／{len(record["recorded_capture_failures"])} | {len(record["saved_non_native_rasters"])} |')
for record in records:
    lines += ['', '## ' + record['brand'], '', record['official_reference_url'], '',
              'Desktop：`' + str(record['primary_desktop_screen']) + '`；舊record Mobile：`' + str(record['primary_mobile_screen']) + '`。完整已知screen／device與每檔雜湊見同名JSON；不能由檔名推論MOBILE成功。', '']
    lines += ['- ' + value for value in record['immediate_gaps']]
    hash_problems = [row for row in record['retained_asset_files'] + record['native_export_files'] if not row['exists'] or row.get('recorded_hash_matches') is False]
    lines += ['', '素材／匯出缺檔或雜湊差異：' + (json.dumps(hash_problems, ensure_ascii=False) if hash_problems else '此次磁碟檢查未發現（只有已記錄雜湊的檔案可驗證原始完整性）。')]
(ROOT / '.stitch-work/remaining-twelve-oct11-inventory.md').write_text('\n'.join(lines) + '\n')
print(json.dumps(dict(count=len(records),path=str(target),summaries=[dict(brand=r['brand'],project=r['existing_official_specific_project'],screens=len(r['known_official_specific_screens']),assets=r['retained_asset_count'],raw_failure_rows=len(r['recorded_capture_failures']),native_export_files=len(r['native_export_files']),current_full_phase_records=len(r['current_full_phase_records'])) for r in records])))
