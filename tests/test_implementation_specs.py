import hashlib
import json
import re
import sys
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from implementation_specs import contrast, luminance


class ImplementationSpecTests(unittest.TestCase):
    def test_catalog_modes_and_palettes_describe_the_current_downloadable_spec(self):
        profiles = json.loads((ROOT / 'data/implementation/specs.json').read_text())['profiles']
        catalog = json.loads((ROOT / 'assets/catalog.json').read_text())['designs']
        for item in catalog:
            profile = profiles[item['slug']]['profile']
            colors = profile['colors']
            self.assertEqual(item['primary'], colors['accent'], item['slug'])
            self.assertEqual(item['canvas'], colors['canvas'], item['slug'])
            self.assertEqual(item['ink'], colors['ink'], item['slug'])
            self.assertEqual(item['mode'], 'dark' if luminance(colors['canvas']) < .25 else 'light', item['slug'])
            self.assertEqual(item['implementationVersion'], profile['version'])

    def test_every_primary_spec_is_self_contained_and_has_real_values(self):
        data = json.loads((ROOT / 'data/zh-TW/studies.json').read_text())
        profiles = json.loads((ROOT / 'data/implementation/specs.json').read_text())['profiles']
        self.assertEqual(len(profiles), 74)
        for slug, row in data['studies'].items():
            profile = profiles[slug]['profile']
            design = row['documents']['analysis']
            prompt = row['documents']['prompts']
            self.assertEqual(set(row['implementation_files']), {'TOKENS.json','ASSETS.json','ASSETS.md','starter.css'})
            self.assertNotIn('design-md/', design, slug)
            self.assertNotRegex(prompt, r'Stitch|RGB|DPR|accepted|MOBILE|DESKTOP|provider-notes', slug)
            self.assertNotIn('使用官方目前', prompt, slug)
            self.assertIn('無圖版', prompt)
            self.assertIn('實作建議', design)
            for value in profile['colors'].values():
                self.assertRegex(value, r'^#[a-fA-F0-9]{6}$')
                self.assertIn(value, design)
            for a,b in [('canvas','ink'),('accent','on-accent'),('surface','on-surface'),('canvas','muted')]:
                self.assertGreaterEqual(contrast(profile['colors'][a],profile['colors'][b]),4.5,slug+':'+a+'/'+b)
            css = row['implementation_files']['starter.css']['text']
            self.assertIn(css.rstrip(), design)
            self.assertNotIn('@import', css)
            self.assertNotRegex(css, r'url\(\s*["\']?https?://')
            self.assertIn('minmax(0,1fr)',css)
            self.assertIn('max-width:767px',css)
            assets = json.loads(row['implementation_files']['ASSETS.json']['text'])
            self.assertTrue(assets['can_run_without_external_assets'])
            self.assertFalse(assets['fonts']['files_supplied'])
            self.assertTrue(all(not image['supplied'] and not image['required_to_run'] for image in assets['images']))
            self.assertEqual(profile['reference_preview_sha256'],row['source_preview_sha256'])

    def test_declared_colors_have_hash_bound_evidence_and_other_values_are_labeled(self):
        profiles = json.loads((ROOT / 'data/implementation/specs.json').read_text())['profiles']
        source_root = ROOT / '.stitch-work/current-official'
        for slug, row in profiles.items():
            p = row['profile']
            self.assertEqual(set(p['colors']),set(p['color_provenance']))
            for key, evidence in p['color_provenance'].items():
                if evidence['kind'] == 'implementation_recommendation':
                    self.assertIn('非官網量測',evidence['label'])
                else:
                    self.assertEqual(evidence['kind'],'source_declaration')
                    file = source_root / evidence['path']
                    self.assertEqual(hashlib.sha256(file.read_bytes()).hexdigest(),evidence['sha256'])
                    value = p['colors'][key].lower()
                    short = '#'+''.join(value[i] for i in (1,3,5)) if all(value[i]==value[i+1] for i in (1,3,5)) else value
                    self.assertTrue(value in evidence['excerpt'].lower() or short in evidence['excerpt'].lower(),slug)

    def test_single_brand_zip_and_full_zip_match_every_public_dependency(self):
        output = ROOT / 'dist'
        studies = json.loads((output / 'assets/official-studies.json').read_text())['studies']
        with zipfile.ZipFile(output / 'assets/design-references.zip') as full:
            self.assertEqual(len(full.namelist()),448)
            for name in ('LICENSE','ATTRIBUTION.md'):
                self.assertEqual(full.read(name),(ROOT/name).read_bytes())
            for row in studies:
                self.assertIn('implementation_pack',row)
                slug = row['slug']
                with zipfile.ZipFile(output / row['implementation_pack']) as single:
                    self.assertIsNone(single.testzip())
                    self.assertEqual(len(single.namelist()),10)
                    for name in ('LICENSE','ATTRIBUTION.md'):
                        self.assertEqual(single.read(name),(ROOT/name).read_bytes())
                    for kind,name in [('analysis','DESIGN.md'),('prompts','PROMPTS.md')]:
                        expected=(output/row['study'][kind]).read_bytes()
                        self.assertEqual(single.read(name),expected)
                        self.assertEqual(full.read(slug+'/'+name),expected)
                    for name, file in row['implementation_files'].items():
                        expected=(output/file['path']).read_bytes()
                        self.assertEqual(hashlib.sha256(expected).hexdigest(),file['sha256'])
                        self.assertEqual(single.read(name),expected)
                        self.assertEqual(full.read(slug+'/'+name),expected)
                    self.assertIn('不依賴未附上的延伸規格',single.read('README.md').decode())


if __name__ == '__main__':
    unittest.main()
