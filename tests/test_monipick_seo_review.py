import copy
import json
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import urljoin, urlsplit

from scripts import prepare_monipick_seo_review as seo
from scripts import prepare_monipick_content_candidate as content
from scripts.build_monipick_cloudflare import content_fingerprint, read_content_approval


class SeoReviewTests(unittest.TestCase):
    def test_complete_catalog_has_unique_descriptions_and_evidence(self):
        summaries=seo.expanded_summaries()
        self.assertEqual(len(summaries),30)
        self.assertEqual(len({item['description'] for item,_ in summaries.values()}),30)
        for item,section in summaries.values():
            self.assertEqual(len(item['claims']),2)
            self.assertIn('공식 근거 · ',section)
            self.assertIn('호환성 승인이 아닙니다',section)
            for claim in item['claims']:
                self.assertEqual(set(claim['expected_facts']),set(claim['expected_context']))

    def test_scopes_and_sources_cannot_drift_silently(self):
        for key,value in [('scope','WRONG_SCOPE'),('location','WRONG_LOCATION'),('source_refs',[])]:
            data=content.official(content.load(content.FACTS))
            product=next(p for p in data['products'] if p['id']=='monitor:dell-u2724d')
            next(f for f in product['facts'] if f['property']=='usb_c')[key]=value
            with self.subTest(key=key),patch.object(content,'official',return_value=data),self.assertRaises(ValueError):
                seo.expanded_summaries()

    def test_value_unit_or_qualifier_change_blocks_new_summaries(self):
        for key,value in [('value',144),('unit','W'),('qualifier','UNKNOWN')]:
            data=content.official(content.load(content.FACTS))
            product=next(p for p in data['products'] if p['id']=='monitor:lg-32gs95ue-b')
            next(f for f in product['facts'] if f['property']=='refresh')[key]=value
            with self.subTest(key=key),patch.object(content,'official',return_value=data),self.assertRaises(ValueError):
                seo.expanded_summaries()

    def test_every_detail_has_one_summary_and_navigation_without_changing_tables(self):
        _,base=content.polished_artifacts();_,proposed=seo.review_artifacts()
        details=[n for n in proposed if re.fullmatch(r'monitors/[^/]+/index.html',n)]
        self.assertEqual(len(details),30)
        for name in details:
            old=base[name].decode();new=proposed[name].decode()
            self.assertEqual(new.count('id="model-highlights"'),1)
            self.assertEqual(new.count('aria-label="현재 위치"'),1)
            self.assertIn('href="/information#corrections"',new)
            self.assertEqual(re.findall(r'<table>.*?</table>',old,re.S),re.findall(r'<table>.*?</table>',new,re.S))
            self.assertIn('한국 판매 SKU 동일성은 미확인',new)

    def test_internal_page_links_resolve_directly_and_fragments_exist(self):
        plan,artifacts=seo.review_artifacts()
        routes={p['route']:p['source'] for p in plan['pages']}
        for name,body in artifacts.items():
            if not name.endswith('.html') or name.startswith('naver'):continue
            for href in re.findall(r'href="([^"]*)"',body.decode()):
                target=urlsplit(urljoin('https://monipick.com/'+name,href))
                if target.netloc!='monipick.com' or target.path not in routes:continue
                destination=artifacts[routes[target.path]].decode()
                if target.fragment:self.assertIn('id="'+target.fragment+'"',destination,(name,href))
            self.assertNotRegex(body.decode(),r'href="[^"#?]*(?:monitor-v3|information|monitor-buying|tech-news|monitor10-review)\.html')

    def test_existing_production_fingerprint_and_authorizations_unchanged(self):
        _,before=content.polished_artifacts()
        expected=read_content_approval()['approved_content_fingerprint']
        self.assertEqual(content_fingerprint({n:content.digest(v) for n,v in before.items()}),expected)
        seo.review_artifacts()
        _,after=content.polished_artifacts()
        self.assertEqual(before,after)

    def test_candidate_tampering_and_approval_promotion_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'review';m=seo.build_review(out)
            self.assertEqual(seo.validate_review(out),[])
            self.assertFalse(m['publication_authorized']);self.assertFalse(m['analytics_enabled'])
            self.assertFalse(m['advertising_enabled']);self.assertFalse(m['deployment_authorized'])
            target=out/'site/monitors/lg-32gs95ue-b/index.html';original=target.read_bytes()
            target.write_bytes(original.replace('480Hz'.encode(),'960Hz'.encode()))
            self.assertTrue(seo.validate_review(out));target.write_bytes(original)
            path=out/'manifest.json';data=json.loads(path.read_text());data['publication_authorized']=True
            path.write_text(json.dumps(data));self.assertTrue(seo.validate_review(out))
            with self.assertRaises(ValueError):seo.build_review(out)
