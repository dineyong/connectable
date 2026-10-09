"""Validate one isolated, observed image-evidence batch; no network or projection.

The bounded binding below records the prior direct check. It does not discover
page assets, authenticate image content, approve a SKU or approve compatibility.
A different page/image/assertion requires another reviewed evidence contract.
"""
import hashlib
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.data_trust import require_official_source
from scripts.site_content_validation import payload, validate_content
from scripts.validate_official_spec_review import digest
from scripts.validate_question_corpus_v2 import (
    audit_schema, check_value, sensitive_strings, unique_object, reject_constant,
)

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT/'data/official/crossover_pd_followup_2026-10-09.json'
SCHEMA = ROOT/'schemas/crossover-pd-evidence.schema.json'
PAGE = 'https://www.crosslcd.co.kr/shop/item.php?it_id=1716533757'
ASSET = 'https://www.crosslcd.co.kr/data/editor/2411/047dd0567fcc29d7226521dd0b0f9f78_1732598597_5708.jpg'
CAPTURE = 'docs/evidence/crossover-27uld950-pd65-followup.jpg'
CHECKED_ON = '2026-10-09'


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'),
                      object_pairs_hook=unique_object, parse_constant=reject_constant)


def capture_digest(path):
    # Reject symlinks as well as traversal. Only the existing excerpt is in scope.
    if path != CAPTURE:
        raise ValueError('capture path outside reviewed excerpt scope')
    target = ROOT/path
    if any(p.is_symlink() for p in [target, *target.parents]) or not target.is_file():
        raise ValueError('missing or symbolic capture path')
    return hashlib.sha256(target.read_bytes()).hexdigest()


def validate(data):
    schema = load(SCHEMA)
    audit_schema(schema)
    errors = check_value(data, schema, schema) + sensitive_strings(data)
    if errors:
        raise ValueError(str(errors[:5]))
    # Validate upstream data, not just a derived index of its IDs.
    site = validate_content(load(ROOT/'data/site/content-v2.json'))
    product = next((m for m in site['monitors'] if m['id'] == data['product_id']), None)
    if not product or product['display_model'] != data['model_scope']:
        raise ValueError('unknown or mismatched product/model')
    fact = next((f for f in product['features'] if f['fact_id'] == data['related_fact_id']), None)
    if not fact or fact['product_id'] != product['id'] or digest(fact) != data['original_fact_sha256']:
        raise ValueError('missing, cross-product or stale original fact')
    if fact['property'] != data['assertion']['property']:
        raise ValueError('supplement property differs from original')
    source, asset, assertion = data['source'], data['asset'], data['assertion']
    require_official_source(source, product['manufacturer'], 'source')
    if source['url'] != PAGE or source['model_scope'] != product['display_model']:
        raise ValueError('source page/model outside observed scope')
    # The related fact must already cite this precise product page.
    sources = {s['record_id']: s for s in product['source_refs']}
    if not any(sources[r]['url'] == PAGE for r in fact['source_refs']):
        raise ValueError('parent fact does not cite the observed product page')
    if asset['parent_source_ref'] != source['source_id'] or asset['url'] != ASSET:
        raise ValueError('asset does not match observed parent-page binding')
    if source['source_id'] == asset['asset_id'] or assertion['assertion_id'] in {source['source_id'], asset['asset_id']}:
        raise ValueError('duplicate local object ID')
    if assertion['evidence_refs'] != [asset['asset_id']]:
        raise ValueError('exact nonempty image evidence reference required')
    if source['checked_on'] != CHECKED_ON or asset['checked_on'] != CHECKED_ON:
        raise ValueError('cannot invent a new direct-check date')
    if asset['capture_sha256'] != capture_digest(asset['capture_path']):
        raise ValueError('capture bytes differ from recorded SHA-256')
    payload(assertion, 'assertion')
    if set(assertion['confirmed_fields']) != {'mode', 'watts', 'rating_basis'} or assertion['unconfirmed_fields'] != ['interface']:
        raise ValueError('partial field scope must preserve unknown interface')
    if not (ROOT/data['provenance_report']).is_file():
        raise ValueError('missing provenance report')
    return data


if __name__ == '__main__':
    validate(load(PATH))
    print('PASS: isolated PD65 supplemental evidence; original/UI unchanged; human/public approval withheld')
