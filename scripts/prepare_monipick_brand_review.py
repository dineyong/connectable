"""Local-only structured data and share identity review; no publication authority."""
import argparse
from html import escape,unescape
from http.server import ThreadingHTTPServer
import json
from pathlib import Path
import re
import struct

from scripts.prepare_monipick_seo_review import review_artifacts,build_review
from scripts.prepare_monipick_content_candidate import ROOT,digest
from scripts.serve_monipick_candidate import handler_for
from scripts.validate_local_site import Document

ORIGIN='https://monipick.com'
ASSET_ROOT=ROOT/'assets/brand'
SHARE='/assets/brand/monipick-share-v1.png'
ASSETS=('monipick-share-v1.png','favicon.svg','favicon-48.png','favicon-180.png','favicon-192.png','favicon.ico')
PURPOSE='BRAND_METADATA_REVIEW_NOT_AUTHORIZED'
HOLDS=('publication_authorized','deployment_authorized','indexing_authorized','analytics_enabled','advertising_enabled')


def safe_json(value):
    return json.dumps(value,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')


def structured_data(page,text):
    canonical=page['proposed_canonical']
    if not page['sitemap_candidate']:return None
    doc=Document(text)
    if len(doc.titles)!=1 or len(doc.meta.get('description',[]))!=1:
        raise ValueError('unique visible-page metadata required')
    website=ORIGIN+'/#website'
    graph=[]
    if page['route']=='/':
        graph.append({'@type':'WebSite','@id':website,'url':ORIGIN+'/','name':'모니픽','inLanguage':'ko-KR'})
    webpage={'@type':'WebPage','@id':canonical+'#webpage','url':canonical,
             'name':doc.titles[0],'description':doc.meta['description'][0],
             'inLanguage':'ko-KR','isPartOf':{'@id':website}}
    graph.append(webpage)
    if re.fullmatch(r'monitors/[^/]+/index.html',page['source']):
        nav=re.search(r'<nav class="seo-breadcrumb"[^>]*>(.*?)</nav>',text,re.S)
        if not nav:raise ValueError('visible breadcrumb required')
        title=re.search(r'aria-current="page">(.*?)</span>',nav[1],re.S)
        anchors=re.findall(r'<a href="([^"]+)">(.*?)</a>',nav[1],re.S)
        if not title or anchors!=[('/','홈'),('/monitors/','전체 모니터')]:
            raise ValueError('visible breadcrumb hierarchy changed')
        breadcrumb_id=canonical+'#breadcrumb'
        items=[('홈',ORIGIN+'/'),('전체 모니터',ORIGIN+'/monitors/'),(unescape(title[1]),canonical)]
        graph.append({'@type':'BreadcrumbList','@id':breadcrumb_id,'itemListElement':[
            {'@type':'ListItem','position':i,'name':name,'item':url} for i,(name,url) in enumerate(items,1)]})
        webpage['breadcrumb']={'@id':breadcrumb_id}
    return {'@context':'https://schema.org','@graph':graph}


def brand_artifacts():
    plan,artifacts=review_artifacts()
    assets={name:(ASSET_ROOT/name).read_bytes() for name in ASSETS}
    sizes={'monipick-share-v1.png':(1200,630),'favicon-48.png':(48,48),
           'favicon-180.png':(180,180),'favicon-192.png':(192,192)}
    for name,size in sizes.items():
        body=assets[name]
        if body[:8]!=b'\x89PNG\r\n\x1a\n' or struct.unpack('>II',body[16:24])!=size:
            raise ValueError('invalid image dimensions: '+name)
    if assets['favicon.ico'][:6]!=struct.pack('<HHH',0,1,3):raise ValueError('three-size ICO required')
    if b'<script' in assets['favicon.svg'] or b'href=' in assets['favicon.svg']:raise ValueError('self-contained icon required')
    for name,body in assets.items():artifacts['assets/brand/'+name]=body
    artifacts['favicon.ico']=assets['favicon.ico']
    for page in plan['pages']:
        name=page['source'];text=artifacts[name].decode()
        if Document(text).jsonld:raise ValueError('existing structured data must be reconciled, not duplicated')
        tags=('<link rel="icon" type="image/svg+xml" href="/assets/brand/favicon.svg">\n'
              '<link rel="icon" type="image/png" sizes="48x48" href="/assets/brand/favicon-48.png">\n'
              '<link rel="icon" type="image/png" sizes="192x192" href="/assets/brand/favicon-192.png">\n'
              '<link rel="shortcut icon" href="/favicon.ico">\n'
              '<link rel="apple-touch-icon" sizes="180x180" href="/assets/brand/favicon-180.png">\n')
        if name!='404.html':
            tags+=('<meta property="og:image" content="'+ORIGIN+SHARE+'">\n'
                '<meta property="og:image:secure_url" content="'+ORIGIN+SHARE+'">\n'
                '<meta property="og:image:type" content="image/png">\n'
                '<meta property="og:image:width" content="1200">\n'
                '<meta property="og:image:height" content="630">\n'
                '<meta property="og:image:alt" content="모니픽 — 모니터 선택의 기준. 사양은 나란히, 출처는 분명하게.">\n'
                '<meta name="twitter:image" content="'+ORIGIN+SHARE+'">\n'
                '<meta name="twitter:image:alt" content="모니픽 — 모니터 선택의 기준">\n')
            text,count=re.subn(r'(<meta name="twitter:card" content=")summary(")',r'\g<1>summary_large_image\2',text)
            if count!=1:raise ValueError('one share card required')
        schema=structured_data(page,text)
        if schema:tags+='<script type="application/ld+json">'+safe_json(schema)+'</script>\n'
        if text.count('</head>')!=1:raise ValueError('one head required')
        artifacts[name]=text.replace('</head>',tags+'</head>').encode()
    artifacts['index.html']=artifacts['monitor-v3.html']
    return plan,artifacts


def validate_brand_review(output):
    try:
        output=Path(output);_,expected=brand_artifacts()
        manifest_path=output/'manifest.json'
        if manifest_path.is_symlink():return ['manifest symlink']
        manifest=json.loads(manifest_path.read_text())
        paths=list((output/'site').rglob('*'))
        if any(p.is_symlink() for p in paths):return ['symlink not permitted']
        if {str(p.relative_to(output/'site'))for p in paths if p.is_file()}!=set(expected):return ['inventory mismatch']
        if (manifest.get('purpose')!=PURPOSE or manifest.get('blockers')!=['BRAND_METADATA_REVIEW_PENDING'] or
                any(manifest.get(k) is not False for k in HOLDS)):return ['review holds changed']
        if manifest.get('files')!={n:digest(v) for n,v in expected.items()}:return ['manifest hash mismatch']
        return ['altered file: '+n for n,v in expected.items() if (output/'site'/n).read_bytes()!=v]
    except (OSError,ValueError,KeyError,TypeError,struct.error) as e:return [str(e)]


def build_brand_review(output):
    _,artifacts=brand_artifacts();manifest=build_review(output)
    for name,value in artifacts.items():
        path=Path(output)/'site'/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(value)
    manifest.update(purpose=PURPOSE,blockers=['BRAND_METADATA_REVIEW_PENDING'],files={n:digest(v)for n,v in artifacts.items()})
    (Path(output)/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    errors=validate_brand_review(output)
    if errors:raise ValueError('; '.join(errors))
    return manifest


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',required=True)
    p.add_argument('--serve',action='store_true');p.add_argument('--port',type=int,default=8886)
    a=p.parse_args();build_brand_review(a.output)
    print('PASS: local metadata/brand review; deployment remains unauthorized',flush=True)
    if a.serve:
        server=ThreadingHTTPServer(('127.0.0.1',a.port),handler_for(Path(a.output),validate_brand_review))
        print(f'REVIEW ONLY: http://127.0.0.1:{server.server_port}/',flush=True);server.serve_forever()


if __name__=='__main__':main()
