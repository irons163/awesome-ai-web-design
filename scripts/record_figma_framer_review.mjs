import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const work = path.resolve('.stitch-work/current-official');
const capture = path.resolve(process.argv[2] || '/private/tmp/official-browser-figma-framer-oct10');
const read = file => JSON.parse(fs.readFileSync(file, 'utf8'));
const write = (file, value) => fs.writeFileSync(file, JSON.stringify(value, null, 2) + '\n');
const hash = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const final = read(path.join(capture, 'local-final-measurements.json'));
const navigation = read(path.join(capture, 'local-navigation-measurements.json'));
const media = read(path.join(capture, 'local-media-measurements.json'));
const progress = read(path.join(work, 'progress.json'));
const equal = (a, b) => JSON.stringify(a) === JSON.stringify(b);

for (const brand of ['figma', 'framer']) {
  const views = {};
  for (const variant of ['desktop', 'mobile']) {
    const source = read(path.join(work, `${brand}-${variant}-browser-reference.json`));
    const local = final[`${brand}-${variant}`];
    const headings = source.headings.filter(h => h.box.width && h.box.height);
    const differences = [];
    if (headings.length !== local.headings.length) differences.push({field: 'heading count'});
    headings.forEach((sourceHeading, index) => {
      for (const field of ['text', 'sourceText', 'box', 'font']) {
        if (!equal(sourceHeading[field], local.headings[index]?.[field])) differences.push({index, field, source: sourceHeading[field], local: local.headings[index]?.[field]});
      }
    });
    const dimensionsMatch = source.bodyWidth === local.body.width && source.bodyHeight === local.body.height;
    if (differences.length || !dimensionsMatch || local.brokenImages.length) throw new Error(`Observed layout/image regression: ${brand} ${variant}`);
    const screenshots = ['first', 'full'].map(view => {
      const file = `${brand}-local-${variant}-${view}.jpg`, bytes = fs.readFileSync(path.join(work, file));
      return {path: file, bytes: bytes.length, sha256: hash(bytes), method: 'Original local working-study browser screenshot unchanged; not a production screenshot.'};
    });
    views[variant] = {source: `${brand}-${variant}-browser-reference.json`, source_observed_at: source.observed_at, local, compared_headings: headings.length, heading_differences: differences, body_dimensions_match: dimensionsMatch, screenshots};
  }
  const selectedNavigation = Object.fromEntries(Object.entries(navigation).filter(([key]) => key.startsWith(brand)));
  if (brand === 'framer') {
    const source = read(path.join(work, 'framer-desktop-platform-navigation-browser-reference.json'));
    const local = selectedNavigation.framerDesktopPlatform;
    const differences = [];
    source.links.forEach((link, i) => {for (const field of ['text', 'href', 'box']) if (!equal(link[field], local.links[i]?.[field])) differences.push({index:i, field, source:link[field], local:local.links[i]?.[field]});});
    if (source.links.length !== local.links.length) differences.push({field:'link count'});
    if (differences.length || local.unresolvedSvg.length) throw new Error('Official expanded Platform navigation differs');
    local.source_reference = 'framer-desktop-platform-navigation-browser-reference.json';
    local.compared_links = source.links.length;
    local.differences = differences;
  }
  const selectedMedia = Object.fromEntries(Object.entries(media).filter(([key]) => key.startsWith(brand)));
  if (brand === 'figma' && (!selectedMedia.figmaPausedPlayer.paused || selectedMedia.figmaPlayingPlayer.paused || selectedMedia.figmaPausedPlayer.readyState !== 4 || selectedMedia.figmaPlayingPlayer.readyState !== 4)) throw new Error('Actual ready Vimeo video must pause and play');
  const build = read(path.join(work, `${brand}-draft-build-record.json`));
  if (hash(fs.readFileSync(path.join(work, `${brand}.html`))) !== build.working_draft.sha256) throw new Error('Draft changed after generation/build record');
  const record = {accepted: false, reviewed_at: new Date().toISOString(), working_draft:build.working_draft, views, navigation:selectedNavigation, media:selectedMedia, limitations:progress[brand].remaining, scope:'Measured dated layout, image decoding and selected local UI actions. Full-page pixels, all interactions, motion, actual mobile devices and rendered production are not accepted.'};
  write(path.join(work, `${brand}-review.json`), record);
  console.log(JSON.stringify({brand,headings:Object.values(views).reduce((n,v)=>n+v.compared_headings,0),images:Object.values(views).reduce((n,v)=>n+v.local.imageCount,0),accepted:false}));
}
