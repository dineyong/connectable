"""Server-side Partners deeplink client. Never logs or persists credentials/results."""
import datetime as dt
import hashlib
import hmac
import json
import os
import re
import urllib.request
from urllib.parse import urlsplit
PATH='/v2/providers/affiliate_open_api/apis/openapi/v1/deeplink'
ORIGIN='https://api-gateway.coupang.com'

def authorization(access,secret,stamp):
    if not access or not secret or re.search(r'[\s,\r\n]',access): raise ValueError('invalid credentials')
    if not re.fullmatch(r'\d{6}T\d{6}Z',stamp): raise ValueError('invalid timestamp')
    signature=hmac.new(secret.encode(),(stamp+'POST'+PATH).encode(),hashlib.sha256).hexdigest()
    return f'CEA algorithm=HmacSHA256, access-key={access}, signed-date={stamp}, signature={signature}'

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs): raise ValueError('API redirects refused')

def deeplink(url):
    u=urlsplit(url)
    if u.scheme!='https' or u.hostname!='www.coupang.com' or u.username or u.password or u.port not in (None,443) or u.fragment or re.search(r'[\s\\\x00-\x1f]',url): raise ValueError('expected official Coupang URL')
    access=os.environ.get('COUPANG_PARTNERS_ACCESS_KEY','')
    secret=os.environ.get('COUPANG_PARTNERS_SECRET_KEY','')
    if not access or not secret: raise ValueError('Coupang Partners environment keys required')
    stamp=dt.datetime.now(dt.timezone.utc).strftime('%y%m%dT%H%M%SZ')
    request=urllib.request.Request(ORIGIN+PATH,data=json.dumps({'coupangUrls':[url]}).encode(),headers={'Content-Type':'application/json','Authorization':authorization(access,secret,stamp)},method='POST')
    with urllib.request.build_opener(NoRedirect()).open(request,timeout=15) as response:
        raw=response.read(262145)
    if len(raw)>262144: raise ValueError('API response too large')
    result=json.loads(raw)
    if result.get('rCode')!='0': raise ValueError('Coupang Partners API rejected request')
    rows=result.get('data',[])
    if len(rows)!=1 or rows[0].get('originalUrl')!=url: raise ValueError('unmatched deeplink response')
    target=rows[0].get('shortenUrl',''); p=urlsplit(target)
    if p.scheme!='https' or p.hostname not in {'link.coupang.com','coupa.ng'} or p.username or p.password or p.port not in (None,443) or re.search(r'[\s\\\x00-\x1f]',target): raise ValueError('unsafe deeplink response')
    return target
