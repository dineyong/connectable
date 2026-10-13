"""Validate manually checked outbound review links and build bounded UI data."""
import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.validate_monitor_expansion import load, official, community

SOURCE = ROOT / 'data/research/monitor-review-links.json'
OUTPUT = ROOT / 'data/site/monitor-review-links.json'
JS_OUTPUT = ROOT / 'web/monitor-review-links-data.js'
BINDINGS = ROOT / 'data/research/monitor-review-link-bindings.json'
PUBLIC_FIELDS = ('id', 'product_id', 'url', 'site', 'title', 'summary', 'checked_on',
                 'commercial_context', 'source_review_id', 'model_scope', 'review_type')
SITES = {'RTINGS': 'www.rtings.com', 'Quasarzone': 'quasarzone.com',
         'YouTube': 'www.youtube.com', 'NaverBlog': 'blog.naver.com'}
# Bounded model bindings checked against each public review, not URL substring guesses.
REVIEWED_PATHS = {
    'monitor:gigabyte-m32u': '/monitor/reviews/gigabyte/m32u',
    'monitor:asus-xg27aqdmg': '/monitor/reviews/asus/rog-strix-oled-xg27aqdmg',
    'monitor:asus-pg32ucdm': '/monitor/reviews/asus/rog-swift-oled-pg32ucdm',
    'monitor:aoc-q27g3xmn': '/monitor/reviews/aoc/q27g3xmn',
    'monitor:lg-27gr83q-b': '/monitor/reviews/lg/27gr83q-b',
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def normalized_url(value):
    require(isinstance(value, str) and value and not re.search(r'[\s\\%\x00-\x1f\x7f]', value), 'unsafe URL encoding or characters')
    parsed = urlsplit(value)
    require(parsed.scheme == 'https' and parsed.hostname and not parsed.username and not parsed.password,
            'URL must be HTTPS without credentials')
    require(parsed.port is None and not parsed.fragment, 'URL port/fragment not allowed')
    require(not parsed.query or (parsed.hostname == 'www.youtube.com' and parsed.path == '/watch' and
            re.fullmatch(r'v=[A-Za-z0-9_-]{11}', parsed.query)), 'URL query not allowed')
    require(not any(part in ('.', '..') for part in parsed.path.split('/')), 'URL path traversal')
    require(parsed.netloc == parsed.hostname, 'noncanonical host')
    return urlunsplit(('https', parsed.hostname.lower(), parsed.path.rstrip('/'), parsed.query, ''))


def reviewed_bindings(data):
    require(type(data) is dict and type(data.get('schema_version')) is int and data.get('schema_version') == 1 and type(data.get('items')) is list,
            'invalid reviewed binding registry')
    result = {}
    for item in data['items']:
        require(type(item) is dict, 'binding object required')
        require(all(isinstance(item.get(key), str) and item[key].strip() for key in
                    ('product_id', 'site', 'url', 'checked_model', 'evidence_location', 'checked_on')),
                'binding evidence missing')
        require(item.get('evidence_origin') == 'DIRECT_CHECK', 'binding direct check required')
        require(re.fullmatch(r'\d{4}-\d{2}-\d{2}', item['checked_on']) is not None, 'binding date format')
        dt.date.fromisoformat(item['checked_on'])
        url = normalized_url(item['url'])
        require(url not in result, 'duplicate binding URL')
        result[url] = item
    return result


def validate(data, products=None, reviews=None, bindings=None):
    if products is None:
        products = official(load(ROOT / 'data/research/monitor-expansion/official_specs.json'))['products']
    if reviews is None:
        reviews = community(load(ROOT / 'data/research/monitor-expansion/community_reviews.json'))['reviews']
    bindings = reviewed_bindings(load(BINDINGS) if bindings is None else bindings)
    products = {p['id']: p for p in products}
    reviews = {r['id']: r for r in reviews}
    require(type(data) is dict, 'dataset must be object')
    require(type(data.get('schema_version')) is int and data.get('schema_version') == 1 and type(data.get('items')) is list, 'invalid dataset structure')
    ids, urls = set(), set()
    for index, item in enumerate(data['items'], 1):
        prefix = f'item {index}: '
        require(type(item) is dict, prefix + 'object required')
        require(all(field in item for field in PUBLIC_FIELDS), prefix + 'missing field')
        require(all(isinstance(item[field], str) and item[field].strip() for field in ('id', 'product_id', 'title', 'summary', 'site')), prefix + 'empty required text')
        require(item['id'] not in ids, prefix + 'duplicate ID')
        ids.add(item['id'])
        require(item['product_id'] in products, prefix + 'unknown product')
        product = products[item['product_id']]
        require(item['model_scope'] == 'EXACT_DOCUMENT_MODEL', prefix + 'uncertain model scope')
        require(item.get('evidence_origin') == 'DIRECT_CHECK', prefix + 'direct check required')
        require(item.get('checked_model') == product['display_model'], prefix + 'model identity mismatch')
        require(isinstance(item.get('evidence_location'), str) and item['evidence_location'].strip(), prefix + 'missing evidence location')
        require(item['commercial_context'] in ('PRESENT', 'UNKNOWN', 'NOT_OBSERVED'), prefix + 'commercial enum')
        require(item['review_type'] in ('FIRST_HAND_REVIEW', 'PROFESSIONAL_REVIEW'), prefix + 'review enum')
        require(isinstance(item['checked_on'], str), prefix + 'date must be text')
        require(re.fullmatch(r'\d{4}-\d{2}-\d{2}', item['checked_on'] or '') is not None, prefix + 'date format')
        dt.date.fromisoformat(item['checked_on'])
        require(len(item['title']) <= 90 and len(item['summary']) <= 220, prefix + 'copy too long')
        require(not re.search(r'<[^>]+>|\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b|01[016789][- ]?\d{3,4}[- ]?\d{4}', item['title'] + ' ' + item['summary'], re.I), prefix + 'HTML or personal contact data')
        url = normalized_url(item['url'])
        parsed = urlsplit(url)
        require((item['site'] in SITES and parsed.hostname == SITES[item['site']]) or
                (item['site'] == 'Tistory' and re.fullmatch(r'[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.tistory\.com', parsed.hostname)) or (item['site'] in ('Blog', 'Forum') and url in bindings), prefix + 'site host mismatch')
        require((item['site'] == 'RTINGS' and re.fullmatch(r'/monitor/reviews/[a-z0-9-]+/[a-z0-9-]+', parsed.path)) or
                (item['site'] == 'Quasarzone' and re.fullmatch(r'/bbs/qf_dp/views/\d+', parsed.path)) or
                (item['site'] == 'YouTube' and parsed.path == '/watch' and re.fullmatch(r'v=[A-Za-z0-9_-]{11}', parsed.query)) or
                (item['site'] == 'NaverBlog' and re.fullmatch(r'/[A-Za-z0-9_-]+/\d+', parsed.path)) or
                (item['site'] == 'Tistory' and re.fullmatch(r'/\d+', parsed.path)) or (item['site'] in ('Blog', 'Forum') and url in bindings), prefix + 'non-review path')
        require(url not in urls, prefix + 'duplicate normalized URL')
        urls.add(url)
        if item['site'] == 'RTINGS':
            require(REVIEWED_PATHS.get(item['product_id']) == parsed.path, prefix + 'unreviewed model URL binding')
        if item['site'] in ('YouTube', 'NaverBlog', 'Tistory', 'Blog', 'Forum'):
            proof = bindings.get(url)
            require(proof is not None and proof['product_id'] == item['product_id'] and
                    proof['site'] == item['site'] and proof['checked_model'] == item['checked_model'],
                    prefix + 'unreviewed model URL binding')
        ref = item['source_review_id']
        require(ref is None or isinstance(ref, str), prefix + 'source reference must be text or null')
        require(item['site'] != 'Quasarzone' or ref is not None, prefix + 'community source reference required')
        if ref is not None:
            require(ref in reviews, prefix + 'unknown source review')
            review = reviews[ref]
            require(normalized_url(review['url']) == url, prefix + 'source URL mismatch')
            require(review['display_model'] == product['display_model'] and review['manufacturer'] == product['manufacturer'], prefix + 'source model mismatch')
            require(review['record_type'] == 'FIRST_HAND_REVIEW', prefix + 'source is not first-hand review')
    return data


def build():
    data = validate(load(SOURCE))
    return {'schema_version': 1, 'items': [{key: item[key] for key in PUBLIC_FIELDS} for item in data['items']],
            'reviewed_bindings': [{key: item[key] for key in ('product_id', 'site', 'url')}
                                  for item in data['items']]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = build()
    payload = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
    js = 'window.CONNECTABLE_REVIEW_LINKS = ' + json.dumps(data, ensure_ascii=False).replace('<', '\\u003c') + ';\n'
    for path, expected in ((OUTPUT, payload), (JS_OUTPUT, js)):
        if args.check:
            require(path.exists() and path.read_text(encoding='utf-8') == expected, f'stale output: {path}')
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(expected, encoding='utf-8')
    print(f'Monitor review links: {len(data["items"])} validated' + ('; outputs match' if args.check else '; generated'))


if __name__ == '__main__':
    main()
