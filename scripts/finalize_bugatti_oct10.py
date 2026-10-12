from pathlib import Path
import json,hashlib,datetime
from PIL import Image
w=Path('.stitch-work/current-official');b='bugatti';now=datetime.datetime.now(datetime.timezone.utc).isoformat();sha=hashlib.sha256((w/f'{b}.html').read_bytes()).hexdigest()
assert json.loads((w/f'{b}-oct10-native-coverage.json').read_text())['previewSha256']==sha
native=json.loads((w/f'{b}-oct10-native-export-hashes.json').read_text());dims=list(Image.open(w/f'{b}-oct10-stitch-desktop.png').size);assert dims==native['declaredDimensions']
assets=json.loads((w/f'{b}-oct10-assets.json').read_text());assert len(assets['assets'])==107 and not assets['failures']
assert Image.open(w/f'{b}-oct10-official-initial-popup.jpg').size==(1280,720)
assert Image.open(w/f'{b}-oct10-corrected-narrow-playback.jpg').size==(390,844)
playback=json.loads((w/f'{b}-oct10-corrected-narrow-playback.json').read_text());assert len(playback['videos'])==3 and all(v['ready']==4 for v in playback['videos']) and sum(not v['paused']and v['currentTime']>1 for v in playback['videos'])==2
playback['previewSha256']=sha;(w/f'{b}-oct10-corrected-narrow-playback.json').write_text(json.dumps(playback,indent=2)+'\n')
guard=json.loads((w/f'{b}-oct10-source-scroll-guard.json').read_text())
for x in guard.values():x['guard']=x['guard'].replace('~0.03px','~0.06px')
(w/f'{b}-oct10-source-scroll-guard.json').write_text(json.dumps(guard,indent=2)+'\n')
scopes=[]
for mode,width,height,sourceTotal,localTotal,count,segments in [('desktop',1280,720,7112,7119,10,4),('narrow',390,844,8584,8592,11,5)]:
 r=json.loads((w/f'{b}-oct10-official-{width}-reference.json').read_text());html=''.join(r['htmlParts']);a=json.loads((w/f'{b}-oct10-corrected-{mode}.json').read_text())
 assert len(html.encode('utf-16-le'))//2==r['html_length']and hashlib.sha256(html.encode()).hexdigest()==r['html_sha256']and html.endswith('</html>')
 source=json.loads((w/f'{b}-oct10-official-{width}-phases.json').read_text());phases=json.loads((w/f'{b}-oct10-corrected-{width}-phases.json').read_text())
 assert len(source)==len(phases)==count and all(p['draft_sha256']==sha and p['bodyHeight']==localTotal for p in phases)
 assert a['height']==localTotal and a['scrollWidth']==width and a['fontStatus']=='loaded'and len(a['images'])==20 and all(i['loaded']for i in a['images'])
 headings=[h for h in a['headings']if h['level']in ['H1','H2','H3']];assert len(headings)==len(source[0]['headings'])==16
 diffs=[]
 for x,y in zip(source[0]['headings'],headings):
  assert x['text']==y['text'];d=max(abs(x['box'][k]-y['bounds'][k])for k in ['x','y','width','height']);diffs.append(d);assert d<=.01
 scopes.append(dict(scope=mode,viewport=a['viewport'],sourceURL=r['url'],previewURL=a['url'],previewObservedAt=a['observedAt'],sourceHeight=sourceTotal,previewHeight=localTotal,heightDifference=localTotal-sourceTotal,noHorizontalOverflow=True,fontStatus='loaded',allDomImages=20,imagesNotReady=0,sourcePhases=count,previewPhases=count,completeSequentialViewportCoverage=True,trueScreenshotDimensions=[width,height],comparisonSegments=[f'{b}-oct10-compare-{mode}-{i}.png'for i in range(segments)],matchingMainHeadingCount=16,maxHeadingBoundsDifference=max(diffs),sourceCompleteness=dict(utf16Units=r['html_length'],sha256=r['html_sha256'],complete=True),smoothScrollSourceGuard=f'{b}-oct10-source-scroll-guard.json'))
remaining=[
 'The preview restores native document scrolling from the official fixed smooth-wrapper/translated smooth-content. Official source was explicitly allowed to settle before every screenshot. Exact smooth scrolling, reveal/blur timing, parallax positions and image crop movement differ; source composites visibly contain changing parallax crops between phases.',
 'The original3public main-page videos load and play (readyState4; two visible videos observed progressing above1s). Their frames and initial playback timing differ. No frame-by-frame, model hover-video or desktop/narrow movie synchronization is accepted.',
 'Source/corrected page heights are7112/7119px desktop (+7) and8584/8592px narrow (+8). All16main H1/H2/H3 texts and bounds match within0.01px at both widths; the remaining footer/end-canvas geometry is not accepted as exact parity.',
 'Recruitment toast was dismissed through its public Close button before full-page review; its actual initial screenshot is preserved. Menu/drawer, category/hover model states, social Load more, privacy/cookie and language controls, full keyboard/focus behavior and destination/service routes are not implemented or accepted by this static correction. The source social grid had no posts, with a desktop Load more button and hidden narrow grid; no invented posts were added.',
 'Fresh genuine Stitch edit is DESKTOP only. Prior original DESKTOP/MOBILE/DESIGN.md/design-md remain preserved. Other sizes, real phone hardware, locales/routes and published deployment are not reviewed.'
]
analysis='''# Bugatti 目前公開首頁設計分析

來源 https://www.bugatti.com/，觀察2026-10-11。當日仍為Destrier電影主視覺，Menu/BUGATTI/Store透明導覽、原始Destrier手寫SVG、等寬宣傳文字與桌面描邊/窄版底線CTA。三種原始字型Bugatti Display/Text/Monospace，黑色頁底；桌面48px邊距、60px大標，窄版12px邊距、36px大標與直排內容。招聘提示經可見Close關閉後比較，初始實拍另保存。

完整順序為La Maison三卡、Programme Solitaire與Sur Mesure兩支原始影片、HONMA/C SEED當日生活風格卡、六車型Tourbillon/W16 Mistral/Bolide/Chiron/Divo/Centodieci網格、BUGATTI Live、原始手寫引言與四欄完整頁尾。當日社群格沒有文章，桌面顯示Load more、窄版隱藏；未加入虛構社群內容。

官方GSAP平滑捲動會讓scrollY先改變而可見內容尚未到位；一般截圖在這個網站不構成完整可靠證據。已保留錯誤步距/未穩定的早期資料，校正為半量wheel並逐段讀取smooth-content矩陣，直到translationY≈-scrollY誤差小於0.15px且連續三次穩定才拍攝。來源主標docY於整頁約0.06px內穩定，完整桌面10段7112px、窄版11段8584px；真實1280×720/390×844尺寸、連續覆蓋、完整來源長度/hash/結尾均檢查。

genuine Google Stitch MCP新桌面稿保留完整指令/回應/rawHTML/未改縮圖/fullPNG；具體成品再用完整當日DOM/CSS與107份原始素材校正，匯出/傳輸失敗分別保留並補回，最終素材失敗0。取消來源固定平滑容器，改為原生文件捲動，照片採原始scale1.1靜態裁切。三支主頁影片實測readyState4，兩支同畫面可見影片已播放超過1秒；所有20張DOM圖片與字型載入、無溢位，16個主要標題座標/尺寸在兩寬均誤差不超過0.01px。全部4張桌面與5張窄版比較圖目視核對；成品頁尾總長仍比來源多7/8px，保留差異。

'''+''.join('- '+x+'\n'for x in remaining)+'\naccepted=false；未付費、未部署、未提交帳戶/表單，帳戶計費未稽核。\n'
(w/f'{b}-oct10-analysis.md').write_text(analysis)
(w/f'{b}-oct10-reproduction-prompt.md').write_text('''# Rewritten AI instruction — Bugatti current public homepage

Reconstruct https://www.bugatti.com/ as actually observed2026-10-11. Preserve Destrier's authentic SVG/cinematic video, exact Menu/BUGATTI/Store navigation, original Bugatti Display/Text/Monospace,60px/36px section titles,48px/12px gutters, true Maison/Solitaire/Sur Mesure/HONMA/C SEED/six-model/Live/signature/footer order and public assets. Source Live grid is empty with desktop Load more and hidden narrow content; don't invent social posts, accounts or specifications. Recruitment toast review scope is after the visible Close action, retaining initial screenshot.

Retain fresh genuine DESKTOP/full response/exact prompt/rawHTML/original thumbnail/fullPNG and prior native MOBILE/DESIGN.md/design-md. Correct concrete page from complete source DOM/CSS and107 originals. Explicitly settle official smooth-content transformY to negative scrollY before screenshots; use half wheel distance to prevent missing coverage. Restore native document flow for the static study, preserve actual public videos and photos, document parallax/reveal/crop/frame differences. Verify actual source/corrected1280×720 and390×844 complete10/11-phase pages, true dimensions/hash/coverage,20loaded images/fonts/no overflow,16matching main headings within0.01px, and video readiness/playback. Disclose source/corrected7112/7119 desktop and8584/8592 narrow footer differences, unavailable UI/social/privacy/language/services/native MOBILE/other widths/deployment. Provider verified/authentic/precise statements are not validation. accepted=false; no paid actions or account/form submission.
''')
(w/f'{b}-oct10-provider-notes.md').write_text('''# Genuine Google Stitch provenance and unverified provider statements

Fresh DESKTOP project16684760316385838723/session7536732851875743783/screenefc859e290d041f9b038c409a777c605. Full response/exact prompt/rawHTML/unchanged thumbnail/fullPNG preserve exact provider URLs/bytes/hashes. Actual fullPNG2560×14344 independently matches provider metadata.

Provider says verified public observation, authentic photography, exact headings, and real-world cookie consent preserved. These statements do not establish validation. Its added Account navigation link and fixed-header claim are not present in observed source (Menu/BUGATTI/Store within scroll content). Cookie consent parity was not inspected or accepted. Concrete source correction follows actual original public content/assets, not these assertions; all native exports remain unmodified.

Suggestions retained: explore Tourbillon model detail; inspect mobile drawer; refine Destrier hero contrast. These suggestions are not completed validation or fresh native MOBILE. No purchase/upgrades; account billing not audited.
''')
verified=['Fresh genuine desktop Stitch edit and unchanged native originals retained.','Complete current source DOM/CSS corrected with107public assets; final content failures0.','Source/corrected10desktop and11narrow actual viewport phases with true dimensions/coverage/hash; official smooth transforms settled before source images; all9comparison segments reviewed.','20images and original fonts loaded at both widths, no overflow;16main headings match within0.01px;3main videos readyState4 and two visible videos observed playing beyond1s.']
result=dict(brand=b,recordedAt=now,status='visually_compared_with_scoped_differences',accepted=False,reference_url='https://www.bugatti.com/',preview='bugatti.html',previewSha256=sha,sourceCorrectionCompleted=True,recordUpdates=dict(status='visually_compared_with_scoped_differences',accepted=False,reference_url='https://www.bugatti.com/',native_screen=native['screen'],preview='bugatti.html',verified=verified,remaining=remaining,review_note='已依當日Destrier完整來源重製並完成穩定平滑捲動後桌面/窄版全頁實拍；16主要標題相合，頁尾7/8px、視差、影片與互動仍未接受官方一致。'),checks=scopes,nativeGeneration=dict(reused=False,screen=native['screen'],sessionId=native['sessionId'],fullRawResponse=f'{b}-oct10-native-response.json',rawHtml=f'{b}-oct10-stitch-desktop.html',fullNativeScreenshot=f'{b}-oct10-stitch-desktop.png',fullScreenshotDimensions=dims,nativeMobileCorrection=False),assets=dict(manifest=f'{b}-oct10-assets.json',count=107,publicContentFailures=0,bytes=sum(a['bytes']for a in assets['assets'])),remainingDifferences=remaining,designAnalysis=f'{b}-oct10-analysis.md',rewrittenPrompt=f'{b}-oct10-reproduction-prompt.md',providerClaimsAndSuggestions=f'{b}-oct10-provider-notes.md',hashManifest=f'{b}-oct10-file-hashes.json',noPaidActions=True,scopeNote='CSS responsive viewports with desktopUA; toast dismissed; no account/services/deployment review.',handoff='Root integrates and verifies publication; no global/progress/hosting edits by this agent.')
(w/f'{b}-oct10-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
build=json.loads((w/f'{b}-oct10-build-record.json').read_text());build['remaining']=remaining;build['actualReview']=f'{b}-oct10-result.json';(w/f'{b}-oct10-build-record.json').write_text(json.dumps(build,indent=2)+'\n')
paths=[p for p in w.glob(b+'*')if p.is_file()and p.name!=b+'-oct10-file-hashes.json']+[p for p in (w/(b+'-assets')).rglob('*')if p.is_file()]+[p for p in Path('scripts').glob('*'+b+'*')if p.is_file()]
(w/f'{b}-oct10-file-hashes.json').write_text(json.dumps({'recordedAt':now,'files':{str(p):{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p in paths}},indent=2)+'\n')
print(json.dumps({'brand':b,'previewSha256':sha,'accepted':False,'nativeDimensions':dims}))
