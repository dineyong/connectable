import copy
import unittest
from scripts.validate_official_products import load_catalog, validate_catalog
from scripts.evaluate_display_count_candidate import evaluate


class OfficialFoundationTests(unittest.TestCase):
    def setUp(self):
        self.catalog = load_catalog()
        self.request = dict(product_id='product:air-m1-2020', output_method='NATIVE',
                            builtin_active=True, external_independent_count=2)

    def test_actual_catalog(self):
        self.assertEqual([], validate_catalog(self.catalog))

    def test_duplicate_product(self):
        self.catalog['products'].append(copy.deepcopy(self.catalog['products'][0]))
        self.assertTrue(validate_catalog(self.catalog))

    def test_missing_source(self):
        self.catalog['products'][0]['claims'][0]['source_refs'] = ['missing']
        self.assertTrue(validate_catalog(self.catalog))

    def test_incomplete_profile(self):
        del self.catalog['products'][0]['claims'][0]['refresh_hz']
        self.assertTrue(validate_catalog(self.catalog))

    def test_bad_date(self):
        self.catalog['sources'][0]['accessed_at'] = '2026-02-30'
        self.assertTrue(validate_catalog(self.catalog))

    def test_nonofficial_url(self):
        self.catalog['sources'][0]['source_url'] = 'https://example.com/spec'
        self.assertTrue(validate_catalog(self.catalog))

    def test_count_candidate_not_public_verdict(self):
        r = evaluate(self.request)
        self.assertEqual('INCOMPATIBLE', r['candidate_status'])
        self.assertEqual('UNKNOWN', r['status'])
        self.assertTrue(r['claim_refs'])

    def test_count_within_limit_not_positive(self):
        self.request['external_independent_count'] = 1
        self.assertEqual('UNKNOWN', evaluate(self.request)['candidate_status'])

    def test_other_modes_not_native(self):
        for mode in ['DISPLAYLINK', 'UNKNOWN', 'MIRROR']:
            self.request['output_method'] = mode
            self.assertEqual('UNKNOWN', evaluate(self.request)['candidate_status'])

    def test_clamshell_not_inferred(self):
        for state in [False, None, 'true']:
            self.request['builtin_active'] = state
            self.assertEqual('UNKNOWN', evaluate(self.request)['candidate_status'])

    def test_unknown_model_not_inferred(self):
        self.request['product_id'] = 'MacBook Air M1'
        self.assertEqual('UNKNOWN', evaluate(self.request)['candidate_status'])

    def test_bad_count(self):
        for count in [True, 0, -1, 2.5, '2']:
            self.request['external_independent_count'] = count
            with self.assertRaises(ValueError):
                evaluate(self.request)

    def test_invalid_catalog_rejected(self):
        del self.catalog['sources'][0]['accessed_at']
        with self.assertRaises(ValueError):
            evaluate(self.request, self.catalog)
