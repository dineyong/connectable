"""Local headline/link feed cache. No article-body scraping or public deployment.

Only two fixed publisher RSS endpoints are fetched. Respect robots, reject
redirects, bound XML, preserve stale data per source, and mark heuristic tags.
--watch polls every 15 minutes while this process runs; not a hosted scheduler.
"""
import argparse
import datetime as dt
import hashlib
import html
import json
import re
import sys
import time
import urllib.error
import urllib.request
import urllib.robotparser
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT/'data/news/tech_news.json'
ASSET = ROOT/'web/tech-news-data.js'
UA = 'ConnectableFeedPreview/1.0'
MAX_BYTES = 2_000_000
SOURCES = {
    'samsung-kr': {'name':'삼성전자 뉴스룸', 'url':'https://news.samsung.com/kr/feed', 'hosts':{'news.samsung.com'}, 'kind':'MANUFACTURER_NEWSROOM', 'language':'ko'},
    'windows-blog': {'name':'Windows Blog', 'url':'https://blogs.windows.com/feed/', 'hosts':{'blogs.windows.com'}, 'kind':'MANUFACTURER_NEWSROOM', 'language':'en'},
}


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')


def date(value):
    try:
        parsed = dt.datetime.fromisoformat(value.replace('Z','+00:00'))
        if parsed.tzinfo is None:
            raise ValueError('timezone required')
        return parsed
    except (TypeError, AttributeError, ValueError) as e:
        raise ValueError('invalid timezone-aware date') from e


def public_link(url, source_id):
    try:
        p = urlsplit(url)
        return (p.scheme == 'https' and p.hostname in SOURCES[source_id]['hosts']
                and not p.username and not p.password and p.port in (None,443)
                and not re.search(r'[\s\\\x00-\x1f]',url))
    except (ValueError, KeyError, TypeError):
        return False


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError('redirect not fetched; review publisher endpoint')


def request_bytes(url):
    opener = urllib.request.build_opener(NoRedirect())
    with opener.open(urllib.request.Request(url,headers={'User-Agent':UA}),timeout=15) as response:
        data = response.read(MAX_BYTES+1)
        if len(data)>MAX_BYTES:
            raise ValueError('feed exceeds byte limit')
        return data


def fetch(source_id):
    source = SOURCES[source_id]
    origin = urlsplit(source['url'])
    robots_url = f'{origin.scheme}://{origin.netloc}/robots.txt'
    robots = request_bytes(robots_url).decode('utf-8',errors='replace')
    policy = urllib.robotparser.RobotFileParser()
    policy.parse(robots.splitlines())
    if not policy.can_fetch(UA,source['url']):
        raise ValueError('robots denies feed access')
    return request_bytes(source['url'])


def parse(raw, source_id, fetched_at):
    if source_id not in SOURCES or len(raw)>MAX_BYTES or b'\x00' in raw or re.search(br'<!\s*(DOCTYPE|ENTITY)',raw,re.I):
        raise ValueError('unsupported source, oversized or entity-bearing XML')
    root=ET.fromstring(raw)
    if root.tag not in ('rss','{http://www.w3.org/2005/Atom}feed'):
        raise ValueError('expected RSS/Atom, not an HTML error page')
    records=[]
    for item in root.findall('./channel/item')[:30]+root.findall('{http://www.w3.org/2005/Atom}entry')[:30]:
        atom='{http://www.w3.org/2005/Atom}'
        title=item.findtext('title') or item.findtext(atom+'title') or ''
        title=html.unescape(re.sub('<[^>]+>','',title)).strip()
        link=item.findtext('link')
        if not link:
            alternate=next((x for x in item.findall(atom+'link') if x.get('rel','alternate')=='alternate'),None)
            link=alternate.get('href') if alternate is not None else None
        if not title or len(title)>500 or not public_link(link,source_id):
            continue
        original_date=item.findtext('pubDate') or item.findtext(atom+'published') or item.findtext(atom+'updated')
        try:
            published=parsedate_to_datetime(original_date) if item.findtext('pubDate') else date(original_date)
            if published.tzinfo is None or published>date(fetched_at)+dt.timedelta(minutes=5):
                continue
            published=published.astimezone(dt.timezone.utc).isoformat(timespec='seconds')
        except (TypeError,ValueError,AttributeError):
            continue
        records.append({'id':'news:'+hashlib.sha256(link.encode()).hexdigest()[:20], 'source_id':source_id, 'title':title,'url':link,'published_at':published,'fetched_at':fetched_at,'category':'MONITOR_DISPLAY' if re.search(r'monitor|display|oled|모니터|디스플레이|odyssey',title,re.I) else 'TECH','category_basis':'TITLE_KEYWORD_HEURISTIC','review_status':'PENDING_PUBLICATION_REVIEW'})
    return records


def validate(data):
    if set(data)!={'schema_version','updated_at','public_status','sources','items'} or type(data['schema_version']) is not int or data['schema_version']!=1 or data['public_status']!='UNKNOWN':
        raise ValueError('invalid isolated news envelope')
    date(data['updated_at'])
    sources=data['sources']
    if not isinstance(sources,list) or {s['id'] for s in sources}!=set(SOURCES) or len(sources)!=len(SOURCES):
        raise ValueError('source registry mismatch')
    for s in sources:
        if set(s)!={'id','name','url','kind','language','last_attempt_at','last_success_at','status'}:
            raise ValueError('unexpected source metadata')
        expected=SOURCES[s['id']]
        if any(s[k]!=expected[k] for k in ['name','url','kind','language']) or s['status'] not in {'OK','ACCESS_FAILED','STALE'}:
            raise ValueError('source metadata/status mismatch')
        if date(s['last_attempt_at']) > date(data['updated_at']):raise ValueError('attempt follows cache timestamp')
        if s['last_success_at'] is not None and date(s['last_success_at']) > date(s['last_attempt_at']):raise ValueError('success cannot follow last attempt')
        if s['status']=='OK' and s['last_success_at'] is None:raise ValueError('OK needs successful check')
    if not isinstance(data['items'],list) or len(data['items'])>60:raise ValueError('bounded item list required')
    seen=set(); ids=set()
    for i in data['items']:
        if set(i)!={'id','source_id','title','url','published_at','fetched_at','category','category_basis','review_status'}:raise ValueError('unexpected article body/fields')
        if not public_link(i['url'],i['source_id']) or i['url'] in seen or i['id'] in ids or i['id']!='news:'+hashlib.sha256(i['url'].encode()).hexdigest()[:20]:raise ValueError('invalid/duplicate article identity')
        seen.add(i['url']);ids.add(i['id'])
        if not isinstance(i['title'],str) or not i['title'].strip() or len(i['title'])>500:raise ValueError('invalid title')
        if i['category'] not in {'MONITOR_DISPLAY','TECH'} or i['category_basis']!='TITLE_KEYWORD_HEURISTIC' or i['review_status']!='PENDING_PUBLICATION_REVIEW':raise ValueError('invalid category/public review state')
        if date(i['published_at'])>date(i['fetched_at'])+dt.timedelta(minutes=5) or date(i['fetched_at'])>date(data['updated_at']):raise ValueError('invalid publication/fetch chronology')
    return data


def refresh(previous=None, fetcher=fetch, stamp=None):
    stamp=stamp or now()
    previous=validate(previous) if previous else {'items':[],'sources':[]}
    source_records=[]; items=[]
    for sid, definition in SOURCES.items():
        old=[i for i in previous['items'] if i['source_id']==sid]
        old_source=next((s for s in previous['sources'] if s['id']==sid),{})
        record={k:definition[k] for k in ['name','url','kind','language']}
        record.update(id=sid,last_attempt_at=stamp,last_success_at=old_source.get('last_success_at'),status='ACCESS_FAILED')
        try:
            new=parse(fetcher(sid),sid,stamp)
            if not new:raise ValueError('empty usable feed; preserve prior cache')
            record.update(status='OK',last_success_at=stamp)
            items.extend(new)
        except (ValueError,ET.ParseError,OSError):
            items.extend(old)
            record['status']='STALE' if old else 'ACCESS_FAILED'
        source_records.append(record)
    unique={i['url']:i for i in items}
    result={'schema_version':1,'updated_at':stamp,'public_status':'UNKNOWN','sources':source_records,'items':sorted(unique.values(),key=lambda i:i['published_at'],reverse=True)}
    return validate(result)


def asset(data):
    validate(data)
    encoded=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('\u2028','\\u2028').replace('\u2029','\\u2029')
    return 'window.CONNECTABLE_TECH_NEWS = '+encoded+';\n'


def write(data):
    validate(data)
    for path,text in [(CACHE,json.dumps(data,ensure_ascii=False,indent=2)+'\n'),(ASSET,asset(data))]:
        temp=path.with_suffix(path.suffix+'.tmp');temp.write_text(text,encoding='utf-8');temp.replace(path)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    parser.add_argument('--watch',action='store_true')
    parser.add_argument('--interval',type=int,default=900)
    args=parser.parse_args()
    if args.interval<900:parser.error('minimum refresh interval is 900 seconds')
    if args.check:
        data=validate(json.loads(CACHE.read_text()))
        if ASSET.read_text()!=asset(data):raise SystemExit('news JS cache is stale')
        print(f"PASS: {len(data['items'])} headline links; no public approval")
        return
    while True:
        previous=json.loads(CACHE.read_text()) if CACHE.exists() else None
        result=refresh(previous)
        write(result)
        print(f"refreshed {len(result['items'])} headlines; {[(s['id'],s['status']) for s in result['sources']]}",flush=True)
        if not args.watch:return
        time.sleep(args.interval)


if __name__=='__main__':main()
