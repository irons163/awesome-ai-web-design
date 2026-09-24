"""Replace invented Stitch details with public Linear homepage observations.

Run after refine-linear.py and extend-linear.py. Reference: https://linear.app/
Observed 2026-09-24T18:54:23Z at a 1280 x 720 viewport.
"""
from html import escape
from pathlib import Path
import hashlib
import json
import re

root = Path(__file__).parent
page = root / 'linear.html'
html = page.read_text()


def replace_span(start, end, replacement):
    global html
    first = html.index(start)
    last = html.index(end, first)
    html = html[:first] + replacement + html[last:]


intake_columns = [
    ('Backlog', '8', [
        ('ENG-2085', 'Reduce UI flicker during autonomy...'),
        ('ENG-2094', 'Add buffering for autonomy event streams'),
        ('ENG-2092', 'Reduce startup delay caused by vehicle sync'),
        ('ENG-2200', 'Fix delayed route updates during rerouting'),
    ]),
    ('Todo', '71', [
        ('ENG-926', 'Remove UI inconsistencies'),
        ('ENG-2088', 'TypeError: Cannot read properties'),
        ('ENG-924', 'Upgrade to Claude Opus 5'),
        ('ENG-1882', 'Optimize load times'),
    ]),
    ('In Progress', '3', [
        ('ENG-1487', 'Remove contentData from GraphQL API'),
        ('MKT-1028', 'Launch page assets'),
        ('ENG-2187', 'Prevent duplicate ride requests on poor networks'),
    ]),
    ('Done', '53', [
        ('ENG-2074', 'Clean up deprecated APIs'),
        ('ENG-1912', 'Reduce latency in autonomy streams'),
        ('ENG-1951', 'Reduce ETA fluctuations during rerouting'),
        ('ENG-1960', 'Improve fallback messaging'),
        ('ENG-1991', 'Improve rider visibility into vehicle status'),
    ]),
]
board = '<div class="linear-intake-visual"><div class="linear-intake-columns">'
for title, count, issues in intake_columns:
    board += f'<div class="linear-intake-column"><h3>{escape(title)} <small>{count}</small></h3>'
    for code, label in issues:
        board += f'<div class="linear-intake-issue"><small>{escape(code)}</small><span>{escape(label)}</span></div>'
    board += '</div>'
board += '''</div><div class="linear-thread"><div class="linear-thread-title">✣ &nbsp; Thread <span>#product</span></div>
  <p><strong>lena</strong> Anyone else noticing the iOS app feels slow to open if you haven’t used it in a bit?</p>
  <p><strong>didier</strong> Yea, we’re still blocking initial render on a full vehicle_state sync every time...</p>
  <p><strong>andreas</strong> Feels like we could render sooner and load the rest in the background. Probably also worth tracking startup timing so we know how often this happens!</p>
  <div class="linear-thread-compose">@Linear create issues and assign to me</div>
</div></div>\n\n'''
replace_span('    <!-- Product Interface Demo:', '      <!-- Features badges list -->', '    '+board+'    ')

planning = '''<div class="linear-planning-visual">
  <div class="linear-roadmap"><div class="linear-roadmap-months"><span>MAR</span><span>APR</span><span>MAY</span><span>JUN</span><span>JUL</span><span>AUG</span><span>SEP</span></div>
    <div class="linear-roadmap-row"><span>UI Refresh</span><div><i style="left:8%;width:41%"></i><small>Core screens &nbsp; Polish</small></div></div>
    <div class="linear-roadmap-row"><span>Split fares</span><div><i style="left:23%;width:44%"></i><small>Internal &nbsp; Public Beta</small></div></div>
    <div class="linear-roadmap-row"><span>Autonomy status clarity</span><div><i style="left:39%;width:43%"></i><small>Alpha</small></div></div>
    <div class="linear-roadmap-row"><span>Autonomy telemetry reliability</span><div><i style="left:55%;width:40%"></i><small>Beta &nbsp; GA</small></div></div>
  </div>
  <div class="linear-cycle-chart"><p>Cycle time by agent</p><svg viewBox="0 0 520 330" preserveAspectRatio="none" aria-label="Cycle time by agent line chart"><path class="linear-chart-grid" d="M0 40H520 M0 120H520 M0 200H520 M0 280H520"/><path class="linear-chart-line one" d="M0 168H150L172 138H272L297 187H390L414 172H520"/><path class="linear-chart-line two" d="M0 227H146L168 247H273L297 231H390L413 249H520"/><path class="linear-chart-line three" d="M0 250H145L168 298H271L294 323H389L414 287H520"/></svg></div>
</div>\n\n'''
replace_span('    <!-- Gantt MAR-SEP', '      <!-- Features badges list -->', '    '+planning+'    ')

ai_cards = [
    ('Linear <small>Opus 5</small>', 'what are the three most important customer requests around permissions? add them to the Access Controls project', 'Worked for 8 sec', 'Three issues ranked by customer impact: ENG-2298 Add granular project permissions; ENG-2647 Let guests access multiple teams; ENG-2352 Create custom roles with scoped access. I’ve added them to Access Controls.'),
    ('Cursor', 'add retry handling for failed image uploads described in this issue', 'ENG-2844 added to context', ''),
    ('Linear <small>Opus 5</small>', 'Review today’s mobile triage and group the issues by what should happen next', 'Mobile Triage added to context', ''),
    ('ChatPRD', 'review this issue, draft complete offline mode requirements, and break the work into sub-issues', 'ENG-2521 added to context · Worked for 1 min', 'Updated the issue with requirements, open product decisions, and acceptance criteria. ENG-2920 Define offline mode requirements'),
]
agents = '<div class="linear-ai-visual"><div class="linear-ai-track">'
for title, prompt, status, result in ai_cards:
    agents += f'<article class="linear-ai-card"><header>{title}</header><p class="linear-ai-prompt">{escape(prompt)}</p><p class="linear-ai-status">{escape(status)}</p>'
    if result:
        agents += f'<p class="linear-ai-result">{escape(result)}</p>'
    agents += '</article>'
agents += '</div></div>\n\n'
replace_span('    <!-- Agent conversation cards:', '    <!-- Features badges list -->', '    '+agents+'    ')

review_issues = [
    ('In Review', [('ENG-2498','Replace isFullySynced with a sync status'),('ENG-2380','Show a stale data banner while syncing'),('ENG-2039','Pass sync status to the dashboard')]),
    ('In Progress', [('ENG-2076','Reduce ETA jitter'),('ENG-2108','Handle GPS dropouts gracefully'),('ENG-2143','Optimize map tile loading on initial app open'),('ENG-2187','Prevent duplicate ride requests on poor networks')]),
    ('Todo', [('ENG-2254','Reduce unnecessary map re-rendering on home screen'),('ENG-2291','Clean up deprecated APIs used by the rider app'),('ENG-2327','Speed up CI pipelines for mobile builds'),('ENG-2358','Reduce flakiness in mobile UI tests')]),
]
build = '<div class="linear-build-visual"><div class="linear-build-issues">'
for title, issues in review_issues:
    build += f'<h3>{escape(title)} <small>{len(issues)}</small></h3>'
    for code, label in issues:
        build += f'<div><small>{escape(code)}</small><span>{escape(label)}</span></div>'
build += '''</div><div class="linear-diff"><header>kinetic-ios/src/screens/Home/HomeScreen.tsx</header><div class="linear-diff-columns"><pre>import React from 'react'
import { View, ActivityIndicator } from 'react-native'
import { useVehicleState } from '@hooks/useVehicleState'
import { Dashboard } from '@components/Dashboard'

export const HomeScreen = () =&gt; {
  const { vehicleState, isFullySynced } = useVehicleState()
  if (!isFullySynced) {
    return &lt;ActivityIndicator size="large" /&gt;
  }
  return &lt;Dashboard state={vehicleState} /&gt;
}</pre><pre>import React from 'react'
import { View, ActivityIndicator } from 'react-native'
import { useVehicleState, SyncStatus } from '@hooks/useVehicleState'
import { Dashboard } from '@components/Dashboard'

export const HomeScreen = () =&gt; {
  const { vehicleState, syncStatus } = useVehicleState()
  if (syncStatus === SyncStatus.PENDING) {
    return &lt;ActivityIndicator size="large" /&gt;
  }
  return &lt;Dashboard state={vehicleState} syncStatus={syncStatus} /&gt;
}</pre></div></div></div>\n\n'''
replace_span('    <!-- Issue rows plus code diff -->', '      <!-- Features badges list -->', '    '+build+'    ')

changelog = [
    ('New controls for Linear coding agent','Coding sessions are the shortest path from issue to diff. Assign a task to Linear Agent, and it works in a secure cloud environment to write and test the code before opening a pull request for review.','SEP 24, 2026','https://linear.app/changelog/2026-09-24-new-controls-for-linear-coding-agent'),
    ('Loops for product management','Loops are recurring agent workflows for teams. They now respond to more workspace activity, including changes to initiatives, projects, and cycles. They can also edit Linear documents and post updates to Slack.','SEP 10, 2026','https://linear.app/changelog/2026-09-14-loops-for-product-management'),
    ('Priority inbox','An active workspace can create a significant amount of notifications each day, and until now your inbox treated them all the same. The new Priority tab separates what needs your attention from what can wait, so something like a review blocking a release never gets buried.','SEP 3, 2026','https://linear.app/changelog/2026-09-03-priority-inbox'),
]
news = '<section class="linear-current-changelog" aria-labelledby="linear-changelog-title"><h2 id="linear-changelog-title">Changelog</h2><div class="linear-news-line"><span></span><span></span><span></span></div><div class="linear-news-grid">'
for title, summary, date, href in changelog:
    news += f'<a href="{href}"><h3>{escape(title)}</h3><p>{escape(summary)}</p><time>{date}</time></a>'
news += '</div><a class="linear-news-all" href="https://linear.app/changelog">View all →</a></section>\n\n'
replace_span('  <!-- CHANGELOG SECTION', '  <!-- CUSTOMER QUOTES & STATS -->', '  '+news+'  ')

footer_groups = [
    ('Product',[('Intake','/intake'),('Plan','/plan'),('AI','/ai'),('Build','/build'),('Pricing','/pricing'),('Security','/security')]),
    ('Features',[('Asks','/asks'),('Agents','/agents'),('Coding Sessions','/coding-sessions'),('Customer Requests','/customer-requests'),('Insights','/insights'),('Mobile','/mobile'),('Integrations','/integrations'),('Changelog','/changelog')]),
    ('Company',[('About','/about'),('Customers','/customers'),('Careers','/careers'),('Now','/now'),('Method','/method'),('Quality','/quality'),('Brand','/brand')]),
    ('Resources',[('Switch','/switch'),('Download','/download'),('Documentation','/docs'),('Developers','/developers'),('Status','https://linearstatus.com/'),('Enterprise','/enterprise'),('Startups','/startups')]),
    ('Connect',[('Contact us','/contact'),('Community','/join-slack'),('X (Twitter)','https://x.com/linear'),('GitHub','https://github.com/linear'),('YouTube','https://www.youtube.com/@linear')]),
]
mark = re.search(r'<path\b[^>]*>.*?</path>', (root/'linear-official-logo.svg').read_text(), re.S)
assert mark is not None
mark_svg = '<svg width="24" height="24" viewBox="0 0 100 100" fill="currentColor" aria-hidden="true">'+mark.group(0)+'</svg>'
demo_mark = '<svg width="14" height="14" viewBox="0 0 100 100" fill="currentColor" aria-hidden="true">'+mark.group(0)+'</svg>'
html = html.replace('<span class="linear-mark">◒</span>', '<span class="linear-mark">'+demo_mark+'</span>', 1)
footer = '<footer class="linear-current-footer"><div class="linear-footer-main"><a class="linear-footer-mark" aria-label="Linear home" href="https://linear.app/">'+mark_svg+'</a>'
for title, links in footer_groups:
    footer += f'<div><h3>{escape(title)}</h3>'
    for label, href in links:
        url = href if href.startswith('https://') else 'https://linear.app'+href
        footer += f'<a href="{escape(url,quote=True)}">{escape(label)}</a>'
    footer += '</div>'
footer += '</div><div class="linear-footer-legal"><span>Linear Orbital, Inc.</span>'
for label, href in [('Privacy','/privacy'),('Terms','/terms'),('DPA','/dpa'),('AUP','/legal/aup')]:
    footer += f'<a href="https://linear.app{href}">{label}</a>'
footer += '</div></footer>'
replace_span('  <!-- FOOTER (', '  </footer>', '  '+footer+'\n')
html = html.replace('  </footer>\n\n</body>', '\n</body>', 1)

css = '''
#reference-replica .linear-intake-visual,#reference-replica .linear-planning-visual,#reference-replica .linear-ai-visual,#reference-replica .linear-build-visual{height:700px;position:relative;overflow:hidden;background:#101112;color:#a7a9ad}
#reference-replica .linear-intake-columns{display:flex;gap:12px;min-width:1200px;padding:64px 20px 20px 360px;opacity:.76}
#reference-replica .linear-intake-column{width:260px;flex:none}
#reference-replica .linear-intake-column h3,#reference-replica .linear-build-issues h3{font-size:13px;font-weight:500;margin:0 0 12px;color:#b6b8bc}
#reference-replica .linear-intake-column small,#reference-replica .linear-build-issues small{color:#777a80;font-size:11px}
#reference-replica .linear-intake-issue{min-height:82px;border:1px solid #292b2d;background:#1a1b1d;border-radius:9px;margin:8px 0;padding:12px;display:flex;flex-direction:column;gap:5px;font-size:12px}
#reference-replica .linear-thread{position:absolute;top:22px;left:0;width:480px;height:520px;border:1px solid #303133;border-radius:14px;background:#1b1c1e;box-shadow:30px 20px 70px #0008;padding:20px 24px;font-size:14px;line-height:1.5}
#reference-replica .linear-thread-title{padding-bottom:22px;border-bottom:1px solid #303133;font-weight:600;color:#eee}
#reference-replica .linear-thread-title span{font-weight:400;color:#999}
#reference-replica .linear-thread p{margin-top:22px;color:#aaa}
#reference-replica .linear-thread strong{display:block;color:#ddd}
#reference-replica .linear-thread-compose{margin-top:26px;border:1px solid #36383a;border-radius:8px;padding:12px;color:#ddd}
#reference-replica .linear-planning-visual{display:grid;grid-template-columns:1fr 1fr;background:#0c0d0e}
#reference-replica .linear-roadmap{padding:50px 28px;min-width:0;background:repeating-linear-gradient(90deg,transparent 0,transparent 79px,#202123 80px)}
#reference-replica .linear-roadmap-months{display:flex;justify-content:space-between;font-size:11px;color:#777}
#reference-replica .linear-roadmap-row{margin-top:55px;font-size:12px;color:#a7a9ad}
#reference-replica .linear-roadmap-row>div{height:24px;margin-top:8px;background:#1c1d1f;border:1px solid #303134;position:relative}
#reference-replica .linear-roadmap-row i{position:absolute;top:0;height:100%;background:#343537}
#reference-replica .linear-roadmap-row small{position:absolute;top:28px;left:30%;color:#777}
#reference-replica .linear-cycle-chart{border-left:1px solid #303134;background:#191a1c;padding:32px}
#reference-replica .linear-cycle-chart p{font-size:14px;color:#c3c5c7}
#reference-replica .linear-cycle-chart svg{width:100%;height:460px;margin-top:40px}
#reference-replica .linear-chart-grid{stroke:#2d2f31;stroke-width:1;stroke-dasharray:2 5;fill:none}
#reference-replica .linear-chart-line{fill:none;stroke-width:1.3;opacity:.48}
#reference-replica .linear-chart-line.one{stroke:#a96266}.linear-chart-line.two{stroke:#b48559}.linear-chart-line.three{stroke:#697a8d}
#reference-replica .linear-ai-visual{background:linear-gradient(90deg,#0c0d0e,#151617,#0c0d0e)}
#reference-replica .linear-ai-track{display:flex;gap:12px;width:max-content;margin-left:-170px;padding:50px 0}
#reference-replica .linear-ai-card{width:400px;height:585px;flex:none;border:1px solid #303133;border-radius:12px;background:#18191b;padding:20px;font-size:13px}
#reference-replica .linear-ai-card header{font-weight:600;color:#d2d4d7}
#reference-replica .linear-ai-card header small{font-weight:400;color:#777}
#reference-replica .linear-ai-prompt{background:#252628;border-radius:8px;margin-top:30px;padding:14px;color:#c7c9cb}
#reference-replica .linear-ai-status{font-size:11px;color:#777;text-align:right;margin-top:8px}
#reference-replica .linear-ai-result{margin-top:46px;color:#999;line-height:1.6}
#reference-replica .linear-build-visual{display:grid;grid-template-columns:410px 1fr;background:#131415}
#reference-replica .linear-build-issues{overflow:hidden;border-right:1px solid #303133;padding:20px;font-size:12px}
#reference-replica .linear-build-issues h3{padding:12px 0;border-bottom:1px solid #282a2c}
#reference-replica .linear-build-issues>div{display:flex;gap:8px;white-space:nowrap;padding:9px 4px;border-bottom:1px solid #242527}
#reference-replica .linear-build-issues span{overflow:hidden;text-overflow:ellipsis}
#reference-replica .linear-diff{overflow:hidden;color:#bec1c5}
#reference-replica .linear-diff header{height:45px;border-bottom:1px solid #303133;padding:13px 20px;font-size:12px}
#reference-replica .linear-diff-columns{display:grid;grid-template-columns:1fr 1fr}
#reference-replica .linear-diff pre{font-size:11px;line-height:26px;margin:0;padding:16px;border-right:1px solid #303133;overflow:hidden}
#reference-replica .linear-current-changelog{max-width:1280px;margin:0 auto;padding:78px 42px 30px;min-height:550px;border-top:1px solid #242527}
#reference-replica .linear-current-changelog h2{font-size:40px;font-weight:500;letter-spacing:-.03em}
#reference-replica .linear-news-line{display:grid;grid-template-columns:repeat(3,1fr);gap:64px;border-top:1px solid #292a2c;margin:90px 0 54px}
#reference-replica .linear-news-line span{position:relative}
#reference-replica .linear-news-line span:before{content:'';position:absolute;top:-10px;left:0;width:20px;height:20px;border-radius:50%;background:#28292c;border:6px solid #111}
#reference-replica .linear-news-line span:first-child:before{background:#c7656a}
#reference-replica .linear-news-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:64px}
#reference-replica .linear-news-grid h3{font-size:15px;color:#d6d8db;font-weight:500;margin-bottom:8px}
#reference-replica .linear-news-grid p{font-size:15px;color:#8d9197;line-height:24px;display:-webkit-box;-webkit-box-orient:vertical;-webkit-line-clamp:2;overflow:hidden}
#reference-replica .linear-news-grid time{display:block;margin-top:18px;font-size:10px;letter-spacing:.08em;color:#6d7075}
#reference-replica .linear-news-all{display:inline-block;margin-top:48px;font-size:14px;color:#92969b}
#reference-replica .linear-current-footer{background:#111213;border-top:1px solid #262729;padding:54px 42px;color:#8f9298}
#reference-replica .linear-footer-main{display:grid;grid-template-columns:180px repeat(5,1fr);gap:30px;max-width:1280px;margin:auto}
#reference-replica .linear-footer-mark{color:#f8f8f8;font-size:25px}
#reference-replica .linear-footer-main h3{font-size:13px;color:#eceeef;font-weight:500;margin-bottom:18px}
#reference-replica .linear-footer-main a:not(.linear-footer-mark){display:block;margin:9px 0;font-size:13px;color:#8f9298}
#reference-replica .linear-footer-legal{max-width:1280px;margin:70px auto 0;padding-top:24px;border-top:1px solid #292a2c;display:flex;gap:24px;font-size:12px}
#reference-replica .linear-footer-legal span{margin-right:auto}
@media(max-width:800px){#reference-replica .linear-current-changelog{padding:55px 24px}#reference-replica .linear-news-grid{grid-template-columns:1fr;gap:28px}#reference-replica .linear-news-line{display:none}#reference-replica .linear-footer-main{grid-template-columns:repeat(2,1fr)}#reference-replica .linear-footer-mark{grid-column:1/-1}#reference-replica .linear-build-visual,#reference-replica .linear-planning-visual{grid-template-columns:1fr}#reference-replica .linear-cycle-chart{display:none}}
'''
html = html.replace('</head>', '<style>'+css+'</style></head>')
page.write_text(html)
metadata = json.loads((root/'linear-refinements.json').read_text())
metadata['reference_observed_at'] = '2026-09-24T18:54:23.208Z'
metadata['edits'].append('Replace invented feature panels, Changelog cards, and footer links with observed public content')
metadata['remaining'] = ['Whole-page desktop visual comparison and CSS tuning','Responsive visual comparison','Interaction review','Catalog screenshot and publication']
metadata['refined_sha256'] = hashlib.sha256(html.encode()).hexdigest()
(root/'linear-refinements.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')
