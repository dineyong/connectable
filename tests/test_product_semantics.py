import copy
import unittest
from scripts.build_site_content_v2 import build
from scripts.site_content_validation import validate_content
from scripts.product_semantics import inspect_fact, validate_semantics


class ProductSemanticTests(unittest.TestCase):
    def test_real_profile_mutation_is_rejected(self):
        d = build()
        d['monitors'][2]['features'][0]['payload']['refresh_hz'] = 144
        with self.assertRaises(ValueError):
            validate_content(d)

    def test_real_power_mutation_is_rejected(self):
        d = build()
        d['monitors'][0]['features'][2]['summary'] = '영상용 USB-C upstream에서 최대 15W 공급'
        with self.assertRaises(ValueError):
            validate_content(d)

    def test_real_protocol_version_mutation_is_rejected(self):
        d = build()
        d['monitors'][0]['features'][1]['payload']['version'] = '1.2'
        with self.assertRaises(ValueError):
            validate_content(d)

    def test_real_port_role_mutation_is_rejected(self):
        d = build()
        d['monitors'][0]['features'][3]['payload']['interface'] = 'USB_C_VIDEO_UPSTREAM'
        with self.assertRaises(ValueError):
            validate_content(d)

    def test_resolution_scope_and_dimensions(self):
        for field, value in [('width', 2560), ('height', 1440), ('scope', 'PORT')]:
            d = build()
            d['monitors'][0]['features'][0]['payload'][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_content(d)

    def test_port_functions_and_delivery_roles(self):
        for field, value in [('mode', 'TRANSPORT_LIMIT'), ('rating_basis', 'RATED')]:
            d = build()
            d['monitors'][0]['features'][2]['payload'][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_content(d)
        d = build()
        d['monitors'][3]['features'][3]['payload']['interfaces'].pop()
        with self.assertRaises(ValueError):
            validate_content(d)

    def test_negation_quotes_and_multiple_values_are_manual(self):
        f = copy.deepcopy(build()['monitors'][0]['features'][2])
        for text in ['최대 90W 공급이 아니다', '"영상용 USB-C upstream에서 최대 15W 공급"은 잘못된 설명', '90W 공급 / 실제 측정 15W', '영상용 USB-C upstream에서 최대 15W 공급이라는 주장 미확인']:
            f['summary'] = text
            with self.subTest(text=text):
                self.assertEqual(inspect_fact(f)['status'], 'MANUAL_REVIEW')
                validate_semantics(f, 'test')

    def test_unknown_is_manual_not_inferred(self):
        f = copy.deepcopy(build()['monitors'][0]['features'][2])
        f['payload']['watts'] = 'UNKNOWN'
        self.assertEqual(inspect_fact(f)['status'], 'MANUAL_REVIEW')
        self.assertEqual(f['payload']['watts'], 'UNKNOWN')

    def test_no_4k_or_pd_label_conversion(self):
        d = build()
        for f in [d['monitors'][3]['features'][0], d['monitors'][4]['features'][1]]:
            before = copy.deepcopy(f)
            self.assertEqual(inspect_fact(f)['status'], 'MANUAL_REVIEW')
            self.assertEqual(f, before)

    def test_bare_pd_label_does_not_establish_rating_or_direction(self):
        f = copy.deepcopy(build()['monitors'][1]['features'][2])
        f['payload']['rating_basis'] = 'UP_TO'
        f['payload']['mode'] = 'TRANSPORT_LIMIT'
        result = inspect_fact(f)
        self.assertFalse(result['conflicts'])
        self.assertNotIn('mode', result['checked_fields'])
        self.assertNotIn('rating_basis', result['checked_fields'])

    def test_decimal_hz_and_different_interfaces(self):
        f = copy.deepcopy(build()['monitors'][2]['features'][0])
        f['summary'] = 'DisplayPort에서 2560×1440 59.94Hz'
        f['payload']['refresh_hz'] = 59.94
        self.assertEqual(inspect_fact(f)['status'], 'CONSISTENT_EXPLICIT_FIELDS')
        f['payload']['interface'] = 'HDMI'
        with self.assertRaises(ValueError):
            validate_semantics(f, 'test')

    def test_actual_data_has_no_conflicts_and_remains_read_only(self):
        d = build()
        before = copy.deepcopy(d)
        results = [inspect_fact(f) for m in d['monitors'] for f in m['features']]
        self.assertEqual(len(results), 29)
        self.assertEqual(sum(r['status'] == 'MANUAL_REVIEW' for r in results), 2)
        self.assertFalse(any(r['conflicts'] for r in results))
        self.assertEqual(d, before)


if __name__ == '__main__':
    unittest.main()
