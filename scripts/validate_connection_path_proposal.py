"""Structural proposal validation only; never compatibility approval."""
import json
from pathlib import Path
from scripts.validate_question_corpus_v2 import audit_schema, check_value

ROOT = Path(__file__).resolve().parents[1]


def validate(data):
    spec = json.loads((ROOT / 'schemas/connection-path-v1.proposed.schema.json').read_text())
    audit_schema(spec)
    errors = check_value(data, spec, spec)
    if errors:
        return errors
    tables = {}
    seen = set()
    for name in ['devices', 'ports', 'capabilities', 'edges', 'paths']:
        tables[name] = {r['id']: r for r in data[name]}
        for row in data[name]:
            if row['id'] in seen:
                errors.append(f"{name}.{row['id']}: duplicate object ID")
            seen.add(row['id'])
    devices, ports, caps, edges = [tables[k] for k in ['devices', 'ports', 'capabilities', 'edges']]
    for row in devices.values():
        if row['identity_status'] == 'EXACT' and 'product_ref' not in row:
            errors.append(f"{row['id']}: EXACT requires product_ref")
    for row in ports.values():
        if row['device_id'] not in devices:
            errors.append(f"{row['id']}: missing device")
    for row in list(ports.values()) + list(edges.values()):
        if not set(row['capability_refs']).issubset(caps):
            errors.append(f"{row['id']}: missing capability")
    subjects = set(devices) | set(ports) | set(edges)
    for row in caps.values():
        if row['subject_id'] not in subjects:
            errors.append(f"{row['id']}: missing capability subject")
    for row in edges.values():
        if row['from_port'] not in ports or row['to_port'] not in ports:
            errors.append(f"{row['id']}: missing endpoint")
            continue
        a, b = ports[row['from_port']], ports[row['to_port']]
        same_device = a['device_id'] == b['device_id']
        if (row['kind'] == 'INTERNAL_ROUTING') != same_device:
            errors.append(f"{row['id']}: routing kind/device mismatch")
    for path in tables['paths'].values():
        source = devices.get(path['source_device_id'])
        if not source or source['kind'] != 'SOURCE':
            errors.append(f"{path['id']}: missing source device")
        if not set(path['edge_ids']).issubset(edges):
            errors.append(f"{path['id']}: missing edge")
            continue
        targets = [t['display_device_id'] for t in path['display_targets']]
        if len(set(targets)) != len(targets):
            errors.append(f"{path['id']}: duplicate display target")
        for target in targets:
            if target not in devices or devices[target]['kind'] != 'DISPLAY':
                errors.append(f"{path['id']}: missing display device")
        if path['topology_completeness'] == 'COMPLETE':
            reachable = {p['id'] for p in ports.values() if p['device_id'] == path['source_device_id']}
            selected = [edges[e] for e in path['edge_ids']]
            for _ in range(len(selected)):
                for edge in selected:
                    if edge['from_port'] in reachable:
                        reachable.add(edge['to_port'])
            if not targets:
                errors.append(f"{path['id']}: complete path needs target")
            for target in targets:
                if not any(p['id'] in reachable for p in ports.values() if p['device_id'] == target):
                    errors.append(f"{path['id']}: unreachable display {target}")
    return errors
