import {checkedNativeScreenshot} from './capture_checked_native_oct11.mjs';
export async function settledNativeScreenshot(tab,width,height){
  let state;
  for(let i=0;i<12;i++){
    state=await tab.playwright.evaluate(()=>({fonts:document.fonts.status,pending:[...document.images].filter(e=>{const b=e.getBoundingClientRect();return !e.complete&&b.width>0&&b.height>0&&b.top<innerHeight&&b.bottom>0}).length}));
    if(state.fonts==='loaded'&&!state.pending)return checkedNativeScreenshot(tab,width,height);
    await tab.playwright.domSnapshot();
  }
  throw new Error(`Visible image/font loading is unresolved; do not record this phase as verified (${JSON.stringify(state)}).`);
}
