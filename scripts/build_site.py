#!/usr/bin/env python3
"""Stage only public website files for static hosting, after build.py."""
import json
import re
import shutil
from html import escape, unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'dist'
OFFICIAL_DRAFTS = ('spotify', 'linear', 'claude', 'notion', 'figma', 'framer', 'vercel', 'airbnb', 'airtable', 'stripe', 'starbucks', 'shopify', 'slack', 'supabase', 'resend', 'ollama', 'raycast', 'cal', 'cursor', 'apple', 'clay', 'clickhouse', 'cohere', 'composio', 'expo', 'mintlify', 'elevenlabs', 'miro', 'opencode.ai', 'voltagent', 'posthog', 'warp', 'webflow', 'wise', 'zapier', 'tesla', 'mistral.ai', 'replicate', 'together.ai', 'sanity', 'sentry', 'ibm', 'mongodb')
DRAFT_SOURCE = ROOT / '.stitch-work' / 'current-official'


class AssetReferences(HTMLParser):
    def __init__(self):
        super().__init__()
        self.values = []

    def handle_starttag(self, _tag, attributes):
        for name, value in attributes:
            if name in ('src', 'href', 'poster') and value:
                self.values.append(value)


def stage_official_drafts():
    destination = OUTPUT / 'official-drafts'
    destination.mkdir()
    source_root = DRAFT_SOURCE.resolve()
    progress = json.loads((DRAFT_SOURCE / 'progress.json').read_text())
    for name in OFFICIAL_DRAFTS:
        source = DRAFT_SOURCE / f'{name}.html'
        html = source.read_text()
        references = AssetReferences()
        references.feed(html)
        references.values.extend(re.findall(r'url\(([^)]+)\)', html))
        for value in references.values:
            value = unescape(value).strip(' \t\n\r\'"')
            if unquote(value).startswith('#'):
                continue
            if value.startswith(('https:', 'http:', 'data:', 'mailto:', 'tel:', '#', '/')):
                continue
            relative = Path(urlsplit(value).path)
            asset = (DRAFT_SOURCE / relative).resolve()
            asset.relative_to(source_root)
            if not asset.is_file():
                raise FileNotFoundError(f'Missing {name} draft asset: {relative}')
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(asset, target)
        if name in ('slack', 'supabase', 'voltagent', 'posthog', 'warp', 'webflow', 'wise', 'zapier', 'tesla', 'mistral.ai', 'replicate', 'together.ai', 'sentry'):
            # Runtime tabs select additional official media that do not appear
            # in static src attributes; keep those assets with each draft.
            asset_dir = f'{name}-assets'
            shutil.copytree(DRAFT_SOURCE / asset_dir,
                            destination / asset_dir, dirs_exist_ok=True)
        if name == 'sanity':
            # Large public imagery and video remain on Sanity's own CDN.
            for asset in (DRAFT_SOURCE / 'sanity-assets').rglob('*'):
                if asset.is_file() and asset.suffix in {
                    '.css', '.woff', '.woff2', '.ttf', '.svg', '.webp'
                }:
                    target = destination / asset.relative_to(DRAFT_SOURCE)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(asset, target)
        record = progress['linear.app' if name == 'linear' else name]
        observed = escape((record.get('observed_at') or record.get('reference_observed_at') or '')[:10] or '日期未記錄')
        note = record.get('review_note')
        badge = ('<div class="official-draft-badge" role="note">'
                 '<strong>官網重製草稿 · 尚未視覺驗收</strong>'
                 f'<span>參考資料：{observed}；非品牌官方網站。</span>'
                 + (f'<span>{escape(note)}</span>' if note else '')
                 + '<a href="../official-progress.html">查看 74 站進度 ↗</a></div>')
        style = '''<meta name="robots" content="noindex"><style>
.official-draft-badge{position:fixed;right:16px;bottom:16px;z-index:2147483647;max-width:min(340px,calc(100vw - 32px));padding:12px 16px;background:#fffdf7;color:#20211f;border:1px solid #d5d3ca;border-radius:9px;box-shadow:0 8px 34px #0004;font:12px/1.5 system-ui,sans-serif;display:grid;gap:3px}
.official-draft-badge strong{font-size:13px}.official-draft-badge span{color:#555}.official-draft-badge a{color:#a53d22;text-decoration:underline}
</style>'''
        html = html.replace('</head>', style + '</head>', 1)
        match = re.search(r'<body\b[^>]*>', html, re.I)
        if match is None:
            raise ValueError(f'Draft has no body: {source}')
        html = html[:match.end()] + badge + html[match.end():]
        (destination / f'{name}.html').write_text(html)


def stage_official_progress():
    """Make the 74-brand status visible without implying a saved page is current."""
    catalog = json.loads((ROOT / 'assets/catalog.json').read_text())['designs']
    progress = json.loads((DRAFT_SOURCE / 'progress.json').read_text())
    assert len(catalog) == len(progress) == 74
    labels = {
        'in_visual_review': ('草稿待視覺驗收', 'draft'),
        'draft_unverified': ('草稿待視覺驗收', 'draft'),
        'local_draft_pending_stitch': ('本機草稿待 Stitch 與視覺驗收', 'local'),
        'source_snapshot_only': ('已保存網頁資料，尚未重製', 'snapshot'),
        'reference_pending': ('尚無可用參考畫面', 'pending'),
    }
    rows = []
    counts = {'draft': 0, 'local': 0, 'snapshot': 0, 'pending': 0}
    for item in catalog:
        slug = item['slug']
        record = progress[slug]
        label, kind = labels[record['status']]
        counts[kind] += 1
        draft_name = 'linear' if slug == 'linear.app' else slug
        href = (f'official-drafts/{draft_name}.html' if kind == 'draft'
                else record['reference_url'] if kind == 'local'
                else f'index.html#/design/{slug}')
        date = (record.get('observed_at') or record.get('reference_observed_at') or '')[:10] or '—'
        note = record.get('review_note')
        rows.append('<tr><th scope="row"><a href="' + escape(href, quote=True) + '">' +
                    escape(item['name']) + ' ↗</a></th><td class="' + kind + '">' +
                    label + (f'<br><small>{escape(note)}</small>' if note else '') +
                    '</td><td>' + escape(date) + '</td></tr>')
    assert sum(counts.values()) == 74 and counts['draft'] == len(OFFICIAL_DRAFTS), counts
    page = '''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>74 個網站重製進度 · Awesome AI Web Design</title><style>
body{font:16px/1.6 system-ui,sans-serif;background:#f8f7f3;color:#20211f;margin:0}main{max-width:1040px;margin:auto;padding:48px 24px 96px}a{color:inherit}a:hover{color:#bf421e}header a{font-weight:700;text-decoration:none}h1{font-size:clamp(32px,5vw,54px);line-height:1.1;margin:32px 0 16px}p{max-width:760px}table{border-collapse:collapse;width:100%;background:white;margin-top:36px}th,td{text-align:left;border-bottom:1px solid #e2e0da;padding:13px 18px}thead th{background:#eeeae1;font-size:13px;letter-spacing:.04em}tbody th{font-weight:600}tbody th a{text-decoration:none}.draft{color:#a34317}.local{color:#805ba5}.snapshot{color:#4d6381}.pending{color:#777}small{color:#666}@media(max-width:600px){main{padding:28px 14px}th,td{padding:10px 8px;font-size:13px}}
</style></head><body><main><header><a href="index.html#official-drafts">← 返回設計集</a></header><h1>74 個網站重製進度</h1><p>目前有 ''' + str(counts['draft']) + ''' 份公開的官網重製草稿、''' + str(counts['local']) + ''' 份尚未公開的本機草稿，0 份完成逐頁視覺驗收；其餘 ''' + str(counts['snapshot']) + ''' 個已保存特定日期的網頁資料，''' + str(counts['pending']) + ''' 個尚無可用參考畫面。原本的 Stitch 範例不列為官網重製完成品。</p><p><small>「參考日期」是資料擷取日期，不代表今天的官網畫面；所有草稿仍需和品牌現行網站逐頁、逐裝置比較。</small></p><table><thead><tr><th scope="col">品牌</th><th scope="col">狀態</th><th scope="col">參考日期</th></tr></thead><tbody>''' + ''.join(rows) + '''</tbody></table></main></body></html>'''
    (OUTPUT / 'official-progress.html').write_text(page)


def main():
    if OUTPUT.is_symlink():
        raise RuntimeError('dist must be a regular build directory')
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir()
    for name in ('index.html', 'README.md', 'ATTRIBUTION.md', 'LICENSE', 'CONTRIBUTING.md'):
        shutil.copy2(ROOT / name, OUTPUT / name)
    for name in ('assets', 'design-md', 'prompts'):
        shutil.copytree(ROOT / name, OUTPUT / name, ignore=shutil.ignore_patterns('all-designs.zip') if name == 'assets' else None)
    # Keep the complete, unchanged exports in GitHub and the downloadable ZIP.
    # Pin hosted images to their source commit so later pushes cannot change them.
    image_base = json.loads((ROOT / 'data/hosting-assets.json').read_text())['image_base_url'].rstrip('/') + '/'
    catalog_path = OUTPUT / 'assets/catalog.json'
    catalog = json.loads(catalog_path.read_text())
    for entry in catalog['designs']:
        preview = entry['preview']
        if preview['status'] != 'generated':
            continue
        for key in ('image', 'thumbnail'):
            relative = preview[key]
            preview[key] = image_base + relative
            (OUTPUT / relative).unlink(missing_ok=True)
    catalog_path.write_text(json.dumps(catalog, ensure_ascii=False, separators=(',', ':')) + '\n')
    stage_official_drafts()
    stage_official_progress()
    print(f'Staged public website in {OUTPUT}')


if __name__ == '__main__':
    main()
