import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { setTimeout as delay } from 'node:timers/promises';
import test from 'node:test';
import { JSDOM } from 'jsdom';

// These exercise the real catalog UI with its generated progress page. They
// check navigation and async state, not browser rendering or visual fidelity.
const root = new URL('../', import.meta.url);
const read = path => readFileSync(new URL(path, root), 'utf8');
const html = read('index.html');
const application = read('assets/app.js');
const catalog = read('assets/catalog.json');
const published = existsSync(new URL('dist/client/official-progress.html', root)) ? 'dist/client/' : 'dist/';
const progress = read(published + 'official-progress.html');
const studies = JSON.parse(read(published + 'assets/official-studies.json')).studies;

async function settleUntil(predicate) {
  for (let attempt = 0; attempt < 30; attempt++) {
    if (predicate()) return;
    await delay(5);
  }
  assert.fail('Catalog UI did not reach the expected state');
}

async function fixture(t, slug, progressMarkup = progress, studyDocuments = {}) {
  const dom = new JSDOM(html, {
    url: `https://catalog.test/#/design/${encodeURIComponent(slug)}`,
    runScripts: 'outside-only',
  });
  t.after(async () => {
    // Programmatic details.open changes enqueue a toggle event. Let it finish
    // while this fixture still has its document before disposing the window.
    await delay(0);
    dom.window.close();
  });
  const { window } = dom;
  const query = selector => window.document.querySelector(selector);
  window.HTMLDialogElement.prototype.showModal = function () {
    this.setAttribute('open', '');
  };
  window.HTMLDialogElement.prototype.close = function () {
    this.removeAttribute('open');
  };
  let resolveProgress;
  const requested = [], copied = [];
  Object.defineProperty(window.navigator, 'clipboard', {value:{writeText:async text=>copied.push(text)}});
  const pendingProgress = new Promise(resolve => { resolveProgress = resolve; });
  window.fetch = async path => {
    requested.push(path);
    if (path === 'assets/catalog.json') {
      return { ok: true, json: async () => JSON.parse(catalog) };
    }
    if (path === 'official-progress.html') return pendingProgress;
    if (Object.hasOwn(studyDocuments, path)) {
      const content=studyDocuments[path];
      if(typeof content==='function')return content();
      return {ok:content!==false, text:async () => content};
    }
    if (/^official-drafts\/[a-z0-9.-]+\.md$/.test(path)) return {ok:true,text:async()=>read(published+path)};
    throw new Error(`Unexpected fetch: ${path}`);
  };
  window.eval(application);
  await settleUntil(() => query('#design-dialog').open);
  return {
    window, query, requested, copied,
    revealProgress: () => resolveProgress({ ok: true, text: async () => progressMarkup }),
    failProgress: () => resolveProgress({ ok: false }),
    original: JSON.parse(catalog).designs.find(item => item.slug === slug).preview,
  };
}

function assertOfficialOnly(query) {
  assert.equal(query('#official-preview').hidden, false);
  assert.equal(query('#creation-history').open, false);
  for (const selector of ['#preview-frame', '#preview-image']) {
    assert.equal(query(selector).hidden, true);
    assert.equal(query(selector).hasAttribute('src'), false);
  }
  assert.equal(query('#preview-actions').hidden, true);
  assert.equal(query('#preview-frame').getAttribute('sandbox'), 'allow-scripts');
}
async function openHistory(ui,view='image') {
  ui.query('#creation-history').open=true;
  await settleUntil(()=>ui.query('#preview-image').hasAttribute('src'));
  ui.query(`[data-preview="${view}"]`).click();
}

test('a modified Stitch web export is identified as adjusted in its history', async t => {
  const ui = await fixture(t, 'google');
  ui.revealProgress();
  await settleUntil(() => ui.query('#official-preview-link').getAttribute('href') === 'official-drafts/google.html');
  await openHistory(ui);
  assert.match(ui.query('.history-description').textContent, /經修改並重新截圖/);
  assert.match(ui.query('#preview-image').alt, /調整後的預覽截圖/);
  assert.equal(ui.query('[data-preview="html"]').textContent, '調整後 HTML');
  assert.match(ui.query('#preview-actions .preview-note').textContent, /人工調整/);
});

test('a late combined-copy response cannot replace a different brand or enable a stale copy', async t => {
  const old=studies.find(study=>study.slug==='wired');
  const next=studies.find(study=>study.slug==='pinterest');
  let resolveOld;
  const pending=new Promise(resolve=>{resolveOld=resolve;});
  const ui=await fixture(t,'wired',progress,{[old.study.analysis]:()=>pending});
  ui.revealProgress();
  await settleUntil(()=>ui.requested.includes(old.study.analysis));
  assert.equal(ui.query('#copy-full-reference').disabled,true);
  ui.window.location.hash='#/design/pinterest';
  await settleUntil(()=>ui.query('#detail-title').textContent==='Pinterest'&&!ui.query('#copy-full-reference').disabled);
  const expected=ui.query('#combined-reference-text').textContent;
  assert.ok(expected.includes(read(published+next.study.analysis).trimEnd()));
  resolveOld({ok:true,text:async()=> 'STALE_WIRED_DOCUMENT'});
  await delay(0);
  assert.equal(ui.query('#combined-reference-text').textContent,expected);
  ui.query('#copy-full-reference').click();
  await settleUntil(()=>ui.copied.at(-1)===expected);
  assert.ok(!ui.copied.at(-1).includes('STALE_WIRED_DOCUMENT'));
});

function assertCurrentStudyStatus(query, slug) {
  const study = studies.find(item => item.slug === slug);
  assert.ok(study, `Missing published study metadata: ${slug}`);
  assert.equal(query('#official-preview-status').textContent, `參考日期：${study.date}`);
  assert.equal(query('#official-study-source').getAttribute('href'), study.reference_url);
  assert.equal(query('#official-study-source').textContent, `${study.name} 官網 ↗`);
}

test('a direct brand link defaults to the official draft and waits for its progress', async t => {
  const ui = await fixture(t, 'wired');
  assertOfficialOnly(ui.query);
  assert.match(ui.query('#official-preview-status').textContent, /讀取/);
  ui.revealProgress();
  await settleUntil(() => ui.query('#official-preview-link').getAttribute('href') === 'official-drafts/wired.html');
  assertOfficialOnly(ui.query);
  assertCurrentStudyStatus(ui.query, 'wired');
  assert.equal(ui.query('#open-preview').getAttribute('href'), 'https://catalog.test/official-drafts/wired.html');
  assert.equal(ui.query('#official-preview-link').target, '_blank');
  assert.equal(ui.query('#official-preview-link').rel, 'noopener');
});

test('late progress updates the main preview while preserving an explicitly opened AI history', async t => {
  const ui = await fixture(t, 'wired');
  await openHistory(ui,'html');
  assert.equal(ui.query('#preview-frame').getAttribute('src'), ui.original.html);
  assert.equal(ui.query('#download-html').getAttribute('href'), ui.original.html+'?download=1');
  assert.equal(ui.query('#generation-prompt').getAttribute('href'), ui.original.prompt+'?download=1');
  ui.revealProgress();
  await settleUntil(() => ui.query('.official-drafts-count').textContent.includes('份參考來源'));
  assert.equal(ui.query('#official-preview').hidden, false);
  assert.equal(ui.query('#preview-frame').hidden, false);
  assert.equal(ui.query('#preview-frame').getAttribute('src'), ui.original.html);
  assert.equal(ui.query('[data-preview="html"]').getAttribute('aria-pressed'), 'true');
  assert.equal(ui.query('#open-preview').getAttribute('href'),'https://catalog.test/official-drafts/wired.html');
  assert.equal(ui.query('#open-generation-preview').getAttribute('href'),ui.original.html);
  ui.query('#creation-history').open=false;
  await settleUntil(()=>!ui.query('#preview-frame').hasAttribute('src'));
  assertOfficialOnly(ui.query);
  assert.equal(ui.query('#official-preview-link').getAttribute('href'), 'official-drafts/wired.html');
});

test('a brand without an official draft stays pending instead of showing its fictional original', async t => {
  const pendingPage = new JSDOM(progress);
  const link = pendingPage.window.document.querySelector('th a[href="official-drafts/pinterest.html"]');
  assert.ok(link, 'The actual catalog must include the new Pinterest draft');
  link.setAttribute('href', 'index.html#/design/pinterest');
  link.closest('tr').querySelector('td.draft').className = 'pending';
  const pendingMarkup = pendingPage.serialize();
  pendingPage.window.close();
  const ui = await fixture(t, 'pinterest', pendingMarkup);
  ui.revealProgress();
  await settleUntil(() => ui.query('#official-preview-status').textContent.includes('尚無'));
  assertOfficialOnly(ui.query);
  assert.equal(ui.query('#official-preview-link').getAttribute('href'), 'reference-sources.html');
  assert.equal(ui.query('#current-preview-image').hidden,true);
  await openHistory(ui);
  assert.equal(ui.query('#preview-image').getAttribute('src'), ui.original.image);
  assert.equal(ui.query('#preview-caption').textContent,'設計預覽');
});

for (const slug of ['pinterest', 'vodafone']) {
  test(`${slug} opens its new official draft from the real published progress`, async t => {
    const ui = await fixture(t, slug);
    ui.revealProgress();
    await settleUntil(() => ui.query('#official-preview-link').getAttribute('href') === `official-drafts/${slug}.html`);
    assertOfficialOnly(ui.query);
    assertCurrentStudyStatus(ui.query, slug);
    assert.equal(ui.query('.official-drafts-count').textContent, `${studies.length} 份參考來源`);
  });
}

test('Linear uses the catalog slug and the actual published draft filename', async t => {
  const ui = await fixture(t, 'linear.app');
  ui.revealProgress();
  await settleUntil(() => ui.query('#official-preview-link').getAttribute('href') === 'official-drafts/linear.html');
  assertOfficialOnly(ui.query);
});

test('a failed progress request preserves the official view with a recovery link', async t => {
  const ui = await fixture(t, 'spotify');
  ui.failProgress();
  await settleUntil(() => ui.query('#official-preview-status').textContent.includes('無法載入'));
  assertOfficialOnly(ui.query);
  assert.equal(ui.query('#official-preview-link').getAttribute('href'), 'reference-sources.html');
  assert.equal(ui.query('#download-design').hidden,true);
  assert.equal(ui.query('#download-prompts').hidden,true);
  assert.equal(ui.query('#download-implementation-pack').hidden,true);
  assert.match(ui.query('#document-reference').textContent,/無法載入/);
  ui.query('#tab-document').click();
  assert.equal(ui.query('#copy-document').disabled,true);
  assert.match(ui.query('#document-text').textContent,/重新整理/);
  assert.ok(!ui.requested.some(path=>path.startsWith('design-md/')));
});

test('opening another brand resets an original preview choice to its official draft', async t => {
  const ui = await fixture(t, 'wired');
  ui.revealProgress();
  await settleUntil(() => ui.query('#official-preview-link').getAttribute('href') === 'official-drafts/wired.html');
  await openHistory(ui,'html');
  ui.window.location.hash = '#/design/spotify';
  await settleUntil(() => ui.query('#official-preview-link').getAttribute('href') === 'official-drafts/spotify.html');
  assertOfficialOnly(ui.query);
  assert.equal(ui.query('#detail-title').textContent, 'Spotify');
});

test('all catalog covers and the default detail image depict the same current study', async t=>{
  const ui=await fixture(t,'pinterest');
  assert.equal(ui.query('#catalog').querySelectorAll('img').length,0);
  ui.revealProgress();
  await settleUntil(()=>ui.query('#catalog').querySelectorAll('img').length===studies.length);
  for(const study of studies){
    const image=ui.query(`[data-design="${study.slug}"] .card-art img`);
    assert.equal(image.getAttribute('src'),study.cover.src);
    assert.equal(study.cover.preview_sha256,study.preview_sha256);
  }
  const current=studies.find(study=>study.slug==='pinterest');
  assert.equal(ui.query('#current-preview-image').getAttribute('src'),current.cover.src);
  assertOfficialOnly(ui.query);
});

test('public preview keeps source and date while detailed checks stay in developer records', async t => {
  const ui = await fixture(t, 'starbucks');
  ui.revealProgress();
  await settleUntil(() => ui.query('#official-preview-link').getAttribute('href') === 'official-drafts/starbucks.html');
  assertCurrentStudyStatus(ui.query, 'starbucks');
  assert.equal(ui.query('#official-study-details').hidden, false);
  assert.equal(ui.query('#download-implementation-pack').hidden,false);
  assert.equal(ui.query('#download-implementation-pack').getAttribute('href'),'assets/design-packs/starbucks.zip');
  assert.equal(ui.query('#official-study-limits'), null);
  assert.equal(ui.query('#official-study-scope'), null);
  assert.match(ui.query('#official-preview .preview-note').textContent, /此預覽供設計參考，部分互動為示範/);
  assert.doesNotMatch(ui.query('#official-preview').textContent, /RGB|2560|中繼資料|像素|未驗證/);
  assert.match(progress, /開發比對紀錄/);
  assert.match(progress, /0\.249/);
});

test('the main AI tab copies and downloads its dated prompt, with the original three in history', async t => {
  const markup = new JSDOM(progress);
  const row = markup.window.document.querySelector('#elevenlabs');
  const href = row.querySelector('.study-prompts').getAttribute('href');
  markup.window.close();
  const exactPrompt = '# 實際重寫指令\n\nPreserve the current source and recorded differences.\n';
  const ui = await fixture(t, 'elevenlabs', progress, {[href]:exactPrompt});
  ui.revealProgress();
  await settleUntil(() => ui.query('#download-prompts').getAttribute('href')===href+'?download=1');
  assert.equal(ui.query('#prompt-list').children.length, 3);
  assert.ok(ui.query('#creation-history').contains(ui.query('#prompt-list')));
  assert.equal(ui.query('#original-prompt-details').open,false);
  assert.equal(ui.query('#download-original-prompts').getAttribute('href'),'design-md/elevenlabs/PROMPTS.md?download=1');
  ui.query('#tab-prompts').click();
  await settleUntil(() => ui.query('#copy-current-prompt').disabled === false);
  assert.equal(ui.query('#current-prompt-text').textContent, exactPrompt);
  ui.query('#copy-current-prompt').click();
  await settleUntil(()=>ui.copied.length===1);
  assert.equal(ui.copied[0],exactPrompt);
  ui.window.location.hash = '#/design/wired';
  await settleUntil(() => ui.query('#detail-title').textContent === 'WIRED');
  assert.equal(ui.query('#current-prompt-text').textContent, '');
  assert.equal(ui.query('#copy-current-prompt').disabled,true);
  assert.equal(ui.query('#prompt-list').children.length, 3);
});

test('a directly opened analysis waits for metadata then reads, copies and downloads the same current file',async t=>{
  const study=studies.find(row=>row.slug==='pinterest'),href=study.study.analysis;
  const exact='# Current dated analysis\n\nPreserve this exact content.\n';
  const ui=await fixture(t,'pinterest',progress,{[href]:exact});
  ui.query('#tab-document').click();
  assert.equal(ui.query('#copy-document').disabled,true);
  assert.equal(ui.query('#download-design').hidden,true);
  assert.ok(!ui.requested.some(path=>path.startsWith('design-md/')));
  ui.revealProgress();
  await settleUntil(()=>!ui.query('#copy-document').disabled);
  assert.equal(ui.query('#document-text').textContent,exact);
  assert.equal(ui.query('#download-design').getAttribute('href'),href+'?download=1');
  assert.ok(ui.query('#document-reference').textContent.includes(study.date));
  assert.equal(ui.query('#current-analysis-note'),null);
  ui.query('#copy-document').click();
  await settleUntil(()=>ui.copied.length===1);
  assert.equal(ui.copied[0],exact);
  assert.equal(ui.query('#download-original-design').getAttribute('href'),'design-md/pinterest/DESIGN.md?download=1');
  assert.equal(ui.query('#creation-history').open,false);
});

test('all primary analysis and prompt links match their preview while original files remain in history',async t=>{
  const ui=await fixture(t,'pinterest');ui.revealProgress();
  await settleUntil(()=>ui.query('#catalog').querySelectorAll('img').length===studies.length);
  for(const study of studies){
    ui.window.location.hash='#/design/'+encodeURIComponent(study.slug);
    await settleUntil(()=>ui.query('#detail-title').textContent===study.name);
    assert.ok(study.study.analysis&&study.study.prompts,study.slug);
    assert.equal(ui.query('#download-design').getAttribute('href'),study.study.analysis+'?download=1');
    assert.equal(ui.query('#download-prompts').getAttribute('href'),study.study.prompts+'?download=1');
    assert.equal(ui.query('#download-original-design').getAttribute('href'),`design-md/${study.slug}/DESIGN.md?download=1`);
    assert.equal(ui.query('#download-original-prompts').getAttribute('href'),`design-md/${study.slug}/PROMPTS.md?download=1`);
    assert.equal(ui.query('#creation-history').open,false);
  }
});

for(const [tab,kind,output,copy] of [['document','analysis','#document-text','#copy-document'],['prompts','prompts','#current-prompt-text','#copy-current-prompt']]){
  test(`late ${kind} responses cannot overwrite a newly selected brand`,async t=>{
    const first=studies.find(row=>row.slug==='pinterest').study[kind],second=studies.find(row=>row.slug==='wired').study[kind];
    let completeFirst;
    const waiting=new Promise(resolve=>completeFirst=resolve);
    const ui=await fixture(t,'pinterest',progress,{[first]:()=>waiting,[second]:'# WIRED current content\n'});
    ui.revealProgress();await settleUntil(()=>ui.query('#download-design').hidden===false);
    ui.query('#tab-'+tab).click();await settleUntil(()=>ui.requested.includes(first));
    ui.window.location.hash='#/design/wired';await settleUntil(()=>ui.query('#detail-title').textContent==='WIRED');
    ui.query('#tab-'+tab).click();await settleUntil(()=>!ui.query(copy).disabled);
    completeFirst({ok:true,text:async()=>'# Obsolete Pinterest response\n'});await delay(10);
    assert.equal(ui.query(output).textContent,'# WIRED current content\n');
    ui.query(copy).click();await settleUntil(()=>ui.copied.length===1);
    assert.equal(ui.copied[0],'# WIRED current content\n');
  });

  test(`failed current ${kind} requests stay explicit and can retry without loading the old file`,async t=>{
    const href=studies.find(row=>row.slug==='pinterest').study[kind];let fail=true;
    const ui=await fixture(t,'pinterest',progress,{[href]:()=>({ok:!fail,text:async()=>'# Current content after retry\n'})});
    ui.revealProgress();await settleUntil(()=>ui.query('#download-design').hidden===false);
    ui.query('#tab-'+tab).click();await settleUntil(()=>ui.query(output).textContent.includes('無法'));
    assert.equal(ui.query(copy).disabled,true);
    assert.ok(!ui.requested.some(path=>path.startsWith('design-md/')));
    fail=false;
    ui.query('#tab-preview').click();ui.query('#tab-'+tab).click();
    await settleUntil(()=>!ui.query(copy).disabled);
    assert.equal(ui.query(output).textContent,'# Current content after retry\n');
  });
}
