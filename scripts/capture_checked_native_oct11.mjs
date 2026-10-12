// CUA-only screenshot helper. Guard physical raster dimensions before recording.
function dimensions(bytes) {
  const b=Buffer.from(bytes);
  if(b[0]===0x89&&b[1]===0x50&&b[2]===0x4e&&b[3]===0x47)return{width:b.readUInt32BE(16),height:b.readUInt32BE(20)};
  if(b[0]!==0xff||b[1]!==0xd8)throw new Error('Unexpected native screenshot encoding');
  let at=2;
  while(at<b.length){
    while(b[at]===0xff)at++;
    const marker=b[at++];
    if(marker===0xd9||marker===0xda)break;
    if(marker===0x01||(marker>=0xd0&&marker<=0xd7))continue;
    const length=b.readUInt16BE(at);
    if([0xc0,0xc1,0xc2,0xc3,0xc5,0xc6,0xc7,0xc9,0xca,0xcb,0xcd,0xce,0xcf].includes(marker))return{height:b.readUInt16BE(at+3),width:b.readUInt16BE(at+5)};
    if(length<2)throw new Error('Malformed native JPEG');
    at+=length;
  }
  throw new Error('Native JPEG dimensions unavailable');
}
export async function checkedNativeScreenshot(tab,width,height){
  const bytes=await tab.screenshot({fullPage:false});
  const actual=dimensions(bytes);
  if(actual.width!==width||actual.height!==height)throw new Error(`Excluded physical screenshot ${actual.width}x${actual.height}; expected ${width}x${height}. Use a fresh selected tab before recording.`);
  return bytes;
}
