import copy
import unittest
from scripts.audit_path_instance_goals import audit_goal, audit_all
from scripts.path_instance_v1 import load_instances, evaluate


class GoalAuditTests(unittest.TestCase):
    def setUp(self):
        self.data = load_instances()

    def test_existing_qhd_variants_are_not_original_goal_matches(self):
        results = audit_all(self.data)
        self.assertEqual(['VARIANT', 'VARIANT', 'PARTIAL_MATCH',
                          'PARTIAL_MATCH', 'PARTIAL_MATCH'],
                         [r['status'] for r in results])
        self.assertTrue(all(r['approved'] is False for r in results))

    def test_4k_goal_match_does_not_approve_or_change_engine(self):
        r = self.data['instances'][0]
        r['request']['targets'][0].update(width=3840, height=2160)
        # Synthetic mutation only: its existing QHD screen is NOT a 4K claim.
        self.assertEqual('PARTIAL_MATCH', audit_goal(r)['status'])
        self.assertFalse(audit_goal(r)['approved'])
        self.assertEqual('UNKNOWN', evaluate(r)['candidate_status'])
        self.assertEqual('UNKNOWN', evaluate(r)['public_status'])

    def test_4k30_still_variant(self):
        r = self.data['instances'][1]
        r['request']['targets'][0].update(width=3840, height=2160, refresh_hz=30)
        self.assertEqual('VARIANT', audit_goal(r)['status'])

    def test_wrong_model_generation(self):
        r = self.data['instances'][2]
        r['devices'][0]['product_ref'] = 'product:air-m1-2020'
        self.assertEqual('VARIANT', audit_goal(r)['status'])

    def test_displaylink_count_cannot_be_replaced_by_one(self):
        r = self.data['instances'][3]
        r['request']['independent_external_count'] = 1
        self.assertEqual('VARIANT', audit_goal(r)['status'])

    def test_displaylink_cannot_be_replaced_by_native(self):
        r = self.data['instances'][3]
        r['request']['output_method'] = 'NATIVE'
        self.assertEqual('VARIANT', audit_goal(r)['status'])

    def test_direct_path_dock_detected(self):
        r = self.data['instances'][2]
        r['devices'].append(dict(id='extra', kind='DOCK', identity_status='UNKNOWN'))
        self.assertEqual('VARIANT', audit_goal(r)['status'])

    def test_windows_not_macos_goal(self):
        r = self.data['instances'][4]
        r['request']['context']['os_family'] = 'Windows'
        self.assertEqual('VARIANT', audit_goal(r)['status'])

    def test_non_mst_binding_not_mst_goal(self):
        r = self.data['instances'][4]
        r['bindings'] = []
        self.assertEqual('VARIANT', audit_goal(r)['status'])

    def test_plan_drift_requires_reconsidering_contract(self):
        with self.assertRaisesRegex(ValueError, 'draft plan changed'):
            audit_goal(self.data['instances'][0], plan_text='changed plan')

    def test_outside_scope_is_not_checked(self):
        r = self.data['instances'][0]
        r['gold_plan_id'] = 'GP-01'
        self.assertEqual('NOT_CHECKED', audit_goal(r)['status'])

    def test_audit_is_read_only(self):
        original = copy.deepcopy(self.data)
        audit_all(self.data)
        self.assertEqual(original, self.data)

    def test_invalid_path_not_audited_as_valid(self):
        self.data['instances'][0]['edges'][0]['to_port'] = 'missing'
        with self.assertRaises(ValueError):
            audit_all(self.data)

    def test_m2_direct_match_exposes_unset_goals_and_unverified_state(self):
        result = audit_goal(self.data['instances'][2])
        self.assertEqual('PARTIAL_MATCH', result['status'])
        self.assertEqual(['resolution', 'refresh_hz', 'external_display_count', 'charging_goal'],
                         result['unspecified_goal_fields'])
        self.assertEqual('NOT_VERIFIED', result['verification_status'])
        self.assertFalse(result['approved'])

    def test_all_five_have_unset_goals_and_are_not_verified(self):
        for result in audit_all(self.data):
            self.assertTrue(result['unspecified_goal_fields'])
            self.assertEqual('NOT_VERIFIED', result['verification_status'])
            self.assertNotIn(result['status'], ('MATCHES_STATED_GOAL', 'VERIFIED', 'COMPLETE'))

    def test_uhd_goal_defined_but_configuration_not_approved(self):
        r = copy.deepcopy(self.data['instances'][0])
        r['request']['targets'][0].update(width=3840, height=2160)
        result = audit_goal(r)
        self.assertEqual('PARTIAL_MATCH', result['status'])
        self.assertNotIn('4K_pixel_dimensions', result['unspecified_goal_fields'])
        self.assertIn('charging_goal', result['unspecified_goal_fields'])
        self.assertEqual('NOT_VERIFIED', result['verification_status'])
        self.assertFalse(result['approved'])

    def test_dci_4k_is_not_the_approved_uhd_goal(self):
        for row in self.data['instances'][:2]:
            row['request']['targets'][0].update(width=4096, height=2160)
            self.assertEqual('VARIANT', audit_goal(row)['status'])

    def test_unspecified_goal_list_cannot_mutate_shared_contract(self):
        r = self.data['instances'][2]
        audit_goal(r)['unspecified_goal_fields'].clear()
        self.assertTrue(audit_goal(r)['unspecified_goal_fields'])

    def test_uhd_goal_is_identical_for_dp_and_hdmi(self):
        for row in self.data['instances'][:2]:
            row['request']['targets'][0].update(width=3840, height=2160, refresh_hz=60)
            result = audit_goal(row)
            self.assertEqual([], result['differences'])
            self.assertNotIn('4K_pixel_dimensions', result['unspecified_goal_fields'])

    def test_other_paths_unspecified_goals_remain_unchanged(self):
        results = audit_all(self.data)
        self.assertEqual(['resolution', 'refresh_hz', 'external_display_count', 'charging_goal'],
                         results[2]['unspecified_goal_fields'])
        self.assertEqual(['resolution', 'refresh_hz', 'charging_goal'],
                         results[3]['unspecified_goal_fields'])
        self.assertEqual(['source_device_model', 'resolution', 'refresh_hz',
                          'external_display_count', 'charging_goal'],
                         results[4]['unspecified_goal_fields'])
