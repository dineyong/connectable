"""Validate the local 18-case review mapping without importing it into the corpus.

Reuse the authoritative v2 object schemas and semantic checks in memory. The
small envelope and evidence scope annotations are review-only; no second v2
schema, official facts, engine inputs or approval mechanism are created.
"""
import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from urllib.parse import unquote

if __package__:
    from . import validate_question_corpus_v2 as v2
else:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts import validate_question_corpus_v2 as v2

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'data/research/review/public_usage_batch_2026-10-08.jsonl'
MAPPING = ROOT / 'data/research/review/public_usage_mapped_2026-10-08.jsonl'
EXPECTED_IDS = {f'PUR-{i:03}' for i in range(1, 19)}
DOMAINS = ('VIDEO_OUTPUT', 'SIGNAL_MODE', 'UI_SCALE', 'PD_CHARGING',
           'CLAMSHELL', 'SLEEP_WAKE', 'RECONNECT', 'OTHER')
ROLES = ('AUTHOR_OBSERVATION', 'PERFORMED_CHANGE', 'CONFIGURATION_REPORT',
         'ADVICE', 'PURCHASE_PLAN', 'PRODUCT_DESCRIPTION', 'CONTEXT')


def text_spec(enum=None, pattern=None):
    spec = {'type': 'string', 'minLength': 1}
    if enum is not None:
        spec['enum'] = list(enum)
    if pattern is not None:
        spec['pattern'] = pattern
    return spec


def array_spec(items, minimum=0):
    return {'type': 'array', 'items': items, 'minItems': minimum, 'uniqueItems': True}


def object_spec(properties):
    return {'type': 'object', 'properties': properties,
            'required': list(properties), 'additionalProperties': False}


def review_schema():
    """Compose a review envelope from the actual v2 schema, never a copied fork."""
    canonical = v2.load_schema()
    props = copy.deepcopy(canonical['properties'])
    for name in ('id', 'schema_version', 'migration', 'configuration_conclusions'):
        props.pop(name, None)
    mapping = {'type': 'object', 'properties': props,
               'required': [x for x in canonical['required'] if x in props],
               'additionalProperties': False}
    refs = array_spec(text_spec(pattern=r'^[a-z][a-z0-9_-]*$'))
    result = object_spec({'status': text_spec(('NORMAL', 'PROBLEM', 'TEMPORARY_WORKAROUND', 'UNKNOWN')),
                          'evidence_refs': refs, 'notes': text_spec()})
    quantity = text_spec(pattern=r'^(UNKNOWN|[1-9][0-9]*(?:\.[0-9]+)?)$')
    observation = object_spec({
        'observation_id': text_spec(), 'video_output': result,
        'signal_mode': object_spec({
            'resolution_pixels': text_spec(pattern=r'^(UNKNOWN|[1-9][0-9]*x[1-9][0-9]*)$'),
            'resolution_label': text_spec(),
            'label_basis': text_spec(('REPORTED_OUTPUT', 'SELECTABLE_LABEL', 'SELECTED_SETTING', 'UNKNOWN')),
            'hz': quantity,
            'hz_basis': text_spec(('REPORTED_OUTPUT', 'SELECTABLE_LIMIT', 'SELECTED_SETTING', 'UNKNOWN')),
            'evidence_refs': refs, 'notes': text_spec()}),
        'ui_scale': object_spec({'value': text_spec(), 'evidence_refs': refs}),
        'pd': object_spec({'recognized': text_spec(('YES', 'NO', 'UNKNOWN')),
                           'watts': quantity,
                           'power_basis': text_spec(('MEASURED', 'UNKNOWN')),
                           'evidence_refs': refs}),
        'clamshell': result, 'sleep_wake': result, 'reconnect': result,
        'other_notes': text_spec()})
    annotation = object_spec({
        'evidence_id': text_spec(), 'statement_role': text_spec(ROLES),
        'basis': text_spec(('USER_REPORT',)),
        'domains': array_spec(text_spec(DOMAINS)),
        'configuration_ids': array_spec(text_spec()),
        'source_pointers': array_spec(text_spec(pattern=r'^/.*$'), 1),
        'resolution_role': text_spec(('SIGNAL', 'UI_SCALE', 'PRODUCT_DESCRIPTION', 'UNKNOWN')),
        'mode_basis': text_spec(('REPORTED_OUTPUT', 'SELECTABLE_LIMIT', 'SELECTED_SETTING', 'UNKNOWN')),
        'label_basis': text_spec(('REPORTED_OUTPUT', 'SELECTABLE_LABEL', 'SELECTED_SETTING', 'UNKNOWN')),
        'power_role': text_spec(('CHARGING_RECOGNITION', 'MEASURED_INPUT', 'PRODUCT_MAXIMUM', 'UNKNOWN'))})
    spec = object_spec({
        'id': text_spec(pattern=r'^PUR-[0-9]{3}$'),
        'source_id': text_spec(pattern=r'^PUR-[0-9]{3}$'),
        'record_status': text_spec(('REVIEW_ONLY',)),
        'public_status': text_spec(('UNKNOWN',)),
        'approved_gold_count': {'type': 'integer', 'enum': [0]},
        'mapping_basis': text_spec(('EXISTING_REVIEW_SUMMARY',)),
        'source_line_sha256': text_spec(pattern=r'^[0-9a-f]{64}$'),
        'mapping': mapping, 'evidence_annotations': array_spec(annotation, 1),
        'functional_observations': array_spec(observation),
        'unscoped_statements': array_spec(object_spec({'evidence_id': text_spec(), 'notes': text_spec()}))})
    spec['$defs'] = canonical['$defs']
    # Review-only provenance for a new direct semantic check; not corpus approval.
    spec['properties']['semantic_review'] = object_spec({
        'status': text_spec(('AI_MATCHED', 'AI_CORRECTED', 'UNVERIFIED')),
        'checked_at': {'type': 'string', 'format': 'date'},
        'source_url': {'type': 'string', 'format': 'uri'},
        'access': text_spec(('BODY_DIRECT_CHECK', 'UNAVAILABLE')),
        'locations': array_spec(object_spec({
            'kind': text_spec(('ORIGINAL_POST', 'AUTHOR_COMMENT', 'EDITED_POST', 'OTHER_COMMENT')),
            'actor': text_spec(('CASE_AUTHOR', 'OTHER')),
            'location': text_spec(), 'summary': text_spec()}), 1),
        'notes': text_spec()})
    v2.audit_schema(spec)
    return spec


def normalized_url(url):
    """Reuse corpus normalization, plus mobile Tistory and percent encoding."""
    host, path, query = v2.url_key(url)
    if host and host.startswith('www.'):
        host = host[4:]
    path = unquote(path)
    if host and host.endswith('.tistory.com') and path.startswith('/m/entry/'):
        path = path[2:]
    return host, path, query


def pointer_value(record, pointer):
    current = record
    for key in pointer.split('/')[1:]:
        key = key.replace('~1', '/').replace('~0', '~')
        current = current[int(key)] if isinstance(current, list) else current[key]
    return current


def validate_record(record, source, source_hash, schema=None):
    schema = schema or review_schema()
    errors = v2.check_value(record, schema, schema)
    if errors:
        return errors
    m = record['mapping']
    errors.extend(v2.check_semantics(m))
    errors.extend(v2.sensitive_strings(record))
    def error(path, message):
        errors.append(f'{path}: {message}')
    if record['id'] != record['source_id'] or record['source_id'] != source['id']:
        error('$.source_id', 'source ID must be preserved')
    if record['source_line_sha256'] != source_hash:
        error('$.source_line_sha256', 'source line hash mismatch')
    expected_source = dict(source_url=source['source']['url'], site_name=source['source']['site'],
                           published_at=source['source']['published_on'], checked_at=source['source']['checked_on'],
                           public_access='YES', original_language='ko', source_status='AVAILABLE')
    if m['source'] != expected_source:
        error('$.mapping.source', 'source URL/date/access metadata must be preserved')
    if source['record_status'] != 'REVIEW_ONLY' or source['source']['access'] != 'BODY_DIRECT_CHECK':
        error('$.source_id', 'search leads cannot become checked cases')
    if source['source']['reliability_grade'] != 'C' or m['review']['reliability_grade'] != 'C':
        error('$.mapping.review', 'single-user review batch must remain C')
    if m['review']['status'] != 'NEEDS_REVIEW' or m['review']['usable_for_compatibility'] != 'NO':
        error('$.mapping.review', 'review-only batch cannot be approved')
    if m['product_links'] or m['outcome']['status'] != 'UNKNOWN':
        error('$.mapping', 'no catalog binding or case outcome approval in this batch')
    evidence = {e['id']: e for e in m['evidence']}
    annotations = {}
    semantic = record.get('semantic_review')
    if semantic:
        if semantic['source_url'] != m['source']['source_url']:
            error('$.semantic_review', 'semantic review must refer to the same source URL')
        if (semantic['access'] == 'UNAVAILABLE') != (semantic['status'] == 'UNVERIFIED'):
            error('$.semantic_review', 'unavailable source cannot be marked checked')
    for a in record['evidence_annotations']:
        eid = a['evidence_id']
        if eid in annotations:
            error('$.evidence_annotations', 'duplicate evidence annotation')
        annotations[eid] = a
        e = evidence.get(eid)
        if not e:
            error('$.evidence_annotations', 'dangling evidence annotation')
            continue
        direct_pointers = [p for p in a['source_pointers'] if p.startswith('/semantic_review/locations/')]
        if direct_pointers:
            if not semantic or semantic['access'] != 'BODY_DIRECT_CHECK' or e['origin'] != 'DIRECT_CHECK' or e['checked_at'] != semantic['checked_at']:
                error('$.mapping.evidence', 'new semantic evidence needs direct recheck provenance')
        elif e['checked_at'] != source['source']['checked_on'] or e['origin'] != source['evidence']['origin']:
            error('$.mapping.evidence', 'retain original check date and origin; mapping is not a new source check')
        for pointer in a['source_pointers']:
            try:
                location = pointer_value(record if pointer in direct_pointers else source, pointer)
                if pointer in direct_pointers and (not isinstance(location, dict) or
                        e['actor'] != location.get('actor') or e['kind'] != location.get('kind')):
                    error('$.evidence_annotations', 'semantic evidence kind/actor must match checked location')
            except (KeyError, IndexError, ValueError, TypeError):
                error('$.evidence_annotations.source_pointers', 'missing source pointer')
        if a['statement_role'] == 'AUTHOR_OBSERVATION':
            if e['actor'] != 'CASE_AUTHOR' or not (direct_pointers or any(p.startswith('/author_observations/') for p in a['source_pointers'])):
                error('$.evidence_annotations', 'author observation requires a checked author observation, not advice/plan/product text')
    if set(annotations) != set(evidence):
        error('$.evidence_annotations', 'every evidence object requires exactly one role annotation')
    configs = {c['id']: c for c in m['configurations']}
    for a in annotations.values():
        if not set(a['configuration_ids']).issubset(configs):
            error('$.evidence_annotations.configuration_ids', 'dangling configuration scope')
    for c in configs.values():
        settings = {s['key']: s for s in c['settings']}
        for key in ('external_power', 'lid', 'hdr', 'os_name', 'os_version'):
            if key not in settings:
                error('$.mapping.configurations.settings', 'missing condition must be explicit UNKNOWN')
        if len(settings) != len(c['settings']):
            error('$.mapping.configurations.settings', 'duplicate setting key')
    for n in m['nodes']:
        if 'display_model' not in n or 'normalized_model' not in n or (n['kind'] == 'SOURCE' and 'chip' not in n):
            error('$.mapping.nodes', 'missing model/chip must be explicit UNKNOWN')
    observations = {o['id']: o for o in m['observations']}
    details = {}
    for d in record['functional_observations']:
        oid = d['observation_id']
        if oid in details:
            error('$.functional_observations', 'duplicate observation detail')
        details[oid] = d
        o = observations.get(oid)
        if not o:
            error('$.functional_observations', 'dangling observation reference')
            continue
        cfg = o['configuration_id']
        for eid in o['evidence_refs']:
            a = annotations.get(eid)
            if not a or a['statement_role'] != 'AUTHOR_OBSERVATION' or cfg not in a['configuration_ids']:
                error('$.mapping.observations', 'advice/plan/change/product description or another configuration cannot become an observation')
        def require_scope(value, domain, known):
            refs = value['evidence_refs']
            if not known:
                if refs:
                    error('$.functional_observations', 'UNKNOWN function cannot borrow another function evidence')
                return
            if not refs:
                error('$.functional_observations', 'known result needs function-specific evidence')
            for eid in refs:
                a = annotations.get(eid)
                if (not a or a['statement_role'] != 'AUTHOR_OBSERVATION' or a['basis'] != 'USER_REPORT'
                        or domain not in a['domains'] or cfg not in a['configuration_ids']):
                    error('$.functional_observations', f'{domain} requires scoped author observation; no advice or cross-function promotion')
                if eid not in o['evidence_refs']:
                    error('$.functional_observations', 'functional evidence must also support this observation')
        for field, domain in [('video_output', 'VIDEO_OUTPUT'), ('clamshell', 'CLAMSHELL'),
                              ('sleep_wake', 'SLEEP_WAKE'), ('reconnect', 'RECONNECT')]:
            require_scope(d[field], domain, d[field]['status'] != 'UNKNOWN')
        sm = d['signal_mode']
        known_mode = any(sm[k] != 'UNKNOWN' for k in ('hz', 'resolution_pixels', 'resolution_label'))
        require_scope(sm, 'SIGNAL_MODE', known_mode)
        if (sm['resolution_label'] == 'UNKNOWN') != (sm['label_basis'] == 'UNKNOWN'):
            error('$.functional_observations.signal_mode', 'resolution label and basis must agree')
        if sm['resolution_label'] != 'UNKNOWN' and not all(annotations.get(e, {}).get('label_basis') == sm['label_basis'] for e in sm['evidence_refs']):
            error('$.functional_observations.signal_mode', 'selectable resolution label cannot become actual output')
        if sm['hz'] != 'UNKNOWN' and not all(annotations.get(e, {}).get('mode_basis') == sm['hz_basis'] for e in sm['evidence_refs']):
            error('$.functional_observations.signal_mode', 'Hz basis cannot promote a selection limit/setting into actual output')
        if (sm['hz'] == 'UNKNOWN') != (sm['hz_basis'] == 'UNKNOWN'):
            error('$.functional_observations.signal_mode', 'Hz value and observation basis must agree')
        if sm['resolution_pixels'] != 'UNKNOWN' and not all(annotations.get(e, {}).get('resolution_role') == 'SIGNAL' for e in sm['evidence_refs']):
            error('$.functional_observations.signal_mode', 'UI scale/product label cannot become signal pixels')
        require_scope(d['ui_scale'], 'UI_SCALE', d['ui_scale']['value'] != 'UNKNOWN')
        if d['ui_scale']['value'] != 'UNKNOWN' and not all(annotations.get(e, {}).get('resolution_role') == 'UI_SCALE' for e in d['ui_scale']['evidence_refs']):
            error('$.functional_observations.ui_scale', 'UI scale requires UI_SCALE role')
        pd = d['pd']
        require_scope(pd, 'PD_CHARGING', pd['recognized'] != 'UNKNOWN' or pd['watts'] != 'UNKNOWN')
        if pd['watts'] != 'UNKNOWN' and not all(annotations.get(e, {}).get('power_role') == 'MEASURED_INPUT' for e in pd['evidence_refs']):
            error('$.functional_observations.pd', 'charging recognition/product maximum cannot become measured input power')
        if (pd['watts'] == 'UNKNOWN') != (pd['power_basis'] == 'UNKNOWN'):
            error('$.functional_observations.pd', 'supply/marketing maximum is not measured power')
        if o['pd_charging'] != pd['recognized']:
            error('$.mapping.observations.pd_charging', 'core charging value and scoped detail must agree')
        if o['clamshell'] == 'YES' and d['clamshell']['status'] == 'UNKNOWN':
            error('$.mapping.observations.clamshell', 'clamshell needs its own scoped observation')
        if o['signal_state'] == 'NORMAL' and d['video_output']['status'] != 'NORMAL':
            error('$.mapping.observations.signal_state', 'normal video needs scoped video evidence')
        for state in o['display_states']:
            if state['lit'] == 'YES' and d['video_output']['status'] == 'UNKNOWN':
                error('$.mapping.observations.display_states', 'lit display requires its own video evidence')
            if 'resolution' in state and (state['resolution'] != sm['resolution_pixels'] or sm['resolution_pixels'] == 'UNKNOWN'):
                error('$.mapping.observations.display_states', 'signal pixels cannot be copied from UI scale or labels')
            if 'resolution_label' in state and (sm['label_basis'] != 'REPORTED_OUTPUT' or state['resolution_label'] != sm['resolution_label']):
                error('$.mapping.observations.display_states', 'selectable resolution label is not actual output')
            if 'hz' in state and (sm['hz_basis'] != 'REPORTED_OUTPUT' or str(state['hz']) != sm['hz']):
                error('$.mapping.observations.display_states', 'selection limit/setting is not actual output Hz')
        if 'pd_watts' in o and (pd['power_basis'] != 'MEASURED' or str(o['pd_watts']) != pd['watts']):
            error('$.mapping.observations.pd_watts', 'core watts need measured-power evidence')
    if set(details) != set(observations):
        error('$.functional_observations', 'every observation needs all function slots including UNKNOWN')
    for a in m['attempts']:
        for eid in a['evidence_refs']:
            ann = annotations.get(eid)
            if not ann or ann['statement_role'] != 'PERFORMED_CHANGE' or a['configuration_id'] not in ann['configuration_ids']:
                error('$.mapping.attempts', 'advice or purchase plan cannot become a performed change')
    for statement in record['unscoped_statements']:
        if statement['evidence_id'] not in evidence:
            error('$.unscoped_statements', 'dangling statement evidence')
    return errors


def read_jsonl(path):
    content = Path(path).read_bytes()
    if not content or not content.endswith(b'\n') or b'\r' in content or content.startswith(b'\xef\xbb\xbf'):
        raise ValueError('JSONL must be nonempty UTF-8, LF, final newline, no BOM/CR')
    rows = []
    for line, raw in enumerate(content.splitlines(keepends=True), 1):
        try:
            row = json.loads(raw.decode('utf-8'), object_pairs_hook=v2.unique_object, parse_constant=v2.reject_constant)
        except (ValueError, UnicodeError) as exc:
            raise ValueError(f'line {line}: invalid JSON/UTF-8/duplicate keys') from exc
        if not isinstance(row, dict):
            raise ValueError(f'line {line}: expected object')
        rows.append((line, row, hashlib.sha256(raw).hexdigest()))
    return rows


def validate_files(mapping_path=MAPPING, source_path=SOURCE):
    errors = []
    try:
        sources = read_jsonl(source_path)
        records = read_jsonl(mapping_path)
        schema = review_schema()
    except (OSError, ValueError) as exc:
        return [str(exc)]
    source_ids = [r['id'] for _, r, _ in sources if 'id' in r]
    if len(sources) != 18 or len(set(source_ids)) != 18 or set(source_ids) != EXPECTED_IDS:
        errors.append('source batch must contain exactly PUR-001..PUR-018 once')
    for number, source, _ in sources:
        metadata = source.get('source')
        if (not isinstance(metadata, dict) or any(k not in metadata for k in
                ('url', 'site', 'published_on', 'checked_on', 'access', 'reliability_grade'))
                or not isinstance(source.get('evidence'), dict) or 'origin' not in source['evidence']
                or 'record_status' not in source):
            errors.append(f'{source_path}: line {number}: incomplete source metadata')
    if errors:
        return errors
    inputs = {r['id']: (r, digest) for _, r, digest in sources if 'id' in r}
    seen, urls = set(), set()
    for number, record, _ in records:
        prefix = f'{mapping_path}: line {number}'
        identifier = record.get('source_id')
        if identifier not in inputs:
            errors.append(f'{prefix}: unknown source ID (user hardware and leads are outside this batch)')
            continue
        source, digest = inputs[identifier]
        local = validate_record(record, source, digest, schema)
        if record.get('id') in seen:
            local.append('duplicate review ID')
        seen.add(record.get('id'))
        if not local:
            key = normalized_url(record['mapping']['source']['source_url'])
            if key in urls:
                local.append('duplicate normalized URL')
            urls.add(key)
        errors.extend(f'{prefix}: {e}' for e in local)
    if len(records) != 18 or seen != EXPECTED_IDS:
        errors.append('mapping must contain exactly all 18 source IDs once')
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mapping', type=Path, default=MAPPING)
    parser.add_argument('--source', type=Path, default=SOURCE)
    args = parser.parse_args(argv)
    errors = validate_files(args.mapping, args.source)
    for error in errors:
        print(error, file=sys.stderr)
    if not errors:
        print('PASS: 18 review mappings; source hashes retained; C / public UNKNOWN / approved gold 0; no corpus import')
    return int(bool(errors))


if __name__ == '__main__':
    raise SystemExit(main())
