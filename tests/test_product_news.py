import copy
import json
import unittest
from scripts.product_news import DATA, ASSET, validate, asset

class ProductNewsTests(unittest.TestCase):
    def setUp(self): self.data=json.loads(DATA.read_text())
    def test_real_data_and_asset(self): self.assertEqual(ASSET.read_text(),asset(self.data))
    def test_untrusted_urls(self):
        for url in ['https://www.benq.com.evil.test/ko-kr/news/products/x','javascript:alert(1)','https://user@www.benq.com/ko-kr/news/products/x','https://www.benq.com:88/ko-kr/news/products/x','https://www.benq.com/ko-kr/news/products/%2e%2e/x']:
            with self.subTest(url=url):
                d=copy.deepcopy(self.data);d['items'][0]['url']=url
                with self.assertRaises(ValueError):validate(d)
    def test_unknown_and_missing_evidence(self):
        for key,value in [('review_status','APPROVED'),('evidence_location',''),('checked_on','invalid')]:
            d=copy.deepcopy(self.data);d['items'][0][key]=value
            with self.assertRaises(ValueError):validate(d)
    def test_duplicate_and_schedule(self):
        self.data['items'].append(copy.deepcopy(self.data['items'][0]))
        with self.assertRaises(ValueError):validate(self.data)
        self.data['items'].pop();self.data['items'][1]['preorder_on']='2026-11-01'
        with self.assertRaises(ValueError):validate(self.data)
    def test_script_escape(self):
        self.data['items'][0]['title']='</script>'
        self.assertNotIn('</script>',asset(self.data))
