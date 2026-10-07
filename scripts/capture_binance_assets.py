#!/usr/bin/env python3
"""Import observed public brand originals; preserve source methods and hashes."""
import hashlib
import json
import shutil
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / '.stitch-work/current-official'
DEST = WORK / 'binance-assets'


def main():
    DEST.mkdir(exist_ok=True)
    rows, failures = [], []
    path_by_digest = {}
    for directory in (arg for arg in sys.argv[1:] if not arg.startswith('--public-')):
        bundle = Path(directory)
        manifest = json.loads((bundle / 'manifest.json').read_text())
        failures.extend(manifest.get('failures', []))
        for asset in manifest['assets']:
            source = Path(asset['path'])
            data = source.read_bytes()
            digest = hashlib.sha256(data).hexdigest()
            suffix = { 'image/webp': '.webp', 'image/png': '.png',
                       'image/jpeg': '.jpg', 'image/svg+xml': '.svg',
                       'text/css': '.css', 'font/woff2': '.woff2' }.get(
                           asset.get('contentType'), source.suffix)
            target = path_by_digest.setdefault(digest, DEST / (hashlib.sha256(asset['url'].encode()).hexdigest()[:12] + suffix))
            if not target.exists():
                shutil.copyfile(source, target)
            assert hashlib.sha256(target.read_bytes()).hexdigest() == digest
            if not any(r['source_url'] == asset['url'] for r in rows):
                rows.append({'source_url': asset['url'], 'path': str(target.relative_to(WORK)),
                             'kind': asset['kind'], 'content_type': asset.get('contentType'),
                             'sha256': digest, 'bytes': len(data), 'bundle': bundle.name})
    font_urls = ['https://bin.bnbstatic.com/static/fonts/bn/v2/BinanceNova-' + name + '.woff2' for name in ('Regular', 'Medium', 'SemiBold')]
    if '--public-fonts' in sys.argv:
        # The native fetch reported a TypeError, not an access denial. A normal
        # unauthenticated HTTPS request successfully returned the original font.
        for url in font_urls:
            target = DEST / urlsplit(url).path.rsplit('/', 1)[-1]
            if not target.exists():
                with urllib.request.urlopen(url, timeout=15) as response:
                    if response.status != 200:
                        raise ValueError('Unsuccessful public font request: ' + url)
                    data = response.read()
                if data[:4] != b'wOF2':
                    raise ValueError('Public response is not WOFF2: ' + url)
                target.write_bytes(data)
            data = target.read_bytes()
            assert data[:4] == b'wOF2'
            rows.append({'source_url': url, 'path': str(target.relative_to(WORK)),
                         'kind': 'font', 'content_type': 'font/woff2',
                         'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data),
                         'method': 'Standard unauthenticated HTTPS, HTTP 200, original WOFF2 signature verified.',
                         'retrieved_at': datetime.fromtimestamp(target.stat().st_mtime, timezone.utc).isoformat()})
            path_by_digest[rows[-1]['sha256']] = target
    if '--public-styles' in sys.argv:
        interactions = json.loads((WORK / 'binance-interactions-browser-export.json').read_text())
        captured_urls = {row['source_url'] for row in rows}
        for entry in interactions['stylesheet_order']:
            url = entry.get('href')
            if not url or url in captured_urls:
                continue
            if urlsplit(url).netloc not in ('bin.bnbstatic.com', 'public.bnbstatic.com') or not urlsplit(url).path.endswith('.css'):
                raise ValueError('Unrecognized observed public stylesheet: ' + url)
            target = DEST / (hashlib.sha256(url.encode()).hexdigest()[:12] + '.css')
            if not target.exists():
                with urllib.request.urlopen(url, timeout=15) as response:
                    if response.status != 200 or 'css' not in response.headers.get('content-type', ''):
                        raise ValueError('Unsuccessful public stylesheet request: ' + url)
                    target.write_bytes(response.read())
            data = target.read_bytes()
            rows.append({'source_url': url, 'path': str(target.relative_to(WORK)),
                         'kind': 'stylesheet', 'content_type': 'text/css',
                         'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data),
                         'method': 'Observed public stylesheet link; standard unauthenticated HTTPS, HTTP 200 with CSS content type.',
                         'retrieved_at': datetime.fromtimestamp(target.stat().st_mtime, timezone.utc).isoformat()})
            path_by_digest[rows[-1]['sha256']] = target
    if '--public-images' in sys.argv:
        references = [json.loads((WORK / f'binance-{mode}-browser-export.json').read_text()) for mode in ('desktop', 'mobile')]
        interactions = json.loads((WORK / 'binance-interactions-browser-export.json').read_text())
        images = [image for reference in references for image in reference['images']]
        images.extend(interactions['download_desktop']['images'])
        images.extend(image for states in interactions['market_states'].values() for state in states.values() for image in state['images'])
        captured_urls = {row['source_url'] for row in rows}
        urls = sorted({image['src'] for image in images if image.get('loaded') and image['src'].startswith('https://') and image['src'] not in captured_urls})
        for url in urls:
            if urlsplit(url).netloc != 'bin.bnbstatic.com' or not urlsplit(url).path.endswith('.png'):
                raise ValueError('Unrecognized observed public PNG: ' + url)
            target = DEST / (hashlib.sha256(url.encode()).hexdigest()[:12] + '.png')
            if not target.exists():
                with urllib.request.urlopen(url, timeout=15) as response:
                    if response.status != 200:
                        raise ValueError('Unsuccessful public image request: ' + url)
                    data = response.read()
                if data[:8] != b'\x89PNG\r\n\x1a\n':
                    raise ValueError('Public response is not PNG: ' + url)
                target.write_bytes(data)
            data = target.read_bytes()
            assert data[:8] == b'\x89PNG\r\n\x1a\n'
            rows.append({'source_url': url, 'path': str(target.relative_to(WORK)),
                         'kind': 'image', 'content_type': 'image/png',
                         'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data),
                         'method': 'Observed loaded public DOM image; standard unauthenticated HTTPS, HTTP 200, original PNG signature verified.',
                         'retrieved_at': datetime.fromtimestamp(target.stat().st_mtime, timezone.utc).isoformat()})
            path_by_digest[rows[-1]['sha256']] = target
    provenance = {'observed_at': '2026-10-07', 'reference_url': 'https://www.binance.com/en',
                  'method': 'Original bytes from supported pageAssets bundles, supplemented by ordinary unauthenticated HTTP 200 downloads of URLs observed in the public DOM and font declarations. Each supplemental resource records its method. No runtime stores or application scripts are used.',
                  'assets': rows, 'capture_failures': failures,
                  'remote_fonts': [url for url in font_urls if not any(row['source_url'] == url for row in rows)],
                  'remote_font_note': 'Native font fetch TypeError is retained above. Original regular/medium/semibold fonts were retrieved by ordinary unauthenticated HTTP 200 requests; no substitute fonts were used.' if '--public-fonts' in sys.argv else 'Native font download failed; observed original URLs remain external.'}
    (WORK / 'binance-asset-provenance.json').write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'asset_records': len(rows), 'unique_files': len(path_by_digest), 'bytes': sum(p.stat().st_size for p in set(path_by_digest.values())), 'failed_records': len(failures)}))


if __name__ == '__main__':
    main()
