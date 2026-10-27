// Deterministic, dependency-free ZIP of the same public study documents.
import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {deflateRawSync} from 'node:zlib';
import {fileURLToPath} from 'node:url';

const README = "# 設計實作資料包\n\n繁體中文（台灣用語，zh-TW）。版本：2026-10-20。\n\n1. 選擇一個品牌資料夾，將 DESIGN.md 與 PROMPTS.md 交給 AI。\n2. 在指令中填入自己的產品、內容、功能及資料；沒有照片時選擇規格的無圖版。\n3. 檢查 390、768、1440px 與主要操作，依結果調整，不把單次生成視為完成驗收。\n\nDESIGN.md 已含完整角色色碼、字級、間距、元件狀態、響應式條件、素材替代方式與可直接採用的 CSS，不依賴未附上的延伸規格。starter.css 與 TOKENS.json 是同版本的樣式與機器可讀數值；ASSETS.md、ASSETS.json 列出自有素材需求與缺少時的作法。單一品牌 ZIP 的檔案直接放在根目錄。每個 ZIP 均附 LICENSE 與 ATTRIBUTION.md，保留授權與來源說明。\n\n規格明確區分來源宣告與實作建議值，不保證與原官網像素相同。品牌圖片、商標、專有字型與後端未附，但不使用外部素材也能依規格做出文字版原型。請勿將建議素材路徑當成已存在檔案。\n\nSOURCES.json 記錄原參考日期、預覽摘要與實作版本，線上路徑以 https://webdesign.zero2codex.dev/ 為基準。歷史生成及比對紀錄另保留於網站開發紀錄，AI 指令不依賴它們。\n";

function crc32(bytes) {
  let value = 0xffffffff;
  for (const byte of bytes) {
    value ^= byte;
    for (let bit = 0; bit < 8; bit++) value = (value >>> 1) ^ ((value & 1) ? 0xedb88320 : 0);
  }
  return (value ^ 0xffffffff) >>> 0;
}

export function writeStudyPack(output, studies) {
  const entries = [], sources = [];
  const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
  const notices = ['LICENSE', 'ATTRIBUTION.md'].map(name => [name, fs.readFileSync(path.join(root,name))]);
  for (const study of [...studies].sort((a,b)=>a.slug<b.slug?-1:a.slug>b.slug?1:0)) {
    if (!/^[a-z0-9.-]+$/.test(study.slug)) throw new Error('Unsafe study pack name');
    const brandEntries = [];
    for (const [kind,name] of [['analysis','DESIGN.md'],['prompts','PROMPTS.md']]) {
      const source = study.study[kind];
      if (!/^official-drafts\/[a-z0-9.-]+\.md$/.test(source || '')) throw new Error('Study pack requires a current '+kind+': '+study.slug);
      const data = fs.readFileSync(path.join(output,source));
      entries.push([study.slug+'/'+name,data]);
      brandEntries.push([name,data]);
    }
    for (const [name,file] of Object.entries(study.implementation_files || {}).sort(([a],[b])=>a<b?-1:a>b?1:0)) {
      if (!['ASSETS.json','ASSETS.md','TOKENS.json','starter.css'].includes(name) || file.path !== `implementation/${study.slug}/${name}`) throw new Error('Unsafe study pack companion');
      const data = fs.readFileSync(path.join(output,file.path));
      if (createHash('sha256').update(data).digest('hex') !== file.sha256) throw new Error('Study pack companion hash mismatch');
      entries.push([study.slug+'/'+name,data]);
      brandEntries.push([name,data]);
    }
    const sourceRow = {slug:study.slug,date:study.date,preview:study.preview,preview_sha256:study.preview_sha256,
      analysis:study.study.analysis,prompts:study.study.prompts,review:study.study.review || null};
    if (study.implementation_files) {
      Object.assign(sourceRow,{implementation_version:study.implementation_version,reference_url:study.reference_url,implementation_files:study.implementation_files});
      const pack = path.join(output,'assets/design-packs',study.slug+'.zip');
      fs.mkdirSync(path.dirname(pack),{recursive:true});
      writeZip(pack,[...brandEntries,['README.md',Buffer.from(README)],['SOURCES.json',Buffer.from(JSON.stringify([sourceRow])+'\n')],...notices]);
      study.implementation_pack = 'assets/design-packs/'+study.slug+'.zip';
    }
    sources.push(sourceRow);
  }
  entries.push(['README.md',Buffer.from(README)],['SOURCES.json',Buffer.from(JSON.stringify(sources)+'\n')],...notices);
  writeZip(path.join(output,'assets/design-references.zip'),entries);
}

function writeZip(outputFile, entries) {
  const files=[], directory=[];
  let offset=0;
  for (const [name,data] of entries) {
    const filename=Buffer.from(name), crc=crc32(data), compressed=deflateRawSync(data,{level:6});
    const local=Buffer.alloc(30);
    local.writeUInt32LE(0x04034b50,0);local.writeUInt16LE(20,4);local.writeUInt16LE(33,12);
    local.writeUInt16LE(8,8);local.writeUInt32LE(crc,14);local.writeUInt32LE(compressed.length,18);local.writeUInt32LE(data.length,22);local.writeUInt16LE(filename.length,26);
    const central=Buffer.alloc(46);
    central.writeUInt32LE(0x02014b50,0);central.writeUInt16LE(788,4);central.writeUInt16LE(20,6);central.writeUInt16LE(33,14);
    central.writeUInt16LE(8,10);central.writeUInt32LE(crc,16);central.writeUInt32LE(compressed.length,20);central.writeUInt32LE(data.length,24);central.writeUInt16LE(filename.length,28);
    central.writeUInt32LE(0o100644*65536,38);central.writeUInt32LE(offset,42);
    files.push(local,filename,compressed);directory.push(central,filename);offset+=local.length+filename.length+compressed.length;
  }
  const central=Buffer.concat(directory), end=Buffer.alloc(22);
  end.writeUInt32LE(0x06054b50,0);end.writeUInt16LE(entries.length,8);end.writeUInt16LE(entries.length,10);
  end.writeUInt32LE(central.length,12);end.writeUInt32LE(offset,16);
  fs.writeFileSync(outputFile,Buffer.concat([...files,central,end]));
}
