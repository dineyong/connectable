"""Build a separate, noindex Monitor10 review page without merging product data."""
import argparse
import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
SOURCE = ROOT / 'data/research/monitor-expansion/monitor10_verified_supplement.json'
OUTPUT = ROOT / 'web/monitor10-review.html'

LABELS = {
    'screen_size_inch': '화면 크기 (인치)', 'screen_size_cm': '화면 크기 (cm)',
    'resolution': '해상도', 'panel': '패널', 'max_refresh_hz': '최대 주사율 (Hz)',
    'video_ports': '영상 포트', 'usb_c_video': 'USB-C 영상 입력',
    'usb_c_pd_power_w': 'USB-C 전력 공급 (W)', 'brightness': '밝기와 조건',
    'hdr': 'HDR', 'stand_and_mount': '스탠드·장착', 'brightness_advertised': '밝기 표기',
    'stand_adjustments': '스탠드 조절', 'vesa_mm': 'VESA (mm)', 'usb_pd_support': 'USB PD 지원',
    'hdmi_supported_modes': 'HDMI 지원 모드', 'displayport_supported_modes': 'DisplayPort 지원 모드',
    'usb_c_power_profiles': 'USB-C 전력 프로파일', 'usb_c_external_power_advice': 'USB-C 별도 전원 안내',
    'exact_korean_sku': '한국 판매 페이지 식별자', 'displayport_ports': 'DisplayPort 입력·출력',
    'usb_c_power_delivery': 'USB-C 충전 방향·전력', 'hdr_peak_brightness_nits': 'HDR 피크 밝기 (nits)',
    'distinct_related_model': '구분해야 하는 관련 모델', 'input_profiles': '입력별 주사율 조건',
    'connectivity': '연결 포트', 'brightness_cd_m2': '밝기 (cd/m²)',
    'support_product_link': '공식 지원 모델 연결', 'usb_c_pd_page_max_w': '페이지의 USB-C 최대 전력 (W)',
    'brightness_typical_cd_m2': '일반 밝기 (cd/m²)',
    'APL_percent':'APL 조건 (%)', 'HDR_peak':'HDR 피크',
    'USB_3_0':'USB 3.0', 'USB_Type_C':'USB Type-C', 'amps':'전류 (A)',
    'console':'콘솔 조건', 'count':'개수', 'dell_part':'Dell 부품', 'direction':'방향',
    'displayport':'DisplayPort', 'displayport_count':'DisplayPort 개수',
    'displayport_version':'DisplayPort 버전', 'downstream':'다운스트림',
    'downstream_charging_w':'다운스트림 충전 (W)', 'dsc':'DSC', 'frl':'FRL',
    'from':'연결 원본', 'hdmi':'HDMI', 'hdmi_count':'HDMI 개수', 'hdmi_version':'HDMI 버전',
    'hdr_peak_nits':'HDR 피크 (nits)', 'height':'세로', 'height_mm':'높이 조절 (mm)',
    'input_count':'입력 개수', 'input_version':'입력 버전', 'manufacturer_part':'제조사 부품',
    'max_hz':'최대 (Hz)', 'merge_allowed':'동일 모델 병합 허용', 'minimum':'최소',
    'mode':'모드', 'model':'모델', 'name':'공식 이름', 'normal':'일반',
    'normal_hz':'일반 (Hz)', 'offering_id':'판매 항목 ID', 'output_count':'출력 개수',
    'overclock':'오버클록', 'overclock_hz':'오버클록 (Hz)', 'pc':'PC 조건',
    'qualifier':'표현 종류', 'refresh_hz':'주사율 (Hz)', 'relationship':'관계',
    'sdr_typical_nits':'SDR 일반 (nits)', 'signalling':'신호 방식',
    'swivel_deg':'좌우 회전 (도)', 'tilt_deg':'기울기 (도)', 'to':'연결 대상',
    'typical':'일반', 'typical_mode_unspecified_nits':'일반 밝기·화면 모드 미지정 (nits)',
    'unit':'단위', 'upstream':'업스트림', 'upstream_host_power_delivery':'업스트림 호스트 전력 공급',
    'usb_3_0_downstream':'USB 3.0 다운스트림', 'usb_3_0_upstream':'USB 3.0 업스트림',
    'usb_c':'USB-C', 'value':'표기값', 'version':'버전', 'volts':'전압 (V)',
    'vrr':'가변 주사율', 'watts':'전력 (W)', 'width':'가로',
    'stand_height_mm':'높이 조절 (mm)', 'usb_c_data_kvm':'USB-C 데이터·KVM',
    'field':'항목', 'status':'검토 상태', 'notes':'검토 메모', 'url':'원문',
    'related_url':'관련 원문', 'location':'문서 위치', 'reason':'보류 이유',
    'claims':'문서별 표기', 'review_resolution':'검토 결론', 'stand_swivel_deg':'좌우 회전 (도)',
    'source_claims':'문서별 표기', 'rj45':'RJ45', 'hdmi_vertical_frequency_scope':'HDMI 수직 주파수 적용 범위',
}
VALUES = {'CONFLICT':'충돌 검토', 'UNKNOWN':'미확인', 'UP_TO':'최대', 'RATED':'정격', 'DIRECT_CHECK':'원문 재확인',
          'CONFLICT_PENDING':'충돌 검토 보류', 'SCOPE_REVIEW':'적용 범위 검토',
          'MANUFACTURER_STATED':'제조사 표기', 'TYPICAL':'일반',
          'MINIMUM':'최소', 'PENDING_HUMAN_REVIEW':'사람 검토 대기',
          'USER_SUPPLIED_CONFLICT_PENDING_RECHECK':'전달 자료상 충돌 · 원문 재확인 대기',
          'USER_SUPPLIED_AMBIGUITY_PENDING_RECHECK':'전달 자료상 모호함 · 원문 재확인 대기',
          'OFFICIAL_SUPPORT_TO_PRODUCT_LINK':'공식 지원 페이지에서 제품 페이지로 연결',
          'SUPPORTED_MANUFACTURER_STATEMENT':'제조사가 지원을 명시함'}


def esc(value):
    return html.escape(str(value), quote=True)


def label(key):
    return LABELS.get(key, key)


def render_value(value, field=None):
    """Readable nested values; no raw JSON, inferred units, URLs or markup execution."""
    if field == 'field' and isinstance(value, str):
        return esc(label(value))
    if field in {'resolution', 'vesa_mm'}:
        pair = value
        if isinstance(value, dict) and set(value) == {'width', 'height'}:
            pair = [value['width'], value['height']]
        if isinstance(pair, list) and len(pair) == 2 and all(type(v) in (int, float) for v in pair):
            return f'<span>{esc(pair[0])} × {esc(pair[1])}</span>'
    if isinstance(value, dict):
        return '<dl class="value-list">' + ''.join(
            f'<div><dt>{esc(label(k))}</dt><dd>{render_value(v, k)}</dd></div>'
            for k, v in value.items()) + '</dl>'
    if isinstance(value, list):
        return '<ul class="value-items">' + ''.join(f'<li>{render_value(v)}</li>' for v in value) + '</ul>'
    if value is True:
        return '<span>지원 / 허용</span>'
    if value is False:
        return '<span>미지원 / 허용하지 않음</span>'
    if value is None or value == 'UNKNOWN':
        return '<span class="m10-unknown">미확인</span>'
    return esc(VALUES.get(value, value) if isinstance(value, str) else value)


def render_record(record):
    rows = []
    for fact in record['confirmed']:
        rows.append(f'''<tr><th scope="row">{esc(label(fact['field']))}</th>
<td class="fact-value">{render_value(fact['value'], fact['field'])}</td>
<td><p>{esc(fact['notes']) if fact['notes'] else '별도 추가 조건 기록 없음'}</p>
<details class="scope-detail"><summary>적용 범위·문서 위치</summary><p>범위 식별자: <code>{esc(fact['scope'])}</code></p><p>문서 위치: {esc(fact['location'])}</p></details></td>
<td class="source-cell"><a href="{esc(fact['url'])}" target="_blank" rel="noopener noreferrer">공식 원문 ↗</a><span>재확인 {esc(record['checked_on'])}</span></td></tr>''')
    conflicts = ''.join('<li>' + render_value({('review_resolution' if k == 'resolution' else k): v for k, v in item.items()}) + '</li>' for item in record['conflicts'])
    unknowns = ''.join(f'<li>{render_value(item)}</li>' for item in record['unconfirmed'])
    return f'''<article class="m10-product" id="{esc(record['id'])}" aria-labelledby="title-{esc(record['id'])}">
<div class="m10-product-head"><div><p class="eyebrow">OFFICIAL SOURCE REVIEW</p><h2 id="title-{esc(record['id'])}">{esc(record['selection_model'])}</h2></div><span class="m10-badge">{len(record['confirmed'])}개 항목 재확인</span></div>
<div class="table-scroll" tabindex="0" aria-label="{esc(record['selection_model'])} 공식 사양 보강표 가로 스크롤"><table><caption>{esc(record['selection_model'])} — 확인한 표기값과 그 조건</caption><thead><tr><th scope="col">항목</th><th scope="col">확인한 내용</th><th scope="col">조건과 해석 범위</th><th scope="col">근거</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>
<div class="m10-review-grid"><section class="m10-caution"><h3>충돌·범위 검토</h3>{'<ul>'+conflicts+'</ul>' if conflicts else '<p>이번 재확인에서 별도 충돌 기록 없음. 전체 사양 승인이라는 뜻은 아닙니다.</p>'}</section>
<section class="m10-pending"><h3>아직 확인하지 못한 내용</h3>{'<ul>'+unknowns+'</ul>' if unknowns else '<p>별도 미확인 항목 기록 없음.</p>'}</section></div>
<details class="m10-existing"><summary>기존 자료와의 관계</summary><p>{esc(record['existing_match_notes'])}</p></details><a class="m10-back" href="#model-index">모델 목록으로 ↑</a></article>'''


def render(data):
    from scripts.validate_monitor10_supplement import validate
    errors = validate(data)
    if errors:
        raise ValueError('\n'.join(errors))
    records = data['records']
    count = sum(len(r['confirmed']) for r in records)
    index = ''.join(f'<a href="#{esc(r["id"])}"><span>{i:02d}</span>{esc(r["selection_model"])}</a>' for i, r in enumerate(records, 1))
    return f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><meta name="description" content="모니터 10종의 공식 사양 재확인 자료. 확인값과 미확인 항목, 조건 및 공식 출처를 구분합니다."><meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'none'; style-src 'self'; img-src 'self'; connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'"><title>모니터 10종, 공식 자료 더 살펴보기 — Connectable</title><link rel="stylesheet" href="monitor-v3.css"><link rel="stylesheet" href="monitor10-review.css"></head>
<body><a class="skip" href="#model-index">모델 목록으로 건너뛰기</a><header><div class="header-inner"><a class="brand" href="monitor-v3.html">Connectable.</a><nav aria-label="주 메뉴"><a href="monitor-v3.html">모니터 찾기</a><a href="#model-index" aria-current="page">공식 자료 보강</a><a href="tech-news.html">테크 소식</a></nav><span class="preview-label">LOCAL PREVIEW</span></div></header>
<main class="m10-main"><section class="m10-hero"><p class="eyebrow">A LITTLE MORE CERTAINTY</p><h1>같은 모델명도,<br>조건까지 확인합니다.</h1><p>모니터 10종의 공식 원문을 다시 살펴봤어요.<br>확인한 사양은 출처와 함께, 남은 질문은 그대로 남겼습니다.</p><div class="m10-metrics"><span><strong>{len(records)}</strong>개 모델</span><span><strong>{count}</strong>개 재확인 항목</span><span><strong>출처별</strong>적용 범위 유지</span></div></section>
<aside class="m10-notice" aria-label="자료의 검토 범위"><strong>기존 비교 자료를 보완하는 별도 조사 페이지입니다.</strong><p>한국 판매 SKU·리비전의 동일성이나 호환성 승인을 뜻하지 않습니다. 원본 30종에 자동 병합하지 않았으며, 사용자 후기·가격·판매 순위는 이 자료에 포함하지 않습니다.</p></aside>
<nav class="m10-index" id="model-index" aria-label="모델 바로가기"><h2>모델 바로가기</h2><div>{index}</div></nav>
{''.join(render_record(r) for r in records)}
<section class="m10-bottom"><h2>확인하지 못한 것은, 미확인으로.</h2><p>미확인은 미지원이 아닙니다. 문서가 다르게 말하면 하나를 골라 확정하지 않습니다. 수치가 같아도 입력 방향·화면 모드·지역이 다르면 별도로 읽어주세요.</p><a href="monitor-v3.html">← 모니터 탐색으로 돌아가기</a></section></main><footer><a class="brand" href="monitor-v3.html">Connectable.</a><p>더 명확한 비교, 더 나은 선택.</p><p>로컬 조사 자료 · 공개 승인 보류</p></footer></body></html>
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    try:
        from scripts.validate_monitor10_supplement import load
        result = render(load(SOURCE))
        if args.check:
            if not OUTPUT.exists() or OUTPUT.read_text(encoding='utf-8') != result:
                raise ValueError('monitor10-review.html is stale; run scripts/build_monitor10_review.py')
        else:
            OUTPUT.write_text(result, encoding='utf-8')
        print('monitor10 review page: PASS')
    except (ValueError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
