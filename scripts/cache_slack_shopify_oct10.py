import pathlib,re,json,urllib.request,urllib.parse,hashlib,concurrent.futures,sys
root=pathlib.Path('.stitch-work/current-official')
for brand in sys.argv[1:]:
 if brand not in ['slack','shopify']:raise ValueError('Out of bounded scope')
 p=root/(brand+'.html');s=p.read_text();assets=root/(brand+'-assets');assets.mkdir(exist_ok=True);manifest=[]
 cssurls=re.findall(r'<link[^>]*href="([^"]+)"[^>]*rel="stylesheet"',s)+re.findall(r'<link[^>]*rel="stylesheet"[^>]*href="([^"]+)"',s)
 cssurls=list(dict.fromkeys(cssurls))
 for u in cssurls:
  u=u.replace('&amp;','&')
  try:
   data=urllib.request.urlopen(u,timeout=35).read();css=data.decode(); css=re.sub(r'url\(([\'"]?)([^)\'\"]+)\1\)',lambda m:'url('+m.group(1)+urllib.parse.urljoin(u,m.group(2))+m.group(1)+')' if not m.group(2).startswith('data:') else m.group(0),css)
   name='oct10-'+hashlib.sha256(u.encode()).hexdigest()[:16]+'.css';(assets/name).write_text(css);local=brand+'-assets/'+name;s=s.replace(u,local);manifest.append({'url':u,'local':local,'sha256':hashlib.sha256(css.encode()).hexdigest(),'bytes':len(css.encode())})
  except Exception as e:manifest.append({'url':u,'error':str(e)})
 # Cache real image and font assets while leaving original public video sources live.
 texts=[s]+[x.read_text() for x in assets.glob('oct10-*.css')]
 urls=set()
 for t in texts:
  for u in re.findall(r'https?://[^\s"\'<>),]+',t):
   u=u.replace('&amp;','&');ext=pathlib.PurePosixPath(urllib.parse.urlparse(u).path).suffix.lower()
   if ext in ['.svg','.png','.jpg','.jpeg','.webp','.avif','.gif','.woff','.woff2','.ttf','.otf']:urls.add(u)
 def fetch(u):
  ext=pathlib.PurePosixPath(urllib.parse.urlparse(u).path).suffix.lower();name='oct10-'+hashlib.sha256(u.encode()).hexdigest()[:20]+ext;dest=assets/name
  try:
   if not dest.exists():dest.write_bytes(urllib.request.urlopen(u,timeout=40).read())
   b=dest.read_bytes();return {'url':u,'local':brand+'-assets/'+name,'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
  except Exception as e:return {'url':u,'error':str(e)}
 with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:manifest+=list(ex.map(fetch,sorted(urls)))
 for item in manifest:
  if 'local' in item:
   # HTML paths are relative to current-official; CSS paths to each brand asset directory.
   s=s.replace(item['url'].replace('&','&amp;'),item['local']).replace(item['url'],item['local'])
 for cssp in assets.glob('oct10-*.css'):
  css=cssp.read_text()
  for item in manifest:
   if 'local' in item:css=css.replace(item['url'],pathlib.Path(item['local']).name)
  cssp.write_text(css)
 p.write_text(s);(root/(brand+'-oct10-assets.json')).write_text(json.dumps(manifest,indent=2));print(brand,'cached',sum('local'in x for x in manifest),'failed',sum('error'in x for x in manifest),'totalBytes',sum(x.get('bytes',0) for x in manifest))
