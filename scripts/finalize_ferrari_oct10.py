from pathlib import Path
from datetime import datetime, timezone
import hashlib, json
from PIL import Image

work=Path('.stitch-work/current-official')
brand='ferrari'
def read(name): return json.loads((work/name).read_text())
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def save(name,data): (work/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
sha=digest(work/'ferrari.html')
measured=read('ferrari-oct10-measured-checks.json')
assert measured['previewSha256']==sha
assets=read('ferrari-oct10-assets.json')
for a in assets['assets']: assert digest(work/a['path'])==a['sha256']
remaining=[
 'The first hero is an original public static poster. Official HLS video frames differ visibly; Play and cover controls are not implemented. Other covers are retained in source templates but their active rendered states are not accepted.',
 'Official news auto-cycles: the first desktop full capture showed story3, while the first narrow pass crossed news/reveal transitions. Separate genuine Barcelona source screenshots at both widths and a second complete narrow pass show the selected story2 used in the preview. Auto-cycle, navigation buttons and transition timing remain different.',
 'Official entrance/curtain animations are terminal static states in the preview. The first narrow official pass contains unrevealed tiles; its raw images remain preserved. Seven second-pass actual390x844 source images, separately recorded, show all six tiles after reveal. No frame-timing or animation parity is claimed.',
 'The downward desktop sequence hides its header using a simple scroll threshold. The separately selected official Barcelona desktop shot retains a visible header while the downward local shot hides it. Full up/down navigation, hover menus, Search, Subscribe, footer/social accordions, keyboard/focus and privacy/accessibility services are not implemented or accepted by the static correction.',
 'Seven unused alternate/medium/CJK font URLs returned405. The needed Body-Font was preserved from a normal browser CSS200 response and both main regular/medium FerrariSans assets are cached; every observed image is loaded at both reviewed widths. Unreviewed locales and fallback fonts are not accepted.',
 'Two fresh genuine Stitch DESKTOP edits are preserved separately. Prior native MOBILE, DESIGN.md and design-md originals are retained.390px is a CSS responsive viewport with desktop user-agent, not phone hardware. Other widths, routes, account/configurator/purchase services and deployment are not reviewed.'
]
checks=[]
for width,height,mode in [(1280,720,'desktop'),(390,844,'narrow')]:
 source=read(f'ferrari-oct10-official-{width}-phases.json')
 local=read(f'ferrari-oct10-corrected-{width}-phases.json')
 assert len(source)==len(local)==7
 assert all(q['draft_sha256']==sha for q in local)
 assert all('Charles on the podium at Marina Bay' in [h['text']for h in q['headings']] and 'A solid Saturday in Singapore' not in [h['text']for h in q['headings']]for q in local)
 assert all(i['loaded']for i in local[-1]['images'])
 for side,phases in [('official',source),('corrected',local)]:
  assert phases[0]['scrollY']==0
  assert all(b['scrollY']<=a['scrollY']+height for a,b in zip(phases,phases[1:]))
  assert phases[-1]['scrollY']+height==phases[-1]['bodyHeight']
  for q in phases: assert Image.open(work/q['screenshot']).size==(width,height)
 completeness={}
 for tag in ['reference','top-reference','news-reference']:
  r=read(f'ferrari-oct10-official-{width}-{tag}.json')
  for key,leng,hashed in [('htmlParts','html_length','html_sha256'),('shadowHTMLParts','shadowHTML_length','shadowHTML_sha256')]:
   s=''.join(r[key]);assert len(s.encode('utf-16-le'))//2==r[leng] and hashlib.sha256(s.encode()).hexdigest()==r[hashed] and s.endswith('</html>')
  completeness[tag]={'observedAt':r['observed_at'],'url':r['url'],'htmlUtf16Units':r['html_length'],'htmlSha256':r['html_sha256'],'shadowHtmlUtf16Units':r['shadowHTML_length'],'shadowHtmlSha256':r['shadowHTML_sha256'],'shadowRoots':r['shadowCount'],'adoptedStyleSheets':len(r['shadowCSS']),'complete':True}
 m=measured[mode]
 checks.append({'scope':mode,'viewport':{'width':width,'height':height,'dpr':1,'scope':'CSS responsive viewport with desktop user-agent; not real phone hardware'},'sourceURL':'https://www.ferrari.com/en-US','previewURL':'http://127.0.0.1:4173/.stitch-work/current-official/ferrari.html','previewObservedAt':[local[0]['observed_at'],local[-1]['observed_at']],'sourceHeight':source[-1]['bodyHeight'],'previewHeight':local[-1]['bodyHeight'],'heightDifference':0,'noHorizontalOverflow':m['noHorizontalOverflow'],'fontStatus':m['fontsStatus'],'allDomImages':m['imageCount'],'imagesNotReady':0,'sourcePhases':7,'previewPhases':7,'completeSequentialViewportCoverage':True,'trueScreenshotDimensions':[width,height],'captureTimePreviewSha256':sha,'actualDocumentCurrentStoryObserved':True,'matchingMainHeadingCount':8,'maxMainHeadingBoundsDifference':0,'measuredDetails':'ferrari-oct10-measured-checks.json','sourceCompleteness':completeness,'comparisonSegments':[f'ferrari-oct10-compare-{mode}-{i}.png'for i in range(3)],'sameNewsStateComparison':f'ferrari-oct10-compare-{mode}-news.png'})
supplement=read('ferrari-oct10-official-second-pass-390-phases.json')
assert len(supplement)==7 and supplement[-1]['scrollY']+844==5258
for q in supplement: assert Image.open(work/q['screenshot']).size==(390,844)
native=[]
notes=['# Ferrari native provider text and suggestions','Provider text is retained as an unvalidated generation claim. Source/native exports are unchanged. The corrected preview and actual CUA images supply the scoped evidence.']
for date in ['oct10','oct12']:
 ex=read(f'ferrari-{date}-native-export-hashes.json')
 for f in ex['files']:assert digest(work/f['file'])==f['sha256']
 dimensions=list(Image.open(work/f'ferrari-{date}-stitch-desktop.png').size)
 assert dimensions==ex['declaredDimensions']==[2560,7258]
 native.append({'reused':False,'deviceType':'DESKTOP','screen':ex['screen'],'sessionId':ex['sessionId'],'fullRawResponse':f'ferrari-{date}-native-response.json','exactPrompt':f'ferrari-{date}-stitch-edit-prompt.txt','rawHtml':f'ferrari-{date}-stitch-desktop.html','fullNativeScreenshot':f'ferrari-{date}-stitch-desktop.png','fullScreenshotDimensions':dimensions,'originalExportHashes':f'ferrari-{date}-native-export-hashes.json'})
 response=read(f'ferrari-{date}-native-response.json');response=response.get('structuredContent')or json.loads(next(c['text']for c in response['content']if c['type']=='text'))
 notes.append('\n## '+date+' session '+ex['sessionId'])
 for c in response['outputComponents']:
  if 'text'in c:notes.append('\nProvider claim, unvalidated:\n\n'+c['text'])
  if 'suggestion'in c:notes.append('\nProvider suggestion: '+c['suggestion'])
notes.append('\n## Review implication\nThe provider added an EN-US utility,01/04 index and a Magazine eyebrow above Sketch Body that were absent from the observed source. The current source correction restores actual DOM, shadow CSS, SVG marks, text and original images. Its native styling/fonts and generated imagery remain separate. Neither provider claims nor suggestions establish fidelity or tested accordion behavior. Fresh native output covers DESKTOP only.')
(work/'ferrari-oct10-provider-notes.md').write_text('\n'.join(notes)+'\n')
analysis='''# Ferrari 當日官方首頁設計分析

來源為 https://www.ferrari.com/en-US 。沿用 oct10 檔名前綴；最新來源與實際畫面觀察時間為2026-10-11T23:08Z之後，臺北時間2026-10-12。新聞第一則已更新為「Charles on the podium at Marina Bay」，舊 qualifying 報導不再留在目前稿件。新聞第二則 Barcelona 為本預覽的選定靜態狀態。

官方首頁以滿版影片、透明黑色導航與白色新聞區形成對比。Scuderia Ferrari HP 首屏佔完整視窗；三封面指示器與四則新聞輪播皆有原始資料。六張照片卡在1280px形成兩欄，在390px依序堆疊。Sketch Body 沒有 Magazine 小標。灰色 Newsletter 區接黑色五類頁尾，窄版呈閉合列；完整社群、公司法律文字、隱私連結、國別與 Shell 標記均保留。

真正的兩次 Google Stitch 桌面修改與未改動輸出已保存。首次生成含與來源不同的字型、影像、EN-US工具、01/04索引與 Sketch Body 小標，因此再以完整公開 DOM、220個開放 shadow roots、64份 adopted CSS 與實際公開素材逐項校正。保留正常CSS瀏覽器200回應的原始 Ferrari 字型；不載入追蹤與服務腳本。

目前 SHA 的稿件重新載入後，桌面1280×720與窄版390×844各有7張真正視窗截圖，連續覆蓋4337與5258px。每張核對實際檔案尺寸、網址、捲動位置、頁高與擷取時稿件雜湊。兩版19張DOM圖片全部載入，沒有橫向溢出。首屏、六卡與Newsletter共8個主要標題的文字及邊界差值皆為0。補充同一 Barcelona 新聞狀態的兩版實拍，以及官方窄版動畫完成後再走一次的7張完整實拍；所有比較圖已實際開啟檢視。

完整官方第一趟窄版截圖仍保留尚未出現的動畫卡與輪播過渡，第二趟真實截圖可見全部照片。預覽採原始公開影片海報與動畫終態，不重現HLS影格、入場/輪播時序、Play、Menu、Search、Subscribe、頁尾展開或外部服務。桌面額外新聞實拍的官方導航仍顯示，本地向下捲動狀態已收起，兩者差異亦保留。7個未使用的替代/CJK字型網址405仍記錄，不能宣稱所有取得嘗試成功。

accepted=false。此證據只支持已列範圍的版面與內容比較，不能宣稱全面官方一致、真手機測試或已發布驗證。原生MOBILE、DESIGN.md及 design-md 原件保持不變；帳戶、購買、訂閱與付費動作均未執行。
'''
(work/'ferrari-oct10-analysis.md').write_text(analysis)
prompt='''# Ferrari 重寫 AI 指令

依2026-10-12臺北時間實際觀察的 https://www.ferrari.com/en-US 重製公開首頁，先用 Google Stitch MCP 原生產生並保留完整回應與原始HTML/圖片，再依當日實際DOM與公開素材校正。保留既有DESIGN.md與原生MOBILE原件。不能以生成器文字當作驗證。

以1280×720桌面和390×844窄版CSS視窗為比較尺寸；390並非真手機。首屏保留官方馬匹SVG、五大分類/Search，窄版Menu/馬匹/Search。三封面為Scuderia Ferrari HP、START YOUR ENGINE、FW 26 RUNWAY COLLECTION；第一封面選定，若僅採原始公開poster，必須明示其與HLS影片的差異。

四則當日新聞依來源保留：Charles on the podium at Marina Bay、499Ps set for action in Barcelona、FERRARI OPENS ITS GATES TO THE NEXT GENERATION、The Making of the Ferrari Luce Tailor Made — Chassis 0。第一則使用Singapore Grand Prix race-report公開連結與當日原圖/全文摘要；第二則維持Barcelona原始FIA WEC文字、原圖和公開連結為可見狀態。不增加來源沒有的01/04文字索引。

以原始公開照片依序排列六卡：Collections/FERRARI HYPERSAIL REPLICA COLLECTION、Ferrari Museums/Greatest Hits、Magazine/A Natural Beauty、Sketch Body（無Magazine小標）、Magazine/A 50-year love affair、Sports Cars/PAST MODELS。兩欄桌面、單欄窄版，保留照片焦點、字體、留白、Discover圓箭頭。

保留Newsletter、Stay up to date原文、紅色Subscribe、完整五類頁尾及所有實際法律/社群/國別/Shell內容。使用當日公開Ferrari字型與SVG；保存完整open-shadowDOM/adoptedCSS與素材雜湊。移除服務/追蹤腳本後，互動若未實作或未實測，直接列為未接受。

重新載入最終稿，先讀取當日新聞文字確認不是舊頁。逐段捲動實拍兩版整頁；核對實際圖片尺寸、載入、網址、scrollY、頁高、截圖時稿件SHA。輪播與入場動畫須保存實際狀態，另補同選定新聞及已出現的照片狀態。每張比較圖實際檢視，列出影片影格、導航/輪播/動畫與服務差異。未完成完整官方一致驗收前維持accepted=false，不使用付費服務或代辦帳戶/交易。
'''
(work/'ferrari-oct10-reproduction-prompt.md').write_text(prompt)
result={'brand':brand,'recordedAt':datetime.now(timezone.utc).isoformat(),'status':'visually_compared_with_scoped_differences','accepted':False,'reference_url':'https://www.ferrari.com/en-US','preview':'ferrari.html','previewSha256':sha,'sourceCorrectionCompleted':True,'recordUpdates':{'status':'visually_compared_with_scoped_differences','accepted':False,'reference_url':'https://www.ferrari.com/en-US','native_screen':native[-1]['screen'],'preview':'ferrari.html','verified':['Two genuine desktop Stitch edits retained, including latest Charles race report update.','Current public DOM/open shadow roots/adopted CSS and original public assets corrected.','Final reloaded current-news document:7 desktop and7 narrow true-dimension phases, complete range and capture-time SHA;8 main headings match exactly;19 images loaded at both widths.','First official narrow reveal/auto-cycle states preserved;7 second-pass actual narrow phases and both same-news-state comparisons separately inspected.'],'remaining':remaining,'review_note':'已同步Charles最新賽後新聞，完成目前SHA桌面/窄版整頁實拍及八主要標題比較；靜態海報、影片、輪播、導航與互動差異仍未接受官方一致。'},'checks':checks,'officialNarrowSecondPass':{'phases':7,'trueScreenshotDimensions':[390,844],'completeSequentialViewportCoverage':True,'sourcePhasesFile':'ferrari-oct10-official-second-pass-390-phases.json','comparisonSegments':[f'ferrari-oct10-compare-narrow-second-pass-{i}.png'for i in range(3)],'scope':'Additional source-only actual screenshots after initially unrevealed tiles; no replacement or concealment of first-pass source states.'},'nativeGeneration':native[-1],'nativeGenerationHistory':native,'assets':{'manifest':'ferrari-oct10-assets.json','count':len(assets['assets']),'bytes':sum(a['bytes']for a in assets['assets']),'remainingAcquisitionFailures':len(assets['failures']),'failureScope':assets['failureScope'],'browserFontResponse':'ferrari-oct10-browser-font-response.json','deploymentClosureNote':'Includes unused originalHLS/SDK assets for provenance; root should package only referenced files and retain raw evidence locally.'},'remainingDifferences':remaining,'designAnalysis':'ferrari-oct10-analysis.md','rewrittenPrompt':'ferrari-oct10-reproduction-prompt.md','providerClaimsAndSuggestions':'ferrari-oct10-provider-notes.md','hashManifest':'ferrari-oct10-file-hashes.json','noPaidActions':True,'scopeNote':'Dated public en-US homepage, CSS desktopUA viewports, selected first cover/static Barcelona news; no complete motion/UI/services/deployment parity.','handoff':'Root owns global integration and publication. No progress/global/hosting changes by this agent.'}
save('ferrari-oct10-result.json',result)
build=read('ferrari-oct10-build-record.json');build['remaining']=remaining;build['actualReview']={'result':'ferrari-oct10-result.json','previewSha256':sha,'reloadedDocumentCurrentStoryObserved':True,'desktopPhases':7,'narrowPhases':7,'sourceSecondPassNarrowPhases':7,'accepted':False};save('ferrari-oct10-build-record.json',build)
paths=sorted(p for p in work.glob('ferrari*')if p.is_file()and p.name!='ferrari-oct10-file-hashes.json')+sorted(p for p in (work/'ferrari-assets').rglob('*')if p.is_file())+sorted(p for p in Path('scripts').glob('*ferrari*')if p.is_file())
save('ferrari-oct10-file-hashes.json',{'recordedAt':datetime.now(timezone.utc).isoformat(),'previewSha256':sha,'files':[{'file':str(p),'bytes':p.stat().st_size,'sha256':digest(p)}for p in paths]})
print(json.dumps({'previewSha256':sha,'accepted':False,'phases':[7,7],'additionalOfficialNarrowPhases':7,'assets':len(assets['assets']),'remainingFontFailures':len(assets['failures']),'hashedFiles':len(paths)}))
