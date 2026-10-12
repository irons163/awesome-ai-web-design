from pathlib import Path
import json, hashlib, datetime
from PIL import Image

w=Path('.stitch-work/current-official'); b='resend'
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
meta=json.loads((w/f'{b}-generated.json').read_text())
remaining=[
 'The official desktop capture had the Floor background and Light ray image requests not ready, and its WebGL cube canvas was empty. The preserved public background originals load locally. Desktop WebGL fidelity was not verified.',
 'The narrow header uses a documented raster-stability CSS correction: its child is raised above the captured backdrop and the before blur layer is removed. The source sequential screenshots show a120px blurred band while the corrected header remains readable. This is an explicit visual difference.',
 'The narrow cube and four product videos, testimonial marquee offsets, status pulse and dynamic demo IDs/timestamps are frozen or show different frames. React code-pane internal scroll differs in one desktop comparison. Animation/frame/state parity is not claimed.',
 'Navigation dropdown/hamburger, SDK/framework switching, copy controls, Test-mode and editor demos, React file/view/theme tabs, tooltips and dashboard tabs remain captured initial states. Their complete behavior and keyboard focus were not accepted.',
 'Authentication, email sending, newsletter/account services, real phone hardware, other viewport widths and final published deployment are outside this review. Inputs are read-only and public service links lead to official pages.'
]
scopes=[]
for mode,width,height in [('desktop',1280,720),('narrow',390,844)]:
 r=json.loads((w/f'{b}-oct10-official-{width}-reference.json').read_text())
 p=json.loads((w/f'{b}-oct10-corrected-final-{mode}.json').read_text())
 op=json.loads((w/f'{b}-oct10-official-{width}-phases.json').read_text())
 cp=json.loads((w/f'{b}-oct10-corrected-final-{width}-phases.json').read_text())
 html=''.join(r['htmlParts'])
 assert len(html.encode('utf-16-le'))//2==r['html_length'] and hashlib.sha256(html.encode()).hexdigest()==r['html_sha256'] and html.endswith('</html>')
 assert p['height']==op[-1]['bodyHeight'] and all(i['loaded']for i in p['images']) and p['scrollWidth']==width
 for phases in [op,cp]:
  ys=[x['scrollY']for x in phases]
  assert ys[0]==0 and all(y<=x+height for x,y in zip(ys,ys[1:])) and ys[-1]+height==phases[-1]['bodyHeight']
  assert all(Image.open(w/x['screenshot']).size==(width,height) for x in phases)
 scopes.append(dict(scope=mode,viewport=p['viewport'],sourceURL=r['url'],previewURL=p['url'],sourceObservedAt=op[0]['observed_at'],previewObservedAt=p['observedAt'],sourceHeight=op[-1]['bodyHeight'],previewHeight=p['height'],heightDifference=0,noHorizontalOverflow=True,fontStatus=p['fontStatus'],allDomImages=len(p['images']),imagesNotReady=0,sourcePhases=len(op),previewPhases=len(cp),completeSequentialViewportCoverage=True,screenshotMethod='Raw CDP PNG viewport phases, verified exact image dimensions and scroll coverage; full PNGs are separate frozen frames.',officialSequentialComposite=f'{b}-oct10-official-{mode}-phase-composite.png',previewSequentialComposite=f'{b}-oct10-corrected-final-{mode}-phase-composite.png',previewScreenshot=f'{b}-oct10-corrected-final-{mode}.png',comparisonSegments=[x.name for x in sorted(w.glob(f'{b}-oct10-compare-{mode}-*.png'))],sourceCompleteness=dict(utf16Units=r['html_length'],sha256=r['html_sha256'],complete=True)))

(w/f'{b}-oct10-analysis.md').write_text('''# Resend 目前公開首頁設計分析

官方來源：https://resend.com/，來源觀察2026-10-10；最後校正畫面2026-10-11（台灣時間）。黑色背景搭配 Domaine 襯線主標與 Favorit 內文，保留 Email for developers、Forward 活動提示、十二個實際客戶商標、十三種語言及九個 Node 框架導覽。開發者體驗、公開編輯器初始白色區域、Contact management、Broadcast analytics、React 程式碼與 ACME 預覽、九張送達功能卡、實際客戶證言、控制台示例與完整頁尾均取自完整官方渲染 DOM/CSS。

與先前保存官方設計相比，主要內容及結構相同，因此重用9月27日 genuine Google Stitch MCP 原生生成；今天的 get_screen 完整回應另存。原候選含有重新詮釋及技術/客戶聲明風險，沒有直接視為通過。原始 HTML、PNG、生成 metadata、分析及 DESIGN.md/design-md 保留。校正版使用63份已觀察的公開原素材，包括五段影片、海報、商標、字型與實際分析圖。

實際1280×720桌面與390×844窄版各17段捲動截圖。PIL確認每段真實像素尺寸及從頂到頁尾無缺口；頁高各12154與14143px，與官方相同。73張本機DOM圖片皆載入，字型載入完成，無水平溢位。逐段檢視七張桌面、八張窄版2000px比較圖。主內容、字體、卡片、程式碼及頁尾位置相合，動態及互動差異如下。

## 尚存差異

'''+''.join('- '+x+'\n'for x in remaining)+'\naccepted=false；沒有宣稱全面官方一致。沒有購買、付費升級或部署；帳戶計費未稽核。\n')
(w/f'{b}-oct10-reproduction-prompt.md').write_text('''# Rewritten AI instruction — Resend current public homepage

Reconstruct https://resend.com/ as independently observed2026-10-10. Retain the genuine Google Stitch MCP original screen, rawHTML/PNG, metadata, DESIGN.md/design-md and prior analysis independently. Main structure is unchanged, so the9月27日 generation may be reused; do not label the get_screen retrieval a new generation.

Use complete verified resend-oct10-official-1280-reference.json and390-reference.json and63 exact public originals in resend-oct10-assets.json. Preserve the current Forward banner, Domaine/Favorit fonts, real12customer logos,13language/9framework navigation, exact sample code, editor initial state, contact and analytics images, React template, nine deliverability cards, real testimony, dashboard and full footer. Do not invent customers, technical claims or code. A product file named analytics is not a tracking endpoint.

Compare actual rendered pages at1280×720 and390×844 CSS pixels,DPR1,unchanged desktopUA. Verify all73DOMimages/fonts, page heights, no overflow and full sequential screenshot coverage. Keep source-unloaded Floor/Light images and empty desktop WebGL explicit. Preserve current public video assets while declaring frame timing differences. Document the narrow header raster correction and React code-pane scroll difference. Navigation/demo controls are captured initial states until separately implemented and verified. Never send email or submit account/newsletter forms. accepted=false while these differences remain.
''')
(w/f'{b}-oct10-provider-notes.md').write_text('''# Google Stitch provenance and limits

The existing genuine Google Stitch MCP screen projects/550486715627478887/screens/0b3ec1d40d22446faacec58909b1b8ab is reused because the current main content/structure agrees with the preserved prior official source. Its title is Resend — Email for developers (2026-09-27),2560×14304 DESKTOP,session9758531443187345982. Complete current get_screen response is resend-oct10-reused-screen.json. Raw resend-stitch.html/png and original metadata remain intact.

Original metadata warns that the raw candidate invented or reinterpreted customers, testimonials, statistics and technical claims. These provider claims are not validation. The full original9月27日 generation text/suggestions was not found in this current-official archive; do not claim it was newly preserved. The earlier .stitch-work/resend-generated.json belongs to a different project and is not substituted.

Current rendered public source correction and independently captured screenshots establish only the stated scope. No purchases or paid upgrades were performed; account billing was not audited.
''')
sha=hashlib.sha256((w/f'{b}.html').read_bytes()).hexdigest()
verified=['Concrete complete current official DOM/CSS/public-asset source correction after preserved genuine Stitch generation.','Both current reference DOMs verified by chunk integrity, JavaScript UTF16 length and SHA256.','17actual desktop and17actual narrow phases on each source/preview, true1280×720/390×844 dimensions and complete scroll coverage.','All15comparison segments visually inspected; desktop12154px/narrow14143px heights match,73localDOMimages load, fonts loaded,no overflow.']
result=dict(brand=b,recordedAt=now,status='visually_compared_with_scoped_differences',accepted=False,reference_url='https://resend.com/',preview='resend.html',sourceCorrectionCompleted=True,previewSha256=sha,recordUpdates=dict(status='visually_compared_with_scoped_differences',accepted=False,reference_url='https://resend.com/',observed_at=scopes[0]['sourceObservedAt'],native_screen=meta['screen'],preview='resend.html',verified=verified,remaining=remaining,review_note='目前官方完整首頁已校正並完成指定桌面/窄版逐段實際畫面比較；WebGL、header backdrop、動畫與互動保留明確差異，尚未接受為全面官方一致。'),checks=scopes,nativeGeneration=dict(reused=True,screen=meta['screen'],originalMetadata='resend-generated.json',currentGetScreen='resend-oct10-reused-screen.json',fullOriginalGenerationResponseAvailable=False,reason='Current main structure/copy/assets agree with preserved prior official source.'),assets=dict(manifest='resend-oct10-assets.json',count=63,failures=[]),remainingDifferences=remaining,designAnalysis='resend-oct10-analysis.md',rewrittenPrompt='resend-oct10-reproduction-prompt.md',providerClaimsAndSuggestions='resend-oct10-provider-notes.md',hashManifest='resend-oct10-file-hashes.json',noPaidActions=True,scopeNote='CSS responsive browser viewports; not real mobile hardware or comprehensive official parity.',handoff='Root integrates and verifies published deployment; no progress/global/hosting edits by this agent.')
(w/f'{b}-oct10-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
paths=[p for p in w.glob(b+'*')if p.is_file()and p.name!=b+'-oct10-file-hashes.json']+[p for p in (w/(b+'-assets')).rglob('*')if p.is_file()]+[p for p in Path('scripts').glob('*'+b+'*')if p.is_file()]
(w/f'{b}-oct10-file-hashes.json').write_text(json.dumps({'recordedAt':now,'files':{str(p):{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p in paths}},indent=2)+'\n')
print(json.dumps({'brand':b,'previewSha256':sha,'accepted':False,'heights':[x['previewHeight']for x in scopes]}))
