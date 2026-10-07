#!/usr/bin/env python3
"""Correct preserved Stitch exports using dated public DOM and original artwork.

The downloaded Stitch HTML/PNG and captured brand assets are never edited.
The displayed study is a separate refinement, not a native or accepted export.
"""
import hashlib
import json
import re
from html import escape
from pathlib import Path
from urllib.parse import urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / '.stitch-work/current-official'
ORIGIN = 'https://www.mastercard.com'
GRID = 'aem-Grid aem-Grid--12 aem-Grid--default--12'
COLUMN = 'aem-GridColumn aem-GridColumn--default--12'
ASSETS = json.loads((WORK / 'mastercard-asset-provenance.json').read_text())['assets']


def public(path):
    return urljoin(ORIGIN, path)


def local(url):
    return next(a['path'] for a in ASSETS if a['source_url'] == url)


def artwork(name, alt, width, height):
    rows = [a for a in ASSETS if a['kind'] == 'image' and urlsplit(a['source_url']).path.endswith('/' + name)]
    desktop = next((a for a in rows if 'width=1920' in a['source_url']), rows[0])
    mobile = next((a for a in rows if 'width=480' in a['source_url']), desktop)
    return (f'<div class="cmp-teaser__image"><div class="cmp-image"><picture>'
            f'<source media="(max-width:600px)" srcset="{mobile["path"]}">'
            f'<img class="cmp-image__image" width="{width}" height="{height}" '
            f'alt="{escape(alt, quote=True)}" src="{desktop["path"]}" loading="lazy">'
            '</picture></div></div>')


def container(content, classes='', ident='', column=False):
    attribute = ' id="' + ident + '"' if ident else ''
    return (f'<div class="container responsivegrid {classes} {COLUMN if column else ""}">'
            f'<div class="cmp-container"{attribute}>{content}</div></div>')


def teaser(title, classes, *, level=3, eyebrow='', copy='', href='', action='', label='', image='', ident=''):
    content = '<div class="cmp-teaser__content">'
    if eyebrow:
        content += '<p class="cmp-teaser__pretitle"><span class="cmp-pretitle-icon" aria-hidden="true"></span>' + escape(eyebrow) + '</p>'
    content += f'<h{level} class="cmp-teaser__title"> {escape(title)} </h{level}>'
    if copy:
        content += '<div class="cmp-teaser__description"><p>' + escape(copy) + '</p></div>'
    if action:
        content += ('<div class="cmp-teaser__action-container"><a class="cmp-teaser__action-link" '
                    f'aria-label="{escape(label or action, quote=True)}" href="{escape(public(href), quote=True)}">'
                    + escape(action) + '</a></div>')
    content += '</div>' + image
    if href and not action:
        content = f'<a class="cmp-teaser__link" href="{escape(public(href), quote=True)}">{content}</a>'
    attribute = ' id="' + ident + '"' if ident else ''
    return (f'<div class="teaser {classes} in-viewport"><div class="cmp-teaser"'
            f'{attribute}>{content}</div></div>')


def branded_carousel():
    slides = [
        ('梅西交換球衣。', '故事', 'messi-banner-home-page.jpg', '李奧·梅西與球迷', 1280, 720,
         '/tw/zh/news-and-trends/stories/2026/lionel-messi-fans-jersey-swap.html'),
        ('Mastercard 影響報告', '報告', 'impact-report-horizontal-pill.jpg', '指紋特寫。', 1280, 720,
         '/tw/zh/news-and-trends/press/2026/july/beyond-one-billion--inside-the-journey-to-a-more-inclusive-and-s.html'),
        ('新旅行方案', '報告', 'travel-report-art.jpg', 'Two hikers stand atop a peak with their arms out overlooking mountains.', 1972, 1314,
         '/tw/zh/news-and-trends/stories/2026/travel-report-2026.html'),
    ]
    content = ''
    indicators = ''
    for i, (title, category, name, alt, width, height, href) in enumerate(slides):
        content += (f'<div id="news-panel-{i}" class="swiper-slide cmp-carousel__item {"swiper-slide-active" if i==0 else ""}" '
                    f'role="tabpanel" aria-labelledby="news-tab-{i}" aria-label="投影片 {i+1}，共 3 張">'
                    + teaser(title, 'mccom-carousel-slide-branded', level=2, eyebrow=category, href=href,
                             image=artwork(name, alt, width, height)) + '</div>')
        indicators += (f'<li id="news-tab-{i}" role="tab" tabindex="{0 if i==0 else -1}" aria-selected="{str(i==0).lower()}" '
                       f'aria-controls="news-panel-{i}" aria-label="投影片 {i+1}" '
                       f'class="cmp-carousel__indicator swiper-pagination-bullet {"swiper-pagination-bullet-active" if i==0 else ""}">萬事達卡Agent Pay</li>')
    def button(kind, label):
        return (f'<button class="swiper-button-{kind} cmp-carousel__action" type="button" aria-label="{label}">'
                f'<span class="cmp-carousel__action-icon"></span><span class="swiper-button-text">{label}</span></button>')
    return ('<div class="carousel panelcontainer mccom-carousel__branded mccom-branded-intro">'
            '<div id="carousel-a0bcb5c3c7" class="cmp-carousel swiper animate swiper-initialized swiper-horizontal in-viewport" role="group">'
            '<div class="cmp-carousel__actions swiper-navigation">' + button('prev', '上一步') + button('next', '下一步') + '</div>'
            '<div class="cmp-carousel__content swiper-wrapper">' + content + '</div>'
            '<div class="cmp-carousel__actions-bottom"><ol class="cmp-carousel__indicators swiper-pagination swiper-pagination-bullets swiper-pagination-horizontal" '
            'role="tablist" aria-label="Choose a slide to display">' + indicators + '</ol>'
            '<div class="cmp-carousel__actions swiper-navigation">' + button('pause', '暫停') + button('play', '播放') + '</div></div></div></div>')


def services():
    data = [
        ('觀點洞察', '顧問服務', 'mccom-vertical-pill expect-tall-image',
         'br45724-mastercard-websiteimageryrefresh-solutions-2-9x16-ezgif-com-loop-count.gif', '正在用行動裝置打字的女子。', 918, 1632, '/tw/zh/business/insights-intelligence.html'),
        ('個人消費與商務支付', '解決方案', 'mccom-circle-pill expect-square-image mccom-circle-keyline-left',
         'br45724-mastercard-websiteimageryrefresh-solutions-4-1x1.jpg', '一個人正在用手錶付款。', 1080, 1080, '/tw/zh/business/payments.html'),
        ('資金流動', '解決方案', 'mccom-vertical-pill expect-tall-image',
         'br45724-mastercard-websiteimageryrefresh-solutions-6-9x16.jpg', '一名繫著安全帶的人坐在停好的車內看手機。', 1080, 1920, '/tw/zh/business/payments/Mastercard%20Move.html'),
        ('資訊安全與詐欺防制', '顧問服務', 'mccom-circle-pill expect-square-image mccom-circle-keyline-right',
         'br45724-mastercard-websiteimageryrefresh-solutions-1-1x1-ezgif-com-loop-count.gif', '在螢幕上點擊。', 1080, 1080, '/tw/zh/business/cybersecurity-fraud-prevention.html'),
        ('消費者拓展與互動經營', '顧問服務', 'mccom-vertical-pill expect-tall-image',
         'br45724-mastercard-websiteimageryrefresh-solutions-3-9x16.jpg', '一名女子在幫一位試穿洋裝的顧客調整皮帶。', 1080, 1920, '/tw/zh/business/consumer-acquisition-and-engagement.html'),
        ('開放式金融', '顧問服務', 'mccom-circle-pill expect-square-image',
         'br45724-mastercard-websiteimageryrefresh-solutions-5-1x1-ezgif-com-loop-count.gif', '企業主在平板電腦上打字。', 864, 864, '/tw/zh/business/open-finance.html'),
    ]
    panels = [teaser(t, cls+' mccom-scroll-trigger', eyebrow=e, href=h, image=artwork(n,a,w,ht)) for t,e,cls,n,a,w,ht,h in data]
    def group(start):
        return panels[start] + container(panels[start+1], 'mccom-margin-bottom-lg mccom-margin-top-lg') + panels[start+2]
    left_classes = ('mccom-margin-top-lg aem-GridColumn--tablet--12 aem-GridColumn--offset--tablet--0 '
                    'aem-GridColumn--default--none aem-GridColumn--phone--none aem-GridColumn--phone--12 '
                    'aem-GridColumn--tablet--none aem-GridColumn aem-GridColumn--default--5 '
                    'aem-GridColumn--offset--phone--0 aem-GridColumn--offset--default--0')
    right_classes = ('mccom aem-GridColumn--tablet--12 aem-GridColumn--offset--tablet--0 '
                     'aem-GridColumn--default--none aem-GridColumn--phone--12 aem-GridColumn--phone--newline '
                     'aem-GridColumn aem-GridColumn--tablet--newline aem-GridColumn--default--5 '
                     'aem-GridColumn--offset--default--2 aem-GridColumn--offset--phone--0')
    grid = ('<div class="aem-Grid aem-Grid--12 aem-Grid--tablet--12 aem-Grid--default--12 aem-Grid--phone--12">'
            + container(group(0), left_classes) + container(group(3), right_classes) + '</div>')
    return container(container(grid, 'mccom-max-width-lg mccom-margin-top-lg mccom-stagger-columns'),
                     'mccom-circle-box mccom-margin-bottom-lg', column=True)


FOOTER_GROUPS = [
    ('需要幫助嗎？', [('獲取支援','/tw/zh/personal/get-support.html'), ('通報卡片遺失或遭竊','/tw/zh/personal/get-support.html'),
                   ('搜尋 ATM','/tw/zh/personal/get-support/atm-near-me.html'), ('常見問題','/tw/zh/personal/get-support/frequently-asked-questions.html')]),
    ('公司', [('關於我們','/tw/zh/for-the-world/about-us.html'), ('徵才資訊','https://careers.mastercard.com/us/en'),
             ('新聞中心','https://www.mastercard.com/news/ap/zh-tw'), ('投資者關係','https://investor.mastercard.com/overview/default.aspx')]),
    ('法律與隱私', [('隱私與數據責任','/tw/zh/for-the-world/about-us/mastercard-privacy-and-data-responsibility.html'),
                ('約束性企業規則（BCRs）','/content/dam/mccom/shared/footer/mastercard-bcrs.pdf'), ('Cookie 通知','/tw/zh/cookie-notice.html')]),
    ('萬事達卡網站', [('priceless.com','https://www.priceless.com/'),
                  ('萬事達卡商業智慧','https://mbi.mastercardservices.com/?utm_source=mastercardwebsite&utm_medium=footer&utm_campaign=services&utm_id=mbi&utm_term=global&utm_content=mastercard_business_intelligence'),
                  ('萬事達卡開發者平台','https://developer.mastercard.com/'), ('萬事達卡行銷中心','https://www.mastercard.com/marketingcenter'),
                  ('包容性成長中心','https://www.mastercardcenter.org/')]),
]


def footer():
    groups = ''
    for i, (title, links) in enumerate(FOOTER_GROUPS):
        content = (f'<div class="title"><div class="cmp-title"><h6 class="cmp-title__text">'
                   f'<button id="navMenu-{i}-button" aria-label="{title}" aria-controls="navMenu-{i}-panel" tabindex="0" aria-expanded="true">{title}</button>'
                   '</h6></div></div><div class="text"><div class="cmp-text">'
                   f'<ul id="navMenu-{i}-panel" aria-hidden="false">'
                   + ''.join('<li'+(' id="'+['support','report','atm','faq'][j]+'"' if i==0 else '')+f'><a href="{escape(public(h),quote=True)}"'
                             + (' target="_blank" rel="noopener"' if h.startswith('https:') else '')
                             + f'>{escape(t)}'
                             + ('<span class="cmp-link__screen-reader-only">在新標籤中開啟</span>' if h.startswith('https:') else '')
                             + '</a></li>' for j,(t,h) in enumerate(links))
                   + '</ul></div></div>')
        groups += container(content, 'mccom', 'footer-tools-navigation' if i==0 else '')
    social = [('social-linkedin','Linkedin','http://www.linkedin.com/company/mastercard'),
              ('social-facebook','Facebook','https://www.facebook.com/MasterCardUS?brand_redir=1'),
              ('social-twitter','Twitter/X','https://x.com/mastercardnews'),
              ('social-youtube','Youtube','https://www.youtube.com/user/MasterCard')]
    options = ''
    for i,line in enumerate((WORK/'mastercard-country-options.txt').read_text().splitlines()):
        label,href=line.split('|',1)
        options += (f'<li id="study-country-option-{i}" role="option" aria-selected="{str(label=="Taiwan (Traditional Chinese)").lower()}" '
                    'class="made-c-overflow-menu__item" tabindex="-1">'
                    f'<a class="made-c-overflow-menu__link" href="{escape(public(href),quote=True)}">{escape(label)}</a></li>')
    country = ('<div class="countryselector"><div id="countrySelectorContainter" class="mccom-country-selector">'
               '<forms-ui-select class="hydrated"><div class="made-c-form__element outer-div">'
               '<label class="made-c-form__label" for="countrySelectorDropdownCustomInput">Select a country</label>'
               '<div class="made-c-select__wrapper made-u-margin-top-1-x"><div class="forms-ui-select-input-container">'
               '<input id="countrySelectorDropdownCustomInput" class="made-c-select made-c-text-input--select-filter" '
               'role="combobox" aria-expanded="false" aria-controls="study-country-list" readonly value="Taiwan (Traditional Chinese)">'
               '<span class="forms-ui-icon-wrapper"><svg width="20" height="20" viewBox="0 0 20 20" class="made-c-select__arrow" fill="none">'
               '<path d="M16.25 6.875L10 13.125L3.75 6.875" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></span>'
               '</div></div><div id="study-country-overflow" class="made-c-overflow-menu made-c-overflow-menu--form overflow-menu--closed">'
               '<ul id="study-country-list" role="listbox" class="made-c-overflow-menu__list overflow-menu__list-custom-padding made-c-overflow-menu__list--select made-c-scrollbar">'
               + options + '</ul></div></div></forms-ui-select></div></div>')
    socials = '<div class="text"><div id="footer-social-links" class="cmp-text"><ul>'
    socials += ''.join(f'<li id="{i}"><a href="{escape(h,quote=True)}" title="{t}">{t}</a></li>' for i,t,h in social) + '</ul></div></div>'
    legal = ('<div class="text"><div id="footer-copyright" class="cmp-text"><p>© 1994-2026萬事達卡。</p></div></div>'
             '<div class="footercommonlinks text"><div class="text"><div id="footer-copyright-links" class="cmp-text"><ul>'
             '<li><a href="https://www.mastercard.com/tw/zh/privacy.html" title="隱私">隱私</a></li>'
             '<li><a href="https://www.mastercard.com/tw/zh/terms-of-use.html" title="條款">條款</a></li>'
             '<li><a href="#" class="optanon-show-settings" title="管理 Cookie">管理 Cookie</a></li></ul></div></div></div>')
    secondary = container(legal,'mccom study-footer-legal','footer-legal-navigation') + container(country + socials, 'mccom study-footer-social', 'footer-social-navigation')
    return ('<footer class="experiencefragment '+COLUMN+'"><div id="footer" class="cmp-experiencefragment cmp-experiencefragment--footer">'
            '<div id="container-18c57d2602" class="cmp-container"><div class="breadcrumb"></div><div class="image"></div>'
            '<div class="text"><div id="footer-title" class="cmp-text"><p>當您需要幫忙時，我們一直在這裡</p></div></div>'
            + container(groups, 'mccom', 'footer-primary-navigation')
            + '<div class="separator"><div id="footer-separator" class="cmp-separator"><hr class="cmp-separator__horizontal-rule"></div></div>'
            '<div class="disclaimer"></div>' + container(secondary, 'mccom', 'footer-secondary-navigation') + '</div></div></footer>')


def header():
    labels = [('1f2ad0e473','萬事達卡'), ('e51b865f32','萬事達卡商務'), ('74968c2f23','願景'), ('900a6ee2fb','創新推動'), ('bba1fd377f','新聞洞察')]
    buttons = ''.join(f'<li role="menuitem"><button id="heading-{i}" aria-controls="section-{i}" aria-expanded="false" aria-haspopup="true">{t}</button></li>' for i,t in labels)
    return ('<div id="container-652caa2ed1" class="cmp-container"><div class="navigation-header responsivegrid"><div class="navigation-bar">'
            '<div class="navigation-bar__logo"><a href="https://www.mastercard.com/tw/zh.html"><img src="mastercard-assets/47346e7995ee.svg" '
            'alt="Mastercard brand symbol - a global technology company in the payments industry"></a></div>'
            '<div class="navigation-bar__main"><div class="l1-container"><button id="mobileMenuToggle" class="mobile-menu-button" '
            'aria-controls="mobileMenu" aria-expanded="false"><span class="mobile-menu-button-text">Open Menu</span><span class="mobile-menu-button-indicator"></span></button>'
            '<div id="mobileMenu" class="mobile-menu" aria-labelledby="mobileMenuToggle"><ul role="menubar" aria-orientation="horizontal">' + buttons + '</ul></div></div></div>'
            '<div class="navigation-bar__search"><button id="search-toggle" class="search-toggle" aria-controls="search-content" aria-expanded="false" aria-label="Open search">'
            '<span class="toggle-icon search-icon" aria-hidden="true"></span><span class="toggle-icon close-icon" aria-hidden="true"></span></button></div></div></div></div>'
            '<div id="study-navigation" class="study-navigation-panel" hidden></div>'
            '<div id="search-content" class="study-navigation-panel" hidden><form id="study-search" role="search"><label for="study-search-input">搜尋 Mastercard</label>'
            '<input id="study-search-input" type="search" placeholder="您需要什麼協助？"><button type="submit">搜尋</button></form><p id="study-search-result"></p></div>')


def hero():
    return container('<div class="video-hero"><div class="mccom-video-hero-container"><div class="video-js mccom-video-hero mccom-video-hero-skin vjs-fill vjs-controls-enabled vjs-v8 vjs-user-active" '
                     'role="region" aria-label="Experience Priceless Video"><video id="study-hero" class="vjs-tech" muted autoplay playsinline preload="metadata" '
                     'src="https://www.mastercard.com/content/dam/mccom/shared/homepage/videos/translated-welcome-videos/homepage-video-zh-TW_16x9_.mp4"></video>'
                     '<div class="vjs-control-bar"><button class="vjs-play-control vjs-control vjs-button" type="button" title="Pause">'
                     '<span class="vjs-icon-placeholder" aria-hidden="true"></span><span class="vjs-control-text">Pause</span></button>'
                     '<button class="vjs-mute-control vjs-control vjs-button vjs-vol-0" type="button" title="Unmute"><span class="vjs-icon-placeholder" aria-hidden="true"></span>'
                     '<span class="vjs-control-text">Unmute</span></button></div></div></div></div>', 'mccom-full-width', column=True)


def main_content():
    intro = container(teaser('驅動經濟，賦能民眾', 'mccom-section-intro-default mccom-cta__primary', level=1, copy='為全球的消費者、企業與政府釋放潛能。'), 'mccom-margin-bottom-lg')
    news = container(intro + branded_carousel(), 'mccom-max-width-lg mccom-margin-top-lg', column=True)
    business = container(teaser('共創無價可能','mccom-section-intro-display-header mccom-scroll-trigger mccom-cta__primary', eyebrow='企業與政府解決方案', copy='以創新解決方案，打造更安全、更智慧的數位經濟。'), 'mccom-max-width-lg mccom-margin-top-lg', column=True)
    benefit_intro = teaser('支持您實現目標的權益與服務', 'mccom-section-intro-display-header mccom-scroll-trigger mccom-cta__primary', eyebrow='卡片與權益', copy='滿足您日常生活與未來旅程所需的權益、服務、回饋獎勵與消費力。', href='/tw/zh/personal/find-a-card/card-benefits.html', action='了解更多', label='了解卡片權益')
    touch = teaser('尋找適合您的卡片', 'mccom-horizontal-pill-right mccom-scroll-trigger', href='/tw/zh/personal/find-a-card.html', action='了解更多', label='了解更多卡片資訊', image=artwork('mastercard-whiteplastic-radialtex-animation1-small.gif','萬事達卡Touch Card。',640,360))
    ways = teaser('隨心支付','mccom-horizontal-pill-left mccom-scroll-trigger', copy='日常與旅途中的現代支付方式', href='/tw/zh/personal/ways-to-pay.html', action='了解更多', label='探索更多支付方式', image=artwork('br45724-mastercard-websiteimageryrefresh-benefitsservices-2-ezgif-com-loop-count.gif','女人微笑。',960,540))
    benefits = container(benefit_intro + container(touch, 'mccom') + container(ways, 'mccom'), 'mccom-white-box mccom-max-width-lg mccom-margin-bottom-lg', column=True)
    priceless = container(teaser('點燃熱情的精彩體驗','mccom-section-intro-default mccom-scroll-trigger mccom-cta__secondary', eyebrow='無價體驗', copy='「Priceless Experience 無價體驗」讓您有機會參與精彩的運動賽事、旅遊行程、美食和娛樂饗宴，值得您永遠珍藏。', href='https://www.priceless.com/', action='探索 priceless.com', label='前往 priceless.com，探索更多無價體驗。'), 'mccom-margin-bottom-md')
    poster = '<div class="video"><div class="mccom-video-container"><div class="youtube-player mccom-video-skin"><div id="player-video-1655747854"><img width="100%" alt="poster" src="mastercard-assets/258aca04d44d.jpg"><button type="button" class="video-js vjs-big-play-button" aria-label="Play video"><span class="vjs-icon-placeholder" aria-hidden="true"></span></button></div></div></div></div>'
    experiences = container(priceless+poster, 'mccom-max-width-lg mccom-margin-bottom-lg', column=True)
    special = teaser('Priceless Specials','mccom-horizontal-pill-left mccom-circle-keyline-left mccom-scroll-trigger mccom-cta__secondary '+COLUMN, copy='年度精選優惠讓每個時刻獨一無二：無價', href='https://specials.priceless.com/zh-tw/homePage', action='了解更多', image=artwork('asian-family-happy-1280x720.jpg','Premium Mastercard Services',1280,720))
    travel = teaser('Travel Rewards','mccom-horizontal-pill-right mccom-circle-keyline-left mccom-scroll-trigger mccom-cta__secondary '+COLUMN, copy='萬事達卡海外消費回饋，讓您於全球指定特約免稅店、DFS、百貨或各式商戶消費，單筆滿額即享高額現金回饋！', href='/tw/zh/personal/experience-mastercard/offers-and-promotions.html', action='了解更多‎', image=artwork('2-women-window-shopping.jpg','Premium Mastercard Services',767,431))
    offers = container('<div class="'+GRID+'">'+special+travel+'</div>','mccom-max-width-lg mccom-margin-bottom-md',column=True)
    content = '<div class="'+GRID+'">'+hero()+news+business+services()+benefits+experiences+offers+'</div>'
    main = container(content, ident='main-content', column=True)
    return ('<div class="root container responsivegrid"><div id="container-5dfb0149a2" class="cmp-container"><div class="'+GRID+'">'
            '<main class="container responsivegrid '+COLUMN+'"><div id="container-bb54d2adc6" class="cmp-container"><div class="'+GRID+'">'
            + main + '</div></div></main>'+footer()+'</div></div></div>')


def resolved_styles():
    styles = []
    by_url = {a['source_url']: a for a in ASSETS}
    by_path = {urlsplit(a['source_url']).path: a for a in ASSETS}
    for row in ASSETS:
        if row['kind'] != 'stylesheet':
            continue
        original = (WORK / row['path']).read_text()
        def replace(match):
            value = match.group(1).strip().strip('"\'')
            if value.startswith(('data:', '#')):
                return match.group(0)
            absolute = urljoin(row['source_url'], value)
            captured = by_url.get(absolute) or by_path.get(urlsplit(absolute).path)
            return 'url("' + (captured['path'] if captured else absolute) + '")'
        styles.append(re.sub(r'url\(([^)]+)\)', replace, original))
    return '\n'.join(styles)


def main():
    for row in ASSETS:
        data = (WORK / row['path']).read_bytes()
        assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'], row['path']
    seed = (WORK / 'mastercard-stitch-desktop-raw.html').read_text()
    head = re.search(r'<head>(.*?)</head>',seed,re.S).group(1)
    head = re.sub(r'<(?:style|script)\b[^>]*>.*?</(?:style|script)>', '', head, flags=re.S|re.I)
    head = re.sub(r'<link\b[^>]*>', '', head, flags=re.I)
    head = re.sub(r'<title>.*?</title>', '<title>萬事達卡：支付領域的全球性科技公司 · 官網研究草稿</title>', head, flags=re.S)
    stylesheet = resolved_styles()+'\n'+(ROOT/'scripts/mastercard-current-official.css').read_text()
    js = (ROOT/'scripts/mastercard-current-official.js').read_text()
    dialogs = (ROOT/'scripts/mastercard-dialogs.html').read_text()
    html = ('<!doctype html><html lang="zh-TW" class="is-loaded is-ready"><head>'+head
            + '<link rel="icon" href="mastercard-assets/882c5c05740e.svg"><style>'+stylesheet+'</style></head>'
            + '<body id="page-1cb73cc92e" class="page basicpage mccom">'
            + '<!-- Separate correction of unchanged native Stitch exports. Public Taiwan DOM observed 2026-10-07; full visual acceptance pending. -->'
            + header()+main_content()+dialogs
            + '<div class="study-chat-container"><button id="livechatIcon" type="button" aria-label="Open chat"><img src="mastercard-assets/81e42280663a.gif" alt="" aria-hidden="true"></button></div>'
            + '<script>'+js+'</script></body></html>')
    (WORK/'mastercard.html').write_text(html)
    print(json.dumps({'display_bytes':len(html.encode()),'captured_urls':len(ASSETS),'native_seed_sha256':hashlib.sha256(seed.encode()).hexdigest()}))


if __name__ == '__main__':
    main()
