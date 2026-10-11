import unittest
from scripts import build_monitor_v3 as builder

class RemainingMonitorRecheck(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.products={p['display_model']:p for p in builder.build(builder.load(builder.SOURCE))['products']}

    def fact(self,model,prop):
        return next(f for f in self.products[model]['facts'] if f['property']==prop)

    def test_explicit_no_is_not_missing_feature(self):
        self.assertIs(self.products['27GP850-B']['filters']['usb_c_video'],False)
        self.assertIsNone(self.products['PA278QV']['filters']['usb_c_video'])
        for prop in ('pip','pbp'):
            self.assertIs(self.fact('27GP850-B',prop)['value'],False)
        self.assertIn('vesa',self.products['27GP850-B']['missing_fields'])

    def test_port_versions_do_not_upgrade_refresh(self):
        self.assertEqual(self.fact('27GP850-B','hdmi')['value']['version'],'2.0')
        self.assertEqual(self.fact('27GP850-B','displayport')['value']['version'],'1.4')
        self.assertEqual(self.products['27GP850-B']['filters']['refresh'],165)

    def test_units_stand_context_and_region_survive(self):
        w=self.fact('U2724D','weight')['value']
        self.assertEqual(w,{'unit':'lb','with_stand':14.46,'condition':'approximate'})
        self.assertEqual(self.fact('U2724D','warranty')['scope'],'US')
        self.assertIn('한국 보증 미확인',self.fact('U2724D','warranty')['value'])
        self.assertEqual(self.fact('27GP850-B','dimensions')['value']['with_stand']['height'],[465.9,575.9])

    def test_kvm_has_direct_model_specific_evidence(self):
        for model in ('MAG 274QRF QD E2','MPG 321URX QD-OLED'):
            f=self.fact(model,'kvm');self.assertIs(f['value'],True)
            sources={s['id']:s for s in self.products[model]['source_refs']}
            self.assertTrue(all(sources[r]['checked_on']=='2026-10-11' for r in f['source_refs']))
            self.assertTrue(all(sources[r]['access_status']=='DIRECT_CHECK' for r in f['source_refs']))

    def test_pd_conflict_does_not_become_96w_or_consumption(self):
        p=self.products['27UP850K-W']
        self.assertEqual(self.fact('27UP850K-W','pd_supply')['value'],90)
        self.assertTrue(any('CONFLICT_REVIEW' in n and '96W' in n for n in p['notes']))
        self.assertIn('power_consumption',p['missing_fields'])
        self.assertIn('kvm',p['missing_fields'])

    def test_all_approval_and_korean_sku_holds_remain(self):
        for p in self.products.values():
            self.assertEqual(p['review_status'],'PENDING_HUMAN_REVIEW')
            self.assertEqual(p['usable_for_compatibility'],'NO')
            self.assertIn('korean_sku_identity',p['missing_fields'])
            self.assertIn('warranty_korea',p['missing_fields'])
