import copy
import json
import unittest

from scripts.build_site_content_v2 import ROOT, BATCH_PATH, build, read, validate_monitor_batch
from scripts.site_content_validation import validate_content


class SiteValidationHardeningTests(unittest.TestCase):
    def setUp(self):
        self.data = build()
        self.batch = read(BATCH_PATH)

    def reject(self, batch):
        with self.assertRaises(ValueError):
            validate_monitor_batch(batch, self.data['reviews'])

    def test_empty_fact_evidence(self):
        self.batch['facts'][0]['source_refs'] = []
        self.reject(self.batch)

    def test_empty_product_evidence(self):
        self.batch['products'][0]['source_refs'] = []
        self.reject(self.batch)

    def test_empty_review_link_evidence(self):
        self.batch['review_links'][0]['source_refs'] = []
        self.reject(self.batch)

    def test_invalid_typed_payload(self):
        self.batch['facts'][0]['payload'] = {'watts': -1}
        self.reject(self.batch)

    def test_wrong_manufacturer_model_scope(self):
        self.batch['facts'][0]['source_refs'] = ['SITE-MSI-MD271UL']
        self.reject(self.batch)

    def test_public_projection_keeps_fact_targets(self):
        text = (ROOT/'web/site-content-v2.js').read_text()
        data = json.loads(text.split('window.CONNECTABLE_SITE_V2 = ', 1)[1].rsplit(';', 1)[0])
        for monitor in data['monitors']:
            ids = {f.get('fact_id') for f in monitor['features']}
            for capability in monitor.get('capabilities', {}).values():
                self.assertTrue(set(capability['feature_refs']) <= ids)

    def test_invalid_numbers_and_units(self):
        for value in (-1, 0, True, '65W', float('inf')):
            with self.subTest(value=value):
                b = copy.deepcopy(self.batch)
                b['facts'][2]['payload']['watts'] = value
                self.reject(b)

    def test_unknown_power_is_not_guessed(self):
        b = copy.deepcopy(self.batch)
        f = next(f for f in b['facts'] if f['payload'].get('rating_basis') == 'PRODUCT_LABEL_ONLY')
        f['payload']['watts'] = 65
        self.reject(b)

    def test_invalid_url_and_dates(self):
        for field, value in [('url', 'https://user:secret@example.com'), ('url', 'https:///missing'), ('checked_at', '2026-02-30'), ('checked_at', '20261009')]:
            with self.subTest(field=field, value=value):
                b = copy.deepcopy(self.batch)
                b['sources'][0][field] = value
                self.reject(b)

    def test_dangling_fact_source(self):
        self.batch['facts'][0]['source_refs'] = ['missing']
        self.reject(self.batch)

    def test_missing_fact_target_in_projection(self):
        d = copy.deepcopy(self.data)
        d['monitors'][3]['features'].pop(1)
        with self.assertRaises(ValueError):
            validate_content(d)

    def test_duplicate_and_dangling_global_relationships(self):
        for mutation in ('duplicate', 'monitor', 'guide'):
            with self.subTest(mutation=mutation):
                d = copy.deepcopy(self.data)
                if mutation == 'duplicate':
                    d['monitors'].append(copy.deepcopy(d['monitors'][0]))
                elif mutation == 'monitor':
                    d['reviews'][0]['monitor_ids'] = ['missing']
                else:
                    d['guides'][0]['related_review_ids'] = ['missing']
                with self.assertRaises(ValueError):
                    validate_content(d)

    def test_review_evidence_and_configuration_references(self):
        for key in ('configuration_id', 'evidence_refs'):
            d = copy.deepcopy(self.data)
            d['reviews'][0]['observations'][0][key] = ['missing'] if key == 'evidence_refs' else 'missing'
            with self.subTest(key=key), self.assertRaises(ValueError):
                validate_content(d)

    def test_valid_source_and_public_projection(self):
        validate_content(self.data)
        text = (ROOT/'web/site-content-v2.js').read_text()
        validate_content(json.loads(text.split('window.CONNECTABLE_SITE_V2 = ', 1)[1].rsplit(';', 1)[0]))

    def test_source_file_record_and_url_integrity(self):
        for field, value in [('source_file', 'data/missing.json'), ('record_id', 'missing'), ('url', 'https://example.com/not-the-original')]:
            d = copy.deepcopy(self.data)
            d['monitors'][0]['source_refs'][0][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_content(d)


if __name__ == '__main__':
    unittest.main()
