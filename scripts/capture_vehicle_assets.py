#!/usr/bin/env python3
"""Capture public vehicle-brand CSS/fonts observed in the rendered browser."""
import hashlib
import json
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1] / '.stitch-work/current-official'
ASSETS = {
    'bugatti': [
        ('stylesheet','https://www.bugatti.com/_app/immutable/assets/0.xfduWHPw.css'),
        ('stylesheet','https://www.bugatti.com/_app/immutable/assets/create.BM4r_MQJ.css'),
        ('stylesheet','https://www.bugatti.com/_app/immutable/assets/teaserSizeVariants.B-ZTzIE-.css'),
        ('font','https://www.bugatti.com/fonts/BUGATTIMonospace-Regular.woff2'),
        ('font','https://www.bugatti.com/fonts/BUGATTIDisplay-Regular.woff2'),
        ('font','https://www.bugatti.com/fonts/BUGATTIText-Regular.woff2'),
    ],
    'ferrari': [
        ('stylesheet','https://www.ferrari.com/etc.clientlibs/ferrari-fcom/clientlibs/clientlib-base.lc-3922c1330ee72a5c5c8af9620d7e5426-lc.min.css'),
        ('stylesheet','https://www.ferrari.com/etc.clientlibs/ferrari-fcom/clientlibs/clientlib-dependencies.lc-d41d8cd98f00b204e9800998ecf8427e-lc.min.css'),
        ('stylesheet','https://www.ferrari.com/etc.clientlibs/ferrari-fcom/clientlibs/clientlib-site.lc-3c054323b28f931f45a097506a22bfa3-lc.min.css'),
        ('stylesheet','https://ferrari.scene7.com/is/content/ferraristage/_CSS/fcom-background/fcom-background.css'),
        ('font','https://www.ferrari.com/etc.clientlibs/ferrari-fcom/clientlibs/clientlib-site/resources/fonts/Ferrari-SansRegular.woff2?v=1'),
        ('font','https://www.ferrari.com/etc.clientlibs/ferrari-fcom/clientlibs/clientlib-site/resources/fonts/Ferrari-SansMedium.woff2?v=1'),
        ('font','https://static.apps.ferrarinetwork.ferrari.com/autoloader/v1/static/fonts/Ferrari-SansRegular.32fade35.woff2'),
    ],
}


def capture(task):
    brand, index, kind, url = task
    stamp = datetime.now(ZoneInfo('Asia/Taipei')).isoformat()
    relative = brand + '-assets/' + ('source-' + str(index) + '.css' if kind == 'stylesheet' else url.split('/')[-1].split('?')[0])
    row = {'source_url':url, 'kind':kind, 'observed_at':stamp}
    with tempfile.TemporaryDirectory(prefix='vehicle-reference-') as folder:
        target = Path(folder) / 'asset'
        response = subprocess.run(['curl','--silent','--show-error','--location','--max-time','30','--output',str(target),'--write-out','%{http_code}',url],capture_output=True)
        row['status'] = int(response.stdout or '0')
        if response.returncode or row['status'] != 200:
            row['error'] = response.stderr.decode(errors='replace').strip() or 'HTTP ' + str(row['status'])
            return brand, False, row
        raw = target.read_bytes()
        if raw.startswith(b'<!DOCTYPE') and kind == 'font':
            row['error'] = 'Unexpected HTML instead of a font'
            return brand, False, row
        saved = ROOT / relative
        saved.parent.mkdir(parents=True,exist_ok=True)
        saved.write_bytes(raw)
        row.update({'path':relative,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
        return brand, True, row


if __name__ == '__main__':
    tasks=[(b,i,k,u) for b,values in ASSETS.items() for i,(k,u) in enumerate(values)]
    records={b:{'assets':[],'capture_failures':[]} for b in ASSETS}
    with ThreadPoolExecutor(max_workers=4) as pool:
        for brand,success,row in pool.map(capture,tasks):
            records[brand]['assets' if success else 'capture_failures'].append(row)
    for brand,data in records.items():
        (ROOT / (brand+'-asset-provenance.json')).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps({'brand':brand,'captured':len(data['assets']),'failures':data['capture_failures']}),flush=True)
