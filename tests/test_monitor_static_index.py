import tempfile
import unittest
from pathlib import Path
from scripts.build_monitor_pages_v3 import build, render_index, load, SOURCE

class MonitorStaticIndexTests(unittest.TestCase):
    def test_all_products_have_distinct_links_and_region(self):
        products = load(SOURCE)['products']
        page = render_index(products)
        for product in products:
            href = product['id'].removeprefix('monitor:') + '/'
            self.assertEqual(page.count('href="'+href+'"'), 1)
        self.assertIn('noindex,nofollow', page)
        self.assertIn('한국 판매 SKU 동일성 미확인', page)
        self.assertNotIn('<script',page)

    def test_missing_or_stale_index_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder)
            build(output=output)
            index = output/'index.html'
            index.unlink()
            with self.assertRaises(ValueError): build(output=output, check=True)
            build(output=output)
            index.write_text('stale')
            with self.assertRaises(ValueError): build(output=output, check=True)

    def test_model_markup_is_escaped(self):
        products = load(SOURCE)['products']
        products[0]['display_model'] = '<img onerror=alert(1)>'
        self.assertIn('&lt;img',render_index(products))
        self.assertNotIn('<img',render_index(products))
