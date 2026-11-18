#!/usr/bin/env python3
"""Write cargo/jsonld.html: the prototype's JSON-LD, pointed at the Cargo site.

Paste the output into Cargo > Publish Settings > Meta Tags.
Run after `python3 ../prototipo/build.py` so it picks up the latest data.
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).parent
PROTO = HERE.parent / 'prototipo' / 'index.html'
OUT = HERE / 'jsonld.html'

CARGO = 'https://449156.cargo.site'
# Images uploaded in Cargo's Publish Settings (preview image) on 2026-11-17
OG_IMAGE = 'https://freight.cargo.site/w/1200/i/E3235483773140029999971861867770/og-image.jpg'

html = PROTO.read_text(encoding='utf-8')
block = re.search(r'(?s)<script type="application/ld\+json">(.*?)</script>', html).group(1)
site = re.search(r'"url": "(https?://[^"]+?)/"', block).group(1)
data = json.loads(block.replace(site, CARGO))

for node in data['@graph']:
    if node['@type'] == 'Organization':
        node.pop('logo', None)  # the prototype's SVG isn't hosted on Cargo
    if node['@type'] == 'WebPage':
        node['primaryImageOfPage'] = OG_IMAGE
        node.pop('contributor', None)  # comes back with the team section

OUT.write_text('<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + '</script>\n',
               encoding='utf-8')
print(OUT.name, OUT.stat().st_size, 'bytes,', [n['@type'] for n in data['@graph']])
