"""Compare only complete, explicitly supported summary templates.

No broad numeric extraction, language model, source inference, or 4K conversion.
Unrecognised text and unknown typed values always require manual review.
"""
import argparse
import json
import re
from pathlib import Path


def inspect_fact(fact):
    text, prop, p = fact.get('summary', ''), fact.get('property'), fact.get('payload', {})
    expected = {}
    if prop == 'VIDEO_PROFILE':
        patterns = [
            (r'패널 기본 해상도 (\d+)×(\d+) (\d+(?:\.\d+)?)Hz', 'PANEL', None),
            (r'패널 (\d+)×(\d+), (\d+(?:\.\d+)?)Hz', 'PANEL', None),
            (r'27형 IPS (\d+)×(\d+), (\d+(?:\.\d+)?)Hz 공식 표기', 'PANEL', None),
            (r'(DisplayPort|HDMI)에서 (\d+)×(\d+) (\d+(?:\.\d+)?)Hz', 'PORT', 'reported'),
            (r'(HDMI|DISPLAYPORT|USB_C) 입력 최대 (\d+)×(\d+) (\d+(?:\.\d+)?)Hz 표기', 'PORT', 'maximum'),
        ]
        for pattern, scope, interface in patterns:
            m = re.fullmatch(pattern, text)
            if m:
                values = list(m.groups())
                expected = {'scope': scope}
                if interface:
                    expected['interface'] = values.pop(0).upper()
                if interface == 'maximum':
                    expected['rating_basis'] = 'UP_TO'
                expected.update(width=int(values[0]), height=int(values[1]), refresh_hz=float(values[2]))
                break
    elif prop == 'POWER_TRANSFER':
        patterns = [
            (r'영상용 USB-C upstream에서 최대 (\d+(?:\.\d+)?)W 공급', 'USB_C_VIDEO_UPSTREAM', 'UP_TO'),
            (r'USB-C downstream은 최대 (\d+(?:\.\d+)?)W 충전', 'USB_C_DOWNSTREAM', 'UP_TO'),
            (r'USB-C PD 표기 (\d+(?:\.\d+)?)W', 'USB_C', None),
            (r'USB-C 충전 공급 (\d+(?:\.\d+)?)W 표기; 실제 수전W 미확인', 'USB_C', None),
            (r'USB-C (\d+(?:\.\d+)?)W Power Delivery 공급 표기', 'USB_C', None),
        ]
        for pattern, interface, basis in patterns:
            m = re.fullmatch(pattern, text)
            if m:
                expected = {'watts': float(m[1]), 'interface': interface}
                if '공급' in text or 'downstream' in text:
                    expected['mode'] = 'OFFER'
                if basis:
                    expected['rating_basis'] = basis
                break
    elif prop == 'PROTOCOL':
        m = re.fullmatch(r'영상용 USB-C upstream은 DP (\d+\.\d+) Alt Mode', text)
        if m:
            expected = {'interface': 'USB_C_VIDEO_UPSTREAM', 'protocol': 'DISPLAYPORT', 'version': m[1], 'mode': 'ALT_MODE', 'support': 'SUPPORTED'}
        elif text in ('USB-C DP Alternate Mode 지원', 'USB-C DP Alternate 영상 입력 표기'):
            expected = {'interface': 'USB_C', 'protocol': 'DISPLAYPORT', 'mode': 'ALT_MODE', 'support': 'SUPPORTED'}
        elif text == 'USB-C 영상 연결 기능 표기':
            expected = {'interface': 'USB_C', 'support': 'SUPPORTED'}
    elif prop == 'PORTS':
        tokens = {'HDMI 2.0': 'HDMI_2.0', 'DP 1.2': 'DISPLAYPORT_1.2', 'USB-C': 'USB_C', 'USB-B': 'USB_B', 'USB-A 2.0': 'USB_A_2.0'}
        m = re.fullmatch(r'(.+) 제공', text)
        if m and all(t in tokens for t in m[1].split('·')):
            expected = {'interfaces': [tokens[t] for t in m[1].split('·')]}
    elif prop == 'VESA':
        m = re.fullmatch(r'(\d+)×(\d+)mm VESA 홀 표기', text)
        if m:
            expected = {'width_mm': int(m[1]), 'height_mm': int(m[2])}
    elif prop == 'TILT':
        m = re.fullmatch(r'스탠드 틸트 (-?\d+)°~(-?\d+)° 표기', text)
        if m:
            expected = {'min_degrees': int(m[1]), 'max_degrees': int(m[2])}
    else:
        literals = {'KVM': 'KVM 스위치 기능 표기', 'SPEAKERS': '내장 스피커 표기', 'HEIGHT_ADJUSTMENT': '스탠드 높이 조절 기능 표기', 'PIP_PBP': 'PIP·PBP 기능 표기', 'REMOTE_CONTROL': '리모컨으로 OSD·입력·볼륨 조절'}
        if prop in literals and text == literals[prop]:
            expected = {'support': 'SUPPORTED'}
    errors, unresolved = [], []
    for key, value in expected.items():
        actual = p.get(key, 'UNKNOWN')
        if actual == 'UNKNOWN':
            unresolved.append(key)
        elif (set(actual) != set(value) if key == 'interfaces' else actual != value):
            errors.append({'field': key, 'summary_value': value, 'typed_value': actual})
    return {'fact_id': fact.get('fact_id'), 'status': 'CONFLICT' if errors else 'MANUAL_REVIEW' if not expected or unresolved else 'CONSISTENT_EXPLICIT_FIELDS',
            'checked_fields': list(expected), 'unresolved_fields': unresolved, 'unexamined_fields': sorted(set(p)-set(expected)), 'conflicts': errors,
            'scope_note': 'Template fields only; source truth and other language semantics need human review.'}


def validate_semantics(fact, path):
    result = inspect_fact(fact)
    if result['conflicts']:
        raise ValueError(f'{path}: summary/typed contradiction: {result["conflicts"]}')
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=Path, default=Path(__file__).resolve().parents[1]/'data/site/content-v2.json')
    args = parser.parse_args()
    data = json.loads(args.input.read_text(encoding='utf-8'))
    results = [dict(inspect_fact(f), monitor_id=m['id']) for m in data['monitors'] for f in m['features']]
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return int(any(r['status'] == 'CONFLICT' for r in results))


if __name__ == '__main__':
    raise SystemExit(main())
