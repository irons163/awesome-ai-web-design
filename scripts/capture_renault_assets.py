#!/usr/bin/env python3
"""Preserve original public Renault styles, fonts and responsive media evidence."""
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote
from zoneinfo import ZoneInfo
from official_html_tree import Tree

ROOT = Path(__file__).resolve().parents[1] / '.stitch-work/current-official'
ORIGIN = 'https://www.renaultgroup.com/'
ALLOWED = {'www.renaultgroup.com', 'assets.renaultgroup.com'}


def import_browser_manifest(manifest):
    """Import a documented pageAssets bundle without re-encoding its images."""
    provenance = ROOT / 'renault-asset-provenance.json'
    evidence = json.loads(provenance.read_text())
    records = {row['source_url']: row for row in evidence['assets']}
    bundle = json.loads(Path(manifest).read_text())
    for asset in bundle['assets']:
        if urlsplit(asset['url']).hostname not in ALLOWED:
            raise ValueError('Unexpected bundled resource host')
        original = Path(asset['path'])
        data = original.read_bytes()
        suffix = '.webp' if data[:4] == b'RIFF' and data[8:12] == b'WEBP' else original.suffix
        # A browser encodes a Unicode URL itself. Literal percent escapes in a
        # filesystem basename would otherwise be decoded into a missing file.
        name = 'browser-' + asset['id'] + '-' + Path(unquote(asset['name'])).stem + suffix
        target = ROOT / 'renault-assets' / name
        shutil.copyfile(original, target)
        previous = records.get(asset['url'])
        if previous and previous.get('path') != str(target.relative_to(ROOT)):
            previous_path = ROOT / previous['path']
            if previous_path.exists() and previous_path.name.startswith('browser-'):
                previous_path.unlink()
        records[asset['url']] = {
            'source_url': asset['url'], 'path': str(target.relative_to(ROOT)),
            'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
            'content_type': asset.get('contentType'),
            'method': 'documented pageAssets bundle; observed official page resource; original bytes',
            'observed_at': datetime.now(ZoneInfo('Asia/Taipei')).isoformat()}
    evidence['assets'] = list(records.values())
    provenance.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'imported': len(bundle['assets']), 'assets': len(records),
                      'bytes': sum(row['bytes'] for row in records.values())}))


def capture(url):
    if urlsplit(url).hostname not in ALLOWED:
        raise ValueError('Unexpected source resource: ' + url)
    basename = unquote(Path(urlsplit(url).path).name)
    if not Path(basename).suffix:
        basename += '.asset'
    name = hashlib.sha256(url.encode()).hexdigest()[:10] + '-' + basename
    row = {'source_url': url, 'observed_at': datetime.now(ZoneInfo('Asia/Taipei')).isoformat(),
           'method': 'ordinary public HTTP request; original bytes'}
    with tempfile.TemporaryDirectory(prefix='renault-asset-') as folder:
        file = Path(folder) / 'resource'
        response = subprocess.run(['curl', '--silent', '--show-error', '--location', '--max-time', '45',
                                   '--output', str(file), '--write-out', '%{http_code}', url], capture_output=True)
        row['status'] = int(response.stdout or '0')
        if response.returncode or row['status'] != 200:
            row['error'] = response.stderr.decode(errors='replace') or 'HTTP ' + str(row['status'])
            return None, row
        data = file.read_bytes()
        if not data or data.lstrip().lower().startswith((b'<!doctype html', b'<html')):
            row['error'] = 'Empty or unexpected HTML resource'
            return None, row
    path = ROOT / 'renault-assets' / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    row.update(path=str(path.relative_to(ROOT)), bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
    return data, row


def main():
    source = Tree((ROOT / 'renault-source-current.html').read_text())
    styles = [urljoin(ORIGIN, n.attrs['href']) for n in source.root.walk()
              if n.tag == 'link' and n.attrs.get('rel') == 'stylesheet']
    records, failures, extras = [], [], set()
    for url in dict.fromkeys(styles):
        data, row = capture(url)
        if data is None:
            failures.append(row)
            continue
        records.append(row)
        for value in re.findall(r'url\(([^)]+)\)', data.decode()):
            value = value.strip(' \t\r\n\'"')
            if value.startswith(('data:', '#')):
                continue
            absolute = urljoin(url, value)
            if urlsplit(absolute).hostname in ALLOWED:
                extras.add(absolute)
    images = []
    for n in source.root.walk():
        if n.tag == 'img':
            value = n.attrs.get('src', '')
            if urlsplit(value).hostname in ALLOWED:
                extras.add(value)
                images.append({'src': value, 'srcset': n.attrs.get('srcset'), 'alt': n.attrs.get('alt', '')})
    with ThreadPoolExecutor(max_workers=6) as pool:
        for data, row in pool.map(capture, sorted(extras)):
            (records if data is not None else failures).append(row)
    (ROOT / 'renault-asset-provenance.json').write_text(json.dumps({
        'assets': records, 'capture_failures': failures, 'images': images}, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'assets': len(records), 'bytes': sum(r['bytes'] for r in records),
                      'failures': failures, 'fonts': [r['source_url'] for r in records
                      if urlsplit(r['source_url']).path.endswith(('.woff', '.woff2', '.ttf'))]}))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        for manifest in sys.argv[1:]:
            import_browser_manifest(manifest)
    else:
        main()
