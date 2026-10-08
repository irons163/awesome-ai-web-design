(() => {
  const mount = document.getElementById('study-mount');
  let mode, hero = 0, product = 0, heroTimer, productTimer, backgroundPlayer;
  const root = () => mount.querySelector('.hpg_main');
  const query = selector => mount.querySelector(selector);
  const all = selector => [...mount.querySelectorAll(selector)];
  function showHero(index) {
    hero = (index + 3) % 3;
    const owner = query('#hpg-hero-div');
    const items = [...owner.querySelectorAll('.owl-stage>.owl-item')];
    const width = owner.getBoundingClientRect().width;
    const gap = innerWidth >= 768 ? 10 : 0;
    const stage = owner.querySelector('.owl-stage');
    stage.style.width = ((width + gap) * items.length) + 'px';
    stage.style.transform = `translate3d(${-((width + gap) * (hero + 2))}px,0,0)`;
    items.forEach((item, i) => {
      item.style.width = width + 'px';
      item.style.marginRight = gap + 'px';
      item.classList.toggle('active', i === hero + 2);
      item.classList.toggle('center', i === hero + 2);
      item.setAttribute('aria-hidden', String(i !== hero + 2));
      item.querySelectorAll('.owl-item-tab').forEach(e => e.tabIndex = i === hero + 2 ? 0 : -1);
    });
    owner.querySelectorAll('.hpg-carousal-step').forEach(e => e.textContent = (hero + 1) + '/3');
  }
  function showProduct(index) {
    product = (index + 7) % 7;
    const owner = query('#ghpg-product-item-container');
    const stage = owner.querySelector('.owl-stage');
    const items = [...stage.children];
    const gap = innerWidth >= 1024 ? 24 : 8;
    const width = parseFloat(items[0].style.width);
    const initial = mode === 'desktop' ? 109 : 67;
    stage.style.transform = `translate3d(${initial - (width + gap) * product}px,0,0)`;
    items.forEach((item, i) => {
      item.classList.toggle('active', i === product || i === product + 1);
      item.classList.toggle('center', i === product);
      item.setAttribute('aria-hidden', String(i !== product));
      item.querySelectorAll('a,button').forEach(e => e.tabIndex = i === product ? 0 : -1);
    });
    owner.querySelectorAll('.owl-dot').forEach((dot, i) => {
      dot.classList.toggle('active', i === product);
      dot.disabled = i === product;
    });
  }
  function swapHeader(key) {
    const template = document.querySelector(`[data-study-state="${key}"]`);
    const next = template.content.querySelector('header').cloneNode(true);
    query('#unified-masthead').replaceWith(next);
    labelMenuToggle();
  }
  function labelMenuToggle() {
    const open = query('#unified-masthead').getAttribute('data-state') === 'mobile-expanded';
    all('.mh-mobile-nav-toggle').forEach(e => e.setAttribute('aria-label',open ? '關閉導覽選單' : '開啟導覽選單'));
  }
  function closeMenu() {
    document.getElementById('study-menu-shade')?.remove();
    document.body.classList.remove('mh-bodyOverFlow-Hidden');
    const template = document.querySelector(`[data-study-layout="${mode}"]`);
    query('#unified-masthead').replaceWith(template.content.querySelector('#unified-masthead').cloneNode(true));
    labelMenuToggle();
  }
  function openMenu() {
    swapHeader('mobile_menu');
    document.body.classList.add('mh-bodyOverFlow-Hidden');
    const shade = document.createElement('div');
    shade.id = 'study-menu-shade';
    shade.addEventListener('click', closeMenu);
    document.body.append(shade);
  }
  function loadLayout() {
    const nextMode = innerWidth < 1024 ? 'mobile' : 'desktop';
    if (mode === nextMode) return;
    clearInterval(heroTimer); clearInterval(productTimer);
    document.getElementById('study-menu-shade')?.remove();
    document.body.classList.remove('mh-bodyOverFlow-Hidden');
    mode = nextMode; hero = product = 0;
    backgroundPlayer?.destroy();
    mount.replaceChildren(document.querySelector(`[data-study-layout="${mode}"]`).content.cloneNode(true));
    labelMenuToggle();
    // Keep the dated paused first state. Original account/cart/support links
    // remain official destinations; no provider SDK or credentials are copied.
    showHero(0);
    const video = query('video[data-study-background]');
    if (video) {
      video.muted = true;
      video.addEventListener('loadedmetadata',() => {
        // Retain the observed paused frame; playback starts with its control.
        video.currentTime = Number(video.dataset.studyPausedTime);
        video.pause();
      },{once:true});
      if (window.Hls?.isSupported()) {
        backgroundPlayer = new Hls({enableWorker:false});
        backgroundPlayer.loadSource(video.dataset.studyBackground);
        backgroundPlayer.attachMedia(video);
      } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
        video.src = video.dataset.studyBackground;
      }
    }
  }
  mount.addEventListener('click', event => {
    const target = event.target.closest('button,a,h3');
    if (!target) return;
    if (target.matches('.hpg-carousal-prev,.hpg-carousal-next')) {
      showHero(hero + (target.matches('.hpg-carousal-next') ? 1 : -1));
    } else if (target.matches('.hpg-carousal-loop-btn')) {
      if (heroTimer) { clearInterval(heroTimer); heroTimer = null; }
      else heroTimer = setInterval(() => showHero(hero + 1),8000);
      all('.hpg-carousal-loop-btn').forEach(e => {
        const label = heroTimer ? '暫停' : '播放'; e.setAttribute('aria-label',label);
        e.firstChild.textContent = label;
        e.querySelector('use')?.setAttribute('xlink:href',heroTimer ? '#dds__icon--pause' : '#dds__icon--play-cir');
      });
    } else if (target.matches('#ghpg-product-carousal-prev,#ghpg-product-carousal-next')) {
      showProduct(product + (target.id.endsWith('next') ? 1 : -1));
    } else if (target.matches('.owl-dot') && target.closest('#ghpg-product-item-container')) {
      showProduct([...target.parentElement.children].indexOf(target));
    } else if (target.matches('#owl-nav-loop-product')) {
      if (productTimer) { clearInterval(productTimer); productTimer = null; }
      else productTimer = setInterval(() => showProduct(product + 1),8000);
      target.firstChild.textContent = productTimer ? '暫停' : '播放';
      target.setAttribute('aria-label',productTimer ? '暫停' : '播放');
    } else if (target.matches('.mh-mobile-nav-toggle')) {
      query('#unified-masthead').getAttribute('data-state') === 'mobile-expanded' ? closeMenu() : openMenu();
    } else if (mode === 'mobile' && target.matches('.mh-top-nav-button') && target.textContent.trim() === '電腦與配件') {
      swapHeader('mobile_products_menu');
    } else if (target.closest('#mh-unified-footer .stack') && target.matches('button[id^="Section"]')) {
      const open = target.getAttribute('aria-expanded') !== 'true';
      target.setAttribute('aria-expanded',String(open));
      const group = target.closest('.stack');
      group.classList.toggle('study-footer-open',open);
      group.querySelector('h3')?.classList.toggle('active',open);
    } else if (target.matches('#floating-button')) {
      location.href = 'https://www.dell.com/zh-tw/shop/lp/contact-us';
    } else if (target.matches('.ghpg-video-section button.dds__button--editorial')) {
      const video = query('video[data-study-background]');
      if (video.paused) video.play().catch(() => {});
      else video.pause();
      const playing = !video.paused;
      const label = playing ? '暫停' : '播放';
      target.firstChild.textContent = label;
      target.setAttribute('aria-label',label);
      target.querySelector('use')?.setAttribute('xlink:href',playing ? '#dds__icon--pause' : '#dds__icon--play-cir');
    }
  });
  document.addEventListener('keydown',event => {if(event.key === 'Escape' && document.getElementById('study-menu-shade')) closeMenu();});
  window.addEventListener('resize',() => {loadLayout();showHero(hero);});
  loadLayout();
})();
