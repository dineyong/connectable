import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from scripts import prepare_monipick_summary_expansion as expansion
from scripts import prepare_monipick_content_candidate as content


class SummaryExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.summaries=expansion.expansion_summaries()
        _,cls.before=content.polished_artifacts()
        _,cls.after=expansion.expanded_artifacts()

    def test_only_remaining_27_pages_change_and_existing_three_are_byte_identical(self):
        changed={n for n,v in self.before.items() if self.after[n]!=v}
        self.assertEqual(changed,{'monitors/'+p.removeprefix('monitor:')+'/index.html' for p in self.summaries})
        self.assertEqual(len(changed),27)
        self.assertEqual(sum(b'id="model-highlights"' in v for n,v in self.after.items() if n.endswith('.html')),30)
        for n in changed:
            # Original specs/notes/source tables survive; only accessible aside names differ.
            original=self.before[n].decode().split('<section aria-labelledby="specs">',1)[1]
            updated=self.after[n].decode().split('<section aria-labelledby="specs">',1)[1]
            updated=updated.replace('<aside aria-label="사양 적용 범위">','<aside>').replace('<aside class="source-conflict" aria-label="공식 자료 표기 차이">','<aside class="source-conflict">')
            self.assertEqual(original,updated)

    def test_uncertainty_and_conflict_notes_are_bound(self):
        original=content.official(content.load(content.FACTS))
        for mutation in ('resolved_missing','removed_conflict','new_conflict'):
            bad=copy.deepcopy(original)
            p=next(p for p in bad['products'] if p['id']=='monitor:lg-27up850k-w')
            if mutation=='resolved_missing': p['missing_fields'].remove('korean_sku_identity')
            elif mutation=='removed_conflict':p['notes']=[n for n in p['notes'] if not n.startswith('CONFLICT_REVIEW ')]
            else:p['notes'].append('CONFLICT_REVIEW new conflict requires editorial review')
            with self.subTest(mutation=mutation),patch.object(content,'official',return_value=bad),self.assertRaises(ValueError):
                expansion.expansion_summaries()

    def test_model_region_and_variant_changes_require_review(self):
        original=content.official(content.load(content.FACTS))
        for key,value in [('display_model','M27Q rev.2.0'),('region','KR'),('variant_status','UNKNOWN')]:
            bad=copy.deepcopy(original)
            next(p for p in bad['products'] if p['id']=='monitor:gigabyte-m27q-rev-1-0')[key]=value
            with self.subTest(key=key),patch.object(content,'official',return_value=bad),self.assertRaises(ValueError):
                expansion.expansion_summaries()

    def test_value_unit_qualifier_scope_and_source_changes_are_rejected(self):
        original=content.official(content.load(content.FACTS))
        for key,value in [('value',100),('unit','Hz'),('qualifier','UNKNOWN'),('scope','DOWNSTREAM'),('source_refs',[])]:
            bad=copy.deepcopy(original)
            f=next(f for p in bad['products'] if p['id']=='monitor:benq-pd2725u' for f in p['facts'] if f['property']=='pd_supply')
            f[key]=value
            with self.subTest(key=key),patch.object(content,'official',return_value=bad),self.assertRaises(ValueError):
                expansion.expansion_summaries()

    def test_incomplete_bindings_or_replaced_existing_product_are_rejected(self):
        data=json.loads(expansion.EDITORIAL.read_text())
        for mutation in ('scope','conflict','product'):
            bad=copy.deepcopy(data)
            if mutation=='scope':del bad['products'][0]['claims'][0]['expected_facts']['size']['scope']
            elif mutation=='conflict':del bad['products'][0]['expected_conflict_notes']
            else:bad['products'][0]['product_id']='monitor:asus-pa279crv'
            with tempfile.TemporaryDirectory() as tmp:
                file=Path(tmp)/'editorial.json';file.write_text(json.dumps(bad))
                with self.subTest(mutation=mutation),patch.object(expansion,'EDITORIAL',file),self.assertRaises(ValueError):
                    expansion.expansion_summaries()

    def test_power_direction_and_alternative_modes_are_not_combined(self):
        benq=self.summaries['monitor:benq-pd2725u'][1]
        for s in ('65W','업스트림','15W','다운스트림'):self.assertIn(s,benq)
        lg=self.summaries['monitor:lg-32gs95ue-b'][1]
        self.assertIn('3840×2160 최대 240Hz와 1920×1080 최대 480Hz의 대안 모드',lg)
        self.assertIn('두 모드의 동시 출력으로 합치지 않습니다',lg)
        dell=self.summaries['monitor:dell-u2724d'][1]
        self.assertIn('데이터 전용',dell);self.assertIn('FRL 지원으로 확장 해석하지 않습니다',dell)

    def test_explicit_unsupported_is_separate_from_unknown_and_conflicts(self):
        self.assertIn('미지원으로 명시',self.summaries['monitor:lg-27gp850-b'][1])
        self.assertIn('USB-C 영상 모드·PD 공급 전력은 미확인',self.summaries['monitor:gigabyte-m28u'][1])
        lg=self.summaries['monitor:lg-27up850k-w'][0]
        self.assertNotIn('pd_supply',{p for c in lg['claims'] for p in c['expected_facts']})
        self.assertIn('공식 자료 간 표기 충돌',lg['caution'])
        self.assertIn('LS34C650UEEXXY',self.summaries['monitor:samsung-s65uc-ls34c650ueexxy'][1])

    def test_generated_artifacts_and_authorization_flags_are_verified(self):
        before=content.FACTS.read_bytes()
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'candidate';manifest=expansion.build_summary_expansion(out)
            self.assertEqual(expansion.validate_summary_expansion(out),[])
            self.assertTrue(all(manifest[f] is False for f in expansion.FLAGS))
            for flag in expansion.FLAGS:
                bad=copy.deepcopy(manifest);bad[flag]=True
                (out/'manifest.json').write_text(json.dumps(bad))
                self.assertTrue(expansion.validate_summary_expansion(out))
            (out/'manifest.json').write_text(json.dumps(manifest))
            p=out/'site/monitors/benq-pd2725u/index.html';p.write_bytes(p.read_bytes().replace(b'65W',b'90W'))
            self.assertTrue(expansion.validate_summary_expansion(out))
        self.assertEqual(before,content.FACTS.read_bytes())

    def test_unexpected_file_and_symlink_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'candidate';expansion.build_summary_expansion(out)
            extra=out/'site/extra.html';extra.write_text('unexpected')
            self.assertTrue(expansion.validate_summary_expansion(out));extra.unlink()
            extra.symlink_to(out/'site/index.html')
            self.assertTrue(expansion.validate_summary_expansion(out))
