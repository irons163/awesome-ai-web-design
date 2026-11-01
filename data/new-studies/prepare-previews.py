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
WORK = ROOT / '.test-artifacts/five-new-designs-2026-11-01'
OUTPUT = WORK / 'review-previews'


def svg_data(svg):
    return 'data:image/svg+xml;base64,' + base64.b64encode(svg.encode()).decode()


AVATAR = svg_data('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="32" fill="#dce6ec"/><circle cx="32" cy="24" r="11" fill="#56717d"/><path d="M12 58c2-13 10-19 20-19s18 6 20 19" fill="#56717d"/></svg>')
LAPTOP = svg_data('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 520"><defs><linearGradient id="g" x2="1" y2="1"><stop stop-color="#e9f4ff"/><stop offset="1" stop-color="#b9d3ed"/></linearGradient></defs><rect width="800" height="520" fill="url(#g)"/><rect x="176" y="96" width="448" height="276" rx="18" fill="#1d3042"/><rect x="188" y="108" width="424" height="252" rx="7" fill="#bad7ef"/><path d="M207 327 330 196l81 81 72-100 111 150" fill="none" stroke="#327fc2" stroke-width="14"/><path d="M151 386h498l-29 30H180z" fill="#667e92"/><path d="M341 386h118l-8 9H349z" fill="#dae5ed"/></svg>')
ICONS = {
    'account_tree':'⑂','accessibility_new':'♿','add':'+','api':'⌘','arrow_forward':'→',
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
        replacement = LAPTOP if '原創旗艦筆記型電腦' in tag else AVATAR
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
    if slug == 'google':
        for old, new in [('已啟用隱私無痕', '搜尋示範介面'), ('無痕安全設定', '示範設定'),
                         ('· 根據網路位址推測', '· 示範資料'), ('純粹架構 · 零追蹤日誌 · 獨立自建資料集', '設計示範 · 不提供實際搜尋服務'),
                         ('在全網搜尋或鍵入關鍵字', '搜尋示範資料或鍵入關鍵字')]:
            if old not in html:
                raise ValueError(f'{slug}: expected phrase missing: {old}')
            html = html.replace(old, new)
    if slug == 'netflix':
        # Do not request personal information or present invented legal or contact details as fact.
        html = html.replace('請輸入您的電子郵件地址...', '示範介面不需輸入個人資料')
        html = html.replace('required="" type="email"', 'disabled="" type="text"')
        html = html.replace('輸入電子郵件或直接體驗本機示範，開啟專屬觀影清單。', '直接體驗本機示範，瀏覽虛構的影音清單。')
        html = html.replace('輸入電子郵件，即刻啟動 映潮 StreamWave 訪客體驗，隨時享受專屬片單。', '直接體驗虛構的訪客介面，不需要輸入個人資料。')
        html = html.replace('示範帳戶已暫存於瀏覽器暫存區，隨時可關閉重設。', '這是示範畫面，不會建立帳戶。')
        html = re.sub(r'<label\b[^>]*for="(?:hero-email|bottom-email)"[^>]*>.*?</label>', '', html, flags=re.S)
        html = re.sub(r'<input\b[^>]*id="(?:hero-email|bottom-email)"[^>]*/?>', '', html)
        html = html.replace('文化部數位影音內容分級制度與兒少保護落實平台', '原創設計示範，內容與服務皆為虛構')
        html = re.sub(r'<div class="p-space-md rounded-lg bg-surface-container-low mb-space-lg flex flex-col gap-space-xs"><p class="font-label-sm text-label-sm text-on-surface font-semibold">【中華民國電影與電視節目分級規範聲明】</p>.*?</div>', '', html, flags=re.S)
        html = re.sub(r'統一編號：88320491[^<]*', '本頁為設計示範，不提供註冊、付款或影音服務。', html)
        html = html.replace('映潮串流娛樂股份有限公司 StreamWave Taiwan Co., Ltd. 保留一切權利。', '映潮 StreamWave・虛構範例。')
        if any(word in html for word in ('88320491', '0800-880-999', '中華民國電影與電視節目分級規範聲明')):
            raise ValueError('Invented Netflix example contact or legal claims remain')
    if slug == 'github':
        html = html.replace('git init &amp;&amp; git remote add origin https://pulse.git/demo/starter.git', 'git init')
        html = html.replace('git init && git remote add origin https://pulse.git/demo/starter.git', 'git init')
        html = html.replace('git clone https://pulse.git/demo/starter.git', 'git init')
        html = html.replace('curl -fsSL https://pulse.git/install.sh | bash', 'git --version')
        html = html.replace('已複製一鍵安裝腳本', '已複製示範命令')
        html = html.replace('curl 安裝 CLI 工具', '複製示範命令')
        if 'pulse.git' in html:
            raise ValueError('Unverified executable URL remains')
    if slug == 'youtube':
        html = html.replace('</head>', '''<style>@media(max-width:600px){
          body>div.pl-20{padding-left:0!important} aside{display:none!important}
          header>div>div:last-child,header>div>div:first-child a,header button[aria-label="語音搜尋"]{display:none!important}
          header>div>div:nth-child(2){min-width:0;flex:1}
          #btnToggleDrawer{white-space:nowrap} #btnToggleDrawer,#btnResetFilters,#btnToggleEmpty{padding-left:10px;padding-right:10px}
          #btnToggleDrawer>span:first-child,#btnResetFilters>span:first-child,#btnToggleEmpty>span:first-child{display:none}
          #btnToggleDrawer{gap:4px} #btnToggleDrawer>span:last-child{display:none}
          #btnToggleDrawer,#btnResetFilters,#btnToggleEmpty{font-size:13px}
          #btnToggleDrawer~*{min-width:0} #activeQueryLabel{min-width:0;overflow:hidden;text-overflow:ellipsis}
          #btnToggleEmpty{white-space:nowrap}
        }</style></head>''', 1)
    banner = ('<div role="note" style="position:fixed;bottom:0;left:0;right:0;z-index:9999;padding:8px 16px;'
              'background:#202721;color:#fff;text-align:center;font:14px/1.5 system-ui,sans-serif">'
              '設計示範：品牌、內容與互動皆為範例，不提供實際服務。</div>')
    html, count = re.subn(r'(<body\b[^>]*>)', r'\1' + banner, html, count=1, flags=re.I)
    if count != 1:
        raise ValueError(f'{slug}: missing body')
    return html


def main():
    OUTPUT.mkdir(exist_ok=True)
    for slug in ('google', 'youtube', 'netflix', 'github', 'microsoft'):
        with zipfile.ZipFile(WORK / f'{slug}-stitch.zip') as archive:
            html = archive.read('code.html').decode('utf-8')
        (OUTPUT / f'{slug}.html').write_text(clean_html(slug, html))
        print(slug, 'prepared for local review')


if __name__ == '__main__':
    main()
