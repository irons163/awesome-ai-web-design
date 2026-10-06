#!/usr/bin/env node
// Build the same static Site as build_site.py where Python is unavailable.
import fs from 'node:fs';
import { createHash } from 'node:crypto';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const OUTPUT = path.join(ROOT, 'dist');
const DRAFT_SOURCE = path.join(ROOT, '.stitch-work', 'current-official');
const OFFICIAL_DRAFTS = [
  'spotify', 'linear', 'claude', 'notion', 'figma', 'framer', 'vercel',
  'airbnb', 'airtable', 'stripe', 'starbucks', 'shopify', 'slack',
  'supabase', 'resend', 'ollama', 'raycast', 'cal', 'cursor', 'apple',
  'clay', 'clickhouse', 'cohere', 'composio', 'expo', 'mintlify',
  'elevenlabs', 'miro', 'opencode.ai', 'voltagent', 'posthog', 'warp',
  'webflow', 'wise', 'zapier', 'tesla', 'mistral.ai', 'replicate', 'together.ai', 'sanity', 'sentry', 'ibm', 'mongodb', 'intercom', 'superhuman', 'kraken', 'coinbase', 'nike', 'minimax', 'spacex', 'hashicorp', 'lovable', 'x.ai', 'nvidia', 'hp', 'playstation', 'runwayml', 'uber', 'bmw', 'bmw-m', 'bugatti', 'ferrari', 'lamborghini', 'renault',
];
const COPY_ALL_ASSETS = new Set([
  'slack', 'supabase', 'voltagent', 'posthog', 'warp', 'webflow', 'wise',
  'zapier', 'tesla', 'mistral.ai', 'replicate', 'together.ai', 'sentry', 'intercom', 'superhuman', 'kraken', 'coinbase', 'nike', 'minimax', 'spacex', 'bmw', 'bmw-m', 'bugatti', 'ferrari', 'renault',
]);
const SANITY_HOSTED_SUFFIXES = new Set([
  '.css', '.woff', '.woff2', '.ttf', '.svg', '.webp',
]);

const read = p => fs.readFileSync(p, 'utf8');
const write = (p, content) => fs.writeFileSync(p, content);
const json = p => JSON.parse(read(p));
const REMOTE_ASSETS = json(path.join(ROOT, 'data', 'official-remote-assets.json')).assets;
const REMOTE_PATHS = new Set(REMOTE_ASSETS.map(asset => asset.path));

function retainOriginalMedia(html) {
  for (const asset of REMOTE_ASSETS) {
    if (!html.includes(asset.path)) continue;
    const original = fs.readFileSync(path.join(DRAFT_SOURCE, asset.path));
    if (original.length !== asset.bytes ||
        createHash('sha256').update(original).digest('hex') !== asset.sha256 ||
        new URL(asset.source_url).protocol !== 'https:') {
      throw new Error('Original media provenance differs: ' + asset.path);
    }
    html = html.replaceAll(asset.path, asset.source_url);
  }
  return html;
}
const escapeHtml = text => String(text).replace(/&/g, '&amp;')
  .replace(/</g, '&lt;').replace(/>/g, '&gt;')
  .replace(/"/g, '&quot;').replace(/'/g, '&#x27;');

function decodeEntities(value) {
  return value.replace(/&(?:amp|quot|apos|lt|gt|#x[0-9a-f]+|#[0-9]+);/gi, match => {
    const named = { '&amp;': '&', '&quot;': '"', '&apos;': "'", '&lt;': '<', '&gt;': '>' };
    if (named[match.toLowerCase()]) return named[match.toLowerCase()];
    if (match.toLowerCase().startsWith('&#x')) {
      return String.fromCodePoint(parseInt(match.slice(3, -1), 16));
    }
    return String.fromCodePoint(parseInt(match.slice(2, -1), 10));
  });
}

function references(html) {
  // Retain script src attributes, but exclude JavaScript strings containing
  // runtime-generated markup. The Python HTML parser also ignores this text.
  html = html.replace(/(<script\b[^>]*>)[\s\S]*?<\/script\s*>/gi, '$1</script>');
  const values = [];
  for (const match of html.matchAll(/(?:^|\s)(?:src|href|poster)\s*=\s*(?:"([^"]*)"|'([^']*)')/gim)) {
    values.push(match[1] ?? match[2]);
  }
  for (const match of html.matchAll(/url\(([^)]+)\)/g)) values.push(match[1]);
  return values;
}

function copyReferencedAsset(name, value) {
  value = decodeEntities(value).trim().replace(/^['"]|['"]$/g, '');
  if (!value || decodeURIComponent(value).startsWith('#') ||
      /^(?:https?:|data:|mailto:|tel:|\/)/i.test(value)) return;
  const relative = value.split(/[?#]/, 1)[0];
  const source = path.resolve(DRAFT_SOURCE, relative);
  if (!source.startsWith(DRAFT_SOURCE + path.sep)) {
    throw new Error('Draft asset escapes source area: ' + name + ': ' + relative);
  }
  if (!fs.existsSync(source) || !fs.statSync(source).isFile()) {
    throw new Error('Missing ' + name + ' draft asset: ' + relative);
  }
  const target = path.join(OUTPUT, 'official-drafts', relative);
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.copyFileSync(source, target);
}

function stageOfficialDrafts(progress) {
  const destination = path.join(OUTPUT, 'official-drafts');
  fs.mkdirSync(destination);
  const style = `<meta name="robots" content="noindex"><style>
.official-draft-badge{position:fixed;right:16px;bottom:16px;z-index:2147483647;max-width:min(340px,calc(100vw - 32px));padding:12px 16px;background:#fffdf7;color:#20211f;border:1px solid #d5d3ca;border-radius:9px;box-shadow:0 8px 34px #0004;font:12px/1.5 system-ui,sans-serif;display:grid;gap:3px}
.official-draft-badge strong{font-size:13px}.official-draft-badge span{color:#555}.official-draft-badge a{color:#a53d22;text-decoration:underline}
</style>`;
  for (const name of OFFICIAL_DRAFTS) {
    let html = retainOriginalMedia(read(path.join(DRAFT_SOURCE, name + '.html')));
    for (const value of references(html)) copyReferencedAsset(name, value);
    if (COPY_ALL_ASSETS.has(name)) {
      fs.cpSync(path.join(DRAFT_SOURCE, name + '-assets'),
        path.join(destination, name + '-assets'), {
          recursive: true, force: true,
          filter: source => !REMOTE_PATHS.has(path.relative(DRAFT_SOURCE, source)) &&
            (!['bmw', 'bmw-m', 'bugatti', 'ferrari'].includes(name) || !path.basename(source).startsWith('source-')) &&
            (name !== 'tesla' ||
            !['Homepage-FSD-Card-Desktop.mp4', 'Homepage-FSD-Card-Mobile.mp4'].includes(path.basename(source))),
        });
    }
    if (name === 'sanity') {
      const sourceRoot = path.join(DRAFT_SOURCE, 'sanity-assets');
      const copyFiltered = directory => {
        for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
          const source = path.join(directory, entry.name);
          if (entry.isDirectory()) {
            copyFiltered(source);
          } else if (entry.isFile() && SANITY_HOSTED_SUFFIXES.has(path.extname(entry.name))) {
            const target = path.join(destination,
              path.relative(DRAFT_SOURCE, source));
            fs.mkdirSync(path.dirname(target), { recursive: true });
            fs.copyFileSync(source, target);
          }
        }
      };
      copyFiltered(sourceRoot);
    }
    if (name === 'lamborghini') {
      const sourceRoot = path.join(DRAFT_SOURCE, 'lamborghini-assets');
      for (const entry of fs.readdirSync(sourceRoot, { withFileTypes: true })) {
        if (!entry.isFile() || !(entry.name === 'display.css' ||
            ['.woff', '.woff2', '.ttf', '.svg'].includes(path.extname(entry.name)))) continue;
        const source = path.join(sourceRoot, entry.name);
        const target = path.join(destination, path.relative(DRAFT_SOURCE, source));
        fs.mkdirSync(path.dirname(target), { recursive: true });
        fs.copyFileSync(source, target);
      }
    }
    const record = progress[name === 'linear' ? 'linear.app' : name];
    const observed = escapeHtml((record.observed_at || record.reference_observed_at || '').slice(0, 10) || '日期未記錄');
    const note = record.review_note;
    const badge = '<div class="official-draft-badge" role="note">' +
      '<strong>官網重製草稿 · 尚未視覺驗收</strong>' +
      `<span>參考資料：${observed}；非品牌官方網站。</span>` +
      (note ? `<span>${escapeHtml(note)}</span>` : '') +
      '<a href="../official-progress.html">查看 74 站進度 ↗</a></div>';
    if (!html.includes('</head>')) throw new Error('Draft has no head: ' + name);
    html = html.replace('</head>', style + '</head>');
    const body = /<body\b[^>]*>/i.exec(html);
    if (!body) throw new Error('Draft has no body: ' + name);
    html = html.slice(0, body.index + body[0].length) + badge +
      html.slice(body.index + body[0].length);
    write(path.join(destination, name + '.html'), html);
  }
}

function stageOfficialProgress(progress) {
  const catalog = json(path.join(ROOT, 'assets', 'catalog.json')).designs;
  if (catalog.length !== 74 || Object.keys(progress).length !== 74) {
    throw new Error('Expected 74 catalog and progress records');
  }
  const labels = {
    in_visual_review: ['草稿待視覺驗收', 'draft'],
    draft_unverified: ['草稿待視覺驗收', 'draft'],
    local_draft_pending_stitch: ['本機草稿待 Stitch 與視覺驗收', 'local'],
    source_snapshot_only: ['已保存網頁資料，尚未重製', 'snapshot'],
    reference_pending: ['尚無可用參考畫面', 'pending'],
  };
  const counts = { draft: 0, local: 0, snapshot: 0, pending: 0 };
  const rows = [];
  for (const item of catalog) {
    const record = progress[item.slug];
    const [label, kind] = labels[record.status];
    counts[kind]++;
    const draftName = item.slug === 'linear.app' ? 'linear' : item.slug;
    const href = kind === 'draft' ? `official-drafts/${draftName}.html`
      : kind === 'local' ? record.reference_url
      : `index.html#/design/${item.slug}`;
    const date = (record.observed_at || record.reference_observed_at || '').slice(0, 10) || '—';
    const note = record.review_note;
    rows.push('<tr><th scope="row"><a href="' + escapeHtml(href) + '">' +
      escapeHtml(item.name) + ' ↗</a></th><td class="' + kind + '">' +
      label + (note ? `<br><small>${escapeHtml(note)}</small>` : '') +
      '</td><td>' + escapeHtml(date) + '</td></tr>');
  }
  if (Object.values(counts).reduce((a, b) => a + b, 0) !== 74 ||
      counts.draft !== OFFICIAL_DRAFTS.length) {
    throw new Error('Draft status count differs from staged pages');
  }
  const page = '<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>74 個網站重製進度 · Awesome AI Web Design</title><style>\n' +
    'body{font:16px/1.6 system-ui,sans-serif;background:#f8f7f3;color:#20211f;margin:0}main{max-width:1040px;margin:auto;padding:48px 24px 96px}a{color:inherit}a:hover{color:#bf421e}header a{font-weight:700;text-decoration:none}h1{font-size:clamp(32px,5vw,54px);line-height:1.1;margin:32px 0 16px}p{max-width:760px}table{border-collapse:collapse;width:100%;background:white;margin-top:36px}th,td{text-align:left;border-bottom:1px solid #e2e0da;padding:13px 18px}thead th{background:#eeeae1;font-size:13px;letter-spacing:.04em}tbody th{font-weight:600}tbody th a{text-decoration:none}.draft{color:#a34317}.local{color:#805ba5}.snapshot{color:#4d6381}.pending{color:#777}small{color:#666}@media(max-width:600px){main{padding:28px 14px}th,td{padding:10px 8px;font-size:13px}}\n' +
    '</style></head><body><main><header><a href="index.html#official-drafts">← 返回設計集</a></header><h1>74 個網站重製進度</h1><p>目前有 ' +
    counts.draft + ' 份公開的官網重製草稿、' + counts.local +
    ' 份尚未公開的本機草稿，0 份完成逐頁視覺驗收；其餘 ' +
    counts.snapshot + ' 個已保存特定日期的網頁資料，' +
    counts.pending + ' 個尚無可用參考畫面。原本的 Stitch 範例不列為官網重製完成品。</p><p><small>「參考日期」是資料擷取日期，不代表今天的官網畫面；所有草稿仍需和品牌現行網站逐頁、逐裝置比較。</small></p><table><thead><tr><th scope="col">品牌</th><th scope="col">狀態</th><th scope="col">參考日期</th></tr></thead><tbody>' +
    rows.join('') + '</tbody></table></main></body></html>';
  write(path.join(OUTPUT, 'official-progress.html'), page);
}

function main() {
  if (fs.existsSync(OUTPUT) && fs.lstatSync(OUTPUT).isSymbolicLink()) {
    throw new Error('dist must be a regular build directory');
  }
  fs.rmSync(OUTPUT, { recursive: true, force: true });
  fs.mkdirSync(OUTPUT);
  for (const name of ['index.html', 'README.md', 'ATTRIBUTION.md', 'LICENSE', 'CONTRIBUTING.md']) {
    fs.copyFileSync(path.join(ROOT, name), path.join(OUTPUT, name));
  }
  for (const name of ['assets', 'design-md', 'prompts']) {
    fs.cpSync(path.join(ROOT, name), path.join(OUTPUT, name), { recursive: true });
  }
  fs.rmSync(path.join(OUTPUT, 'assets', 'all-designs.zip'), { force: true });
  const imageBase = json(path.join(ROOT, 'data', 'hosting-assets.json')).image_base_url.replace(/\/?$/, '/');
  const catalogPath = path.join(OUTPUT, 'assets', 'catalog.json');
  const catalog = json(catalogPath);
  for (const item of catalog.designs) {
    if (item.preview.status !== 'generated') continue;
    for (const key of ['image', 'thumbnail']) {
      const relative = item.preview[key];
      item.preview[key] = imageBase + relative;
      fs.rmSync(path.join(OUTPUT, relative), { force: true });
    }
  }
  write(catalogPath, JSON.stringify(catalog) + '\n');
  const progress = json(path.join(DRAFT_SOURCE, 'progress.json'));
  stageOfficialDrafts(progress);
  stageOfficialProgress(progress);
  console.log('Staged public website in ' + OUTPUT);
}

main();
