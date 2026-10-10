"""Deterministic local-only product documents; no public approval or canonical."""
import argparse
import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.validate_monitor_expansion import official, load

SOURCE = ROOT / 'data/research/monitor-expansion/official_specs.json'
OUTPUT = ROOT / 'web/monitors'
LABELS = {'size':'화면 크기','width':'가로 해상도','height':'세로 해상도','panel':'패널',
          'refresh':'최대 주사율','brightness_typical':'일반 밝기','brightness_hdr_peak':'HDR 최대 밝기',
          'contrast_native':'기본 명암비','response':'응답시간 표기','color_gamut':'색 영역','hdr':'HDR',
          'hdmi':'HDMI','displayport':'DisplayPort','usb_c':'USB-C','pd_supply':'PD 공급 전력',
          'power_consumption':'소비전력','stand':'스탠드 조절','vesa':'VESA','weight':'무게',
          'dimensions':'크기','warranty':'보증','kvm':'KVM','usb_hub':'USB 허브','vrr':'가변 주사율'}
QUALIFIERS = {'RATED':'정격','UP_TO':'최대 한도','MANUFACTURER_STATED':'제조사 표기','UNKNOWN':'미확인'}

def esc(value):
    return html.escape(str(value), quote=True)

def formatted(value):
    if value is None: return '미확인'
    if isinstance(value, bool): return '지원' if value else '미지원'
    if isinstance(value, (dict, list)): return json.dumps(value, ensure_ascii=False, indent=2)
    return str(value)

def render(product):
    title = product['manufacturer'] + ' ' + product['display_model']
    sources = {s['id']:s for s in product['source_refs']}
    rows=[]
    for f in product['facts']:
        links=' · '.join(f'<a href="{esc(sources[r]["url"])}" rel="noreferrer">공식 문서 · {esc(sources[r]["checked_on"])}</a>' for r in f['source_refs'])
        value=formatted(f['value']) + (' '+f['unit'] if f['unit'] else '')
        rows.append(f'<tr><th scope="row">{esc(LABELS.get(f["property"],f["property"]))}</th><td><pre>{esc(value)}</pre><span class="qualifier">{esc(QUALIFIERS[f["qualifier"]])}</span></td><td>{esc(f["scope"])}<br>{esc(f["location"])}<br>{links}</td></tr>')
    missing=''.join(f'<li>{esc(LABELS.get(v,v))}</li>' for v in product['missing_fields'])
    notes=''.join(f'<li>{esc(v)}</li>' for v in product['notes'])
    return f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>{esc(title)} 사양·출처 | Connectable</title>
<meta name="description" content="{esc(title)}의 수집된 공식 사양, 입력 조건과 미확인 항목을 함께 확인하세요. 로컬 검토용 문서입니다.">
<link rel="stylesheet" href="../../monitor-detail-v3.css"></head>
<body><a class="skip" href="#main">본문으로 이동</a><header><a class="brand" href="../../monitor-v3.html">Connectable<span>모니터 선택의 기준</span></a><nav aria-label="주요 메뉴"><a href="../../monitor-v3.html">모니터 찾기</a><a href="../../tech-news.html">테크 소식</a></nav></header>
<main id="main"><a class="back" href="../../monitor-v3.html">← 모니터 목록</a><p class="eyebrow">MONITOR DETAILS</p><h1>{esc(title)}</h1>
<p class="intro">사양은 자세하게, 확인되지 않은 정보는 분명하게.</p>
<aside><strong>로컬 검토용 · 공개 승인 전</strong><p>문서 지역: {esc(product['region'])}. 한국 판매 SKU 동일성은 미확인입니다. 아래 제조사 표기는 사람 검토 완료나 기기 호환성 보장이 아닙니다. 미확인은 미지원과 다릅니다.</p></aside>
<section aria-labelledby="specs"><h2 id="specs">공식 문서에서 수집한 사양</h2><p>최대값은 입력·모드에 따라 달라질 수 있습니다. PD 공급 전력과 모니터 소비전력은 서로 다른 항목입니다.</p><div class="table-wrap" tabindex="0" role="region" aria-label="공식 사양 표, 좁은 화면에서는 가로 이동"><table><caption>{esc(title)} 사양과 항목별 근거</caption><thead><tr><th scope="col">항목</th><th scope="col">값·표현 종류</th><th scope="col">조건·문서 위치·출처</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div></section>
<section><h2>아직 확인이 필요한 항목</h2><ul>{missing or '<li>원본에 별도 결측 목록 없음. 전체 검증 완료를 뜻하지 않습니다.</li>'}</ul><details><summary>조사 범위와 원본 메모</summary><ul>{notes}</ul></details></section>
<footer>Connectable · 원본 사양과 사용자 경험을 구분합니다. 가격·판매량·구매 인증을 제공하는 페이지가 아닙니다.</footer></main></body></html>'''

def build(source=SOURCE, output=OUTPUT, check=False):
    data=official(load(source))
    expected={p['id'].removeprefix('monitor:')+'/index.html':render(p)+'\n' for p in data['products']}
    if check:
        stale=[key for key,value in expected.items() if not (output/key).is_file() or (output/key).read_text()!=value]
        extra=set(str(p.relative_to(output)) for p in output.glob('*/index.html'))-set(expected)
        if stale or extra: raise ValueError(f'Product documents stale/missing={stale}, unexpected={sorted(extra)}')
    else:
        for key,value in expected.items():
            path=output/key;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(value)
    return len(expected)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true')
    args=parser.parse_args();print(f'PASS: {build(check=args.check)} local product documents')
