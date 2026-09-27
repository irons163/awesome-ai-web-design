#!/usr/bin/env python3
"""Replace unobserved Stitch content with the dated Cal.com public reference."""
import calendar
from pathlib import Path

root = Path(__file__).resolve().parent
raw = (root / 'cal-stitch.html').read_text()
for phrase in ('The better way to', 'Partnerships Meeting',
               'With us, appointment scheduling is easy',
               'Smarter, simpler scheduling'):
    assert phrase in raw, phrase
for name in ('cal-sans.woff2', 'cal-sans-ui-light.woff2',
             'matter-regular.woff2', 'matter-semibold.woff2',
             'booking-avatar.png'):
    assert (root / 'cal-assets' / name).is_file(), name


def replace_between(text, start, end, replacement):
    assert text.count(start) == text.count(end) == 1, (start, end)
    a = text.index(start)
    b = text.index(end, a)
    return text[:a] + replacement + '\n\n  ' + text[b:]


header = '''<!-- CURRENT OFFICIAL NAVIGATION, OBSERVED 2026-09-27 -->
<header class="cal-header">
  <div class="cal-navbar">
    <a class="cal-logo" href="https://cal.com/" aria-label="Cal.com home">Cal.com</a>
    <nav class="cal-nav" aria-label="Main navigation">
      <details><summary>Solutions</summary><div class="cal-menu"><a href="https://cal.com/scheduling/sales-teams">Sales</a><a href="https://cal.com/scheduling/marketing">Marketing</a><a href="https://cal.com/scheduling/customer-support">Customer Support</a></div></details>
      <a href="https://cal.com/enterprise">Enterprise</a><a href="https://cal.com/ai">Cal.ai</a>
      <details><summary>Developer</summary><div class="cal-menu"><a href="https://cal.com/docs">Docs</a><a href="https://cal.com/atoms">Cal.com Atoms</a><a href="https://github.com/calcom/cal.com">GitHub</a></div></details>
      <details><summary>Resources</summary><div class="cal-menu"><a href="https://cal.com/blog/category/all-categories">Blog</a><a href="https://cal.com/help">Help Docs</a><a href="https://cal.com/font">Cal Fonts</a></div></details>
      <a href="https://cal.com/pricing">Pricing</a>
    </nav>
    <div class="cal-auth"><a href="https://app.cal.com/auth/login">Sign in</a><a class="cal-dark" href="https://app.cal.com/signup">Get started <span aria-hidden="true">›</span></a></div>
    <details class="cal-mobile"><summary aria-label="Open navigation">☰</summary><div class="cal-menu"><a href="https://cal.com/enterprise">Enterprise</a><a href="https://cal.com/ai">Cal.ai</a><a href="https://cal.com/docs">Developer</a><a href="https://cal.com/pricing">Pricing</a><a href="https://app.cal.com/signup">Get started</a></div></details>
  </div>
</header>'''

hero = '''<!-- SOURCE-BACKED HERO WITH A DATED STATE OF THE LIVE BOOKING CAROUSEL -->
<section class="cal-hero" aria-labelledby="cal-hero-title">
  <div class="cal-hero-left">
    <a class="cal-announcement" href="https://cal.com/blog/calcom-v6-9">Cal.com launches v6.9 <span aria-hidden="true">›</span></a>
    <h1 id="cal-hero-title">The better way to<br>schedule your<br>meetings</h1>
    <p class="cal-hero-description">A fully customizable scheduling software for individuals, businesses taking calls and developers building scheduling platforms where users meet users.</p>
    <div class="cal-signup"><a href="https://app.cal.com/auth/sso/google"><span aria-hidden="true" style="font:bold 16px Arial;background:conic-gradient(#4285f4 0 80deg,#34a853 80deg 160deg,#fbbc05 160deg 240deg,#ea4335 240deg);background-clip:text;color:transparent">G</span> Sign up with Google</a><a href="https://app.cal.com/signup">Sign up with email <span aria-hidden="true">›</span></a></div>
    <p class="cal-credit">No credit card required</p>
  </div>
  <div class="cal-booking-side">
    <div class="cal-booking" aria-label="Cal.com public booking interface sample">
      <div class="cal-person"><img src="cal-assets/booking-avatar.png" alt=""><span class="cal-person-name">Isabella Valce</span><h3>Photoshoot</h3><p class="cal-person-description">Capture your special moments with our professional photography services today.</p><div class="cal-durations"><span>15m</span><span>30m</span><span class="active">45m</span><span>1h</span></div><div class="cal-person-meta"><span><b>◈</b> Rock Wall Woods</span><span><b>◎</b> South America/Rio de Janeiro</span></div></div>
      <div class="cal-calendar"><div class="cal-calendar-title">May 2025</div><div class="cal-week"><span>SUN</span><span>MON</span><span>TUE</span><span>WED</span><span>THU</span><span>FRI</span><span>SAT</span></div><div class="cal-days">{{CALENDAR_DAYS}}</div></div>
    </div>
    <div class="cal-ratings" aria-label="Public review marks observed on Cal.com"><div class="cal-rating trust"><span class="stars">★★★★★</span><strong>★ Trustpilot</strong></div><div class="cal-rating"><span class="stars">★★★★★</span><strong>◉ Product Hunt</strong></div><div class="cal-rating"><span class="stars">★★★★★</span><strong>◉ G2</strong></div></div>
  </div>
</section>'''

blank = ['<span class="cal-day"></span>' for _ in range(4)]
open_days = {6, 8, 9, 20, 21, 22, 23, 27, 28, 29, 30}
days = blank + [
    f'<span class="cal-day{(" selected" if day == 8 else " open" if day in open_days else "")}">{day}</span>'
    for day in range(1, 32)
]
assert calendar.monthrange(2025, 5)[1] == 31
hero = hero.replace('{{CALENDAR_DAYS}}', ''.join(days))

testimonials = '''<!-- OBSERVED TESTIMONIALS; NO STITCH-INVENTED REVIEWS -->
<section class="cal-testimonials py-10">
  <div class="text-center max-w-2xl mx-auto mb-10"><span class="text-sm text-neutral-500">Testimonials</span><h2 class="cal-headline text-5xl mt-3">Don’t just take our word for it</h2><p class="text-neutral-600 mt-3">Our users are our best ambassadors. Discover why we're the top choice for scheduling meetings.</p></div>
  <div class="cal-quote-grid"><article class="cal-quote"><blockquote>“Just gave it a go and it's definitely the easiest meeting I've ever scheduled!”</blockquote><strong>Aria Minaei</strong><small>CEO, Theatre.JS</small></article><article class="cal-quote"><blockquote>“I finally made the move to Cal.com after I couldn't find how to edit events in the Calendly dashboard.”</blockquote><strong>Ant Wilson</strong><small>Co-Founder &amp; CTO, Supabase</small></article><article class="cal-quote"><blockquote>“At Navi, protecting personal health information is a non-negotiable, so choosing Cal.com for scheduling just makes sense.”</blockquote><strong>Micah Friedland</strong><small>CEO &amp; Founder, Navi</small></article></div>
</section>
<section class="cal-wall"><span class="text-sm text-neutral-500">Wall of love</span><h2 class="cal-headline">See why our users love Cal.com</h2><p>Read the impact we've had from those who matter most - our customers.</p><a href="https://app.cal.com/signup">Get started →</a> <a href="https://cal.com/talk-to-sales">Book a demo →</a></section>'''

faq = '''<!-- CURRENT PUBLIC FAQ QUESTIONS; FIRST ANSWER EXPANDED -->
<section class="cal-faq bg-white rounded-2xl cal-border p-8 md:p-12"><div class="mb-6"><span class="text-sm text-neutral-500">FAQ</span><h2 class="cal-headline text-5xl mt-3">Frequently asked questions</h2><p class="text-neutral-600 mt-3">These are some of our most frequently asked questions.</p></div>
  <details open><summary>What is Cal.com and how does it work as a scheduling app?</summary><p>Cal.com is a scheduling app and meeting scheduling software used by over a million people to eliminate booking back-and-forth. You share a link, and Cal.com handles calendar syncing, timezone detection, reminders, and video calls through Zoom, Google Meet, Microsoft Teams, and Cal Video.</p></details>
  <details><summary>What makes Cal.com different from other scheduling apps?</summary><p>Cal.com’s free tier is robust and always free for individuals. It is built for flexibility and customization.</p></details>
  <details><summary>How much does Cal.com cost and what's included in each plan?</summary><p>See the current plan details on Cal.com's pricing page. <a href="https://cal.com/pricing">View pricing →</a></p></details>
  <details><summary>What are Cal.com's pricing plans, and is it good scheduling software for small businesses?</summary><p>See the current plan details on Cal.com's pricing page. <a href="https://cal.com/pricing">View pricing →</a></p></details>
  <details><summary>Can Cal.com be used as scheduling software for Healthcare, Sales, Support, and B2B teams?</summary><p>Cal.com supports those use cases. <a href="https://cal.com/enterprise">Learn more →</a></p></details>
</section>'''

closing = '''<!-- OBSERVED WHITE FINAL CARD -->
<section class="cal-closing"><h2 class="cal-headline">Smarter, simpler scheduling</h2><div class="cal-closing-actions"><a href="https://app.cal.com/signup">Get started &nbsp; ›</a><a href="https://cal.com/talk-to-sales">Talk to sales &nbsp; ›</a></div></section>'''

footer = '''<!-- SOURCE-BACKED MULTI-COLUMN FOOTER -->
<footer class="cal-footer">
  <div class="cal-footer-left"><h3>Cal.com</h3><p>Cal.com® and Cal® are registered trademarks of Cal.com, Inc. All rights reserved.</p><div class="cal-footer-badges"><span>ISO<br>27001</span><span>SOC 2</span><span>CCPA</span><span>GDPR</span><span>HIPAA</span></div><p>Our mission is to connect a billion people by 2031 through calendar scheduling.</p><p><a href="https://status.cal.com/">All Systems Operational</a></p><h4>Downloads</h4><div class="cal-downloads"><a href="https://go.cal.com/android">Android</a><a href="https://go.cal.com/chrome">Chrome</a><a href="https://go.cal.com/safari">Safari</a><a href="https://go.cal.com/edge">Edge</a><a href="https://go.cal.com/firefox">Firefox</a><a href="https://cal.com/download">macOS</a><a href="https://cal.com/download">Windows</a><a href="https://cal.com/download">Linux</a></div><p>Need Help? <a href="mailto:support@cal.com">support@cal.com</a> or visit <a href="https://cal.com/help">cal.com/help</a>.</p></div>
  <div><h4>Solutions</h4><a href="https://cal.com/app">iOS/Android App</a><a href="https://github.com/calcom/cal.com">Self-hosted</a><a href="https://cal.com/pricing">Pricing</a><a href="https://cal.com/docs">Docs</a><a href="https://cal.com/ai">Cal.ai - AI Phone Agent</a><a href="https://cal.com/enterprise">Enterprise</a><a href="https://cal.com/integrate">Integrate Cal.com</a><a href="https://cal.com/routing">Routing</a><a href="https://cal.com/atoms">Cal.com Atoms</a><a href="https://cal.com/download">Desktop App</a><a href="https://cal.com/faq">FAQ</a><a href="https://github.com/calcom/cal.com">GitHub</a></div>
  <div><h4>Use Cases</h4><a href="https://cal.com/scheduling/sales-teams">Sales</a><a href="https://cal.com/scheduling/marketing">Marketing</a><a href="https://cal.com/scheduling/talent-acquisition-teams">Talent Acquisition</a><a href="https://cal.com/scheduling/customer-support">Customer Support</a><a href="https://cal.com/scheduling/higher-education">Higher Education</a><a href="https://cal.com/scheduling/telehealth">Telehealth</a><a href="https://cal.com/scheduling/professional-services">Professional Services</a><a href="https://cal.com/scheduling/hiring-marketplaces">Hiring Marketplace</a><a href="https://cal.com/scheduling/people-operations">Human Resources</a><a href="https://cal.com/scheduling/c-suite">C-suite</a><a href="https://cal.com/scheduling/law">Law</a></div>
  <div><h4>Resources</h4><a href="https://cal.com/help">Help Docs</a><a href="https://cal.com/blog/category/all-categories">Blog</a><a href="https://cal.com/font">Cal Fonts</a><a href="https://cal.com/teams">Teams</a><a href="https://cal.com/embed">Embed</a><a href="https://cal.com/features/recurring-events">Recurring events</a><a href="https://cal.com/docs">Developers</a><a href="https://cal.com/features/workflows">Workflows</a><a href="https://cal.com/features/instant-meetings">Instant Meetings</a><a href="https://cal.com/features/app-store">App Store</a><a href="https://cal.com/features/payments">Payments</a></div>
  <div><h4>Company</h4><a href="https://cal.com/jobs">Jobs</a><a href="https://cal.com/about">About</a><a href="https://cal.com/open">Open Startup</a><a href="https://cal.com/privacy">Privacy</a><a href="https://cal.com/terms">Terms</a><a href="https://cal.com/security">Security</a><a href="https://cal.com/subscribe">Changelog</a><a href="https://cal.com/talk-to-sales">Get a demo</a><a href="https://cal.com/talk-to-sales">Talk to sales</a></div>
</footer>'''

html = raw
html = replace_between(html, '<!-- STICKY / SCROLLING NAVIGATION HEADER -->',
                       '<!-- MAIN WRAPPER -->', header)
html = replace_between(html, '<!-- HERO SECTION (Large White Card Container) -->',
                       '<!-- TRUSTED BY LOGO RAIL -->', hero)
html = replace_between(html, '<!-- TESTIMONIALS / SOCIAL PROOF SECTION -->',
                       '<!-- FREQUENTLY ASKED QUESTIONS SECTION -->', testimonials)
html = replace_between(html, '<!-- FREQUENTLY ASKED QUESTIONS SECTION -->',
                       '<!-- FINAL CTA BANNER -->', faq)
html = replace_between(html, '<!-- FINAL CTA BANNER -->', '</main>', closing)
html = replace_between(html, '<!-- MULTI-COLUMN CAL.COM FOOTER -->',
                       '</body>', footer)

replacements = {
    'Notice and buffers controls to guard your focused work time.':
        'Only get booked when you want to. Set daily, weekly or monthly limits and add buffers around your events to allow you to focus or take a break.',
    'Personalize your brand with clean, memorably short URLs.':
        'Customize your booking link so it’s short and easy to remember for your bookers. No more long, complicated links one can easily forget.',
    'Smooth date selection with dynamic time zone conversion and overlay.':
        'Let your bookers overlay their calendar, receive booking confirmations via text or email, get events added to their calendar, and allow them to reschedule with ease.',
    'Trigger SMS and email workflows before calls to ensure high attendance.':
        'Easily send sms or meeting reminder emails about bookings, and send automated follow-ups to gather any relevant information before the meeting.',
    'Verified custom link': 'Partnerships &amp; Collaborations',
    'Automatic Timezone Sync': '12h &nbsp; 24h',
    'Email reminder (24h before)': 'Meeting starts in 15 mins',
    'SMS reminder (1h before)': 'Booking rescheduled',
    'Delivered': '15 mins',
    'Scheduled': '30 mins',
}
for before, after in replacements.items():
    assert before in html, before
    html = html.replace(before, after)

# The native generation added unsourced subtitles to integration badges.
for unsourced in ('Notifications', 'CRM Sync', 'Lead routing',
                 'Conferencing', 'Workflows'):
    html = html.replace(f'<span class="text-[11px] text-neutral-500">{unsourced}</span>', '')
html = html.replace('<span class="text-[11px] text-neutral-500">Payments</span>', '')
html = html.replace('href="#"', 'href="https://cal.com/talk-to-sales"')
html = html.replace('<title>Cal.com | Reconstructed Homepage</title>',
                    '<title>Cal.com | Scheduling Software for Online Bookings</title>')
style = (root / 'cal-refined.css').read_text()
assert '</head>' in html
html = html.replace('</head>', '<style>\n' + style + '\n</style>\n</head>', 1)
for invention in ('Design Team Lead', 'Engineering Director',
                  'Independent Consultant', 'Automatic Timezone Sync',
                  'Join hundreds of thousands', 'href="#"'):
    assert invention not in html, invention
for heading in ('The better way to', 'With us, appointment scheduling is easy',
                'Your all-purpose scheduling app', 'See why our users love Cal.com',
                'Smarter, simpler scheduling'):
    assert heading in html, heading
html = '\n'.join(line.rstrip() for line in html.splitlines()) + '\n'
(root / 'cal.html').write_text(html)
print('Wrote source-corrected Cal.com dated draft')
