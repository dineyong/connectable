import copy
import json
import subprocess
import sys
import unittest
from scripts import build_monitor_review_links as links


class MonitorReviewLinkTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(links.SOURCE.read_text())

    def reject(self, mutate):
        data = copy.deepcopy(self.data)
        mutate(data)
        with self.assertRaises(ValueError):
            links.validate(data)

    def test_real_source_and_generated_outputs(self):
        self.assertEqual(len(links.validate(self.data)['items']), 5)
        subprocess.run([sys.executable, str(links.ROOT / 'scripts/build_monitor_review_links.py'), '--check'], check=True, capture_output=True)

    def test_build_is_read_only_and_projects_public_fields(self):
        before = links.SOURCE.read_bytes()
        result = links.build()
        self.assertEqual(links.SOURCE.read_bytes(), before)
        self.assertNotIn('evidence_location', result['items'][0])
        self.assertEqual(result['items'][0]['model_scope'], 'EXACT_DOCUMENT_MODEL')

    def test_empty_source_supported(self):
        self.assertEqual(links.validate({'schema_version': 1, 'items': []})['items'], [])

    def test_missing_and_empty_required_fields(self):
        self.reject(lambda d: d['items'][0].pop('summary'))
        self.reject(lambda d: d['items'][0].update(title=' '))
        self.reject(lambda d: d['items'][0].update(evidence_location=''))

    def test_unknown_product_and_uncertain_models(self):
        self.reject(lambda d: d['items'][0].update(product_id='monitor:missing'))
        self.reject(lambda d: d['items'][0].update(model_scope='PARTIAL'))
        self.reject(lambda d: d['items'][0].update(checked_model='M32U-A'))

    def test_wrong_product_rebinding_even_with_changed_model(self):
        self.reject(lambda d: d['items'][0].update(product_id='monitor:asus-xg27aqdmg', checked_model='XG27AQDMG'))

    def test_duplicate_id_and_normalized_url(self):
        self.reject(lambda d: d['items'].append(copy.deepcopy(d['items'][0])))
        def duplicate(d):
            row = copy.deepcopy(d['items'][0])
            row.update(id='review-link:new', url=row['url'] + '/')
            d['items'].append(row)
        self.reject(duplicate)

    def test_unsafe_urls(self):
        for value in ('http://www.rtings.com/monitor/reviews/gigabyte/m32u',
                      'https://www.rtings.com.evil.test/monitor/reviews/gigabyte/m32u',
                      'https://x@www.rtings.com/monitor/reviews/gigabyte/m32u',
                      'https://www.rtings.com:443/monitor/reviews/gigabyte/m32u',
                      'https://www.rtings.com/monitor/reviews/gigabyte/m32u?redirect=evil',
                      'https://www.rtings.com/monitor/reviews/gigabyte/%6d32u',
                      'https://www.rtings.com/monitor/reviews/gigabyte/../m32u',
                      'https://www.rtings.com\\evil/monitor/reviews/gigabyte/m32u'):
            with self.subTest(url=value):
                self.reject(lambda d: d['items'][0].update(url=value))

    def test_bad_dates_and_enums(self):
        for update in ({'checked_on': '2026-02-30'}, {'checked_on': '2026-1-1'},
                       {'checked_on': []}, {'source_review_id': []}, {'commercial_context': 'APPROVED'}, {'review_type': 'QUESTION'},
                       {'evidence_origin': 'MIGRATED'}):
            self.reject(lambda d: d['items'][0].update(update))

    def test_original_reference_integrity(self):
        self.reject(lambda d: d['items'][-1].update(source_review_id='mr:missing'))
        self.reject(lambda d: d['items'][-1].update(source_review_id='mr:u2723qe-body-gap'))
        self.reject(lambda d: d['items'][-1].update(source_review_id=None))

    def test_contact_details_and_html_rejected(self):
        for text in ('contact@example.com', '010-1234-5678', '<img src=x>'):
            self.reject(lambda d: d['items'][0].update(summary=text))


if __name__ == '__main__':
    unittest.main()
