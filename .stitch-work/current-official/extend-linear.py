"""Replace Stitch's fictional product demo with observed Linear homepage content."""
from pathlib import Path
import hashlib
import json

root = Path(__file__).parent
html = (root / 'linear.html').read_text()
start = html.index('  <!-- PRODUCT DEMO')
end = html.index('  <!-- CUSTOMER LOGOS', start)

demo = '''  <!-- Current public Linear homepage demonstration, observed at 1280 x 720. -->
  <section class="linear-demo-reference" aria-label="A screenshot of the Linear app showing the issue that's currently in progress">
    <div class="linear-app-reference">
      <aside class="linear-app-sidebar">
        <div class="linear-workspace"><span class="linear-mark">◒</span><strong>Linear</strong><span class="linear-chevron">⌄</span><span class="linear-search">⌕</span><span class="linear-new">□</span></div>
        <nav class="linear-primary-nav">
          <div><span>ϟ</span>Pulse</div><div><span>▢</span>Inbox</div><div><span>◌</span>My issues</div><div><span>♧</span>Reviews</div>
        </nav>
        <p class="linear-sidebar-label">Workspace</p>
        <nav class="linear-secondary-nav"><div><span>◇</span>Initiatives</div><div><span>☷</span>Projects</div><div><span>···</span>More</div></nav>
        <p class="linear-sidebar-label">Favorites⌄</p>
        <nav class="linear-favorites"><div class="linear-selected"><span class="linear-yellow">◷</span>Faster app launch</div><div><span>⚑</span>Agent tasks</div><div><span>♧</span>Agent Insights</div><div><span>⚒</span>UI Refresh</div></nav>
      </aside>
      <main class="linear-issue-main">
        <div class="linear-issue-toolbar"><span class="linear-yellow">◷</span><span>DRV-8852</span><span>Faster app launch</span><span class="linear-star">★</span><span class="linear-dots">···</span><span class="linear-issue-count">1 / 84</span></div>
        <div class="linear-issue-body">
          <h3>Faster app launch</h3>
          <p class="linear-description">Render UI before <code>vehicle_state</code> sync when minimum required state is present, instead of blocking on full refresh during iOS startup.</p>
          <div class="linear-activity-heading">Activity</div>
          <div class="linear-activity-line"><span class="linear-avatar">◒</span><span>Linear created the issue via Slack on behalf of Karri · 2min ago</span></div>
          <div class="linear-activity-line"><span class="linear-avatar">◇</span><span>Triage Intelligence added the labels Performance and iOS · 2min ago</span></div>
          <div class="linear-activity-card"><p><span class="linear-avatar">K</span> karri · 4 min ago</p><p>Right now we show a spinner forever, which makes it look like the car disappeared...</p><hr><p><span class="linear-avatar">J</span> jori · just now</p><p>@Linear can you take a stab at this?</p></div>
          <div class="linear-activity-card"><p><span class="linear-avatar">◒</span> Linear connected by Jori · 2 min ago</p><hr><p>Changed 2 files&nbsp; Draft PR awaiting your review · 2 min ago</p></div>
          <div class="linear-activity-line"><span class="linear-yellow">◷</span>Linear moved from Todo to In Progress · just now</div>
        </div>
      </main>
      <div class="linear-agent-panel"><div class="linear-panel-header">Reviews <span>Revert</span></div><div class="linear-agent-request">Fix the dimmed ride rows that never reset and open a PR</div><p class="linear-agent-context">◷ &nbsp; DRV-364 added to context</p><p>Worked for 10 sec</p><p>Pushed and opened a draft PR. Removed dimmedIds — isItemDimmed now checks waitingStatusById directly.</p><div class="linear-agent-pr">Changed 2 files &nbsp;<span>+22 −10</span><br>Draft &nbsp; Reset dimmed ride rows</div><div class="linear-agent-reply">Reply...</div></div>
    </div>
  </section>

'''
html = html[:start] + demo + html[end:]
logos = json.loads((root / 'linear-official-logos.json').read_text())
logo_start = html.index('  <!-- CUSTOMER LOGOS')
logo_end = html.index('  <!-- INTRODUCTION', logo_start)
logo_section = '''  <!-- Seven customer marks observed on Linear's public homepage. -->
  <section class="linear-official-logos"><a href="https://linear.app/customers" aria-label="Customer stories"><div class="linear-logo-row">'''
logo_section += ''.join(f'<span>{svg}</span>' for svg in logos)
logo_section += '''</div></a><p>Powering the companies building the future</p></section>

'''
html = html[:logo_start] + logo_section + html[logo_end:]
css = '''
#reference-replica .linear-demo-reference{max-width:1280px;height:748px;margin:0 auto;padding:0 32px;overflow:hidden}
#reference-replica>section.linear-demo-reference>div.linear-app-reference{height:720px}
#reference-replica .linear-app-reference{position:relative;display:flex;width:calc(100% + 32px);height:720px;border:1px solid #28292b;border-radius:12px;overflow:hidden;background:#191a1c;box-shadow:0 30px 60px rgba(0,0,0,.28);color:#b9bcc3;font-size:13px;line-height:20px}
#reference-replica .linear-app-sidebar{width:240px;flex:none;background:#1b1c1e;border-right:1px solid #303136;padding:16px 16px 0 16px}
#reference-replica .linear-workspace{display:flex;align-items:center;height:32px;gap:8px;padding:0 8px;color:#e2e4e7}
#reference-replica .linear-workspace strong{font-weight:500}
#reference-replica .linear-mark{font-size:18px;color:#f2f3f4}
#reference-replica .linear-chevron{color:#8c9098;font-size:17px}
#reference-replica .linear-search{margin-left:auto;color:#9a9da3;font-size:22px}
#reference-replica .linear-new{font-size:22px;color:#9a9da3}
#reference-replica .linear-primary-nav{margin-top:12px}
#reference-replica .linear-app-sidebar nav div{height:30px;display:flex;align-items:center;gap:10px;padding:0 8px;border-radius:6px}
#reference-replica .linear-app-sidebar nav span{display:inline-block;width:14px;text-align:center;color:#8c9098}
#reference-replica .linear-sidebar-label{margin:17px 0 4px 8px;color:#858992;font-size:12px}
#reference-replica .linear-selected{background:#28292b;color:#e1e4e7}
#reference-replica .linear-favorites .linear-yellow,#reference-replica .linear-issue-toolbar .linear-yellow,#reference-replica .linear-activity-line .linear-yellow{color:#dccb69}
#reference-replica>section.linear-demo-reference main.linear-issue-main{flex:none;width:660px;padding:0;background:#1b1c1e;border-right:1px solid #303136}
#reference-replica .linear-issue-toolbar{height:52px;display:flex;align-items:center;gap:8px;padding:0 24px;border-bottom:1px solid #303136;font-size:12px;color:#b9bcc3;white-space:nowrap}
#reference-replica .linear-star{margin-left:4px;color:#ead26e}
#reference-replica .linear-dots{color:#a2a5aa}
#reference-replica .linear-issue-count{margin-left:auto;color:#666a71}
#reference-replica .linear-issue-body{padding:62px 72px 30px;overflow:hidden}
#reference-replica .linear-issue-body h3{font-size:20px;line-height:27px;font-weight:600;margin:0 0 8px;color:#dfe1e4}
#reference-replica .linear-description{font-size:14px;line-height:21px;color:#a7aab1}
#reference-replica .linear-description code{background:#2a2b2e;border:1px solid #37383b;border-radius:4px;color:#d0d2d6;padding:2px 4px;font-size:13px}
#reference-replica .linear-activity-heading{margin:34px 0 20px;font-size:14px;font-weight:600;color:#e1e4e7}
#reference-replica .linear-activity-line{display:flex;align-items:center;gap:10px;margin-bottom:12px;color:#888c94;font-size:12px;white-space:nowrap}
#reference-replica .linear-avatar{display:inline-flex;align-items:center;justify-content:center;width:14px;height:14px;border-radius:50%;background:#4c4e54;color:#fff;font-size:10px;flex:none}
#reference-replica .linear-activity-card{background:#242528;border:1px solid #34353a;border-radius:8px;padding:12px 16px;margin:22px -72px 18px -16px;font-size:12px;color:#aaaeb5}
#reference-replica .linear-activity-card p{margin:0 0 7px}
#reference-replica .linear-activity-card hr{border:0;border-top:1px solid #34353a;margin:12px -16px}
#reference-replica .linear-agent-panel{flex:1;background:#1a1b1d;padding:68px 20px 20px;color:#8c9097;min-width:260px;font-size:12px}
#reference-replica .linear-panel-header{font-size:12px;display:flex;justify-content:space-between}
#reference-replica .linear-agent-request{margin-top:22px;border-radius:8px;background:#252629;padding:12px 10px;color:#cdd0d4}
#reference-replica .linear-agent-panel p{margin-top:16px}
#reference-replica .linear-agent-context{color:#686d75}
#reference-replica .linear-agent-pr{margin-top:16px;border:1px solid #303238;border-radius:8px;background:#242528;padding:10px;color:#bfc2c7}
#reference-replica .linear-agent-pr span{color:#7db69c}
#reference-replica .linear-agent-reply{position:absolute;right:10px;bottom:12px;width:315px;height:100px;border:1px solid #36383b;border-radius:8px;padding:12px;color:#656a72}
#reference-replica>section.linear-official-logos{height:145px;max-width:1280px;margin:52px auto 0;padding:0 40px;border:0}
#reference-replica .linear-logo-row{display:flex;justify-content:space-between;align-items:center;width:100%;height:40px;color:#f5f6f7}
#reference-replica .linear-logo-row>span{display:flex;align-items:center;justify-content:center}
#reference-replica .linear-official-logos p{margin-top:28px;color:#61656e;text-transform:uppercase;font-family:monospace;font-size:10px;letter-spacing:.03em}
'''
html = html.replace('</head>', '<style>' + css + '</style></head>')
(root / 'linear.html').write_text(html)
meta = json.loads((root / 'linear-refinements.json').read_text())
meta['edits'].append('Replace invented demo copy with observed public Linear issue/sidebar/activity content')
meta['edits'].append('Replace invented customer names with seven exact official SVG logos')
meta['refined_sha256'] = hashlib.sha256(html.encode()).hexdigest()
meta['remaining'] = ['Visual comparison and layout adjustment of product demo', 'Replace fictional feature illustrations and metrics', 'Current footer and changelog links', 'Responsive comparison']
(root / 'linear-refinements.json').write_text(json.dumps(meta, indent=2))
