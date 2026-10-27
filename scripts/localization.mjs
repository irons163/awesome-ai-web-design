// Publish reviewed Chinese text without mutating captured preview evidence.
import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';

const digest = value => createHash('sha256').update(value).digest('hex');

export function loadLocalizations(root, catalog) {
  const data = JSON.parse(fs.readFileSync(path.join(root,'data/zh-TW/studies.json'),'utf8'));
  if (data.locale !== 'zh-TW' || Object.keys(data.studies).sort().join('\n') !== catalog.map(item=>item.slug).sort().join('\n')) {
    throw new Error('Incomplete Taiwan Chinese publication');
  }
  return data;
}

export function localizeStudy(root, destination, status, data) {
  const row = data.studies[status.slug];
  if (row.source_preview_sha256 !== status.preview_sha256) throw new Error('Chinese text is bound to another preview: '+status.slug);
  if (digest(JSON.stringify(status.remaining_differences)) !== row.remaining_source_sha256) throw new Error('Chinese limitations require review: '+status.slug);
  if (Object.keys(row.documents).sort().join('\n') !== Object.keys(status.study).sort().join('\n')) throw new Error('Chinese document coverage differs: '+status.slug);
  status.document_sha256 = {};
  for (const [kind,relative] of Object.entries(status.study)) {
    const source = row.source_documents[kind];
    if (relative !== source.path || !relative.startsWith('official-drafts/') || path.posix.basename(relative) !== relative.slice('official-drafts/'.length)) throw new Error('Unsafe or stale Chinese document path');
    const original = path.join(root,'.stitch-work/current-official',path.posix.basename(relative));
    if (digest(fs.readFileSync(original)) !== source.sha256) throw new Error('Chinese document source changed: '+relative);
    const target = path.join(destination,path.posix.basename(relative));
    if (!fs.existsSync(target) || digest(fs.readFileSync(target)) !== source.sha256) throw new Error('Unexpected document before localization: '+relative);
    const text = row.documents[kind];
    if (!text.includes('繁體中文（台灣用語，zh-TW）')) throw new Error('Missing Taiwan Chinese document');
    fs.writeFileSync(target,text);
    status.document_sha256[kind] = digest(text);
  }
  status.remaining_differences = row.remaining_differences;
  status.document_language = 'zh-TW';
  status.localized_at = data.updated;
  if (row.implementation_files) {
    status.implementation_files = {};
    for (const [name,file] of Object.entries(row.implementation_files)) {
      const relative = file.path;
      if (!['TOKENS.json','ASSETS.json','ASSETS.md','starter.css'].includes(name) || relative !== `implementation/${status.slug}/${name}`) throw new Error('Unsafe implementation companion path');
      const target = path.join(path.dirname(destination),relative);
      fs.mkdirSync(path.dirname(target),{recursive:true});
      fs.writeFileSync(target,file.text);
      status.implementation_files[name] = {path:relative,sha256:digest(file.text)};
    }
    status.implementation_version = data.updated;
  }
}
