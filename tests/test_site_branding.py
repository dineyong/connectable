"""Current-site branding remains consistent without granting public approval."""
from html.parser import HTMLParser
from pathlib import Path
import unittest

from scripts.prepare_launch_preview import ASSETS, WEB
from scripts.site_branding import social_metadata


class Head(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.meta = {}
        self.title = ''
        self.in_title = False
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'title':
            self.in_title = True
        if tag == 'meta':
            key = attrs.get('property') or attrs.get('name')
            self.meta.setdefault(key, []).append(attrs.get('content'))

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False

    def handle_data(self, text):
        if self.in_title:
            self.title += text


class SiteBrandingTests(unittest.TestCase):
    def test_all_current_pages_have_matching_brand_and_metadata(self):
        pages = [WEB / name for name in ASSETS if name.endswith('.html')]
        pages += sorted((WEB / 'monitors').rglob('index.html'))
        self.assertEqual(len(pages), 37)
        for path in pages:
            with self.subTest(page=str(path.relative_to(WEB))):
                text = path.read_text()
                head = Head(text)
                self.assertIn('모니픽', head.title)
                self.assertNotIn('connectable', text.lower())
                for stale in ['로컬 미리보기', '로컬 검토용', '로컬 시연', 'LOCAL PREVIEW']:
                    self.assertNotIn(stale, text)
                self.assertEqual(head.meta['og:site_name'], ['모니픽'])
                self.assertEqual(head.meta['og:locale'], ['ko_KR'])
                self.assertEqual(head.meta['og:title'], [head.title])
                self.assertEqual(head.meta['twitter:title'], [head.title])
                self.assertEqual(head.meta['og:description'], head.meta['description'])
                self.assertEqual(head.meta['twitter:description'], head.meta['description'])
                self.assertIn('noindex', head.meta['robots'][0])
                self.assertNotIn('og:url', head.meta)
                self.assertNotIn('rel="canonical"', text)

    def test_social_metadata_escapes_untrusted_model_text(self):
        value = 'A "quoted" <script> & model'
        text = social_metadata(value, value)
        head = Head(text)
        self.assertNotIn('<script>', text)
        self.assertEqual(head.meta['og:title'], [value])
        self.assertEqual(head.meta['og:description'], [value])

    def test_existing_browser_storage_and_internal_contract_are_preserved(self):
        script = (WEB / 'monitor-v3.js').read_text()
        self.assertIn('connectable-v3-comparison', script)
        self.assertIn('connectable-v3-helpful:', script)
        self.assertIn('ConnectableValueFormat', script)
        information = (WEB / 'information.html').read_text()
        self.assertIn('반응은 이 브라우저에 저장합니다', information)
        self.assertIn('한국 판매 SKU 미확인', information)
