import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const media = new Set(['.mp4','.webm','.png','.jpg','.jpeg','.webp','.avif','.gif','.svg','.woff','.woff2','.ttf','.otf']);
const text = new Set(['.html','.css','.js','.mjs','.json']);
const hash = data => crypto.createHash('sha256').update(data).digest('hex');
function files(directory) {
  return fs.readdirSync(directory,{withFileTypes:true}).flatMap(entry=>{
    const file=path.join(directory,entry.name);
    return entry.isDirectory()?files(file):[file];
  });
}
function validatedMedia(sourceRoot,output,config) {
  const selected=[],seen=new Set();
  for(const asset of config.assets) {
    const name=asset.path;
    if(path.isAbsolute(name)||name.split('/').some(x=>!x||x==='.'||x==='..')||name.includes('\\')||!media.has(path.extname(name).toLowerCase())||seen.has(name)) throw new Error('Invalid hosted media path: '+name);
    seen.add(name);
    const source=path.join(sourceRoot,name),relative=path.relative(fs.realpathSync(sourceRoot),fs.realpathSync(source));
    if(relative==='..'||relative.startsWith('../')||path.isAbsolute(relative)) throw new Error('Media leaves the source directory');
    const data=fs.readFileSync(source);
    if(data.length!==asset.bytes||hash(data)!==asset.sha256) throw new Error('Hosted original media changed: '+name);
    const staged=path.join(output,name);
    if(!fs.existsSync(staged)) continue;
    if(hash(fs.readFileSync(staged))!==asset.sha256) throw new Error('Staged media differs: '+name);
    selected.push({name,file:staged,bytes:asset.bytes});
  }
  return selected;
}

export function compactCatalogMedia(root,output,catalog) {
  const configPath=path.join(root,'data/hosting-assets.json'),config=JSON.parse(fs.readFileSync(configPath,'utf8'));
  if(!/^https:\/\/raw\.githubusercontent\.com\/[^/]+\/[^/]+\/[a-f0-9]{40}\/$/.test(config.image_base_url)) throw new Error('Catalog media requires an immutable GitHub commit');
  const expected=catalog.designs.filter(x=>x.preview.status==='generated').flatMap(x=>[x.preview.image,x.preview.thumbnail]).sort();
  if(JSON.stringify(expected)!==JSON.stringify(config.assets.map(x=>x.path).sort())) throw new Error('Catalog media allowlist differs from the published collection');
  const selected=validatedMedia(root,output,config);
  for(const {file} of selected) fs.unlinkSync(file);
  fs.copyFileSync(configPath,path.join(output,'assets/catalog-media-hosting.json'));
}

export function compactHostedMedia(root,output) {
  const configPath=path.join(root,'data/hosted-official-media.json'),config=JSON.parse(fs.readFileSync(configPath,'utf8'));
  const match=config.base_url.match(/^https:\/\/raw\.githubusercontent\.com\/[^/]+\/[^/]+\/([a-f0-9]{40})\/\.stitch-work\/current-official\/$/);
  if(!match||match[1]!==config.source_commit) throw new Error('Official media requires an immutable GitHub commit');
  const work=path.join(root,'.stitch-work/current-official'),drafts=path.join(output,'official-drafts');
  const selected=validatedMedia(work,drafts,config),proof={};
  for(const file of files(drafts).sort()) {
    if(!text.has(path.extname(file).toLowerCase())) continue;
    const relative=path.relative(drafts,file).split(path.sep).join('/'),original=fs.readFileSync(file);
    if(!original.equals(fs.readFileSync(path.join(work,relative)))) throw new Error('Staged text differs from preserved source: '+relative);
    proof[relative]={source_sha256:hash(original),published_sha256:hash(original),replacements:[]};
  }
  for(const {file} of selected) fs.unlinkSync(file);
  fs.rmSync(path.join(output,'_redirects'),{force:true});
  fs.copyFileSync(configPath,path.join(output,'assets/official-media-hosting.json'));
  fs.writeFileSync(path.join(output,'assets/official-media-publication.json'),JSON.stringify({transport:'same_origin_immutable_proxy',source_commit:config.source_commit,files:proof})+'\n');
  const studiesPath=path.join(output,'assets/official-studies.json');
  if(fs.existsSync(studiesPath)) {
    const studies=JSON.parse(fs.readFileSync(studiesPath,'utf8'));
    studies.media_publication='assets/official-media-publication.json';
    for(const study of studies.studies) study.published_preview_sha256=hash(fs.readFileSync(path.join(output,study.preview)));
    fs.writeFileSync(studiesPath,JSON.stringify(studies)+'\n');
  }
  const total=files(output).reduce((sum,file)=>sum+fs.statSync(file).size,0);
  if(total>config.max_bundle_bytes) throw new Error('Static deployment exceeds its uploadable size budget');
  return {hosted_media_count:selected.length,hosted_media_bytes:selected.reduce((sum,x)=>sum+x.bytes,0),bundled_static_bytes:total,transported_reference_count:0};
}
