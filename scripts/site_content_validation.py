"""Strict validation of the site data contract, without network or inference."""
from datetime import date
from math import isfinite
from urllib.parse import urlsplit
from pathlib import Path
import json


def fail(path, message):
    raise ValueError(f'{path}: {message}')


def refs(value, path, targets=None, required=True):
    if not isinstance(value, list) or (required and not value):
        fail(path, 'expected nonempty reference array' if required else 'expected reference array')
    if any(not isinstance(v, str) or not v.strip() for v in value) or len(value) != len(set(value)):
        fail(path, 'references must be unique nonempty strings')
    if targets is not None and not set(value) <= set(targets):
        fail(path, 'dangling reference')


def checked_date(value, path, unknown=False):
    if unknown and value == 'UNKNOWN':
        return
    try:
        if not isinstance(value, str) or date.fromisoformat(value).isoformat() != value:
            raise ValueError()
    except (ValueError, TypeError):
        fail(path, 'expected YYYY-MM-DD')


def https_url(value, path):
    try:
        u = urlsplit(value)
        if (not isinstance(value, str) or any(c.isspace() for c in value)
                or u.scheme != 'https' or not u.hostname or u.username or u.password):
            raise ValueError()
        u.port
    except (ValueError, TypeError):
        fail(path, 'expected credential-free HTTPS URL')


def payload(fact, path):
    """Site-specific contracts preserve UNKNOWN; they are not engine rules."""
    p = fact.get('payload')
    prop = fact.get('property')
    specifications = {
        'VIDEO_PROFILE': ({'scope'}, {'scope', 'width', 'height', 'refresh_hz', 'interface', 'resolution_label', 'rating_basis'}),
        'PROTOCOL': ({'interface', 'protocol', 'support'}, {'interface', 'protocol', 'support', 'mode', 'version'}),
        'POWER_TRANSFER': ({'mode', 'interface', 'watts', 'rating_basis'}, {'mode', 'interface', 'watts', 'rating_basis', 'label'}),
        'PORTS': ({'interfaces'}, {'interfaces'}),
        'VESA': ({'width_mm', 'height_mm'}, {'width_mm', 'height_mm'}),
        'TILT': ({'min_degrees', 'max_degrees'}, {'min_degrees', 'max_degrees'}),
    }
    for name in ('KVM', 'SPEAKERS', 'HEIGHT_ADJUSTMENT', 'PIP_PBP', 'REMOTE_CONTROL'):
        specifications[name] = ({'support'}, {'support'})
    if prop not in specifications or not isinstance(p, dict):
        fail(path, 'unsupported property or payload type')
    required, allowed = specifications[prop]
    if not required <= p.keys() or not p.keys() <= allowed:
        fail(path, 'missing or unexpected typed payload fields')
    if prop == 'VIDEO_PROFILE' and not ({'width', 'height', 'refresh_hz'} <= p.keys() or 'resolution_label' in p):
        fail(path, 'video profile needs dimensions or reported resolution label')
    enums = {
        'scope': {'PANEL', 'PORT'},
        'support': {'SUPPORTED', 'UNSUPPORTED', 'UNKNOWN'},
        'protocol': {'DISPLAYPORT', 'HDMI', 'THUNDERBOLT', 'USB4', 'USB_DATA', 'UNKNOWN'},
        'mode': {'OFFER', 'PASS_THROUGH', 'TRANSPORT_LIMIT', 'UNKNOWN'} if prop == 'POWER_TRANSFER' else None,
        'rating_basis': {'UP_TO', 'RATED', 'MANUFACTURER_STATED', 'PRODUCT_LABEL_ONLY', 'UNKNOWN'},
    }
    for key, value in p.items():
        if key in ('width', 'height', 'width_mm', 'height_mm', 'refresh_hz', 'watts', 'min_degrees', 'max_degrees'):
            if value == 'UNKNOWN':
                continue
            if type(value) not in (int, float) or not isfinite(value):
                fail(path+'.'+key, 'expected finite number or UNKNOWN')
            if key not in ('min_degrees', 'max_degrees') and value <= 0:
                fail(path+'.'+key, 'expected positive value')
            if key in ('width', 'height', 'width_mm', 'height_mm') and type(value) is not int:
                fail(path+'.'+key, 'expected integer dimensions')
        elif key == 'interfaces':
            refs(value, path+'.interfaces')
        elif not isinstance(value, str) or not value.strip():
            fail(path+'.'+key, 'expected nonempty text')
        if enums.get(key) is not None and value not in enums[key]:
            fail(path+'.'+key, 'invalid enum')
    if prop == 'TILT' and all(type(p[k]) in (int, float) for k in ('min_degrees', 'max_degrees')):
        if p['min_degrees'] > p['max_degrees']:
            fail(path, 'reversed tilt range')
    if prop == 'POWER_TRANSFER' and p['rating_basis'] == 'PRODUCT_LABEL_ONLY' and p['watts'] != 'UNKNOWN':
        fail(path, 'product label is not numeric power evidence')


def unique(items, field, path):
    if not isinstance(items, list):
        fail(path, 'expected array')
    result = {}
    for item in items:
        key = item.get(field) if isinstance(item, dict) else None
        if not isinstance(key, str) or not key.strip() or key in result:
            fail(path, 'missing or duplicate ID')
        result[key] = item
    return result


def validate_content(data):
    """Validate both full content and public projection reference targets."""
    maps = {k: unique(data[k], 'id', k) for k in ('monitors', 'reviews', 'guides')}
    all_ids = [i for m in maps.values() for i in m]
    source_cache = {}
    if len(all_ids) != len(set(all_ids)):
        fail('$', 'duplicate global ID')
    for kind, records in maps.items():
        for ident, item in records.items():
            path = kind+'/'+ident
            sources = item.get('source_refs')
            if not isinstance(sources, list) or not sources:
                fail(path, 'missing source evidence')
            source_ids = unique(sources, 'record_id', path+'/sources')
            for s in sources:
                https_url(s.get('url'), path+'/url')
                checked_date(s.get('checked_on'), path+'/checked_on')
                checked_date(s.get('published_on'), path+'/published_on', unknown=True)
                if 'source_file' in s:
                    root = Path(__file__).resolve().parents[1]
                    file = (root/s['source_file']).resolve()
                    if not file.is_relative_to(root) or not file.is_file():
                        fail(path+'/source_file', 'missing or outside-repository source file')
                    if file not in source_cache:
                        text = file.read_text(encoding='utf-8')
                        raw = [json.loads(line) for line in text.splitlines() if line.strip()] if file.suffix == '.jsonl' else json.loads(text)
                        candidates = raw if isinstance(raw, list) else raw.get('sources', [])
                        source_cache[file] = {r.get('source_id', r.get('id')): r for r in candidates}
                    record = source_cache[file].get(s['record_id'])
                    if record is None:
                        fail(path+'/record_id', 'source record not found')
                    origin = record.get('mapping', record)
                    original_url = origin.get('source', origin).get('source_url', origin.get('url'))
                    if original_url != s['url']:
                        fail(path+'/url', 'source URL differs from original record')
            for field, target in [('monitor_ids', 'monitors'), ('related_monitor_ids', 'monitors'), ('related_review_ids', 'reviews')]:
                if field in item:
                    refs(item[field], path+'/'+field, maps[target], required=False)
            if kind == 'monitors':
                facts = unique(item['features'], 'fact_id', path+'/features')
                for f in facts.values():
                    payload(f, path+'/'+f['fact_id'])
                    refs(f.get('source_refs'), path+'/fact.source_refs', source_ids)
                    if f.get('basis') != 'MANUFACTURER_SPEC':
                        fail(path, 'official feature needs manufacturer basis')
                capability_properties = {'usb_c_video': 'PROTOCOL', 'pd_supply': 'POWER_TRANSFER', 'kvm': 'KVM', 'speakers': 'SPEAKERS', 'height_adjustment': 'HEIGHT_ADJUSTMENT'}
                for name, cap in item.get('capabilities', {}).items():
                    if name not in capability_properties:
                        fail(path+'/capability', 'unsupported capability')
                    if cap.get('status') not in ('CONFIRMED_MANUFACTURER_STATEMENT', 'UNKNOWN'):
                        fail(path+'/capability', 'invalid capability status')
                    refs(cap.get('feature_refs'), path+'/capability', facts, required=cap.get('status') == 'CONFIRMED_MANUFACTURER_STATEMENT')
                    for ref in cap['feature_refs']:
                        fact = facts[ref]
                        if fact['property'] != capability_properties[name]:
                            fail(path+'/capability', 'feature property does not match capability')
                        if cap['status'] == 'CONFIRMED_MANUFACTURER_STATEMENT':
                            p = fact['payload']
                            if name == 'pd_supply':
                                valid = p['mode'] == 'OFFER'
                            else:
                                valid = p['support'] == 'SUPPORTED'
                            if name == 'usb_c_video':
                                valid = valid and p['interface'].startswith('USB_C')
                            if not valid:
                                fail(path+'/capability', 'confirmed capability lacks matching supported fact')
            if kind == 'reviews':
                local = {k: unique(item[k], 'id', path+'/'+k) for k in ('nodes', 'ports', 'evidence', 'configurations', 'observations', 'attempts')}
                ids = [i for objects in local.values() for i in objects]
                if len(ids) != len(set(ids)):
                    fail(path, 'duplicate local object ID')
                def walk(value):
                    if isinstance(value, dict):
                        for key, v in value.items():
                            targets = {'evidence_refs': 'evidence', 'node_ids': 'nodes', 'observation_ids': 'observations'}
                            singles = {'node_id': 'nodes', 'configuration_id': 'configurations', 'observation_id': 'observations', 'recurrence_of': 'observations', 'from_port': 'ports', 'to_port': 'ports'}
                            if key in targets:
                                refs(v, path+'/'+key, local[targets[key]], required=False)
                            elif key in singles and v not in local[singles[key]]:
                                fail(path+'/'+key, 'dangling local reference')
                            else:
                                walk(v)
                    elif isinstance(value, list):
                        for v in value:
                            walk(v)
                for field in ('nodes', 'ports', 'configurations', 'observations', 'attempts', 'functional_observations', 'configuration_conclusions'):
                    walk(item.get(field, []))
                for link in item.get('monitor_links', []):
                    if link['review_id'] != ident or link['monitor_id'] not in item['monitor_ids'] or link['node_id'] not in local['nodes']:
                        fail(path+'/monitor_links', 'invalid review/product/node reference')
                    refs(link.get('source_refs'), path+'/link.source_refs', source_ids)
    return data
