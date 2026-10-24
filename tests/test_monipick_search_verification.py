"""Only the explicitly requested Naver ownership proof extends the approved release."""
import copy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from scripts import build_monipick_cloudflare as build


class SearchVerificationTests(unittest.TestCase):
    def test_exact_official_file_is_added_without_changing_reviewed_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / 'release'
            manifest = build.build_for_branch(build.PRODUCTION_BRANCH, output)
            proofs = manifest['search_verification_files']
            self.assertEqual(len(proofs), 1)
            name = 'naverb7d1be496d4d21a4cf88c23246e48079.html'
            self.assertEqual((output / 'site' / name).read_bytes(),
                             ('naver-site-verification: ' + name).encode())
            baseline = {k:v for k,v in manifest['files'].items() if k not in proofs}
            self.assertEqual(build.content_fingerprint(baseline),
                             manifest['approved_content_fingerprint'])
            self.assertFalse(manifest['advertising_enabled'])
            self.assertFalse(manifest['analytics_enabled'])
            self.assertNotIn('search-verification.json',manifest['files'])

    def test_preview_gets_no_verification_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / 'preview'
            build.build_for_branch(build.PREVIEW_BRANCH, output)
            self.assertFalse(list((output / 'site').glob('naver*.html')))

    def test_unapproved_wrong_origin_and_extra_files_are_rejected(self):
        record = build.read_search_verification()
        for key,value in [('approval_status','PENDING'),('origin','https://other.example'),
                          ('files',{'../index.html':'malicious'}),
                          ('files',{'index.html':'malicious'}),
                          ('files',{'naverb7d1be496d4d21a4cf88c23246e48079.html':'wrong content'})]:
            invalid=copy.deepcopy(record); invalid[key]=value
            with self.subTest(key=key,value=value), self.assertRaises(ValueError):
                build.search_verification_artifacts(invalid)

    def test_missing_verification_approval_fails_before_creating_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / 'release'
            with patch.object(build,'read_search_verification',side_effect=FileNotFoundError), self.assertRaises(FileNotFoundError):
                build.build_for_branch(build.PRODUCTION_BRANCH,output)
            self.assertFalse(output.exists())
