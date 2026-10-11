import unittest
from scripts import build_monitor_v3 as builder

class AsusRecheck(unittest.TestCase):
    def test_core_values_and_original_input_limits_remain_separate(self):
        result = builder.build(builder.load(builder.SOURCE))
        products = {p['display_model']:p for p in result['products']}
        x = products['XG27AQDMG']; pg = products['PG32UCDM']
        self.assertEqual(x['filters']['size'],26.5)
        self.assertEqual(pg['filters']['panel'],'QD-OLED')
        for p in (x,pg):
            self.assertEqual(p['filters']['refresh'],240)
            self.assertIn('korean_sku_identity',p['missing_fields'])
            self.assertIn('warranty_korea',p['missing_fields'])
            self.assertEqual(p['review_status'],'PENDING_HUMAN_REVIEW')
            self.assertEqual(p['usable_for_compatibility'],'NO')
            refs=p['filter_fact_refs']['refresh']
            facts=[f for f in p['facts'] if f['id'] in refs]
            self.assertTrue(all(f['scope']=='PANEL' and 'overview' in f['source_refs'][0] for f in facts))
        self.assertEqual(next(f['value']['max'] for f in x['facts'] if f['property']=='input_vertical_frequency' and f['scope']=='HDMI'),144)
        pd=next(f for f in pg['facts'] if f['property']=='pd_supply')
        self.assertIn('65W',pd['location']); self.assertIn('OSD',pd['location'])
        self.assertEqual(pd['value'],90)
