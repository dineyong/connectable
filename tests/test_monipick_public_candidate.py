"""Public-format files are prepared locally without approving publication or facts."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from xml.etree import ElementTree as ET

from scripts.build_monipick_public_candidate import build_candidate, validate_candidate
from scripts.prepare_launch_preview import WEB
from scripts.validate_local_site import Document


class PublicCandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.output = Path(cls.temp.name) / 'candidate'
        cls.before = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in WEB.rglob('*') if p.is_file()}
        cls.manifest = build_candidate(cls.output)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_build_remains_unapproved_and_does_not_mutate_sources(self):
        self.assertEqual(validate_candidate(self.output), [])
        for key in ['deployment_authorized', 'publication_authorized', 'indexing_authorized', 'analytics_enabled']:
            self.assertIs(self.manifest[key], False)
        self.assertEqual(self.manifest['purpose'], 'PUBLIC_FORMAT_CANDIDATE_NOT_AUTHORIZED')
        self.assertTrue(all(hashlib.sha256(p.read_bytes()).hexdigest() == h for p,h in self.before.items()))

    def test_every_page_has_matching_metadata_and_preserves_exclusions(self):
        for page in self.manifest['pages']:
            doc = Document((self.output / 'site' / page['source']).read_text())
            self.assertEqual(doc.meta['robots'], [page['proposed_robots']])
            self.assertEqual(doc.canonicals, [] if page['source'] == '404.html' else [page['proposed_canonical']])
        home = Document((self.output / 'site/index.html').read_text())
        self.assertEqual(home.canonicals, ['https://monipick.com/'])
        urls = [n.text for n in ET.parse(self.output/'site/sitemap.xml').findall('{*}url/{*}loc')]
        self.assertEqual(len(urls), 34)
        self.assertEqual(len(set(urls)), 34)
        self.assertNotIn('https://monipick.com/tech-news', urls)

    def test_public_copy_keeps_uncertainty_and_contact_without_preview_promises(self):
        site = self.output / 'site'
        for p in site.rglob('*.html'):
            text = p.read_text()
            self.assertNotIn('비공개 검수 중', text)
            self.assertNotIn('공개 전 실제 운영', text)
        detail = (site/'monitors/asus-pa279crv/index.html').read_text()
        self.assertIn('한국 판매 SKU 동일성은 미확인', detail)
        info = (site/'information.html').read_text()
        self.assertIn('mailto:contact@monipick.com', info)
        self.assertIn('Cloudflare Email Routing', info)
        self.assertIn('운영 Gmail', info)
        self.assertIn('전체 이용자 수나 제품 평가 점수로 집계하지 않습니다', info)
        self.assertIn('사양 적용 범위 확인 필요', detail)

    def test_safe_headers_redirects_inventory_and_data_identity(self):
        site = self.output/'site'
        headers = (site/'_headers').read_text()
        self.assertIn("script-src 'self'", headers)
        self.assertNotIn('unsafe-inline', headers)
        self.assertNotIn('no-store', headers)
        self.assertNotIn('immutable', headers)
        self.assertNotIn('/* /index.html 200', (site/'_redirects').read_text())
        for name in ['manifest.json','activation-drafts','site-v2.js','legacy.html','__preview_http_check.html']:
            self.assertFalse((site/name).exists())
        for p in site.rglob('*.js'):
            self.assertEqual(p.read_bytes(), (WEB/p.relative_to(site)).read_bytes())

    def assert_invalid_mutation(self, path, replacement):
        p=self.output/path
        original=p.read_bytes() if p.exists() else None
        try:
            p.write_text(replacement)
            self.assertTrue(validate_candidate(self.output))
        finally:
            if original is None: p.unlink()
            else: p.write_bytes(original)

    def test_bad_canonical_and_accidental_noindex_are_rejected(self):
        p=self.output/'site/index.html'
        text=p.read_text()
        self.assert_invalid_mutation('site/index.html', text.replace('https://monipick.com/','https://wrong.example/'))
        self.assert_invalid_mutation('site/index.html', text.replace('index,follow','noindex,nofollow'))

    def test_display_payload_and_private_files_cannot_be_smuggled_in(self):
        self.assert_invalid_mutation('site/monitor-v3-data.js', 'window.CONNECTABLE_MONITORS = {};')
        self.assert_invalid_mutation('site/private.txt', 'internal only')

    def test_approval_flags_cannot_be_manually_promoted(self):
        m=json.loads((self.output/'manifest.json').read_text())
        m['publication_authorized']=True
        self.assert_invalid_mutation('manifest.json', json.dumps(m))

    def test_missing_inventory_and_tampered_policy_are_rejected(self):
        p=self.output/'site/robots.txt'
        self.assert_invalid_mutation('site/robots.txt','User-agent: *\nDisallow: /\n')
        self.assert_invalid_mutation('site/_headers',"/*\n  Content-Security-Policy: script-src * 'unsafe-inline'\n")
        m=json.loads((self.output/'manifest.json').read_text())
        m['files'].pop('monitor-v3.js')
        self.assert_invalid_mutation('manifest.json',json.dumps(m))

    def test_malformed_manifest_and_missing_file_are_rejected(self):
        self.assert_invalid_mutation('manifest.json', '[]')
        self.assert_invalid_mutation('manifest.json', '{invalid')
        p=self.output/'site/monitor-v3.js'
        original=p.read_bytes()
        try:
            p.unlink()
            self.assertTrue(validate_candidate(self.output))
        finally: p.write_bytes(original)

    def test_candidate_symlink_is_rejected(self):
        p=self.output/'site/extra.txt'
        try:
            p.symlink_to(self.output/'manifest.json')
            self.assertTrue(validate_candidate(self.output))
        finally: p.unlink()

    def test_existing_output_never_overwritten(self):
        with self.assertRaises(ValueError): build_candidate(self.output)


if __name__=='__main__': unittest.main()
