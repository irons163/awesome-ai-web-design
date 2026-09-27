#!/usr/bin/env python3
"""Refine the OpenCode Stitch draft with a dated, source-backed page snapshot."""

import json
import re
from html import escape, unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / '.stitch-work' / 'current-official'
ASSETS = ROOT / 'opencode.ai-assets'

STYLESHEETS = (
    'entry-client-VF7ouASi.css',
    'index-C1kvjbTM.css',
    'footer-BBCO41N-.css',
    'language-picker-pPcoMiyM.css',
    'dropdown-BwAG2emZ.css',
)
FONTS = (
    'IBMPlexMono-Regular-Latin1-BsnL3gsb.woff2',
    'IBMPlexMono-Medium-Latin1-DBHUbp12.woff2',
    'IBMPlexMono-Bold-Latin1-K_Zucu9w.woff2',
)
COMMANDS = {
    'curl': 'curl -fsSL https://opencode.ai/v2/install | bash',
    'npm': 'npm install -g @opencode/cli',
    'bun': 'bun install -g --trust @opencode/cli',
    'brew': 'brew install anomalyco/tap/opencode-v2',
    'paru': 'paru -S opencode-beta',
    'yay': 'yay -S opencode-beta',
}
FAQ = {
    'What is OpenCode?': "OpenCode is an open source agent that helps you write and run code with any AI model. It's available as a terminal-based interface, desktop app, or IDE extension.",
    'How do I use OpenCode?': 'The easiest way to get started is to read the intro.',
    'Do I need extra AI subscriptions to use OpenCode?': 'Not necessarily, OpenCode comes with a set of free models that you can use without creating an account. Aside from these, you can use any of the popular coding models by creating a Zen account. While we encourage users to use Zen, OpenCode also works with all popular providers such as OpenAI, Anthropic, xAI etc. You can even connect your local models.',
    'Can I use my existing AI subscriptions with OpenCode?': 'Yes, OpenCode supports subscription plans from all major providers. You can use your Claude Pro/Max, ChatGPT Plus/Pro, or GitHub Copilot subscriptions. Learn more.',
    'Can I only use OpenCode in the terminal?': 'Not anymore! OpenCode is now available as an app for your desktop and web!',
    'How much does OpenCode cost?': 'OpenCode is 100% free to use. It also comes with a set of free models. There might be additional costs if you connect any other provider.',
    'What about data and privacy?': 'Your data and information is only stored when you use our free models or create sharable links. Learn more about our models and share pages.',
    'Is OpenCode open source?': 'Yes, OpenCode is fully open source. The source code is public on GitHub under the MIT License, meaning anyone can use, modify, or contribute to its development. Anyone from the community can file issues, submit pull requests, and extend functionality.',
}

for name in (*STYLESHEETS, *FONTS, 'logo-dark.svg', 'logo-light.svg',
             'opencode-poster-CbUiDHgA.png', 'opencode-min-CiEsORKQ.mp4'):
    if not (ASSETS / name).is_file():
        raise FileNotFoundError(name)

# Keep the downloaded stylesheets untouched as evidence. The local derivatives
# resolve the observed Latin-1 fonts locally and other font subsets against the
# original, versioned OpenCode asset URLs.
for name in STYLESHEETS:
    css = (ASSETS / name).read_text()
    css = css.replace('url("/_build/assets/',
                      'url("https://opencode.ai/_build/assets/')
    for font in FONTS:
        css = css.replace('https://opencode.ai/_build/assets/' + font, font)
    (ASSETS / ('local-' + name)).write_text(css)

page = (ROOT / 'opencode.ai-source-current.html').read_text()
page = re.sub(r'<script\b[^>]*>.*?</script>', '', page, flags=re.S | re.I)
page = re.sub(r'<link\b[^>]*rel="modulepreload"[^>]*>', '', page, flags=re.I)
page = re.sub(r'<link\b[^>]*rel="manifest"[^>]*>', '', page, flags=re.I)
page = re.sub(r'<link\b[^>]*rel="canonical"[^>]*>', '', page, flags=re.I)
page = re.sub(r'<link\b[^>]*rel="alternate"[^>]*>', '', page, flags=re.I)
for stylesheet in STYLESHEETS:
    page = page.replace('/_build/assets/' + stylesheet,
                        'opencode.ai-assets/local-' + stylesheet)
for name in FONTS:
    preload = (f'<link rel="preload" as="font" type="font/woff2" crossorigin '
               f'href="opencode.ai-assets/{name}">')
    page = page.replace('</head>', preload + '</head>', 1)

page = page.replace('/_build/assets/opencode-min-CiEsORKQ.mp4',
                    'opencode.ai-assets/opencode-min-CiEsORKQ.mp4')
page = page.replace('/_build/assets/opencode-poster-CbUiDHgA.png',
                    'opencode.ai-assets/opencode-poster-CbUiDHgA.png')
for variant in ('light', 'dark'):
    pattern = r'(data-slot="logo ' + variant + r'" src=")[^"]+(" alt="OpenCode")'
    page, n = re.subn(pattern,
                      lambda m: m.group(1) + 'opencode.ai-assets/logo-' + variant + '.svg' + m.group(2),
                      page, count=1)
    assert n == 1, variant

# Favicon and navigation still go to the official service. This draft has no
# account backend; the observed waitlist form submits to OpenCode itself.
page = page.replace('href="/favicon-v3.ico"',
                    'href="opencode.ai-assets/favicon-v3.ico"')
page = re.sub(r'(<a\b[^>]*?\bhref=")/([^"]*)"',
              lambda m: m.group(1) + 'https://opencode.ai/' + m.group(2) + '"',
              page, flags=re.S | re.I)
page = re.sub(r'(<form\b[^>]*?\baction=")/([^"]*)"',
              lambda m: m.group(1) + 'https://opencode.ai/' + m.group(2) + '"',
              page, flags=re.S | re.I)


def add_faq_answer(match):
    button = match.group(0)
    name_match = re.search(r'data-slot="faq-question-text">([^<]+)<', button)
    if not name_match:
        return button
    question = unescape(name_match.group(1).strip())
    if question not in FAQ:
        raise ValueError(f'Unexpected official FAQ: {question}')
    return button + (f'<div data-slot="faq-answer" hidden>'
                     f'{escape(FAQ[question])}</div>')


page, count = re.subn(
    r'<button\b[^>]*data-slot="faq-question"[^>]*>.*?</button>',
    add_faq_answer, page, flags=re.S | re.I,
)
assert count == len(FAQ), count

enhancements = r'''<style>
[data-slot="faq-answer"][hidden]{display:none!important}
[data-slot="command"]{cursor:pointer}
.draft-mobile-menu[hidden]{display:none!important}
.draft-mobile-menu{position:fixed;top:80px;left:0;right:0;bottom:0;z-index:90;background:#131010;padding:24px 20px;overflow:auto}
.draft-mobile-menu a{display:block;color:#f2eded;text-decoration:none;padding:22px 0;font-size:16px}
[data-component="nav-mobile-toggle"][aria-expanded="true"] .icon-hamburger{display:none}
[data-component="nav-mobile-toggle"][aria-expanded="true"]:after{content:"×";font:28px/1 sans-serif;color:#b8b2b2}
@media(min-width:961px){.draft-mobile-menu{display:none!important}}
</style><div id="nav-mobile-menu" class="draft-mobile-menu" hidden>
<a href="https://opencode.ai/">Home</a>
<a href="https://github.com/anomalyco/opencode/tree/v2">GitHub</a>
<a href="https://opencode.ai/v2/docs">Docs</a>
<a href="https://opencode.ai/data">Data</a>
<a href="https://opencode.ai/zen">Zen</a>
<a href="https://opencode.ai/go">Go</a>
<a href="https://opencode.ai/enterprise">Enterprise</a>
<a href="https://opencode.ai/download">Get started for free</a>
</div><script>
const commands = COMMANDS_JSON;
const tabs = document.querySelector('[data-component="tabs"]');
const commandText = document.querySelector('[data-slot="command-script"]');
document.querySelectorAll('[role="tab"][data-key]').forEach(tab => tab.addEventListener('click', () => {
  const key = tab.dataset.key;
  tabs.dataset.active = key;
  document.querySelectorAll('[role="tab"][data-key]').forEach(other => {
    other.setAttribute('aria-selected', String(other === tab));
    if (other === tab) other.setAttribute('data-selected', '');
    else other.removeAttribute('data-selected');
  });
  commandText.textContent = commands[key];
}));
document.querySelector('[data-slot="command"]').addEventListener('click', () => {
  navigator.clipboard?.writeText(commands[tabs.dataset.active]);
});
document.querySelectorAll('[data-slot="faq-question"]').forEach(button => {
  button.addEventListener('click', () => {
    const item = button.closest('[data-slot="faq-item"]');
    const answer = item.querySelector('[data-slot="faq-answer"]');
    const isOpen = button.getAttribute('aria-expanded') === 'true';
    button.setAttribute('aria-expanded', String(!isOpen));
    answer.hidden = isOpen;
    if (isOpen) {
      item.setAttribute('data-closed', ''); button.setAttribute('data-closed', '');
      item.removeAttribute('data-open'); button.removeAttribute('data-open');
    } else {
      item.setAttribute('data-open', ''); button.setAttribute('data-open', '');
      item.removeAttribute('data-closed'); button.removeAttribute('data-closed');
    }
  });
});
const mobileToggle = document.querySelector('[data-component="nav-mobile-toggle"]');
const mobileMenu = document.getElementById('nav-mobile-menu');
mobileToggle?.addEventListener('click', () => {
  const open = mobileMenu.hidden;
  mobileMenu.hidden = !open;
  mobileToggle.setAttribute('aria-expanded', String(open));
  mobileToggle.querySelector('.sr-only').textContent = open ? 'Close menu' : 'Open menu';
});
</script>'''.replace('COMMANDS_JSON', json.dumps(COMMANDS, ensure_ascii=False))
page = page.replace('</body>', enhancements + '</body>', 1)

(ROOT / 'opencode.ai.html').write_text(page)
print(f'Wrote {ROOT / "opencode.ai.html"} ({len(page)} characters)')
