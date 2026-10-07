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


class V2Tests(unittest.TestCase):
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

    def test_archived_proposed_records_are_not_active_v2_input(self):
        archived = ROOT / 'data/research/archive/user_questions_v2.example.jsonl'
        errors = v2.validate_files([archived])
        self.assertTrue(any('schema_version' in e and 'invalid enum' in e for e in errors))

    def test_actual_five_examples(self):
        self.assertEqual({r['id'] for r in self.records[:5]}, {'UQ-0007', 'UQ-0009', 'UQ-0010', 'UQ-0012', 'UQ-0022'})
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
        r = next(r for r in self.records if r['id'] == 'UQ-0022')
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
        self.error(expected='explicit author case termination')
        self.record['evidence'][0]['author_case_termination'] = dict(termination_type='ABANDONED_REPORTED', summary='작성자가 전체 목표의 사용 포기를 명시한 테스트 전용 진술')
        self.assertEqual(v2.validate_record(self.record), [])
        # Structural allowance is not evidence truth; fixture mutation is not saved.

    def config_failure(self, configuration_id='cfg_initial', termination='ABANDONED_REPORTED'):
        self.record['configuration_conclusions'] = [dict(configuration_id=configuration_id,
            status='FAILURE', termination_type=termination, evidence_refs=['e_post'],
            summary='해당 구성의 사용 포기를 명시한 테스트 전용 결론')]

    def declare_config_failure(self, configuration_id='cfg_initial', termination='ABANDONED_REPORTED'):
        self.record['evidence'][0]['author_configuration_terminations'] = [dict(
            configuration_id=configuration_id, termination_type=termination,
            summary='작성자가 해당 구성 사용을 최종 포기했다고 명시한 테스트 전용 근거')]

    def test_configuration_failure_without_explicit_declaration_rejected(self):
        self.config_failure()
        self.error(expected='scoped explicit author configuration termination')

    def test_no_signal_observation_is_insufficient_for_configuration_failure(self):
        self.config_failure()
        self.record['configuration_conclusions'][0]['observation_ids'] = ['o_initial']
        self.assertEqual(self.record['observations'][0]['signal_state'], 'NO_SIGNAL')
        self.error(expected='NO_SIGNAL or silence')

    def test_no_reply_is_insufficient_for_configuration_failure(self):
        self.config_failure()
        self.record['configuration_conclusions'][0]['summary'] = '작성자 후속 답변이 없음'
        self.error(expected='scoped explicit')

    def test_explicit_configuration_abandonment_keeps_case_success(self):
        self.config_failure()
        self.declare_config_failure()
        before = copy.deepcopy(self.record)
        self.assertEqual(v2.validate_record(self.record), [])
        self.assertEqual(self.record, before)
        self.assertEqual(self.record['outcome']['status'], 'SUCCESS')
        self.assertEqual(self.record['configuration_conclusions'][0]['status'], 'FAILURE')

    def test_final_failure_declaration_accepted(self):
        self.config_failure(termination='FINAL_FAILURE_REPORTED')
        self.declare_config_failure(termination='FINAL_FAILURE_REPORTED')
        self.assertEqual(v2.validate_record(self.record), [])

    def test_configuration_observations_are_optional(self):
        self.config_failure()
        self.declare_config_failure()
        self.assertNotIn('observation_ids', self.record['configuration_conclusions'][0])
        self.assertEqual(v2.validate_record(self.record), [])

    def test_wrong_configuration_declaration_rejected(self):
        self.config_failure()
        self.declare_config_failure('cfg_retry')
        self.error(expected='scoped explicit')

    def test_wrong_termination_declaration_rejected(self):
        self.config_failure()
        self.declare_config_failure(termination='FINAL_FAILURE_REPORTED')
        self.error(expected='scoped explicit')

    def test_unreferenced_declaration_cannot_support_failure(self):
        self.config_failure()
        declaration = copy.deepcopy(self.record['evidence'][0])
        declaration.update(id='e_terminal', author_configuration_terminations=[dict(
            configuration_id='cfg_initial', termination_type='ABANDONED_REPORTED', summary='테스트 전용 명시적 포기')])
        self.record['evidence'].append(declaration)
        self.error(expected='scoped explicit')

    def test_other_comment_cannot_declare_author_termination(self):
        self.config_failure()
        self.declare_config_failure()
        e = self.record['evidence'][0]
        e.update(kind='OTHER_COMMENT', actor='OTHER')
        self.error(expected='explicit termination must be a CASE_AUTHOR')

    def test_configuration_failure_does_not_prove_whole_case_failure(self):
        self.config_failure()
        self.declare_config_failure()
        self.record['outcome'].update(status='FAILURE', closure='ABANDONED_REPORTED')
        self.error(expected='explicit author case termination')

    def test_success_outcome_does_not_prove_configuration_termination(self):
        self.config_failure()
        self.assertEqual(self.record['outcome']['status'], 'SUCCESS')
        self.error(expected='scoped explicit')

    def test_configuration_termination_status_mismatch(self):
        self.config_failure()
        self.declare_config_failure()
        self.record['configuration_conclusions'][0]['status'] = 'SUCCESS'
        self.error(expected='status/termination_type')

    def test_conclusion_observation_must_match_configuration(self):
        self.config_failure()
        self.declare_config_failure()
        self.record['configuration_conclusions'][0]['observation_ids'] = ['o_final']
        self.error(expected='observation must belong')

    def test_target_configuration_cannot_be_abandoned_as_actual_configuration(self):
        self.config_failure('cfg_target')
        self.declare_config_failure('cfg_target')
        self.error(expected='OBSERVED configuration')

    def test_duplicate_configuration_conclusions_rejected(self):
        self.record['configuration_conclusions'].append(copy.deepcopy(self.record['configuration_conclusions'][0]))
        self.error(expected='duplicate items')

    def test_conflicting_conclusions_for_same_configuration_rejected(self):
        conclusion = copy.deepcopy(self.record['configuration_conclusions'][0])
        conclusion.update(status='LIMITED_SUCCESS', termination_type='PARTIAL_OR_CONDITIONAL')
        self.record['configuration_conclusions'].append(conclusion)
        self.error(expected='one conclusion per configuration')

    def test_configuration_conclusion_summary_is_short(self):
        self.record['configuration_conclusions'][0]['summary'] = '가' * 301
        self.error(expected='maximum string length')

    def test_explicit_termination_without_short_statement_rejected(self):
        self.config_failure()
        self.declare_config_failure()
        del self.record['evidence'][0]['author_configuration_terminations'][0]['summary']
        self.error(expected='required field')

    def test_optional_configuration_conclusions_can_be_omitted(self):
        del self.record['configuration_conclusions']
        self.assertEqual(v2.validate_record(self.record), [])

    def test_actual_examples_do_not_invent_terminal_failure(self):
        for r in self.records:
            self.assertFalse(any(c['status'] == 'FAILURE' for c in r['configuration_conclusions']))
            self.assertFalse(any('author_configuration_terminations' in e for e in r['evidence']))

    def test_long_term_type_requires_duration_or_continued_use_basis(self):
        self.record['case_classification']['types'] = ['LONG_TERM_REPORT']
        self.error(expected='explicit duration or continued-use basis')

    def test_explicit_long_term_use_basis_accepted(self):
        self.record['case_classification'].update(types=['LONG_TERM_REPORT'], long_term_basis=dict(
            kind='USE_DURATION_REPORTED', summary='작성자가 1년 사용을 명시한 테스트 전용 요약', evidence_refs=['e_post']))
        self.assertEqual(v2.validate_record(self.record), [])

    def test_commercial_review_required(self):
        del self.record['review']['commercial_context']
        self.error(expected='commercial_context')

    def test_affiliate_use_report_records_inclusion_basis(self):
        context = self.records[3]['review']['commercial_context']
        self.assertEqual(context['affiliate_links'], 'YES')
        self.assertEqual(context['sales_links'], 'YES')
        self.assertEqual(context['advertising'], 'UNKNOWN')
        self.assertTrue(context['inclusion_basis'])

    def test_mirror_and_extended_members_cannot_overlap(self):
        r = copy.deepcopy(self.records[0])
        r['observations'][0]['counts']['independent_extended'] = 1
        self.error(r, 'membership exceeds')

    def test_missing_mirror_count_does_not_hide_known_mirror_overlap(self):
        r = copy.deepcopy(self.records[0])
        del r['observations'][0]['counts']['mirrored']
        r['observations'][0]['counts']['independent_extended'] = 2
        self.error(r, 'overlap known display states')

    def test_missing_lit_count_does_not_allow_overlapping_connected_count(self):
        r = copy.deepcopy(self.record)
        counts = r['observations'][-1]['counts']
        del counts['lit']
        counts.update(independent_extended=2, mirrored=2)
        self.error(r, 'exceeds physical bound')

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
            v2.audit_schema({'type': 'array', 'maxItems': 1})

    def test_catalog_link_does_not_confirm_model_automatically(self):
        self.record['product_links'] = [dict(node_id='src', catalog_id='product:unverified', resolution='CONFIRMED', evidence_refs=['e_post'])]
        self.error(expected='invalid enum')

    def test_no_compatibility_approval_in_corpus_schema(self):
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
