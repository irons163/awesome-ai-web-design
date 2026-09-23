"""Refine the native Stitch Claude export against the observed public homepage.

The raw export stays in claude-stitch.html. This script only creates claude.html.
"""

from html import escape
import json
from pathlib import Path
import re

ROOT = Path(__file__).parent
raw = (ROOT / "claude-stitch.html").read_text()
reference = json.loads((ROOT / "claude-browser-reference.json").read_text())


def replace_once(source: str, pattern: str, replacement: str) -> str:
    updated, count = re.subn(pattern, lambda _: replacement, source, count=1, flags=re.S)
    if count != 1:
        raise ValueError(f"Expected one replacement for {pattern!r}, got {count}")
    return updated


def list_markup(items: list[str]) -> str:
    return '<ul class="claude-feature-list">' + "".join(
        f'<li><span aria-hidden="true">✓</span>{escape(item)}</li>' for item in items
    ) + "</ul>"


raw = raw.replace(
    '<meta name="viewport" content="width=1280, initial-scale=1.0">',
    '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
)
raw = raw.replace('<span class="italic font-light">build faster</span>', "build faster")
wordmark = reference["assets"]["wordmark"]
raw = replace_once(
    raw,
    r"<!-- Claude Sunburst & Wordmark -->.*?<!-- Primary Nav -->",
    '<!-- Observed public Claude wordmark -->\n'
    f'<a href="https://claude.com/" class="claude-wordmark">{wordmark}</a>\n'
    '      <!-- Primary Nav -->',
)

# Stitch invented a Cowork task list. The official homepage actually plays this
# 612px-high video at the right of the hero, so use the public asset itself.
raw = replace_once(
    raw,
    r"<!-- Right Hero App Demo Panel.*?</section>",
    '<video class="claude-hero-video" src="claude-official-hero.mp4" '
    'autoplay loop muted playsinline aria-label="Claude homepage introduction"></video>\n'
    "  </section>",
)
raw = raw.replace(
    "By signing up, you agree to our <a href=\"#\" class=\"underline hover:text-[#aba8a1]\">Terms of Service</a> and acknowledge our <a href=\"#\" class=\"underline hover:text-[#aba8a1]\">Privacy Policy</a>.",
    "By continuing, you acknowledge Anthropic's "
    '<a href="https://www.anthropic.com/legal/privacy" class="underline">Privacy Policy</a> '
    "and agree to get occasional promotional emails and notifications.",
)
raw = raw.replace("https://claude.com/login", "https://claude.ai/login")
raw = raw.replace("https://claude.com/contact-sales", "https://claude.com/contact-sales")
raw = raw.replace("https://claude.com/try", "https://claude.ai")
raw = raw.replace("https://claude.com/upgrade", "https://claude.ai/login")
for old, new in {
    'href="#product"': 'href="https://claude.com/product/overview"',
    'href="#developers"': 'href="https://code.claude.com/docs/en/overview"',
    'href="#enterprise"': 'href="https://claude.com/solutions/enterprise"',
    'href="#resources"': 'href="https://claude.com/blog"',
    'href="#download"': 'href="https://claude.com/download"',
}.items():
    raw = raw.replace(old, new)
for marker, destination in (
    ("Google Button", "https://claude.ai/login"),
    ("Continue with email", "https://claude.ai/?redirect=claude.com&via=static_email"),
):
    pattern = rf"(<!-- {re.escape(marker)} -->\s*)<button([^>]*)>(.*?)</button>"
    raw, count = re.subn(
        pattern,
        lambda match: (
            match.group(1)
            + f'<a href="{escape(destination, quote=True)}"'
            + match.group(2)
            + ">"
            + match.group(3)
            + "</a>"
        ),
        raw,
        count=1,
        flags=re.S,
    )
    if count != 1:
        raise ValueError(f"Stitch login control {marker} missing")

for index, name in enumerate(("Free", "Pro", "Max"), 1):
    end = f"<!-- CARD {index + 1}:" if index < 3 else "    </div>\n\n    <!-- Pricing Disclaimer -->"
    pattern = rf"(<!-- CARD {index}: {name.upper()}.*?)(?={re.escape(end)})"
    match = re.search(pattern, raw, re.S)
    if not match:
        raise ValueError(f"Stitch plan card {name} missing")
    card = match.group(1)
    icon = next(x["svg"] for x in reference["assets"]["planPictograms"] if x["name"] == name)
    card = replace_once(
        card,
        r"<!-- Plan Icon -->\s*<div[^>]*>\s*<svg.*?</svg>\s*</div>",
        f'<!-- Observed plan pictogram -->\n<div class="claude-plan-icon">{icon}</div>',
    )
    features = next(x["features"] for x in reference["planCards"] if x["name"] == name)
    card = replace_once(card, r"<ul class=\"space-y-3\.5.*?</ul>", list_markup(features))
    card = card.replace(
        'class="rounded-[24px] border-2 border-[#cc785c] bg-[#1a1a18] p-8 flex flex-col justify-between relative shadow-xl"',
        'class="claude-plan-card rounded-[24px] border border-[#383735] bg-[#1a1a18] p-8 flex flex-col justify-between"',
    )
    card = re.sub(
        r'<div class="absolute -top-3\.5.*?Most Popular\s*</div>',
        "",
        card,
        count=1,
        flags=re.S,
    )
    card = card.replace('href="https://claude.ai"', f'href="https://claude.ai/login?plan={name.lower()}"')
    card = card.replace('href="https://claude.ai/login"', f'href="https://claude.ai/login?plan={name.lower()}"')
    raw = raw[: match.start(1)] + card + raw[match.end(1) :]

for before, after in {
    "Chat on web, iOS, Android, and desktop": "Chat on web, iOS, Android, and on your desktop",
    "Annual subscription discount ($28 if billed monthly)": "Per month with annual subscription discount ($280 billed up front). $28 if billed monthly.",
    "Prices exclude applicable taxes. Usage limits, rate caps, and fair use terms apply to all tiers.": "*Usage limits apply. Prices shown don't include applicable tax. Prices and plans are subject to change at Anthropic's discretion.",
}.items():
    raw = raw.replace(before, after)

faq = [
    (
        "What is Claude and how does it work?",
        "Claude is an artificial intelligence, trained by Anthropic using Constitutional AI to be safe, accurate, and secure — the trusted assistant for you to do your best work. You can use Claude for your own personal use or create a Team account to collaborate with your teammates.",
    ),
    (
        "What should I use Claude for?",
        "If you can dream it, Claude can help you do it. Claude can process large amounts of information, brainstorm ideas, generate text and code, help you understand subjects, coach you through difficult situations, simplify your busywork so you can focus on what matters most, and so much more.",
    ),
    (
        "How much does it cost to use?",
        "Claude has five pricing plans available — Free, Pro, Max, Team, and Enterprise. The Free plan offers limited use with no payment required.",
    ),
]
faq_markup = (
    '<section class="claude-faq" aria-labelledby="claude-faq-heading">'
    '<h2 id="claude-faq-heading">FAQ</h2><div class="claude-faq-items">'
    + "".join(
        '<details class="claude-faq-item">'
        f'<summary>{escape(question)}<span aria-hidden="true">+</span></summary>'
        f'<p>{escape(answer)}</p></details>'
        for question, answer in faq
    )
    + "</div></section>"
)
raw = replace_once(raw, r"<!-- FAQ SECTION -->.*?<!-- LARGE PUBLIC ANTHROPIC FOOTER -->", faq_markup + "\n<!-- LARGE PUBLIC ANTHROPIC FOOTER -->")

group_names = [
    ["Products", "Capabilities", "Extensions", "Models"],
    ["Enterprise", "Departments", "Industries", "Programs"],
    ["Developers", "Platform", "Resources", "Help and security"],
    ["Company", "Terms and policies"],
]
groups = {group["heading"]: group["links"] for group in reference["footer"]}


def link_group(name: str) -> str:
    items = "".join(
        f'<li><a href="{escape(link["href"], quote=True)}">{escape(link["text"])}</a></li>'
        for link in groups[name]
    )
    return f'<div class="claude-footer-group"><h3>{escape(name)}</h3><ul>{items}</ul></div>'


footer_columns = "".join(
    '<div class="claude-footer-column">'
    + "".join(link_group(name) for name in names)
    + "</div>"
    for names in group_names
)
footer = (
    '<footer class="claude-footer"><div class="claude-footer-grid">'
    '<div class="claude-footer-brand">'
    f'<a href="https://claude.com/" class="claude-wordmark">{wordmark}</a>'
    '<form action="https://claude.ai" method="get" class="claude-ask-form">'
    '<input name="q" aria-label="Ask Claude" placeholder="How can I help you today?">'
    '<button type="submit" aria-label="Submit">↑</button></form>'
    '<div class="claude-footer-legal"><strong>ANTHROPIC</strong><small>© 2026 Anthropic PBC</small></div>'
    "</div>"
    + footer_columns
    + "</div></footer>"
)
raw = replace_once(raw, r"<!-- LARGE PUBLIC ANTHROPIC FOOTER -->.*?</footer>", footer)

css = """
<style id="claude-official-refinement">
@font-face { font-family: AnthropicSans; src: url('claude-fonts/AnthropicSans_Roman.woff2') format('woff2'); font-display: swap; }
@font-face { font-family: AnthropicSerif; src: url('claude-fonts/AnthropicSerif_Roman.woff2') format('woff2'); font-display: swap; }
* { box-sizing: border-box; }
html, body { width: 100% !important; max-width: none; min-width: 0; }
body { font-family: AnthropicSans, system-ui, sans-serif; background:#141413; }
.serif-title { font-family: AnthropicSerif, Georgia, serif; }
header { padding-inline: max(4.64vw, 24px) !important; }
header .claude-wordmark { display:block; flex:none; width:120px; height:27px; color:#faf9f5; }
.claude-wordmark svg { display:block; width:100%; height:100%; }
header nav { margin-left:160px; gap:24px; }
header nav a { white-space:nowrap; }
body > section:first-of-type { height:632px; min-height:632px; position:relative; border:0; }
body > section:first-of-type > div:first-child { position:absolute; left:113.71px; top:54.59px; width:448px; padding:0; align-items:center; }
body > section:first-of-type h1 { font-family:AnthropicSerif,Georgia,serif; width:max-content; max-width:100%; margin:0 auto; font-size:67.72px; line-height:74.49px; letter-spacing:-0.015em; text-align:center; font-weight:400; }
body > section:first-of-type h1 + p { width:max-content; max-width:100%; margin:16px auto 0; font-size:22.57px; line-height:33.86px; color:#87867f; letter-spacing:0; text-align:center; }
body > section:first-of-type > div:first-child > div:first-of-type { width:448px; min-height:244px; margin-top:32px; padding:28px; border-radius:32px; background:#141413; box-shadow:none; }
body > section:first-of-type > div:first-child > div:first-of-type > a { display:flex; align-items:center; justify-content:center; width:100%; height:46px; border-radius:8px; }
body > section:first-of-type > div:first-child > div:first-of-type > p { font-size:12px; line-height:17px; margin-top:20px; }
body > section:first-of-type > div:first-child > div:last-of-type { margin-top:24px; }
body > section:first-of-type > div:first-child > div:last-of-type a { border-radius:10px; font-size:16px; font-weight:600; }
.claude-hero-video { position:absolute; left:calc(50% + 24px); top:20px; width:556.57px; height:612px; object-fit:cover; border-radius:16px; }
#pricing { padding:128px max(4.64vw,24px) 64px; }
#pricing > div:first-child { max-width:1161.14px; }
#pricing > div:first-child h2 { font-size:49.43px; line-height:59.31px; }
#pricing > div:first-child > div { margin-top:96px; height:44px; }
#pricing > div:nth-child(2) { max-width:1161.14px; margin-top:48px; gap:32px; }
#pricing > div:nth-child(2) > div { min-height:969.5px; background:#1f1e1c; border:1px solid #363532; border-radius:24px; box-shadow:none; }
#pricing > div:nth-child(2) > div h3 { font-size:32px; }
#pricing > div:nth-child(2) > div span[class*="text-[42px]"] { font-size:24px; }
#pricing > div:nth-child(2) > div a[class*="rounded-full"] { border-radius:9px; }
#pricing > div:nth-child(2) > div div[class*="uppercase"] { display:none; }
.claude-plan-icon { width:64px; height:64px; margin-bottom:26px; }
.claude-plan-icon svg { width:100%; height:100%; }
.claude-feature-list { list-style:none; padding:0; margin:0; display:grid; gap:18px; font-size:15px; line-height:1.45; color:#cbc9c4; }
.claude-feature-list li { display:flex; align-items:flex-start; gap:16px; }
.claude-feature-list li span { flex:none; color:#faf9f5; }
.claude-faq { min-height:676px; padding:128px 24px 112px; background:#141413; }
.claude-faq h2 { font:400 49.43px/1.2 AnthropicSerif,Georgia,serif; text-align:center; margin:0 0 60px; }
.claude-faq-items { max-width:662px; margin:auto; }
.claude-faq-item { border-top:1px solid #363532; }
.claude-faq-item summary { list-style:none; cursor:pointer; display:flex; align-items:center; justify-content:space-between; padding:28px 0; font:400 21px/1.4 AnthropicSerif,Georgia,serif; }
.claude-faq-item summary::-webkit-details-marker { display:none; }
.claude-faq-item summary span { font:300 25px AnthropicSans,Arial,sans-serif; color:#aaa9a3; }
.claude-faq-item[open] summary span { transform:rotate(45deg); }
.claude-faq-item p { color:#aaa9a3; font-size:15px; line-height:1.55; padding:0 0 24px; margin:0; }
.claude-footer { background:#141413; border-top:1px solid #30302d; padding:64px max(4.64vw,24px) 32px; color:#faf9f5; min-height:1163px; }
.claude-footer-grid { max-width:1161.14px; margin:auto; display:grid; grid-template-columns:409px repeat(4,minmax(0,1fr)); gap:0; }
.claude-footer-brand { min-height:1090px; display:flex; flex-direction:column; align-items:flex-start; }
.claude-footer-brand .claude-wordmark { display:block; width:145px; height:33px; margin:0 0 46px; }
.claude-ask-form { width:280px; height:48px; border:1px solid #3b3a36; background:#292824; border-radius:12px; display:flex; align-items:center; padding:5px; }
.claude-ask-form input { flex:1; width:0; background:transparent; border:0; color:#faf9f5; outline:none; padding:0 8px; font-size:13px; }
.claude-ask-form button { flex:none; width:30px; height:30px; border-radius:8px; background:#cc785c; color:white; }
.claude-footer-legal { margin-top:auto; display:grid; gap:10px; color:#8e8b87; }
.claude-footer-legal strong { font-size:15px; letter-spacing:.08em; }
.claude-footer-legal small { font-size:12px; }
.claude-footer-group { margin-bottom:42px; }
.claude-footer-group h3 { color:#8e8b87; font-size:13px; font-weight:400; margin:0 0 18px; }
.claude-footer-group ul { list-style:none; padding:0; margin:0; display:grid; gap:14px; }
.claude-footer-group li { font-size:13px; line-height:1.35; padding-right:14px; }
.claude-footer-group a:hover { text-decoration:underline; }
@media (max-width:1100px) {
 header nav { margin-left:40px; gap:12px; }
 header .claude-wordmark { width:100px; }
 .claude-hero-video { left:52%; width:46%; }
 body > section:first-of-type > div:first-child { left:5%; width:42%; }
 body > section:first-of-type > div:first-child > div:first-of-type { width:100%; }
 .claude-footer-grid { grid-template-columns:32% repeat(4,minmax(0,1fr)); }
}
@media (max-width:760px) {
 header { height:64px; padding-inline:20px !important; }
 header nav, header > div:last-child a:nth-child(-n+2) { display:none; }
 body > section:first-of-type { height:auto; min-height:0; padding:60px 20px 0; display:flex; flex-direction:column; }
 body > section:first-of-type > div:first-child { position:static; width:100%; max-width:448px; }
 body > section:first-of-type h1 { font-size:50px; line-height:1.08; }
 body > section:first-of-type h1 + p { font-size:17px; }
 body > section:first-of-type > div:first-child > div:first-of-type { min-height:0; }
 .claude-hero-video { position:static; width:100%; max-width:556px; height:auto; margin:40px auto 0; }
 #pricing { padding:80px 20px; }
 #pricing > div:first-child > div { margin-top:48px; }
 #pricing > div:nth-child(2) { grid-template-columns:1fr; gap:20px; }
 #pricing > div:nth-child(2) > div { min-height:0; }
 .claude-footer-grid { grid-template-columns:repeat(2,minmax(0,1fr)); gap:24px; }
 .claude-footer-brand { min-height:0; grid-column:1 / -1; }
 .claude-footer-legal { margin-top:24px; }
}
</style>
"""
raw = raw.replace("</head>", css + "</head>")
raw = raw.replace(
    '<body class="w-[1280px] bg-[#141413] text-[#f4f3ef] antialiased selection:bg-[#cc785c] selection:text-white">',
    '<body class="bg-[#141413] text-[#f4f3ef] antialiased selection:bg-[#cc785c] selection:text-white">',
)

(ROOT / "claude.html").write_text(raw)
print(f"Wrote claude.html ({len(raw):,} characters) from native Stitch + observed official reference")
