"""Offline preview checks deliberately separate from public release approval."""
import tempfile
import unittest
from pathlib import Path

from scripts.validate_local_site import validate_site

BASE = '''<!doctype html><html lang="ko"><head><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>페이지</title><meta name="description" content="설명"></head><body><h1 id="main">본문</h1>{body}</body></html>'''


class LocalSiteTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(self, body='', text=None, path='page.html'):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text if text is not None else BASE.format(body=body), encoding='utf-8')
        return target

    def check(self, *pages):
        return validate_site(self.root, pages or ['page.html'])

    def test_valid_internal_fragment_assets_and_external_source(self):
        self.write('<a href="#main">본문</a><a href="https://example.org/spec#external">출처</a><script src="app.js"></script>')
        (self.root / 'app.js').write_text('', encoding='utf-8')
        self.assertEqual(self.check(), [])

    def test_missing_local_asset(self):
        self.write('<link rel="stylesheet" href="absent.css">')
        self.assertTrue(any('missing local target' in e for e in self.check()))

    def test_cross_page_fragment_and_relative_root_links(self):
        self.write('<a href="/page.html#main">목록</a>', path='nested/page.html', text=None)
        self.write('<a href="nested/page.html#main">상세</a>')
        self.assertEqual(self.check(), [])
        self.write('<a href="nested/page.html#absent">상세</a>')
        self.assertTrue(any('missing fragment' in e for e in self.check()))

    def test_unicode_percent_encoded_fragment(self):
        self.write('<p id="한글">본문</p><a href="#%ED%95%9C%EA%B8%80">이동</a>')
        self.assertEqual(self.check(), [])

    def test_path_escape_and_encoded_escape_rejected(self):
        for href in ('../outside', '%2e%2e/outside', '/%2e%2e/outside'):
            with self.subTest(href=href):
                self.write(f'<a href="{href}">이동</a>')
                self.assertTrue(any('escapes document root' in e for e in self.check()))

    def test_unsafe_url_syntax_and_schemes(self):
        for href in ('javascript:alert(1)', 'data:text/html,test', 'folder%5cfile', 'page.html%00'):
            with self.subTest(href=href):
                self.write(f'<a href="{href}">이동</a>')
                self.assertTrue(self.check())

    def test_unsupported_scheme_with_authority_rejected(self):
        for href in ('javascript://evil.example/a', 'data://evil.example/foo', 'file://evil.example/path'):
            with self.subTest(href=href):
                self.write(f'<a href="{href}">이동</a>')
                self.assertTrue(any('unsupported URL scheme' in e for e in self.check()))

    def test_symlink_escape_rejected(self):
        with tempfile.TemporaryDirectory() as outside:
            Path(outside, 'page.html').write_text(BASE.format(body=''), encoding='utf-8')
            (self.root / 'escape').symlink_to(outside, target_is_directory=True)
            self.write('<a href="escape/page.html">이동</a>')
            self.assertTrue(any('escapes document root' in e for e in self.check()))

    def test_missing_metadata_or_wrong_language_rejected(self):
        for old, new in [('lang="ko"', 'lang="en"'), ('width=device-width', 'width=1000'), ('<title>페이지</title>', ''), ('content="설명"', 'content=""')]:
            with self.subTest(old=old):
                self.write(text=BASE.format(body='').replace(old, new))
                self.assertTrue(self.check())

    def test_missing_or_conflicting_noindex_rejected(self):
        for value in ('index,follow', 'noindex,index', 'all', 'nofollow'):
            with self.subTest(value=value):
                self.write(text=BASE.format(body='').replace('noindex,nofollow', value))
                self.assertTrue(any('noindex' in e for e in self.check()))

    def test_duplicate_title_and_description_rejected(self):
        self.write()
        self.write(path='other.html')
        errors = self.check('page.html', 'other.html')
        self.assertTrue(any('duplicate title' in e for e in errors))
        self.assertTrue(any('duplicate description' in e for e in errors))

    def test_duplicate_ids_and_base_rejected(self):
        self.write('<div id="main"></div><base href="https://example.org/">')
        errors = self.check()
        self.assertTrue(any('duplicate HTML ids' in e for e in errors))
        self.assertTrue(any('base element' in e for e in errors))

    def test_canonical_deferred(self):
        self.write('<link rel="canonical" href="https://example.org/product">')
        self.assertTrue(any('canonical deferred' in e for e in self.check()))

    def test_nested_publication_schema_rejected(self):
        for field in ('offers', 'aggregateRating', 'review', 'reviewRating'):
            with self.subTest(field=field):
                self.write('<script type="application/ld+json">{"@graph":[{"'+field+'":{}}]}</script>')
                self.assertTrue(any('publication-gated' in e for e in self.check()))

    def test_standalone_publication_types_rejected(self):
        import json
        for value in ('AggregateRating', 'Offer', 'AggregateOffer', 'Review',
                      'https://schema.org/AggregateRating', 'http://schema.org/Offer',
                      ['Thing', 'https://schema.org/Review']):
            with self.subTest(value=value):
                payload = json.dumps({'@type': value, 'ratingValue': 5, 'ratingCount': 99})
                self.write('<script type="application/ld+json">'+payload+'</script>')
                self.assertTrue(any('publication-gated' in e for e in self.check()))
        self.write('<script type="application/ld+json">{"@type":"Product","name":"모델"}</script>')
        self.assertEqual(self.check(), [])

    def test_invalid_jsonld_and_harmless_jsonld(self):
        self.write('<script type="application/ld+json">invalid</script>')
        self.assertTrue(any('invalid JSON-LD' in e for e in self.check()))
        self.write('<script type="application/ld+json">{"@type":"WebPage","name":"페이지"}</script>')
        self.assertEqual(self.check(), [])

    def test_real_modern_pages(self):
        self.assertEqual(validate_site(), [])


if __name__ == '__main__':
    unittest.main()
