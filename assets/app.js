'use strict';
const $ = selector => document.querySelector(selector);
const escapeHTML = value => String(value).replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
const downloadURL = href => `${href}?download=1`;
const STORAGE_KEY = 'awesome-ai-web-design:favorites:v1';
const FEATURED = ['claude','linear.app','stripe','notion','vercel','supabase','figma','apple','spotify'];
let OFFICIAL_DRAFTS = {};
let officialDraftsState = 'loading', officialDraftDates = {}, officialStudies = {};
let designs = [], category = 'all', savedOnly = false, currentDesign = null, currentTab = 'preview', previewMode = 'official';
let startPrompt = '';
let copyIntro = '', combinedReference = '', combinedSource = '', combinedRequest = 0, combinedState = 'idle';
const studyTextRequests = new Map();
let documentText = '', documentSource = '', documentRequest = 0, currentPromptText = '', currentPromptSource = '', currentPromptRequest = 0, toastTimer, lastFocused, returningHash = '#collection';
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
  return `<article class="design-card" data-design="${escapeHTML(item.slug)}"><a href="#/design/${encodeURIComponent(item.slug)}" class="card-link" aria-label="查看 ${escapeHTML(item.name)} 設計">${cardArt(item)}<div class="card-body"><div class="card-name-row"><h3>${escapeHTML(item.name)}</h3><span class="card-open" aria-hidden="true">↗</span></div><p class="card-description">${escapeHTML(item.description)}</p><div class="card-meta"><span class="card-category">${escapeHTML(item.categoryLabel)}</span><span class="card-palette" aria-hidden="true">${item.colors.slice(0,4).map(color => `<i style="background:${escapeHTML(color)}"></i>`).join('')}</span></div></div></a><button class="save-button" data-save="${escapeHTML(item.slug)}" aria-label="${picked ? '取消收藏' : '收藏'} ${escapeHTML(item.name)}" aria-pressed="${picked}"><svg class="ui-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1.1-1.1a5.5 5.5 0 0 0-7.8 7.8L12 21l8.8-8.6a5.5 5.5 0 0 0 0-7.8Z"/></svg></button></article>`;
}
function cardArt(item) {
  const cover=officialStudies[item.slug]?.cover;
  return cover?`<div class="card-art"><img src="${escapeHTML(cover)}" alt="${escapeHTML(item.name)} 設計預覽，與完整預覽相同的研究版本" loading="lazy" decoding="async" width="800" height="450"></div>`:
    `<div class="card-art pending-art"><span>${escapeHTML(item.name)}</span><small>${officialDraftsState==='loading'?'預覽準備中':'預覽暫時無法載入'}</small></div>`;
}
function refreshCardArt() {
  document.querySelectorAll('[data-hero-cover]').forEach(image=>{
    const cover=officialStudies[image.dataset.heroCover]?.cover;
    image.hidden=!cover;
    if(cover)image.src=cover;
    else image.removeAttribute('src');
  });
  document.querySelectorAll('[data-design]').forEach(card=>{
    const item=designs.find(item=>item.slug===card.dataset.design);
    if(item)card.querySelector('.card-art').outerHTML=cardArt(item);
  });
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
  if (!text) { toast('內容尚未載入，請稍後再試。'); return false; }
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
    return true;
  } catch {
    toast('瀏覽器無法存取剪貼簿，請選取下方文字複製，或下載檔案。');
    return false;
  }
}
function readStudyText(href) {
  if (!studyTextRequests.has(href)) {
    const request = (async () => {
      const response = await fetch(href);
      if (!response.ok) throw new Error('Study document unavailable');
      const text = await response.text();
      if (!text.trim()) throw new Error('Empty study document');
      return text;
    })().catch(error => { studyTextRequests.delete(href); throw error; });
    studyTextRequests.set(href, request);
  }
  return studyTextRequests.get(href);
}
async function loadCombinedReference() {
  const item = currentDesign, study = officialStudies[item?.slug];
  if (!item || !study?.links.analysis || !study?.links.prompts || !copyIntro) return;
  const source = JSON.stringify([item.slug, study.links.analysis, study.links.prompts]);
  if (source === combinedSource && ['loading','ready'].includes(combinedState)) return;
  const request = ++combinedRequest;
  combinedSource = source; combinedReference = ''; combinedState = 'loading';
  const button = $('#copy-full-reference');
  button.disabled = true; button.textContent = '準備複製內容…';
  $('#reference-load-status').textContent = '正在讀取完整設計規格與 AI 指令…';
  $('#combined-reference-text').textContent = '';
  try {
    const [design, prompt] = await Promise.all([readStudyText(study.links.analysis), readStudyText(study.links.prompts)]);
    if (request !== combinedRequest || currentDesign?.slug !== item.slug || combinedSource !== source) return;
    combinedReference = `# ${item.name} 網站製作參考\n\n${copyIntro}\n\n---\n\n## DESIGN.md｜完整設計規格\n\n${design.trimEnd()}\n\n---\n\n## PROMPTS.md｜完整 AI 實作指令\n\n${prompt.trimEnd()}\n`;
    combinedState = 'ready';
    $('#combined-reference-text').textContent = combinedReference;
    $('#reference-load-status').textContent = '已包含兩份完整文件，可直接貼給 AI，並填入自己的需求。';
    button.disabled = false; button.textContent = '一次複製給 AI';
  } catch {
    if (request !== combinedRequest || currentDesign?.slug !== item.slug) return;
    combinedState = 'error';
    button.disabled = false; button.textContent = '重新載入複製內容';
    $('#reference-load-status').textContent = '複製版暫時無法載入，請按「重新載入複製內容」重試，或下載簡易包。';
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
  if (name === 'document') loadDocument();
  if (name === 'prompts') loadCurrentPrompt();
}
function setPreview(view) {
  previewMode = view;
  const preview = currentDesign.preview;
  const ready = preview.status === 'generated';
  const modified = preview.modified === true;
  $('.history-description').textContent = modified
    ? '此設計由 Google Stitch 網頁版生成，公開預覽經修改並重新截圖；原始輸出摘要及修改說明見生成紀錄。'
    : '延伸規格與三則任務指令已改為台灣繁體中文；Google Stitch 原始預覽與截圖保留來源原貌。';
  $('[data-preview="image"]').textContent = modified ? '調整後截圖' : '初稿截圖';
  $('[data-preview="html"]').textContent = modified ? '調整後 HTML' : '初稿 HTML';
  $('#open-generation-preview').textContent = modified ? '開啟調整後預覽 ↗' : '開啟 AI 初稿 ↗';
  $('#download-html').textContent = modified ? '下載調整後 HTML ↗' : '下載初稿 HTML ↗';
  $('#preview-actions .preview-note').textContent = modified
    ? '此預覽由 Stitch 生成後經人工調整，部分操作及資料為示範。'
    : '此處保留早期生成範例，部分按鈕與資料為展示內容。';
  const official = view === 'official' || !$('#creation-history').open;
  const draft = OFFICIAL_DRAFTS[currentDesign.slug];
  $('#official-preview').hidden = false;
  const study = officialStudies[currentDesign.slug];
  $('#preview-caption').textContent = '設計預覽';
  $('#preview-pending').hidden = official || ready;
  $('#preview-image').hidden = official || !ready || view !== 'image';
  $('#preview-frame').hidden = official || !ready || view !== 'html';
  $('#preview-actions').hidden = official || !ready;
  document.querySelectorAll('[data-preview="image"],[data-preview="html"]').forEach(button => { button.hidden = !ready; });
  {
    const status = $('#official-preview-status');
    const link = $('#official-preview-link');
    const hasDraft = !!draft;
    if (hasDraft) {
      status.textContent = `參考日期：${officialDraftDates[currentDesign.slug]}`;
      link.href = `official-drafts/${draft}.html`;
      link.textContent = `開啟 ${currentDesign.name} 完整預覽 ↗`;
    } else {
      status.textContent = officialDraftsState === 'loading' ? '正在讀取預覽…' :
        officialDraftsState === 'error' ? '預覽暫時無法載入，請查看參考來源。' : '此設計尚無可開啟的完整預覽。';
      link.href = 'reference-sources.html';
      link.textContent = '查看參考來源 ↗';
    }
    $('#open-preview').href = link.href;
    $('#open-preview').textContent = hasDraft ? '開啟完整預覽 ↗' : '查看參考來源 ↗';
    const image=$('#current-preview-image');
    image.hidden=!hasDraft||!study?.cover;
    if(!image.hidden){image.src=study.cover;image.alt=`${currentDesign.name} 設計預覽，參考日期 ${officialDraftDates[currentDesign.slug]}`;}
    else image.removeAttribute('src');
  }
  if (official) {
    $('#preview-frame').removeAttribute('src');
    $('#preview-image').removeAttribute('src');
  } else if (ready) {
    $('#preview-image').src = preview.image;
    $('#preview-image').alt = `${currentDesign.name} 風格：${preview.title}，${modified ? '調整後的預覽截圖' : 'Google Stitch 原始生成截圖'}`;
    if (view === 'html') $('#preview-frame').src = preview.html;
    else $('#preview-frame').removeAttribute('src');
    $('#preview-frame').title = `${currentDesign.name} — Stitch 生成的 HTML 頁面`;
    $('#open-generation-preview').href = preview.html;
    $('#download-html').href = downloadURL(preview.html);
    $('#generation-record').href = preview.provenance;
    $('#generation-prompt').href = downloadURL(preview.prompt);
  } else {
    $('#preview-frame').removeAttribute('src');
    $('#preview-image').removeAttribute('src');
  }
  $('#open-preview').hidden = false;
  document.querySelectorAll('[data-preview]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.preview === view)));
}

async function loadDocument() {
  if (!currentDesign) return;
  const slug = currentDesign.slug, href = officialStudies[slug]?.links.analysis;
  if (documentSource === href && documentText) return;
  const request = ++documentRequest;
  documentText = ''; documentSource = href || '';
  $('#copy-document').disabled = true;
  $('#document-text').textContent = officialDraftsState === 'loading' ? '正在讀取這份預覽的設計規格…' : '這份預覽的設計規格暫時無法載入，請重新整理頁面。原始分析可在製作紀錄查看。';
  if (!href) return;
  $('#document-text').textContent = '正在讀取設計規格…';
  try {
    const text = await readStudyText(href);
    if (request !== documentRequest || currentDesign?.slug !== slug || officialStudies[slug]?.links.analysis !== href) return;
    documentText = text; $('#document-text').textContent = text; $('#copy-document').disabled = false;
  } catch {
    if (request !== documentRequest || currentDesign?.slug !== slug) return;
    $('#document-text').textContent = '無法載入檔案。請切換分頁再重試，或使用上方下載按鈕。';
  }
}
function openDesign(item) {
  if (currentDesign?.slug === item.slug && $('#design-dialog').open) return;
  lastFocused = document.activeElement;
  documentRequest++; currentPromptRequest++; documentText = ''; documentSource = ''; currentPromptText = ''; currentPromptSource = ''; currentDesign = item;
  combinedRequest++; combinedReference = ''; combinedSource = ''; combinedState = 'idle';
  $('#copy-full-reference').disabled = true; $('#copy-full-reference').textContent = '一次複製給 AI';
  $('#combined-reference-text').textContent = ''; $('#reference-load-status').textContent = '正在準備規格與指令…';
  $('#detail-title').textContent = item.name;
  $('#detail-description').textContent = item.description;
  $('#detail-category').textContent = item.categoryLabel;
  const originalAnalysis = `design-md/${encodeURIComponent(item.slug)}/DESIGN.md`;
  $('#original-design-link').href = originalAnalysis;
  $('#download-original-design').href = downloadURL(originalAnalysis);
  $('#download-original-design').download = `${item.slug}-original-DESIGN.md`;
  $('#download-original-prompts').href = downloadURL(`design-md/${encodeURIComponent(item.slug)}/PROMPTS.md`);
  $('#download-original-prompts').download = `${item.slug}-original-PROMPTS.md`;
  $('#prompt-list').innerHTML = item.prompts.map((prompt,index) => `<article class="prompt-card"><div class="prompt-heading"><h3>${String(index+1).padStart(2,'0')} / ${escapeHTML(prompt.title)}</h3><button class="button secondary" data-copy-prompt="${index}" aria-label="複製${escapeHTML(prompt.title)}指令">複製指令 ↗</button></div><pre tabindex="0">${escapeHTML(prompt.text)}</pre></article>`).join('');
  $('#creation-history').open=false;
  $('#original-prompt-details').open=false;
  $('#individual-downloads').open=false;
  $('#copy-reference-details').open=false;
  $('#download-usage').open=false;
  $('#document-text').textContent = ''; $('#current-prompt-text').textContent = '';
  $('#copy-document').disabled = true; $('#copy-current-prompt').disabled = true;
  setTab('preview'); setPreview('official');
  showOfficialDraft(item);
  if (!$('#design-dialog').open) $('#design-dialog').showModal();
  $('#design-dialog').scrollTop = 0;
  $('#close-dialog').focus();
  document.title = `${item.name} — Awesome AI Web Design`;
}
function showOfficialDraft(item) {
  const study = officialStudies[item.slug];
  const sourceLink = $('#official-study-source');
  const hasSource = /^https?:\/\//i.test(study?.source || '');
  $('#official-study-details').hidden = !hasSource;
  sourceLink.textContent = `${item.name} 官網 ↗`;
  if (hasSource) sourceLink.href = study.source;
  else sourceLink.removeAttribute('href');
  for (const [selector, kind, filename] of [['#download-design','analysis','DESIGN.md'],['#download-prompts','prompts','PROMPTS.md']]) {
    const link = $(selector), href = study?.links[kind];
    link.hidden = !href;
    if (href) { link.href = downloadURL(href); link.download = `${item.slug}-${filename}`; }
    else link.removeAttribute('href');
  }
  const pack = $('#download-implementation-pack');
  pack.hidden = !study?.implementationVersion;
  const simple = $('#download-simple-pack');
  simple.hidden = pack.hidden || !study?.links.analysis || !study?.links.prompts;
  if (!simple.hidden) {
    simple.href = `assets/design-packs/${encodeURIComponent(item.slug)}-simple.zip`;
    simple.download = `${item.slug}-simple.zip`;
    simple.setAttribute('aria-label', `下載 ${item.name} 簡易包`);
  } else simple.removeAttribute('href');
  $('#usage-content').hidden = simple.hidden;
  $('#copy-start-prompt').disabled = simple.hidden || !startPrompt;
  $('#pack-status').textContent = simple.hidden ? (officialDraftsState === 'loading' ? '正在準備設計參考…' : '設計參考暫時無法載入，請重新整理頁面。') : '只需兩份文件 · 下載或複製，選一種就好';
  if (!pack.hidden) { pack.href = `assets/design-packs/${encodeURIComponent(item.slug)}.zip`; pack.download = `${item.slug}-design-pack.zip`; }
  else pack.removeAttribute('href');
  const reference = study ? `參考日期：${study.date}${study.implementationVersion ? ` · 實作規格 ${study.implementationVersion}` : ''}` : officialDraftsState === 'loading' ? '正在讀取預覽對應內容…' : '參考紀錄暫時無法載入';
  $('#document-reference').textContent = reference;
  $('#prompt-reference').textContent = reference;
  if (currentTab === 'document') loadDocument();
  if (currentTab === 'prompts') loadCurrentPrompt();
  if (!simple.hidden) loadCombinedReference();
}
async function loadCurrentPrompt() {
  if (!currentDesign) return;
  const slug = currentDesign?.slug, href = officialStudies[slug]?.links.prompts;
  if (currentPromptSource === href && currentPromptText) return;
  const request = ++currentPromptRequest;
  currentPromptText = ''; currentPromptSource = href || '';
  $('#copy-current-prompt').disabled = true;
  $('#current-prompt-text').textContent = officialDraftsState === 'loading' ? '正在讀取這份預覽的 AI 指令…' : '這份預覽的 AI 指令暫時無法載入，請重新整理頁面。原始指令可在製作紀錄查看。';
  if (!href) return;
  $('#current-prompt-text').textContent = '正在讀取 AI 指令…';
  try {
    const text = await readStudyText(href);
    if (currentDesign?.slug !== slug || request !== currentPromptRequest || officialStudies[slug]?.links.prompts !== href) return;
    // Keep the exact dated prompt, including any recorded transcription fix.
    currentPromptText = text;
    $('#current-prompt-text').textContent = text;
    $('#copy-current-prompt').disabled = false;
  } catch {
    if (request !== currentPromptRequest || currentDesign?.slug !== slug) return;
    $('#current-prompt-text').textContent = '目前無法讀取指令，請使用下載連結。';
  }
}
function dismiss() {
  documentRequest++; currentPromptRequest++;
  combinedRequest++;
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
    if (data.count !== data.designs.length) throw new Error('Catalog count does not match its designs');
    document.querySelectorAll('[data-design-count]').forEach(element => { element.textContent = String(data.count); });
    startPrompt = typeof data.startPrompt === 'string' ? data.startPrompt : '';
    copyIntro = typeof data.copyIntro === 'string' ? data.copyIntro : '';
    $('#start-prompt').textContent = startPrompt || '使用說明暫時無法載入；下載設計包後，可依包內 README.md 開始使用。';
    $('#stitch-count').textContent = `${data.count} 套免費設計參考`;
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
async function loadOfficialDrafts() {
  const grid = $('.official-draft-grid');
  const count = $('.official-drafts-count');
  try {
    const response = await fetch('official-progress.html');
    if (!response.ok) throw new Error('Progress unavailable');
    const page = new DOMParser().parseFromString(await response.text(), 'text/html');
    const drafts = [...page.querySelectorAll('tbody tr')].flatMap(row => {
      if (!row.querySelector('td.draft')) return [];
      const link = row.querySelector('th a');
      const match = /^official-drafts\/([a-z0-9.-]+)\.html$/.exec(link?.getAttribute('href') || '');
      if (!match) return [];
      return [{
        slug: match[1] === 'linear' ? 'linear.app' : match[1],
        file: match[1],
        name: link.textContent.replace(/\s*↗\s*$/, '').trim(),
        date: row.querySelector('td:last-child')?.textContent.trim() || '日期未記錄',
        status: row.dataset.status || 'unverified',
        cover: /^assets\/current-previews\/[a-z0-9.-]+-[a-f0-9]{16}\.webp$/.test(row.dataset.cover || '')?row.dataset.cover:null,
        source: row.querySelector('.study-source')?.getAttribute('href') || '',
        implementationVersion: /^\d{4}-\d{2}-\d{2}$/.test(row.dataset.implementationVersion || '') ? row.dataset.implementationVersion : null,
        links: Object.fromEntries(['analysis','prompts','review'].flatMap(key => {
          const href = row.querySelector(`.study-${key}`)?.getAttribute('href');
          return /^official-drafts\/[a-z0-9.-]+\.md$/.test(href || '') ? [[key, href]] : [];
        })),
      }];
    });
    if (!drafts.length) throw new Error('No draft records');
    OFFICIAL_DRAFTS = Object.fromEntries(drafts.map(item => [item.slug, item.file]));
    officialDraftDates = Object.fromEntries(drafts.map(item => [item.slug, item.date]));
    officialStudies = Object.fromEntries(drafts.map(item => [item.slug, item]));
    officialDraftsState = 'ready';
    refreshCardArt();
    count.textContent = `${drafts.length} 份參考來源`;
    grid.innerHTML = drafts.map(item =>
      `<a href="official-drafts/${escapeHTML(item.file)}.html">${escapeHTML(item.name)} <span>${escapeHTML(item.date)} ↗</span></a>`
    ).join('');
    if (currentDesign) {
      showOfficialDraft(currentDesign);
      setPreview(previewMode);
    }
  } catch {
    officialDraftsState = 'error';
    count.textContent = '參考來源暫時無法載入';
    refreshCardArt();
    grid.innerHTML = '<a href="reference-sources.html">查看參考來源 ↗</a>';
    if (currentDesign) { showOfficialDraft(currentDesign); setPreview(previewMode); }
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
  const tabs = [...document.querySelectorAll('[data-tab]')].map(tab => tab.dataset.tab); let next = tabs.indexOf(currentTab);
  if (event.key === 'ArrowRight') next = (next+1)%3;
  else if (event.key === 'ArrowLeft') next = (next+2)%3;
  else if (event.key === 'Home') next = 0;
  else if (event.key === 'End') next = 2;
  else return;
  event.preventDefault(); setTab(tabs[next], true);
});
$('#creation-history').addEventListener('click', event => { const button = event.target.closest('[data-preview]'); if (button) setPreview(button.dataset.preview); });
$('#creation-history').addEventListener('toggle',()=>{if(currentDesign)setPreview($('#creation-history').open?(previewMode==='official'?'image':previewMode):'official');});
$('#copy-document').addEventListener('click', event => copyText(documentText, event.currentTarget));
$('#copy-current-prompt').addEventListener('click', event => copyText(currentPromptText, event.currentTarget));
$('#copy-start-prompt').addEventListener('click', event => copyText(startPrompt, event.currentTarget));
$('#download-simple-pack').addEventListener('click', () => { if (currentDesign) { setTab('prompts'); $('#download-usage').open = true; } });
$('#copy-full-reference').addEventListener('click', async event => {
  if (!currentDesign) return;
  setTab('prompts');
  if (!combinedReference) { $('#copy-reference-details').open = true; loadCombinedReference(); return; }
  const slug = currentDesign.slug;
  if (!await copyText(combinedReference, event.currentTarget) && currentDesign?.slug === slug) {
    $('#copy-reference-details').open = true;
    $('#combined-reference-text').focus();
  }
});
$('#prompt-list').addEventListener('click', event => { const button = event.target.closest('[data-copy-prompt]'); if (button) copyText(currentDesign.prompts[Number(button.dataset.copyPrompt)].text, button); });
window.addEventListener('hashchange', route);
window.addEventListener('storage', event => {
  if (event.key !== STORAGE_KEY && event.key !== null) return;
  try { const value = JSON.parse(event.newValue || '[]'); saved = new Set(Array.isArray(value) ? value.filter(slug => designs.some(item => item.slug === slug)) : []); render(); } catch { /* Ignore malformed data from another tab. */ }
});
document.addEventListener('keydown', event => { if (event.key === '/' && !event.metaKey && !event.ctrlKey && !$('#design-dialog').open && !['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName)) { event.preventDefault(); $('#search').focus(); } });
loadCatalog();
loadOfficialDrafts();
