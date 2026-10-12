from pathlib import Path
from html import escape,unescape
import hashlib,json,re
p=Path('.stitch-work/current-official')
s=(p/'ibm.html').read_text()
backup=p/'ibm-oct10-pre-footer-draft.html'
if not backup.exists():backup.write_text(s)
source=(p/'ibm-oct10-source.html').read_text()
source=source[source.index('<c4d-footer '):source.index('</c4d-footer>')+len('</c4d-footer>')]
def clean(s):return unescape(re.sub('<[^>]*>','',s)).strip()
groups=[]
for title,body in re.findall(r'<c4d-footer-nav-group[^>]*title-text="([^"]*)"[^>]*>(.*?)</c4d-footer-nav-group>',source,re.S):
 links=[{'text':clean(t),'href':unescape(u)} for u,t in re.findall(r'<c4d-footer-nav-item[^>]*href="([^"]*)"[^>]*>(.*?)</c4d-footer-nav-item>',body,re.S)]
 groups.append({'title':title,'links':links})
assert [len(x['links']) for x in groups]==[6,5,6,8,0]
legal=[{'text':clean(t),'href':unescape(u)} for u,t in re.findall(r'<c4d-legal-nav-item[^>]*href="([^"]*)"[^>]*>(.*?)</c4d-legal-nav-item>',source,re.S)]
assert len(legal)==4
cards=[]
for i,g in enumerate(groups):
 links=''.join(f'<a href="{escape(x["href"])}">{escape(x["text"])}</a>' for x in g['links'])
 cards.append(f'<section class="footer-group footer-group-{i}"><h3><button type="button" aria-expanded="false" aria-controls="ibm-footer-links-{i}" aria-label="{escape(g["title"] or "More information")}">{escape(g["title"])}<span aria-hidden="true">⌄</span></button></h3><div class="footer-links" id="ibm-footer-links-{i}" hidden>{links}</div></section>')
footer='<footer class="footer"><div class="footer-layout"><a class="footer-brand" href="https://www.ibm.com/ca-en" aria-label="IBM"><img src="ibm-logo.svg" alt="IBM"></a><div class="footer-top">'+''.join(cards)+'</div></div><div class="footer-bottom">'+''.join(f'<a href="{escape(x["href"])}">{escape(x["text"])}</a>' for x in legal)+'<a href="https://www.ibm.com/privacy?lnk=flg-priv-caen">Cookie Preferences</a></div></footer>'
s=re.sub(r'<footer class="footer">.*?</footer>',footer,s,flags=re.S)
css='''
/* Current official IBM footer, source links and collapsed narrow layout. */
.footer{border:0;background:#161616;color:#f4f4f4;padding:60px 16px 32px}.footer-layout{display:grid;grid-template-columns:25% 75%}.footer-brand{padding:0 16px;margin:0!important}.footer-brand img{display:block;width:128px;height:52px;filter:brightness(0) invert(1)}.footer-top{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));grid-template-areas:"discover connect blank" "follow about blank";gap:40px 0}.footer-group{padding:0 16px}.footer-group-0{grid-area:discover}.footer-group-1{grid-area:follow}.footer-group-2{grid-area:connect}.footer-group-3{grid-area:about}.footer-group-4{grid-area:blank}.footer h3{font-size:14px;line-height:20px;font-weight:600;margin:0 0 8px}.footer h3 button{border:0;background:none;color:inherit;font:inherit;padding:0;text-align:left;width:100%}.footer h3 button span{display:none}.footer-links[hidden]{display:block}.footer a{color:#c6c6c6;font-size:14px;line-height:20px;text-decoration:none;margin:0 0 8px}.footer a:hover{text-decoration:underline}.footer-bottom{border-color:#393939;margin:48px 0 0 25%;padding:16px 16px 0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));grid-template-rows:repeat(2,28px);grid-auto-flow:column;gap:0}.footer-bottom a{font-size:14px}
@media(max-width:900px){.footer{padding:0 0 38px}.footer-layout{display:block}.footer-brand{display:block;padding:54px 16px 56px}.footer-top{display:block}.footer-group{padding:0;border-top:1px solid #393939}.footer-group:last-child{border-bottom:1px solid #393939}.footer h3{margin:0;font-weight:400}.footer h3 button{display:flex;align-items:center;justify-content:space-between;padding:0 16px;min-height:47px;cursor:pointer}.footer h3 button span{display:block}.footer-links[hidden]{display:none}.footer-links{padding:8px 16px 16px}.footer-bottom{border:0;margin:0;padding:10px 16px 0;display:block}.footer-bottom a{display:block;margin:0 0 8px}}
'''
s=s.replace('</style>',css+'</style>',1)
s=s.replace('</body>','<script>document.querySelectorAll(".footer-group button").forEach(b=>b.addEventListener("click",()=>{const open=b.getAttribute("aria-expanded")==="true";b.setAttribute("aria-expanded",String(!open));document.getElementById(b.getAttribute("aria-controls")).hidden=open}));</script></body>')
(p/'ibm.html').write_text(s)
(p/'ibm-oct10-footer-provenance.json').write_text(json.dumps({'source':'ibm-oct10-source.html','source_sha256':hashlib.sha256((p/'ibm-oct10-source.html').read_bytes()).hexdigest(),'groups':groups,'legal':legal,'cookie_preferences_note':'Public privacy-page destination used; original cookie-management service is not reproduced.','preview_sha256':hashlib.sha256(s.encode()).hexdigest(),'accepted':False},indent=2)+'\n')
print('IBM footer corrected',hashlib.sha256(s.encode()).hexdigest())
