"""Apply observed Taiwan Spotify content to the preserved Stitch screen."""
from pathlib import Path
from html import escape
import hashlib
import json
import sys

root = Path(__file__).parent
region = sys.argv[1] if len(sys.argv) > 1 else 'tw'
if region not in ('tw', 'ca'):
    raise ValueError('Use tw or ca')
reference = json.loads((root / f'spotify-{region}-browser-reference.json').read_text())
screen = (root / 'spotify-base.html').read_text()
section_ids = [
    '0JQ5DB5E8N831KzFzsBBQ2',
    '0JQ5DAnM3wGh0gz1MXnu3C',
    '0JQ5DAnM3wGh0gz1MXnu3B',
    '0JQ5DAnM3wGh0gz1MXnu4h',
    '0JQ5DAzQHECxDlYNI6xD1g',
]

def a(value):
    return escape(value, quote=True)

parts = ['<section class="official-stage"><article class="official-content">']
for index, row in enumerate(reference['sections']):
    title = row['name']
    parts.append(f'<section class="official-row official-row-{index}"><div class="official-heading">')
    parts.append(f'<h2>{a(title)}</h2><a href="https://open.spotify.com/section/{section_ids[index]}">Show all</a></div>')
    parts.append('<div class="official-carousel">')
    for card in row['cards']:
        name, _, description = card['text'].partition('\n\n')
        picture_class = ' official-artist' if index == 1 else ''
        parts.append(f'<a class="official-card" href="{a(card["url"])}" aria-label="{a(name)}">')
        parts.append(f'<span class="official-cover{picture_class}"><img src="{a(card["image"])}" alt="{a(name)}" loading="lazy"><span class="official-play" aria-hidden="true">▶</span></span>')
        if index < 3:
            parts.append(f'<span class="official-name">{a(name)}</span>')
        parts.append(f'<span class="official-description">{a(description)}</span></a>')
    parts.append('</div></section>')

parts.append('<footer class="official-footer"><div class="official-footer-columns">')
for group in reference['footerGroups']:
    parts.append(f'<div><h4>{a(group["title"])}</h4>')
    for link in group['links']:
        parts.append(f'<a href="{a(link["url"])}">{a(link["text"])}</a>')
    parts.append('</div>')
social = [
    ('https://www.instagram.com/spotify/', 'Instagram', '<path d="M8 1.44c2.136 0 2.389.009 3.233.047.78.036 1.203.166 1.485.276.348.128.663.332.921.598.266.258.47.573.599.921.11.282.24.706.275 1.485.039.844.047 1.097.047 3.233s-.008 2.389-.047 3.232c-.035.78-.166 1.204-.275 1.486a2.65 2.65 0 0 1-1.518 1.518c-.282.11-.706.24-1.486.275-.843.039-1.097.047-3.233.047s-2.39-.008-3.232-.047c-.78-.035-1.204-.165-1.486-.275a2.5 2.5 0 0 1-.921-.599 2.5 2.5 0 0 1-.599-.92c-.11-.282-.24-.706-.275-1.486-.038-.844-.047-1.096-.047-3.232s.009-2.39.047-3.233c.036-.78.166-1.203.275-1.485.129-.348.333-.663.599-.921a2.5 2.5 0 0 1 .92-.599c.283-.11.707-.24 1.487-.275.843-.038 1.096-.047 3.232-.047L8 1.441zm.001-1.442c-2.172 0-2.445.01-3.298.048-.854.04-1.435.176-1.943.373a3.9 3.9 0 0 0-1.417.923c-.407.4-.722.883-.923 1.417-.198.508-.333 1.09-.372 1.942S0 5.826 0 8c0 2.172.01 2.445.048 3.298.04.853.174 1.433.372 1.941.2.534.516 1.017.923 1.417.4.407.883.722 1.417.923.508.198 1.09.333 1.942.372s1.126.048 3.299.048 2.445-.01 3.298-.048c.853-.04 1.433-.174 1.94-.372a4.1 4.1 0 0 0 2.34-2.34c.199-.508.334-1.09.373-1.942S16 10.172 16 7.999s-.01-2.445-.048-3.298c-.04-.853-.174-1.433-.372-1.94a3.9 3.9 0 0 0-.923-1.418A3.9 3.9 0 0 0 13.24.42c-.508-.197-1.09-.333-1.942-.371-.851-.041-1.125-.05-3.298-.05z"/><path d="M8 3.892a4.108 4.108 0 1 0 0 8.216 4.108 4.108 0 0 0 0-8.216m0 6.775a2.668 2.668 0 1 1 0-5.335 2.668 2.668 0 0 1 0 5.335m4.27-5.978a.96.96 0 1 0 0-1.92.96.96 0 0 0 0 1.92"/>'),
    ('https://x.com/spotify', 'X', '<path d="M9.303 6.928 14.403 1h-1.208L8.766 6.147 5.23 1H1.15L6.5 8.784 1.15 15h1.208l4.676-5.436L10.77 15h4.08zM7.648 8.852l-.542-.775L2.795 1.91H4.65l3.48 4.977.541.775 4.523 6.47H11.34l-3.691-5.28Z"/>'),
    ('https://www.facebook.com/Spotify', 'Facebook', '<path d="M16 8a8 8 0 1 0-9.25 7.903v-5.59H4.719V8H6.75V6.237c0-2.005 1.194-3.112 3.022-3.112.875 0 1.79.156 1.79.156V5.25h-1.008c-.994 0-1.304.617-1.304 1.25V8h2.219l-.355 2.313H9.25v5.59A8 8 0 0 0 16 8"/>'),
]
parts.append('</div><div class="official-social">')
for url, label, paths in social:
    parts.append(f'<a href="{url}" aria-label="{label}"><svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">{paths}</svg></a>')
parts.append('</div>')
parts.append('<p>© 2026 Spotify AB</p></footer></article></section>')

start = screen.index('<section class="flex-1 h-[574px]')
end = screen.index('</section>\n</main>', start) + len('</section>')
screen = screen[:start] + ''.join(parts) + screen[end:]

style = '''
#reference-replica .official-stage{flex:none;width:922px;height:574px;overflow-y:auto;overflow-x:hidden;scrollbar-width:none;background:#121212;border-radius:8px;position:relative}
#reference-replica .official-content{padding:23px 40px 0;background:linear-gradient(#222 0,#121212 280px);min-height:100%}
#reference-replica .official-row{height:299.727px}
#reference-replica .official-row-0{height:350.789px}
#reference-replica .official-row-1{height:304.727px}
#reference-replica .official-row-2{height:330.727px}
#reference-replica .official-row-3{height:301.727px}
#reference-replica .official-heading{height:29px;display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;padding-right:8px}
#reference-replica .official-heading h2{font-family:'SpotifyMixUITitle','SpotifyMixUI',sans-serif;font-size:24px;font-weight:700;line-height:29px;letter-spacing:0}
#reference-replica .official-heading a{font-size:14px;font-weight:700;color:#b3b3b3}
#reference-replica .official-carousel{display:flex;gap:24px;width:calc(100% + 40px);overflow-x:auto;scrollbar-width:none;padding-bottom:12px}
#reference-replica .official-card{display:block;flex:none;width:153.73px;text-decoration:none}
#reference-replica .official-cover{display:block;width:153.73px;height:153.73px;position:relative}
#reference-replica .official-cover img{display:block;width:100%;height:100%;object-fit:cover;border-radius:4px}
#reference-replica .official-cover.official-artist img{border-radius:50%}
#reference-replica .official-play{display:none;position:absolute;right:8px;bottom:8px;width:48px;height:48px;border-radius:50%;background:#1ed760;color:#000;align-items:center;justify-content:center}
#reference-replica .official-card:hover .official-play{display:flex}
#reference-replica .official-name{display:-webkit-box;-webkit-box-orient:vertical;-webkit-line-clamp:2;overflow:hidden;margin-top:8px;color:#fff;font-size:16px;font-weight:400;line-height:normal}
#reference-replica .official-description{display:-webkit-box;-webkit-box-orient:vertical;-webkit-line-clamp:2;overflow:hidden;margin-top:4px;color:#b3b3b3;font-size:14px;line-height:21px}
#reference-replica .official-row-3 .official-description,#reference-replica .official-row-4 .official-description{margin-top:8px}
#reference-replica .official-footer{position:relative;margin:86px -16px 0;width:calc(100% + 32px);padding:39px 0 40px}
#reference-replica .official-footer:before{content:'';position:absolute;left:0;right:0;top:-26px;border-top:1px solid #292929}
#reference-replica .official-footer-columns{display:flex;gap:24px;width:722px}
#reference-replica .official-footer-columns>div{width:144.4px;flex:none}
#reference-replica .official-footer h4{font-size:16px;font-weight:700;line-height:24px;margin:0 0 8px}
#reference-replica .official-footer-columns a{display:block;color:#b3b3b3;font-size:16px;line-height:22px;margin-bottom:8px}
#reference-replica .official-social{display:flex;gap:16px;position:absolute;right:0;top:39px}
#reference-replica .official-social a{width:40px;height:40px;display:flex;align-items:center;justify-content:center;border-radius:50%;background:#292929;color:#fff}
#reference-replica .official-footer>p{margin-top:40px;border-top:1px solid #292929;padding-top:40px;text-align:right;color:#b3b3b3;font-size:14px}
#reference-replica .official-stage a:hover{text-decoration:underline}
#reference-replica .language{margin-top:28px}
#reference-replica>footer{border-radius:16px!important;padding:0 16px!important}
#reference-replica>footer>a{width:154px;height:48px}
'''
if region == 'ca':
    style = style.replace('.official-row-3{height:301.727px}', '.official-row-3{height:303.727px}')
screen = screen.replace('</head>', '<style>' + style + '</style></head>')
if region == 'ca':
    for old, new in {
        'https://www.spotify.com/legal/privacy-policy/': 'https://www.spotify.com/ca-en/legal/privacy-policy/',
        'https://www.spotify.com/legal/cookies-policy/': 'https://www.spotify.com/ca-en/legal/cookies-policy/',
        'https://www.spotify.com/safety-and-privacy-center/': 'https://www.spotify.com/ca-en/safetyandprivacy/',
        'https://www.spotify.com/accessibility/': 'https://www.spotify.com/ca-en/accessibility/',
        'https://www.spotify.com/legal/': 'https://www.spotify.com/ca-en/legal/',
    }.items():
        screen = screen.replace(old, new)
    screen = screen.replace(
        '<a href="https://www.spotify.com/ca-en/legal/privacy-policy/">About Ads</a>',
        '<a href="https://www.spotify.com/ca-en/legal/privacy-policy/#s3">About Ads</a>',
    )
    screen = screen.replace(
        '<a class="cookies-link" href="https://www.spotify.com/ca-en/legal/cookies-policy/">Cookies</a>',
        '<a class="cookies-link" href="https://www.spotify.com/legal/cookies-policy/">Cookies</a>',
    )
(root / ('spotify.html' if region == 'tw' else 'spotify-ca.html')).write_text(screen)
metadata = json.loads((root / 'spotify-refinements.json').read_text())
metadata.update({
    'reference_region': 'Taiwan' if region == 'tw' else 'Canada',
    'reference_observed_at': reference['observedAt'],
    'observed_card_count': sum(len(row['cards']) for row in reference['sections']),
    'status': 'in_visual_review',
    'refined_sha256': hashlib.sha256(screen.encode()).hexdigest(),
    'remaining': [f'Visual comparison of complete {"Taiwan" if region == "tw" else "Canada"} page', 'Responsive comparison', 'Navigation and buttons', 'Capture refined screenshot for catalog'],
})
(root / ('spotify-refinements.json' if region == 'tw' else 'spotify-ca-refinements.json')).write_text(json.dumps(metadata, indent=2, ensure_ascii=False))
