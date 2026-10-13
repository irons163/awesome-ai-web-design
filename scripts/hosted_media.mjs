import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const media = new Set(['.mp4','.webm','.png','.jpg','.jpeg','.webp','.avif','.gif','.woff','.woff2','.ttf','.otf']);
const hash = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const encode = name => name.split('/').map(encodeURIComponent).join('/').replace(/[!'()*]/g, c => '%' + c.charCodeAt(0).toString(16).toUpperCase());
function bytes(directory) {
  return fs.readdirSync(directory, {withFileTypes:true}).reduce((sum, entry) => {
    const file=path.join(directory,entry.name);
    return sum + (entry.isDirectory() ? bytes(file) : fs.statSync(file).size);
  },0);
}

export function compactHostedMedia(root, output) {
  const configPath=path.join(root,'data/hosted-official-media.json');
  const config=JSON.parse(fs.readFileSync(configPath,'utf8'));
  const match=config.base_url.match(/^https:\/\/raw\.githubusercontent\.com\/[^/]+\/[^/]+\/([a-f0-9]{40})\/\.stitch-work\/current-official\/$/);
  if(!match || match[1]!==config.source_commit) throw new Error('Official media requires an immutable GitHub commit');
  const work=path.join(root,'.stitch-work/current-official');
  const selected=[], seen=new Set();
  for(const asset of config.assets) {
    const name=asset.path;
    if(path.isAbsolute(name)||name.split('/').includes('..')||name.includes('\\')||!media.has(path.extname(name).toLowerCase())||seen.has(name)) throw new Error('Invalid hosted media path: '+name);
    seen.add(name);
    const source=path.join(work,name), relative=path.relative(fs.realpathSync(work),fs.realpathSync(source));
    if(relative==='..'||relative.startsWith('../')||path.isAbsolute(relative)) throw new Error('Media leaves the source directory');
    if(fs.statSync(source).size!==asset.bytes||hash(source)!==asset.sha256) throw new Error('Hosted original media changed: '+name);
    const staged=path.join(output,'official-drafts',name);
    if(!fs.existsSync(staged)) continue;
    if(hash(staged)!==asset.sha256) throw new Error('Staged media differs: '+name);
    const rule='/official-drafts/'+encode(name)+' '+config.base_url+encode(name)+' 302';
    if(rule.length>1000) throw new Error('Media redirect exceeds the hosting limit');
    selected.push({file:staged,rule,bytes:asset.bytes});
  }
  if(selected.length>2000) throw new Error('Too many static media redirects');
  for(const asset of selected) fs.unlinkSync(asset.file);
  fs.writeFileSync(path.join(output,'_redirects'),selected.map(x=>x.rule).sort().join('\n')+'\n');
  fs.copyFileSync(configPath,path.join(output,'assets/official-media-hosting.json'));
  const total=bytes(output);
  if(total>config.max_bundle_bytes) throw new Error('Static deployment exceeds its uploadable size budget');
  return {hosted_media_count:selected.length,hosted_media_bytes:selected.reduce((sum,x)=>sum+x.bytes,0),bundled_static_bytes:total};
}
