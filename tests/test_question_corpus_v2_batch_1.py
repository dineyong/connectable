"""Batch 1 regressions for observed/target separation and source preservation."""
import csv
import hashlib
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('batch_v2_validator', ROOT / 'scripts/validate_question_corpus_v2.py')
v2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v2)
BATCH = {'UQ-0014', 'UQ-0024', 'UQ-0025', 'UQ-0006', 'UQ-0008'}


class MigrationBatch1Tests(unittest.TestCase):
    def setUp(self):
        self.raw = v2.DEFAULT_FILE.read_bytes()
        self.records = {r['id']: r for r in map(json.loads, self.raw.splitlines())}

    def test_ten_records_validate_with_unique_ids_and_urls(self):
        self.assertEqual(len(self.records), 10)
        self.assertTrue(BATCH.issubset(self.records))
        self.assertEqual(v2.validate_files([v2.DEFAULT_FILE]), [])
        self.assertEqual(len({v2.url_key(r['source']['source_url']) for r in self.records.values()}), 10)

    def test_v1_files_and_prior_v2_prefix_preserved_byte_for_byte(self):
        expected = {
            'data/research/user_questions.csv': 'e2da17baec6dd9343777737ecbad40651df9a670d43bf6d4fb6b9f93da388570',
            'data/research/user_questions.example.csv': 'f8083e85e996513df348b52ec0497570c1fbcefaeb947cd0acd864dcfb9d6a27',
        }
        for path, digest in expected.items():
            self.assertEqual(hashlib.sha256((ROOT / path).read_bytes()).hexdigest(), digest)
        prefix = b''.join(self.raw.splitlines(keepends=True)[:5])
        self.assertEqual(hashlib.sha256(prefix).hexdigest(), 'a3dcf04b2f6d576723ca4f16c471ce5bf32ebb36ccac84e7370de404432a9d9d')

    def test_all_migration_hashes_and_outcomes_match_v1(self):
        with (ROOT / 'data/research/user_questions.csv').open(newline='', encoding='utf-8') as f:
            rows = {r['id']: r for r in csv.DictReader(f)}
        for record in self.records.values():
            old = rows[record['id']]
            digest = hashlib.sha256(json.dumps(old, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
            self.assertEqual(record['migration']['row_sha256'], digest)
            self.assertEqual(record['outcome']['status'], old['outcome'])

    def test_update_problem_does_not_become_successful_advice_attempt(self):
        r = self.records['UQ-0014']
        self.assertEqual(r['environment']['os_version'], 'Monterey 12.5.1')
        self.assertEqual(r['outcome']['status'], 'UNRESOLVED')
        advice = {c['id'] for c in r['configurations'] if c['role'] == 'ADVICE'}
        self.assertTrue(advice)
        self.assertFalse(any(a['configuration_id'] in advice for a in r['attempts']))
        self.assertEqual(r['configuration_conclusions'], [])

    def test_port_comparison_uses_two_display_ports_without_terminal_failure(self):
        r = self.records['UQ-0024']
        ports = {p['id']: p for p in r['ports']}
        self.assertEqual(ports['display_lightning']['node_id'], 'display')
        self.assertEqual(ports['display_icon']['node_id'], 'display')
        observed = {o['configuration_id']: o['signal_state'] for o in r['observations']}
        self.assertEqual(observed, {'cfg_lightning': 'NORMAL', 'cfg_icon': 'NO_SIGNAL'})
        self.assertEqual(r['configuration_conclusions'], [])
        self.assertEqual({a['sequence_basis'] for a in r['attempts']}, {'UNORDERED'})

    def test_purchase_candidates_are_only_targets_and_thanks_is_not_success(self):
        r = self.records['UQ-0025']
        self.assertEqual(r['case_classification']['types'], ['PRE_PURCHASE_QUESTION'])
        for cfg in r['configurations']:
            if {'planned_hub', 'planned_c_dp'} & set(cfg['node_ids']):
                self.assertEqual(cfg['role'], 'TARGET')
        self.assertEqual(r['attempts'], [])
        self.assertEqual(r['outcome']['status'], 'UNKNOWN')
        self.assertEqual({o['configuration_id'] for o in r['observations']}, {'cfg_current'})
        self.assertEqual(r['nodes'][0]['evidence_refs'], ['e_model_v1'])
        self.assertEqual(next(e for e in r['evidence'] if e['id'] == 'e_model_v1')['origin'], 'MIGRATED_V1')

    def test_direct_hdmi_and_hub_limit_have_separate_observations(self):
        r = self.records['UQ-0006']
        observations = {o['id']: o for o in r['observations']}
        self.assertEqual(observations['o_direct']['display_states'][0]['hz'], 60)
        self.assertEqual(observations['o_hub_30']['display_states'][0]['hz'], 30)
        self.assertNotEqual(observations['o_direct']['configuration_id'], observations['o_hub_30']['configuration_id'])
        self.assertEqual(r['outcome']['status'], 'LIMITED_SUCCESS')

    def test_55hz_50hz_video_and_audio_remain_distinct(self):
        r = self.records['UQ-0008']
        observations = {o['id']: o for o in r['observations']}
        self.assertEqual(observations['o_55']['signal_state'], 'INTERMITTENT')
        self.assertEqual(observations['o_55']['display_states'][0]['hz'], 55)
        self.assertEqual(observations['o_50_video']['signal_state'], 'NORMAL')
        self.assertEqual(observations['o_50_video']['display_states'][0]['hz'], 50)
        self.assertIn('스피커 미인식', observations['o_50_audio']['summary'])
        self.assertEqual(observations['o_50_video']['configuration_id'], observations['o_50_audio']['configuration_id'])
        self.assertIn('o_50_audio', r['outcome']['observation_ids'])

    def test_batch_does_not_infer_modes_dates_or_compatibility(self):
        for id in BATCH:
            r = self.records[id]
            self.assertEqual(r['review']['usable_for_compatibility'], 'NO')
            self.assertEqual(r['review']['official_comparison'], 'NOT_CHECKED')
            self.assertTrue(any(e['origin'] == 'DIRECT_CHECK' for e in r['evidence']))
            for o in r['observations']:
                self.assertNotIn('observed_on', o)
                self.assertNotIn('mirrored', o['counts'])
                self.assertNotIn('independent_extended', o['counts'])
            self.assertFalse(any(c['status'] == 'FAILURE' for c in r['configuration_conclusions']))


if __name__ == '__main__':
    unittest.main()
