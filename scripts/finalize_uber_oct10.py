from pathlib import Path
import json,hashlib,datetime
from PIL import Image
w=Path('.stitch-work/current-official');b='uber';now=datetime.datetime.now(datetime.timezone.utc).isoformat()
sha=hashlib.sha256((w/f'{b}.html').read_bytes()).hexdigest()
assert json.loads((w/f'{b}-oct10-native-coverage.json').read_text())['previewSha256']==sha
native=json.loads((w/f'{b}-oct10-native-export-hashes.json').read_text());dims=list(Image.open(w/f'{b}-oct10-stitch-desktop.png').size);assert dims==native['declaredDimensions']
manifest=json.loads((w/f'{b}-oct10-assets.json').read_text());assert len(manifest['assets'])==154 and not manifest['failures']
scopes=[]
for mode,width,height,total,count,images in [('desktop',1280,720,7540,11,66),('narrow',390,844,7860,10,78)]:
 r=json.loads((w/f'{b}-oct10-official-{width}-reference.json').read_text());html=''.join(r['htmlParts']);a=json.loads((w/f'{b}-oct10-corrected-{mode}.json').read_text())
 assert len(html.encode('utf-16-le'))//2==r['html_length'] and hashlib.sha256(html.encode()).hexdigest()==r['html_sha256'] and html.endswith('</html>')
 source=json.loads((w/f'{b}-oct10-official-{width}-phases.json').read_text());phases=json.loads((w/f'{b}-oct10-corrected-{width}-phases.json').read_text())
 assert len(source)==len(phases)==count and all(p['draft_sha256']==sha and p['bodyHeight']==total for p in phases)
 assert a['height']==total and a['scrollWidth']==width and a['fontStatus']=='loaded' and len(a['images'])==images and all(i['loaded']for i in a['images'])
 headings=[h for h in a['headings']if h['level']in ['H1','H2','H3']];assert len(headings)==len(source[-1]['headings'])==52
 assert all(x['text']==y['text']and x['box']==y['bounds']for x,y in zip(source[-1]['headings'],headings))
 scopes.append(dict(scope=mode,viewport=a['viewport'],sourceURL=r['url'],previewURL=a['url'],previewObservedAt=a['observedAt'],sourceHeight=total,previewHeight=total,heightDifference=0,noHorizontalOverflow=True,fontStatus='loaded',allDomImages=images,imagesNotReady=0,sourcePhases=count,previewPhases=count,completeSequentialViewportCoverage=True,trueScreenshotDimensions=[width,height],comparisonSegments=[f'{b}-oct10-compare-{mode}-{i}.png'for i in range(4)],matchingHeadingBounds=52,heroTitleBounds=headings[0]['bounds'],sourceCompleteness=dict(utf16Units=r['html_length'],sha256=r['html_sha256'],complete=True)))
remaining=[
 'The Canadian-English URL automatically rendered Taipei, CA / Taipei and Uber Formosa public footer content. Only this observed regional variant is reviewed; no location permission or geographic variant change was performed.',
 'City Hub video and animated Journey-line frame timing differs; original media is retained. Sticky header/bottom CTA repeat in sequential composites and can obscure a strip of content; these composites are not single full-page screenshots. Narrow top CTA visibility was corrected and rechecked, but exact transition thresholds/timing are not accepted.',
 'The captured initial galleries are retained (desktop ride steps1/2; narrow ride steps1/5 and other galleries1/3). Gallery paging, menus/mobile drawer, language/city/pickup date controls, autocomplete/location permission, full keyboard/focus, ride requests/reservations, authentication, earning and membership/service flows are not implemented or accepted. Route inputs are readonly in the static source correction; action links lead to observed official services. No account/location/form submission occurred.',
 'Fresh genuine native correction is DESKTOP only. Prior original native desktop/mobile/DESIGN.md/design-md remain preserved. Other sizes, real phone hardware, other routes/locales and published deployment are not reviewed.'
]
analysis='''# Uber 目前公開首頁設計分析

來源 https://www.uber.com/ca/en/，觀察2026-10-11。加拿大英文網址在本次公開工作階段自動顯示Taipei, CA / Taipei，頁尾為Uber Formosa公開登記文字；沒有要求或授予定位權限，也不推定使用者精確位置。新版已替換10月5日舊稿的account/Reserve段落，採黑白大區塊、64px固定黑導覽、UberMove/UberMoveText字型、52px/64桌面Go anywhere與32px/40窄版主標。桌面hero左右欄各459px，保留真實旅遊拼貼、取車/下車欄與Pickup now、Schedule ahead。

完整順序為六種服務卡、How to request a ride步驟圖庫、City Hub、More ways三卡、Uber Eats大圖與餐食/寵物卡、Uber One、家庭車輛大圖、Earn圖庫、Business、雙App下載與完整公司/產品/公民/旅遊/社群/商店/法律頁尾。保留當日真實官方照片、車輛圖示、SVG、QR與影片，未沿用生成稿的虛構會員優惠或錯誤App名稱。

genuine Google Stitch MCP新增當日桌面校正屏幕，完整指令、回應、原始HTML/縮圖/fullPNG分開保留；具體頁面再以完整當日官方DOM/CSS及154份公開素材校正。pageAssets有30項匯出失敗，精確已觀察公開網址下載補齊後素材失敗0。已修正窄版頂部固定價格列的顯示，來源與成品桌面11段7540px、窄版10段7860px完整實拍；真實尺寸、連續覆蓋、hash及完整來源長度/結尾檢查通過。全部4張桌面與4張窄版比較圖已目視核對，修正後頂部再核對。桌面66張、窄版78張DOM圖片載入、字型完成、無溢位；52個H1/H2/H3文字與座標尺寸逐項相合。主標桌面x64/y160/459×64、窄版x24/y136/342×40。

'''+''.join('- '+x+'\n'for x in remaining)+'\naccepted=false；未付費、未部署，帳戶計費未稽核。\n'
(w/f'{b}-oct10-analysis.md').write_text(analysis)
(w/f'{b}-oct10-reproduction-prompt.md').write_text('''# Rewritten AI instruction — Uber current public homepage

Reconstruct https://www.uber.com/ca/en/ as actually observed2026-10-11: preserve the automatically served Taipei regional public content without inferring precise location, the complete current7540px desktop/7860px narrow black-and-white design,64px navigation, authentic UberMove/UberMoveText,52px desktop/32px narrow Go anywhere, original travel collage and exact route-action layout. Keep all current service/ride-step/City Hub/more-ways/Eats/Uber One/family-car/Earn/Business/App/footer sections, genuine public artwork, SVG icons, QR and store badges. Do not invent membership discounts, prices, availability, airport visuals, or replace actual rider/driver App names.

Retain fresh genuine DESKTOP/full response/exact prompt/rawHTML/unchanged thumbnail/fullPNG separately, and all prior MOBILE/DESIGN.md/design-md. Correct concrete HTML from complete current source DOM/CSS and154 original public assets. Verify actual1280×720 and390×844 sequential viewport coverage, screenshots' true dimensions/hash,66/78loaded images/fonts/no overflow and all52 heading bounds. Correct narrow initial lower-CTA visibility. Disclose video/GIF/transition timing, sticky-overlay strips, captured initial galleries, readonly inputs, unimplemented navigation/city/date/autocomplete/location/ride/auth/services, native MOBILE/other widths/deployment. Provider precise/authentic/verified statements do not validate fidelity. accepted=false; no payment, location permission, form or account submission.
''')
(w/f'{b}-oct10-provider-notes.md').write_text('''# Genuine Google Stitch provenance and unverified provider statements

Fresh DESKTOP project12825280253887614924/session17468190394270834350/screen72909e628199476293d5cca028db15ec. Full response/exact prompt/rawHTML/unchanged thumbnail/fullPNG preserved with precise URLs/bytes/hashes. Actual fullPNG2560×14106 independently matches provider metadata.

Provider says it aligns precisely and describes verified/authentic artwork or benefits. These are not validation. Its Uber One $0 Delivery Fee/5% off claims are absent from observed source, and its Apps Download labels Uber Rider & Courier / Uber Eats Food & Grocery replace actual Uber app / Driver app. Its route-context lower bar, location-filled pickup field, enlarged overlay copy and airport-transfer visual are not accepted as official evidence. Concrete correction follows observed source text/assets and exact52-heading geometry, not these provider embellishments. Original native files remain unmodified.

Provider suggestions retained: review mobile responsive behavior; inspect input interaction states/micro-interactions; explore localized city variants. No new native MOBILE or geographic/service parity is claimed. No purchases/upgrades; account billing not audited.
''')
verified=['Genuine fresh desktop Stitch edit and unchanged native originals retained.','Complete current rendered DOM/CSS and154public original assets corrected;30bundle failures recovered; final content failures0.','Source/corrected11desktop and10narrow actual viewport phases cover7540/7860px; true dimensions/coverage/hash verified;8comparison segments reviewed and final narrow top CTA fix checked.','66desktop/78narrow images loaded, fonts loaded, no overflow; all52H1/H2/H3 texts and bounds match each source width.']
result=dict(brand=b,recordedAt=now,status='visually_compared_with_scoped_differences',accepted=False,reference_url='https://www.uber.com/ca/en/',preview='uber.html',previewSha256=sha,sourceCorrectionCompleted=True,recordUpdates=dict(status='visually_compared_with_scoped_differences',accepted=False,reference_url='https://www.uber.com/ca/en/',native_screen=native['screen'],preview='uber.html',verified=verified,remaining=remaining,review_note='已依當日公開新版和實際Taipei變體重製，桌面/窄版全頁實拍與52主標相合；動態、圖庫與服務差異未接受官方一致。'),checks=scopes,nativeGeneration=dict(reused=False,screen=native['screen'],sessionId=native['sessionId'],fullRawResponse=f'{b}-oct10-native-response.json',rawHtml=f'{b}-oct10-stitch-desktop.html',fullNativeScreenshot=f'{b}-oct10-stitch-desktop.png',fullScreenshotDimensions=dims,nativeMobileCorrection=False),assets=dict(manifest=f'{b}-oct10-assets.json',count=154,bundleFailuresRecovered=30,publicContentFailures=0),remainingDifferences=remaining,designAnalysis=f'{b}-oct10-analysis.md',rewrittenPrompt=f'{b}-oct10-reproduction-prompt.md',providerClaimsAndSuggestions=f'{b}-oct10-provider-notes.md',hashManifest=f'{b}-oct10-file-hashes.json',noPaidActions=True,scopeNote='CSS responsive viewports with desktopUA; observed auto-served regional variant; no account/location/services/deployment review.',handoff='Root integrates and verifies publication; no global/progress/hosting edits by this agent.')
(w/f'{b}-oct10-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
build=json.loads((w/f'{b}-oct10-build-record.json').read_text());build['remaining']=remaining;build['actualReview']=f'{b}-oct10-result.json';(w/f'{b}-oct10-build-record.json').write_text(json.dumps(build,indent=2)+'\n')
paths=[p for p in w.glob(b+'*')if p.is_file()and p.name!=b+'-oct10-file-hashes.json']+[p for p in (w/(b+'-assets')).rglob('*')if p.is_file()]+[p for p in Path('scripts').glob('*'+b+'*')if p.is_file()]
(w/f'{b}-oct10-file-hashes.json').write_text(json.dumps({'recordedAt':now,'files':{str(p):{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p in paths}},indent=2)+'\n')
print(json.dumps({'brand':b,'previewSha256':sha,'accepted':False,'nativeDimensions':dims}))
