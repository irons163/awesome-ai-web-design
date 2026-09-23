"""Local, short-lived form to persist browser-observed public reference data."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs
import json
import re

ROOT = Path(__file__).parent
FORM = b'''<!doctype html><meta charset="utf-8"><title>Reference capture</title>
<form method="post" action="/capture"><label>Slug <input name="slug"></label>
<label>Reference JSON <textarea name="payload" rows="20" cols="100"></textarea></label>
<button type="submit">Save reference</button></form>'''


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != '/':
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(FORM)

    def do_POST(self):
        if self.path != '/capture':
            self.send_error(404)
            return
        length = int(self.headers.get('Content-Length', '0'))
        if not 0 < length < 5_000_000:
            self.send_error(413)
            return
        form = parse_qs(self.rfile.read(length).decode('utf-8'))
        slug = form.get('slug', [''])[0]
        payload = form.get('payload', [''])[0]
        if not re.fullmatch(r'[a-z0-9.-]+', slug):
            self.send_error(400)
            return
        try:
            data = json.loads(payload)
        except json.JSONDecodeError:
            self.send_error(400)
            return
        (ROOT / f'{slug}-browser-reference.json').write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + '\n'
        )
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(f'Saved {slug}'.encode())


if __name__ == '__main__':
    server = ThreadingHTTPServer(('127.0.0.1', 4181), Handler)
    print('Reference capture form → http://127.0.0.1:4181/', flush=True)
    server.serve_forever()
