#!/usr/bin/env python3
"""Refine the preserved native Stitch document using dated public evidence."""
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urljoin, urlsplit

from official_html_tree import Node, Tree

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / '.stitch-work/current-official'
ORIGIN = 'https://www.theverge.com/'
REFERENCE = json.loads((WORK / 'theverge-desktop-browser-export.json').read_text())
STATES = json.loads((WORK / 'theverge-states-browser-export.json').read_text())
DETAILS = json.loads((WORK / 'theverge-source-details.json').read_text())
ASSETS = json.loads((WORK / 'theverge-asset-provenance.json').read_text())['assets']
FONTS = {a['source_url']: a['path'] for a in ASSETS if a['kind'] == 'font' and a['retained']}
STYLES = {a['source_url']: a['path'] for a in ASSETS if a['kind'] == 'stylesheet' and a['retained']}
SVG = re.compile(r'<svg\b[\s\S]*?</svg>', re.I)


def css_text(text, base=ORIGIN):
    def substitute(match):
        value = next(v for v in match.groups() if v is not None).strip()
        if value.startswith(('data:', '#', 'blob:')):
            return match.group()
        original = urljoin(base, value)
        return 'url("' + FONTS.get(original, original) + '")'
    return re.sub(r'url\(\s*(?:"([^\"]*)"|\'([^\']*)\'|([^)]*))\s*\)', substitute, text)


def prepare(markup):
    if '[Truncated]' in markup:
        raise ValueError('Truncated public markup cannot be used.')
    vectors = []
    def hold_svg(match):
        vectors.append(match.group())
        return f'<study-vector index="{len(vectors)-1}"></study-vector>'
    tree = Tree(SVG.sub(hold_svg, markup)).root
    def clean(node):
        node.children = [child for child in node.children
                         if child.tag not in ('script', 'noscript', 'iframe', 'style')
                         and not (child.tag == 'form' and 'facebook.com/tr' in child.attrs.get('action', ''))]
        for child in node.children:
            clean(child)
    clean(tree)
    for frame in STATES['framePlacements']:
        # Preserve the observed river ad's inline box without executing its
        # advertising frame. The creative remains outside this study.
        rect = frame['rect']
        if frame.get('title') != '3rd party ad content' or rect['width'] != 300:
            continue
        parent_id = frame.get('parentId')
        parent = tree.find(lambda n: n.attrs.get('id') == parent_id)
        if parent:
            parent.children.append(Node('span', {
                'aria-hidden': 'true',
                'data-study-observed-ad-box': '',
                'style': f"display:inline-block;width:{rect['width']}px;height:{rect['height']}px;max-width:100%",
            }.items()))
    for node in tree.walk():
        node.attrs = {k: v for k, v in node.attrs.items()
                      if not k.startswith('on') and k != 'value'
                      and not re.search(r'nonce|csrf|token|integrity', k, re.I)}
        for key in ('src', 'href', 'poster', 'action'):
            if node.attrs.get(key) and not node.attrs[key].startswith(('data:', '#', 'mailto:', 'tel:')):
                node.attrs[key] = urljoin(ORIGIN, node.attrs[key])
        if node.attrs.get('style'):
            node.attrs['style'] = css_text(node.attrs['style'])
        if node.tag == 'form' and node.attrs.get('aria-label') == 'Search Form':
            assert urlsplit(DETAILS['search']['url']).path == '/search'
            node.attrs.update(action='https://www.theverge.com/search', method='get')
            for field in node.walk():
                if field.tag == 'input':
                    field.attrs['name'] = 'q'
        if node.tag == 'input':
            state = next((s for s in STATES['navigationInputs'] if s['id'] == node.attrs.get('id')), None)
            if state and state['checked']:
                node.attrs['checked'] = None
    output = tree.render()
    return re.sub(r'<study-vector index="(\d+)"></study-vector>', lambda m: vectors[int(m.group(1))], output)


def element(tag, attrs=None, content=''):
    node = Node(tag, (attrs or {}).items())
    if content:
        node.children = [Node(text=content)]
    return node


def main():
    assert REFERENCE['url'] == ORIGIN and len(FONTS) == 19
    for asset in ASSETS:
        if not asset['retained']:
            continue
        content = (WORK / asset['path']).read_bytes()
        assert len(content) == asset['bytes'] and hashlib.sha256(content).hexdigest() == asset['sha256']
    for path in sorted(WORK.glob('theverge-stitch-*-downloads.json')):
        for record in json.loads(path.read_text()):
            content = (WORK / record['path']).read_bytes()
            assert len(content) == record['bytes'] and hashlib.sha256(content).hexdigest() == record['sha256']
    native = WORK / 'theverge-stitch-desktop-raw.html'
    generated = Tree(native.read_text()).root
    html = generated.find(lambda n: n.tag == 'html')
    head = html.find(lambda n: n.tag == 'head')
    body = html.find(lambda n: n.tag == 'body')
    html.attrs = {'lang': 'en-US'}
    body.attrs = dict(REFERENCE['body']['attributes'])
    rules, seen, original_sheets = [], set(), 0
    for state in (REFERENCE, STATES['navigationDrawer'], STATES['followingPanel']):
        for sheet in state['styles']:
            href = sheet.get('href')
            key = href or '\n'.join(sheet.get('rules', []))
            if key in seen:
                continue
            seen.add(key)
            # CSSOM serialization can lose variable-based font shorthands.
            # Preserve the original public stylesheet bytes in cascade order.
            if href in STYLES:
                content = (WORK / STYLES[href]).read_text()
                original_sheets += 1
            else:
                content = '\n'.join(sheet.get('rules', []))
            rules.append(css_text(content, href or ORIGIN))
    head.children = [
        element('meta', {'charset': 'utf-8'}),
        element('meta', {'name': 'viewport', 'content': 'width=device-width,initial-scale=1'}),
        element('title', content='The Verge · Current official homepage study'),
        element('meta', {'name': 'description', 'content': 'Free unofficial dated study of the October9,2026 public homepage. Full visual and mobile acceptance remains pending.'}),
        element('meta', {'name': 'stitch-native-seed-sha256', 'content': hashlib.sha256(native.read_bytes()).hexdigest()}),
        element('style', content='\n'.join(rules) + '\n[data-study-mobile-hidden],[data-study-hidden]{display:none!important}'),
    ]
    markup = prepare(''.join(REFERENCE['htmlParts']))
    templates = ''.join('<template id="study-' + name + '">' + prepare(state['html']) + '</template>'
                        for name, state in (('drawer', STATES['navigationDrawer']), ('drawer-tech', STATES['navigationTechExpanded']), ('following', STATES['followingPanel'])))
    tab_data = '<script type="application/json" id="study-source-tabs">' + json.dumps(DETAILS['tabs']).replace('<', '\\u003c') + '</script>'
    body.children = [Node(text=markup + templates + tab_data), element('script', content=(ROOT / 'scripts/theverge-current-official.js').read_text())]
    (WORK / 'theverge.html').write_text('<!doctype html>' + html.render() + '\n')
    print(json.dumps({'draft': 'theverge.html', 'original_stylesheets': original_sheets, 'style_blocks': len(rules), 'original_font_files': len(FONTS), 'accepted': False}))


if __name__ == '__main__':
    main()
