import unittest
from scripts import build_monitor_v3 as builder

class ResearchFollowupTests(unittest.TestCase):
    def product(self, model):
        return next(p for p in builder.build(builder.load(builder.SOURCE))['products'] if p['display_model']==model)

    def test_adaptive_sync_is_not_a_refresh_range_or_sku_approval(self):
        for model in ('Modern MD271UL', 'M27Q rev.1.0'):
            with self.subTest(model=model):
                p=self.product(model)
                f=next(f for f in p['facts'] if f['property']=='vrr')
                self.assertEqual(f['value'],'Adaptive-Sync')
                self.assertIn('korean_sku_identity',p['missing_fields'])
                self.assertEqual(p['usable_for_compatibility'],'NO')
                self.assertEqual(p['region'],'Global')

    def test_md_weight_conflict_preserves_original_values(self):
        p=self.product('Modern MD271UL')
        self.assertEqual(next(f['value'] for f in p['facts'] if f['property']=='weight'),{'unit':'kg','net':5.75,'gross':7.35})
        self.assertTrue(any(n.startswith('CONFLICT_REVIEW ') and '5.3' in n and '7.4' in n for n in p['notes']))
        self.assertIn('power_consumption',p['missing_fields'])

    def test_korean_product_page_is_not_exact_sales_sku_or_pd_evidence(self):
        for model in ('M28U','M32U'):
            with self.subTest(model=model):
                p=self.product(model)
                self.assertTrue(any(s['url']==f'https://www.gigabyte.com/kr/Monitor/{model}' for s in p['source_refs']))
                self.assertIn('korean_sku_identity',p['missing_fields'])
                self.assertIn('pd_supply',p['missing_fields'])
                self.assertIn('usb_c.video_mode',p['missing_fields'])
                self.assertEqual(p['region'],'Global')
