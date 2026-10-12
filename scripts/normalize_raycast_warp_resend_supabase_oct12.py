"""Make historical evidence binding explicit; never add capture hashes to old phases."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json
from PIL import Image

w=Path('.stitch-work/current-official')
now=datetime.now(timezone.utc).isoformat()
def read(name):return json.loads((w/name).read_text())
def sha(data):return hashlib.sha256(data).hexdigest()
def digest(path):return sha(path.read_bytes())
def save(name,data):(w/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def preserve(name,backup):
 target=w/backup
 if not target.exists():target.write_bytes((w/name).read_bytes())
 return json.loads(target.read_text())

for brand in ['raycast','warp','resend','supabase']:
 result_name=f'{brand}-oct10-result.json'
 original=preserve(result_name,f'{brand}-oct12-result-before-lineage.json')
 original_manifest=preserve(f'{brand}-oct10-file-hashes.json',f'{brand}-oct12-file-hashes-before-lineage.json')
 original_build=preserve(f'{brand}-oct10-build-record.json',f'{brand}-oct12-build-record-before-lineage.json')
 current=(w/(brand+'.html')).read_bytes();current_sha=sha(current)
 assert current_sha==original['previewSha256']
 evidence={'brand':brand,'recordedAt':now,'currentPreviewSha256':current_sha,'currentFullPageRecaptured':False,'oldPhaseJsonMutated':False,'captureHashesBackfilled':False,'kind':'historical observations with separately identified final changes or posthoc hashes','historicalResult':f'{brand}-oct12-result-before-lineage.json','historicalManifest':f'{brand}-oct12-file-hashes-before-lineage.json','historicalBuildRecord':f'{brand}-oct12-build-record-before-lineage.json','scopes':[]}
 result=json.loads(json.dumps(original))
 result['currentFullPageCaptureComplete']=False
 result['currentFullPageComparisonComplete']=False
 result['historicalFullPageComparisonComplete']=True
 result['evidenceLineage']=f'{brand}-oct12-evidence-lineage.json'
 result['evidenceLineageNormalizedAt']=now
 result['accepted']=False
 result['recordUpdates']['accepted']=False
 build=json.loads(json.dumps(original_build))
 if brand=='raycast':
  prior='4bf651b1081991e24c357074fb8979b0e1ec8712c3533434c25dab29e5e50bef'
  before=(w/'raycast-oct10-before-footer-label-fix.html').read_bytes()
  old=rb'\u003cinput type=\"submit\" class=\"Submit-module__Fa7Cva__submit\" value=\"\" readonly=\"\">'
  new=rb'\u003cinput type=\"submit\" class=\"Submit-module__Fa7Cva__submit\" value=\"Subscribe\">'
  assert sha(before)==prior and before.count(old)==current.count(new)==2 and before.replace(old,new)==current
  normalized=current.replace(new,old);assert sha(normalized)==prior
  evidence['normalization']={'kind':'exact two responsive submit-input substitutions','priorFullPageSha256':prior,'currentSha256':current_sha,'normalizedCurrentSha256':sha(normalized),'replacementCount':2,'forwardByteEquality':True,'reverseByteEquality':normalized==before,'unchangedScope':'Every byte outside exactly two submit-input tags is identical, including styles, runtime, assets and all other responsive template content.','changedScope':'Two footer submit labels restored to Subscribe; readonly removed from submit controls.','proof':'raycast-oct10-footer-label-diff-proof.json'}
  phase_files=['raycast-oct10-corrected-final-desktop-native-1280-phases.json','raycast-oct10-corrected-final-390-phases.json']
  note='完整整頁比較屬4bf651…歷史稿；目前2564ae…僅兩個Subscribe輸入標籤不同，已做精確雙向位元組證明及目前SHA頁尾補驗，未宣稱目前稿整頁逐段重拍。'
  extra='Full current-SHA D/N page recapture was not performed. Historical full-page screenshots bind to4bf651…; exact two-input normalization proves the remaining bytes unchanged. Final footer-only screenshots bind to2564ae… and verify the changed Subscribe labels.'
 elif brand=='warp':
  prior='8a483c0d26c5635cd6583266148306604a97316d5c3b64638801e6d0e284b5b4'
  new=rb'class=\"roi-chart no-frame\"';old=rb'class=\"roi-chart\"'
  assert current.count(new)==2
  normalized=current.replace(new,old);assert sha(normalized)==prior
  evidence['normalization']={'kind':'exact inverse two responsive chart-class substitutions','priorFullPageSha256':prior,'currentSha256':current_sha,'normalizedCurrentSha256':sha(normalized),'replacementCount':2,'normalizationByteHashVerified':True,'unchangedScope':'Every byte outside the two exact roi-chart class attributes is identical to the historical capture SHA, including styles, runtime, assets and remaining template content.','changedScope':'no-frame class added to two static ROI chart images.','proof':'warp-oct10-chart-frame-diff-proof.json'}
  phase_files=['warp-oct10-corrected-final-native-1280-phases.json','warp-oct10-corrected-final-native-390-phases.json']
  note='完整整頁比較屬8a483c…歷史稿；目前65894e…只有兩個圖表class不同，逆替換已精確還原舊SHA；圖表局部補驗另列，補圖無原始capture-time HTML SHA，未宣稱目前稿整頁重拍。'
  extra='Full current-SHA D/N page recapture was not performed. Historical full-page screenshots bind to8a483c…; exact two-class normalization proves unchanged bytes elsewhere. Final chart-only screenshots were associated with65894e… in the subsequent result/diff proof; their original metadata does not record capture-time HTML SHA.'
 else:
  prior=None
  phase_files=[f'{brand}-oct10-corrected'+('-final'if brand=='resend'else'')+f'-{width}-phases.json'for width in [1280,390]]
  entries=original_manifest['files']
  entry=entries[str(w/(brand+'.html'))] if isinstance(entries,dict)else next(x for x in entries if x['file'].endswith('/'+brand+'.html'))
  assert entry['sha256']==current_sha
  evidence['posthocFileLineage']={'recordedAt':original_manifest['recordedAt'],'manifest':f'{brand}-oct12-file-hashes-before-lineage.json','manifestEntrySha256':entry['sha256'],'currentFileMatchesPosthocManifest':True,'buildRecordHtmlSha256':original_build['html']['sha256'],'buildRecordMatchesCurrentFile':original_build['html']['sha256']==current_sha,'meaning':'A posthoc result/manifest file digest establishes the file present when that record was finalized. It does not establish an omitted capture-time SHA for any earlier phase.'}
  if brand=='resend':
   note='10月10日完整桌面/窄版畫面比較保留為歷史證據；D僅第6–16張原始記錄含目前SHA，前6張與N17張缺capture-time SHA。事後manifest相合不等於當時整頁逐張版本綁定，尚未補完整目前SHA重拍。'
   extra='Historical desktop/narrow observations and comparisons remain valid dated observations. Only desktop phase indices6–16 originally contain capture-time SHA; desktop0–5 and all narrow phases do not. The later manifest/current file match is posthoc lineage and is not retroactive full-page SHA binding.'
  else:
   note='10月10日桌面/窄版完整畫面比較保留為歷史證據；D11/N12皆未記capture-time SHA。13:31事後manifest與目前d5d729…相合，舊build353872…差異來源未完整重建；不得宣稱目前SHA已整頁逐張驗證。'
   extra='Historical D11/N12 observations contain no capture-time SHA. The later13:31 manifest/current d5d729… match is posthoc only; the original build record names353872… instead. The exact change from that build is not reconstructed here, and no current-SHA whole-page comparison is claimed.'
 result['recordUpdates']['review_note']=note
 result['recordUpdates']['verified']=[v for v in original['recordUpdates']['verified']if not any(t in v for t in ['Actual','actual viewport','All16comparison','All13main comparison','FinalSHA-bound'])]+[extra]
 if extra not in result['remainingDifferences']:result['remainingDifferences'].append(extra)
 result['recordUpdates']['remaining']=result['remainingDifferences']
 result['scopeNote']=original.get('scopeNote','')+' Historical full-page and current-version scope are separated in '+evidence['brand']+'-oct12-evidence-lineage.json. Current full-page recapture/comparison flags are false.'
 for index,(check,phase_file)in enumerate(zip(result['checks'],phase_files)):
  path=w/phase_file;unchanged_hash=digest(path);phases=json.loads(path.read_text());width,height=([1280,720]if index==0 else[390,844]);mode=['desktop','narrow'][index]
  recorded=[{'phaseIndex':i,'observedAt':q['observed_at'],'captureTimeSha256':q['draft_sha256']}for i,q in enumerate(phases)if q.get('draft_sha256')]
  missing=[i for i,q in enumerate(phases)if not q.get('draft_sha256')]
  if prior:assert not missing and all(x['captureTimeSha256']==prior for x in recorded)
  for q in phases:
   if brand in ['raycast','warp','resend']:assert Image.open(w/q['screenshot']).size==(width,height)
  scope={'scope':mode,'historicalPhaseFile':phase_file,'historicalPhaseFileSha256':unchanged_hash,'phaseCount':len(phases),'observedAt':[phases[0]['observed_at'],phases[-1]['observed_at']],'originalCaptureTimeShaRecords':recorded,'missingCaptureTimeShaIndices':missing,'currentWholePageCaptureShaBound':False,'fullPageCurrentShaRecapturePerformed':False,'historicalObservationScope':'Original dated screenshots and measurements are retained; they have not been retagged as current-version captures.'}
  if prior:scope['historicalFullPageSha256']=prior
  check['historicalCompleteSequentialViewportCoverage']=bool(check.get('completeSequentialViewportCoverage',True))
  check['completeSequentialViewportCoverage']=False
  check['currentShaBoundCompleteSequentialViewportCoverage']=False
  check['currentFullPageComparisonComplete']=False
  check['historicalPhaseFile']=phase_file
  check['historicalPhaseFileSha256']=unchanged_hash
  check['captureTimeHashComplete']=not missing
  check['captureTimeHashRecordCount']=len(recorded)
  check['captureTimeHashMissingCount']=len(missing)
  check['coverageScope']='Historical full-page observed range. Current-SHA complete capture/comparison is false; see separate lineage and localized supplements.'
  if brand in ['raycast','warp']:
   file=f'{brand}-oct10-final-'+('footer'if brand=='raycast'else'chart')+'-'+mode
   supplement=read(file+'.json');assert Image.open(w/(file+'.jpg')).size==(width,height)
   capture_hash=supplement.get('draft_sha256')or supplement.get('previewSha256')
   scope['currentLocalizedSupplement']={'metadata':file+'.json','metadataSha256':digest(w/(file+'.json')),'screenshot':file+'.jpg','screenshotSha256':digest(w/(file+'.jpg')),'trueScreenshotDimensions':[width,height],'captureTimeHtmlSha256':capture_hash,'captureTimeHtmlShaRecorded':bool(capture_hash),'posthocAssociatedCurrentSha256':current_sha,'scope':'Footer Subscribe label only'if brand=='raycast'else'Two chart frame classes / visible chart area only','wholePageCurrentCapture':False}
   check['currentLocalizedSupplement']=scope['currentLocalizedSupplement']
  assert digest(path)==unchanged_hash
  evidence['scopes'].append(scope)
 result['captureBinding']={'kind':'historical full-page plus localized final changes'if prior else'historical observations with incomplete capture-time hashes','currentPreviewSha256':current_sha,'historicalFullPageSha256':prior,'currentFullPageCaptureComplete':False,'currentFullPageComparisonComplete':False,'unchangedByteScopeNormalizationVerified':bool(prior),'lineage':f'{brand}-oct12-evidence-lineage.json'}
 build['historicalHtmlRecord']=original_build['html']
 build['html']={'bytes':len(current),'sha256':current_sha}
 build['htmlDigestRecordKind']='Posthoc current file digest; not a new build or retroactive capture-time binding'
 build['htmlDigestNormalizedAt']=now
 build['captureBinding']=result['captureBinding']
 build['actualReviewScope']=extra
 build['remaining']=['Historical version/capture-time binding limitations documented in '+f'{brand}-oct12-evidence-lineage.json']+result['remainingDifferences']
 save(f'{brand}-oct12-evidence-lineage.json',evidence)
 save(result_name,result)
 save(f'{brand}-oct10-build-record.json',build)
 analysis=w/f'{brand}-oct10-analysis.md';old_analysis=analysis.read_text();marker='\n\n## 2026-10-12 驗證版本綁定校正\n'
 if marker in old_analysis:old_analysis=old_analysis.split(marker)[0]
 analysis.write_text(old_analysis.rstrip()+marker+'\n'+note+'\n\n'+extra+'\n\n完整歷史phase JSON未改寫，也沒有補造capture-time SHA。`currentFullPageCaptureComplete=false`、`currentFullPageComparisonComplete=false`；歷史完整觀察與精確未變範圍/局部補驗分開記錄，accepted=false。\n')
 paths=[]
 for p in w.glob(brand+'*'):
  if p.is_file()and p.name!=f'{brand}-oct10-file-hashes.json':paths.append(p)
  elif p.is_dir():paths.extend(q for q in p.rglob('*')if q.is_file())
 paths+=list(p for p in Path('scripts').glob('*'+brand+'*')if p.is_file())
 save(f'{brand}-oct10-file-hashes.json',{'recordedAt':now,'previewSha256':current_sha,'recordKind':'Posthoc current files; historical prior manifest preserved separately; not capture-time evidence','files':{str(p):{'bytes':p.stat().st_size,'sha256':digest(p)}for p in sorted(set(paths))}})
 print(json.dumps({'brand':brand,'currentSha256':current_sha,'currentFullPageCaptureComplete':False,'normalizationVerified':bool(prior),'missingCaptureHashes':[len(s['missingCaptureTimeShaIndices'])for s in evidence['scopes']],'phaseJsonMutated':False,'accepted':False}))
