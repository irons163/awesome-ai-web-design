import sys
import unittest
import hashlib
import json
import tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from publication import references, study_status
from hosted_media import compact_hosted_media


class PublicationTests(unittest.TestCase):
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
