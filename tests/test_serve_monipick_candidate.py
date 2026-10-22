"""Real loopback HTTP behavior of the prepared output; not a CDN simulation."""
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
from pathlib import Path
import tempfile
import threading
import unittest
from scripts.build_monipick_public_candidate import build_candidate
from scripts.serve_monipick_candidate import handler_for


class CandidateHTTPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory()
        cls.output=Path(cls.temp.name)/'candidate'
        build_candidate(cls.output)
        handler=handler_for(cls.output)
        handler.log_message=lambda *args:None
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),handler)
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown();cls.server.server_close();cls.thread.join();cls.temp.cleanup()

    def request(self,path,method='GET'):
        connection=HTTPConnection('127.0.0.1',self.server.server_port,timeout=5)
        try:
            connection.request(method,path)
            r=connection.getresponse()
            return r.status,dict(r.getheaders()),r.read()
        finally:connection.close()

    def test_real_200_and_404_with_security_headers(self):
        for path,status in [('/',200),('/information',200),('/monitors/',200),
                            ('/monitors/asus-pa279crv/',200),('/monitor-v3.js',200),
                            ('/missing',404),('/monitors/missing/',404)]:
            with self.subTest(path=path):
                code,headers,body=self.request(path)
                self.assertEqual(code,status)
                self.assertEqual(headers['X-Frame-Options'],'DENY')
                self.assertIn("script-src 'self'",headers['Content-Security-Policy'])
                self.assertEqual(headers['X-Content-Type-Options'],'nosniff')
                if status==404:self.assertIn('페이지를 찾을 수 없어요.'.encode(),body)

    def test_excluded_pages_keep_noindex(self):
        for path in ['/tech-news','/monitor10-review','/404']:
            self.assertEqual(self.request(path)[1]['X-Robots-Tag'],'noindex, follow')
        self.assertNotIn('X-Robots-Tag',self.request('/')[1])

    def test_redirect_query_and_head_are_explicit(self):
        code,headers,body=self.request('/monitor-v3.html?q=4k')
        self.assertEqual((code,headers['Location'],body),(301,'/?q=4k',b''))
        code,headers,body=self.request('/information.html')
        self.assertEqual((code,headers['Location']),(308,'/information'))
        self.assertEqual(self.request('/monitors')[1]['Location'],'/monitors/')
        self.assertEqual(self.request('/',method='HEAD')[2],b'')

    def test_internal_files_and_path_traversal_are_not_served(self):
        for path in ['/_headers','/_redirects','/manifest.json','/activation-drafts/',
                     '/.git/config','/data/research/user_questions.csv']:
            self.assertEqual(self.request(path)[0],404)
        self.assertEqual(self.request('/%2e%2e/README.md')[0],400)


if __name__=='__main__':unittest.main()
