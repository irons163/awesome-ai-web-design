"""Refine the native Stitch screen against the observed public Notion page.

The raw Stitch export is retained as notion-stitch.html. This transformation
removes its placeholders and fictional content while preserving its screen
hierarchy and observed public copy.
"""

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
raw = (ROOT / "notion-stitch.html").read_text()
for required in ("Where teams and", "AI where your team works.", "Trusted by teams that ship."):
    assert required in raw, f"Unexpected Stitch source: missing {required}"

reference = json.loads((ROOT / "notion-browser-reference.json").read_text())
logo_data = json.loads((ROOT / "notion-logo-browser-reference.json").read_text())
assets = "notion-assets/"


def esc(value):
    return html.escape(value, quote=True)


def cta():
    return '<div class="actions"><a class="button primary" href="https://www.notion.com/signup">Get Notion free</a><a class="button secondary" href="https://www.notion.com/contact-sales">Request a demo</a></div>'


brand_names = ("openai", "a24", "figma", "fedex", "ramp", "cursor", "substack", "nvidia", "toyota")
brand_logos = "".join(
    f'<img src="{assets}logo-{name}.svg" alt="{name.title()}" loading="eager">'
    for name in brand_names
)

use_cases = [
    ("Triage product feedback", "mailbox", "https://www.notion.com/product/ai/use-cases/triage-product-feedback", "#097fe8"),
    ("Resolve support tickets in Slack", "rock", "https://www.notion.com/product/ai/use-cases/resolve-support-tickets-in-slack", "#e8a42e"),
    ("Respond to security alerts faster", "sign", "https://www.notion.com/product/ai/use-cases/respond-to-security-alerts-faster", "#e35845"),
    ("Automate weekly reporting", "apple", "https://www.notion.com/product/ai/use-cases/automate-weekly-reporting", "#39a944"),
    ("Create your own developer tools", "light-bulb", "https://www.notion.com/product/dev", "#1313ba"),
]
use_case_html = "".join(
    f'<a class="usecase" href="{esc(url)}"><span class="case-icon" style="background:{color}"><img src="{assets}usecase-{icon}.png" alt="">'
    + (f'<img class="worker" src="{assets}usecase-worker.png" alt="">' if icon == "light-bulb" else "")
    + f'</span><strong>{esc(title)} <span aria-hidden="true">→</span></strong></a>'
    for title, icon, url, color in use_cases
)

stories = [
    ("Cursor", "cursor", "Using the most AI-native tools like Notion is an important competitive advantage for us to stay small while doing a lot.", "Michael Truell, Co-founder & CEO", "https://www.notion.com/customers/cursor"),
    ("Faire", "faire", "Notion’s thoughtful design speeds up collaboration and decisions so we can deliver impact to our customers faster.", "Renee Solorzano, Sr. Director of Product Design", "https://www.notion.com/customers/faire"),
    ("Ramp", "ramp", "Notion Custom Agents help our team go beyond doing work with AI to building AI tools that do the work for them.", "Ben Levick, Head of Operations & Internal AI", "https://www.notion.com/customers/ramp"),
]
story_html = "".join(
    f'<a class="story story-{slug}" href="{esc(url)}" style="background-image:linear-gradient(180deg,transparent 28%,rgba(0,0,0,.75) 100%),linear-gradient(0deg,var(--tint),var(--tint)),url({assets}story-{slug}.png)"><img class="story-logo" src="{assets}logo-{slug}.svg" alt="{esc(name)}"><div class="story-text"><blockquote>“{esc(quote)}”</blockquote><p>{esc(person)}</p></div></a>'
    for name, slug, quote, person, url in stories
)

footer_groups = []
for group in reference["footer"]:
    if group["title"] not in {"Product", "Resources", "Company", "Notion for"}:
        continue
    links = "".join(f'<a href="{esc(link["url"])}">{esc(link["text"])}</a>' for link in group["links"])
    footer_groups.append(f'<div class="footer-group"><h3>{esc(group["title"])}</h3>{links}</div>')
footer_html = "".join(footer_groups)

page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(reference['title'])}</title>
<meta name="description" content="{esc(reference['hero']['subheading'])}">
<style>
@font-face{{font-family:NotionInter;src:url({assets}font-regular.woff2)}}
@font-face{{font-family:NotionInter;src:url({assets}font-medium.woff2);font-weight:500}}
@font-face{{font-family:NotionInter;src:url({assets}font-semibold.woff2);font-weight:600}}
@font-face{{font-family:NotionInter;src:url({assets}font-bold.woff2);font-weight:700 900}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}body{{margin:0;background:#fff;color:#1b1b1b;font-family:NotionInter,Arial,sans-serif;-webkit-font-smoothing:antialiased}}a{{color:inherit;text-decoration:none}}button{{font:inherit}}
.site-nav{{height:64px;padding:0 24px;display:grid;grid-template-columns:1fr auto 1fr;align-items:center;position:sticky;top:0;background:#fff;z-index:50;border-bottom:1px solid #f2f2f2}}
.nav-logo{{display:block;width:33px;height:34px}}.nav-logo svg{{display:block;width:33px;height:34px}}.nav-links,.nav-actions{{display:flex;align-items:center;gap:32px;font-size:15px;font-weight:500;white-space:nowrap}}.nav-actions{{justify-self:end;gap:26px}}.nav-links a:hover,.nav-actions a:not(.button):hover{{text-decoration:underline}}.chev{{font-size:13px;padding-left:4px}}
.button{{display:inline-flex;align-items:center;justify-content:center;min-height:38px;padding:0 18px;border-radius:8px;font-size:16px;font-weight:500;white-space:nowrap}}.button.primary{{background:#2e73c5;color:white}}.button.primary:hover{{background:#215eaa}}.button.secondary{{background:#eaf3ff;color:#284e75}}.nav-actions .button{{font-size:15px;min-height:36px;padding:0 14px}}
.hero{{height:1425px;position:relative;text-align:center;padding-top:80px;overflow:hidden}}.hero h1{{margin:0 auto;font-size:96px;line-height:1.09;letter-spacing:-.046em;font-weight:700;max-width:1152px}}.pill{{display:inline-flex;align-items:center;gap:12px;border-radius:80px;background:#fff0c8;padding:0 20px;white-space:nowrap;font-size:.88em;line-height:1.05;vertical-align:baseline;letter-spacing:-.04em}}.pill-dot{{width:31px;height:31px;background:#fac350;border-radius:50%;display:inline-block;flex:none}}.hero-subtitle{{font-size:20px;line-height:1.4;margin:23px 20px 20px}}.actions{{display:flex;justify-content:center;gap:16px}}.hero-video{{display:block;position:absolute;top:469px;left:50%;transform:translateX(-50%);width:958px;height:599px;object-fit:cover;border-radius:10px 10px 0 0;box-shadow:0 0 3px #ddd}}
.brand-strip{{position:absolute;left:0;right:0;top:611px;height:59px;background:#fff;z-index:2;display:flex;align-items:center;justify-content:space-around;gap:28px;overflow:hidden;padding:0 7.5%}}.brand-strip img{{display:block;max-width:100px;max-height:32px;object-fit:contain;filter:grayscale(1)}}
.content{{width:min(1094px,calc(100% - 48px));margin:auto}}h2{{font-size:52px;line-height:1.08;letter-spacing:-.038em;margin:0;font-weight:700}}.features{{margin-top:0}}.feature-grid{{display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-top:25px}}.feature{{background:#fbfbfa;border-radius:12px;min-height:530px;padding:24px;overflow:hidden;position:relative}}.feature-kicker{{font-size:15px;margin:0 0 10px;color:#444}}.feature h3{{font-size:24px;line-height:1.17;letter-spacing:-.027em;margin:0;max-width:460px}}.arrow-circle{{position:absolute;right:24px;top:76px;background:#000;color:#fff;width:32px;height:32px;border-radius:50%;display:grid;place-items:center;font-size:24px;line-height:1}}.feature-visual{{position:absolute;left:24px;right:24px;top:164px;height:487px;background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 3px 20px #00000009}}.feature-visual img{{display:block;width:100%;height:100%;object-fit:cover}}.feature-visual .overlay{{position:absolute;width:100%;height:auto;left:0;bottom:0;object-fit:contain}}.feature-wide{{height:300px;min-height:0;margin-top:24px}}.feature-wide .feature-visual{{left:auto;right:0;top:0;width:52%;height:100%;background:transparent;box-shadow:none}}.feature-wide .feature-visual img{{position:absolute;width:62%;height:auto;object-fit:contain;right:0;bottom:0}}.feature-wide .feature-visual img:first-child{{right:34%;bottom:-20px}}
.usecases{{margin-top:30px}}.section-kicker{{color:#6b6b6b;font-size:15px;margin:0 0 12px}}.usecase-grid{{display:grid;grid-template-columns:repeat(5,1fr);gap:8px}}.usecase{{border:1px solid #ddd;border-radius:12px;height:160px;padding:24px;display:flex;flex-direction:column;justify-content:space-between}}.usecase:hover{{background:#f8f8f8}}.case-icon{{display:grid;place-items:center;width:39px;height:39px;border-radius:50%;position:relative}}.case-icon img{{width:35px;height:35px;object-fit:contain}}.case-icon img.worker{{position:absolute;width:20px;height:20px;right:-16px;bottom:-3px}}.usecase strong{{font-size:16px;line-height:1.4;letter-spacing:-.01em}}
.stories{{margin-top:200px}}.story-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;margin-top:34px}}.story{{height:436px;border-radius:11px;overflow:hidden;background-size:cover;background-position:center;display:flex;flex-direction:column;justify-content:space-between;color:#fff;padding:16px 20px 24px;--tint:rgba(233,67,53,.62)}}.story-faire{{--tint:rgba(31,87,160,.66)}}.story-ramp{{--tint:rgba(195,123,10,.60)}}.story-logo{{display:block;max-width:90px;max-height:24px;object-fit:contain;object-position:left;filter:brightness(0) invert(1)}}.story-ramp .story-logo{{max-width:98px}}.story blockquote{{font:20px/1.36 Georgia,serif;margin:0 0 13px}}.story p{{font-size:14px;line-height:1.45;margin:0}}
.metrics{{margin-top:110px;display:flex;justify-content:center;gap:50px;color:#555;font-size:15px;overflow:hidden;white-space:nowrap;border-bottom:1px solid #f1f1f1;padding-bottom:24px}}.end-cta{{text-align:center;margin:120px auto 120px}}.end-cta h2{{font-size:44px;margin-bottom:20px}}
.site-footer{{border-top:1px solid #f3f3f3;padding:78px max(5%,calc((100% - 1152px)/2)) 38px}}.footer-layout{{display:grid;grid-template-columns:2fr repeat(4,1fr);gap:36px}}.footer-mark{{display:flex;align-items:center;gap:12px;font-size:28px;font-weight:700}}.footer-mark svg{{width:37px;height:37px}}.quote{{font:18px/1.3 Georgia,serif;margin:85px 0 18px}}.quote-credit{{color:#747474;font-size:14px}}.footer-group{{display:flex;flex-direction:column;gap:9px;min-width:140px;font-size:15px}}.footer-group h3{{margin:0 0 4px;color:#777;font-size:14px;font-weight:400}}.footer-group a:hover{{text-decoration:underline}}.footer-bottom{{display:flex;justify-content:space-between;gap:20px;margin:60px 0 0 34%;color:#777;font-size:14px}}
@media(max-width:800px){{.site-nav{{grid-template-columns:auto 1fr;padding:0 18px}}.nav-links{{display:none}}.nav-actions{{gap:12px}}.nav-actions>a:first-child{{display:none}}.hero{{height:960px;padding-top:62px}}.hero h1{{font-size:clamp(43px,8.5vw,70px);line-height:1.12;padding:0 15px}}.pill{{padding:0 10px;gap:6px}}.pill-dot{{width:15px;height:15px}}.hero-subtitle{{font-size:16px}}.hero-video{{width:94%;height:auto;top:380px}}.brand-strip{{top:600px;padding:0 4%;gap:24px;justify-content:flex-start;overflow:auto}}.brand-strip img{{flex:none;max-width:85px}}.content{{width:calc(100% - 32px)}}h2{{font-size:36px}}.feature-grid,.story-grid{{grid-template-columns:1fr}}.feature{{min-height:520px}}.feature-visual{{height:390px}}.feature-wide{{height:310px;min-height:0}}.feature-wide .feature-visual{{width:65%}}.usecase-grid{{grid-template-columns:repeat(2,1fr)}}.usecase{{height:145px}}.stories{{margin-top:110px}}.metrics{{gap:20px;justify-content:flex-start}}.footer-layout{{grid-template-columns:repeat(2,1fr)}}.footer-brand{{grid-column:1/-1}}.footer-bottom{{margin-left:0}}}}
</style>
</head>
<body>
<nav class="site-nav" aria-label="Main"><a class="nav-logo" href="https://www.notion.com/product" aria-label="Notion – Home">{logo_data['svg']}</a><div class="nav-links"><a href="https://www.notion.com/product">Product <span class="chev">⌄</span></a><a href="https://www.notion.com/resources">Resources <span class="chev">⌄</span></a><a href="https://www.notion.com/pricing">Pricing</a><a href="https://www.notion.com/contact-sales">Request a demo</a></div><div class="nav-actions"><a href="https://www.notion.com/login">Log in</a><a class="button primary" href="https://www.notion.com/signup">Get Notion free</a></div></nav>
<main>
<section class="hero"><h1>Where teams and<br>agents <span class="pill"><span class="pill-dot"></span>Build</span> together.</h1><p class="hero-subtitle">{esc(reference['hero']['subheading'])}</p>{cta()}<video class="hero-video" autoplay muted loop playsinline poster="{assets}hero-poster.jpg" src="{assets}hero.mp4"></video><div class="brand-strip" aria-label="Customers">{brand_logos}</div></section>
<section class="content features"><h2>AI where your team works.</h2><div class="feature-grid"><a class="feature" href="https://www.notion.com/product/docs"><p class="feature-kicker">Capture knowledge</p><h3>Bring everything into one system of record.</h3><span class="arrow-circle">→</span><div class="feature-visual"><img src="{assets}feature-capture.jpg" alt="Notion Meetings knowledge base"></div></a><a class="feature" href="https://www.notion.com/product/ai"><p class="feature-kicker">Find answers</p><h3>Get answers, instantly—with citations.</h3><span class="arrow-circle">→</span><div class="feature-visual"><img src="{assets}feature-find.png" alt="Notion AI answers"><img class="overlay" src="{assets}feature-find-overlay.png" alt=""></div></a></div><a class="feature feature-wide" href="https://www.notion.com/product/ai/agents"><p class="feature-kicker">Automate busywork</p><h3>Keep work moving 24/7 with agents.</h3><span class="arrow-circle">→</span><div class="feature-visual"><img src="{assets}feature-automate-back.png" alt="Notion engineering tasks"><img src="{assets}feature-automate-front.jpg" alt="Notion coding agent"></div></a></section>
<section class="content usecases"><p class="section-kicker">See what Notion can do</p><div class="usecase-grid">{use_case_html}</div></section>
<section class="content stories"><h2>Trusted by teams that ship.</h2><div class="story-grid">{story_html}</div></section><div class="metrics"><span>62% of Fortune 100 use Notion</span><span>G2’s #1 knowledge base for 3 consecutive years</span><span>100M users in over 50 countries</span></div>
<section class="end-cta"><h2>Get started today.</h2>{cta()}</section>
</main>
<footer class="site-footer"><div class="footer-layout"><div class="footer-brand"><div class="footer-mark">{logo_data['svg']}<span>Notion</span></div><p class="quote">“We shape our tools,<br>and thereafter our tools shape us.”</p><p class="quote-credit">Marshall McLuhan</p></div>{footer_html}</div><div class="footer-bottom"><span>© 2026 Notion Labs, Inc.</span><span>Cookie settings</span><span>English (US)⌄</span></div></footer>
</body></html>'''

(ROOT / "notion.html").write_text(page)
print("notion.html", len(page), "bytes")
