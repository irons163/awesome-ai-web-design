import concurrent.futures
import hashlib
import json
import pathlib
import re
import shutil
import urllib.request
from html import escape

ROOT = pathlib.Path(__file__).resolve().parents[1]
P = ROOT / '.stitch-work/current-official'
old = P / 'ibm-sep28-draft-preserved.html'
if not old.exists():
    shutil.copy2(P / 'ibm.html', old)
s = old.read_text()
reference = json.loads((P / 'ibm-oct10-official-desktop-reference.json').read_text())
asset_dir = P / 'ibm-oct10-assets'
asset_dir.mkdir(exist_ok=True)

def fetch(image):
    url = image['currentSrc']
    name = hashlib.sha256(url.encode()).hexdigest()[:20] + '.avif'
    path = asset_dir / name
    if not path.exists():
        data = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=45).read()
        path.write_bytes(data)
    return {'url': url, 'file': path.relative_to(P).as_posix(), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'bytes': path.stat().st_size, 'alt': image['alt']}

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    assets = list(executor.map(fetch, reference['images'][:5]))
(P / 'ibm-oct10-asset-provenance.json').write_text(json.dumps(assets, indent=2))
s = s.replace('Scale AI through governance', 'Own your digital future, on your terms')
s = re.sub(r'<p class="hero-description">.*?</p>', '<p class="hero-description">Protect your data, maintain full transparency and deploy AI with accountability</p>', s)
s = s.replace('https://www.ibm.com/fr-fr/reports/state-of-salesforce?lnk=hpls1caen', 'https://www.ibm.com/forms/mkt-whitepaper-20992?lnk=hpls1caen').replace('Download the full report', 'Path to digital sovereignty')
s = s.replace('https://www.ibm.com/consulting/salesforce?lnk=hpls2caen', 'https://ibm.webcasts.com/starthere.jsp?ei=1748947&amp;tp_key=27bde79fa6?lnk=hpls2caen').replace('Drive smarter transformation', 'How Digital Sovereignty Shapes Business Imperatives')
s = s.replace('ibm-browser-images/72be7c966a1a5eeb3ad0.avif', assets[0]['file'])
news = [('New IBM CHRO Study: Canadian Employees Worry AI Is Eroding Skills as Critical Thinking Gains Importance', 'https://canada.newsroom.ibm.com/2026-10-02-New-IBM-CHRO-Study-Canadian-Employees-Worry-AI-Is-Eroding-Skills-as-Critical-Thinking-Gains-Importance'), ('IBM Study: Canadian Sports Fans Expect More From the Fan Experience as AI Reshapes Sports', 'https://canada.newsroom.ibm.com/2026-27-08-IBM-Study-Canadian-Sports-Fans-Expect-More-From-the-Fan-Experience-as-AI-Reshapes-Sports')]
s = re.sub(r'<aside class="news">.*?</aside>', '<aside class="news"><h2>Latest News</h2>' + ''.join(f'<a href="{escape(url)}"><span class="news-label">{escape(label)}</span><span class="news-arrow">→</span></a>' for label, url in news) + '<div class="news-dots"><b>1</b><span>2</span><span>3</span><span>4</span></div></aside>', s)
rec = [('Learn', 'Digital sovereignty solutions', 'https://www.ibm.com/solutions/digital-sovereignty?lnk=hprc1caen'), ('Free trial', 'Experience the full power of IBM Bob: Get 50 Bobcoins for 30 days', 'https://bob.ibm.com/trial?lnk=hprc2caen'), ('News', 'IBM Cloud announces Sovereignty Risk Profile', 'https://newsroom.ibm.com/blog-ibm-cloud-announces-sovereignty-risk-profile?lnk=hprc2caen'), ('Webinar', 'Learn from Maximo experts specializing in Energy & Utilities and Manufacturing', 'https://ibm.webcasts.com/starthere.jsp?ei=1775634&tp_key=0fdff6f221&sti=web?lnk=hprc3caen')]
cards = ''.join(f'<a class="recommend-card" href="{escape(url)}"><img src="{assets[i+1]["file"]}" alt="{escape(assets[i+1]["alt"])}"><span class="copy"><small>{escape(kicker)}</small><strong>{escape(label)}</strong></span></a>' for i, (kicker, label, url) in enumerate(rec))
s = re.sub(r'<section class="recommend">.*?</section>', '<section class="recommend"><h2 class="eyebrow">Recommended for you</h2><div class="recommend-grid">' + cards + '</div></section>', s)
css = '''
/* Current public reference correction, 2026-10-10. */
html{scroll-behavior:auto}.hero{grid-template-columns:minmax(0,452px) minmax(0,1fr) 156px;min-height:600px;padding-bottom:66px}.hero-visual{min-width:0;max-width:100%}.hero h1{font-size:47.25px;line-height:1.19;max-width:420px}.hero-description{margin-top:104px}.hero-actions{margin-top:32px}.hero-actions .action{min-height:114px;align-items:flex-start;padding-top:14px;border-radius:3px}.news h2{margin-bottom:48px}.news>a{height:164px;margin:0 0 30px;padding:0 0 28px;overflow:hidden;line-height:24px}.news>a .news-label{display:-webkit-box;-webkit-box-orient:vertical;-webkit-line-clamp:4;overflow:hidden;margin:0}.news>a .news-arrow{margin-top:16px}.recommend{padding-left:16px!important;padding-right:16px!important;border:0;padding-top:24px;padding-bottom:61px}.recommend-grid{gap:0}.recommend-card{min-height:144px;flex-direction:row;border:0;border-left:1px solid #e0e0e0;padding:16px}.recommend-card img{width:80px;height:80px;flex-shrink:0}.recommend-card .copy{padding:0 0 0 16px}.recommend-card small{font-size:14px}.recommend-card strong{font-size:16px;line-height:24px}.section-title{font-size:47.25px;line-height:1.19}.impact{padding-top:32px;padding-bottom:72px}.impact-card{min-height:470px}.impact-card .main{font-size:28px}.impact-card img{width:128px;height:80px;object-fit:contain}.technology-grid{grid-template-columns:repeat(4,minmax(0,1fr))}.tech-card{min-width:0}.connected>.section-title{font-size:32px}.newsletter h3{font-size:32px}.footer-top{grid-template-columns:repeat(2,minmax(0,1fr))}
@media(max-width:900px){.hero{padding-top:32px;padding-bottom:30px;min-height:0}.hero h1{font-size:32.7955px;line-height:1.22;max-width:358px}.hero-description{margin-top:56px}.hero-actions{margin-top:30px}.hero-actions .action{min-height:64px;width:288px;padding-top:14px}.hero-visual{margin-top:32px}.news{display:none}.recommend{padding-top:28px;padding-bottom:38px}.recommend-grid{grid-template-columns:1fr}.recommend-card{min-height:147px;padding:16px;border-left:0;border-bottom:1px solid #e0e0e0}.recommend-card img{width:80px;height:80px}.section-title{font-size:32.7955px}.impact-card{min-height:340px}.technology-grid{grid-template-columns:1fr}.footer-top{grid-template-columns:1fr}.footer h3{font-size:14px}.connected>.section-title,.newsletter h3{font-size:32px}}
'''
s = s.replace('</style>', css + '</style>', 1)
(P / 'ibm.html').write_text(s)
print('IBM corrected', hashlib.sha256(s.encode()).hexdigest(), len(assets))
