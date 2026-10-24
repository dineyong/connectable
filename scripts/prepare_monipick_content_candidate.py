"""Build an unapproved content/link review candidate, preserving production approval.

No deployment, account changes, advertising or analytics activation.
"""
import argparse
import json
import re
from html import escape, unescape
from pathlib import Path
from urllib.parse import urljoin, urlsplit, urlunsplit

from scripts.build_monipick_public_candidate import build_candidate, expected_artifacts, digest
from scripts.prepare_monipick_release import ORIGIN
from scripts.validate_monitor_expansion import official, load

ROOT=Path(__file__).resolve().parents[1]
EDITORIAL=ROOT/'data/editorial/monitor-summary-pilot.json'
FACTS=ROOT/'data/research/monitor-expansion/official_specs.json'
PURPOSE='CONTENT_POLISH_CANDIDATE_NOT_AUTHORIZED'


def final_link(value, source, routes):
    """Only known same-origin documents; retain queries and fragment-only links."""
    if not value or value.startswith(('#','?')):
        return value
    target=urlsplit(urljoin(ORIGIN+'/'+source,value))
    if (target.scheme,target.netloc)!=('https','monipick.com') or target.path not in routes:
        return value
    return urlunsplit(('', '', routes[target.path],target.query,target.fragment))


def normalize_links(text, source, routes):
    def replace(match):
        value=unescape(match[3])
        final=final_link(value,source,routes)
        if value==final: return match[0]
        return match[1]+match[2]+escape(final,quote=True)+match[2]
    return re.sub(r'(\bhref\s*=\s*)([\"\x27])(.*?)(\2)',replace,text,flags=re.I)


def reviewed_summaries():
    data=json.loads(EDITORIAL.read_text())
    if data.get('status')!='EDITORIAL_CANDIDATE':
        raise ValueError('editorial candidate status required')
    products={p['id']:p for p in official(load(FACTS))['products']}
    result={}
    for item in data['products']:
        pid=item['product_id']
        if pid in result or pid not in products: raise ValueError('duplicate or unknown editorial model')
        product=products[pid]
        if not set(item['required_missing_fields']).issubset(product['missing_fields']):
            raise ValueError('editorial uncertainty changed; review caution')
        source_map={s['id']:s for s in product['source_refs']}
        facts={}
        for fact in product['facts']: facts.setdefault(fact['property'],[]).append(fact)
        rendered=[]
        for claim in item['claims']:
            if not claim['summary'].strip() or not claim['expected_facts']:
                raise ValueError('summary needs explicit fact bindings')
            refs=set()
            for prop,value in claim['expected_facts'].items():
                matches=facts.get(prop,[])
                if len(matches)!=1 or any(matches[0][key]!=expected for key,expected in value.items()) or set(value)!={'value','unit','qualifier'}:
                    raise ValueError('editorial fact changed or ambiguous: '+pid+'/'+prop)
                fact=matches[0]
                if fact['qualifier']=='UNKNOWN' or not fact['source_refs']:
                    raise ValueError('summary cannot promote unknown or unsourced facts')
                refs.update(fact['source_refs'])
            links=' · '.join('<a href="'+escape(source_map[r]['url'],quote=True)+'" target="_blank" rel="noopener noreferrer">공식 근거 · '+escape(source_map[r]['checked_on'])+'</a>' for r in sorted(refs))
            rendered.append('<li><p>'+escape(claim['summary'])+'</p><p>'+links+'</p></li>')
        section=('<section class="model-highlights" aria-labelledby="model-highlights"><h2 id="model-highlights">이 모델에서 먼저 볼 점</h2><ul>'
                 +''.join(rendered)+'</ul><p><strong>구매 전 확인:</strong> '+escape(item['caution'])+'</p>'
                 '<p>문서 지역: '+escape(product['region'])+'. 기존 공식 자료의 요약이며 실측·후기·호환성 승인이 아닙니다.</p>'
                 '<p><a href="/guides/monitor-buying#usb-c">USB-C·포트 선택 가이드</a> · <a href="/monitors/">전체 모니터 사양 보기</a></p></section>')
        result[pid]=(item,section)
    return result


def polished_artifacts():
    plan,artifacts=expected_artifacts()
    # The protected web source and existing production builder remain unchanged.
    routes={'/'+p['source']:p['route'] for p in plan['pages']}
    routes['/index.html']='/'
    summaries=reviewed_summaries()
    for name,content in list(artifacts.items()):
        if not name.endswith('.html'): continue
        text=content.decode('utf-8')
        text=normalize_links(text,name,routes)
        pid='monitor:'+name.split('/')[1] if name.startswith('monitors/') and name.count('/')==2 else None
        if pid in summaries:
            item,section=summaries[pid]
            # One metadata description and its social counterpart, same factual summary.
            text=re.sub(r'(<meta name="description" content=")[^"]*(")',lambda m:m[1]+escape(item['description'],quote=True)+m[2],text)
            text=re.sub(r'(<meta (?:property="og:description"|name="twitter:description") content=")[^"]*(")',lambda m:m[1]+escape(item['description'],quote=True)+m[2],text)
            marker='<section aria-labelledby="specs">'
            if text.count(marker)!=1: raise ValueError('one specifications section required')
            text=text.replace(marker,section+marker)
            text=text.replace('<aside>', '<aside aria-label="사양 적용 범위">').replace('<aside class="source-conflict">', '<aside class="source-conflict" aria-label="공식 자료 표기 차이">')
        artifacts[name]=text.encode('utf-8')
    artifacts['monitor-detail-v3.css']+=b'\n.model-highlights{padding:24px;border:1px solid #dce5de;border-radius:18px;background:#fff}.model-highlights h2{margin-top:0}.model-highlights ul{padding-left:22px}.model-highlights li{padding-left:6px;margin-bottom:18px}.model-highlights li p{margin:6px 0}.model-highlights li a{font-size:12px}.model-highlights>p{font-size:14px}@media(max-width:600px){.model-highlights{padding:18px}.model-highlights h2{font-size:20px}}\n'
    # Single known dynamic local-document link in the reviewed application script.
    artifacts['monitor-v3.js']=artifacts['monitor-v3.js'].replace(b'href="monitor10-review.html#',b'href="/monitor10-review#')
    return plan,artifacts


def validate_content_candidate(output):
    output=Path(output)
    try:
        _,expected=polished_artifacts()
        manifest=json.loads((output/'manifest.json').read_text())
        if (output/'manifest.json').is_symlink(): return ['manifest symlink not allowed']
        files=list((output/'site').rglob('*'))
        if any(p.is_symlink() for p in files): return ['symlink not allowed']
        actual={str(p.relative_to(output/'site')) for p in files if p.is_file()}
        if actual!=set(expected): return ['content candidate inventory mismatch']
        if (manifest.get('purpose')!=PURPOSE or manifest.get('blockers')!=['CONTENT_AND_DESIGN_REVIEW_PENDING'] or
                any(manifest.get(k) is not False for k in ('publication_authorized','deployment_authorized','indexing_authorized','analytics_enabled','advertising_enabled'))):
            return ['content candidate must retain approval holds']
        if manifest.get('files')!={n:digest(v) for n,v in expected.items()}: return ['manifest mismatch']
        return ['altered file: '+n for n,v in expected.items() if (output/'site'/n).read_bytes()!=v]
    except (OSError,ValueError,KeyError,TypeError) as e: return [str(e)]


def build_content_candidate(output):
    _,artifacts=polished_artifacts() # reject changed editorial facts before creating files
    manifest=build_candidate(output)
    for name,content in artifacts.items(): (Path(output)/'site'/name).write_bytes(content)
    manifest.update(purpose=PURPOSE,blockers=['CONTENT_AND_DESIGN_REVIEW_PENDING'],
                    files={n:digest(v) for n,v in artifacts.items()},advertising_enabled=False)
    (Path(output)/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    errors=validate_content_candidate(output)
    if errors: raise ValueError('; '.join(errors))
    return manifest


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    build_content_candidate(args.output)
    print('PASS: local content candidate; public release unchanged')
