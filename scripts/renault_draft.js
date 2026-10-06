(() => {
  const all = (selector, root = document) => Array.from(root.querySelectorAll(selector));
  const mobile = () => window.matchMedia('(max-width:1023px)').matches;
  all('[data-study-carousel]').forEach(root => {
    const track = root.querySelector('.Carousel_carousel-content__8aYJ4');
    const original = Array.from(track.children);
    const hero = root.dataset.studyCarousel === 'hero';
    let index = 0, startX = null;
    track.style.transition = 'none';
    if (hero) {
      const before = original.at(-1).cloneNode(true), after = original[0].cloneNode(true);
      before.setAttribute('aria-hidden', 'true'); after.setAttribute('aria-hidden', 'true');
      all('a,button', before).concat(all('a,button', after)).forEach(n => n.tabIndex = -1);
      track.prepend(before); track.append(after);
    }
    const position = () => {
      if (hero) all('.HeroCarrousel_hero-carousel-card__s0HSm', root).forEach(article => {
        const arrow = article.querySelector('.HeroCarrousel_hero-carousel-card__btn__UjYy5');
        const destination = mobile() ? article.querySelector('.CarouselCard_actions__LUPdz') : article.querySelector('.HeroCarrousel_hero-carousel-card__title__Tj8mf > span');
        if (arrow.parentElement !== destination) destination.append(arrow);
      });
      const step = original[0].getBoundingClientRect().width;
      const card = original[0].querySelector('article');
      const center = hero && !mobile() ? (root.clientWidth - card.getBoundingClientRect().width) / 2 : 0;
      track.style.transform = `translateX(${center - (index + (hero ? 1 : 0)) * step}px)`;
      root.dataset.activeSlide = String(index);
      all('[data-carousel-index]', root).forEach(n => {
        const selected = Number(n.dataset.carouselIndex) === index;
        n.setAttribute('aria-pressed', String(selected));
        n.classList.toggle('Carousel_carousel-btn--selected__SWQEV', selected);
      });
      if (hero) {
        const size = card.getBoundingClientRect();
        root.style.setProperty('--carousel-arrow-edge-pos', `${size.width / 2}px`);
        all('.Carousel_carousel-prev__hwGpo,.Carousel_carousel-next__iwi1t', root).forEach(n => n.classList.add('Carousel_positioned__0pvGn'));
        const bg = document.querySelector('.HeroCarrousel_bg-image__Jrexq img');
        bg.src = original[index].querySelector('img').src;
      } else if (root.dataset.studyCarousel === 'brands') {
        root.style.setProperty('--carousel-arrow-top-offset', `${card.clientHeight / 2 - 20}px`);
      }
    };
    const choose = next => { index = (next + original.length) % original.length; position(); };
    all('[data-carousel-step]', root).forEach(n => n.addEventListener('click', () => choose(index + Number(n.dataset.carouselStep))));
    all('[data-carousel-index]', root).forEach(n => n.addEventListener('click', () => choose(Number(n.dataset.carouselIndex))));
    track.addEventListener('pointerdown', e => startX = e.clientX);
    track.addEventListener('pointerup', e => { if (startX !== null && Math.abs(e.clientX - startX) > 35) choose(index + (e.clientX < startX ? 1 : -1)); startX = null; });
    root.tabIndex = 0;
    root.addEventListener('keydown', e => { if (['ArrowLeft', 'ArrowRight'].includes(e.key)) { e.preventDefault(); choose(index + (e.key === 'ArrowRight' ? 1 : -1)); } });
    window.addEventListener('resize', position);
    document.fonts.ready.then(position);
    position();
    requestAnimationFrame(() => requestAnimationFrame(() => track.style.transition = ''));
  });
  const mobileMenu = document.getElementById('study-mobile-menu');
  const toggle = document.querySelector('[aria-label="Basculer la navigation"]');
  const closeMenus = () => {
    mobileMenu.hidden = true;
    document.body.classList.remove('study-menu-open');
    toggle.classList.remove('study-mobile-close');
    toggle.setAttribute('aria-expanded', 'false');
    all('[data-menu-panel]').forEach(n => n.dataset.state = 'closed');
    all('[data-menu-open]').forEach(n => n.setAttribute('aria-expanded', 'false'));
    all('[data-desktop-menu]').forEach(n => n.hidden = true);
    all('.NavigationMenu_navigation-menu-trigger__S0vai').forEach(n => { n.dataset.state = 'closed'; n.setAttribute('aria-expanded', 'false'); });
  };
  toggle.addEventListener('click', () => {
    if (!mobileMenu.hidden) { closeMenus(); return; }
    mobileMenu.hidden = false;
    document.body.classList.add('study-menu-open');
    toggle.classList.add('study-mobile-close');
    toggle.setAttribute('aria-expanded', 'true');
    mobileMenu.querySelector('button,a').focus();
  });
  all('[data-menu-open]').forEach(n => n.addEventListener('click', () => {
    all('[data-menu-panel]').forEach(panel => panel.dataset.state = panel.dataset.menuPanel === n.dataset.menuOpen ? 'open' : 'closed');
    n.setAttribute('aria-expanded', 'true');
    mobileMenu.querySelector('[data-state="open"] [data-menu-back]').focus();
  }));
  all('[data-menu-back]').forEach(n => n.addEventListener('click', () => {
    const panel = n.closest('[data-menu-panel]'); panel.dataset.state = 'closed';
    const trigger = all('[data-menu-open]').find(x => x.dataset.menuOpen === panel.dataset.menuPanel);
    trigger.setAttribute('aria-expanded', 'false'); trigger.focus();
  }));
  all('.NavigationMenu_navigation-menu-trigger__S0vai').forEach(n => n.addEventListener('click', () => {
    const label = n.textContent.startsWith('Évènement') ? 'Évènement' : n.textContent.trim();
    if (label === 'Évènement') { location.href = 'https://events.renault.com/'; return; }
    const panel = all('[data-desktop-menu]').find(x => x.dataset.desktopMenu === label);
    const opening = panel.hidden; closeMenus(); panel.hidden = !opening;
    n.dataset.state = opening ? 'open' : 'closed'; n.setAttribute('aria-expanded', String(opening));
  }));
  all('[data-magazine-tab]').forEach(n => {
    const select = () => {
    all('[data-magazine-tab]').forEach(tab => {
      const selected = tab === n;
      tab.setAttribute('aria-selected', String(selected));
      tab.dataset.state = selected ? 'active' : 'inactive';
    });
    all('[data-magazine-panel]').forEach(panel => {
      const selected = panel.dataset.magazinePanel === n.dataset.magazineTab;
      panel.hidden = !selected; panel.dataset.state = selected ? 'active' : 'inactive';
    });
    };
    n.addEventListener('pointerenter', select);
    n.addEventListener('focus', select);
    n.addEventListener('click', () => { location.href = n.dataset.topicUrl; });
  });
  document.addEventListener('click', e => { if (!e.target.closest('header,.study-desktop-panels,#study-mobile-menu')) closeMenus(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') { closeMenus(); toggle.focus(); } });
  all('.Accordion_trigger__rY9B6').forEach(n => n.addEventListener('click', () => {
    const panel = document.getElementById(n.getAttribute('aria-controls'));
    const open = n.getAttribute('aria-expanded') !== 'true';
    n.setAttribute('aria-expanded', String(open)); n.dataset.state = open ? 'open' : 'closed';
    panel.hidden = !open; panel.dataset.state = open ? 'open' : 'closed';
  }));
  all('[role="switch"]').forEach(n => n.addEventListener('click', () => {
    const enabled = n.getAttribute('aria-checked') !== 'true';
    all('[role="switch"]').forEach(x => { x.setAttribute('aria-checked', String(enabled)); x.dataset.state = enabled ? 'checked' : 'unchecked'; x.querySelector('.Switch_switch-thumb__hgXoH').dataset.state = x.dataset.state; });
    document.documentElement.classList.toggle('study-accessibility', enabled);
  }));
  const search = document.getElementById('study-search');
  all('[title="Recherche"]').forEach(n => n.addEventListener('click', () => {
    closeMenus(); search.dataset.state = 'open'; search.showModal();
    n.setAttribute('aria-expanded', 'true'); search.querySelector('input').focus();
  }));
  search.querySelector('[data-dialog-close]').addEventListener('click', () => search.close());
  search.addEventListener('close', () => {
    search.dataset.state = 'closed';
    all('[title="Recherche"]').forEach(n => n.setAttribute('aria-expanded', 'false'));
  });
  const help = document.getElementById('study-help');
  all('[aria-label="Informations sur l\'aide"]').forEach(n => n.addEventListener('click', () => {
    const rect = n.getBoundingClientRect();
    help.hidden = !help.hidden; help.style.top = `${rect.bottom + 8}px`;
    help.style.right = `${window.innerWidth - rect.right}px`;
    help.style.maxWidth = '280px'; n.setAttribute('aria-expanded', String(!help.hidden));
    if (!help.hidden) help.focus();
  }));
  document.addEventListener('keydown', e => { if (e.key === 'Escape') {
    help.hidden = true; all('[aria-label="Informations sur l\'aide"]').forEach(n => n.setAttribute('aria-expanded', 'false'));
  }});
  document.addEventListener('click', e => {
    if (!e.target.closest('#study-help,[aria-label="Informations sur l\'aide"]')) {
      help.hidden = true; all('[aria-label="Informations sur l\'aide"]').forEach(n => n.setAttribute('aria-expanded', 'false'));
    }
  });
  all('.DropdownTranslation_trigger__FHH99').forEach(n => {
    const menu = document.createElement('div'); menu.hidden = true; menu.className = 'study-languages'; menu.setAttribute('role', 'menu');
    [['Français', 'https://www.renaultgroup.com/'], ['English', 'https://www.renaultgroup.com/en/']].forEach(([label, url]) => {
      const a = document.createElement('a'); a.textContent = label; a.href = url; a.setAttribute('role', 'menuitem'); menu.append(a);
    });
    n.after(menu); n.addEventListener('click', () => { menu.hidden = !menu.hidden; n.setAttribute('aria-expanded', String(!menu.hidden)); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape') { menu.hidden = true; n.setAttribute('aria-expanded', 'false'); } });
  });
})();
