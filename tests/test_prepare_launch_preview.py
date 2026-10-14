"""Regression guards for candidate isolation, entry point and publication hold."""
import hashlib
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.prepare_launch_preview import WEB, prepare


class LaunchPreviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name) / 'candidate'

    def test_current_design_is_root_and_legacy_is_excluded(self):
        manifest = prepare(self.output)
        site = self.output / 'site'
        self.assertEqual((site / 'index.html').read_bytes(), (WEB / 'monitor-v3.html').read_bytes())
        for legacy in ['legacy.html', 'review.html', 'site-v2.js', 'derive-site-content.py']:
            self.assertFalse((site / legacy).exists())
        self.assertEqual(len(list((site / 'monitors').glob('*/index.html'))), 30)
        self.assertIn('monitor10-review.html', manifest['files'])

    def test_sources_are_preserved_and_manifest_hashes_match(self):
        before = {p: p.read_bytes() for p in WEB.rglob('*') if p.is_file()}
        manifest = prepare(self.output)
        self.assertTrue(all(p.read_bytes() == content for p, content in before.items()))
        for name, digest in manifest['files'].items():
            self.assertEqual(hashlib.sha256((self.output / 'site' / name).read_bytes()).hexdigest(), digest)
        self.assertFalse((self.output / 'site' / 'manifest.json').exists())

    def test_candidate_keeps_publication_hold(self):
        manifest = prepare(self.output)
        self.assertFalse(manifest['deployment_authorized'])
        self.assertIsNone(manifest['domain'])
        for page in (self.output / 'site').rglob('*.html'):
            self.assertIn('noindex', page.read_text())

    def test_existing_output_is_not_overwritten(self):
        self.output.mkdir()
        marker = self.output / 'keep.txt'
        marker.write_text('keep')
        with self.assertRaises(ValueError):
            prepare(self.output)
        self.assertEqual(marker.read_text(), 'keep')

    def test_output_cannot_be_inside_original_web(self):
        with self.assertRaises(ValueError):
            prepare(WEB / '__not_created_launch_test__')
        self.assertFalse((WEB / '__not_created_launch_test__').exists())

    def test_invalid_source_is_rejected_before_output_creation(self):
        with patch('scripts.prepare_launch_preview.validate_site', return_value=['bad source']):
            with self.assertRaisesRegex(ValueError, 'source validation failed'):
                prepare(self.output)
        self.assertFalse(self.output.exists())

    def source_copy(self):
        copied = Path(self.temp.name) / 'web'
        shutil.copytree(WEB, copied)
        return copied

    def test_invalid_runtime_data_rejected(self):
        web = self.source_copy()
        (web / 'monitor-v3-data.js').write_text('window.CONNECTABLE_MONITORS = ;')
        with self.assertRaises(ValueError):
            prepare(self.output, web)
        self.assertFalse(self.output.exists())

    def test_supplemental_index_despite_noindex_comment_rejected(self):
        web = self.source_copy()
        page = web / 'monitor10-review.html'
        page.write_text(page.read_text().replace('noindex,nofollow', 'index,follow') + '<!-- noindex -->')
        with self.assertRaises(ValueError):
            prepare(self.output, web)
        self.assertFalse(self.output.exists())

    def test_supplemental_canonical_rejected(self):
        web = self.source_copy()
        page = web / 'monitor10-review.html'
        page.write_text(page.read_text().replace('</head>', '<link rel="canonical" href="https://example.org/"></head>'))
        with self.assertRaises(ValueError):
            prepare(self.output, web)
        self.assertFalse(self.output.exists())

    def test_supplemental_missing_asset_rejected(self):
        web = self.source_copy()
        page = web / 'monitor10-review.html'
        page.write_text(page.read_text().replace('</head>', '<link rel="stylesheet" href="missing.css"></head>'))
        with self.assertRaises(ValueError):
            prepare(self.output, web)
        self.assertFalse(self.output.exists())

    def test_all_generated_display_assets_are_bound_to_validated_originals(self):
        for name in ['monitor-v3-data.js', 'monitor-review-links-data.js', 'tech-news-data.js', 'product-news-data.js']:
            with self.subTest(asset=name):
                web = Path(self.temp.name) / name.replace('.js', '')
                shutil.copytree(WEB, web)
                target = web / name
                target.write_text(target.read_text() + '\nwindow.UNREVIEWED_EXTRA = true;\n')
                with self.assertRaisesRegex(ValueError, 'altered generated display data'):
                    prepare(self.output, web)
                self.assertFalse(self.output.exists())
