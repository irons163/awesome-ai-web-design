import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
const capture=path.resolve(process.argv[2]||'/private/tmp/official-browser-vercel-airbnb-oct10');
const work=path.resolve('.stitch-work/current-official');
const read=(folder,name)=>JSON.parse(fs.readFileSync(path.join(folder,name),'utf8'));
const hash=bytes=>crypto.createHash('sha256').update(bytes).digest('hex');
const equal=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const layoutFields=['text','box','fontFamily','fontSize','fontWeight','lineHeight','letterSpacing','color'];
const headings=[],phaseDimensions=[];
for(const variant of ['desktop','mobile']){
  const source=read(work,'vercel-'+variant+'-scroll-phases.json'),local=read(capture,'vercel-working-'+variant+'-scroll-phases.json');
  if(source.length!==local.length)throw new Error('Scroll traversal incomplete');
  const unique=new Map();
  source.forEach((a,index)=>{
    const b=local[index];if(a.scrollY!==b.scrollY)throw new Error('Different native scroll traversal');
    phaseDimensions.push({variant,phase:index,scroll_y:a.scrollY,source_body_height:a.bodyHeight,working_body_height:b.bodyHeight,equal:a.bodyHeight===b.bodyHeight});
    for(const h of a.headings){const found=b.headings.find(x=>x.text===h.text);if(!found||!layoutFields.every(k=>equal(h[k],found[k])))throw new Error('Heading layout differs: '+variant+': '+h.text);unique.set(h.text,h);}
  });
  for(const h of unique.values())headings.push({variant,...h});
  if(source.at(-1).bodyHeight!==local.at(-1).bodyHeight)throw new Error('Settled page dimensions differ');
  fs.copyFileSync(path.join(capture,'vercel-working-'+variant+'-scroll-phases.json'),path.join(work,'vercel-working-'+variant+'-scroll-phases.json'));
}
const nav=[];
for(const [localName,sourceName]of [['desktop-products','desktop-products-menu'],['desktop-resources','desktop-resources-menu'],['mobile-menu','mobile-menu'],['mobile-products-menu','mobile-products-menu'],['mobile-resources-menu','mobile-resources-menu']]){
  const source=read(work,'vercel-'+sourceName+'-browser-reference.json');
  const local=read(capture,'vercel-working-'+localName+'-links.json');
  if(!local.open)throw new Error('Menu did not open');
  const links=local.links.filter(l=>l.text);
  for(const link of links)if(!source.links.some(s=>['href','text','box','fontFamily','fontSize','fontWeight','lineHeight','letterSpacing'].every(k=>equal(s[k],link[k]))))throw new Error('Menu link differs: '+localName+': '+link.text);
  nav.push({state:sourceName,links:links.length,source_observed_at:source.observed_at,source_html_sha256:source.html_sha256});
  fs.copyFileSync(path.join(capture,'vercel-working-'+localName+'-links.json'),path.join(work,'vercel-working-'+localName+'-links.json'));
}
const closed=read(capture,'vercel-working-mobile-closed-links.json');if(closed.open||closed.mainInert)throw new Error('Closing the mobile menu left the page inert');
const screenshots=[];
for(const state of ['desktop','mobile','desktop-products-menu','desktop-resources-menu','mobile-menu','mobile-products-menu','mobile-resources-menu']){
  const name='vercel-working-'+state+'-first.jpg',bytes=fs.readFileSync(path.join(capture,name));fs.writeFileSync(path.join(work,name),bytes);
  screenshots.push({path:name,bytes:bytes.length,sha256:hash(bytes),method:'Original local working-study browser capture, unchanged. Not a public deployment screenshot.'});
}
const assets=read(work,'vercel-browser-asset-provenance.json');
const record={accepted:false,observed_at:new Date().toISOString(),viewports:[{width:1280,height:720},{width:390,height:844}],heading_records:headings,heading_count:headings.length,navigation_states:nav,navigation_link_count:nav.reduce((n,s)=>n+s.links,0),phase_dimensions:phaseDimensions,screenshots,asset_records:assets.assets.length,asset_bytes:assets.assets.reduce((n,a)=>n+a.bytes,0),checks:['All visible heading text, typography and boxes match after the same native scroll traversal.','All compared navigation destination, text, font and box records match.','Native details/summary accordion switches Products/Resources and the mobile menu closes without leaving main inert.','Settled desktop and narrow body heights match at5654px and6671px.'],limitations:['The desktop official source had already cached content-visibility intrinsic sizes. The new local page initially has a smaller height; every recorded visible heading matches, and settled dimensions converge after traversal. This is not an initial document-height match.','Only the original official static hero fallback is reproduced; live WebGL pixels and animation remain unaccepted.','Narrow captures use a desktop user agent. True phones, tablet, all hover/focus and advanced interactions require further review.','Account/AI/agent/cookie workflows delegate to the official service.','Full-page pixel and rendered production acceptance remain pending. Saved browser preferences block the Site origin and Airbnb.ca; no alternate-origin or connector bypass was attempted.']};
fs.writeFileSync(path.join(work,'vercel-visual-review.json'),JSON.stringify(record,null,2)+'\n');
fs.writeFileSync(path.join(work,'vercel-visual-review.md'),'# Vercel — October10 public-source study\n\nStatus: unfinished, unofficial and free. Full visual acceptance: **false**.\n\n'+headings.length+' unique heading layout/font records across1280×720 and390×844 and '+record.navigation_link_count+' link records across five actual menu states match the dated public source after the same scroll traversal. Settled body heights are5654px and6671px. Source and working screenshots are separately labeled and retain original bytes.\n\n'+record.limitations.map(s=>'- '+s).join('\n')+'\n\nGenuine Stitch requests, original exports and complete provider text/suggestions are preserved separately. Generation claims are not acceptance results.\n');
const progress=read(work,'progress.json');progress.vercel.verified=record.checks;progress.vercel.review='vercel-visual-review.md';progress.vercel.accepted=false;
fs.writeFileSync(path.join(work,'progress.json'),JSON.stringify(progress,null,2)+'\n');
console.log(JSON.stringify({headings:headings.length,links:record.navigation_link_count,assets:record.asset_records,accepted:false}));
