import datetime,hashlib,json
from pathlib import Path
from PIL import Image
p=Path('.stitch-work/current-official');H=lambda b:hashlib.sha256(b).hexdigest();now=datetime.datetime.now(datetime.timezone.utc).isoformat()
for slug,width,height,interval in [('replicate',1280,720,[4320,5040]),('together.ai',390,844,[0,1.5])]:
 source=p/f'{slug}-oct12-supplement-reference.json';fresh=json.loads(source.read_text());html=''.join(fresh['htmlParts']);assert len(html.encode('utf-16-le'))//2==fresh['html_length'] and H(html.encode())==fresh['html_sha256'] and html.endswith('</html>');assert Image.open(p/fresh['screenshot']).size==(width,height);assert H((p/fresh['screenshot']).read_bytes())==fresh['screenshot_sha256'];assert fresh['scrollY']==interval[0]
 result_path=p/f'{slug}-oct10-result.json';result=json.loads(result_path.read_text());preview=H((p/f'{slug}.html').read_bytes());assert preview==result['preview_sha256']
 phases_path=p/f'{slug}-oct10-official-{width}-phases.json';backup=p/f'{slug}-oct12-original-official-{width}-phases.json';
 if not backup.exists():backup.write_bytes(phases_path.read_bytes())
 phases=json.loads(backup.read_text());record={k:v for k,v in fresh.items() if k not in ['htmlParts','images','stylesheets','html_length']};record['source_reference']=source.name;record['actual_raster_dimensions']=[width,height];record['fresh_supplement']=True
 if slug=='replicate':
  original=phases[6];record['supersedes_original_raster']=original['screenshot'];record['superseded_raster_sha256']=H((p/original['screenshot']).read_bytes());record['brokenVisibleImages']=[];record['prefers_reduced_motion']=False;phases[6]=record
 else:phases.insert(0,record)
 end=0;gaps=[]
 for phase in phases:
  assert Image.open(p/phase['screenshot']).size==(width,height)
  if phase['scrollY']>end+1:gaps.append([end,phase['scrollY']])
  end=max(end,phase['scrollY']+height)
 assert not gaps and phases[0]['scrollY']==0 and end>=phases[-1]['bodyHeight']
 phases_path.write_text(json.dumps(phases,ensure_ascii=False,indent=2)+'\n')
 old_refs=list(p.glob(f'{slug}-oct10-official-{width}-reference.json'));old_source_hash=json.loads(old_refs[0].read_text()).get('html_sha256') if old_refs else None
 supplement={'captured_at_utc':fresh['observed_at'],'local_date':'2026-10-12','timezone':'Asia/Taipei','not_backdated':True,'reference_url':fresh['url'],'source_reference':source.name,'source_html_sha256':fresh['html_sha256'],'prior_source_html_sha256':old_source_hash,'screenshot':fresh['screenshot'],'screenshot_sha256':fresh['screenshot_sha256'],'actual_raster_dimensions':[width,height],'scrollY':fresh['scrollY'],'covered_interval':interval,'full_viewport_interval':[fresh['scrollY'],fresh['scrollY']+height],'preview_sha256_unchanged':preview,'comparison_raster':f'{slug}-oct12-supplement-comparison.jpg','actual_comparison_raster_inspected_by_owner':True,'canonical_phase_file':phases_path.name,'original_phase_file_preserved':backup.name,'canonical_coverage_after_supplement':{'phase_count':len(phases),'covered_to':end,'page_height':phases[-1]['bodyHeight'],'gaps':gaps},'scope_note':'Fresh supplement plus retained earlier official captures provide continuous reviewed CSS coverage. This does not assert all captures came from the same time/version. Only the supplemented viewport was freshly compared to the unchanged locally reviewed preview.'}
 if slug=='replicate':supplement['scope_note']+=' The fresh whole-page source hash differs; dynamic model run counts/order and animation can differ. The4320–5040 band retains the same code/Scale copy/logo layout at7994px total height. Original phase6 raster repeated3600 despite4320 metadata and is excluded.'
 else:supplement['scope_note']+=' The current top hero/header layout and6456px total height were observed; logo marquee phase differs. Retaining the original1.5px phase alongside the new0px phase also prevents a new844–845.5px coverage gap.'
 result['supplemental_source_evidence']=[supplement];result['source_coverage_repaired_at']=now;result['accepted']=False;result['official_consistency_claim']=False
 result['normalization_evidence']['source_coverage_correction']=supplement;result['normalization_evidence']['basis']='Earlier actual owner raster review bound to unchanged preview hash, with an offline audit subsequently finding a source-raster coverage gap. The explicitly dated2026-10-12 Taipei fresh supplement closes that gap; preserved prior timestamps are not rewritten.'
 note='Source coverage supplement captured2026-10-12 Asia/Taipei ('+fresh['observed_at']+' UTC): '+str(interval)+' CSS px. Combined evidence spans different capture times; no historical or animation/service equivalence claim.'
 for key in ['remaining_differences','remaining_differences_and_limits']:
  if note not in result[key]:result[key].append(note)
 review_path=p/result['visual_review'];review=review_path.read_text();marker='\n\n## Explicitly dated source coverage supplement\n\n'
 review=review.split(marker)[0]+marker+note+'\n\n'+supplement['scope_note']+'\n\nOriginal phase JSON: `'+backup.name+'`. Fresh source context: `'+source.name+'`. Fresh screenshot and comparison rasters were actually inspected. Preview remains `'+preview+'`.\n';review_path.write_text(review)
 result_path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 hashpath=p/result['hash_manifest'];hashes=json.loads(hashpath.read_text());list_format=isinstance(hashes,list);hashes={x['path']:{k:v for k,v in x.items() if k!='path'} for x in hashes} if list_format else hashes
 for f in [phases_path,review_path,result_path,*p.glob(slug+'-oct12-*')]:
  if f.is_file():hashes[f.name]={'sha256':H(f.read_bytes()),'bytes':f.stat().st_size}
 hashpath.write_text(json.dumps([{'path':k,**v} for k,v in sorted(hashes.items())] if list_format else hashes,indent=2)+'\n')
 print(json.dumps({'brand':slug,'supplement_time_utc':fresh['observed_at'],'preview_unchanged':preview,'canonical_phases':len(phases),'coverage_end':end,'gaps':gaps}))
