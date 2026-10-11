"""Reviewed product announcements, separate from automated RSS and spec catalog."""
import datetime as dt
import json
import re
from pathlib import Path
from urllib.parse import urlsplit
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/news/product_announcements.json'
ASSET=ROOT/'web/product-news-data.js'
SOURCES={'benq-kr':('www.benq.com','/ko-kr/news/products/'), 'apple-kr':('images.apple.com','/kr/newsroom/')}

def validate(data):
    if set(data)!={'public_status','items'} or data['public_status']!='UNKNOWN': raise ValueError('public hold required')
    seen=set(); urls=set()
    for item in data['items']:
        required={'id','source_id','source_name','url','title','summary','category','published_on','checked_on','evidence_location','region','preorder_on','available_on','review_status'}
        if set(item)!=required: raise ValueError('unexpected announcement fields')
        if item['id'] in seen or item['url'] in urls: raise ValueError('duplicate announcement')
        seen.add(item['id']); urls.add(item['url'])
        host,prefix=SOURCES[item['source_id']]
        u=urlsplit(item['url'])
        if u.scheme!='https' or u.hostname!=host or not u.path.startswith(prefix) or u.username or u.password or u.port not in (None,443) or u.query or u.fragment or re.search(r'[\s\\%]',item['url']): raise ValueError('invalid official URL')
        if item['category'] not in {'MONITOR_LAUNCH','PHONE_PREORDER'} or item['review_status']!='PENDING_PUBLICATION_REVIEW' or item['region'] not in {'KR','UNKNOWN'}: raise ValueError('invalid state')
        for key in ['title','summary','source_name','evidence_location']:
            if not isinstance(item[key],str) or not item[key].strip() or len(item[key])>500: raise ValueError('missing or long text')
        for key in ['published_on','checked_on','preorder_on','available_on']:
            value=item[key]
            if value is None and key in {'preorder_on','available_on'}: continue
            if not isinstance(value,str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}',value): raise ValueError('date required')
            dt.date.fromisoformat(value)
        if item['published_on']>item['checked_on']: raise ValueError('future publication')
        if item['preorder_on'] and item['available_on'] and item['preorder_on']>item['available_on']: raise ValueError('invalid schedule')
    return data

def asset(data):
    return 'window.CONNECTABLE_PRODUCT_NEWS = '+json.dumps(validate(data),ensure_ascii=False).replace('<','\\u003c').replace('\u2028','\\u2028').replace('\u2029','\\u2029')+';\n'

if __name__=='__main__':
    import sys
    generated=asset(json.loads(DATA.read_text()))
    if '--check' in sys.argv:
        if ASSET.read_text()!=generated: raise SystemExit('stale product news asset')
        print('PASS: product announcement evidence and derived asset')
    else: ASSET.write_text(generated)
