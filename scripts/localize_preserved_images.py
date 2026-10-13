"""Use checksum-verified image bytes without changing the rest of a saved study."""
import hashlib
import re
from html import escape
from html.parser import HTMLParser
from urllib.parse import urljoin


def localize_images(markup, origin, assets, observed_images, work):
    retained = {a['source_url'].strip(): a for a in assets
                if a.get('retained') and a.get('kind') == 'image'}
    observed = {image['src'].strip(): image.get('currentSrc', '').strip()
                for image in observed_images if image.get('src')}
    verified, edits, changes = set(), [], []
    offsets = [0]
    for line in markup.splitlines(keepends=True):
        offsets.append(offsets[-1] + len(line))

    class Images(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=False)
            self.pictures = []

        def handle_starttag(self, tag, attrs):
            raw = self.get_starttag_text()
            line, column = self.getpos()
            start = offsets[line - 1] + column
            values = dict(attrs)
            if tag == 'picture':
                self.pictures.append({'localized': False, 'sources': []})
            elif tag == 'source' and values.get('srcset') and self.pictures:
                # A retained fallback must not be overridden by an unretained
                # responsive URL. Video/audio source elements remain intact.
                self.pictures[-1]['sources'].append((start, start + len(raw), ''))
            elif tag == 'img':
                source = urljoin(origin, (values.get('src') or '').strip())
                candidates = [observed.get(source), source]
                candidates += [urljoin(origin, match.group(1)) for match in
                               re.finditer(r'(\S+)\s+\d+(?:\.\d+)?[wx](?:\s*,\s*|$)', values.get('srcset') or '')]
                selected = next((retained[url] for url in candidates if url in retained), None)
                if not selected:
                    return
                path = selected['path']
                if path not in verified:
                    data = (work / path).read_bytes()
                    if len(data) != selected['bytes'] or hashlib.sha256(data).hexdigest() != selected['sha256']:
                        raise ValueError('Preserved image differs: ' + path)
                    verified.add(path)
                values['src'] = path
                values['loading'] = 'eager'
                for name in ('srcset', 'data-src', 'data-srcset'):
                    values.pop(name, None)
                replacement = '<img' + ''.join(' ' + key + ('' if value is None else
                              '="' + escape(value, quote=True) + '"') for key, value in values.items()) + '>'
                edits.append((start, start + len(raw), replacement))
                changes.append({'source_url': selected['source_url'], 'path': path, 'sha256': selected['sha256']})
                if self.pictures:
                    self.pictures[-1]['localized'] = True

        def handle_startendtag(self, tag, attrs):
            self.handle_starttag(tag, attrs)

        def handle_endtag(self, tag):
            if tag == 'picture' and self.pictures:
                picture = self.pictures.pop()
                if picture['localized']:
                    edits.extend(picture['sources'])

    Images().feed(markup)
    for start, end, replacement in sorted(edits, reverse=True):
        markup = markup[:start] + replacement + markup[end:]
    return markup, changes
