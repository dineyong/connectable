"""Joint mutations that formerly bypassed product/evidence trust checks."""
import copy
import unittest
from scripts.build_site_content_v2 import build, read, BATCH_PATH, validate_monitor_batch
from scripts.site_content_validation import validate_content


class P1DataTrustTests(unittest.TestCase):
    def setUp(self):
        self.data = build()
        self.batch = read(BATCH_PATH)

    def test_joint_model_mutation_rejected(self):
        link = self.batch['review_links'][0]
        case = next(r for r in self.data['reviews'] if r['id'] == link['review_id'])
        node = next(n for n in case['nodes'] if n['id'] == link['node_id'])
        node['display_model'] = link['reported_model'] = 'OTHER-MODEL'
        with self.assertRaisesRegex(ValueError, 'MANUAL_REVIEW'):
            validate_monitor_batch(self.batch, self.data['reviews'])

    def test_fake_manufacturer_url_rejected(self):
        self.batch['sources'][0]['url'] = 'https://example.com/not-manufacturer'
        with self.assertRaisesRegex(ValueError, 'UNKNOWN'):
            validate_monitor_batch(self.batch, self.data['reviews'])

    def test_projection_different_model_reference_rejected(self):
        r = next(r for r in self.data['reviews'] if r['monitor_ids'])
        node = next(n for n in r['nodes'] if n['kind'] == 'DISPLAY')
        node['display_model'] = 'OTHER-MODEL'
        for link in r.get('monitor_links', []):
            link['reported_model'] = 'OTHER-MODEL'
        with self.assertRaises(ValueError):
            validate_content(self.data)

    def test_projection_unofficial_manufacturer_url_rejected(self):
        m = self.data['monitors'][0]
        for s in m['source_refs']:
            s.pop('source_file', None)
            s['url'] = 'https://example.com/spec'
        with self.assertRaises(ValueError):
            validate_content(self.data)

    def test_normal_batch_and_content_unchanged(self):
        before = copy.deepcopy(self.data)
        validate_monitor_batch(self.batch, self.data['reviews'])
        validate_content(self.data)
        self.assertEqual(self.data, before)


class TrustPolicyTests(unittest.TestCase):
    def test_exact_model_and_unknown_aliases(self):
        from scripts.data_trust import model_identity
        self.assertEqual(model_identity('V32UE', 'V32UE', 'V32UE'), 'EXACT_MODEL_LABEL')
        for label in ('V32UE-E', '주연테크 V32UE', 'v32ue', ' V32UE ', 'UNKNOWN', None, 'V32UE/KR-SKU'):
            with self.subTest(label=label):
                self.assertEqual(model_identity('V32UE', label), 'MANUAL_REVIEW')

    def test_normal_manufacturer_product_and_support_urls(self):
        from scripts.data_trust import official_url_status
        examples = [
            ('Dell', 'https://www.dell.com/support/product-details/en-us/product/u2723qe-monitor/resources/manuals'),
            ('Dell', 'https://dl.dell.com/content/manual12109242-dell-u2723qe-monitor-user-s-guide.pdf?language=en-us'),
            ('LG', 'https://www.lg.com/lv/monitori/lg-27up850-w'),
            ('MSI', 'https://www.msi.com/Business-Productivity-Monitor/Modern-MD271UL/Specification'),
            ('크로스오버', 'https://crosslcd.co.kr/shop/item.php?it_id=1716533757'),
            ('주연테크', 'https://www.jooyon.co.kr/bbs/board.php?bo_table=press&page=16&wr_id=227'),
        ]
        for maker, url in examples:
            with self.subTest(url=url):
                self.assertEqual(official_url_status(url, maker), 'OFFICIAL_URL_SCOPE')

    def test_spoofed_domains_and_ambiguous_authorities(self):
        from scripts.data_trust import official_url_status
        for url in (
            'https://www.dell.com.evil.example/support/spec',
            'https://evil-www.dell.com/support/spec',
            'https://www.deIl.com/support/spec',
            'https://www.dell.com@evil.example/support/spec',
            'https://evil.example/support/spec?site=www.dell.com',
            'https://www.dell.com:444/support/spec',
            'https://www.dell.com./support/spec',
            'https://support.dell.com/support/spec',  # Not reviewed host; no suffix guessing.
            'http://www.dell.com/support/spec',
            'https://www.dell.com\\@evil.example/support/spec',
            'https://www.dell.com/support/%2e%2e/redirect',
            'https://www.dell.com/support/spec#redirect',
        ):
            with self.subTest(url=url):
                self.assertEqual(official_url_status(url, 'Dell'), 'UNKNOWN')
        self.assertEqual(official_url_status('https://www.dell.com/support/spec', 'LG'), 'UNKNOWN')

    def test_redirect_routes_and_parameters_are_unknown(self):
        from scripts.data_trust import official_url_status
        for url in (
            'https://www.dell.com/redirect?url=https://evil.example',
            'https://www.dell.com/support/redirect?language=en-us',
            'https://www.dell.com/support/spec?url=https://evil.example',
            'https://www.dell.com/support/spec?language=https%253A%252F%252Fevil.example',
            'https://www.dell.com/support/spec?language=en&language=de',
            'https://www.dell.com/unknown-endpoint',
        ):
            with self.subTest(url=url):
                self.assertEqual(official_url_status(url, 'Dell'), 'UNKNOWN')

    def test_recorded_final_destination_must_be_official(self):
        from scripts.data_trust import require_official_source
        good = {'url': 'https://www.dell.com/support/spec',
                'redirect_chain': ['https://www.dell.com/support/spec-2'],
                'final_url': 'https://dl.dell.com/content/manual.pdf'}
        before = copy.deepcopy(good)
        require_official_source(good, 'Dell', 'source')
        self.assertEqual(good, before)
        for field, value in [('final_url', 'https://evil.example/spec'),
                             ('redirect_chain', ['https://evil.example', good['final_url']]),
                             ('redirect_chain', [])]:
            bad = copy.deepcopy(good)
            bad[field] = value
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, 'UNKNOWN'):
                require_official_source(bad, 'Dell', 'source')

    def test_alias_and_sku_variants_do_not_create_links(self):
        from scripts.build_site_content_v2 import validate_monitor_batch
        data = build()
        for label in ('V32UE-E', 'JYT V32UE', 'V32UE/KR-SKU', 'UNKNOWN'):
            batch = read(BATCH_PATH)
            cases = copy.deepcopy(data['reviews'])
            link = batch['review_links'][0]
            node = next(n for r in cases if r['id'] == link['review_id'] for n in r['nodes'] if n['id'] == link['node_id'])
            node['display_model'] = link['reported_model'] = label
            with self.subTest(label=label), self.assertRaisesRegex(ValueError, 'MANUAL_REVIEW'):
                validate_monitor_batch(batch, cases)

    def test_real_public_projection_still_valid(self):
        from pathlib import Path
        text = Path('web/site-content-v2.js').read_text()
        import json
        projection = json.loads(text.split('window.CONNECTABLE_SITE_V2 = ', 1)[1].rsplit(';', 1)[0])
        validate_content(projection)

    def test_spec_review_uses_same_official_host_policy(self):
        import json
        from scripts.validate_official_spec_review import PATH, validate
        data = json.loads(PATH.read_text())
        validate(data)
        source = next(s for s in data['sources'] if s['source_id'] == data['assertions'][0]['source_refs'][0])
        source['url'] = 'https://unreviewed.dell.com/support/spec'
        with self.assertRaisesRegex(ValueError, 'UNKNOWN'):
            validate(data)

    def test_manufacturer_board_is_not_automatically_official_spec(self):
        from scripts.data_trust import official_url_status
        self.assertEqual(official_url_status('https://www.jooyon.co.kr/bbs/board.php?bo_table=user&wr_id=227', '주연테크'), 'UNKNOWN')
        self.assertEqual(official_url_status('https://www.crosslcd.co.kr/bbs/board.php?bo_table=review&wr_id=1', '크로스오버'), 'UNKNOWN')
