"""Validate the authoritative v2 JSONL structure and corpus semantics (stdlib only).

A bounded JSON Schema subset, not a general engine. It checks all validation
keywords used by this schema and rejects unsupported keywords at schema load.
Source truth, authorship and catalog matches still require human review.
"""
import argparse
import datetime
import json
import math
import re
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / 'schemas/user-question-v2.schema.json'
DEFAULT_FILE = ROOT / 'data/research/user_questions_v2.jsonl'
SUPPORTED = {'$schema', '$id', '$defs', '$ref', 'title', 'description', 'examples',
             'type', 'properties', 'required', 'additionalProperties', 'items',
             'enum', 'pattern', 'format', 'minLength', 'maxLength', 'minimum',
             'exclusiveMinimum', 'minItems', 'uniqueItems'}


def audit_schema(spec):
    """Fail closed if a later schema adds validation we do not implement."""
    unknown = set(spec) - SUPPORTED
    if unknown:
        raise ValueError(f'unsupported schema keywords: {sorted(unknown)}')
    for name in ('properties', '$defs'):
        for child in spec.get(name, {}).values():
            audit_schema(child)
    if 'items' in spec:
        audit_schema(spec['items'])
    if '$ref' in spec:
        if not spec['$ref'].startswith('#/$defs/'):
            raise ValueError('only local $defs references supported')
        if set(spec) - {'$ref', 'description', 'title'}:
            raise ValueError('validation siblings of $ref are not supported')
    if 'format' in spec and spec['format'] not in ('date', 'uri'):
        raise ValueError('unsupported format')
    if 'additionalProperties' in spec and spec['additionalProperties'] is not False:
        raise ValueError('objects must disallow additional properties')


def load_schema():
    spec = json.loads(SCHEMA_PATH.read_text(encoding='utf-8'))
    audit_schema(spec)
    return spec


def public_url(value):
    try:
        u = urlsplit(value)
        return (u.scheme in ('http', 'https') and bool(u.hostname)
                and not u.username and not u.password
                and not re.search(r'\s', value)
                and (u.port is None or 0 < u.port < 65536))
    except ValueError:
        return False


def url_key(value):
    u = urlsplit(value)
    q = parse_qs(u.query)
    if u.hostname and (u.hostname == 'ppomppu.co.kr' or u.hostname.endswith('.ppomppu.co.kr')):
        return ('ppomppu', tuple(q.get('id', [])), tuple(q.get('no', [])))
    cleaned = tuple(sorted((k, tuple(v)) for k, v in q.items()
                           if not k.startswith('utm_') and k not in ('fbclid', 'gclid')))
    return (u.hostname, u.path.rstrip('/'), cleaned)


def check_value(value, spec, root, path='$'):
    if '$ref' in spec:
        spec = root['$defs'][spec['$ref'].split('/')[-1]]
    kind = spec['type']
    matches = {'object': isinstance(value, dict), 'array': isinstance(value, list),
               'string': isinstance(value, str), 'integer': type(value) is int,
               'number': type(value) in (int, float)}
    if not matches[kind]:
        return [f'{path}: expected {kind}']
    errors = []
    if 'enum' in spec and value not in spec['enum']:
        errors.append(f'{path}: invalid enum')
    if kind == 'object':
        for k in spec.get('required', []):
            if k not in value:
                errors.append(f'{path}.{k}: required field missing')
        for k, v in value.items():
            if k not in spec['properties']:
                errors.append(f'{path}.{k}: unknown field')
            else:
                errors.extend(check_value(v, spec['properties'][k], root, f'{path}.{k}'))
    elif kind == 'array':
        if len(value) < spec.get('minItems', 0):
            errors.append(f'{path}: too few items')
        if spec.get('uniqueItems') and len({json.dumps(v, sort_keys=True) for v in value}) != len(value):
            errors.append(f'{path}: duplicate items')
        for i, v in enumerate(value):
            errors.extend(check_value(v, spec['items'], root, f'{path}[{i}]'))
    elif kind == 'string':
        if not value.strip() or len(value) < spec.get('minLength', 0):
            errors.append(f'{path}: blank/short value; omit unknown optional fields')
        if len(value) > spec.get('maxLength', len(value)):
            errors.append(f'{path}: exceeds maximum string length')
        if value.startswith(('=', '+', '-', '@')):
            errors.append(f'{path}: spreadsheet formula prefix forbidden')
        if 'pattern' in spec and not re.fullmatch(spec['pattern'], value):
            errors.append(f'{path}: invalid pattern')
        if spec.get('format') == 'uri' and not public_url(value):
            errors.append(f'{path}: invalid public HTTP(S) URL')
        if spec.get('format') == 'date':
            try:
                if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
                    raise ValueError()
                datetime.date.fromisoformat(value)
            except ValueError:
                errors.append(f'{path}: invalid date')
    else:
        if not math.isfinite(value):
            errors.append(f'{path}: non-finite number')
        if 'minimum' in spec and value < spec['minimum']:
            errors.append(f'{path}: below minimum')
        if 'exclusiveMinimum' in spec and value <= spec['exclusiveMinimum']:
            errors.append(f'{path}: must exceed minimum')
    return errors


def sensitive_strings(value, path='$'):
    errors = []
    if isinstance(value, dict):
        for k, v in value.items():
            errors.extend(sensitive_strings(v, f'{path}.{k}'))
    elif isinstance(value, list):
        for i, v in enumerate(value):
            errors.extend(sensitive_strings(v, f'{path}[{i}]'))
    elif isinstance(value, str):
        patterns = [r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}',
                    r'(?<!\d)01[016789][- ]?\d{3,4}[- ]?\d{4}(?!\d)',
                    r'AKIA[0-9A-Z]{16}', r'gh[pousr]_[A-Za-z0-9]{20,}',
                    r'-----BEGIN [A-Z ]*PRIVATE KEY-----']
        if any(re.search(p, value) for p in patterns):
            errors.append(f'{path}: possible personal information or secret')
    return errors


def check_semantics(r):
    errors = []
    def error(path, message):
        errors.append(f'{path}: {message}')
    def index(items, path):
        result = {}
        for item in items:
            if item['id'] in result:
                error(path, 'duplicate local ID')
            result[item['id']] = item
        return result
    evidence = index(r['evidence'], '$.evidence')
    nodes = index(r['nodes'], '$.nodes')
    ports = index(r['ports'], '$.ports')
    configs = index(r['configurations'], '$.configurations')
    observations = index(r['observations'], '$.observations')
    index(r['attempts'], '$.attempts')
    author_ids = {k for k, e in evidence.items() if e['actor'] == 'CASE_AUTHOR'}
    def check_refs(value, path='$'):
        if isinstance(value, dict):
            if 'evidence_refs' in value:
                for identifier in value['evidence_refs']:
                    if identifier not in evidence:
                        error(path + '.evidence_refs', 'dangling evidence reference')
            for k, v in value.items():
                check_refs(v, path + '.' + k)
        elif isinstance(value, list):
            for i, v in enumerate(value):
                check_refs(v, f'{path}[{i}]')
    def author_refs(value, path):
        if not set(value['evidence_refs']).issubset(author_ids):
            error(path, 'actual report must use CASE_AUTHOR evidence only')
    check_refs(r)
    author_refs(r['case_classification'], '$.case_classification')
    author_refs(r['environment'], '$.environment')
    for e in r['evidence']:
        if e['kind'] in ('ORIGINAL_POST', 'AUTHOR_COMMENT', 'EDITED_POST') and e['actor'] != 'CASE_AUTHOR':
            error('$.evidence', 'author evidence kind requires CASE_AUTHOR')
        if e['kind'] == 'OTHER_COMMENT' and e['actor'] != 'OTHER':
            error('$.evidence', 'OTHER_COMMENT requires OTHER')
        if e.get('published_at', e['checked_at']) > e['checked_at']:
            error('$.evidence', 'publication after check date')
    for e in evidence.values():
        if ('author_configuration_terminations' in e or 'author_case_termination' in e) and e['actor'] != 'CASE_AUTHOR':
            error('$.evidence', 'explicit termination must be a CASE_AUTHOR declaration')
        declared_configs = set()
        for declaration in e.get('author_configuration_terminations', []):
            cid = declaration['configuration_id']
            if cid in declared_configs:
                error('$.evidence.author_configuration_terminations', 'duplicate configuration declaration')
            declared_configs.add(cid)
            if cid not in configs or configs[cid]['role'] != 'OBSERVED':
                error('$.evidence.author_configuration_terminations', 'declaration requires OBSERVED configuration')
    classification = r['case_classification']
    if 'LONG_TERM_REPORT' in classification['types'] and 'long_term_basis' not in classification:
        error('$.case_classification', 'LONG_TERM_REPORT requires explicit duration or continued-use basis')
    if 'long_term_basis' in classification:
        author_refs(classification['long_term_basis'], '$.case_classification.long_term_basis')
    author_refs(r['review']['commercial_context'], '$.review.commercial_context')
    source = r['source']
    if source.get('published_at', source['checked_at']) > source['checked_at']:
        error('$.source', 'publication after check date')
    publication_orders = [e['publication_sequence'] for e in r['evidence'] if 'publication_sequence' in e]
    if len(set(publication_orders)) != len(publication_orders):
        error('$.evidence.publication_sequence', 'duplicate publication order')
    for n in nodes.values():
        if n['kind'] == 'DISPLAY' and 'display_scope' not in n:
            error('$.nodes', 'DISPLAY requires explicit display_scope including UNKNOWN')
    for p in ports.values():
        if p['node_id'] not in nodes:
            error('$.ports', 'dangling node reference')
    for cfg in configs.values():
        members = set(cfg['node_ids'])
        if not members.issubset(nodes):
            error('$.configurations.node_ids', 'dangling node reference')
        if sum(nodes[n]['kind'] == 'SOURCE' for n in members if n in nodes) != 1:
            error('$.configurations', 'exactly one source node required')
        index(cfg['edges'], '$.configurations.edges')
        if cfg['role'] != 'ADVICE':
            author_refs(cfg, '$.configurations')
            for nid in members & nodes.keys():
                author_refs(nodes[nid], '$.nodes')
            for setting in cfg['settings']:
                author_refs(setting, '$.configurations.settings')
        graph = {n: set() for n in members}
        for edge in cfg['edges']:
            if cfg['role'] != 'ADVICE':
                author_refs(edge, '$.configurations.edges')
            if edge['from_port'] not in ports or edge['to_port'] not in ports:
                error('$.configurations.edges', 'dangling port reference')
                continue
            if cfg['role'] != 'ADVICE':
                for endpoint in ('from_port', 'to_port'):
                    author_refs(ports[edge[endpoint]], '$.ports')
            a, b = (ports[edge[k]]['node_id'] for k in ('from_port', 'to_port'))
            if a not in members or b not in members:
                error('$.configurations.edges', 'endpoint outside configuration')
                continue
            if a == b:
                error('$.configurations.edges', 'self-device connection forbidden')
            if edge['purpose'] in ('VIDEO', 'VIDEO_AND_POWER'):
                graph[a].add(b)
            if cfg['topology_completeness'] == 'COMPLETE_REPORTED' and edge['path_status'] == 'UNKNOWN_GAP':
                error('$.configurations', 'complete topology contains unknown gap')
        visited, active = set(), set()
        def cyclic(n):
            if n in active:
                return True
            if n in visited:
                return False
            active.add(n)
            if any(cyclic(child) for child in graph[n]):
                return True
            active.remove(n)
            visited.add(n)
            return False
        if any(cyclic(n) for n in graph if n not in visited):
            error('$.configurations.edges', 'video cycle')
        if cfg['topology_completeness'] == 'COMPLETE_REPORTED':
            sources = [n for n in members if n in nodes and nodes[n]['kind'] == 'SOURCE']
            reachable, queue = set(sources), list(sources)
            while queue:
                for child in graph[queue.pop()]:
                    if child not in reachable:
                        reachable.add(child)
                        queue.append(child)
            for nid in members:
                if nid in nodes and nodes[nid]['kind'] == 'DISPLAY' and nodes[nid].get('display_scope') != 'INTERNAL' and nid not in reachable:
                    error('$.configurations', 'complete video topology has unreachable display')
    for name in ('attempts', 'observations'):
        if [v['sequence'] for v in r[name]] != list(range(1, len(r[name]) + 1)):
            error('$.' + name, 'sequence must be unique contiguous presentation order')
    for a in r['attempts']:
        cfg = configs.get(a['configuration_id'])
        if not cfg or cfg['role'] != 'OBSERVED':
            error('$.attempts', 'attempt must reference OBSERVED configuration')
        author_refs(a, '$.attempts')
        for oid in a['observation_ids']:
            o = observations.get(oid)
            if not o or o['configuration_id'] != a['configuration_id']:
                error('$.attempts.observation_ids', 'missing observation or configuration mismatch')
        if a.get('author_confirmed_on', source['checked_at']) > source['checked_at']:
            error('$.attempts', 'confirmation after check date')
    for cid in r['goal']['configuration_ids']:
        if cid not in configs or configs[cid]['role'] != 'TARGET':
            error('$.goal.configuration_ids', 'goal must reference TARGET configuration')
    author_refs(r['goal'], '$.goal')
    def counts(c, path):
        author_refs(c, path)
        if c['basis'] == 'UNKNOWN' and any(k in c for k in ('connected', 'lit', 'independent_extended', 'mirrored')):
            error(path, 'numeric counts require a stated basis')
        for low, high in [('lit', 'connected'), ('independent_extended', 'lit'), ('mirrored', 'lit')]:
            if low in c and high in c and c[low] > c[high]:
                error(path, f'{low} exceeds {high}')
        if all(k in c for k in ('independent_extended', 'mirrored', 'lit')) and c['independent_extended'] + c['mirrored'] > c['lit']:
            error(path, 'extended and mirrored membership exceeds lit count')
    def mode_counts(c, states, path):
        if c['scope'] == 'UNKNOWN':
            return
        scoped = [state for state in states if state['node_id'] in nodes and
                  (c['scope'] == 'INCLUDING_INTERNAL' or
                   nodes[state['node_id']].get('display_scope') == 'EXTERNAL')]
        known_mirror = sum(state['lit'] == 'YES' and state.get('display_mode') == 'MIRROR' for state in scoped)
        known_extended = sum(state['lit'] == 'YES' and state.get('display_mode') == 'EXTEND' for state in scoped)
        for key, known in [('mirrored', known_mirror), ('independent_extended', known_extended)]:
            if key in c and c[key] < known:
                error(path, 'counts contradict known per-display mode')
        for bound in ('lit', 'connected'):
            if bound in c:
                if c.get('independent_extended', 0) + known_mirror > c[bound] or c.get('mirrored', 0) + known_extended > c[bound]:
                    error(path, 'mirror and extended membership overlap known display states')
                if all(key in c for key in ('independent_extended', 'mirrored')) and c['independent_extended'] + c['mirrored'] > c[bound]:
                    error(path, 'extended and mirrored membership exceeds physical bound')
    counts(r['goal']['counts'], '$.goal.counts')
    mode_counts(r['goal']['counts'], r['goal']['display_states'], '$.goal.counts')
    for o in observations.values():
        author_refs(o, '$.observations')
        cfg = configs.get(o['configuration_id'])
        if not cfg or cfg['role'] != 'OBSERVED':
            error('$.observations.configuration_id', 'actual state must reference OBSERVED configuration')
        counts(o['counts'], '$.observations.counts')
        mode_counts(o['counts'], o['display_states'], '$.observations.counts')
        seen = set()
        for state in o['display_states']:
            nid = state['node_id']
            if nid in seen:
                error('$.observations.display_states', 'duplicate display state')
            seen.add(nid)
            if nid not in nodes or nodes[nid]['kind'] != 'DISPLAY' or (cfg and nid not in cfg['node_ids']):
                error('$.observations.display_states', 'display outside configuration')
            author_refs(state, '$.observations.display_states')
        scope = o['counts']['scope']
        known_lit = sum(state['lit'] == 'YES' for state in o['display_states']
                        if state['node_id'] in nodes and
                        (scope == 'INCLUDING_INTERNAL' or
                         (scope == 'EXTERNAL_ONLY' and nodes[state['node_id']].get('display_scope') == 'EXTERNAL')))
        if scope != 'UNKNOWN' and 'lit' in o['counts'] and known_lit > o['counts']['lit']:
            error('$.observations.counts', 'known lit display states exceed count')
        if 'recurrence_of' in o:
            prior = observations.get(o['recurrence_of'])
            if not prior or prior['sequence'] >= o['sequence'] or prior['signal_state'] != 'NORMAL':
                error('$.observations.recurrence_of', 'must reference earlier NORMAL observation')
            if o['durability'] != 'RECURRENT':
                error('$.observations.durability', 'recurrence link requires RECURRENT')
        elif o['durability'] == 'RECURRENT':
            error('$.observations', 'RECURRENT requires recurrence_of')
        if o.get('observed_on', source['checked_at']) > source['checked_at']:
            error('$.observations', 'observation after check date')
    target_nodes = {nid for cid in r['goal']['configuration_ids'] if cid in configs for nid in configs[cid]['node_ids']}
    for state in r['goal']['display_states']:
        if state['node_id'] not in nodes or nodes[state['node_id']]['kind'] != 'DISPLAY':
            error('$.goal.display_states', 'invalid display reference')
        if state['node_id'] not in target_nodes:
            error('$.goal.display_states', 'display outside target configurations')
        author_refs(state, '$.goal.display_states')
    outcome = r['outcome']
    author_refs(outcome, '$.outcome')
    for oid in outcome['observation_ids']:
        if oid not in observations:
            error('$.outcome.observation_ids', 'dangling observation reference')
    allowed = {'SUCCESS': {'GOAL_MET_REPORTED'}, 'LIMITED_SUCCESS': {'PARTIAL_OR_CONDITIONAL'},
               'FAILURE': {'FINAL_FAILURE_REPORTED', 'ABANDONED_REPORTED'},
               'UNRESOLVED': {'OPEN'}, 'UNKNOWN': {'UNKNOWN'}}
    if outcome['closure'] not in allowed[outcome['status']]:
        error('$.outcome', 'status/closure mismatch; no signal is not final FAILURE')
    if outcome['status'] not in ('UNKNOWN', 'FAILURE') and not outcome['observation_ids']:
        error('$.outcome', 'reported outcome requires observation evidence')
    if outcome['status'] == 'FAILURE':
        if not any(evidence[eid].get('author_case_termination', {}).get('termination_type') == outcome['closure']
                   for eid in outcome['evidence_refs'] if eid in author_ids):
            error('$.outcome', 'FAILURE requires an explicit author case termination; configuration failure alone is insufficient')
    concluded = set()
    for conclusion in r.get('configuration_conclusions', []):
        cid = conclusion['configuration_id']
        path = '$.configuration_conclusions'
        if cid in concluded:
            error(path, 'one conclusion per configuration; conflicting duplicates forbidden')
        concluded.add(cid)
        if cid not in configs or configs[cid]['role'] != 'OBSERVED':
            error(path, 'conclusion requires OBSERVED configuration')
        author_refs(conclusion, path)
        for oid in conclusion.get('observation_ids', []):
            if oid not in observations or observations[oid]['configuration_id'] != cid:
                error(path + '.observation_ids', 'observation must belong to concluded configuration')
        if conclusion['termination_type'] not in allowed[conclusion['status']]:
            error(path, 'status/termination_type mismatch')
        if conclusion['status'] == 'FAILURE':
            supported = any(declaration['configuration_id'] == cid and
                            declaration['termination_type'] == conclusion['termination_type']
                            for eid in conclusion['evidence_refs'] if eid in author_ids
                            for declaration in evidence[eid].get('author_configuration_terminations', []))
            if not supported:
                error(path, 'FAILURE requires a scoped explicit author configuration termination; NO_SIGNAL or silence is insufficient')
        # Never infer or overwrite the case outcome from this array.
    for link in r['product_links']:
        if link['node_id'] not in nodes:
            error('$.product_links', 'dangling node reference')
    if 'UNKNOWN' in r['case_classification']['types'] and len(r['case_classification']['types']) > 1:
        error('$.case_classification', 'UNKNOWN must stand alone')
    migration = r.get('migration')
    if migration and migration['source_record_id'] != r['id']:
        error('$.migration', 'v1 ID must be preserved')
    errors.extend(sensitive_strings(r))
    return errors


def validate_record(record, schema=None):
    schema = schema or load_schema()
    errors = check_value(record, schema, schema)
    return errors if errors else check_semantics(record)


def unique_object(pairs):
    result = {}
    for k, v in pairs:
        if k in result:
            raise ValueError('duplicate JSON key')
        result[k] = v
    return result


def reject_constant(_):
    raise ValueError('non-finite JSON constant')


def validate_files(paths):
    schema = load_schema()
    errors, ids, urls = [], set(), set()
    for path in paths:
        try:
            with Path(path).open(encoding='utf-8') as f:
                any_line = False
                for number, line in enumerate(f, 1):
                    any_line = True
                    prefix = f'{path}: line {number}'
                    try:
                        record = json.loads(line, object_pairs_hook=unique_object, parse_constant=reject_constant)
                    except (ValueError, RecursionError):
                        errors.append(f'{prefix}: invalid JSON/object keys')
                        continue
                    local = validate_record(record, schema)
                    if not local:
                        identifier, key = record['id'], url_key(record['source']['source_url'])
                        if identifier in ids:
                            local.append('$.id: duplicate corpus ID')
                        if key in urls:
                            local.append('$.source.source_url: duplicate canonical URL')
                        ids.add(identifier)
                        urls.add(key)
                    errors.extend(f'{prefix}: {e}' for e in local)
                if not any_line:
                    errors.append(f'{path}: empty v2 corpus file')
        except (OSError, UnicodeError) as exc:
            errors.append(f'{path}: file error: {type(exc).__name__}')
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('files', nargs='*', type=Path)
    args = parser.parse_args(argv)
    paths = args.files or [DEFAULT_FILE]
    try:
        errors = validate_files(paths)
    except (ValueError, KeyError) as exc:
        print(f'schema error: {exc}', file=sys.stderr)
        return 1
    for error in errors:
        print(error, file=sys.stderr)
    if not errors:
        print('PASS: authoritative v2 JSONL: ' + ', '.join(str(p) for p in paths))
    return int(bool(errors))


if __name__ == '__main__':
    raise SystemExit(main())
