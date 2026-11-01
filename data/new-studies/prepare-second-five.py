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
WORK = ROOT / '.test-artifacts/five-more-designs-2026-11-01'
OUTPUT = WORK / 'review-previews'


def svg_data(svg):
    return 'data:image/svg+xml;base64,' + base64.b64encode(svg.encode()).decode()


AVATAR = svg_data('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="32" fill="#dce6ec"/><circle cx="32" cy="24" r="11" fill="#56717d"/><path d="M12 58c2-13 10-19 20-19s18 6 20 19" fill="#56717d"/></svg>')
LAPTOP = svg_data('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 520"><defs><linearGradient id="g" x2="1" y2="1"><stop stop-color="#e9f4ff"/><stop offset="1" stop-color="#b9d3ed"/></linearGradient></defs><rect width="800" height="520" fill="url(#g)"/><rect x="176" y="96" width="448" height="276" rx="18" fill="#1d3042"/><rect x="188" y="108" width="424" height="252" rx="7" fill="#bad7ef"/><path d="M207 327 330 196l81 81 72-100 111 150" fill="none" stroke="#327fc2" stroke-width="14"/><path d="M151 386h498l-29 30H180z" fill="#667e92"/><path d="M341 386h118l-8 9H349z" fill="#dae5ed"/></svg>')
GLOBE = svg_data('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300"><circle cx="150" cy="150" r="132" fill="#1e2d3e" stroke="#80a9e7" stroke-width="4"/><circle cx="150" cy="150" r="112" fill="none" stroke="#6c91c5" stroke-width="2"/><ellipse cx="150" cy="150" rx="57" ry="112" fill="none" stroke="#6c91c5" stroke-width="2"/><path d="M40 150h220M55 95h190M55 205h190M150 38v224" fill="none" stroke="#6c91c5" stroke-width="2"/><circle cx="150" cy="150" r="24" fill="#a6c8f5"/><path d="m150 110 8 26 27 14-27 14-8 26-8-26-27-14 27-14z" fill="#edf5ff"/></svg>')
LOGO = svg_data('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="18" fill="#425b4b"/><path d="M14 40 32 15l18 25-18 10z" fill="#f3e4ba"/><circle cx="32" cy="32" r="6" fill="#425b4b"/></svg>')
ICONS = {
    'account_balance':'▥','arrow_drop_down':'⌄','arrow_downward':'↓','arrow_outward':'↗','add_reaction':'☺','add_shopping_cart':'+','bookmark':'▣','bookmark_added':'✓','bookmark_border':'▢','cabin':'⌂','coffee':'☕','crop_free':'▢','dataset':'▦','delete':'×','delete_sweep':'×','eco':'✿','edit_note':'✎','filter_alt':'☷','forest':'♠','format_size':'Aa','group':'●','handyman':'⚒','help_outline':'?','history_edu':'◷','inventory_2':'▣','lightbulb':'✦','local_cafe':'☕','mode_fan':'✣','north_east':'↗','production_quantity_limits':'▢','send':'➤','spa':'✿','splitscreen':'▥','straight':'↑','sync_alt':'⇄','tips_and_updates':'✦','track_changes':'◎','translate':'文','volume_up':'♪','wallet':'▣','code':'⌘','account_tree':'⑂','accessibility_new':'♿','add':'+','api':'⌘','arrow_forward':'→',
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
        replacement = GLOBE if slug == 'wikipedia' else LOGO
        return re.sub(r'src="https://lh3\.googleusercontent\.com/[^"]+"', 'src="' + replacement + '"', tag)
    html = re.sub(r'<img\b[^>]*src="https://lh3\.googleusercontent\.com/[^"]+"[^>]*>', image, html)
    # Stitch's icon font is remote; use local text symbols so failed font loads
    # do not expose long ligature names or break the mobile layout.
    def icon(match):
        name = match.group(2).strip()
        if name not in ICONS:
            raise ValueError(f'{slug}: unmapped icon {name}')
        return match.group(1) + ICONS[name] + match.group(3)
    html = re.sub(r'(<span\b[^>]*class="[^"]*material-symbols-outlined[^"]*"[^>]*>)\s*([^<>]+?)\s*(</span>)', icon, html)
    for old, new in [('textContent = \'add\'', "textContent = '+'"),
                     ('textContent = \'close\'', "textContent = '×'"),
                     ('textContent = \'check\'', "textContent = '✓'")]:
        html = html.replace(old, new)
    html = html.replace('</head>', '<style>.material-symbols-outlined{font-family:system-ui,sans-serif!important;line-height:1;font-style:normal}</style></head>', 1)
    if slug == 'wikipedia':
        for old, new in [('由全球獨立學者協作校閱之六大學術範疇核心索引','六個虛構的知識分類範例'),('所有目次皆受同儕匿名核實，完全無追蹤、純粹供公眾查閱','本頁資料與條目數量均為介面示範'),('致力於公共學術記錄之開放保存。無行為追蹤、無個人識別標籤、拒絕商業演算法干涉，純粹守護知識本體之探索空間。','本頁為原創設計範例，不提供真實百科資料。'),('開放源碼協議 (CC0 / MIT)','示範內容'),('純粹隱私宣言','使用說明'),('開源資料授權','示範資料'),('典藏倫理','關於範例')]:
            html = html.replace(old, new)
    if slug == 'discord':
        # User-entered text must never be interpreted as HTML.
        old = "'<p class=\"font-body-md text-body-md text-on-surface mt-0.5 leading-relaxed\">' + msg.text + '</p>' +"
        new = "'<p class=\"font-body-md text-body-md text-on-surface mt-0.5 leading-relaxed\"></p>' +"
        if old not in html: raise ValueError('Missing Discord message template')
        html = html.replace(old,new).replace('          messageContainer.appendChild(item);',"          item.querySelector('p').textContent = msg.text;\n          messageContainer.appendChild(item);")
    if slug == 'duolingo':
        html = html.replace('馬上隨手試做 3 題日常小對話', '馬上試做 1 題單字練習')
        html = html.replace('</head>', '<style>a.bg-primary-container{color:#183500}@media(max-width:600px){header>div{padding-left:16px!important;padding-right:16px!important;gap:8px!important}header>div>div:nth-child(2){display:none}header a{white-space:nowrap;padding-left:14px!important;padding-right:14px!important}}</style></head>',1)
    if slug == 'ikea':
        html = html.replace('</head>', '<style>@media(max-width:600px){header{position:relative!important}header>div:first-child{display:none!important}header>div:nth-child(2){gap:8px!important;padding:0 16px!important}header>div:nth-child(2)>div:first-child{flex:none}header>div:nth-child(2)>div:nth-child(2){min-width:0;margin:0!important}header>div:nth-child(2)>div:last-child a:last-child{display:none!important}header>div:nth-child(2)>div:last-child a{padding:0 10px!important}header>div:nth-child(2)>div:last-child a>span:last-child{font-size:0}header>div:nth-child(2)>div:last-child a>span:last-child span{font-size:12px}main{padding-top:0!important}}</style></head>',1)
    if slug == 'discord':
        for old,new in [('60 FPS','即時'),('原生響應速率','介面回應'),('無障礙對比度規範 (WCAG AAA)','無障礙設計示意'),('開放源碼原創呈現','原創介面示範')]:
            html = html.replace(old,new)
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
    for slug in ('wikipedia', 'amazon', 'discord', 'duolingo', 'ikea'):
        with zipfile.ZipFile(WORK / f'{slug}-stitch.zip') as archive:
            html = archive.read('code.html').decode('utf-8')
        (OUTPUT / f'{slug}.html').write_text(clean_html(slug, html))
        print(slug, 'prepared for local review')


if __name__ == '__main__':
    main()
