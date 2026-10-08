(() => {
  const byId = id => document.getElementById(id);
  const drawerId = 'drawer_:R196:';
  const initialDrawer = byId(drawerId)?.cloneNode(true);
  const following = byId('study-following')?.content.firstElementChild.cloneNode(true);
  if (following) {
    following.hidden = true;
    following.setAttribute('data-study-hidden', '');
    byId('follows-panel')?.replaceWith(following);
  }
  const initialTabs = Object.fromEntries([...document.querySelectorAll('button[role="tab"]')].map(el => [el.id, Object.fromEntries([...el.attributes].map(a => [a.name, a.value]))]));
  const techButtonId = 'headlessui-disclosure-button-:R8cja2r96:';
  let returnFocus, oldOverflow = '';

  function closeDrawer() {
    const drawer = byId(drawerId);
    if (!drawer || drawer.hidden || !initialDrawer) return;
    drawer.replaceWith(initialDrawer.cloneNode(true));
    document.body.style.overflow = oldOverflow;
    returnFocus?.focus();
  }

  function bindDrawer(drawer) {
    drawer.querySelector('[aria-label="Close Drawer"]')?.addEventListener('click', closeDrawer);
    drawer.querySelectorAll('button[aria-expanded][aria-controls]').forEach(button => {
      const panel = byId(button.getAttribute('aria-controls'));
      if (!panel) return;
      panel.hidden = button.getAttribute('aria-expanded') !== 'true';
      button.addEventListener('click', () => {
        const expanded = button.getAttribute('aria-expanded') !== 'true';
        button.setAttribute('aria-expanded', String(expanded));
        button.setAttribute('data-headlessui-state', expanded ? 'open' : '');
        button.toggleAttribute('data-open', expanded);
        button.classList.toggle('_17jblij3', expanded);
        panel.hidden = !expanded;
        panel.setAttribute('data-headlessui-state', expanded ? 'open' : '');
        panel.toggleAttribute('data-open', expanded);
        panel.querySelector('ul')?.classList.toggle('_1044qizu', !expanded);
        if (button.id === techButtonId) {
          const source = byId(expanded ? 'study-drawer-tech' : 'study-drawer').content.querySelector(`[id="${techButtonId}"]`);
          button.setAttribute('aria-label', source.getAttribute('aria-label'));
          button.replaceChildren(...[...source.childNodes].map(node => node.cloneNode(true)));
        }
      });
    });
    drawer.querySelectorAll('input[type="checkbox"]').forEach(input => input.addEventListener('change', () => {
      drawer.querySelectorAll('input[type="checkbox"]').forEach(other => { other.checked = other === input; });
      const label = input.closest('label')?.textContent.trim().toLowerCase() || '';
      document.body.dataset.duetTheme = (label.includes('dark') || label.includes('system') && matchMedia('(prefers-color-scheme:dark)').matches) ? 'vergeDark' : 'vergeLight';
    }));
  }

  function openDrawer(opener) {
    const drawer = byId(drawerId);
    const template = byId('study-drawer');
    if (!drawer || !template) return;
    returnFocus = opener;
    oldOverflow = document.body.style.overflow;
    const opened = template.content.firstElementChild.cloneNode(true);
    drawer.replaceWith(opened);
    document.body.style.overflow = 'hidden';
    bindDrawer(opened);
    opened.querySelector('[aria-label="Close Drawer"]')?.focus();
  }
  [...document.querySelectorAll('button')].filter(button => button.getAttribute('aria-label') === 'Open Drawer' || button.querySelector('svg title')?.textContent === 'Hamburger Navigation Button').forEach(opener => {
    opener.addEventListener('click', () => openDrawer(opener));
  });
  document.addEventListener('keydown', event => { if (event.key === 'Escape') closeDrawer(); });

  const mobileTabs = matchMedia('(max-width:1179px)');
  const isMobile = () => mobileTabs.matches;
  function selectTab(name) {
    const river = byId('storyStream-panel')?.parentElement;
    const stories = byId('topStories-panel')?.parentElement;
    if (isMobile()) {
      river?.classList.toggle('_1044qizq', name === 'topStories');
      stories?.classList.toggle('_1044qizq', name !== 'topStories');
    } else {
      river?.classList.remove('_1044qizq');
      stories?.classList.remove('_1044qizq');
    }
    document.querySelectorAll('button[role="tab"]').forEach(tab => {
      const controls = tab.getAttribute('aria-controls');
      const selected = controls === (name === 'following' ? 'follows-panel' : name === 'topStories' ? 'topStories-panel' : 'storyStream-panel');
      tab.setAttribute('aria-selected', String(selected));
      const initial = initialTabs[tab.id];
      const base = (initial?.class || '_1cuypub6').split(' ').filter(c => !['_1cuypub8', '_1cuypub7'].includes(c));
      tab.className = [...base, ...(selected ? ['_1cuypub8', '_1cuypub7'] : [])].join(' ');
    });
    for (const [id, visible] of [['topStories-panel', !isMobile() || name === 'topStories'], ['storyStream-panel', name === 'latest'], ['follows-panel', name === 'following']]) {
      const panel = byId(id);
      if (!panel) continue;
      panel.hidden = !visible;
      panel.toggleAttribute('data-study-hidden', !visible);
    }
    history.replaceState(null, '', name === 'following' ? '#following' : name === 'topStories' ? '#topStories' : '#latest');
  }
  document.querySelectorAll('button[role="tab"]').forEach(tab => tab.addEventListener('click', () => {
    selectTab(tab.getAttribute('aria-controls') === 'follows-panel' ? 'following' : tab.getAttribute('aria-controls') === 'topStories-panel' ? 'topStories' : 'latest');
  }));
  if (isMobile()) selectTab('topStories');
  mobileTabs.addEventListener('change', () => selectTab(isMobile() ? 'topStories' : 'latest'));

  document.querySelector('[aria-label="Dismiss privacy notice"]')?.addEventListener('click', event => {
    event.currentTarget.closest('aside.duet--navigation--pmc-privacy-banner')?.remove();
  });
  document.querySelectorAll('button').forEach(button => {
    if (button.textContent.trim().toLowerCase() === 'done') button.addEventListener('click', () => { location.href = 'https://www.theverge.com/auth/login?returnPath=%2F'; });
    if (button.textContent.trim().toLowerCase() === 'see all latest') button.addEventListener('click', () => {
      selectTab('latest');
      byId('mobile-latest-tab')?.scrollIntoView({block: 'start'});
    });
  });
  document.querySelectorAll('#follows-panel li button').forEach(button => button.addEventListener('click', () => {
    location.href = 'https://www.theverge.com/auth/login?returnPath=%2F';
  }));
})();
