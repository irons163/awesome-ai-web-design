import fs from 'node:fs';
import path from 'node:path';
const work = path.resolve('.stitch-work/current-official');
const read = name => JSON.parse(fs.readFileSync(path.join(work, name), 'utf8'));
const write = (name, value) => fs.writeFileSync(path.join(work, name), JSON.stringify(value, null, 2) + '\n');
function compare(source, local, fonts = true) {
  const headings = source.headings.filter(h => h.box.width > 0 && h.box.height > 0);
  const differences = [];
  if (headings.length !== local.headings.length) differences.push({count: {source: headings.length, local: local.headings.length}});
  headings.forEach((heading, index) => {
    const actual = local.headings[index];
    if (!actual || actual.text !== heading.text) {differences.push({index, source: heading.text, local: actual?.text}); return;}
    for (const key of ['x', 'y', 'width', 'height']) {
      const delta = actual.box[key] - heading.box[key];
      if (Math.abs(delta) > .01) differences.push({text: heading.text, property: key, source: heading.box[key], local: actual.box[key], delta});
    }
    if (fonts) for (const key of Object.keys(heading.font)) if (heading.font[key] !== actual.font[key]) differences.push({text: heading.text, font: key, source: heading.font[key], local: actual.font[key]});
  });
  return {heading_count: headings.length, differences};
}

const progress = read('progress.json');
for (const brand of ['spotify', 'linear']) {
  const views = {};
  for (const mode of ['desktop', 'mobile']) {
    const source = read(brand + '-' + mode + '-browser-reference.json');
    const local = read(brand + '-' + mode + '-local-review.json');
    const result = compare(source, local);
    if (local.bodyWidth !== source.bodyWidth || local.bodyHeight !== source.bodyHeight) throw new Error('Body dimensions differ: ' + brand + '/' + mode);
    if (brand === 'linear' || mode === 'desktop') {
      if (result.differences.length) throw new Error('Unexpected reference difference: ' + brand + '/' + mode);
    } else if (result.differences.some(d => d.property !== 'y' || Math.abs(d.delta) > 1.5)) throw new Error('Unexpected narrow Spotify difference');
    if (local.images.loaded !== local.images.total) throw new Error('Original images did not all decode');
    views[mode] = {reference: brand + '-' + mode + '-browser-reference.json', local: brand + '-' + mode + '-local-review.json',
      source_observed_at: source.observed_at, local_observed_at: local.observed_at,
      viewport: local.viewport, body: {width: local.bodyWidth, height: local.bodyHeight}, images: local.images, ...result};
  }
  const native = read(brand + '-stitch-oct10-generated.json');
  const provenance = read(brand + '-browser-asset-provenance.json');
  const review = {accepted: false, views, native_exports: brand + '-stitch-oct10-generated.json',
    assets: {retained: provenance.assets.length, bytes: provenance.assets.reduce((sum, a) => sum + a.bytes, 0), original_native_failures_retained: provenance.failures.length},
    rendered_public_deployment_comparison: 'Not performed: the saved public Site-origin browser permission remains denied. A successful native deployment status does not establish rendered visual equivalence.',
    full_pixel_acceptance: false};
  if (brand === 'spotify') {
    const source = read('spotify-desktop-scroll-browser-reference.json');
    const local = read('spotify-desktop-scroll-local-review.json');
    const result = compare(source, local, false);
    if (result.differences.length || source.scrolls[0].height !== local.scrolls[0].height || source.scrolls[0].top !== local.scrolls[0].top) throw new Error('Post-scroll source differs');
    review.scroll = {reference: 'spotify-desktop-scroll-browser-reference.json', local: 'spotify-desktop-scroll-local-review.json', method: 'Two separate one-page wheel actions, each followed by a browser state check; content visibility and lazy layout depend on traversal.', ...result, ...local.scrolls[0]};
    review.narrow_limit = 'The recorded desktop user agent at390×844 renders812px-wide content. Six lower heading y-values remain1.5px above the initial reference. This is not a true phone acceptance.';
  } else {
    const local = read('linear-mobile-menu-local-review.json');
    const source = read('linear-mobile-menu-reference.json');
    const differences = [];
    source.links.forEach((link, index) => {
      const actual = local.links[index];
      if (!actual || actual.text !== link.text || actual.href !== link.href) differences.push({index, content: true});
      else for (const key of ['x', 'y', 'width', 'height']) if (Math.abs(link.box[key] - actual.box[key]) > .01) differences.push({index, box: key});
    });
    if (differences.length) throw new Error('Mobile menu differs');
    review.mobile_navigation = {reference: 'linear-mobile-menu-reference.json', local: 'linear-mobile-menu-local-review.json', links_checked: source.links.length, differences, opened_and_closed_with_escape: true};
    review.desktop_navigation = {references: ['linear-desktop-product-menu-reference.json', 'linear-desktop-resources-menu-reference.json'], checks: 'Both click-open panels, first-link boxes and Escape closure checked locally against the recorded1280×720 source. Product box379,64,860,281.5; Resources box379,64,860,226; first links400,85,256,90.5.', complete_keyboard_hover_acceptance: false};
  }
  write(brand + '-review.json', review);
  const key = brand === 'linear' ? 'linear.app' : brand;
  const prior = progress[key];
  const localDate = new Date(Date.parse(views.desktop.source_observed_at) + 8 * 60 * 60 * 1000).toISOString().replace('Z', '+08:00');
  progress[key] = {...prior, status: 'in_visual_review', accepted: false,
    previous_native_screen: prior.previous_native_screen || prior.native_screen,
    previous_reference_observed_at: prior.previous_reference_observed_at || prior.reference_observed_at,
    native_screen: native.screens[0].name, observed_at: localDate, reference_observed_at: views.desktop.source_observed_at,
    reference_kind: 'sanitized_rendered_public_browser_capture', reference: brand + '-reference.json',
    reference_record: brand + '-desktop-browser-reference.json', mobile_reference_record: brand + '-mobile-browser-reference.json',
    generation_record: brand + '-stitch-oct10-generated.json', generation_notes: brand + '-stitch-oct10-generation-notes.md',
    asset_provenance: brand + '-browser-asset-provenance.json', draft_build_record: brand + '-draft-build-record.json', review: brand + '-review.json',
    review_note: brand === 'spotify' ? '10 月 10 日台灣官網桌面與捲動頁尾已比對；窄視窗下方仍差1.5px，手機專用版與完整互動待驗收。' : '10 月 10 日官網桌面與390px標題、原始圖片與選單已比對；整頁像素、動畫與完整互動待驗收。',
    verified: [
      'October10 public desktop1280×720 and narrow390×844 rendered DOM/CSS/CSSOM, original vectors, source screenshots and actual body dimensions retained without reading accounts, cookies or storage.',
      'One new genuine DESKTOP Stitch generation, independently authored source-specific prompt, complete response and suggestions, immutable original HTML/PNG and separate source-corrected working study retained. Native screen metadata is not the thumbnail pixel size.',
      provenance.assets.length + ' unchanged public assets retained with source URL, size and SHA-256; failed native captures remain recorded even where supplementary public downloads succeed.',
      brand === 'spotify' ? 'All11 initial desktop heading boxes/fonts and all9 post-scroll heading boxes match the dated source; the two-step1440px scroll produces the same2119px content height. All54 original card covers and the two consent images decode locally; source decoded-image classes prevent invisible lower artwork.' : 'All15 heading texts, boxes and computed font records and total9614px/5873px document heights match at the recorded desktop/narrow viewports. All39 original image elements decode locally.',
      brand === 'spotify' ? 'Narrow document width812px matches the clipped source; the remaining six lower y-offsets of-1.5px are explicitly recorded.' : 'All15 mobile navigation link destinations and boxes match; open/Escape closure and both desktop Product/Resources panel and first-link boxes checked.',
    ],
    remaining: brand === 'spotify' ? [
      'Resolve the1.5px lower-heading narrow offset and obtain a true mobile-user-agent reference; the current narrow desktop player is clipped.',
      'Current native MOBILE generation, full-page pixel/motion, horizontal shelves, language/consent, keyboard and intermediate widths remain unaccepted. Accounts, playback and service search delegate to Spotify.',
      'The older Canada source remains a historical separate working snapshot and has not been revalidated.',
      'Published Site browser comparison remains unavailable under its saved origin permission; native publication status is not rendered visual acceptance.',
    ] : [
      'Current native MOBILE output, complete full-page pixel/animation, tablet/intermediate widths, sticky states, hover/keyboard/focus and demonstration interactions remain unaccepted.',
      'The public product demo is a dated visual state; account/project services remain on Linear.',
      'Published Site browser comparison remains unavailable under its saved origin permission; native publication status is not rendered visual acceptance.',
    ],
  };
  if (brand === 'spotify') progress[key].reference_variants = prior.reference_variants.map(v => v.region === 'Taiwan' ? {...v, observed_at: views.desktop.source_observed_at} : v);
  console.log(JSON.stringify({brand, headings: Object.fromEntries(Object.entries(views).map(([mode, v]) => [mode, {count: v.heading_count, differences: v.differences.length}])), assets: provenance.assets.length, accepted: false}));
}
write('progress.json', progress);
