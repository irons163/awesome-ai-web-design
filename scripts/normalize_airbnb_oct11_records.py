"""Bind retained Airbnb viewport evidence without inventing a Stitch export."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess

from PIL import Image
from publication import references, is_asset

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / '.stitch-work/current-official'


def read(name):
    return json.loads((WORK / name).read_text())


def hashed(name):
    data = (WORK / name).read_bytes()
    return dict(path=name, bytes=len(data), sha256=hashlib.sha256(data).hexdigest())


def write(name, value):
    (WORK / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


legacy_name = 'airbnb-oct10-result.json'
legacy = read(legacy_name)
preview = hashed('airbnb.html')
assert preview['sha256'] == legacy['local_draft']['sha256']
# The old result binds the then-current HTML and every retained capture. Do not
# retroactively insert capture-time hashes into its older slice schema.
legacy_checks = []
for name, expected in sorted(legacy['hashes'].items()):
    item = hashed(name)
    assert item['sha256'] == expected, 'Retained historical evidence changed: ' + name
    legacy_checks.append(item)
assert len(legacy_checks) == 83
originals = []
for name in ['DESIGN.md', 'PROMPTS.md', 'STITCH-PROMPT.md']:
    relative = 'design-md/airbnb/' + name
    file = ROOT / relative
    old = subprocess.run(['git', 'show', 'HEAD:' + relative], cwd=ROOT, capture_output=True, check=True).stdout
    assert old == file.read_bytes(), 'Historical original changed: ' + relative
    originals.append(dict(path=relative, bytes=len(old), sha256=hashlib.sha256(old).hexdigest(), unchanged_from_HEAD=True))
request = read('airbnb-oct10-stitch-desktop-request.json')
prompt = (WORK / 'airbnb-oct10-stitch-desktop-prompt.md').read_text().strip()
assert request['prompt'].strip() == prompt
assert legacy['native_stitch']['current_native_generation_complete'] is False
assert legacy['native_stitch']['retrieved_current_export'] is None
new_native = None
new_native_files = []
if (WORK / 'airbnb-oct11-stitch-narrow-response.json').exists():
    response = read('airbnb-oct11-stitch-narrow-response.json')['structuredContent']
    narrow_request = read('airbnb-oct11-stitch-narrow-request.json')
    screens = [screen for component in response['outputComponents']
               for screen in component.get('design', {}).get('screens', [])]
    assert len(screens) == 1 and response['projectId'] == request['projectId']
    screen = screens[0]
    new_native_files = [
        'airbnb-oct11-stitch-narrow-prompt.md', 'airbnb-oct11-stitch-narrow-request.json',
        'airbnb-oct11-stitch-narrow-response.json', 'airbnb-oct11-stitch-narrow-downloads.private.json',
        'airbnb-oct11-stitch-narrow-raw-0.html', 'airbnb-oct11-stitch-narrow-raw-0.png',
    ]
    assert hashed(new_native_files[-2])['sha256'] == '581e5e85b9145ba924b5bd61d25ab133bc4106139576bb5ec00414ec51e6daec'
    assert hashed(new_native_files[-1])['sha256'] == 'c066f6f2b9a3c4e4bdc8773bd11221781dd8e4f3d7bcb11cc1c9f905d04e5ec6'
    assert narrow_request['deviceType'] == 'MOBILE' and screen['deviceType'] == 'DESKTOP'
    new_native = dict(
        project='projects/' + response['projectId'], session_id=response['sessionId'],
        screen=screen['name'], scope='Distinct390px narrow generation, separate from the original desktop timeout request.',
        requested_device='MOBILE', returned_device=screen['deviceType'],
        provider_metadata_dimensions=[int(screen['width']), int(screen['height'])],
        genuine_generation_returned=True, mobile_device_success=False,
        original_desktop_timeout_still_unresolved=True, original_desktop_timeout_retry_performed=False,
        raw_files=[hashed(name) for name in new_native_files],
        root_actual_native_png_inspection='Root actually viewed the original provider PNG: narrow content atleft with large white region atright; many property photos/category icons are purple placeholders. Not official comparison or successful mobile viewport evidence.',
        provider_claims_not_adopted=True, provider_image_is_not_browser_QA=True,
        current_source_corrected_preview_not_replaced=True,
    )

evidence = {}
for role in ['official', 'local']:
    for mode, size in [('desktop', (1440, 900)), ('narrow', (390, 844))]:
        name = f'airbnb-oct10-{role}-{mode}-slices.json'
        frames = read(name)
        final_height = frames[-1]['height']
        end, gaps, screenshots = 0, [], []
        for frame in frames:
            shot = hashed(frame['file'])
            with Image.open(WORK / frame['file']) as image:
                dimensions = image.size
            assert dimensions == size, 'Invalid raster dimensions: ' + frame['file']
            screenshots.append(dict(**shot, dimensions=list(dimensions), scroll_y=frame['scrollY']))
            assert not frame.get('brokenImages', [])
        intervals = sorted((max(0, f['scrollY']), min(final_height, f['scrollY'] + size[1])) for f in frames)
        for start, stop in intervals:
            if start > end + 1:
                gaps.append([end, start])
            end = max(end, stop)
        if end < final_height - 1:
            gaps.append([end, final_height])
        assert not gaps, 'Uncovered viewport evidence: ' + name
        evidence[f'{role}_{mode}'] = dict(
            slices=name, viewport=dict(width=size[0], height=size[1], dpr=1, mobile=False),
            coordinate_space='document_scroll', sampled_rows=len(frames),
            unique_screenshot_files=len({f['file'] for f in frames}),
            sampled_document_heights=list(dict.fromkeys(f['height'] for f in frames)),
            settled_compact_page_height=final_height, union_covered_through=end,
            whole_page_covered=True, uncovered_document_y_intervals=gaps,
            screenshots=screenshots, actual_native_dimensions_valid=True,
            current_preview_bound=(role == 'local'),
            binding_method='Unmodified retained result binds current preview and all slice/capture hashes; older slice files have no per-frame capture-time digest.',
        )

now = datetime.now(timezone.utc).isoformat()
source = read('airbnb-oct10-browser-reference.json')
narrow_source = read('airbnb-oct10-narrow-browser-reference.json')
assets = read('airbnb-oct10-asset-provenance.json')
for row in assets['assets']:
    assert hashed(row['local'])['sha256'] == row['sha256']
limits = [
    '本次必要的 Google Stitch 生成逾時；十次間隔查詢沒有取得畫面，10月11日唯讀查詢仍為空。現有來源校正不是已完成的當次原生 Stitch 匯出，這項要求仍未完成。',
    '桌面縮小導覽的卡片圖示偏小，部分標籤間距、標題箭頭與愛心圖示仍有可見差異，沒有逐像素一致的結論。',
    '此為匿名英文加拿大首頁的一次地區／個人化樣本；房源、價格、可用日期與評分僅代表取樣當時，不能推廣為所有訪客目前皆相同。',
    '搜尋／分類視窗為簡化操作；Experiences／Services 不會重現官方完整對應房源，getaway 頁籤與語言／貨幣對話框也未完整重製。',
    '本機最愛僅為頁面狀態，不是官方帳戶或願望清單；帳戶、真實搜尋、預訂、付款與其他服務未驗證，未執行交易或送出外部表單。',
    '完整動畫時序、選單深度、其他地區／尺寸、實體手機與目前部署畫面尚未驗證。390px 是桌面 UA 的響應式窄版。',
    '早期官網整頁 captureBeyondViewport 圖未完整繪出延遲載入內容，保留作失敗診斷並排除；有效完整覆蓋以重疊的實際 viewport PNG 為準。桌面來源與本機捲動位置不同，不能宣稱每段在同一 offset 逐像素配對。',
]
if new_native:
    limits[0] = '10月10日原DESKTOP生成逾時與十次空查詢仍原樣保留；10月11日另發390px窄版MOBILE新工作已取得真正原生輸出，但提供者回報DESKTOP2560×9340，原PNG左側窄內容、右側大片白區，房源照片／分類圖示仍有大量紫色placeholder。已有新生成不表示MOBILE成功或與官方一致，588a來源校正版未由此輸出替換。'
design_name = 'airbnb-oct11-design-analysis.md'
prompt_name = 'airbnb-oct11-rewritten-prompts.md'
review_name = 'airbnb-oct11-visual-review.md'
(WORK / design_name).write_text('''# Airbnb｜10月10日公開首頁，10月11日證據整理

來源為 [Airbnb 加拿大英文公開首頁](https://www.airbnb.ca/?locale=en)。桌面取樣時間 2026-10-10T11:09:10.905Z，窄版 11:16:55.079Z；只接受必要 Cookie。這是一次匿名地區／個人化內容，不代表所有訪客、所有語言或持續更新的房源。

目前頁面以白底、Airbnb Cereal、近黑文字、灰色次要資訊與紅色搜尋按鈕構成。桌面首屏有 Airbnb 標誌、All／Homes／Experiences／Services、Become a host 與選單，下方大型 Where／When／Who 搜尋膠囊；捲動後收為較矮的固定導覽。390px窄版改為堆疊搜尋／分類與橫向房源列，這次使用桌面 UA，沒有驗證實體手機。

內容為十列當日房源：Lake Kawaguchi、Taitung City、Taichung City this weekend、Kaohsiung City、Tokyo、Osaka、Bangkok、Vancouver、Busan next month、Kyoto next month。保留80張真正觀察到的房源照片、價格／日期／評分及房源連結；卡片含圓角照片、Guest favourite、愛心及輪播箭頭。沒有沿用9月舊稿的 Experiences／Services 宣傳組合。

後段是淡灰底 Inspiration for future getaways、目的地分類／地名，再接 Support／Hosting／Airbnb 三欄頁尾、2026版權、English(CA)／CAD與社群圖示。89項選用來源素材已記錄原 URL、下載方式與雜湊；本機86個圖片元素與 Cereal 字型的載入檢查已保存，標誌的歷史來源紀錄另存。

既有實際畫面檢視涵蓋桌面1440×900與窄版390×844的完整重疊取樣；本次另驗證所有原始證據雜湊與PNG真實尺寸仍對應目前HTML。桌面有8列取樣、7張獨立圖（頁尾重複一次），窄版有10張；桌面縮小導覽後頁高4508px，窄版4980px。桌面初始頁高4613px與官網延遲掛載過程均保留，沒有把相同頁高當作完全一致。

**accepted=false，不宣稱與官方一致。** 當次Google Stitch原生生成逾時且至10月11日仍沒有screen／export；手動來源校正與主畫面比對不能代替這項尚未完成的要求。圖示／間距、分類、語言、帳戶、搜尋／預訂服務與動畫等差異詳列於畫面紀錄。原有DESIGN.md、PROMPTS.md、STITCH-PROMPT.md與歷史輸出完整保留。研究頁免費瀏覽，未購買方案、訂閱或交易；不對外部提供者帳戶計費狀態作保證。
''')
(WORK / prompt_name).write_text(
    '# Airbnb｜實際送出指令與後續來源校正規格\n\n'
    '以下完整保留本次實際送交 Google Stitch MCP 的原文。project `13625555706512007030`、DESKTOP；請求逾時，尚無當次原生輸出。原文保存不表示生成成功。\n\n'
    '```text\n' + prompt + '\n```\n\n'
    '## 後續校正規格（未另送出 Stitch）\n\n'
    '依10月10日加拿大英文公開首頁的完整桌面1440×900與390×844參照重製，保留十列房源、80張當日公開照片與89項選用原始素材，不臆造房源、價格或帳戶狀態。使用Cereal字型、All／Homes／Experiences／Services、Where／When／Who搜尋、首屏／縮小固定導覽、getaway目的地與完整頁尾。窄版重排與卡片裁切必須依實際PNG，不把桌面UA結果說成實體手機。\n\n'
    '保留原生請求、完整回應、十次查詢及10月11日唯讀查詢紀錄；在提供者仍無輸出時明寫未完成，不把舊生成稿或來源校正說成當次原生匯出。之後若有真正輸出，保留原始HTML／PNG，再以當前雜湊重新查看完整桌面與窄版。不得因頁高、文字或圖片載入相同而宣稱與官方一致。\n\n'
    '微調卡片圖示、標籤間距與箭頭／愛心時需重新檢查畫面。搜尋／分類、getaway頁籤、語言／貨幣、最愛／帳戶及預訂服務未完整重製；不能虛構已可用的後端。保持研究免費，列明地區／時間／動畫／互動與部署限制。\n')
table = ['| 保存取樣 | 視窗 | 列數／獨立圖 | 最終範圍 | 覆蓋缺口 |', '|---|---|---:|---:|---|']
for key, item in evidence.items():
    view = item['viewport']
    table.append(f'| {key} | {view["width"]}×{view["height"]} | {item["sampled_rows"]}／{item["unique_screenshot_files"]} | {item["settled_compact_page_height"]}px | 無 |')
(WORK / review_name).write_text(
    '# Airbnb｜10月11日現有證據與狀態整理\n\n來源取樣日期：2026-10-10；此次整理不冒稱重新拍攝。當前HTML SHA-256：`' + preview['sha256'] + '`。\n\n'
    '**accepted=false，不宣稱與官方一致；當次Google Stitch原生輸出仍未取得。**\n\n'
    + '\n'.join(table) + '\n\n'
    '保留的10月10日紀錄與主代理既有回報確認實際檢視了桌面／窄版主畫面、80張來源房源照片、字型、頁尾與固定導覽。此次整理驗證舊result的83筆檔案雜湊全部相符、每張有效PNG真實尺寸正確、重疊範圍到頁底無缺口。這是經保留雜湊鏈綁定目前HTML的既有畫面證據；沒有倒填舊slice不存在的逐張capture-time hash，也沒有宣稱整理者這輪重新看過全部畫面。\n\n'
    '桌面來源與本機各8列，但頁尾各重複同一張，因此各7張獨立圖；窄版各10張。來源桌面延遲掛載頁高2633→4172→4508px，本機由4613px縮小導覽後4508px；初始完整來源量測另為4613px。沒有宣稱所有桌面offset相同。\n\n'
    '本機輪播前後、最愛切換、選單開啟／Escape及窄版搜尋視窗開關曾實際測試；它們只證明本機簡化操作，不能證明官方服務或帳戶流程一致。\n\n'
    + '\n\n'.join('- ' + value for value in limits) + '\n')

if new_native:
    design_file = WORK / design_name
    design = design_file.read_text().replace(
        '當次Google Stitch原生生成逾時且至10月11日仍沒有screen／export；手動來源校正與主畫面比對不能代替這項尚未完成的要求。',
        '原DESKTOP生成逾時與十次空查詢歷史仍保留。10月11日另做390px窄版工作，確實取得新的Google Stitch原生輸出；但MOBILE請求回傳DESKTOP2560×9340，原圖有大片右側白區與紫色placeholder，不能視為成功MOBILE或官網一致。既有588a來源校正版與其主畫面證據保留，不以此生成稿替換。')
    design_file.write_text(design)
    prompt_file = WORK / prompt_name
    rewritten = prompt_file.read_text().replace(
        '以下完整保留本次實際送交 Google Stitch MCP 的原文。project `13625555706512007030`、DESKTOP；請求逾時，尚無當次原生輸出。原文保存不表示生成成功。',
        '以下完整保留10月10日實際送交Google Stitch MCP的原DESKTOP指令。project `13625555706512007030`；該請求逾時且十次查詢為空，仍未取得該次輸出。後續不同390px範圍的新工作另列，不能抹除這條失敗歷史。')
    narrow_prompt = (WORK / 'airbnb-oct11-stitch-narrow-prompt.md').read_text().rstrip()
    narrow_section = (
        '## 10月11日另送出的390px窄版新工作\n\n'
        '此為不同範圍的新MOBILE請求，不是重送原DESKTOP逾時請求。session `2686441563832907567`，screen `73285e56f28a4277af38628dc351e433`。已取得完整原始HTML／PNG與回應；提供者實際回報DESKTOP2560×9340。主代理已查看原PNG，左側窄內容與右側大片白區、紫色placeholder均保留為限制，不宣稱MOBILE成功或與官方一致。原始輸出與來源校正HTML分開保存。\n\n'
        '```text\n' + narrow_prompt + '\n```\n\n')
    rewritten = rewritten.replace('## 後續校正規格（未另送出 Stitch）', narrow_section + '## 後續校正規格（本段尚未另送出 Stitch）')
    rewritten = rewritten.replace(
        '在提供者仍無輸出時明寫未完成，不把舊生成稿或來源校正說成當次原生匯出。之後若有真正輸出，保留原始HTML／PNG，再以當前雜湊重新查看完整桌面與窄版。',
        '原DESKTOP逾時仍未完成，新增窄版工作已有真正輸出但device回錯且有placeholder，不能把它說成成功MOBILE。兩次請求、完整原始HTML／PNG分開保存；如再校正，仍須以當前雜湊重新查看完整桌面與窄版。')
    prompt_file.write_text(rewritten)
    review_file = WORK / review_name
    review = review_file.read_text().replace(
        '**accepted=false，不宣稱與官方一致；當次Google Stitch原生輸出仍未取得。**',
        '**accepted=false，不宣稱與官方一致。原DESKTOP逾時仍無輸出；新增窄版原生工作已返回，但不是成功MOBILE。**')
    review += ('\n新增原生輸出由主代理實際查看，判讀只屬提供者PNG：左側窄版內容＋大片右白，照片／分類icon有紫色placeholder；metadata為DESKTOP2560×9340。這不是官網或本機瀏覽器QA，也沒有改變588a來源校正版的桌面／窄版既有檢視歸屬。原HTML與PNG分別以581e5e85…／c066f6f2…雜湊獨立保留。\n')
    review_file.write_text(review)

# Read only actual local dependencies; raw DOM/network/provider bundles and
# screenshots are retained privately and never inferred as publication assets.
required, queue = set(), references((WORK / 'airbnb.html').read_text(), 'airbnb')
while queue:
    name = queue.pop(0)
    if name in required:
        continue
    assert is_asset(name, 'airbnb') and (WORK / name).is_file(), name
    required.add(name)
    if Path(name).suffix.lower() in ['.css', '.svg', '.js']:
        queue += references((WORK / name).read_text(), 'airbnb', str(Path(name).parent))
texts = [design_name, prompt_name, review_name]
manifest_name = 'airbnb-oct11-publication-manifest.json'
write(manifest_name, dict(
    brand='airbnb', accepted=False, official_consistency_claim=False, preview=preview,
    study_text=texts, required_local_assets=[hashed(name) for name in sorted(required)],
    publish_allowlist=['airbnb.html', *texts, *sorted(required)],
    native_current_generation_complete=False,
    native_current_generation_available=bool(new_native), native_current_mobile_success=False,
    native_current_exports=new_native_files[-2:] if new_native else [],
    native_original_exports_retained_privately=new_native_files[-2:] if new_native else [],
    publication_note='Preserve exact preview bytes. Main-page scoped review does not complete the missing current native Stitch generation. Raw captures, DOM, bundles and provider responses remain private provenance.',
))
audit_name = 'airbnb-oct11-evidence-normalization.json'
write(audit_name, dict(
    normalized_at_utc=now, preview=preview, retained_result=hashed(legacy_name),
    original_hash_manifest_entries_verified=len(legacy_checks), retained_capture_hashes_unchanged=True,
    evidence=evidence, actual_visual_review_attribution='root and the retained2026-10-10 review record; not a new full raster inspection by this normalizer',
    historical_review_preserved_without_new_acceptance=True,
    previous_ui_unverified_reason='Old custom status plus absent normalized full-coverage/current-raster flags; resultFor already selected the correct preview digest.',
    raw_failed_full_captures_excluded=legacy['current_reference']['full_capture_excluded'],
    capture_time_hashes_not_retroactively_invented=True,
))
provenance_name = 'airbnb-oct11-provenance.json'
write(provenance_name, dict(
    brand='airbnb', normalized_at_utc=now, preview=preview,
    source_observed_at=dict(desktop=source['observedAt'], narrow=narrow_source['observedAt']),
    original_analysis_and_prompts=originals, source_assets=hashed('airbnb-oct10-asset-provenance.json'),
    native_stitch=legacy['native_stitch'], additional_distinct_narrow_generation=new_native,
    latest_read_only_native_status=hashed('airbnb-oct11-stitch-existing-project-status.json'),
    retained_original_artifacts=legacy_checks,
    current_supplements=[hashed(name) for name in [*texts, audit_name, manifest_name]],
    public_dependencies=[hashed(name) for name in sorted(required)],
    private_raw_retention=True, accepted=False, official_consistency_claim=False,
))
native = dict(legacy['native_stitch'], latest_read_only_status='airbnb-oct11-stitch-existing-project-status.json')
if new_native:
    native.update(original_desktop_generation_complete=False,
                  genuine_current_generation_available=True,
                  successful_current_mobile_generation=False,
                  additional_distinct_narrow_generation=new_native)
write('airbnb-oct11-result.json', dict(
    brand='airbnb', observed_at=source['observedAt'], normalized_at_utc=now,
    accepted=False, official_consistency_claim=False, status='in_visual_review',
    reference_url=source['sourceUrl'], preview='airbnb.html', preview_sha256=preview['sha256'], preview_bytes=preview['bytes'],
    scope=dict(desktop=dict(width=1440,height=900,dpr=1),narrow=dict(width=390,height=844,dpr=1,mobile=False),
               public_anonymous=True, locale='en-CA', geographic_personalized_session_only=True,
               service_actions_performed=False, physical_devices_verified=False),
    native_stitch=native, current_native_generation_complete=False,
    current_native_generation_available=bool(new_native), current_native_mobile_generation_success=False,
    native_status_note='Original DESKTOP request remains timed out without screen; a distinct later390MOBILE generation returned genuine DESKTOP output with placeholders, not a successful mobile canvas.' if new_native else 'Original DESKTOP request remains timed out without screen.',
    method='Original genuine current Stitch DESKTOP request timed out; a distinct390MOBILE request now has retained genuine DESKTOP exports with wrong device/placeholder limits. Public-source corrected588a preview remains separate, with unchanged retained desktop/narrow review and historical digest binding.' if new_native else 'Retained genuine current Stitch request timed out without export; separately preserved public-source correction and actual prior desktop/narrow review bound by unchanged historical result/artifact digests.',
    evidence=evidence, retained_hash_binding_audit=audit_name,
    latest_draft_full_desktop_and_narrow_coverage=True,
    actual_raster_inspection_bound_to_current_preview=True, latest_draft_actual_render_checked=True,
    visual_inspection_owner='root_and_retained_oct10_review', writer_independent_visual_acceptance=False,
    actual_raster_inspection_is_retained_not_new=True,
    verified_scope=legacy['verified_scope'], remaining_differences_and_limits=limits,
    design_analysis_and_original_prompts=originals,
    public_assets=dict(manifest='airbnb-oct10-asset-provenance.json',chosen_count=len(assets['assets']),required_dependencies=len(required),listing_count=80),
    current_supplements=dict(design_analysis=design_name,rewritten_prompts=prompt_name,visual_review=review_name,provenance=provenance_name,publication_manifest=manifest_name),
    free_study=dict(study_access_free=True,purchases_or_subscriptions_performed=False,provider_usage_billing_not_asserted=True),
    hashes=[hashed(name) for name in [*texts,audit_name,manifest_name,provenance_name,legacy_name]],
))
print(json.dumps(dict(brand='airbnb',sha256=preview['sha256'],retained_hashes_verified=len(legacy_checks),full_coverage=True,actual_retained_raster_bound=True,native_current_generation_available=bool(new_native),native_mobile_success=False,native_current_generation_complete=False,required_assets=len(required),accepted=False)))
