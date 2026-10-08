"""Read-only field review projection and withheld editorial review ledger."""
import json
import re
from pathlib import Path
from scripts.validate_official_spec_review import validate, digest
from scripts.site_content_validation import checked_date, validate_content
from scripts.validate_question_corpus_v2 import check_value

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT/'data/official/spec_manual_review_2026-10-09.json'
LEDGER = ROOT/'data/review/content_reviews.json'


def project(monitors, batch):
    validate(batch)
    partial = {r['fact_id']: r for r in batch['manual_reviews']}
    assertions = {r['target_fact_id']: r for r in batch['assertions'] if 'target_fact_id' in r}
    for m in monitors:
        for f in m['features']:
            r = partial.get(f['fact_id']) or assertions.get(f['fact_id'])
            fields = f['payload']
            verified = r['verified_fields'] if r else []
            # Only exact existing field checks can become reviewed fields.
            f['field_review'] = {
                'status': r['status'] if r else 'PENDING_HUMAN_REVIEW',
                'verified_fields': verified,
                'unverified_fields': [k for k in fields if k not in verified],
                'source_refs': [next(s for s in batch['sources'] if s['source_id'] == ref) for ref in r['source_refs']] if r else [],
                'variant_match': 'UNKNOWN',
            }
        # Separate assertion; never replaces or merges the original RATED fact.
        m['separate_spec_reviews'] = [r | {'sources': [s for s in batch['sources'] if s['source_id'] in r['source_refs']]} for r in batch['assertions'] if r['product_id'] == m['id'] and r['assertion_id'] == 'SR-LG-PD']
    return monitors


def validate_ledger(data):
    schema = json.loads((ROOT/'schemas/content-review.schema.json').read_text())
    errors = check_value(data, schema, schema)
    if errors:
        raise ValueError(str(errors[:5]))
    if set(data) != {'schema_version', 'public_status', 'records'} or data['schema_version'] != 1 or data['public_status'] != 'UNKNOWN' or not isinstance(data['records'], list):
        raise ValueError('invalid withheld review ledger')
    site = validate_content(json.loads((ROOT/'data/site/content-v2.json').read_text()))
    facts = {f['fact_id']: (m, f) for m in site['monitors'] for f in m['features']}
    ids = set()
    for r in data['records']:
        required = {'id','target_fact_id','target_sha256','reviewer_id','reviewed_on','result','source_refs','notes','public_status','usable_for_compatibility'}
        if set(r) != required or r['result'] not in {'NEEDS_REVIEW','PARTIALLY_VERIFIED','EVIDENCE_SUFFICIENT','REJECTED'}:
            raise ValueError('invalid review fields/result; public approval unsupported')
        if r['id'] in ids or not isinstance(r['id'], str) or not r['id'].strip():
            raise ValueError('invalid/duplicate review ID')
        ids.add(r['id'])
        if not isinstance(r['reviewer_id'],str) or not re.fullmatch(r'reviewer:[a-z0-9-]+', r['reviewer_id']) or not isinstance(r['notes'],str) or not r['notes'].strip():
            raise ValueError('reviewer and rationale required')
        checked_date(r['reviewed_on'], 'reviewed_on')
        if r['public_status'] != 'UNKNOWN' or r['usable_for_compatibility'] != 'NO':
            raise ValueError('public approval withheld')
        if r['target_fact_id'] not in facts:
            raise ValueError('unknown fact')
        m, f = facts[r['target_fact_id']]
        if r['target_sha256'] != digest(f):
            raise ValueError('stale target hash')
        if not isinstance(r['source_refs'],list) or not r['source_refs'] or len(set(r['source_refs'])) != len(r['source_refs']) or not set(r['source_refs']) <= set(f['source_refs']):
            raise ValueError('exact fact evidence required')
    return data


if __name__ == '__main__':
    validate_ledger(json.loads(LEDGER.read_text()))
    print('PASS: editorial records validated; public approval withheld')
