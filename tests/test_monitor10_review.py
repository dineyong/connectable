"""Supplement rendering never upgrades evidence or executes source content."""
import copy
import json
import unittest
import tempfile
import io
from contextlib import redirect_stderr
from pathlib import Path
from unittest.mock import patch
from html.parser import HTMLParser

from scripts import build_monitor10_review as builder


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.links = []
        self.meta = []
        self.scripts = 0
        self.headers = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'a':
            self.links.append(attrs)
        if tag == 'meta':
            self.meta.append(attrs)
        if tag == 'script':
            self.scripts += 1


class Monitor10ReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(builder.SOURCE.read_text(encoding='utf-8'))

    def test_real_data_reproducible(self):
        rendered = builder.render(self.data)
        self.assertEqual(rendered, builder.OUTPUT.read_text(encoding='utf-8'))
        parser = PageParser()
        parser.feed(rendered)
        self.assertEqual(len(parser.ids), len(set(parser.ids)))
        for record in self.data['records']:
            self.assertIn(record['id'], parser.ids)
        self.assertEqual(sum('class="m10-product"' in line for line in rendered.splitlines()), 10)

    def test_anchors_and_evidence_links(self):
        parser = PageParser()
        parser.feed(builder.render(self.data))
        expected = [f['url'] for r in self.data['records'] for f in r['confirmed']]
        actual = []
        for link in parser.links:
            if link['href'].startswith('#'):
                self.assertIn(link['href'][1:], parser.ids)
            if link['href'].startswith('https:'):
                actual.append(link['href'])
                self.assertIn('noopener', link['rel'])
        self.assertEqual(actual, expected)

    def test_no_public_promotion_or_scripts(self):
        parser = PageParser()
        rendered = builder.render(self.data)
        parser.feed(rendered)
        self.assertEqual(parser.scripts, 0)
        self.assertTrue(any(m.get('name') == 'robots' and m['content'] == 'noindex,nofollow' for m in parser.meta))
        self.assertNotIn('AggregateRating', rendered)
        self.assertIn('자동 병합하지 않았', rendered)
        self.assertIn('공개 승인 보류', rendered)

    def test_main_rejects_duplicate_json_keys_before_writing(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'duplicate.json'
            source.write_text('{"public_status":"APPROVED","public_status":"UNKNOWN"}', encoding='utf-8')
            output = Path(directory) / 'page.html'
            with patch.object(builder, 'SOURCE', source), patch.object(builder, 'OUTPUT', output), patch('sys.argv', ['build_monitor10_review.py']), redirect_stderr(io.StringIO()):
                self.assertEqual(builder.main(), 1)
            self.assertFalse(output.exists())

    def test_approval_change_fails_before_render(self):
        data = copy.deepcopy(self.data)
        data['public_status'] = 'APPROVED'
        with self.assertRaises(ValueError):
            builder.render(data)

    def test_unknown_and_false_remain_distinct(self):
        self.assertIn('미확인', builder.render_value('UNKNOWN'))
        self.assertIn('미지원', builder.render_value(False))
        self.assertNotEqual(builder.render_value('UNKNOWN'), builder.render_value(False))

    def test_nested_values_render_labels_without_raw_json(self):
        value = {'downstream_charging_w': 15, 'upstream_host_power_delivery': 'UNKNOWN'}
        result = builder.render_value(value)
        self.assertIn('다운스트림 충전 (W)', result)
        self.assertIn('15', result)
        self.assertIn('미확인', result)
        self.assertNotIn('{', result)
        self.assertNotIn('downstream_charging_w', result)

    def test_resolution_and_vesa_pairs_are_readable_without_inferring_units(self):
        self.assertEqual(builder.render_value([2560, 1440], 'resolution'), '<span>2560 × 1440</span>')
        self.assertEqual(builder.render_value({'width': 3840, 'height': 2160}, 'resolution'), '<span>3840 × 2160</span>')
        self.assertEqual(builder.render_value([75, 75], 'vesa_mm'), '<span>75 × 75</span>')
        self.assertIn('<ul', builder.render_value([60, 144], 'input_profiles'))
        self.assertIn('미확인', builder.render_value([2560, 'UNKNOWN'], 'resolution'))

    def test_known_relationship_enums_use_korean(self):
        self.assertEqual(builder.render_value('OFFICIAL_SUPPORT_TO_PRODUCT_LINK'), '공식 지원 페이지에서 제품 페이지로 연결')
        self.assertEqual(builder.render_value('SUPPORTED_MANUFACTURER_STATEMENT'), '제조사가 지원을 명시함')
        self.assertIn('높이 조절 (mm)', builder.render_value({'field': 'stand_height_mm'}))
        self.assertNotIn('usb_c_data_kvm', builder.render_value({'field': 'usb_c_data_kvm'}))

    def test_hostile_text_escaped(self):
        result = builder.render_value({'<script>': '<img src=x onerror=alert(1)>'})
        self.assertNotIn('<script>', result)
        self.assertNotIn('<img', result)
        self.assertIn('&lt;img', result)

    def test_all_confirmed_fields_have_readable_labels(self):
        for record in self.data['records']:
            for fact in record['confirmed']:
                self.assertIn(fact['field'], builder.LABELS)

    def test_confirmed_status_cannot_hide_missing_evidence(self):
        data = copy.deepcopy(self.data)
        data['records'][0]['confirmed'][0]['url'] = ''
        with self.assertRaises(ValueError):
            builder.render(data)


if __name__ == '__main__':
    unittest.main()


class ConflictLabelTests(unittest.TestCase):
    def test_conflict_resolution_is_not_display_resolution(self):
        from scripts.build_monitor10_review import render_record
        from scripts.validate_monitor10_supplement import DATA, load
        record = load(DATA)['records'][7]
        rendered = render_record(record)
        self.assertIn('검토 결론', rendered)
        self.assertNotIn('claims</dt>', rendered)
