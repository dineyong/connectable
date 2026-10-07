"""Ensure the mockup projection never becomes an independent evidence dataset."""
import importlib.util
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('mockup_cases',ROOT/'scripts/build_mockup_cases.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class MockupProjectionTests(unittest.TestCase):
    def setUp(self):
        self.payload=module.build()
        self.records=json.loads(self.payload.split('window.CONNECTABLE_CASES = ',1)[1].removesuffix(';\n'))
        self.source={r['id']:r for r in map(json.loads,(ROOT/'data/research/user_questions_v2.jsonl').read_text().splitlines())}

    def test_generated_asset_is_reproducible(self):
        self.assertEqual((ROOT/'web/cases.js').read_text(),self.payload)

    def test_projection_preserves_evidence_and_results(self):
        self.assertEqual({r['id'] for r in self.records},set(self.source))
        for r in self.records:
            original=self.source[r['id']]
            self.assertEqual(r['outcome'],original['outcome']['status'])
            self.assertEqual(r['url'],original['source']['source_url'])
            self.assertEqual(r['summary'],original['outcome']['summary'])
            self.assertEqual(r['observations'],[o['summary'] for o in original['observations']])

    def test_projection_does_not_create_compatibility_claims(self):
        for r in self.records:
            self.assertNotIn('compatible',r)
            self.assertNotIn('max_resolution',r)
            self.assertNotIn('max_refresh',r)
            self.assertEqual(self.source[r['id']]['review']['usable_for_compatibility'],'NO')

    def test_generated_script_cannot_contain_html_tags(self):
        self.assertNotIn('<',self.payload)

if __name__=='__main__':
    unittest.main()
