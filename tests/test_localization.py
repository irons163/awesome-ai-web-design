import copy
import hashlib
import json
import re
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from localization import localize_study


class LocalizationTests(unittest.TestCase):
    def test_every_public_document_and_download_uses_reviewed_chinese(self):
        # Collection tests stage this directory before the localization checks.
        output = ROOT / 'dist'
        metadata = json.loads((output / 'assets/official-studies.json').read_text())
        self.assertEqual(metadata['locale'], 'zh-TW')
        self.assertEqual(len(metadata['studies']), 74)
        english_sentence = re.compile(r"(?:[A-Za-z][A-Za-z’'.-]+[ ,]+){5,}[A-Za-z][A-Za-z’'.-]+")
        forbidden = re.compile('默認|用户|數據|組件|服務器|鏈接|登錄|視頻|预覽|鼠標|屏幕|信息')
        with zipfile.ZipFile(output / 'assets/design-references.zip') as archive:
            self.assertEqual(len(archive.namelist()), 448)
            for study in metadata['studies']:
                self.assertEqual(study['document_language'], 'zh-TW')
                self.assertFalse(study['accepted'])
                self.assertFalse(study['official_consistency_claim'])
                self.assertEqual(hashlib.sha256((output / study['preview']).read_bytes()).hexdigest(), study['preview_sha256'])
                for kind, relative in study['study'].items():
                    data = (output / relative).read_bytes()
                    text = data.decode()
                    self.assertIn('繁體中文（台灣用語，zh-TW）', text)
                    self.assertIn(study['name'], text)
                    self.assertIn(study['date'], text)
                    self.assertEqual(hashlib.sha256(data).hexdigest(), study['document_sha256'][kind])
                    prose = re.sub(r'https?://\S+|(?<!`)`(?!`)[^`\n]+`(?!`)', '', text)
                    self.assertNotRegex(prose, english_sentence, study['slug'] + ': ' + kind)
                    self.assertNotRegex(prose, forbidden, study['slug'] + ': ' + kind)
                    if kind in ('analysis', 'prompts'):
                        filename = 'DESIGN.md' if kind == 'analysis' else 'PROMPTS.md'
                        self.assertEqual(archive.read(study['slug'] + '/' + filename), data)
                for value in study['remaining_differences']:
                    self.assertRegex(value, '[\u4e00-\u9fff]')

    def test_chinese_extension_specs_keep_source_tokens_and_original_exports(self):
        styles = json.loads((ROOT / 'data/zh-TW/design-sources.json').read_text())
        for slug, source in styles.items():
            folder = ROOT / 'design-md' / slug
            text = (folder / 'DESIGN.md').read_text()
            self.assertIn(source['tokens'], text)
            self.assertIn('language: zh-TW', text)
            self.assertIn('來源與規格層次', text)
            prompts = (folder / 'PROMPTS.md').read_text()
            self.assertEqual(prompts.count('```text'), 3)
            self.assertIn('繁體中文（台灣用語）', prompts)
            original = json.loads((folder / 'STITCH.json').read_text())
            for name, digest in original['files'].items():
                self.assertEqual(hashlib.sha256((folder / name).read_bytes()).hexdigest(), digest)

    def test_stale_translation_cannot_replace_new_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            work = root / '.stitch-work/current-official'
            destination = root / 'public/official-drafts'
            work.mkdir(parents=True)
            destination.mkdir(parents=True)
            original = b'Original observed text\n'
            filename = 'example-analysis.md'
            (work / filename).write_bytes(original)
            (destination / filename).write_bytes(original)
            status = dict(slug='example', preview_sha256='a' * 64,
                          remaining_differences=['Motion remains unverified.'],
                          study={'analysis': 'official-drafts/' + filename})
            digest = lambda value: hashlib.sha256(value).hexdigest()
            row = dict(source_preview_sha256='a' * 64,
                       remaining_source_sha256=digest(json.dumps(status['remaining_differences'], separators=(',', ':')).encode()),
                       source_documents={'analysis': {'path': 'official-drafts/' + filename, 'sha256': digest(original)}},
                       documents={'analysis': '# 範例\n繁體中文（台灣用語，zh-TW）\n'},
                       remaining_differences=['動態尚未驗證。'])
            data = {'updated': '2026-10-15', 'studies': {'example': row}}
            localize_study(root, destination, copy.deepcopy(status), data)
            self.assertEqual((work / filename).read_bytes(), original)
            self.assertIn('繁體中文', (destination / filename).read_text())
            (destination / filename).write_bytes(original)
            changed = copy.deepcopy(status)
            changed['preview_sha256'] = 'b' * 64
            with self.assertRaisesRegex(ValueError, 'another preview'):
                localize_study(root, destination, changed, data)
            changed = copy.deepcopy(status)
            changed['remaining_differences'].append('A new unresolved limitation.')
            with self.assertRaisesRegex(ValueError, 'limitations require review'):
                localize_study(root, destination, changed, data)
            (work / filename).write_bytes(b'New observed design')
            with self.assertRaisesRegex(ValueError, 'source changed'):
                localize_study(root, destination, copy.deepcopy(status), data)
            self.assertEqual((destination / filename).read_bytes(), original)


if __name__ == '__main__':
    unittest.main()
