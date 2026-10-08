"""Read-only derivation of existing public research; no network or approval."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.site_content_validation import checked_date, https_url, payload, refs, validate_content
from scripts.data_trust import linked_model_identity, require_official_source
from scripts.site_input_validation import validate_inputs
from scripts.validate_question_corpus_v2 import unique_object, reject_constant

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'data/site/content-v2.json'
BATCH_PATH = 'data/site/monitor-batch-1-sources.json'
INPUTS = ('data/official/connection_model_pilot.json', 'data/official/products.json',
          'data/research/review/public_usage_batch_2026-10-08.jsonl',
          'data/research/review/public_usage_mapped_2026-10-08.jsonl',
          'data/research/user_questions_v2.jsonl', BATCH_PATH)

def read(path):
    text = (ROOT / path).read_text(encoding='utf-8')
    options = {'object_pairs_hook': unique_object, 'parse_constant': reject_constant}
    return [json.loads(line, **options) for line in text.splitlines() if line.strip()] if path.endswith('.jsonl') else json.loads(text, **options)

def reference(source, path, record_id):
    return {'url': source.get('source_url', source.get('url')), 'title': source.get('site_name', source.get('title', '공개 원문')),
            'checked_on': source.get('checked_at', source.get('accessed_at', 'UNKNOWN')),
            'published_on': source.get('published_at', 'UNKNOWN'), 'source_file': path, 'record_id': record_id}

def build():
    pilot, official, raw, mapped, corpus = [read(p) for p in INPUTS[:5]]
    batch = read(BATCH_PATH)
    validate_inputs(pilot, official, raw, mapped, corpus, ROOT, INPUTS)
    sources = {s['source_id']: s for s in pilot['sources']}
    monitors = []
    for product in pilot['products']:
        if product['kind'] != 'DISPLAY':
            continue
        monitors.append({'id': product['product_id'], 'title': product['manufacturer']+' '+product['model'],
                         'display_model': product['model'], 'manufacturer': product['manufacturer'],
                         'region': product['region'], 'identity_status': product['identity_status'],
                         'review_status': product['review_status'], 'public_status': 'UNKNOWN',
                         'source_refs': [reference(sources[s], INPUTS[0], s) for s in product['source_refs']],
                         'features': [dict(f, basis='MANUFACTURER_SPEC') for f in pilot['facts'] if f['product_id'] == product['product_id']],
                         'missing_fields': product['missing_fields'], 'price': 'UNKNOWN', 'rating': 'UNKNOWN',
                         'image': 'UNKNOWN', 'purchase_url': 'UNKNOWN'})
    reviews = []
    for item in mapped:
        case = item['mapping']
        if case['source']['public_access'] != 'YES':
            continue
        reviews.append(review(item['id'], case, INPUTS[3], item))
    for case in corpus:
        if case['source']['public_access'] == 'YES':
            reviews.append(review(case['id'], case, INPUTS[4]))
    # Only exact, literal model equality is linked. Similar family labels stay unlinked.
    for r in reviews:
        r['monitor_ids'] = [m['id'] for m in monitors if m['display_model'] in r['reported_monitor_models']]
    append_monitor_batch(monitors, reviews, batch)
    guides = []
    topics = [
        ('guide-usb-c', 'USB-C 한 선 연결 구매 전 확인', ['영상용 USB-C 입력과 충전 공급 포트를 구분하세요.', '공식 공급 W는 실제 맥북 수전 W와 다릅니다. 케이블 모델과 길이, OS, 덮개 상태를 기록하세요.']),
        ('guide-mode', '해상도와 주사율을 읽는 방법', ['패널 사양과 입력별 최대 타이밍을 따로 확인하세요.', '보기 배율, 선택 가능한 Hz, 실제 신호 모드는 서로 다릅니다. 후기에서 미측정 값은 UNKNOWN으로 남깁니다.']),
        ('guide-review', '연결 후기를 비교하는 방법', ['같은 모니터라도 직접 연결과 허브 경유는 다른 구성입니다.', '타인의 조언이나 교체 계획은 작성자의 성공 관측이 아닙니다. 복제 화면 수와 독립 확장 화면 수도 구분하세요.'])]
    for ident, title, body in topics:
        guides.append({'id': ident, 'title': title, 'body': body, 'review_status': 'NEEDS_REVIEW',
                       'source_refs': [ref for m in monitors for ref in m['source_refs']] + [ref for r in reviews if r['id'] in ('PUR-001', 'PUR-008', 'PUR-013') for ref in r['source_refs']],
                       'related_monitor_ids': [m['id'] for m in monitors], 'related_review_ids': ['PUR-001', 'PUR-008', 'PUR-013'],
                       'basis': 'EDITORIAL_CHECKLIST', 'public_status': 'UNKNOWN'})
    return validate_content({'schema_version': '2', 'generated_on': batch['checked_on'], 'monitors': monitors, 'reviews': reviews, 'guides': guides,
            'disclosures': {'editorial': '기존 공개 연구 자료의 편집 요약입니다. 원문과 검토 상태를 함께 확인하세요.',
                            'compatibility': '사용자 관측과 제조사 사양은 별도 근거입니다. 모든 공개 호환 판정은 UNKNOWN이며 사람 승인을 뜻하지 않습니다.',
                            'advertising': '광고 자리 준비 단계이며 실제 광고 코드와 구매·제휴 링크는 없습니다.',
                            'affiliate': '향후 제휴 링크를 운영할 경우 광고 관계를 표시합니다. 현재 제휴 계정 승인 여부는 UNKNOWN입니다.'},
            'provenance': [{'path': p, 'sha256': hashlib.sha256((ROOT/p).read_bytes()).hexdigest()} for p in INPUTS]})

def validate_monitor_batch(batch, reviews):
    """Reject unsupported identity joins and references before writing the asset."""
    sources = {s['source_id']: s for s in batch['sources']}
    products = {p['product_id']: p for p in batch['products']}
    cases = {r['id']: r for r in reviews}
    checked_date(batch['checked_on'], 'batch.checked_on')
    if len(sources) != len(batch['sources']) or len(products) != len(batch['products']):
        raise ValueError('duplicate source/product ID')
    fact_ids = [f['fact_id'] for f in batch['facts']]
    if len(fact_ids) != len(set(fact_ids)):
        raise ValueError('duplicate fact ID')
    for source in sources.values():
        https_url(source['url'], source['source_id']+'.url')
        checked_date(source['checked_at'], source['source_id']+'.checked_at')
        checked_date(source['published_at'], source['source_id']+'.published_at', unknown=True)
        if (source['source_status'] != 'DIRECT_CHECK' or source['access'] != 'BODY_DIRECT_CHECK'
                or not source['url'].startswith('https://') or not source['checked_at']):
            raise ValueError('source lacks direct public check')
    for product in products.values():
        refs(product.get('source_refs'), product['product_id']+'.source_refs', sources)
        if product['review_status'] != 'PENDING_HUMAN_REVIEW':
            raise ValueError('product approval must remain pending')
        for ref in product['source_refs']:
            if ref not in sources or not sources[ref]['source_type'].startswith('MANUFACTURER_'):
                raise ValueError('product lacks manufacturer evidence')
            require_official_source(sources[ref], product['manufacturer'], ref)
    for fact in batch['facts']:
        refs(fact.get('source_refs'), fact['fact_id']+'.source_refs', sources)
        payload(fact, fact['fact_id']+'.payload')
        if (fact.get('source_status') != 'DIRECT_CHECK'
                or not isinstance(fact.get('location'), str) or not fact['location'].strip()
                or not isinstance(fact.get('summary'), str) or not fact['summary'].strip()):
            raise ValueError('fact needs checked location and summary')
        if fact['product_id'] not in products or fact['review_status'] != 'PENDING_HUMAN_REVIEW':
            raise ValueError('invalid fact product or approval')
        for ref in fact['source_refs']:
            if ref not in sources or not sources[ref]['source_type'].startswith('MANUFACTURER_'):
                raise ValueError('user report is not manufacturer specification')
            if (ref not in products[fact['product_id']]['source_refs']
                    or sources[ref]['model_scope'] not in (products[fact['product_id']]['model'], 'Modern '+products[fact['product_id']]['model'])):
                raise ValueError('fact evidence belongs to a different product/model')
    seen = set()
    for link in batch['review_links']:
        refs(link.get('source_refs'), 'review_link.source_refs', sources)
        checked_date(link['checked_on'], 'review_link.checked_on')
        pair = (link['review_id'], link['monitor_id'])
        if pair in seen or pair[0] not in cases or pair[1] not in products:
            raise ValueError('invalid or duplicate review link')
        seen.add(pair)
        case = cases[pair[0]]
        node = next((n for n in case['nodes'] if n['id'] == link['node_id']), None)
        if not node or linked_model_identity(products[pair[1]]['manufacturer'], products[pair[1]]['model'],
                                             node.get('display_model'), link.get('reported_model')) != 'EXACT_MODEL_LABEL':
            raise ValueError('MANUAL_REVIEW: review/node/target model identity unconfirmed')
        if (not node or node['kind'] != 'DISPLAY' or node.get('display_model') != link['reported_model']
                or link['match_basis'] != 'DIRECT_CHECK_EXACT_MODEL_LABEL'
                or link['match_scope'] != 'MODEL_ONLY' or link['variant_match'] != 'UNKNOWN'
                or link['review_status'] != 'NEEDS_REVIEW'):
            raise ValueError('unsupported model/variant identity link')
        for ref in link['source_refs']:
            if (ref not in sources or sources[ref]['source_type'] != 'PUBLIC_USER_REPORT'
                    or sources[ref]['url'] != case['source_refs'][0]['url']
                    or sources[ref]['model_scope'] != products[pair[1]]['model']):
                raise ValueError('review link evidence must be the same public source')
    return sources


def append_monitor_batch(monitors, reviews, batch):
    sources = validate_monitor_batch(batch, reviews)
    if {p['product_id'] for p in batch['products']} & {m['id'] for m in monitors}:
        raise ValueError('batch cannot replace existing monitor')
    for product in batch['products']:
        facts = [dict(f, basis='MANUFACTURER_SPEC') for f in batch['facts'] if f['product_id'] == product['product_id']]
        capabilities = {}
        for name, prop in [('usb_c_video','PROTOCOL'), ('pd_supply','POWER_TRANSFER'), ('kvm','KVM'),
                           ('speakers','SPEAKERS'), ('height_adjustment','HEIGHT_ADJUSTMENT')]:
            matching = [f for f in facts if f['property'] == prop and
                        (name != 'usb_c_video' or f['payload'].get('interface') == 'USB_C')]
            capabilities[name] = {'status': 'CONFIRMED_MANUFACTURER_STATEMENT' if matching else 'UNKNOWN',
                                  'feature_refs': [f['fact_id'] for f in matching],
                                  'notes': '제조사 기능 표기; Mac 구성 관측·사람 승인과 별개' if matching else '공식 자료에서 확인하지 못함; 미지원 의미 아님'}
        monitors.append({'id': product['product_id'], 'title': product['manufacturer']+' '+product['model'],
                         'display_model': product['model'], 'manufacturer': product['manufacturer'],
                         'region': product['region'], 'identity_status': product['identity_status'],
                         'variant': product['variant'], 'review_status': product['review_status'], 'public_status': 'UNKNOWN',
                         'source_refs': [reference(sources[ref], BATCH_PATH, ref) for ref in product['source_refs']],
                         'features': facts, 'capabilities': capabilities, 'missing_fields': product['missing_fields'],
                         'price': 'UNKNOWN', 'rating': 'UNKNOWN', 'image': 'UNKNOWN', 'purchase_url': 'UNKNOWN'})
    for link in batch['review_links']:
        case = next(r for r in reviews if r['id'] == link['review_id'])
        if link['monitor_id'] not in case['monitor_ids']:
            case['monitor_ids'].append(link['monitor_id'])
        case.setdefault('monitor_links', []).append(link)
        for ref in link['source_refs']:
            case['source_refs'].append(reference(sources[ref], BATCH_PATH, ref))

def review(ident, case, path, envelope=None):
    envelope = envelope or {}
    nodes = case['nodes']
    return {'id': ident, 'title': ident+' · '+next((n.get('display_model', 'UNKNOWN') for n in nodes if n['kind']=='SOURCE'), 'UNKNOWN')+' 연결 기록',
            'source_refs': [reference(case['source'], path, ident)], 'review_status': case['review']['status'],
            'record_status': envelope.get('record_status', 'CORPUS_RESEARCH'), 'public_status': 'UNKNOWN',
            'reliability_grade': case['review']['reliability_grade'], 'usable_for_compatibility': 'NO', 'basis': 'USER_REPORT',
            'macbook_display_name': next((n.get('display_model','UNKNOWN') for n in nodes if n['kind']=='SOURCE'), 'UNKNOWN'),
            'reported_monitor_models': [n['display_model'] for n in nodes if n['kind']=='DISPLAY' and n.get('display_model')],
            'monitor_ids': [], 'connection_summary': [e['summary'] for e in case['evidence'] if e['id'] in {ref for c in case['configurations'] for ref in c.get('evidence_refs', [])}],
            'configurations': case['configurations'], 'observations': case['observations'],
            'functional_observations': envelope.get('functional_observations', []),
            'evidence': case['evidence'], 'nodes': nodes, 'ports': case['ports'],
            'attempts': case['attempts'], 'unscoped_statements': envelope.get('unscoped_statements', []),
            'missing_fields': case['review']['missing_fields'], 'commercial_context': case['review']['commercial_context'],
            'semantic_review': envelope.get('semantic_review', {'status':'UNVERIFIED'}),
            'reported_outcome': case['outcome'], 'configuration_conclusions': case.get('configuration_conclusions', []),
            'source_line_sha256': envelope.get('source_line_sha256', 'UNKNOWN'), 'image': 'UNKNOWN'}

def serialize(data):
    return json.dumps(data, ensure_ascii=False, indent=2)+'\n'

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--check', action='store_true'); args=parser.parse_args()
    result=serialize(build())
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding='utf-8') != result:
            raise SystemExit('content-v2.json is stale')
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True); OUTPUT.write_text(result, encoding='utf-8')
    print('site content v2: reproducible; source files read-only')

if __name__ == '__main__': main()
