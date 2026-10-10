"""Regression checks for conservative monitor display derivation."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import build_monitor_v3 as builder


class MonitorV3Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = builder.load(builder.SOURCE)

    def test_preserves_every_original_fact_and_product_field(self):
        before = copy.deepcopy(self.source)
        result = builder.build(self.source)
        self.assertEqual(self.source, before)
        self.assertEqual(len(result['products']), 30)
        for original, derived in zip(self.source['products'], result['products']):
            self.assertEqual(original, {key: derived[key] for key in original})
            self.assertEqual(derived['review_status'], 'PENDING_HUMAN_REVIEW')
            self.assertEqual(derived['usable_for_compatibility'], 'NO')
        self.assertEqual(result['public_status'], 'UNKNOWN')

    def test_rejects_invalid_source_before_generation(self):
        for mutate in (
            lambda s: s.update(public_status='APPROVED'),
            lambda s: s['products'][0]['facts'][0].update(source_refs=['missing']),
            lambda s: s['products'][0]['source_refs'][0].update(url='https://www.asus.com.example.org/'),
        ):
            source = copy.deepcopy(self.source)
            mutate(source)
            with self.assertRaises(ValueError):
                builder.build(source)

    def fact(self, prop='refresh', value=144, unit='Hz', scope='PANEL', qualifier='MANUFACTURER_STATED'):
        return dict(id='fact:test', property=prop, value=value, unit=unit, scope=scope, qualifier=qualifier)

    def test_exact_units_scope_and_positive_non_boolean_numeric_values(self):
        for changes in ({'unit': 'kHz'}, {'scope': 'HDMI'}, {'value': True},
                        {'value': '144'}, {'value': 0}, {'value': -1}, {'value': float('inf')},
                        {'qualifier': 'UNKNOWN'}):
            fact = self.fact()
            fact.update(changes)
            self.assertEqual(builder.select_filter([fact], 'refresh'), (None, []))

    def test_conflicting_values_are_unknown(self):
        self.assertEqual(builder.select_filter([self.fact(), self.fact(value=165)], 'refresh'), (None, []))

    def test_matching_values_retain_all_evidence(self):
        second = self.fact()
        second['id'] = 'fact:second'
        self.assertEqual(builder.select_filter([self.fact(), second], 'refresh'), (144, ['fact:test', 'fact:second']))

    def test_native_resolution_requires_integer_pixels(self):
        self.assertEqual(builder.select_filter([self.fact('width', 3840.5, 'px', 'NATIVE_RESOLUTION')], 'width'), (None, []))

    def test_usb_c_connector_data_power_or_thunderbolt_never_imply_video(self):
        for value in ({'count': 1}, {'data': True}, {'pd': 90}, {'mode': 'DisplayPort maybe'},
                      {'video_mode': None}, {'data_only_upstream': 1}, True):
            self.assertEqual(builder.select_filter([self.fact('usb_c', value, None, 'PORT')], 'usb_c_video'), (None, []))
        self.assertEqual(builder.select_filter([self.fact('thunderbolt', {'upstream_video_data': 1}, None, 'PORT')], 'usb_c_video'), (None, []))

    def test_explicit_usb_c_video_and_explicit_absence(self):
        for mode in builder.VIDEO_MODES:
            self.assertEqual(builder.select_filter([self.fact('usb_c', {'mode': mode}, None, 'PORT')], 'usb_c_video'), (True, ['fact:test']))
        self.assertEqual(builder.select_filter([self.fact('usb_c', False, None, 'PORT')], 'usb_c_video'), (False, ['fact:test']))

    def test_usb_c_conflicting_evidence_is_unknown(self):
        facts = [self.fact('usb_c', False, None, 'PORT'), self.fact('usb_c', {'mode': 'DP Alt Mode'}, None, 'PORT')]
        self.assertEqual(builder.select_filter(facts, 'usb_c_video'), (None, []))

    def test_real_port_frequency_does_not_become_panel_refresh(self):
        products = {p['id']: p for p in builder.build(self.source)['products']}
        self.assertIsNone(products['monitor:asus-xg27aqdmg']['filters']['refresh'])
        self.assertIsNone(products['monitor:asus-pg32ucdm']['filters']['refresh'])
        self.assertEqual(products['monitor:gigabyte-m28u']['filters']['refresh'], 144)
        self.assertIsNone(products['monitor:gigabyte-m28u']['filters']['usb_c_video'])
        self.assertTrue(products['monitor:asus-pa279crv']['filters']['usb_c_video'])

    def test_derived_filter_refs_exist_in_local_product(self):
        for product in builder.build(self.source)['products']:
            ids = {fact['id'] for fact in product['facts']}
            for key, refs in product['filter_fact_refs'].items():
                self.assertLessEqual(set(refs), ids)
                self.assertEqual(bool(refs), product['filters'][key] is not None)

    def test_serialization_is_deterministic_and_js_matches_json(self):
        raw, js = builder.serialized(self.source)
        self.assertEqual((raw, js), builder.serialized(self.source))
        self.assertEqual(json.loads(raw), json.loads(js.split('window.CONNECTABLE_MONITORS = ', 1)[1].rstrip(';\n')))

    def test_script_breakout_source_text_is_escaped(self):
        source = copy.deepcopy(self.source)
        source['products'][0]['notes'].append('</script><script>alert(1)</script>')
        raw, js = builder.serialized(source)
        self.assertNotIn('</script>', js)
        self.assertIn('</script>', raw)

    def test_check_detects_stale_missing_and_byte_changed_outputs(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / 'monitor.json'
            script = Path(folder) / 'monitor.js'
            # Use in-repository-looking paths only for CLI diagnostic relative paths.
            with patch.object(builder, 'ROOT', Path(folder)), patch.object(builder, 'SOURCE', Path(folder) / 'source.json'), patch.object(builder, 'JSON_OUTPUT', output), patch.object(builder, 'JS_OUTPUT', script):
                builder.SOURCE.write_text(json.dumps(self.source), encoding='utf-8')
                self.assertEqual(builder.main(['--check']), 1)
                self.assertEqual(builder.main([]), 0)
                self.assertEqual(builder.main(['--check']), 0)
                output.write_text('{}\n', encoding='utf-8')
                self.assertEqual(builder.main(['--check']), 1)

    def test_real_generated_files_are_current(self):
        self.assertEqual(builder.main(['--check']), 0)


if __name__ == '__main__':
    unittest.main()
