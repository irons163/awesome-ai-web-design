#!/usr/bin/env node
// Stage the public catalog with an exact dependency closure per current study.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {stageOfficialContent} from './publication.mjs';
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const OUTPUT = path.join(ROOT, 'dist');
const DRAFT_SOURCE = path.join(ROOT, '.stitch-work/current-official');
const json = file => JSON.parse(fs.readFileSync(file, 'utf8'));
const write = (file, text) => fs.writeFileSync(file, text);

function main() {
  if (fs.existsSync(OUTPUT) && fs.lstatSync(OUTPUT).isSymbolicLink()) {
    throw new Error('dist must be a regular build directory');
  }
  fs.rmSync(OUTPUT, { recursive: true, force: true });
  fs.mkdirSync(OUTPUT);
  for (const name of ['index.html', 'README.md', 'ATTRIBUTION.md', 'LICENSE', 'CONTRIBUTING.md']) {
    fs.copyFileSync(path.join(ROOT, name), path.join(OUTPUT, name));
  }
  for (const name of ['assets', 'design-md', 'prompts']) {
    fs.cpSync(path.join(ROOT, name), path.join(OUTPUT, name), { recursive: true,
      filter: source => path.basename(source) !== 'all-designs.zip' });
  }
  fs.rmSync(path.join(OUTPUT, 'assets', 'all-designs.zip'), { force: true });
  const imageBase = json(path.join(ROOT, 'data', 'hosting-assets.json')).image_base_url.replace(/\/?$/, '/');
  const catalogPath = path.join(OUTPUT, 'assets', 'catalog.json');
  const catalog = json(catalogPath);
  for (const item of catalog.designs) {
    if (item.preview.status !== 'generated') continue;
    for (const key of ['image', 'thumbnail']) {
      const relative = item.preview[key];
      item.preview[key] = imageBase + relative;
      fs.rmSync(path.join(OUTPUT, relative), { force: true });
    }
  }
  write(catalogPath, JSON.stringify(catalog) + '\n');
  const progress = json(path.join(DRAFT_SOURCE, 'progress.json'));
  const summary = stageOfficialContent(ROOT, OUTPUT, progress, catalog.designs);
  console.log(JSON.stringify(summary));
  console.log('Staged public website in ' + OUTPUT);
}

main();
