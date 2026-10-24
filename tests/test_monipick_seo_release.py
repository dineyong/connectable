import copy
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from scripts import build_monipick_cloudflare as build
from scripts import prepare_monipick_seo_review as review


class SeoReleaseTests(unittest.TestCase):
    def test_production_bytes_equal_reviewed_candidate_including_all_summaries(self):
        _,expected=review.review_artifacts()
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'release';manifest=build.build_for_branch(build.PRODUCTION_BRANCH,out)
            self.assertEqual(manifest['files'],{n:build.digest(v) for n,v in expected.items()})
            for n,v in expected.items():self.assertEqual((out/'site'/n).read_bytes(),v)
            self.assertTrue(manifest['publication_authorized'])
            self.assertFalse(manifest['analytics_enabled']);self.assertFalse(manifest['advertising_enabled'])
            self.assertFalse((out/'site/deploy').exists())

    def test_changed_scope_fingerprint_or_unreviewed_candidate_is_rejected(self):
        record=build.read_seo_approval()
        for key,value in [('approval_status','PENDING'),('origin','https://wrong.example'),
            ('reviewed_candidate_commit','unreviewed'),('baseline_content_fingerprint','0'*64),
            ('approved_content_fingerprint','0'*64),('advertising_enabled',True),('analytics_enabled',True),
            ('main_merge_authorized',True),('compatibility_approval_authorized',True)]:
            bad=copy.deepcopy(record);bad[key]=value
            with tempfile.TemporaryDirectory() as tmp,self.subTest(key=key):
                out=Path(tmp)/'release'
                with patch.object(build,'read_seo_approval',return_value=bad),self.assertRaises(ValueError):
                    build.build_for_branch(build.PRODUCTION_BRANCH,out)
                self.assertFalse(out.exists())

    def test_missing_seo_approval_or_modified_candidate_cannot_be_published(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'release'
            with patch.object(build,'read_seo_approval',side_effect=FileNotFoundError),self.assertRaises(FileNotFoundError):
                build.build_for_branch(build.PRODUCTION_BRANCH,out)
            original=review.review_artifacts
            def changed():
                plan,artifacts=original();artifacts['monitor-detail-v3.css']+=b'body{display:none}'
                return plan,artifacts
            with patch.object(review,'review_artifacts',side_effect=changed),self.assertRaises(ValueError):
                build.build_for_branch(build.PRODUCTION_BRANCH,out)
            self.assertFalse(out.exists())
