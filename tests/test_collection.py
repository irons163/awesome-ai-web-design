import hashlib
import json
import re
import sys
import unittest
import zipfile
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from rewrite_prompts import make_prompts, remove_upstream_instructions, MARKER
from build import contrast_ink, luminance

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]
    def handle_starttag(self,tag,attrs):
        for key,value in attrs:
            if key in ('href','src') and value:
                self.links.append(value)

class CollectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.recipes=json.loads((ROOT/'data/recipes.json').read_text())
        cls.catalog=json.loads((ROOT/'assets/catalog.json').read_text())
        cls.upstream=json.loads((ROOT/'data/upstream.json').read_text())

    def test_complete_public_collection(self):
        slugs={entry['slug'] for entry in self.recipes}
        self.assertEqual(len(slugs),len(self.recipes))
        self.assertTrue(set(self.upstream['files']).issubset(slugs))
        self.assertEqual(slugs,{p.parent.name for p in (ROOT/'design-md').glob('*/DESIGN.md')})
        self.assertEqual(self.catalog['count'],len(slugs))
        for slug in slugs:
            for filename in ('DESIGN.md','PROMPTS.md','README.md','preview.html','preview-dark.html'):
                self.assertTrue((ROOT/'design-md'/slug/filename).is_file(),f'{slug}/{filename}')

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
        files=[ROOT/'index.html']+list((ROOT/'design-md').glob('*/*.html'))
        for path in files:
            parser=Links(); parser.feed(path.read_text())
            for link in parser.links:
                if link.startswith(('#','http:','https:','mailto:')): continue
                self.assertTrue((path.parent/link.split('#')[0].split('?')[0]).exists(),f'{path}: {link}')
        for path in [ROOT/'index.html',ROOT/'assets/app.js',ROOT/'README.md']:
            self.assertNotRegex(path.read_text(),r'https?://(?:[^/]*\.)?(?:getdesign\.md/(?:request|design-md-pass)|everyfeed\.ai|sponsors\.voltagent\.dev)')
        self.assertNotRegex((ROOT/'index.html').read_text(),r'<script[^>]+src=["\']https?:')

    def test_readme_links_resolve(self):
        for path in [ROOT/'README.md']+list((ROOT/'design-md').glob('*/README.md')):
            for link in re.findall(r'\]\(([^)]+)\)',path.read_text()):
                if not link.startswith(('http:','https:','#')):
                    self.assertTrue((path.parent/link).exists(),f'{path}: {link}')

    def test_bundle_contains_complete_designs_and_license(self):
        with zipfile.ZipFile(ROOT/'assets/all-designs.zip') as archive:
            self.assertIsNone(archive.testzip())
            for entry in self.recipes:
                for filename in ('DESIGN.md','PROMPTS.md','preview.html','preview-dark.html'):
                    name=f"design-md/{entry['slug']}/{filename}"
                    self.assertEqual(archive.read(name),(ROOT/name).read_bytes())
            self.assertIn('Copyright (c) 2026 VoltAgent',archive.read('LICENSE').decode())
            self.assertIn('ATTRIBUTION.md',archive.namelist())
            self.assertIn('assets/preview.css',archive.namelist())
            self.assertIn('assets/preview.js',archive.namelist())

if __name__=='__main__':
    unittest.main()
