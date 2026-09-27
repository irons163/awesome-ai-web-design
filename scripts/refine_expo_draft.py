#!/usr/bin/env python3
"""Refine the native Expo Stitch export against a dated public-site capture.

The two Stitch HTML exports remain untouched. This script removes invented UI and
uses assets and copy observed on expo.dev on 2026-09-28. The output is a draft,
not a claim that the resulting page has passed visual acceptance.
"""

import html
import json
import re
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / '.stitch-work' / 'current-official'
ASSETS = WORK / 'expo-assets'


def between(source: str, start: str, end: str, replacement: str) -> str:
    assert source.count(start) == 1, start
    tail = source.index(start) + len(start)
    assert source.count(end, tail) == 1, end
    return source[:source.index(start)] + replacement + source[source.index(end, tail):]


def inline_svg(filename: str, css_class: str) -> str:
    source = (ASSETS / filename).read_text()
    updated, count = re.subn(r'\bclass="[^"]*"', f'class="{css_class}"', source, count=1)
    assert count == 1, filename
    return updated


def app_icons() -> str:
    source = (WORK / 'expo-source.html').read_text()
    provenance = json.loads((WORK / 'expo-asset-provenance.json').read_text())
    by_path = {urlsplit(asset['url']).path: asset['file']
               for asset in provenance['assets'] if asset['url'].startswith('https://')}
    icons = []
    for tag in re.findall(r'<img\b[^>]*alt="App Icon \d+"[^>]*>', source):
        url_match = re.search(r'\bsrc="([^"]+)"', tag)
        assert url_match, tag[:100]
        path = urlsplit(html.unescape(url_match.group(1))).path
        icons.append(by_path[path])
    assert len(icons) == 40 and icons[:20] == icons[20:], len(icons)
    return '\n'.join(
        f'<img src="expo-assets/{name}" alt="Expo customer app icon {index + 1}" width="40" height="40">'
        for index, name in enumerate(icons)
    )


def workflow() -> str:
    descriptions = [
        ('Develop', 'Build beautiful apps anywhere powered by Expo’s CLI, Skills, and MCP. Test on your device with Expo Go, validate with Simulators, distribute with Launch or Builds.'),
        ('Test', 'Find what breaks before your users do. Cloud simulators and device infrastructure for your team and your agents. Workflows runs your test suites on every change, starting from ready-made templates.'),
        ('Deploy', 'Deploy to TestFlight and the app stores for native releases, Update for everything after, with channels and rollouts you control.'),
        ('Monitor', 'See how the app behaves in production. Observe surfaces crash information, performance metrics, and Update adoption, and Update ships the fix if something breaks.'),
    ]
    drawings = ['544bb57ca0d3da57.svg', '74f500f272e10518.svg',
                'c7f8d5a40ee7bad0.svg', '9acfe04379e53ce5.svg']
    buttons = '\n'.join(
        f'<button class="expo-flow-tab{" active" if i == 0 else ""}" type="button" '
        f'data-step="{i}" aria-pressed="{"true" if i == 0 else "false"}">'
        f'<span>{name}</span><small>{html.escape(description)}</small></button>'
        for i, (name, description) in enumerate(descriptions)
    )
    art = '\n'.join(
        f'<div class="expo-flow-frame{" active" if i == 0 else ""}" data-step="{i}">'
        + inline_svg(filename, 'expo-flow-svg') + '</div>'
        for i, filename in enumerate(drawings)
    )
    return f'''<!-- Official workflow recovered after the second Stitch screen omitted it. -->
<section class="expo-workflow" aria-labelledby="expo-workflow-title">
  <div class="expo-workflow-inner">
    <div class="expo-workflow-copy">
      <h2 id="expo-workflow-title">Building blocks<br>for agentic workflows</h2>
      <div class="expo-flow-tabs" role="group" aria-label="Workflow stages">{buttons}</div>
    </div>
    <div class="expo-flow-art" aria-hidden="true">{art}</div>
  </div>
</section>
'''


def bento() -> str:
    mark = inline_svg('5d0aded8e32aeb20.svg', 'expo-sdk-svg')
    claude = inline_svg('ae167c2979bb21e5.svg', 'expo-claude-svg')
    return f'''<!-- Expo SDK and platform cards: layout and visible copy observed on expo.dev. -->
<section class="expo-bento" aria-label="Expo platform highlights">
  <article class="expo-sdk-card expo-card">
    <div class="expo-sdk-mark">{mark}</div>
    <div class="expo-sdk-copy"><h3>The Expo SDK</h3><p>10+ years in the making.<br>Powering thousands of apps.</p>
      <a class="expo-white-pill" href="https://github.com/expo/expo">◉&nbsp; expo/expo</a></div>
  </article>
  <article class="expo-ai-card expo-card">
    <div class="expo-ai-glow"></div>
    <div class="expo-ai-icons"><span class="expo-claude-icon">{claude}</span><span class="expo-mcp-icon">MCP</span></div>
    <div class="expo-ai-copy"><h3>Powering AI-native app devs</h3>
      <a href="https://docs.expo.dev/guides/using-claude/">Try the Expo Claude Code connector</a></div>
  </article>
  <article class="expo-api-card expo-card">
    <div class="expo-api-phone"><div class="expo-api-island"></div><div class="expo-api-glow"></div>
      <div class="expo-api-chat">✧&nbsp; Best model <span>◉</span></div><div class="expo-api-dock">▦&nbsp;&nbsp;&nbsp; ◉&nbsp;&nbsp;&nbsp; ●</div></div>
    <h3>100+ production APIs<br>one <code>install</code> away</h3>
  </article>
  <article class="expo-native-card expo-card">
    <div class="expo-native-logos" aria-hidden="true"><span class="ts">TS</span><span class="objc">[OBJ-C]</span><span class="js">JS</span><span class="kotlin">K</span><span class="swift">◈</span></div>
    <h3>All native<br>code welcome</h3>
  </article>
</section>
'''


def infrastructure() -> str:
    cards = [
        ('Get your app<br>on every device', 'Build your app and distribute it to Android, iOS, and the web from a single codebase with Build and Hosting.', 'https://docs.expo.dev/build/', 'distribution'),
        ('Get the latest to<br>every user, instantly', 'Send fast over-the-air updates to get the latest fixes and improvements to your users fast with Update.', 'https://docs.expo.dev/eas-update/introduction/', 'update'),
        ('A device in<br>your agent\'s hands', 'Cloud simulators your coding agent can drive on demand. It runs your app, verifies its own work, and attaches screenshots, recordings, and logs as proof. No Mac required.', 'https://expo.dev/services/simulators', 'simulator'),
        ('Launch anything<br>to the App Store', "Launch makes it easy by guiding you through the technical stuff, so your app can be in real users' hands. No config or prior knowledge needed.", 'https://expo.dev/services/launch', 'launch'),
        ('Built-in monitoring<br>and observability', 'Performance metrics for understanding how your app is performing for users in production.', 'https://expo.dev/services/eas-observe', 'observe'),
        ('Automate your builds,<br>tests, and releases', 'Build for the app stores, run tests, send updates, and more automatically with Workflows.', 'https://expo.dev/services/workflows', 'workflows'),
    ]
    art = {
        'distribution': '<div class="expo-distribution"><div class="expo-distribution-expo">⌃</div><div class="expo-branches"></div><div class="expo-platforms"><span>●<small>iOS</small></span><span>♟<small>android</small></span><span>◎<small>www</small></span></div></div>',
        'update': '<div class="expo-update"><div class="expo-update-shadow">♧&nbsp; App updates #124 <span>Updates</span></div><div class="expo-update-card"><b>▱&nbsp; Over-the-air update</b><div class="expo-update-labels">Platform <span>Duration</span><span>Rollout %</span></div><div class="expo-update-row">☁&nbsp; Android <span>2m 30s</span><strong>100% ●</strong></div></div></div>',
        'simulator': '<div class="expo-simulator"><div class="expo-sim-log">iOS Simulator session<br><small>Logs&nbsp;&nbsp; Network</small></div><div class="expo-sim-phone"><div class="expo-sim-island"></div><span>9:41</span><div class="expo-sim-content">Your app<br><br>✓&nbsp; Ready to test</div></div><div class="expo-sim-results"><span>Logs</span><span>Network</span><div>0:46.0 · 2 events</div></div></div>',
        'launch': '<div class="expo-launch"><div class="expo-launch-row"><span>◉</span><b>App Store Connect</b><small>Approved</small></div><div class="expo-launch-row"><span>▶</span><b>Google Play Console</b><small>Approved</small></div></div>',
        'observe': '<div class="expo-observe"><div class="expo-observe-head">Performance overview <span>Live</span></div><div class="expo-bars"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div><div class="expo-observe-foot">Crash-free sessions&nbsp; <strong>99.8%</strong></div></div>',
        'workflows': '<div class="expo-workflows"><div class="expo-workflow-node">GitHub<br><small>main branch</small></div><div class="expo-workflow-line"></div><div class="expo-workflow-node">Build<br><small>iOS · Android</small></div><div class="expo-workflow-line"></div><div class="expo-workflow-node">Test<br><small>Simulator</small></div><div class="expo-workflow-line"></div><div class="expo-workflow-node">Release<br><small>App stores</small></div></div>',
    }
    html_cards = []
    for heading, body, href, kind in cards:
        full = kind in ('simulator', 'workflows')
        html_cards.append(f'''<article class="expo-service-card {kind}{' full' if full else ''}">
          <div class="expo-service-copy"><h3>{heading}</h3><p>{html.escape(body)}</p>
          <a href="{href}">Learn more&nbsp; ›</a></div>
          <div class="expo-service-art" aria-hidden="true">{art[kind]}</div>
        </article>''')
    return '''<section class="expo-infrastructure" aria-labelledby="expo-infrastructure-title">
  <div class="expo-infrastructure-heading"><h2 id="expo-infrastructure-title">Infrastructure for your apps</h2>
    <div class="expo-techs"><span>⌃&nbsp; Expo</span><span>⚛&nbsp; React Native</span><span>🟧&nbsp; Swift</span><span>⬡&nbsp; Jetpack Compose</span><span>◢&nbsp; Kotlin</span></div>
    <a class="expo-white-pill" href="https://expo.dev/eas">Learn more</a></div>
  <div class="expo-service-grid">''' + '\n'.join(html_cards) + '</div></section>\n'


def community() -> str:
    posts = [
        ('Peter Piekarczyk', '@peterpme', 'avatar-peter.jpg', 'Expo is amazing', 'https://x.com/peterpme/status/1946019090679603318'),
        ('Hugo Duarte', '@hugoasduarte', 'avatar-hugo.jpg', 'I love @expo so much! Was struggling to upgrade an old React Native app to the latest version for a few days without success. Created a new expo app, copied my src folder along with some package installs and was ready in just a few minutes!', 'https://x.com/hugoasduarte/status/1831618467365007777'),
        ('Josh Gonsalves', '@joshgonsalves_', 'avatar-josh.jpg', 'Makes sense. I do LOVE expo.', 'https://x.com/joshgonsalves_/status/1966582778088022426'),
        ('NicoDevs', '@Nico_Devs', 'avatar-nico.jpg', 'I love @expo, it made React Native dev so much easier. Firstly, it allows anyone to dev from any machine, even with very low specs and run the app on device with Expo Go app. Also, it includes so many libraries and the performance is crazy especially on Expo SDK 54', 'https://x.com/Nico_Devs/status/1960268219626684768'),
    ]
    quotes = '\n'.join(
        '<a class="expo-quote" href="' + url + '"><div class="expo-quote-author"><img src="expo-assets/' + avatar + '" alt="" width="40" height="40"><span><b>'
        + html.escape(name) + '</b><small>' + html.escape(handle) + '</small></span></div><p>'
        + html.escape(quote) + '</p><small>View post ↗</small></a>'
        for name, handle, avatar, quote, url in posts
    )
    return '''<section class="expo-community"><h2>Expo is a community</h2><p>80% of React Native developers choose Expo.<br>Hear what developers say about their experience.</p>
    <a class="expo-dark-pill" href="https://chat.expo.dev">Join us on Discord</a>
    <div class="expo-quotes">''' + quotes + '''</div></section>
<section class="expo-bottom-cta"><h2>Build beautiful<br>native apps</h2><a class="expo-white-pill" href="https://expo.dev/new">Get started</a></section>
'''


def main() -> None:
    page = (WORK / 'expo-stitch-revised.html').read_text()
    assert page.count('<!-- ==================== BENTO ARCHITECTURE SECTION ==================== -->') == 1
    page = page.replace('width=1280, initial-scale=1.0', 'width=device-width, initial-scale=1.0', 1)
    page = page.replace('<link href="https://fonts.googleapis.com" rel="preconnect"/>', '', 1)
    page = page.replace('<link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>', '', 1)
    page = re.sub(r'<link href="https://fonts.googleapis.com/css2[^>]+>', '', page, count=1)
    wordmark = inline_svg('fab8e495904e4eee.svg', 'expo-wordmark')
    page = between(page, '<!-- Expo Logo -->', '<!-- Horizontal Nav Links -->',
                   '<a class="expo-brand" href="https://expo.dev/">' + wordmark + '</a>\n')
    page = between(page, '<!-- Search bar trigger -->', '<!-- Github Star Indicator -->', '')
    corona = inline_svg('12cf2966ad66a468.svg', 'expo-corona')
    page = between(page, '<!-- Right Column: Starburst with radiating particle graphic with Expo \'A\' logo badge -->',
                   '<!-- Bottom of Hero: Colorful 40-icon/app strip of real mobile apps made with Expo -->',
                   '<div class="expo-hero-art">' + corona + '</div></div>\n')
    trust = ('<div class="expo-trust"><div class="expo-trust-label">3M+ DEVELOPERS. 50K+ GITHUB STARS. TRUSTED IN PRODUCTION BY:</div>'
             '<div class="expo-icon-viewport"><div class="expo-icon-track">' + app_icons() + '</div></div></div>\n')
    page = between(page, '<!-- Bottom of Hero: Colorful 40-icon/app strip of real mobile apps made with Expo -->',
                   '</section>\n<!-- ==================== BENTO ARCHITECTURE SECTION ==================== -->', trust)
    hero_old = '<section class="relative w-full max-w-[1280px] mx-auto px-6 pt-[80px] pb-16 min-h-[640px] flex flex-col justify-between">'
    assert page.count(hero_old) == 1
    page = page.replace(hero_old, '<section class="expo-hero relative w-full max-w-[1280px] mx-auto px-6">', 1)
    page = between(page, '<!-- ==================== BENTO ARCHITECTURE SECTION ==================== -->',
                   '<!-- ==================== STATISTICS STRIP ==================== -->',
                   workflow() + bento() + infrastructure())
    page = between(page, '<!-- ==================== COMMUNITY SECTION ("Expo is a community") ==================== -->',
                   '<!-- ==================== FOOTER ==================== -->', community())
    css = (ROOT / 'assets' / 'expo-official-draft.css').read_text()
    page = page.replace('</head>', '<style>\n' + css + '\n</style>\n</head>', 1)
    js = '''<script>
document.querySelectorAll('.expo-flow-tab').forEach(button => button.addEventListener('click', () => {
  const step = button.dataset.step;
  document.querySelectorAll('.expo-flow-tab').forEach(item => {
    const active = item.dataset.step === step;
    item.classList.toggle('active', active);
    item.setAttribute('aria-pressed', String(active));
  });
  document.querySelectorAll('.expo-flow-frame').forEach(item =>
    item.classList.toggle('active', item.dataset.step === step));
}));
</script>'''
    page = page.replace('</body>', js + '\n</body>', 1)
    assert '<h2 id="expo-workflow-title">' in page
    assert page.count('expo-assets/') == 46, page.count('expo-assets/')
    assert 'Search...' not in page and 'v52.0 Production Ready' not in page
    assert 'EAS build velocity and the developer experience' not in page
    (WORK / 'expo.html').write_text(page)
    print(f'Wrote {WORK / "expo.html"} ({len(page):,} characters)')


if __name__ == '__main__':
    main()
