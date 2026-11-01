import sys
import unittest
import hashlib
import json
import tempfile
import shutil
import subprocess
from zipfile import ZipFile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from publication import references, study_status
from hosted_media import compact_hosted_media
from study_covers import cover_for
from study_pack import write_study_pack


class PublicationTests(unittest.TestCase):
    @unittest.skipUnless(shutil.which('node'), 'Node is required for cross-builder parity')
    def test_both_zip_builders_give_the_same_brand_and_collection_instructions(self):
        with tempfile.TemporaryDirectory() as directory:
            output=Path(directory);(output/'assets').mkdir();(output/'official-drafts').mkdir()
            (output/'official-drafts/example-analysis.md').write_text('# 設計規格\n')
            (output/'official-drafts/example-reproduction-prompt.md').write_text('# AI 指令\n')
            (output/'implementation/example').mkdir(parents=True)
            files={}
            for name in ['ASSETS.json','ASSETS.md','TOKENS.json','starter.css']:
                data=b'{}\n';relative='implementation/example/'+name
                (output/relative).write_bytes(data)
                files[name]=dict(path=relative,sha256=hashlib.sha256(data).hexdigest())
            study=dict(slug='example',name='範例品牌',date='2026-10-13',preview='official-drafts/example.html',preview_sha256='current',reference_url='https://example.com/',implementation_version='2026-10-20',implementation_files=files,study=dict(analysis='official-drafts/example-analysis.md',prompts='official-drafts/example-reproduction-prompt.md'))
            write_study_pack(output,[study])
            paths=['assets/design-references.zip','assets/design-packs/example.zip','assets/design-packs/example-simple.zip']
            expected={}
            comments={}
            for path in paths:
                with ZipFile(output/path) as archive:
                    expected[path]={name:archive.read(name) for name in archive.namelist()}
                    comments[path]=archive.comment
            subprocess.run([shutil.which('node'),'--input-type=module','-e',"import {writeStudyPack} from './scripts/study_pack.mjs';writeStudyPack(process.argv[1],[JSON.parse(process.argv[2])]);",str(output),json.dumps(study)],cwd=ROOT,check=True,capture_output=True,text=True)
            for path in paths:
                with ZipFile(output/path) as archive:
                    self.assertIsNone(archive.testzip())
                    self.assertEqual({name:archive.read(name) for name in archive.namelist()},expected[path])
                    self.assertEqual(archive.comment,comments[path])

    def test_download_pack_contains_the_current_files_and_rejects_missing_study_links(self):
        with tempfile.TemporaryDirectory() as directory:
            output=Path(directory);(output/'assets').mkdir();(output/'official-drafts').mkdir()
            analysis=b'# Current analysis\n';prompts=b'# Current prompt\n'
            (output/'official-drafts/example-analysis.md').write_bytes(analysis)
            (output/'official-drafts/example-reproduction-prompt.md').write_bytes(prompts)
            study=dict(slug='example',date='2026-10-13',preview='official-drafts/example.html',preview_sha256='current',study=dict(analysis='official-drafts/example-analysis.md',prompts='official-drafts/example-reproduction-prompt.md'))
            write_study_pack(output,[study]);first=(output/'assets/design-references.zip').read_bytes()
            with ZipFile(output/'assets/design-references.zip') as archive:
                self.assertIsNone(archive.testzip())
                self.assertEqual(archive.read('example/DESIGN.md'),analysis)
                self.assertEqual(archive.read('example/PROMPTS.md'),prompts)
                self.assertEqual(json.loads(archive.read('SOURCES.json'))[0]['preview_sha256'],'current')
            write_study_pack(output,[study]);self.assertEqual((output/'assets/design-references.zip').read_bytes(),first)
            del study['study']['analysis']
            with self.assertRaisesRegex(ValueError,'current analysis'):write_study_pack(output,[study])

    def test_current_cover_rejects_changed_preview_evidence_or_image(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);work=root/'.stitch-work/current-official';work.mkdir(parents=True)
            folder=root/'assets/current-previews';folder.mkdir(parents=True)
            (work/'source.png').write_bytes(b'actual retained screenshot');(work/'review.json').write_bytes(b'current review');(folder/'cover.webp').write_bytes(b'derived cover')
            digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
            record={'brand':'example','preview_sha256':'current','source':{'path':'source.png','sha256':digest(work/'source.png')},'result':{'path':'review.json','sha256':digest(work/'review.json')},'image':{'path':'assets/current-previews/cover.webp','sha256':digest(folder/'cover.webp'),'bytes':13,'width':800,'height':450}}
            self.assertEqual(cover_for(root,record,'example','current')['preview_sha256'],'current')
            with self.assertRaisesRegex(ValueError,'Stale'):cover_for(root,record,'example','new')
            (work/'source.png').write_bytes(b'changed screenshot')
            with self.assertRaisesRegex(ValueError,'evidence'):cover_for(root,record,'example','current')
            (work/'source.png').write_bytes(b'actual retained screenshot');(folder/'cover.webp').write_bytes(b'changed cover')
            with self.assertRaisesRegex(ValueError,'image'):cover_for(root,record,'example','current')

    def test_media_publication_preserves_original_and_rejects_mutable_or_changed_sources(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);work=root/'.stitch-work/current-official';out=root/'dist'
            (root/'data').mkdir();(work/'example-assets').mkdir(parents=True);(out/'official-drafts/example-assets').mkdir(parents=True);(out/'assets').mkdir()
            original=b'unchanged original media';source=work/'example-assets/photo.png';source.write_bytes(original)
            staged=out/'official-drafts/example-assets/photo.png';staged.write_bytes(original)
            html=('你好 🧩 <svg><path d="M0 0"/></svg><img src="example-assets/photo.png">'
                  '<div style="background-image:url(&quot;./example-assets/photo.png&quot;)"></div>'
                  '<img src="/official-drafts/example-assets/photo.png?width=640">'
                  '<script type="application/json">{"image":"example-assets\\/photo.png"}</script>').encode()
            (out/'official-drafts/example.html').write_bytes(html);(work/'example.html').write_bytes(html)
            css=b'.hero{background:url("photo.png#original")}'
            (out/'official-drafts/example-assets/style.css').write_bytes(css);(work/'example-assets/style.css').write_bytes(css)
            commit='a'*40;base='https://raw.githubusercontent.com/owner/repo/'+commit+'/.stitch-work/current-official/'
            config={'source_commit':commit,'base_url':base,'max_bundle_bytes':10000,'assets':[{'path':'example-assets/photo.png','bytes':len(original),'sha256':hashlib.sha256(original).hexdigest()}]}
            config_path=root/'data/hosted-official-media.json';config_path.write_text(json.dumps(config))
            compact_hosted_media(root,out)
            self.assertEqual(source.read_bytes(),original)
            self.assertEqual((work/'example.html').read_bytes(),html)
            published=(out/'official-drafts/example.html').read_bytes()
            self.assertEqual(published,html)
            self.assertEqual((work/'example-assets/style.css').read_bytes(),css)
            self.assertEqual((out/'official-drafts/example-assets/style.css').read_bytes(),css)
            self.assertFalse((out/'_redirects').exists())
            proof=json.loads((out/'assets/official-media-publication.json').read_text())
            self.assertEqual(proof['files']['example.html']['source_sha256'],hashlib.sha256(html).hexdigest())
            self.assertEqual(proof['files']['example.html']['published_sha256'],hashlib.sha256(html).hexdigest())
            self.assertEqual(proof['files']['example.html']['replacements'],[])
            staged.write_bytes(original)
            config['base_url']=base.replace(commit,'main');config_path.write_text(json.dumps(config))
            with self.assertRaisesRegex(ValueError,'immutable'):compact_hosted_media(root,out)
            config['base_url']=base;config_path.write_text(json.dumps(config));source.write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError,'changed'):compact_hosted_media(root,out)
            self.assertEqual(staged.read_bytes(),original)

    def status(self, record, current='current'):
        return study_status(ROOT, 'example', {'slug':'example','name':'Example'}, {}, record, current, [])

    def test_a_saved_draft_or_stale_review_cannot_claim_a_current_comparison(self):
        full=dict(preview_sha256='earlier',latest_draft_full_desktop_and_narrow_coverage=True,
                  actual_raster_inspection_bound_to_current_preview=True)
        for record in [{}, {'preview_sha256':'current','accepted':True}, full,
                       dict(full,preview_sha256='current',latest_draft_full_desktop_and_narrow_coverage=False)]:
            status=self.status(record)
            self.assertEqual(status['status'],'unverified')
            self.assertFalse(status['accepted'])
            self.assertFalse(status['official_consistency_claim'])

    def test_current_rendered_review_exposes_differences_and_reduced_motion_scope(self):
        status=self.status(dict(preview_sha256='current',latest_draft_full_desktop_and_narrow_coverage=True,
            actual_raster_inspection_bound_to_current_preview=True,scope={'prefers_reduced_motion':True},
            remaining_differences_and_limits=['Animation timing remains unverified.']))
        self.assertEqual(status['status'],'compared_with_differences')
        self.assertIn('減少動態',status['scope'])
        self.assertEqual(status['remaining_differences'],['Animation timing remains unverified.'])
        self.assertFalse(status['official_consistency_claim'])

    def test_inert_templates_srcsets_and_unusual_asset_names_are_preserved(self):
        markup='<script>const CONFIG={"body":"<img src=\\"example-assets/Frame 1 (5).png\\"><source srcset=\\"example-assets/a.jpg, example-assets/b.jpg 2x\\"><img src=\\"example-assets/original.bin\\"><img src=\\"example-observed-map.png\\">"}</script>'
        self.assertEqual(references(markup,'example'),[
            'example-assets/Frame 1 (5).png','example-assets/a.jpg','example-assets/b.jpg','example-assets/original.bin','example-observed-map.png'])

    def test_relative_css_paths_and_remote_url_comments_are_distinct(self):
        css='/* source https://static.example.com/example-build-assets/css/banner.css */ @font-face{src:url("font.woff2")} .x{background:url(../image.svg)}'
        self.assertEqual(references(css,'example','example-assets/css'),[
            'example-assets/css/font.woff2','example-assets/image.svg'])

    def test_search_result_template_expressions_are_not_local_files(self):
        markup = '<template><a href="${hit?.url}"><img src="${hit.image}"></a><a href="{BTN_LINK}">Continue</a><img src="{BG_DESKTOP}?$3200px$"></template><img src="example-assets/logo.svg">'
        self.assertEqual(references(markup, 'example'), ['example-assets/logo.svg'])


if __name__=='__main__': unittest.main()
