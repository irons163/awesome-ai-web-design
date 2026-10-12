import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {JSDOM,VirtualConsole} from 'jsdom';
const work=path.resolve('.stitch-work/current-official');
const file=path.join(work,'clickhouse.html');
const original=fs.readFileSync(file,'utf8');
const start=original.indexOf('const CONFIG=')+13,end=original.indexOf(';(function runtime',start);
const config=JSON.parse(original.slice(start,end));
const source=JSON.parse(fs.readFileSync(path.join(work,'clickhouse-oct10-official-1280-reference.json')));
const doc=new JSDOM(source.htmlParts.join(''),{virtualConsole:new VirtualConsole()}).window.document;
const style=doc.documentElement.getAttribute('style');
if(style!=='--header-height: 76px;')throw new Error('Current source desktop header offset changed');
const previous=config.attributes[1280].html.style||'';
config.attributes[1280].html.style=style;
const corrected=original.slice(0,start)+JSON.stringify(config).replace(/</g,'\\u003c')+original.slice(end);
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const backup=path.join(work,'clickhouse-oct11-pre-header-offset.html');
if(!fs.existsSync(backup))fs.writeFileSync(backup,original);
fs.writeFileSync(file,corrected);
fs.writeFileSync(path.join(work,'clickhouse-oct11-header-offset-correction.json'),JSON.stringify({
  accepted:false,official_consistency_claim:false,previous_sha256:hash(original),corrected_sha256:hash(corrected),
  width:1280,previous_html_style:previous,corrected_html_style:style,
  reference:'clickhouse-oct10-official-1280-reference.json',observed_at:source.observed_at,
  reason:'Original first desktop end DOM lacked runtime header CSS variable, so the customer-story sticky sidebar overlapped the fixed navigation.',
  actual_render_after_correction_verified:false
},null,2)+'\n');
console.log(JSON.stringify({brand:'clickhouse',bytes:Buffer.byteLength(corrected),sha256:hash(corrected)}));
