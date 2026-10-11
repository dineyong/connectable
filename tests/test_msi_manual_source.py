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
