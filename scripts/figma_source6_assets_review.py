"""Prepare preserved source assets/contact sheets; never change a preview."""
import concurrent.futures
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys
import urllib.error
import urllib.request
from urllib.parse import urlsplit, urljoin
from PIL import Image, ImageDraw

SLUG = sys.argv[1]
assert SLUG in ['figma', 'framer', 'linear', 'vercel', 'claude', 'notion']
BASE = Path(__file__).resolve().parents[1] / '.stitch-work/current-official'
NOW = datetime.now(timezone.utc).isoformat()
tracking = re.compile(r'google-analytics|analytics\.google|doubleclick|googlead|/pagead/|/collect(?:[/?]|$)|/pixel|segment\.com|bat\.bing|facebook\.com/tr|connect\.facebook|googletagmanager', re.I)
denied = re.compile(r'\b(403|404|429)\b')
target = BASE / f'{SLUG}-assets' / 'oct10'
target.mkdir(parents=True, exist_ok=True)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def fingerprint(path):
    data = path.read_bytes()
    return {'path': str(path.relative_to(BASE)), 'bytes': len(data), 'sha256': digest(data)}


def extension(data, content_type, url):
    if data.startswith(b'RIFF') and data[8:12] == b'WEBP': return '.webp'
    if data.startswith(b'\x89PNG'): return '.png'
    if data.startswith(b'\xff\xd8'): return '.jpg'
    if data.startswith(b'wOF2'): return '.woff2'
    if b'<svg' in data[:1000]: return '.svg'
    if data[4:8] == b'ftyp': return '.avif' if b'avif' in data[:32] else '.mp4'
    return {'text/css': '.css', 'font/woff': '.woff', 'font/ttf': '.ttf'}.get(content_type.split(';')[0], Path(urlsplit(url).path).suffix or '.bin')


bundle = json.loads((BASE / f'{SLUG}-oct10-asset-bundle.json').read_text())
ledger_path = BASE / f'{SLUG}-oct10-source-asset-attempts.json'
ledger = json.loads(ledger_path.read_text()) if ledger_path.exists() else {}
items = {a['url']: a for a in bundle['assets'] + bundle['failures'] if not tracking.search(a['url'])}
references = {}
for width in [1280, 390]:
    path = BASE / f'{SLUG}-oct10-official-{width}-reference.json'
    reference = json.loads(path.read_text())
    html = ''.join(reference['htmlParts'])
    assert len(html.encode('utf-16-le')) // 2 == reference['html_length']
    assert digest(html.encode()) == reference['html_sha256']
    assert '</body>' in html.lower() and re.search(r'</html>\s*$', html, re.I), path.name
    references[width] = reference
    for url in [x['src'] for x in reference['images']] + reference['stylesheets']:
        if url.startswith('https://') and not tracking.search(url):
            items.setdefault(url, {'url': url})


def preserve(item):
    url = item['url']
    previous = ledger.get(url)
    if previous:
        if previous.get('asset'):
            asset = previous['asset']
            assert digest((BASE / asset['path']).read_bytes()) == asset['sha256']
            return asset, previous
        return None, previous  # A failed exact URL is never retried.
    record = {'url': url, 'attempted_at': NOW, 'pageAssets_reason': item.get('reason')}
    try:
        if item.get('path'):
            data = Path(item['path']).read_bytes()
            content_type = item.get('contentType') or ''
            method = 'pageAssets original bytes, copied unchanged from its exported file'
        else:
            if denied.search(item.get('reason', '')):
                record.update(error=item['reason'], http_denial_seen=True, retried=False,
                              acquisition='No additional request after pageAssets HTTP403/404/429')
                return None, record
            if not url.startswith('https://'):
                record.update(error='No file bytes exported for non-HTTPS inline resource', retried=False)
                return None, record
            request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': '*/*'})
            with urllib.request.urlopen(request, timeout=35) as response:
                data = response.read()
                content_type = response.headers.get('Content-Type', '')
                record['final_asset_response_url'] = response.geturl()
            method = 'One unauthenticated HTTPS GET of the exact observed public asset URL; no HTTP-denial retry or URL variation'
        sha = digest(data)
        path = target / (sha[:20] + extension(data, content_type, url))
        path.write_bytes(data)
        asset = {'source_url': url, 'path': str(path.relative_to(BASE)), 'bytes': len(data),
                 'sha256': sha, 'contentType': content_type, 'acquisition': method,
                 'preserved_at': NOW}
        record['asset'] = asset
        return asset, record
    except urllib.error.HTTPError as error:
        record.update(error=str(error), http_status=error.code, retried=False,
                      http_denial_seen=error.code in [403, 404, 429])
        return None, record
    except Exception as error:
        record.update(error=str(error), retried=False)
        return None, record


assets, failures = [], []
seen_urls = set()
pending = items
for depth in range(5):
    if not pending: break
    fresh_assets = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        for url, future in [(url, pool.submit(preserve, item)) for url, item in pending.items()]:
            seen_urls.add(url)
            asset, record = future.result()
            ledger[url] = record
            write_json(ledger_path, ledger)
            if asset:
                assets.append(asset)
                fresh_assets.append(asset)
            else: failures.append({'source_url': url, **{k: v for k, v in record.items() if k != 'url'}})
    pending = {}
    for asset in fresh_assets:
        if asset['contentType'].split(';')[0] != 'text/css' and not asset['path'].endswith('.css'): continue
        css = (BASE / asset['path']).read_text(errors='replace')
        # Match a complete quoted data SVG, rather than its nested filter url(#a).
        candidates = [next(x for x in match.groups() if x is not None)
                      for match in re.finditer(r'url\(\s*(?:"([^"]*)"|\'([^\']*)\'|([^)]*))\s*\)', css)]
        candidates += re.findall(r'@import\s+[\"\']([^\"\']+)', css)
        for raw in candidates:
            if raw.startswith(('data:', '#', '%23')) or raw.startswith('--'): continue
            url = urljoin(asset['source_url'], raw.strip())
            if not url.startswith('https://') or url in seen_urls or tracking.search(url): continue
            pending.setdefault(url, {'url': url, 'observed_in_official_stylesheet': asset['source_url']})
manifest = {'source_research_only': True, 'prepared_at': NOW,
            'assets': sorted(assets, key=lambda x: x['source_url']), 'failures': failures,
            'trackingExcluded': True, 'http_denials_not_retried': True,
            'attempt_ledger': ledger_path.name}
write_json(BASE / f'{SLUG}-oct10-assets.json', manifest)

scopes, sheets = {}, []
for width, height in [(1280, 720), (390, 844)]:
    phases_path = BASE / f'{SLUG}-oct10-official-{width}-phases.json'
    phases = json.loads(phases_path.read_text())
    end, gaps, rasters = 0, [], []
    for phase in phases:
        path = BASE / phase['screenshot']
        with Image.open(path) as image:
            size = list(image.size)
        assert size == [width, height], (path.name, size)
        assert phase['viewport'] == {'width': width, 'height': height}
        assert phase['url'] == references[width]['url']
        y = phase['scrollY']
        if y > end + 1: gaps.append([end, y])
        end = max(end, y + height)
        rasters.append({**fingerprint(path), 'actual_dimensions': size, 'scrollY': y,
                        'observed_at': phase['observed_at'],
                        'broken_visible_images': phase['brokenVisibleImages']})
    page_height = phases[-1]['bodyHeight']
    assert end + 1 >= page_height and not gaps, (SLUG, width, end, page_height, gaps)
    for start in range(0, len(phases), 6):
        group = phases[start:start+6]
        cell_width = 480 if width == 1280 else 260
        tile_height = round(height * cell_width / width)
        sheet = Image.new('RGB', (cell_width*3, (tile_height+32)*((len(group)+2)//3)), '#e7e7e7')
        draw = ImageDraw.Draw(sheet)
        for i, phase in enumerate(group):
            with Image.open(BASE / phase['screenshot']) as image:
                thumb = image.convert('RGB').resize((cell_width, tile_height))
            x, y = i%3*cell_width, i//3*(tile_height+32)
            sheet.paste(thumb, (x, y+32))
            draw.text((x+8, y+8), f'{SLUG} {width} | phase {start+i} | y={phase["scrollY"]}', fill='#111111')
        out = BASE / f'{SLUG}-oct10-source-contact-{width}-{start//6+1}.jpg'
        sheet.save(out, quality=94)
        sheets.append(fingerprint(out))
    scopes[str(width)] = {'viewport': [width, height], 'page_height': page_height,
                          'phase_count': len(phases), 'coverage_gaps': gaps,
                          'covered_to': end, 'actual_raster_dimensions_match': True,
                          'phase_metadata': fingerprint(phases_path),
                          'reference': fingerprint(BASE / f'{SLUG}-oct10-official-{width}-reference.json'),
                          'complete_dom_html_sha256': references[width]['html_sha256'],
                          'browser_annotation_root_present': 'codex-browser-sidebar-comments-root' in ''.join(references[width]['htmlParts']),
                          'cssom_count': len(references[width].get('cssomStylesheets', [])),
                          'cssom_unreadable': [x for x in references[width].get('cssomStylesheets', []) if not x['readable']],
                          'rasters': rasters}
preview_path = BASE / f'{SLUG}.html'
review = {'brand': SLUG, 'source_research_only': True, 'prepared_at': NOW,
          'reference_url': references[1280]['url'],
          'title': references[1280].get('title'),
          'document_language': references[1280].get('document_language'),
          'regional_scope': 'Anonymous public homepage at the recorded final URL; no inferred physical geolocation.',
          'official_consistency_claim': False, 'accepted': False,
          'preview_untouched_sha256': digest(preview_path.read_bytes()) if preview_path.exists() else None,
          'scopes': scopes, 'contact_sheets': sheets,
          'all_source_contact_sheets_inspected_by_owner': False,
          'asset_manifest': f'{SLUG}-oct10-assets.json', 'assets_count': len(assets),
          'asset_failures': failures, 'http_denials_not_retried': True,
          'current_main_headings': [x['text'] for x in json.loads((BASE / f'{SLUG}-oct10-official-1280-phases.json').read_text())[0]['headings']],
          'visual_findings': [], 'limitations': ['Desktop user agent at1280×720 and390×844 responsive viewport; not physical-device verification.',
                                              'Source-only research. No local preview review, Stitch generation or equivalence acceptance is performed by this task.']}
write_json(BASE / f'{SLUG}-oct10-source-review.json', review)
print(json.dumps({'brand': SLUG, 'assets': len(assets), 'asset_bytes': sum(x['bytes'] for x in assets),
                  'failures': failures, 'scopes': {k: {x:v[x] for x in ['phase_count','page_height','coverage_gaps']} for k,v in scopes.items()},
                  'contact_sheets': [x['path'] for x in sheets]}, ensure_ascii=False, indent=2))
