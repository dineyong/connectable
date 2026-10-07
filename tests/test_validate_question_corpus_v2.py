"""Regression checks for provenance, temporal results and graph/count mistakes."""
import copy
import csv
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('v2_validator', ROOT / 'scripts/validate_question_corpus_v2.py')
v2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v2)


class ProposedV2Tests(unittest.TestCase):
    def setUp(self):
        self.records = [json.loads(line) for line in v2.DEFAULT_FILE.read_text().splitlines()]
        self.record = copy.deepcopy(self.records[2])
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / 'test.jsonl'

    def error(self, record=None, expected=''):
        errors = v2.validate_record(record if record is not None else self.record)
        self.assertTrue(errors)
        self.assertTrue(any(expected in e for e in errors), errors)

    def write(self, records):
        self.path.write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in records))
        return v2.validate_files([self.path])

    def test_actual_five_examples(self):
        self.assertEqual({r['id'] for r in self.records}, {'UQ-0007', 'UQ-0009', 'UQ-0010', 'UQ-0012', 'UQ-0022'})
        self.assertEqual(v2.validate_files([v2.DEFAULT_FILE]), [])

    def test_migration_preserves_v1_identity_and_row_hash(self):
        with (ROOT / 'data/research/user_questions.csv').open(encoding='utf-8', newline='') as stream:
            rows = {r['id']: r for r in csv.DictReader(stream)}
        for r in self.records:
            old = rows[r['id']]
            digest = hashlib.sha256(json.dumps(old, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
            self.assertEqual(r['migration']['row_sha256'], digest)
            self.assertEqual(r['migration']['legacy_outcome'], old['outcome'])
            self.assertEqual(r['source']['source_url'], old['source_url'])

    def test_home_mirroring_is_not_two_extended_displays(self):
        home = self.records[0]['observations'][0]
        self.assertEqual(home['counts']['lit'], 2)
        self.assertEqual(home['counts']['mirrored'], 2)
        self.assertEqual(home['counts']['independent_extended'], 0)
        self.assertEqual(self.records[0]['outcome']['status'], 'UNRESOLVED')

    def test_recurrence_has_earlier_temporary_success(self):
        observations = self.records[1]['observations']
        last = observations[-1]
        prior = next(o for o in observations if o['id'] == last['recurrence_of'])
        self.assertEqual(prior['durability'], 'TEMPORARY')
        self.assertEqual(last['durability'], 'RECURRENT')
        self.assertEqual(self.records[1]['outcome']['status'], 'LIMITED_SUCCESS')

    def test_source_parallel_paths_do_not_connect_cables_in_series(self):
        r = self.records[2]
        ports = {p['id']: p['node_id'] for p in r['ports']}
        cfg = r['configurations'][-1]
        paths = {(ports[e['from_port']], ports[e['to_port']]) for e in cfg['edges']}
        self.assertIn(('src', 'usb_cable'), paths)
        self.assertIn(('src', 'hdmi_replacement'), paths)
        self.assertNotIn(('usb_cable', 'hdmi_replacement'), paths)

    def test_hub_has_two_separate_display_branches(self):
        r = self.records[-1]
        ports = {p['id']: p['node_id'] for p in r['ports']}
        cfg = r['configurations'][-1]
        destinations = {ports[e['to_port']] for e in cfg['edges'] if ports[e['from_port']] == 'hub'}
        self.assertEqual(destinations, {'hdmi_vga', 'dp_cable'})
        self.assertEqual(r['observations'][-1]['counts']['lit'], 2)
        self.assertNotIn('pd_watts', r['observations'][-1])

    def test_no_signal_attempt_is_not_case_failure(self):
        r = self.records[3]
        self.assertTrue(any(o['signal_state'] == 'NO_SIGNAL' for o in r['observations']))
        self.assertEqual(r['outcome']['status'], 'SUCCESS')

    def test_optional_unknown_date_omitted(self):
        self.assertTrue(all('observed_on' not in o for o in self.record['observations']))
        self.assertEqual(v2.validate_record(self.record), [])

    def test_invalid_enum(self):
        self.record['outcome']['status'] = 'TEMPORARY_SUCCESS'
        self.error(expected='invalid enum')

    def test_missing_required_field(self):
        del self.record['evidence']
        self.error(expected='required field')

    def test_unknown_fields_forbid_username_and_official_specs(self):
        for key in ['username', 'official_specs']:
            r = copy.deepcopy(self.record)
            r[key] = 'forbidden'
            self.error(r, 'unknown field')

    def test_invalid_date(self):
        self.record['source']['checked_at'] = '2026-02-30'
        self.error(expected='invalid date')

    def test_invalid_url(self):
        for value in ['ftp://example.com', 'https://', 'https://user:pass@localhost', 'https://example.com:bad']:
            r = copy.deepcopy(self.record)
            r['source']['source_url'] = value
            self.error(r, 'HTTP(S)')

    def test_duplicate_id_across_files(self):
        self.write([self.record])
        self.assertTrue(any('duplicate corpus ID' in e for e in v2.validate_files([self.path, self.path])))

    def test_duplicate_canonical_url(self):
        other = copy.deepcopy(self.record)
        other['id'] = 'UQ-9000'
        other['migration']['source_record_id'] = other['id']
        other['source']['source_url'] += '?utm_source=test#comment'
        self.assertTrue(any('duplicate canonical URL' in e for e in self.write([self.record, other])))

    def test_mobile_and_pc_ppomppu_share_key(self):
        self.assertEqual(v2.url_key('https://m.ppomppu.co.kr/new/bbs_view.php?id=computer&no=10'), v2.url_key('https://www.ppomppu.co.kr/zboard/view.php?id=computer&no=10'))

    def test_duplicate_local_id(self):
        self.record['nodes'][1]['id'] = 'src'
        self.error(expected='duplicate local ID')

    def test_dangling_evidence(self):
        self.record['observations'][0]['evidence_refs'] = ['absent']
        self.error(expected='dangling evidence')

    def test_dangling_port(self):
        self.record['configurations'][-1]['edges'][0]['to_port'] = 'absent'
        self.error(expected='dangling port')

    def test_endpoint_outside_configuration(self):
        self.record['configurations'][-1]['node_ids'].remove('usb_cable')
        self.error(expected='endpoint outside')

    def test_video_cycle(self):
        e = copy.deepcopy(self.record['configurations'][-1]['edges'][0])
        e['id'] = 'cycle'
        e['from_port'], e['to_port'] = e['to_port'], e['from_port']
        self.record['configurations'][-1]['edges'].append(e)
        self.error(expected='video cycle')

    def test_complete_topology_cannot_hide_disconnected_display(self):
        self.record['configurations'][-1]['edges'].pop()
        self.error(expected='unreachable display')

    def test_unknown_gap_cannot_be_complete(self):
        self.record['configurations'][-1]['edges'][0]['path_status'] = 'UNKNOWN_GAP'
        self.error(expected='unknown gap')

    def test_other_comment_not_actual_result(self):
        self.record['evidence'].append(dict(id='e_advice', kind='OTHER_COMMENT', actor='OTHER', location='타인 댓글', checked_at='2026-10-07', summary='해결책 제안', origin='MIGRATED_V1'))
        self.record['observations'][0]['evidence_refs'] = ['e_advice']
        self.error(expected='CASE_AUTHOR')

    def test_other_comment_not_actual_setting(self):
        self.record['evidence'].append(dict(id='e_advice', kind='OTHER_COMMENT', actor='OTHER', location='타인 댓글', checked_at='2026-10-07', summary='해결책 제안', origin='MIGRATED_V1'))
        self.record['configurations'][-1]['settings'][0]['evidence_refs'] = ['e_advice']
        self.error(expected='CASE_AUTHOR')

    def test_observation_not_target(self):
        self.record['observations'][0]['configuration_id'] = 'cfg_target'
        self.error(expected='OBSERVED')

    def test_goal_not_observed(self):
        self.record['goal']['configuration_ids'] = ['cfg_final']
        self.error(expected='TARGET')

    def test_failure_requires_explicit_closure(self):
        self.record['outcome']['status'] = 'FAILURE'
        self.error(expected='status/closure')
        self.record['outcome']['closure'] = 'ABANDONED_REPORTED'
        self.assertEqual(v2.validate_record(self.record), [])
        # Structural allowance is not evidence truth; fixture mutation is not saved.

    def test_counts_cannot_exceed_lit_or_connected(self):
        self.record['observations'][-1]['counts']['independent_extended'] = 3
        self.error(expected='exceeds')

    def test_numeric_unknown_count_has_no_basis(self):
        self.record['observations'][-1]['counts']['basis'] = 'UNKNOWN'
        self.error(expected='stated basis')

    def test_lit_display_states_cannot_exceed_count(self):
        self.record['observations'][-1]['counts']['lit'] = 1
        self.error(expected='known lit display states')

    def test_display_scope_must_be_explicit(self):
        del self.record['nodes'][1]['display_scope']
        self.error(expected='display_scope')

    def test_goal_display_must_belong_to_target(self):
        self.record['goal']['display_states'] = [dict(node_id='usb_display', lit='YES', evidence_refs=['e_post'])]
        self.record['configurations'][0]['node_ids'].remove('usb_display')
        self.error(expected='outside target')

    def test_duplicate_publication_order(self):
        self.record['evidence'][0]['publication_sequence'] = 1
        other = copy.deepcopy(self.record['evidence'][0])
        other['id'] = 'e_other'
        self.record['evidence'].append(other)
        self.error(expected='duplicate publication order')

    def test_sequence_collision(self):
        self.record['observations'][-1]['sequence'] = 1
        self.error(expected='sequence')

    def test_recurrence_cannot_point_forward(self):
        r = copy.deepcopy(self.records[1])
        r['observations'][-1]['recurrence_of'] = r['observations'][-1]['id']
        self.error(r, 'earlier NORMAL')

    def test_count_rejects_bool_negative_null(self):
        for value in [True, -1, None]:
            r = copy.deepcopy(self.record)
            r['observations'][-1]['counts']['lit'] = value
            self.error(r, 'counts.lit')

    def test_non_finite_json_and_duplicate_keys(self):
        for value in ['{"x": NaN}\n', '{"id":"a","id":"b"}\n']:
            self.path.write_text(value)
            self.assertTrue(any('invalid JSON' in e for e in v2.validate_files([self.path])))

    def test_malformed_and_blank_line_location(self):
        self.path.write_text(json.dumps(self.record) + '\n\nnot-json\n')
        errors = v2.validate_files([self.path])
        self.assertTrue(any('line 2' in e for e in errors))
        self.assertTrue(any('line 3' in e for e in errors))

    def test_empty_example_rejected(self):
        self.path.write_text('')
        self.assertTrue(any('empty v2' in e for e in v2.validate_files([self.path])))

    def test_nested_wrong_type_does_not_crash(self):
        self.record['observations'] = [{}]
        self.error(expected='required field')

    def test_pii_and_secret_detection(self):
        for value in ['person' + '@' + 'example.com', '010' + '-1234-5678', 'AKIA' + 'Z' * 16, '메모: -----BEGIN ' + 'PRIVATE KEY-----']:
            r = copy.deepcopy(self.record)
            r['outcome']['summary'] = value
            self.error(r, 'personal information or secret')

    def test_confirmation_after_check_rejected(self):
        self.record['attempts'][-1]['author_confirmed_on'] = '2027-01-01'
        self.error(expected='confirmation after')

    def test_schema_unknown_keyword_fails_closed(self):
        with self.assertRaises(ValueError):
            v2.audit_schema({'type': 'string', 'maxLength': 1})

    def test_catalog_link_does_not_confirm_model_automatically(self):
        self.record['product_links'] = [dict(node_id='src', catalog_id='product:unverified', resolution='CONFIRMED', evidence_refs=['e_post'])]
        self.error(expected='invalid enum')

    def test_no_compatibility_approval_in_proposed_schema(self):
        self.record['review']['usable_for_compatibility'] = 'YES'
        self.error(expected='invalid enum')

    def test_original_v1_id_preserved(self):
        self.record['migration']['source_record_id'] = 'UQ-9999'
        self.error(expected='v1 ID')

    def test_fresh_record_does_not_require_migration(self):
        del self.record['migration']
        self.assertEqual(v2.validate_record(self.record), [])

    def test_cli_default_example(self):
        self.assertEqual(v2.main([]), 0)


if __name__ == '__main__':
    unittest.main()
