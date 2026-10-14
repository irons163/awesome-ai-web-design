// Deterministic, dependency-free ZIP of the same public study documents.
import fs from 'node:fs';
import path from 'node:path';

const README = '# 設計參考資料包\n\n每個品牌資料夾的 DESIGN.md 與 PROMPTS.md，對應網站主要分頁的設計分析與 AI 指令。\n\n各份參考日期與線上預覽路徑列於 SOURCES.json；相對路徑以網站根目錄為準。這個資料包提供 Markdown 規格，不包含完整預覽的圖片、字型或外部服務。\n\n原始 74 份分析、222 則任務指令與 AI 初稿仍保留於網站製作紀錄。已知差異依各品牌紀錄判讀。\n';

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
  for (const study of [...studies].sort((a,b)=>a.slug<b.slug?-1:a.slug>b.slug?1:0)) {
    if (!/^[a-z0-9.-]+$/.test(study.slug)) throw new Error('Unsafe study pack name');
    for (const [kind,name] of [['analysis','DESIGN.md'],['prompts','PROMPTS.md']]) {
      const source = study.study[kind];
      if (!/^official-drafts\/[a-z0-9.-]+\.md$/.test(source || '')) throw new Error('Study pack requires a current '+kind+': '+study.slug);
      entries.push([study.slug+'/'+name, fs.readFileSync(path.join(output,source))]);
    }
    sources.push({slug:study.slug,date:study.date,preview:study.preview,preview_sha256:study.preview_sha256,
      analysis:study.study.analysis,prompts:study.study.prompts,review:study.study.review || null});
  }
  entries.push(['README.md',Buffer.from(README)],['SOURCES.json',Buffer.from(JSON.stringify(sources)+'\n')]);
  const files=[], directory=[];
  let offset=0;
  for (const [name,data] of entries) {
    const filename=Buffer.from(name), crc=crc32(data);
    const local=Buffer.alloc(30);
    local.writeUInt32LE(0x04034b50,0);local.writeUInt16LE(20,4);local.writeUInt16LE(33,12);
    local.writeUInt32LE(crc,14);local.writeUInt32LE(data.length,18);local.writeUInt32LE(data.length,22);local.writeUInt16LE(filename.length,26);
    const central=Buffer.alloc(46);
    central.writeUInt32LE(0x02014b50,0);central.writeUInt16LE(788,4);central.writeUInt16LE(20,6);central.writeUInt16LE(33,14);
    central.writeUInt32LE(crc,16);central.writeUInt32LE(data.length,20);central.writeUInt32LE(data.length,24);central.writeUInt16LE(filename.length,28);
    central.writeUInt32LE(0o100644*65536,38);central.writeUInt32LE(offset,42);
    files.push(local,filename,data);directory.push(central,filename);offset+=local.length+filename.length+data.length;
  }
  const central=Buffer.concat(directory), end=Buffer.alloc(22);
  end.writeUInt32LE(0x06054b50,0);end.writeUInt16LE(entries.length,8);end.writeUInt16LE(entries.length,10);
  end.writeUInt32LE(central.length,12);end.writeUInt32LE(offset,16);
  fs.writeFileSync(path.join(output,'assets/design-references.zip'),Buffer.concat([...files,central,end]));
}
