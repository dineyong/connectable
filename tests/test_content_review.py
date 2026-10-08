import copy
import json
import unittest
from scripts.content_review import ROOT, REVIEW, LEDGER, project, validate_ledger, digest

class ContentReviewTests(unittest.TestCase):
    def setUp(self):
        self.site = json.loads((ROOT/'data/site/content-v2.json').read_text())
        self.batch = json.loads(REVIEW.read_text())
        self.monitors = copy.deepcopy(self.site['monitors'])

    def test_projection_partial_fields_and_original_preserved(self):
        before = copy.deepcopy(self.monitors)
        project(self.monitors,self.batch)
        for m, old in zip(self.monitors,before):
            for f, original in zip(m['features'],old['features']):
                self.assertEqual(f['payload'], original['payload'])
                self.assertEqual(f['summary'], original['summary'])
        partial = [f['field_review'] for m in self.monitors for f in m['features'] if f['field_review']['status']=='PARTIALLY_VERIFIED']
        self.assertEqual(len(partial),2)
        self.assertEqual(partial[1]['verified_fields'],['label'])
        self.assertIn('watts',partial[1]['unverified_fields'])

    def test_lg_equal_numbers_not_merged_or_sku_promoted(self):
        project(self.monitors,self.batch)
        m=next(m for m in self.monitors if m['id']=='product:lg-27up850-w')
        f=next(f for f in m['features'] if f['property']=='POWER_TRANSFER')
        a=m['separate_spec_reviews'][0]
        self.assertEqual(f['payload']['rating_basis'],'RATED')
        self.assertEqual(a['payload']['rating_basis'],'UP_TO')
        self.assertEqual(a['variant_match'],'UNKNOWN')
        self.assertEqual(a['sources'][0]['region'],'LV')

    def record(self):
        f=self.site['monitors'][0]['features'][0]
        return {'id':'test-only','target_fact_id':f['fact_id'],'target_sha256':digest(f),'reviewer_id':'reviewer:test','reviewed_on':'2026-10-09','result':'EVIDENCE_SUFFICIENT','source_refs':f['source_refs'],'notes':'Synthetic test record; not saved','public_status':'UNKNOWN','usable_for_compatibility':'NO'}

    def check(self,r):
        return validate_ledger({'schema_version':1,'public_status':'UNKNOWN','records':[r]})

    def test_record_does_not_approve_and_real_ledger_empty(self):
        self.check(self.record())
        self.assertEqual(validate_ledger(json.loads(LEDGER.read_text()))['records'],[])

    def test_invalid_reviews_rejected(self):
        for k,v in [('reviewer_id',''),('reviewed_on','2026-02-30'),('source_refs',[]),('source_refs',['other-model']),('target_sha256','0'*64),('target_fact_id','missing'),('notes',''),('result','APPROVED'),('public_status','COMPATIBLE'),('usable_for_compatibility','YES')]:
            with self.subTest(field=k,value=v):
                r=self.record();r[k]=v
                with self.assertRaises(ValueError): self.check(r)

    def test_duplicate_id_and_unknown_fields_rejected(self):
        r=self.record()
        with self.assertRaises(ValueError): validate_ledger({'schema_version':1,'public_status':'UNKNOWN','records':[r,r]})
        r['approved']=True
        with self.assertRaises(ValueError): self.check(r)

    def test_tampered_partial_batch_rejected(self):
        self.batch['manual_reviews'][1]['verified_fields'].append('watts')
        with self.assertRaises(ValueError): project(self.monitors,self.batch)
