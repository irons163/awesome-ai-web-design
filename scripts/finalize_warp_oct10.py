from pathlib import Path
import json, hashlib, datetime
from PIL import Image

w=Path('.stitch-work/current-official'); b='warp'; now=datetime.datetime.now(datetime.timezone.utc).isoformat()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
final=sha(w/'warp.html'); coverage=json.loads((w/f'{b}-oct10-native-coverage.json').read_text())
proof=json.loads((w/f'{b}-oct10-chart-frame-diff-proof.json').read_text())
assert coverage['previewSha256']==proof['priorFullPageSha256'] and final==proof['finalSha256']
html=(w/'warp.html').read_text(); assert html.count('class=\\"roi-chart no-frame\\"')==2
assert hashlib.sha256(html.replace('class=\\"roi-chart no-frame\\"','class=\\"roi-chart\\"').encode()).hexdigest()==proof['priorFullPageSha256']
checks=[]
for mode,width,height,pageheight,phases,segments in [('desktop',1280,720,9395,14,5),('narrow',390,844,14041,17,8)]:
 r=json.loads((w/f'{b}-oct10-official-{width}-reference.json').read_text()); source=''.join(r['htmlParts'])
 assert len(source.encode('utf-16-le'))//2==r['html_length'] and hashlib.sha256(source.encode()).hexdigest()==r['html_sha256'] and source.endswith('</html>')
 audit=json.loads((w/f'{b}-oct10-corrected-{mode}.json').read_text())
 assert audit['height']==pageheight and audit['scrollWidth']==width and len(audit['images'])==70 and all(x['loaded']for x in audit['images']) and audit['fontStatus']=='loaded'
 p=json.loads((w/f'{b}-oct10-corrected-final-native-{width}-phases.json').read_text()); assert len(p)==phases and all(x['draft_sha256']==coverage['previewSha256']for x in p)
 supplement=json.loads((w/f'{b}-oct10-final-chart-{mode}.json').read_text()); shot=w/f'{b}-oct10-final-chart-{mode}.jpg'
 assert Image.open(shot).size==(width,height) and supplement['loaded'] and supplement['boxShadow']=='none' and supplement['height']==pageheight
 checks.append(dict(scope=mode,viewport=[width,height],sourceURL=r['url'],sourceObservedAt=r['observed_at'],sourceHeight=pageheight,previewHeight=pageheight,heightDifference=0,sourcePhases=phases,previewPhases=phases,completeSequentialViewportCoverage=True,actualScreenshotDimensionsGuarded=True,previewPhaseSha256=coverage['previewSha256'],finalSha256=final,finalChartSupplement=dict(screenshot=shot.name,sha256=sha(shot),observedAt=supplement['observedAt'],loaded=True,boxShadow='none'),allDomImages=70,sourceDomImages=len(r['images']),imagesNotReady=0,fontStatus='loaded',noHorizontalOverflow=True,sourceCompleteness=dict(utf16Units=r['html_length'],sha256=r['html_sha256'],complete=True),comparisonSegments=[f'{b}-oct10-compare-{mode}-{i}.png'for i in range(segments)],allComparisonSegmentsVisuallyReviewed=True))
proof['finalActualChartSupplementsPending']=False;proof['finalActualChartSupplementsComplete']=True
(w/f'{b}-oct10-chart-frame-diff-proof.json').write_text(json.dumps(proof,indent=2)+'\n')
remaining=[
 'The 224 task-grid statuses, PR counts, live roster, logo marquee position, section boot text and reveal opacity differ by captured animation phase. The corrected page retains observed static task/roster states and CSS motion. Exact timing is not accepted; the official narrow source itself was captured with several headings mid-fade.',
 'The cost-per-PR canvas is represented by dated crops of actual official desktop/narrow screenshots, with provenance and independent bounds. It is a static drawing without hover, scrubbing or live recomputation. The computer-use story is a captured illustrative state, not a working browser or sales form.',
 'The header is restored at scrollY0 and blue desktop section navigation appears after scrolling. The 64px local swap threshold was not independently established as the exact official threshold; transitional positions are not accepted.',
 'Configuration directory tabs, folder expansion, SDLC switchers, the mobile menu, sign-in/get-started popovers, FAQ expansion, operating-system switchers, copy/download actions and sound controls were not implemented or accepted as complete official interaction parity. Public destination links are retained; no account action, form submission, command execution or download installation was performed.',
 'The fresh native Stitch output is DESKTOP only. Its declared 2560×16384 screenshot exports as an actual 2560×16383 PNG; no fresh native MOBILE output is claimed. Provider assertions of authenticity, a live stdout runner stream and +3.7x are not validation; the source-corrected page retains the observed SDLC image and +3.7.',
 'Other pages, account/product services, real phone hardware, untested widths and published deployment are outside this review. accepted=false; no comprehensive official-equivalence claim.'
]
analysis='''# Warp 目前公開首頁設計分析

來源 https://www.warp.dev/，2026-10-11實際觀察。當前首頁已新增「Your software factory, defined in code.」完整配置區，不能沿用舊版頁面。白色與淡紫紙張背景、細黑線、技術等寬字體、74px桌面邊距、56px兩行主標、皇家藍#2818F4和淡黃色Book a demo共同構成新版。英雄區8×28任務格、17個當日品牌證明、八個配置類別及23行factory.yaml、六項SDLC、三個品質指標、藍色成本案例、企業故事、四層開放架構、治理圖表、三項產品、九項FAQ和完整2026頁尾均保留。

新版已透過 genuine Google Stitch MCP 產生獨立校正候選。原始完整工具回應、供應者HTML、全尺寸PNG和縮圖，以及舊候選/DESIGN.md/design-md均分別保留。以完整分塊官方DOM、CSS和84份公開原始素材進行實際頁面校正；成本圖表另保存兩份官方實際視窗擷取，明確標記為靜態canvas記錄。

桌面1280×720與窄版390×844各14與17段實際JPEG，完整覆蓋9395px與14041px頁高。PIL逐張確認影像尺寸，檢查頂部、頁尾、連續捲動和HTML SHA256；5張桌面與8張窄版比較圖均已目視檢查。兩尺寸各70張本機DOM圖片全部載入，字型完成且無水平溢位。最後只移除兩張圖表誤套的圖片外框，另附確切hash差異證明與兩尺寸實際補拍。

'''+''.join('- '+x+'\n'for x in remaining)+'\n未購買、未付費升級或部署；帳戶計費未稽核。\n'
(w/f'{b}-oct10-analysis.md').write_text(analysis)
(w/f'{b}-oct10-reproduction-prompt.md').write_text('''# Rewritten AI instruction — Warp current public homepage

Reconstruct https://www.warp.dev/ as observed2026-10-11, preserving the current Configuration section instead of the obsolete prior layout. Keep the white/lavender paper, fine rules, royal blue#2818F4, technical mono typography, exact current navigation, yellow Book a demo, 56px two-line desktop heading, 224-cell factory figure, actual proof marks, eight configuration categories, original23-line factory.yaml, six SDLC rows and actual setup image, 96%/1.00x/+3.7 charts, $80-to-$30 case study, current benchmark asset, Rectangle Health and Docker stories, open layers, governance, three products, nine FAQs and full2026 footer. All claims are dated public design content, not independent product/financial validation.

Preserve genuine Google Stitch MCP full response and raw candidate separately: projects/15794086566439011906/screens/cb27713199f84cd6855b85d7c9d4a277, session4607812042676727197. Do not adopt provider-invented stdout visualization or +3.7x. Keep old native screens and DESIGN.md/design-md. Correct the concrete preview using complete1280/390 source chunks, current CSS and84exact public assets. Preserve dated canvas crops with source screenshots/bounds; never call a static drawing live or interactive. Verify actual1280×720 and390×844 sequential viewport captures, full9395/14041px coverage, image/font loading, current headings and footer. Record all motion/UI/nativeMOBILE/device/deployment gaps and maintain accepted=false while unresolved. No account services, paid actions, form transmission or CLI execution.
''')
(w/f'{b}-oct10-provider-notes.md').write_text('''# Genuine Google Stitch provenance

Fresh DESKTOP edit: project15794086566439011906, screen cb27713199f84cd6855b85d7c9d4a277, session4607812042676727197. Exact request and full tool response are warp-oct10-native-correction-prompt.txt and warp-oct10-native-correction-response.json. Raw provider HTML, PNG and thumbnail are retained independently with original URLs/hashes in warp-oct10-native-export-hashes.json. Declared dimensions2560×16384; full downloaded PNG actual2560×16383. Old native desktop/mobile screens, DESIGN.md and design-md exports were preserved. Prior warp-generated.json is an unrelated PulseTerm project and is not substituted as generation evidence.

Provider words such as authentic, exact and accurate are provider assertions, not validation. Its live stdout terminal runner stream and +3.7x interpretation differ from the observed SDLC setup image and +3.7; the source-corrected preview retains actual source content. Provider suggested: create a390px mobile companion, add interactive switching for eight configuration files, and export the224-task grid/factory.yaml as reusable components. These suggestions are preserved as suggestions, not reported as completed native output or validated functionality.

No purchases or paid upgrades were performed; account billing was not audited.
''')
verified=['Current complete public homepage concretely corrected after fresh genuine Google Stitch MCP edit.','Complete source HTML UTF16 lengths/SHA256/closing tags verified;84public original assets preserved without failures, plus2dated actual-canvas crops.','Desktop14 and narrow17 actual viewport screenshots per side cover the entire9395/14041px pages; PIL native1280×720/390×844 dimensions guarded.','All13main comparison segments visually reviewed;70local DOM images per width loaded,fonts loaded,no overflow. Final two chart-frame class fixes are bounded by hash proof and actual desktop/narrow supplements.']
screen='projects/15794086566439011906/screens/cb27713199f84cd6855b85d7c9d4a277'
result=dict(brand=b,recordedAt=now,status='visually_compared_with_scoped_differences',accepted=False,reference_url='https://www.warp.dev/',preview='warp.html',previewSha256=final,sourceCorrectionCompleted=True,recordUpdates=dict(status='visually_compared_with_scoped_differences',accepted=False,native_screen=screen,preview='warp.html',verified=verified,remaining=remaining,review_note='已依新版官方完整公開首頁校正，完成指定桌面/窄版連續實際全頁比較；動態狀態、互動、native MOBILE及其他範圍明確保留，未接受為全面官方一致。'),checks=checks,nativeGeneration=dict(reused=False,screen=screen,sessionId='4607812042676727197',fullRawResponse='warp-oct10-native-correction-response.json',rawHtml='warp-oct10-stitch-desktop.html',fullNativeScreenshot='warp-oct10-stitch-desktop.png',declaredScreenshotDimensions=[2560,16384],actualScreenshotDimensions=list(Image.open(w/'warp-oct10-stitch-desktop.png').size),nativeMobileCorrection=False),assets=dict(manifest='warp-oct10-assets.json',publicOriginalCount=84,failures=[],additionalStaticCanvasCrops=2,canvasProvenance='warp-oct10-canvas-provenance.json'),finalChangeProof='warp-oct10-chart-frame-diff-proof.json',remainingDifferences=remaining,designAnalysis='warp-oct10-analysis.md',rewrittenPrompt='warp-oct10-reproduction-prompt.md',providerClaimsAndSuggestions='warp-oct10-provider-notes.md',hashManifest='warp-oct10-file-hashes.json',noPaidActions=True,scopeNote='CSS responsive viewports with unchanged desktop UA; animation timing, real hardware, account services and published deployment not accepted.',handoff='Root integrates and verifies deployment. This agent did not change progress/global/hosting files.')
(w/f'{b}-oct10-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
build=json.loads((w/f'{b}-oct10-build-record.json').read_text());build['html']={'bytes':(w/'warp.html').stat().st_size,'sha256':final};build['remaining']=remaining;build['actualReviewResult']='warp-oct10-result.json';(w/f'{b}-oct10-build-record.json').write_text(json.dumps(build,indent=2)+'\n')
paths=[p for p in w.glob(b+'*')if p.is_file()and p.name!=b+'-oct10-file-hashes.json']+[p for p in (w/(b+'-assets')).rglob('*')if p.is_file()]+[p for p in Path('scripts').glob('*'+b+'*')if p.is_file()]
(w/f'{b}-oct10-file-hashes.json').write_text(json.dumps({'recordedAt':now,'files':{str(p):{'bytes':p.stat().st_size,'sha256':sha(p)}for p in paths}},indent=2)+'\n')
print(json.dumps({'brand':b,'previewSha256':final,'accepted':False,'heights':[9395,14041],'finalChartSupplements':True}))
