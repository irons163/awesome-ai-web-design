"""Finalize only an owner-inspected, hash-bound public homepage review."""
import datetime,hashlib,json,re,sys
from pathlib import Path
from PIL import Image
p=Path('.stitch-work/current-official');slug=sys.argv[1];cfg=json.loads((p/f'{slug}-oct10-result-input.json').read_text());assert cfg['raster_reviewed_by_owner'] is True
H=lambda b:hashlib.sha256(b).hexdigest();preview=H((p/f'{slug}.html').read_bytes());now=datetime.datetime.now(datetime.timezone.utc).isoformat();checks={}
for w,h in ((1280,720),(390,844)):
 sides={s:json.loads((p/f'{slug}-oct10-{s}-{w}-phases.json').read_text()) for s in ('official','local')};coverage={}
 for side,a in sides.items():
  end=0;gaps=[];dims=[]
  for x in a:
   if x['scrollY']>end+1:gaps.append([end,x['scrollY']])
   end=max(end,x['scrollY']+h);dim=Image.open(p/x['screenshot']).size;sx,sy=dim[0]/w,dim[1]/h
   assert abs(dim[0]*h/w-dim[1])<=1.1 and .98<=sx<=1.01 and .98<=sy<=1.01,(side,w,dim)
   assert x['viewport']=={'width':w,'height':h}
   if side=='local':assert x['draft_sha256']==preview
   dims.append({'screenshot':x['screenshot'],'actual_raster_dimensions':dim,'css_viewport':[w,h],'uniform_scale':[sx,sy],'exact_css_dimensions':dim==(w,h)})
  assert not gaps and abs(a[0]['scrollY'])<=1 and end>=a[-1]['bodyHeight']-1
  coverage[side]={'phase_count':len(a),'covered_to':end,'page_height':a[-1]['bodyHeight'],'gaps':gaps,'dimensions':dims,'complete_raster_content_inspected':True}
 a=[x for x in sides['official'][0]['headings'] if x['box']['height']>0 and (cfg.get('heading_filter')!='horizontal_viewport' or x['box']['x']<w and x['box']['x']+x['box']['width']>0)];b=[x for x in sides['local'][0]['headings'] if x['box']['height']>0 and (cfg.get('heading_filter')!='horizontal_viewport' or x['box']['x']<w and x['box']['x']+x['box']['width']>0)];pairs=[]
 for i,(x,y) in enumerate(zip(a,b)):
  normalize=lambda t:re.sub(r'\s+',' ',t).strip().upper()
  pairs.append({'index':i,'official_text':normalize(x['text']),'local_text':normalize(y['text']),'text_match':normalize(x['text'])==normalize(y['text']),'max_box_delta':max(abs(x['box'][k]-y['box'][k]) for k in ('x','y','width','height'))})
 checks[str(w)]={'coverage':coverage,'official_positive_size_headings':len(a),'local_positive_size_headings':len(b),'heading_pairs':pairs,'maximum_paired_heading_box_delta':max([x['max_box_delta'] for x in pairs],default=0),'all_paired_heading_text_matches':len(a)==len(b) and all(x['text_match'] for x in pairs),'overflow':any(x['bodyWidth']>w for a in sides.values() for x in a),'broken_visible_images':sum(len(x['brokenVisibleImages']) for a in sides.values() for x in a),'raster_reviewed':True,'local_sha256':preview}
assets=json.loads((p/f'{slug}-oct10-assets.json').read_text());limits=cfg['remaining_differences_and_limits'];assert limits
(p/f'{slug}-oct10-design-analysis.md').write_text('# '+cfg['name']+' 現行官方首頁設計分析\n\n'+cfg['design_analysis_text']+'\n\n原始 DESIGN.md、先前原生 Stitch 匯出與本次完整資料均保留。此為有明確範圍的視覺研究；未驗證項目不得宣稱官方一致。\n')
review='# '+cfg['name']+' visual review\n\nFinal preview SHA256: `'+preview+'`.\n\n'+cfg['visual_review_text']+'\n\nCoverage and actual original raster dimensions are recorded in the result JSON. CSS viewport coverage and raster pixel resolution are separate measurements. Uniformly scaled originals are retained unaltered; comparison montages may normalize viewing widths. Cropped or stale compositor diagnostics are excluded.\n\nRemaining differences and limits:\n\n'+''.join('- '+x+'\n' for x in limits)
(p/f'{slug}-oct10-visual-review.md').write_text(review)
r={'brand':slug,'observed_at':now,'audit_date':now[:10],'reference_url':cfg['reference_url'],'reference_final_url':cfg['reference_url'],'accepted':False,'status':'in_visual_review','official_consistency_claim':False,'preview_sha256':preview,'latest_draft_full_desktop_and_narrow_coverage':True,'actual_raster_inspection_bound_to_current_preview':True,'latest_draft_actual_render_checked':True,'native_generation':cfg['native_generation'],'implementation':{'html':slug+'.html','sha256':preview,'bytes':(p/f'{slug}.html').stat().st_size,'method':cfg['implementation_method']},'design_analysis':f'{slug}-oct10-design-analysis.md','rewritten_prompts':f'{slug}-oct10-prompt.md','visual_review':f'{slug}-oct10-visual-review.md','assets':{'manifest':f'{slug}-oct10-assets.json','original_count':len(assets['assets']),'original_bytes':sum(a['bytes'] for a in assets['assets']),'failures':assets['failures'],'notes':cfg.get('asset_notes','All originals retained with exact observed public URL and SHA256. No paid service invoked.')},'checks':checks,'corrections':cfg['corrections'],'raster_evidence':{'desktop_official':f'{slug}-oct10-official-1280-phases.json','narrow_official':f'{slug}-oct10-official-390-phases.json','desktop_local':f'{slug}-oct10-local-1280-phases.json','narrow_local':f'{slug}-oct10-local-390-phases.json','reviewed_montages':[f'{slug}-oct10-comparison-{w}-{i}.jpg' for w in (1280,390) for i in range((min(len(json.loads((p/f'{slug}-oct10-official-{w}-phases.json').read_text())),len(json.loads((p/f'{slug}-oct10-local-{w}-phases.json').read_text())))+3)//4)]},'remaining_differences_and_limits':limits,'remaining_differences':limits,'proposed_progress_update':{'status':'in_visual_review','accepted':False,'reference_checked_at':now[:10],'reference_url':cfg['reference_url'],'review_path':f'{slug}-oct10-result.json','prompt_path':f'{slug}-oct10-prompt.md','visual_verification':cfg['progress_note']},'hash_manifest':f'{slug}-oct10-hashes.json',**cfg.get('extra',{})}
manifest={}
for f in sorted(p.glob(slug+'-oct10-*')):
 if f.is_file() and f.name not in (f'{slug}-oct10-result.json',f'{slug}-oct10-hashes.json'):manifest[f.name]={'sha256':H(f.read_bytes()),'bytes':f.stat().st_size}
manifest[slug+'.html']={'sha256':preview,'bytes':(p/f'{slug}.html').stat().st_size};(p/f'{slug}-oct10-hashes.json').write_text(json.dumps(manifest,indent=2)+'\n');(p/f'{slug}-oct10-result.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'brand':slug,'preview_sha256':preview,'bytes':r['implementation']['bytes'],'checks':{w:{'official_height':x['coverage']['official']['page_height'],'local_height':x['coverage']['local']['page_height'],'heading_counts':[x['official_positive_size_headings'],x['local_positive_size_headings']],'max_delta':x['maximum_paired_heading_box_delta'],'text_matches':x['all_paired_heading_text_matches']} for w,x in checks.items()}},ensure_ascii=False))
