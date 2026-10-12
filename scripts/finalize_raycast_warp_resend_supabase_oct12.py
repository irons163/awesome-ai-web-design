#!/usr/bin/env python3
"""Finalize actually viewed Oct12 current-preview evidence; never retag old captures."""
import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / '.stitch-work/current-official'
BRANDS = ('raycast', 'warp', 'resend', 'supabase')
NOW = datetime.now(timezone.utc).isoformat()


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(name):
    return json.loads((BASE / name).read_text())


def write(name, value):
    (BASE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


NOTES = {
    'raycast': {
        'desktop': 'All23 complete current viewport frames and8 dated-source comparison segments viewed. Header, Clipboard History launcher, extension cards, AI section, community, six technical illustrations, keyboard, footer and restored Subscribe label are visible. Hero WebGL is blank locally; AI Extensions, snippets, hotkeys and SVG frames differ from the moving source.',
        'narrow': 'All19 complete current viewport frames and8 dated-source comparison segments viewed. Final Window Management launcher state differs from source Clipboard History; fixed Granola/Things reply adds26px total height relative to dated source and shifts some sequential-composite sections by about51.5px around changing demo heights. Footer Subscribe is visible in the current complete sequence. No broken-image placeholder or horizontal page overflow observed.',
        'fresh': 'Fresh official desktop top shows the red WebGL hero absent locally; desktop DOM height15992 vs current15991. Fresh narrow top was captured during initial fade/lazy initialization at height14051; its temporarily absent shortcuts section is not evidence of a design removal. Fresh source is top-only, dated full-source evidence remains separately timed.',
    },
    'warp': {
        'desktop': 'All14 complete current viewport frames and5 dated-source comparison segments viewed. Factory grid, configuration YAML, SDLC,96%/1.00X/+3.7 metrics, enterprise cards, layers, cost-per-PR chart, illustrative computer-use state, product cards, FAQ and footer visible. The final chart has no extra frame. Live task states, logo marquee, reveal opacity and illustrated browser state differ.',
        'narrow': 'All17 complete current viewport frames and8 dated-source comparison segments viewed. Stacked configuration, quality cards, enterprise cards, four layers, no-frame cost chart, captured computer-use story, three product cards, FAQs and full footer visible. Source headings were mid-fade in several dated phases; local headings are static. Current chart-only historical supplement is superseded by this SHA-bound complete capture, without editing its original metadata.',
        'fresh': 'Fresh official desktop/narrow top has the same main heading, responsive layout and measured page heights as current. Factory task-grid positions, active/shipped counts and reveal timing visibly differ; no timing or service parity is accepted.',
    },
    'resend': {
        'desktop': 'All17 complete current viewport frames and7 dated-source comparison segments viewed. Headline, customer logos, SDK/code panel, test/webhook demos, editor, contacts, React email preview, deliverability features, dashboard, testimonials, end CTA and footer visible. Current floor/light-ray originals load where dated official capture had pending requests. React code-pane internal scroll, icon/video frames and marquee positions differ.',
        'narrow': 'All17 complete current viewport frames and8 dated-source comparison segments viewed. Cube poster, title, logos, SDK panel, demos, editor white initial body, React preview, deliverability list, testimonial, dashboard, end CTA and full footer visible. The source blur/header band differs from the documented readable static header correction; videos/cube/marquee phases are frozen or different.',
        'fresh': 'Fresh official narrow DOM says Integrate this morning; current preview retains captured Integrate this weekend. Fresh narrow top cube orientation differs but hero text/layout align. Fresh official desktop observation timed out; no fresh desktop source screenshot or full fresh source traversal is claimed. The original desktop source date remains2026-10-10.',
    },
    'supabase': {
        'desktop': 'All11 complete current viewport frames and4 dated-source comparison segments viewed. Product grid, twelve-logo band, dashboard, React panel, six templates, five customer cards, community,111.2K graphic, CTA, security marks and full footer visible. Dashboard video shows an empty-table frame while source shows populated rows; community carousel positions differ. Repeated sticky headers in the derived sequence composite are capture overlaps, not duplicate page nodes.',
        'narrow': 'All12 complete current viewport frames and5 dated-source comparison segments viewed. Stacked product cards, logos, dashboard, React code, all templates, Lovable open customer card, community, GitHub graphic, security and two-column full footer visible. Local community avatars load where dated source requests were pending. No broken image or horizontal page overflow observed.',
        'fresh': 'Fresh official desktop/narrow top text and hero/card geometry visually align. Fresh desktop page height7691 equals current; fresh narrow top DOM height9807 vs current9819 (+12px). No complete fresh official traversal was performed, so this residual current-source height difference is not represented as exact latest full-page geometry parity.',
    },
}

for brand in BRANDS:
    html = BASE / f'{brand}.html'
    current_sha = digest(html)
    coverage = read(f'{brand}-oct12-current-coverage.json')
    assert coverage['previewSha256'] == current_sha
    result_name = f'{brand}-oct10-result.json'
    build_name = f'{brand}-oct10-build-record.json'
    result = read(result_name)
    build = read(build_name)
    lineage = read(f'{brand}-oct12-evidence-lineage.json')
    lineage_sha = digest(BASE / f'{brand}-oct12-evidence-lineage.json')
    # Keep the honest intermediate audit and its false-at-that-time flags as history.
    for name, value in [(f'{brand}-oct12-result-historical-lineage.json', result),
                        (f'{brand}-oct12-build-record-historical-lineage.json', build)]:
        if not (BASE / name).exists():
            write(name, value)
    analysis = BASE / f'{brand}-oct10-analysis.md'
    analysis_backup = BASE / f'{brand}-oct12-analysis-historical-lineage.md'
    if not analysis_backup.exists():
        analysis_backup.write_bytes(analysis.read_bytes())

    historical_checks = copy.deepcopy(result['checks'])
    for scope in lineage['scopes']:
        assert digest(BASE / scope['historicalPhaseFile']) == scope['historicalPhaseFileSha256']

    current_checks, viewed_frames, viewed_sheets, comparisons, fresh_pairs = [], [], [], [], []
    for rec, historical in zip(coverage['records'], historical_checks):
        scope, width, height = rec['scope'], rec['width'], rec['height']
        phases = read(rec['phaseFile'])
        loaded = read(rec['loadedHtmlResponse'])
        assert loaded['exactByteEquality']
        assert loaded['documentResponseSha256'] == loaded['currentFileSha256'] == current_sha
        assert len(phases) == rec['phases']
        y, max_end = 0, 0
        for i, phase in enumerate(phases):
            assert phase['draft_sha256'] == current_sha
            assert phase['viewport']['width'] == width and phase['viewport']['height'] == height
            assert phase['url'] == loaded['url']
            shot = BASE / phase['screenshot']
            assert digest(shot) == phase['screenshotSha256']
            with Image.open(shot) as img:
                assert img.size == (width, height)
                assert img.format == 'JPEG'
            guard = phase['postScreenshotGuard']
            assert guard['url'] == phase['url'] and guard['width'] == width and guard['height'] == height
            assert guard['scrollY'] == phase['scrollY'] and guard['bodyHeight'] == phase['bodyHeight']
            assert phase['bodyHeight'] == rec['bodyHeight']
            if i == 0:
                assert phase['scrollY'] == 0
            else:
                assert y <= phase['scrollY'] <= max_end
            y = phase['scrollY']
            max_end = max(max_end, y + height)
            viewed_frames.append({'scope': scope, 'phaseIndex': i, 'file': phase['screenshot'],
                                  'sha256': phase['screenshotSha256'], 'observedAt': phase['observed_at'],
                                  'captureTimeHtmlSha256': current_sha, 'actualRasterDimensions': [width, height],
                                  'scrollY': y, 'wholeViewportVisuallyViewed': True})
        assert max_end >= rec['bodyHeight'] and y == rec['bodyHeight'] - height
        sheet_indices = []
        for sheet in rec['wholeViewportReviewSheets']:
            sheet_indices.extend(sheet['phaseIndices'])
            viewed_sheets.append({**sheet, 'scope': scope, 'sha256': digest(BASE / sheet['file']),
                                  'visuallyViewed': True})
        assert sorted(sheet_indices) == list(range(len(phases)))
        comparisons.extend({'file': name, 'scope': scope, 'sha256': digest(BASE / name), 'visuallyViewed': True,
                            'officialSourceObservedAt': historical['sourceObservedAt']} for name in rec['historicalSourceComparisonSegments'])
        fresh = rec.get('freshOfficialTop')
        if fresh:
            fresh_pairs.append({'file': fresh['comparison'], 'sha256': digest(BASE / fresh['comparison']),
                                'scope': scope, 'visuallyViewed': True, 'officialObservedAt': fresh['observedAt'],
                                'officialReviewScope': 'Top native viewport only; full DOM is read-only data, not full visual traversal.'})
        check = {
            'scope': scope, 'viewport': {'width': width, 'height': height, 'dpr': 1,
                'scope': 'CSS responsive viewport, unchanged desktop UA; not real phone hardware'},
            'sourceURL': historical['sourceURL'], 'sourceObservedAt': historical['sourceObservedAt'],
            'sourceObservationScope': 'Original dated complete official visual baseline; not relabelled Oct12.',
            'sourceHeight': historical['sourceHeight'], 'sourceCompleteness': historical.get('sourceCompleteness'),
            'sourcePhases': historical.get('sourcePhases'),
            'officialSequentialComposite': rec['historicalOfficialComposite'],
            'previewURL': loaded['url'], 'previewObservedAt': phases[-1]['observed_at'],
            'previewObservedAtRange': rec['observedAt'], 'previewHeight': rec['bodyHeight'],
            'heightDifference': rec['bodyHeight'] - historical['sourceHeight'],
            'previewSha256': current_sha, 'mainPhaseHtmlSha256': current_sha,
            'previewPhasePrefix': rec['phaseFile'].removesuffix('-phases.json'),
            'phaseFile': rec['phaseFile'], 'phaseFileSha256': digest(BASE / rec['phaseFile']),
            'previewPhases': len(phases), 'localTraversalPhases': len(phases),
            'captureTimeHashComplete': True, 'captureTimeHashRecordCount': len(phases), 'captureTimeHashMissingCount': 0,
            'completeSequentialViewportCoverage': True, 'currentShaBoundCompleteSequentialViewportCoverage': True,
            'currentFullPageComparisonComplete': True, 'freshOfficialFullPageComparisonComplete': False,
            'coverageScope': 'Complete current SHA-bound preview vs original dated full official baseline, plus separately dated fresh top observations.',
            'coverageProof': f'{brand}-oct12-current-coverage.json',
            'actualScreenshotDimensionsGuarded': True, 'trueNativeScreenshotDimensions': [width, height],
            'screenshotMethod': 'CUA tab.screenshot fullPage:false original JPEG at selected browser viewport; no original image resizing or cropping.',
            'allDomImages': rec['allImages'], 'imagesNotReady': rec['imagesNotReady'],
            'fontStatus': rec['fontStatus'], 'noHorizontalOverflow': rec['noHorizontalOverflow'],
            'loadedHtmlResponse': rec['loadedHtmlResponse'], 'loadedHtmlResponseSha256': digest(BASE / rec['loadedHtmlResponse']),
            'loadedResponseExactFileEquality': True, 'documentResponseSha256': loaded['documentResponseSha256'],
            'previewSequentialComposite': rec['nativePhaseComposite'],
            'comparisonSegments': rec['historicalSourceComparisonSegments'], 'allComparisonSegmentsVisuallyReviewed': True,
            'wholeViewportReviewSheets': [s['file'] for s in rec['wholeViewportReviewSheets']],
            'allCompleteRawViewportFramesVisuallyViewed': True, 'freshOfficialTop': fresh,
            'visualReviewNote': NOTES[brand][scope],
        }
        current_checks.append(check)

    # Remove superseded limitations about absent current captures; preserve them in lineage snapshots.
    prior = read(f'{brand}-oct12-result-before-lineage.json')
    remaining = list(prior['remainingDifferences'])
    if brand == 'raycast':
        remaining = [s for s in remaining if not s.startswith('The Subscribe input label was restored')]
        remaining[0] = 'The public hero WebGL canvas is blank in the static corrected page. The dated official narrow source and fresh Oct12 official desktop top show red moving geometry absent locally. WebGL fidelity is not verified; no invented raster substitute was used.'
    if brand == 'resend':
        remaining[0] = 'The dated Oct10 official desktop capture had Floor/light-ray image requests not ready and an empty WebGL cube. Preserved public background originals load locally. Fresh Oct12 official desktop capture timed out, so desktop WebGL/current-source fidelity remains unverified.'
    if brand == 'supabase':
        remaining = [s.replace('The current official captures had', 'The dated Oct10 official captures had') for s in remaining]
    remaining.append(NOTES[brand]['fresh'])
    remaining.append('Fresh official observations in this supplement cover the top viewport and complete DOM only. Full visual comparison uses the original dated official-page evidence; no latest full-page official equivalence is claimed. accepted=false.')

    total = len(viewed_frames)
    visual = {'brand': brand, 'recordedAt': NOW, 'previewSha256': current_sha,
              'currentCompleteRawViewportFramesViewed': total, 'allCompleteRawViewportFramesVisuallyViewed': True,
              'currentFrames': viewed_frames, 'inspectionSheets': viewed_sheets,
              'datedOfficialComparisonSegments': comparisons, 'freshOfficialTopComparisons': fresh_pairs,
              'allComparisonSegmentsVisuallyReviewed': True,
              'visualNotes': NOTES[brand],
              'method': 'Every complete viewport frame was viewed through the listed derived inspection sheets; all original JPEGs retain their native raster. Every separately generated dated-source comparison segment and fresh source top pair was also opened and viewed. Inspection sheets/composites are derived review aids, not original captures.',
              'accepted': False}
    write(f'{brand}-oct12-current-visual-review.json', visual)
    binding = {'kind': 'New complete current-preview native viewport sequences with capture-time SHA and loaded document byte equality',
               'currentPreviewSha256': current_sha, 'currentFullPageCaptureComplete': True,
               'currentFullPageComparisonComplete': True, 'freshOfficialFullPageComparisonComplete': False,
               'comparisonScope': 'Current preview vs original dated full official evidence; fresh official top only is separately timed.',
               'historicalLineage': f'{brand}-oct12-evidence-lineage.json', 'historicalLineageSha256': lineage_sha,
               'oldPhaseJsonMutated': False, 'oldCaptureHashesBackfilled': False,
               'passes': [{k: c[k] for k in ['scope', 'phaseFile', 'phaseFileSha256', 'previewObservedAtRange',
                   'previewSha256', 'previewPhases', 'trueNativeScreenshotDimensions', 'loadedHtmlResponse',
                   'loadedHtmlResponseSha256', 'documentResponseSha256', 'loadedResponseExactFileEquality']} for c in current_checks]}
    verification = {'brand': brand, 'recordedAt': NOW, 'accepted': False, 'preview': f'{brand}.html',
                    'previewSha256': current_sha, 'previewHtmlChangedDuringSupplement': False,
                    'currentFullPageCaptureComplete': True, 'currentFullPageComparisonComplete': True,
                    'freshOfficialFullPageComparisonComplete': False, 'captureBinding': binding,
                    'checks': current_checks, 'remainingDifferences': remaining,
                    'visualReview': f'{brand}-oct12-current-visual-review.json',
                    'historicalLineage': f'{brand}-oct12-evidence-lineage.json',
                    'nativeGenerationChanged': False, 'paidActions': False, 'published': False}
    write(f'{brand}-oct12-current-verification.json', verification)
    result['recordedAt'] = NOW
    result['accepted'] = False
    result['previewSha256'] = current_sha
    if 'mainPhaseHtmlSha256' in result:
        result['historicalMainPhaseHtmlSha256'] = result['mainPhaseHtmlSha256']
        result['mainPhaseHtmlSha256'] = current_sha
    result['historicalChecksAtLineageAudit'] = historical_checks
    result['checks'] = current_checks
    result['captureBinding'] = binding
    result['currentFullPageCaptureComplete'] = True
    result['currentFullPageComparisonComplete'] = True
    result['freshOfficialFullPageComparisonComplete'] = False
    result['currentVerification'] = f'{brand}-oct12-current-verification.json'
    result['currentVisualReview'] = f'{brand}-oct12-current-visual-review.json'
    result['remainingDifferences'] = remaining
    result['scopeNote'] = binding['comparisonScope'] + ' CSS responsive desktop/narrow viewport evidence, not real phone hardware; dynamic/UI/service limits remain explicit and accepted=false.'
    result['recordUpdates']['accepted'] = False
    result['recordUpdates']['verified'] = [
        'Original genuine Google Stitch MCP candidate, full provider response/exports, DESIGN.md/design-md and source correction remain preserved; this supplement changes no preview HTML or native generation.',
        f'Current final SHA captured in {current_checks[0]["previewPhases"]} desktop and {current_checks[1]["previewPhases"]} narrow complete native viewport frames. Each capture records that SHA, exact URL/scroll post-shot guard, original screenshot SHA and actual1280×720/390×844 PIL raster guard.',
        'Both newly reloaded document response bodies match the current HTML disk bytes exactly by SHA256. No current preview was changed during supplement.',
        f'All{total} complete viewport frames, all{len(comparisons)} dated-official comparison segments and{len(fresh_pairs)} separately dated fresh-official top pairs visually viewed. Fonts loaded, all DOM images ready, no horizontal page overflow; coverage reaches the full footer without gaps.',
        'Historical incomplete/mismatched capture hashes remain honestly recorded in the unchanged Oct12 evidence-lineage file. Old phase JSON and old timestamps were not relabelled or backfilled.',
        NOTES[brand]['fresh'],
    ]
    result['recordUpdates']['remaining'] = remaining
    result['recordUpdates']['review_note'] = f'2026-10-12補拍已完整綁目前SHA：D{current_checks[0]["previewPhases"]}/N{current_checks[1]["previewPhases"]}，原生實際1280×720/390×844，全部視窗及新舊來源比較圖逐張檢視。官方完整比較仍用原拍攝日期；最新來源僅頂部畫面另記，accepted=false。'
    write(result_name, result)

    build['captureBinding'] = binding
    build['actualReviewResult'] = result_name
    build['actualReviewScope'] = binding['comparisonScope']
    build['actualReviewSupplement'] = f'{brand}-oct12-current-verification.json'
    build['currentFullPageCaptureComplete'] = True
    build['currentFullPageComparisonComplete'] = True
    build['freshOfficialFullPageComparisonComplete'] = False
    build['remaining'] = remaining
    # htmlDigestRecordKind stays posthoc: this supplement is verification, not a rebuild.
    write(build_name, build)

    historic_text = analysis_backup.read_text()
    historic_text = historic_text.replace('## 2026-10-12 驗證版本綁定校正',
        '## 歷史紀錄：2026-10-12 補拍前的版本綁定稽核\n\n以下「尚未重拍」與false flags只描述當時狀態；後續補拍已完成，請以本文開頭與最新result為準。')
    overview = f'''# 2026-10-12 目前稿完整補驗 — {brand}

目前稿 SHA256：`{current_sha}`；本次未修改HTML、原生Stitch輸出、原始設計匯出或公開素材。

桌面1280×720共{current_checks[0]['previewPhases']}張、窄版390×844共{current_checks[1]['previewPhases']}張，從頂到頁尾完整實際視窗無缺口；每張當時記錄目前稿SHA、截圖SHA與截圖後URL/捲動守衛，PIL逐檔確認原生尺寸。兩次重新載入的document response bytes均與磁碟稿完全相等。全部{total}張完整視窗、{len(comparisons)}張對照圖與{len(fresh_pairs)}張最新官方頂部對照已逐張檢視。所有DOM圖片載入、字型loaded，無頁面水平溢位。桌面檢視contact sheet使用半尺寸顯示，窄版原尺寸；原始JPEG完全未縮放或裁切。

`currentFullPageCaptureComplete=true`、`currentFullPageComparisonComplete=true`只表示目前SHA已整頁實看並與**原日期官方完整畫面**比較。`freshOfficialFullPageComparisonComplete=false`：最新官方另存完整DOM與一張頂部實拍，不冒充最新完整逐段來源。先前歷史phase及缺capture-time SHA的紀錄完全未改寫。

{NOTES[brand]['desktop']}

{NOTES[brand]['narrow']}

{NOTES[brand]['fresh']}

accepted=false；動畫、UI、服務與最新全頁差異仍依result明列，沒有宣稱全面官方一致。本次沒有付費、登入、提交表單或部署。

當前證據：`{brand}-oct12-current-verification.json`、`{brand}-oct12-current-visual-review.json`；歷史脈絡保留於`{brand}-oct12-evidence-lineage.json`。以下原設計分析與歷史稽核依原日期保留。

---

'''
    analysis.write_text(overview + historic_text)
    assert digest(html) == current_sha
    assert digest(BASE / f'{brand}-oct12-evidence-lineage.json') == lineage_sha
    for scope in lineage['scopes']:
        assert digest(BASE / scope['historicalPhaseFile']) == scope['historicalPhaseFileSha256']

# A posthoc inventory is distinct from the original capture-time hashes above.
for brand in BRANDS:
    manifest_path = BASE / f'{brand}-oct10-file-hashes.json'
    own_paths = [p for p in BASE.rglob('*') if p.is_file() and p.relative_to(BASE).parts[0].startswith(brand)]
    own_paths += [p for p in (ROOT / 'scripts').glob('*') if p.is_file() and any(x in p.name for x in BRANDS)]
    files = {str(p.relative_to(ROOT)): {'bytes': p.stat().st_size, 'sha256': digest(p)}
             for p in sorted(set(own_paths)) if p != manifest_path}
    write(manifest_path.name, {'recordedAt': NOW, 'previewSha256': digest(BASE / f'{brand}.html'),
          'recordKind': 'Posthoc current files inventory. New capture-time SHA is separately recorded in original Oct12 phases and loaded-response records; old manifests preserved.',
          'files': files})
    print(json.dumps({'brand': brand, 'sha256': digest(BASE / f'{brand}.html'), 'files': len(files),
                      'result': f'{brand}-oct10-result.json', 'accepted': False}))
