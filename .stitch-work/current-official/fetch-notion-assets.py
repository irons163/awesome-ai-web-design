"""Save public Notion homepage assets observed in the browser reference."""

import json
import subprocess
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "notion-assets"
OUTPUT.mkdir(exist_ok=True)
reference = json.loads((ROOT / "notion-browser-reference.json").read_text())
inventory = json.loads((ROOT / "notion-assets-browser-reference.json").read_text())

by_name = {item["name"]: item["url"] for item in inventory["assets"] if item.get("url")}
images = reference["assets"]["images"]
downloads = {
    "hero.mp4": reference["assets"]["heroVideo"],
    "font-regular.woff2": by_name["NotionInter-Regular.woff2"],
    "font-medium.woff2": by_name["NotionInter-Medium.woff2"],
    "font-semibold.woff2": by_name["NotionInter-SemiBold.woff2"],
    "font-bold.woff2": by_name["NotionInter-Bold.woff2"],
    "logo-openai.svg": by_name["OpenAI.svg"],
    "logo-a24.svg": by_name["a24-mono.svg"],
    "logo-figma.svg": by_name["Figma_Wordmark__Black_.svg"],
    "logo-fedex.svg": by_name["FedEx.svg"],
    "logo-ramp.svg": by_name["Ramp.svg"],
    "logo-cursor.svg": by_name["cursor-logo-mono.svg"],
    "logo-faire.svg": by_name["Faire_logo_-_black.svg"],
    "logo-substack.svg": by_name["substack-wordmark-mono.svg"],
    "logo-nvidia.svg": by_name["Nvidia.svg"],
    "logo-toyota.svg": by_name["toyota-black.svg"],
    "feature-capture.jpg": images[1]["src"],
    "feature-find.png": images[2]["src"],
    "feature-find-overlay.png": images[3]["src"],
    "feature-automate-front.jpg": images[4]["src"],
    "feature-automate-back.png": images[5]["src"],
    "story-cursor.png": images[6]["src"],
    "story-faire.png": images[7]["src"],
    "story-ramp.png": images[8]["src"],
    "usecase-mailbox.png": "https://www.notion.com/_next/image?url=%2Ffront-static%2Fagents%2Fmailbox.png&w=96&q=75",
    "usecase-rock.png": "https://www.notion.com/_next/image?url=%2Ffront-static%2Fagents%2Frock.png&w=96&q=75",
    "usecase-sign.png": "https://www.notion.com/_next/image?url=%2Ffront-static%2Fagents%2Fsign.png&w=96&q=75",
    "usecase-apple.png": "https://www.notion.com/_next/image?url=%2Ffront-static%2Fagents%2Fapple.png&w=96&q=75",
    "usecase-light-bulb.png": "https://www.notion.com/_next/image?url=%2Ffront-static%2Fagents%2Flight_bulb.png&w=96&q=75",
    "usecase-worker.png": "https://www.notion.com/_next/image?url=%2Ffront-static%2Fpages%2Fhome%2Fjune%2Fworker.png&w=48&q=75",
}

for name, url in downloads.items():
    target = OUTPUT / name
    if target.exists() and target.stat().st_size:
        print(name, "already saved", target.stat().st_size)
        continue
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=45) as response:
        data = response.read()
    target.write_bytes(data)
    print(name, len(data))

poster = OUTPUT / "hero-poster.jpg"
if not poster.exists():
    subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-ss", "0.5", "-i", str(OUTPUT / "hero.mp4"), "-frames:v", "1", "-q:v", "2", str(poster)],
        check=True,
    )
    print(poster.name, poster.stat().st_size)

(ROOT / "notion-asset-provenance.json").write_text(json.dumps(downloads, indent=2) + "\n")
