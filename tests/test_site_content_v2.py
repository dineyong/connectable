import copy
import hashlib
import json
import re
import unittest
from scripts.build_site_content_v2 import ROOT, OUTPUT, INPUTS, BATCH_PATH, build, serialize, read, validate_monitor_batch

class SiteContentV2Tests(unittest.TestCase):
    def setUp(self):
        self.data = build()

    def test_reproducible_and_read_only(self):
        before = {p: (ROOT/p).read_bytes() for p in INPUTS}
        self.assertEqual(OUTPUT.read_text(encoding='utf-8'), serialize(build()))
        for p, contents in before.items():
            self.assertEqual(contents, (ROOT/p).read_bytes())
        for record in self.data['provenance']:
            self.assertEqual(record['sha256'], hashlib.sha256(before[record['path']]).hexdigest())

    def test_contract_and_source_references(self):
        self.assertEqual(self.data['schema_version'], '2')
        ids = [r['id'] for key in ('monitors','reviews','guides') for r in self.data[key]]
        self.assertEqual(len(ids), len(set(ids)))
        monitor_ids={m['id'] for m in self.data['monitors']}
        review_ids={r['id'] for r in self.data['reviews']}
        for key in ('monitors','reviews','guides'):
            for item in self.data[key]:
                for field in ('id','title','source_refs','review_status'):
                    self.assertTrue(item[field])
                for ref in item['source_refs']:
                    self.assertTrue(ref['url'].startswith('https://'))
                    self.assertTrue((ROOT/ref['source_file']).is_file())
                self.assertTrue(set(item.get('monitor_ids',item.get('related_monitor_ids',[]))) <= monitor_ids)
                self.assertTrue(set(item.get('related_review_ids',[])) <= review_ids)

    def test_review_projection_and_privacy(self):
        self.assertEqual(len(self.data['reviews']), 38)
        originals={r['id']: r for r in read(INPUTS[4])}
        originals.update({r['id']: r['mapping'] for r in read(INPUTS[3])})
        for review in self.data['reviews']:
            original=originals[review['id']]
            self.assertEqual(review['observations'], original['observations'])
            self.assertEqual(review['commercial_context'], original['review']['commercial_context'])
            self.assertEqual(review['public_status'],'UNKNOWN')
            self.assertEqual(review['usable_for_compatibility'],'NO')
            self.assertEqual(review['source_refs'][0]['url'], original['source']['source_url'])
            self.assertEqual(original['source']['public_access'],'YES')
        text=serialize(self.data)
        self.assertIsNone(re.search(r'(?i)(sk-[a-z0-9]{20,}|-----BEGIN .*PRIVATE KEY|[\w.+-]+@[\w.-]+\.[a-z]{2,}|010[- ]?\d{4}[- ]?\d{4})',text))
        for forbidden in ('nickname','email','username','author_name','access_token'):
            self.assertNotIn('"'+forbidden+'":',text)

    def test_official_features_not_user_or_ad_claims(self):
        pilot=read(INPUTS[0])
        self.assertEqual(len(self.data['monitors']),6)
        for monitor in self.data['monitors']:
            self.assertEqual(monitor['public_status'],'UNKNOWN')
            self.assertEqual(monitor['price'],'UNKNOWN')
            self.assertEqual(monitor['rating'],'UNKNOWN')
            for feature in monitor['features']:
                self.assertEqual(feature['basis'],'MANUFACTURER_SPEC')
                source=next(f for f in pilot['facts'] + read(BATCH_PATH)['facts'] if f['fact_id']==feature['fact_id'])
                self.assertEqual(feature,dict(source,basis='MANUFACTURER_SPEC'))

    def test_original_source_and_content_preservation(self):
        manifest = read('data/site/monitor-batch-1-preservation.json')
        for path, expected in manifest['source_hashes'].items():
            self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(), expected, path)
        def digest(value):
            return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',',':')).encode()).hexdigest()
        for monitor in self.data['monitors'][:3]:
            self.assertEqual(digest(monitor), manifest['existing_monitors'][monitor['id']])
        for review in self.data['reviews']:
            value = copy.deepcopy(review)
            value.pop('monitor_links', None)
            value['monitor_ids'] = []
            value['source_refs'] = value['source_refs'][:1]
            self.assertEqual(digest(value), manifest['existing_reviews'][review['id']])

    def test_exact_links_and_deferred_variant(self):
        linked={r['id']: r['monitor_ids'] for r in self.data['reviews'] if r['monitor_ids']}
        self.assertEqual(linked, {'PUR-001':['product:jooyon-v32ue'],
                                 'PUR-005':['product:crossover-27uld950'],
                                 'PUR-006':['product:crossover-27uld950'],
                                 'PUR-014':['product:msi-md271ul']})
        self.assertEqual(read(BATCH_PATH)['deferred_candidates'][0]['status'], 'DEFERRED_VARIANT_UNKNOWN')
        for review in self.data['reviews']:
            for link in review.get('monitor_links', []):
                self.assertEqual(link['variant_match'],'UNKNOWN')
                self.assertEqual(link['match_scope'],'MODEL_ONLY')

    def test_reject_similar_model_and_other_post(self):
        batch=read(BATCH_PATH)
        batch['review_links'][0]['reported_model']='주연테크 V32UE-E'
        with self.assertRaises(ValueError): validate_monitor_batch(batch,self.data['reviews'])
        batch=read(BATCH_PATH)
        batch['review_links'][0]['source_refs']=['SITE-CHECK-PUR-006']
        with self.assertRaises(ValueError): validate_monitor_batch(batch,self.data['reviews'])
        batch=read(BATCH_PATH)
        batch['review_links'][0]['monitor_id']='product:msi-md271ul'
        with self.assertRaises(ValueError): validate_monitor_batch(batch,self.data['reviews'])

    def test_reject_unchecked_and_user_spec_evidence(self):
        batch=read(BATCH_PATH)
        batch['sources'][0]['source_status']='SEARCH_SNIPPET'
        with self.assertRaises(ValueError): validate_monitor_batch(batch,self.data['reviews'])
        batch=read(BATCH_PATH)
        batch['facts'][0]['source_refs']=['SITE-CHECK-PUR-001']
        with self.assertRaises(ValueError): validate_monitor_batch(batch,self.data['reviews'])
        batch=read(BATCH_PATH)
        batch['products'][0]['review_status']='APPROVED'
        with self.assertRaises(ValueError): validate_monitor_batch(batch,self.data['reviews'])

    def test_official_unknowns_stay_separate_from_observations(self):
        monitors={m['id']:m for m in self.data['monitors']}
        cross=monitors['product:crossover-27uld950']
        self.assertEqual(cross['capabilities']['usb_c_video']['status'],'UNKNOWN')
        power=next(f for f in cross['features'] if f['property']=='POWER_TRANSFER')
        self.assertEqual(power['payload']['watts'],'UNKNOWN')
        self.assertEqual(cross['capabilities']['kvm']['status'],'CONFIRMED_MANUFACTURER_STATEMENT')
        for mid in ('product:jooyon-v32ue','product:msi-md271ul'):
            self.assertEqual(monitors[mid]['capabilities']['height_adjustment']['status'],'UNKNOWN')
        for review in self.data['reviews']:
            for f in review['functional_observations']:
                self.assertEqual(f['signal_mode']['resolution_pixels'],'UNKNOWN')
                self.assertEqual(f['pd']['watts'],'UNKNOWN')

    def test_batch_fact_and_capability_references(self):
        batch=read(BATCH_PATH)
        sources=validate_monitor_batch(batch,self.data['reviews'])
        for monitor in self.data['monitors'][3:]:
            features={f['fact_id']:f for f in monitor['features']}
            for capability in monitor['capabilities'].values():
                self.assertTrue(set(capability['feature_refs']) <= set(features))
            for feature in features.values():
                self.assertTrue(set(feature['source_refs']) <= set(sources))
                self.assertTrue(feature['location'])
                self.assertEqual(feature['source_status'],'DIRECT_CHECK')

if __name__=='__main__': unittest.main()
