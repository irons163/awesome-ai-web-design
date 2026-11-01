#!/usr/bin/env python3
"""Prepare review-only previews from the preserved Stitch ZIP exports.

The original exports remain untouched in .test-artifacts. These outputs are
not publication-ready until their actual interaction and responsive checks pass.
"""
import base64
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / '.test-artifacts/five-third-designs-2026-11-01'
OUTPUT = WORK / 'review-previews'


def svg_data(svg):
    return 'data:image/svg+xml;base64,' + base64.b64encode(svg.encode()).decode()


AVATAR = svg_data('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="32" fill="#dce6ec"/><circle cx="32" cy="24" r="11" fill="#56717d"/><path d="M12 58c2-13 10-19 20-19s18 6 20 19" fill="#56717d"/></svg>')
LAPTOP = svg_data('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 520"><defs><linearGradient id="g" x2="1" y2="1"><stop stop-color="#e9f4ff"/><stop offset="1" stop-color="#b9d3ed"/></linearGradient></defs><rect width="800" height="520" fill="url(#g)"/><rect x="176" y="96" width="448" height="276" rx="18" fill="#1d3042"/><rect x="188" y="108" width="424" height="252" rx="7" fill="#bad7ef"/><path d="M207 327 330 196l81 81 72-100 111 150" fill="none" stroke="#327fc2" stroke-width="14"/><path d="M151 386h498l-29 30H180z" fill="#667e92"/><path d="M341 386h118l-8 9H349z" fill="#dae5ed"/></svg>')
GLOBE = svg_data('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300"><circle cx="150" cy="150" r="132" fill="#1e2d3e" stroke="#80a9e7" stroke-width="4"/><circle cx="150" cy="150" r="112" fill="none" stroke="#6c91c5" stroke-width="2"/><ellipse cx="150" cy="150" rx="57" ry="112" fill="none" stroke="#6c91c5" stroke-width="2"/><path d="M40 150h220M55 95h190M55 205h190M150 38v224" fill="none" stroke="#6c91c5" stroke-width="2"/><circle cx="150" cy="150" r="24" fill="#a6c8f5"/><path d="m150 110 8 26 27 14-27 14-8 26-8-26-27-14 27-14z" fill="#edf5ff"/></svg>')
LOGO = svg_data('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="18" fill="#425b4b"/><path d="M14 40 32 15l18 25-18 10z" fill="#f3e4ba"/><circle cx="32" cy="32" r="6" fill="#425b4b"/></svg>')
TRAVEL = svg_data('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500"><rect width="800" height="500" fill="#dcecef"/><circle cx="625" cy="110" r="62" fill="#f5c66a"/><path d="M0 390 210 150 390 350 530 210 800 420v80H0z" fill="#78a39d"/><path d="M0 440 200 260 380 430 545 285 800 440v60H0z" fill="#396d71"/><path d="M315 500 455 370 560 500" fill="#e7d7af"/></svg>')
ICONS = {
    'cottage':'⌂','location_on':'●','nature_people':'♧','timelapse':'◷','travel_explore':'⌕','alt_route':'⇄','arrow_back':'←','auto_fix_high':'✦','brush':'✎','chat_bubble':'▰','crop':'⊞','edit':'✎','exposure':'◐','favorite':'♥','favorite_border':'♡','gesture':'⌁','grid_goldenratio':'▦','groups':'●','meeting_room':'▣','near_me':'➤','notifications':'●','play_circle':'▶','recommend':'✦','schedule':'◷','school':'▤','screen_share':'▣','share':'↗','sort':'☷','video_camera_front':'▣','videocam':'▣','view_in_ar':'◇','visibility':'◉','volume_off':'◌','volume_up':'♪','account_circle':'●','account_balance':'▥','arrow_drop_down':'⌄','arrow_downward':'↓','arrow_outward':'↗','add_reaction':'☺','add_shopping_cart':'+','bookmark':'▣','bookmark_added':'✓','bookmark_border':'▢','cabin':'⌂','coffee':'☕','crop_free':'▢','dataset':'▦','delete':'×','delete_sweep':'×','eco':'✿','edit_note':'✎','filter_alt':'☷','forest':'♠','format_size':'Aa','group':'●','handyman':'⚒','help_outline':'?','history_edu':'◷','inventory_2':'▣','lightbulb':'✦','local_cafe':'☕','mode_fan':'✣','north_east':'↗','production_quantity_limits':'▢','send':'➤','spa':'✿','splitscreen':'▥','straight':'↑','sync_alt':'⇄','tips_and_updates':'✦','track_changes':'◎','translate':'文','volume_up':'♪','wallet':'▣','code':'⌘','account_tree':'⑂','accessibility_new':'♿','add':'+','api':'⌘','arrow_forward':'→',
    'auto_awesome':'✦','battery_charging_full':'▰','bolt':'ϟ','call_split':'⑂','check':'✓',
    'check_circle':'✓','chevron_left':'‹','chevron_right':'›','close':'×','cloud':'☁',
    'cloud_sync':'☁','commit':'●','content_copy':'⧉','dark_mode':'◐','description':'▤',
    'desktop_windows':'▣','developer_board':'▦','developer_mode':'⌘','devices':'▣','dns':'▤',
    'draw':'✎','east':'→','expand_more':'⌄','explore':'◇','filter_list':'☰','fitness_center':'◈',
    'graphic_eq':'▥','grid_view':'▦','hd':'HD','high_quality':'HQ','history':'↺','home':'⌂',
    'hourglass_empty':'⌛','hub':'✣','info':'ⓘ','insights':'⌁','keyboard_arrow_down':'⌄',
    'language':'◎','laptop_mac':'▱','local_fire_department':'✦','lock':'◉','lock_open':'◌',
    'memory':'▣','menu':'☰','menu_book':'▤','mic':'◉','more_vert':'⋮','movie_filter':'▷',
    'offline_bolt':'ϟ','palette':'◈','passkey':'⚿','person':'●','play_arrow':'▶','public':'◎',
    'restart_alt':'↻','rocket_launch':'↗','screen_rotation':'↻','search':'⌕','search_insights':'⌕',
    'search_off':'⌕','security':'◇','settings':'⚙','shield':'◇','smart_display':'▷','smart_toy':'✦',
    'speed':'◴','subscriptions':'▣','task_alt':'✓','terminal':'›_','thermostat':'◉','timer':'◷',
    'touch_app':'◉','trending_down':'↘','tune':'☷','verified':'✓','verified_user':'✓',
    'video_library':'▣','visibility_off':'◌','west':'←',
}


def clean_html(slug, source):
    html = source
    css_file = ROOT / 'data/new-studies/styles' / f'{slug}-tailwind.css'
    if not css_file.is_file():
        raise FileNotFoundError(f'先從實際執行的 Stitch 畫面保存樣式：{css_file}')
    generated_css = css_file.read_text()
    if len(generated_css) < 5000:
        raise ValueError(f'{slug}: generated styles are incomplete')
    # Capture the actual utility stylesheet rather than requiring a runtime CDN.
    html, count = re.subn(r'<script\b[^>]*src="https://cdn\.tailwindcss\.com"[^>]*>\s*</script>',
                          lambda _: '<style>' + generated_css + '</style>', html, count=1)
    if count != 1:
        raise ValueError(f'{slug}: missing Tailwind source')
    html, count = re.subn(r'<script\b[^>]*>\s*tailwind\.config\s*=.*?</script>', '', html,
                          count=1, flags=re.S)
    if count != 1:
        raise ValueError(f'{slug}: missing Tailwind configuration')
    html = re.sub(r'<link\b[^>]*href="https://fonts\.(?:googleapis|gstatic)\.com[^>]*>', '', html)
    # Replace broken remote image URLs with original, local vector artwork.
    def image(match):
        tag = match.group(0)
        replacement = TRAVEL if slug == 'booking' and 'Logo' not in tag else LOGO
        return re.sub(r'src="https://lh3\.googleusercontent\.com/[^"]+"', 'src="' + replacement + '"', tag)
    html = re.sub(r'<img\b[^>]*src="https://lh3\.googleusercontent\.com/[^"]+"[^>]*>', image, html)
    if slug == 'booking':
        html = re.sub(r'https://lh3\.googleusercontent\.com/[^\"\']+', TRAVEL, html)
    # Stitch's icon font is remote; use local text symbols so failed font loads
    # do not expose long ligature names or break the mobile layout.
    def icon(match):
        name = match.group(2).strip()
        if name.startswith('${'): return match.group(0)
        if name not in ICONS:
            raise ValueError(f'{slug}: unmapped icon {name}')
        return match.group(1) + ICONS[name] + match.group(3)
    html = re.sub(r'(<span\b[^>]*class="[^"]*material-symbols-outlined[^"]*"[^>]*>)\s*([^<>]+?)\s*(</span>)', icon, html)
    for old, new in [('textContent = \'add\'', "textContent = '+'"),
                     ('textContent = \'close\'', "textContent = '×'"),
                     ('textContent = \'check\'', "textContent = '✓'")]:
        html = html.replace(old, new)
    html = html.replace('</head>', '<style>.material-symbols-outlined{font-family:system-ui,sans-serif!important;line-height:1;font-style:normal}</style></head>', 1)
    if slug == 'bbc':
        html = html.replace('（中央研究院當代思想研究室客座學者）','（虛構作者，僅供版面示範）')
    if slug == 'twitch':
        html = html.replace('特戰英豪','原創競技遊戲').replace('機戰傭兵VI','原創機甲遊戲')
    if slug == 'adobe':
        html = html.replace('</head>', '<style>@media(max-width:600px){#categoryPillContainer button{flex-shrink:0;white-space:nowrap}}</style></head>',1)
        html = html.replace('以極致流暢的零延遲本機架構，賦予每道靈感即刻成真的力量。','以下是使用範例資料製作的介面示範。')
    if slug == 'zoom':
        html = html.replace('連線正常：延遲 < 14ms','示範畫面：未連接會議')
    # Render dynamic icon names as symbols too.
    for name, symbol in ICONS.items():
        html = html.replace('>' + name + '</span>', '>' + symbol + '</span>')
    banner = ('<div role="note" style="position:fixed;bottom:0;left:0;right:0;z-index:9999;padding:8px 16px;'
              'background:#202721;color:#fff;text-align:center;font:14px/1.5 system-ui,sans-serif">'
              '設計示範：品牌、內容與互動皆為範例，不提供實際服務。</div>')
    html, count = re.subn(r'(<body\b[^>]*>)', r'\1' + banner, html, count=1, flags=re.I)
    if count != 1:
        raise ValueError(f'{slug}: missing body')
    return html


def main():
    OUTPUT.mkdir(exist_ok=True)
    for slug in ('adobe', 'bbc', 'twitch', 'zoom', 'booking'):
        if not (WORK / f'{slug}-stitch.zip').exists(): continue
        with zipfile.ZipFile(WORK / f'{slug}-stitch.zip') as archive:
            html = archive.read('code.html').decode('utf-8')
        (OUTPUT / f'{slug}.html').write_text(clean_html(slug, html))
        print(slug, 'prepared for local review')


if __name__ == '__main__':
    main()
