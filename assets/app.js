'use strict';
const $ = selector => document.querySelector(selector);
const escapeHTML = value => String(value).replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
const STORAGE_KEY = 'awesome-ai-web-design:favorites:v1';
const FEATURED = ['claude','linear.app','stripe','notion','vercel','supabase','figma','apple','spotify'];
let designs = [], category = 'all', savedOnly = false, currentDesign = null, currentTab = 'preview', previewMode = 'image';
let documentText = '', documentRequest = 0, toastTimer, lastFocused, returningHash = '#collection';
let saved;
try { const value = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]'); saved = new Set(Array.isArray(value) ? value.filter(x => typeof x === 'string') : []); }
catch { saved = new Set(); }

function toast(message) {
  $('#toast').textContent = message;
  $('#toast').classList.add('visible');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => $('#toast').classList.remove('visible'), 3200);
}
function saveFavorites() {
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify([...saved])); }
  catch { toast('本次收藏已更新；瀏覽器目前無法保存至下次使用。'); }
}
function renderCategories(categories) {
  const buttons = [['all','全部設計'], ...Object.entries(categories)];
  $('#categories').innerHTML = buttons.map(([key,label]) => `<button class="category" data-category="${escapeHTML(key)}" aria-pressed="${category === key}"><span>${escapeHTML(label)}</span><span>${key === 'all' ? designs.length : designs.filter(item => item.category === key).length}</span></button>`).join('');
}
function card(item) {
  const picked = saved.has(item.slug);
  const preview = item.preview;
  const art = preview.status === 'generated'
    ? `<div class="card-art"><img src="${escapeHTML(preview.thumbnail)}" alt="${escapeHTML(item.name)} 風格的 Stitch 生成頁面" loading="lazy" decoding="async" width="${preview.width}" height="${preview.height}"><span class="stitch-badge">STITCH</span></div>`
    : `<div class="card-art pending-art"><span>${escapeHTML(item.name)}</span><small>Stitch 範例待生成</small></div>`;
  return `<article class="design-card"><a href="#/design/${encodeURIComponent(item.slug)}" class="card-link" aria-label="查看 ${escapeHTML(item.name)} 設計">${art}<div class="card-body"><div class="card-name-row"><h3>${escapeHTML(item.name)}</h3><span>↗</span></div><p class="card-description">${escapeHTML(item.description)}</p><div class="card-meta"><span>${escapeHTML(item.categoryLabel)}</span><span class="card-palette" aria-hidden="true">${item.colors.slice(0,4).map(color => `<i style="background:${escapeHTML(color)}"></i>`).join('')}</span></div></div></a><button class="save-button" data-save="${escapeHTML(item.slug)}" aria-label="${picked ? '取消收藏' : '收藏'} ${escapeHTML(item.name)}" aria-pressed="${picked}">${picked ? '♥' : '♡'}</button></article>`;
}
function render() {
  const query = $('#search').value.trim().toLocaleLowerCase();
  const mode = $('#mode').value;
  const results = designs.filter(item => (category === 'all' || item.category === category) && (mode === 'all' || item.mode === mode) && (!savedOnly || saved.has(item.slug)) && `${item.name} ${item.slug} ${item.description} ${item.categoryLabel} ${item.category} ${item.brief}`.toLocaleLowerCase().includes(query));
  $('#catalog').innerHTML = results.map(card).join('');
  $('#result-count').textContent = `${results.length} 套設計${query ? ` ·「${$('#search').value.trim()}」` : ''}`;
  $('#saved-count').textContent = saved.size;
  $('#empty').hidden = results.length > 0;
  $('#favorites-filter').setAttribute('aria-pressed', String(savedOnly));
  document.querySelectorAll('[data-category]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.category === category)));
}
function resetFilters() {
  category = 'all'; savedOnly = false; $('#search').value = ''; $('#mode').value = 'all'; render();
}
async function copyText(text, button) {
  if (!text) { toast('內容尚未載入，請稍後再試。'); return; }
  try {
    if (navigator.clipboard?.writeText) { await navigator.clipboard.writeText(text); }
    else {
      const input = document.createElement('textarea');
      input.value = text; input.style.position = 'fixed'; input.style.opacity = '0';
      const parent = $('#design-dialog').open ? $('#design-dialog') : document.body;
      parent.append(input); input.select();
      const ok = document.execCommand('copy'); input.remove();
      if (!ok) throw new Error('Clipboard unavailable');
    }
    toast('已複製，可以貼到你的 AI 工具。');
    button?.focus();
  } catch {
    toast('瀏覽器無法存取剪貼簿，請選取下方文字複製，或下載檔案。');
  }
}
function setTab(name, focus = false) {
  currentTab = name;
  document.querySelectorAll('[data-tab]').forEach(button => {
    const active = button.dataset.tab === name;
    button.setAttribute('aria-selected', String(active)); button.tabIndex = active ? 0 : -1;
    if (active && focus) button.focus();
  });
  ['preview','document','prompts'].forEach(id => { $(`#panel-${id}`).hidden = id !== name; });
  if (name === 'document' && !documentText) loadDocument();
}
function setPreview(view) {
  previewMode = view;
  const preview = currentDesign.preview;
  const ready = preview.status === 'generated';
  $('#preview-pending').hidden = ready;
  $('#preview-image').hidden = !ready || view !== 'image';
  $('#preview-frame').hidden = !ready || view !== 'html';
  $('#preview-actions').hidden = !ready;
  $('#preview-controls').hidden = !ready;
  if (ready) {
    $('#preview-image').src = preview.image;
    $('#preview-image').alt = `${currentDesign.name} 風格：${preview.title}，Google Stitch 原始生成截圖`;
    if (view === 'html') $('#preview-frame').src = preview.html;
    else $('#preview-frame').removeAttribute('src');
    $('#preview-frame').title = `${currentDesign.name} — Stitch 生成的 HTML 頁面`;
    $('#open-preview').href = preview.html;
    $('#download-html').href = preview.html;
    $('#generation-record').href = preview.provenance;
    $('#generation-prompt').href = preview.prompt;
  } else {
    $('#preview-frame').removeAttribute('src');
    $('#preview-image').removeAttribute('src');
  }
  $('#open-preview').hidden = !ready;
  document.querySelectorAll('[data-preview]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.preview === view)));
}

async function loadDocument() {
  const request = ++documentRequest;
  const slug = currentDesign.slug;
  $('#document-text').textContent = '讀取完整文件中…';
  $('#copy-document').disabled = true;
  try {
    const response = await fetch(`design-md/${encodeURIComponent(slug)}/DESIGN.md`);
    if (!response.ok) throw new Error('Document unavailable');
    const text = await response.text();
    if (request !== documentRequest || currentDesign?.slug !== slug) return;
    documentText = text; $('#document-text').textContent = text; $('#copy-document').disabled = false;
  } catch {
    if (request !== documentRequest) return;
    $('#document-text').textContent = '無法載入文件。請切換分頁再重試，或使用上方下載按鈕。';
  }
}
function openDesign(item) {
  if (currentDesign?.slug === item.slug && $('#design-dialog').open) return;
  lastFocused = document.activeElement;
  documentRequest++; documentText = ''; currentDesign = item;
  $('#detail-title').textContent = item.name;
  $('#detail-description').textContent = item.description;
  $('#detail-category').textContent = item.categoryLabel;
  $('#download-design').href = `design-md/${encodeURIComponent(item.slug)}/DESIGN.md`;
  $('#download-design').download = `${item.slug}-DESIGN.md`;
  $('#download-prompts').href = `design-md/${encodeURIComponent(item.slug)}/PROMPTS.md`;
  $('#download-prompts').download = `${item.slug}-PROMPTS.md`;
  $('#prompt-list').innerHTML = item.prompts.map((prompt,index) => `<article class="prompt-card"><div class="prompt-heading"><h3>${String(index+1).padStart(2,'0')} / ${escapeHTML(prompt.title)}</h3><button class="button secondary" data-copy-prompt="${index}" aria-label="複製${escapeHTML(prompt.title)}指令">複製指令 ↗</button></div><pre tabindex="0">${escapeHTML(prompt.text)}</pre></article>`).join('');
  setTab('preview'); setPreview('image');
  if (!$('#design-dialog').open) $('#design-dialog').showModal();
  $('#design-dialog').scrollTop = 0;
  $('#close-dialog').focus();
  document.title = `${item.name} — Awesome AI Web Design`;
}
function dismiss() {
  documentRequest++;
  if ($('#design-dialog').open) $('#design-dialog').close();
  currentDesign = null;
  document.title = 'Awesome AI Web Design — 免費設計參考集';
  if (lastFocused?.isConnected) lastFocused.focus({preventScroll:true});
}
function closeDesign() {
  history.replaceState(null, '', location.pathname + location.search + returningHash);
  dismiss();
}
function route() {
  if (!designs.length) return;
  if (location.hash.startsWith('#/design/')) {
    let slug;
    try { slug = decodeURIComponent(location.hash.slice('#/design/'.length)); }
    catch { toast('設計連結格式有誤。'); closeDesign(); return; }
    const item = designs.find(entry => entry.slug === slug);
    if (item) openDesign(item);
    else { toast('找不到這份設計，請從目錄重新選擇。'); closeDesign(); }
  } else { returningHash = location.hash || '#collection'; dismiss(); }
}
async function loadCatalog() {
  $('#load-error').hidden = true;
  $('#result-count').textContent = '載入設計中…';
  try {
    const response = await fetch('assets/catalog.json');
    if (!response.ok) throw new Error('Catalog unavailable');
    const data = await response.json();
    if (!Array.isArray(data.designs) || !data.designs.length) throw new Error('Invalid catalog');
    $('#stitch-count').textContent = `${data.generatedCount} / ${data.count} 個 Stitch 生成範例`;
    designs = data.designs.sort((a,b) => {
      const first = FEATURED.indexOf(a.slug), second = FEATURED.indexOf(b.slug);
      return (first < 0 ? 100 : first) - (second < 0 ? 100 : second) || a.name.localeCompare(b.name);
    });
    saved = new Set([...saved].filter(slug => designs.some(item => item.slug === slug)));
    renderCategories(data.categories); render(); route();
  } catch {
    $('#result-count').textContent = '載入失敗'; $('#load-error').hidden = false; $('#empty').hidden = true;
  }
}
$('#search').addEventListener('input', render);
$('#mode').addEventListener('change', render);
$('#clear-filters').addEventListener('click', resetFilters);
$('#retry').addEventListener('click', loadCatalog);
$('#favorites-filter').addEventListener('click', () => { savedOnly = !savedOnly; render(); });
$('#categories').addEventListener('click', event => { const button = event.target.closest('[data-category]'); if (button) { category = button.dataset.category; render(); } });
$('#catalog').addEventListener('click', event => {
  const button = event.target.closest('[data-save]');
  if (!button) return;
  const slug = button.dataset.save;
  saved.has(slug) ? saved.delete(slug) : saved.add(slug);
  saveFavorites(); render();
  const replacement = [...document.querySelectorAll('[data-save]')].find(element => element.dataset.save === slug);
  (replacement || $('#favorites-filter')).focus({preventScroll:true});
});
$('#close-dialog').addEventListener('click', closeDesign);
$('#design-dialog').addEventListener('cancel', event => { event.preventDefault(); closeDesign(); });
$('#design-dialog').addEventListener('click', event => { if (event.target === $('#design-dialog')) { const rect = event.target.getBoundingClientRect(); if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) closeDesign(); } });
$('.detail-tabs').addEventListener('click', event => { const tab = event.target.closest('[data-tab]'); if (tab) setTab(tab.dataset.tab); });
$('.detail-tabs').addEventListener('keydown', event => {
  const tabs = ['preview','document','prompts']; let next = tabs.indexOf(currentTab);
  if (event.key === 'ArrowRight') next = (next+1)%3;
  else if (event.key === 'ArrowLeft') next = (next+2)%3;
  else if (event.key === 'Home') next = 0;
  else if (event.key === 'End') next = 2;
  else return;
  event.preventDefault(); setTab(tabs[next], true);
});
$('.preview-toolbar').addEventListener('click', event => { const button = event.target.closest('[data-preview]'); if (button) setPreview(button.dataset.preview); });
$('#copy-document').addEventListener('click', event => copyText(documentText, event.currentTarget));
$('#prompt-list').addEventListener('click', event => { const button = event.target.closest('[data-copy-prompt]'); if (button) copyText(currentDesign.prompts[Number(button.dataset.copyPrompt)].text, button); });
window.addEventListener('hashchange', route);
window.addEventListener('storage', event => {
  if (event.key !== STORAGE_KEY && event.key !== null) return;
  try { const value = JSON.parse(event.newValue || '[]'); saved = new Set(Array.isArray(value) ? value.filter(slug => designs.some(item => item.slug === slug)) : []); render(); } catch { /* Ignore malformed data from another tab. */ }
});
document.addEventListener('keydown', event => { if (event.key === '/' && !event.metaKey && !event.ctrlKey && !$('#design-dialog').open && !['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName)) { event.preventDefault(); $('#search').focus(); } });
loadCatalog();
