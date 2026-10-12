"""Exact public dependency closure and conservative current-preview labels."""
from pathlib import Path, PurePosixPath
from html import escape, unescape
import hashlib
import json
import re
import shutil
from urllib.parse import unquote


def read_json(path):
    return json.loads(path.read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_file(work, relative):
    if not relative or Path(relative).is_absolute() or '\\' in relative or '..' in relative.split('/'):
        raise ValueError('Unsafe publication path: ' + str(relative))
    file = work / relative
    file.resolve().relative_to(work.resolve())
    if not file.is_file():
        raise FileNotFoundError('Missing publication file: ' + relative)
    return file


def is_asset(relative, brand):
    return bool(re.match(r'[a-z0-9.-]+-(?:assets|fonts|browser-images)/', relative) or re.fullmatch(r'[a-z0-9.-]+\.(?:svg|png|webp|avif|woff2?|ttf|css|js)', relative))


def references(text, brand, base=''):
    templates=[]
    config=re.search(r'(?:const|let|var)\s+CONFIG\s*=\s*',text)
    if config:
        value, _=json.JSONDecoder().raw_decode(text[config.end():])
        def collect(value):
            if isinstance(value,str) and '<' in value:
                templates.append(value)
            elif isinstance(value,dict):
                for child in value.values(): collect(child)
            elif isinstance(value,list):
                for child in value: collect(child)
        collect(value)
    text='\n'.join([text]+templates)
    normalized = re.sub(r'\\u002f', '/', text, flags=re.I)
    normalized = re.sub(r'\\u0026', '&', normalized, flags=re.I).replace('\\/', '/')
    static_html = re.sub(r'(<script\b[^>]*>)[\s\S]*?</script\s*>', r'\1</script>', normalized, flags=re.I)
    values = [a or b for a, b in re.findall(r'''(?:^|\s)(?:src|href|poster|xlink:href)\s*=\s*(?:"([^"]*)"|'([^']*)')''', static_html, re.I | re.M)]
    values += [match[1] for match in re.findall(r'''url\(\s*(['"]?)(.*?)\1\s*\)''', normalized)]
    values += re.findall(r'''@import\s+['"]([^'"]+)['"]''', normalized)
    values += re.findall(r'(?<![a-zA-Z0-9._~:/-])' + re.escape(brand) + r'''-(?:[a-z0-9]+-)*assets/[^<>"'\\\r\n?#]*?\.[a-zA-Z0-9]{1,10}(?=[\s,)"'\\?#<}]|$)''', unescape(normalized))
    out = set()
    for value in values:
        value = re.sub(r'''\\(['"])''', r'\1', unescape(value)).strip().strip('\'"')
        # Search-result templates resolve these expressions in the browser.
        # Their placeholders are not literal local files to package.
        if '${' in value or re.fullmatch(r'\{[A-Z][A-Z0-9_]*\}(?:[?#].*)?', value):
            continue
        if not value or re.match(r'^(?:[a-z][a-z0-9+.-]*:|/|#)', value, re.I) or unquote(value).startswith('#'):
            continue
        relative = re.split('[?#]', value, maxsplit=1)[0]
        if not relative or relative.endswith('/'):
            continue
        joined = relative if re.match(r'[a-z0-9.-]+-(?:assets|fonts|browser-images)/', relative) else str(PurePosixPath(base) / relative)
        # CSS may legitimately use ../ inside its own asset directory.
        parts = []
        for part in joined.split('/'):
            if part == '..' and parts:
                parts.pop()
            elif part != '.':
                parts.append(part)
        out.add('/'.join(parts))
    return sorted(out)


def preview_hash(record, brand, work):
    for value in [record.get('preview_sha256'), record.get('previewSha256'), record.get('local_draft', {}).get('sha256'),
                  record.get('preview', {}).get('sha256') if isinstance(record.get('preview'), dict) else None]:
        if isinstance(value, str):
            return value
    stores = [record.get('hashes'), record.get('files')]
    for name in [record.get('hashManifest'), record.get('hash_manifest')]:
        if isinstance(name, str):
            stores.append(read_json(source_file(work, name)))
    for store in stores:
        rows = store if isinstance(store, list) else [dict(path=key, **({'sha256': value} if isinstance(value, str) else value)) for key, value in (store or {}).items()]
        for row in rows:
            if PurePosixPath(row.get('path') or row.get('file') or '').name == brand + '.html':
                return row.get('sha256')
    return None


def result_for(work, brand, current):
    for file in sorted(work.glob(brand + '-*-result.json'), reverse=True):
        if re.search(r'-pre-|pre-current|pre-oct', file.name):
            continue
        record = read_json(file)
        if preview_hash(record, brand, work) == current:
            return file.name, record
    return None, {}


def manifest_for(work, brand, current):
    files = sorted(work.glob(brand + '-*-publication-manifest.json'), reverse=True)
    for file in files:
        manifest = read_json(file)
        if manifest.get('preview', {}).get('sha256') == current and manifest['preview']['path'] == brand + '.html':
            return dict(manifest, filename=file.name)
    if files:
        raise ValueError('Publication manifest does not bind current preview: ' + brand)
    return None


def study_texts(work, brand, record, manifest):
    supplied = (manifest or {}).get('study_text') or [value for value in record.get('current_supplements', {}).values() if isinstance(value, str) and value.endswith('.md')]
    inferred = [record.get(key) for key in ['designAnalysis', 'design_analysis', 'rewrittenPrompt', 'rewritten_prompts', 'visual_review', 'review', 'prompt']]
    return sorted({name for name in supplied + inferred if isinstance(name, str) and name.startswith(brand + '-') and name.endswith('.md') and (work / name).is_file()})


def study_status(work, brand, item, progress, record, current, texts):
    bound = preview_hash(record, brand, work) == current
    normalized = record.get('latest_draft_full_desktop_and_narrow_coverage') is True and (record.get('actual_raster_inspection_bound_to_current_preview') is True or record.get('latest_draft_actual_render_checked') is True)
    stated = (record.get('status') or record.get('recordUpdates', {}).get('status')) == 'visually_compared_with_scoped_differences'
    compared = bound and (normalized or stated)
    date = (record.get('observed_at') or record.get('recordedAt') or record.get('referenceDate') or record.get('source_provenance', {}).get('1280', {}).get('captured_at_utc') or record.get('audit_date') or record.get('inspection_date_local') or progress.get('observed_at') or progress.get('reference_observed_at') or '')[:10] or '日期未記錄'
    scope = ('桌面與390px窄版；官網減少動態模式' if record.get('scope', {}).get('prefers_reduced_motion') else
             '已記錄的桌面與窄版公開首頁；其他尺寸與互動未驗證' if compared else '尚未完成目前檔案的桌面與窄版主要畫面比對')
    remaining = record.get('remaining_differences_and_limits') or record.get('remainingDifferences') or record.get('remaining_differences') or record.get('remaining') or []
    study = {}
    for name in texts:
        key = ('prompts' if re.search(r'rewritten-prompts|reproduction-prompt|stitch.*prompt|prompt\.md', name, re.I) else
               'review' if re.search('review', name, re.I) else 'analysis' if re.search('analysis', name, re.I) else None)
        if key and key not in study:
            study[key] = 'official-drafts/' + name
    return dict(slug=item['slug'], file=brand, name=item['name'], preview=f'official-drafts/{brand}.html', preview_sha256=current,
                status='compared_with_differences' if compared else 'unverified', status_label='已比對主要畫面，仍有差異' if compared else '尚未驗證',
                date=date, scope=scope, reference_url=record.get('reference_url') or record.get('officialURL') or progress.get('reference_url') or '',
                remaining_differences=[value for value in remaining if isinstance(value, str)] if isinstance(remaining, list) else [],
                study=study, accepted=False, official_consistency_claim=False)


def stage_official_content(root, output, progress, catalog):
    work = root / '.stitch-work/current-official'
    destination = output / 'official-drafts'
    destination.mkdir(parents=True, exist_ok=True)
    assert len(catalog) == len(progress) == 74
    remote = read_json(root / 'data/official-remote-assets.json')['assets']
    studies, audit = [], []
    for item in catalog:
        brand = 'linear' if item['slug'] == 'linear.app' else item['slug']
        source = source_file(work, brand + '.html')
        raw, current = source.read_text(), digest(source)
        result_name, record = result_for(work, brand, current)
        manifest = manifest_for(work, brand, current)
        texts = study_texts(work, brand, record, manifest)
        status = study_status(work, brand, item, progress[item['slug']], record, current, texts)
        html = raw
        for asset in remote:
            if asset['path'] not in html:
                continue
            file = source_file(work, asset['path'])
            if file.stat().st_size != asset['bytes'] or digest(file) != asset['sha256'] or not asset['source_url'].startswith('https://'):
                raise ValueError('Original media provenance differs: ' + asset['path'])
            # Keep current preview and all referenced original media unchanged.
        exact = set(manifest['publish_allowlist']) if manifest and 'publish_allowlist' in manifest else None
        assets, queue = set(), references(html, brand)
        resolved, aliases = {}, []
        def dependency_file(relative):
            if relative in resolved:
                return resolved[relative]
            if (work / relative).is_file():
                file = source_file(work, relative)
            elif '/' not in relative and re.search(r'\.(?:woff2?|ttf|otf)$', relative, re.I):
                candidates = list((work / (brand + '-assets')).rglob(relative))
                if len(candidates) != 1:
                    raise ValueError('Missing/ambiguous original font: ' + brand + ': ' + relative)
                file = candidates[0]
                aliases.append(dict(path=relative, source_path=str(file.relative_to(work)), sha256=digest(file)))
            else:
                file = source_file(work, relative)
            resolved[relative] = file
            return file
        for value in (manifest or {}).get('runtime_required_assets', []) + (manifest or {}).get('required_local_assets', []):
            queue.append(value if isinstance(value, str) else value['path'])
        for relative in sorted(exact or []):
            source_file(work, relative)
            if relative != brand + '.html' and relative not in texts and not is_asset(relative, brand):
                raise ValueError('Nonpublic file in exact allowlist: ' + relative)
            if is_asset(relative, brand):
                queue.append(relative)
        for asset in (manifest or {}).get('required_local_assets', []) + (manifest or {}).get('runtime_required_assets', []):
            if isinstance(asset, dict) and asset.get('sha256'):
                file = source_file(work, asset['path'])
                if digest(file) != asset['sha256'] or ('bytes' in asset and file.stat().st_size != asset['bytes']):
                    raise ValueError('Required asset hash differs: ' + asset['path'])
        while queue:
            relative = queue.pop(0)
            if not relative or relative in assets or relative == brand + '.html':
                continue
            if not is_asset(relative, brand) or re.search(r'(?:asset-bundle|reference\.json|phases\.json|response\.json|manifest\.json)$', relative, re.I):
                raise ValueError('Unexpected public dependency: ' + brand + ': ' + relative)
            if exact is not None and relative not in exact:
                raise ValueError('Dependency missing from exact allowlist: ' + relative)
            file = dependency_file(relative)
            assets.add(relative)
            if file.suffix.lower() in ['.css', '.svg', '.js', '.mjs']:
                queue += references(file.read_text(), brand, str(PurePosixPath(relative).parent))
        for relative in sorted(assets | set(texts)):
            if exact is not None and relative not in exact:
                raise ValueError('Study text missing from exact allowlist: ' + relative)
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            asset_file = dependency_file(relative) if relative in assets else source_file(work, relative)
            if target.exists() and digest(target) != digest(asset_file):
                raise ValueError('Public dependency path collision: ' + relative)
            shutil.copy2(asset_file, target)
        shutil.copy2(source, destination / (brand + '.html'))
        if digest(source) != current or digest(destination / (brand + '.html')) != current:
            raise ValueError('Preview changed during publication staging: ' + brand)
        studies.append(status)
        audit.append(dict(brand=brand, preview_sha256=current, published_sha256=current, preview_copied_without_mutation=True,
                          result=result_name, manifest=(manifest or {}).get('filename'), assets=sorted(assets), dependency_aliases=aliases, study_text=texts,
                          bytes=sum(dependency_file(relative).stat().st_size for relative in assets)))
    compared = sum(study['status'] == 'compared_with_differences' for study in studies)
    (output / 'assets/official-studies.json').write_text(json.dumps(dict(count=len(studies), compared_with_differences=compared, unverified=len(studies)-compared,
        official_consistency_claim=False, studies=studies), ensure_ascii=False, separators=(',', ':')) + '\n')
    rows = []
    labels = dict(analysis='目前設計分析', prompts='重寫 AI 指令', review='畫面校正紀錄')
    for study in studies:
        limits = ''.join('<li>' + escape(value) + '</li>' for value in study['remaining_differences'])
        links = ''.join(f'<a class="study-{key}" href="{escape(value)}">{labels[key]} ↗</a> ' for key, value in study['study'].items())
        rows.append(f'<tr id="{escape(study["slug"])}" data-status="{study["status"]}"><th scope="row"><a href="{study["preview"]}">{escape(study["name"])} ↗</a></th><td class="draft"><strong>{escape(study["status_label"])}</strong><br><small class="study-scope">{escape(study["scope"])}</small><details><summary>範圍與差異</summary><a class="study-source" href="{escape(study["reference_url"])}" target="_blank" rel="noopener">公開官網 ↗</a><ul class="study-limits">{limits}</ul>{links}</details></td><td>{escape(study["date"])}</td></tr>')
    page = f'<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>74個網站重製進度 · Awesome AI Web Design</title><style>body{{font:16px/1.6 system-ui,sans-serif;background:#f8f7f3;color:#20211f;margin:0}}main{{max-width:1120px;margin:auto;padding:48px 24px 96px}}a{{color:inherit}}h1{{font-size:clamp(32px,5vw,54px);line-height:1.1}}table{{border-collapse:collapse;table-layout:fixed;width:100%;background:white;margin-top:32px}}th,td{{box-sizing:border-box;text-align:left;border-bottom:1px solid #e2e0da;padding:16px;vertical-align:top;overflow-wrap:anywhere}}th:first-child{{width:18%}}th:last-child{{width:18%}}small{{color:#666}}details{{max-width:100%;min-width:0;margin-top:8px}}summary{{cursor:pointer}}details ul{{padding-inline-start:20px}}li{{margin-bottom:8px}}.draft strong{{color:#a34317}}td a{{display:inline-block;max-width:calc(100% - 8px);margin:4px 8px 4px 0;overflow-wrap:anywhere}}@media(max-width:600px){{main{{padding:28px 12px}}th,td{{padding:10px 6px;font-size:13px}}th:first-child{{width:22%}}th:last-child{{width:23%}}}}</style></head><body><main><header><a href="index.html#official-drafts">← 返回設計集</a></header><h1>74個網站重製進度</h1><p>{compared}份已比對主要畫面、仍有差異；{len(studies)-compared}份尚未驗證。所有研究均為免費的日期限定重製，未宣稱與官方完全一致。</p><p>已比對僅涵蓋記錄的公開首頁與尺寸。動畫、服務、其他尺寸及目前部署須依每頁紀錄判讀。原有74份設計分析及222則指令完整保留。</p><table><thead><tr><th>品牌</th><th>狀態與範圍</th><th>參考日期</th></tr></thead><tbody>{"".join(rows)}</tbody></table></main></body></html>'
    (output / 'official-progress.html').write_text(page)
    (root / '.stitch-work/publication-plan.json').write_text(json.dumps(dict(official_consistency_claim=False, studies=audit), ensure_ascii=False, indent=2) + '\n')
    return dict(count=len(studies), compared_with_differences=compared, public_asset_count=sum(len(row['assets']) for row in audit), public_asset_bytes=sum(row['bytes'] for row in audit))
