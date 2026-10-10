import copy
import unittest
from scripts.tech_news import parse, refresh, validate, asset, CACHE, fetch
from unittest.mock import patch
STAMP='2026-10-10T12:00:00+00:00'
def feed(host='news.samsung.com',title='OLED monitor update',pub='Sat, 10 Oct 2026 10:00:00 +0000'):
    return f'<rss><channel><item><title>{title}</title><link>https://{host}/test-news</link><pubDate>{pub}</pubDate><description>DO NOT SAVE ARTICLE BODY</description></item></channel></rss>'.encode()
def fetcher(sid):return feed('news.samsung.com' if sid=='samsung-kr' else 'blogs.windows.com')

class TechNewsTests(unittest.TestCase):
    def setUp(self):self.data=refresh(fetcher=fetcher,stamp=STAMP)
    def test_real_cache(self):validate(__import__('json').loads(CACHE.read_text()))
    def test_metadata_only(self):
        self.assertEqual(len(self.data['items']),2)
        self.assertNotIn('DO NOT SAVE',asset(self.data))
    def test_title_based_monitor_tag(self):self.assertEqual(self.data['items'][0]['category_basis'],'TITLE_KEYWORD_HEURISTIC')
    def test_failed_refresh_preserves_cache(self):
        def fail(_):raise OSError('blocked')
        after=refresh(self.data,fetcher=fail,stamp='2026-10-10T12:15:00+00:00')
        self.assertEqual(after['items'],self.data['items'])
        self.assertEqual(after['sources'][0]['status'],'STALE')
        self.assertEqual(after['sources'][0]['last_success_at'],STAMP)
    def test_empty_feed_preserves_old(self):
        after=refresh(self.data,fetcher=lambda _:b'<rss><channel/></rss>',stamp=STAMP)
        self.assertEqual(after['items'],self.data['items'])
    def test_unsafe_article_links_not_saved(self):
        for host in ['evil.test','news.samsung.com.evil.test','user@news.samsung.com:8080']:
            self.assertEqual(parse(feed(host), 'samsung-kr',STAMP),[])
    def test_future_and_invalid_dates_not_saved(self):
        for p in ['bad date','Sun, 11 Oct 2026 10:00:00 +0000']:
            self.assertEqual(parse(feed(pub=p),'samsung-kr',STAMP),[])
    def test_doctype_and_entity_rejected(self):
        for raw in [b'<!DOCTYPE rss><rss/>', b'<!ENTITY x "test"><rss/>']:
            with self.assertRaises(ValueError):parse(raw,'samsung-kr',STAMP)
    def test_html_error_rejected(self):
        with self.assertRaises(ValueError):parse(b'<html/>','samsung-kr',STAMP)
    def test_duplicate_article_rejected(self):
        self.data['items'].append(copy.deepcopy(self.data['items'][0]))
        with self.assertRaises(ValueError):validate(self.data)
    def test_body_and_public_promotion_rejected(self):
        self.data['items'][0]['body']='not allowed'
        with self.assertRaises(ValueError):validate(self.data)
        self.data['items'][0].pop('body');self.data['public_status']='APPROVED'
        with self.assertRaises(ValueError):validate(self.data)
    def test_script_text_escaped_in_js(self):
        self.data['items'][0]['title']='</script><script>alert(1)</script>'
        self.assertNotIn('</script>',asset(self.data))
    def test_timezone_required(self):
        self.data['updated_at']='2026-10-10T12:00:00'
        with self.assertRaises(ValueError):validate(self.data)
    def test_robots_denial_prevents_feed_request(self):
        with patch('scripts.tech_news.request_bytes',return_value=b'User-agent: *\nDisallow: /') as mock:
            with self.assertRaises(ValueError):fetch('samsung-kr')
            self.assertEqual(mock.call_count,1)
    def test_redirect_not_followed(self):
        from scripts.tech_news import NoRedirect
        with self.assertRaises(ValueError):NoRedirect().redirect_request(None,None,302,'',{},'https://evil.test/')
    def test_atom_supported(self):
        raw=b'<feed xmlns="http://www.w3.org/2005/Atom"><entry><title>Update</title><link href="https://news.samsung.com/test"/><published>2026-10-10T10:00:00Z</published></entry></feed>'
        self.assertEqual(len(parse(raw,'samsung-kr',STAMP)),1)

if __name__=='__main__':unittest.main()
