import copy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from scripts import build_monipick_cloudflare as build


class ApprovedContentReleaseTests(unittest.TestCase):
    def test_production_matches_approved_content_and_preserves_holds(self):
        with tempfile.TemporaryDirectory() as temp:
            output=Path(temp)/'release'
            m=build.build_for_branch(build.PRODUCTION_BRANCH,output)
            self.assertEqual(m['reviewed_candidate_commit'],'89dd4ec')
            self.assertIn('model-highlights',(output/'site/monitors/asus-pa279crv/index.html').read_text())
            self.assertNotIn('href="../../monitor-v3.html"',(output/'site/monitors/asus-pa279crv/index.html').read_text())
            self.assertNotEqual(m['approved_content_fingerprint'],m['baseline_approved_content_fingerprint'])
            self.assertFalse(m['analytics_enabled']); self.assertFalse(m['advertising_enabled'])
            self.assertTrue((output/'site'/build.NAVER_PROOF).exists())
            self.assertIn('no-transform',(output/'site/_headers').read_text())

    def test_missing_and_invalid_content_approval_fail_closed(self):
        record=build.read_content_approval()
        for key,value in [('approval_status','PENDING'),('origin','https://other.example'),
                          ('reviewed_candidate_commit','unreviewed'),('baseline_content_fingerprint','0'*64),
                          ('approved_content_fingerprint','0'*64),('advertising_enabled',True),
                          ('analytics_enabled',True),('main_merge_authorized',True)]:
            bad=copy.deepcopy(record);bad[key]=value
            with tempfile.TemporaryDirectory() as tmp, self.subTest(key=key):
                output=Path(tmp)/'release'
                with patch.object(build,'read_content_approval',return_value=bad), self.assertRaises(ValueError):
                    build.build_for_branch(build.PRODUCTION_BRANCH,output)
                self.assertFalse(output.exists())

    def test_changed_summary_or_style_is_not_automatically_approved(self):
        original=build.polished_artifacts
        def changed():
            plan,artifacts=original();artifacts['monitor-detail-v3.css']+=b'\nbody{display:none}'
            return plan,artifacts
        with tempfile.TemporaryDirectory() as tmp,patch.object(build,'polished_artifacts',side_effect=changed),self.assertRaises(ValueError):
            build.build_for_branch(build.PRODUCTION_BRANCH,Path(tmp)/'release')
