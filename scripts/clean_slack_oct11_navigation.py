from pathlib import Path
import re,json,hashlib,datetime
w=Path('.stitch-work/current-official');p=w/'slack.html';before=p.read_text();oldhash=hashlib.sha256(p.read_bytes()).hexdigest();changes=[]
def clean(m):
 url=m.group(1)
 if not re.search(r'[?&]_gl=',url):return m.group(0)
 base,query=url.split('?',1);fragment=''
 if '#'in query:query,fragment=query.split('#',1);fragment='#'+fragment
 sep='&amp;' if '&amp;'in query else '&'
 parts=query.split(sep);removed=[x for x in parts if x.split('=',1)[0]=='_gl'];kept=[x for x in parts if x.split('=',1)[0]!='_gl']
 assert len(removed)==1
 cleanurl=base+('?' +sep.join(kept) if kept else '')+fragment
 changes.append({'attribute':'href','beforeUrlSha256':hashlib.sha256(url.encode()).hexdigest(),'afterUrl':cleanurl,'removedParameter':'_gl','removedValueDisclosed':False})
 return 'href="'+cleanurl+'"'
after=re.sub(r'href="([^"]*)"',clean,before);assert len(changes)==2
assert not re.search(r'[?&]_gl=',after)
p.write_text(after);finalhash=hashlib.sha256(p.read_bytes()).hexdigest()
proof={'recordedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'priorFullPageSha256':oldhash,'finalSha256':finalhash,'onlyChanges':'Exactly two href attributes have their _gl query parameter removed; all other bytes unchanged. SVG ID containing _gl is an unrelated artwork identifier and remains unchanged.','changeCount':2,'changes':changes,'visualContentStylesRuntimeAndAssetsUnchanged':True,'method':'Single regex pass rewrites only matching href attributes, preserving all other source bytes; values intentionally not printed or included in proof.','finalActualSupplementsPending':True}
(w/'slack-oct11-navigation-cleanup-proof.json').write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps({'brand':'slack','priorSha256':oldhash,'finalSha256':finalhash,'removedQueryKeys':2,'queryValueDisclosed':False}))
