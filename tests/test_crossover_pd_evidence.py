"""Bounded supplemental evidence must never promote the old fact or public state."""
import copy
import json
import unittest
from unittest.mock import patch
from scripts.crossover_pd_evidence import PATH, ROOT, load, validate


class CrossoverPDEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.data = load(PATH)

    def reject(self):
        with self.assertRaises(ValueError):
            validate(self.data)

    def test_real_batch_is_read_only_and_original_unknown(self):
        before = copy.deepcopy(self.data)
        original = (ROOT/'data/site/content-v2.json').read_bytes()
        validate(self.data)
        self.assertEqual(self.data, before)
        self.assertEqual((ROOT/'data/site/content-v2.json').read_bytes(), original)
        site = json.loads(original)
        fact = next(f for m in site['monitors'] for f in m['features'] if f['fact_id'] == self.data['related_fact_id'])
        self.assertEqual(fact['payload']['watts'], 'UNKNOWN')
        self.assertEqual(self.data['assertion']['payload']['watts'], 65)

    def test_stale_fact_hash(self):
        self.data['original_fact_sha256'] = '0'*64
        self.reject()

    def test_wrong_product_or_model(self):
        for field, value in [('product_id','product:lg-27up850-w'), ('model_scope','27ULD951')]:
            with self.subTest(field=field):
                data = copy.deepcopy(self.data)
                data[field] = value
                with self.assertRaises(ValueError): validate(data)

    def test_wrong_parent_source(self):
        self.data['source']['url'] = 'https://www.crosslcd.co.kr/shop/item.php?it_id=123'
        self.reject()

    def test_parent_url_spoofing(self):
        for url in ['https://www.crosslcd.co.kr.evil.test/shop/item.php?it_id=1716533757', 'https://www.crosslcd.co.kr/shop/item.php?it_id=1716533757&redirect=https://evil.test', 'http://www.crosslcd.co.kr/shop/item.php?it_id=1716533757']:
            with self.subTest(url=url):
                data = copy.deepcopy(self.data)
                data['source']['url'] = url
                with self.assertRaises(ValueError): validate(data)

    def test_asset_not_bound_by_same_host_alone(self):
        self.data['asset']['url'] = 'https://www.crosslcd.co.kr/data/editor/2411/other-model.jpg'
        self.reject()

    def test_asset_ref_and_evidence_refs(self):
        for field in ['parent_source_ref','asset_id']:
            with self.subTest(field=field):
                data = copy.deepcopy(self.data)
                data['asset'][field] = 'MISSING'
                with self.assertRaises(ValueError): validate(data)

    def test_empty_or_duplicate_evidence(self):
        for refs in [[], ['CROSS-PD-IMAGE','CROSS-PD-IMAGE'], ['CROSS-PD-PAGE']]:
            data = copy.deepcopy(self.data)
            data['assertion']['evidence_refs'] = refs
            with self.assertRaises(ValueError): validate(data)

    def test_capture_hash_and_bytes(self):
        self.data['asset']['capture_sha256'] = '0'*64
        self.reject()
        self.data = load(PATH)
        with patch('scripts.crossover_pd_evidence.capture_digest', return_value='1'*64): self.reject()

    def test_capture_path_escape(self):
        for path in ['../outside.jpg','/tmp/capture.jpg','docs/evidence/../other.jpg']:
            data = copy.deepcopy(self.data)
            data['asset']['capture_path'] = path
            with self.assertRaises(ValueError): validate(data)

    def test_unknown_port_or_qualifier_cannot_be_promoted(self):
        for field, value in [('interface','USB_C'),('rating_basis','UP_TO'),('rating_basis','RATED'),('watts',90)]:
            data = copy.deepcopy(self.data)
            data['assertion']['payload'][field] = value
            with self.assertRaises(ValueError): validate(data)

    def test_partial_field_coverage(self):
        self.data['assertion']['confirmed_fields'] = ['watts']
        self.reject()

    def test_no_public_human_or_catalog_approval(self):
        for field, value in [('catalog_application','APPLIED'),('public_status','COMPATIBLE'),('usable_for_compatibility','YES')]:
            data = copy.deepcopy(self.data)
            data[field] = value
            with self.assertRaises(ValueError): validate(data)
        self.data['assertion']['review_status'] = 'APPROVED'
        self.reject()

    def test_checked_date_and_origin(self):
        for field, value in [('checked_on','2026-02-30'),('checked_on','2026-10-10'),('source_status','MIGRATED_V1'),('model_scope','OTHER')]:
            data = copy.deepcopy(self.data)
            data['source'][field] = value
            with self.assertRaises(ValueError): validate(data)

    def test_extra_fields_and_personal_information(self):
        self.data['assertion']['reviewer'] = 'invented'
        self.reject()
        self.data = load(PATH)
        self.data['limitations'].append('contact@example.com')
        self.reject()

    def test_symbolic_capture_rejected(self):
        with patch('pathlib.Path.is_symlink', return_value=True):
            self.reject()

    def test_duplicate_local_ids(self):
        self.data['assertion']['assertion_id'] = self.data['asset']['asset_id']
        self.reject()

    def test_schema_is_strict_supported_contract(self):
        from scripts.crossover_pd_evidence import SCHEMA
        from scripts.validate_question_corpus_v2 import audit_schema
        schema = load(SCHEMA)
        audit_schema(schema)
        self.assertFalse(schema['additionalProperties'])
        self.assertEqual(set(schema['required']), set(schema['properties']))

    def test_duplicate_json_keys_rejected(self):
        from tempfile import TemporaryDirectory
        from pathlib import Path
        with TemporaryDirectory() as folder:
            p = Path(folder)/'duplicate.json'
            p.write_text('{"schema_version":1,"schema_version":2}')
            with self.assertRaises(ValueError): load(p)


if __name__ == '__main__':
    unittest.main()
