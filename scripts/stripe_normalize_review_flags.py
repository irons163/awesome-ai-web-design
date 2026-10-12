from pathlib import Path
from datetime import datetime, timezone
import json, hashlib
from PIL import Image

p = Path('.stitch-work/current-official')
sha = lambda f: hashlib.sha256(f.read_bytes()).hexdigest()
descriptions = {
    'stripe': 'Financial infrastructure homepage with a lavender gradient hero, Stripe typography, original diagrams, product demonstrations and long editorial sections. Current localized en-ca public copy and original assets are preserved. Motion is bounded by the explicit review limits.',
    'tesla': 'White Tesla navigation over full-width vehicle photography, centered product labels and clean compact CTAs. Current1.99%APR campaign, vehicle order, service demonstrations and footer copy follow the observed official page. Dynamic counters and map behavior remain dated observations.',
    'mistral.ai': 'Cream, black and warm orange Sovereign AI homepage with original ALTMistral typography and photographic media. Current MistralLarge4 and organization-choice copy, editorial sections and footer preserve the observed official structure. Native motion and product services remain bounded.',
    'replicate': 'Minimal black-and-white developer homepage with oversized type, original model thumbnails, code examples, model cards and pink/deep-purple accents. Original model art and source typography/layout are preserved; the shader grid and late-loading thumbnail states have explicit differences.',
    'together.ai': 'AI Native Cloud homepage with warm white typography over dark blue/violet, original illustration assets, a three-part platform section, research and customer stories. Current content, responsive geometry and observed platform-state markup are preserved; animation and backend services remain limited.',
    'sanity': 'Content Operations homepage with a yellow/white editorial system, bold original typography, chapter graphics, product/editor illustrations and automation nodes. The current complete source and original media inform layout corrections; editor/API/customer motion states remain scoped differences.',
    'sentry': 'Dark violet developer homepage with DammitSans display type, Rubik text, rotated magenta emphasis, grain/space artwork, original Rive animation and monitoring screenshots. Current default page, native root menu and Python install state are visually compared; alternate modes and service behavior remain unaccepted.'
}
for brand, description in descriptions.items():
    f = p / f'{brand}-oct10-result.json'
    d = json.loads(f.read_text())
    preview_hash = sha(p / f'{brand}.html')
    if brand == 'stripe':
        declared = d['hashes'][brand + '.html']['sha256']
    else:
        manifest = json.loads((p / d['hash_manifest']).read_text())
        declared = next(x['sha256'] for x in manifest if x['path'] == brand + '.html')
    if declared != preview_hash:
        raise RuntimeError(f'{brand}: current preview differs from reviewed hash')
    scopes = {}
    for key, c in d['checks'].items():
        if brand == 'stripe':
            pairs = json.loads((p / f'stripe-oct10-{key}-segments.json').read_text())
            local = [x['local'] for x in pairs]
        elif brand == 'tesla':
            local = c['local_segments']
        elif brand == 'mistral.ai':
            local = json.loads((p / c['final_local_phases']).read_text())
        else:
            local = json.loads((p / c['local_phases']).read_text())
        end = 0
        gaps = []
        dimensions = []
        for r in sorted(local, key=lambda x: x.get('scrollY', x.get('y', 0))):
            y = r.get('scrollY', r.get('y', 0))
            viewport = r.get('viewport', {'width': r.get('width'), 'height': r.get('height')})
            height = viewport['height']
            if y > end + 1:
                gaps.append([end, y])
            end = max(end, y + height)
            filename = r.get('screenshot', r.get('file'))
            dimensions.append(list(Image.open(p / filename).size) == [viewport['width'], height])
        page_height = local[-1].get('bodyHeight', local[-1].get('pageHeight'))
        if gaps or end < page_height or not all(dimensions):
            raise RuntimeError(f'{brand}/{key}: incomplete coverage or incorrect raster dimensions')
        scopes[key] = {'phase_count': len(local), 'gaps': gaps, 'covered_to': end, 'page_height': page_height,
                       'actual_dimensions_match': all(dimensions)}
    remaining = d.get('remaining_differences', d.get('remaining', []))
    d.update({'preview_sha256': preview_hash, 'latest_draft_full_desktop_and_narrow_coverage': True,
              'actual_raster_inspection_bound_to_current_preview': True, 'latest_draft_actual_render_checked': True,
              'accepted': False, 'official_consistency_claim': False, 'remaining_differences_and_limits': remaining,
              'normalized_review_flags_at': datetime.now(timezone.utc).isoformat(),
              'normalization_evidence': {'basis': 'Existing actual browser captures and owner raster comparisons already completed for this same unchanged preview hash; no new browser run or expanded acceptance claim.', 'coverage_and_dimensions_rechecked': scopes}})
    analysis = f'{brand}-oct10-design-analysis.md'
    review = f'{brand}-oct10-visual-review.md'
    (p / analysis).write_text('# Current public homepage design observation\n\n' + description + '\n\nThe original repository design-md/' + brand + '/DESIGN.md remains preserved. This dated observation supplements it. It does not certify exact official consistency.\n')
    (p / review).write_text('# Scoped actual visual review\n\nReference: ' + d['reference_url'] + '\n\nReviewed preview SHA-256: ' + preview_hash + '\n\nActual desktop and390px narrow homepage screenshots were compared across complete scroll coverage. Existing screenshot dimensions and current preview hash were rechecked when normalizing this record. This records a completed scoped visual review; accepted=false and official_consistency_claim=false.\n\n' + '\n'.join('- ' + str(x) for x in remaining) + '\n')
    d['design_analysis'] = analysis
    d['rewritten_prompts'] = d['prompt']
    d['visual_review'] = review
    f.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
    if d.get('hash_manifest'):
        mf = p / d['hash_manifest']
        rows = json.loads(mf.read_text())
        for name in [analysis, review]:
            rows = [x for x in rows if x['path'] != name]
            file = p / name
            rows.append({'path': name, 'bytes': file.stat().st_size, 'sha256': sha(file)})
        mf.write_text(json.dumps(sorted(rows, key=lambda x: x['path']), indent=2) + '\n')
    print(brand, 'normalized same reviewed hash', preview_hash, flush=True)
