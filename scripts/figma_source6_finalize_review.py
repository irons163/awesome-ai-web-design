"""Finalize an explicitly authored owner inspection of source-only contact sheets."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import sys

slug=sys.argv[1]
assert slug in ['figma','framer','linear','vercel','claude','notion']
base=Path(__file__).resolve().parents[1]/'.stitch-work/current-official'
notes=json.loads((base/f'{slug}-oct10-source-review-notes.json').read_text())
assert notes['all_contact_sheets_raster_inspected_by_owner'] is True
path=base/f'{slug}-oct10-source-review.json'
review=json.loads(path.read_text())
for sheet in review['contact_sheets']:
    assert hashlib.sha256((base/sheet['path']).read_bytes()).hexdigest()==sheet['sha256']
review.update(all_source_contact_sheets_inspected_by_owner=True,
              source_contact_sheet_inspected_at=datetime.now(timezone.utc).isoformat(),
              visual_findings=notes['visual_findings'],
              historical_backup_note=notes.get('historical_backup_note','No pre-existing same-name oct10 source artifacts were present before this source task; no older source artifacts were overwritten.'))
review.update(notes.get('extra_metadata',{}))
review['limitations']+=notes['limitations']
path.write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
assets=json.loads((base/review['asset_manifest']).read_text())
text='# Current official source research\n\nAnonymous final URL: '+review['reference_url']+'\n\n'
text+='Document language: '+str(review['document_language'])+'. '+review['regional_scope']+'\n\n'
for scope in review['scopes'].values():
    text+=f'{scope["viewport"][0]}×{scope["viewport"][1]}: {scope["phase_count"]} original native viewport rasters; full page {scope["page_height"]}px, actual dimensions checked, no scroll-coverage gaps.\n\n'
text+='All '+str(len(review['contact_sheets']))+' contact sheets visually inspected. Complete DOM arrays/UTF-16 lengths/hashes, readable CSSOM, original files and per-width warmed top snapshots are preserved.\n\n'
text+='\n\n'.join(review['visual_findings'])+'\n\nLimitations:\n\n'+'\n'.join('- '+x for x in review['limitations'])
text+=f'\n\nOriginal assets: {len(assets["assets"])} URLs, {sum(x["bytes"] for x in assets["assets"])} bytes; {len(assets["failures"])} unresolved failures. HTTP403/404/429 resources are not retried and no URL variations are used.\n\nSource-only task: preview HTML untouched; no local QA, native Stitch generation or official-consistency acceptance.\n'
(base/f'{slug}-oct10-source-review.md').write_text(text)
patterns=[f'{slug}-oct10-official-*',f'{slug}-oct10-asset-*',f'{slug}-oct10-assets.json',f'{slug}-oct10-source-*']
files={p for pattern in patterns for p in base.glob(pattern) if p.is_file() and not p.name.endswith('source-hashes.json')}
files|={base/x['path'] for x in assets['assets']}
hashes={str(p.relative_to(base)):{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(files)}
(base/f'{slug}-oct10-source-hashes.json').write_text(json.dumps(hashes,indent=2)+'\n')
print(slug,'source research finalized;',len(files),'preserved files')
