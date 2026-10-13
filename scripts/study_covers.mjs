import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
const digest=file=>crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
function inside(root,relative){const file=fs.realpathSync(path.resolve(root,relative));if(!file.startsWith(fs.realpathSync(root)+path.sep))throw new Error('Unsafe cover evidence path');return file;}
export function coversFor(root,catalog){
  const manifest=JSON.parse(fs.readFileSync(path.join(root,'data/study-covers.json'),'utf8'));
  const covers=new Map(manifest.covers.map(row=>[row.slug,row]));
  if(covers.size!==manifest.covers.length||covers.size!==catalog.length||catalog.some(row=>!covers.has(row.slug)))throw new Error('Current cover inventory differs from catalog');
  return covers;
}
export function coverFor(root,record,brand,current){
  if(record.brand!==brand||record.preview_sha256!==current)throw new Error('Stale current-study cover: '+brand);
  const work=path.join(root,'.stitch-work/current-official');
  for(const key of ['source','result'])if(digest(inside(work,record[key].path))!==record[key].sha256)throw new Error('Changed cover evidence: '+brand);
  const image=record.image,file=inside(path.join(root,'assets/current-previews'),path.relative('assets/current-previews',image.path));
  if(digest(file)!==image.sha256||fs.statSync(file).size!==image.bytes)throw new Error('Changed cover image: '+brand);
  return {src:image.path,width:image.width,height:image.height,sha256:image.sha256,preview_sha256:current};
}
