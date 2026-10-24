import json
from pathlib import Path
import re
import tempfile
import threading
import unittest
import urllib.request
from http.server import ThreadingHTTPServer

from scripts import prepare_monipick_brand_review as brand
from scripts.prepare_monipick_seo_review import review_artifacts
from scripts.validate_local_site import Document,forbidden_schema
from scripts.build_monipick_cloudflare import content_fingerprint,read_seo_approval,NAVER_PROOF


class BrandReviewTests(unittest.TestCase):
    def test_graphs_cover_indexable_pages_without_invented_product_or_rating(self):
        plan,artifacts=brand.brand_artifacts();counts={}
        for page in plan['pages']:
            text=artifacts[page['source']].decode();doc=Document(text)
            self.assertEqual(len(doc.jsonld),int(page['sitemap_candidate']))
            if not doc.jsonld:continue
            data=json.loads(doc.jsonld[0]);self.assertEqual(list(forbidden_schema(data)),[])
            nodes=data['@graph'];self.assertEqual(len({n['@id']for n in nodes}),len(nodes))
            webpage=next(n for n in nodes if n['@type']=='WebPage')
            self.assertEqual(webpage['url'],doc.canonicals[0])
            self.assertEqual(webpage['name'],doc.titles[0])
            self.assertEqual(webpage['description'],doc.meta['description'][0])
            for node in nodes:counts[node['@type']]=counts.get(node['@type'],0)+1
        self.assertEqual(counts,{'WebSite':1,'WebPage':34,'BreadcrumbList':30})
        self.assertEqual(artifacts['index.html'],artifacts['monitor-v3.html'])

    def test_breadcrumbs_match_the_actual_visible_hierarchy(self):
        plan,artifacts=brand.brand_artifacts()
        for page in plan['pages']:
            if not re.fullmatch(r'monitors/[^/]+/index.html',page['source']):continue
            text=artifacts[page['source']].decode();data=json.loads(Document(text).jsonld[0])
            items=next(n for n in data['@graph']if n['@type']=='BreadcrumbList')['itemListElement']
            self.assertEqual([n['position']for n in items],[1,2,3])
            self.assertEqual([n['item']for n in items],[brand.ORIGIN+'/',brand.ORIGIN+'/monitors/',page['proposed_canonical']])
            self.assertEqual(items[-1]['name'],re.search(r'<h1>(.*?)</h1>',text)[1])

    def test_visible_design_assets_policies_and_approved_production_do_not_change(self):
        _,base=review_artifacts();_,proposed=brand.brand_artifacts()
        for name,value in base.items():
            if name.endswith('.html') and not name.startswith('naver'):
                self.assertEqual(value.split(b'<body',1)[1],proposed[name].split(b'<body',1)[1],name)
                a,b=Document(value.decode()),Document(proposed[name].decode())
                self.assertEqual(a.meta['robots'],b.meta['robots']);self.assertEqual(a.canonicals,b.canonicals)
            else:self.assertEqual(value,proposed[name],name)
        self.assertEqual(content_fingerprint({n:brand.digest(v)for n,v in base.items()if n!=NAVER_PROOF}),read_seo_approval()['approved_content_fingerprint'])

    def test_share_and_icon_tags_use_current_origin_and_real_assets(self):
        plan,a=brand.brand_artifacts()
        for page in plan['pages']:
            text=a[page['source']].decode()
            self.assertIn('sizes="48x48"',text);self.assertIn('sizes="192x192"',text)
            if page['source']=='404.html':continue
            self.assertEqual(text.count('property="og:image"'),1)
            self.assertIn(brand.ORIGIN+brand.SHARE,text)
            self.assertIn('summary_large_image',text)
        self.assertEqual(a['favicon.ico'],a['assets/brand/favicon.ico'])

    def test_script_safe_json_round_trip(self):
        value={'name':'A </script><script>alert(1)</script> & <b> model'}
        serialized=brand.safe_json(value)
        self.assertNotIn('<',serialized);self.assertNotIn('&',serialized)
        self.assertEqual(json.loads(serialized),value)

    def test_duplicate_or_unmatched_schema_is_rejected(self):
        plan,a=brand.brand_artifacts()
        p=next(p for p in plan['pages']if p['source']=='monitors/dell-u2724d/index.html')
        text=a[p['source']].decode().replace('href="/monitors/">전체 모니터','href="/">전체 모니터')
        with self.assertRaises(ValueError):brand.structured_data(p,text)

    def test_review_cannot_silently_grant_approval_or_accept_changed_assets(self):
        with tempfile.TemporaryDirectory()as tmp:
            out=Path(tmp)/'brand';manifest=brand.build_brand_review(out)
            self.assertEqual(brand.validate_brand_review(out),[])
            for flag in brand.HOLDS:self.assertFalse(manifest[flag])
            img=out/'site/assets/brand/monipick-share-v1.png';raw=img.read_bytes();img.write_bytes(raw+b'changed')
            self.assertTrue(brand.validate_brand_review(out));img.write_bytes(raw)
            m=out/'manifest.json';d=json.loads(m.read_text());d['publication_authorized']=True;m.write_text(json.dumps(d))
            self.assertTrue(brand.validate_brand_review(out))
            with self.assertRaises(ValueError):brand.build_brand_review(out)

    def test_local_assets_are_served_with_correct_mime_and_existing_security(self):
        with tempfile.TemporaryDirectory()as tmp:
            out=Path(tmp)/'brand';brand.build_brand_review(out)
            server=ThreadingHTTPServer(('127.0.0.1',0),brand.handler_for(out,brand.validate_brand_review))
            worker=threading.Thread(target=server.serve_forever,daemon=True);worker.start()
            try:
                for name,mime in [('monipick-share-v1.png','image/png'),('favicon.svg','image/svg+xml'),('favicon.ico','image/vnd.microsoft.icon')]:
                    with urllib.request.urlopen(f'http://127.0.0.1:{server.server_port}/assets/brand/{name}')as r:
                        self.assertEqual(r.status,200);self.assertEqual(r.headers.get_content_type(),mime)
                        self.assertIn("script-src 'self'",r.headers['Content-Security-Policy'])
            finally:server.shutdown();server.server_close();worker.join()
