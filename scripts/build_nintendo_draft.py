#!/usr/bin/env python3
"""Refine the genuine Nintendo Stitch document with dated public evidence."""
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urljoin

from official_html_tree import Node, Tree

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / '.stitch-work/current-official'
ORIGIN = 'https://www.nintendo.com/en-ca/'
REFERENCE = json.loads((WORK / 'nintendo-2001-desktop-browser-export.json').read_text())
STATES = json.loads((WORK / 'nintendo-2001-states-browser-export.json').read_text())
SEARCH = json.loads((WORK / 'nintendo-2001-search-browser-export.json').read_text())
ASSETS = json.loads((WORK / 'nintendo-2001-asset-provenance.json').read_text())['assets']
FONT_ASSETS = {a['source_url']: a['path'] for a in ASSETS if a['path'].endswith(('.woff2', '.woff', '.ttf'))}
SVG = re.compile(r'<svg\b[\s\S]*?</svg>', re.I)


def css_text(text, base=ORIGIN):
    def replace(match):
        value = match.group(1).strip().strip('\"\'')
        if value.startswith(('data:', '#')):
            return match.group()
        original = urljoin(base, value)
        return 'url("' + FONT_ASSETS.get(original, original) + '")'
    return re.sub(r'url\(([^)]+)\)', replace, text)


def prepare(markup, nav_state=None):
    if '[Truncated]' in markup:
        raise ValueError('Truncated public DOM is not a usable reference.')
    vectors = []
    def hold_svg(match):
        vectors.append(match.group())
        return f'<study-vector index="{len(vectors)-1}"></study-vector>'
    tree = Tree(SVG.sub(hold_svg, markup)).root
    for node in tree.walk():
        node.attrs = {key: value for key, value in node.attrs.items()
                      if not key.startswith('on') and key != 'value'
                      and (not key.startswith('data-') or key in ('data-testid', 'data-study-state', 'data-icon-wrap', 'data-image-frame'))}
        if node.tag in ('script', 'iframe', 'noscript'):
            raise ValueError('Source runtime must not be copied into a study.')
        if node.attrs.get('src') in ('', 'null'):
            node.attrs.pop('src', None)
        if node.tag == 'nav' and nav_state and nav_state.startswith('desktop_'):
            node.attrs['data-testid'] = 'desktop-nav'
        for key in ('src', 'href', 'poster', 'action'):
            if node.attrs.get(key) and not node.attrs[key].startswith(('data:', '#', 'mailto:', 'tel:')):
                node.attrs[key] = urljoin(ORIGIN, node.attrs[key])
        # Search opens the observed public endpoint; no provider SDK is copied.
        if node.tag == 'form':
            node.attrs.update({'action': 'https://www.nintendo.com/search', 'method': 'get'})
            for field in node.walk():
                if field.tag == 'input' and field.attrs.get('type') == 'text':
                    field.attrs['name'] = 'q'
        if node.attrs.get('style'):
            node.attrs['style'] = re.sub(r'url\("([^"\s()]+)"\)', r'url(\1)', css_text(node.attrs['style']))
        # These public styling hooks and boolean states were omitted by the
        # capture serializer; their values were checked in the live DOM.
        if '_8dTgA' in node.attrs.get('class', '').split():
            node.attrs['data-image-frame'] = 'true'
        if node.attrs.get('id') in ('explore-tab', 'shop-tab', 'support-tab'):
            wrapper = next((n for n in node.children if n.tag == 'div'), None)
            if wrapper:
                wrapper.attrs['data-icon-wrap'] = 'true'
            selected = nav_state == 'desktop_' + node.attrs['id'].replace('-tab', '')
            node.attrs['aria-expanded'] = str(selected).lower()
            node.attrs['aria-selected'] = str(selected).lower()
        if node.attrs.get('id') in ('explore-panel', 'shop-panel', 'support-panel'):
            selected = nav_state == 'desktop_' + node.attrs['id'].replace('-panel', '')
            if selected:
                for key in ('hidden', 'inert', 'aria-hidden'):
                    node.attrs.pop(key, None)
            else:
                node.attrs.update({'hidden': None, 'inert': None, 'aria-hidden': 'true'})
    text = tree.render()
    return re.sub(r'<study-vector index="(\d+)"></study-vector>', lambda m: vectors[int(m.group(1))], text)


def element(tag, attrs=None, content=''):
    node = Node(tag, (attrs or {}).items())
    if content:
        node.children = [Node(text=content)]
    return node


def main():
    assert REFERENCE['reference_url'] == ORIGIN
    for asset in ASSETS:
        data = (WORK / asset['path']).read_bytes()
        assert len(data) == asset['bytes'] and hashlib.sha256(data).hexdigest() == asset['sha256']
    native = json.loads((WORK / 'nintendo-2001-stitch-downloads.json').read_text())
    for record in native:
        data = (WORK / record['path']).read_bytes()
        assert len(data) == record['bytes'] and hashlib.sha256(data).hexdigest() == record['sha256']
    raw = WORK / 'nintendo-2001-stitch-desktop-raw.html'
    # Edit the generated document, preserving the native export separately.
    generated = Tree(raw.read_text()).root
    html = generated.find(lambda n: n.tag == 'html')
    head = html.find(lambda n: n.tag == 'head')
    body = html.find(lambda n: n.tag == 'body')
    html.attrs = {'lang': 'en-CA'}
    body.attrs = {}
    styles = []
    seen = set()
    for sheet in REFERENCE['stylesheet_order']:
        if sheet.get('href'):
            asset = next(a for a in ASSETS if a['source_url'] == sheet['href'])
            styles.append(css_text((WORK / asset['path']).read_text(), sheet['href']))
        elif sheet['rule_count'] < 500:
            for batch in sheet['rules']:
                for rule in batch:
                    if rule not in seen:
                        seen.add(rule)
                        styles.append(css_text(rule))
    for state in [*STATES['menus'].values(), SEARCH]:
        for sheet in state['stylesheet_order']:
            for batch in sheet['rules']:
                for rule in batch:
                    if rule not in seen:
                        seen.add(rule)
                        styles.append(css_text(rule))
    for hero in STATES['hero']:
        for rule in hero['css']:
            if rule not in seen:
                seen.add(rule)
                styles.append(css_text(rule))
    styles.append((ROOT / 'scripts/nintendo-current-official.css').read_text())
    head.children = [
        element('meta', {'charset': 'utf-8'}),
        element('meta', {'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}),
        element('title', content='Nintendo Canada · Current official homepage study'),
        element('meta', {'name': 'description', 'content': 'Free unofficial study of the October 8, 2026 Nintendo Canada homepage. Visual acceptance is pending.'}),
        element('meta', {'name': 'stitch-native-seed-sha256', 'content': hashlib.sha256(raw.read_bytes()).hexdigest()}),
        element('style', content='\n'.join(styles)),
    ]
    markup = prepare(''.join(REFERENCE['root_parts']), 'closed')
    source_tree = Tree(markup).root
    desktop = source_tree.find(lambda n: n.tag == 'nav' and n.attrs.get('data-testid') == 'desktop-nav')
    # Templates contain only the observed affected component, not whole pages.
    templates = ['<template data-study-nav="closed">' + desktop.render() + '</template>']
    for key, state in {**STATES['menus'], 'desktop_search': SEARCH}.items():
        templates.append('<template data-study-nav="' + key + '">' + prepare(state['nav_parts'][0], key) + '</template>')
    for index, hero in enumerate(STATES['hero']):
        templates.append(f'<template data-study-hero="{index}">' + prepare(hero['markup']) + '</template>')
    body.children = [Node(text=markup + ''.join(templates)),
                     element('script', content=(ROOT / 'scripts/nintendo-current-official.js').read_text())]
    # Remove the native doctype/comment nodes and serialize its edited document.
    output = '<!doctype html>' + html.render() + '\n'
    (WORK / 'nintendo-2001.html').write_text(output)
    notes = ['# Nintendo Stitch generation outputs', '',
             'Original tool text and suggestions are retained below. Native fidelity claims are not review results. The first mobile request returned DESKTOP; the correction returned MOBILE. Official live mobile and published visual acceptance remain pending.', '']
    for mode in ('desktop', 'mobile', 'mobile-correction'):
        result = json.loads((WORK / f'nintendo-2001-stitch-{mode}-response.json').read_text())
        result = result.get('structuredContent') or json.loads(next(c['text'] for c in result['content'] if c['type'] == 'text'))
        notes.extend(['## ' + mode, ''])
        for component in result.get('outputComponents', []):
            if 'text' in component:
                notes.extend([component['text'], ''])
            if 'suggestion' in component:
                notes.extend(['Suggestion: ' + component['suggestion'], ''])
    (WORK / 'nintendo-2001-generation-notes.md').write_text('\n'.join(notes))
    print(json.dumps({'draft_bytes': len(output.encode()), 'original_asset_records': len(ASSETS), 'native_exports': len(native), 'accepted': False}))


if __name__ == '__main__':
    main()
