"""Validate withheld supplemental editorial records; never apply or approve them.

Empty records are intentional. Reviewer identity and actual human work cannot be
proved by this offline contract; repository review is required for real records.
"""
import datetime
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.crossover_pd_evidence import ROOT, PATH, load, validate as validate_evidence
from scripts.validate_official_spec_review import digest
from scripts.validate_question_corpus_v2 import audit_schema, check_value, sensitive_strings

LEDGER = ROOT/'data/review/supplemental_content_reviews.json'
SCHEMA = ROOT/'schemas/supplemental-content-review.schema.json'
REMAINING = {'interface', 'power_qualifier', 'pd_profiles', 'simultaneous_budget', 'sku_revision', 'actual_host_power'}


def validate(data):
    schema = load(SCHEMA)
    audit_schema(schema)
    errors = check_value(data, schema, schema) + sensitive_strings(data)
    if errors:
        raise ValueError(str(errors[:5]))
    batch = validate_evidence(load(PATH))
    assertion = batch['assertion']
    seen = set()
    for r in data['records']:
        if r['id'] in seen:
            raise ValueError('duplicate supplemental review ID')
        seen.add(r['id'])
        if (r['target_batch_id'] != batch['batch_id'] or
                r['target_assertion_id'] != assertion['assertion_id'] or
                r['evidence_batch_sha256'] != digest(batch) or
                r['related_fact_sha256'] != batch['original_fact_sha256'] or
                r['capture_sha256'] != batch['asset']['capture_sha256']):
            raise ValueError('stale or mismatched supplemental evidence binding')
        if set(r['evidence_refs']) != {batch['source']['source_id'], batch['asset']['asset_id']}:
            raise ValueError('review requires exact product-page and image evidence')
        fields = set(r['reviewed_fields'])
        if not fields <= set(assertion['confirmed_fields']) or set(r['remaining_unknowns']) != REMAINING:
            raise ValueError('review cannot promote unconfirmed conditions')
        if r['result'] == 'EVIDENCE_SUFFICIENT' and fields != set(assertion['confirmed_fields']):
            raise ValueError('sufficient applies only to the complete bounded assertion')
        if r['result'] == 'PARTIALLY_VERIFIED' and not fields:
            raise ValueError('partial review requires at least one checked field')
        if datetime.date.fromisoformat(r['reviewed_on']) < datetime.date.fromisoformat(batch['asset']['checked_on']):
            raise ValueError('review predates the evidence check')
    return data


if __name__ == '__main__':
    result = validate(load(LEDGER))
    print(f"PASS: {len(result['records'])} supplemental editorial records; no public approval or projection")
