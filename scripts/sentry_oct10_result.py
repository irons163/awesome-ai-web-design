from pathlib import Path
from datetime import datetime, timezone
from PIL import Image
import json, hashlib

p = Path('.stitch-work/current-official')
brand = 'sentry'
sha = lambda f: hashlib.sha256(f.read_bytes()).hexdigest()
hs = sha(p / 'sentry.html')
checks = {}
for w in (1280, 390):
    a = json.loads((p / f'{brand}-oct10-official-{w}-phases.json').read_text())
    b = json.loads((p / f'{brand}-oct10-local-{w}-phases.json').read_text())
    def coverage(ps):
        end = 0
        gaps = []
        for r in sorted(ps, key=lambda x: x['scrollY']):
            if r['scrollY'] > end + .01:
                gaps.append([end, r['scrollY']])
            end = max(end, r['scrollY'] + r['viewport']['height'])
        return {'gaps': gaps, 'covered_to': end, 'final_page_height': ps[-1]['bodyHeight']}
    pairs = [{'official_text': x['text'], 'local_text': y['text'],
              'same_text': x['text'] == y['text'],
              'box_deltas': {k: y['box'][k] - x['box'][k] for k in ['x', 'y', 'width', 'height']}}
             for x, y in zip(a[-1]['headings'], b[-1]['headings'])
             if x['box']['height'] > 0 or y['box']['height'] > 0]
    dims = [{'path': r['screenshot'], 'actual_size': list(Image.open(p / r['screenshot']).size),
             'matches_declared': list(Image.open(p / r['screenshot']).size) == [r['viewport']['width'], r['viewport']['height']]}
            for r in a + b]
    ref = json.loads((p / f'{brand}-oct10-official-{w}-reference.json').read_text())
    html = ''.join(ref['htmlParts'])
    checks[str(w)] = {
        'viewport': b[-1]['viewport'], 'official_height': a[-1]['bodyHeight'], 'local_height': b[-1]['bodyHeight'],
        'heading_pairs': pairs, 'max_visible_heading_delta': max(abs(v) for q in pairs for v in q['box_deltas'].values()),
        'all_heading_texts_match_including_hidden': [x['text'] for x in a[-1]['headings']] == [x['text'] for x in b[-1]['headings']],
        'official_phases': f'{brand}-oct10-official-{w}-phases.json', 'local_phases': f'{brand}-oct10-local-{w}-phases.json',
        'official_coverage': coverage(a), 'local_coverage': coverage(b), 'actual_screenshot_dimensions': dims,
        'all_dimensions_match': all(x['matches_declared'] for x in dims),
        'all_local_phases_bound_to_final_html': all(r.get('draft_sha256') == hs for r in b),
        'local_broken_visible_images': sum(len(r['brokenVisibleImages']) for r in b),
        'local_horizontal_overflow': any(r['bodyWidth'] > w for r in b),
        'complete_reference': {'html_length': len(html), 'length_matches_record': len(html) == ref['html_length'],
                               'has_end_body_html': '</body>' in html and html.rstrip().endswith('</html>'),
                               'sha256': hashlib.sha256(html.encode()).hexdigest(),
                               'hash_matches_record': hashlib.sha256(html.encode()).hexdigest() == ref['html_sha256']},
        'scope': 'Actual desktop1280×720 and narrow390×844 native browser viewports with desktop UA. Complete default homepage scroll coverage; not physical phone or other widths.'}

assets = json.loads((p / 'sentry-oct10-assets.json').read_text())
native = json.loads((p / 'sentry-oct10-native-retention.json').read_text())
py_a = json.loads((p / 'sentry-oct10-official-python-settled.json').read_text())
py_b = json.loads((p / 'sentry-oct10-local-python.json').read_text())
record = {
    'brand': brand, 'observed_at': datetime.now(timezone.utc).isoformat(),
    'reference_url': 'https://sentry.io/welcome/', 'reference_final_url': 'https://sentry.io/welcome/',
    'accepted': False, 'status': 'in_visual_review', 'native_generation': native,
    'prompt': 'sentry-oct10-prompt.md',
    'preserved': 'Existing design analysis, genuine Google Stitch MCP desktop/mobile exports, original thumbnails and full provider responses are preserved unchanged. Fresh complete source observations found no new main heading/paragraph content and the same stylesheet URLs, so earlier native outputs are retained transparently. This is not a claim of a fresh generation or an untouched native export.',
    'implementation': {'html': 'sentry.html', 'sha256': hs, 'bytes': (p / 'sentry.html').stat().st_size,
                       'method': 'Current complete public DOM/CSS/original observed assets corrected after retained genuine native Stitch. Source-backed root navigation, SDK/tabs and carousel initial-state correction; original public Rive runtime and artwork retained locally.'},
    'corrections': [
        'Preserved complete desktop/narrow current DOM chunks, verified their lengths and hashes, and retained all original native exports.',
        'Removed escaped noscript head fallback before parsing, avoiding24px of literal fallback text.',
        'Preserved153 original public pageAssets and four exact observed Rive runtime/WASM/artwork/helper URLs, with source hashes.',
        'Adapted only the original Rive runtime relative helper import into a separate derivative; loaded original local WASM/artwork with intersection playback.',
        'Restored native root mobile menu, scroll header styling, bounded tab state and native SDK selection markup.',
        'Corrected54px narrow excess caused by eager-loading initially inert offscreen feature images; default inactive images retain the observed initial zero size.',
        'Re-captured all final13desktop and13narrow local phases after the last change, with finalHTML SHA256 bindings.',
        'Compared every screenshot pair, root mobile menu open/close, and settled Python installation state against actual official screenshots.'
    ],
    'checks': checks,
    'assets': {'manifest': 'sentry-oct10-assets.json', 'original_count': len(assets['assets']),
               'original_bytes': sum(x['bytes'] for x in assets['assets']), 'failures': assets.get('failures', []),
               'rive_derivative': assets.get('rive_derivative'),
               'notes': '157 original assets and one separate local-module derivative. Exact public URL/byte/hash provenance is preserved. No paid service invoked.'},
    'menu': {'official': 'sentry-oct10-official-mobile-menu.jpg', 'local': 'sentry-oct10-local-mobile-menu.jpg',
             'check': 'sentry-oct10-local-menu-check.json', 'visually_compared': True, 'root_open_close_verified': True},
    'python_sdk': {'official': 'sentry-oct10-official-python-settled.jpg', 'local': 'sentry-oct10-local-python.jpg',
                   'visually_compared': True, 'box_matches': py_a['box'] == py_b['box'],
                   'official_box': py_a['box'], 'local_box': py_b['box'],
                   'note': 'Earlier official transition screenshot and zero-height metadata retained as diagnostic evidence; settled screenshot is canonical. CSS transition was allowed to finish before final comparison.'},
    'remaining_differences': [
        'The original Rive hero runs locally, but its animation time, scan beam, terminal lines and customer-logo marquee phase differ from the official frame.',
        'Narrow first-screen original artwork appears slightly blurred at a different Rive playback phase. Exact frame synchronization is not accepted.',
        'Menu focus ring and transient browser scrollbars can differ after interaction; the compared root menu geometry/content match.',
        'Marketing Mode alternate homepage, all desktop/nested mobile navigation branches, feature-carousel visited/lazy-load states, tab branches and all23SDKs are not exhaustively verified. Default and Python SDK states only are evidenced.',
        'Copy-code, newsletter, chatbot, signup, demos and account/backend service behavior are not reproduced or submitted. Official destinations remain linked.',
        'Other widths, physical devices and final published deployment are for root verification.'
    ],
    'proposed_progress_update': {'status': 'in_visual_review', 'accepted': False, 'reference_url': 'https://sentry.io/welcome/',
                                 'reference_checked_at': '2026-10-11', 'review_path': 'sentry-oct10-result.json',
                                 'prompt_path': 'sentry-oct10-prompt.md',
                                 'visual_verification': 'Full default homepage13desktop/13narrow screenshots compared. Heights8796/10798 and18desktop/17narrow visible heading boxes match with0delta;157original assets, original Rive, root menu and settled Python panel verified. Motion/alternate UI/service limits remain; do not label official-identical.'}
}
pending = p / 'sentry-oct10-pending-review.json'
if pending.exists():
    d = json.loads(pending.read_text())
    d.update({'resolved_at': datetime.now(timezone.utc).isoformat(), 'status': 'final_render_review_completed_with_explicit_limits',
              'final_result': 'sentry-oct10-result.json', 'pending': []})
    pending.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
files = [f for f in p.glob('sentry-oct10-*') if f.is_file() and f.name not in ['sentry-oct10-result.json', 'sentry-oct10-hashes.json']]
files += [p / 'sentry.html'] + [f for f in (p / 'sentry-assets/oct10').rglob('*') if f.is_file()]
manifest = [{'path': str(f.relative_to(p)), 'bytes': f.stat().st_size, 'sha256': sha(f)} for f in sorted(set(files))]
(p / 'sentry-oct10-hashes.json').write_text(json.dumps(manifest, indent=2) + '\n')
record['hash_manifest'] = 'sentry-oct10-hashes.json'
(p / 'sentry-oct10-result.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'accepted': False, 'html_sha256': hs, 'assets': len(assets['assets']),
                  'heights': {k: v['local_height'] for k, v in checks.items()},
                  'visible_headings': {k: len(v['heading_pairs']) for k, v in checks.items()},
                  'all_hash_bound': all(v['all_local_phases_bound_to_final_html'] for v in checks.values()),
                  'all_dimensions_match': all(v['all_dimensions_match'] for v in checks.values())}))
