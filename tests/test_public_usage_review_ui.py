"""Ensure the internal screen is a reproducible read-only review projection."""
import hashlib
import json
import unittest
from pathlib import Path
from scripts import build_public_usage_review_ui as ui
from scripts import validate_public_usage_review as review

class PublicUsageReviewUIProjectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload=ui.build()
        cls.data=json.loads(cls.payload.split('window.CONNECTABLE_REVIEW_DATA = ',1)[1].removesuffix(';\n'))
        cls.original={r['id']:r for _,r,_ in review.read_jsonl(review.MAPPING)}

    def test_asset_reproducible(self):
        self.assertEqual(ui.OUTPUT.read_text(),self.payload)

    def test_exact_eighteen_ids_without_private_case(self):
        self.assertEqual({r['id'] for r in self.data['records']},review.EXPECTED_IDS)
        self.assertEqual(len(self.data['records']),18)

    def test_unknown_review_status_and_no_approval(self):
        self.assertEqual((self.data['recordStatus'],self.data['publicStatus'],self.data['approvedGold']),('REVIEW_ONLY','UNKNOWN',0))
        for r in self.data['records']:
            self.assertEqual((r['grade'],r['reviewStatus'],r['basis']),('C','NEEDS_REVIEW','USER_REPORT'))
            self.assertNotIn('outcome',r)
            self.assertNotIn('compatible',r)

    def test_functional_slots_copied_without_promotion(self):
        for r in self.data['records']:
            original=self.original[r['id']]
            self.assertEqual(r['functionalObservations'],original['functional_observations'])
            self.assertEqual(r['observations'],original['mapping']['observations'])
            self.assertEqual(r['attempts'],original['mapping']['attempts'])
            self.assertEqual(r['configurations'],original['mapping']['configurations'])

    def test_source_dates_and_actor_roles_retained(self):
        for r in self.data['records']:
            original=self.original[r['id']]
            self.assertEqual(r['source'],original['mapping']['source'])
            self.assertEqual(r['evidence'],original['mapping']['evidence'])
            self.assertEqual(r['commercial'],original['mapping']['review']['commercial_context'])

    def test_internal_source_pointers_hashes_and_file_paths_omitted(self):
        self.assertNotIn('source_pointers',self.payload)
        self.assertNotIn('source_line_sha256',self.payload)
        self.assertNotIn(str(ui.ROOT),self.payload)
        self.assertNotIn('data/research/',self.payload)

    def test_public_https_only_no_local_or_credential_urls(self):
        for url in ['file:///Users/person/secret','https://user:secret@example.com','http://example.com','https://127.0.0.1','https://device.local','https://service.internal']:
            self.assertFalse(ui.safe_external_url(url),url)
        self.assertTrue(ui.safe_external_url('https://example.com/post'))

    def test_script_safe_projection(self):
        self.assertNotIn('<',self.payload)

    def test_generator_does_not_write_source_data(self):
        paths=[review.SOURCE,review.MAPPING,ui.ROOT/'data/research/user_questions_v2.jsonl',ui.ROOT/'data/rules/path_instances_v1.json']
        before=[hashlib.sha256(p.read_bytes()).hexdigest() for p in paths]
        ui.build()
        self.assertEqual(before,[hashlib.sha256(p.read_bytes()).hexdigest() for p in paths])

if __name__=='__main__':unittest.main()
