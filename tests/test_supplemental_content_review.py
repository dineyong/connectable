"""Synthetic reviewer fixtures stay in tests; shipped ledger must stay empty."""
import copy
import unittest
from scripts.supplemental_content_review import LEDGER, PATH, ROOT, REMAINING, load, validate, digest


class SupplementalContentReviewTests(unittest.TestCase):
    def setUp(self):
        batch = load(PATH)
        self.data = load(LEDGER)
        self.record = {
            'id':'supp-review:test-only', 'target_batch_id':batch['batch_id'],
            'target_assertion_id':batch['assertion']['assertion_id'],
            'evidence_batch_sha256':digest(batch),
            'related_fact_sha256':batch['original_fact_sha256'],
            'capture_sha256':batch['asset']['capture_sha256'],
            'reviewer_id':'reviewer:test-fixture', 'reviewed_on':'2026-10-09',
            'result':'PARTIALLY_VERIFIED',
            'evidence_refs':[batch['source']['source_id'],batch['asset']['asset_id']],
            'reviewed_fields':['watts'], 'remaining_unknowns':sorted(REMAINING),
            'notes':'Synthetic fixture; not a real review or approval.',
            'public_status':'UNKNOWN', 'usable_for_compatibility':'NO',
        }
        self.data['records'] = [self.record]

    def reject(self):
        with self.assertRaises(ValueError): validate(self.data)

    def test_shipped_ledger_empty_and_validation_read_only(self):
        original = load(LEDGER)
        self.assertEqual(original['records'], [])
        before = copy.deepcopy(self.data)
        paths = [LEDGER, PATH, ROOT/'data/review/content_reviews.json', ROOT/'data/site/content-v2.json']
        contents = {p:p.read_bytes() for p in paths}
        validate(self.data)
        self.assertEqual(self.data, before)
        for p, content in contents.items(): self.assertEqual(p.read_bytes(), content)

    def test_results_preserve_public_hold(self):
        for result in ['NEEDS_REVIEW','PARTIALLY_VERIFIED','REJECTED','EVIDENCE_SUFFICIENT']:
            self.record['result'] = result
            self.record['reviewed_fields'] = ['mode','watts','rating_basis']
            self.assertEqual(validate(self.data)['records'][0]['public_status'], 'UNKNOWN')

    def test_stale_hashes_rejected(self):
        for key in ['evidence_batch_sha256','related_fact_sha256','capture_sha256']:
            data = copy.deepcopy(self.data)
            data['records'][0][key] = '0'*64
            with self.assertRaises(ValueError): validate(data)

    def test_wrong_target(self):
        self.record['target_assertion_id'] = 'SR-LG-PD'
        self.reject()

    def test_wrong_or_incomplete_evidence(self):
        for refs in [[], ['CROSS-PD-PAGE'], ['CROSS-PD-PAGE','OTHER'], ['CROSS-PD-PAGE','CROSS-PD-IMAGE','CROSS-PD-IMAGE']]:
            self.record['evidence_refs'] = refs
            self.reject()

    def test_unconfirmed_field_not_approved(self):
        self.record['reviewed_fields'] = ['interface']
        self.reject()

    def test_remaining_conditions_cannot_disappear(self):
        self.record['remaining_unknowns'].remove('sku_revision')
        self.reject()

    def test_partial_and_sufficient_need_fields(self):
        self.record['reviewed_fields'] = []
        self.reject()
        self.record['reviewed_fields'] = ['watts']
        self.record['result'] = 'EVIDENCE_SUFFICIENT'
        self.reject()

    def test_cannot_approve_public_or_compatibility(self):
        for key, value in [('result','APPROVED'),('public_status','COMPATIBLE'),('usable_for_compatibility','YES')]:
            data = copy.deepcopy(self.data)
            data['records'][0][key] = value
            with self.assertRaises(ValueError): validate(data)

    def test_reviewer_date_and_notes_required(self):
        for key, value in [('reviewer_id',''),('reviewer_id','agent:test'),('notes',''),('reviewed_on','2026-02-30'),('reviewed_on','2026-10-08')]:
            data = copy.deepcopy(self.data)
            data['records'][0][key] = value
            with self.assertRaises(ValueError): validate(data)

    def test_duplicate_ids_and_extra_fields(self):
        self.data['records'].append(copy.deepcopy(self.record))
        self.reject()
        self.data['records'] = [self.record]
        self.record['approve_public'] = 'YES'
        self.reject()

    def test_personal_information_rejected(self):
        self.record['notes'] = 'contact@example.com'
        self.reject()


if __name__ == '__main__': unittest.main()
