import fs from 'node:fs/promises';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { nativeScreenshot } from './figma_source6_research.mjs';

const base = '/Users/pchang01/Documents/mygithub/awesome-ai-web-design/.stitch-work/current-official';
const allowed = new Set(['linear', 'vercel', 'claude', 'notion']);
const sha = data => createHash('sha256').update(data).digest('hex');
const chunks = value => Array.from({length: Math.ceil(value.length / 80000)}, (_, i) => value.slice(i * 80000, (i + 1) * 80000));

/** Call only in CUA, with selectors derived from the current observed DOM. */
export async function captureMenuState(tab, cdp, slug, state, expectedUrl, selectors) {
  if (!allowed.has(slug) || !['closed-before', 'open', 'closed-after'].includes(state)) throw new Error('Out of scope');
  await cdp.send('Page.bringToFront', {});
  await tab.playwright.domSnapshot();
  const result = await tab.playwright.evaluate(({selectors}) => {
    const parts = value => Array.from({length: Math.ceil(value.length / 80000)}, (_, i) => value.slice(i * 80000, (i + 1) * 80000));
    const attrs = node => node ? Object.fromEntries(Array.from(node.attributes).map(a => [a.name, a.value])) : null;
    const styles = node => {
      const cs = getComputedStyle(node);
      const r = node.getBoundingClientRect();
      return {display: cs.display, visibility: cs.visibility, opacity: cs.opacity, position: cs.position,
        transform: cs.transform, transition: cs.transition, animation: cs.animation, overflow: cs.overflow,
        overflowY: cs.overflowY, pointerEvents: cs.pointerEvents, zIndex: cs.zIndex,
        box: {x: r.x, y: r.y, width: r.width, height: r.height}};
    };
    const html = document.documentElement.outerHTML;
    const selected = selectors.map(selector => ({selector, elements: Array.from(document.querySelectorAll(selector)).map((node, index) => {
      const outer = node.outerHTML;
      const ancestors = [];
      for (let parent = node.parentElement; parent; parent = parent.parentElement) {
        ancestors.push({tag: parent.tagName, attributes: attrs(parent), computed: styles(parent)});
      }
      return {index, tag: node.tagName, attributes: attrs(node), computed: styles(node),
        outerHTMLParts: parts(outer), outerHTML_length: outer.length, ancestors};
    })}));
    const cssomStylesheets = Array.from(document.styleSheets).map((sheet, index) => {
      try {
        const css = Array.from(sheet.cssRules).map(rule => rule.cssText).join('\n');
        return {index, href: sheet.href, ownerTag: sheet.ownerNode?.tagName || null,
          readable: true, cssParts: parts(css), css_length: css.length};
      } catch (error) {
        return {index, href: sheet.href, ownerTag: sheet.ownerNode?.tagName || null,
          readable: false, error: String(error), cssParts: [], css_length: 0};
      }
    });
    return {observed_at: new Date().toISOString(), url: location.href, title: document.title,
      document_language: document.documentElement.lang, viewport: [innerWidth, innerHeight],
      scrollY, bodyHeight: Math.max(document.body.scrollHeight, document.documentElement.scrollHeight),
      html_attributes: attrs(document.documentElement), body_attributes: attrs(document.body),
      html_computed: styles(document.documentElement), body_computed: styles(document.body),
      htmlParts: parts(html), html_length: html.length, selected, cssomStylesheets};
  }, {selectors});
  if (result.url !== expectedUrl || result.viewport[0] !== 390 || result.viewport[1] !== 844) throw new Error('URL/viewport guard failed: ' + JSON.stringify({url: result.url, viewport: result.viewport}));
  result.html_sha256 = sha(result.htmlParts.join(''));
  for (const group of result.selected) for (const element of group.elements) element.outerHTML_sha256 = sha(element.outerHTMLParts.join(''));
  for (const sheet of result.cssomStylesheets) sheet.css_sha256 = sha(sheet.cssParts.join(''));
  const bytes = await nativeScreenshot(tab, 390, 844);
  const screenshot = `${slug}-oct12-official-menu${state === 'open' ? '' : '-' + state}.jpg`;
  await fs.writeFile(path.join(base, screenshot), bytes);
  result.screenshot = screenshot;
  result.screenshot_sha256 = sha(bytes);
  result.screenshot_bytes = bytes.length;
  result.actual_raster_dimensions = [390, 844];
  result.native_screenshot_unmodified = true;
  result.source_research_only = true;
  result.state = state;
  const reference = `${slug}-oct12-official-menu-${state}-reference.private.json`;
  await fs.writeFile(path.join(base, reference), JSON.stringify(result, null, 2) + '\n');
  return {state, reference, screenshot, screenshot_sha256: result.screenshot_sha256,
    observed_at: result.observed_at, viewport: result.viewport,
    selected: result.selected.map(group => ({selector: group.selector, count: group.elements.length,
      elements: group.elements.map(e => ({attributes: e.attributes, computed: e.computed}))}))};
}

export async function finalizeMenuResearch(slug, details) {
  if (!allowed.has(slug) || details.all_native_rasters_inspected_by_owner !== true) throw new Error('Explicit raster inspection is required');
  const states = {};
  for (const state of ['closed-before', 'open', 'closed-after']) {
    const file = `${slug}-oct12-official-menu-${state}-reference.private.json`;
    const data = await fs.readFile(path.join(base, file));
    const reference = JSON.parse(data);
    const screenshot = await fs.readFile(path.join(base, reference.screenshot));
    if (sha(screenshot) !== reference.screenshot_sha256) throw new Error('Raster hash changed');
    states[state] = {reference: file, reference_sha256: sha(data), ...reference};
  }
  const destination = path.join(base, `${slug}-oct12-official-menu.private.json`);
  try {
    const prior = JSON.parse(await fs.readFile(destination, 'utf8'));
    if (prior.status === 'browser_unavailable_before_new_observation') {
      await fs.rename(destination, path.join(base, `${slug}-oct12-official-menu-blocked-history.private.json`));
    } else throw new Error('Prior menu evidence exists; refusing to overwrite');
  } catch (error) {
    if (error.code !== 'ENOENT' && error.message !== undefined && !error.message.includes('no such file')) throw error;
  }
  const record = {brand: slug, source_research_only: true, status: 'public_root_menu_open_close_observed',
    prepared_at: new Date().toISOString(), official_consistency_claim: false, accepted: false,
    viewport: [390, 844], ...details, states};
  await fs.writeFile(destination, JSON.stringify(record, null, 2) + '\n');
  return {file: destination, bytes: (await fs.stat(destination)).size, sha256: sha(await fs.readFile(destination))};
}

export { chunks };
