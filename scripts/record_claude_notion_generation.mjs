import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const work = path.resolve('.stitch-work/current-official');
const read = name => JSON.parse(fs.readFileSync(path.join(work, name), 'utf8'));
const hash = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
function unpack(response, field) {
  if (response.structuredContent?.[field]) return response.structuredContent;
  for (const block of response.content || []) if (block.type === 'text') {
    try {const value = JSON.parse(block.text); if (value[field]) return value;} catch {}
  }
  throw new Error('No native ' + field + ' response');
}
for (const brand of (process.argv.slice(2).length ? process.argv.slice(2) : ['claude', 'notion'])) {
  const generationFile = brand + '-stitch-oct10-desktop-response.json';
  const generation = unpack(read(generationFile), 'outputComponents');
  const nativeScreens=generation.outputComponents.flatMap(component=>component.design?.screens||[]);
  if(!nativeScreens.length)throw new Error('No genuine generated screens');
  const screens=nativeScreens.map((generated,index)=>{
    const screenFile=brand+'-stitch-oct10-screen-'+index+'-response.json';
    const screen=unpack(read(screenFile),'name');
    if(screen.name!==generated.name)throw new Error('Screen did not originate in this generation');
    const exports=[['html',screen.htmlCode],['png',screen.screenshot]].map(([extension,file])=>{
      const name=brand+'-stitch-oct10-desktop-'+index+'.'+extension;
      const bytes=fs.readFileSync(path.join(work,name));
      const dimensions=extension==='png'&&bytes.subarray(0,8).equals(Buffer.from([137,80,78,71,13,10,26,10]))?{width:bytes.readUInt32BE(16),height:bytes.readUInt32BE(20)}:undefined;
      if(extension==='png'&&!dimensions)throw new Error('Invalid original PNG');
      if(extension==='html'&&!/<html[\s>]/i.test(bytes.toString()))throw new Error('Invalid original HTML');
      return {path:name,bytes:bytes.length,sha256:hash(bytes),native_file:file.name,source_url:file.downloadUrl,...(dimensions?{actual_image_dimensions:dimensions}:{})};
    });
    return {name:screen.name,title:screen.title,device:screen.deviceType,provider_dimensions:{width:screen.width,height:screen.height},screen_response:screenFile,exports};
  });
  const promptName = brand + '-stitch-oct10-desktop-prompt.md';
  const prompt = fs.readFileSync(path.join(work, promptName));
  const messages = generation.outputComponents.filter(c => typeof c.text === 'string').map(c => c.text);
  const suggestions = generation.outputComponents.filter(c => typeof c.suggestion === 'string').map(c => c.suggestion);
  const record = {accepted: false, project_id: generation.projectId, session_id: generation.sessionId,
    prompt: {path: promptName, bytes: prompt.length, sha256: hash(prompt), method: 'New source-specific instructions independently authored from the October 10 public browser references; upstream AI instructions were not reused.'},
    response: generationFile, screens,
    provider_text: messages, provider_suggestions: suggestions,
    limitation: 'Provider descriptions are unverified claims. Export image dimensions are recorded separately from provider screen metadata. Original HTML and image files remain unchanged; source corrections are separate working drafts.'};
  fs.writeFileSync(path.join(work, brand + '-stitch-oct10-generated.json'), JSON.stringify(record, null, 2) + '\n');
  const notes = '# ' + brand + ' — genuine Stitch generation, October 10\n\n' +
    '這是 Google Stitch 原始回覆與建議，完整保存供查核。下列「忠實」「精準」等敘述是生成工具的自述，並非驗收結果；校正草稿與原始生成檔分開保存。本輪未宣稱與官網完全一致。\n\n' +
    'Native screens:\n\n' + screens.map(screen=>'- `'+screen.name+'`').join('\n') + '\n\nPrompt: `' + promptName + '`\n\n' +
    '## Provider output (verbatim)\n\n' + messages.join('\n\n') + '\n\n## Provider suggestions (not accepted automatically)\n\n' + suggestions.map(s => '- ' + s).join('\n') + '\n';
  fs.writeFileSync(path.join(work, brand + '-stitch-oct10-generation-notes.md'), notes);
  console.log(JSON.stringify({brand,screens:screens.map(screen=>({name:screen.name,exports:screen.exports.map(e=>({path:e.path,bytes:e.bytes,image:e.actual_image_dimensions}))})),suggestions}));
}
