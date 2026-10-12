import hashlib
import json
import re
import sys
import unittest
import zipfile
from html.parser import HTMLParser
from html import unescape
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from rewrite_prompts import make_prompts, remove_upstream_instructions, MARKER
from build import contrast_ink, luminance

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]
    def handle_starttag(self,tag,attrs):
        for key,value in attrs:
            if key in ('href','src','poster') and value:
                self.links.append(value)


class PageDependencies(Links):
    """Read actual markup and CSS, including decoded inert page templates."""
    def __init__(self):
        super().__init__(); self.css=[]; self.in_style=False
    def handle_starttag(self, tag, attrs):
        super().handle_starttag(tag, attrs)
        self.in_style = self.in_style or tag == 'style'
        for key, value in attrs:
            if key == 'style' and value:
                self.css.append(value)
            elif key == 'srcset' and value:
                # URL tokens may contain commas in query values; descriptors
                # and whitespace delimit candidates in the HTML algorithm.
                rest=value
                while rest.strip(' \t\n\r,'):
                    rest=rest.lstrip(' \t\n\r,')
                    match=re.match(r'\S+',rest)
                    token=match.group(0); rest=rest[len(token):]
                    candidate=token.rstrip(',')
                    # An upstream data-image placeholder has an empty 2x
                    # candidate; a density descriptor is not a local URL.
                    if not re.fullmatch(r'\d+(?:\.\d+)?[wx]',candidate):
                        self.links.append(candidate)
                    if not token.endswith(','):
                        _, separator, rest=rest.partition(',')
                        if not separator: break
    def handle_endtag(self, tag):
        if tag == 'style': self.in_style=False
    def handle_data(self, data):
        if self.in_style: self.css.append(data)


def page_dependencies(markup):
    parser=PageDependencies(); parser.feed(markup)
    match=re.search(r'(?:const|let|var)\s+CONFIG\s*=\s*', markup)
    if match:
        config, _=json.JSONDecoder().raw_decode(markup[match.end():])
        def templates(value):
            if isinstance(value, dict):
                for child in value.values(): templates(child)
            elif isinstance(value, list):
                for child in value: templates(child)
            elif isinstance(value, str) and '<' in value:
                parser.feed(value)
        templates(config)
    css=re.sub(r'/\*.*?\*/', '', '\n'.join(parser.css), flags=re.S)
    return parser.links+[match[1] for match in re.findall(r'''url\(\s*(['"]?)(.*?)\1\s*\)''', css)]

class CollectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.recipes=json.loads((ROOT/'data/recipes.json').read_text())
        cls.catalog=json.loads((ROOT/'assets/catalog.json').read_text())
        cls.upstream=json.loads((ROOT/'data/upstream.json').read_text())
        cls.site_built=False

    @classmethod
    def ensure_site_build(cls):
        if not cls.site_built:
            from build_site import main as build_site
            build_site()
            cls.site_built=True

    def test_complete_public_collection(self):
        slugs={entry['slug'] for entry in self.recipes}
        self.assertEqual(len(slugs),len(self.recipes))
        self.assertTrue(set(self.upstream['files']).issubset(slugs))
        self.assertEqual(slugs,{p.parent.name for p in (ROOT/'design-md').glob('*/DESIGN.md')})
        self.assertEqual(self.catalog['count'],len(slugs))
        for slug in slugs:
            for filename in ('DESIGN.md','PROMPTS.md','README.md','preview.html','STITCH.json','STITCH-PROMPT.md'):
                self.assertTrue((ROOT/'design-md'/slug/filename).is_file(),f'{slug}/{filename}')

    def test_stitch_exports_are_real_unique_and_preserved(self):
        screens, html_hashes = set(), set()
        self.assertEqual(self.catalog['generatedCount'], len(self.recipes))
        for entry in self.catalog['designs']:
            folder = ROOT / 'design-md' / entry['slug']
            record = json.loads((folder / 'STITCH.json').read_text())
            self.assertEqual(record['provider'], 'Google Stitch')
            self.assertEqual(record['transport'], 'MCP')
            self.assertEqual(entry['preview']['status'], 'generated')
            self.assertEqual(record['screen_name'], f"projects/{record['project_id']}/screens/{record['screen_id']}")
            self.assertNotIn(record['screen_name'], screens)
            screens.add(record['screen_name'])
            for name, checksum in record['files'].items():
                self.assertEqual(hashlib.sha256((folder / name).read_bytes()).hexdigest(), checksum)
            self.assertNotIn(record['files']['preview.html'], html_hashes)
            html_hashes.add(record['files']['preview.html'])
            self.assertNotIn('TOKEN SPECIMEN', (folder / 'preview.html').read_text())
            self.assertFalse((folder / 'preview-dark.html').exists())
            self.assertTrue((ROOT / entry['preview']['image']).is_file())
            image_data = (ROOT / entry['preview']['image']).read_bytes()
            if image_data.startswith(b'\x89PNG'):
                self.assertGreaterEqual(int.from_bytes(image_data[16:20], 'big'), min(1280, record['width']))
            self.assertEqual(record['files']['STITCH-PROMPT.md'], hashlib.sha256((folder / 'STITCH-PROMPT.md').read_bytes()).hexdigest())

    def test_prompts_are_original_and_brand_specific(self):
        prompts=[]
        for entry in self.recipes:
            generated=make_prompts(entry)
            prompts.extend(prompt['text'] for prompt in generated)
            design=(ROOT/'design-md'/entry['slug']/'DESIGN.md').read_text()
            prompt_doc=(ROOT/'design-md'/entry['slug']/'PROMPTS.md').read_text()
            base=design.split(MARKER)[0]
            self.assertNotRegex(base,r'(?im)^#{1,6} .*?(Agent Prompt Guide|Example Component Prompts|Iteration Guide)')
            self.assertEqual(design.count(MARKER),1)
            self.assertGreater(len(base),3000)
            for prompt in generated:
                self.assertIn(prompt['text'],design)
                self.assertIn(prompt['text'],prompt_doc)
                self.assertIn(entry['name'],prompt['text'])
            self.assertIn(entry['brief'],generated[0]['text'])
            self.assertIn(entry['component'],generated[1]['text'])
        self.assertEqual(len(prompts),len(set(prompts)))
        self.assertEqual(len(prompts),self.catalog['promptCount'])

    def test_removal_retains_analysis_and_following_sections(self):
        source='# Design\n## Colors\nkeep\n## 9. Agent Prompt Guide\nremove\n### Examples\nremove too\n## Known Gaps\nkeep gap\n'
        output=remove_upstream_instructions(source)
        self.assertIn('keep gap',output)
        self.assertNotIn('remove',output)
        nested='## Components\n### Iteration Guide\nremove\n### Buttons\nkeep buttons\n'
        self.assertIn('keep buttons',remove_upstream_instructions(nested))

    def test_metadata_matches_files_and_safe_tokens(self):
        for entry in self.catalog['designs']:
            doc=(ROOT/'design-md'/entry['slug']/'DESIGN.md').read_bytes()
            self.assertEqual(hashlib.sha256(doc).hexdigest(),entry['sha256'])
            self.assertEqual(len(doc),entry['bytes'])
            self.assertIn(entry['category'],self.catalog['categories'])
            for color in entry['colors']+[entry['canvas'],entry['primary']]:
                self.assertRegex(color,r'^#[0-9a-fA-F]{6}$')
                ink=contrast_ink(color)
                values=sorted([luminance(color),luminance(ink)])
                self.assertGreaterEqual((values[1]+.05)/(values[0]+.05),4.5)

    def test_static_links_resolve_without_commercial_routes(self):
        from build_site import OFFICIAL_DRAFTS
        self.ensure_site_build()
        files=[ROOT/'dist/index.html']
        for path in files:
            parser=Links(); parser.feed(path.read_text())
            for link in parser.links:
                if link.startswith(('#','http:','https:','mailto:','tel:')): continue
                self.assertTrue((path.parent/link.split('#')[0].split('?')[0]).exists(),f'{path}: {link}')
        for name in OFFICIAL_DRAFTS:
            draft=ROOT/'dist/official-drafts'/f'{name}.html'
            self.assertTrue(draft.is_file(),draft)
            html=draft.read_text()
            # Actual render evidence binds these exact bytes. Study labels live
            # beside the preview and must never be injected during publication.
            self.assertEqual(draft.read_bytes(),(ROOT/'.stitch-work/current-official'/f'{name}.html').read_bytes())
            for link in page_dependencies(html):
                link=unescape(link).strip(' \t\n\r\'"')
                # Captured search/wizard templates contain runtime placeholders.
                if '${' in link or re.fullmatch(r'\{[A-Z][A-Z0-9_]*\}(?:[?#].*)?',link): continue
                # Encoded SVG filter IDs inside data images are fragments,
                # not missing local files. Preserve the original SVG bytes.
                if unquote(link).startswith('#'): continue
                if link.startswith(('#','/')) or re.match(r'[a-z][a-z0-9+.-]*:',link,re.I): continue
                self.assertTrue((draft.parent/link.split('#')[0].split('?')[0]).exists(),f'{draft}: {link}')
        metadata=json.loads((ROOT/'dist/assets/official-studies.json').read_text())
        self.assertEqual(metadata['count'],74)
        self.assertFalse(metadata['official_consistency_claim'])
        for study in metadata['studies']:
            draft=ROOT/'dist'/study['preview']
            self.assertEqual(hashlib.sha256(draft.read_bytes()).hexdigest(),study['preview_sha256'])
            self.assertFalse(study['accepted'])
            self.assertFalse(study['official_consistency_claim'])
            self.assertIn(study['status_label'],['已比對主要畫面，仍有差異','尚未驗證'])
            for link in study['study'].values(): self.assertTrue((ROOT/'dist'/link).is_file(),link)
        for file in (ROOT/'dist/official-drafts').rglob('*'):
            if file.is_file():
                self.assertNotRegex(file.name,r'(?:-asset-bundle|-reference|-phases|-response|-pre-).*\.(?:json|html)$')
        for path in [ROOT/'index.html',ROOT/'assets/app.js',ROOT/'README.md']:
            self.assertNotRegex(path.read_text(),r'https?://(?:[^/]*\.)?(?:getdesign\.md/(?:request|design-md-pass)|everyfeed\.ai|sponsors\.voltagent\.dev)')
        self.assertNotRegex((ROOT/'index.html').read_text(),r'<script[^>]+src=["\']https?:')

    def test_readme_links_resolve(self):
        for path in [ROOT/'README.md']+list((ROOT/'design-md').glob('*/README.md')):
            for link in re.findall(r'\]\(([^)]+)\)',path.read_text()):
                if not link.startswith(('http:','https:','#')):
                    self.assertTrue((path.parent/link).exists(),f'{path}: {link}')

    def test_hosted_images_match_pinned_exports(self):
        self.ensure_site_build()
        hosted = json.loads((ROOT / 'dist/assets/catalog.json').read_text())
        base = json.loads((ROOT / 'data/hosting-assets.json').read_text())['image_base_url']
        self.assertRegex(base, r'^https://raw\.githubusercontent\.com/irons163/awesome-ai-web-design/[a-f0-9]{40}/$')
        self.assertFalse((ROOT / 'dist/assets/all-designs.zip').exists())
        for local, remote in zip(self.catalog['designs'], hosted['designs']):
            self.assertEqual(local['slug'], remote['slug'])
            for key in ('image', 'thumbnail'):
                relative = local['preview'][key]
                self.assertEqual(remote['preview'][key], base + relative)
                self.assertTrue((ROOT / relative).is_file())
                self.assertFalse((ROOT / 'dist' / relative).exists())
            for key in ('html', 'prompt', 'provenance'):
                self.assertEqual(remote['preview'][key], local['preview'][key])
                relative = local['preview'][key]
                self.assertEqual((ROOT / 'dist' / relative).read_bytes(), (ROOT / relative).read_bytes())

    def test_bundle_contains_complete_designs_and_license(self):
        with zipfile.ZipFile(ROOT/'assets/all-designs.zip') as archive:
            self.assertIsNone(archive.testzip())
            for entry in self.recipes:
                for filename in ('DESIGN.md','PROMPTS.md','preview.html','STITCH.json','STITCH-PROMPT.md'):
                    name=f"design-md/{entry['slug']}/{filename}"
                    self.assertEqual(archive.read(name),(ROOT/name).read_bytes())
                record = json.loads((ROOT / 'design-md' / entry['slug'] / 'STITCH.json').read_text())
                for filename, checksum in record['files'].items():
                    self.assertEqual(hashlib.sha256(archive.read(f"design-md/{entry['slug']}/{filename}")).hexdigest(), checksum)
            self.assertIn('Copyright (c) 2026 VoltAgent',archive.read('LICENSE').decode())
            self.assertIn('ATTRIBUTION.md',archive.namelist())
            self.assertNotIn('assets/preview.css',archive.namelist())
            self.assertNotIn('assets/preview.js',archive.namelist())

if __name__=='__main__':
    unittest.main()
