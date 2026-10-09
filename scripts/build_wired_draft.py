#!/usr/bin/env python3
"""Refine native Stitch output using the dated, public WIRED UI evidence."""
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urljoin

from official_html_tree import Node, Tree

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / '.stitch-work/current-official'
ORIGIN = 'https://www.wired.com/'
REFERENCE = json.loads((WORK / 'wired-complete-browser-export.json').read_text())
STATES = json.loads((WORK / 'wired-states-browser-export.json').read_text())
CSS = json.loads((WORK / 'wired-complete-css-browser-export.json').read_text())
ORIGINAL_STYLES = json.loads((WORK / 'wired-original-styles-browser-export.json').read_text())
SERVER_STYLES = json.loads((WORK / 'wired-original-server-styles.json').read_text())
ASSETS = json.loads((WORK / 'wired-asset-provenance.json').read_text())['assets']
ASSETS += json.loads((WORK / 'wired-font-repair-provenance.json').read_text())['assets']
ASSETS += json.loads((WORK / 'wired-additional-asset-provenance.json').read_text())['assets']
FONTS = {a['source_url']: a['path'] for a in ASSETS if a['kind'] == 'font' and a['retained']}
SVG = re.compile(r'<svg\b[\s\S]*?</svg>', re.I)
FONT_DECLARATIONS = {}
FONT_TOKENS = set()
for style in ORIGINAL_STYLES['nodes']:
    FONT_TOKENS.update(re.findall(r'--font-[\w-]+(?=\s*:)', ''.join(style['cssParts'])))
for source_style in SERVER_STYLES['styles']:
    for selector, declarations in re.findall(r'(\.[\w-]+)\{([^{}]*)\}', ''.join(source_style['cssParts'])):
        font = re.search(r'(?:^|;)font:([^;]+);', declarations)
        if font:
            FONT_DECLARATIONS.setdefault(selector, set()).add(font.group(1))


def restore_fonts(text):
    def repair(match):
        selector, declarations = match.groups()
        fonts = FONT_DECLARATIONS.get(selector, set())
        if 'font-family: ;' not in declarations:
            return match.group()
        if len(fonts) == 1:
            font = next(iter(fonts))
        else:
            # Runtime-only variants are absent from server-generated classes.
            # Use the paired public typography token only when the observed
            # variant references it and the original brand CSS declares it.
            variant = re.search(r'font-feature-settings:\s*var\(--variant-([\w-]+)', declarations)
            token = '--font-' + variant.group(1) if variant else None
            if token not in FONT_TOKENS:
                return match.group()
            font = 'var(' + token + ')'
        declarations = re.sub(r'(?:font-[\w-]+|line-height):\s*;', '', declarations)
        return selector + '{font:' + font + ';' + declarations + '}'
    return re.sub(r'(\.[\w-]+)\s*\{([^{}]*)\}', repair, text)


def css_text(text, base=ORIGIN):
    def substitute(match):
        value = next(v for v in match.groups() if v is not None).strip()
        if value.startswith(('data:', '#', 'blob:')):
            return match.group()
        original = urljoin(base, value)
        return 'url("' + FONTS.get(original, original) + '")'
    return re.sub(r'url\(\s*(?:"([^\"]*)"|\'([^\']*)\'|([^)]*))\s*\)', substitute, text)


def prepare(markup, body_children=False):
    if '[Truncated]' in markup:
        raise ValueError('Truncated public markup cannot be used.')
    vectors = []
    def hold_svg(match):
        vectors.append(match.group())
        return f'<study-vector index="{len(vectors)-1}"></study-vector>'
    tree = Tree(SVG.sub(hold_svg, markup)).root
    def clean(node):
        node.children = [c for c in node.children
                         if c.tag not in ('script', 'noscript', 'iframe', 'style')]
        for child in node.children:
            clean(child)
    clean(tree)
    if body_children:
        for frame in REFERENCE['iframes']:
            rect = frame['rect']
            if frame.get('title') != '3rd party ad content' or not rect['height']:
                continue
            parent = tree.find(lambda n: n.attrs.get('id') == frame.get('parentId'))
            if parent:
                # Retain the observed inline box; the original advertising
                # frame, its scripts, and its changing creative stay excluded.
                parent.children.append(Node('span', {
                    'aria-hidden': 'true', 'data-study-observed-ad-box': '',
                    'style': f"display:inline-block;vertical-align:bottom;width:{rect['width']}px;height:{rect['height']}px;max-width:100%",
                }.items()))
    for node in tree.walk():
        node.attrs = {k: v for k, v in node.attrs.items()
                      if not k.startswith('on') and k != 'value'
                      and not re.search(r'nonce|csrf|token|integrity', k, re.I)}
        for key in ('src', 'href', 'poster', 'action'):
            if node.attrs.get(key) and not node.attrs[key].startswith(('data:', '#', 'mailto:', 'tel:')):
                node.attrs[key] = urljoin(ORIGIN, node.attrs[key])
        if node.tag == 'img':
            observed = next((image for image in REFERENCE['images']
                             if image['src'] == node.attrs.get('src')), None)
            if observed and observed['naturalWidth']:
                # These originals were already decoded in the dated reference.
                # Without the provider observer, zero-size lazy images can
                # remain unloaded and collapse the source's editorial rows.
                node.attrs['loading'] = 'eager'
        if node.attrs.get('style'):
            node.attrs['style'] = css_text(node.attrs['style'])
    if body_children:
        tree = tree.find(lambda n: n.tag == 'body')
        output = ''.join(n.render() for n in tree.children)
    else:
        output = tree.render()
    return re.sub(r'<study-vector index="(\d+)"></study-vector>', lambda m: vectors[int(m.group(1))], output)


def element(tag, attrs=None, content=''):
    node = Node(tag, (attrs or {}).items())
    if content:
        node.children = [Node(text=content)]
    return node


def main():
    assert REFERENCE['url'] == ORIGIN and len(FONTS) == 22
    for asset in ASSETS:
        if not asset['retained']:
            continue
        data = (WORK / asset['path']).read_bytes()
        assert len(data) == asset['bytes'] and hashlib.sha256(data).hexdigest() == asset['sha256']
    for path in WORK.glob('wired-stitch-*-downloads.json'):
        for record in json.loads(path.read_text()):
            data = (WORK / record['path']).read_bytes()
            assert len(data) == record['bytes'] and hashlib.sha256(data).hexdigest() == record['sha256']
    native = WORK / 'wired-stitch-desktop-raw.html'
    generated = Tree(native.read_text()).root
    html = generated.find(lambda n: n.tag == 'html')
    head = html.find(lambda n: n.tag == 'head')
    body = html.find(lambda n: n.tag == 'body')
    html.attrs = dict(REFERENCE['htmlAttributes'])
    body.attrs = dict(REFERENCE['body']['attributes'])
    body.attrs['class'] = re.sub(r'\bpri_[\w-]+\s*', '', body.attrs.get('class', ''))
    assert len(ORIGINAL_STYLES['nodes']) == len(CSS['styles'])
    rules = []
    server_styled = next(s for s in SERVER_STYLES['styles'] if 'data-styled' in dict(s['attributes']))
    styled_text = ''.join(server_styled['cssParts'])
    assert '.gGwmsI{' in styled_text and 'font:var(--font-navigation-text-label)' in styled_text
    source_revision = next(dict(s['attributes'])['data-revision'] for s in SERVER_STYLES['styles'] if dict(s['attributes']).get('id') == 'brand-identity')
    assert source_revision == '2404674862461224740'
    for index, (raw, sheet) in enumerate(zip(ORIGINAL_STYLES['nodes'], CSS['styles'])):
        assert raw['href'] == sheet.get('href')
        text = ''.join(raw['cssParts'] if raw['textLength'] else sheet.get('cssParts', []))
        if index == 2:
            # Keep scoped original rules too: shared summary selectors have
            # distinct fonts in different editorial blocks.
            text = styled_text + '\n' + text
        # Restore the original font within its observed rule. Prepending a
        # second stylesheet would let later base rules override the same font.
        rules.append(css_text(restore_fonts(text), sheet.get('href') or ORIGIN))
    rules.append(css_text(restore_fonts('\n'.join(STATES['extraStyles']))))
    # The retained desktop DOM keeps this nested grid's intrinsic minimum
    # width on a narrow viewport. Constrain the study's mobile adaptation;
    # this is not evidence of an observed official mobile layout.
    rules.append('@media(max-width:767px){.subtopic-discovery-grid{grid-column:1/-1;min-width:0}}')
    head.children = [
        element('meta', {'charset': 'utf-8'}),
        element('meta', {'name': 'viewport', 'content': 'width=device-width,initial-scale=1'}),
        element('title', content='WIRED · Current official homepage study'),
        element('meta', {'name': 'description', 'content': 'Free unofficial dated study of the October 9, 2026 public WIRED homepage. Full visual and mobile acceptance remains pending.'}),
        element('meta', {'name': 'stitch-native-seed-sha256', 'content': hashlib.sha256(native.read_bytes()).hexdigest()}),
        element('style', content='\n'.join(rules)),
    ]
    public_body = prepare(''.join(REFERENCE['htmlParts']), body_children=True)
    templates = ''.join('<template id="study-wired-' + name + '">' + prepare(STATES[key]['html']) + '</template>'
                        for name, key in [('drawer', 'navigationDrawer'), ('drawer-more', 'navigationMoreExpanded'), ('menu-open', 'openedToggle'), ('account', 'accountDropdown')])
    ui = json.loads((WORK / 'wired-source-ui-reference.json').read_text())
    state = '<script type="application/json" id="study-wired-ui">' + json.dumps(ui).replace('<', '\\u003c') + '</script>'
    body.children = [Node(text=public_body + templates + state), element('script', content=(ROOT / 'scripts/wired-current-official.js').read_text())]
    output = '<!doctype html>' + html.render() + '\n'
    (WORK / 'wired.html').write_text(output)
    print(json.dumps({'draft': 'wired.html', 'original_fonts': len(FONTS), 'style_blocks': len(rules), 'retained_assets': len({a['path'] for a in ASSETS if a['retained']}), 'accepted': False}))


if __name__ == '__main__':
    main()
