import fs from 'node:fs';
import path from 'node:path';
const work=path.resolve('.stitch-work/current-official');
const capture=path.resolve(process.argv[2]||'/private/tmp/official-browser-claude-notion-oct10');
const read=(root,name)=>JSON.parse(fs.readFileSync(path.join(root,name),'utf8'));
const write=(name,value)=>fs.writeFileSync(path.join(work,name),JSON.stringify(value,null,2)+'\n');
const progress=read(work,'progress.json');
const normalize=text=>text.replace(/\s+/g,' ').trim();
function geometry(source,local){const differences=[];for(const key of ['x','y','width','height'])if(Math.abs(source[key]-local[key])>.01)differences.push({property:key,source:source[key],local:local[key]});return differences;}
for(const brand of ['claude','notion']){
  const views={},navigation=[];
  for(const variant of ['desktop','mobile']){
    const referenceName=`${brand}-${variant}-browser-reference.json`,localName=`${brand}-${variant}-local-review.json`;
    const source=read(work,referenceName),local=read(capture,`${brand}-${variant}-local-metrics.json`);
    const sourceHeadings=source.headings.filter(h=>h.box.height>0&&h.box.width>0),localHeadings=local.headings.filter(h=>h.box.height>0&&h.box.width>0);
    const differences=[];
    if(sourceHeadings.length!==localHeadings.length)throw new Error('Heading count differs');
    sourceHeadings.forEach((heading,index)=>{
      const actual=localHeadings[index];
      if(heading.sourceText!==actual.sourceText)differences.push({index,copy:true});
      for(const difference of geometry(heading.box,actual.box))differences.push({index,...difference});
      for(const key of Object.keys(heading.font))if(heading.font[key]!==actual.font[key])differences.push({index,font:key});
    });
    if(local.bodyHeight!==source.bodyHeight||local.bodyWidth!==source.bodyWidth)throw new Error('Body size differs');
    if(differences.length)throw new Error('Measured heading geometry/font differs');
    if(local.images.some(image=>!image.loaded))throw new Error('Original image did not decode');
    write(localName,local);
    fs.copyFileSync(path.join(capture,`${brand}-${variant}-local-first.jpg`),path.join(work,`${brand}-${variant}-local-first.jpg`));
    views[variant]={reference:referenceName,local:localName,source_observed_at:source.observed_at,local_observed_at:local.observed_at,viewport:local.viewport,body:{width:local.bodyWidth,height:local.bodyHeight},heading_layout_records:sourceHeadings.length,visible_heading_text_records:localHeadings.filter(h=>h.text).length,differences,images:{total:local.images.length,loaded:local.images.filter(i=>i.loaded).length}};
  }
  const variants=brand==='claude'?['desktop-product','mobile','mobile-product']:['desktop-product','desktop-resources','mobile','mobile-resources'];
  for(const variant of variants){
    const records={};
    for(const kind of ['official','local']){
      const record=read(capture,`${brand}-${variant}-${kind}-nav-metrics.json`);
      record.links=record.links.map(link=>{const url=new URL(link.href,brand==='claude'?'https://claude.com/index.html':'https://www.notion.com/');for(const key of ['tid','gclid','fbclid','li_fat_id'])url.searchParams.delete(key);return{...link,href:url.href};});
      const name=`${brand}-${variant}-${kind}-navigation-review.json`;write(name,record);records[kind]={file:name,data:record};
      fs.copyFileSync(path.join(capture,`${brand}-${variant}-${kind}-nav.jpg`),path.join(work,`${brand}-${variant}-${kind}-nav.jpg`));
    }
    const source=records.official.data,local=records.local.data,differences=[];
    if(source.links.length!==local.links.length)throw new Error('Navigation link count differs');
    source.links.forEach((link,index)=>{const actual=local.links[index];if(link.text!==actual.text||link.label!==actual.label||link.href!==actual.href)differences.push({index,content:true});for(const difference of geometry(link.box,actual.box))differences.push({index,...difference});});
    if(differences.length)throw new Error('Navigation differs: '+brand+'/'+variant+' '+JSON.stringify(differences));
    navigation.push({variant,source:records.official.file,local:records.local.file,links_checked:source.links.length,differences});
  }
  const interaction={};
  if(brand==='claude'){
    const records={};
    for(const kind of ['official','local']){
      const record=read(capture,`claude-${kind}-interaction-review.json`);
      record.panels=record.panels.map(panel=>({...panel,text:panel.hidden||panel.display==='none'?undefined:panel.text}));
      record.faq=record.faq.map(item=>({...item,content:item.expanded==='true'?item.content:undefined}));
      const name=`claude-${kind}-interaction-review.json`;write(name,record);records[kind]=record;
    }
    if(JSON.stringify(records.official.tabs)!==JSON.stringify(records.local.tabs))throw new Error('Selected plan differs');
    const active=record=>record.panels.filter(panel=>!panel.hidden&&panel.display!=='none').map(panel=>normalize(panel.text));
    if(JSON.stringify(active(records.official))!==JSON.stringify(active(records.local)))throw new Error('Visible plan copy differs');
    records.official.faq.forEach((item,index)=>{const actual=records.local.faq[index];if(item.expanded!==actual.expanded||item.display!==actual.display||(item.expanded==='true'&&normalize(item.content)!==normalize(actual.content)))throw new Error('FAQ state or visible answer differs');});
    interaction.plans_and_faq={source:'claude-official-interaction-review.json',local:'claude-local-interaction-review.json',selected_plan:'Team & Enterprise',first_faq_open:true};
    write('claude-faq-visual-reference.json',read(capture,'claude-faq-visual-state.json'));
  }else{
    const video=read(capture,'notion-local-video-review.json');
    if(!video.paused.paused||video.playing.paused||video.playing.readyState<2)throw new Error('Video controls failed');
    write('notion-local-video-review.json',video);interaction.video={source:'notion-video-controls.json',local:'notion-local-video-review.json',original_video_play_pause:true};
  }
  const native=read(work,brand+'-stitch-oct10-generated.json'),assets=read(work,brand+'-browser-asset-provenance.json');
  const review={accepted:false,full_pixel_acceptance:false,views,navigation,interaction,native_exports:brand+'-stitch-oct10-generated.json',assets:{retained:assets.assets.length,bytes:assets.assets.reduce((sum,a)=>sum+a.bytes,0),native_visual_failures_retained:assets.failures.length},rendered_public_deployment_comparison:'Not performed. The saved public Site-origin browser permission remains denied; native deployment success verifies hosting only.',limitations:brand==='claude'?['Public /index.html is the actual reference because the root redirected to login. The official hero video remained an empty source; no replacement is invented.','Current native MOBILE generation, true phone user agent, full-page pixels, animation timing, remaining menus, quiz, carousel, language/privacy and complete focus/keyboard states remain unaccepted.']:['Rotating wording, marquee and video phases are dated states, not complete motion acceptance.','Current native MOBILE generation, true phone user agent, intermediate widths, full-page pixels, remaining interactions, privacy/language and complete focus/keyboard states remain unaccepted.']};
  write(brand+'-review.json',review);
  const prior=progress[brand];
  progress[brand]={...prior,status:'in_visual_review',accepted:false,previous_native_screen:prior.previous_native_screen||prior.native_screen,previous_reference_observed_at:prior.previous_reference_observed_at||prior.reference_observed_at||prior.observed_at,native_screen:native.screens[0].name,observed_at:new Date(Date.parse(views.desktop.source_observed_at)+8*3600000).toISOString().replace('Z','+08:00'),reference_observed_at:views.desktop.source_observed_at,reference_url:brand==='claude'?'https://claude.com/index.html':'https://www.notion.com/',reference_kind:'sanitized_rendered_public_browser_capture',reference:brand+'-reference.json',reference_record:brand+'-desktop-browser-reference.json',mobile_reference_record:brand+'-mobile-browser-reference.json',generation_record:brand+'-stitch-oct10-generated.json',generation_notes:brand+'-stitch-oct10-generation-notes.md',asset_provenance:brand+'-browser-asset-provenance.json',draft_build_record:brand+'-draft-build-record.json',review:brand+'-review.json',review_note:brand==='claude'?'10 月 10 日公開首頁桌面與390px排版、選單、方案與FAQ已本機比對；主視覺來源空白、動畫及完整視覺驗收仍待確認。':'10 月 10 日官網桌面與390px排版、主選單、Resources子選單及原始影片控制已本機比對；輪替動畫、完整視覺與公開版畫面驗收待完成。',verified:[
    'October10 public desktop1280×720 and narrow390×844 browser DOM/CSS/CSSOM, original vectors, assets and screenshots retained without reading cookies, storage or private account APIs.',
    'One independently prompted genuine DESKTOP Stitch request returned '+native.screens.length+' screen(s); every original HTML/PNG, full response and suggestion remains unchanged. Native PNGs are thumbnails, not full-resolution proof.',
    Object.values(views).reduce((sum,v)=>sum+v.heading_layout_records,0)+' heading layout/font records and both total body dimensions match the dated reference. All '+Object.values(views).reduce((sum,v)=>sum+v.images.total,0)+' local image elements decode.',
    navigation.length+' observed navigation states and '+navigation.reduce((sum,n)=>sum+n.links_checked,0)+' link destinations/boxes match the source; these counts include repeated header links.',
    brand==='claude'?'Selected Team & Enterprise plan and the first expanded FAQ answer match observed official states; the source is-opened accordion class is retained.':'Original public hero video play/pause and actual native control SVG states work locally; observed mobile Resources content is retained.',
    assets.assets.length+' original public visual resource records retain URLs, sizes and SHA-256; native acquisition failures remain recorded separately from successful supplementary downloads or unchanged cached originals.'
  ],remaining:[...review.limitations,'Published Site browser comparison remains unavailable under its saved origin permission; successful hosting is not rendered visual acceptance.']};
  console.log(JSON.stringify({brand,headings:Object.fromEntries(Object.entries(views).map(([key,v])=>[key,v.heading_layout_records])),navigation_states:navigation.length,native_screens:native.screens.length,accepted:false}));
}
write('progress.json',progress);
