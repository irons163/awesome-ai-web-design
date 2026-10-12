from pathlib import Path
import json,hashlib,datetime
w=Path('.stitch-work/current-official');b='supabase';now=datetime.datetime.now(datetime.timezone.utc).isoformat();meta=json.loads((w/f'{b}-generated.json').read_text());native=json.loads((w/f'{b}-oct10-reused-screen.json').read_text())
remaining=[
'Actual official/local dashboard videos show different frames and the community column carousel is captured at different offsets. Layout and copy were compared; animation phase/timing parity is not claimed.',
'Navigation dropdowns, narrow hamburger, dashboard/framework tab changes, customer-story expansion, theme/privacy controls and keyboard focus behavior remain captured initial UI states; they are not fully wired or accepted as official behavior.',
'The current official captures had some community avatar requests not ready. Preserved public originals load locally; this is an explicit screenshot difference, not claimed pixel equality.',
'The page is a dated public homepage study. Newsletter input is read-only and forms link out; dashboard, authentication, database/account services, real devices, other widths and final published deployment are outside verified scope.'
]
scopes=[]
for mode,v in [('desktop',1280),('narrow',390)]:
 o=json.loads((w/f'{b}-oct10-official-{mode}.json').read_text());p=json.loads((w/f'{b}-oct10-corrected-{mode}.json').read_text());ph=json.loads((w/f'{b}-oct10-corrected-{v}-phases.json').read_text());r=json.loads((w/f'{b}-oct10-official-{v}-reference.json').read_text());assert p['height']==o['height'];assert not any(not i['loaded'] for i in p['images']);assert r['html_sha256']==hashlib.sha256(''.join(r['htmlParts']).encode()).hexdigest()
 scopes.append(dict(scope=mode,viewport=p['viewport'],sourceURL=o['url'],previewURL=p['url'],sourceObservedAt=o['observedAt'],previewObservedAt=p['observedAt'],sourceHeight=o['height'],previewHeight=p['height'],heightDifference=0,noHorizontalOverflow=p['scrollWidth']==v,fontStatus=p['fontStatus'],allDomImages=len(p['images']),imagesNotReady=0,officialScreenshot=f'{b}-oct10-official-{mode}.png',previewScreenshot=f'{b}-oct10-corrected-{mode}.png',localTraversalPhases=len(ph),comparisonSegments=[x.name for x in sorted(w.glob(f'{b}-oct10-compare-{mode}-*.png'))],sourceCompleteness=dict(characters=r['html_length'],sha256=r['html_sha256'],complete=''.join(r['htmlParts']).endswith('</html>'))))
analysis='''# Supabase目前公開首頁設計分析 — 2026-10-10

官方來源：https://supabase.com/ 。深灰背景、綠色重點、細邊框卡片與實際Postgres線框插畫，保留目前「Build in a weekend / Scale to millions」標題與完整產品網格。十二個客戶商標、實際Table Editor影片、React程式碼、六張範本、五家客戶展開卡、社群原始內容、111.2K GitHub圖像、完整六欄頁尾及安全標章均以今天官方的完整渲染DOM/CSS與原始公開素材校正。

主要版型與先前保存官方參考相同，因此重用9月27日 genuine Google Stitch MCP原生生成，10月10日透過get_screen重新確認並保存完整回應。原始HTML、PNG、生成紀錄、DESIGN.md/design-md及原分析均保留；沒有把原生候選當成驗證結果。

實際1280×720桌面與390×844窄版逐段捲動並截圖，完整頁面高度各7691、9819px，均與官方相同。最後在指定尺寸重新載入以排除固定導覽繪製殘留，58張DOM圖片皆載入、字型載入完成、無水平溢位。逐一檢視4張桌面及5張窄版2000px比較段；主要文字、格線、商標、範本、客戶卡與頁尾布局相合。影片與社群輪播相位不同、部分官方頭像未載入；這是實測範圍，不能推論全面官方一致。

## 尚有差異

'''+''.join('- '+x+'\n' for x in remaining)+'\naccepted=false。未採購、付費升級或部署。\n'
(w/f'{b}-oct10-analysis.md').write_text(analysis)
(w/f'{b}-oct10-reproduction-prompt.md').write_text('''# Rewritten AI instruction — Supabase current public homepage

Reconstruct https://supabase.com/ as observed2026-10-10, keeping the preserved genuine Google Stitch MCP original independently. Use complete supabase-oct10-official-1280-reference.json and390-reference.json, verified chunk/hash integrity, the exact captured responsive layouts and supabase-oct10-assets.json public originals. Retain original analysis and DESIGN.md/design-md exports.

Preserve the current dark/green typography, seven-product card grid with original SVG product art, twelve real customer logos, actual dashboard video, exact React code and six template cards, Lovable/eXp/Phoenix/Chatbase/Rally stories, community copy/avatars,111.2K GitHub display, security badges and full footer. Never fabricate database rows, claims, customer names, code or testimonials. Set literal loading="eager" on local image elements to make full-page evidence reliable; do not alter official references.

Render and compare all sections at1280×720 and390×844 CSS pixels,DPR1,unchanged desktopUA. Use fresh reload after setting each width to settle fixed header paint, verify fonts/images and no overflow, save actual screenshots and hashes. Keep animation phase, captured-only interactive controls, account services and actual-device limits explicit. No account forms or payments. accepted=false until all required evidence exists.
''')
(w/f'{b}-oct10-provider-notes.md').write_text('''# Existing genuine Stitch output reused

Current design structure was compared with the saved prior official source and remains the same. The original9月27日 generation is reused, not represented as a new10月10日 generation. The complete10月10日 get_screen response is in supabase-oct10-reused-screen.json; rawHTML/PNG and original generated metadata remain unchanged.

The full9月27日 generation response text/suggestions was not found in this current-official archive; do not claim it was newly preserved. The earlier .stitch-work/supabase-generated.json belongs to another project and must not be substituted. Provider screen title, dimensions and visual assertions are provenance only. Today’s independent browser references and actual local captures establish only the stated scope. No payment or paid upgrade performed; account billing was not audited.
''')
verified=['Current complete official DOM/CSS/public assets preserved with chunk lengths and SHA-256 checks at1280 and390 CSS pixels.','Genuine existing Google Stitch MCP screen reused because current observed design structure is unchanged; complete10月10日 get_screen response and original exports preserved.','Concrete complete current homepage corrected after Stitch; previous draft archived, original source/design exports retained.','Actual full desktop7691px and narrow9819px source/local pages and all nine2000px comparison segments visually checked; heights match,58localDOMimages loaded, fonts loaded,no overflow.']
result=dict(brand=b,recordedAt=now,status='visually_compared_with_scoped_differences',accepted=False,reference_url='https://supabase.com/',preview=b+'.html',recordUpdates=dict(status='visually_compared_with_scoped_differences',accepted=False,reference_url='https://supabase.com/',observed_at=scopes[0]['sourceObservedAt'],native_screen=meta['screen'],preview=b+'.html',verified=verified,remaining=remaining,review_note='10月10日目前完整官方首頁已具體校正並在指定桌面與窄版逐段比較；影片、輪播與互動仍有明確差異，尚未接受為全面官方一致。'),checks=scopes,sourceCorrectionCompleted=True,nativeGeneration=dict(reused=True,screen=meta['screen'],originalMetadata=b+'-generated.json',currentGetScreen=b+'-oct10-reused-screen.json',reason='Current main structure/copy/assets compared with saved prior official source; no major design change observed.'),providerRawUnchanged=True,remainingDifferences=remaining,rewrittenPrompt=b+'-oct10-reproduction-prompt.md',designAnalysis=b+'-oct10-analysis.md',providerClaimsAndSuggestions=b+'-oct10-provider-notes.md',hashManifest=b+'-oct10-file-hashes.json',previewSha256=hashlib.sha256((w/f'{b}.html').read_bytes()).hexdigest(),noPaidActions=True,scopeNote='CSS responsive desktop/narrow browser viewports, not real mobile hardware. Main page layout and content scoped evidence; no comprehensive official-match claim.',handoff='Root integrates source and verifies final deployment; no progress/global/hosting edits by this agent.')
(w/f'{b}-oct10-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
paths=[p for p in w.glob(b+'*') if p.is_file() and p.name!=b+'-oct10-file-hashes.json']+[p for p in (w/(b+'-assets')).rglob('*') if p.is_file()]+[p for p in Path('scripts').glob('*'+b+'*') if p.is_file()]
(w/f'{b}-oct10-file-hashes.json').write_text(json.dumps({'recordedAt':now,'files':{str(p):{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p in paths}},indent=2)+'\n');print(json.dumps(dict(brand=b,previewSha256=result['previewSha256'],accepted=False,heights=[x['previewHeight']for x in scopes])))
