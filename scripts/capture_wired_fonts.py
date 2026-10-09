#!/usr/bin/env python3
"""Retain unchanged resources declared in the dated public browser capture."""
import concurrent.futures
import hashlib
import json
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote, urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / '.stitch-work/current-official'
REFERENCE = BASE / 'wired-asset-provenance.json'
ASSETS = BASE / 'wired-assets'


def main():
    reference = json.loads(REFERENCE.read_text())
    sources = {a['source_url']: a['kind'] for a in reference['assets'] if a['kind'] == 'font' and a.get('error') == 'InvalidURL'}
    ASSETS.mkdir(exist_ok=True)

    def download(item):
        url, kind = item
        record = {'source_url': url, 'kind': kind, 'observed_at': datetime.now(timezone.utc).isoformat()}
        accept = 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8' if kind == 'image' else '*/*'
        request = urllib.request.Request(quote(url, safe=':/?&=#%'), headers={'User-Agent': 'Mozilla/5.0', 'Accept': accept})
        try:
            with urllib.request.urlopen(request, timeout=25) as response:
                data = response.read()
                record.update(http_status=response.status, content_type=response.headers.get('Content-Type'), bytes=len(data))
            if record['http_status'] != 200 or not data:
                raise ValueError('Expected a complete public HTTP200 response')
            mime = (record['content_type'] or '').split(';')[0]
            if kind == 'stylesheet' and mime != 'text/css':
                raise ValueError('Response is not a public stylesheet')
            if kind == 'font' and not (data[:4] in (b'wOF2', b'wOFF', b'OTTO', b'\x00\x01\x00\x00')):
                raise ValueError('Response is not an original font')
            if kind == 'image' and not mime.startswith('image/'):
                raise ValueError('Response is not an image')
            suffix = { 'image/avif': '.avif', 'image/webp': '.webp', 'image/jpeg': '.jpg', 'image/png': '.png', 'image/svg+xml': '.svg', 'image/gif': '.gif', 'text/css': '.css' }.get(mime)
            suffix = suffix or Path(urlsplit(url).path).suffix or '.bin'
            target = ASSETS / (hashlib.sha256(url.encode()).hexdigest()[:16] + suffix)
            if target.exists() and target.read_bytes() != data:
                raise ValueError('Retained original differs; do not overwrite')
            target.write_bytes(data)
            record.update(path=str(target.relative_to(BASE)), sha256=hashlib.sha256(data).hexdigest(), retained=True)
        except Exception as error:
            record.update(retained=False, error=type(error).__name__)
        return record

    records = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        for future in concurrent.futures.as_completed([pool.submit(download, item) for item in sources.items()]):
            records.append(future.result())
            if len(records) % 40 == 0:
                print(json.dumps({'checked': len(records), 'total': len(sources), 'retained': sum(r['retained'] for r in records)}), flush=True)
    result = {'reference_url': reference['reference_url'], 'reference_observed_at': reference['reference_observed_at'], 'method': 'Ordinary unauthenticated HTTP GET of public stylesheet and font declarations and observed image currentSrc/src URLs; complete original bytes, no resizing or recompression.', 'responsive_scope': 'Responsive candidates remain the observed CDN srcset declarations; this capture does not claim to download or verify every possible candidate.', 'assets': sorted(records, key=lambda r: r['source_url'])}
    output = BASE / 'wired-font-repair-provenance.json'
    if output.exists():
        raise RuntimeError('Retain existing provenance; do not overwrite')
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'checked': len(records), 'retained': sum(r['retained'] for r in records), 'bytes': sum(r.get('bytes', 0) for r in records if r['retained']), 'provenance': str(output)}), flush=True)


if __name__ == '__main__':
    main()
