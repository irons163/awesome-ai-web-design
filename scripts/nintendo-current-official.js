/* Source-backed components refined from the preserved native Stitch document. */
(() => {
  let heroIndex = 0;
  let autoplay = null;
  const desktopNav = () => document.querySelector('nav[data-testid="desktop-nav"]');
  const activeHero = () => document.getElementById('center-stage');
  const clone = selector => document.querySelector(selector).content.firstElementChild.cloneNode(true);
  const playIcon = activeHero()?.querySelector('button[aria-label="Play"] svg')?.innerHTML;

  function updatePlayButton() {
    const button = activeHero()?.querySelector('button[aria-label="Play"],button[aria-label="Pause"]');
    if (!button) return;
    button.setAttribute('aria-label', autoplay ? 'Pause' : 'Play');
    const icon = button.querySelector('svg');
    if (icon) icon.innerHTML = autoplay
      ? '<rect x="10" y="7" width="4" height="18" fill="currentColor"/><rect x="18" y="7" width="4" height="18" fill="currentColor"/>'
      : playIcon;
  }

  function showHero(index, focus = false) {
    heroIndex = (index + 4) % 4;
    activeHero().replaceWith(clone('template[data-study-hero="' + heroIndex + '"]'));
    for (const panel of activeHero().querySelectorAll('[role="tabpanel"]')) {
      const box = panel.getBoundingClientRect();
      const visible = box.x + box.width / 2 > 0 && box.x + box.width / 2 < innerWidth;
      panel.setAttribute('aria-hidden', String(!visible));
      panel.inert = !visible;
    }
    updatePlayButton();
    if (focus) activeHero().querySelector('[role="tab"][aria-selected="true"]')?.focus({preventScroll: true});
  }

  function setNav(name) {
    const key = document.body.dataset.studyNavOpen === name ? 'closed' : name;
    desktopNav().replaceWith(clone('template[data-study-nav="' + key + '"]'));
    if (key === 'closed') delete document.body.dataset.studyNavOpen;
    else document.body.dataset.studyNavOpen = key;
    if (key === 'desktop_search') desktopNav().querySelector('input[type="text"]')?.focus();
  }

  function closeNav() {
    if (document.body.dataset.studyNavOpen) {
      desktopNav().replaceWith(clone('template[data-study-nav="closed"]'));
      delete document.body.dataset.studyNavOpen;
    }
    document.querySelector('.study-mobile-menu')?.remove();
  }

  function mobileSearch() {
    closeNav();
    const drawer = document.createElement('section');
    drawer.className = 'study-mobile-menu study-mobile-search';
    drawer.setAttribute('role', 'dialog');
    drawer.setAttribute('aria-label', 'Search');
    const close = document.createElement('button');
    close.textContent = 'Close'; close.dataset.studyClose = '';
    const heading = document.createElement('h2'); heading.textContent = 'Search';
    const observed = clone('template[data-study-nav="desktop_search"]');
    const form = observed.querySelector('form');
    if (!form) return;
    drawer.append(close, heading, form);
    document.body.append(drawer);
    drawer.querySelector('input[type="text"]')?.focus();
  }

  function mobileMenu() {
    if (document.querySelector('.study-mobile-menu')) return closeNav();
    const drawer = document.createElement('section');
    drawer.className = 'study-mobile-menu';
    drawer.setAttribute('role', 'dialog');
    drawer.setAttribute('aria-label', 'Main menu');
    const header = document.createElement('header');
    const title = document.createElement('strong');
    title.textContent = 'Nintendo';
    const close = document.createElement('button');
    close.textContent = 'Close'; close.dataset.studyClose = '';
    header.append(title, close); drawer.append(header);
    for (const [id, name] of [['explore-panel', 'Explore'], ['shop-panel', 'Shop'], ['support-panel', 'Support']]) {
      const h2 = document.createElement('h2'); h2.textContent = name; drawer.append(h2);
      for (const original of desktopNav().querySelectorAll('#' + id + ' a')) {
        const anchor = document.createElement('a');
        anchor.href = original.href;
        anchor.textContent = original.textContent.trim();
        if (anchor.textContent) drawer.append(anchor);
      }
    }
    document.body.append(drawer); close.focus();
  }

  function railFor(button) {
    let parent = button.parentElement;
    while (parent && parent !== document.body) {
      const rail = [...parent.querySelectorAll('div')].find(e =>
        e.clientWidth > 0 && e.scrollWidth > e.clientWidth + 4 &&
        ['auto', 'scroll', 'hidden'].includes(getComputedStyle(e).overflowX));
      if (rail) return {rail, widget: parent};
      parent = parent.parentElement;
    }
    return null;
  }

  function bindRails() {
    for (const button of document.querySelectorAll('#main button[aria-label="Next page"]')) {
      const found = railFor(button);
      if (!found) continue;
      const {rail, widget} = found;
      const update = () => {
        const before = widget.querySelector('button[aria-label="Previous page"]');
        const after = widget.querySelector('button[aria-label="Next page"]');
        if (before) before.disabled = rail.scrollLeft < 2;
        if (after) after.disabled = rail.scrollLeft >= rail.scrollWidth - rail.clientWidth - 2;
      };
      rail.addEventListener('scroll', update, {passive: true});
      update();
    }
  }

  document.addEventListener('click', event => {
    const button = event.target.closest('button');
    if (!button) return;
    const label = button.getAttribute('aria-label');
    const heroTab = button.closest('#center-stage [role="tab"]');
    if (heroTab) {
      event.preventDefault(); event.stopPropagation();
      showHero([...activeHero().querySelectorAll('[role="tab"]')].indexOf(heroTab), true);
    } else if (button.closest('#center-stage') && ['Play', 'Pause'].includes(label)) {
      if (autoplay) { clearInterval(autoplay); autoplay = null; }
      else autoplay = setInterval(() => showHero(heroIndex + 1), 7000);
      updatePlayButton();
    } else if (['explore-tab', 'shop-tab', 'support-tab'].includes(button.id)) {
      setNav('desktop_' + button.id.replace('-tab', ''));
    } else if (label === 'Search' && button.closest('nav[data-testid="mobile-nav"]')) {
      mobileSearch();
    } else if (button.id === 'search') {
      setNav('desktop_search');
    } else if (label === 'Main menu') {
      mobileMenu();
    } else if (label === 'Close' || button.hasAttribute('data-study-close')) {
      closeNav();
    } else if (['Previous page', 'Next page'].includes(label)) {
      event.preventDefault(); event.stopPropagation();
      const found = railFor(button);
      if (found) found.rail.scrollBy({left: (label === 'Next page' ? 1 : -1) * (found.rail.clientWidth - 32), behavior: 'smooth'});
    } else if (label === 'Account' || button.textContent.trim() === 'Log in / Sign up') {
      location.href = 'https://www.nintendo.com/en-ca/';
    }
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape') closeNav();
    const tab = event.target.closest('#center-stage [role="tab"]');
    if (tab && ['ArrowLeft', 'ArrowRight'].includes(event.key)) {
      event.preventDefault(); showHero(heroIndex + (event.key === 'ArrowRight' ? 1 : -1), true);
    }
  });
  showHero(0);
  bindRails();
})();
