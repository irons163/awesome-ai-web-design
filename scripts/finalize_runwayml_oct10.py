from pathlib import Path
import json, hashlib, datetime
from PIL import Image

w = Path('.stitch-work/current-official'); b = 'runwayml'
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
sha = hashlib.sha256((w / f'{b}.html').read_bytes()).hexdigest()
coverage = json.loads((w / f'{b}-oct10-native-coverage.json').read_text())
assert coverage['previewSha256'] == sha
native = json.loads((w / f'{b}-oct10-native-export-hashes.json').read_text())
dims = list(Image.open(w / f'{b}-oct10-stitch-desktop.png').size)
assert dims == native['declaredDimensions']
assets = json.loads((w / f'{b}-oct10-assets.json').read_text())
assert len(assets['assets']) == 44 and not assets['failures']
scopes = []
for mode, width, height, total, count, segments in [('desktop', 1280, 720, 5015, 7, 3), ('narrow', 390, 844, 9377, 12, 5)]:
    r = json.loads((w / f'{b}-oct10-official-{width}-reference.json').read_text())
    audit = json.loads((w / f'{b}-oct10-corrected-{mode}.json').read_text())
    html = ''.join(r['htmlParts'])
    assert len(html.encode('utf-16-le')) // 2 == r['html_length']
    assert hashlib.sha256(html.encode()).hexdigest() == r['html_sha256'] and html.endswith('</html>')
    phases = json.loads((w / f'{b}-oct10-corrected-{width}-phases.json').read_text())
    source = json.loads((w / f'{b}-oct10-official-{width}-phases.json').read_text())
    assert len(phases) == len(source) == count and all(x['draft_sha256'] == sha for x in phases)
    assert all(x['selectedPlatform'] == ['Runway Creative'] for x in phases + source)
    assert audit['height'] == total and len(audit['images']) == 16
    assert all(i['loaded'] for i in audit['images']) and audit['scrollWidth'] == width and audit['fontStatus'] == 'loaded'
    assert audit['headings'][0]['bounds'] == source[0]['headings'][0]['box']
    scopes.append(dict(scope=mode, viewport=audit['viewport'], sourceURL=r['url'], previewURL=audit['url'], previewObservedAt=audit['observedAt'], sourceHeight=total, previewHeight=total, heightDifference=0, noHorizontalOverflow=True, fontStatus='loaded', allDomImages=16, imagesNotReady=0, sourcePhases=count, previewPhases=count, selectedPlatform='Runway Creative', completeSequentialViewportCoverage=True, trueScreenshotDimensions=[width,height], comparisonSegments=[f'{b}-oct10-compare-{mode}-{i}.png' for i in range(segments)], sourceCompleteness=dict(utf16Units=r['html_length'], sha256=r['html_sha256'], complete=True), heroTitleBounds=audit['headings'][0]['bounds']))

remaining = [
    'Official homepage auto-cycles between Creative, Dev and Robotics panels, changing body height. This review explicitly selected Runway Creative / How Runway is Used. Dev/Robotics and other Creative tabs are not accepted; the static preview retains the selected captured state.',
    'Mux shadow-root video/HLS playback is replaced with the exact observed public srcset poster. Hero, Creative, Robotics and the Creative use-case panel show different motion phases or static posters; Research video frame timing also differs. No frame-by-frame or playback parity is claimed.',
    'The official narrow top screenshot catches navigation over the blue promotion banner during its transition; the corrected header sits below the visible banner, then sticks at top after scroll. Partner-logo positions and their occlusion by sticky navigation differ in sequential phases. These states are not accepted as exact official parity.',
    'Navigation menus/mobile drawer, platform/tab switching, cookie/privacy and language controls, full keyboard/focus behavior and account/API/contact service flows are not implemented or accepted by this static source correction. Observed links lead to official destinations; no account or form submission occurred.',
    'Fresh genuine Stitch edit is DESKTOP only. Prior original desktop/mobile/DESIGN.md/design-md remain preserved. Other widths, real phone hardware, other routes/locales and published deployment are not reviewed.'
]
analysis = '''# Runway 目前公開首頁設計分析

入口 https://runwayml.com/ 目前轉到 https://runway.com/，觀察2026-10-11。當日新增藍色企業促銷公告，桌面高48px、窄版60.5px；白色64px固定導覽，下接黑底原始影片主視覺。abcNormal 主標 Building Real-World Intelligence 的實測位置，桌面為x58.75/y347.53/520.49×43.89、38.17px字型；窄版為x50.59/y280.11/288.83×64.39、28px字型。

完整順序保留合作品牌SVG列、三平台Creative/Dev/Robotics介紹、平台選擇與Creative使用方式頁籤、模糊流動Research影像與三個研究連結、Runway Ads/Praxis-1/OpenAI Marketplace/Claude Motion四則當日新聞，以及完整黑色多欄頁尾。品牌或產品宣傳文字僅代表當日官方頁面，不代表另行產品查核。

官方平台面板會自動輪播，造成頁高變動。本次透過可見按鈕明確選定 Runway Creative / How Runway is Used，再以每段狀態檢查完整拍攝：來源與成品桌面各7段、窄版各12段，頁高5015/9377px。每張實際影像尺寸、連續捲動覆蓋、前後捲動與頁高一致、成品hash皆驗證；全部3張桌面與5張窄版比較圖逐段目視檢查。16張DOM圖片與字型載入完成、無水平溢位，主標位置和尺寸完全相合。

genuine Google Stitch MCP 新增桌面屏幕，完整指令、回應、原始HTML、未改縮圖和fullPNG分開保留；具體重製再使用完整當日官方DOM/CSS及44份公開原始素材校正。已修正公告被固定導覽遮蓋與Dev區塊原始背景圖漏載；Mux播放器使用原始srcset海報，不以生成圖片替代。舊版與不穩定輪播證據均另外保留，不混作本次完整驗證。

''' + ''.join('- ' + x + '\n' for x in remaining) + '\naccepted=false；未付費、未部署、未提交帳戶/表單，帳戶計費未稽核。\n'
(w / f'{b}-oct10-analysis.md').write_text(analysis)
(w / f'{b}-oct10-reproduction-prompt.md').write_text('''# Rewritten AI instruction — Runway current public homepage

Reconstruct the public https://runway.com/ homepage reached from https://runwayml.com/ as actually observed2026-10-11. Preserve the blue enterprise offer dated10/31,64px white navigation, abcNormal typography, exact Building Real-World Intelligence copy, official original media, logo SVG strip, three platform columns, explicitly selected Runway Creative / How Runway is Used state, Research, the four current Runway Ads/Praxis-1/OpenAI Marketplace/Claude Motion cards and complete black footer. Use the actual observed official text/assets, without fabricated robot-cooking illustrations, telemetry tags or SLA claims.

Retain genuine fresh DESKTOP edit/full response/exact prompt/rawHTML/unchanged thumbnail/fullPNG separately, preserving prior MOBILE/DESIGN.md/design-md. Correct the concrete preview from complete current source DOM/CSS and44 public assets, including Dev's original background photo. Render observed original Mux srcset posters visibly as static fallbacks. Verify full5015px desktop and9377px narrow pages at1280×720 and390×844 with actual screenshots, true-dimension/continuous-coverage/hash/selected-platform guards,16loaded images/fonts/no overflow and exact title geometry. Disclose platform auto-cycling, video/poster/marquee/header-transition differences and unimplemented UI/services/native MOBILE/other widths/deployment. Provider exact/authentic/verified statements are not validation. accepted=false; free gallery, no paid actions or account submission.
''')
(w / f'{b}-oct10-provider-notes.md').write_text('''# Genuine Google Stitch provenance and unverified provider statements

Fresh DESKTOP edit, project600178545926470613, session15460128491004954810, screenb28f3869b77f408db904e19a079e7c3d. Complete native response runwayml-oct10-native-response.json and exact prompt runwayml-oct10-native-prompt.txt are preserved. Native raw HTML, unchanged screenshot thumbnail and fullPNG retain their precise provider URLs/bytes/hashes in runwayml-oct10-native-export-hashes.json. Actual fullPNG dimensions2560×7838 independently checked against metadata.

Provider descriptions claiming exact or authentic official reproduction do not validate fidelity. Its generated robot-cooking prompt image, GWM-1 ACTIVE INFERENCE telemetry labels and enterprise SLA note were not accepted from official source evidence. The Team Plan thumbnail used for its Creative panel and paraphrased news claims were corrected to actually observed source content/media in the concrete preview. Full original exports remain unmodified.

Provider suggestions retained: generate tablet/390px responsive variants, export HTML/CSS, and simulate Dev/Robotics tabs. No fresh native MOBILE or verified Dev/Robotics behavior is claimed. No purchases or paid upgrades occurred; account billing was not audited.
''')
verified = ['Genuine fresh desktop Stitch correction and full original native exports retained.', 'Complete current source DOM/CSS corrected with44 public original assets; final asset failures0.', 'Source and corrected7desktop/12narrow actual viewport phases cover5015/9377px completely; true dimensions, contiguous coverage, hash and selected Creative state guards passed; all8comparison segments reviewed.', '16images loaded at both widths, fonts loaded, no horizontal overflow, matching page heights and exact hero title geometry.']
result = dict(brand=b, recordedAt=now, status='visually_compared_with_scoped_differences', accepted=False, reference_url='https://runway.com/', entry_url='https://runwayml.com/', preview='runwayml.html', previewSha256=sha, sourceCorrectionCompleted=True, recordUpdates=dict(status='visually_compared_with_scoped_differences', accepted=False, reference_url='https://runway.com/', native_screen=native['screen'], preview='runwayml.html', verified=verified, remaining=remaining, review_note='已校正當日官方完整首頁並完成指定桌面/窄版Creative狀態全頁實拍；平台輪播、影片、窄版導覽過渡及互動差異未接受官方一致。'), checks=scopes, nativeGeneration=dict(reused=False, screen=native['screen'], sessionId=native['sessionId'], fullRawResponse=f'{b}-oct10-native-response.json', rawHtml=f'{b}-oct10-stitch-desktop.html', fullNativeScreenshot=f'{b}-oct10-stitch-desktop.png', fullScreenshotDimensions=dims, nativeMobileCorrection=False), assets=dict(manifest=f'{b}-oct10-assets.json',count=44,publicContentFailures=0,unusedOriginalVideo='Original Dev workflow MP4 preserved but not referenced by selected Creative concrete preview.'), remainingDifferences=remaining, designAnalysis=f'{b}-oct10-analysis.md', rewrittenPrompt=f'{b}-oct10-reproduction-prompt.md', providerClaimsAndSuggestions=f'{b}-oct10-provider-notes.md', hashManifest=f'{b}-oct10-file-hashes.json', noPaidActions=True, scopeNote='CSS responsive viewports with desktopUA; explicitly selected Creative state; no account services/deployment review.', handoff='Root integrates and verifies publication; no global/progress/hosting edits by this agent.')
(w / f'{b}-oct10-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
build = json.loads((w/f'{b}-oct10-build-record.json').read_text());build['remaining']=remaining;build['actualReview']=f'{b}-oct10-result.json'
(w/f'{b}-oct10-build-record.json').write_text(json.dumps(build,indent=2)+'\n')
pending = json.loads((w/f'{b}-oct10-pending.json').read_text());pending.update(status='resolved_to_scoped_visual_review',previewSha256=sha,supersededBy=f'{b}-oct10-result.json',required=[],limitations=remaining,nativeEdit={'status':'completed','screen':native['screen'],'sessionId':native['sessionId']},assets={'manifest':f'{b}-oct10-assets.json','count':44,'failures':0})
(w/f'{b}-oct10-pending.json').write_text(json.dumps(pending,ensure_ascii=False,indent=2)+'\n')
paths=[p for p in w.glob(b+'*') if p.is_file() and p.name!=b+'-oct10-file-hashes.json']+[p for p in (w/(b+'-assets')).rglob('*') if p.is_file()]+[p for p in Path('scripts').glob('*'+b+'*') if p.is_file()]
(w/f'{b}-oct10-file-hashes.json').write_text(json.dumps({'recordedAt':now,'files':{str(p):{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths}},indent=2)+'\n')
print(json.dumps({'brand':b,'previewSha256':sha,'accepted':False,'nativeDimensions':dims}))
