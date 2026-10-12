"""Normalize Expo records from root-owned, hash-bound final browser evidence."""
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
    data = (WORK / name).read_bytes()
    return {'path': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


preview = hashed('expo.html')
evidence = {}
for role in ['official', 'local']:
    for width, label in [(1280, 'desktop'), (390, 'narrow')]:
        stem = f'expo-oct10-{role}-{width}'
        frames = read(stem + '-phases.json')
        end, gaps = 0, []
        for start, stop in sorted((max(0, x['scrollY']), min(x['bodyHeight'], x['scrollY'] + x['viewport']['height'])) for x in frames):
            if start > end + 1: gaps.append([end, start])
            end = max(end, stop)
        height = frames[-1]['bodyHeight']
        if end < height - 1: gaps.append([end, height])
        current = role == 'local' and all(x.get('draft_sha256') == preview['sha256'] for x in frames)
        evidence[f'{role}_{label}'] = {
            'measurement': stem + '-reference.json', 'phases': stem + '-phases.json',
            'viewport': frames[0]['viewport'], 'settled_page_height': height,
            'screenshots': len(frames), 'whole_page_covered': not gaps,
            'uncovered_document_y_intervals': gaps,
            'rect_based_visible_broken_candidates': max(len(x['brokenVisibleImages']) for x in frames),
            'horizontal_overflow_observed': any(x['bodyWidth'] > x['viewport']['width'] for x in frames),
            'screenshot_files': [x['screenshot'] for x in frames],
            'proves_latest_draft': current if role == 'local' else None,
            'draft_sha256_at_capture': preview['sha256'] if current else None,
        }
comparison = read('expo-oct10-layout-comparison.json')
response = read('expo-oct10-stitch-response.json')['structuredContent']
screen = [s for x in response['outputComponents'] for s in x.get('design', {}).get('screens', [])][0]
native = {
    'project': 'projects/' + response['projectId'],
    'current_screen': f'projects/{response["projectId"]}/screens/{screen["id"]}',
    'requests_and_outputs': ['expo-oct10-reproduction-prompt.md', 'expo-oct10-stitch-response.json',
                             'expo-oct10-download-manifest.json', 'expo-oct10-stitch-raw-0.html',
                             'expo-oct10-stitch-raw-0.png'],
    'original_exports_preserved': True, 'provider_images_are_not_browser_QA': True,
    'provider_claims_not_adopted': 'Raw provider descriptions are provenance, not official consistency acceptance.',
}
originals = []
for name in ['DESIGN.md', 'PROMPTS.md', 'STITCH-PROMPT.md']:
    file = ROOT / 'design-md/expo' / name
    old = subprocess.run(['git', 'show', f'HEAD:design-md/expo/{name}'], cwd=ROOT, capture_output=True)
    originals.append({'path': f'design-md/expo/{name}', 'sha256': hashlib.sha256(file.read_bytes()).hexdigest(),
                      'unchanged_from_HEAD': old.returncode == 0 and old.stdout == file.read_bytes()})
remaining = [
    'The metallic SDK canvas motion is absent; the underlying original static Expo artwork remains. A44px footer canvas gradient is missing.',
    'Hero app-icon ribbon, native-code carousel, testimonials and dark CTA orb phases are not synchronized with the source. The official desktop phase8 usage/community reveal was blank while the local static content was visible.',
    'Building blocks preserves the sampled active pause icon, but pause/tab behavior is unverified. Menus, theme controls, account/contact/services, real devices and deployed-site behavior are unverified.',
    'Desktop one recorded heading has a20px Y difference; narrow heading geometry has no recorded differences. Equal page height and matching heading geometry do not establish visual consistency.',
]
analysis = '''# Expo｜2026-10-10 公開官網設計分析

來源為 [Expo 官方公開首頁](https://expo.dev/)。本次主標已改為「Agentic mobile infrastructure」，以近黑底、Inter 字體、灰白文字及白色膠囊按鈕建立層級。桌面與390px窄版主標皆取樣48px、行高52.8px、字重600。既有設計分析與原始指令保留，本檔補充當日實際頁面。

桌面首屏左側有 New／Try Observe 提示、主標、四行介紹、Get started 與 Talk to our team；右側為白色圓角 Expo 圖示及向外放射的細線。下方有應用程式圖示列。窄版將圖像與文字堆疊，導覽收合；本次窄版為桌面 UA 的390px響應式測試，不是實體手機。

主要順序為 Building blocks for agentic workflows、SDK／MCP／原生程式碼卡、Infrastructure for your apps，再到裝置支援、即時更新、代理模擬器、App Store Launch、觀測與 Workflows 等圖文區塊。淺色產品圖卡、灰色細分隔線與深色留白交替，沒有套用通用 SaaS 價格卡。

後段保留當日使用量與社群文案、Build beautiful native apps、信任標誌、多欄頁尾、電子報／狀態／主題控制。數字為當日公開來源樣本，不作為持續更新的指標。原始官方圖像與字型已保存；真實 Google Stitch MCP 的原始 HTML、PNG、完整回應及下載網址也另存。

主代理已實際檢視全部7張桌面／窄版對照接觸圖與原生 Stitch 圖。最新檔案有對應雜湊的12段桌面、14段窄版完整取樣，頁高8436／10998px；保存檢查沒有可見破圖候選或橫向溢位。這些只證明所列檢查範圍，不能用來宣稱畫面完全一致。

**accepted=false，不宣稱與官方一致。** 金屬 SDK 動畫、44px頁尾 Canvas 漸層、圖示列／程式碼輪播／見證／CTA 球體時間點，以及選單、主題與暫停互動仍未通過驗證。此補充由子代理整理紀錄，實際畫面判讀屬主代理，沒有將未看過的畫面宣稱已驗收。

研究內容免費瀏覽，沒有開啟付費方案、提交表單或執行交易；不對外部生成服務的帳戶計費狀態作保證。
'''
(WORK / 'expo-oct10-design-analysis.md').write_text(analysis, encoding='utf8')
prompt = (WORK / 'expo-oct10-reproduction-prompt.md').read_text().rstrip()
(WORK / 'expo-oct10-rewritten-prompts.md').write_text(
    '# Expo｜本次送交 Google Stitch MCP 的完整重寫指令\n\n'
    '以下為保留的實際指令；原始輸出另存。生成畫面與供應商自述不能替代實際瀏覽器驗證。\n\n'
    '```text\n' + prompt + '\n```\n\n'
    '後續校正應使用當日公開官網的原始圖像、字型與實際版面，避免沿用舊版 native apps 宣傳主標。'
    '保留原始 Stitch 輸出，將校正檔與日期／視窗／雜湊分開記錄；動畫、互動與尚未完成的範圍必須明列。\n', encoding='utf8')
table = ['| 實際取樣 | 頁高 | 分段數 | 全頁覆蓋 | 對應目前檔案 |', '|---|---:|---:|---|---|']
for key, entry in evidence.items():
    table.append(f'| {key} | {entry["settled_page_height"]} | {entry["screenshots"]} | {"是" if entry["whole_page_covered"] else "否"} | '
                 + ('官方取樣' if key.startswith('official') else ('是' if entry['proves_latest_draft'] else '否')) + ' |')
(WORK / 'expo-oct10-visual-review.md').write_text(
    '# Expo｜2026-10-10 畫面校正紀錄\n\n'
    '來源：https://expo.dev/。目前重製檔 SHA-256：`' + preview['sha256'] + '`。\n\n'
    '**accepted=false，不宣稱與官方一致。** 主代理已實際檢視全部7張對照接觸圖及原生 Stitch 圖；'
    '本補充整理保存證據，沒有宣稱子代理獨立檢視了未觀看的畫面。\n\n'
    + '\n'.join(table) + '\n\n'
    '桌面12個、窄版14個保存捲動位置均與來源對應；量測沒有可見破圖候選或橫向溢位。'
    '詳細幾何與對照圖清單見 expo-oct10-layout-comparison.json。\n\n'
    + '\n\n'.join(remaining) + '\n', encoding='utf8')
text_files = ['expo-oct10-design-analysis.md', 'expo-oct10-rewritten-prompts.md', 'expo-oct10-visual-review.md']
assets = read('expo-oct10-assets.json')
required = sorted(set(re.findall(r'expo-assets/oct10/[A-Za-z0-9_.-]+', (WORK / 'expo.html').read_text())))
missing = [name for name in required if not (WORK / name).is_file()]
private = ['expo-oct10-asset-bundle.json', 'expo-oct10-official-1280-reference.json',
           'expo-oct10-official-390-reference.json', 'expo-oct10-local-1280-reference.json',
           'expo-oct10-local-390-reference.json', 'expo-oct10-stitch-response.json']
manifest = {'brand': 'expo', 'accepted': False, 'official_consistency_claim': False,
            'preview': preview, 'study_text': text_files, 'runtime_required_assets': required,
            'missing_required_assets': missing, 'original_asset_manifest': 'expo-oct10-assets.json',
            'native_original_exports': ['expo-oct10-stitch-raw-0.html', 'expo-oct10-stitch-raw-0.png'],
            'evidence_phases': [entry['phases'] for entry in evidence.values()],
            'private_work_files_do_not_stage': private,
            'publication_instructions': 'Publish selected study/evidence files and actually referenced assets only. Preserve native exports and historical analyses. Do not recursively stage raw DOM, network/tracking bundles or unused media. Preserve all unresolved motion/UI/deployment limits.'}
(WORK / 'expo-oct10-publication-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
hash_names = {'expo.html', 'expo-oct10-layout-comparison.json', 'expo-oct10-assets.json',
              'expo-oct10-build-record.json', 'expo-oct10-publication-manifest.json',
              *native['requests_and_outputs'], *text_files, *private, *required}
for entry in evidence.values(): hash_names.update([entry['measurement'], entry['phases'], *entry['screenshot_files']])
for entry in comparison.values(): hash_names.update(entry['diagnosticContactSheets'])
hashes = [hashed(name) for name in sorted(hash_names) if (WORK / name).is_file()]
provenance = {'brand': 'expo', 'reference_url': 'https://expo.dev/', 'observed_at': '2026-10-10',
              'native_stitch': native, 'downloads': read('expo-oct10-download-manifest.json'),
              'original_analysis_and_prompts': originals, 'original_asset_manifest': 'expo-oct10-assets.json',
              'current_preview': preview, 'browser_evidence': evidence, 'visual_inspection_owner': 'root',
              'writer_independent_visual_acceptance': False, 'hashes': hashes, 'private_raw_retention': private}
(WORK / 'expo-oct10-provenance.json').write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + '\n')
full_latest = all(evidence[f'local_{mode}']['whole_page_covered'] and evidence[f'local_{mode}']['proves_latest_draft'] for mode in ['desktop', 'narrow'])
result = {'brand': 'expo', 'observed_at': '2026-10-10', 'accepted': False, 'official_consistency_claim': False,
          'status': 'in_visual_review', 'reference_url': 'https://expo.dev/',
          'scope': {'desktop': {'width': 1280, 'height': 720}, 'narrow': {'width': 390, 'height': 844,
                    'mobile': False, 'description': 'Responsive narrow desktop-UA browser, not a physical phone.'},
                    'public_anonymous': True, 'service_actions_performed': False},
          'preview': 'expo.html', 'preview_sha256': preview['sha256'],
          'method': 'Genuine native Stitch followed by root source/asset correction and actual final raster review; this supplement attributes visual inspection to root.',
          'native_stitch': native, 'design_analysis_and_original_prompts': originals,
          'rewritten_native_instructions': ['expo-oct10-reproduction-prompt.md'],
          'public_assets': {'manifest': 'expo-oct10-assets.json', 'count': len(assets['assets']), 'failures': assets['failures']},
          'evidence': evidence, 'layout_comparison': 'expo-oct10-layout-comparison.json',
          'visual_inspection_owner': 'root', 'writer_independent_visual_acceptance': False,
          'root_actual_review': 'Root reports viewing all7 saved diagnostic comparison JPEGs and the native PNG.',
          'latest_draft_actual_render_checked': full_latest,
          'latest_draft_full_desktop_and_narrow_coverage': full_latest,
          'remaining_differences_and_limits': remaining,
          'cost': {'external_purchase_or_paid_plan_started': False, 'study_access_free': True,
                   'provider_usage_billing_not_asserted': True},
          'current_supplements': {'design_analysis': text_files[0], 'rewritten_prompts': text_files[1],
                                 'visual_review': text_files[2], 'provenance': 'expo-oct10-provenance.json',
                                 'publication_manifest': 'expo-oct10-publication-manifest.json'},
          'proposed_progress_updates': {'status': 'in_visual_review', 'accepted': False,
              'reference_url': 'https://expo.dev/', 'observed_at': '2026-10-10',
              'native_screen': native['current_screen'], 'preview': 'expo.html', 'review': 'expo-oct10-result.json',
              'review_note': '已依當日Agentic mobile infrastructure官網透過原生Stitch與官方素材校正，桌面與窄版完整實際取樣對應目前雜湊；動畫、互動及部署驗證未完成，不宣稱與官方一致。',
              'remaining': remaining},
          'hashes': hashes + [hashed('expo-oct10-provenance.json')]}
(WORK / 'expo-oct10-result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'brand': 'expo', 'sha256': preview['sha256'], 'latest_full_both': full_latest,
                  'accepted': False, 'required_assets': len(required), 'missing_assets': missing}))
