"""Cloudflare candidate guards without credentials or network access."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from scripts.prepare_cloudflare_preview import prepare_cloudflare
from scripts.prepare_launch_preview import WEB


class CloudflarePreviewTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.output = Path(temporary.name) / 'candidate'

    def test_headers_and_robots_preserve_indexing_hold(self):
        prepare_cloudflare(self.output)
        site = self.output / 'site'
        headers = (site / '_headers').read_text()
        self.assertTrue(headers.startswith('/*\n'))
        for directive in ['X-Robots-Tag: noindex, nofollow, noarchive',
                          'X-Content-Type-Options: nosniff', 'X-Frame-Options: DENY',
                          'Referrer-Policy: strict-origin-when-cross-origin',
                          'Permissions-Policy: camera=(), microphone=(), geolocation=()',
                          'Cache-Control: no-store']:
            self.assertIn(directive, headers)
        self.assertEqual((site / 'robots.txt').read_text(), 'User-agent: *\nDisallow: /\n')

    def test_manifest_never_claims_deployment_or_authentication(self):
        manifest = prepare_cloudflare(self.output)
        self.assertFalse(manifest['deployment_authorized'])
        self.assertFalse(manifest['access_control_verified'])
        self.assertTrue(manifest['requires_access_control_before_upload'])
        self.assertIsNone(manifest['domain'])
        self.assertEqual(json.loads((self.output / 'manifest.json').read_text()), manifest)
        self.assertFalse((self.output / 'site' / 'manifest.json').exists())
        self.assertFalse((self.output / 'site' / '_worker.js').exists())

    def test_all_package_files_have_matching_hashes(self):
        manifest = prepare_cloudflare(self.output)
        site = self.output / 'site'
        files = {str(p.relative_to(site)): hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in site.rglob('*') if p.is_file()}
        self.assertEqual(manifest['files'], files)

    def test_existing_output_is_preserved(self):
        self.output.mkdir()
        marker = self.output / 'keep.txt'
        marker.write_text('keep')
        with self.assertRaises(ValueError):
            prepare_cloudflare(self.output)
        self.assertEqual(marker.read_text(), 'keep')

    def test_original_web_and_research_are_not_published(self):
        before = {p: p.read_bytes() for p in WEB.rglob('*') if p.is_file()}
        prepare_cloudflare(self.output)
        self.assertTrue(all(p.read_bytes() == content for p, content in before.items()))
        site = self.output / 'site'
        for name in ['review.html', 'site-v2.js', 'data', 'schemas', '.git']:
            self.assertFalse((site / name).exists())
        self.assertEqual((site / 'index.html').read_bytes(), (WEB / 'monitor-v3.html').read_bytes())
        self.assertTrue((site / '404.html').is_file())

    def test_http_diagnostics_are_opt_in_and_manifest_bound(self):
        manifest = prepare_cloudflare(self.output, include_http_check=True)
        self.assertTrue(manifest['http_check_included'])
        for name in ['__preview_http_check.html', '__preview_http_check.js']:
            target = self.output / 'site' / name
            self.assertEqual(hashlib.sha256(target.read_bytes()).hexdigest(), manifest['files'][name])
        page = (self.output / 'site' / '__preview_http_check.html').read_text()
        self.assertIn('noindex,nofollow', page)
        self.assertIn("connect-src 'self'", page)

    def test_default_package_excludes_http_diagnostics(self):
        manifest = prepare_cloudflare(self.output)
        self.assertFalse(manifest['http_check_included'])
        self.assertFalse(list((self.output / 'site').glob('__preview_http_check.*')))
