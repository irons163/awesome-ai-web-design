#!/usr/bin/env python3
"""Separate Dell refinement; native Stitch exports and brand bytes stay intact."""
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urljoin

from official_html_tree import Tree

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / '.stitch-work/current-official'
ORIGIN = 'https://www.dell.com/zh-tw'
SVG = re.compile(r'<svg\b[\s\S]*?</svg>', re.I)
PROVENANCE = json.loads((WORK / 'dell-1996-asset-provenance.json').read_text())
ASSETS = {a['source_url']: a for a in PROVENANCE['assets']}
MEDIA = json.loads((WORK / 'dell-1996-media-provenance.json').read_text())
ASSETS.update({a['source_url']: a for a in MEDIA['assets']})
REFERENCES = {m: json.loads((WORK / f'dell-1996-{m}-browser-export.json').read_text()) for m in ('desktop', 'mobile')}
INTERACTIONS = json.loads((WORK / 'dell-1996-interactions-browser-export.json').read_text())
VIDEO_META = {v['id']: v for v in INTERACTIONS['media']['videos']}


def local_url(value):
    if value.startswith(('data:', '#')):
        return value
    url = urljoin(ORIGIN, value)
    return ASSETS[url]['path'] if url in ASSETS else url


def css_text(text, base=ORIGIN):
    def replace(match):
        raw = match.group(1).strip().strip('"\'')
        if raw.startswith(('data:', '#')):
            return match.group()
        url = urljoin(base, raw)
        return 'url("' + (ASSETS[url]['path'] if url in ASSETS else url) + '")'
    return re.sub(r'url\(([^)]+)\)', replace, text)


def prepare(markup, loaded_images=None):
    if '[Truncated]' in markup:
        raise ValueError('A truncated browser capture is not a usable reference.')
    originals = []
    def save_svg(match):
        originals.append(match.group())
        return f'<study-svg index="{len(originals)-1}"></study-svg>'
    tree = Tree(SVG.sub(save_svg, markup)).root
    for node in tree.walk():
        node.attrs = {k: v for k, v in node.attrs.items() if not k.startswith('on') and k not in ('value', 'data-metrics')}
        if node.tag == 'video':
            node.attrs.pop('src', None)  # A source-tab blob cannot work in a separate document.
            video = VIDEO_META.get(node.attrs.get('id'), {})
            if video.get('poster'):
                node.attrs['poster'] = local_url(video['poster'])
            if video.get('loop') and MEDIA['local_background_manifest']:
                node.attrs.update({'data-study-background': MEDIA['local_background_manifest'],
                                   'data-study-paused-time': str(INTERACTIONS['media']['background_paused_reference']['current_time']),
                                   'muted': None, 'loop': None, 'playsinline': None, 'preload': 'auto'})
        if node.tag == 'img' and loaded_images and node.attrs.get('alt') in loaded_images:
            source = node.attrs.get('src') or ''
            if source in ('', 'null') or source.startswith('data:image/svg+xml'):
                # The recorded inactive slides use empty SVG fallbacks. Keep
                # their original responsive <source> candidates and give the
                # fallback the actual, separately observed product image.
                node.attrs['src'] = loaded_images[node.attrs['alt']]
        if node.attrs.get('src') in ('', 'null'):
            # Empty provider thumbnail/lazy placeholders are not files.
            node.attrs.pop('src', None)
        for key in ('src', 'data-src'):
            if node.attrs.get(key) and node.attrs[key] != 'null':
                node.attrs[key] = local_url(node.attrs[key])
        # Dell's single srcset URLs contain commas in size/op_usm query
        # values. Do not split such URLs as if they were multiple candidates.
        for key in ('srcset', 'data-srcset'):
            if node.attrs.get(key) and not re.search(r'\s', node.attrs[key]):
                node.attrs[key] = local_url(node.attrs[key])
        if node.attrs.get('href') and not node.attrs['href'].startswith('#'):
            node.attrs['href'] = urljoin(ORIGIN, node.attrs['href'])
        if node.attrs.get('style'):
            style = css_text(node.attrs['style'])
            # Simple image URLs need no CSS quotes inside an HTML attribute.
            node.attrs['style'] = re.sub(r'url\("([^"\s()]+)"\)', r'url(\1)', style)
    rendered = tree.render()
    return re.sub(r'<study-svg index="(\d+)"></study-svg>', lambda m: originals[int(m.group(1))], rendered)


def main():
    for asset in ASSETS.values():
        assert hashlib.sha256((WORK / asset['path']).read_bytes()).hexdigest() == asset['sha256']
    native = []
    for name in ('desktop', 'mobile-request', 'mobile'):
        for suffix in ('html', 'png'):
            path = WORK / f'dell-1996-stitch-{name}-raw.{suffix}'
            native.append({'path': path.name, 'bytes': path.stat().st_size, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
    (WORK / 'dell-1996-stitch-downloads.json').write_text(json.dumps(native, indent=2) + '\n')
    loaded = {i['alt']: i['src'] for i in INTERACTIONS['products_loaded_desktop']['images']
              if i['loaded'] and i['src'].startswith('https://')}
    templates = []
    for mode, reference in REFERENCES.items():
        markup = '<div class="hpg_main">' + ''.join(reference['root_parts']) + '</div>'
        templates.append(f'<template data-study-layout="{mode}">' + prepare(markup, loaded) + '</template>')
    for key in ('mobile_menu', 'mobile_products_menu', 'mobile_footer_account'):
        templates.append(f'<template data-study-state="{key}">' + prepare(INTERACTIONS[key]['root']) + '</template>')
    styles = []
    for entry in REFERENCES['desktop']['stylesheet_order']:
        if entry.get('href') in ASSETS:
            styles.append(css_text((WORK / ASSETS[entry['href']]['path']).read_text(), entry['href']))
        elif 'text' in entry:
            styles.append(css_text(entry['text']))
        else:
            raise ValueError('Missing observed public stylesheet: ' + str(entry))
    styles.append((ROOT / 'scripts/dell-current-official.css').read_text())
    seed = next(n['sha256'] for n in native if n['path'] == 'dell-1996-stitch-desktop-raw.html')
    markup = ('<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
              '<title>Dell 台灣 · 官網研究草稿</title><meta name="description" content="免費的 Dell 台灣官網研究草稿；依 2026-10-08 公開版本重製，尚未視覺驗收。">'
              '<meta name="stitch-native-seed-sha256" content="' + seed + '"><style>' + '\n'.join(styles) + '</style></head><body>'
              + ''.join(REFERENCES['desktop']['sprite']) + '<div id="study-mount"></div>' + ''.join(templates)
              + '<script src="runwayml-assets/hls.light.min.js"></script>'
              + '<script>' + (ROOT / 'scripts/dell-current-official.js').read_text() + '</script></body></html>')
    (WORK / 'dell-1996.html').write_text(markup)
    print(json.dumps({'bytes': len(markup.encode()), 'native_exports': len(native), 'original_resource_records': len(PROVENANCE['assets'])}))


if __name__ == '__main__':
    main()
