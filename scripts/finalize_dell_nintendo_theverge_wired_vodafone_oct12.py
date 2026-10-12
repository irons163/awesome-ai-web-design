"""Finalize source-only research after every whole-viewport sheet was actually reviewed."""
import hashlib,json,sys
from datetime import datetime,timezone
from pathlib import Path
work=Path('/Users/pchang01/Documents/mygithub/awesome-ai-web-design/.stitch-work/current-official')
brand=sys.argv[1];notes=json.loads(Path(sys.argv[2]).read_text())
assert brand in {'dell-1996','nintendo-2001','theverge','wired','vodafone'}
sha=lambda b:hashlib.sha256(b).hexdigest()
reviewpath=work/f'{brand}-oct12-source-review.json';review=json.loads(reviewpath.read_text())
assert len(review['coverage'])==2 and all(c['gapless'] and c['nativeDimensionsAllCorrect'] for c in review['coverage'])
assert notes['allReviewSheetsOpened'] and len(notes['reviewedSheets'])==len(review['reviewSheets'])
assert set(notes['reviewedSheets'])=={s['file'] for s in review['reviewSheets']}
review['visualReviewComplete']=True;review['reviewedAt']=datetime.now(timezone.utc).isoformat();review['visualNotes']=notes['visualNotes'];review['limitations']=notes['limitations']
reviewpath.write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
refs=[]
for width in (1280,390):
 path=work/f'{brand}-oct10-official-{width}-reference.json';r=json.loads(path.read_text());html=''.join(r['htmlParts']);assert sha(html.encode())==r['html_sha256'] and html.endswith('</html>') and '</body>' in html
 refs.append({'file':path.name,'sha256':sha(path.read_bytes()),'observedAt':r['observed_at'],'url':r['url'],'viewport':r['viewport'],'bodyHeight':r['bodyHeight'],'htmlSha256':r['html_sha256'],'htmlLengthUTF16':r['html_length'],'cssomSheets':len(r['cssom']),'accessibleCSSOMSheets':sum('cssParts' in s for s in r['cssom']),'cssomFailures':[{'href':s['href'],'error':s['error']} for s in r['cssom'] if 'error' in s]})
manifest=work/f'{brand}-oct10-assets.json';assets=json.loads(manifest.read_text());preview=work/f'{brand}.html'
result={'observedAt':datetime.now(timezone.utc).isoformat(),'brand':brand,'scope':'Current anonymous public official homepage source/assets research only. Existing preview was not changed, no new Stitch generation or clone QA was performed in this bounded task.','sourceObservationDates':[r['observedAt'] for r in refs],'filenameConvention':'oct10 canonical compatibility filenames contain the explicit new observedAt dates; they are not claims of an October 10 capture.','sourceCompleteDesktopNarrow':True,'sourceVisualReviewComplete':True,'accepted':False,'officialFidelityClaimed':False,'sourceReferences':refs,'nativeCoverage':review['coverage'],'sourceVisualReviewFile':reviewpath.name,'sourceVisualReviewSha256':sha(reviewpath.read_bytes()),'visualNotes':notes['visualNotes'],'limitations':notes['limitations'],'assets':{'manifest':manifest.name,'manifestSha256':sha(manifest.read_bytes()),'originalPreservedCount':len(assets['assets']),'unresolvedCount':len(assets['failures']),'nativeBundles':assets['nativeBundles'],'trackingExcludedFromReusableManifest':True,'HTTPFailuresNotRetried':True},'privatePriorSourceHistory':brand+'-oct12-private-source-history/manifest.json','existingPreviewSha256Observed':sha(preview.read_bytes()) if preview.exists() else None,'previewUnmodifiedByThisTask':True,'nextOwnerActions':['Send current observed design to genuine Google Stitch MCP as needed','Correct and verify the resulting actual local desktop/narrow preview','Retain source dates and visible dynamic-state limitations in any fidelity claim']}
path=work/f'{brand}-oct12-source-result.json';path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
files=[p for p in work.glob(brand+'-oct10-official-*') if p.is_file()]+[manifest,work/f'{brand}-oct10-asset-bundle.json',reviewpath,path]+[work/s['file'] for s in review['reviewSheets']]
(work/f'{brand}-oct12-source-file-hashes.json').write_text(json.dumps({'observedAt':datetime.now(timezone.utc).isoformat(),'files':[{'file':p.name,'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(set(files))]},indent=2)+'\n')
print(json.dumps({'brand':brand,'result':path.name,'frames':len(review['nativeFrames']),'sheetsReviewed':len(review['reviewSheets']),'assets':len(assets['assets']),'limitations':notes['limitations']},ensure_ascii=False))
