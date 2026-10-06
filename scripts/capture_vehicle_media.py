#!/usr/bin/env python3
"""Preserve currently observed public media without changing the original bytes."""
import hashlib
import json
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1] / '.stitch-work/current-official'


def capture(item):
    brand, name, url = item
    row = {'source_url': url, 'observed_at': datetime.now(ZoneInfo('Asia/Taipei')).isoformat(),
           'capture_method': 'ordinary public CDN request; original bytes'}
    with tempfile.TemporaryDirectory(prefix='vehicle-media-') as folder:
        target = Path(folder) / 'asset'
        result = subprocess.run(['curl', '--silent', '--show-error', '--location', '--max-time', '45',
                                 '--output', str(target), '--write-out', '%{http_code}', url], capture_output=True)
        row['status'] = int(result.stdout or '0')
        if result.returncode or row['status'] != 200:
            row['error'] = result.stderr.decode(errors='replace').strip() or 'HTTP ' + str(row['status'])
            return brand, False, row
        raw = target.read_bytes()
        if not raw or raw.lstrip().lower().startswith((b'<!doctype html', b'<html')):
            row['error'] = 'Unexpected empty or HTML response'
            return brand, False, row
        relative = brand + '-assets/' + name
        saved = ROOT / relative
        saved.parent.mkdir(parents=True, exist_ok=True)
        saved.write_bytes(raw)
        row.update(path=relative, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
        return brand, True, row


def tasks():
    q = '?auto=format,compress&cs=srgb&sharp=10'
    items = [('bugatti', 'destrier.svg', 'https://bugatti.imgix.net/6a69ff82795c83144775d413/destrier-b-1.svg'+q+'&w=798&dpr=1'),
             ('bugatti', 'solitaire.svg', 'https://bugatti.imgix.net/689394f09fe9b36d362dec02/Solitaire_Wordmark_black_tight.svg'+q+'&w=512&dpr=1'),
             ('bugatti', 'signature.svg', 'https://bugatti.imgix.net/67fd1191e7036b2ee3b81ecb/If%20comparable%20it%20is%20no%20longer%20Bugatti-1.svg'+q+'&w=1246&dpr=1')]
    for name, path, tail in [
        ('maison', '6734a2b6eae7ef2f6d1c330d/02%20BUGATTI_Custmer-Car-Gathering.jpg', '&w=380&dpr=1'),
        ('history', '6734a28b8d33578d8bd2af36/01%20BUGATTI_Type%2035%20Making%20of%20a%20Champion_edit.jpg', '&w=380&dpr=1'),
        ('careers', '6734a52ceae7ef2f6d1c380c/AB105132_Crop.jpg', '&w=380&dpr=1'),
        ('honma', '6a2be22e4df15199c1bfc3dd/bugatti-x-honma-landing-keyvisual-01.jpg', '&w=594&dpr=1'),
        ('cseed', '6a0f12d4de485e5e8455ada5/c-seed-SM_konvert_27.jpg', '&w=594&dpr=1'),
        ('careers-toast', '675dd71ea55eb753a13b8f55/careers_mission_surmesure.jpg', '&fit=crop&ar=4:5&h=328&fp-x=0.5&fp-y=0.5&dpr=1'),
    ]:
        items.append(('bugatti', name+'.jpg', 'https://bugatti.imgix.net/'+path+q+tail))
    for name, logo_id, photo_path in [
        ('tourbillon','67079fd3fa42b0c51df171f2','6733871ced9d56f31c5f0182/bugatti-tourbillon-card.jpg'),
        ('mistral','67079cfafa42b0c51df16f7f','677e8130e825e63ca2bd56fe/bugatti-w16mistral-card_v3.jpg'),
        ('bolide','67079f31fa42b0c51df1719b','6733878496f2c0c4a773f58b/bugatti-bolide-card.jpg'),
        ('chiron','67079f94fa42b0c51df171b9','67338aa2ed9d56f31c5f0689/bugatti-chiron-card-02.jpg'),
        ('divo','67079c56fa42b0c51df16e98','673387e8ed9d56f31c5f01c5/bugatti-divo-card.jpg'),
        ('centodieci','67079bbcfa42b0c51df16dda','6733881f96f2c0c4a773f5b2/bugatti-centodieci-card.jpg'),
    ]:
        items.extend([('bugatti', name+'-logo.png', 'https://bugatti.imgix.net/'+logo_id+'/'+name+'.png'+q+'&w=442&dpr=1'),
                      ('bugatti', name+'.jpg', 'https://bugatti.imgix.net/'+photo_path+q+'&fit=crop&ar=4:5&h=594&fp-x=0.5&fp-y=0.5&dpr=1')])
    for name, asset in [('racing','gateway-scuderia-ferrari-2026-main-launch-desk-AVS'),
                        ('sports','GT-Cover_Auto_Gamma-AVS'),
                        ('collections','FERRARI_FW26_60_16X9_NO%20LOGO%20OPENING-AVS')]:
        items.append(('ferrari', name+'.mpd', 'https://ferrari.scene7.com/is/content/ferrari/'+asset+'.mpd'))
    desktop = ['20260728_NS_HS_PE-07_012-GA-desk','2026_Greatest+Hits+KV_GTW1','ferrari-malfi-po-gate-desk',
               'ferrari-sketch-book-gate-desk','6887356138f4370021589edb-ferrari-166mm-gtw-desk',
               '67bee6a38e935a00568351bf-ferrari-125-s-gate-past-model-launch-desk-2']
    mobile = ['20260728_NS_HS_PE-07_012-GA-mob','2026_Greatest+Hits+KV_GTW2','ferrari-malfi-po-gate-mob',
              'ferrari-sketch-book-gate-mob','68873bcf30b362002146736a-ferrari-166mm-gtw-mob-v2',
              '67bee6a2a680f800114abc15-ferrari-125-s-gate-past-model-launch-mob-2']
    for label, assets, tail in [('desktop',desktop,'?fmt=avif-alpha&wid=1200&hei=800&fit=constrain'),
                                ('mobile',mobile,'?fmt=avif-alpha&wid=960&hei=960&fit=constrain')]:
        for i, asset in enumerate(assets):
            items.append(('ferrari', 'editorial-'+str(i)+'-'+label+'.avif', 'https://ferrari.scene7.com/is/image/ferrari/'+asset+tail))
    for label, assets, tail in [
        ('desktop',['bah-race-report-gtw2','ferrari-salone-provinciale-orientamento-scolastico-2026-news-rullo-2',
                    'gtw2-wec-fuji-2026-race','rullo_mob_Luce-Pebbble_800x900'],'?fmt=avif-alpha&wid=530&hei=597&fit=constrain'),
        ('mobile',['bah-race-report-gtw1','ferrari-salone-provinciale-orientamento-scolastico-2026-news-rullo-1',
                   'gtw1-wec-fuji-2026-race','rullo_desk_Luce-Pebbble_800x900'],'?fmt=avif-alpha&wid=750&hei=500&fit=constrain')]:
        for i, asset in enumerate(assets):
            items.append(('ferrari','news-'+str(i)+'-'+label+'.avif','https://ferrari.scene7.com/is/image/ferrari/'+asset+tail))
    return items


if __name__ == '__main__':
    records = {b: {'assets': [], 'capture_failures': []} for b in ('bugatti','ferrari')}
    with ThreadPoolExecutor(max_workers=6) as pool:
        for brand, success, row in pool.map(capture, tasks()):
            records[brand]['assets' if success else 'capture_failures'].append(row)
    for brand, data in records.items():
        (ROOT / (brand+'-media-provenance.json')).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps({'brand':brand,'captured':len(data['assets']),'failures':data['capture_failures']}),flush=True)
