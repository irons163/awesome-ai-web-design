"""One exact-URL retry for transport timeouts; never retry denials/404."""
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlsplit
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json

WORK = Path(__file__).resolve().parents[1] / '.stitch-work/current-official'
for brand in ['clickhouse', 'mintlify', 'miro']:
    path = WORK / f'{brand}-oct10-assets.json'
    manifest = json.loads(path.read_text())
    targets = [a for a in manifest['failures'] if 'timed out' in a['error'].lower()]
    attempts = []

    def get(item):
        url = item['source_url']
        record = {'source_url': url, 'previous_error': item['error'],
                  'method': 'Single exact observed URL unauthenticated HTTPS transport retry; no origin/credential changes'}
        try:
            with urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'image/webp,image/avif,image/*,*/*;q=0.8'}), timeout=45) as response:
                data = response.read()
                content_type = response.headers.get('Content-Type', '')
            digest = hashlib.sha256(data).hexdigest()
            suffix = '.webp' if data.startswith(b'RIFF') and data[8:12] == b'WEBP' else '.png' if data.startswith(b'\x89PNG') else '.jpg' if data.startswith(b'\xff\xd8') else '.svg' if b'<svg' in data[:1000] else Path(urlsplit(url).path).suffix
            output = WORK / f'{brand}-assets/oct10/{digest[:20]}{suffix}'
            output.write_bytes(data)
            record['asset'] = {'source_url': url, 'path': str(output.relative_to(WORK)),
                'bytes': len(data), 'sha256': digest, 'contentType': content_type,
                'acquisition': 'Exact observed public asset GET, one retry after transport timeout'}
            record['success'] = True
        except Exception as error:
            record.update(success=False, error=str(error))
        return record

    with ThreadPoolExecutor(max_workers=4) as pool:
        attempts = list(pool.map(get, targets))
    recovered = {a['source_url']: a['asset'] for a in attempts if a['success']}
    manifest['assets'] = sorted(manifest['assets'] + list(recovered.values()), key=lambda a: a['source_url'])
    manifest['failures'] = [a for a in manifest['failures'] if a['source_url'] not in recovered]
    manifest['transport_retry_record'] = f'{brand}-oct10-asset-transport-retry.json'
    path.write_text(json.dumps(manifest, indent=2) + '\n')
    (WORK / f'{brand}-oct10-asset-transport-retry.json').write_text(json.dumps({
        'brand': brand, 'accepted': False, 'attempts': attempts,
        'retry_limit': 'One exact-URL retry of transport timeouts only. HTTP403/404 or explicit denials were not retried.',
    }, indent=2) + '\n')
    print(json.dumps({'brand': brand, 'attempts': len(attempts), 'recovered': len(recovered), 'remaining_failures': manifest['failures']}), flush=True)
