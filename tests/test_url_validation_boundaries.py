"""Regression evidence for the integration-boundary review."""
import copy
import json
import unittest
from urllib.parse import quote
from unittest.mock import patch
from scripts import build_site_content_v2 as builder
from scripts.data_trust import official_url_status
from scripts.site_content_validation import validate_content
from scripts.validate_official_spec_review import PATH, validate


class URLBoundaryTests(unittest.TestCase):
    def test_decoded_controls_and_del_are_unknown(self):
        for s in ('%00', '%0A', '%0D', chr(127)):
            with self.subTest(suffix=s):
                self.assertEqual(official_url_status('https://www.dell.com/support/spec'+s, 'Dell'), 'UNKNOWN')

    def test_query_values_are_language_codes_not_encoded_urls(self):
        v = 'https://evil.example'
        for _ in range(5):
            v = quote(v, safe='')
        for value in (v, '%ZZ', '', 'english', 'en-us&&', 'en-us;url=evil'):
            with self.subTest(value=value):
                self.assertEqual(official_url_status('https://www.dell.com/support/spec?language='+value, 'Dell'), 'UNKNOWN')

    def test_legitimate_unicode_and_language_remain_valid(self):
        self.assertEqual(official_url_status('https://www.dell.com/pl-pl/shop/monitory-i-akcesoria-do-monitor%C3%B3w?language=en-us', 'Dell'), 'OFFICIAL_URL_SCOPE')


