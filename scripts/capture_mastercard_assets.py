#!/usr/bin/env python3
"""Import byte-exact public Mastercard assets from documented browser bundles."""
import hashlib
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

WORK = Path(__file__).resolve().parents[1] / '.stitch-work/current-official'
BUNDLES = [
    '51794ce0-9760-4055-a574-c227c00dd2dc',
    'b4fa17c5-900e-4375-a5cb-cefe46f491f2',
    '5aafbaa8-86d5-4784-b7d5-63bcfdf7ba7a',
    '92e5eda7-7850-417d-adc5-2b47af0c658c',
    '641291d8-323a-451f-932b-0e1d3b9badfa',
    'c893e46b-8e73-4c38-93a8-02ec9ca84341',
    '3ff6ea49-c253-449f-91ef-6be044b967a8',
]
BUNDLE_ROOT = Path('/var/folders/34/yb_61rwx2kd7pc6f1xd7l80w0000gn/T/browser-use/assets')


def main():
    destination = WORK / 'mastercard-assets'
    destination.mkdir(exist_ok=True)
    provenance = WORK / 'mastercard-asset-provenance.json'
    evidence = json.loads(provenance.read_text()) if provenance.exists() else {'assets': []}
    rows = {r['source_url']: r for r in evidence['assets']}
    hashes = {r['sha256']: r['path'] for r in rows.values()}
    failures = []
    for bundle_id in BUNDLES:
        bundle = json.loads((BUNDLE_ROOT / bundle_id / 'manifest.json').read_text())
        failures.extend(bundle['failures'])
        for asset in bundle['assets']:
            if asset['url'] in rows:
                continue
            original = Path(asset['path'])
            data = original.read_bytes()
            digest = hashlib.sha256(data).hexdigest()
            relative = hashes.get(digest, 'mastercard-assets/' + asset['id'][:12] + original.suffix)
            (WORK / relative).write_bytes(data)
            hashes[digest] = relative
            rows[asset['url']] = {
                'source_url': asset['url'], 'path': relative, 'kind': asset['kind'],
                'content_type': asset['contentType'], 'bytes': len(data), 'sha256': digest,
                'method': 'documented pageAssets bundle; original bytes',
                'observed_at': datetime.now(ZoneInfo('Asia/Taipei')).isoformat(),
            }
    evidence.update(assets=list(rows.values()), capture_failures=failures)
    provenance.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'urls': len(rows), 'files': len(hashes), 'failures': len(failures)}))


if __name__ == '__main__':
    main()
