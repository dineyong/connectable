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


class InputBoundaryTests(unittest.TestCase):
    def test_generator_rejects_unknown_original_redirect_metadata(self):
        pilot = builder.read(builder.INPUTS[0])
        pilot['sources'][0]['final_url'] = 'https://evil.example/spec'
        original = builder.read
        with patch.object(builder, 'read', side_effect=lambda p: copy.deepcopy(pilot) if p == builder.INPUTS[0] else original(p)):
            with self.assertRaises(ValueError):
                builder.build()

    def test_other_model_fact_source_rejected(self):
        d = builder.build()
        s = copy.deepcopy(d['monitors'][2]['source_refs'][0])
        d['monitors'][0]['source_refs'].append(s)
        d['monitors'][0]['features'][0]['source_refs'] = [s['record_id']]
        with self.assertRaises(ValueError):
            validate_content(d)

    def test_sku_promotion_rejected_in_content(self):
        d = builder.build()
        r = next(r for r in d['reviews'] if r.get('monitor_links'))
        r['monitor_links'][0]['variant_match'] = 'EXACT_SKU'
        r['monitor_links'][0]['match_scope'] = 'SKU'
        with self.assertRaises(ValueError):
            validate_content(d)

    def test_public_or_human_approval_promotion_rejected(self):
        for key,value in [('public_status','COMPATIBLE'), ('review_status','APPROVED')]:
            d = builder.build()
            d['monitors'][0][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                validate_content(d)

    def test_partial_mode_cannot_be_promoted(self):
        d = json.loads(PATH.read_text())
        r = d['manual_reviews'][1]
        r['verified_fields'].append('mode')
        r['unverified_fields'].remove('mode')
        with self.assertRaises(ValueError):
            validate(d)

    def test_unverified_payload_mutation_rejected(self):
        d = json.loads(PATH.read_text())
        d['assertions'][0]['payload']['width'] = 9999
        d['assertions'][0]['summary'] = '확인 해상도 미상'
        d['assertions'][0]['verified_fields'] = ['scope']
        with self.assertRaises(ValueError):
            validate(d)

    def test_mapping_observation_input_is_validated_before_build(self):
        records = builder.read(builder.INPUTS[3])
        records[0]['mapping']['observations'][0]['configuration_id'] = 'missing'
        original = builder.read
        with patch.object(builder, 'read', side_effect=lambda p: copy.deepcopy(records) if p == builder.INPUTS[3] else original(p)):
            with self.assertRaises(ValueError):
                builder.build()

    def test_corpus_duplicate_input_rejected_before_build(self):
        records = builder.read(builder.INPUTS[4])
        records.append(copy.deepcopy(records[0]))
        original = builder.read
        with patch.object(builder, 'read', side_effect=lambda p: copy.deepcopy(records) if p == builder.INPUTS[4] else original(p)):
            with self.assertRaises(ValueError):
                builder.build()

    def test_partial_fact_approval_and_review_approval_rejected(self):
        d = builder.build()
        m = next(m for m in d['monitors'] if 'crossover' in m['id'])
        m['features'][1]['review_status'] = 'APPROVED'
        with self.assertRaises(ValueError):
            validate_content(d)

    def test_protocol_unknown_mode_cannot_bypass_typed_contract(self):
        from scripts.site_content_validation import payload
        f = {'property':'PROTOCOL','summary':'수동 문장', 'payload':{'interface':'USB_C','protocol':'DISPLAYPORT','mode':'NOT_A_MODE','support':'SUPPORTED'}}
        with self.assertRaises(ValueError):
            payload(f, 'test')
