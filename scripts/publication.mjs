// Exact public dependency closure and conservative, hash-bound study labels.
import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';

const sha = bytes => createHash('sha256').update(bytes).digest('hex');
const escape = value => String(value).replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#x27;'}[char]));
const readJSON = file => JSON.parse(fs.readFileSync(file, 'utf8'));
function decode(value) {
  return value.replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#(?:x([0-9a-f]+)|(\d+));/gi, (_, hex, number) => String.fromCodePoint(parseInt(hex || number, hex ? 16 : 10)));
}
function sourceFile(work, relative) {
  if (!relative || path.isAbsolute(relative) || relative.includes('\\') || relative.split('/').includes('..')) throw new Error('Unsafe publication path: ' + relative);
  const file = path.resolve(work, relative);
  if (!fs.existsSync(file) || !fs.statSync(file).isFile() || !fs.realpathSync(file).startsWith(fs.realpathSync(work) + path.sep)) throw new Error('Missing/unsafe publication file: ' + relative);
  return file;
}
function isAsset(relative, brand) {
  // A few historical studies share one explicitly referenced media library.
  return /^[a-z0-9.-]+-(?:assets|fonts|browser-images)\//.test(relative) || /^[a-z0-9.-]+\.(?:svg|png|webp|avif|woff2?|ttf|css|js)$/.test(relative);
}
function references(text, brand, base = '') {
  // JSON templates are inert source data. Read their escaped asset strings;
  // never execute captured scripts or discard their dependency references.
  const templates = [];
  const config = /(?:const|let|var)\s+CONFIG\s*=\s*/.exec(text);
  if (config) {
    const start = config.index + config[0].length;
    let depth = 0, quoted = false, escaped = false, end = start;
    for (; end < text.length; end++) {
      const char = text[end];
      if (quoted) {if (escaped) escaped = false; else if (char === '\\') escaped = true; else if (char === '"') quoted = false;}
      else if (char === '"') quoted = true;
      else if (char === '{' || char === '[') depth++;
      else if ((char === '}' || char === ']') && --depth === 0) {end++; break;}
    }
    const collect = value => {
      if (typeof value === 'string' && value.includes('<')) templates.push(value);
      else if (value && typeof value === 'object') Object.values(value).forEach(collect);
    };
    collect(JSON.parse(text.slice(start, end)));
  }
  const normalized = [text, ...templates].join('\n').replace(/\\u002f/gi, '/').replace(/\\u0026/gi, '&').replace(/\\\//g, '/');
  const staticHTML = normalized.replace(/(<script\b[^>]*>)[\s\S]*?<\/script\s*>/gi, '$1</script>');
  const values = [];
  for (const match of staticHTML.matchAll(/(?:^|\s)(?:src|href|poster|xlink:href)\s*=\s*(?:"([^"]*)"|'([^']*)')/gim)) values.push(match[1] ?? match[2]);
  for (const match of normalized.matchAll(/url\(\s*(['"]?)(.*?)\1\s*\)/g)) values.push(match[2]);
  for (const match of normalized.matchAll(/@import\s+['"]([^'"]+)['"]/g)) values.push(match[1]);
  const escapedBrand = brand.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  for (const match of decode(normalized).matchAll(new RegExp('(?<![a-zA-Z0-9._~:/-])' + escapedBrand + '(?:-[a-z0-9]+)*-assets/[^<>"\'\\\\\\r\\n?#]*?\\.[a-zA-Z0-9]{1,10}(?=[\\s,)"\'\\\\?#<}]|$)', 'g'))) values.push(match[0]);
  const out = new Set();
  for (let value of values) {
    value = decode(value).replace(/\\(['"])/g, '$1').trim().replace(/^['"]|['"]$/g, '');
    // Search-result template expressions are resolved by the browser, not files.
    if (value.includes('${') || /^\{[A-Z][A-Z0-9_]*\}(?:[?#].*)?$/.test(value)) continue;
    if (!value || /^(?:[a-z][a-z0-9+.-]*:|\/|#)/i.test(value) || decodeURIComponent(value).startsWith('#')) continue;
    const relative = value.split(/[?#]/, 1)[0];
    if (!relative || relative.endsWith('/')) continue;
    const joined = /^[a-z0-9.-]+-(?:assets|fonts|browser-images)\//.test(relative) ? relative : path.posix.normalize(path.posix.join(base, relative));
    out.add(joined);
  }
  return [...out].sort();
}
function previewHash(record, brand, work) {
  for (const value of [record.preview_sha256, record.previewSha256, record.local_draft?.sha256, record.preview?.sha256]) if (typeof value === 'string') return value;
  const stores = [record.hashes, record.files];
  for (const name of [record.hashManifest, record.hash_manifest]) if (typeof name === 'string') stores.push(readJSON(sourceFile(work, name)));
  for (const store of stores) {
    const rows = Array.isArray(store) ? store : Object.entries(store || {}).map(([key, value]) => ({path: key, ...(typeof value === 'string' ? {sha256: value} : value)}));
    for (const row of rows) if (path.posix.basename(row.path || row.file || '') === brand + '.html') return row.sha256;
  }
  return null;
}
function resultFor(work, brand, current) {
  for (const name of fs.readdirSync(work).filter(name => name.startsWith(brand + '-') && name.endsWith('-result.json') && !/-pre-|pre-current|pre-oct/.test(name)).sort().reverse()) {
    const record = readJSON(path.join(work, name));
    if (previewHash(record, brand, work) === current) return {name, record};
  }
  return {name: null, record: {}};
}
function manifestFor(work, brand, current) {
  const names = fs.readdirSync(work).filter(name => name.startsWith(brand + '-') && name.endsWith('-publication-manifest.json')).sort().reverse();
  if (!names.length) return null;
  for (const name of names) {
    const manifest = readJSON(path.join(work, name));
    if (manifest.preview?.sha256 === current && manifest.preview.path === brand + '.html') return {...manifest, filename: name};
  }
  throw new Error('Publication manifest does not bind current preview: ' + brand);
}
function studyTexts(work, brand, record, manifest) {
  const supplied = manifest?.study_text || Object.values(record.current_supplements || {}).filter(value => typeof value === 'string' && value.endsWith('.md'));
  const inferred = [record.designAnalysis, record.design_analysis, record.rewrittenPrompt, record.rewritten_prompts, record.visual_review, record.review, record.prompt];
  const names = [...new Set([...supplied, ...inferred].filter(value => typeof value === 'string' && value.startsWith(brand + '-') && value.endsWith('.md')))];
  return names.filter(name => fs.existsSync(path.join(work, name))).sort();
}
function studyStatus(brand, item, progress, record, current, texts) {
  const bound = previewHash(record, brand, progress.work) === current;
  const normalized = record.latest_draft_full_desktop_and_narrow_coverage === true && (record.actual_raster_inspection_bound_to_current_preview === true || record.latest_draft_actual_render_checked === true);
  const statedComparison = (record.status || record.recordUpdates?.status) === 'visually_compared_with_scoped_differences';
  // Older records without explicit full-coverage/raster flags remain unverified.
  const compared = bound && (normalized || statedComparison);
  const date = (record.observed_at || record.recordedAt || record.referenceDate || record.source_provenance?.['1280']?.captured_at_utc || record.audit_date || record.inspection_date_local || progress.observed_at || progress.reference_observed_at || '').slice(0, 10) || '日期未記錄';
  const scope = record.scope?.prefers_reduced_motion ? '桌面與390px窄版；官網減少動態模式' : compared ? '已記錄的桌面與窄版公開首頁；其他尺寸與互動未驗證' : '尚未完成目前檔案的桌面與窄版主要畫面比對';
  const remaining = record.remaining_differences_and_limits || record.remainingDifferences || record.remaining_differences || record.remaining || [];
  const study = {};
  for (const name of texts) {
    const key = /(?:rewritten-prompts|reproduction-prompt|stitch.*prompt|prompt\.md)/i.test(name) ? 'prompts' : /review/i.test(name) ? 'review' : /analysis/i.test(name) ? 'analysis' : null;
    if (key && !study[key]) study[key] = 'official-drafts/' + name;
  }
  return {slug: item.slug, file: brand, name: item.name, preview: `official-drafts/${brand}.html`, preview_sha256: current,
    status: compared ? 'compared_with_differences' : 'unverified', status_label: compared ? '已比對主要畫面，仍有差異' : '尚未驗證',
    date, scope, reference_url: record.reference_url || record.officialURL || progress.reference_url || '',
    remaining_differences: Array.isArray(remaining) ? remaining.filter(value => typeof value === 'string') : [], study,
    accepted: false, official_consistency_claim: false};
}

export function stageOfficialContent(root, output, progress, catalog) {
  const work = path.join(root, '.stitch-work/current-official');
  const destination = path.join(output, 'official-drafts');
  fs.mkdirSync(destination, {recursive: true});
  if (catalog.length !== 74 || Object.keys(progress).length !== 74) throw new Error('Expected74 original catalog/progress records');
  const remote = readJSON(path.join(root, 'data/official-remote-assets.json')).assets;
  const studies = [], audit = [];
  for (const item of catalog) {
    const brand = item.slug === 'linear.app' ? 'linear' : item.slug;
    const source = sourceFile(work, brand + '.html');
    const raw = fs.readFileSync(source, 'utf8'), current = sha(fs.readFileSync(source));
    const {name: resultName, record} = resultFor(work, brand, current);
    const manifest = manifestFor(work, brand, current);
    const texts = studyTexts(work, brand, record, manifest);
    const status = studyStatus(brand, item, {...progress[item.slug], work}, record, current, texts);
    let html = raw;
    for (const asset of remote) if (html.includes(asset.path)) {
      const bytes = fs.readFileSync(sourceFile(work, asset.path));
      if (bytes.length !== asset.bytes || sha(bytes) !== asset.sha256 || new URL(asset.source_url).protocol !== 'https:') throw new Error('Original media provenance differs: ' + asset.path);
      // Preserve current preview bytes: referenced original media stays local.
    }
    const exact = manifest?.publish_allowlist ? new Set(manifest.publish_allowlist) : null;
    const assets = new Set(), queue = references(html, brand), resolved = new Map(), aliases = [];
    function dependencyFile(relative) {
      if (resolved.has(relative)) return resolved.get(relative);
      let file;
      if (fs.existsSync(path.join(work, relative))) file = sourceFile(work, relative);
      else if (!relative.includes('/') && /\.(?:woff2?|ttf|otf)$/i.test(relative)) {
        // Historical inline font CSS uses bare hashed filenames. Publish a
        // byte-identical alias only when one exact basename is preserved.
        const directory = path.join(work, brand + '-assets');
        const candidates = [];
        const walk = dir => {for (const entry of fs.readdirSync(dir, {withFileTypes:true})) {const next=path.join(dir,entry.name);if(entry.isDirectory())walk(next);else if(entry.isFile()&&entry.name===relative)candidates.push(next);}};
        if (fs.existsSync(directory)) walk(directory);
        if (candidates.length !== 1) throw new Error('Missing/ambiguous original font: ' + brand + ': ' + relative);
        file = candidates[0]; aliases.push({path:relative, source_path:path.relative(work,file), sha256:sha(fs.readFileSync(file))});
      } else file = sourceFile(work, relative);
      resolved.set(relative, file); return file;
    }
    for (const value of manifest?.runtime_required_assets || []) queue.push(typeof value === 'string' ? value : value.path);
    for (const value of manifest?.required_local_assets || []) queue.push(typeof value === 'string' ? value : value.path);
    if (exact) for (const relative of exact) {
      sourceFile(work, relative);
      if (relative !== brand + '.html' && !texts.includes(relative) && !isAsset(relative, brand)) throw new Error('Nonpublic file in exact allowlist: ' + relative);
      if (isAsset(relative, brand)) queue.push(relative);
    }
    for (const asset of [...(manifest?.required_local_assets || []), ...(manifest?.runtime_required_assets || [])]) if (typeof asset === 'object' && asset.sha256) {
      const bytes = fs.readFileSync(sourceFile(work, asset.path));
      if (sha(bytes) !== asset.sha256 || (asset.bytes !== undefined && bytes.length !== asset.bytes)) throw new Error('Required asset hash differs: ' + asset.path);
    }
    while (queue.length) {
      const relative = queue.shift();
      if (!relative || assets.has(relative)) continue;
      if (relative === brand + '.html') continue;
      if (!isAsset(relative, brand) || /(?:asset-bundle|reference\.json|phases\.json|response\.json|manifest\.json)$/i.test(relative)) throw new Error('Unexpected public dependency: ' + brand + ': ' + relative);
      if (exact && !exact.has(relative)) throw new Error('Dependency missing from exact allowlist: ' + relative);
      const file = dependencyFile(relative);
      assets.add(relative);
      if (/\.(?:css|svg|js|mjs)$/i.test(relative)) queue.push(...references(fs.readFileSync(file, 'utf8'), brand, path.posix.dirname(relative)));
    }
    for (const relative of [...assets, ...texts].sort()) {
      if (exact && !exact.has(relative)) throw new Error('Study text missing from exact allowlist: ' + relative);
      const target = path.join(destination, relative);
      fs.mkdirSync(path.dirname(target), {recursive: true});
      const assetFile = assets.has(relative) ? dependencyFile(relative) : sourceFile(work, relative);
      if (fs.existsSync(target) && sha(fs.readFileSync(target)) !== sha(fs.readFileSync(assetFile))) throw new Error('Public dependency path collision: ' + relative);
      fs.copyFileSync(assetFile, target);
    }
    fs.copyFileSync(source, path.join(destination, brand + '.html'));
    if (sha(fs.readFileSync(source)) !== current || sha(fs.readFileSync(path.join(destination, brand + '.html'))) !== current) throw new Error('Preview changed during publication staging: ' + brand);
    studies.push(status);
    audit.push({brand, preview_sha256: current, published_sha256: current, preview_copied_without_mutation: true,
      result: resultName, manifest: manifest?.filename || null, assets: [...assets].sort(), dependency_aliases:aliases, study_text: texts, bytes: [...assets].reduce((total, relative) => total + fs.statSync(dependencyFile(relative)).size, 0)});
  }
  const compared = studies.filter(study => study.status === 'compared_with_differences').length;
  fs.writeFileSync(path.join(output, 'assets/official-studies.json'), JSON.stringify({count: studies.length, compared_with_differences: compared, unverified: studies.length - compared, official_consistency_claim: false, studies}) + '\n');
  const rows = studies.map(study => `<tr id="${escape(study.slug)}" data-status="${study.status}"><th scope="row"><a href="${study.preview}">${escape(study.name)} ↗</a></th><td class="draft"><strong>${escape(study.status_label)}</strong><br><small class="study-scope">${escape(study.scope)}</small><details><summary>範圍與差異</summary><a class="study-source" href="${escape(study.reference_url)}" target="_blank" rel="noopener">公開官網 ↗</a><ul class="study-limits">${study.remaining_differences.map(value => '<li>' + escape(value) + '</li>').join('')}</ul>${Object.entries(study.study).map(([key, value]) => `<a class="study-${key}" href="${escape(value)}">${({analysis:'目前設計分析',prompts:'重寫 AI 指令',review:'畫面校正紀錄'})[key]} ↗</a> `).join('')}</details></td><td>${escape(study.date)}</td></tr>`);
  const page = `<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>74個網站重製進度 · Awesome AI Web Design</title><style>body{font:16px/1.6 system-ui,sans-serif;background:#f8f7f3;color:#20211f;margin:0}main{max-width:1120px;margin:auto;padding:48px 24px 96px}a{color:inherit}h1{font-size:clamp(32px,5vw,54px);line-height:1.1}table{border-collapse:collapse;table-layout:fixed;width:100%;background:white;margin-top:32px}th,td{box-sizing:border-box;text-align:left;border-bottom:1px solid #e2e0da;padding:16px;vertical-align:top;overflow-wrap:anywhere}th:first-child{width:18%}th:last-child{width:18%}small{color:#666}details{max-width:100%;min-width:0;margin-top:8px}summary{cursor:pointer}details ul{padding-inline-start:20px}li{margin-bottom:8px}.draft strong{color:#a34317}td a{display:inline-block;max-width:calc(100% - 8px);margin:4px 8px 4px 0;overflow-wrap:anywhere}@media(max-width:600px){main{padding:28px 12px}th,td{padding:10px 6px;font-size:13px}th:first-child{width:22%}th:last-child{width:23%}}</style></head><body><main><header><a href="index.html#official-drafts">← 返回設計集</a></header><h1>74個網站重製進度</h1><p>${compared}份已比對主要畫面、仍有差異；${studies.length - compared}份尚未驗證。所有研究均為免費的日期限定重製，未宣稱與官方完全一致。</p><p>已比對僅涵蓋記錄的公開首頁與尺寸。動畫、服務、其他尺寸及目前部署須依每頁紀錄判讀。原有74份設計分析及222則指令完整保留。</p><table><thead><tr><th>品牌</th><th>狀態與範圍</th><th>參考日期</th></tr></thead><tbody>${rows.join('')}</tbody></table></main></body></html>`;
  fs.writeFileSync(path.join(output, 'official-progress.html'), page);
  fs.writeFileSync(path.join(root, '.stitch-work/publication-plan.json'), JSON.stringify({official_consistency_claim: false, studies: audit}, null, 2) + '\n');
  return {count: studies.length, compared_with_differences: compared, public_asset_count: audit.reduce((sum, row) => sum + row.assets.length, 0), public_asset_bytes: audit.reduce((sum, row) => sum + row.bytes, 0)};
}
