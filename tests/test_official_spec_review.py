import copy
import json
import unittest
from scripts.validate_official_spec_review import PATH, validate


class OfficialSpecReviewTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(PATH.read_text())

    def reject(self):
        with self.assertRaises(ValueError):
            validate(self.data)

    def test_real_batch(self):
        before = copy.deepcopy(self.data)
        validate(self.data)
        self.assertEqual(before, self.data)
        self.assertEqual(len(self.data['assertions']), 10)

    def test_unread_manual_cannot_support_assertion(self):
        self.data['assertions'][0]['source_refs'] = ['SR-DELL-MANUAL']
        self.reject()

    def test_nonmanufacturer_source_rejected(self):
        self.data['sources'][2]['url'] = 'https://example.com/review'
        self.reject()

    def test_cross_model_evidence_rejected(self):
        self.data['assertions'][0]['source_refs'] = ['SR-LG-LV']
        self.reject()

    def test_unknown_is_not_verified(self):
        self.data['manual_reviews'][0]['verified_fields'].append('width')
        self.reject()

    def test_original_fact_hash_is_required(self):
        self.data['manual_reviews'][0]['original_fact_sha256'] = '0'*64
        self.reject()

    def test_no_compatibility_or_catalog_promotion(self):
        self.data['assertions'][0]['public_status'] = 'COMPATIBLE'
        self.reject()
        self.data = json.loads(PATH.read_text())
        self.data['catalog_application'] = 'APPLIED'
        self.reject()

    def test_dell_ports_lg_limits_and_manual_unknowns(self):
        assertions = {a['assertion_id']: a for a in self.data['assertions']}
        self.assertEqual(assertions['SR-dell-u2723qe:3']['payload']['watts'], 90)
        self.assertEqual(assertions['SR-dell-u2723qe:4']['payload']['watts'], 15)
        for port in ['HDMI', 'DISPLAYPORT', 'USB_C']:
            self.assertEqual(assertions['SR-LG-'+port]['payload']['refresh_hz'], 60)
        self.assertIn('watts', self.data['manual_reviews'][1]['unverified_fields'])


if __name__ == '__main__':
    unittest.main()
