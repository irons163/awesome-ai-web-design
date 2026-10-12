from pathlib import Path
import json,hashlib,datetime
from PIL import Image
w=Path('.stitch-work/current-official');b='zapier';now=datetime.datetime.now(datetime.timezone.utc).isoformat()
sha=hashlib.sha256((w/f'{b}.html').read_bytes()).hexdigest();coverage=json.loads((w/f'{b}-oct10-native-coverage.json').read_text());assert coverage['previewSha256']==sha
native=json.loads((w/f'{b}-oct10-native-export-hashes.json').read_text());dims=list(Image.open(w/f'{b}-oct10-stitch-desktop.png').size);assert dims==native['declaredDimensions']
scopes=[]
for mode,width,height,total,segments in [('desktop',1280,720,9508,5),('narrow',390,844,11137,6)]:
 r=json.loads((w/f'{b}-oct10-official-{width}-reference.json').read_text());p=json.loads((w/f'{b}-oct10-corrected-{mode}.json').read_text());html=''.join(r['htmlParts'])
 assert len(html.encode('utf-16-le'))//2==r['html_length'] and hashlib.sha256(html.encode()).hexdigest()==r['html_sha256'] and html.endswith('</html>')
 phases=json.loads((w/f'{b}-oct10-corrected-native-{width}-phases.json').read_text());assert len(phases)==14 and all(x['draft_sha256']==sha for x in phases)
 assert p['height']==total and len(p['images'])==44 and all(i['loaded'] for i in p['images']) and p['scrollWidth']==width
 scopes.append(dict(scope=mode,viewport=p['viewport'],sourceURL=r['url'],previewURL=p['url'],previewObservedAt=p['observedAt'],sourceHeight=total,previewHeight=p['height'],heightDifference=0,noHorizontalOverflow=True,fontStatus=p['fontStatus'],allDomImages=44,imagesNotReady=0,sourcePhases=14,previewPhases=14,completeSequentialViewportCoverage=True,comparisonSegments=[f'{b}-oct10-compare-{mode}-{i}.png'for i in range(segments)],sourceCompleteness=dict(utf16Units=r['html_length'],sha256=r['html_sha256'],complete=True)))
remaining=[
 'Official scroll-entry reveal animations appear partially faded and translated in several actual source phases; the source-corrected template retains its fully revealed captured state. Exact opacity/translation and reveal timing are not accepted as official parity.',
 'Hero, MCP, workflow and governance video frames, video playback state and moving partner-logo positions differ in time. Public original media bytes are preserved; frame-by-frame motion synchronization is outside this review.',
 'Navigation mega menus/mobile drawer, feature accordion switching, agency slider/tab switching, customer carousel switching, footer Show more, cookie/privacy controls, full keyboard/focus behavior and account/service flows are not implemented or accepted by this static source correction. Links lead to observed official destinations; no account or form submission occurred.',
 'Fresh genuine Stitch edit is DESKTOP only. Existing prior native desktop/mobile exports remain preserved. Other viewports, real phone hardware, other routes/locales and published deployment are not reviewed.'
]
analysis='''# Zapier 目前公開首頁設計分析

來源 https://zapier.com/，觀察2026-10-11。目前仍是 Welcome to automation in the agentic era 的暖白編輯式首頁：56px黏性導覽、Degular Display兩行桌面主標、三行窄版主標、橘色email與描邊Google按鈕；桌面原始產品影片位於x128/y459，寬1024px。保留真實原始字型、logo與產品影像，不使用生成稿中的終端機或虛構控制台。

完整順序為合作品牌條、Build anywhere宣言、Zapier MCP、Next Gen Zaps、深咖啡Crunchbase引言區、Fluid Determinism四級卡與Ticket intake圖、Governance、Mercari案例、Security與Platform controls、Go from AI to ROI、完整A-Z/分類/社群/法律頁尾。引用與數字均保留為當日公開畫面內容，不代表產品效能查核。

透過 genuine Google Stitch MCP 新增桌面校正屏幕，完整回應、精確指令、HTML與原始縮圖/fullPNG獨立保留；原DESIGN.md、design-md、先前桌面/手機稿不變。具體頁面以完整當日官方DOM/CSS與141份公開素材校正。瀏覽器資源匯出有21項CORS/response-type失敗，精確已觀察資源網址的公開HTTP下載補全，最終素材失敗0。

來源與成品各保存桌面1280×720及窄版390×844完整14段實際畫面；真實影像尺寸與無缺段覆蓋皆檢查。全部5張桌面、6張窄版比較圖已逐段目視核對；頁高9508/11137相合，44張DOM圖片載入、字型完成、無水平溢位。主標位置/尺寸為桌面x256/y190/768×112、窄版x20/y138/350×120。動畫淡入、影片/品牌條時間點及互動差異仍明列。

'''+''.join('- '+x+'\n'for x in remaining)+'\naccepted=false；沒有付費操作或部署，帳戶計費未稽核。\n'
(w/f'{b}-oct10-analysis.md').write_text(analysis)
(w/f'{b}-oct10-reproduction-prompt.md').write_text('''# Rewritten AI instruction — Zapier current public homepage

Reconstruct https://zapier.com/ as actually observed2026-10-11, preserving warm#fffefb, ink#201515, orange#ff4f00, authentic Degular Display/Inter/editorial serif,56px sticky navigation, actual hero x128/y459/1024×576, exact agentic-era copy and official original videos. Keep the entire existing section sequence, real public logo strip, features, Kelly Scheib/Crunchbase quote, Fluid Determinism initial Deterministic state, Mercari quote and dated47,000/3,000+ metrics, governance/security/finalCTA and complete directory/social/legal footer. Do not create terminal diagrams, fabricated Crunchbase metrics or security console claims.

Retain genuine fresh desktop screen and full response/prompt/rawHTML/original thumbnail/fullPNG separately, along with prior desktop/mobile/DESIGN.md/design-md. Correct concrete HTML with complete source DOM/CSS and141 observed public original assets. Verify the full9508px desktop and11137px narrow page at1280×720/390×844 using actual screenshots with true dimension/coverage/hash guards,44loaded images/fonts/no overflow. Explicitly disclose reveal animation/video/marquee phase differences and unimplemented menus/accordions/slider/carousel/footer expansion/keyboard/services/native MOBILE/other sizes/deployment. No provider verified/exact/authentic claims count as validation. accepted=false; free gallery, no paid actions or account submissions.
''')
notes='''# Genuine Google Stitch provenance and unverified provider statements

Fresh DESKTOP edit, project6052931744795035931, session13232724403068796202, screen82b48a0f12844c37aee73b203e19bdee. Full raw response zapier-oct10-native-response.json and exact prompt zapier-oct10-native-prompt.txt. Raw HTML, unchanged provider thumbnail and fullPNG retained with exact URLs/bytes/hashes in zapier-oct10-native-export-hashes.json; actual full dimensions independently checked against provider metadata.

Provider describes its design as a verified official release and claims authentic/precise/verified elements. Those statements are not validation. It invents Cursor/Claude3.7 lead-routing orchestration, Claude Desktop MCP terminal, Claude3.5Sonnet exception reasoning, Crunchbase84% faster incident response/12M+ enrichment metrics and an Enterprise Control Center with Zero-Storage Model Routing/EU PII Masking/Execution Budget Caps. None are accepted from the official homepage evidence. It also labels Zero AI Training Opt-Out and Observability Telemetry beyond the observed wording. Concrete source correction retains original official media and text, with no fabricated console/metrics.

Provider suggestions preserved: generate matching390px responsive view; toggle Fluid Determinism states; inspect Enterprise Control Center security view. No new native MOBILE is claimed, and the invented Control Center is not used as source evidence. No purchases or paid upgrades; account billing not audited.
'''
(w/f'{b}-oct10-provider-notes.md').write_text(notes)
verified=['Genuine fresh desktop Stitch correction; complete current public DOM/CSS/original assets used for the concrete source correction.','Full source UTF16 lengths/closing tags/SHA256 verified;141public assets preserved, final content failures0.','Source/corrected14desktop+14narrow actual viewport phases each cover9508/11137px; actual dimensions/contiguous coverage/hash binding checked; all11comparison segments visually reviewed.','44images loaded at both widths, fonts loaded, no horizontal overflow, exact final heights and hero title geometry.']
result=dict(brand=b,recordedAt=now,status='visually_compared_with_scoped_differences',accepted=False,reference_url='https://zapier.com/',preview='zapier.html',previewSha256=sha,sourceCorrectionCompleted=True,recordUpdates=dict(status='visually_compared_with_scoped_differences',accepted=False,reference_url='https://zapier.com/',native_screen=native['screen'],preview='zapier.html',verified=verified,remaining=remaining,review_note='已依現行agentic-era官方首頁校正並完成指定桌面/窄版完整實際畫面比較；淡入、影片與互動差異未接受官方一致。'),checks=scopes,nativeGeneration=dict(reused=False,screen=native['screen'],sessionId=native['sessionId'],fullRawResponse='zapier-oct10-native-response.json',rawHtml='zapier-oct10-stitch-desktop.html',fullNativeScreenshot='zapier-oct10-stitch-desktop.png',fullScreenshotDimensions=dims,nativeMobileCorrection=False),assets=dict(manifest='zapier-oct10-assets.json',count=141,bundleFailuresRecovered=21,publicContentFailures=0),remainingDifferences=remaining,designAnalysis='zapier-oct10-analysis.md',rewrittenPrompt='zapier-oct10-reproduction-prompt.md',providerClaimsAndSuggestions='zapier-oct10-provider-notes.md',hashManifest='zapier-oct10-file-hashes.json',noPaidActions=True,scopeNote='CSS responsive viewports with desktopUA; no account services or deployment review.',handoff='Root integrates and verifies publication; no global/progress/hosting edits by this agent.')
(w/f'{b}-oct10-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
build=json.loads((w/f'{b}-oct10-build-record.json').read_text());build['remaining']=remaining;build['actualReview']='zapier-oct10-result.json';(w/f'{b}-oct10-build-record.json').write_text(json.dumps(build,indent=2)+'\n')
paths=[p for p in w.glob(b+'*')if p.is_file()and p.name!=b+'-oct10-file-hashes.json']+[p for p in (w/(b+'-assets')).rglob('*')if p.is_file()]+[p for p in Path('scripts').glob('*'+b+'*')if p.is_file()]
(w/f'{b}-oct10-file-hashes.json').write_text(json.dumps({'recordedAt':now,'files':{str(p):{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p in paths}},indent=2)+'\n')
print(json.dumps({'brand':b,'previewSha256':sha,'accepted':False,'nativeDimensions':dims}))
