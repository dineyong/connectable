"""Display-only labels. Preserve unknown keys, values, units and ordering."""
VALUE_KEYS = {'version': '버전',
 'count': '개수',
 'mode': '모드',
 'note': '조건 메모',
 'unit': '단위',
 'type_a': 'USB-A',
 'type_c': 'USB-C',
 'horizontal': '가로',
 'vertical': '세로',
 'axes': '축 순서',
 'with_stand': '스탠드 포함',
 'without_stand': '스탠드 제외',
 'estimate_status': '추정 표기',
 'tilt_deg': '틸트 (도)',
 'swivel_deg': '스위블 (도)',
 'pivot_deg': '피벗 (도)',
 'height_mm': '높이 조절 (mm)',
 'input_count': '입력 개수',
 'output_count': '출력 개수',
 'upstream': '업스트림',
 'downstream': '다운스트림',
 'upstream_count': '업스트림 개수',
 'downstream_count': '다운스트림 개수',
 'upstream_video_data': '영상·데이터 업스트림',
 'data_only_upstream': '데이터 전용 업스트림',
 'downstream_pd_w': '다운스트림 PD (W)',
 'pd_w': 'PD (W)',
 'width': '가로',
 'height': '세로',
 'depth': '깊이',
 'refresh_hz': '주사율 (Hz)',
 'min': '최소',
 'max': '최대',
 'modes': '모드 목록',
 'chroma': '크로마',
 'consoles': '콘솔',
 'dsc': 'DSC',
 'mst': 'MST',
 'hdr': 'HDR',
 'vrr': '가변 주사율',
 'pivot': '피벗',
 'swivel': '스위블',
 'tilt': '틸트',
 'height_adjustment': '높이 조절',
 'height_adjustment_inch': '높이 조절 (인치)',
 'gross': '총중량',
 'net': '순중량',
 'metric': '측정 기준',
 'condition': '조건',
 'direction': '방향',
 'data': '데이터',
 'video_mode': '영상 모드',
 'signalling': '신호 방식',
 'speed_gbps': '데이터 속도 (Gb/s)',
 'standard': '표준',
 'earc_count': 'eARC 개수',
 'bc12': 'BC 1.2',
 'frl': 'FRL',
 'type_b': 'USB-B',
 'type_a_downstream': 'USB-A 다운스트림',
 'type_b_upstream': 'USB-B 업스트림',
 'type_c_downstream': 'USB-C 다운스트림',
 'upstream_type_b': 'USB-B 업스트림',
 'upstream_usb20': '업스트림 USB 2.0',
 'upstream_usb30': '업스트림 USB 3.0',
 'upstream_usb31': '업스트림 USB 3.1',
 'upstream_usb32': '업스트림 USB 3.2',
 'downstream_usb20': '다운스트림 USB 2.0',
 'downstream_usb30': '다운스트림 USB 3.0',
 'downstream_usb31': '다운스트림 USB 3.1',
 'downstream_usb32': '다운스트림 USB 3.2'}

def formatted(value):
    if value is None: return '미확인'
    if isinstance(value, bool): return '지원' if value else '미지원'
    if isinstance(value, dict):
        if not value: return '{}'
        lines=[]
        for key, item in value.items():
            text = formatted(item)
            if key == 'estimate_status' and item == 'MANUFACTURER_ESTIMATE':
                text = '제조사 추정 (MANUFACTURER_ESTIMATE)'
            if key == 'axes' and item == 'W,H,D': text = '가로·높이·깊이 (W,H,D)'
            lines.append(f'{VALUE_KEYS.get(key,key)}: {text}')
        return '\n'.join(lines)
    if isinstance(value, list): return '[' + ', '.join(formatted(v) for v in value) + ']'
    return str(value)


def fact_text(value, unit):
    suffix = ('\n단위: ' if isinstance(value, (dict, list)) else ' ') + unit if unit else ''
    return formatted(value) + suffix
