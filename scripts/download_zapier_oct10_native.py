from pathlib import Path
import json,urllib.request,hashlib,concurrent.futures
w=Path('.stitch-work/current-official');b='zapier';r=json.loads((w/f'{b}-oct10-native-response.json').read_text())['structuredContent'];s=next(x['design']['screens'][0]for x in r['outputComponents']if 'design'in x)
items=[(f'{b}-oct10-stitch-desktop.html',s['htmlCode']['downloadUrl'],'Native provider raw HTML'),(f'{b}-oct10-stitch-desktop-thumbnail.png',s['screenshot']['downloadUrl'],'Unmodified provider screenshot URL'),(f'{b}-oct10-stitch-desktop.png',s['screenshot']['downloadUrl']+'=w'+s['width'],'Provider full resolution image sizing URL, same repository importer method; verify actual PNG dimensions independently')]
def save(item):
 name,url,method=item
 with urllib.request.urlopen(url,timeout=90)as p:data=p.read()
 (w/name).write_bytes(data)
 return{'file':name,'source_url':url,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'acquisition':method}
with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:records=list(pool.map(save,items))
(w/f'{b}-oct10-native-export-hashes.json').write_text(json.dumps({'projectId':r['projectId'],'sessionId':r['sessionId'],'screen':s['name'],'declaredDimensions':[int(s['width']),int(s['height'])],'files':records},indent=2)+'\n')
print(json.dumps({'screen':s['name'],'files':[{k:x[k]for k in ['file','bytes','sha256']}for x in records]}))
