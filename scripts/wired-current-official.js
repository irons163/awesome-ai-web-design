(() => {
  'use strict';
  const ui = JSON.parse(document.getElementById('study-wired-ui').textContent);
  const toggles = [...document.querySelectorAll('span[role="button"][data-testid="hamburger_menu"]')];
  const closedToggle = toggles[0].innerHTML;
  let menuOpen = false;
  let moreOpen = false;
  let accountOpen = false;
  const clone = name => document.getElementById('study-wired-' + name).content.firstElementChild.cloneNode(true);
  const applyAncestors = (element, records) => {
    let node = element;
    for (const record of records) {
      if (!node) break;
      const attrs = new Map(record.attrs);
      for (const name of ['class', 'inert', 'aria-hidden', 'data-active-triggerable-container']) {
        if (attrs.has(name)) node.setAttribute(name, attrs.get(name));
        else node.removeAttribute(name);
      }
      node = node.parentElement;
    }
  };
  const setAccount = open => {
    accountOpen = open;
    const panel = document.querySelector('[data-testid="identity-dropdown"]');
    panel.setAttribute('aria-hidden', String(!open));
    const root = document.querySelector('[data-testid="one-nav-container-identityDropdown"]');
    applyAncestors(root, ui.account[open ? 'opened' : 'closed']);
    for (const toggle of document.querySelectorAll('span[role="button"][data-testid="identityDropdown"]')) {
      toggle.setAttribute('aria-expanded', String(open));
    }
    if (open) panel.querySelector('a')?.focus();
  };
  const setMenu = (open, focus = true) => {
    menuOpen = open;
    if (open && accountOpen) setAccount(false);
    const current = document.querySelector('[data-testid="one-nav-container-hamburger_menu"]');
    const drawer = clone(moreOpen ? 'drawer-more' : 'drawer');
    current.replaceWith(drawer);
    applyAncestors(drawer, ui.menu[open ? 'opened' : 'closed']);
    for (const toggle of toggles) {
      toggle.innerHTML = open ? clone('menu-open').innerHTML : closedToggle;
      toggle.setAttribute('aria-expanded', String(open));
    }
    if (open && focus) drawer.querySelector('a')?.focus();
  };
  document.addEventListener('click', event => {
    const target = event.target.closest('button,[role="button"],a');
    if (!target) return;
    if (target.matches('span[role="button"][data-testid="hamburger_menu"]')) {
      event.preventDefault();
      setMenu(!menuOpen);
    } else if (target.matches('span[role="button"][data-testid="identityDropdown"]')) {
      event.preventDefault();
      if (menuOpen) setMenu(false, false);
      setAccount(!accountOpen);
    } else if (target.getAttribute('aria-controls')?.startsWith('accordion-content-More-')) {
      event.preventDefault();
      moreOpen = !moreOpen;
      setMenu(true, false);
      document.querySelector('[aria-controls^="accordion-content-More-"]')?.focus();
    } else if (target.getAttribute('aria-label') === 'Next Slide' || target.getAttribute('aria-label') === 'Previous Slide') {
      const carousel = target.closest('[data-testid="carousel-container"]');
      const list = carousel.querySelector('[data-testid="carousel-list"]');
      const step = Math.max(list.clientWidth, 1);
      list.scrollBy({left: target.getAttribute('aria-label') === 'Next Slide' ? step : -step, behavior: 'smooth'});
    } else if (target.classList.contains('responsive-clip__play-pause')) {
      const video = target.closest('.responsive-clip')?.querySelector('video') || target.parentElement.querySelector('video');
      if (video) video.paused ? video.play().catch(() => {}) : video.pause();
    } else if (target.id === 'fides-modal-link') {
      location.assign('https://www.condenast.com/privacy-policy/');
    } else if (target.matches('.audio')) {
      const card = target.closest('article') || target.closest('[data-testid="SummaryItemWrapper"]') || target.parentElement.parentElement;
      const link = card.querySelector('a[href*="/story/"]');
      if (link) location.assign(link.href);
    }
  });
  document.addEventListener('keydown', event => {
    const target = event.target;
    if ((event.key === 'Enter' || event.key === ' ') && target.matches('span[role="button"]')) {
      event.preventDefault();
      target.click();
    } else if (event.key === 'Escape' && (menuOpen || accountOpen)) {
      const closingMenu = menuOpen;
      if (menuOpen) setMenu(false, false);
      if (accountOpen) setAccount(false);
      const selector = closingMenu ? 'hamburger_menu' : 'identityDropdown';
      [...document.querySelectorAll('span[role="button"][data-testid="' + selector + '"]')].find(e => e.getClientRects().length)?.focus();
    }
  });
  for (const video of document.querySelectorAll('video[autoplay]')) video.muted = true;
})();
