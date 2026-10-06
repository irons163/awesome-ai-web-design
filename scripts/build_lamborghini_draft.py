#!/usr/bin/env python3
"""Correct the Stitch study with dated public DOM, styles and original media."""
import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, quote

ROOT = Path(__file__).resolve().parents[1] / '.stitch-work/current-official'
ORIGIN = 'https://www.lamborghini.com'
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}
SOURCE_ICONS = {}


class Node:
    def __init__(self, tag='', attributes=None, children=None):
        self.tag, self.a, self.children = tag, dict(attributes or []), children or []

    def all(self, predicate):
        result = [self] if predicate(self) else []
        for child in self.children:
            if isinstance(child, Node):
                result.extend(child.all(predicate))
        return result

    def cls(self, name):
        return name in self.a.get('class', '').split()

    def first(self, predicate):
        return self.all(predicate)[0]

    def render(self):
        if self.tag in {'script', 'style', 'noscript'}:
            return ''
        children = ''.join(c.render() if isinstance(c, Node) else html.escape(c, quote=False) for c in self.children)
        if not self.tag:
            return children
        attributes = []
        for key, value in self.a.items():
            if key.startswith('on') or key == 'data-layer':
                continue
            if key in ('href', 'src', 'poster') and value and value.startswith('/'):
                value = urljoin(ORIGIN, value)
            attributes.append(' ' + key + ('' if value is None else '="' + html.escape(value, quote=True) + '"'))
        start = '<' + self.tag + ''.join(attributes) + '>'
        return start if self.tag in VOID else start + children + '</' + self.tag + '>'


class Tree(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node()
        self.stack = [self.root]

    def handle_starttag(self, tag, attributes):
        node = Node(tag, attributes)
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attributes):
        self.handle_starttag(tag, attributes)
        if tag not in VOID:
            self.stack.pop()

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                self.stack = self.stack[:i]
                break

    def handle_data(self, value):
        self.stack[-1].children.append(value)


def image(url, alt='', classes='', style=''):
    return Node('img', {'src': urljoin(ORIGIN, url), 'alt': alt, 'class': classes, 'style': style})


def fill_image(url, alt='', mode='contain', ratio=None):
    style = 'box-sizing:border-box;display:block;overflow:hidden;position:relative;'
    if ratio is not None:
        style += 'padding-top:' + str(ratio) + '%;'
    else:
        style += 'position:absolute;inset:0;'
    return Node('span', {'style': style}, [image(url, alt, 'css-ns94h9',
               'position:absolute;inset:0;width:100%;height:100%;object-fit:' + mode + ';')])


def action_link(action, gallery=False):
    label = next(r['value'][0] for r in action['labels'] if r['key'] == 'title_primary')
    style = action.get('ctaStyleFacelift', {}).get('value', ['primary'])[0]
    button = action.get('ctaType', {}).get('value', ['link'])[0] == 'button'
    attributes = {'class': ('' if gallery else 'slide-cta ') +
                  'btn-' + style + (' btn-large' if gallery else ' btn-medium') +
                  ' has-icon ' + ('css-1cj9f0q' if button else 'css-v977j5')}
    for field in action.get('attributes', []):
        if field['key'] in {'aria-label', 'data-target'} and '{{' not in field['value'][0]:
            attributes[field['key']] = field['value'][0]
    if button:
        attributes['type'] = 'button'
    else:
        attributes['href'] = action['url']['url']
    path = ('M2 5V19H22V5H2ZM3 6H21L14.293 13H9.707L3 6ZM3 7.707L7.793 12.5L3 17.293V7.707ZM16.207 12.5L21 7.707V17.293L16.207 12.5Z'
            if label.lower() == 'enquire' else 'M16.4133 6L15.5553 6.92298L19.6739 11.3473H2V12.6527H19.6739L15.5541 17.077L16.4145 18L22 12L16.4145 6H16.4133Z')
    icon = SOURCE_ICONS.get(label.lower()) or Node('svg', {'aria-hidden': 'true', 'class': 'icon light', 'width': '24', 'height': '24',
                       'viewBox': '0 0 24 24', 'fill': 'none'}, [Node('path', {'d': path, 'fill': 'currentColor'})])
    return Node('button' if button else 'a', attributes, [Node('span', children=[label]), icon])


def main():
    raw = (ROOT / 'lamborghini-source-current.html').read_text()
    content = json.loads((ROOT / 'lamborghini-content-reference.json').read_text())
    assets = json.loads((ROOT / 'lamborghini-asset-provenance.json').read_text())['assets']
    local = {r['source_url']: r['path'] for r in assets}
    parser = Tree()
    parser.feed(raw)
    root = parser.root.first(lambda n: n.a.get('id') == '__next')
    original_actions = root.first(lambda n: n.cls('model__actions'))
    for node in original_actions.all(lambda n: n.tag in {'a', 'button'}):
        label = ''.join(c for c in node.first(lambda n: n.tag == 'span').children if isinstance(c, str))
        SOURCE_ICONS[label.lower()] = node.first(lambda n: n.tag == 'svg')
    styles = [r for r in assets if r['path'].endswith('.css')]
    order = ['tokens.css', 'de7cede1cbf6622f.css', '1276aad8662927b5.css']
    css = '\n'.join((ROOT / next(r['path'] for r in styles if r['source_url'].endswith(name))).read_text() for name in order)
    css += '\n' + '\n'.join(re.findall(r'<style[^>]*>(.*?)</style>', raw, re.S))

    def css_url(match):
        value = match[1].strip(' \t\n\r\'"')
        absolute = urljoin(ORIGIN, value)
        if absolute in local:
            return 'url("' + quote(Path(local[absolute]).name) + '")'
        if value.startswith('/'):
            return 'url("' + absolute + '")'
        return match[0]

    css = re.sub(r'url\(([^)]+)\)', css_url, css)
    css += '''
.lam-hero-slide__header{opacity:1!important;animation:none!important}
#burger-menu{top:104px}#burger-menu:not(.open){visibility:hidden;pointer-events:none}
#burger-menu.open{visibility:visible;pointer-events:auto}.lam-header.menu-open:before{opacity:1}
#hero-film{width:100%;height:100%;object-fit:cover;display:block}
#families-gallery .swiper-slide{flex-shrink:0;width:900px}
#families-gallery .swiper-wrapper{align-items:flex-start;transition:transform .5s ease}
#families-gallery .carousel-item__image--images{position:relative}
#model-chooser .react-tabs__tab-list-wrapper{overflow-x:auto;scrollbar-width:none}
#model-chooser .react-tabs__tab-list{flex-wrap:nowrap;white-space:nowrap}
.css-1scxgtc{position:absolute;height:100%;width:calc(100% + 7rem);left:-3.5rem;pointer-events:none;display:flex;justify-content:space-between;align-items:center}
.css-1scxgtc .right-arrow,.css-1scxgtc .left-arrow{pointer-events:auto}
.menu-study-preview{padding-top:24px;white-space:normal}.menu-study-preview img{width:100%;object-fit:contain}
.study-dialog{max-width:min(820px,calc(100vw - 32px));border:0;background:#181818;color:white;padding:32px}
.study-dialog::backdrop{background:#000b}.study-dialog img{max-width:100%}
@media(max-width:991.98px){#families-gallery .swiper-slide{width:100%}#families-gallery .lam-carousel__controls{display:none}#families-gallery .react-tabs__tab-list{display:none}}
@media(min-width:992px){#families-gallery .lam-carousel__footer{display:none}}
@media(max-width:767.98px){#burger-menu{top:80px}.menu-study-preview{display:none}.css-1scxgtc .right-arrow,.css-1scxgtc .left-arrow{min-width:auto!important}}
@media(prefers-reduced-motion:reduce){*,*:before,*:after{animation:none!important;transition:none!important}}
'''
    (ROOT / 'lamborghini-assets/display.css').write_text(css)
    hero = root.first(lambda n: n.a.get('id') == 'hero-banner')
    hero_slide = hero.first(lambda n: n.cls('lam-hero-slide'))
    video = Node('div', {'class': 'lam-hero-slide__video css-i47aud'}, [Node('video', {
        'id': 'hero-film', 'muted': None, 'autoplay': None, 'loop': None, 'playsinline': None,
        'poster': 'https://medialamborghini-meride-tv.akamaized.net/meride/lamborghini/video/images/folder1/2846/1786627119hero.jpg'})])
    hero_slide.children.insert(0, video)
    for n in hero.all(lambda n: n.cls('swiper-slide')):
        n.a['class'] += ' swiper-slide-active'
    texts = content['elements'][0]['hbSlide'][0]['hbSlideObjects'][1]
    hero.first(lambda n: n.cls('lam-hero-slide__cols')).children.append(Node('div', {
        'class': 'lam-hero-slide__col-right'}, [Node('div', {'class': 'lam-hero-slide__actions'},
        [action_link(a) for a in texts['callToActions']])]))
    eyelet = hero.first(lambda n: n.cls('lam-hero-slide__eyelet'))
    sentence = ''.join(c for c in eyelet.children if isinstance(c, str))
    eyelet.children = []
    for index, word in enumerate(sentence.split()):
        if index:
            eyelet.children.append(' ')
        attributes = {'aria-hidden': 'true', 'style': 'position:relative;display:inline-block'}
        eyelet.children.append(Node('div', attributes, [Node('div', attributes, [letter]) for letter in word]))

    gallery = root.first(lambda n: n.a.get('id') == 'families-gallery')
    gallery.first(lambda n: n.cls('swiper')).a['class'] += ' swiper-initialized swiper-horizontal swiper-autoheight swiper-watch-progress swiper-backface-hidden'
    families = content['elements'][2]['subElements']
    slides = gallery.all(lambda n: n.cls('swiper-slide'))
    gallery_models = []
    for i, (slide, family) in enumerate(zip(slides, families)):
        slide.a['class'] += ' swiper-slide-active' if i == 0 else ''
        marks = family['image'][0]
        mark = Node('picture', children=[Node('source', {'media': '(max-width:991.98px)', 'srcset': urljoin(ORIGIN, marks.get('mobile', marks['desktop'])['url'])}),
                    image(marks['desktop']['url'], 'Lamborghini ' + str(i + 1), 'carousel-item__logo carousel-item__logo--images css-1f1o7mt')])
        slide.first(lambda n: n.cls('carousel-item__logo-container')).children = [mark]
        model = family['subElements'][0]
        picture = model['image'][0]['desktop']
        inner = slide.first(lambda n: n.cls('carousel-item__inner'))
        inner.children.append(Node('div', {'class': 'carousel-item__image carousel-item__image--images css-81cm2m'},
                                   [fill_image(picture['url'], picture.get('alt', ''))]))
        family_panels = slide.all(lambda n: n.a.get('role') == 'tabpanel')
        for panel, member in zip(family_panels, family['subElements']):
            panel.children = [Node('div', {'class': 'react-tabs__tab-panel-content'},
                                   [action_link(a, True) for a in member['callToActions']])]
        if not family_panels:
            slide.first(lambda n: n.cls('carousel-item__children')).children = [Node('div', {
                'class': 'react-tabs__tab-panel-content'}, [action_link(a, True) for a in model['callToActions']])]
        actions = slide.first(lambda n: n.cls('carousel-item__children'))
        actions.children = [Node('div', {'class': 'd-none d-lg-block'}, actions.children), Node('div', {
            'class': 'd-block d-lg-none'}, [Node('div', {'class': 'family-gallery__ctas'},
            [action_link(a, True) for a in model['callToActions']])])]
        gallery_models.append([{'image': urljoin(ORIGIN, m['image'][0]['desktop']['url']),
                                'disclaimer': family.get('disclaimerBanner', '')} for m in family['subElements']])
    disclaimer = Tree()
    disclaimer.feed(families[0]['disclaimerBanner'])
    gallery.first(lambda n: n.cls('consumption-emissions-section')).children = [Node('div', {
        'class': 'container container-hero'}, [Node('span', children=disclaimer.root.children)])]
    gallery.first(lambda n: n.cls('lam-carousel__footer')).children = [Node('div', {
        'class': 'study-pagination lam-carousel__pagination lam-carousel__pagination--images lam-carousel__pagination--bullets swiper-pagination swiper-pagination-clickable swiper-pagination-bullets swiper-pagination-horizontal'},
        [Node('span', {'role': 'button', 'tabindex': '0', 'class': 'swiper-pagination-bullet' + (' swiper-pagination-bullet-active' if i == 0 else ''),
        'aria-label': 'Go to slide ' + str(i + 1), 'data-slide': str(i), 'aria-current': 'true' if i == 0 else 'false'}) for i in range(len(slides))])]

    banner = root.first(lambda n: n.a.get('id') == 'banner')
    art = content['elements'][3]['image'][0]
    banner.first(lambda n: n.cls('lam-banner')).children.insert(0, Node('div', {'class': 'lam-banner__image'}, [Node('picture', children=[
        Node('source', {'media': '(max-width:767.98px)', 'srcset': urljoin(ORIGIN, art['mobile']['url'])}),
        image(art['desktop']['url'], art['desktop'].get('alt', ''), '', 'width:100%;height:100%;object-fit:cover')])]))

    chooser = root.first(lambda n: n.a.get('id') == 'model-chooser')
    chooser.first(lambda n: n.cls('react-tabs__tab-list-wrapper')).children.append(Node('div', {'class': 'css-1scxgtc'}, [
        Node('button', {'type': 'button', 'aria-label': 'Scroll ' + name, 'class': side + '-arrow btn-ghost btn-medium has-icon css-1cj9f0q'},
            [Node('svg', {'aria-hidden': 'true', 'class': 'icon light', 'width': '24', 'height': '24', 'viewBox': '0 0 24 24', 'fill': 'none'},
                [Node('path', {'d': path, 'fill': 'currentColor'})])])
        for name, side, path in [('previous', 'left', 'M15.646 22.354L5.29297 12L15.647 1.646L16.353 2.353L6.70697 12L16.353 21.646L15.646 22.354Z'),
        ('next', 'right', 'M8.35397 22.354L7.64697 21.647L17.293 12L7.64697 2.35397L8.35297 1.64697L18.707 12L8.35297 22.354H8.35397Z')]]))
    models = content['elements'][4]['itemModelChooser']
    panels = chooser.all(lambda n: n.a.get('role') == 'tabpanel')
    for panel, model in zip(panels, models):
        for n in panel.all(lambda n: n.cls('model__image')):
            mode = 'desktop' if n.cls('d-lg-block') else 'mobile'
            art = model['image'][0].get(mode, model['image'][0]['desktop'])
            ratio = float(art['height']) / float(art['width']) * 100
            n.children = [fill_image(art['url'], art.get('alt', ''), 'contain', ratio)]
        panel.first(lambda n: n.cls('consumption-emissions-section')).children = [Node('span', children=[model.get('disclaimerBanner', '')])]

    for n in root.all(lambda n: n.tag == 'img'):
        absolute = urljoin(ORIGIN, n.a.get('src', ''))
        if absolute in local and urlsplit(absolute).path.endswith('.svg'):
            n.a['src'] = quote(local[absolute], safe='/')
    for n in root.all(lambda n: n.tag == 'source'):
        absolute = urljoin(ORIGIN, n.a.get('srcset', ''))
        if absolute in local and urlsplit(absolute).path.endswith('.svg'):
            n.a['srcset'] = quote(local[absolute], safe='/')
    for n in root.all(lambda n: True):
        n.children = [c.replace('Copyright © null', 'Copyright © 2026') if isinstance(c, str) else c for c in n.children]
        if n.a.get('href') == '#onetrust-settings':
            n.a['href'] = ORIGIN + '/en-en#onetrust-settings'

    menus = content['header']['menus'][0]['values']
    services = {}
    for item in content['footer'].get('subElements', []):
        ids = [v['value'][0] for v in item.get('componentSettings', {}).get('attributes', []) if v.get('key') == 'id']
        if not ids:
            continue
        for child in item.get('subElements', []):
            for label in child.get('labelsLong', []):
                if label.get('key') == 'iframe_src':
                    services[ids[0]] = urljoin(ORIGIN, label['value'][0])
            art = child.get('desktop')
            if art and ids[0] in {'eu-warranty-label', 'legal-guarantee-notice-en'}:
                services[ids[0]] = urljoin(ORIGIN, art['url'])
    services['form-model-temerario'] = services['form-modal-temerario']
    services['form-model-revuelto'] = services['form-modal-revuelto']
    services['form-model-urus-se'] = services['form-modal-urus-se']
    for link in root.all(lambda n: n.tag == 'a' and n.a.get('data-target') in services):
        link.a['href'] = services[link.a['data-target']]
    initial_menu = root.first(lambda n: n.a.get('id') == 'burger-content').render()
    script = (Path(__file__).with_name('lamborghini_interactions.js')).read_text()
    state = {'families': gallery_models, 'menus': menus, 'initialMenu': initial_menu, 'services': services,
             'desktopVideo': 'https://videolamborghini-meride-tv.akamaized.net/video/folder2/1786627119hero_lamborghini/1786627119hero_lamborghini.m3u8',
             'mobileVideo': 'https://videolamborghini-meride-tv.akamaized.net/video/folder2/1786627187hero_mobile_lamborghini/1786627187hero_mobile_lamborghini.m3u8'}
    document = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Lamborghini — current official-site study</title><link rel="stylesheet" href="lamborghini-assets/display.css"></head><body>'
    document += root.render() + '<script src="runwayml-assets/hls.light.min.js"></script><script>'
    document += 'const sourceReference=' + json.dumps(state, ensure_ascii=False).replace('</', '<\\/') + ';\n' + script
    document += '</script></body></html>'
    (ROOT / 'lamborghini.html').write_text(document)
    print('Built source-corrected Lamborghini draft with original responsive artwork and styles')


if __name__ == '__main__':
    main()
