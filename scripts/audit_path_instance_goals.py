"""Review-only goal audit for the first five scenarios; never gold acceptance.

The contracts below transcribe only explicit draft goals. Missing goals stay
missing. The user specified UHD 3840x2160 at 60Hz for GP-02/03 only.
"""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.path_instance_v1 import ROOT, load_instances, claim_index, validate

CONTRACTS = {
    'GP-02': ('M1 Air USB-C→DP UHD 3840×2160 60Hz', 'product:air-m1-2020', 'NATIVE', 'DISPLAYPORT'),
    'GP-03': ('M1 Air USB-C→HDMI UHD 3840×2160 60Hz', 'product:air-m1-2020', 'NATIVE', 'HDMI'),
    'GP-06': ('M1 Air DisplayLink 외장 2대', 'product:air-m1-2020', 'DISPLAYLINK', None),
    'GP-07': ('M2 Air USB-C 직결', 'product:air-m2-2022', 'NATIVE', 'USB_C'),
    'GP-25': ('MST 경로 macOS', None, None, None),
}


UNSPECIFIED_GOALS = {
    'GP-02': ['external_display_count', 'charging_goal'],
    'GP-03': ['external_display_count', 'charging_goal'],
    'GP-06': ['resolution', 'refresh_hz', 'charging_goal'],
    'GP-07': ['resolution', 'refresh_hz', 'external_display_count', 'charging_goal'],
    'GP-25': ['source_device_model', 'resolution', 'refresh_hz',
              'external_display_count', 'charging_goal'],
}


def audit_goal(instance, plan_text=None, claims=None):
    if plan_text is None:
        plan_text = (ROOT / 'docs/CONNECTION_GOLD_SET_PLAN.md').read_text(encoding='utf-8')
    if claims is None:
        claims, _ = claim_index()
    goal = instance['gold_plan_id']
    contract = CONTRACTS.get(goal)
    if contract is None:
        return dict(instance_id=instance['id'], gold_plan_id=goal,
                    status='NOT_CHECKED', differences=['outside first-batch scope'],
                    unspecified_goal_fields=[], verification_status='NOT_VERIFIED', approved=False)
    label, product, method, connector = contract
    if f'| {goal} | {label} |' not in plan_text:
        raise ValueError(f'{goal}: draft plan changed; review audit contract')
    devices = {d['id']: d for d in instance['devices']}
    source = devices[instance['source_device_id']]
    request = instance['request']
    differences = []
    if product and source.get('product_ref') != product:
        differences.append('source product differs from plan')
    if method and request['output_method'] != method:
        differences.append('output method differs from plan')
    if connector:
        display_ports = [p for p in instance['ports'] if p['device_id'] in request['display_device_ids']]
        edges = instance['edges']
        incoming = {e['to_port'] for e in edges}
        if not display_ports or any(p['connector'] != connector for p in display_ports if p['id'] in incoming):
            differences.append('selected display input differs from plan')
    if goal in ('GP-02', 'GP-03'):
        # Goal definition approval does not approve the path or its capabilities.
        if not request['targets'] or any((t['width'], t['height'], t['refresh_hz']) != (3840, 2160, 60) for t in request['targets']):
            differences.append('UHD 3840x2160 at 60Hz differs from the approved goal definition')
    if goal == 'GP-06' and request['independent_external_count'] != 2:
        differences.append('two independent external displays required by plan')
    if goal == 'GP-07':
        if any(d['kind'] in ('DOCK', 'HUB', 'ADAPTER') for d in devices.values()):
            differences.append('direct path contains an intermediate dock/hub/adapter')
    if goal == 'GP-25':
        if request['context'].get('os_family') != 'macOS':
            differences.append('macOS goal differs')
        route_refs = [b['claim_ref'] for b in instance['bindings']]
        if not any(claims.get(ref, {}).get('payload', {}).get('mechanism') == 'MST' for ref in route_refs):
            differences.append('MST route binding missing')
    return dict(instance_id=instance['id'], gold_plan_id=goal,
                status='VARIANT' if differences else 'PARTIAL_MATCH',
                differences=differences, unspecified_goal_fields=list(UNSPECIFIED_GOALS[goal]),
                verification_status='NOT_VERIFIED', approved=False)


def audit_all(data):
    errors = validate(data)
    if errors:
        raise ValueError('; '.join(errors))
    return [audit_goal(r) for r in data['instances']]


if __name__ == '__main__':
    print(json.dumps(dict(results=audit_all(load_instances()), approved_gold_count=0,
                         notice='partial goal match; unspecified goals stay missing; NOT_VERIFIED; no human approval'),
                     ensure_ascii=False, indent=2))
