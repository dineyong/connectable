"""Invented object IDs are structural fixtures, never research/product/gold facts."""
import unittest
from scripts.validate_connection_path_proposal import validate


def fixture():
    return dict(model_version='1-proposed', status='PROPOSED',
                devices=[dict(id='test-source', kind='SOURCE', identity_status='UNKNOWN'),
                         dict(id='test-display', kind='DISPLAY', identity_status='UNKNOWN')],
                ports=[dict(id='test-out', device_id='test-source', connector='UNKNOWN',
                            video_direction='UNKNOWN', power_role='UNKNOWN', capability_refs=[]),
                       dict(id='test-in', device_id='test-display', connector='UNKNOWN',
                            video_direction='UNKNOWN', power_role='UNKNOWN', capability_refs=[])],
                capabilities=[], edges=[dict(id='test-edge', from_port='test-out', to_port='test-in',
                    kind='PHYSICAL', output_method='UNKNOWN', protocol='UNKNOWN', capability_refs=[])],
                paths=[dict(id='test-path', source_device_id='test-source', edge_ids=['test-edge'],
                    display_targets=[dict(display_device_id='test-display')], topology_completeness='COMPLETE',
                    context=dict(lid_state='UNKNOWN', builtin_state='UNKNOWN', external_power='UNKNOWN', external_input='UNKNOWN'))])


class ConnectionPathProposalTests(unittest.TestCase):
    def setUp(self):
        self.data = fixture()

    def test_unknown_capability_is_valid_structure_not_approval(self):
        self.assertEqual([], validate(self.data))

    def test_duplicate_id(self):
        self.data['ports'][0]['id'] = 'test-source'
        self.assertTrue(validate(self.data))

    def test_missing_endpoint(self):
        self.data['edges'][0]['to_port'] = 'missing'
        self.assertTrue(validate(self.data))

    def test_missing_capability(self):
        self.data['ports'][0]['capability_refs'] = ['missing']
        self.assertTrue(validate(self.data))

    def test_exact_requires_product(self):
        self.data['devices'][0]['identity_status'] = 'EXACT'
        self.assertTrue(validate(self.data))

    def test_internal_routing_cannot_cross_devices(self):
        self.data['edges'][0]['kind'] = 'INTERNAL_ROUTING'
        self.assertTrue(validate(self.data))

    def test_complete_requires_reachability(self):
        self.data['paths'][0]['edge_ids'] = []
        self.assertTrue(validate(self.data))

    def test_partial_preserves_gap(self):
        self.data['paths'][0]['edge_ids'] = []
        self.data['paths'][0]['topology_completeness'] = 'PARTIAL'
        self.assertEqual([], validate(self.data))

    def test_bad_enum(self):
        self.data['edges'][0]['output_method'] = 'USB_C'
        self.assertTrue(validate(self.data))

    def test_no_compatibility_status_in_topology(self):
        self.data['paths'][0]['public_status'] = 'COMPATIBLE'
        self.assertTrue(validate(self.data))
