"""Write Clay Global supplements from root-owned evidence; never claim unviewed parity."""
from pathlib import Path
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / '.stitch-work/current-official'


def read(name):
    return json.loads((WORK / name).read_text())


def hashed(name):
    file = WORK / name
    data = file.read_bytes()
    return {'path': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def frame_scope(role, width):
    stem = f'clay-oct10-{role}-{width}'
    frames = read(stem + '-phases.json')
    intervals = sorted((max(0, f['scrollY']), min(f['bodyHeight'], f['scrollY'] + f['viewport']['height'])) for f in frames)
    end, gaps = 0, []
    for start, stop in intervals:
        if start > end + 1: gaps.append([end, start])
        end = max(end, stop)
    height = frames[-1]['bodyHeight']
    if end < height - 1: gaps.append([end, height])
    bound = role == 'local' and all(f.get('draft_sha256') == preview['sha256'] for f in frames)
    return {
        'measurement': stem + '-reference.json', 'phases': stem + '-phases.json',
        'viewport': frames[0]['viewport'], 'settled_page_height': height,
        'screenshots': len(frames), 'whole_page_covered': not gaps,
        'uncovered_document_y_intervals': gaps,
        'rect_based_visible_broken_candidates': max(len(f['brokenVisibleImages']) for f in frames),
        'horizontal_overflow_observed': any(f['bodyWidth'] > f['viewport']['width'] for f in frames),
        'screenshot_files': [f['screenshot'] for f in frames],
        'proves_latest_draft': bound if role == 'local' else None,
        'draft_sha256_at_capture': preview['sha256'] if bound else None,
        'capture_binding_note': 'Root owns actual visual inspection. Latest local phase records embed the current preview hash.' if bound else 'Official-source evidence or no current-preview hash binding.',
    }


preview = hashed('clay.html')
comparison = read('clay-oct10-layout-comparison.json')
max_narrow_heading_delta = max((abs(x['local'] - x['official']) for x in comparison['390']['headingDifferences'] if x['property'] == 'y'), default=0)
evidence = {f'{role}_{"desktop" if width == 1280 else "narrow"}': frame_scope(role, width)
            for role in ['official', 'local'] for width in [1280, 390]}
full_latest = all(evidence[f'local_{mode}']['whole_page_covered'] and evidence[f'local_{mode}']['proves_latest_draft'] for mode in ['desktop', 'narrow'])
response = read('clay-oct10-stitch-response.json')['structuredContent']
screen = [s for block in response['outputComponents'] for s in block.get('design', {}).get('screens', [])][0]
native = {
    'project': 'projects/' + response['projectId'],
    'current_screen': f'projects/{response["projectId"]}/screens/{screen["id"]}',
    'requests_and_outputs': ['clay-oct10-reproduction-prompt.md', 'clay-oct10-stitch-response.json',
                             'clay-oct10-download-manifest.json', 'clay-oct10-stitch-raw-0.html',
                             'clay-oct10-stitch-raw-0.png'],
    'original_exports_preserved': True, 'provider_images_are_not_browser_QA': True,
    'provider_claims_not_adopted': 'The provider title/descriptions use “Official” and “verified”; these are retained raw provider text, not the study’s conclusion. The study is unofficial and accepted=false.',
}
original = []
for name in ['DESIGN.md', 'PROMPTS.md', 'STITCH-PROMPT.md']:
    path = ROOT / 'design-md/clay' / name
    blob = subprocess.run(['git', 'show', f'HEAD:design-md/clay/{name}'], cwd=ROOT, capture_output=True)
    original.append({'path': f'design-md/clay/{name}', 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                     'unchanged_from_HEAD': blob.returncode == 0 and blob.stdout == path.read_bytes(),
                     'historical_brand_note': 'Preserved historical file. DESIGN.md describes Clay.com GTM software and must not be used as the current Clay Global agency reference.'})
remaining = [
    'Root actual review found differences in public video frames, logo/reveal timing and3D states. Desktop hero and fintech artwork use explicitly observed static cropped-region fallbacks; these do not reproduce live3D motion.',
    'The footer3D artwork is missing. Header/menu, service accordions, FAQ, contact actions and other UI behavior have not been fully verified.',
    f'Narrow sampled reveal/heading states differ; recorded heading Y positions differ by up to{max_narrow_heading_delta:g}px. Reveal/timing/static-state effects remain scoped limits; equal total height is not visual acceptance.',
    'Root reviewed all11 earlier final comparison sheets and latest affected top/fintech desktop/narrow sheets after the header-filter/fintech-background corrections. The latest local phases embed the current draft hash. Narrow has17 matched source/local scroll positions and2 unpaired official positions caused by actual smooth-scroll phase; this is not41 exact paired screenshots or pixel parity.',
]
desktop_gap = evidence['local_desktop']['uncovered_document_y_intervals']
if desktop_gap:
    remaining.append('Current saved desktop phase sequence has uncovered document-Y intervals: ' + json.dumps(desktop_gap) + '. A genuine top/remaining screenshot is required before calling coverage complete.')
assets = read('clay-oct10-assets.json')
required = sorted(set(re.findall(r'clay-assets/oct10/[A-Za-z0-9_.-]+', (WORK / 'clay.html').read_text())))
missing = [name for name in required if not (WORK / name).is_file()]
static = [hashed(name) for name in [
    'clay-assets/oct10/observed-hero-3d-phase.png',
    'clay-assets/oct10/observed-fintech-3d-region.png']]
for entry in static:
    entry.update(kind='Observed static cropped-region fallback from root-owned public render',
                 original_download=False, live_3d_motion_verified=False,
                 crop_provenance_note='Owning agent captured the observed region. This supplement preserves bytes/hash; it does not invent an unrecorded source rectangle or claim a live3D export.')

analysis = '''# Clay Global｜2026-10-10 公開官網設計分析

本次來源為 [Clay Global](https://clay.global/)，是品牌與 UX 設計代理公司。既有 DESIGN.md 描述 Clay.com 的 GTM 軟體，已原樣保存作為歷史紀錄；該檔的黏土插畫、多彩 SaaS 卡片與產品導向不能作為本次代理公司官網的依據。

現行頁面以淡暖灰首屏、近黑文字、Universal Sans 字體與大量留白建立層級。導覽包含 Work、Clients、Services、Industries、About、Blog 與黑色 Contact 按鈕。主標為「Clay is a global branding and UX design agency」，桌面取樣64px、行高70.4px、字重740；390px 窄版取樣40px、行高44px。

首屏與 Showreel 接續品牌／服務介紹，再進入「The Future of Finance is Intelligent」特色區及大型作品展示。桌面以兩欄、錯位與大尺寸圖像呈現14個案例，包括 Slack、STC Bank、Sky、Snapchat、Joe & The Juice、Vantara、Grayscale、Discover、Marqeta、Yahoo! Games、Serena & Lily、Tipalti、Wealth、Art Bridges。作品圖像主導色彩，文字與導覽維持克制。

後段依序有設計創新介紹、團隊／辦公室影像、Featured News、FAQ 與 Let’s Talk 聯絡頁尾。當日新聞標題包括 Tipalti Redesign Wins Design Awards and Features、Complete Guide to Buttons in Web Design for2026、Clay Global Shows Up Strong at The Webby Awards2026。這些日期限定內容以保存的官方 DOM／截圖為依據。

本次透過真實 Google Stitch MCP 產生並完整保留原始輸出，再依公開來源、字型與原始圖像／影片校正。主代理的實際畫面檢查仍發現影片、標誌、捲動顯示及3D時間點差異。首屏與 Fintech 使用明示的實際觀察靜態裁切區，頁尾3D仍缺少；互動尚未通過驗證。

**accepted=false，不宣稱與官方一致。** 本補充由子代理整理來源紀錄；實際畫面最終判讀由主代理負責，未將未看過的畫面描述為已驗證。研究內容免費瀏覽，沒有開啟付費方案、提交聯絡表單或執行交易；不對外部生成服務的帳戶計費狀態作保證。
'''
(WORK / 'clay-oct10-design-analysis.md').write_text(analysis, encoding='utf8')
prompt = (WORK / 'clay-oct10-reproduction-prompt.md').read_text().rstrip()
(WORK / 'clay-oct10-rewritten-prompts.md').write_text(
    '# Clay Global｜本次送交 Google Stitch MCP 的完整重寫指令\n\n'
    '以下為保留的實際重製指令。原始回應、HTML、PNG 與下載網址另存，生成預覽不作為實際官網一致性證明。\n\n'
    '```text\n' + prompt + '\n```\n\n'
    '後續校正須以日期限定公開官網的實際畫面與原始資產為依據，明確區分 Clay Global 與 Clay.com。'
    '所有靜態3D取樣須標示來源與限制，不能稱為完整動畫；每次修改後須重新核對對應雜湊的桌面與390px窄版。'
    '頁高相同、內容標題相同或供應商自述已驗證，均不能替代實際畫面驗收。\n', encoding='utf8')
table = ['| 實際證據 | 頁高 | 分段數 | 保存範圍完整 |', '|---|---:|---:|---|']
for key, scope in evidence.items():
    table.append(f'| {key} | {scope["settled_page_height"]} | {scope["screenshots"]} | {"是" if scope["whole_page_covered"] else "否"} |')
(WORK / 'clay-oct10-visual-review.md').write_text(
    '# Clay Global｜2026-10-10 畫面校正紀錄\n\n'
    '來源：https://clay.global/；1280×720 桌面及390×844窄版桌面 UA，匿名公開首頁。'
    '目前重製檔 SHA-256：`' + preview['sha256'] + '`。\n\n'
    '**accepted=false，不宣稱與官方一致。** 實際畫面最終判讀由主代理負責；此補充整理保存的量測與主代理回報，沒有將未檢視的畫面稱為已通過。\n\n'
    + '\n'.join(table) + '\n\n'
    '保存量測中沒有矩形可見破圖候選或橫向溢位，桌面與窄版來源／重製總頁高分別同為15667／15618px。'
          '這些數字只支持所列取樣，不能證明畫面一致。最新本地分段記錄綁定目前重製檔雜湊。主代理檢視11張較早完整對照圖，以及最後修正影響的桌面／窄版頁首與 Fintech 對照。窄版17個捲動位置配對，另2個官方位置因實際平滑捲動時間點未配對，不宣稱41張精確配對或像素一致。詳細幾何差異與接觸圖清單見 clay-oct10-layout-comparison.json；'
    '若目前分段數與該較早比較檔不同，應以最新 phase 清單為範圍紀錄。\n\n'
    + '\n\n'.join(remaining) + '\n', encoding='utf8')
text_files = ['clay-oct10-design-analysis.md', 'clay-oct10-rewritten-prompts.md', 'clay-oct10-visual-review.md']
raw_private = ['clay-oct10-asset-bundle.json', 'clay-oct10-official-1280-reference.json',
               'clay-oct10-official-390-reference.json', 'clay-oct10-local-1280-reference.json',
               'clay-oct10-local-390-reference.json', 'clay-oct10-stitch-response.json']
manifest = {
    'brand': 'clay', 'brand_identity': 'Clay Global agency, clay.global; not Clay.com GTM software',
    'accepted': False, 'official_consistency_claim': False, 'preview': preview,
    'study_text': text_files, 'runtime_required_assets': required, 'missing_required_assets': missing,
    'runtime_asset_bytes': sum((WORK / name).stat().st_size for name in required if (WORK / name).is_file()),
    'original_asset_manifest': 'clay-oct10-assets.json', 'derived_static_assets': static,
    'native_original_exports': ['clay-oct10-stitch-raw-0.html', 'clay-oct10-stitch-raw-0.png'],
    'evidence_phases': [scope['phases'] for scope in evidence.values()],
    'private_work_files_do_not_stage': raw_private,
    'publication_instructions': 'Publish only selected study text/evidence and assets actually referenced by the preview. Preserve historical originals and native exports. Never recursively stage raw DOM, tracking/network bundles or unused media. All unresolved3D/UI and coverage/hash-binding limits must remain explicit.',
}
(WORK / 'clay-oct10-publication-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
hash_names = {'clay.html', 'clay-oct10-layout-comparison.json', 'clay-oct10-assets.json',
              'clay-oct10-build-record.json', 'clay-oct10-publication-manifest.json',
              *native['requests_and_outputs'], *text_files, *raw_private, *required}
for scope in evidence.values():
    hash_names.update([scope['measurement'], scope['phases'], *scope['screenshot_files']])
for entry in comparison.values(): hash_names.update(entry['diagnosticContactSheets'])
hashes = [hashed(name) for name in sorted(hash_names) if (WORK / name).is_file()]
provenance = {
    'brand': 'clay', 'reference_url': 'https://clay.global/', 'observed_at': '2026-10-10',
    'native_stitch': native, 'downloads': read('clay-oct10-download-manifest.json'),
    'original_analysis_and_prompts': original, 'original_asset_manifest': 'clay-oct10-assets.json',
    'derived_static_assets': static, 'current_preview': preview, 'browser_evidence': evidence,
    'visual_inspection_owner': 'root', 'writer_independent_visual_acceptance': False,
    'hashes': hashes, 'private_raw_retention': raw_private,
}
(WORK / 'clay-oct10-provenance.json').write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + '\n')
result = {
    'brand': 'clay', 'brand_identity': 'Clay Global branding and UX design agency',
    'observed_at': '2026-10-10', 'accepted': False, 'official_consistency_claim': False,
    'status': 'in_visual_review', 'reference_url': 'https://clay.global/',
    'scope': {'desktop': {'width': 1280, 'height': 720},
              'narrow': {'width': 390, 'height': 844, 'mobile': False,
                         'description': 'Responsive narrow desktop-UA browser, not a physical phone.'},
              'public_anonymous': True, 'service_actions_performed': False},
    'preview': 'clay.html', 'preview_sha256': preview['sha256'],
    'method': 'Genuine native Stitch followed by root source/asset correction; this supplement attributes actual visual inspection to root and does not claim independent unviewed parity.',
    'native_stitch': native, 'design_analysis_and_original_prompts': original,
    'rewritten_native_instructions': ['clay-oct10-reproduction-prompt.md'],
    'public_assets': {'manifest': 'clay-oct10-assets.json', 'count': len(assets['assets']),
                      'bytes': sum(x.get('bytes', 0) for x in assets['assets']), 'failures': assets['failures'],
                      'derived_static_assets': static},
    'evidence': evidence, 'layout_comparison': 'clay-oct10-layout-comparison.json',
    'visual_inspection_owner': 'root', 'writer_independent_visual_acceptance': False,
    'root_actual_review': 'Root reports viewing all11 earlier final sheets plus latest affected top/fintech desktop/narrow sheets; final local capture phases bind the current preview hash.',
    'latest_draft_actual_render_checked': full_latest,
    'latest_draft_full_desktop_and_narrow_coverage': full_latest,
    'remaining_differences_and_limits': remaining,
    'cost': {'external_purchase_or_paid_plan_started': False, 'study_access_free': True,
             'provider_usage_billing_not_asserted': True},
    'current_supplements': {'design_analysis': text_files[0], 'rewritten_prompts': text_files[1],
                            'visual_review': text_files[2], 'provenance': 'clay-oct10-provenance.json',
                            'publication_manifest': 'clay-oct10-publication-manifest.json'},
    'proposed_progress_updates': {'status': 'in_visual_review', 'accepted': False,
                                 'reference_url': 'https://clay.global/', 'observed_at': '2026-10-10',
                                 'native_screen': native['current_screen'], 'preview': 'clay.html',
                                 'review': 'clay-oct10-result.json',
                                 'review_note': '已依Clay Global代理公司當日公開官網透過原生Stitch及官方素材校正；原Clay.com分析留作歷史，3D／動畫／互動及未完成範圍明列，不宣稱與官方一致。',
                                 'remaining': remaining},
    'hashes': hashes + [hashed('clay-oct10-provenance.json')],
}
(WORK / 'clay-oct10-result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'brand': 'clay', 'sha256': preview['sha256'], 'accepted': False,
                  'evidence_counts': {k: v['screenshots'] for k, v in evidence.items()},
                  'desktop_gaps': desktop_gap, 'required_assets': len(required), 'missing_assets': missing}))
