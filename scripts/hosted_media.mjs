import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const media = new Set(['.mp4','.webm','.png','.jpg','.jpeg','.webp','.avif','.gif','.woff','.woff2','.ttf','.otf']);
const text = new Set(['.html','.css','.js','.mjs','.json']);
const hash = data => crypto.createHash('sha256').update(data).digest('hex');
const encode = name => name.split('/').map(encodeURIComponent).join('/').replace(/[!'()*]/g,c=>'%' + c.charCodeAt(0).toString(16).toUpperCase());
function files(directory) {
  return fs.readdirSync(directory,{withFileTypes:true}).flatMap(entry=>{
    const file=path.join(directory,entry.name);
    return entry.isDirectory()?files(file):[file];
  });
}
function references(names,parent,base) {
  if(!names.length) return {values:new Map(),pattern:/(?!)/g};
  const values=new Map();
  for(const name of names) {
    const relative=path.posix.relative(parent||'.',name);
    const variants=new Set([relative,encode(relative),'/official-drafts/'+encode(name)]);
    if(!relative.startsWith('../')) for(const value of [...variants]) if(!value.startsWith('/')) variants.add('./'+value);
    const target=base+encode(name);
    for(const value of variants) {
      values.set(value,[target,name]);
      if(value.includes('/')) values.set(value.replaceAll('/','\\/'),[target.replaceAll('/','\\/'),name]);
    }
  }
  return {values,pattern:/(?<![A-Za-z0-9_./:\-])(?:\\?\/)?[A-Za-z0-9_.%\-]+(?:(?:\\?\/)[A-Za-z0-9_.%\-]+)*(?=$|[?#&\s"'<>()\\,;])/g};
}

export function compactHostedMedia(root,output) {
  const configPath=path.join(root,'data/hosted-official-media.json');
  const config=JSON.parse(fs.readFileSync(configPath,'utf8'));
  const match=config.base_url.match(/^https:\/\/raw\.githubusercontent\.com\/[^/]+\/[^/]+\/([a-f0-9]{40})\/\.stitch-work\/current-official\/$/);
  if(!match||match[1]!==config.source_commit) throw new Error('Official media requires an immutable GitHub commit');
  const work=path.join(root,'.stitch-work/current-official'),selected=[],seen=new Set();
  for(const asset of config.assets) {
    const name=asset.path;
    if(path.isAbsolute(name)||name.split('/').includes('..')||name.includes('\\')||!media.has(path.extname(name).toLowerCase())||seen.has(name)) throw new Error('Invalid hosted media path: '+name);
    seen.add(name);
    const source=path.join(work,name),relative=path.relative(fs.realpathSync(work),fs.realpathSync(source));
    if(relative==='..'||relative.startsWith('../')||path.isAbsolute(relative)) throw new Error('Media leaves the source directory');
    const data=fs.readFileSync(source);
    if(data.length!==asset.bytes||hash(data)!==asset.sha256) throw new Error('Hosted original media changed: '+name);
    const staged=path.join(output,'official-drafts',name);
    if(!fs.existsSync(staged)) continue;
    if(hash(fs.readFileSync(staged))!==asset.sha256) throw new Error('Staged media differs: '+name);
    selected.push({name,file:staged,bytes:asset.bytes});
  }
  const drafts=path.join(output,'official-drafts'),names=selected.map(x=>x.name),cache=new Map(),pending=[],proof={};
  for(const file of files(drafts).sort()) {
    if(!text.has(path.extname(file).toLowerCase())) continue;
    const relative=path.relative(drafts,file).split(path.sep).join('/'),parent=path.posix.dirname(relative)==='.'?'':path.posix.dirname(relative);
    if(!cache.has(parent)) cache.set(parent,references(names,parent,config.base_url));
    const {values,pattern}=cache.get(parent),original=fs.readFileSync(file),latin=original.toString('latin1');
    const matches=[];
    for(const found of latin.matchAll(pattern)) if(values.has(found[0])) matches.push(found);
    if(!matches.length) continue;
    if(!original.equals(fs.readFileSync(path.join(work,relative)))) throw new Error('Staged text differs from preserved source: '+relative);
    const chunks=[],records=[];let cursor=0;
    for(const found of matches) {
      const [replacement,assetName]=values.get(found[0]),start=found.index,end=start+found[0].length;
      chunks.push(original.subarray(cursor,start),Buffer.from(replacement));
      records.push([start,end,found[0],assetName]);cursor=end;
    }
    chunks.push(original.subarray(cursor));
    const published=Buffer.concat(chunks);
    proof[relative]={source_sha256:hash(original),published_sha256:hash(published),replacements:records};
    pending.push({file,data:published});
  }
  for(const {file,data} of pending) fs.writeFileSync(file,data);
  for(const {file} of selected) fs.unlinkSync(file);
  fs.rmSync(path.join(output,'_redirects'),{force:true});
  fs.copyFileSync(configPath,path.join(output,'assets/official-media-hosting.json'));
  fs.writeFileSync(path.join(output,'assets/official-media-publication.json'),JSON.stringify({transport:'absolute_immutable_urls',source_commit:config.source_commit,files:proof})+'\n');
  const studiesPath=path.join(output,'assets/official-studies.json');
  if(fs.existsSync(studiesPath)) {
    const studies=JSON.parse(fs.readFileSync(studiesPath,'utf8'));
    studies.media_publication='assets/official-media-publication.json';
    for(const study of studies.studies) study.published_preview_sha256=hash(fs.readFileSync(path.join(output,study.preview)));
    fs.writeFileSync(studiesPath,JSON.stringify(studies)+'\n');
  }
  const total=files(output).reduce((sum,file)=>sum+fs.statSync(file).size,0);
  if(total>config.max_bundle_bytes) throw new Error('Static deployment exceeds its uploadable size budget');
  return {hosted_media_count:selected.length,hosted_media_bytes:selected.reduce((sum,x)=>sum+x.bytes,0),bundled_static_bytes:total,transported_reference_count:Object.values(proof).reduce((n,p)=>n+p.replacements.length,0)};
}
