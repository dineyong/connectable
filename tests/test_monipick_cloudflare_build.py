"""Only the explicitly reviewed file inventory may enter the production build."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from scripts import build_monipick_cloudflare as build
from scripts.build_monipick_public_candidate import validate_candidate


class CloudflareReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.output=Path(self.temp.name)/'build'

    def test_production_uses_identical_approved_content_with_separate_approval_manifest(self):
        manifest=build.build_for_branch(build.PRODUCTION_BRANCH,self.output)
        self.assertTrue(manifest['publication_authorized'])
        self.assertTrue(manifest['deployment_authorized'])
        self.assertFalse(manifest['analytics_enabled'])
        self.assertFalse(manifest['advertising_enabled'])
        self.assertEqual(manifest['domain'],'monipick.com')
        self.assertEqual(manifest['approved_content_fingerprint'],build.content_fingerprint(manifest['files']))
        self.assertFalse((self.output/'site/manifest.json').exists())
        self.assertIn('index,follow',(self.output/'site/index.html').read_text())
        self.assertFalse((self.output/'site/__preview_http_check.html').exists())
        self.assertTrue(validate_candidate(self.output)) # candidate validator must not silently grant approval

    def test_preview_still_uses_protected_builder(self):
        manifest=build.build_for_branch(build.PREVIEW_BRANCH,self.output)
        self.assertFalse(manifest['deployment_authorized'])
        self.assertIn('noindex',(self.output/'site/index.html').read_text())
        self.assertIn('Disallow: /',(self.output/'site/robots.txt').read_text())

    def test_main_unknown_and_missing_branch_refused_before_build(self):
        for branch in ['main','codex/unreviewed','']:
            with self.subTest(branch=branch),self.assertRaises(ValueError):build.build_for_branch(branch,self.output)
        self.assertFalse(self.output.exists())

    def test_missing_or_inconsistent_approval_refused(self):
        record=json.loads(build.APPROVAL.read_text())
        for key,value in [('approval_status','PENDING'),('origin','https://other.example'),
                          ('analytics_enabled',True),('advertising_enabled',True),
                          ('main_merge_authorized',True),('compatibility_approval_authorized',True),
                          ('approved_on','invalid'),('approved_content_fingerprint','0'*64)]:
            bad=copy.deepcopy(record);bad[key]=value
            with self.subTest(key=key),patch.object(build,'read_approval',return_value=bad),self.assertRaises(ValueError):
                build.build_for_branch(build.PRODUCTION_BRANCH,self.output)
        self.assertFalse(self.output.exists())

    def test_approval_required_and_content_change_is_not_silently_approved(self):
        with patch.object(build,'read_approval',side_effect=FileNotFoundError),self.assertRaises(FileNotFoundError):
            build.build_for_branch(build.PRODUCTION_BRANCH,self.output)
        real=build.expected_artifacts
        def changed():
            plan,artifacts=real()
            artifacts['monitor-v3.js']+=b'\n// changed content\n'
            return plan,artifacts
        with patch.object(build,'expected_artifacts',side_effect=changed),self.assertRaises(ValueError):
            build.build_for_branch(build.PRODUCTION_BRANCH,self.output)
        self.assertFalse(self.output.exists())

    def test_sitemap_encoding_is_independent_of_locale(self):
        from scripts.prepare_monipick_release import sitemap,release_plan
        from scripts.prepare_launch_preview import WEB
        plan=release_plan(WEB)
        values=[]
        for spelling in ['UTF-8','utf-8','cp949']:
            with patch('locale.getpreferredencoding',return_value=spelling):
                values.append(sitemap(plan))
        self.assertTrue(all(v==values[0] for v in values))
        self.assertTrue(values[0].startswith("<?xml version='1.0' encoding='UTF-8'?>"))

    def test_existing_output_is_not_overwritten(self):
        self.output.mkdir();(self.output/'keep').write_text('keep')
        with self.assertRaises(ValueError):build.build_for_branch(build.PRODUCTION_BRANCH,self.output)
        self.assertEqual((self.output/'keep').read_text(),'keep')
