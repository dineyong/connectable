"""Local-only remaining-monitor editorial overlay. Does not authorize deployment."""
import argparse
import json
import re
from html import escape
from pathlib import Path
from scripts import prepare_monipick_content_candidate as content

EDITORIAL=content.ROOT/'data/editorial/monitor-summary-expansion.json'
PURPOSE='SUMMARY_EXPANSION_CANDIDATE_NOT_AUTHORIZED'
BLOCKERS=['SUMMARY_EXPANSION_REVIEW_PENDING']
FLAGS=('publication_authorized','deployment_authorized','indexing_authorized','analytics_enabled','advertising_enabled')


def expansion_summaries():
    data=json.loads(EDITORIAL.read_text())
    if len(data['products'])!=27: raise ValueError('exactly 27 expansion summaries required')
    products={p['id']:p for p in content.official(content.load(content.FACTS))['products']}
    for item in data['products']:
        identity=item.get('expected_identity',{})
        if set(identity)!={'manufacturer','display_model','region','variant_status'} or any(products.get(item['product_id'],{}).get(k)!=v for k,v in identity.items()):
            raise ValueError('model, region or variant changed; editorial review required')
        if len(item['claims'])!=3: raise ValueError('three reviewed claims required')
        if not item['description'].strip() or not item['caution'].strip():
            raise ValueError('description and caution required')
        if 'expected_conflict_notes' not in item: raise ValueError('conflict binding required')
        for claim in item['claims']:
            if any(set(v)!={'value','unit','qualifier','scope','source_refs'} for v in claim['expected_facts'].values()):
                raise ValueError('scoped source binding required')
    summaries=content.reviewed_summaries(EDITORIAL)
    prior=content.reviewed_summaries()
    official_ids={p['id'] for p in content.official(content.load(content.FACTS))['products']}
    if set(summaries)&set(prior) or set(summaries)|set(prior)!=official_ids:
        raise ValueError('expansion must cover only remaining official models')
    return summaries


def expanded_artifacts():
    summaries=expansion_summaries()
    plan,artifacts=content.polished_artifacts()
    for pid,(item,section) in summaries.items():
        name='monitors/'+pid.removeprefix('monitor:')+'/index.html'
        text=artifacts[name].decode()
        marker='<section aria-labelledby="specs">'
        if text.count(marker)!=1 or 'id="model-highlights"' in text:
            raise ValueError('one original specifications section required')
        text=text.replace(marker,section+marker)
        text=re.sub(r'(<meta (?:name="description"|property="og:description"|name="twitter:description") content=")[^"]*(")',
                    lambda m:m[1]+escape(item['description'],quote=True)+m[2],text)
        text=text.replace('<aside>','<aside aria-label="사양 적용 범위">').replace('<aside class="source-conflict">','<aside class="source-conflict" aria-label="공식 자료 표기 차이">')
        artifacts[name]=text.encode()
    return plan,artifacts


def validate_summary_expansion(output):
    output=Path(output)
    try:
        _,expected=expanded_artifacts()
        if output.is_symlink() or (output/'site').is_symlink() or (output/'manifest.json').is_symlink():
            return ['symlink not allowed']
        manifest=json.loads((output/'manifest.json').read_text())
        files=list((output/'site').rglob('*'))
        if any(p.is_symlink() for p in files): return ['symlink not allowed']
        if {str(p.relative_to(output/'site')) for p in files if p.is_file()}!=set(expected):
            return ['summary expansion inventory mismatch']
        if manifest.get('purpose')!=PURPOSE or manifest.get('blockers')!=BLOCKERS or any(manifest.get(k) is not False for k in FLAGS):
            return ['summary expansion must retain approval holds']
        if manifest.get('files')!={n:content.digest(v) for n,v in expected.items()}: return ['manifest mismatch']
        return ['altered file: '+n for n,v in expected.items() if (output/'site'/n).read_bytes()!=v]
    except (OSError,ValueError,KeyError,TypeError) as e: return [str(e)]


def build_summary_expansion(output):
    _,artifacts=expanded_artifacts()
    manifest=content.build_content_candidate(output)
    for name,value in artifacts.items(): (Path(output)/'site'/name).write_bytes(value)
    manifest.update(purpose=PURPOSE,blockers=BLOCKERS,files={n:content.digest(v) for n,v in artifacts.items()})
    (Path(output)/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    errors=validate_summary_expansion(output)
    if errors: raise ValueError('; '.join(errors))
    return manifest


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True)
    build_summary_expansion(parser.parse_args().output)
    print('PASS: 30 summary local candidate; production approval unchanged')
