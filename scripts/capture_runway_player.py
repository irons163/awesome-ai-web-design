#!/usr/bin/env python3
"""Pin and preserve the public hls.js light distribution and its package license."""
import base64
import argparse
import hashlib
import io
import json
import tarfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / '.stitch-work/current-official'


def get(url):
    with urllib.request.urlopen(url,timeout=45) as response:
        if response.status != 200:
            raise ValueError('HLS distribution unavailable')
        data=response.read(12*1024*1024)
        if len(data)==12*1024*1024:
            raise ValueError('Unexpectedly large HLS package')
        return data


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--version',default='1.7.3')
    args=parser.parse_args()
    metadata_url='https://registry.npmjs.org/hls.js/'+args.version
    metadata=json.loads(get(metadata_url))
    dist=metadata['dist']
    tarball=get(dist['tarball'])
    expected=dist['integrity']
    actual='sha512-'+base64.b64encode(hashlib.sha512(tarball).digest()).decode()
    if expected!=actual:
        raise ValueError('HLS package integrity mismatch')
    assets=[]
    with tarfile.open(fileobj=io.BytesIO(tarball),mode='r:gz') as archive:
        for member,filename in [('package/dist/hls.light.min.js','hls.light.min.js'),('package/LICENSE','hls-LICENSE')]:
            data=archive.extractfile(member).read()
            relative='runwayml-assets/'+filename
            (ROOT/relative).write_bytes(data)
            assets.append({'path':relative,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'package_member':member})
    (ROOT/'runwayml-player-provenance.json').write_text(json.dumps({
        'package':'hls.js','version':metadata['version'],'license':metadata['license'],
        'documentation':'https://github.com/video-dev/hls.js',
        'registry_metadata_url':metadata_url,'package_url':dist['tarball'],
        'registry_integrity':expected,'verified_integrity':actual,
        'observed_at':'2026-10-05','assets':assets,
        'use':'MSE fallback for the original publicly observed Runway Mux streams. No alternate media is generated.'
    },indent=2)+'\n')
    print(json.dumps({'version':metadata['version'],'assets':assets}))


if __name__=='__main__':
    main()
