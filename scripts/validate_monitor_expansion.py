"""Validate isolated monitor research, without claiming popularity or approval.

Official facts, community observations and market signals remain separate.
Domain checks are a bounded publisher allowlist, not live source authentication.
"""
import json
import math
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit, unquote
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scripts.validate_question_corpus_v2 import unique_object, reject_constant, sensitive_strings, url_key
from scripts.site_content_validation import checked_date
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/research/monitor-expansion'
DOMAINS={
 'LG':{'www.lg.com'}, 'Dell':{'www.dell.com'},
 'Samsung':{'www.samsung.com','images.samsung.com'},
 'BenQ':{'www.benq.com'}, 'ASUS':{'www.asus.com','rog.asus.com'},
 'MSI':{'www.msi.com'}, 'Gigabyte':{'www.gigabyte.com'}, 'AOC':{'www.aoc.com'},
}


def load(path):return json.loads(Path(path).read_text(),object_pairs_hook=unique_object,parse_constant=reject_constant)
def require(test,message):
    if not test:raise ValueError(message)
def fields(obj,names,path):require(isinstance(obj,dict) and set(obj)==set(names.split()),path+': missing/unexpected fields')
def text(value,path):require(isinstance(value,str) and bool(value.strip()),path+': nonblank text required')
def strings(value,path,empty=True):
    require(isinstance(value,list) and (empty or bool(value)),path+': array required')
    for v in value:text(v,path)
    require(len(value)==len(set(value)),path+': duplicate value')
def enum(value,allowed,path):require(value in allowed.split(),path+': invalid enum')
def url(value):
    text(value,'url')
    require(not re.search(r'[\s\\\x00-\x1f]',value),'unsafe URL characters')
    try:p=urlsplit(value);port=p.port
    except ValueError as e:raise ValueError('invalid URL') from e
    require(not re.search(r'%(?![0-9a-fA-F]{2})|(?i:%(?:0[0-9a-f]|1[0-9a-f]|7f|25|5c))',value),'unsafe URL encoding')
    decoded=unquote(value,errors='strict')
    require(not re.search(r'[\x00-\x1f\x7f\\]',decoded),'decoded URL controls')
    require(p.scheme=='https' and bool(p.hostname) and not p.username and not p.password and port in (None,443),'public HTTPS URL required')
    return p

def envelope(data,keys):
    fields(data,'schema_version checked_on public_status '+keys,'root')
    require(type(data['schema_version']) is int and data['schema_version']==1,'unsupported version')
    checked_date(data['checked_on'],'checked_on');require(data['public_status']=='UNKNOWN','research approval withheld')
    errors=sensitive_strings(data);require(not errors,str(errors[:3]))

def index(rows,key):
    require(isinstance(rows,list),'rows must be array');result={}
    for row in rows:
        text(row[key],key);require(row[key] not in result,'duplicate '+key);result[row[key]]=row
    return result

def references(refs,objects):
    strings(refs,'references',empty=False);require(set(refs)<=set(objects),'missing reference')

def official(data):
    envelope(data,'products');products=index(data['products'],'id')
    for p in products.values():
        fields(p,'id manufacturer display_model region variant_status source_refs facts missing_fields notes','product')
        require(re.fullmatch(r'monitor:[a-z0-9-]+',p['id']),'invalid product ID')
        for k in ['manufacturer','display_model','region']:text(p[k],k)
        enum(p['variant_status'],'UNKNOWN EXACT_DOCUMENT_MODEL','variant_status')
        strings(p['missing_fields'],'missing_fields');strings(p['notes'],'notes')
        sources=index(p['source_refs'],'id');require(bool(sources),'official sources required')
        for s in sources.values():
            fields(s,'id url title checked_on access_status location','source')
            parsed=url(s['url']);checked_date(s['checked_on'],'source.checked_on')
            require(s['access_status']=='DIRECT_CHECK','unread official source')
            for k in ['title','location']:text(s[k],k)
            domains=DOMAINS.get(p['manufacturer'],set())
            require(parsed.hostname in domains,'unknown manufacturer host; manual scope review required')
        facts=index(p['facts'],'id');require(bool(facts),'no verified facts')
        for f in facts.values():
            fields(f,'id property value unit scope source_refs location qualifier','fact')
            for k in ['property','scope','location']:text(f[k],k)
            require(f['unit'] is None or isinstance(f['unit'],str),'invalid unit')
            enum(f['qualifier'],'MANUFACTURER_STATED UP_TO RATED UNKNOWN','qualifier')
            references(f['source_refs'],sources)
            if type(f['value']) in (int,float):require(math.isfinite(f['value']),'nonfinite fact')
    return data

def community(data):
    envelope(data,'reviews classifications excluded_sources');reviews=index(data['reviews'],'id');urls=set()
    for r in reviews.values():
        fields(r,'id manufacturer display_model url site checked_on origin record_type sentiment summary positives limitations usage_conditions commercial_context review_status usable_for_compatibility','review')
        url(r['url']);key=url_key(r['url']);require(key not in urls,'duplicate review URL');urls.add(key)
        checked_date(r['checked_on'],'review.checked_on')
        for k in ['manufacturer','display_model','site','summary']:text(r[k],k)
        enum(r['origin'],'DIRECT_CHECK EXISTING_RESEARCH','origin')
        enum(r['record_type'],'FIRST_HAND_REVIEW PROBLEM_REPORT QUESTION RECOMMENDATION','record_type')
        enum(r['sentiment'],'POSITIVE MIXED NEGATIVE UNKNOWN','sentiment')
        enum(r['commercial_context'],'PRESENT NOT_OBSERVED UNKNOWN','commercial_context')
        require(r['review_status']=='PENDING_HUMAN_REVIEW' and r['usable_for_compatibility']=='NO','review cannot approve compatibility')
        for k in ['positives','limitations','usage_conditions']:strings(r[k],k)
    for c in index(data['classifications'],'display_model').values():
        fields(c,'display_model label review_refs rationale','review classification');text(c['rationale'],'rationale');references(c['review_refs'],reviews)
        enum(c['label'],'POSITIVE_REVIEW_CANDIDATE MIXED_REPORTS INSUFFICIENT_EVIDENCE','classification')
        selected=[reviews[r] for r in c['review_refs']]
        require(all(r['display_model']==c['display_model'] for r in selected),'cross-model review classification')
        if c['label']=='POSITIVE_REVIEW_CANDIDATE':
            require(len(selected)>=2 and all(r['sentiment']=='POSITIVE' and r['record_type']=='FIRST_HAND_REVIEW' for r in selected),'positive candidate needs two actual positive review documents')
    for x in data['excluded_sources']:
        fields(x,'url reason','excluded');url(x['url']);text(x['reason'],'reason')
    return data

def market(data):
    envelope(data,'signals classifications access_attempts');signals=index(data['signals'],'id')
    for s in signals.values():
        fields(s,'id display_model platform url checked_on metric value unit period scope source_kind is_proxy limitations','signal')
        url(s['url']);checked_date(s['checked_on'],'signal.checked_on')
        enum(s['platform'],'NAVER COUPANG OTHER','platform');enum(s['metric'],'SEARCH_VOLUME SALES_COUNT PLATFORM_RANK REVIEW_COUNT SEARCH_INTEREST_INDEX','metric')
        require(s['source_kind']=='DIRECT_CHECK','signal needs direct check')
        require(type(s['is_proxy']) is bool,'proxy flag required')
        for k in ['display_model','period','scope']:text(s[k],k)
        strings(s['limitations'],'limitations',empty=False)
        require(s['value'] is not None,'missing metric cannot be a collected signal')
        require(type(s['value']) in (int,float) and math.isfinite(s['value']) and s['value']>=0,'numeric metric required')
        require(s['unit'] is None or isinstance(s['unit'],str),'invalid signal unit')
        if s['metric'] in {'PLATFORM_RANK','REVIEW_COUNT','SEARCH_INTEREST_INDEX'}:require(s['is_proxy'],'proxy cannot become search/sales count')
    for c in index(data['classifications'],'display_model').values():
        fields(c,'display_model label signal_refs rationale','market classification');text(c['rationale'],'rationale')
        enum(c['label'],'SEARCH_INTEREST_CANDIDATE PURCHASE_INTEREST_CANDIDATE INSUFFICIENT_PUBLIC_DATA','market classification')
        strings(c['signal_refs'],'signal_refs');require(set(c['signal_refs'])<=set(signals),'unknown market signal')
        selected=[signals[r] for r in c['signal_refs']]
        require(all(s['display_model']==c['display_model'] for s in selected),'cross-model popularity classification')
        if c['label']!='INSUFFICIENT_PUBLIC_DATA':
            require(bool(selected),'popularity needs evidence')
            allowed={'SEARCH_VOLUME','SEARCH_INTEREST_INDEX'} if c['label']=='SEARCH_INTEREST_CANDIDATE' else {'SALES_COUNT','PLATFORM_RANK','REVIEW_COUNT'}
            require(any(s['metric'] in allowed for s in selected),'wrong evidence for popularity classification')
    for a in data['access_attempts']:
        fields(a,'url status reason','access');url(a['url']);text(a['reason'],'reason');enum(a['status'],'ACCESS_FAILED LOGIN_REQUIRED NO_PUBLIC_METRIC DIRECT_CHECK','access status')
    return data


def validate_all():
    values={}
    for name,method in [('official_specs.json',official),('community_reviews.json',community),('market_signals.json',market)]:values[name]=method(load(DATA/name))
    return values

if __name__=='__main__':
    values=validate_all()
    print('PASS: isolated official facts, community candidates and market proxies; public UNKNOWN')
    print({name:len(value.get('products',value.get('reviews',value.get('signals',[])))) for name,value in values.items()})
