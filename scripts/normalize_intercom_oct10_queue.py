"""Normalize the six bounded October 10 records without changing global progress."""
from pathlib import Path
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / '.stitch-work/current-official'
BRANDS = ['ibm', 'mongodb', 'intercom', 'superhuman', 'kraken', 'coinbase']

NOTES = {
    'ibm': {
        'title': 'IBM',
        'design': [
            '加拿大英文官網採用白底、IBM Plex、藍色主按鈕與細分隔線。首屏為「Own your digital future, on your terms」、數位主權說明、兩個 CTA、書本／光纖造型圖片，以及右側新聞。',
            '下方依序為四張推薦卡、Smarter impact、Top enterprise technology、Inside IBM、Stay connected／電子報、深色頁尾。桌面頁尾有品牌、Discover、Connect、Follow、About；390px 窄版使用五列收合項目。',
            '本次實際校正首屏、新聞、推薦圖片與文字、圖片溢位、頁尾分組及窄版收合。窄版 Discover 開合已實際操作並留下截圖。',
        ],
        'remaining': [
            'Latest corrected full page is4161px versus4303px source desktop and7229px versus7740px source narrow. Impact/product/Inside IBM card styling, omitted promotional strip and newsletter composition still differ materially.',
            'The corrected footer preserves observed group/legal links and dark/narrow layout. Newsletter required/privacy text, disabled submit appearance and original cookie-preference service are not fully reproduced.',
            'Native Stitch lower content contains invented claims and remains a preserved provider draft; the source-corrected manual page is the preview.',
        ],
    },
    'mongodb': {
        'title': 'MongoDB',
        'design': [
            '本次官方入口導向 /zh-tw，但實際可見文案為英文。頁首有輪播公告，奶油白底首屏以窄體大標「EVERY WORKLOAD. ANY CLOUD. ONE PLATFORM.」搭配右側真實程式碼圖。',
            '後續區塊以深藍、奶油白交替，包含學習卡、Atlas 使用案例、企業客戶輪播、整合夥伴、代理程式 CTA 及深色多欄頁尾。原先深藍置中選擇器版型已過時。',
            '全頁截圖查出企業客戶輪播保留 opacity-inc00 初始隱藏狀態，已用原內容與原資產改為靜態可見。另移除頂部 noscript 解析殘留文字，並恢復桌面最後 CTA 的原始 compass.svg；最新桌面與窄版全頁已逐段確認這三項修正。',
        ],
        'remaining': [
            'Latest5637... root screenshots cover10desktop/11narrow phases with complete current-hash coverage. Actual inspection confirms customer logos/quotes restored, escaped-noscript leading text absent, and exact original compass illustration visible in the desktop CTA while original narrow hiding is retained.',
            'Latest desktop height6503 vs6519 source (-16px); narrow8597 equals source. The prior45px narrow offset came from the now-removed leading text row, not solely announcement state. Official/local customer-carousel selections and partner-marquee order visibly vary; exact phase synchronization and the remaining desktop spacing/opacity differences are unverified.',
            'Navigation expansion, Atlas use-case tabs, customer-carousel transitions and assistant behavior are not implemented or verified.',
        ],
    },
    'intercom': {
        'title': 'Intercom',
        'design': [
            '官網使用奶油白背景、細邊線、Saans 字體、四張裝飾照片與「A complete system for AI and human customer service」。首屏有 Start free trial、View demo，並保留現行多彩 Fin4 橫幅。',
            '主要順序為 Inbox／Copilot2、AI Helpdesk、Fin AI Agent、團隊與 Fin 協作、客戶見證、整合、價格及頁尾。桌面大標80px，390px 窄版40px。',
            '第一次原生指令錯將照片及彩色橫幅移除，已以第二次真實 Stitch 編輯更正；兩次原始指令與輸出均完整保留。實際全頁驗證另發現 Fin 的 Rive 動畫區留白，不能以頁高相同判定一致。',
        ],
        'remaining': [
            'Latest full desktop height9492 matches source; narrow10419 vs10421. These measurements do not establish visual consistency: the first desktop Fin panel under “Train and test Fin to handle complex queries” is visibly blank, and captured source HTML contains an empty lazy-media container.',
            'Fresh root IAB active-source inspection also showed an empty Fin pane, zero canvas/video nodes, and preserved actual screenshot/fragment. Complete React payload identifies the two original Rive assets, now saved with URL/byte/hash provenance. Earlier Chrome source raster showed a visible phase; a working original Rive render or directly captured visible phase remains unverified. No substitute was invented.',
            'The source notification/chat iframe overlay is excluded. Inactive tab images and complete=false SVG candidates are not automatically classified as visible broken images; product tabs, accordions, navigation and service states remain unverified.',
        ],
    },
    'superhuman': {
        'title': 'Superhuman',
        'design': [
            '現行官網為白色導覽與淡紫公告、深色發光 Mail 首屏：「Save4+hours each week with Superhuman Mail」、左側文案／右側真實 Mail 示範，搭配 Mail、Go、Docs 切換。',
            '下方依序有品牌列、Go 助理、Grammarly／Email Assistant／Daily Briefs、客戶見證、Mail 排程、Docs、企業方案、彩色 CTA 與密集深色頁尾。',
            '桌面首屏與全頁高度已對照實際官網取樣；窄版在排程與 Docs 等區塊仍有間距差異，且影片畫格會隨播放時間改變。',
        ],
        'remaining': [
            'Latest desktop full height7320 matches the sampled source. Narrow settled10308 vs10530 source; lower email/scheduling, Docs and enterprise spacing/state differences remain visible.',
            'Public Mail video was observed loaded and playing, but remote video availability, exact frames and transition timing are not fixed or comprehensively verified.',
            'Product-tab transitions, expanded navigation and account flows are unverified.',
        ],
    },
    'kraken': {
        'title': 'Kraken',
        'design': [
            '本次取樣為加拿大英文 /ca、拒絕非必要 Cookie 並關閉地區提示。淡紫首屏為「Own the power of your money」，下方為 Pro、Kraken、Wallet、Krak 深色產品卡。',
            '後續有代理程式工具、20x 槓桿、日期限定行情表、開戶 CTA、法律說明與現行 Payward 頁尾。390px 取樣為窄版桌面 UA，不是實體手機。',
            '實際截圖查出多個卡片只剩背景：原頁把文字與圖片包在初始 --opacity-start:0 的捲動顯示層。已保留原資產與文字，固定為所記錄的最終 opacity／transform；新版桌面與窄版全頁已實際確認產品文字及圖片恢復。',
        ],
        'remaining': [
            'Latest62c3... root screenshots cover10desktop/10narrow phases from top through bottom with no coverage gaps. Actual raster inspection confirms the Pro trading view, Kraken/Wallet phone views, Krak cards, CLI code and20x illustration are visible; the former blank panels are corrected.',
            'Latest desktop settled6722 vs6685 source (+37px); narrow7958 equals source height. Narrow first-screen header/content sits about9px higher and the source email field has a focused outline/password-manager icon absent locally. These captured state differences and exact reveal motion remain explicit.',
            'Visible market prices differ between dated source snapshots; no live market parity is claimed. Public menus/search/locale/product behavior, app-banner dismissal and all account/trading services are unverified.',
        ],
    },
    'coinbase': {
        'title': 'Coinbase',
        'design': [
            '現行加拿大英文 /en-ca 首屏為「Buy. Sell. Trade. Trust.」、淺灰分區與藍色按鈕，接續 Earn more on USDC、Built for Canada、品牌影片、10% APY、Advanced Trade、Coinbase One、信任卡與法律頁尾。',
            '本次可見內文為 USDC3.60%，同頁手機圖片寫3.75%；兩者都保留當日來源樣本，不改寫成新利率。原先 CA$200 宣傳列已不存在；來源其他 boosted-rate 欄位為空值時保持空值，不臆造數字。',
            '第一次原生指令混入通用行情卡與 FAQ，已另送真實 Stitch 校正，保留兩次原始回應。原始 CSSOM 中空 style 標籤的有效規則已補回，以恢復版面。',
        ],
        'remaining': [
            'Latestb842... root screenshots cover11desktop/14narrow phases from top through bottom, with complete current-hash coverage and no visible broken-image/overflow candidates. Actual inspection confirms the hero, USDC, Canada payments, video, staking, Advanced, One, four trust cards, disclosures and full footer are present. Heights7727px/11148px match the sampled source; this is scoped evidence, not full visual acceptance.',
            'Official and local brand-video frames/subtitles differ with timing; narrow first-screen header/content is about10px higher in the latest local capture. Exact motion, region variants, dropdowns and locale controls remain unverified.',
            'Google sign-in stylesheet returned403 and was excluded without retrying. Authentication and all financial/account services are unverified.',
        ],
    },
}


def read(name):
    return json.loads((WORK / name).read_text())


def digest(path):
    data = path.read_bytes()
    return {'path': str(path.relative_to(WORK)), 'bytes': len(data),
            'sha256': hashlib.sha256(data).hexdigest()}


def coverage(brand, role, mode, current_hash):
    stem = f'{brand}-oct10-{role}-{mode}'
    width = 1280 if mode == 'desktop' else 390
    new_stem = f'{brand}-oct10-{role}-{width}'
    if role == 'local' and (WORK / (new_stem + '-phases.json')).exists():
        frames = read(new_stem + '-phases.json')
        capture_hashes = {f.get('draft_sha256') for f in frames}
        capture_hash = next(iter(capture_hashes)) if len(capture_hashes) == 1 else None
        height, covered, gaps = frames[-1]['bodyHeight'], 0, []
        for frame in sorted(frames, key=lambda f: f['scrollY']):
            y = max(0, frame['scrollY'])
            if y > covered + 1: gaps.append([covered, y])
            covered = max(covered, min(height, y + frame['viewport']['height']))
        if covered < height - 1: gaps.append([covered, height])
        return {
            'measurement': new_stem + '-reference.json', 'slices': new_stem + '-phases.json',
            'capture_schema': 'root_iab_phases', 'viewport': frames[0]['viewport'],
            'initial_page_height': frames[0]['bodyHeight'], 'settled_page_height': height,
            'screenshots': len(frames), 'whole_page_covered': not gaps,
            'uncovered_document_y_intervals': gaps,
            'last_scroll_y': frames[-1]['scrollY'],
            'uncovered_bottom_px': max(0, height - frames[-1]['scrollY'] - frames[-1]['viewport']['height']),
            'rect_based_incomplete_or_unloaded_candidates': max(len(f['brokenVisibleImages']) for f in frames),
            'horizontal_overflow_observed': any(f['bodyWidth'] > width for f in frames),
            'image_candidate_note': 'Root visible-image filter returned zero candidates where recorded; actual saved raster inspection is separately documented and remains the visual evidence.',
            'screenshot_files': [f['screenshot'] for f in frames],
            'proves_latest_draft': capture_hash == current_hash,
            'draft_sha256_at_capture': capture_hash,
            'evidence_status': 'current_hash' if capture_hash == current_hash else 'prior_revision_not_latest_proof',
        }
    reference = read(stem + '-reference.json')
    frames = read(stem + '-slices.json')
    last = frames[-1]
    h = last['viewport']['height']
    hashes = {f.get('draft_sha256') for f in frames}
    capture_hash = hashes.pop() if len(hashes) == 1 else None
    record = {
        'measurement': stem + '-reference.json', 'slices': stem + '-slices.json',
        'viewport': frames[0]['viewport'], 'initial_page_height': reference['pageHeight'],
        'settled_page_height': last['height'], 'screenshots': len(frames),
        'whole_page_covered': last['scrollY'] + h >= last['height'] - 1,
        'last_scroll_y': last['scrollY'],
        'uncovered_bottom_px': max(0, last['height'] - last['scrollY'] - h),
        'rect_based_incomplete_or_unloaded_candidates': max(len(f.get('brokenImages', [])) for f in frames),
        'image_candidate_note': 'Rect-only candidates can include offscreen/hidden carousel layers or pending SVGs. They are not a verified count of visible broken images; actual raster review takes precedence.',
        'screenshot_files': [f['file'] for f in frames],
    }
    if role == 'local':
        record.update(proves_latest_draft=capture_hash == current_hash,
                      draft_sha256_at_capture=capture_hash,
                      evidence_status='current_hash' if capture_hash == current_hash else 'prior_revision_not_latest_proof')
    return record


for brand in BRANDS:
    meta = NOTES[brand]
    result_path = WORK / f'{brand}-oct10-result.json'
    result = read(result_path.name)
    preview = digest(WORK / f'{brand}.html')
    result['preview_sha256'] = preview['sha256']
    result['accepted'] = False
    result['official_consistency_claim'] = False
    result['status'] = 'in_visual_review'
    result['remaining_differences_and_limits'] = meta['remaining']
    result['evidence'] = {
        f'{role}_{mode}': coverage(brand, role, mode, preview['sha256'])
        for role in ['official', 'local'] for mode in ['desktop', 'narrow']
    }
    local = [result['evidence'][f'local_{mode}'] for mode in ['desktop', 'narrow']]
    result['latest_draft_actual_render_checked'] = any(x['proves_latest_draft'] for x in local)
    result['latest_draft_full_desktop_and_narrow_coverage'] = all(
        x['proves_latest_draft'] and x['whole_page_covered'] for x in local)
    result['static_visual_acceptance'] = False
    result['browser_blocker'] = {
        'kind': 'browser_connection_policy_loader',
        'scope': 'This subagent connection; root IAB remains available and supplies separately recorded current captures.',
        'root_current_hash_capture_available': result['latest_draft_full_desktop_and_narrow_coverage'],
        'message': 'Fresh scoped Chrome recovered once and enabled new IBM/Intercom/Superhuman/Kraken desktop proof. A later24s evaluation deadline and60s reset were followed by failed known-tab rebind and tab-list requests at the request-header policy loader. No site-specific denial or page result was returned; no alternative control technology/bypass was used.',
        'pending_cleanup': 'Owned Chrome tabs2142948910,2142948923,2142948930 could not be rebound for cleanup; root informed. Last current local override1280x720; earlier tabs may retain390px. Reset temporary per-tab metrics before closing if reconnected.',
    }
    if brand == 'ibm':
        result['corrections'] += [] if any('footer' in x.lower() for x in result['corrections']) else [
            'Rebuilt the observed dark footer, complete group/legal links and390px collapsed rows; actually tested Discover expansion/collapse.']
    for marker in ['static-reveal-correction', 'footer-provenance']:
        f = WORK / f'{brand}-oct10-{marker}.json'
        if f.exists(): result[marker.replace('-', '_')] = f.name
    comparison = WORK / f'{brand}-oct10-latest-layout-review.json'
    if comparison.exists(): result['latest_actual_raster_comparison'] = comparison.name
    inspection = WORK / f'{brand}-oct10-raster-inspection.json'
    if inspection.exists():
        result['actual_raster_inspection'] = inspection.name
        result['actual_raster_inspection_bound_to_current_preview'] = read(inspection.name)['preview_sha256'] == preview['sha256']
    if brand == 'intercom':
        result['original_animation_assets'] = 'intercom-oct10-rive-provenance.json'
        result['additional_official_evidence'] = {
            'screenshot': 'intercom-oct10-fin-active-iab.png',
            'reference': 'intercom-oct10-fin-active-iab-reference.json',
            'scope_note': 'Fresh root IAB active Fin pane at1280x720, scroll3674.5; empty lazy-media slot and zero canvas/video nodes. This evidences an environment rendering limitation, not the expected working Rive appearance.',
        }
    original = []
    for item in result['design_analysis_and_original_prompts']:
        f = ROOT / item['path']
        blob = subprocess.run(['git', 'show', f'HEAD:{item["path"]}'], cwd=ROOT, capture_output=True)
        original.append({'path': item['path'], 'sha256': hashlib.sha256(f.read_bytes()).hexdigest(),
                         'unchanged_from_HEAD': blob.returncode == 0 and blob.stdout == f.read_bytes()})
    result['design_analysis_and_original_prompts'] = original
    design_name = f'{brand}-oct10-design-analysis.md'
    prompts_name = f'{brand}-oct10-rewritten-prompts.md'
    review_name = f'{brand}-oct10-visual-review.md'
    provenance_name = f'{brand}-oct10-provenance.json'
    manifest_name = f'{brand}-oct10-publication-manifest.json'
    (WORK / design_name).write_text(
        f'# {meta["title"]}｜2026-10-10 公開官網設計分析\n\n'
        f'取樣來源：{result["reference_url"]}。{result["locale_note"]}\n\n'
        + '\n\n'.join(meta['design'])
        + '\n\n原有 DESIGN.md、PROMPTS.md 與 STITCH-PROMPT.md 保留；本檔為日期限定補充。'
          '研究頁免費瀏覽，未開啟付費方案或交易；不對外部生成服務的帳戶計費狀態作保證。'
          '\n\n驗證範圍為匿名公開首頁、1280×720 與390×844、DPR1、桌面 UA。'
          '未完成實體手機、其他地區、完整互動或服務驗證；目前 accepted=false，不宣稱與官方一致。\n', encoding='utf8')
    requests = sorted(WORK.glob(f'{brand}-oct10-stitch-*request.json'),
                      key=lambda f: ('visual-correction' in f.name, f.name))
    blocks = [f'# {meta["title"]}｜本次送交 Google Stitch MCP 的重寫指令\n\n'
              '以下保留實際送出的完整指令，原始請求／回應與原始下載另存。生成預覽不能替代瀏覽器實際畫面驗證。\n']
    if brand in ['intercom', 'coinbase']:
        blocks.append('第一輪指令含有與當日官網不符的描述，已由第二輪 visual-correction 指令更正。第一輪僅供追溯，不能用作現行設計依據。\n')
    for request in requests:
        q = read(request.name)
        blocks.append(f'## {request.name}\n\nProject: `{q["projectId"]}`；Device: `{q["deviceType"]}`；Selected screens: `{", ".join(q["selectedScreenIds"])}`\n\n```text\n{q["prompt"]}\n```\n')
    blocks.append('## 後續實際校正規則\n\n以當日公開官網的實際截圖、完整 DOM、有效 CSSOM 與原始公開資產為依據；不得加入原頁沒有的數字、區塊或圖片。保留原生 Stitch 原始輸出，將衍生修正另存。每次修改後必須以對應檔案雜湊重新檢查桌面及390px 窄版，逐項記錄圖片、版面、文字、導覽與剩餘差異。頁高相同或生成圖片相似不代表官網一致。\n')
    (WORK / prompts_name).write_text('\n'.join(blocks), encoding='utf8')
    table = ['| 實際取樣 | 頁高 | 全頁覆蓋 | 對應目前重製檔 |', '|---|---:|---|---|']
    for key, evidence in result['evidence'].items():
        table.append(f'| {key} | {evidence["settled_page_height"]} | {"是" if evidence["whole_page_covered"] else "否"} | '
                     + ('官方取樣' if key.startswith('official') else ('是' if evidence['proves_latest_draft'] else '否；較早修訂')) + ' |')
    (WORK / review_name).write_text(
        f'# {meta["title"]}｜2026-10-10 畫面校正紀錄\n\n'
        f'來源：{result["reference_url"]}。目前重製檔 SHA-256：`{preview["sha256"]}`。\n\n'
        '**accepted=false；尚不宣稱與官方一致。** 已透過原生 Google Stitch MCP 編輯並保留完整輸出，再依當日來源具體校正。\n\n'
        + '\n'.join(table) + '\n\n'
        + '\n\n'.join(meta['remaining'])
        + '\n\n全頁概覽由已保存的實際瀏覽器分段截圖拼接，只用於比較；部分為較早修訂並有明確標籤。'
          '圖片候選數僅為矩形與載入狀態檢查，包含隱藏輪播層，不能當作可見破圖數。'
          '導覽連結已保留公開目的地，未提交帳戶、預約、電子報、付款或交易。'
          '\n\n本子代理的瀏覽器連線政策載入器失敗；主代理已用可用的 IAB 補拍，是否對應目前檔案以表中雜湊綁定為準。未繞過來源安全限制。\n', encoding='utf8')
    result['current_supplements'] = {'design_analysis': design_name, 'rewritten_prompts': prompts_name,
                                     'visual_review': review_name, 'provenance': provenance_name,
                                     'publication_manifest': manifest_name}
    current_evidence = sorted({name for e in result['evidence'].values()
                               for name in [e['measurement'], e['slices'], *e['screenshot_files']]})
    work_files = sorted(f.name for f in WORK.glob(f'{brand}-oct10-*') if f.is_file()
                        and any(token in f.name for token in ['asset-bundle', 'source.html',
                            'reference-unfiltered', 'official-1280-reference', 'official-390-reference',
                            'pre-footer', 'pre-static', 'pre-noscript', 'pre-cta-image', 'stitch-correction-response', 'stitch-visual-correction-response']))
    native_files = [f for f in result['native_stitch']['requests_and_outputs'] if f.endswith(('.html', '.png'))]
    manifest = {
        'brand': brand, 'accepted': False, 'official_consistency_claim': False,
        'preview': preview, 'study_text': [design_name, prompts_name, review_name],
        'public_asset_manifest': result['public_assets']['manifest'],
        'native_original_exports': native_files,
        'native_export_note': 'Preserved provider drafts, not browser QA or a claim of official consistency.',
        'evidence_references': current_evidence,
        'comparison_overview': f'{brand}-oct10-comparison-overview.png',
        'diagnostic_comparison_contact_sheets': sorted(f.name for f in WORK.glob(f'{brand}-oct10-latest-*-review-*.jpg')),
        'private_work_files_do_not_stage': work_files,
        'publication_instructions': 'Publish only selected study artifacts and required preview assets after root integration. Do not recursively stage the raw work folder or asset-bundle directories. Raw HTML/DOM/network bundles may contain irrelevant tracking state and are retained privately for provenance. Preserve original exports and analyses. Mark all unresolved or stale-hash scopes explicitly.',
    }
    (WORK / manifest_name).write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    hash_files = {f'{brand}.html', *current_evidence, *work_files, design_name, prompts_name, review_name, manifest_name,
                  result['public_assets']['manifest'], f'{brand}-oct10-comparison-overview.png',
                  *result['native_stitch']['requests_and_outputs']}
    for marker in ['static-reveal-correction', 'footer-provenance', 'style-normalization', 'build-record']:
        f = WORK / f'{brand}-oct10-{marker}.json'
        if f.exists(): hash_files.add(f.name)
    for marker in ['noscript-text-correction', 'cta-image-correction', 'latest-layout-review', 'raster-inspection']:
        f = WORK / f'{brand}-oct10-{marker}.json'
        if f.exists(): hash_files.add(f.name)
    for f in WORK.glob(f'{brand}-oct10-*-review-*.jpg'):
        hash_files.add(f.name)
    for f in WORK.glob(f'{brand}-oct10-prior-*-raster-inspection.json'):
        hash_files.add(f.name)
    for marker in ['footer-narrow-expanded.png', 'image-check.json']:
        f = WORK / f'{brand}-oct10-{marker}'
        if f.exists(): hash_files.add(f.name)
    if brand == 'intercom':
        hash_files.update(['intercom-oct10-rive-provenance.json',
                          'intercom-oct10-fin-active-iab.png',
                          'intercom-oct10-fin-active-iab-reference.json'])
        hash_files.update(x['path'] for x in read('intercom-oct10-rive-provenance.json')['assets'] if 'path' in x)
    hashes = [digest(WORK / name) for name in sorted(hash_files) if (WORK / name).is_file()]
    provenance = {
        'brand': brand, 'reference_url': result['reference_url'], 'observed_at': result['observed_at'],
        'scope': result['scope'], 'native_stitch': result['native_stitch'],
        'download_note': 'Native HTML/PNG bytes were downloaded from successful provider response URLs and retained unchanged; full responses preserve their URL provenance. Provider images are not browser evidence.',
        'original_analysis_and_prompts': original, 'source_assets': result['public_assets'],
        'current_preview': preview, 'browser_evidence': result['evidence'], 'hashes': hashes,
        'private_raw_retention': work_files, 'publication_manifest': manifest_name,
    }
    (WORK / provenance_name).write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + '\n')
    result['hashes'] = hashes + [digest(WORK / provenance_name)]
    result['proposed_progress_updates'].update(
        accepted=False, status='in_visual_review', remaining=meta['remaining'],
        review_note='已依10月10日公開官網透過原生Stitch生成並具體校正；新版實際取樣、可見缺漏與互動限制逐項保留，未宣稱與官方一致。')
    result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'brand': brand, 'sha256': preview['sha256'],
                      'latest_full_both': result['latest_draft_full_desktop_and_narrow_coverage'],
                      'accepted': False, 'hashes': len(result['hashes'])}))
