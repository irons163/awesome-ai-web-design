#!/usr/bin/env python3
"""Separate refinement of genuine Stitch exports from dated public DOM/CSS.

Original Stitch HTML/PNG and bundled brand files are never modified. Browser
exports exclude scripts, runtime stores, account frames and entered values.
"""
import hashlib
import html
import json
import re
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / '.stitch-work/current-official'
ORIGIN = 'https://www.binance.com/en'
PROVENANCE = json.loads((WORK / 'binance-asset-provenance.json').read_text())
ASSETS = {a['source_url']: a for a in PROVENANCE['assets']}
REFERENCES = {k: json.loads((WORK / f'binance-{k}-browser-export.json').read_text()) for k in ('desktop', 'mobile')}
INTERACTIONS = json.loads((WORK / 'binance-interactions-browser-export.json').read_text())
VOID = {'img', 'input', 'br', 'hr', 'source', 'meta', 'link'}
SVG_RE = re.compile(r'<svg\b[\s\S]*?</svg>', re.I)
OLD_ATTRS = {'class', 'id', 'style', 'href', 'src', 'srcset', 'alt', 'width', 'height', 'viewbox', 'fill', 'd', 'stroke', 'stroke-width', 'fill-rule', 'clip-rule', 'preserveaspectratio', 'points', 'x', 'y', 'x1', 'y1', 'x2', 'y2', 'rx', 'ry', 'xmlns', 'xmlns:xlink', 'xlink:href', 'type', 'placeholder', 'role', 'disabled', 'checked', 'selected', 'tabindex', 'for', 'rel', 'target', 'loading', 'aria-label', 'aria-hidden', 'aria-expanded', 'aria-selected', 'aria-controls', 'aria-labelledby', 'data-state'}


class Fingerprint(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []

    def handle_starttag(self, tag, attrs):
        self.parts.append((tag, tuple(sorted((k, v or '') for k, v in attrs if k in OLD_ATTRS))))

    handle_startendtag = handle_starttag

    def handle_data(self, data):
        if data.strip():
            self.parts.append(data.strip())


def fingerprint(markup):
    parser = Fingerprint()
    parser.feed(markup)
    return repr(parser.parts)


class Node:
    def __init__(self, tag='', attrs=(), parent=None, text=None, raw=None):
        self.tag, self.attrs, self.parent = tag, dict(attrs), parent
        self.children, self.data, self.raw = [], text, raw

    def walk(self):
        yield self
        for child in self.children:
            yield from child.walk()

    def text(self):
        return self.data or ''.join(n.text() for n in self.children)

    def addclass(self, name):
        self.attrs['class'] = (self.attrs.get('class', '') + ' ' + name).strip()

    def render(self):
        if self.raw is not None:
            return self.raw
        if self.data is not None:
            return html.escape(self.data, quote=False)
        content = ''.join(n.render() for n in self.children)
        if not self.tag:
            return content
        attrs = ''.join(' ' + k + ('="' + html.escape(v, quote=True) + '"' if v is not None else '') for k, v in self.attrs.items())
        return '<' + self.tag + attrs + '>' + ('' if self.tag in VOID else content + '</' + self.tag + '>')


class Tree(HTMLParser):
    def __init__(self, markup, svgs):
        super().__init__(convert_charrefs=True)
        self.root = self.current = Node()
        self.svgs = svgs
        self.feed(markup)

    def handle_starttag(self, tag, attrs):
        if tag == 'study-svg':
            self.current.children.append(Node(raw=self.svgs[int(dict(attrs)['index'])], parent=self.current))
            return
        attrs = [(k, v) for k, v in attrs if not k.startswith('on') and k not in ('value', 'data-reactroot')]
        node = Node(tag, attrs, self.current)
        self.current.children.append(node)
        if tag not in VOID:
            self.current = node

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID and tag != 'study-svg':
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag == 'study-svg':
            return
        current = self.current
        while current.parent:
            if current.tag == tag:
                self.current = current.parent
                break
            current = current.parent

    def handle_data(self, data):
        if self.current.tag == 'style':
            # Rendered-reference serialization escaped stylesheet text. Style
            # elements are raw-text HTML nodes; decode that one layer before
            # localizing their observed URLs instead of escaping CSS again.
            self.current.children.append(Node(raw=css_text(html.unescape(data)), parent=self.current))
        else:
            self.current.children.append(Node(text=data, parent=self.current))


def local_url(url):
    absolute = urljoin(ORIGIN, url)
    return ASSETS[absolute]['path'] if absolute in ASSETS else absolute


SVG_MATCHES = defaultdict(int)


def prepare(markup, mode, root_name=None, prefix_ids=True):
    markup = re.sub(r'<(?:script|iframe|noscript)\b[\s\S]*?</(?:script|iframe|noscript)>', '', markup, flags=re.I)
    candidates = defaultdict(list)
    for raw in INTERACTIONS['svg_original_markup'].get(mode, {}).get(root_name, []):
        candidates[fingerprint(raw)].append(raw)
    svgs = []
    def svg_placeholder(match):
        raw = match.group()
        choices = candidates.get(fingerprint(raw))
        if choices:
            raw = choices[0]
            SVG_MATCHES[mode] += 1
        svgs.append(raw)
        return f'<study-svg index="{len(svgs)-1}"></study-svg>'
    tree = Tree(SVG_RE.sub(svg_placeholder, markup), svgs).root
    ids = defaultdict(int)
    id_map = {}
    for node in tree.walk():
        if node.attrs.get('style'):
            style = css_text(html.unescape(node.attrs['style']))
            # Safe local/CDN URL tokens need no CSS quotes inside an HTML
            # attribute. Keep quoting for any URL containing CSS delimiters.
            node.attrs['style'] = re.sub(r'url\("([^"\s()\\]+)"\)', r'url(\1)', style)
        for key in ('src', 'href'):
            if node.attrs.get(key) and not node.attrs[key].startswith('#'):
                node.attrs[key] = local_url(node.attrs[key]) if key == 'src' else urljoin(ORIGIN, node.attrs[key])
        if node.attrs.get('srcset'):
            node.attrs['srcset'] = ', '.join(local_url(part.strip().split()[0]) + (' ' + ' '.join(part.strip().split()[1:]) if len(part.strip().split()) > 1 else '') for part in node.attrs['srcset'].split(','))
        old_id = node.attrs.get('id')
        if old_id and prefix_ids:
            ids[old_id] += 1
            node.attrs['id'] = mode + '-' + old_id + (f'-{ids[old_id]}' if ids[old_id] > 1 else '')
            id_map.setdefault(old_id, node.attrs['id'])
            if old_id == '__APP':
                node.addclass('study-app')
    for node in tree.walk():
        for key in ('aria-controls', 'aria-labelledby', 'for'):
            if node.attrs.get(key):
                node.attrs[key] = ' '.join(id_map.get(value, value) for value in node.attrs[key].split())
    return tree


def descendants(node, role):
    return [n for n in node.walk() if n.attrs.get('role') == role]


def annotate(tree, mode):
    for row in tree.walk():
        if 'faq-item-widget' in row.attrs.get('class', '').split():
            parts = [n for n in row.children if n.tag]
            if len(parts) >= 2:
                trigger, answer = parts[0], parts[-1]
                trigger.attrs.update({'role': 'button', 'tabindex': '0', 'aria-expanded': 'false'})
                trigger.addclass('study-faq-trigger')
                answer.addclass('study-faq-answer')
                answer.attrs['id'] = f'{mode}-faq-{sum(1 for n in tree.walk() if n.attrs.get("class", "").find("study-faq-answer") >= 0)}'
                trigger.attrs['aria-controls'] = answer.attrs['id']
                trigger.attrs['aria-label'] = next(n.text().strip() for n in trigger.walk() if n.tag == 'h2')
        if row.tag == 'h3' and 'footer-navlist-title' in row.attrs.get('class', ''):
            parent = row.parent
            if any(n.tag == 'ul' for n in parent.children):
                parent.addclass('study-footer-group')
                row.attrs.update({'role': 'button', 'tabindex': '0', 'aria-expanded': 'false', 'aria-label': row.text().strip()})
    market_number = 0
    for tablist in descendants(tree, 'tablist'):
        tabs = descendants(tablist, 'tab')
        labels = [t.text().strip() for t in tabs]
        if labels == ['Popular', 'New Listing', 'Stocks', 'tCommodities']:
            owner = tablist.parent
            while owner.parent and not descendants(owner, 'tabpanel'):
                owner = owner.parent
            owner.addclass('study-market')
            owner.attrs['data-study-market'] = str(market_number)
            panel_id = f'{mode}-market-panel-{market_number}'
            for i, tab in enumerate(tabs):
                tab.attrs['id'] = f'{mode}-market-tab-{market_number}-{i}'
                tab.attrs['aria-controls'] = panel_id
                tab.attrs['data-study-market-tab'] = labels[i]
                tab.attrs['tabindex'] = '0' if i == 0 else '-1'
            for panel in descendants(owner, 'tabpanel'):
                panel.attrs['id'] = panel_id
                panel.attrs['aria-labelledby'] = tabs[0].attrs['id']
            market_number += 1
        elif labels == ['Mobile', 'Desktop']:
            for tab in tabs:
                tab.attrs['data-study-download-tab'] = tab.text().strip()


def css_text(text, base=ORIGIN):
    def replace_url(match):
        raw = match.group(1).strip().strip('"\'')
        if raw.startswith(('data:', '#')):
            return match.group()
        absolute = urljoin(base, raw)
        return 'url("' + (ASSETS[absolute]['path'] if absolute in ASSETS else absolute) + '")'
    text = re.sub(r'url\(([^)]+)\)', replace_url, text)
    text = re.sub(r'#__APP(?![\w-])', '.study-app', text)
    # The original mobile rule hides this exact id. IDs are namespaced to
    # keep the separately captured desktop/mobile trees accessible.
    return text.replace('#toRegisterPage', ':is(#desktop-toRegisterPage,#mobile-toRegisterPage,#menu-mobile-toRegisterPage)')


def main():
    for asset in PROVENANCE['assets']:
        assert hashlib.sha256((WORK / asset['path']).read_bytes()).hexdigest() == asset['sha256']
    for export in json.loads((WORK / 'binance-stitch-downloads.json').read_text()):
        assert hashlib.sha256((WORK / export['path']).read_bytes()).hexdigest() == export['sha256']
    blocks, templates = [], []
    for mode, reference in REFERENCES.items():
        roots = []
        for key in ('__APP_HEADER', '__APP', '__APP_FOOTER'):
            tree = prepare(reference['roots'][key], mode, key)
            annotate(tree, mode)
            roots.append(tree.render())
        blocks.append(f'<div class="study-branch study-{mode}" data-study-branch="{mode}">' + ''.join(roots) + '</div>')
        for label, snapshot in INTERACTIONS['market_states'][mode].items():
            panel = snapshot['panel'][0]['html']
            tree = prepare(panel, mode)
            templates.append(f'<template data-study-market-template="{mode}:{label}">' + tree.render() + '</template>')
    desktop_download = prepare(INTERACTIONS['download_desktop']['html'], 'desktop')
    annotate(desktop_download, 'desktop')
    templates.append('<template data-study-download-template="Desktop">' + desktop_download.render() + '</template>')
    desktop_app = prepare(REFERENCES['desktop']['roots']['__APP'], 'desktop')
    app = next(n for n in desktop_app.walk() if n.attrs.get('id') == 'desktop-__APP')
    section_parent = next(n for n in app.children if n.tag)
    mobile_download = [n for n in section_parent.children if n.tag][3]
    annotate(mobile_download, 'desktop')
    templates.append('<template data-study-download-template="Mobile">' + mobile_download.render() + '</template>')
    for key, snapshot in INTERACTIONS['desktop_menus'].items():
        if snapshot['html']:
            templates.append(f'<template data-study-desktop-menu="{key}">' + prepare(snapshot['html'], 'menu-' + key).render() + '</template>')
    templates.append('<template data-study-mobile-menu>' + prepare(INTERACTIONS['mobile_menu']['html'], 'menu-mobile').render() + '</template>')
    templates.append('<template data-study-cookie-manager>' + prepare(INTERACTIONS['cookie_manager_open']['html'], 'cookie-manager').render() + '</template>')
    for label, snapshot in INTERACTIONS['cookie_categories_open'].items():
        templates.append(f'<template data-study-cookie-category="{label}">' + prepare(snapshot['html'], 'cookie-category-' + label.split()[0].lower()).render() + '</template>')
    minus_svg = SVG_RE.search(INTERACTIONS['faq_first_open']['html']).group()
    templates.append('<template data-study-minus>' + minus_svg + '</template>')
    style = ''
    for entry in INTERACTIONS['stylesheet_order']:
        if 'href' in entry and entry['href'] in ASSETS:
            sheet = css_text((WORK / ASSETS[entry['href']]['path']).read_text(), entry['href'])
            if '/static/cookie-manager/' in entry['href']:
                # The official page loads this stylesheet only when its
                # preference modal first opens. Its global reset changes
                # body/footer geometry, so preserve that observed timing.
                templates.append('<template data-study-cookie-styles><style>' + sheet + '</style></template>')
            else:
                style += '\n' + sheet
        elif 'text' in entry:
            style += '\n' + css_text(entry['text'])
    style += '\n' + (ROOT / 'scripts/binance-current-official.css').read_text()
    sprite = INTERACTIONS['svg_original_markup']['sprite']
    cookie_roots = ''.join(prepare(REFERENCES['desktop']['roots'].get(n) or '', 'cookie', prefix_ids=False).render() for n in ('cm-banner-sdk', 'onetrust-consent-sdk', 'pre-chat-container'))
    source_seed = (WORK / 'binance-stitch-desktop-raw.html').read_bytes()
    seed_hash = hashlib.sha256(source_seed).hexdigest()
    script = (ROOT / 'scripts/binance-current-official.js').read_text()
    markup = ('<!doctype html><html lang="en" dir="ltr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
              '<title>Binance · 官網研究草稿</title><meta name="description" content="Dated free study of the public Binance homepage; visual acceptance pending.">'
              '<meta name="stitch-native-seed-sha256" content="' + seed_hash + '"><style>' + style + '</style></head><body class="theme-root dark ltr">'
              + '<div id="common-widget-icon-sprite">' + sprite + '</div>' + ''.join(blocks) + cookie_roots + ''.join(templates)
              + '<script>' + script + '</script></body></html>')
    (WORK / 'binance.html').write_text(markup)
    print(json.dumps({'bytes': len(markup.encode()), 'svg_original_matches': dict(SVG_MATCHES), 'native_seed_sha256': seed_hash, 'templates': len(templates)}))


if __name__ == '__main__':
    main()
