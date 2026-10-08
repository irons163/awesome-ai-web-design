#!/usr/bin/env python3
"""Import unchanged Dell public resources and record each observed source."""
import hashlib
import json
import shutil
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / '.stitch-work/current-official'
DEST = WORK / 'dell-1996-assets'
HOSTS = {'i.dell.com', 'www.dell.com', 'afcs.dellcdn.com'}
SUFFIXES = {'image/png': '.png', 'image/jpeg': '.jpg', 'image/webp': '.webp',
            'image/svg+xml': '.svg', 'text/css': '.css', 'font/woff2': '.woff2'}


def main():
    DEST.mkdir(exist_ok=True)
    manifest = json.loads((Path(sys.argv[1]) / 'manifest.json').read_text())
    (WORK / 'dell-1996-native-asset-bundle.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    rows, files = [], {}
    for asset in manifest['assets']:
        data = Path(asset['path']).read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        suffix = SUFFIXES.get(asset.get('contentType'), Path(asset['path']).suffix)
        path = files.setdefault(digest, DEST / (hashlib.sha256(asset['url'].encode()).hexdigest()[:12] + suffix))
        if not path.exists():
            shutil.copyfile(asset['path'], path)
        assert hashlib.sha256(path.read_bytes()).hexdigest() == digest
        rows.append({'source_url': asset['url'], 'path': str(path.relative_to(WORK)),
                     'kind': asset['kind'], 'content_type': asset.get('contentType'),
                     'sha256': digest, 'bytes': len(data), 'method': 'Documented pageAssets bundle; original bytes unchanged.'})
    references = [json.loads((WORK / f'dell-1996-{m}-browser-export.json').read_text()) for m in ('desktop', 'mobile')]
    interactions = json.loads((WORK / 'dell-1996-interactions-browser-export.json').read_text())
    images = [image for reference in references for image in reference['images']]
    images.extend(interactions['products_loaded_desktop']['images'])
    known = {row['source_url'] for row in rows}
    urls = sorted({image['src'] for image in images if image.get('loaded') and image['src'].startswith('https://') and image['src'] not in known})

    def download(url):
        if urlsplit(url).hostname not in HOSTS:
            raise ValueError('Unrecognized observed image host: ' + url)
        with urllib.request.urlopen(url, timeout=20) as response:
            content_type = response.headers.get_content_type()
            if response.status != 200 or not content_type.startswith('image/'):
                raise ValueError('Public resource unavailable: ' + url)
            data = response.read()
        valid = data.startswith((b'\x89PNG\r\n\x1a\n', b'\xff\xd8\xff')) or (data[:4] == b'RIFF' and data[8:12] == b'WEBP') or b'<svg' in data[:600]
        if not valid:
            raise ValueError('Unexpected original image signature: ' + url)
        return url, data, content_type

    failures = list(manifest.get('failures', []))
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = [(url, pool.submit(download, url)) for url in urls]
        for url, future in futures:
            try:
                _, data, content_type = future.result()
            except Exception as error:
                failures.append({'url': url, 'reason': str(error), 'method': 'Ordinary unauthenticated request of an already observed, loaded public image. No access-denial fallback.'})
                continue
            digest = hashlib.sha256(data).hexdigest()
            target = files.setdefault(digest, DEST / (hashlib.sha256(url.encode()).hexdigest()[:12] + SUFFIXES[content_type]))
            if not target.exists():
                target.write_bytes(data)
            assert hashlib.sha256(target.read_bytes()).hexdigest() == digest
            rows.append({'source_url': url, 'path': str(target.relative_to(WORK)), 'kind': 'image',
                         'content_type': content_type, 'sha256': digest, 'bytes': len(data),
                         'method': 'Observed loaded public DOM image; ordinary unauthenticated HTTPS returned HTTP 200; original signature verified.',
                         'retrieved_at': datetime.now(timezone.utc).isoformat()})
    result = {'reference_url': 'https://www.dell.com/zh-tw', 'observed_at': '2026-10-08',
              'method': 'Documented pageAssets bundle and original HTTP 200 resources already observed in public rendered DOM. No runtime stores, tracking scripts, account data or generated replacements.',
              'assets': rows, 'capture_failures': failures}
    (WORK / 'dell-1996-asset-provenance.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'records': len(rows), 'files': len(files), 'bytes': sum(p.stat().st_size for p in set(files.values())), 'failures': len(failures)}))


if __name__ == '__main__':
    main()
