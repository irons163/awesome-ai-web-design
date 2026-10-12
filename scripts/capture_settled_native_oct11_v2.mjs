import {checkedNativeScreenshot} from './capture_checked_native_oct11.mjs';

// Horizontally clipped carousel images do not enter the painted viewport.
export async function settledNativeScreenshot(tab, width, height) {
  let state;
  for (let i = 0; i < 12; i++) {
    state = await tab.playwright.evaluate(() => ({
      fonts: document.fonts.status,
      pending: [...document.images].filter(element => {
        const box = element.getBoundingClientRect();
        const style = getComputedStyle(element);
        return !element.complete && box.width > 0 && box.height > 0 &&
          box.top < innerHeight && box.bottom > 0 && box.left < innerWidth && box.right > 0 &&
          style.display !== 'none' && style.visibility !== 'hidden';
      }).length,
    }));
    if (state.fonts === 'loaded' && !state.pending) {
      return checkedNativeScreenshot(tab, width, height);
    }
    await tab.playwright.domSnapshot();
  }
  throw new Error(`Visible image/font loading is unresolved; do not record this phase as verified (${JSON.stringify(state)}).`);
}
