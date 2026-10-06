#!/usr/bin/env python3
"""Preserve public resources from the dated, successful Lamborghini response."""
import hashlib
import json
import re
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1] / '.stitch-work/current-official'
ORIGIN = 'https://www.lamborghini.com'


class Source(HTMLParser):
    def __init__(self):
        super().__init__()
        self.json_parts = []
        self.in_json = False
        self.stylesheets = []

    def handle_starttag(self, tag, attributes):
        a = dict(attributes)
        if tag == 'script' and a.get('id') == '__NEXT_DATA__':
            self.in_json = True
        if tag == 'link' and a.get('rel') == 'stylesheet':
            self.stylesheets.append(urljoin(ORIGIN, a['href']))

    def handle_endtag(self, tag):
        if tag == 'script':
            self.in_json = False

    def handle_data(self, value):
        if self.in_json:
            self.json_parts.append(value)


def capture(url):
    name = hashlib.sha256(url.encode()).hexdigest()[:10] + '-' + unquote(Path(urlsplit(url).path).name)
    path = ROOT / 'lamborghini-assets' / name
    row = {'source_url': url, 'observed_at': datetime.now(ZoneInfo('Asia/Taipei')).isoformat(),
           'method': 'ordinary public resource request; original bytes'}
    with tempfile.TemporaryDirectory(prefix='lambo-assets-') as folder:
        temporary = Path(folder) / 'asset'
        r = subprocess.run(['curl', '--silent', '--show-error', '--location', '--max-time', '45',
                            '--output', str(temporary), '--write-out', '%{http_code}', url], capture_output=True)
        row['status'] = int(r.stdout or '0')
        if r.returncode or row['status'] != 200:
            row['error'] = r.stderr.decode(errors='replace').strip() or 'HTTP ' + str(row['status'])
            return False, row
        data = temporary.read_bytes()
        if not data or data.lstrip().lower().startswith((b'<!doctype html', b'<html')):
            row['error'] = 'Empty or unexpected HTML resource'
            return False, row
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        row.update(path=str(path.relative_to(ROOT)), bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
        return True, row


def main():
    source = (ROOT / 'lamborghini-source-current.html').read_text()
    parser = Source()
    parser.feed(source)
    public = json.loads(''.join(parser.json_parts))['props']['pageProps']['data']
    # These are public CMS fields in the saved HTTP response, not a browser-store read.
    content = {'header': public['commonElements']['header'], 'footer': public['commonElements']['footer'],
               'elements': public['elements'], 'reference_date': '2026-10-06'}
    (ROOT / 'lamborghini-content-reference.json').write_text(json.dumps(content, ensure_ascii=False, indent=2) + '\n')
    urls = set(parser.stylesheets)
    urls.add(ORIGIN + '/fonts/2024/lambotype-web-variable/Lambotype-Variable.woff')
    urls.add(ORIGIN + '/sites/it-en/files/DAM/lamborghini/logos/2024/03_26/logo_header_01.svg')
    urls.add(ORIGIN + '/sites/it-en/files/DAM/lamborghini/EmpCO/badge/GARAN_Label_nested_display_1.png')

    def walk(value):
        if isinstance(value, dict):
            for key, item in value.items():
                if key == 'url' and isinstance(item, str) and re.search(r'\.(?:svg|png|jpg|jpeg|webp)(?:\?|$)', item):
                    urls.add(urljoin(ORIGIN, item))
                else:
                    walk(item)
        elif isinstance(value, list):
            for item in value:
                walk(item)

    # Capture gallery, dealer and chooser artwork. Full-res raster originals
    # remain source evidence; the hosted page streams them from their public origin.
    walk(content['elements'][:5])
    urls.update([
        'https://medialamborghini-meride-tv.akamaized.net/meride/lamborghini/video/images/folder1/2846/1786627119hero.jpg',
        'https://medialamborghini-meride-tv.akamaized.net/meride/lamborghini/video/images/folder1/2847/1786627187hero_mobile.jpg',
        'https://videolamborghini-meride-tv.akamaized.net/video/folder2/1786627119hero_lamborghini/1786627119hero_lamborghini.m3u8',
        'https://videolamborghini-meride-tv.akamaized.net/video/folder2/1786627187hero_mobile_lamborghini/1786627187hero_mobile_lamborghini.m3u8',
    ])
    record = {'assets': [], 'capture_failures': [], 'full_resolution_rasters_stream_from_original_origin': True}
    with ThreadPoolExecutor(max_workers=4) as pool:
        for success, row in pool.map(capture, sorted(urls)):
            record['assets' if success else 'capture_failures'].append(row)
    (ROOT / 'lamborghini-asset-provenance.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'captured': len(record['assets']), 'bytes': sum(r['bytes'] for r in record['assets']),
                      'failures': record['capture_failures']}), flush=True)


if __name__ == '__main__':
    main()
