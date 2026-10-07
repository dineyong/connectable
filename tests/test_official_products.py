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


class OfficialBatchTwoTests(unittest.TestCase):
    def setUp(self):
        self.catalog = load_catalog()
        self.pro = self.catalog['products'][2]
        self.max = self.catalog['products'][3]
        self.air = self.catalog['products'][4]

    def test_shared_source(self):
        self.assertEqual(2, len(self.catalog['sources'][2]['applies_to_models']))
        self.assertEqual([], validate_catalog(self.catalog))

    def test_group_sum_mismatch(self):
        self.max['claims'][0]['external_count'] = 3
        self.assertTrue(validate_catalog(self.catalog))

    def test_flattened_max_rejected(self):
        self.max['claims'][0]['resolution_label'] = '6K'
        self.assertTrue(validate_catalog(self.catalog))

    def test_closed_lid_builtin_rejected(self):
        self.air['claims'][1]['prerequisites']['builtin_state'] = 'ON'
        self.assertTrue(validate_catalog(self.catalog))

    def test_support_grade_not_spec_grade(self):
        self.catalog['sources'][4]['reliability_grade'] = 'A'
        self.assertTrue(validate_catalog(self.catalog))

    def test_pro_and_max_limits_not_merged(self):
        for product, count, expected in [(self.pro, 3, 'INCOMPATIBLE'),
                                         (self.max, 4, 'UNKNOWN'),
                                         (self.max, 5, 'INCOMPATIBLE')]:
            result = evaluate(dict(product_id=product['product_id'], output_method='NATIVE',
                                   builtin_active=True, external_independent_count=count))
            self.assertEqual(expected, result['candidate_status'])
            self.assertEqual('UNKNOWN', result['status'])

    def test_m3_open_and_closed_not_merged(self):
        for builtin, expected in [(True, 'INCOMPATIBLE'), (False, 'UNKNOWN')]:
            r = evaluate(dict(product_id=self.air['product_id'], output_method='NATIVE',
                              builtin_active=builtin, external_independent_count=2))
            self.assertEqual(expected, r['candidate_status'])

    def test_contradictory_request_unknown(self):
        r = evaluate(dict(product_id=self.air['product_id'], output_method='NATIVE',
                          builtin_active=True, lid_state='CLOSED', external_independent_count=2))
        self.assertEqual('UNKNOWN', r['candidate_status'])

    def test_m3_requirements_retained(self):
        pre = self.air['claims'][1]['prerequisites']
        self.assertEqual('14.3', pre['minimum_macos'])
        self.assertEqual('YES', pre['power_required'])
        self.assertEqual('YES', pre['external_input_required'])
        self.assertEqual(['6K', '5K'], [g['resolution_label'] for g in self.air['claims'][1]['display_groups']])

    def test_existing_catalog_facts_preserved(self):
        import hashlib, json
        # First-batch canonical product hash; independent of shallow Git history.
        actual = hashlib.sha256(json.dumps(self.catalog['products'][:2],
                                          sort_keys=True, ensure_ascii=False).encode()).hexdigest()
        self.assertEqual('96cd725df425709308df1ca685d9e6da69941647f85ab8101f4450ff4a7d0d5b', actual)
