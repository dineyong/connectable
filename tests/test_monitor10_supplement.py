"""Adversarial tests for the bounded independent review supplement."""
import copy
import unittest

from scripts.validate_monitor10_supplement import DATA, load, validate


class Monitor10SupplementTests(unittest.TestCase):
    def setUp(self):
        self.data = load(DATA)

    def reject(self, mutate):
        mutate(self.data)
        self.assertTrue(validate(self.data))

    def test_actual_ten_records_and_eighty_selected_groups(self):
        self.assertEqual(validate(self.data), [])
        self.assertEqual(len(self.data['records']), 10)
        self.assertEqual(sum(len(r['confirmed']) for r in self.data['records']), 80)

    def test_preserves_input_data(self):
        before = copy.deepcopy(self.data)
        validate(self.data)
        self.assertEqual(self.data, before)

    def test_approval_and_source_hash_cannot_be_promoted(self):
        self.reject(lambda d: d.update(public_status='APPROVED'))
        self.setUp()
        self.reject(lambda d: d.update(source_file_sha256='0' * 64))

    def test_duplicate_and_missing_model_ids(self):
        self.reject(lambda d: d['records'][1].update(id='m10-01'))
        self.setUp()
        self.reject(lambda d: d['records'].pop())

    def test_model_alias_cannot_replace_exact_review_model(self):
        self.reject(lambda d: d['records'][3].update(selection_model='M27Q rev.1.0'))

    def test_blank_evidence_and_date_are_rejected(self):
        for field in ('location', 'scope', 'url'):
            self.setUp()
            self.reject(lambda d: d['records'][0]['confirmed'][0].update({field: ''}))
        self.setUp()
        self.reject(lambda d: d.update(checked_on='2026-02-30'))

    def test_cross_model_or_lookalike_urls_rejected(self):
        for url in ('https://www.lge.co.kr/monitors/27gs95qe',
                    'https://www.lge.co.kr.evil.test/monitors/27gp850',
                    'https://www.lge.co.kr/monitors/27gp850?redirect=https://evil.test',
                    'https://www.lge.co.kr:444/monitors/27gp850',
                    'https://www.lge.co.kr/monitors/%252f27gp850'):
            self.setUp()
            self.reject(lambda d: d['records'][0]['confirmed'][0].update(url=url))

    def test_country_scope_cannot_be_promoted(self):
        self.reject(lambda d: d['records'][8]['confirmed'][0].update(scope='Exact Korean SKU'))

    def test_duplicate_confirmed_fields(self):
        self.reject(lambda d: d['records'][0]['confirmed'].append(copy.deepcopy(d['records'][0]['confirmed'][0])))

    def test_wrong_numeric_boolean_nonfinite_and_negative(self):
        for value in (True, '68.5', -1, float('nan'), float('inf')):
            self.setUp()
            self.reject(lambda d: d['records'][0]['confirmed'][0].update(value=value))

    def test_nested_payload_required_keys(self):
        self.reject(lambda d: d['records'][0]['confirmed'][3]['value'].pop('DP'))

    def test_unknown_qualifier_remains_unknown(self):
        fact = next(f for f in self.data['records'][9]['confirmed'] if f['field'] == 'brightness_advertised')
        fact['value']['qualifier'] = 'UP_TO'
        self.assertTrue(validate(self.data))

    def test_conflicts_cannot_be_removed_or_confirmed(self):
        self.reject(lambda d: d['records'][7].update(conflicts=[]))
        self.setUp()
        self.reject(lambda d: d['records'][7]['conflicts'][0].update(field='panel'))

    def test_related_model_merge_and_usb_video_false_remain_fixed(self):
        fact = next(f for f in self.data['records'][6]['confirmed'] if f['field'] == 'distinct_related_model')
        fact['value']['merge_allowed'] = True
        self.assertTrue(validate(self.data))
        self.setUp()
        fact = next(f for f in self.data['records'][5]['confirmed'] if f['field'] == 'usb_c_video')
        fact['value'] = True
        self.assertTrue(validate(self.data))

    def test_conflict_source_substitution_rejected(self):
        self.reject(lambda d: d['records'][7]['conflicts'][0]['claims'][0].update(url='https://www.msi.com/Monitor/OTHER/Specification'))

    def test_conflict_shape_status_and_blank_context_rejected(self):
        mutations = [
            lambda d: d['records'][7]['conflicts'][0].update(status='NOT_CONFLICT_APPROVED'),
            lambda d: d['records'][7]['conflicts'][0].update(claims=[]),
            lambda d: d['records'][7]['conflicts'][0].update(resolution=''),
            lambda d: d['records'][7]['conflicts'][0]['claims'][0].update(location=''),
            lambda d: d['records'][5]['conflicts'][0].update(notes=''),
            lambda d: d['records'][6]['conflicts'][0].update(related_url='javascript:alert(1)'),
        ]
        for mutation in mutations:
            self.setUp()
            self.reject(mutation)

    def test_uncertainty_and_extra_approval_fields_rejected(self):
        self.reject(lambda d: d['records'][0].update(unconfirmed=[]))
        self.setUp()
        self.reject(lambda d: d['records'][0].update(approved=True))


if __name__ == '__main__':
    unittest.main()
