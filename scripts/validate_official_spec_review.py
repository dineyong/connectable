"""Validate the isolated manual-review evidence batch; never apply to catalog."""
import hashlib
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.site_content_validation import checked_date, https_url, payload, refs, unique
from scripts.data_trust import require_official_source

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT/'data/official/spec_manual_review_2026-10-09.json'


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def validate(data):
    site = json.loads((ROOT/'data/site/content-v2.json').read_text())
    products = {m['id']: m for m in site['monitors']}
    facts = {f['fact_id']: f for m in site['monitors'] for f in m['features']}
    checked_date(data['checked_on'], 'checked_on')
    if data['catalog_application'] != 'NOT_APPLIED':
        raise ValueError('review batch must remain isolated')
    sources = unique(data['sources'], 'source_id', 'sources')
    unique(data['assertions'], 'assertion_id', 'assertions')
    unique(data['manual_reviews'], 'fact_id', 'manual_reviews')
    for s in sources.values():
        https_url(s['url'], s['source_id'])
        checked_date(s['checked_at'], s['source_id'])
        if s['source_status'] not in ('DIRECT_CHECK', 'ACCESS_FAILED') or not s['location'].strip():
            raise ValueError('invalid source check status/location')

    def evidence(item, product):
        refs(item['source_refs'], 'source_refs', sources)
        for ref in item['source_refs']:
            s = sources[ref]
            if s['source_status'] != 'DIRECT_CHECK' or s['model_scope'] != product['display_model']:
                raise ValueError('evidence needs checked manufacturer/model source')
            require_official_source(s, product['manufacturer'], ref)
        if item['public_status'] != 'UNKNOWN' or item['usable_for_compatibility'] != 'NO':
            raise ValueError('spec review is not compatibility approval')

    for c in data['assertions']:
        if c['product_id'] not in products or c['status'] != 'VERIFIED_MODEL_SCOPE' or c['variant_match'] != 'UNKNOWN':
            raise ValueError('invalid assertion/model scope')
        evidence(c, products[c['product_id']])
        payload(c, c['assertion_id'])
        refs(c['verified_fields'], 'verified_fields', c['payload'])
        if not c['location'].strip() or any(c['payload'][f] == 'UNKNOWN' for f in c['verified_fields']):
            raise ValueError('unknown fields cannot be verified')
        if 'target_fact_id' in c:
            f = facts.get(c['target_fact_id'])
            if not f or c['target_fact_sha256'] != digest(f) or f['product_id'] != c['product_id']:
                raise ValueError('invalid target fact/hash')
            if any(f['payload'].get(k) != c['payload'][k] for k in c['verified_fields']):
                raise ValueError('existing fact differs from verified fields')
    for r in data['manual_reviews']:
        f = facts.get(r['fact_id'])
        if not f or r['original_fact_sha256'] != digest(f) or r['status'] != 'PARTIALLY_VERIFIED':
            raise ValueError('invalid original manual fact/hash/status')
        evidence(r, products[f['product_id']])
        refs(r['verified_fields'], 'verified_fields', f['payload'])
        refs(r['unverified_fields'], 'unverified_fields', f['payload'])
        if set(r['verified_fields']) & set(r['unverified_fields']) or any(f['payload'][k] == 'UNKNOWN' for k in r['verified_fields']):
            raise ValueError('manual field certainty mismatch')
    return data


if __name__ == '__main__':
    result = validate(json.loads(PATH.read_text()))
    print(f"PASS: {len(result['assertions'])} model-scope assertions; {len(result['manual_reviews'])} partial manual reviews; catalog unchanged")
