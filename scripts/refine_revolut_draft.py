#!/usr/bin/env python3
"""Refine genuine Stitch exports against the dated rendered UK Revolut homepage."""
import hashlib
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / '.stitch-work/current-official'
ORIGIN = 'https://www.revolut.com'
PROVENANCE = json.loads((WORK / 'revolut-asset-provenance.json').read_text())
ASSETS = PROVENANCE['assets']

def asset(name):
    rows = [r for r in ASSETS if r['source_url'].endswith('/' + name)]
    if len(rows) != 1:
        raise ValueError('Ambiguous or missing official resource: ' + name)
    return rows[0]['path']

def link(text, url):
    if url.startswith('/'):
        url = ORIGIN + url
    return '<a href="' + escape(url, quote=True) + '">' + escape(text) + '</a>'

def cta(text, url='https://get.revolut.com/E528/'):
    return link(text, url).replace('<a ', '<a class="cta" ', 1)

def image(name, cls='', alt=''):
    return '<img class="' + cls + '" src="' + asset(name) + '" alt="' + escape(alt, quote=True) + '">'

def video(desktop, mobile=None, cls='', poster=None):
    attrs = ' class="' + cls + '" autoplay muted loop playsinline preload="metadata"'
    if poster:
        attrs += ' poster="' + asset(poster) + '"'
    return '<video' + attrs + ' data-desktop="' + desktop + '" data-mobile="' + (mobile or desktop) + '" aria-hidden="true"></video>'

MEDIA = 'https://assets.revolut.com/published-assets-v3/'
SKY = 'f94bbcee-b4a0-49f2-8043-c472b47d0ac7.png'
WOMAN = '0eb1515a-91e8-4d4e-8e19-ff7c82de5410.png'
SKY_MOBILE = '2f242895-e89a-44d3-9f8a-fb78b32d80c5.png'
WOMAN_MOBILE = '2442a1d3-8d03-44b9-a046-db33242f100a.png'
PHONE = '8fb2616d-e499-4546-8288-9db34a2e881f.png'
CARD_VIDEO = MEDIA + '5b4c4cc6-f5e3-4013-abb9-02ed70191f31/79c359d8-7025-4121-924b-b7880f97bcf4.mp4'
CARD_VIDEO_MOBILE = MEDIA + 'a3f03841-ddde-4f99-bf75-c2cacf2558b4/eb48080b-a584-4744-9c09-15943a9c0781.mp4'
VIRTUAL_VIDEO = MEDIA + '94a4cf97-5819-45b0-8219-b7b16e94ecac/959ae3c2-0d48-4c3e-a30e-2defda91b1f0.mp4'
VIRTUAL_VIDEO_MOBILE = MEDIA + '808aee1c-ad2e-4005-ae3c-5ce1a5a0837e/7cf0d9a5-2d49-47cc-8b05-da204ccaa15e.mp4'
AIR_VIDEO = MEDIA + '01191ed4-da4e-4f6b-927b-62523ffec28d/b2e3f4d8-5321-4e16-9942-34f83106159b.mp4'
AIR_VIDEO_MOBILE = MEDIA + '4954fed1-0d3f-4a3c-ab32-4ddb30e34976/13038c65-2a71-424a-93cd-544b2c6152d4.mp4'
SECURITY_VIDEO = MEDIA + '7bf7c951-27c0-4ceb-9021-881e85ca6b25/332f5fdd-c0b9-44be-8dea-fc17b3d6ccdf.mp4'
STOCK_VIDEO = MEDIA + 'a07a910c-0df4-45f5-b0ca-7864377877a3/0da52da5-f59c-4863-a918-d8861c032000.mp4'
BADGES = [
    ('91d20a70-1a2d-46e1-8f45-ebd7e83196a8.png', '#3 most downloaded finance app'),
    ('2fb9c781-10a1-4bbf-bb42-7526bcc81286.png', '4.7 out of 5 on Trustpilot'),
    ('dce27cc2-39ac-4f46-b887-46b8e1f5e976.png', "World's Best Digital Bank"),
    ('1bc89c99-4c81-4639-970a-51a8a20a5f5c.png', "World's Best Banks List"),
    ('931fbf11-937a-45d4-9c9d-7078412a8ba9.png', 'Best International Payments Provider 2025'),
    ('3829d1d5-8883-4351-a6a8-a960d419f04e.png', 'Customer Satisfaction — Gold'),
    ('264c79dd-e283-4f7d-9e60-a11079c7fc02.png', 'Consumer Guardian Badge 2025'),
]
SAVINGS = [
    ('Adventure', '7a88c57b-f75a-4e3f-8ab1-4476f7b487d3.png', 'd4473a07-a3bd-47c8-b46d-af2e1ee8e54a.png', 'b703c9e3-0dae-4151-a703-50f5bd61e8cc.png', '60631149-1b04-4ffb-b620-ade697d9d668.png'),
    ('Wedding', 'cde96607-75d5-4a58-b785-991480da4c2f.png', 'a1310b7f-ed8e-4575-b805-d7eac1166bc4.png', '0dc34d59-82c9-47e0-8641-a532b22f5256.png', '3352558a-4eb5-4810-9dbe-4a9c245b61b3.png'),
    ('Moving', 'becea9ab-7462-42d0-913a-6c89c2837708.png', '76336c8a-ffc4-417e-88e9-b023b5edb433.png', '3c0bd2f0-f34c-4547-8890-61e855e0e93e.png', '50faab41-525e-410d-8b14-51f95fed6584.png'),
]
PLANS = [
    ('Standard', 'Free', 'For the financial basics — everything you need for better money management in one place. Sending money abroad or sticking to a budget has never been easier.', '/a-radically-better-account/'),
    ('Plus', '£3.99/month', 'For the smart spender — access additional benefits like better limits for spending abroad and insurance for your purchases, on our affordable paid plan.', '/revolut-plus/'),
    ('Premium', '£7.99/month', 'For elevating every day — access exclusive subscriptions, better savings rates, and exchange unlimited amounts of money.', '/revolut-premium/'),
    ('Metal', '£14.99/month', 'For the global travellers and traders — relax with travel insurance, enjoy enhanced limits, and subscriptions worth £2,200 annually.', '/metal/'),
    ('Ultra', '£55/month', 'For those seeking the best of Revolut — get exceptional benefits like unlimited airport lounge access, monthly global data, partner subscriptions, and cancellation cover.', '/ultra-plan/'),
]
GROUPS = {
    'Global Finances': [('International Transfers','/international-transfers/'),('Lounges','/lounges/'),('Insurance','/global-insurance/')],
    'Investments': [('Stocks','/stock-trading/'),('Stocks & Shares ISA','/stocks-and-shares-isa/'),('Commodities','/commodities-trading/')],
    'Help': [('Contact Us','/contact-us/'),('Help Centre','https://help.revolut.com/help'),('System Status','/system-status/'),('Developers API','https://developer.revolut.com/'),('Site Map','/sitemap/')],
    'Company': [('Sustainability','/sustainability/'),('Code of Conduct','/code-of-conduct/')],
    'Security & Protection': [('How We Protect Your Money','/how-we-keep-your-money-safe/'),('Report Lost Device','/report-lost-device/'),('Learn About Fraud & Scams','/about-fraud-and-scam/'),('Security Bugs','/responsible-disclosure-program/'),('Consumer Security Insight Report','https://assets.revolut.com/pdf/Revolut_Consumer_Security_and_FinCrime_Report_compressed.pdf')],
    'Crypto': [('Crypto','/crypto/'),('Revolut Ramp','/ramp/'),('Revolut X','/revolut-x/')],
    'Plans': [(p[0],p[3]) for p in PLANS] + [('Compare Plans','/our-pricing-plans/')],
    'Revolut AI': [('AIR','/air-ai-by-revolut/')],
    'Accounts': [('Bank Account','/bank-account/'),('Joint Account','/joint-accounts/'),('Professional Account','/revolut-pro/'),('Savings Account','/savings/'),('For ages 16-17','/revolut-for-ages-16-17/'),('Parents and guardians','/revolut-kids-and-teens-parent-and-guardians/')],
    'Mobile & Connectivity': [('Mobile Plans','/mobile-plans/'),('Data Plans','/data-plans/')],
    'Smart Spending': [('Cards','/cards/'),('Send & Receive','/send-and-receive/'),('Money Management','/best-budget-planner/'),('RevPoints','/rev-points/'),('Linked Accounts','/linked-accounts/'),('Shops','/shops/')],
}
MOBILE_ORDER = ['Security & Protection','Help','Plans','Investments','Company','Accounts','Global Finances','Revolut AI','Smart Spending','Crypto','Mobile & Connectivity']
FOOTNOTE = [
    "¹The Annual Equivalent Rate (AER) shows the interest you can earn over 1 year. AER is compounded, so you’ll earn interest on interest already earned. Rates depend on your plan type and savings' currency. Paid plan subscription fees and T&Cs apply. Please refer to the Instant Access Savings T&Cs and our partner T&Cs. For Ultra Plan: Interest is paid at 4% AER (variable) on balances below £200,000, and 3.51% AER (variable) on balances above £200,000. A blended rate applies when your balance exceeds £200,000.",
    '²INVESTMENT SERVICES: capital at risk.',
    'Revolut Trading Ltd provides a non-advised execution-only service in shares. Revolut Trading Ltd does not provide investment advice or personal recommendations. You, as an individual investor, must make your own decisions, seeking independent professional advice if you are unsure as to the suitability or appropriateness of any investment for your individual circumstances or needs.',
    'The value of investments can go up as well as down and you may receive less than your original investment or lose the value of your entire initial investment. Past performance and forecasts are not reliable indicators of future results. Currency rate fluctuations can adversely impact the overall returns on your original investment. Any trades outside of your monthly allowance are charged at 0.25% of the order amount if you are a Standard, Plus, Premium, or Metal customer, or at 0.12% of the order amount if you are an Ultra/Trading Pro customer. Read more on these fees. Further information about the investment service provided by Revolut Trading Ltd can be found in the Terms of Business, Risk Disclosure, and Invest FAQs.',
    'The registered address of Revolut Ltd, Revolut Travel Ltd, and Revolut Trading Ltd is at 30 South Colonnade, London, United Kingdom, E14 5HX. You can read more about our terms and policies here.',
]
LEGAL = [
    '© Revolut Bank UK Ltd 2026 ',
    'To find out more about which Revolut entity you receive services from, check our corresponding FAQ page. If you have any other questions, reach out to us via the in-app chat in the Revolut app.',
    'Revolut Bank UK Ltd is registered in England and Wales (Registered No. 12871051). Registered address: 30 South Colonnade, London, E14 5HX. Authorised by the Prudential Regulation Authority and regulated by the Financial Conduct Authority and Prudential Regulation Authority (Financial Services Register No. 981170).',
    'Revolut Ltd is registered in England and Wales (No. 08804411), is authorised by the Financial Conduct Authority to offer e-money and payment services under the Electronic Money Regulations 2011 (FRN: 900562), and is registered with the Financial Conduct Authority to offer cryptocurrency services under the Money Laundering, Terrorist Financing and Transfer of Funds (Information on the Payer) Regulations 2017. Commodities services are provided by Revolut Ltd and are not regulated by the Financial Conduct Authority.',
    'Investment services are provided by Revolut Trading Ltd (No. 11567840), which is authorised and regulated by the Financial Conduct Authority (FRN: 933846).',
    FOOTNOTE[-1],
]
LEGAL_LINKS = [('Website Terms','/legal/website-terms-and-conditions/'),('Legal Agreements','/legal/'),('Complaints','/legal/complaints-policy/'),('Privacy','/privacy-policy/'),('UK Modern Slavery Policy','/legal/modern-slavery-statement/'),('Customer Vulnerability','/customer-vulnerability/'),('Data Privacy Statement for Candidates','/legal/data-privacy-for-candidates/')]

def paragraphs(values):
    html = ''.join('<p>' + escape(value) + '</p>' for value in values)
    replacements = {
        'Instant Access Savings T&amp;Cs': ('Instant Access Savings T&Cs','/legal/clearbank-savings-terms/'),
        'partner T&amp;Cs': ('partner T&Cs','/legal/clearbank-savings-partner-terms/'),
        'Read more on these fees': ('Read more on these fees','https://help.revolut.com/help/wealth/stocks/trading-stocks/trading-fees/what-fees-will-i-be-charged-for-my-trading/'),
        'Terms of Business': ('Terms of Business','/legal/RTL-terms-of-business/'),
        'Risk Disclosure': ('Risk Disclosure','/legal/RTL-risk-disclosure/'),
        'Invest FAQs': ('Invest FAQs','https://help.revolut.com/help/wealth/'),
        'terms and policies here': ('terms and policies here','/legal/'),
        'FAQ page': ('FAQ page','https://help.revolut.com/help/more/legal-topics/which-revolut-companies-provide-me-with-services/'),
    }
    for text, (label, url) in replacements.items():
        html = html.replace(text, link(label, url))
    return html

def copy(title, text, button, url, legal='', paragraph=True):
    desc = '<p>' + escape(text) + '</p>' if paragraph else escape(text)
    fine = '<div class="fine' + (' wrapped' if paragraph else '') + '">' + ('<p>' + escape(legal) + '</p>' if paragraph else escape(legal)) + '</div>' if legal else ''
    return '<div class="copy"><h2>' + escape(title) + '</h2><div class="desc">' + desc + '</div>' + fine + cta(button,url) + '</div>'

def main():
    # Native candidates remain immutable and independently hashable.
    for device in ('desktop','mobile'):
        if not (WORK / ('revolut-' + device + '-stitch.html')).is_file():
            raise ValueError('Missing native Stitch seed for ' + device)
    fonts = ''.join('@font-face{font-family:"' + family + '";font-style:normal;font-weight:' + weight + ';font-display:swap;src:url("' + asset(file) + '") format("woff2");}' for family,weight,file in [
        ('Aeonik Pro','400','AeonikPro-Regular.woff2'),('Aeonik Pro','500','AeonikPro-Medium.woff2'),('Inter','400','Inter-Regular.woff2'),('Inter','500','Inter-Medium.woff2'),('Inter','600','Inter-SemiBold.woff2')])
    logo_row = next(r for r in ASSETS if r['source_url'] == 'inline-svg:86a8f96a486aeaa0')
    logo = (WORK / logo_row['path']).read_text().replace('fill="var(--rui-color-white)"','fill="currentColor"')
    nav = link('Personal','/') + link('Business','/business/') + '<button type="button" data-kids aria-expanded="false">Kids &amp; Teens</button>' + link('Company','/discover-our-company/')
    menu = '<div id="mobile-navigation" hidden>' + nav + link('Log in','https://app.revolut.com/start') + cta('Sign up') + '</div>'
    header = '<header><div class="header-inner"><a class="wordmark" href="https://www.revolut.com/" aria-label="Revolut">' + logo + '</a><nav class="desktop-nav">' + nav + '</nav><div class="account-links">' + link('Log in','https://app.revolut.com/start') + cta('Sign up') + '</div><button class="menu-button" type="button" aria-label="Open menu" aria-controls="mobile-navigation" aria-expanded="false"><span></span><span></span><span></span></button></div>' + menu + '<div class="kids-links" hidden>' + link('For ages 16-17','/revolut-for-ages-16-17/') + link('Parents and guardians','/revolut-kids-and-teens-parent-and-guardians/') + '</div></header>'
    hero = '<section class="hero"><div class="hero-scene">' + image(SKY,'sky desktop-art') + image(SKY_MOBILE,'sky mobile-art') + image(WOMAN,'woman desktop-art') + image(WOMAN_MOBILE,'woman mobile-art') + image(PHONE,'hero-phone') + '<div class="hero-copy"><h1>Banking &amp; Beyond</h1><p>This is your bank, redefined. Get powerful daily banking and global freedom. Sign up for free in a tap.</p>' + cta('Download the app') + '</div></div><div class="salary"><div class="salary-copy"><h2>Your salary, reimagined</h2><p>Spend smartly, send quickly, sort your salary automatically, and watch your savings grow — all with a Revolut bank account.</p>' + cta('Move your salary') + '</div><div class="salary-carousel"><div class="salary-card portrait">' + image(SKY_MOBILE,'salary-sky') + image(WOMAN_MOBILE,'salary-woman') + image(PHONE,'salary-phone') + '</div>' + image('aab65826-2d49-49f9-803b-061c5c68b842.png','salary-card next') + image('00544e46-b5db-4906-b0ed-87b558057f3f.png','salary-card previous') + '</div><div class="salary-pagination"><button aria-label="Show salary card 1" aria-pressed="true"></button><button aria-label="Show salary card 2" aria-pressed="false"></button><button aria-label="Show salary card 3" aria-pressed="false"></button></div></div></section>'
    # Use each viewport's observed original card photographs. Native exports stay separate.
    salary_composite = '<div class="salary-composite">' + image(SKY,'salary-sky desktop-art') + image(SKY_MOBILE,'salary-sky mobile-art') + image(WOMAN,'salary-woman desktop-art') + image(WOMAN_MOBILE,'salary-woman mobile-art') + image(PHONE,'salary-phone') + '</div>'
    hero = hero.replace('<div class="salary-card portrait">' + image(SKY_MOBILE,'salary-sky') + image(WOMAN_MOBILE,'salary-woman') + image(PHONE,'salary-phone') + '</div>', '<div class="salary-card portrait" data-position="center" data-index="0">' + salary_composite + '</div>')
    for mobile_photo, desktop_photo, position, index in [('aab65826-2d49-49f9-803b-061c5c68b842.png','e0cd59b6-e3e1-4084-b269-a736c0ce8f78.png','right',1),('00544e46-b5db-4906-b0ed-87b558057f3f.png','e306c6b0-8d4e-4b03-ae84-c2e6c4da0904.png','left',2)]:
        old = image(mobile_photo,'salary-card ' + ('next' if index == 1 else 'previous'))
        new = '<picture class="salary-card" data-position="' + position + '" data-index="' + str(index) + '"><source media="(max-width:767px)" srcset="' + asset(mobile_photo) + '">' + image(desktop_photo,alt='Salary account card') + '</picture>'
        hero = hero.replace(old,new)
    awards = '<section class="awards first container"><h2>Join 80+ million customers worldwide and 13 million in the UK</h2><div class="award-grid">' + ''.join('<figure>' + image(name,alt=text) + '<figcaption>' + escape(text) + '</figcaption></figure>' for name,text in BADGES[:4]) + '</div></section><section class="awards second container"><div class="award-grid">' + ''.join('<figure>' + image(name,alt=text) + '<figcaption>' + escape(text) + '</figcaption></figure>' for name,text in BADGES[4:]) + '</div></section>'
    saving_frames = ''.join('<div class="saving-frame" data-savings-frame="' + str(i) + '"' + (' hidden' if i else '') + '><picture><source media="(max-width:767px)" srcset="' + asset(mobile) + '">' + image(desktop,'saving-background') + '</picture><picture><source media="(max-width:767px)" srcset="' + asset(overlay_mobile) + '">' + image(overlay,'saving-overlay','Life, meets savings') + '</picture></div>' for i,(_,desktop,mobile,overlay,overlay_mobile) in enumerate(SAVINGS))
    savings = '<section class="scene savings">' + saving_frames + copy('Life, meets savings','Grow your money with up to 4% AER (variable) interest on Instant Access Savings, paid every day.¹','Explore Savings','/savings/','The rate shown above is for our Ultra plan. Different rates apply per plan. The Annual Equivalent Rate (AER) shows the interest you can earn over 1 year. AER is compounded, so you’ll earn interest on interest already earned. Interest is liable to applicable taxes. Paid plan fees and T&Cs apply.',False) + '<div class="tabs" role="tablist" aria-label="Savings goals">' + ''.join('<button type="button" role="tab" data-savings="' + str(i) + '" aria-selected="' + ('true' if i==0 else 'false') + '">' + label + '</button>' for i,(label,*_) in enumerate(SAVINGS)) + '</div></section>'
    cards = '<section class="scene cards">' + video(CARD_VIDEO,CARD_VIDEO_MOBILE,'physical-video') + video(VIRTUAL_VIDEO,VIRTUAL_VIDEO_MOBILE,'virtual-video') + copy('Elevate your spend','Earn points on your purchases with one of our debit cards. Then redeem them for Airline Miles and other rewards. RevPoints T&Cs apply.','Start earning','https://get.revolut.com/E528/','Some cards available on paid plans only. Fees may apply.',False) + '<div class="tabs" role="tablist" aria-label="Cards"><button role="tab" aria-selected="true" data-card="physical">Physical cards</button><button role="tab" aria-selected="false" data-card="virtual">Virtual cards</button></div></section>'
    air = '<section class="scene air">' + video(AIR_VIDEO,AIR_VIDEO_MOBILE) + copy('Ask, and AIR makes it happen','AI by Revolut, AIR, is your 24/7 personal assistant. Just open your app, swipe, and ask away.','Learn more','/air-ai-by-revolut/') + '</section>'
    secure = '<section class="security container">' + copy('Your money’s safe space','With Revolut Secure, you’re entering the new era of money security — where your bank account has 24/7 protection through proactive, purpose-built defences and a team of specialists.','Learn more','/how-we-keep-your-money-safe/') + video(SECURITY_VIDEO,cls='security-video') + '</section>'
    stocks = '<section class="scene stocks">' + copy('Explore 5,000+ stocks and ETFs','From Apple to Zoom, invest in some of the biggest and most influential companies in the world, commission-free within your monthly allowance.²','Try it out','https://get.revolut.com/E528/','Other fees may apply. Capital at risk.') + video(STOCK_VIDEO,cls='stocks-video',poster='07844b11-869f-4b91-a5e5-ae2605f6c1c8.png') + '</section>'
    closing = '<section class="closing container"><h2>Join the 80+ million using Revolut</h2>' + cta('Download the app') + '</section><section class="footnotes container">' + paragraphs(FOOTNOTE) + '</section>'
    plan_html = '<section class="plans container"><h2>Choose your plan</h2><ul>' + ''.join('<li><a href="' + ORIGIN + url + '"><h2>' + name + '</h2><h3>' + price + '</h3><p>' + escape(desc) + '</p><span class="plan-arrow" aria-hidden="true">→</span></a></li>' for name,price,desc,url in PLANS) + '</ul></section>'
    columns = [('Global Finances','Investments'),('Help','Company'),('Security & Protection','Crypto'),('Plans','Revolut AI'),('Accounts','Mobile & Connectivity'),('Smart Spending',)]
    footer_nav = '<nav class="footer-nav container" aria-label="Footer">'
    for groups in columns:
        footer_nav += '<div class="footer-column">'
        for title in groups:
            footer_nav += '<div class="footer-group" style="--mobile-order:' + str(MOBILE_ORDER.index(title)) + '"><button class="footer-toggle" type="button" aria-expanded="false"><h2>' + escape(title) + '</h2><span aria-hidden="true">⌄</span></button><div class="footer-group-links">' + ''.join(link(text,url) for text,url in GROUPS[title]) + '</div></div>'
        footer_nav += '</div>'
    footer_nav += '</nav>'
    socials = '<div class="social-row container"><a class="wordmark" href="' + ORIGIN + '/" aria-label="Revolut">' + logo + '</a><div>' + ''.join('<a aria-label="' + name + '" href="' + url + '">' + image(file) + '</a>' for name,file,url in [('Facebook','LogoFacebook.svg','https://www.facebook.com/revolut'),('Instagram','LogoInstagram.svg','https://www.instagram.com/revolut/'),('X','LogoTwitter.svg','https://x.com/Revolut'),('LinkedIn','LogoLinkedIn.svg','https://www.linkedin.com/company/revolut'),('TikTok','LogoTikTok.svg','https://www.tiktok.com/@revolut')]) + '</div></div>'
    locales = '<div class="locale-legal container"><span>' + image('GB.webp',alt='') + 'United Kingdom</span><nav>' + ''.join(link(text,url) for text,url in LEGAL_LINKS) + '</nav></div>'
    money = [('India','india'),('Nigeria','nigeria'),('Poland','poland'),('Ghana','ghana'),('Dubai','dubai'),('the UK from India','the-uk-from-india'),('Saudi Arabia','saudi-arabia'),('North Macedonia','north-macedonia'),('Kazakhstan','kazakhstan')]
    currencies = [('GBP','INR'),('USD','GBP'),('GBP','EUR'),('GBP','USD'),('EUR','GBP'),('GBP','PKR'),('GBP','TRY'),('GBP','HKD'),('KRW','GBP'),('AED','GBP'),('INR','GBP'),('GBP','CAD')]
    seo = '<div class="seo container"><p>' + link('International Money Transfers','/money-transfer/') + ': ' + ' | '.join(link('Send Money to '+name,'/money-transfer/send-money-to-'+slug+'/') for name,slug in money) + '</p><p>' + link('Currency Converter','/currency-converter/') + ': ' + ' | '.join(link('Convert '+a+' to '+b,'/currency-converter/convert-'+a.lower()+'-to-'+b.lower()+'-exchange-rate/') for a,b in currencies) + ' | ' + link('Compare Exchange Rates','/compare/') + '</p><p>' + ' | '.join(link('Revolut '+country,'/'+locale+'/money-transfer/') for country,locale in [('USA','en-US'),('Spain','es-ES'),('Australia','en-AU'),('Singapore','en-SG'),('Estonia','ru-EE')]) + '</p></div>'
    seo = seo.replace(link('International Money Transfers','/money-transfer/') + ': ', '<b>' + link('International Money Transfers','/money-transfer/') + ': </b>').replace(link('Currency Converter','/currency-converter/') + ': ', '<b>' + link('Currency Converter','/currency-converter/') + ': </b>')
    seo = seo.replace('<div class="seo container"><p>', '<div class="seo container">').replace('</p><p>', '<br><br>').replace('</p></div>', '</div>')
    css = (ROOT / 'scripts/revolut_draft.css').read_text()
    js = (ROOT / 'scripts/revolut_draft.js').read_text()
    html = '<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Revolut UK — unofficial dated homepage study</title><style>' + fonts + css + '</style></head><body>' + header + '<main>' + hero + awards + savings + cards + air + secure + stocks + closing + '</main><footer>' + plan_html + footer_nav + socials + locales + '<div class="legal container">' + paragraphs(LEGAL) + '</div>' + seo + '</footer><script>' + js + '</script></body></html>'
    (WORK / 'revolut.html').write_text(html)
    # Large captured photos stay in source; hosting retains their original CDN URLs.
    remote_file = ROOT / 'data/official-remote-assets.json'
    remote = json.loads(remote_file.read_text())
    remote['assets'] = [r for r in remote['assets'] if not r['path'].startswith('revolut-assets/')]
    remote['assets'] += [r for r in ASSETS if r['bytes'] > 1_000_000 and r['source_url'].startswith('https://')]
    remote_file.write_text(json.dumps(remote, ensure_ascii=False, indent=2) + '\n')
    native = [{'path':'revolut-'+device+'-stitch'+suffix,'bytes':(WORK / ('revolut-'+device+'-stitch'+suffix)).stat().st_size,'sha256':hashlib.sha256((WORK / ('revolut-'+device+'-stitch'+suffix)).read_bytes()).hexdigest()} for device in ('desktop','mobile') for suffix in ('.html','.png')]
    (WORK / 'revolut-native-export-hashes.json').write_text(json.dumps(native,indent=2)+'\n')
    print(json.dumps({'html_bytes':len(html.encode()),'native_exports':len(native),'captured_assets':len(ASSETS),'hosted_large_assets':'original CDN URLs'}))

if __name__ == '__main__':
    main()
