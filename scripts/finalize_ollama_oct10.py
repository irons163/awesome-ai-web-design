from pathlib import Path
import json,hashlib,datetime
w=Path('.stitch-work/current-official');b='ollama';now=datetime.datetime.now(datetime.timezone.utc).isoformat()
coverage=json.loads((w/f'{b}-oct10-native-coverage.json').read_text());sha=hashlib.sha256((w/f'{b}.html').read_bytes()).hexdigest();assert coverage['previewSha256']==sha
scopes=[]
for mode,width,height in [('desktop',1280,720),('narrow',390,844)]:
 r=json.loads((w/f'{b}-oct10-official-{width}-reference.json').read_text());p=json.loads((w/f'{b}-oct10-corrected-{mode}.json').read_text());html=''.join(r['htmlParts'])
 assert len(html.encode('utf-16-le'))//2==r['html_length'] and hashlib.sha256(html.encode()).hexdigest()==r['html_sha256'] and html.endswith('</html>')
 assert p['height']==(786 if width==1280 else 1000) and all(i['loaded']for i in p['images']) and p['scrollWidth']==width
 scopes.append(dict(scope=mode,viewport=p['viewport'],sourceURL=r['url'],previewURL=p['url'],previewObservedAt=p['observedAt'],sourceHeight=p['height'],previewHeight=p['height'],heightDifference=0,noHorizontalOverflow=True,fontStatus=p['fontStatus'],allDomImages=len(p['images']),imagesNotReady=0,sourcePhases=2,previewPhases=2,completeSequentialViewportCoverage=True,comparisonSegments=[f'{b}-oct10-compare-{mode}-{i}.png'for i in range(2)],sourceCompleteness=dict(utf16Units=r['html_length'],sha256=r['html_sha256'],complete=True)))
remaining=['The narrow captured end-state header retains data-scrolled at the top, so a one-pixel gray bottom rule is visible locally at scrollY0 while the source top screenshot has no rule. The source and local rule agree after scrolling.','The native CSS narrow menu opens and closes with the same five links. The local open-menu screenshot retains a visible vertical scrollbar; the source open-menu screenshot hides it. Scroll locking and full keyboard/focus parity were not accepted.','The fresh Stitch output is a DESKTOP candidate (2560×2048), and its provider response omits the current Meetups footer link. The source-corrected preview retains the actual public link. No new native MOBILE screen was generated.','Sign-in, account creation, model downloads, other pages, real phone hardware, other viewport widths and published deployment are outside this review. No account forms were submitted.']
analysis='''# Ollama 目前公開首頁設計分析

來源 https://ollama.com/，實際觀察及最後校正2026-10-11。官方已從舊版長頁改為精簡白色首頁：細黑線羊駝、右側導覽與182.7K GitHub顯示值、22px主標、20/28px說明、黑色 Get started 圓角按鈕。保留當日官方宣稱的9M+、1B+、200T+，只作有日期的版面內容記錄；十二個灰色公開品牌商標、寬敞右側留白與完整頁尾來自目前官方DOM/CSS/資產。窄版商標改為三欄四列，並有五個連結的全白選單。

新版與原保存設計不同，因此透過 genuine Google Stitch MCP 新增校正屏幕。原候選、完整工具回應、供應者文字/建議與新原始HTML/全尺寸PNG/縮圖分別保留。以完整官方來源及19份公開原資產校正可操作本機頁面，未將供應者的精確性宣稱當成驗證。

1280×720與390×844各兩張實際視窗截圖完整覆蓋786px與1000px頁高；PIL確認實際影像尺寸、頂部/底部與捲動覆蓋。四張逐視窗比較圖與窄版開啟選單圖均已目視檢查。兩尺寸各13張DOM圖片均載入、字型完成、無水平溢位。文字、商標、主要區塊及頁尾位置相合；細線與選單捲軸差異列於下方。

'''+''.join('- '+x+'\n'for x in remaining)+'\naccepted=false，沒有宣稱全面官方一致。沒有購買、付費升級或部署；帳戶計費未稽核。\n'
(w/f'{b}-oct10-analysis.md').write_text(analysis)
(w/f'{b}-oct10-reproduction-prompt.md').write_text('''# Rewritten AI instruction — Ollama current public homepage

Reconstruct https://ollama.com/ as observed2026-10-11. Keep the compact current white homepage, not the obsolete long product/pricing/video layout. Preserve the thin black llama mark, current navigation/GitHub count, exact22px heading and20/28px public paragraph, Get started pill, dated9M+/1B+/200T+ claims, twelve actual public gray customer marks and the complete current footer including Meetups. Do not add product claims, pricing, models, videos or testimonials.

Preserve genuine Google Stitch MCP full response and independent raw outputs; the new DESKTOP screen is projects/7741861711625842120/screens/80eb23ef4d3d4eb6b0ef6a1f10541800. Keep original prior native assets and DESIGN.md/design-md. Use complete verified1280/390 DOM chunks, original CSS and19exact public originals for source correction. Compare actual1280×720 and390×844 CSS responsive viewports with unchanged desktopUA; ensure13images loaded, full786/1000px coverage and native checkbox menu open/close. Declare the retained initial gray header rule, local menu scrollbar, native MOBILE gap, account services, real devices and untested widths. No form submission or paid action. accepted=false until broader acceptance is supported.
''')
(w/f'{b}-oct10-provider-notes.md').write_text('''# Genuine Google Stitch provenance

Fresh edit output: project7741861711625842120, session14228964223863179625, DESKTOP screen80eb23ef4d3d4eb6b0ef6a1f10541800, declared2560×2048. Full raw MCP response is ollama-oct10-native-correction-response.json; request is ollama-oct10-native-correction-prompt.txt. Native raw HTML, provider thumbnail512×410 and full2560×2048 PNG are independent files, with original URLs/hashes in ollama-oct10-native-export-hashes.json. Prior original generation/native/DESIGN.md/design-md were preserved.

Provider response calls the customer marks exact and says it implemented the current page; these are unverified provider claims, not evidence of fidelity. Its footer list omitted Meetups, while the actual source correction retains it. Provider suggestions were to create the corresponding390×844 mobile version and inspect typography/spacing. No native MOBILE correction is claimed. Actual source/preview screenshots, rather than provider text or dimensions, establish the limited scope.

No purchases or paid upgrades were performed; account billing was not audited.
''')
verified=['Complete current public source reconstruction after fresh genuine Google Stitch MCP correction.','Both DOM references verified by complete UTF16 length, SHA256 and closing html tag;19public originals cached without failures.','Each source/local viewport has2actual JPEG screenshots with PIL true1280×720/390×844 dimensions and full786/1000px scroll coverage.','All4main-page comparison pairs and narrow menu pair visually reviewed;13DOMimages load at each width,fonts loaded,no overflow; native menu opened/closed.']
screen='projects/7741861711625842120/screens/80eb23ef4d3d4eb6b0ef6a1f10541800'
result=dict(brand=b,recordedAt=now,status='visually_compared_with_scoped_differences',accepted=False,reference_url='https://ollama.com/',preview='ollama.html',previewSha256=sha,sourceCorrectionCompleted=True,recordUpdates=dict(status='visually_compared_with_scoped_differences',accepted=False,native_screen=screen,preview='ollama.html',verified=verified,remaining=remaining,review_note='已依目前精簡官方首頁重製，完成指定桌面/窄版完整實際畫面及窄版選單比較；細線、捲軸及未測範圍明確保留，未接受為全面官方一致。'),checks=scopes,nativeGeneration=dict(reused=False,screen=screen,sessionId='14228964223863179625',fullRawResponse='ollama-oct10-native-correction-response.json',rawHtml='ollama-oct10-stitch-desktop.html',fullNativeScreenshot='ollama-oct10-stitch-desktop.png',fullScreenshotDimensions=[2560,2048],nativeMobileCorrection=False),assets=dict(manifest='ollama-oct10-assets.json',count=19,failures=[]),remainingDifferences=remaining,designAnalysis='ollama-oct10-analysis.md',rewrittenPrompt='ollama-oct10-reproduction-prompt.md',providerClaimsAndSuggestions='ollama-oct10-provider-notes.md',hashManifest='ollama-oct10-file-hashes.json',noPaidActions=True,scopeNote='CSS responsive viewports with desktopUA; real phone hardware/account services/published deployment not reviewed.',handoff='Root integrates and verifies published deployment; no progress/global/hosting changes by this agent.')
(w/f'{b}-oct10-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
paths=[p for p in w.glob(b+'*')if p.is_file()and p.name!=b+'-oct10-file-hashes.json']+[p for p in (w/(b+'-assets')).rglob('*')if p.is_file()]+[p for p in Path('scripts').glob('*'+b+'*')if p.is_file()]
(w/f'{b}-oct10-file-hashes.json').write_text(json.dumps({'recordedAt':now,'files':{str(p):{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p in paths}},indent=2)+'\n')
print(json.dumps({'brand':b,'previewSha256':sha,'accepted':False,'heights':[786,1000]}))
