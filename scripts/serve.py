#!/usr/bin/env python3
"""Serve the collection locally without package installation."""
import argparse
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--port', type=int, default=4173)
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
try:
    server = ThreadingHTTPServer(('127.0.0.1', args.port), partial(SimpleHTTPRequestHandler, directory=str(root)))
except OSError as error:
    parser.exit(1, f'無法使用連接埠 {args.port}：{error}。請加上 --port 4178 選擇其他連接埠。\n')
print(f'Awesome AI Web Design → http://127.0.0.1:{args.port}', flush=True)
try:
    server.serve_forever()
except KeyboardInterrupt:
    server.server_close()
