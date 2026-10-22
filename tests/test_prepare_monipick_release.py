"""Inactive release artifacts cannot modify the currently protected preview."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from xml.etree import ElementTree as ET

from scripts.prepare_monipick_release import ORIGIN, prepare_release, release_plan, validate_plan
from scripts.prepare_launch_preview import WEB
from scripts.validate_local_site import validate_site


class ReleasePreparationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.output = Path(cls.temp.name) / 'candidate'
        cls.before = {p: hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in WEB.rglob('*') if p.is_file()}
        cls.manifest = prepare_release(cls.output)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_preview_keeps_hold_and_no_release_drafts_are_served(self):
        site = self.output / 'site'
        self.assertEqual(validate_site(site), [])
        self.assertIn('Disallow: /', (site / 'robots.txt').read_text())
        self.assertIn('X-Robots-Tag: noindex', (site / '_headers').read_text())
        for name in ['sitemap.xml', '_redirects', 'manifest.json', 'activation-drafts']:
            self.assertFalse((site / name).exists())
        self.assertFalse(list(site.rglob('*.proposed*')))
        self.assertFalse(list(site.glob('__preview_http_check.*')))
        self.assertIn('no-store', (site / '_headers').read_text())
        self.assertIn('비공개 검수 중', (site / 'index.html').read_text())

    def test_verified_email_receipt_does_not_imply_publication(self):
        self.assertEqual(self.manifest['contact_email'], 'contact@monipick.com')
        self.assertEqual(self.manifest['contact_delivery_status'], 'VERIFIED_EXTERNAL_RECEIPT')
        for flag in ['deployment_authorized', 'publication_authorized', 'indexing_authorized', 'analytics_enabled']:
            self.assertIs(self.manifest[flag], False)
        self.assertEqual(self.manifest['blockers'], ['FINAL_PUBLICATION_APPROVAL_PENDING'])
        for field, value in [('analytics_enabled', True), ('publication_authorized', True),
                             ('indexing_authorized', True), ('contact_delivery_status', 'VERIFIED'), ('contact_email', 'invented@example.com'),
                             ('origin', 'https://example.com'), ('blockers', [])]:
            plan = release_plan(WEB)
            plan[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_plan(plan)

    def test_routes_and_sitemap_only_use_current_stable_pages(self):
        plan = release_plan(WEB)
        self.assertEqual(len(plan['pages']), 37)
        validate_plan(plan)
        pages = {p['source']: p for p in plan['pages']}
        self.assertEqual(pages['monitor-v3.html']['proposed_canonical'], ORIGIN + '/')
        self.assertEqual(pages['monitors/asus-pa279crv/index.html']['route'], '/monitors/asus-pa279crv/')
        self.assertEqual(pages['guides/monitor-buying.html']['route'], '/guides/monitor-buying')
        root = ET.fromstring((self.output / 'activation-drafts/sitemap.xml.proposed').read_text())
        urls = [node.text for node in root.findall('{*}url/{*}loc')]
        self.assertEqual(len(urls), 34)
        self.assertEqual(len(urls), len(set(urls)))
        self.assertEqual(set(urls), {p['proposed_canonical'] for p in plan['pages'] if p['sitemap_candidate']})
        self.assertTrue(all(url.startswith(ORIGIN + '/') and '?' not in url and '#' not in url for url in urls))
        self.assertFalse(root.findall('.//{*}lastmod'))
        for source in ['tech-news.html', 'monitor10-review.html', '404.html']:
            self.assertFalse(pages[source]['sitemap_candidate'])
            self.assertIn('noindex', pages[source]['proposed_robots'])

    def test_bad_canonical_duplicate_route_or_index_scope_rejected(self):
        plan = release_plan(WEB)
        for field, value in [('proposed_canonical', 'https://evil.example/'),
                             ('route', '/?q=4k'), ('sitemap_candidate', True),
                             ('proposed_robots', 'index,follow')]:
            invalid = copy.deepcopy(plan)
            page = next(p for p in invalid['pages'] if p['source'] == '404.html')
            page[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_plan(invalid)
        plan['pages'].append(copy.deepcopy(plan['pages'][0]))
        with self.assertRaises(ValueError):
            validate_plan(plan)

    def test_artifact_hashes_match_and_sources_remain_untouched(self):
        for base, key in [('site', 'files'), ('activation-drafts', 'draft_files')]:
            for name, digest in self.manifest[key].items():
                self.assertEqual(hashlib.sha256((self.output / base / name).read_bytes()).hexdigest(), digest)
        self.assertEqual(json.loads((self.output / 'manifest.json').read_text()), self.manifest)
        self.assertTrue(all(hashlib.sha256(p.read_bytes()).hexdigest() == digest for p, digest in self.before.items()))

    def test_existing_output_refused_without_overwrite(self):
        with self.assertRaises(ValueError):
            prepare_release(self.output)
        self.assertTrue((self.output / 'manifest.json').exists())

    def test_draft_headers_and_redirects_are_conservative(self):
        folder = self.output / 'activation-drafts'
        headers = (folder / '_headers.proposed').read_text()
        for token in ["frame-ancestors 'none'", "script-src 'self'", 'nosniff', 'DENY',
                      'strict-origin-when-cross-origin', 'camera=()']:
            self.assertIn(token, headers)
        for token in ['unsafe-inline', 'immutable', 'max-age=31536000']:
            self.assertNotIn(token, headers)
        redirects = (folder / '_redirects.proposed').read_text().splitlines()
        self.assertEqual(redirects, ['/monitor-v3.html / 301', '/monitor-v3 / 301'])
        self.assertNotIn('/* / 200', '\n'.join(redirects))
