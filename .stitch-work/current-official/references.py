from pathlib import Path
import json,urllib.request,re,concurrent.futures,datetime
root=Path('.stitch-work/current-official')
urls={
'airbnb':'https://www.airbnb.com/','airtable':'https://www.airtable.com/','apple':'https://www.apple.com/','binance':'https://www.binance.com/en','bmw':'https://www.bmw.com/','bmw-m':'https://www.bmw-m.com/','bugatti':'https://www.bugatti.com/','cal':'https://cal.com/','claude':'https://claude.com/','clay':'https://clay.global/','clickhouse':'https://clickhouse.com/','cohere':'https://cohere.com/','coinbase':'https://www.coinbase.com/','composio':'https://composio.dev/','cursor':'https://cursor.com/','dell-1996':'https://www.dell.com/','elevenlabs':'https://elevenlabs.io/','expo':'https://expo.dev/','ferrari':'https://www.ferrari.com/','figma':'https://www.figma.com/','framer':'https://www.framer.com/','hashicorp':'https://www.hashicorp.com/','hp':'https://www.hp.com/','ibm':'https://www.ibm.com/','intercom':'https://www.intercom.com/','kraken':'https://www.kraken.com/','lamborghini':'https://www.lamborghini.com/','linear.app':'https://linear.app/','lovable':'https://lovable.dev/','mastercard':'https://www.mastercard.com/','meta':'https://www.meta.com/','minimax':'https://www.minimax.io/','mintlify':'https://www.mintlify.com/','miro':'https://miro.com/','mistral.ai':'https://mistral.ai/','mongodb':'https://www.mongodb.com/','nike':'https://www.nike.com/','nintendo-2001':'https://www.nintendo.com/','notion':'https://www.notion.com/','nvidia':'https://www.nvidia.com/','ollama':'https://ollama.com/','opencode.ai':'https://opencode.ai/','pinterest':'https://www.pinterest.com/','playstation':'https://www.playstation.com/','posthog':'https://posthog.com/','raycast':'https://www.raycast.com/','renault':'https://www.renault.com/','replicate':'https://replicate.com/','resend':'https://resend.com/','revolut':'https://www.revolut.com/','runwayml':'https://runwayml.com/','sanity':'https://www.sanity.io/','sentry':'https://sentry.io/','shopify':'https://www.shopify.com/','slack':'https://slack.com/','spacex':'https://www.spacex.com/','spotify':'https://open.spotify.com/','starbucks':'https://www.starbucks.com/','stripe':'https://stripe.com/','supabase':'https://supabase.com/','superhuman':'https://superhuman.com/','tesla':'https://www.tesla.com/','theverge':'https://www.theverge.com/','together.ai':'https://www.together.ai/','uber':'https://www.uber.com/','vercel':'https://vercel.com/','vodafone':'https://www.vodafone.com/','voltagent':'https://voltagent.dev/','warp':'https://www.warp.dev/','webflow':'https://webflow.com/','wired':'https://www.wired.com/','wise':'https://wise.com/','x.ai':'https://x.ai/','zapier':'https://zapier.com/'}
def read(item):
 slug,url=item
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
  with urllib.request.urlopen(req,timeout=35) as r:
   b=r.read(8000000);final=r.geturl();status=r.status
  text=b.decode('utf-8',errors='replace');title=re.search(r'<title[^>]*>(.*?)</title>',text,re.S|re.I)
  (root/(slug+'-source.html')).write_text(text)
  return slug,{'url':url,'resolved_url':final,'http_status':status,'title':re.sub('<[^>]+>','',title[1]).strip() if title else '', 'observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'visual_status':'not_reviewed'}
 except Exception as e:return slug,{'url':url,'error':str(e),'visual_status':'not_reviewed'}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:out=dict(pool.map(read,urls.items()))
(root/'references.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print('Downloaded',sum('http_status' in r for r in out.values()),'of',len(out))
for s,r in out.items():
 if 'error' in r:print(s,r['error'])
