# coding: utf-8
"""Build a source-backed Vercel draft from the native Stitch screen and live page observations.

The native vercel-stitch.html export is kept unchanged. This script removes its
invented product copy and substitutes observed public media and section text.
"""

import html
import json
from pathlib import Path
from string import Template


ROOT = Path(__file__).resolve().parent
raw = (ROOT / "vercel-stitch.html").read_text()
for phrase in ("Agentic", "Build agents on infrastructure", "Recently shipped"):
    assert phrase in raw, f"Unexpected Stitch export: {phrase}"

reference = json.loads((ROOT / "vercel-browser-reference.json").read_text())
ASSETS = ROOT / "vercel-assets"
for name in ("geist-variable.woff2", "hero-glow.avif", "notion-product.webp", "zapier-product.webp", "mintlify-product.webp"):
    assert (ASSETS / name).is_file(), name


def esc(value):
    return html.escape(value, quote=True)


cases = []
for index, section in enumerate(reference["sections"]):
    features = "".join(f"<li>{esc(name)}</li>" for name in section["features"])
    media = (f'<img class="case-image" src="vercel-assets/{esc(section["asset"])}" '
             f'alt="{esc(section["customer"])} website shown on Vercel" loading="lazy">')
    info = (f'<div class="case-info"><p>{esc(section["body"])}</p><small>Features</small>'
            f'<ul>{features}</ul></div>')
    contents = info + media if index == 1 else media + info
    cases.append(
        f'<section class="case {"case-reverse case-second" if index == 1 else "case-third" if index == 2 else ""}">'
        f'<h2>{esc(section["heading"])}</h2><div class="case-main">{contents}</div></section>'
    )

capability_text = (
    ("For coding agents", "For coding agents to deploy in their native language, with Vercel's API, CLI, MCP, and Skills."),
    ("To ship apps and agents", "To ship apps and agents in Sandboxed VMs, with durable backends, powered by hundreds of models."),
    ("Automated by agents", "Automated by agents who autonomously investigate errors, plan fixes, and open PRs."),
)
capabilities = "".join(
    f'<details><summary>{esc(title)}</summary><p>{esc(body)}</p></details>'
    for title, body in capability_text
)
customer_logos = {
    "Blackbox": "blackbox",
    "Charles Schwab": "charles-schwab",
    "DoorDash": "doordash",
    "OpenAI": "openai",
    "Supreme": "supreme",
    "The Weather Company": "the-weather-company",
    "Polymarket": "polymarket",
}
assert set(reference["hero"]["customers"]) == set(customer_logos)
for slug in customer_logos.values():
    assert (ASSETS / f"customer-{slug}.svg").is_file(), slug
customers = "".join(
    f'<img src="vercel-assets/customer-{customer_logos[name]}.svg" alt="{esc(name)}">'
    for name in reference["hero"]["customers"]
)

footer_groups = [
    ("Agent Stack", "AI SDK|AI Gateway|Sandbox|Workflows|Connect|Passport|eve"),
    ("Core Platform", "CI/CD|Content Delivery|Fluid Compute|Observability"),
    ("Security", "Platform Security|WAF|Bot Management|BotID"),
    ("Tools", "Vercel Drop|Vercel Agent|Vercel Plugin|Agent Skills|Domains|v0"),
    ("Frameworks", "eve|Next.js|Nuxt|SvelteKit|Nitro|Turborepo|Tanstack Start|FastAPI|All frameworks"),
    ("SDKs", "Vercel SDK|Workflow SDK|Flags SDK|Chat SDK|Queues SDK|Streamdown"),
    ("Build", "AI Apps|Web Apps|Marketing Sites|Platforms|Commerce|Platform Engineers|Design Engineers"),
    ("Learn", "Docs|Blog|Changelog|Knowledge Base|Academy|Articles|Community|Is Agentic"),
    ("Explore", "Customers|Marketplace|Templates|Partner Finder|Vercel + AWS"),
    ("Company", "About|Careers|Press|Events|Startups|Shipped on Vercel|Open Source Program|Enterprise|Pricing|Help"),
    ("Legal & Trust", "Privacy Policy|Terms of Service|Cookie Policy|DPA|Acceptable Use Policy|Legal (all documents)|Trust Center|Status|Cookie Preferences"),
    ("Social", "GitHub|X|LinkedIn|YouTube|Instagram"),
]
assert [group for group, _ in footer_groups] == reference["footerGroups"]
footer = "".join(
    f'<div class="footer-group"><h3>{esc(title)}</h3>'
    + "".join(f'<span>{esc(item)}</span>' for item in items.split("|"))
    + "</div>"
    for title, items in footer_groups
)

page = Template(r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Agentic Infrastructure - Vercel</title><meta name="description" content="Vercel's current Agentic Infrastructure homepage, reconstructed as a public design study.">
<style>
@font-face{font-family:Geist;src:url(vercel-assets/geist-variable.woff2) format('woff2');font-weight:100 900;font-display:swap}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#000;color:#f2f2f2;font-family:Geist,Arial,sans-serif;-webkit-font-smoothing:antialiased}a{color:inherit;text-decoration:none}button{font:inherit}h1,h2,h3,p,ul{margin:0}img{display:block;max-width:100%}
.header{height:64px;position:sticky;top:0;z-index:50;background:#000;display:flex;align-items:center;justify-content:space-between;padding:0 24px;border-bottom:1px solid #151515;font-size:14px}.header-left,.header-links,.header-right{display:flex;align-items:center}.header-left{gap:31px}.header-links{gap:28px;color:#aaa}.header-right{gap:10px}.header-right a{padding:8px 13px;border:1px solid #2a2a2a;border-radius:8px}.header-right .signup{background:#fff;color:#111;border-color:#fff}.header .logo{display:block;width:22px;height:20px;filter:invert(1)}
main{overflow:hidden}.hero{height:856px;position:relative}.announcement{position:absolute;top:21px;left:0;right:0;display:flex;justify-content:center;gap:34px;font-size:14px}.announcement a{color:#fff}.hero-glow{position:absolute;top:82px;left:50%;width:830px;max-width:none;transform:translateX(-50%);pointer-events:none}.hero h1{position:absolute;left:24px;top:238px;width:450px;font-size:64px;line-height:64px;letter-spacing:-.06em;font-weight:400}.hero-actions{position:absolute;top:398px;left:24px;display:flex;gap:10px;font-size:14px}.hero-actions a,.closing-actions a{padding:10px 18px;border:1px solid #333;border-radius:999px;background:#0a0a0a}.hero-actions .primary,.closing-actions .primary{background:#f4f4f4;color:#111;border-color:#f4f4f4}.hero-capabilities{position:absolute;top:285px;right:24px;width:356px;font-size:16px}.hero-capabilities details{margin:0 0 14px}.hero-capabilities summary{list-style:none;cursor:pointer}.hero-capabilities summary::-webkit-details-marker{display:none}.hero-capabilities p{color:#aaa;font-size:13px;line-height:1.45;margin-top:8px}.customer-strip{position:absolute;top:600px;left:0;right:0;height:100px;display:flex;align-items:center;justify-content:space-between;gap:20px;padding:0 24px;white-space:nowrap;overflow:hidden}.customer-strip img{flex:none;max-width:none}
.case{height:819px;padding:72px 24px 0;position:relative;background:radial-gradient(ellipse at 38% 65%,#111 0%,#000 64%)}.case-second{height:820px;background:radial-gradient(ellipse at 63% 65%,#111 0%,#000 64%)}.case-third{height:771px}.case h2{font-size:56px;line-height:56px;letter-spacing:-.05em;font-weight:400;max-width:820px}.case-reverse h2{margin-left:417px}.hero + .case h2{max-width:740px}.case-main{display:grid;grid-template-columns:minmax(0,844px) minmax(0,293px);gap:95px;align-items:center;margin-top:42px}.case-reverse .case-main{grid-template-columns:minmax(0,320px) minmax(0,815px);gap:97px}.case-image{width:100%;height:auto;object-fit:cover;border:1px solid #252525;border-radius:11px}.case-info{align-self:start;padding-top:70px}.case-info p{font-size:23px;line-height:1.4;letter-spacing:-.035em;max-width:300px}.case-info small{display:block;color:#777;font-size:13px;margin:36px 0 10px}.case-info ul{list-style:none;padding:0;display:grid;gap:8px;font-size:14px}
.recent{height:994px;padding:72px 24px 0}.recent h2{font-size:56px;line-height:1;font-weight:400;letter-spacing:-.05em}.recent-grid{margin-top:35px;display:grid;grid-template-columns:1fr 1fr;gap:18px;height:650px}.recent-card{border:1px solid #242424;border-radius:7px;overflow:hidden;position:relative;padding:20px;background:#030303}.recent-right{display:grid;grid-template-rows:1fr 1fr;gap:18px}.recent-card h3{font-weight:400;font-size:23px}.recent-card p{color:#999;font-size:14px;line-height:1.5;margin-top:7px;max-width:290px}.eve-card{display:flex;flex-direction:column;justify-content:end}.eve-card:before{content:'E / E';position:absolute;font:200px/1 Geist,Arial,sans-serif;letter-spacing:-.12em;color:#111;left:4%;top:10%}.eve-card>*{position:relative}.passport-card,.containers-card{display:flex;align-items:end}.passport-card:after{content:'▲';position:absolute;right:15%;top:23%;font-size:90px;color:#f1f1f1}.containers-card:after{content:'▲ vercel deploy\A ✓ Building image from Dockerfile.vercel\A ✓ Deployed to Fluid compute';white-space:pre;position:absolute;right:5%;top:18%;font:13px/2 ui-monospace,monospace;color:#bbb;border:1px solid #242424;background:#080808;padding:14px 18px;border-radius:8px}
.closing{height:256px;text-align:center;padding-top:72px}.closing h2{font-size:56px;line-height:1;font-weight:400;letter-spacing:-.05em}.closing-actions{display:flex;justify-content:center;gap:12px;margin-top:36px;font-size:14px}.footer{border-top:1px solid #222;padding:72px 24px 90px}.footer-grid{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));row-gap:90px}.footer-group{display:flex;flex-direction:column;gap:10px;color:#888;font-size:14px}.footer-group h3{color:#f2f2f2;font-size:14px;font-weight:400;margin-bottom:7px}.footer-bottom{color:#666;font-size:13px;margin-top:100px}
@media(max-width:900px){.header-links{gap:13px}.hero-glow{width:700px}.hero-capabilities{right:20px;width:250px}.customer-strip{font-size:14px}.case,.case-second,.case-third{height:auto;min-height:700px;padding:70px 20px}.case h2{font-size:48px;line-height:1.03}.case-reverse h2{margin-left:0}.case-main,.case-reverse .case-main{grid-template-columns:1.5fr 1fr;gap:25px}.case-reverse .case-main{grid-template-columns:1fr 1.5fr}.recent{height:auto;padding:70px 20px}.recent-grid{height:570px}.footer-grid{grid-template-columns:repeat(3,1fr)}}
@media(max-width:620px){.header{padding:0 16px}.header-links{display:none}.header-right a:first-child{display:none}.header-right a{padding:7px 9px;font-size:12px}.hero{height:760px}.announcement{top:32px;gap:14px;font-size:12px}.hero h1{top:132px;left:16px;font-size:52px;line-height:52px;width:calc(100% - 32px)}.hero-actions{top:256px;left:16px}.hero-glow{width:620px;top:258px}.hero-capabilities{top:575px;left:16px;right:auto;width:calc(100% - 32px);display:flex;gap:12px;font-size:12px}.hero-capabilities details{flex:1}.customer-strip{height:80px;font-size:12px}.case,.case-second,.case-third{min-height:0;padding:70px 16px 90px}.case h2{font-size:37px;line-height:1.06}.case-main,.case-reverse .case-main{display:flex;flex-direction:column;align-items:stretch;margin-top:36px}.case-reverse .case-main{flex-direction:column-reverse}.case-info p{font-size:20px}.recent{padding:70px 16px}.recent h2,.closing h2{font-size:42px}.recent-grid{display:block;height:auto}.recent-card{height:280px;margin-top:14px}.recent-right{display:block}.recent-right .recent-card{height:250px}.closing{height:270px;padding:65px 16px 0}.footer{padding:70px 16px}.footer-grid{grid-template-columns:repeat(2,1fr);gap:55px 20px}}
</style></head><body>
<header class="header"><div class="header-left"><a href="https://vercel.com/home" aria-label="Vercel"><img class="logo" src="vercel-assets/vercel-logo.svg" alt=""></a><nav class="header-links"><a href="https://vercel.com/">Products⌄</a><a href="https://vercel.com/">Resources⌄</a><a href="https://vercel.com/enterprise">Enterprise</a><a href="https://vercel.com/pricing">Pricing</a></nav></div><div class="header-right"><a href="https://vercel.com/contact/sales">Get a Demo</a><a href="https://vercel.com/login">Log In</a><a class="signup" href="https://vercel.com/signup">Sign Up</a></div></header>
<main><section class="hero"><div class="announcement"><span>Ship 26 is coming to SF</span><a href="https://vercel.com/ship">Get your ticket&nbsp; ↗</a></div><img class="hero-glow" src="vercel-assets/hero-glow.avif" alt=""><h1>Agentic<br>Infrastructure</h1><div class="hero-actions"><a class="primary" href="https://vercel.com/new">Deploy now</a><a href="https://vercel.com/contact/sales">Talk to sales</a></div><div class="hero-capabilities">$capabilities</div><div class="customer-strip">$customers</div></section>
$cases
<section class="recent"><h2>Recently shipped</h2><div class="recent-grid"><div class="recent-card eve-card"><h3>eve</h3><p>A framework for building durable agents.</p></div><div class="recent-right"><div class="recent-card passport-card"><div><h3>Passport</h3><p>Secure every internal agent, app, and deployment with your identity provider.</p></div></div><div class="recent-card containers-card"><div><h3>Containers</h3><p>Run production workloads in isolated containers on Vercel.</p></div></div></div></div></section>
<section class="closing"><h2>Built by you, or your agents</h2><div class="closing-actions"><a class="primary" href="https://vercel.com/new">Deploy now</a><a href="https://vercel.com/">Onboard your agent</a></div></section></main>
<footer class="footer"><div class="footer-grid">$footer</div><div class="footer-bottom">© 2026 Vercel, Inc.</div></footer>
</body></html>''').substitute(capabilities=capabilities, customers=customers, cases="\n".join(cases), footer=footer)

for invented in ("Deploy, coordinate, and orchestrate", "Zero cold starts", "Sub-millisecond elastic scale", "Architecture", "Telemetry"):
    assert invented not in page, invented
(ROOT / "vercel.html").write_text(page)
print("vercel.html", len(page), "bytes")
