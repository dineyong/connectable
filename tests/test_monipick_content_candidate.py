import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from scripts import prepare_monipick_content_candidate as content
from scripts.build_monipick_public_candidate import expected_artifacts, digest
from scripts.build_monipick_cloudflare import content_fingerprint, read_approval


class ContentPolishTests(unittest.TestCase):
    def test_routes_preserve_queries_fragments_and_external_urls(self):
        routes={'/monitor-v3.html':'/','/guides/monitor-buying.html':'/guides/monitor-buying'}
        examples=[('../../monitor-v3.html?q=4k#products','/?q=4k#products'),
                  ('../../guides/monitor-buying.html#usb-c','/guides/monitor-buying#usb-c'),
                  ('#specs','#specs'),('?q=4k','?q=4k'),
                  ('https://other.example/monitor-v3.html','https://other.example/monitor-v3.html'),
                  ('mailto:contact@monipick.com','mailto:contact@monipick.com'),
                  ('https://monipick.com.evil.example/monitor-v3.html','https://monipick.com.evil.example/monitor-v3.html')]
        for value,want in examples:
            with self.subTest(value=value):self.assertEqual(content.final_link(value,'monitors/asus-pa279crv/index.html',routes),want)
        self.assertEqual(content.normalize_links('<a href="monitor-v3.html?a=1&amp;b=2#products">x</a>','index.html',routes),'<a href="/?a=1&amp;b=2#products">x</a>')

    def test_three_summaries_have_exact_fact_bindings_and_source_dates(self):
        summaries=content.reviewed_summaries()
        self.assertEqual(len(summaries),3)
        for pid,(item,text) in summaries.items():
            self.assertIn('공식 근거 · 2026-10-10',text)
            self.assertIn('호환성 승인이 아닙니다',text)
            self.assertIn('/guides/monitor-buying#usb-c',text)
        self.assertIn('데이터 전용',summaries['monitor:dell-u2724de'][1])
        self.assertIn('96W',summaries['monitor:asus-pa279crv'][0]['description'])
        self.assertIn('65W',summaries['monitor:msi-modern-md271ul'][0]['description'])

    def test_changed_value_unit_qualifier_or_unknown_cannot_pass(self):
        original=content.official(content.load(content.FACTS))
        for key,value in [('value',99),('unit','Hz'),('qualifier','UNKNOWN')]:
            bad=copy.deepcopy(original)
            fact=next(f for p in bad['products'] if p['id']=='monitor:asus-pa279crv' for f in p['facts'] if f['property']=='pd_supply')
            fact[key]=value
            with self.subTest(key=key),patch.object(content,'official',return_value=bad),self.assertRaises(ValueError):content.reviewed_summaries()

    def test_resolved_uncertainty_requires_new_editorial_review(self):
        bad=content.official(content.load(content.FACTS))
        next(p for p in bad['products'] if p['id']=='monitor:msi-modern-md271ul')['missing_fields'].remove('kvm')
        with patch.object(content,'official',return_value=bad),self.assertRaises(ValueError):content.reviewed_summaries()

    def test_candidate_preserves_raw_data_production_gate_and_source_markup(self):
        _,baseline=expected_artifacts()
        self.assertEqual(content_fingerprint({n:digest(v) for n,v in baseline.items()}),read_approval()['approved_content_fingerprint'])
        before=content.FACTS.read_bytes()
        with tempfile.TemporaryDirectory() as tmp:
            output=Path(tmp)/'review'
            m=content.build_content_candidate(output)
            self.assertFalse(content.validate_content_candidate(output))
            self.assertFalse(m['publication_authorized']);self.assertFalse(m['advertising_enabled']);self.assertFalse(m['analytics_enabled'])
            detail=(output/'site/monitors/asus-pa279crv/index.html').read_text()
            self.assertIn('한국 판매 SKU 동일성은 미확인',detail)
            self.assertIn('model-highlights',detail)
            self.assertIn('href="/"',detail)
            self.assertNotIn('href="../../monitor-v3.html"',detail)
            self.assertIn('href="/monitor10-review#',(output/'site/monitor-v3.js').read_text())
            for name,value in baseline.items():
                if not name.endswith('.html') and name not in ('monitor-v3.js','monitor-detail-v3.css','_headers'):self.assertEqual((output/'site'/name).read_bytes(),value)
            self.assertEqual(content.FACTS.read_bytes(),before)
            (output/'site/monitors/asus-pa279crv/index.html').write_text(detail.replace('96W','100W'))
            self.assertTrue(content.validate_content_candidate(output))

    def test_no_overwrite_and_no_silent_approval(self):
        with tempfile.TemporaryDirectory() as tmp:
            output=Path(tmp)/'review';content.build_content_candidate(output)
            with self.assertRaises(ValueError):content.build_content_candidate(output)
            p=output/'manifest.json';m=json.loads(p.read_text());m['publication_authorized']=True;p.write_text(json.dumps(m))
            self.assertTrue(content.validate_content_candidate(output))

    def test_changed_assets_have_content_versions_for_returning_visitors(self):
        _,artifacts=content.polished_artifacts()
        version=content.digest(artifacts['monitor-detail-v3.css'])[:12]
        self.assertIn('monitor-detail-v3.css?v='+version,artifacts['monitors/asus-pa279crv/index.html'].decode())
        version=content.digest(artifacts['monitor-v3.js'])[:12]
        self.assertIn('monitor-v3.js?v='+version,artifacts['index.html'].decode())
