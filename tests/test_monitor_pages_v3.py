import tempfile
import unittest
from pathlib import Path
from scripts.build_monitor_pages_v3 import build, render, load, SOURCE

class MonitorPagesTests(unittest.TestCase):
    def test_real_documents_match_source(self):
        self.assertEqual(build(check=True),30)

    def test_stale_and_unexpected_documents_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);build(output=root);build(output=root,check=True)
            first=next(root.glob('*/index.html'));first.write_text('stale')
            with self.assertRaises(ValueError):build(output=root,check=True)
            build(output=root);extra=root/'fake/index.html';extra.parent.mkdir();extra.write_text('fake')
            with self.assertRaises(ValueError):build(output=root,check=True)

    def test_full_facts_and_no_public_seo_claims(self):
        p=load(SOURCE)['products'][0];page=render(p)
        self.assertIn('noindex,nofollow',page)
        self.assertIn('한국 판매 SKU 동일성은 미확인',page)
        self.assertNotIn('rel="canonical"',page)
        self.assertNotIn('aggregateRating',page)
        for f in p['facts']:self.assertIn(f['location'].replace('&','&amp;'),page)
        for s in p['source_refs']:self.assertIn(s['checked_on'],page)

    def test_content_is_escaped(self):
        p=load(SOURCE)['products'][0];p['display_model']='<script>alert(1)</script>'
        page=render(p)
        self.assertNotIn('<script>',page)
        self.assertIn('&lt;script&gt;',page)

    def test_qualifiers_remain_separate(self):
        p=load(SOURCE)['products'][0]
        p['facts'][0]['qualifier']='RATED';p['facts'][1]['qualifier']='UP_TO'
        page=render(p);self.assertIn('정격',page);self.assertIn('최대 한도',page)
