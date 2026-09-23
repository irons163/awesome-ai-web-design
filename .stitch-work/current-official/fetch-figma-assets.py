"""Save the public Figma hero poster observed in its Vimeo player."""

import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "figma-assets"
OUTPUT.mkdir(exist_ok=True)
assets = {
    "hero-poster.jpg": "https://i.vimeocdn.com/video/2171666991-f73276c6d7754f194518ebb0593fcfe2e8eee465dc285149c2e12adcf2aedb46-d?mw=1200&mh=1450&q=70",
    "site-font.woff2": "https://www.figma.com/_netlify/_next/static/media/7c42ed55a7834032-s.p.woff2",
}
for filename, url in assets.items():
    target = OUTPUT / filename
    if not target.exists():
        request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(request, timeout=45) as response:
            content = response.read()
        target.write_bytes(content)
        print(filename, len(content))
(ROOT / "figma-asset-provenance.json").write_text(json.dumps(assets, indent=2) + "\n")
