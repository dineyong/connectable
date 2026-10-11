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
LABELS.update({'active_area':'유효 화면 영역','brightness_unspecified':'밝기 (유형 미명시)',
    'contrast_dynamic':'동적 명암비','curvature':'곡률','daisy_chain':'데이지 체인',
    'displayport_out':'DisplayPort 출력','dual_mode':'듀얼 모드','input_profile':'입력별 조건',
    'console_input_profile':'콘솔 입력 조건','input_vertical_frequency':'입력 수직 주파수',
    'local_dimming_zones':'로컬 디밍 구역','pbp':'PBP','pip':'PIP','thunderbolt':'Thunderbolt',
    'pd_supply_downstream':'다운스트림 PD 공급','pd_supply_upstream':'업스트림 PD 공급',
    'power_consumption_ac_input_max':'AC 입력 전력 최대값','power_consumption_max':'최대 소비전력',
    'power_consumption_normal':'일반 소비전력','power_consumption_operating':'동작 소비전력',
    'power_consumption_standby':'대기 소비전력','power_consumption_typical':'대표 소비전력',
    'korean_sku_identity':'한국 판매 SKU 동일성','per_input_simultaneous_conditions':'입력별·동시 사용 조건',
    'physical_test_results':'실물 연결 시험','warranty_korea':'한국 보증 조건',
    'displayport.version':'DisplayPort 버전','hdmi.count':'HDMI 수량','hdmi.version':'HDMI 버전',
    'usb_c.video_mode':'USB-C 영상 모드'})
from scripts.monitor_value_format import formatted, fact_text

def esc(value):
    return html.escape(str(value), quote=True)

def review_section(product_id, reviews):
    items = [item for item in reviews if item['product_id'] == product_id]
    commercial_labels = {'PRESENT':'광고·판매·제휴 요소 있음',
        'NOT_OBSERVED':'광고·제휴 요소 확인되지 않음','UNKNOWN':'광고·제휴 여부 미확인'}
    cards = ''.join(f'<li class="review-link-card"><p class="review-link-meta">{esc(item["site"])} · {"전문 리뷰" if item["review_type"] == "PROFESSIONAL_REVIEW" else "개인 사용기"} · 확인일 {esc(item["checked_on"])}</p><a href="{esc(item["url"])}" target="_blank" rel="noopener noreferrer">{esc(item["title"])} ↗<span class="sr-only"> (새 창 또는 새 탭)</span></a><p>{esc(item["summary"])}</p><p class="review-link-meta">{esc(commercial_labels[item["commercial_context"]])}</p></li>' for item in items)
    return '<section class="external-reviews" aria-labelledby="external-reviews"><h2 id="external-reviews">외부 후기 원문</h2><p class="review-links-note">외부 작성자의 경험입니다. 공식 사양·제품 평가 점수·호환성 승인이 아니며 한국 판매 SKU 동일성을 보장하지 않습니다. 원문은 새 창 또는 새 탭으로 열립니다.</p>' + (f'<ul class="review-link-list">{cards}</ul>' if items else '<p class="review-links-empty">아직 이 모델에 연결해 확인한 외부 후기 링크가 없습니다.</p>') + '</section>'

def render(product, reviews=()):
    title = product['manufacturer'] + ' ' + product['display_model']
    sources = {s['id']:s for s in product['source_refs']}
    rows=[]
    for f in product['facts']:
        links=' · '.join(f'<a href="{esc(sources[r]["url"])}" rel="noreferrer">공식 문서 · {esc(sources[r]["checked_on"])}</a>' for r in f['source_refs'])
        value=fact_text(f['value'], f['unit'])
        rows.append(f'<tr><th scope="row">{esc(LABELS.get(f["property"],f["property"]))}</th><td data-label="값·표현 종류"><pre>{esc(value)}</pre><span class="qualifier">{esc(QUALIFIERS[f["qualifier"]])}</span></td><td data-label="조건·문서 위치·출처">{esc(f["scope"])}<br>{esc(f["location"])}<br>{links}</td></tr>')
    missing=''.join(f'<li>{esc(LABELS.get(v,v))}</li>' for v in product['missing_fields'])
    notes=''.join(f'<li>{esc(v)}</li>' for v in product['notes'])
    conflicts = [v for v in product['notes'] if v.startswith('CONFLICT_REVIEW ')]
    notice = ('<aside class="source-conflict"><strong>공식 자료 간 표기 차이 · 확인 필요</strong><ul>'
              + ''.join(f'<li>{esc(v)}</li>' for v in (n.removeprefix('CONFLICT_REVIEW ') for n in conflicts))
              + '</ul><p>아래 값은 기록된 문서의 표기입니다. 충돌이 해소된 것으로 해석하지 마세요.</p></aside>') if conflicts else ''
    return f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>{esc(title)} 사양·출처 | Connectable</title>
<meta name="description" content="{esc(title)}의 수집된 공식 사양, 입력 조건과 미확인 항목을 함께 확인하세요. 로컬 검토용 문서입니다.">
<link rel="stylesheet" href="../../monitor-detail-v3.css"><link rel="stylesheet" href="../../monitor-review-links.css"></head>
<body><a class="skip" href="#main">본문으로 이동</a><header><a class="brand" href="../../monitor-v3.html">Connectable<span>모니터 선택의 기준</span></a><nav aria-label="주요 메뉴"><a href="../../monitor-v3.html">모니터 찾기</a><a href="../../tech-news.html">테크 소식</a></nav></header>
<main id="main"><a class="back" href="../../monitor-v3.html">← 모니터 목록</a><p class="eyebrow">MONITOR DETAILS</p><h1>{esc(title)}</h1>
<p class="intro">사양은 자세하게, 확인되지 않은 정보는 분명하게.</p>
<aside><strong>로컬 검토용 · 공개 승인 전</strong><p>문서 지역: {esc(product['region'])}. 한국 판매 SKU 동일성은 미확인입니다. 아래 제조사 표기는 사람 검토 완료나 기기 호환성 보장이 아닙니다. 미확인은 미지원과 다릅니다.</p></aside>
{notice}<section aria-labelledby="specs"><h2 id="specs">공식 문서에서 수집한 사양</h2><p>최대값은 입력·모드에 따라 달라질 수 있습니다. PD 공급 전력과 모니터 소비전력은 서로 다른 항목입니다.</p><div class="table-wrap" tabindex="0" role="region" aria-label="공식 사양과 항목별 근거"><table><caption>{esc(title)} 사양과 항목별 근거</caption><thead><tr><th scope="col">항목</th><th scope="col">값·표현 종류</th><th scope="col">조건·문서 위치·출처</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div></section>
<section><h2>아직 확인이 필요한 항목</h2><ul>{missing or '<li>원본에 별도 결측 목록 없음. 전체 검증 완료를 뜻하지 않습니다.</li>'}</ul><details><summary>조사 범위와 원본 메모</summary><ul>{notes}</ul></details></section>
{review_section(product["id"], reviews)}
<footer>Connectable · 원본 사양과 사용자 경험을 구분합니다. 가격·판매량·구매 인증을 제공하는 페이지가 아닙니다.</footer></main></body></html>'''

def render_index(products):
    groups = {}
    for p in sorted(products, key=lambda p: (p['manufacturer'], p['display_model'])):
        groups.setdefault(p['manufacturer'], []).append(p)
    sections = []
    for brand, items in groups.items():
        links = ''.join(f'<li><a href="{esc(p["id"].removeprefix("monitor:"))}/">{esc(p["display_model"])}</a><span>문서 지역 {esc(p["region"])}</span></li>' for p in items)
        sections.append(f'<section><h2>{esc(brand)}</h2><ul>{links}</ul></section>')
    return f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>전체 모니터 사양·출처 목록 | Connectable</title>
<meta name="description" content="조사한 모니터의 사양과 공식 출처를 브랜드별 정적 목록에서 확인하세요. JavaScript 없이 열 수 있는 로컬 검토용 문서입니다.">
<link rel="stylesheet" href="../monitor-detail-v3.css"><link rel="stylesheet" href="../monitor-index.css"></head>
<body><a class="skip" href="#main">본문으로 이동</a><header><a class="brand" href="../monitor-v3.html">connectable<span>모니터 선택의 기준</span></a><nav aria-label="주요 메뉴"><a href="../monitor-v3.html">검색·비교 화면</a><a href="../guides/monitor-buying.html">구매 가이드</a></nav></header>
<main id="main"><p class="eyebrow">ALL MONITORS</p><h1>전체 모니터 사양·출처</h1><p class="intro">브랜드별 {len(products)}개 제품 문서. JavaScript 없이 읽을 수 있어요.</p>
<aside><strong>로컬 검토용 · 한국 판매 SKU 동일성 미확인</strong><p>문서 지역과 구매할 모델을 대조하세요. 조사 내용은 사람 검토 완료나 호환성 보장이 아닙니다.</p></aside>
<div class="static-product-groups">{''.join(sections)}</div><footer>Connectable · 공식 자료의 사양과 조건을 함께 확인하세요.</footer></main></body></html>'''

def build(source=SOURCE, output=OUTPUT, check=False):
    data=official(load(source))
    from scripts.build_monitor_review_links import build as build_reviews
    reviews = build_reviews()['items']
    expected={p['id'].removeprefix('monitor:')+'/index.html':render(p, reviews)+'\n' for p in data['products']}
    expected['index.html'] = render_index(data['products']) + '\n'
    if check:
        stale=[key for key,value in expected.items() if not (output/key).is_file() or (output/key).read_text()!=value]
        extra=set(str(p.relative_to(output)) for p in output.glob('*/index.html'))-set(expected)
        if stale or extra: raise ValueError(f'Product documents stale/missing={stale}, unexpected={sorted(extra)}')
    else:
        for key,value in expected.items():
            path=output/key;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(value)
    return len(data['products'])

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true')
    args=parser.parse_args();print(f'PASS: {build(check=args.check)} local product documents')
