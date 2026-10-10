import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
const work=path.resolve('.stitch-work/current-official');
const read=name=>JSON.parse(fs.readFileSync(path.join(work,name),'utf8'));
const hash=bytes=>crypto.createHash('sha256').update(bytes).digest('hex');
function unpack(response,field){
  if(response.structuredContent?.[field])return response.structuredContent;
  for(const c of response.content||[])if(c.type==='text'){try{const v=JSON.parse(c.text);if(v[field])return v;}catch{}}
  throw new Error('Missing genuine native response');
}
const response='vercel-stitch-oct10-mobile-response.json',generation=unpack(read(response),'outputComponents');
const generated=generation.outputComponents.flatMap(c=>c.design?.screens||[]);if(!generated.length)throw new Error('No genuine mobile-request UI');
const screens=generated.map((g,index)=>{
  const screenResponse='vercel-stitch-oct10-mobile-screen-'+index+'-response.json',s=unpack(read(screenResponse),'name');
  if(s.name!==g.name)throw new Error('Screen not returned by this generation');
  const exports=[['html',s.htmlCode],['png',s.screenshot]].map(([extension,file])=>{
    const name='vercel-stitch-oct10-mobile-'+index+'.'+extension,bytes=fs.readFileSync(path.join(work,name));
    if(extension==='html'&&!/<html[\s>]/i.test(bytes.toString()))throw new Error('Invalid original HTML');
    if(extension==='png'&&!bytes.subarray(0,8).equals(Buffer.from([137,80,78,71,13,10,26,10])))throw new Error('Invalid original PNG');
    return {path:name,bytes:bytes.length,sha256:hash(bytes),native_file:file.name,source_url:file.downloadUrl,...(extension==='png'?{actual_image_dimensions:{width:bytes.readUInt32BE(16),height:bytes.readUInt32BE(20)}}:{})};
  });
  return {name:s.name,title:s.title,device:s.deviceType,provider_dimensions:{width:s.width,height:s.height},screen_response:screenResponse,exports};
});
const promptPath='vercel-stitch-oct10-mobile-prompt.md',prompt=fs.readFileSync(path.join(work,promptPath));
const messages=generation.outputComponents.filter(c=>typeof c.text==='string').map(c=>c.text),suggestions=generation.outputComponents.filter(c=>typeof c.suggestion==='string').map(c=>c.suggestion);
const record={accepted:false,project_id:generation.projectId,session_id:generation.sessionId,prompt:{path:promptPath,bytes:prompt.length,sha256:hash(prompt),method:'Independently authored current-source MOBILE-specific request. Upstream AI prompts were not reused.'},response,screens,provider_text:messages,provider_suggestions:suggestions,review_notes:['The request returned one extra DESKTOP resource and one actual MOBILE resource. Both are preserved rather than relabeled.','Provider text lists Charles Schwab and Supreme and describes extra architecture cards; the current observed source instead includes Meta and SpaceXAI and a cycling supporting line. Provider fidelity claims are not accepted. The source-corrected study retains the actual observed source.'],limitation:'Native device metadata is recorded honestly; actual exported image dimensions are separate. Provider fidelity claims are not visual acceptance. Original native exports remain unchanged and separate from the source-corrected working study.'};
fs.writeFileSync(path.join(work,'vercel-stitch-oct10-mobile-generated.json'),JSON.stringify(record,null,2)+'\n');
fs.writeFileSync(path.join(work,'vercel-stitch-oct10-mobile-generation-notes.md'),'# Vercel — genuine mobile-request Stitch output, October10\n\n以下完整保存 Google Stitch 原始回覆與建議。工具所稱「精準」或「忠實」並非驗收結果；原始生成檔與校正稿分開保存。工具額外產生一個桌面資源及一個真正 MOBILE 資源，兩者皆原樣保留。其回覆提到的 Charles Schwab、Supreme 和額外卡片不符合本次官網觀察；校正稿使用實際的 Meta、SpaceXAI 與輪播文字。\n\nNative screens:\n\n'+screens.map(s=>'- `'+s.name+'` ('+s.device+')').join('\n')+'\n\n## Provider output (verbatim)\n\n'+messages.join('\n\n')+'\n\n## Provider suggestions (not automatically accepted)\n\n'+suggestions.map(s=>'- '+s).join('\n')+'\n');
const progress=read('progress.json');progress.vercel.native_mobile_screens=screens.map(s=>({name:s.name,device:s.device}));
if(screens.some(s=>s.device==='MOBILE'))progress.vercel.remaining=progress.vercel.remaining.filter(s=>s!=='Native MOBILE generation');
fs.writeFileSync(path.join(work,'progress.json'),JSON.stringify(progress,null,2)+'\n');
console.log(JSON.stringify({screens:screens.map(s=>({name:s.name,device:s.device,exports:s.exports.map(e=>({path:e.path,bytes:e.bytes,image:e.actual_image_dimensions}))})),accepted:false}));
