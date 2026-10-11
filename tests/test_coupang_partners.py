import hashlib
import hmac
import json
import unittest
from unittest.mock import patch,MagicMock
from scripts.coupang_partners import authorization,deeplink,PATH,NoRedirect

class CoupangPartnersTests(unittest.TestCase):
    def test_hmac_matches_official_message_order(self):
        stamp='261011T000000Z'
        expected=hmac.new(b'test-secret',(stamp+'POST'+PATH).encode(),hashlib.sha256).hexdigest()
        self.assertTrue(authorization('test-access','test-secret',stamp).endswith(expected))
    def test_unsafe_request_url_rejected_before_network(self):
        for url in ['https://www.coupang.com.evil.test/x','https://user@www.coupang.com/x','http://www.coupang.com/x','https://www.coupang.com:81/x']:
            with self.assertRaises(ValueError):deeplink(url)
    def test_keys_required(self):
        with patch.dict('os.environ',{},clear=True):
            with self.assertRaises(ValueError):deeplink('https://www.coupang.com/vp/products/1')
    def test_redirect_rejected(self):
        with self.assertRaises(ValueError):NoRedirect().redirect_request(None)
    def test_response_validation(self):
        url='https://www.coupang.com/vp/products/1'
        for target,valid in [('https://link.coupang.com/a/test',True),('https://link.coupang.com.evil.test/a/test',False)]:
            opener=MagicMock();opener.open.return_value.__enter__.return_value.read.return_value=json.dumps({'rCode':'0','data':[{'originalUrl':url,'shortenUrl':target}]}).encode()
            with patch.dict('os.environ',{'COUPANG_PARTNERS_ACCESS_KEY':'test','COUPANG_PARTNERS_SECRET_KEY':'test'}),patch('urllib.request.build_opener',return_value=opener):
                if valid:self.assertEqual(deeplink(url),target)
                else:
                    with self.assertRaises(ValueError):deeplink(url)
