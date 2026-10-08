"""Regression boundaries for the 18-case review sidecar, not compatibility truth."""
import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from scripts import validate_public_usage_review as review


class PublicUsageReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = {r['id']: (r, h) for _, r, h in review.read_jsonl(review.SOURCE)}
        cls.rows = [r for _, r, _ in review.read_jsonl(review.MAPPING)]
        cls.schema = review.review_schema()

    def row(self, n=1):
        return copy.deepcopy(self.rows[n-1])

    def errors(self, row):
        src, digest = self.sources[row['source_id']]
        return review.validate_record(row, src, digest, self.schema)

    def reject(self, row, fragment):
        errors = self.errors(row)
        self.assertTrue(any(fragment in e for e in errors), errors)

    def batch(self, rows, sources=None):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'mapped.jsonl'
            path.write_text(''.join(json.dumps(r, ensure_ascii=False)+'\n' for r in rows), encoding='utf-8')
            source = review.SOURCE
            if sources is not None:
                source = Path(directory)/'source.jsonl'
                source.write_text(''.join(json.dumps(r, ensure_ascii=False)+'\n' for r in sources), encoding='utf-8')
            return review.validate_files(path, source)

    def test_all_eighteen_real_mappings_validate(self):
        self.assertEqual(review.validate_files(), [])
        self.assertEqual({r['source_id'] for r in self.rows}, review.EXPECTED_IDS)

    def test_original_batch_bytes_are_frozen(self):
        self.assertEqual(hashlib.sha256(review.SOURCE.read_bytes()).hexdigest(),
                         '8131cea42edf5644c8fc5f276690c6f4767bf4e2a355dd000e037b6bc777eb43')

    def test_existing_v2_definitions_reused_without_fork(self):
        from scripts import validate_question_corpus_v2 as v2
        original = v2.load_schema()
        self.assertEqual(self.schema['$defs'], original['$defs'])
        for name in ('nodes', 'ports', 'observations', 'attempts', 'configurations', 'source'):
            self.assertEqual(self.schema['properties']['mapping']['properties'][name], original['properties'][name])

    def test_review_no_approval_or_catalog_binding(self):
        for r in self.rows:
            self.assertEqual((r['record_status'],r['public_status'],r['approved_gold_count']),('REVIEW_ONLY','UNKNOWN',0))
            self.assertEqual(r['mapping']['review']['reliability_grade'], 'C')
            self.assertEqual(r['mapping']['outcome']['status'], 'UNKNOWN')
            self.assertEqual(r['mapping']['product_links'], [])

    def test_third_party_advice_cannot_be_success_observation(self):
        r=self.row(4)
        r['mapping']['observations'][0]['evidence_refs']=['e_advice']
        self.reject(r,'cannot become an observation')

    def test_authors_purchase_plan_cannot_be_success(self):
        r=self.row(4)
        r['mapping']['observations'][0]['evidence_refs']=['e_plan']
        self.reject(r,'cannot become an observation')

    def test_author_advice_is_not_a_performed_change(self):
        r=self.row(11)
        r['mapping']['attempts'][0]['evidence_refs']=['e_advice']
        self.reject(r,'cannot become a performed change')

    def test_purchase_plan_is_not_a_performed_change(self):
        r=self.row(4); o=r['mapping']['observations'][0]
        r['mapping']['attempts']=[dict(id='a_plan',sequence=1,sequence_basis='UNORDERED',stage='UNKNOWN',configuration_id=o['configuration_id'],action='구매 계획',observation_ids=[o['id']],evidence_refs=['e_plan'])]
        self.reject(r,'cannot become a performed change')

    def test_product_description_is_not_an_author_result(self):
        r=self.row(12)
        r['mapping']['observations'][0]['evidence_refs']=['e_description']
        self.reject(r,'cannot become an observation')

    def test_advice_pointer_cannot_be_relabelled_author_observation(self):
        r=self.row(4)
        a=next(a for a in r['evidence_annotations'] if a['evidence_id']=='e_advice')
        a['statement_role']='AUTHOR_OBSERVATION'
        self.reject(r,'checked author observation')

    def test_ui_scale_cannot_be_signal_pixels(self):
        r=self.row(1); d=r['functional_observations'][0]
        d['signal_mode'].update(resolution_pixels='3008x1692',evidence_refs=d['ui_scale']['evidence_refs'])
        self.reject(r,'cannot become signal pixels')

    def test_core_resolution_cannot_bypass_scale_boundary(self):
        r=self.row(1)
        r['mapping']['observations'][0]['display_states'][0]['resolution']='3008x1692'
        self.reject(r,'cannot be copied from UI scale')

    def test_video_success_cannot_imply_pd(self):
        r=self.row(2); d=r['functional_observations'][-1]; o=r['mapping']['observations'][-1]
        d['pd'].update(recognized='YES',evidence_refs=o['evidence_refs']);o['pd_charging']='YES'
        self.reject(r,'PD_CHARGING requires scoped')

    def test_video_success_cannot_imply_wake(self):
        r=self.row(2); d=r['functional_observations'][-1]
        d['sleep_wake'].update(status='NORMAL',evidence_refs=d['video_output']['evidence_refs'])
        self.reject(r,'SLEEP_WAKE requires scoped')

    def test_video_success_cannot_imply_clamshell(self):
        r=self.row(2); d=r['functional_observations'][-1]
        d['clamshell'].update(status='NORMAL',evidence_refs=d['video_output']['evidence_refs'])
        self.reject(r,'CLAMSHELL requires scoped')

    def test_video_success_cannot_imply_reconnect(self):
        r=self.row(2); d=r['functional_observations'][-1]
        d['reconnect'].update(status='NORMAL',evidence_refs=d['video_output']['evidence_refs'])
        self.reject(r,'RECONNECT requires scoped')

    def test_unscoped_core_charging_value_cannot_bypass_detail(self):
        r=self.row(2);r['mapping']['observations'][-1]['pd_charging']='YES'
        self.reject(r,'charging value and scoped detail must agree')

    def test_advertised_watts_do_not_become_measured_power(self):
        r=self.row(12);r['functional_observations'][0]['pd']['watts']='100'
        self.reject(r,'not measured power')

    def test_relabelling_recognition_as_measurement_is_rejected(self):
        r=self.row(12)
        r['functional_observations'][0]['pd'].update(watts='100',power_basis='MEASURED')
        self.reject(r,'cannot become measured input power')

    def test_relabelling_selection_limit_as_output_is_rejected(self):
        r=self.row(4)
        r['functional_observations'][0]['signal_mode']['hz_basis']='REPORTED_OUTPUT'
        self.reject(r,'cannot promote a selection limit')

    def test_numeric_pd_core_value_requires_measurement(self):
        r=self.row(12);r['mapping']['observations'][0]['pd_watts']=100
        self.reject(r,'measured-power evidence')

    def test_selected_limit_is_not_actual_output_hz(self):
        r=self.row(4);r['mapping']['observations'][0]['display_states'][0]['hz']=30
        self.reject(r,'not actual output Hz')

    def test_black_screen_at_selected_144_is_not_output_144(self):
        r=self.row(17)
        d=r['functional_observations'][1]
        self.assertEqual((d['signal_mode']['hz'],d['signal_mode']['hz_basis'],d['video_output']['status']),('144','SELECTED_SETTING','PROBLEM'))
        self.assertNotIn('hz',r['mapping']['observations'][1]['display_states'][0])

    def test_selectable_4k_label_is_not_actual_resolution(self):
        r=self.row(11);o=r['mapping']['observations'][1]
        self.assertEqual(r['functional_observations'][1]['signal_mode']['label_basis'],'SELECTABLE_LABEL')
        self.assertNotIn('resolution_label',o['display_states'][0])
        o['display_states'][0]['resolution_label']='4K'
        self.reject(r,'selectable resolution label is not actual output')

    def test_ambiguous_lid_transition_not_bound_to_specific_hub(self):
        r=self.row(8);o=r['mapping']['observations'][3]
        cfg=next(c for c in r['mapping']['configurations'] if c['id']==o['configuration_id'])
        self.assertEqual(set(cfg['node_ids']),{'src','screen'})
        self.assertEqual(cfg['edges'][0]['path_status'],'UNKNOWN_GAP')

    def test_no_signal_does_not_become_case_failure(self):
        r=self.row(7);r['mapping']['outcome'].update(status='FAILURE',closure='FINAL_FAILURE_REPORTED')
        self.reject(r,'no catalog binding or case outcome approval')
        self.reject(r,'explicit author case termination')

    def test_missing_function_slot_is_an_error(self):
        r=self.row();del r['functional_observations'][0]['sleep_wake']
        self.reject(r,'required field missing')

    def test_missing_condition_slot_is_an_error(self):
        r=self.row();r['mapping']['configurations'][0]['settings']=[s for s in r['mapping']['configurations'][0]['settings'] if s['key']!='lid']
        self.reject(r,'explicit UNKNOWN')

    def test_unknown_slots_are_explicit_and_empty_evidence(self):
        for r in self.rows:
            for d in r['functional_observations']:
                for field in ('video_output','clamshell','sleep_wake','reconnect'):
                    if d[field]['status']=='UNKNOWN':self.assertEqual(d[field]['evidence_refs'],[])
            for n in r['mapping']['nodes']:
                self.assertIn('display_model',n)
                self.assertEqual(n['normalized_model'],'UNKNOWN')

    def test_unknown_function_cannot_borrow_video_evidence(self):
        r=self.row(2);d=r['functional_observations'][-1]
        d['sleep_wake']['evidence_refs']=d['video_output']['evidence_refs']
        self.reject(r,'UNKNOWN function cannot borrow')

    def test_user_report_cannot_be_independent_physical_test(self):
        r=self.row();r['evidence_annotations'][0]['basis']='INDEPENDENT_TEST'
        self.reject(r,'invalid enum')

    def test_user_report_cannot_be_official_spec(self):
        r=self.row();r['evidence_annotations'][0]['basis']='MANUFACTURER_SPEC'
        self.reject(r,'invalid enum')

    def test_source_hash_mismatch_rejected(self):
        r=self.row();r['source_line_sha256']='0'*64
        self.reject(r,'source line hash mismatch')

    def test_source_check_date_cannot_be_refreshed_without_check(self):
        r=self.row();r['mapping']['source']['checked_at']='2026-10-09'
        self.reject(r,'metadata must be preserved')

    def test_invalid_date_rejected(self):
        r=self.row();r['mapping']['source']['checked_at']='2026-02-30'
        self.reject(r,'invalid date')

    def test_invalid_url_rejected(self):
        r=self.row();r['mapping']['source']['source_url']='https://user:secret@example.com'
        self.reject(r,'HTTP(S)')

    def test_duplicate_id_and_missing_id_rejected(self):
        rows=copy.deepcopy(self.rows);rows[-1]=copy.deepcopy(rows[0])
        errors=self.batch(rows)
        self.assertTrue(any('duplicate review ID' in e for e in errors),errors)
        self.assertTrue(any('exactly all 18' in e for e in errors),errors)

    def test_removed_case_rejected(self):
        self.assertTrue(any('exactly all 18' in e for e in self.batch(self.rows[:-1])))

    def test_user_private_case_or_search_lead_cannot_enter_batch(self):
        rows=copy.deepcopy(self.rows);rows[-1]['source_id']='PUR-019'
        self.assertTrue(any('unknown source ID' in e for e in self.batch(rows)))

    def test_normalized_mobile_and_encoded_url_equivalence(self):
        self.assertEqual(review.normalized_url('https://example.tistory.com/m/entry/한글?utm_source=x#comment'), review.normalized_url('https://example.tistory.com/entry/%ED%95%9C%EA%B8%80'))

    def test_duplicate_normalized_source_url_rejected(self):
        sources=[copy.deepcopy(self.sources[r['source_id']][0]) for r in self.rows]
        sources[1]['source']['url']=sources[0]['source']['url']+'?utm_source=x#comment'
        rows=copy.deepcopy(self.rows)
        for r,src in zip(rows,sources):
            encoded=(json.dumps(src,ensure_ascii=False)+'\n').encode()
            r['source_line_sha256']=hashlib.sha256(encoded).hexdigest()
            r['mapping']['source']['source_url']=src['source']['url']
            r['semantic_review']['source_url']=src['source']['url']
        self.assertTrue(any('duplicate normalized URL' in e for e in self.batch(rows,sources)))

    def test_dangling_source_pointer_rejected(self):
        r=self.row();r['evidence_annotations'][0]['source_pointers']=['/missing-field']
        self.reject(r,'missing source pointer')

    def test_dangling_configuration_scope_rejected(self):
        r=self.row();r['evidence_annotations'][-1]['configuration_ids']=['missing_cfg']
        self.reject(r,'dangling configuration scope')

    def test_other_configuration_cannot_borrow_observation(self):
        r=self.row(2);r['functional_observations'][-1]['video_output']['evidence_refs']=r['mapping']['observations'][0]['evidence_refs']
        self.reject(r,'requires scoped author observation')

    def test_duplicate_local_port_id_rejected(self):
        r=self.row();r['mapping']['ports'].append(copy.deepcopy(r['mapping']['ports'][0]))
        self.reject(r,'duplicate')

    def test_missing_observation_details_rejected(self):
        r=self.row();r['functional_observations'].pop()
        self.reject(r,'every observation needs all function slots')

    def test_author_model_comment_kept_separate_from_body_and_advice(self):
        r=self.row(7);node=next(n for n in r['mapping']['nodes'] if n['id']=='src')
        e=next(e for e in r['mapping']['evidence'] if e['id']==node['evidence_refs'][0])
        self.assertEqual((e['kind'],e['actor']),('AUTHOR_COMMENT','CASE_AUTHOR'))
        self.assertEqual(node['chip'],'UNKNOWN')

    def test_source_model_ambiguity_not_corrected(self):
        for n in (6,7,11,14):
            r=self.row(n);node=next(x for x in r['mapping']['nodes'] if x['id']=='src')
            self.assertEqual(node['chip'],'UNKNOWN')
        self.assertEqual(self.row(14)['mapping']['nodes'][0]['display_model'],'UNKNOWN')

    def test_displaylink_not_native_and_mirror_count_not_invented(self):
        r=self.row(15)
        self.assertTrue(all(s['output_mode']=='DISPLAYLINK' for s in r['mapping']['observations'][0]['display_states']))
        for n in (13,15):
            for o in self.row(n)['mapping']['observations']:
                self.assertNotIn('independent_extended',o['counts'])
                self.assertNotIn('mirrored',o['counts'])

    def test_temporary_workaround_retains_recurrence(self):
        r=self.row(9);obs=r['mapping']['observations']
        self.assertEqual(obs[1]['durability'],'TEMPORARY')
        self.assertEqual((obs[2]['durability'],obs[2]['recurrence_of']),('RECURRENT',obs[1]['id']))

    def test_product_introduction_never_in_observed_configuration(self):
        r=self.row(10)
        self.assertTrue(any(n['display_model']=='Apple MUF82KH/A' for n in r['mapping']['nodes']))
        self.assertTrue(all('introduced_adapter' not in c['node_ids'] for c in r['mapping']['configurations'] if c['role']=='OBSERVED'))

    def test_pii_or_secret_pattern_rejected(self):
        for text in ('person@example.com','010-1234-5678','ghp_'+'a'*30):
            r=self.row();r['mapping']['review']['notes']=text
            self.reject(r,'personal information or secret')

    def test_unrecognized_personal_fields_rejected(self):
        r=self.row();r['username']='forbidden'
        self.reject(r,'unknown field')

    def test_jsonl_rejects_bom_crlf_missing_lf_blank_duplicate_keys_and_nan(self):
        for content in (b'\xef\xbb\xbf{}\n',b'{}\r\n',b'{}',b'{}\n\n',b'{"id":1,"id":2}\n',b'{"n":NaN}\n'):
            with self.subTest(content=content),tempfile.TemporaryDirectory() as d:
                p=Path(d)/'bad.jsonl';p.write_bytes(content)
                with self.assertRaises(ValueError):review.read_jsonl(p)


    def test_semantic_review_is_ai_only_and_all_sources_rechecked(self):
        for r in self.rows:
            self.assertIn(r['semantic_review']['status'], ('AI_MATCHED','AI_CORRECTED'))
            self.assertEqual(r['semantic_review']['access'],'BODY_DIRECT_CHECK')
            self.assertEqual(r['mapping']['review']['status'],'NEEDS_REVIEW')
            self.assertEqual(r['approved_gold_count'],0)

    def test_new_evidence_cannot_borrow_unavailable_review(self):
        r=self.row(8);r['semantic_review'].update(status='UNVERIFIED',access='UNAVAILABLE')
        self.reject(r,'direct recheck provenance')

    def test_semantic_evidence_actor_and_kind_must_match(self):
        r=self.row(3);r['semantic_review']['locations'][1]['actor']='OTHER'
        self.reject(r,'kind/actor must match')

    def test_new_semantic_pointer_cannot_point_to_missing_location(self):
        r=self.row(8)
        next(a for a in r['evidence_annotations'] if a['evidence_id']=='e_o_5')['source_pointers']=['/semantic_review/locations/99']
        self.reject(r,'missing source pointer')

    def test_hdmi_followup_not_merged_into_initial_success(self):
        r=self.row(3);o=next(o for o in r['mapping']['observations'] if o['id']=='o_5')
        self.assertNotEqual(o['signal_state'],'NORMAL')
        e=next(e for e in r['mapping']['evidence'] if e['id']=='e_followup_hdmi')
        self.assertEqual((e['kind'],e['actor']),('AUTHOR_COMMENT','CASE_AUTHOR'))
        self.assertEqual(r['mapping']['outcome']['status'],'UNKNOWN')

    def test_seven_in_one_video_does_not_inherit_six_in_one_modes(self):
        r=self.row(8);d=next(d for d in r['functional_observations'] if d['observation_id']=='o_5')
        self.assertEqual(d['video_output']['status'],'NORMAL')
        self.assertEqual(d['signal_mode']['hz'],'UNKNOWN')
        self.assertEqual(d['sleep_wake']['status'],'UNKNOWN')
        self.assertEqual(d['pd']['recognized'],'UNKNOWN')

    def test_stuttering_use_and_selectable_limit_remain_separate(self):
        d=self.row(4)['functional_observations'][0]
        self.assertEqual(d['video_output']['status'],'PROBLEM')
        self.assertEqual(d['signal_mode']['hz_basis'],'SELECTABLE_LIMIT')

    def test_cable_generation_and_added_post_time_not_inferred(self):
        r=self.row(14);n=next(n for n in r['mapping']['nodes'] if n['id']=='belkin')
        self.assertNotIn('TB4',n['display_model'])
        e=next(e for e in self.row(15)['mapping']['evidence'] if e['id']=='e_o_2')
        self.assertEqual(e['kind'],'EDITED_POST')
        self.assertIn('UNKNOWN',e['location'])

    def test_usb_c_comparison_does_not_infer_mac_host(self):
        r=self.row(5);m=r['mapping']
        c=next(c for c in m['configurations'] if c['id']=='cfg_cc')
        sources=[n for n in m['nodes'] if n['id'] in c['node_ids'] and n['kind']=='SOURCE']
        self.assertEqual(len(sources),1)
        self.assertEqual((sources[0]['display_model'],sources[0]['chip']),('UNKNOWN','UNKNOWN'))

    def test_semantic_review_cannot_claim_human_approval_or_other_source(self):
        r=self.row();r['semantic_review']['status']='HUMAN_APPROVED'
        self.assertTrue(self.errors(r))
        r=self.row();r['semantic_review']['source_url']='https://example.com/other'
        self.reject(r,'same source URL')


if __name__=='__main__':
    unittest.main()
