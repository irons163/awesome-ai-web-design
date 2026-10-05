#!/usr/bin/env python3
"""Save independent public HTTP observations for the current official drafts."""
import hashlib
import json
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1] / '.stitch-work/current-official'
SOURCES = {'runwayml': 'https://runway.com/',
           'uber': 'https://www.uber.com/ca/en/'}


def capture(item):
    brand, url = item
    stamp = datetime.now(ZoneInfo('Asia/Taipei')).isoformat()
    metadata = {'requested_url': url, 'observed_at': stamp,
                'method': 'independent_public_http_request'}
    request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0',
                                                  'Accept-Language': 'en-CA,en;q=0.9'})
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            data = response.read()
            metadata.update({'final_url': response.geturl(), 'status': response.status,
                             'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
        (ROOT / (brand + '-source-current.html')).write_bytes(data)
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as error:
        metadata.update({'status': getattr(error, 'code', None), 'error': str(error)})
    (ROOT / (brand + '-source-metadata.json')).write_text(json.dumps(metadata, indent=2) + '\n')
    return {'brand': brand, **metadata}


if __name__ == '__main__':
    ROOT.mkdir(exist_ok=True)
    with ThreadPoolExecutor(max_workers=2) as pool:
        for result in pool.map(capture, SOURCES.items()):
            print(json.dumps(result))
