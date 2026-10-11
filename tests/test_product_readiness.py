import json
import unittest
from scripts.build_product_readiness import build, SOURCE, OUTPUT


class ReadinessTests(unittest.TestCase):
    def test_checked_in_inventory_matches_all_products(self):
        raw = SOURCE.read_bytes()
        result = build(raw)
        self.assertEqual(result, OUTPUT.read_text())
        for product in json.loads(raw)['products']:
            self.assertIn('`'+product['id']+'`', result)
            for source in product['source_refs']:
                self.assertIn(source['url'], result)

    def test_unknown_is_not_missing_when_false_or_zero(self):
        data = json.loads(SOURCE.read_bytes())
        data['products'] = data['products'][:1]
        data['products'][0]['filters'].update(usb_c_video=False, refresh=0)
        result = build(json.dumps(data).encode())
        row = next(line for line in result.splitlines() if line.startswith('| `monitor:'))
        self.assertNotIn('USB-C 영상', row)
        self.assertNotIn('주사율', row)
        data['products'][0]['filters']['refresh'] = None
        result = build(json.dumps(data).encode())
        row = next(line for line in result.splitlines() if line.startswith('| `monitor:'))
        self.assertIn('주사율', row)
