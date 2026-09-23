"""Save public Figma assets from the committed source-URL manifest."""

import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "figma-assets"
OUTPUT.mkdir(exist_ok=True)
assets = json.loads((ROOT / "figma-asset-provenance.json").read_text())
for filename, url in assets.items():
    if not url.startswith(("https://i.vimeocdn.com/", "https://www.figma.com/", "https://cdn.sanity.io/")):
        raise ValueError(f"Unrecognized public asset source: {url}")
    target = OUTPUT / filename
    if not target.exists():
        request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(request, timeout=45) as response:
            content = response.read()
        if filename.endswith(".svg"):
            content = b"\n".join(line.rstrip() for line in content.splitlines()) + b"\n"
        target.write_bytes(content)
        print(filename, len(content))
