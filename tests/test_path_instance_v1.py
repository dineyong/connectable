import copy
import unittest
from scripts.path_instance_v1 import load_instances, claim_index, validate, evaluate, predicate_value


class PathInstanceTests(unittest.TestCase):
    def setUp(self):
        self.data=load_instances()

    def test_real_five_review_candidates(self):
        self.assertEqual(5,len(self.data['instances']))
        self.assertEqual([],validate(self.data))
        for r in self.data['instances']:
            result=evaluate(r)
            # Author-proposed review expectations, NOT human-approved gold answers.
            self.assertEqual(r['review_expectation'],result['candidate_status'])
            self.assertEqual('UNKNOWN',result['public_status'])

    def test_duplicate_instance(self):
        self.data['instances'].append(copy.deepcopy(self.data['instances'][0]))
        self.assertTrue(validate(self.data))

    def test_duplicate_local_id(self):
        self.data['instances'][0]['ports'][0]['id']='host'
        self.assertTrue(validate(self.data))

    def test_foreign_product_claim(self):
        self.data['instances'][0]['ports'][0]['claim_refs']=['lg-27up850-w:2']
        self.assertTrue(validate(self.data))

    def test_port_profile_on_wrong_connector(self):
        r=self.data['instances'][0]
        next(p for p in r['ports'] if p['id']=='screen1-in')['claim_refs']=['dell-g2724d:2']
        self.assertTrue(validate(self.data))

    def test_reverse_converter(self):
        r=self.data['instances'][0]
        edge=next(e for e in r['edges'] if e['id']=='middle-route')
        edge['from_port'],edge['to_port']=edge['to_port'],edge['from_port']
        self.assertTrue(validate(self.data))

    def test_connector_mismatch(self):
        self.data['instances'][0]['ports'][0]['connector']='HDMI'
        self.assertTrue(validate(self.data))

    def test_missing_port(self):
        self.data['instances'][0]['edges'][0]['to_port']='missing'
        self.assertTrue(validate(self.data))

    def test_unreachable_target(self):
        self.data['instances'][0]['edges'].pop()
        self.assertTrue(validate(self.data))

    def test_cycle(self):
        r=self.data['instances'][0]
        r['edges'].append(dict(id='cycle',from_port='middle-out',to_port='middle-in',kind='INTERNAL_ROUTING',claim_refs=[]))
        self.assertTrue(validate(self.data))

    def test_partial_cable_not_promoted(self):
        self.data['instances'][2]['devices'][1]['identity_status']='EXACT'
        self.assertTrue(validate(self.data))

    def test_unknown_driver_does_not_become_success(self):
        result=evaluate(self.data['instances'][3])
        self.assertEqual('UNKNOWN',result['predicates'][0]['result'])
        self.assertEqual('UNKNOWN',result['candidate_status'])

    def test_installed_driver_not_full_success(self):
        r=self.data['instances'][3]
        r['request']['context']['displaylink_driver']='INSTALLED'
        result=evaluate(r)
        self.assertEqual('TRUE',result['predicates'][0]['result'])
        self.assertEqual('UNKNOWN',result['candidate_status'])

    def test_predicate_missing_and_unknown(self):
        p=dict(context_key='displaylink_driver',operator='EQ',expected='INSTALLED')
        self.assertEqual('UNKNOWN',predicate_value(p,{}))
        self.assertEqual('UNKNOWN',predicate_value(p,{'displaylink_driver':'UNKNOWN'}))

    def test_semantic_version_comparison(self):
        p=dict(context_key='os_version',operator='VERSION_GTE',expected='14.3')
        for actual,expected in [('14.2.9','FALSE'),('14.3','TRUE'),('14.10','TRUE'),('14.3 beta','UNKNOWN'),('UNKNOWN','UNKNOWN')]:
            self.assertEqual(expected,predicate_value(p,{'os_version':actual}))

    def test_invalid_operator_rejected(self):
        self.data['instances'][3]['predicates'][0]['operator']='EVAL'
        self.assertTrue(validate(self.data))

    def test_predicate_requires_official_claim(self):
        self.data['instances'][3]['predicates'][0]['expected']='NOT_NEEDED'
        self.assertTrue(validate(self.data))

    def test_mst_exclusion_and_native_count_separate(self):
        result=evaluate(self.data['instances'][4])
        self.assertEqual('FALSE',result['predicates'][0]['result'])
        self.assertEqual('INCOMPATIBLE',result['source_constraint']['candidate_status'])
        self.assertEqual('UNKNOWN',result['public_status'])

    def test_unknown_os_not_made_mst_supported(self):
        r=self.data['instances'][4]
        r['request']['context']['os_family']='UNKNOWN'
        r['request']['context']['builtin_state']='UNKNOWN'
        result=evaluate(r)
        self.assertEqual('UNKNOWN',result['candidate_status'])

    def test_resource_capacity_must_match_claim(self):
        self.data['instances'][3]['resources'][0]['max_independent_displays']=4
        self.assertTrue(validate(self.data))

    def test_aggregate_capacity_not_simultaneous_approval(self):
        result=evaluate(self.data['instances'][3])
        self.assertEqual(2,result['resources'][0]['selected_display_count'])
        self.assertEqual('WITHIN_AGGREGATE_LIMIT',result['resources'][0]['status'])
        self.assertEqual('UNKNOWN',result['candidate_status'])

    def test_power_upper_bound_not_charging_result(self):
        result=evaluate(self.data['instances'][2])
        self.assertEqual(90,result['power']['recorded_ceiling_w'])
        self.assertEqual('UNKNOWN',result['power']['status'])

    def test_pass_through_not_offer(self):
        r=self.data['instances'][1]
        r['power_flows'][0]['mode']='OFFER'
        self.assertTrue(validate(self.data))

    def test_cannot_auto_approve(self):
        self.data['instances'][0]['review_status']='APPROVED'
        self.assertTrue(validate(self.data))

    def test_expected_review_answer_not_engine_input(self):
        r=self.data['instances'][0]
        before=evaluate(r)
        r['review_expectation']='INCOMPATIBLE'
        after=evaluate(r)
        self.assertEqual(before,after)

    def test_request_hash_changes(self):
        r=self.data['instances'][0]
        before=evaluate(r)['request_sha256']
        r['request']['targets'][0]['refresh_hz']=120
        self.assertNotEqual(before,evaluate(r)['request_sha256'])

    def test_unknown_source_identity_stays_unknown(self):
        r=self.data['instances'][0]
        r['devices'][0]['identity_status']='UNKNOWN'
        self.assertEqual('UNKNOWN',evaluate(r)['candidate_status'])

    def test_arbitrary_predicate_from_other_product(self):
        self.data['instances'][0]['predicates']=[dict(id='other',context_key='os_version',operator='VERSION_GTE',expected='10.14',claim_refs=['plugable-ud-6950h:1'])]
        self.assertTrue(validate(self.data))

    def test_power_disconnected_devices_rejected(self):
        r=self.data['instances'][2]
        r['power_flows'][0]['to_port']='host-usbc'
        self.assertTrue(validate(self.data))

    def test_power_self_edge_rejected(self):
        r=self.data['instances'][2]
        r['power_flows'][0]['to_port']=r['power_flows'][0]['from_port']
        self.assertTrue(validate(self.data))
