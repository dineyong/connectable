import copy
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from scripts import build_monipick_cloudflare as build
from scripts import prepare_monipick_brand_review as review


class BrandReleaseTests(unittest.TestCase):
    def test_release_is_exact_reviewed_bytes_and_retains_policy(self):
        _,expected=review.brand_artifacts()
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'release';m=build.build_for_branch(build.PRODUCTION_BRANCH,out)
            self.assertEqual(m['files'],{n:build.digest(v) for n,v in expected.items()})
            self.assertTrue(m['publication_authorized'])
            self.assertFalse(m['analytics_enabled']);self.assertFalse(m['advertising_enabled'])
            self.assertTrue(review.validate_brand_review(out)) # unapproved validator cannot grant authority

    def test_changed_approval_missing_approval_and_changed_asset_rejected(self):
        record=build.read_brand_approval()
        for key,value in [('approval_status','PENDING'),('origin','https://wrong.example'),
            ('reviewed_candidate_commit','unreviewed'),('baseline_content_fingerprint','0'*64),
            ('approved_content_fingerprint','0'*64),('advertising_enabled',True),('analytics_enabled',True),
            ('main_merge_authorized',True),('compatibility_approval_authorized',True)]:
            bad=copy.deepcopy(record);bad[key]=value
            with tempfile.TemporaryDirectory() as tmp,self.subTest(key=key):
                out=Path(tmp)/'release'
                with patch.object(build,'read_brand_approval',return_value=bad),self.assertRaises(ValueError):
                    build.build_for_branch(build.PRODUCTION_BRANCH,out)
                self.assertFalse(out.exists())
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'release'
            with patch.object(build,'read_brand_approval',side_effect=FileNotFoundError),self.assertRaises(FileNotFoundError):
                build.build_for_branch(build.PRODUCTION_BRANCH,out)
            original=review.brand_artifacts
            def changed():
                plan,a=original();a['assets/brand/monipick-share-v1.png']+=b'changed';return plan,a
            with patch.object(review,'brand_artifacts',side_effect=changed),self.assertRaises(ValueError):
                build.build_for_branch(build.PRODUCTION_BRANCH,out)
            self.assertFalse(out.exists())
