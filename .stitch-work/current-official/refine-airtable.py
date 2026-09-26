#!/usr/bin/env python3
"""Correct a native Stitch export using the saved 2026-09-22 Airtable HTML evidence.

Keep airtable-stitch.html unchanged. This is a dated, unverified reconstruction.
"""
from html import escape
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
html = (HERE / 'airtable-stitch.html').read_text()


def replace_once(before: str, after: str) -> None:
    global html
    assert html.count(before) == 1, f'Expected one occurrence: {before[:70]!r}'
    html = html.replace(before, after, 1)


def replace_section(start: str, end: str, replacement: str) -> None:
    global html
    assert html.count(start) == 1 and html.count(end) == 1, (start, end)
    a = html.index(start)
    b = html.index(end, a)
    html = html[:a] + replacement + html[b:]


replace_once('<title>Airtable | The platform for operational momentum</title>',
             '<title>Airtable: Build Enterprise-ready AI Workflows, Apps &amp; Agents | Airtable</title>')
replace_once('https://www.gstatic.com/labs-code/stitch/stitch-placeholder-300x300.svg',
             'https://cdn.sanity.io/images/hlcyrtq5/production/b9ca4dd53c0c97beff89fca2827f7e51e-1540x866.jpg')
replace_once('</style>', '''@font-face{font-family:AirtableHaas;src:url(https://static.airtable.com/font/NeueHaasGrotTextRound-55Roman-Web.woff2) format('woff2');font-weight:400;font-display:swap}
@font-face{font-family:AirtableHaas;src:url(https://static.airtable.com/font/NeueHaasGrotTextRound-65Medium-Web.woff2) format('woff2');font-weight:500;font-display:swap}
body{font-family:AirtableHaas,Arial,sans-serif}
.source-table{min-width:790px}.source-table-row{display:grid;grid-template-columns:2.1fr .65fr .85fr 1fr 1fr .75fr 1.35fr;gap:10px;align-items:center;padding:12px 16px;border-bottom:1px solid #eef0f2;font-size:12px}
.source-table-row:first-child{background:#f8f9fa;color:#59616b;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.03em}
.source-table-row:nth-child(even){background:#fff}.source-table-row b{font-weight:600}
</style>''')

# The observed public page supplies these actions, not the generated fragment links.
for before, after in {
    'href="#signup"': 'href="https://airtable.com/signup"',
    'href="#demo"': 'href="https://www.airtable.com/contact-sales"',
    'href="#signin"': 'href="https://airtable.com/login"',
    'href="#enterprise"': 'href="https://www.airtable.com/solutions/enterprise"',
    'href="#pricing"': 'href="https://airtable.com/pricing"',
}.items():
    assert before in html
    html = html.replace(before, after)

for before, after in {
    'Operations app': 'Operations',
    '4 Collaborators': 'Share',
    'Workflows &amp; Views': 'Requests',
    'Filtered by Open Status': 'Software &amp; vendor requests',
    'Group: Department': 'Priority',
    'Sort: Priority': 'This quarter',
    'Real-time sync active': 'Share',
    'Airtable AI Agent': 'Latest activity',
    '3 procurement requests pre-reviewed &amp; routed to Legal.': 'New request — Loom · captured from #software-requests',
    'Airtable Agent workflow active:': 'Software &amp; vendor requests',
    'Monitoring 14 intake channels, syncing Jira &amp; Salesforce contracts': 'New request — Loom · captured from #software-requests',
    'View automation rule →': 'Share →',
}.items():
    assert before in html, before
    html = html.replace(before, after)

accounts = [
    ('Snowflake', 'S', 'Tier 2', '$4-4.5B', 'IPO', '7500', 'www.snowflake.com'),
    ('Figma', 'F', 'Tier 1', '$600-700M', 'Series F', '2500', 'www.figma.com'),
    ('HubSpot', 'H', 'Tier 1', '$1.7-2.3B', 'IPO', '7500', 'www.hubspot.com'),
    ('Canva', 'C', 'Tier 3', '$3-4B', 'Series F', '5000', 'www.canva.com'),
    ('Databricks', 'D', 'Tier 1', '$3-4B', 'Series J', '8000', 'www.databricks.com'),
    ('Miro', 'M', 'Tier 1', '$500-560M', 'Series C', '2500', 'www.miro.com'),
]
cols = ('Account name', 'Logo', 'Tier', 'Estimated ARR', 'Funding stage', 'Employees', 'Website')
rows = ['<div class="source-table-row">' + ''.join(f'<span>{escape(c)}</span>' for c in cols) + '</div>']
for account in accounts:
    rows.append('<div class="source-table-row">' + ''.join(
        f'<span>{"<b>" + escape(v) + "</b>" if i == 0 else escape(v)}</span>'
        for i, v in enumerate(account)) + '</div>')
table = '<!-- Source-backed first-frame table from 2026-09-22 HTML -->\n<div class="source-table">' + ''.join(rows) + '</div>\n'
replace_section('<!-- Structured Table Grid -->',
                '<!-- Live Agent AI banner footer inside collaborative app -->', table)

logo_names = (('Schaeffler', 'schaeffler.svg'), ('Cisco', 'cisco.svg'),
              ('Intuit', 'intuit.svg'), ('eBay', 'ebay.svg'),
              ('Google', 'google.svg'), ("Levi's", 'levis.svg'))
logos = ''.join(
    f'<img alt="{escape(name, quote=True)}" loading="lazy" src="https://static.airtable.com/images/homepage-variant-b/logos-grid/{file}" style="max-width:130px;max-height:38px;width:auto;height:auto">'
    for name, file in logo_names)
replace_section('<!-- Actual-Logo Customer Strip -->', '<!-- Narrative Section:',
                '<section aria-label="Airtable customers" class="border-y border-[#f0f2f5] bg-[#fafbfc] py-12 px-6"><div class="max-w-[1400px] mx-auto flex flex-wrap items-center justify-center gap-10 sm:gap-14 lg:gap-20">' + logos + '</div></section>\n')

for before, after in {
    'Structured, reliable data': 'From a sentence to a system',
    'Build on a shared relational foundation. Connect tables, automate schema validation, and ensure enterprise governance across every business unit.': 'Describe the app you need in plain words, or drop in a spreadsheet you already have.',
    'Explore data platform →': 'AI Play: Campaign Concept Generation →',
    'Native AI workflows': 'Automate the busywork',
    'Surface actionable summaries, route complex tasks to autonomous agents, and synthesize feedback across thousands of records automatically.': 'Set agents on approvals, follow-ups, and updates — and check their work anytime.',
    'See Airtable AI in action →': 'AI Play: Brand Checker →',
    'Empowered teams': 'Run on shared data',
    'Empower product, marketing, and operations teams to build customized software and custom interfaces without waiting on engineering sprint backlogs.': 'All your teams and their agents build on the same records. Change one thing, everyone sees it.',
    'Discover team solutions →': 'AI Play: Customer Insights for Product →',
}.items():
    assert before in html, before
    html = html.replace(before, after)

# The generated bottom campaign and one-line footer were not present in the capture.
replace_section('<!-- Bottom CTA Bar -->', '</main>', '')
footer = '''<footer class="border-t border-[#e5e7eb] bg-white text-sm text-[#323842] px-6 py-16">
<div class="max-w-[1400px] mx-auto grid grid-cols-2 md:grid-cols-5 gap-8">
<div><b>Platform</b><p><a href="https://www.airtable.com/platform/app-building">AI App Building</a></p><p><a href="https://www.airtable.com/platform/ai-agents">AI Agents</a></p><p><a href="https://www.airtable.com/platform">Airtable Platform</a></p></div>
<div><b>Solutions</b><p>Product</p><p>Marketing</p><p>Project Management</p><p>Operations</p><p>Sales</p></div>
<div><b>Resources</b><p><a href="https://www.airtable.com/lp/resources">Resources Hub</a></p><p>Templates</p><p>AI Plays</p><p>Blog</p><p>Customer Stories</p></div>
<div><b>Learn</b><p><a href="https://www.airtable.com/guides">How-to guides</a></p><p><a href="https://airtable.com/developers">Developer docs</a></p><p><a href="https://academy.airtable.com/">Airtable Academy</a></p><p><a href="https://community.airtable.com/">Airtable Community</a></p><p><a href="https://support.airtable.com/">Help center</a></p></div>
<div><b>Company</b><p><a href="https://airtable.com/pricing">Pricing</a></p><p><a href="https://www.airtable.com/contact-sales">Contact sales</a></p><p><a href="https://www.airtable.com/company/trust-and-security">Security</a></p><p><a href="https://www.airtable.com/company/privacy">Privacy</a></p><p><a href="https://www.airtable.com/company/terms-and-policies">Terms</a></p></div>
</div></footer>'''
replace_section('<!-- Global Footer -->', '</footer>', footer)
# replace_section stops before the original closing tag; remove its duplicate.
replace_once('</footer></footer>', '</footer>')

assert 'stitch-placeholder' not in html
assert 'Enterprise Cloud Infrastructure Expansion' not in html
assert 'Structured, reliable data' not in html
(HERE / 'airtable.html').write_text(html)
print('Wrote dated Airtable draft:', len(html), 'characters')
