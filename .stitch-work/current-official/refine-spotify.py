from pathlib import Path
import re,json,hashlib
p=Path('.stitch-work/current-official')
raw=p/'spotify-stitch.html'
if not raw.exists():raw.write_bytes((p/'spotify.html').read_bytes())
s=raw.read_text()
images=['ab67616d00001e02ac9d5d5263e9f03802d6864c','ab67616d00001e02322b8ded39dc108536090089','ab67616d00001e027013f42ca4a4d0965d5ad6c1','ab67616d00001e021bababe27a46e73f16d7b619','ab67616d00001e021df7da7e2f1430731f1db26c','ab67616d00001e02c2452dcf7d9dbbff64574d27','ab67616100005174c1719ac9e6a75c1c25835018','ab67616100005174aadc18cac8d48124357c38e6','ab676161000051744293385d324db8558179afd9','ab6761610000517439ba6dcd4355c03de0b50918','ab67616100005174cb565a8e684e3be458d329ac','ab67616100005174e17c0aa1714a03d62b5ce4e0']
for asset in images:s=s.replace('https://www.gstatic.com/labs-code/stitch/stitch-placeholder-300x300.svg','https://i.scdn.co/image/'+asset,1)
assert 'stitch-placeholder' not in s
s=s.replace('title="ADÉLA">ADÉLA','title="Nicole Kidman">Nicole Kidman').replace('title="Nicole Kidman">Nicole Kidman</div>\n</div>','title="ADÉLA"><small class="explicit">E</small> ADÉLA</div>\n</div>',1)
s=s.replace('>Last Thing You Need</div>','>Last Thing You Need (from GTAVI: The Album)</div>').replace('>MISS MY DAWG</div>','>MISS MY DAWG (feat. Drake)</div>').replace('>RHYNO</div>','>RHYNO (from GTAVI: The Album)</div>')
s=s.replace('>Yeat, Drake</div>','><small class="explicit">E</small> Yeat, Drake</div>').replace('>Travis Scott, Grand Theft Auto VI</div>','><small class="explicit">E</small> Travis Scott, Grand Theft Auto VI</div>')
start=s.index('<aside ');end=s.index('</aside>',start)+len('</aside>')
s=s[:start]+'''<aside class="library-reference">
<header><strong>Your Library</strong><button aria-label="Create">＋</button></header>
<div class="library-scroll">
<section><strong>Create your first playlist</strong><p>It's easy, we'll help you</p><button>Create playlist</button></section>
<section><strong>Let's find some podcasts to follow</strong><p>We'll keep you updated on new episodes</p><button>Browse podcasts</button></section>
</div>
<footer><div class="legal-links"><a href="https://www.spotify.com/legal/">Legal</a><a href="https://www.spotify.com/safety-and-privacy-center/">Safety &amp; Privacy Center</a><a href="https://www.spotify.com/legal/privacy-policy/">Privacy Policy</a><a href="https://www.spotify.com/legal/cookies-policy/">Cookies</a><a href="https://www.spotify.com/legal/privacy-policy/">About Ads</a><a href="https://www.spotify.com/accessibility/">Accessibility</a></div><a class="cookies-link" href="https://www.spotify.com/legal/cookies-policy/">Cookies</a><button class="language"><span>◎</span> English</button></footer>
</aside>'''+s[end:]
css='''
/* Refinements measured from the public Spotify page at 1280x720. */
body>header>div[class*="left-[692px]"]{gap:8px}body>header>div[class*="left-[692px]"]>a{margin:0!important}
body>header input{font-size:16px!important;padding-left:0!important}
body>header [href="https://www.spotify.com/signup"]{font-size:14px!important}
body>main{padding:0 8px;gap:8px}
body>main>section{flex:none;width:922px;scrollbar-width:none}
body>main>section>div{padding:23px 40px 60px}
body>main>section>div>div:first-child{height:351px;margin-bottom:0}
body>main>section>div>div>div:first-child{height:29px;margin-bottom:20px}
body>main>section>div>div:nth-child(2)>div:first-child{margin-bottom:16px}
body>main>section h2{line-height:29px;letter-spacing:0}
body>main>section>div>div>div:nth-child(2){padding:0;width:calc(100% + 40px);gap:24px}
.card-item{padding:0;width:153.73px}
.card-item>div:first-child{width:153.73px;height:153.73px;border-radius:4px}
body>main>section>div>div:nth-child(2) .card-item>div:first-child{border-radius:50%}
.card-item>div:nth-child(2){padding:0;margin-top:8px}
.card-item>div:nth-child(2)>div:first-child{font-weight:400;line-height:22px;display:-webkit-box;-webkit-line-clamp:2}
.card-item>div:nth-child(2)>div:nth-child(2){line-height:21px;margin-top:4px}
.explicit{display:inline-block;background:#b3b3b3;color:#121212;line-height:14px;height:14px;width:14px;text-align:center;font-size:10px;font-weight:700}
.library-reference{width:294px;height:574px;flex:none;background:#121212;border-radius:8px;position:relative;overflow:hidden}
.library-reference header{position:absolute;left:20px;right:16px;top:16px;height:35px;display:flex;align-items:center;justify-content:space-between;font-size:16px}
.library-reference header button{background:#1f1f1f;color:#b3b3b3;width:35px;height:35px;border-radius:50%;font-size:25px;font-weight:400}
.library-scroll{position:absolute;left:8px;right:8px;top:91px;height:260px;overflow-y:auto;scrollbar-width:none}
.library-scroll section{padding:16px 20px;background:#1f1f1f;border-radius:8px;min-height:133px;margin-bottom:24px;font-size:16px;line-height:22px}
.library-scroll p{font-size:14px;line-height:20px;margin-top:8px}
.library-scroll button{height:32px;background:white;color:black;border-radius:20px;font-weight:700;font-size:14px;padding:0 16px;margin-top:20px}
.library-reference footer{position:absolute;top:380px;left:24px;right:24px;background:#121212}
.legal-links{display:flex;gap:8px 16px;flex-wrap:wrap;font-size:12px;line-height:17px;color:#b3b3b3}
.cookies-link{display:block;font-size:12px;line-height:22px;margin-top:12px}
.language{display:flex;align-items:center;gap:5px;height:32px;width:101px;border:1px solid #727272;border-radius:20px;font-weight:700;font-size:14px;margin-top:32px;justify-content:center}.language span{font-size:23px;font-weight:400}
body>footer{border-radius:0!important;background:linear-gradient(90deg,#ae2997,#519bf5)!important;padding-left:16px!important}
body>footer>div:first-child>div:first-child{font-size:14px!important;letter-spacing:0!important;text-transform:none!important}
.reference-now-playing{position:absolute;left:1240px;top:64px;width:32px;height:574px;border-radius:8px;background:#121212;color:#b3b3b3;display:flex;align-items:center;justify-content:center;font-size:24px}
'''
css=re.sub(r'/\*.*?\*/','',css,flags=re.S)
css=re.sub(r'(^|})([^{}]+)\{', lambda m: m[1]+','.join(('#reference-replica'+part.strip()[4:] if part.strip().startswith('body') else '#reference-replica '+part.strip()) for part in m[2].split(','))+'{', css)
s=s.replace('<body ', '<body id="reference-replica" ',1)
s=s.replace('</head>','<style>'+css+'</style></head>').replace('</body>','<button class="reference-now-playing" aria-label="Show Now Playing view">‹</button></body>')
s=s.replace('PREVIEW OF SPOTIFY','Preview of Spotify')
(p/'spotify.html').write_text(s)
(p/'spotify-refinements.json').write_text(json.dumps({'base_screen':'projects/17774991018148174598/screens/c3ec8812116f4795b959f071c398543b','reference_url':'https://open.spotify.com/','viewport':{'width':1280,'height':720},'status':'in_visual_review','edits':['Restore exact observed public album/artist asset URLs','Correct initial viewport positions and typography','Restore official labels and library structure'],'raw_stitch_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'refined_sha256':hashlib.sha256(s.encode()).hexdigest()},indent=2))
