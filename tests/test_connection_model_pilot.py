import copy
import json
import unittest
from scripts.validate_connection_model_pilot import ROOT, load_pilot, validate
from scripts.validate_question_corpus_v2 import check_value


class TypedPilotTests(unittest.TestCase):
    def setUp(self):
        self.data = load_pilot()

    def fact(self, property):
        return next(f for f in self.data['facts'] if f['property'] == property)

    def test_real_pilot(self):
        self.assertEqual([], validate(self.data))
        self.assertEqual(9, len(self.data['products']))
        self.assertEqual(29, len(self.data['facts']))

    def test_categories(self):
        from collections import Counter
        kinds = Counter(p['kind'] for p in self.data['products'])
        self.assertEqual(3, kinds['DISPLAY'])
        self.assertEqual(3, kinds['DOCK'] + kinds['HUB'])
        self.assertEqual(3, kinds['CABLE'] + kinds['ADAPTER'])

    def test_pending_and_partial_not_approved(self):
        self.assertTrue(all(f['review_status'] == 'PENDING_HUMAN_REVIEW' for f in self.data['facts']))
        apple = next(p for p in self.data['products'] if p['manufacturer'] == 'Apple')
        self.assertEqual('PARTIAL', apple['identity_status'])

    def test_property_payload_mismatch(self):
        self.fact('POWER_TRANSFER')['payload']['protocol'] = 'DISPLAYPORT'
        self.assertTrue(validate(self.data))

    def test_unknown_property(self):
        self.data['facts'][0]['property'] = 'FREE_TEXT_SPEC'
        self.assertTrue(validate(self.data))

    def test_missing_source_reference(self):
        self.data['products'][0]['source_refs'] = ['missing']
        self.assertTrue(validate(self.data))

    def test_wrong_product_binding(self):
        self.data['facts'][0]['product_id'] = self.data['products'][1]['product_id']
        self.assertTrue(validate(self.data))

    def test_duplicate_fact(self):
        self.data['facts'].append(copy.deepcopy(self.data['facts'][0]))
        self.assertTrue(validate(self.data))

    def test_bad_date(self):
        self.data['sources'][0]['accessed_at'] = '2026-02-30'
        self.assertTrue(validate(self.data))

    def test_nonofficial_url(self):
        self.data['sources'][0]['url'] = 'https://example.com/spec'
        self.assertTrue(validate(self.data))

    def test_none_is_not_power_offer(self):
        fact = next(f for f in self.data['facts'] if f['property'] == 'POWER_TRANSFER' and f['payload']['mode'] == 'NONE')
        fact['payload'].update(watts=100, rating_basis='UP_TO')
        self.assertTrue(validate(self.data))

    def test_power_rating_basis_required(self):
        self.fact('POWER_TRANSFER')['payload'].pop('rating_basis')
        self.assertTrue(validate(self.data))

    def test_transport_is_not_supply(self):
        fact = next(f for f in self.data['facts'] if f['product_id'] == 'product:apple-tb4-pro-cable' and f['property'] == 'POWER_TRANSFER')
        self.assertEqual('TRANSPORT_LIMIT', fact['payload']['mode'])

    def test_panel_is_not_port(self):
        self.assertEqual('PANEL', self.data['facts'][0]['payload']['scope'])
        self.assertEqual('UNKNOWN', self.data['facts'][0]['payload']['interface'])

    def test_incomplete_pixels(self):
        del self.data['facts'][0]['payload']['height']
        self.assertTrue(validate(self.data))

    def test_simultaneous_count_required(self):
        f = next(f for f in self.data['facts'] if f['property'] == 'VIDEO_PROFILE' and f['payload']['scope'] == 'SIMULTANEOUS')
        del f['payload']['display_count']
        self.assertTrue(validate(self.data))

    def test_port_specific_refresh_preserved(self):
        profiles = [f['payload'] for f in self.data['facts'] if f['product_id'] == 'product:dell-g2724d']
        self.assertEqual({'DISPLAYPORT':165, 'HDMI':144}, {p['interface']:p['refresh_hz'] for p in profiles})

    def test_usb_speed_not_video_payload(self):
        self.assertEqual('AGGREGATE_DATA', self.fact('LINK_MODE')['payload']['rate_scope'])

    def test_unknown_color_not_filled(self):
        self.assertTrue(all('color_depth_bits' not in f['payload'] for f in self.data['facts'] if f['property'] == 'VIDEO_PROFILE'))

    def test_driver_and_mst_constraints_retained(self):
        routes = {f['payload']['mechanism']:f['payload'] for f in self.data['facts'] if f['property']=='ROUTING'}
        self.assertEqual('YES', routes['DISPLAYLINK']['driver_required'])
        self.assertEqual(['macOS'], routes['MST']['excluded_os'])
        self.assertEqual(2, routes['DISPLAYLINK']['max_independent_displays'])

    def test_v1_cannot_preserve_typed_payload(self):
        schema = json.loads((ROOT / 'schemas/connection-path-v1.proposed.schema.json').read_text())
        cap = dict(id='probe', subject_id='probe-device', property='ROUTING',
                   claim_refs=['plugable-ud-6950h:1'], source_status='DIRECT_CHECK',
                   review_status='PENDING_HUMAN_REVIEW', conditions=[], value_label='DisplayLink',
                   payload=self.fact('ROUTING')['payload'])
        errors = check_value(cap, schema['properties']['capabilities']['items'], schema)
        self.assertTrue(any('payload: unknown field' in error for error in errors))

    def test_no_public_status_or_gold_answer(self):
        self.data['facts'][0]['public_status'] = 'COMPATIBLE'
        self.assertTrue(validate(self.data))
