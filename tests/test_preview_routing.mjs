import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
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
const progress = read('dist/official-progress.html');

async function settleUntil(predicate) {
  for (let attempt = 0; attempt < 30; attempt++) {
    if (predicate()) return;
    await delay(5);
  }
  assert.fail('Catalog UI did not reach the expected state');
}

async function fixture(t, slug, progressMarkup = progress) {
  const dom = new JSDOM(html, {
    url: `https://catalog.test/#/design/${encodeURIComponent(slug)}`,
    runScripts: 'outside-only',
  });
  t.after(() => dom.window.close());
  const { window } = dom;
  const query = selector => window.document.querySelector(selector);
  window.HTMLDialogElement.prototype.showModal = function () {
    this.setAttribute('open', '');
  };
  window.HTMLDialogElement.prototype.close = function () {
    this.removeAttribute('open');
  };
  let resolveProgress;
  const pendingProgress = new Promise(resolve => { resolveProgress = resolve; });
  window.fetch = async path => {
    if (path === 'assets/catalog.json') {
      return { ok: true, json: async () => JSON.parse(catalog) };
    }
    if (path === 'official-progress.html') return pendingProgress;
    throw new Error(`Unexpected fetch: ${path}`);
  };
  window.eval(application);
  await settleUntil(() => query('#design-dialog').open);
  return {
    window, query,
    revealProgress: () => resolveProgress({ ok: true, text: async () => progressMarkup }),
    failProgress: () => resolveProgress({ ok: false }),
    original: JSON.parse(catalog).designs.find(item => item.slug === slug).preview,
  };
}

function assertOfficialOnly(query) {
  assert.equal(query('#official-preview').hidden, false);
  assert.equal(query('[data-preview="official"]').getAttribute('aria-pressed'), 'true');
  for (const selector of ['#preview-frame', '#preview-image']) {
    assert.equal(query(selector).hidden, true);
    assert.equal(query(selector).hasAttribute('src'), false);
  }
  assert.equal(query('#preview-actions').hidden, true);
  assert.equal(query('#preview-frame').getAttribute('sandbox'), 'allow-scripts');
}

test('a direct brand link defaults to the official draft and waits for its progress', async t => {
  const ui = await fixture(t, 'wired');
  assertOfficialOnly(ui.query);
  assert.match(ui.query('#official-preview-status').textContent, /讀取/);
  ui.revealProgress();
  await settleUntil(() => ui.query('#official-preview-link').getAttribute('href') === 'official-drafts/wired.html');
  assertOfficialOnly(ui.query);
  assert.match(ui.query('#official-preview-status').textContent, /2026-10-09.*尚未/);
  assert.equal(ui.query('#open-preview').getAttribute('href'), 'https://catalog.test/official-drafts/wired.html');
  assert.equal(ui.query('#official-preview-link').target, '_blank');
  assert.equal(ui.query('#official-preview-link').rel, 'noopener');
});

test('late progress does not replace an explicitly selected original HTML preview', async t => {
  const ui = await fixture(t, 'wired');
  ui.query('[data-preview="html"]').click();
  assert.equal(ui.query('#preview-frame').getAttribute('src'), ui.original.html);
  ui.revealProgress();
  await settleUntil(() => ui.query('.official-drafts-count').textContent.includes('份草稿'));
  assert.equal(ui.query('#official-preview').hidden, true);
  assert.equal(ui.query('#preview-frame').hidden, false);
  assert.equal(ui.query('#preview-frame').getAttribute('src'), ui.original.html);
  assert.equal(ui.query('[data-preview="html"]').getAttribute('aria-pressed'), 'true');
  ui.query('[data-preview="official"]').click();
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
  assert.equal(ui.query('#official-preview-link').getAttribute('href'), 'official-progress.html');
  assert.equal(ui.query('#official-draft-note').hidden, true);
  ui.query('[data-preview="image"]').click();
  assert.equal(ui.query('#preview-image').getAttribute('src'), ui.original.image);
  assert.match(ui.query('#preview-caption').textContent, /原始/);
});

for (const slug of ['pinterest', 'vodafone']) {
  test(`${slug} opens its new official draft from the real published progress`, async t => {
    const ui = await fixture(t, slug);
    ui.revealProgress();
    await settleUntil(() => ui.query('#official-preview-link').getAttribute('href') === `official-drafts/${slug}.html`);
    assertOfficialOnly(ui.query);
    assert.match(ui.query('#official-preview-status').textContent, /2026-10-09.*尚未/);
    assert.match(ui.query('.official-drafts-count').textContent, /74 份草稿/);
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
  assert.equal(ui.query('#official-preview-link').getAttribute('href'), 'official-progress.html');
});

test('opening another brand resets an original preview choice to its official draft', async t => {
  const ui = await fixture(t, 'wired');
  ui.revealProgress();
  await settleUntil(() => ui.query('#official-preview-link').getAttribute('href') === 'official-drafts/wired.html');
  ui.query('[data-preview="html"]').click();
  ui.window.location.hash = '#/design/spotify';
  await settleUntil(() => ui.query('#official-preview-link').getAttribute('href') === 'official-drafts/spotify.html');
  assertOfficialOnly(ui.query);
  assert.equal(ui.query('#detail-title').textContent, 'Spotify');
});
