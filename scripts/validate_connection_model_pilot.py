"""Validate the research pilot and its discriminated typed facts (stdlib).

Equivalent to the eight enum-disjoint oneOf branches used here, not a general
JSON Schema engine. No path compatibility inference or source approval.
"""
import copy
import json
import sys
from pathlib import Path
from urllib.parse import urlsplit
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.validate_question_corpus_v2 import audit_schema, check_value, unique_object, reject_constant

ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / 'data/official/connection_model_pilot.json'
ALLOWED = {'www.dell.com', 'www.lg.com', 'www.caldigit.com', 'plugable.com',
           'media.startech.com', 'kb.cablematters.com', 'www.belkin.com', 'support.apple.com'}


def load_pilot():
    return json.loads(FILE.read_text(encoding='utf-8'), object_pairs_hook=unique_object, parse_constant=reject_constant)


def validate(data):
    spec = json.loads((ROOT / 'schemas/connection-model-pilot.schema.json').read_text())
    typed = json.loads((ROOT / 'schemas/typed-capability-v1.proposed.schema.json').read_text())
    if spec['properties']['facts']['items'] != {'$ref': 'typed-capability-v1.proposed.schema.json'}:
        raise ValueError('unexpected typed schema reference')
    if set(typed) != {'$schema', 'title', '$defs', 'oneOf'}:
        raise ValueError('unsupported typed root keywords')
    branches = typed['$defs']
    if typed['oneOf'] != [{'$ref': '#/$defs/' + k} for k in branches]:
        raise ValueError('unsupported typed schema dispatch')
    for name, branch in branches.items():
        audit_schema(branch)
        if branch['properties']['property']['enum'] != [name]:
            raise ValueError('non-disjoint property discriminator')
    envelope = copy.deepcopy(spec)
    envelope['properties']['facts'] = {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'properties': {}, 'required': [], 'additionalProperties': False}}
    # Envelope facts are checked separately; retain length and array type check.
    stripped = copy.deepcopy(data)
    if isinstance(stripped, dict) and isinstance(stripped.get('facts'), list):
        stripped['facts'] = [{} for _ in stripped['facts']]
    audit_schema(envelope)
    errors = check_value(stripped, envelope, envelope)
    if errors:
        return errors
    for i, fact in enumerate(data['facts']):
        if not isinstance(fact, dict) or fact.get('property') not in branches:
            errors.append(f'$.facts[{i}]: unknown typed property')
            continue
        errors.extend(check_value(fact, branches[fact['property']], typed, f'$.facts[{i}]'))
    if errors:
        return errors
    for key, field in [('sources', 'source_id'), ('products', 'product_id'), ('facts', 'fact_id')]:
        ids = [r[field] for r in data[key]]
        if len(ids) != len(set(ids)):
            errors.append(f'{key}: duplicate ID')
    sources = {r['source_id']: r for r in data['sources']}
    products = {r['product_id']: r for r in data['products']}
    urls = [r['url'] for r in sources.values()]
    if len(set(urls)) != len(urls):
        errors.append('duplicate source URL')
    for row in sources.values():
        u = urlsplit(row['url'])
        if u.scheme != 'https' or u.hostname not in ALLOWED or u.username or u.password:
            errors.append(f"{row['source_id']}: unapproved official URL")
        grade = 'A' if row['source_type'] == 'MANUFACTURER_SPEC' else 'B'
        if row['reliability_grade'] != grade:
            errors.append(f"{row['source_id']}: grade mismatch")
    for product in products.values():
        if not set(product['source_refs']).issubset(sources):
            errors.append(f"{product['product_id']}: missing source")
    for fact in data['facts']:
        product = products.get(fact['product_id'])
        if not product or not set(fact['source_refs']).issubset(product['source_refs']):
            errors.append(f"{fact['fact_id']}: invalid product/source binding")
        payload = fact['payload']
        if fact['property'] == 'VIDEO_PROFILE':
            has_pixels = 'width' in payload and 'height' in payload
            if ('width' in payload) != ('height' in payload) or not (has_pixels or 'resolution_label' in payload):
                errors.append(f"{fact['fact_id']}: incomplete resolution")
            if payload['scope'] == 'SIMULTANEOUS' and 'display_count' not in payload:
                errors.append(f"{fact['fact_id']}: simultaneous count missing")
            if payload['scope'] != 'SIMULTANEOUS' and 'display_count' in payload:
                errors.append(f"{fact['fact_id']}: count on non-simultaneous profile")
        if fact['property'] == 'POWER_TRANSFER':
            if payload['mode'] == 'NONE' and set(payload).intersection({'watts','rating_basis','pd_profiles'}):
                errors.append(f"{fact['fact_id']}: NONE cannot offer power")
            if ('watts' in payload) != ('rating_basis' in payload):
                errors.append(f"{fact['fact_id']}: watts/rating basis must be paired")
    return errors


if __name__ == '__main__':
    data = load_pilot()
    errors = validate(data)
    print('\n'.join(errors) if errors else f"PASS: pilot {len(data['products'])} products / {len(data['facts'])} facts; no compatibility approval")
    raise SystemExit(bool(errors))
