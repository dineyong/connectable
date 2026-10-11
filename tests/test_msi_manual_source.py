import copy
import unittest
from scripts.validate_monitor_expansion import DATA, load, official

URL='https://download.msi.com/archive/mnu_exe/monitor/Modern_MD271ULv1.1_Korean.pdf'
class MsiManualSourceTests(unittest.TestCase):
    def candidate(self):
        data=load(DATA/'official_specs.json')
        p=next(p for p in data['products'] if p['display_model']=='Modern MD271UL')
        p['source_refs'][0]['url']=URL
        return data,p

    def test_exact_linked_manual_accepted(self):
        data,_=self.candidate();official(data)

    def test_other_paths_hosts_queries_and_models_rejected(self):
        for value in [URL+'?redirect=https://evil.test',URL+'#other',URL.replace('download.msi.com','download.msi.com.evil.test'),URL.replace('download.msi.com','download-2.msi.com'),URL.replace('v1.1','v1.2'),URL.replace('Modern_MD271UL','Other_Model'),URL.replace('https:','http:')]:
            with self.subTest(url=value):
                data,p=self.candidate();p['source_refs'][0]['url']=value
                with self.assertRaises(ValueError):official(data)
        for key,value in [('display_model','MPG 321URX QD-OLED'),('manufacturer','ASUS'),('id','monitor:other')]:
            with self.subTest(key=key):
                data,p=self.candidate();p[key]=value
                with self.assertRaises(ValueError):official(data)

    def test_brightness_does_not_approve_korean_sku_or_consumption(self):
        p=next(p for p in load(DATA/'official_specs.json')['products'] if p['display_model']=='Modern MD271UL')
        f=next(f for f in p['facts'] if f['property']=='brightness_typical')
        self.assertEqual((f['value'],f['unit']),(300,'nit'))
        self.assertIn('korean_sku_identity',p['missing_fields'])
        self.assertIn('warranty_korea',p['missing_fields'])
        self.assertIn('power_consumption',p['missing_fields'])
        self.assertEqual(p['region'],'Global')

    def test_mag_manual_exact_model_binding(self):
        link='https://download.msi.com/archive/mnu_exe/monitor/MAG_274QRF-QD-E2v1.1_Korean.pdf'
        data=load(DATA/'official_specs.json')
        p=next(p for p in data['products'] if p['display_model']=='MAG 274QRF QD E2')
        p['source_refs'][0]['url']=link
        official(data)
        for bad in [link+'?redirect=other',link.replace('v1.1','v1.2'),link.replace('download.msi.com','download-2.msi.com'),URL]:
            with self.subTest(url=bad):
                p['source_refs'][0]['url']=bad
                with self.assertRaises(ValueError):official(data)

    def test_mag_conflicts_and_conditions_do_not_promote_facts(self):
        from scripts import build_monitor_v3 as builder
        p=next(p for p in builder.build(builder.load(builder.SOURCE))['products'] if p['display_model']=='MAG 274QRF QD E2')
        gamut=next(f for f in p['facts'] if f['property']=='color_gamut')
        self.assertEqual(gamut['value']['DCI_P3'],98)
        self.assertTrue(any(n.startswith('CONFLICT_REVIEW ') and '95%' in n for n in p['notes']))
        self.assertTrue(any(n.startswith('CONFLICT_REVIEW ') and '13.3kg' in n for n in p['notes']))
        self.assertTrue(any('PIP/PBP 활성화' in n and 'Adaptive-Sync' in n for n in p['notes']))
        self.assertEqual(p['usable_for_compatibility'],'NO')
        for field in ('power_consumption','warranty_korea','korean_sku_identity','per_input_simultaneous_conditions'):
            self.assertIn(field,p['missing_fields'])

    def test_mpg_shared_manual_exact_model_binding(self):
        link='https://download.msi.com/archive/mnu_exe/monitor/MPG271QRX_321URX_QD-OLEDv1.1_Korean.pdf'
        data=load(DATA/'official_specs.json')
        p=next(p for p in data['products'] if p['display_model']=='MPG 321URX QD-OLED')
        p['source_refs'][0]['url']=link
        official(data)
        for bad in [link+'?redirect=other',link.replace('v1.1','v1.2'),link.replace('download.msi.com','download-2.msi.com'),URL]:
            with self.subTest(url=bad):
                p['source_refs'][0]['url']=bad
                with self.assertRaises(ValueError):official(data)

    def test_mpg_multisource_support_keeps_conditions_and_unknowns(self):
        from scripts import build_monitor_v3 as builder
        p=next(p for p in builder.build(builder.load(builder.SOURCE))['products'] if p['display_model']=='MPG 321URX QD-OLED')
        for prop in ('pip','pbp'):
            f=next(f for f in p['facts'] if f['property']==prop)
            self.assertIs(f['value'],True)
            self.assertEqual(f['source_refs'],['src:msi-mpg-321urx-qd-oled:manual-20261011'])
            self.assertNotIn(prop,p['missing_fields'])
        self.assertTrue(any('HDR' in n and 'PIP/PBP' in n for n in p['notes']))
        self.assertTrue(any('PIP/PBP 활성화' in n and 'Adaptive-Sync' in n for n in p['notes']))
        self.assertEqual(next(f['value'] for f in p['facts'] if f['property']=='refresh'),240)
        self.assertEqual(p['usable_for_compatibility'],'NO')
        for field in ('power_consumption','warranty_korea','korean_sku_identity','per_input_simultaneous_conditions'):
            self.assertIn(field,p['missing_fields'])
