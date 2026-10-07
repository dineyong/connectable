"""Internal path review slice. No public compatibility approval or gold approval."""
import json
import hashlib
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.validate_question_corpus_v2 import audit_schema, check_value, unique_object, reject_constant
from scripts.validate_connection_model_pilot import load_pilot, validate as validate_pilot
from scripts.validate_official_products import load_catalog, validate_catalog
from scripts.evaluate_display_count_candidate import evaluate as evaluate_count

ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / 'data/rules/path_instances_v1.json'


def load_instances():
    return json.loads(FILE.read_text(encoding='utf-8'), object_pairs_hook=unique_object, parse_constant=reject_constant)


def claim_index():
    pilot, catalog = load_pilot(), load_catalog()
    errors = validate_pilot(pilot) + validate_catalog(catalog)
    if errors:
        raise ValueError('invalid source datasets: ' + '; '.join(errors))
    claims = {f['fact_id']: f for f in pilot['facts']}
    for product in catalog['products']:
        for claim in product['claims']:
            claims[claim['claim_id']] = {**claim, 'product_id': product['product_id']}
    products = {p['product_id']: p for p in pilot['products'] + catalog['products']}
    return claims, products


def predicate_value(predicate, context):
    actual = context.get(predicate['context_key'])
    if actual is None or actual == 'UNKNOWN':
        return 'UNKNOWN'
    expected = predicate['expected']
    op = predicate['operator']
    if op in ('EQ', 'NEQ'):
        equals = actual == expected
        return 'TRUE' if equals == (op == 'EQ') else 'FALSE'
    if op != 'VERSION_GTE':
        raise ValueError('unsupported predicate operator')
    def version(value):
        if not isinstance(value, str) or not re.fullmatch(r'\d+\.\d+(?:\.\d+)?', value):
            return None
        nums = [int(x) for x in value.split('.')]
        return tuple(nums + [0] * (3 - len(nums)))
    left, right = version(actual), version(expected)
    if left is None or right is None:
        return 'UNKNOWN'
    return 'TRUE' if left >= right else 'FALSE'


def predicate_supported(predicate, claims):
    key, op, value = predicate['context_key'], predicate['operator'], predicate['expected']
    for ref in predicate['claim_refs']:
        claim = claims.get(ref, {})
        payload = claim.get('payload', {})
        if key == 'os_family' and op == 'NEQ' and value in payload.get('excluded_os', []):
            return True
        if key == 'os_version' and op == 'VERSION_GTE' and value == payload.get('minimum_macos'):
            return True
        if key == 'displaylink_driver' and op == 'EQ' and value == 'INSTALLED' and payload.get('driver_required') == 'YES':
            return True
        prerequisites = claim.get('prerequisites', {})
        if key in ('builtin_state', 'lid_state') and op == 'EQ' and value == prerequisites.get(key):
            return True
        if key == 'os_version' and op == 'VERSION_GTE' and value == prerequisites.get('minimum_macos'):
            return True
        if key == 'external_power' and op == 'EQ' and value == 'PRESENT' and prerequisites.get('power_required') == 'YES':
            return True
        target = {'host_dsc':'HOST', 'display_dsc':'DISPLAY'}.get(key)
        if target and op == 'EQ' and value == 'SUPPORTED' and any(r['target'] == target and r['feature'] == 'DSC' for r in payload.get('requirements', [])):
            return True
    return False


def validate(data, claims=None, products=None):
    if claims is None or products is None:
        claims, products = claim_index()
    schema = json.loads((ROOT / 'schemas/path-instance-v1.schema.json').read_text())
    audit_schema(schema)
    errors = check_value(data, schema, schema)
    if errors:
        return errors
    case_ids = [r['id'] for r in data['instances']]
    if len(set(case_ids)) != len(case_ids):
        errors.append('duplicate instance ID')
    for instance in data['instances']:
        prefix = instance['id']
        tables = {name:{r['id']:r for r in instance[name]} for name in ('devices','ports','edges','bindings','predicates','resources','power_flows')}
        seen = set()
        for name in tables:
            for row in instance[name]:
                if row['id'] in seen:
                    errors.append(f'{prefix}.{name}: duplicate local object ID {row["id"]}')
                seen.add(row['id'])
        devices, ports, edges = [tables[k] for k in ('devices','ports','edges')]
        def owner(subject):
            if subject in devices:
                return [subject]
            if subject in ports:
                return [ports[subject]['device_id']]
            if subject in edges:
                e = edges[subject]
                return [ports[p]['device_id'] for p in (e['from_port'],e['to_port']) if p in ports]
            return []
        def check_refs(subject, refs):
            owners = [devices.get(d, {}).get('product_ref') for d in owner(subject)]
            for ref in refs:
                if ref not in claims or claims[ref]['product_id'] not in owners:
                    errors.append(f'{prefix}.{subject}: wrong/missing product claim {ref}')
        for d in devices.values():
            product = products.get(d.get('product_ref'))
            if d['identity_status'] != 'UNKNOWN' and not product:
                errors.append(f'{prefix}.{d["id"]}: unresolved product')
            if d['identity_status'] == 'EXACT' and product and product.get('identity_status') == 'PARTIAL':
                errors.append(f'{prefix}.{d["id"]}: partial catalog cannot become exact')
        for p in ports.values():
            if p['device_id'] not in devices:
                errors.append(f'{prefix}.{p["id"]}: missing device')
            check_refs(p['id'],p['claim_refs'])
            for ref in p['claim_refs']:
                claim = claims.get(ref, {})
                payload = claim.get('payload', {})
                if claim.get('property') == 'VIDEO_PROFILE' and payload.get('scope') == 'PORT':
                    if payload['interface'] != p['connector']:
                        errors.append(f'{prefix}.{p["id"]}: port-specific capability on wrong connector')
            if p['binding_precision'] != 'UNKNOWN' and not p['claim_refs']:
                errors.append(f'{prefix}.{p["id"]}: identified port requires claim')
        adjacency = {}
        physical_used = set()
        for e in edges.values():
            if e['from_port'] not in ports or e['to_port'] not in ports:
                errors.append(f'{prefix}.{e["id"]}: missing port')
                continue
            a,b = ports[e['from_port']],ports[e['to_port']]
            same = a['device_id'] == b['device_id']
            if (e['kind']=='INTERNAL_ROUTING') != same:
                errors.append(f'{prefix}.{e["id"]}: wrong routing kind')
            if e['kind']=='PHYSICAL':
                if a['connector'] != b['connector'] and 'UNKNOWN' not in (a['connector'],b['connector']):
                    errors.append(f'{prefix}.{e["id"]}: connector mismatch')
                for endpoint in (e['from_port'],e['to_port']):
                    if endpoint in physical_used:
                        errors.append(f'{prefix}.{e["id"]}: physical port multiply connected')
                    physical_used.add(endpoint)
            adjacency.setdefault(e['from_port'],[]).append(e['to_port'])
            check_refs(e['id'],e['claim_refs'])
        visited, active = set(), set()
        def walk(node):
            if node in active:
                errors.append(f'{prefix}: cyclic video path')
                return
            if node in visited:
                return
            visited.add(node); active.add(node)
            for nxt in adjacency.get(node,[]):
                walk(nxt)
            active.remove(node)
        for p in ports:
            if p not in visited:
                walk(p)
        src = devices.get(instance['source_device_id'])
        if not src or src['kind'] != 'SOURCE':
            errors.append(f'{prefix}: wrong source')
        reachable = {p['id'] for p in ports.values() if p['device_id']==instance['source_device_id']}
        for _ in edges:
            for a, dests in adjacency.items():
                if a in reachable:
                    reachable.update(dests)
        targets = instance['request']['display_device_ids']
        for target in targets:
            if devices.get(target, {}).get('kind') != 'DISPLAY' or not any(p['id'] in reachable for p in ports.values() if p['device_id']==target):
                errors.append(f'{prefix}: unreachable display {target}')
        if instance['request']['independent_external_count'] != len(targets):
            errors.append(f'{prefix}: target/count mismatch')
        if sorted(t['display_device_id'] for t in instance['request']['targets']) != sorted(targets):
            errors.append(f'{prefix}: timing target mismatch')
        for binding in tables['bindings'].values():
            if not owner(binding['subject_id']):
                errors.append(f'{prefix}: missing binding subject')
            check_refs(binding['subject_id'],[binding['claim_ref']])
            claim = claims.get(binding['claim_ref'], {})
            edge = edges.get(binding['subject_id'])
            if edge and claim.get('property') == 'CONVERSION' and edge['from_port'] in ports and edge['to_port'] in ports:
                payload = claim['payload']
                if ports[edge['from_port']]['connector'] != payload['from_connector'] or ports[edge['to_port']]['connector'] != payload['to_connector']:
                    errors.append(f'{prefix}.{binding["id"]}: unsupported conversion direction')
        for predicate in tables['predicates'].values():
            present_products = {d.get('product_ref') for d in devices.values()}
            if any(claims.get(ref,{}).get('product_id') not in present_products for ref in predicate['claim_refs']):
                errors.append(f'{prefix}.{predicate["id"]}: predicate from unrelated product')
            if not predicate_supported(predicate,claims):
                errors.append(f'{prefix}.{predicate["id"]}: predicate not supported by claim')
        for resource in tables['resources'].values():
            claim=claims.get(resource['claim_ref'],{})
            if claim.get('product_id') != devices.get(resource['device_id'],{}).get('product_ref') or claim.get('property')!='ROUTING' or resource['max_independent_displays'] != claim.get('payload',{}).get('max_independent_displays'):
                errors.append(f'{prefix}.{resource["id"]}: resource claim mismatch')
            for port in resource['output_port_ids']:
                if ports.get(port,{}).get('device_id') != resource['device_id']:
                    errors.append(f'{prefix}.{resource["id"]}: resource port mismatch')
            if resource['allocation_status'] != 'AGGREGATE_ONLY':
                errors.append(f'{prefix}: channel mapping unverified in v1')
        power_links = {(e['from_port'], e['to_port']) for e in edges.values()}
        power_seen = set()
        for flow in tables['power_flows'].values():
            pair = (flow['from_port'], flow['to_port'])
            if pair in power_seen or pair[0] == pair[1]:
                errors.append(f'{prefix}.{flow["id"]}: duplicate/self power flow')
            power_seen.add(pair)
            a, b = ports.get(pair[0], {}), ports.get(pair[1], {})
            if a and b and a['device_id'] != b['device_id'] and pair not in power_links and pair[::-1] not in power_links:
                errors.append(f'{prefix}.{flow["id"]}: power flow lacks physical connection')
            if flow['from_port'] not in ports or flow['to_port'] not in ports:
                errors.append(f'{prefix}.{flow["id"]}: missing power endpoint')
            check_refs(flow['from_port'], flow['claim_refs'])
            if flow['mode'] != 'REQUIREMENT_UNKNOWN':
                if len(flow['claim_refs']) != 1 or claims.get(flow['claim_refs'][0],{}).get('payload',{}).get('mode') != flow['mode']:
                    errors.append(f'{prefix}.{flow["id"]}: wrong power mode claim')
            elif flow['claim_refs']:
                errors.append(f'{prefix}: unknown requirement cannot assert power claim')
    return errors


def evaluate(instance, claims=None):
    indexed, products = claim_index()
    claims = indexed if claims is None else claims
    errors = validate(dict(version='1',status='REVIEW_CANDIDATES',instances=[instance]),claims,products)
    if errors:
        raise ValueError('; '.join(errors))
    predicate_results = [{'id':p['id'],'result':predicate_value(p,instance['request']['context']),
                          'claim_refs':p['claim_refs']} for p in instance['predicates']]
    contradicted = [p for p in predicate_results if p['result']=='FALSE']
    ports = {p['id']:p for p in instance['ports']}
    adjacency = {}
    for edge in instance['edges']:
        adjacency.setdefault(edge['from_port'], []).append(edge['to_port'])
    def reachable_targets(start):
        reachable, pending = set(), [start]
        while pending:
            node = pending.pop()
            if node in reachable:
                continue
            reachable.add(node)
            pending.extend(adjacency.get(node,[]))
        return {p['device_id'] for p in ports.values() if p['id'] in reachable and p['device_id'] in instance['request']['display_device_ids']}
    resource_results=[]
    for resource in instance['resources']:
        # Overall dock limit is a necessary constraint, not channel-pair approval.
        selected_targets = set()
        for port in resource['output_port_ids']:
            selected_targets.update(reachable_targets(port))
        resource_results.append(dict(id=resource['id'],selected_display_count=len(selected_targets),status='EXCEEDED' if len(selected_targets) > resource['max_independent_displays'] else 'WITHIN_AGGREGATE_LIMIT',claim_ref=resource['claim_ref']))
    exceeded = any(r['status']=='EXCEEDED' for r in resource_results)
    source = next(d for d in instance['devices'] if d['id']==instance['source_device_id'])
    context = instance['request']['context']
    builtin = {'ON':True, 'OFF':False}.get(context.get('builtin_state'))
    source_constraint = evaluate_count(dict(product_id=source.get('product_ref') if source['identity_status']=='EXACT' else None,
        output_method=instance['request']['output_method'],builtin_active=builtin,
        lid_state=context.get('lid_state'),external_independent_count=instance['request']['independent_external_count']))
    source_exceeded = source_constraint['candidate_status']=='INCOMPATIBLE'
    power_claims=[claims[ref]['payload'] for flow in instance['power_flows'] for ref in flow['claim_refs']]
    ceilings=[p['watts'] for p in power_claims if 'watts' in p]
    request_data = {k:v for k,v in instance.items() if k not in ('review_expectation','expectation_reason')}
    digest = lambda value: hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
    return dict(request_sha256=digest(request_data),catalog_sha256=digest({'pilot':load_pilot(),'mac':load_catalog(),'effective_claims':claims}),rule_version='path-instance-v1.0',instance_id=instance['id'],public_status='UNKNOWN',review_status='PENDING_HUMAN_REVIEW',
                candidate_status='INCOMPATIBLE' if contradicted or exceeded or source_exceeded else 'UNKNOWN',
                rule_status='CONTRADICTED' if contradicted or exceeded or source_exceeded else 'INSUFFICIENT_DATA',
                predicates=predicate_results,resources=resource_results,source_constraint=source_constraint,
                power=dict(status='UNKNOWN',recorded_ceiling_w=min(ceilings) if ceilings else None,
                           meaning='upper bound only; not negotiated or accepted charging power'),
                missing_fields=instance['missing_fields'],reason='explicit prerequisite/resource contradiction' if contradicted or exceeded or source_exceeded else 'full path capabilities and review incomplete')


if __name__ == '__main__':
    data=load_instances()
    errors=validate(data)
    if errors:
        print('\n'.join(errors));raise SystemExit(1)
    if '--check' in sys.argv:
        for row in data['instances']:
            evaluate(row)
        print(f'PASS: {len(data["instances"])} internal review candidates; 0 approved gold')
    else:
        print(json.dumps([evaluate(r) for r in data['instances']],ensure_ascii=False,indent=2))
