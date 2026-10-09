#!/usr/bin/env python3
"""Retain only public inline CSS from an unauthenticated WIRED response."""
import hashlib
import json
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

WORK = Path(__file__).resolve().parents[1] / '.stitch-work/current-official'


class Styles(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.records = []
        self.current = None

    def handle_starttag(self, tag, attrs):
        if tag == 'style':
            self.current = {'attributes': [(k, v) for k, v in attrs if k in ('id', 'data-styled', 'data-styled-version', 'data-slug', 'data-revision', 'type')], 'text': ''}

    def handle_data(self, data):
        if self.current is not None:
            self.current['text'] += data

    def handle_endtag(self, tag):
        if tag == 'style' and self.current is not None:
            self.records.append(self.current)
            self.current = None


def main():
    output = WORK / 'wired-original-server-styles.json'
    if output.exists():
        raise ValueError('Preserve the original dated CSS capture.')
    url = 'https://www.wired.com/'
    with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=40) as response:
        if response.status != 200 or 'text/html' not in response.headers.get('Content-Type', ''):
            raise ValueError('Expected a complete public HTML response.')
        parser = Styles()
        parser.feed(response.read().decode('utf-8'))
    for record in parser.records:
        data = record['text'].encode('utf-8')
        record.update(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
        record['cssParts'] = [record['text'][i:i+100000] for i in range(0, len(record['text']), 100000)]
        del record['text']
    result = {'source_url': url, 'observed_at': datetime.now(timezone.utc).isoformat(), 'method': 'Unauthenticated public HTTP GET; only original inline style tag text is retained. No scripts, application state, entered values, nonce or account data are retained.', 'styles': parser.records}
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'styles': len(parser.records), 'bytes': sum(s['bytes'] for s in parser.records), 'has_observed_navigation_selector': any('.gGwmsI{' in ''.join(s['cssParts']) for s in parser.records)}), flush=True)


if __name__ == '__main__':
    main()
