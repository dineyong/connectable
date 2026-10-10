import copy
import unittest
from scripts.validate_monitor_expansion import DATA,load,official,community,market,validate_all

class MonitorExpansionTests(unittest.TestCase):
    def test_real_batches(self):validate_all()
    def test_original_batches_not_mutated(self):
        for name,validator in [('official_specs.json',official),('community_reviews.json',community),('market_signals.json',market)]:
            data=load(DATA/name);before=copy.deepcopy(data);validator(data);self.assertEqual(data,before)
    def test_wrong_manufacturer_domain(self):
        data=load(DATA/'official_specs.json');data['products'][0]['source_refs'][0]['url']='https://www.asus.com.evil.test/model'
        with self.assertRaises(ValueError):official(data)
    def test_missing_fact_evidence(self):
        data=load(DATA/'official_specs.json');data['products'][0]['facts'][0]['source_refs']=[]
        with self.assertRaises(ValueError):official(data)
    def test_stale_source_origin(self):
        data=load(DATA/'official_specs.json');data['products'][0]['source_refs'][0]['access_status']='ACCESS_FAILED'
        with self.assertRaises(ValueError):official(data)
    def test_duplicate_model_id(self):
        data=load(DATA/'official_specs.json');data['products'].append(copy.deepcopy(data['products'][0]))
        with self.assertRaises(ValueError):official(data)
    def test_duplicate_review_url(self):
        data=load(DATA/'community_reviews.json');r=copy.deepcopy(data['reviews'][0]);r['id']='unique-but-same-url';data['reviews'].append(r)
        with self.assertRaises(ValueError):community(data)
    def test_cross_model_review_ref(self):
        data=load(DATA/'community_reviews.json');data['classifications'][0]['display_model']='WRONG MODEL'
        with self.assertRaises(ValueError):community(data)
    def test_single_positive_not_highly_reviewed(self):
        data=load(DATA/'community_reviews.json');c=data['classifications'][0];c['label']='POSITIVE_REVIEW_CANDIDATE';c['review_refs']=c['review_refs'][:1]
        with self.assertRaises(ValueError):community(data)
    def test_relative_index_cannot_be_absolute(self):
        data=load(DATA/'market_signals.json');data['signals'][0]['is_proxy']=False
        with self.assertRaises(ValueError):market(data)
    def test_no_sales_label_from_search_index(self):
        data=load(DATA/'market_signals.json');data['classifications'][0]['label']='PURCHASE_INTEREST_CANDIDATE'
        with self.assertRaises(ValueError):market(data)
    def test_market_model_ref_mismatch(self):
        data=load(DATA/'market_signals.json');data['classifications'][0]['display_model']='WRONG MODEL'
        with self.assertRaises(ValueError):market(data)
    def test_no_compatibility_promotion(self):
        data=load(DATA/'community_reviews.json');data['reviews'][0]['usable_for_compatibility']='YES'
        with self.assertRaises(ValueError):community(data)
    def test_bad_date_and_private_info(self):
        data=load(DATA/'official_specs.json');data['checked_on']='2026-02-30'
        with self.assertRaises(ValueError):official(data)
        data=load(DATA/'community_reviews.json');data['reviews'][0]['summary']='contact@example.com'
        with self.assertRaises(ValueError):community(data)

if __name__=='__main__':unittest.main()
