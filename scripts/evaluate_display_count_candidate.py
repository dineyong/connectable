"""Research-only count constraint: never a public/full-path compatibility verdict."""
from scripts.validate_official_products import load_catalog, validate_catalog


def evaluate(request, catalog=None):
    catalog = load_catalog() if catalog is None else catalog
    errors = validate_catalog(catalog)
    if errors:
        raise ValueError('invalid catalog: ' + '; '.join(errors))
    result = {'status': 'UNKNOWN', 'candidate_status': 'UNKNOWN',
              'review_status': 'PENDING_HUMAN_REVIEW', 'rule_id': 'NATIVE-COUNT-001',
              'claim_refs': [], 'reason': '모델·출력 방식·동시 조건 또는 전체 경로 근거 부족'}
    count = request.get('external_independent_count')
    if type(count) is not int or count < 1:
        raise ValueError('external_independent_count must be a positive integer')
    products = {p['product_id']: p for p in catalog['products']}
    p = products.get(request.get('product_id'))
    if not p or request.get('output_method') != 'NATIVE' or type(request.get('builtin_active')) is not bool:
        return result
    if request.get('lid_state') == 'CLOSED' and request['builtin_active'] is True:
        return result
    profiles = []
    for c in p['claims']:
        if c['property'] == 'NATIVE_EXTERNAL_DISPLAY_PROFILE' and request['builtin_active'] is True:
            profiles.append(c)
        elif c['property'] == 'CONDITIONAL_NATIVE_DISPLAY_PROFILE':
            pre = c['prerequisites']
            # Only builtin ON profiles are currently evaluated. Closed-lid profiles
            # retain OS/power/input requirements but cannot produce a verdict yet.
            if pre['builtin_state'] == 'ON' and request['builtin_active'] is True:
                if pre['lid_state'] == 'NOT_SPECIFIED' and not set(pre).intersection({'minimum_macos'}):
                    if pre['power_required'] == pre['external_input_required'] == 'NOT_SPECIFIED':
                        profiles.append(c)
    if len(profiles) != 1:
        return result
    profile = profiles[0]
    result['claim_refs'] = [profile['claim_id']]
    if count > profile['external_count']:
        result.update(candidate_status='INCOMPATIBLE', reason='명시된 내장 화면 동시 사용 네이티브 외장 화면 수 제한 초과')
    else:
        result['reason'] = '화면 수 제한 이내이나 모니터·케이블·독·해상도·주사율·전원 검수 미완료'
    return result
