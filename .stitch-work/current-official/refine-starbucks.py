#!/usr/bin/env python3
"""Correct the native Stitch output with the saved 2026-09-22 Starbucks HTML.

The generated HTML and screenshot stay unchanged for provenance. This is still a
dated draft; there is no accepted live desktop or mobile visual comparison.
"""
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin
import re

ROOT = Path(__file__).resolve().parent
source = (ROOT / 'starbucks-source.html').read_text()
html = (ROOT / 'starbucks-stitch.html').read_text()


def once(old: str, new: str) -> None:
    global html
    assert html.count(old) == 1, old[:100]
    html = html.replace(old, new, 1)


class FooterLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sections = {}
        self.current = None
        self.heading = None
        self.anchor = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'h2':
            self.heading = []
        elif tag == 'a' and self.current:
            self.anchor = [attrs.get('href', ''), []]

    def handle_data(self, data):
        if self.heading is not None:
            self.heading.append(data)
        if self.anchor is not None:
            self.anchor[1].append(data)

    def handle_endtag(self, tag):
        if tag == 'h2' and self.heading is not None:
            label = ' '.join(' '.join(self.heading).split())
            self.heading = None
            if label in self.sections:
                self.current = None  # Desktop repeats each mobile group.
            elif label:
                self.current = label
                self.sections[label] = []
        elif tag == 'a' and self.anchor is not None:
            href, chunks = self.anchor
            label = ' '.join(' '.join(chunks).split())
            if href and label:
                self.sections[self.current].append((label, urljoin('https://www.starbucks.com/', href)))
            self.anchor = None


# Use the actual siren mark embedded in the saved official page.
logo_start = source.index('<svg', source.index('<a aria-label="Home, Starbucks"'))
logo_end = source.index('</svg>', logo_start) + len('</svg>')
official_logo = source[logo_start:logo_end]
fake_logo = re.search(r'<svg class="w-13 h-13.*?</svg>', html, re.S)
assert fake_logo
html = html[:fake_logo.start()] + official_logo + html[fake_logo.end():]
once('<a aria-label="Starbucks Home" class="flex-shrink-0"',
     '<a aria-label="Home, Starbucks" class="flex-shrink-0 official-logo"')

# Stitch replaced each requested brand image with a placeholder. The three
# downloaded files are the exact URLs referenced in the saved official HTML.
placeholder = 'https://www.gstatic.com/labs-code/stitch/stitch-placeholder-300x300.svg'
for name, alt in (
    ('137-112587', 'Four fall drinks on a table with hints of people gathered around them.'),
    ('137-112658', 'Two illustrated Peanuts™ branded Starbucks® gift cards.'),
    ('137-112524', 'A close-up of steamed milk being poured into a Gibraltar glass—the final touches of a cortado.'),
):
    assert (ROOT / 'starbucks-assets' / f'{name}.jpg').is_file()
    assert f'https://content-prod-live.cert.starbucks.com/binary/v2/asset/{name}.jpg' in source
    assert f'src="{placeholder}"' in html
    html = html.replace(f'src="{placeholder}"', f'src="starbucks-assets/{name}.jpg"', 1)
    image = re.search(rf'<img[^>]+src="starbucks-assets/{name}\.jpg"[^>]*/>', html)
    assert image
    original = image.group()
    html = html.replace(original, re.sub(r'alt="[^"]*"', f'alt="{escape(alt, quote=True)}"', original), 1)
assert placeholder not in html

# Restore source-backed wording and hierarchy.
once('It’s a great day for coffee', "It's a great day for coffee")
once('<h1 class="text-3xl sm:text-4xl lg:text-[44px]',
     '<h2 class="text-3xl sm:text-4xl lg:text-[44px]')
once('Fall is here. Cue the hits.\n          </h1>',
     'Fall is here. Cue the hits.\n          </h2>')
once('class="w-full bg-[#32462f] text-white py-8 px-4 text-center"',
     'class="official-announcement w-full bg-[#32462f] text-white py-8 px-4 text-center"')
once('class="w-full bg-white border-b border-gray-200 sticky top-0 z-50"',
     'class="w-full bg-white border-b border-gray-200 z-50"')

# Keep the actual source link groups; discard the generated historical links
# and the invented Spotify social link.
footer = FooterLinks()
footer.feed(source[source.index('<footer'):])
expected = ('About Us', 'Careers', 'Social Impact', 'For Business Partners', 'Ways to Shop')
assert tuple(footer.sections) == expected, tuple(footer.sections)
assert [len(footer.sections[x]) for x in expected] == [7, 6, 4, 4, 6]
groups = []
for title in expected:
    links = ''.join(f'<li><a href="{escape(url, quote=True)}">{escape(label)}</a></li>'
                    for label, url in footer.sections[title])
    groups.append(f'<section><h2>{escape(title)}</h2><ul>{links}</ul></section>')
legal = [
    ('Privacy Notice', 'https://www.starbucks.com/terms/privacy-notice/'),
    ('Consumer Health Privacy Notice', 'https://www.starbucks.com/consumer-health-data-privacy-notice/'),
    ('Terms of Use', 'https://www.starbucks.com/terms/starbucks-terms-of-use/'),
    ('Do Not Sell or Share My Personal Information', 'https://www.starbucks.com/personal-information'),
    ('Accessibility', 'https://www.starbucks.com/about-us/accessibility/'),
]
for label, url in legal:
    assert f'href="{url}"' in source and label in source
legal_html = ''.join(f'<a href="{escape(url, quote=True)}">{escape(label)}</a>' for label, url in legal)
new_footer = ('<footer class="official-footer"><div class="official-footer-inner">'
              '<nav aria-label="Global footer" class="official-footer-grid">' + ''.join(groups) + '</nav>'
              '<nav aria-label="Legal" class="official-legal">' + legal_html + '</nav>'
              '<p>© 2026 Starbucks Coffee Company. All rights reserved.</p>'
              '</div></footer>')
html, count = re.subn(r'<footer\b.*?</footer>', lambda _: new_footer, html, count=1, flags=re.S)
assert count == 1

extra_css = '''<style>
.official-logo svg{display:block;width:52px;height:52px}
.official-announcement{max-width:1440px;margin:0 auto}
.official-footer{background:#fff;border-top:1px solid #ddd;box-shadow:0 -2px 5px #00000010;padding:42px 24px 38px;margin-top:32px;color:#212121}
.official-footer-inner{max-width:1360px;margin:auto}
.official-footer-grid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:28px;padding-bottom:34px;border-bottom:1px solid #ddd}
.official-footer-grid h2{font-size:18px;font-weight:500;margin:0 0 24px}
.official-footer-grid ul{list-style:none;padding:0;margin:0}
.official-footer-grid li{margin:0 0 14px}
.official-footer-grid a,.official-legal a{color:#555;text-decoration:none;font-size:14px;line-height:1.5}
.official-footer-grid a:hover,.official-legal a:hover{text-decoration:underline;color:#111}
.official-legal{display:flex;flex-wrap:wrap;gap:12px 22px;padding:28px 0 14px}
.official-footer p{font-size:13px;color:#6b6b6b;margin:0}
main>div>section{min-height:0}
main>div>section>div:has(>img){aspect-ratio:12/7;min-height:0}
main>div>section>div:has(>img) img{object-fit:cover}
main>div>section>div:not(:has(>img)){min-height:0}
@media(max-width:850px){.official-footer-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:767px){.official-footer-grid{grid-template-columns:1fr}.official-footer-grid section{border-bottom:1px solid #ddd;padding-bottom:12px}.official-footer-grid ul{display:none}.official-footer-grid h2{margin:0}main>div>section>div:has(>img){aspect-ratio:12/7}}
</style>'''
once('</head>', extra_css + '</head>')

for value in ('Fall is here. Cue the hits.', 'Great Pumpkin, great gift', 'Nondairy. No extra.'):
    assert value in source and value in html
assert html.count('starbucks-assets/') == 3
assert 'https://spotify.com' not in html
(ROOT / 'starbucks.html').write_text(html)
print('Wrote source-grounded Starbucks draft:', len(html), 'characters')
