"""Isolated research intake. No public/catalog writes or automatic equivalence."""
import argparse
import collections
import hashlib
import json
import math
import re
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / 'data/research/monitor-expansion/quasarzone_intake.json'
DIRECT = {
 'https://quasarzone.com/bbs/qc_qsz/views/1107030': ('EDITORIAL_REVIEW', 'Model and stand adjustment dimensions checked; remaining claims not reverified.', 'article body / stand adjustment'),
 'https://quasarzone.com/bbs/qf_dp/views/515378': ('USER_PROBLEM_REPORT', '27ULD950 and HDMI/USB-C flicker self-report checked; duplicates existing review.', 'article body / model and connection symptoms'),
 'https://quasarzone.com/bbs/qb_saleinfo/views/1404263': ('COMMERCIAL_HISTORICAL_OFFER', '2023-09-11 offer, conditional 32GP850 price and affiliate notice checked; not current price.', 'article date / offer / affiliate notice'),
 'https://quasarzone.com/perf/monitor/detail/1352': ('SECONDARY_SPEC_AND_MEASUREMENT_TABLE', '140TU5 2023 detail destination checked; table separates response time and response speed, test conditions not checked.', 'model heading / specification and performance table'),
}
# Deliberate, review-only hypotheses; do not strip suffixes for identity.
HYPOTHESES = {
 '27GP850': ['27GP850-B'], '27GS95QE': ['27GS95QE-B'], '32GS95UE': ['32GS95UE-B'],
 'MPG 321URX': ['MPG 321URX QD-OLED'], 'M27Q 2.0': ['M27Q rev.1.0'],
 'MOBIUZ EX2710Q': ['EX2710Q'],
}

def pairs(items):
    out = {}
    for k, v in items:
        if k in out: raise ValueError('duplicate JSON key')
        out[k] = v
    return out

def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'), object_pairs_hook=pairs,
                      parse_constant=lambda _: (_ for _ in ()).throw(ValueError('nonfinite JSON')))

def sha(path):
    b = Path(path).read_bytes()
    return {'basename': Path(path).name, 'size_bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def urls(z):
    if isinstance(z, dict):
        for k, v in z.items():
            if k in ('url', 'source_url', 'specs_source_url') and isinstance(v, str): yield v
            else: yield from urls(v)
    elif isinstance(z, list):
        for v in z: yield from urls(v)

def access_class(s):
    if '검색' in s or 'snippet' in s: return 'SEARCH_INDEX_ONLY_CLAIM'
    if '본문' in s or s.startswith('opened_'): return 'BODY_ACCESS_CLAIM'
    return 'UNSPECIFIED'

def observations(z):
    if isinstance(z, dict):
        u = z.get('url') or z.get('source_url')
        if u:
            yield u, z.get('access_level', 'UNSPECIFIED'), z.get('evidence_type', 'UNSPECIFIED')
        for v in z.values(): yield from observations(v)
    elif isinstance(z, list):
        for v in z: yield from observations(v)

def build(source, companion):
    raw = load(source)
    official = load(ROOT / 'data/research/monitor-expansion/official_specs.json')
    reviews = load(ROOT / 'data/research/monitor-expansion/community_reviews.json')
    ms, rs, cs = raw['models'], raw['supplemental_owner_reviews'], raw['catalog_index']
    evidence = set(urls(ms)) | set(urls(rs))
    counters = collections.defaultdict(collections.Counter)
    for u, a, t in observations(ms + rs): counters[u][(a, t)] += 1
    source_urls = set(DIRECT) | evidence | {c['source_url'] for c in cs} | {c['detail_url'] for c in cs if c['detail_url']}
    registry = []
    for i, u in enumerate(sorted(source_urls), 1):
        rec = {'id': 'qzs:%03d' % i, 'url': u, 'provenance': 'USER_SUPPLIED_RESEARCH',
               'access_status': 'NOT_RECHECKED', 'supplied_claims': [
                   {'access_label': a, 'access_class': access_class(a), 'evidence_type_label': t, 'occurrences': n}
                   for (a, t), n in sorted(counters[u].items())],
               'existing_review_ids': [r['id'] for r in reviews['reviews'] if r['url'] == u]}
        if u in DIRECT:
            kind, summary, location = DIRECT[u]
            rec['direct_check'] = {'provenance': 'DIRECT_CHECK', 'checked_on': '2026-10-10',
                'method': 'web.run open/find of public extracted body; cache may be involved',
                'scope': location, 'source_kind': kind, 'result': summary}
            rec['access_status'] = 'DIRECT_CHECK'
        registry.append(rec)
    ids = {s['url']: s['id'] for s in registry}
    candidates = []
    for section, rows in [('DETAIL', ms), ('SUPPLEMENTAL_REVIEW', rs), ('CATALOG_INDEX', cs)]:
        for i, row in enumerate(rows):
            label = row['model']
            exact = [{'id': p['id'], 'display_model': p['display_model'], 'match': 'EXACT_LABEL_ONLY', 'uncertain': True}
                     for p in official['products'] if label == p['display_model']]
            hypotheses = [{'id': p['id'], 'display_model': p['display_model'], 'match': 'VARIANT_OR_MARKETING_LABEL_HYPOTHESIS', 'uncertain': True}
                          for p in official['products'] if p['display_model'] in HYPOTHESES.get(label, [])]
            refs = set(urls(row))
            if section == 'CATALOG_INDEX':
                refs |= {row['source_url']}
                if row['detail_url']: refs.add(row['detail_url'])
            existing = [r['id'] for r in reviews['reviews'] if r['url'] in refs]
            candidate = {'id': 'qzi:%s:%03d' % (section.lower(), i + 1), 'section': section,
                'source_position': i, 'display_label': label, 'brand_label': row.get('brand'),
                'provenance': 'USER_SUPPLIED_RESEARCH', 'source_refs': sorted(ids[u] for u in refs),
                'official_mapping_candidates': exact + hypotheses,
                'existing_review_exact_label_ids': [r['id'] for r in reviews['reviews'] if label == r['display_model']],
                'existing_review_url_ids': existing, 'identity_status': 'UNCERTAIN',
                'review_status': 'PENDING_HUMAN_REVIEW', 'public_status': 'UNKNOWN',
                'priority': 'P1' if exact or hypotheses or existing else ('P3' if section == 'CATALOG_INDEX' else 'P2')}
            if section == 'DETAIL':
                candidate['evidence_counts'] = {k: len(row.get(k, [])) for k in ('specs', 'measurements', 'prices', 'user_pros', 'user_cons', 'editorial_pros', 'editorial_cons')}
            if section == 'SUPPLEMENTAL_REVIEW':
                candidate['supplied_review_type'] = row['evidence_type']
                candidate['supplied_commercial_status'] = row['sponsorship_status']
            if section == 'CATALOG_INDEX':
                candidate['index_only'] = True
                candidate['supplied_link_position'] = row['source_link_index']
                candidate['detail_url_resolved_claim'] = row['detail_url'] is not None
            candidates.append(candidate)
    stats = {'detailed_models': len(ms), 'unique_detailed_labels': len({m['model'] for m in ms}),
        'supplemental_reviews': len(rs), 'supplemental_unique_posts': len({r['source_url'] for r in rs}),
        'supplemental_unique_labels': len({r['model'] for r in rs}), 'evidence_unique_urls_excluding_catalog': len(evidence),
        'catalog_entries': len(cs), 'catalog_unique_labels': len({c['model'] for c in cs}),
        'catalog_resolved_detail_urls': sum(c['detail_url'] is not None for c in cs),
        'catalog_missing_release_month': sum(c['listed_release_month'] is None for c in cs),
        'price_records': sum(len(m['prices']) for m in ms),
        'numeric_price_records': sum(isinstance(p.get('amount'), (int, float)) for m in ms for p in m['prices']),
        'models_with_numeric_prices': sum(any(isinstance(p.get('amount'), (int, float)) for p in m['prices']) for m in ms),
        'models_with_user_experience': sum(bool(m['user_pros'] or m['user_cons']) for m in ms),
        'measurement_records': sum(len(m.get('measurements', [])) for m in ms),
        'models_with_measurements': sum(bool(m.get('measurements')) for m in ms),
        'existing_official_products': len(official['products']), 'existing_reviews': len(reviews['reviews']),
        'direct_checked_urls': len(DIRECT)}
    return {'schema_version': 1, 'checked_on': '2026-10-10', 'public_status': 'UNKNOWN',
        'purpose': 'PRIORITIZED_RESEARCH_INDEX_ONLY', 'originals': [sha(source), sha(companion)],
        'baseline_files': [sha(ROOT / 'data/research/monitor-expansion/official_specs.json'), sha(ROOT / 'data/research/monitor-expansion/community_reviews.json')],
        'statistics': stats, 'sources': registry, 'candidates': candidates,
        'restrictions': ['NO_AUTO_APPROVAL', 'NO_CURRENT_PRICE', 'NO_ALIAS_EQUIVALENCE', 'NO_PUBLIC_IMPORT', 'NO_COMPATIBILITY_USE']}

def validate(data):
    def require(ok, msg):
        if not ok: raise ValueError(msg)
    require(data['schema_version'] == 1 and data['public_status'] == 'UNKNOWN', 'unsafe root status')
    require(data['purpose'] == 'PRIORITIZED_RESEARCH_INDEX_ONLY', 'wrong purpose')
    require(set(data['restrictions']) == {'NO_AUTO_APPROVAL','NO_CURRENT_PRICE','NO_ALIAS_EQUIVALENCE','NO_PUBLIC_IMPORT','NO_COMPATIBILITY_USE'}, 'missing restrictions')
    for original in data['originals'] + data['baseline_files']:
        require(Path(original['basename']).name == original['basename'] and '/' not in original['basename'], 'basename only')
        require(re.fullmatch('[a-f0-9]{64}', original['sha256']) is not None, 'bad hash')
        require(type(original['size_bytes']) is int and original['size_bytes'] > 0, 'bad size')
    sources = {s['id']: s for s in data['sources']}
    require(len(sources) == len(data['sources']), 'duplicate source ID')
    require(len({s['url'] for s in sources.values()}) == len(sources), 'duplicate source URL')
    for s in sources.values():
        u = urlsplit(s['url'])
        require(u.scheme == 'https' and u.netloc == 'quasarzone.com' and not u.fragment and not u.query and not re.search(r'[\s\\%]',s['url'].replace('%2C', ',')), 'unsafe source URL')
        require(s['provenance'] == 'USER_SUPPLIED_RESEARCH', 'promoted provenance')
        require(s['access_status'] in ('NOT_RECHECKED','DIRECT_CHECK'), 'bad access status')
        require((s['access_status'] == 'DIRECT_CHECK') == ('direct_check' in s), 'direct scope missing')
        if 'direct_check' in s:
            require(s['url'] in DIRECT and s['direct_check']['result'] == DIRECT[s['url']][1] and s['direct_check']['provenance'] == 'DIRECT_CHECK', 'unverified direct check')
    candidates = data['candidates']
    require(len({c['id'] for c in candidates}) == len(candidates), 'duplicate candidate ID')
    counts = collections.Counter(c['section'] for c in candidates)
    require(counts == {'DETAIL':75,'SUPPLEMENTAL_REVIEW':29,'CATALOG_INDEX':594}, 'section count mismatch')
    for c in candidates:
        require(c['provenance'] == 'USER_SUPPLIED_RESEARCH' and c['identity_status'] == 'UNCERTAIN' and c['public_status'] == 'UNKNOWN' and c['review_status'] == 'PENDING_HUMAN_REVIEW', 'unsafe candidate promotion')
        require(c['priority'] in ('P1','P2','P3'), 'bad priority')
        require(c['source_refs'] and all(r in sources for r in c['source_refs']), 'dangling source reference')
        require(all(m['uncertain'] is True and m['match'] in ('EXACT_LABEL_ONLY','VARIANT_OR_MARKETING_LABEL_HYPOTHESIS') for m in c['official_mapping_candidates']), 'automatic equivalence')
        if c['section'] == 'CATALOG_INDEX': require(c['index_only'] is True and not c['official_mapping_candidates'], 'catalog promotion')
    st = data['statistics']
    require(st['detailed_models']==counts['DETAIL'] and st['catalog_entries']==counts['CATALOG_INDEX'] and st['supplemental_reviews']==counts['SUPPLEMENTAL_REVIEW'], 'statistics mismatch')
    require(st['direct_checked_urls']==sum(s['access_status']=='DIRECT_CHECK' for s in sources.values()), 'direct count mismatch')
    detail = [c for c in candidates if c['section'] == 'DETAIL']
    supplemental = [c for c in candidates if c['section'] == 'SUPPLEMENTAL_REVIEW']
    catalog = [c for c in candidates if c['section'] == 'CATALOG_INDEX']
    derived = {
        'unique_detailed_labels': len({c['display_label'] for c in detail}),
        'supplemental_unique_labels': len({c['display_label'] for c in supplemental}),
        'supplemental_unique_posts': len({r for c in supplemental for r in c['source_refs']}),
        'catalog_unique_labels': len({c['display_label'] for c in catalog}),
        'catalog_resolved_detail_urls': sum(c['detail_url_resolved_claim'] for c in catalog),
        'price_records': sum(c['evidence_counts']['prices'] for c in detail),
        'measurement_records': sum(c['evidence_counts']['measurements'] for c in detail),
        'models_with_measurements': sum(bool(c['evidence_counts']['measurements']) for c in detail),
        'models_with_user_experience': sum(bool(c['evidence_counts']['user_pros'] or c['evidence_counts']['user_cons']) for c in detail),
    }
    require(all(st[k] == v for k, v in derived.items()), 'derived statistics mismatch')
    require({c['source_position'] for c in catalog} == set(range(594)), 'catalog positions incomplete')
    for baseline in data['baseline_files']:
        live = sha(ROOT / 'data/research/monitor-expansion' / baseline['basename'])
        require(live == baseline, 'baseline changed: regenerate and reassess mapping')

    def scan(z):
        if isinstance(z,dict):
            require(not (set(z)&{'author','email','phone','full_text','current_price','approved','price_paid','amount'}), 'forbidden copied or published field')
            for v in z.values():scan(v)
        elif isinstance(z,list):
            for v in z:scan(v)
        elif isinstance(z,float): require(math.isfinite(z),'nonfinite value')
    scan(data)
    return True

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source'); p.add_argument('--companion'); p.add_argument('--path', default=str(TARGET))
    a = p.parse_args()
    if a.source:
        if not a.companion: p.error('--companion required')
        data = build(a.source,a.companion); validate(data)
        Path(a.path).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    else: validate(load(a.path))
    print('PASS: isolated Quasarzone intake; no publication approval')
