import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const capture=path.resolve(process.argv[2]||'/private/tmp/official-browser-oct9');
const output=path.resolve('.stitch-work/current-official');
const read=file=>JSON.parse(fs.readFileSync(file,'utf8'));
const sha=bytes=>crypto.createHash('sha256').update(bytes).digest('hex');
const text=value=>value.replace(/\s+/g,' ').trim().toLowerCase();

function compare(reference,local){
  if(reference.viewport.width!==local.viewport.width||reference.viewport.height!==local.viewport.height)throw new Error('Wrong comparison viewport');
  const differences=[],fonts=[],positions=[];
  let matchingText=0;
  reference.headings.forEach((a,index)=>{
    const b=local.headings[index];
    if(!b||text(a.text)!==text(b.text)){differences.push({index,text:a.text,reason:'text/order'});return;}
    matchingText++;
    if(!a.box.width||!a.box.height)return;
    const delta=Object.fromEntries(['x','y','width','height'].map(key=>[key,b.box[key]-a.box[key]]));
    const fontMatches=['font','size','weight','lineHeight'].every(key=>a.style[key]===b.style[key]);
    positions.push({index,text:a.text,delta});
    if(!fontMatches)fonts.push({index,text:a.text,reference:a.style,local:b.style});
    if(Object.values(delta).some(value=>Math.abs(value)>.01))differences.push({index,text:a.text,delta});
  });
  return {viewport:local.viewport,reference_observed_at:reference.observed_at,local_observed_at:local.observed_at,
    document:{reference:{height:reference.bodyHeight,width:reference.bodyWidth},local:{height:local.bodyHeight,width:local.bodyWidth},matches:reference.bodyHeight===local.bodyHeight&&reference.bodyWidth===local.bodyWidth},
    source_headings:reference.headings.length,local_headings:local.headings.length,normalized_text_matches:matchingText,
    measured_headings:positions.length,positions,font_differences:fonts,differences,
    limitation:'Rectangles and computed fonts are dated DOM measurements. Zero-size headings are omitted from geometry checks. This is not full-page pixel or interaction acceptance.'};
}

for(const brand of ['pinterest','vodafone']){
  const evidence=[];
  const comparisons={};
  const localRecords={};
  for(const mode of ['desktop','mobile']){
    const localFile=brand+'-local-'+mode+(mode==='mobile'?'-final':'')+'-metrics.json';
    const local=read(path.join(capture,localFile));
    localRecords[mode]=local;
    fs.copyFileSync(path.join(capture,localFile),path.join(output,localFile));
    comparisons[mode]=compare(read(path.join(output,brand+'-'+mode+'-browser-reference.json')),local);
    for(const frame of ['first','full','footer']){
      const file=brand+'-local-'+mode+'-'+frame+'.jpg';
      const source=path.join(capture,file);
      if(!fs.existsSync(source))continue;
      const bytes=fs.readFileSync(source);
      if(bytes[0]!==0xff||bytes[1]!==0xd8)throw new Error('Expected unchanged browser JPEG');
      fs.copyFileSync(source,path.join(output,file));
      evidence.push({path:file,bytes:bytes.length,sha256:sha(bytes),method:'Original local browser screenshot, unchanged; dynamic video frames and animations remain variable.'});
    }
  }
  const interactions=brand==='vodafone'?[
    'Mobile menu opens, Close Device Menu closes, and Escape from a focused menu link closes it and restores inert to the hidden menu.',
    'The actual official everyone.connected vertical submenu and local correction have the same panel and five link rectangles at390×844.',
    'Hero video paused and resumed through its visible control. Only its original icon glyph changes, preserving the source control class and position.',
    'All16 declared lazy source images loaded after traversing the local page; original packaged image bytes remain unchanged.'
  ]:[
    'Desktop View Next moves to the same observed1156px board offset as the official page; original previous-arrow visibility and pointer state update.',
    'View Previous returns to the initial0px offset; final first-state geometry is recorded separately.',
    'Original public Google-button overlay SVG is retained and can route to Pinterest; its live account iframe is excluded and credential inputs are read-only.'
  ];
  const records=brand==='vodafone'?['vodafone-mobile-submenu-reference.json','vodafone-mobile-submenu.jpg','vodafone-local-mobile-submenu.json','vodafone-local-mobile-submenu.jpg','vodafone-local-mobile-menu.jpg']:['pinterest-carousel-reference.json','pinterest-local-carousel.json'];
  for(const file of records){const source=path.join(capture,file);if(!fs.existsSync(source))throw new Error('Missing interaction evidence: '+file);fs.copyFileSync(source,path.join(output,file));}
  const build=read(path.join(output,brand+'-draft-build-record.json'));
  const review={accepted:false,working_draft:build.working_draft,
    method:'Existing browser comparison of genuine Stitch exports separately corrected from dated official source. No additional browser service was installed.',
    comparisons,interactions,interaction_records:records,screenshots:evidence,native_provenance:brand+'-stitch-generated.json',
    asset_provenance:brand+'-browser-asset-provenance.json',remaining:build.limitations,
    public_comparison:'The public Site origin remains unavailable under the saved browser permission. Local comparison and native deployment status do not establish a rendered public-Site match.'};
  if(brand==='pinterest'){
    const raw=read(path.join(capture,'pinterest-desktop-hero.json'));
    const source={reference_url:'https://www.pinterest.com/',observed_date:'2026-10-09',box:raw.box,font:raw.font,size:raw.size,weight:raw.weight,lineHeight:raw.lineHeight,
      method:'Separate public hero inspection during the dated desktop reference capture; exact per-element capture time was not separately retained.'};
    const file='pinterest-desktop-hero-reference.json';
    fs.writeFileSync(path.join(output,file),JSON.stringify(source,null,2)+'\n');
    const local=localRecords.desktop.hero;
    review.hero={reference:file,local,delta:Object.fromEntries(['x','y','width','height'].map(key=>[key,local.box[key]-source.box[key]])),accepted:false};
  }
  fs.writeFileSync(path.join(output,brand+'-review.json'),JSON.stringify(review,null,2)+'\n');
  console.log(JSON.stringify({brand,desktop:comparisons.desktop.document,mobile:comparisons.mobile.document,desktopDifferences:comparisons.desktop.differences.length,mobileDifferences:comparisons.mobile.differences.length,accepted:false}));
}
