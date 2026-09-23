from pathlib import Path
import re,json,hashlib
p=Path(__file__).parent
raw=p/'linear-stitch.html'
s=raw.read_text()
logo=(p/'linear-official-logo.svg').read_text().strip()
s=re.sub(r'(<a href="https://linear.app/"[^>]*>).*?(</a>)',lambda m:m[1]+logo+m[2],s,count=1,flags=re.S)
# Remove additions absent from the observed public homepage.
s=re.sub(r'\s*<!-- Mock Window Controls Bar -->.*?<!-- App Workspace Interior', '\n<!-- App Workspace Interior',s,count=1,flags=re.S)
s=re.sub(r'<span class="[^"]*animate-pulse[^"]*"></span>','',s)
s=s.replace('Continuous evolution','Changelog')
s=s.replace('<body class=','<body id="reference-replica" class=',1)
css='''
#reference-replica .linear-glow{display:none}
#reference-replica>header{background:#08090a;backdrop-filter:none}
#reference-replica>header>a svg{width:88px;height:22px}
#reference-replica>header nav,#reference-replica>header nav>div:first-child{gap:24px}
#reference-replica>section:first-of-type h1{color:#f7f8f8;letter-spacing:-1.408px}
#reference-replica>section:first-of-type [href$="introducing-loops"]{font-size:16px;gap:12px;margin-bottom:4px}
#reference-replica>section:first-of-type [href$="introducing-loops"]>span:first-child{font-size:16px;background:none;border:none;padding:0;font-weight:400}
#reference-replica>section:nth-of-type(2){margin-top:0;padding-right:0;max-width:1312px}
#reference-replica>section:nth-of-type(2)>div{height:748px;background:#171819}
#reference-replica>section:nth-of-type(2)>div>div{height:100%}
#reference-replica>section:nth-of-type(2) aside{background:#171819}
#reference-replica>section:nth-of-type(2) main{background:#171819;padding:0 72px 32px;position:relative}
#reference-replica>section:nth-of-type(2) main>div:first-child>div:first-child{height:52px;border-bottom:1px solid #26272a;margin:0 -72px 62px;padding:0 24px;display:flex;align-items:center;font-size:12px}
#reference-replica>section:nth-of-type(2) main h2{font-size:20px;font-weight:600;line-height:26px;margin-bottom:8px}
#reference-replica>section:nth-of-type(2) main p{font-size:14px;line-height:21px}
@media(min-width:1100px){
 #reference-replica>section:nth-of-type(3){margin-top:64px;height:145px}
 #reference-replica>section:nth-of-type(4){margin-top:0;padding-top:0;border:0;min-height:886px}
 #reference-replica>section:nth-of-type(5){margin-top:0;padding-top:0;min-height:1235px}
 #reference-replica>section:nth-of-type(6){margin-top:0;padding-top:0;min-height:1237px}
 #reference-replica>section:nth-of-type(7){margin-top:0;padding-top:0;min-height:1241px}
 #reference-replica>section:nth-of-type(8){margin-top:0;padding-top:0;min-height:1253px}
}
'''
s=s.replace('</head>','<style>'+css+'</style></head>')
(p/'linear.html').write_text(s)
(p/'linear-refinements.json').write_text(json.dumps({
 'base_screen':'projects/13522171022650732290/screens/27fe5a6ee6a6469c9e9ee74bd4ebbdb3',
 'reference_url':'https://linear.app/','viewport':{'width':1280,'height':720},'status':'in_visual_review',
 'edits':['Restore actual observed Linear logo','Remove generated extra window chrome and decorative glow','Align first viewport hero and demo placement'],
 'remaining':['Product demo interior fidelity','Full page section comparison','Responsive comparison'],
 'raw_stitch_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'refined_sha256':hashlib.sha256(s.encode()).hexdigest()
},indent=2))
