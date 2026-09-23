"""Build the Figma draft from a native Stitch screen and observed official media.

The unchanged native export is figma-stitch.html. This file intentionally removes
Stitch's invented artwork/collaborators and uses the public page's copy, layout,
video frames, gallery media, customer marks, and footer links. It is a draft,
not a visually verified reproduction of the live site.
"""

import html
import json
import re
from pathlib import Path
from string import Template


ROOT = Path(__file__).resolve().parent
raw = (ROOT / "figma-stitch.html").read_text()
for text in ("The full-", "Marcus (AI)", "Elena", "Move fast in the right direction"):
    assert text in raw, f"Unexpected native Stitch export: missing {text}"

reference = json.loads((ROOT / "figma-browser-reference.json").read_text())
assets = json.loads((ROOT / "figma-asset-provenance.json").read_text())
assert reference["hero"]["heading"] == "The full-stack creative canvas"
assert len(reference["footer"]["links"]) == 61
for filename in assets:
    assert (ROOT / "figma-assets" / filename).is_file(), filename


def esc(value):
    return html.escape(value, quote=True)


def asset(filename):
    assert filename in assets, filename
    return f"figma-assets/{filename}"


logo_match = re.search(r"(<svg[^>]*viewbox=\"0 0 38 57\"[^>]*>.*?</svg>)", raw, re.S)
assert logo_match, "Figma mark missing from raw native Stitch export"
logo = logo_match.group(1)

gallery = [
    ("Texture values", "gallery-texture.png", None),
    ("Accessibility", "gallery-accessibility-poster.jpg", "1202189219"),
    ("Auto layout padding", "gallery-padding-poster.jpg", "1202189216"),
    ("Glass depth", "gallery-depth-poster.jpg", "1202189217"),
    ("Brush strokes on type", "gallery-brush.png", None),
    ("Vector editing", "gallery-vector.png", None),
    ("Variable type", "gallery-variable-poster.jpg", "1202189218"),
    ("Type on a path", "gallery-typepath.png", None),
    ("Motion timeline", "gallery-motion-poster.jpg", "1202194414"),
    ("Figma Weave butterfly", "gallery-weave.png", None),
    ("Image displacement", "gallery-displace-poster.jpg", "1203604825"),
    ("Butterfly mosaic", "gallery-butterfly.png", None),
]
gallery_html = "".join(
    (f'<button class="gallery-tile video-trigger" type="button" data-vimeo="{video}" aria-label="Play {esc(label)}"><img src="{asset(filename)}" alt="{esc(label)}" loading="lazy"></button>'
     if video else
     f'<div class="gallery-tile"><img src="{asset(filename)}" alt="{esc(label)}" loading="lazy"></div>')
    for label, filename, video in gallery
)

brands = ("airbnb", "atlassian", "dropbox", "duolingo", "github", "mercadolibre", "microsoft", "netflix", "pentagram", "slack", "stripe", "nyt", "zoom")
brand_html = "".join(
    f'<img src="{asset("logo-" + brand + ".svg")}" alt="{esc("The New York Times" if brand == "nyt" else brand.title())}" loading="lazy">'
    for brand in brands
)

community = [
    ("UI kits", "community-ui-kits.png"),
    ("Websites", "community-websites.png"),
    ("Social media", "community-social.png"),
    ("Mobile apps", "community-mobile.png"),
    ("Presentations", "community-presentations.png"),
]
community_html = "".join(
    f'<div class="community-card"><img src="{asset(filename)}" alt="{esc(label)} template example" loading="lazy"><strong>{esc(label)}</strong></div>'
    for label, filename in community
)

links = reference["footer"]["links"]
groups = [
    ("PRODUCT", links[:15]),
    ("PLANS", links[15:19]),
    ("USE CASES", links[19:35]),
    ("RESOURCES", links[35:56]),
    ("COMPANY", links[56:61]),
]


def footer_group(title, items):
    children = "".join(f'<a href="{esc(item["url"])}">{esc(item["text"])}</a>' for item in items)
    return f'<div class="footer-group"><h3>{esc(title)}</h3>{children}</div>'


footer_html = (
    f'<div class="footer-product">{footer_group(*groups[0])}{footer_group(*groups[1])}</div>'
    + "".join(footer_group(*group) for group in groups[2:])
)

page = Template(r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>$title</title>
<meta name="description" content="Figma is the collaborative canvas for design, code, and AI.">
<style>
@font-face{font-family:FigmaSans;src:url(figma-assets/site-font.woff2) format("woff2");font-weight:100 900;font-display:swap}
:root{font-family:FigmaSans,"SF Pro Display",system-ui,Arial,sans-serif;color:#111;background:#fff}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;overflow-x:hidden}button,a{font:inherit}a{color:inherit;text-decoration:none}button{cursor:pointer}img{display:block;max-width:100%}
.site-header{height:78px;display:flex;align-items:center;justify-content:space-between;padding:0 40px;background:#fff;position:sticky;top:0;z-index:50;border-bottom:1px solid #ededed}
.header-left,.header-right,.nav-main{display:flex;align-items:center}.header-left{gap:52px}.brand-mark{width:28px;height:42px;display:flex;align-items:center}.brand-mark svg{width:28px;height:42px}.nav-main{gap:28px;font-size:15px;font-weight:600}.nav-main details{position:relative}.nav-main summary{cursor:pointer;list-style:none}.nav-main summary::-webkit-details-marker{display:none}.nav-main summary::after{content:"⌄";font-size:15px;margin-left:7px}.nav-menu{position:absolute;top:31px;left:-17px;background:#fff;box-shadow:0 12px 35px #0002;border:1px solid #eaeaea;border-radius:8px;width:208px;padding:12px;display:flex;flex-direction:column;gap:1px}.nav-menu a{padding:9px 10px;border-radius:5px}.nav-menu a:hover{background:#f4f4f4}.header-right{gap:14px;font-size:14px;font-weight:600}.header-right>a{white-space:nowrap}.pill-button{border:1.5px solid #111;border-radius:7px;padding:11px 18px}.pill-button.dark{background:#111;color:#fff}.header-right>a:first-child{margin-right:7px}
h1,h2,h3,p,blockquote{margin:0}h2{font-size:30px;line-height:1.2;letter-spacing:-.035em;font-weight:600}h3{font-size:20px;line-height:1.2;letter-spacing:-.025em}.subhead{font-size:18px;line-height:1.4;color:#666}.section-link{font-size:17px;text-decoration:underline;text-underline-offset:4px;font-weight:600}
.hero{height:972px;position:relative;max-width:1280px;margin:auto;overflow:hidden}.hero h1{position:absolute;top:318px;left:40px;width:288px;font-size:56px;font-weight:500;line-height:1;letter-spacing:-.07em;z-index:2}.hero-media{position:absolute;left:342px;top:110px;width:596px;height:720px;padding:0;border:0;background:#fff;overflow:hidden}.hero-media img{width:100%;height:100%;object-fit:contain}.hero-cta{position:absolute;top:388px;left:calc(100% - 296px);width:224px;height:84px;display:grid;place-items:center;background:#111;color:#fff;border-radius:7px;font-size:19px;font-weight:600}.hero-cta:hover,.pill-button.dark:hover,.cta-button:hover{background:#333}
.observed-section{max-width:1280px;margin:0 auto}.center-heading{width:795px;margin:0 auto;text-align:center}.center-heading .subhead{margin-top:13px}.video-trigger{border:0;padding:0;display:block;position:relative;background:transparent;overflow:hidden}.video-trigger img{height:100%;width:100%;object-fit:cover}.video-trigger:focus-visible{outline:3px solid #0d99ff;outline-offset:3px}.video-trigger iframe{border:0;width:100%;height:100%;display:block}.video-trigger .play-icon{position:absolute;bottom:20px;left:20px;background:#ffffffd9;width:37px;height:37px;border-radius:50%;display:grid;place-items:center;font-size:15px;color:#111}
.workspace{height:990px}.workspace .wide-video{width:calc(100% - 80px);height:540px;margin:55px auto 0;background:#bbe5a5}.workspace-cards{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:40px;max-width:998px;margin:28px auto 0}.workspace-card p{color:#666;font-size:16px;line-height:1.45;margin-top:9px}.workspace-card a{display:inline-block;margin-top:13px;font-size:16px;text-decoration:underline;text-underline-offset:3px}
.ai{height:1035px}.ai .wide-video{width:calc(100% - 80px);height:675px;margin:52px auto 0;background:#b9c9ef}
.expressive{height:1459px}.expressive-header{padding:0 40px}.expressive-header .subhead{margin-top:12px}.expressive-header .section-link{display:inline-block;margin-top:13px}.gallery{margin-top:44px;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;position:relative;left:-8px;width:calc(100% + 16px)}.gallery-tile{height:385px;overflow:hidden;background:#eee;display:block;width:100%;padding:0;border:0}.gallery-tile img{width:100%;height:100%;object-fit:cover}
.make{height:991px}.make .section-link{display:inline-block;margin-top:14px}.make .wide-video{width:calc(100% - 80px);height:675px;margin:49px auto 0;background:#9deef3}
.proof{height:740px;padding:0 40px;overflow:hidden}.proof h2{font-size:44px;line-height:1.1;letter-spacing:-.046em}.proof-body{display:grid;grid-template-columns:1fr 1fr;gap:50px;margin-top:92px;align-items:start}.quote{font-size:31px;line-height:1.21;letter-spacing:-.035em;max-width:550px}.quote-person{display:flex;align-items:center;gap:14px;margin-top:29px;font-size:15px;line-height:1.4}.quote-person img{width:48px;height:48px;border-radius:50%}.quote-person strong{display:block}.stat{text-align:left;padding-left:55px}.stat-number{font-size:160px;line-height:.9;letter-spacing:-.09em;font-weight:600}.stat-label{font-size:23px;line-height:1.18;max-width:300px;margin-top:18px}.stat-note{font-size:13px;color:#777;margin-top:8px}.logo-strip{display:flex;align-items:center;gap:55px;overflow:hidden;white-space:nowrap;margin-top:75px}.logo-strip img{height:31px;width:auto;max-width:165px;flex:none;object-fit:contain}
.end-cta{height:369px;text-align:center}.end-cta h2{font-size:48px;line-height:1.08;letter-spacing:-.045em}.cta-button{display:inline-flex;align-items:center;justify-content:center;background:#111;color:#fff;border-radius:7px;padding:18px 26px;font-size:18px;font-weight:600;margin-top:28px}
.community{height:879px;padding:0 40px;overflow:hidden}.community h2{font-size:48px;line-height:1.08;letter-spacing:-.045em}.community p{font-size:18px;color:#777;margin-top:15px}.community .section-link{display:inline-block;margin-top:17px}.community-cards{display:flex;gap:16px;margin-top:63px;overflow:hidden}.community-card{width:288px;flex:none}.community-card img{height:385px;width:288px;object-fit:cover}.community-card strong{font-size:19px;display:block;margin-top:17px}
.site-footer{background:#111;color:#fff;min-height:980px;padding:0 40px 50px}.footer-layout{max-width:1280px;margin:auto;display:grid;grid-template-columns:2fr repeat(4,1fr);gap:52px}.footer-brand{padding-top:71px}.footer-brand .wordmark{font-size:52px;font-weight:600;letter-spacing:-.06em}.footer-brand .brand-mark{margin:18px 0 37px;filter:brightness(0) invert(1)}.socials{display:flex;gap:12px}.socials a{border:1px solid #777;border-radius:50%;width:37px;height:37px;display:grid;place-items:center;font-size:14px;font-weight:700}.footer-group{display:flex;flex-direction:column;gap:16px;font-size:15px}.footer-group h3{font-size:16px;letter-spacing:.03em;margin:0 0 5px}.footer-group a{line-height:1.35}.footer-group a:hover{text-decoration:underline}.footer-product .footer-group+.footer-group{margin-top:53px}.footer-bottom{max-width:1280px;margin:100px auto 0;font-size:14px;color:#aaa;border-top:1px solid #555;padding-top:23px}
.event-banner{position:fixed;z-index:80;bottom:0;left:0;right:0;background:#e8d9ff;min-height:88px;display:flex;align-items:center;justify-content:center;gap:30px;font-size:17px;color:#111;box-shadow:0 -1px 3px #0001}.event-banner a{background:#111;color:#fff;padding:13px 24px;border-radius:6px;font-weight:600}.event-banner button{position:absolute;right:26px;top:16px;border:0;background:none;font-size:25px}
@media(max-width:900px){.site-header{padding:0 20px}.header-left{gap:20px}.nav-main{gap:12px}.header-right{gap:8px}.header-right .pill-button:first-of-type{display:none}.hero{height:790px}.hero h1{top:245px;left:20px;font-size:46px;width:235px}.hero-media{left:27%;top:103px;width:58%;height:610px}.hero-cta{left:auto;right:20px;top:365px;width:175px;height:66px;font-size:16px}.workspace,.ai,.make,.expressive,.proof,.end-cta,.community{height:auto;padding-bottom:90px}.center-heading{width:min(795px,calc(100% - 40px))}.workspace .wide-video,.ai .wide-video,.make .wide-video{width:calc(100% - 40px);height:auto;aspect-ratio:16/9}.workspace-cards{padding:0 30px}.gallery{left:0;width:100%;padding:0 20px;grid-template-columns:repeat(3,1fr)}.proof{padding:0 20px}.proof-body{gap:20px}.stat-number{font-size:100px}.community{padding:0 20px}.footer-layout{gap:25px}.site-footer{padding:50px 20px}.footer-brand{padding-top:0}}
@media(max-width:620px){.site-header{height:64px}.brand-mark,.brand-mark svg{width:24px;height:36px}.nav-main{display:none}.header-right>a:first-child,.header-right .pill-button{display:none}.header-right .pill-button.dark{display:inline-flex;font-size:12px;padding:9px 11px}.hero{height:710px}.hero h1{position:relative;top:auto;left:auto;width:auto;padding:37px 20px 0;font-size:52px;max-width:390px;line-height:1.02}.hero-media{left:5%;top:270px;width:90%;height:380px}.hero-cta{left:20px;right:auto;top:175px;width:164px;height:59px}.center-heading{text-align:left;width:calc(100% - 40px)}h2{font-size:32px}.subhead{font-size:16px}.workspace .wide-video,.ai .wide-video,.make .wide-video{margin-top:35px}.workspace-cards{grid-template-columns:1fr;gap:30px;margin-top:30px;padding:0 20px}.expressive-header{padding:0 20px}.gallery{grid-template-columns:repeat(2,1fr);gap:8px;margin-top:30px;padding:0 8px}.gallery-tile{height:auto;aspect-ratio:4/5}.make{padding-top:20px}.proof h2,.community h2,.end-cta h2{font-size:36px}.proof-body{grid-template-columns:1fr;margin-top:40px}.quote{font-size:24px}.stat{padding-left:0}.stat-number{font-size:92px}.logo-strip{margin-top:45px;gap:35px}.end-cta{padding:0 20px 85px}.community-cards{margin-top:35px}.community-card{width:210px}.community-card img{width:210px;height:280px}.site-footer{padding:55px 20px}.footer-layout{grid-template-columns:repeat(2,1fr);gap:30px}.footer-brand{grid-column:1/-1}.footer-group{font-size:14px;gap:12px}.event-banner{padding:13px 47px 13px 16px;min-height:73px;gap:10px;justify-content:flex-start;font-size:12px}.event-banner a{font-size:12px;padding:9px 11px;white-space:nowrap}.event-banner button{right:8px;top:3px}}
</style></head><body>
<header class="site-header"><div class="header-left"><a class="brand-mark" aria-label="Figma home" href="https://www.figma.com/">$logo</a><nav class="nav-main" aria-label="Main navigation"><details><summary>Products</summary><div class="nav-menu"><a href="https://www.figma.com/design/">Figma Design</a><a href="https://www.figma.com/make/">Figma Make</a><a href="https://www.figma.com/dev-mode/">Dev Mode</a><a href="https://www.figma.com/figjam/">FigJam</a></div></details><details><summary>Solutions</summary><div class="nav-menu"><a href="https://www.figma.com/design-explore/">Design and explore</a><a href="https://www.figma.com/build-ship/">Build and ship</a><a href="https://www.figma.com/ai/">AI workflows</a></div></details><details><summary>Community</summary><div class="nav-menu"><a href="https://www.figma.com/community">Community</a><a href="https://www.figma.com/templates/">Templates</a></div></details><details><summary>Resources</summary><div class="nav-menu"><a href="https://www.figma.com/blog/">Blog</a><a href="https://www.figma.com/resource-library/">Resource library</a><a href="https://help.figma.com/hc/en-us">Help center</a></div></details><a href="https://www.figma.com/pricing/">Pricing</a></nav></div><div class="header-right"><a href="https://www.figma.com/login">Log in</a><a class="pill-button" href="https://www.figma.com/contact/">Contact sales</a><a class="pill-button dark" href="https://www.figma.com/signup">Get started for free</a></div></header>
<main>
<section class="hero observed-section"><h1>The full-stack creative canvas</h1><button type="button" class="hero-media video-trigger" data-vimeo="1202887330" aria-label="Play Figma creative canvas video"><img src="$hero_poster" alt="Figma's creative canvas product collage"></button><a class="hero-cta" href="https://www.figma.com/signup">Get started</a></section>
<section class="workspace observed-section"><div class="center-heading"><h2>One workspace for your entire product development process.</h2><p class="subhead">Made so your whole team can go from WIP to ship, together.</p></div><button type="button" class="wide-video video-trigger" data-vimeo="1202195955" aria-label="Play Figma workspace video"><img src="$workspace_poster" alt="Figma product development workspace"></button><div class="workspace-cards"><div class="workspace-card"><h3>Design anything you can imagine</h3><p>Turn your ideas into apps, websites, and products.</p><a href="https://www.figma.com/design-explore/">Explore design tools</a></div><div class="workspace-card"><h3>Build with intention</h3><p>Dev tools that take you all the way to production.</p><a href="https://www.figma.com/build-ship/">Explore build tools</a></div></div></section>
<section class="ai observed-section"><div class="center-heading"><h2>Move fast in the right direction on an AI-native canvas.</h2><p class="subhead">Teammates and AI agents work in the same space with shared context. Generate new design directions, refine, and align—together.</p></div><button type="button" class="wide-video video-trigger" data-vimeo="1202195324" aria-label="Play Figma AI canvas video"><img src="$ai_poster" alt="Figma AI canvas showing an app design"></button></section>
<section class="expressive observed-section"><div class="expressive-header"><h2>Powerfully expressive. Incredibly precise.</h2><p class="subhead">Every technical tool you need to dial in the details.</p><a class="section-link" href="https://www.figma.com/design/">Explore Figma Design ↗</a></div><div class="gallery">$gallery</div></section>
<section class="make observed-section"><div class="center-heading"><h2>Start with design context. Build with consistency.</h2><p class="subhead">Your context, codebase, and agents stay connected so what you design is what gets shipped.</p><a class="section-link" href="https://www.figma.com/make/">Explore Figma Make ↗</a></div><button type="button" class="wide-video video-trigger" data-vimeo="1204234347" aria-label="Play Figma Make video"><img src="$make_poster" alt="Figma Make and codebase workspace"></button></section>
<section class="proof observed-section"><h2>The products you love are designed in Figma</h2><div class="proof-body"><div><blockquote class="quote">Everyone is able to influence, inspire, and give input without ever leaving the design file. That creates a really transparent, open, and honest process throughout the whole project.</blockquote><div class="quote-person"><img src="$portrait" alt="Francisco Seiz"><span><strong>Francisco Seiz</strong>Senior Design Director, Code and Theory</span></div></div><div class="stat"><div class="stat-number">95%</div><div class="stat-label">95% of the Fortune 500 uses Figma</div><p class="stat-note">Based on data from March 2025.</p></div></div><div class="logo-strip" aria-label="Figma customers">$brands</div></section>
<section class="end-cta observed-section"><h2>Ideas no longer have to wait their turn</h2><a class="cta-button" href="https://www.figma.com/signup">Get started</a></section>
<section class="community observed-section"><h2>Explore what you can do in Figma.</h2><p>Browse resources made by the community.</p><a class="section-link" href="https://www.figma.com/templates/">Browse all templates ↗</a><div class="community-cards">$community</div></section>
</main>
<footer class="site-footer"><div class="footer-layout"><div class="footer-brand"><div class="wordmark">Figma</div><div class="brand-mark">$logo</div><div class="socials"><a href="https://x.com/figma" aria-label="Figma on X">𝕏</a><a href="https://www.youtube.com/figmadesign" aria-label="Figma on YouTube">▶</a><a href="https://www.instagram.com/figma/" aria-label="Figma on Instagram">◎</a><a href="https://www.facebook.com/figmadesign" aria-label="Figma on Facebook">f</a></div></div>$footer</div><div class="footer-bottom">© 2026 Figma, Inc.</div></footer>
<aside class="event-banner" id="event-banner"><span>Join Config India virtually 15 October for free.</span><a href="https://www.figma.com/events/">Register</a><button type="button" aria-label="Dismiss announcement" onclick="document.getElementById('event-banner').remove()">×</button></aside>
<script>
for(const button of document.querySelectorAll('[data-vimeo]')){
  button.addEventListener('click',()=>{
    const id=button.getAttribute('data-vimeo');
    if(!/^\d+$$/.test(id))return;
    const frame=document.createElement('iframe');
    frame.src='https://player.vimeo.com/video/'+id+'?autoplay=1&muted=1';
    frame.title=button.getAttribute('aria-label')||'Figma video';
    frame.allow='autoplay; fullscreen; picture-in-picture';
    frame.allowFullscreen=true;
    button.replaceWith(frame);
    frame.className=button.className;
  });
}
</script>
</body></html>''').substitute(
    title=esc(reference["title"]), logo=logo,
    hero_poster=asset("hero-poster.jpg"), workspace_poster=asset("workspace-poster.jpg"),
    ai_poster=asset("ai-poster.jpg"), make_poster=asset("make-poster.jpg"),
    portrait=asset("portrait-francisco.jpg"),
    gallery=gallery_html, brands=brand_html, community=community_html, footer=footer_html,
)

for fictional in ("Marcus (AI)", "Elena", "High conversion hero layouts"):
    assert fictional not in page, fictional
(ROOT / "figma.html").write_text(page)
print("figma.html", len(page), "bytes")
