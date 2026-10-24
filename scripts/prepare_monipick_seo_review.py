"""Evidence-bound SEO review only. Never changes approval, accounts or production."""
import argparse
from collections import Counter
from html import escape
import json
from pathlib import Path
import re
from http.server import ThreadingHTTPServer

from scripts import prepare_monipick_content_candidate as content
from scripts.serve_monipick_candidate import handler_for

EDITORIAL=content.ROOT/'data/editorial/monitor-summary-expansion.json'
PURPOSE='SEO_PRODUCT_REVIEW_NOT_AUTHORIZED'


def expanded_summaries():
    data=json.loads(EDITORIAL.read_text())
    products=content.official(content.load(content.FACTS))['products']
    expected={p['id']:p for p in products}
    ids=[item['product_id'] for item in data['products']]
    if Counter(ids)!=Counter(expected.keys()):
        raise ValueError('editorial must cover each current model exactly once')
    for item in data['products']:
        product=expected[item['product_id']]
        if product['manufacturer'] not in item['description'] and item['product_id'] not in {
                'monitor:asus-pa279crv','monitor:dell-u2724de','monitor:msi-modern-md271ul'}:
            raise ValueError('new model descriptions must identify the manufacturer')
        for claim in item['claims']:
            context=claim.get('expected_context')
            if not isinstance(context,dict) or set(context)!=set(claim['expected_facts']):
                raise ValueError('every claim needs explicit source/scope context')
            for prop,wanted in context.items():
                facts=[f for f in product['facts'] if f['property']==prop]
                if len(facts)!=1 or wanted!={k:facts[0][k] for k in ('scope','location','source_refs')}:
                    raise ValueError('scope or source changed; editorial review required')
    return content.reviewed_summaries(EDITORIAL)


def review_artifacts():
    plan,artifacts=content.polished_artifacts()
    previous=content.reviewed_summaries()
    summaries=expanded_summaries()
    for page in plan['pages']:
        name=page['source']
        if not name.startswith('monitors/') or name.count('/')!=2:continue
        pid='monitor:'+name.split('/')[1]
        item,section=summaries[pid]
        text=artifacts[name].decode('utf-8')
        if pid in previous:
            old=previous[pid][1]
            if text.count(old)!=1:raise ValueError('released summary marker changed')
            text=text.replace(old,section)
        else:
            marker='<section aria-labelledby="specs">'
            if text.count(marker)!=1:raise ValueError('specification marker changed')
            text=text.replace(marker,section+marker)
            description=escape(item['description'],quote=True)
            text=re.sub(r'(<meta name="description" content=")[^"]*(")',lambda m:m[1]+description+m[2],text)
            text=re.sub(r'(<meta (?:property="og:description"|name="twitter:description") content=")[^"]*(")',lambda m:m[1]+description+m[2],text)
        # Visible navigation only: no invented schema, review, rating or offer.
        title=re.search(r'<h1>(.*?)</h1>',text).group(1)
        breadcrumb=('<nav class="seo-breadcrumb" aria-label="현재 위치"><a href="/">홈</a><span aria-hidden="true"> › </span>'
                    '<a href="/monitors/">전체 모니터</a><span aria-hidden="true"> › </span><span aria-current="page">'+title+'</span></nav>')
        text=text.replace('<main id="main">','<main id="main">'+breadcrumb)
        text=text.replace('<footer>','<footer><p><a href="/guides/monitor-buying#comparison">사양 비교표 읽는 법</a> · '
                          '<a href="/information#corrections">자료 기준·정정 요청</a></p>')
        artifacts[name]=text.encode('utf-8')
    artifacts['monitor-detail-v3.css']+=b'\n.seo-breadcrumb{display:flex;flex-wrap:wrap;gap:6px;font-size:14px;margin-bottom:18px}.seo-breadcrumb a:focus-visible{outline:2px solid #175c4b;outline-offset:3px}\n'
    version=content.digest(artifacts['monitor-detail-v3.css'])[:12]
    for name,value in list(artifacts.items()):
        if name.endswith('.html'):
            artifacts[name]=re.sub(rb'(monitor-detail-v3\.css\?v=)[a-f0-9]{12}',lambda m:m[1]+version.encode(),value)
    # Ownership file is already public, copied without changing its approval record.
    from scripts.build_monipick_cloudflare import read_search_verification, search_verification_artifacts
    artifacts.update(search_verification_artifacts(read_search_verification()))
    return plan,artifacts


def validate_review(output):
    try:
        output=Path(output);_,expected=review_artifacts()
        manifest_path=output/'manifest.json'
        if manifest_path.is_symlink():return ['manifest symlink']
        manifest=json.loads(manifest_path.read_text())
        paths=list((output/'site').rglob('*'))
        if any(p.is_symlink() for p in paths):return ['symlink not permitted']
        actual={str(p.relative_to(output/'site')) for p in paths if p.is_file()}
        if actual!=set(expected):return ['review inventory mismatch']
        if (manifest.get('purpose')!=PURPOSE or manifest.get('blockers')!=['USER_CONTENT_REVIEW_PENDING'] or
                any(manifest.get(k) is not False for k in ('publication_authorized','deployment_authorized','indexing_authorized','analytics_enabled','advertising_enabled'))):
            return ['review authorization holds changed']
        if manifest.get('files')!={n:content.digest(v) for n,v in expected.items()}:return ['review hash mismatch']
        return ['altered file: '+n for n,v in expected.items() if (output/'site'/n).read_bytes()!=v]
    except (OSError,ValueError,KeyError,TypeError) as e:return [str(e)]


def build_review(output):
    _,artifacts=review_artifacts()
    manifest=content.build_content_candidate(output)
    for name,value in artifacts.items():(Path(output)/'site'/name).write_bytes(value)
    manifest.update(purpose=PURPOSE,blockers=['USER_CONTENT_REVIEW_PENDING'],
                    files={n:content.digest(v) for n,v in artifacts.items()})
    (Path(output)/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    errors=validate_review(output)
    if errors:raise ValueError('; '.join(errors))
    return manifest


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True)
    parser.add_argument('--serve',action='store_true')
    parser.add_argument('--port',type=int,default=8884)
    args=parser.parse_args();build_review(args.output)
    print('PASS: 30-model SEO review; publication/deployment remain false',flush=True)
    if args.serve:
        server=ThreadingHTTPServer(('127.0.0.1',args.port),handler_for(Path(args.output),validate_review))
        print(f'REVIEW ONLY: http://127.0.0.1:{server.server_port}/',flush=True)
        server.serve_forever()


if __name__=='__main__':main()
