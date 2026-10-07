"""Validate the seed official catalog; validation does not approve source truth."""
import json
import sys
from pathlib import Path
from urllib.parse import urlsplit
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.validate_question_corpus_v2 import audit_schema, check_value, unique_object, reject_constant

ROOT = Path(__file__).resolve().parents[1]


def load_catalog():
    return json.loads((ROOT / 'data/official/products.json').read_text(encoding='utf-8'), object_pairs_hook=unique_object, parse_constant=reject_constant)


def validate_catalog(data):
    schema = json.loads((ROOT / 'schemas/official-products.schema.json').read_text())
    audit_schema(schema)
    errors = check_value(data, schema, schema)
    if errors:
        return errors
    for key, field in [('sources', 'source_id'), ('products', 'product_id')]:
        ids = [row[field] for row in data[key]]
        if len(ids) != len(set(ids)):
            errors.append(f'{key}: duplicate {field}')
    sources = {s['source_id']: s for s in data['sources']}
    products = {p['product_id']: p for p in data['products']}
    urls = [s['source_url'] for s in sources.values()]
    if len(urls) != len(set(urls)):
        errors.append('duplicate source_url')
    claim_ids = set()
    for source in sources.values():
        url = urlsplit(source['source_url'])
        if url.scheme != 'https' or url.hostname != 'support.apple.com' or url.username or url.password:
            errors.append(f"{source['source_id']}: unapproved official URL")
        if not set(source['applies_to_models']).issubset(products):
            errors.append(f"{source['source_id']}: missing product")
        expected_grade = 'A' if source['source_type'] == 'MANUFACTURER_SPEC' else 'B'
        if source['reliability_grade'] != expected_grade:
            errors.append(f"{source['source_id']}: source type/grade mismatch")
    for p in products.values():
        for ref in p['source_refs']:
            if ref not in sources or p['product_id'] not in sources[ref]['applies_to_models']:
                errors.append(f"{p['product_id']}: invalid source reference")
        for c in p['claims']:
            if c['claim_id'] in claim_ids:
                errors.append('duplicate claim_id')
            claim_ids.add(c['claim_id'])
            if not set(c['source_refs']).issubset(set(p['source_refs'])):
                errors.append(f"{c['claim_id']}: invalid source reference")
            profile = {'external_count', 'resolution_label', 'refresh_hz'}
            if c['property'] == 'NATIVE_EXTERNAL_DISPLAY_PROFILE' and not profile.issubset(c):
                errors.append(f"{c['claim_id']}: incomplete simultaneous display profile")
            if c['property'] == 'CONDITIONAL_NATIVE_DISPLAY_PROFILE':
                if not {'external_count', 'display_groups', 'prerequisites'}.issubset(c):
                    errors.append(f"{c['claim_id']}: incomplete conditional profile")
                elif sum(g['count'] for g in c['display_groups']) != c['external_count']:
                    errors.append(f"{c['claim_id']}: group count mismatch")
                if {'resolution_label', 'refresh_hz'}.intersection(c):
                    errors.append(f"{c['claim_id']}: flattened conditional profile")
                pre = c.get('prerequisites', {})
                if pre.get('lid_state') == 'CLOSED' and pre.get('builtin_state') != 'OFF':
                    errors.append(f"{c['claim_id']}: closed lid with builtin ON")
            elif {'display_groups', 'prerequisites'}.intersection(c):
                errors.append(f"{c['claim_id']}: conditional fields on unrelated claim")
            if c['property'] == 'PORT_FUNCTIONS' and profile.intersection(c):
                errors.append(f"{c['claim_id']}: display profile fields on unrelated claim")
    return errors


if __name__ == '__main__':
    import sys
    sys.path.insert(0, str(ROOT))
    catalog = load_catalog()
    errors = validate_catalog(catalog)
    print('\n'.join(errors) if errors else f"PASS: official product foundation ({len(catalog['products'])} products)")
    raise SystemExit(bool(errors))
