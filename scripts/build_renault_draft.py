#!/usr/bin/env python3
"""Correct a native Stitch study using Renault's dated public homepage evidence."""
import copy
import html
import json
import re
from pathlib import Path
from urllib.parse import quote, urljoin, urlsplit
from official_html_tree import Tree, Node, fragment

ROOT = Path(__file__).resolve().parents[1] / '.stitch-work/current-official'
ORIGIN = 'https://www.renaultgroup.com/'
MEDIA = 'https://assets.renaultgroup.com/'


def element(tag, cls='', children=(), **attrs):
    if cls:
        attrs['class'] = cls
    node = Node(tag, attrs)
    node.children = [Node(text=html.escape(c, quote=False)) if isinstance(c, str) else c for c in children]
    return node


def has(node, cls):
    return cls in node.attrs.get('class', '').split()


def icon(name):
    return element('svg', 'icon icon-' + name, [element('use', href='#icon-' + name)],
                   width='24', height='24', fill='currentColor', **{'aria-hidden': 'true'})


def controls(carousel, count, kind):
    classes = 'Button_btn__k2_e6 Button_btn-primary__twsyG Button_btn-icon__fkh69 '
    arrows = [element('button', classes + 'Carousel_carousel-' + direction + '__' + suffix +
                      ' Carousel_horizontal__TxOCR Carousel_positioned__0pvGn ' + extra,
                      [icon('arrow-' + arrow + '-24'), element('span', 'sr-only', [label])],
                      type='button', **{'data-carousel-step': str(step)})
              for direction, suffix, arrow, label, step, extra in [
                  ('prev', 'hwGpo', 'left', 'Précèdent', -1, 'MinorNews_carousel-prev__y7D0T' if kind == 'news' else ''),
                  ('next', 'iwi1t', 'right', 'Suivant', 1, 'MinorNews_carousel-next__InmTC' if kind == 'news' else '')]]
    dots = element('div', ('MinorNews_carousel-dots__oa8Iy' if kind == 'news' else
                          'BigCTACards_carousel-dots__fTHaL'), [
        element('button', 'Button_btn__k2_e6 Button_btn-primary__twsyG Button_btn-lg__8NZj_ Carousel_carousel-btn__FMhjf' +
                (' Carousel_carousel-btn--selected__SWQEV' if index == 0 else ''),
                [element('span', 'Carousel_carousel-dot__0wnQ9')], type='button',
                **{'aria-label': 'Slide ' + str(index + 1), 'aria-pressed': str(index == 0).lower(),
                   'data-carousel-index': str(index)}) for index in range(count)])
    carousel.children.append(element('div', 'MinorNews_carousel-controls__t2Buj' if kind == 'news'
                                     else 'BigCTACards_carousel-controls___LxjX',
                                     [arrows[0], dots, arrows[1]] if kind == 'news' else [arrows[0], arrows[1], dots]))


def responsive_carousel(items, kind):
    item_class = 'Carousel_carousel-item__3cNUA Carousel_horizontal__TxOCR'
    if kind == 'news':
        item_class += ' MinorNews_carousel-item__fezb_'
    track = element('div', 'Carousel_carousel-content__8aYJ4 Carousel_horizontal__TxOCR' +
                    (' MinorNews_carousel-content__Jdeq8' if kind == 'news' else ''),
                    [element('div', item_class, [copy.deepcopy(item)], role='listitem',
                             style='padding-left:var(--grid-unit-20);flex-basis:100%',
                             **{'aria-roledescription': 'slide'}) for item in items], role='list',
                    style='margin-left:calc(var(--grid-unit-20) * -1)')
    wrapper = element('div', 'Carousel_content-wrapper__4RHWd', [track])
    if kind == 'news':
        wrapper = element('div', 'MinorNews_carousel-content-wrapper__5RbyU', [wrapper])
    carousel = element('div', 'Carousel_carousel___oe3h Carousel_is-ready__nKrWf d-desktop-none ' +
                       ('MinorNews_carousel__ZlCwD' if kind == 'news' else 'BigCTACards_carousel__EkNuV'),
                       [wrapper], role='region', **{'aria-roledescription': 'carousel', 'data-study-carousel': kind})
    if kind == 'news':
        carousel.children.insert(0, element('div', 'Separator_component__5MkIb Separator_component--horizontal__tPvRQ margin-bottom-32'))
        carousel.children.append(element('div', 'Separator_component__5MkIb Separator_component--horizontal__tPvRQ margin-top-32 margin-bottom-16'))
    controls(carousel, len(items), kind)
    return carousel


def main():
    source = Tree((ROOT / 'renault-source-current.html').read_text())
    page = source.root.find(lambda n: n.attrs.get('id') == 'website')
    data = json.loads((ROOT / 'renault-content-reference.json').read_text())
    assets = json.loads((ROOT / 'renault-asset-provenance.json').read_text())['assets']
    local = {row['source_url']: row['path'] for row in assets}
    media_by_path = {urlsplit(row['source_url']).path: row['path'] for row in assets
                     if 'assets.renaultgroup.com' in row['source_url']}

    def media(url):
        return local.get(url) or media_by_path.get(urlsplit(url).path) or url

    def original_image(url):
        return element('div', 'Image_bg__C7mUp Image_overlay__jIjkG', [element('img', src=media(url), alt='',
                       loading='lazy', style='position:absolute;height:100%;width:100%;inset:0;color:transparent')])

    def post_card(post):
        destination = urljoin(ORIGIN, post['uri'])
        content = [element('a', 'BentoSimpleCard_title__0EWfa stretched-link BentoSimpleCard_is-small__mf0lW text-base font-weight--bold',
                           [element('span', 'text-accessibility', [html.unescape(post['title'])])], href=destination)]
        if post['__typename'] == 'Post':
            content.append(element('p', 'BentoSimpleCard_text__jh2ab NavigationContent_card-date__COh11',
                                   ['.'.join(reversed(post['date'][:10].split('-')))]))
        return element('div', children=[element('article',
            'BentoSimpleCard_card__5pgXY BentoSimpleCard_xs__LVtOY NavigationContent_card__D_yxh', [
                original_image(urljoin(MEDIA, post['featuredImage']['node']['src'])),
                element('div', 'BentoSimpleCard_content__70Tv4', [element('div', children=content),
                    element('a', 'Button_btn__k2_e6 Button_btn-primary__twsyG Button_btn-icon__fkh69',
                            [icon('arrow-oblique-24')], href=destination, **{'aria-label': 'Ouvrir le lien'})])])], role='listitem')

    def new_badge(row, mobile=False):
        return ([element('sup', 'CTAButton_linkNew__dtQAS' if mobile else 'NavigationContent_linkNew__kn8G7', ['New'])]
                if (row.get('subMenuFields') or {}).get('isNew') else [])

    # Original icon sprite and font/style bytes are retained independently of Stitch.
    sprite = source.root.find(lambda n: n.tag == 'svg' and 'width: 0;' in n.attrs.get('style', ''))
    main_node = page.find(lambda n: n.tag == 'main')
    sections = main_node.children[0].children
    hero = sections[0].find(lambda n: has(n, 'HeroCarrousel_hero-carousel__oZGuZ'))
    hero.attrs['class'] += ' Carousel_is-ready__nKrWf'
    hero.attrs['data-study-carousel'] = 'hero'
    for n in hero.walk():
        if n.tag == 'button':
            n.attrs.pop('disabled', None)
            if 'Carousel_carousel-prev__hwGpo' in n.attrs.get('class', ''):
                n.attrs['data-carousel-step'] = '-1'
            elif 'Carousel_carousel-next__iwi1t' in n.attrs.get('class', ''):
                n.attrs['data-carousel-step'] = '1'
            elif n.attrs.get('aria-label', '').startswith('Slide '):
                n.attrs['data-carousel-index'] = str(int(n.attrs['aria-label'].split()[-1]) - 1)
    first_photo = hero.find(lambda n: n.tag == 'img').attrs['src']
    background = original_image(first_photo)
    background.attrs['class'] = 'Image_bg__C7mUp HeroCarrousel_bg-image__Jrexq'
    sections[0].children.insert(0, background)

    news_list = sections[1].find(lambda n: n.attrs.get('role') == 'list')
    news_list.attrs['class'] += ' d-none d-desktop-grid'
    news_items = []
    for item in news_list.children:
        article = copy.deepcopy(item.find(lambda n: n.tag == 'article'))
        article.children = [n for n in article.children if n.attrs.get('role') != 'none']
        article.find(lambda n: n.tag == 'a').attrs['class'] = 'NewsCard_component__wnTt9 MinorNews_card__RfpW_'
        news_items.append(article)
    sections[1].find(lambda n: has(n, 'Section_content__dDJoT')).children.insert(0, responsive_carousel(news_items, 'news'))
    sections[1].find(lambda n: has(n, 'MinorNews_separator-horizontal__r9fv6')).attrs['class'] += ' d-none d-desktop-block'

    brands = sections[6].find(lambda n: has(n, 'BigCTACards_row__Ic_sp'))
    brands.attrs['class'] += ' d-none d-desktop-flex'
    sections[6].find(lambda n: has(n, 'BigCTACards_content__xikkQ')).children.append(
        responsive_carousel([n.find(lambda n: n.tag == 'article') for n in brands.children], 'brands'))

    footer_nav = page.find(lambda n: has(n, 'Footer_menu--list__qyPWL'))
    footer_nav.attrs['class'] += ' d-none d-desktop-flex'
    accordion = element('div', 'Footer_menu__kvB1F menu--accordion d-desktop-none')
    for index, group in enumerate(footer_nav.children):
        title, links = group.children
        label = re.sub('<[^>]+>', '', title.render())
        button = element('button', 'Accordion_trigger__rY9B6 Footer_menu-title__36amu Footer_menu-trigger__7O67r',
                         [html.unescape(label), icon('language-arrow-24')], type='button', id='footer-toggle-' + str(index),
                         **{'aria-controls': 'footer-panel-' + str(index), 'aria-expanded': 'false', 'data-state': 'closed'})
        panel = element('div', 'Accordion_content__r_IbI', [copy.deepcopy(links)], hidden=None, role='region',
                        id='footer-panel-' + str(index), **{'aria-labelledby': button.attrs['id'], 'data-state': 'closed'})
        accordion.children.append(element('div', 'item', [element('h3', 'Accordion_header____fY9', [button]), panel]))
    footer_section = page.find(lambda n: footer_nav in n.children)
    footer_section.children.append(accordion)

    # Menu labels and destinations come from the public HTTP snapshot, not browser stores.
    menu_rows = data['headerLeftItems']['nodes'] + data['headerRightItems']['nodes']
    mobile_list = element('ul', 'list-style-none MobileMenu_mobile-menu-list__3KMv9')
    desktop_panels = element('div', 'study-desktop-panels')
    primary = [row for row in menu_rows if row['parentId'] is None]
    for index, row in enumerate(primary):
        label = html.unescape(row['label'])
        children = [child for child in menu_rows if child['parentId'] == row['id']]
        fields = row.get('megaMenuFields') or {}
        variation = (fields.get('menuVariation') or [None])[0]
        if variation == 'cards':
            children = [{'label': card['title'], 'path': card['link']['url'], 'target': card['link']['target']}
                        for card in fields['cards']]
        elif variation == 'magazine':
            children = [{'label': category['title'] if i == 0 else category['subtitle'][:1].upper() + category['subtitle'][1:],
                         'path': category['ctaButton1']['ctaButton']['action']['url']}
                        for i, category in enumerate(fields['magazine'])]
        link_class = 'Button_btn__k2_e6 Button_btn-primary__twsyG Button_btn-lg__8NZj_ MobileMenu_btn__l5dWJ'
        links = []
        for child in [row] + children:
            if (child.get('subMenuFields') or {}).get('isSeparator'):
                links.append(element('li', children=[element('div',
                    'Separator_component__5MkIb Separator_component--horizontal__tPvRQ MobileMenu_separator__KU5jV')]))
                continue
            links.append(element('li', 'MobileMenu_mobile-menu-item__LcUcx', [element('a', link_class +
                (' MobileMenu_btnSubmenu__YiwIq' if child is not row else ''),
                [element('span', children=[html.unescape(child['label'])])] + new_badge(child, mobile=True),
                href=urljoin(ORIGIN, child['path']), target=child.get('target') or '_self')]))
        if children:
            trigger = element('button', link_class, [element('span', children=[label]), icon('menu-arrow-24')],
                              type='button', **{'data-menu-open': str(index), 'aria-expanded': 'false'})
            back = element('button', 'Button_btn__k2_e6 Button_btn-primary__twsyG Button_btn-icon__fkh69',
                           [icon('menu-back-24')], type='button', **{'aria-label': 'Retour', 'data-menu-back': ''})
            sub = element('div', 'MobileMenu_mobile-menu-subList__s6ulo d-flex flex-column', [
                element('div', 'MobileMenu_mobile-menu-subList-header__dMTQt', [back, element('span',
                    'MobileMenu_mobile-menu-subList-title__1ccwi', [label])]),
                element('ul', 'list-style-none MobileMenu_mobile-menu-subList-list__wfN7f padding-y-48', links)],
                **{'data-state': 'closed', 'data-menu-panel': str(index)})
            mobile_list.children.append(element('li', 'MobileMenu_mobile-menu-item__LcUcx', [trigger, sub]))
        else:
            mobile_list.children.append(element('li', 'MobileMenu_mobile-menu-item__LcUcx', [
                element('a', link_class, [element('span', children=[label]), icon('menu-arrow-24')], href=row['path'])]))
        if label == 'Évènement':
            mobile_list.children[-1].children[0].find(lambda n: n.tag == 'span').children.append(
                element('sup', 'NavigationMenu_navigation-menu-sup__XHXKy NavigationMenu_type-upcoming__G78nE', ['J-5']))
        if label in ['Évènement', 'Presse']:
            mobile_list.children.append(element('div', 'Separator_component__5MkIb Separator_component--horizontal__tPvRQ MobileMenu_separator__KU5jV'))

        heading = element('h4', 'NavigationMenu_navigation-menu-heading__1dfIv', [element('a', children=[label, icon('arrow-right-24')], href=row['path'])])
        desktop_links = []
        for child in children:
            if (child.get('subMenuFields') or {}).get('isSeparator'):
                desktop_links.append(element('li', children=[element('div',
                    'Separator_component__5MkIb Separator_component--horizontal__tPvRQ NavigationContent_separator__cloQD')]))
            else:
                desktop_links.append(element('li', children=[element('a', 'NavigationMenu_navigation-menu-link__XsYWU',
                    [html.unescape(child['label']) + ' '] + new_badge(child), href=urljoin(ORIGIN, child['path']))]))
        link_list = element('ul', 'list-style-none NavigationContent_link-list__CaooU', desktop_links)
        articles = [post_card(post) for post in (fields.get('bentos') or {}).get('nodes', [])]
        grid = element('div', 'd-grid gap-16 lg:gap-40 Grid_grid-cols-12__k_r4C', [
            element('div', 'Grid_col-span-3__okzZv NavigationContent_articles-side-tablet__1B2Zj', [heading, link_list]),
            element('div', 'Grid_col-span-9__JZddM NavigationContent_articles-main-tablet__9CPXo', [element('div',
                'd-grid gap-16 lg:gap-24 Grid_grid-cols-3__wutCA NavigationContent_articles-grid-tablet__oLYy7', articles, role='list')])])
        if variation == 'cards':
            cards = []
            for card in fields['cards']:
                destination = card['link']['url']
                cards.append(element('div', children=[element('article',
                    'BentoSimpleCard_card__5pgXY BentoSimpleCard_xs__LVtOY NavigationContent_card__D_yxh', [
                        original_image(urljoin(MEDIA, card['image']['node']['src'])),
                        element('div', 'BentoSimpleCard_content__70Tv4', [element('a',
                            'BentoSimpleCard_title__0EWfa stretched-link NavigationContent_card-title__QV8dO',
                            [element('span', 'text-accessibility', [card['title']])], href=destination),
                            element('a', 'Button_btn__k2_e6 Button_btn-primary__twsyG Button_btn-icon__fkh69',
                                    [icon('arrow-oblique-24')], href=destination, **{'aria-label': 'Ouvrir le lien'})])])], role='listitem'))
            grid = element('div', children=[heading, element('div',
                'd-grid gap-16 lg:gap-24 Grid_grid-cols-3__wutCA margin-top-24', cards, role='list')])
        elif variation == 'magazine':
            heading.attrs['class'] += ' NavigationContent_magazine-heading__CRfvz'
            tabs = element('div', 'Tabs_list__GBFKI', [heading], role='tablist', **{'aria-orientation': 'vertical'})
            panels = []
            for i, category in enumerate(fields['magazine']):
                tab_id, panel_id = 'magazine-tab-' + str(i), 'magazine-panel-' + str(i)
                tabs.children.append(element('button', 'Tabs_trigger__eEFJa', [
                    element('span', 'Tabs_label__Bdhix', [category['subtitle']]),
                    element('span', 'Tabs_trigger-text___Omtz', [category['title'], icon('menu-arrow-24')])],
                    type='button', role='tab', id=tab_id, **{'aria-controls': panel_id,
                    'aria-selected': str(i == 0).lower(), 'data-state': 'active' if i == 0 else 'inactive',
                    'data-magazine-tab': str(i), 'data-topic-url': category['ctaButton1']['ctaButton']['action']['url']}))
                ctas = []
                for key in ['ctaButton1', 'ctaButton2']:
                    cta = category[key]['ctaButton']
                    if cta['showCta']:
                        ctas.append(element('a', 'Button_btn__k2_e6 Button_btn-primary__twsyG Button_btn-lg__8NZj_ Button_dark__QHG47',
                                            [element('span', children=[cta['label']])], href=cta['action']['url']))
                panels.append(element('div', 'Tabs_content__rHCXk panel-with-section flex-1', [
                    element('div', 'd-grid gap-16 lg:gap-40 Grid_grid-cols-2__WkXUW NavigationContent_magazine-articles__2_ZYB',
                            [post_card(post) for post in category['articles']['nodes'][:2]], role='list'),
                    element('div', 'NavigationContent_magazine-ctas__Y7BVo margin-top-40 d-flex gap-24 justify-center', ctas)],
                    role='tabpanel', id=panel_id, **{'aria-labelledby': tab_id, 'data-magazine-panel': str(i),
                    'data-state': 'active' if i == 0 else 'inactive', **({'hidden': None} if i else {})}))
            grid = element('div', 'Tabs_component__8aLAw', [tabs] + panels, **{'data-orientation': 'vertical'})
        elif variation == 'useful-links':
            useful = element('div', 'Card_card__0AegF Card_has--border__d9Hb2 border-black UsefulLinks_card__fCzxR', role='list')
            for i, link in enumerate(fields['links']):
                if i:
                    useful.children.append(element('div', 'Separator_component__5MkIb Separator_component--horizontal__tPvRQ separator',
                                                   style='background-color:hsl(var(--color--primary) / .3)'))
                file = link['file']['node']
                size = file['fileSize']
                detail = ('PDF - ' + (str(round(size / 1024)) + ' KB' if size < 1024**2 else
                                     str(round(size / 1024**2, 1)) + ' MB')) if link['isAFile'] else link['labelDetail']
                useful.children.append(element('a', 'd-flex align-center justify-between position-relative gap-16', [
                    element('div', 'w-full d-flex flex-column gap-2', [element('span', 'text-s', [link['title']]),
                        element('p', 'text-s font-weight--regular', [link['text']])]),
                    element('div', 'd-flex align-center gap-8', [element('p', 'text-s white-space-nowrap', [detail]),
                        element('span', 'Button_btn__k2_e6 Button_btn-secondary__uWJEr Button_btn-icon-xs__kMv44 UsefulLinks_btn__X6Ua1 flex-1',
                                [icon('download-24' if link['isAFile'] else 'arrow-oblique-24')])])], role='listitem',
                    href=file['mediaItemUrl'] if link['isAFile'] else html.unescape(link['link']['url']), target='_blank'))
            grid.children[0].attrs['class'] = 'Grid_col-span-3__okzZv'
            grid.children[1].attrs['class'] = 'Grid_col-span-9__JZddM'
            grid.children[1].children = [element('div', 'd-grid gap-40 lg:gap-40 Grid_grid-cols-2__WkXUW', [
                element('div', children=[element('div', 'd-grid gap-16 lg:gap-24 Grid_grid-cols-1__ZFlx_', articles[:1], role='list')]),
                element('div', children=[useful])])]
        desktop_panels.children.append(element('div', 'NavigationMenu_navigation-menu-content__sgCJI navigation-menu__content',
                                              [element('div', children=[grid])], hidden=None, **{'data-desktop-menu': label}))

    switch = copy.deepcopy(page.find(lambda n: has(n, 'AccessibilityToggle_component__Yurt_')))
    switch.attrs['class'] += ' MobileMenu_accessibility-toggle__i7zHK'
    mobile_list.children.append(element('li', 'MobileMenu_mobile-menu-item__LcUcx', [switch]))
    mobile_menu = element('div', 'MobileMenu_mobile-menu-content__qaMyk', [
        element('div', 'MobileMenu_mobile-menu-scroll__IlKXD', [element('nav', children=[mobile_list])]),
        element('div', 'MobileMenu_mobile-menu-bottom-content___dKCi', [element('a', children=[
            'COURS DE L’ACTION: RNO 25,24 € -0,08 %'], href=ORIGIN + 'finance/cours-de-laction/',
            title='Observation du 6 octobre 2026, cours non actualisé')])], id='study-mobile-menu', hidden=None,
        role='dialog', **{'aria-label': 'Menu principal', 'data-state': 'open'})
    stock = page.find(lambda n: n.tag == 'a' and n.attrs.get('aria-label') == 'Chargement en cours')
    stock.attrs['aria-label'] = 'Cours observé le 6 octobre 2026 : RNO 25,24 € -0,08 %'
    stock.children = fragment('<div class="d-flex gap-8 font-weight--semi-bold">RNO 25,24 € -0,08 %</div>')
    cookie = page.find(lambda n: n.attrs.get('id') == 'ot-sdk-btn')
    cookie.tag = 'a'
    cookie.attrs['href'] = ORIGIN + 'utilisation-des-cookies/'
    event_trigger = page.find(lambda n: n.tag == 'button' and n.children and n.children[0].text == 'Évènement')
    event_trigger.children.append(element('sup', 'NavigationMenu_navigation-menu-sup__XHXKy NavigationMenu_type-upcoming__G78nE', ['J-5']))

    # Scripts from the source (analytics, session feedback, React runtime) are omitted.
    svg_case = {'viewbox': 'viewBox', 'preserveaspectratio': 'preserveAspectRatio', 'gradientunits': 'gradientUnits',
                'gradienttransform': 'gradientTransform', 'clippathunits': 'clipPathUnits'}
    def clean(node):
        node.children = [child for child in node.children if child.tag not in ['script', 'noscript']]
        for key in list(node.attrs):
            if key.startswith('on') or key == '__typename':
                del node.attrs[key]
            elif key in svg_case:
                node.attrs[svg_case[key]] = node.attrs.pop(key)
        if node.tag == 'img':
            node.attrs['src'] = media(node.attrs['src'])
            node.attrs.pop('srcset', None)
            node.attrs.pop('sizes', None)
        if node.tag == 'a' and node.attrs.get('href', '').startswith('/'):
            node.attrs['href'] = urljoin(ORIGIN, node.attrs['href'])
        for child in node.children:
            clean(child)
    for part in [page, sprite, mobile_menu, desktop_panels]:
        clean(part)

    stylesheet_names = ['14b0e0c313-7d3d1a6fb95c05ae.css', '13423d8da0-453140c5190c29d8.css']
    css = ''
    for name in stylesheet_names:
        style = (ROOT / 'renault-assets' / name).read_text()
        source_url = next(row['source_url'] for row in assets if Path(row['path']).name == name)
        def rewrite(match):
            value = match[1].strip(' \t\n\r\'"')
            if value.startswith(('data:', '#')):
                return match[0]
            absolute = urljoin(source_url, value)
            return 'url("' + (quote(Path(local[absolute]).name) if absolute in local else absolute) + '")'
        css += re.sub(r'url\(([^)]+)\)', rewrite, style) + '\n'
    css += (Path(__file__).with_name('renault_draft.css')).read_text()
    (ROOT / 'renault-assets/display.css').write_text(css)
    js = (Path(__file__).with_name('renault_draft.js')).read_text()
    head = '<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">' \
           '<title>Renault Group — étude de la page officielle du 6 octobre 2026</title><link rel="stylesheet" href="renault-assets/display.css"></head>'
    search_data = data['globalOptions']['general']['search']
    popular = element('div', children=[element('h5', 'margin-top-none margin-bottom-24', ['Recherches populaires']),
        element('div', 'd-grid gap-16 lg:gap-16 Grid_grid-cols-1__ZFlx_ justify-content-start', [
            element('a', 'text-s font-weight--semi-bold', [row['link']['title']], href=row['link']['url'], role='listitem')
            for row in search_data['popularSearches']])])
    useful = element('div', 'Card_card__0AegF Card_has--border__d9Hb2 border-black UsefulLinks_card__fCzxR',
                     [element('p', 'text-s font-weight--semi-bold', ['Liens utiles'])], role='list')
    for i, row in enumerate(search_data['usefulLinks']):
        file = row['file']['node']
        detail = 'PDF - ' + str(round(file['fileSize'] / 1024**2, 1)) + ' MB'
        if i:
            useful.children.append(element('div', 'Separator_component__5MkIb Separator_component--horizontal__tPvRQ separator',
                                           style='background-color:hsl(var(--color--primary) / .3)'))
        useful.children.append(element('a', 'd-flex align-center justify-between position-relative gap-16', [
            element('div', 'w-full d-flex flex-column gap-2', [element('span', 'text-s', [row['title']]),
                element('div', 'd-flex align-center justify-between gap-8', [element('p', 'text-s font-weight--regular', [row['text']]),
                    element('div', 'd-flex align-center gap-8', [element('p', 'text-s white-space-nowrap', [detail]),
                        element('span', 'Button_btn__k2_e6 Button_btn-secondary__uWJEr Button_btn-icon-xs__kMv44 UsefulLinks_btn__X6Ua1 flex-1 UsefulLinks_btn--compact__9ED8p',
                                [icon('download-24')])])])])], href=file['mediaItemUrl'], target='_blank', role='listitem'))
    search = element('dialog', 'Dialog_dialog-content__RMlrT SearchGlobal_dialog__IgFTJ gap-0', [
        element('button', 'Dialog_dialog-close__K_1hW', [icon('close-24'), element('span', 'sr-only', ['Fermer'])],
                type='button', **{'data-dialog-close': '', 'aria-label': 'Fermer'}),
        element('div', 'SearchGlobal_overlay__CboVD', [element('div', 'Container_component__CxkWy SearchGlobal_container__ZszhJ', [
            element('form', children=[element('div', 'InputWrapper_input-wrapper__P6VGx', [
                element('button', 'Button_btn__k2_e6 Button_btn-simple__hkwRc Button_btn-icon-xs__kMv44 Button_dark__QHG47',
                        [icon('search-24')], type='submit', **{'aria-label': 'Rechercher'}),
                element('input', 'InputWrapper_input__ICjqq', type='search', name='query', placeholder='Recherche', required=None,
                        **{'aria-label': 'Recherche'})])], action=ORIGIN + 'search/', method='get'),
            element('div', 'SearchGlobal_state-swap__nzaAx', [element('div', 'SearchGlobal_state__YSwpD SearchGlobal_state--visible__aE1DZ', [
                element('div', 'd-grid gap-32 lg:gap-96 Grid_grid-cols-1__ZFlx_ Grid_md__grid-cols-2__vUo8o',
                        [popular, element('div', children=[useful])])], **{'aria-hidden': 'false'})])])])],
        id='study-search', **{'aria-label': 'Recherche', 'data-state': 'closed'})
    help_dialog = element('div', 'Popover_popover-content__ReT6q AccessibilityToggle_tooltip__U1Hjg', [
        "Ce bouton d'accessibilité vous permet d'afficher notre site Web dans une version accessible.",
        element('span', 'd-block font-weight--semi-bold margin-top-16', [
            "Pour en savoir plus sur notre conformité aux normes d'accessibilité, ",
            element('a', 'text-decoration-underline', ['cliquez ici'], href=ORIGIN + 'accessibilite/'), '.'])],
        id='study-help', role='dialog', hidden=None, tabindex='-1')
    (ROOT / 'renault.html').write_text(head + '<body class="header-no-news">' + sprite.render() + page.render() +
                                      mobile_menu.render() + desktop_panels.render() + search.render() + help_dialog.render() +
                                      '<script>' + js + '</script></body></html>')
    print(json.dumps({'draft': 'renault.html', 'draft_main_images': sum(n.tag == 'img' for n in main_node.walk()),
                      'captured_assets': len(assets)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
