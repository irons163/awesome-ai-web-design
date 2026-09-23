"""Download observed public Framer media listed in the URL manifest."""

import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "framer-assets"
OUT.mkdir(exist_ok=True)
manifest = json.loads((ROOT / "framer-asset-provenance.json").read_text())
for filename, url in manifest.items():
    if not url.startswith(("https://framerusercontent.com/images/", "https://framerusercontent.com/assets/")):
        raise ValueError(f"Unexpected Framer media host: {url}")
    dest = OUT / filename
    if dest.exists():
        continue
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        body = response.read()
    dest.write_bytes(body)
    print(filename, len(body))
