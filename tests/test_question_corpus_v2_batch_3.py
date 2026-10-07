"""Final pilot migration regressions and historical-byte preservation."""
import hashlib
import json
import unittest
from test_question_corpus_v2_batch_1 import ROOT, v2

class MigrationBatch3Tests(unittest.TestCase):
    def setUp(self):
        self.raw=v2.DEFAULT_FILE.read_bytes()
        self.records={r['id']:r for r in map(json.loads,self.raw.splitlines())}

    def test_twenty_records_and_prior_sixteen_bytes(self):
        self.assertEqual(len(self.records),20)
        self.assertEqual(v2.validate_files([v2.DEFAULT_FILE]),[])
        prefix=b''.join(self.raw.splitlines(keepends=True)[:16])
        self.assertEqual(hashlib.sha256(prefix).hexdigest(),'e3fef6418cbebad247bff1790e25f84b480edecaef81933bfb542e0d5f04a1f6')

    def test_recurrence_and_planned_clamshell(self):
        r=self.records['UQ-0011'];obs={o['id']:o for o in r['observations']}
        self.assertEqual(obs['o_hdmi']['durability'],'TEMPORARY')
        self.assertEqual(obs['o_recurrence']['durability'],'RECURRENT')
        self.assertEqual(obs['o_recurrence']['recurrence_of'],'o_hdmi')
        self.assertFalse(any(o['clamshell']=='YES' for o in r['observations']))

    def test_internal_scale_does_not_become_external_resolution(self):
        r=self.records['UQ-0016'];o=next(o for o in r['observations'] if o['id']=='o_open')
        self.assertEqual(o['display_states'][0]['node_id'],'internal')
        self.assertEqual(o['clamshell'],'NO')
        self.assertEqual(r['outcome']['status'],'UNRESOLVED')
        self.assertFalse(any('再起動' in a['action'] or '재부팅' in a['action'] for a in r['attempts']))

    def test_successful_dp_does_not_copy_target_pixel_count(self):
        r=self.records['UQ-0018'];o=next(o for o in r['observations'] if o['id']=='o_final')
        self.assertNotIn('resolution',o['display_states'][0])
        cfg=next(c for c in r['configurations'] if c['id']=='cfg_final')
        self.assertEqual(cfg['topology_completeness'],'PARTIAL')
        self.assertTrue(any(e['path_status']=='UNKNOWN_GAP' for e in cfg['edges']))
        self.assertEqual(len(r['attempts']),11)

    def test_companion_screen_and_final_cable_are_separate(self):
        r=self.records['UQ-0021'];cfg={c['id']:c for c in r['configurations']}
        self.assertIn('portable',cfg['cfg_multi_low']['node_ids'])
        self.assertNotIn('portable',cfg['cfg_removed']['node_ids'])
        self.assertNotIn('portable',cfg['cfg_final']['node_ids'])
        o=next(o for o in r['observations'] if o['id']=='o_final')
        self.assertEqual(o['display_states'][0]['hz'],144)
        self.assertNotIn('resolution',o['display_states'][0])
        self.assertEqual(r['configuration_conclusions'][0]['status'],'SUCCESS')

if __name__=='__main__':unittest.main()
