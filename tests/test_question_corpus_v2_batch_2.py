"""Batch 2 migration evidence and separation regressions."""
import hashlib
import json
import unittest
from test_question_corpus_v2_batch_1 import ROOT, v2

BATCH = {'UQ-0013', 'UQ-0015', 'UQ-0017', 'UQ-0019', 'UQ-0020', 'UQ-0023'}

class MigrationBatch2Tests(unittest.TestCase):
    def setUp(self):
        self.raw = v2.DEFAULT_FILE.read_bytes()
        self.records = {r['id']: r for r in map(json.loads, self.raw.splitlines())}

    def test_sixteen_unique_valid_records(self):
        snapshot = list(map(json.loads, self.raw.splitlines()[:16]))
        self.assertEqual(len(snapshot), 16)
        self.assertTrue(BATCH.issubset(self.records))
        self.assertEqual(v2.validate_files([v2.DEFAULT_FILE]), [])
        self.assertEqual(len({v2.url_key(r['source']['source_url']) for r in snapshot}), 16)

    def test_existing_ten_lines_byte_preserved(self):
        prefix = b''.join(self.raw.splitlines(keepends=True)[:10])
        self.assertEqual(hashlib.sha256(prefix).hexdigest(), 'a2cf4fd3affe9c32179500188c048023816ad78c7557452b048fdef2c41a825d')

    def test_initial_and_replacement_adapters_are_distinct(self):
        r = self.records['UQ-0013']
        cfg = {c['id']: c for c in r['configurations']}
        self.assertIn('first_adapter', cfg['cfg_first']['node_ids'])
        self.assertNotIn('final_adapter', cfg['cfg_first']['node_ids'])
        self.assertIn('final_adapter', cfg['cfg_final']['node_ids'])
        obs = {o['id']: o for o in r['observations']}
        self.assertEqual(obs['o_first']['counts']['mirrored'], 2)
        self.assertEqual(obs['o_final']['counts']['independent_extended'], 2)
        self.assertEqual(r['review']['commercial_context']['advertising'], 'YES')

    def test_detection_is_not_screen_illumination_or_resolution(self):
        r = self.records['UQ-0015']
        obs = {o['id']: o for o in r['observations']}
        self.assertEqual(obs['o_detected']['signal_state'], 'UNKNOWN')
        self.assertNotIn('lit', obs['o_detected']['counts'])
        self.assertEqual(obs['o_dark']['counts']['lit'], 0)
        self.assertEqual(r['outcome']['status'], 'UNRESOLVED')
        self.assertEqual(r['configuration_conclusions'], [])

    def test_account_comparison_and_unknown_remedy(self):
        r = self.records['UQ-0017']
        self.assertEqual(r['outcome']['status'], 'SUCCESS')
        self.assertFalse(any(a['configuration_id'] in {'cfg_advice','cfg_final'} for a in r['attempts']))
        self.assertIn('미상', next(c for c in r['configurations'] if c['id']=='cfg_final')['notes'])
        for o in r['observations']:
            self.assertEqual(o['counts']['scope'], 'UNKNOWN')
            self.assertNotIn('lit', o['counts'])

    def test_selection_cap_and_typo_do_not_become_output_resolution(self):
        r = self.records['UQ-0019']
        self.assertTrue(any('2556*1440' in e['summary'] for e in r['evidence']))
        for o in r['observations']:
            for state in o['display_states']:
                self.assertNotIn('resolution', state)
        self.assertEqual(len(r['attempts']), 1)
        self.assertEqual(r['configuration_conclusions'], [])

    def test_desktop_and_comparison_sources_and_power_are_separate(self):
        r = self.records['UQ-0020']
        cfg = {c['id']: c for c in r['configurations']}
        self.assertIn('comparison_src', cfg['cfg_comparison']['node_ids'])
        self.assertNotIn('src', cfg['cfg_comparison']['node_ids'])
        self.assertIn('power', cfg['cfg_desktop_power']['node_ids'])
        self.assertTrue(any(e['purpose']=='POWER' for e in cfg['cfg_desktop_power']['edges']))
        self.assertTrue(all(o['pd_charging']=='UNKNOWN' for o in r['observations']))
        self.assertEqual(r['outcome']['status'], 'UNRESOLVED')
        self.assertEqual(r['configuration_conclusions'], [])

    def test_hdr_playback_is_separate_from_transport_signal(self):
        r = self.records['UQ-0023']
        obs = {o['id']: o for o in r['observations']}
        self.assertEqual(obs['o_on_signal']['signal_state'], 'NORMAL')
        self.assertIn('끊김', obs['o_on_playback']['summary'])
        self.assertEqual(obs['o_off_playback']['display_states'][0]['hdr'], 'NO')
        self.assertEqual(r['goal']['display_states'][0]['hdr'], 'YES')
        self.assertEqual(r['outcome']['status'], 'LIMITED_SUCCESS')

    def test_evidence_provenance_and_compatibility_restrictions(self):
        for id in BATCH:
            r=self.records[id]
            self.assertEqual(r['review']['usable_for_compatibility'], 'NO')
            self.assertEqual(r['review']['official_comparison'], 'NOT_CHECKED')
            self.assertEqual({e['origin'] for e in r['evidence']}, {'DIRECT_CHECK','MIGRATED_V1'})
            advice={c['id'] for c in r['configurations'] if c['role']=='ADVICE'}
            self.assertFalse(any(a['configuration_id'] in advice for a in r['attempts']))
            self.assertFalse(any(c['status']=='FAILURE' for c in r['configuration_conclusions']))

if __name__ == '__main__':
    unittest.main()
