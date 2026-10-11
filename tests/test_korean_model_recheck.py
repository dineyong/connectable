import unittest
from scripts import build_monitor_v3 as builder

class KoreanModelRecheck(unittest.TestCase):
    def test_korean_document_does_not_approve_foreign_sku(self):
        products={p['display_model']:p for p in builder.build(builder.load(builder.SOURCE))['products']}
        for model,region in [('PD2705U','CA'),('PA279CRV','US')]:
            p=products[model]
            self.assertEqual(p['region'],region)
            self.assertIn('korean_sku_identity',p['missing_fields'])
            self.assertIn('warranty_korea',p['missing_fields'])
            self.assertEqual(p['usable_for_compatibility'],'NO')
            self.assertEqual(p['review_status'],'PENDING_HUMAN_REVIEW')
            self.assertTrue(any('/ko-kr/' in s['url'] or '/kr/' in s['url'] for s in p['source_refs']))
        self.assertIn('vrr',products['PD2705U']['missing_fields'])
        self.assertIn('kvm',products['PA279CRV']['missing_fields'])

    def test_m28u_features_keep_simultaneous_conditions_unknown(self):
        p=next(p for p in builder.build(builder.load(builder.SOURCE))['products'] if p['display_model']=='M28U')
        f={f['property']:f for f in p['facts']}
        self.assertIs(f['pip']['value'],True);self.assertIs(f['pbp']['value'],True)
        self.assertEqual(f['vrr']['value'],'Adaptive-Sync')
        self.assertIn('per_input_simultaneous_conditions',p['missing_fields'])
        self.assertIn('pd_supply',p['missing_fields'])
        self.assertIn('usb_c.video_mode',p['missing_fields'])
        self.assertTrue(all(':kr-batch-20261011' in f[k]['source_refs'][0] for k in ('vrr','pip','pbp')))

    def test_second_batch_preserves_regions_and_partial_evidence(self):
        ps={p['display_model']:p for p in builder.build(builder.load(builder.SOURCE))['products']}
        for model,region in [('PD2725U','CA'),('GW2790QT','CA'),('VA24EHF','Global'),('VG27AQ','US'),('M32U','Global')]:
            p=ps[model]
            self.assertEqual(p['region'],region)
            self.assertIn('korean_sku_identity',p['missing_fields'])
            self.assertIn('warranty_korea',p['missing_fields'])
            self.assertEqual(p['usable_for_compatibility'],'NO')
            self.assertTrue(any(':kr-batch2-20261011' in s['id'] for s in p['source_refs']))
        self.assertIn('usb_c',ps['PD2725U']['missing_fields'])
        self.assertIn('hdr',ps['GW2790QT']['missing_fields'])
        p=ps['M32U'];vrr=next(f for f in p['facts'] if f['property']=='vrr')
        self.assertEqual(vrr['value'],'Adaptive-Sync')
        self.assertIn('usb_c.video_mode',p['missing_fields'])
        self.assertIn('pd_supply',p['missing_fields'])
