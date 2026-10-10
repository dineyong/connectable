import copy
import tempfile
import unittest
from pathlib import Path
from scripts.validate_quasarzone_intake import TARGET, load, validate

class QuasarzoneIntakeTests(unittest.TestCase):
    def setUp(self): self.data = load(TARGET)
    def rejects(self, mutate):
        mutate(self.data)
        with self.assertRaises(ValueError): validate(self.data)
    def test_real_intake(self): self.assertTrue(validate(self.data))
    def test_public_promotion(self): self.rejects(lambda d: d.update(public_status='APPROVED'))
    def test_candidate_promotion(self): self.rejects(lambda d: d['candidates'][0].update(identity_status='EXACT'))
    def test_auto_equivalence(self): self.rejects(lambda d: d['candidates'][0]['official_mapping_candidates'][0].update(uncertain=False))
    def test_dangling_reference(self): self.rejects(lambda d: d['candidates'][0]['source_refs'].append('missing'))
    def test_duplicate_id(self): self.rejects(lambda d: d['candidates'][1].update(id=d['candidates'][0]['id']))
    def test_fake_direct_access(self):
        s = next(s for s in self.data['sources'] if s['access_status']=='NOT_RECHECKED')
        s['access_status']='DIRECT_CHECK'
        with self.assertRaises(ValueError): validate(self.data)
    def test_false_direct_scope(self):
        s = next(s for s in self.data['sources'] if s['access_status']=='DIRECT_CHECK')
        s['direct_check']['result']='All facts verified'
        with self.assertRaises(ValueError): validate(self.data)
    def test_host_spoof(self): self.rejects(lambda d: d['sources'][0].update(url='https://quasarzone.com.evil.test/a'))
    def test_encoded_control(self): self.rejects(lambda d: d['sources'][0].update(url='https://quasarzone.com/a%0A'))
    def test_credentials(self): self.rejects(lambda d: d['sources'][0].update(url='https://user:pass@quasarzone.com/a'))
    def test_current_price_copy(self): self.rejects(lambda d: d['candidates'][0].update(current_price=100))
    def test_pii_copy(self): self.rejects(lambda d: d['candidates'][0].update(email='example@example.com'))
    def test_full_path_copy(self): self.rejects(lambda d: d['originals'][0].update(basename='/Downloads/file.json'))
    def test_catalog_promotion(self):
        c = next(c for c in self.data['candidates'] if c['section']=='CATALOG_INDEX');c['index_only']=False
        with self.assertRaises(ValueError):validate(self.data)
    def test_counts_mismatch(self): self.rejects(lambda d: d['statistics'].update(detailed_models=594))
    def test_unsafe_json(self):
        for content in ['{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}']:
            with tempfile.TemporaryDirectory() as t:
                p=Path(t)/'x.json';p.write_text(content)
                with self.assertRaises(ValueError):load(p)

if __name__=='__main__':unittest.main()
