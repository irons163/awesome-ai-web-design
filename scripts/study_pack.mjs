// Deterministic, dependency-free ZIP of the same public study documents.
import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {deflateRawSync} from 'node:zlib';
import {fileURLToPath} from 'node:url';

const usage = JSON.parse(fs.readFileSync(new URL('../data/usage.json', import.meta.url), 'utf8'));

const COMMON_USAGE = "## 把這段貼給 AI\n\n請先完成上面的檔案放置，再將下方指令貼到能讀取專案檔案的 AI 開發工具，並填入自己的需求。\n\n```text\n" + usage.start_prompt + "\n```\n\n## 檔案怎麼分工\n\n- `DESIGN.md`：畫面與互動規格，包含色彩、字級、間距、元件、響應式規則與必要 CSS；不依賴未附上的延伸規格。\n- `PROMPTS.md`：與這份設計搭配的 AI 實作指令。上方的開工指令會請 AI 一起讀取這兩份文件。\n- `starter.css`、`TOKENS.json`：同版本的樣式與設計數值，依專案需要使用。\n- `ASSETS.md`、`ASSETS.json`：素材需求與缺少圖片時的無圖版做法。建議路徑不代表檔案已存在。\n- `README.md`、`SOURCES.json`：使用說明與來源紀錄。\n- `LICENSE`、`ATTRIBUTION.md`：授權與來源聲明，請一併保留。\n\n請使用自己的產品名稱、內容與素材。這份資料用於建立前端介面，實際功能仍需依需求完成並測試；品牌圖片、商標、專有字型與後端服務未附。\n\n規格版本：2026-10-20。使用說明更新：" + usage.updated + "。參考日期與來源以 SOURCES.json 為準；線上路徑以 https://webdesign.zero2codex.dev/ 為基準。\n";
const BRAND_STEPS = "這個 ZIP 已包含設計規格、AI 指令與補充檔案，不需要再分別下載。\n\n## 照這三步開始\n\n1. 解壓縮這個 ZIP；你會在同一層看到 `DESIGN.md` 與 `PROMPTS.md`。\n2. 在你的專案建立 `design-reference/` 資料夾，把解壓後的全部檔案放進去。\n3. 在 Codex、Claude Code、Cursor 等能讀取專案檔案的工具中貼上下方指令，填入產品與功能需求。\n\n";
const COLLECTION_STEPS = "這是批次收藏用的合集。先選一個品牌資料夾，使用一套設計開始製作。\n\n## 照這三步開始\n\n1. 解壓縮合集，選一個你喜歡的品牌資料夾；每個資料夾都有 `DESIGN.md` 與 `PROMPTS.md`。\n2. 在你的專案建立 `design-reference/`，把選定品牌資料夾內的檔案放進去，並保留合集根目錄的 `LICENSE` 與 `ATTRIBUTION.md`。\n3. 在能讀取專案檔案的 AI 開發工具中貼上下方指令，填入自己的產品與功能需求。\n\n如果只需要一套設計，也可以回到網站下載該品牌的設計包，使用相同的三個步驟。\n\n";

function brandReadme(study) {
  return '# '+(study.name || study.slug)+' 設計包\n\n繁體中文（台灣用語，zh-TW）。\n\n'+BRAND_STEPS+COMMON_USAGE;
}
function collectionReadme(count) {
  return '# '+count+' 套設計合集\n\n繁體中文（台灣用語，zh-TW）。\n\n'+COLLECTION_STEPS+COMMON_USAGE;
}

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
    const simplePack = path.join(output,'assets/design-packs',study.slug+'-simple.zip');
    fs.mkdirSync(path.dirname(simplePack),{recursive:true});
    // Keep the two core documents unchanged; retain the notices in ZIP metadata.
    const notice = Buffer.concat([Buffer.from('LICENSE\n'),notices.find(([name])=>name==='LICENSE')[1],Buffer.from('\n\n'+usage.simple_pack_attribution)]);
    writeZip(simplePack,[...brandEntries],notice);
    study.simple_pack = 'assets/design-packs/'+study.slug+'-simple.zip';
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
      writeZip(pack,[...brandEntries,['README.md',Buffer.from(brandReadme(study))],['SOURCES.json',Buffer.from(JSON.stringify([sourceRow])+'\n')],...notices]);
      study.implementation_pack = 'assets/design-packs/'+study.slug+'.zip';
    }
    sources.push(sourceRow);
  }
  entries.push(['README.md',Buffer.from(collectionReadme(studies.length))],['SOURCES.json',Buffer.from(JSON.stringify(sources)+'\n')],...notices);
  writeZip(path.join(output,'assets/design-references.zip'),entries);
}

function writeZip(outputFile, entries, comment=Buffer.alloc(0)) {
  if(comment.length>65535) throw new Error('ZIP notice is too long');
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
  end.writeUInt16LE(comment.length,20);
  fs.writeFileSync(outputFile,Buffer.concat([...files,central,end,comment]));
}
