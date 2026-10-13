#!/usr/bin/env python3
"""Serve the collection locally without package installation."""
import argparse
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlsplit

parser = argparse.ArgumentParser()
parser.add_argument('--port', type=int, default=4173)
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]


class PreviewHandler(SimpleHTTPRequestHandler):
    def redirect_hosted_media(self):
        request_path = urlsplit(self.path).path
        rules = root / 'dist/_redirects'
        if request_path.startswith('/dist/') and rules.is_file():
            for line in rules.read_text().splitlines():
                parts = line.split()
                if len(parts) == 3 and parts[0] == request_path[len('/dist'):] and parts[2] == '302':
                    self.send_response(302)
                    self.send_header('Location', parts[1])
                    self.end_headers()
                    return True
        return False

    def do_GET(self):
        if not self.redirect_hosted_media():
            super().do_GET()

    def do_HEAD(self):
        if not self.redirect_hosted_media():
            super().do_HEAD()

try:
    server = ThreadingHTTPServer(('127.0.0.1', args.port), partial(PreviewHandler, directory=str(root)))
except OSError as error:
    parser.exit(1, f'無法使用連接埠 {args.port}：{error}。請加上 --port 4178 選擇其他連接埠。\n')
print(f'Awesome AI Web Design → http://127.0.0.1:{args.port}', flush=True)
try:
    server.serve_forever()
except KeyboardInterrupt:
    server.server_close()
