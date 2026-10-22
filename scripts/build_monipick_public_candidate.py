"""Create public-format files locally. Never upload, approve, or change Cloudflare.

The Cloudflare preview build must continue to use prepare_cloudflare_preview.
This output requires explicit publication approval before any public deployment.
"""
import argparse
import hashlib
from html import escape
import json
from pathlib import Path
import re
import shutil

from scripts.prepare_launch_preview import WEB, ASSETS, prepare, validate_display_artifacts
from scripts.prepare_monipick_release import (
    CONTACT_EMAIL, CONTACT_DELIVERY_STATUS, ORIGIN, release_plan, validate_plan,
    proposed_headers, sitemap,
)
from scripts.validate_local_site import Document

PURPOSE = 'PUBLIC_FORMAT_CANDIDATE_NOT_AUTHORIZED'
FLAGS = ('deployment_authorized', 'publication_authorized', 'indexing_authorized', 'analytics_enabled')
ROBOTS = 'User-agent: *\nAllow: /\nSitemap: ' + ORIGIN + '/sitemap.xml\n'
REDIRECTS = '/monitor-v3.html / 301\n/monitor-v3 / 301\n'
OPERATION_SOURCE = '호스팅 서비스와 비공개 검수 인증에서 처리하는 접속·보안 정보는 사이트의 방문 통계와 별개입니다. 공개 전 실제 운영 설정에 맞춰 관련 안내를 확인합니다.'
OPERATION_PUBLIC = ('이 사이트의 정적 파일은 Cloudflare Pages에서 제공합니다. 호스팅 제공자가 서비스 제공과 보안을 위해 '
    '접속 정보를 처리할 수 있으며, 사이트 자체의 방문 통계와 구분됩니다. 문의 메일은 Cloudflare Email Routing을 통해 '
    '운영 Gmail로 전달되며, 회신과 정정 검토에 필요한 범위에서 확인합니다. 불필요한 개인정보를 보내지 마세요.')


def public_html(text, page):
    text, count = re.subn(r'<meta\s+name=["\']robots["\']\s+content=["\'][^"\']*["\']\s*/?>',
        '<meta name="robots" content="' + page['proposed_robots'] + '">', text, flags=re.I)
    if count != 1:
        raise ValueError('exactly one source robots meta required: ' + page['source'])
    for old, new in [
        ('비공개 검수 중 · ', ''), ('비공개 검수 중입니다. ', ''),
        ('비공개 검수 중', '공식 자료 보강'), ('비공개 검수 안내', '사양 안내'),
        ('미리보기 상태', '자료 안내'),
    ]:
        text = text.replace(old, new)
    if page['source'] == 'information.html':
        if text.count(OPERATION_SOURCE) != 1:
            raise ValueError('operations source changed; review public copy before rebuilding')
        text = text.replace(OPERATION_SOURCE, OPERATION_PUBLIC)
        text = text.replace('외부 계정에서의 수신 테스트를 확인했습니다. ', '')
    canonical = page['proposed_canonical']
    if canonical:
        head = ('<link rel="canonical" href="' + escape(canonical, quote=True) + '">\n'
                '<meta property="og:url" content="' + escape(canonical, quote=True) + '">\n')
        if text.count('</head>') != 1:
            raise ValueError('one closing head required')
        text = text.replace('</head>', head + '</head>')
    return text


def expected_artifacts(web=WEB):
    web=Path(web)
    plan=release_plan(web)
    validate_plan(plan)
    files = set(ASSETS) | {'monitors/index.html'} | {
        str(p.relative_to(web)) for p in (web/'monitors').glob('*/index.html')}
    artifacts={name:(web/name).read_bytes() for name in sorted(files)}
    for page in plan['pages']:
        artifacts[page['source']]=public_html(artifacts[page['source']].decode('utf-8'),page).encode('utf-8')
    artifacts['index.html']=artifacts['monitor-v3.html']
    artifacts.update({name:value.encode('utf-8') for name,value in {
        '_headers':proposed_headers(plan), '_redirects':REDIRECTS,
        'robots.txt':ROBOTS, 'sitemap.xml':sitemap(plan),
    }.items()})
    return plan,artifacts


def digest(value):
    return hashlib.sha256(value).hexdigest()


def validate_candidate(output, web=WEB):
    """Compare every served byte with a deterministic transform of validated sources.

    A supplied manifest is not an independent source of truth for facts or inventory.
    """
    output=Path(output)
    errors=[]
    try:
        plan,expected=expected_artifacts(web)
        manifest_path=output/'manifest.json'
        if manifest_path.is_symlink():
            return ['manifest symlink not permitted']
        manifest=json.loads(manifest_path.read_text())
        if not isinstance(manifest,dict):
            return ['manifest object required']
        if (manifest.get('purpose')!=PURPOSE or manifest.get('planned_origin')!=ORIGIN or
                any(manifest.get(flag) is not False for flag in FLAGS) or
                manifest.get('blockers')!=['FINAL_PUBLICATION_APPROVAL_PENDING'] or
                manifest.get('contact_email')!=CONTACT_EMAIL or
                manifest.get('contact_delivery_status')!=CONTACT_DELIVERY_STATUS or
                manifest.get('pages')!=plan['pages']):
            errors.append('manifest must retain candidate identity, current source plan and publication holds')
        site=output/'site'
        paths=list(site.rglob('*'))
        if any(p.is_symlink() for p in paths):
            return errors+['symlinks are not permitted in candidate']
        actual={str(p.relative_to(site)) for p in paths if p.is_file()}
        if actual!=set(expected):
            errors.append('served inventory differs from explicit current-site allowlist')
        hashes={name:digest(value) for name,value in expected.items()}
        if manifest.get('files')!=hashes:
            errors.append('manifest hash inventory differs from expected source transform')
        for name,content in expected.items():
            p=site/name
            if not p.is_file() or p.read_bytes()!=content:
                errors.append('missing or altered candidate file: '+name)
        validate_display_artifacts(site)
        for name in sorted(actual):
            if not name.endswith('.html'): continue
            text=(site/name).read_text()
            doc=Document(text)
            if doc.duplicate_ids or doc.lang!='ko':
                errors.append('invalid document structure: '+name)
            if '비공개 검수 중' in text or '공개 전 실제 운영' in text:
                errors.append('preview-only copy remains: '+name)
    except (OSError,ValueError,KeyError,TypeError) as exc:
        errors.append(str(exc))
    return errors


def build_candidate(output, web=WEB):
    output=Path(output).resolve()
    # Reuse all original/derived validation and safe output-path guards first.
    prepare(output,web)
    try:
        plan,artifacts=expected_artifacts(web)
        for name,content in artifacts.items():
            (output/'site'/name).write_bytes(content)
        manifest={
            'purpose':PURPOSE,'planned_origin':ORIGIN,'domain':None,
            **{flag:False for flag in FLAGS},
            'blockers':['FINAL_PUBLICATION_APPROVAL_PENDING'],
            'contact_email':CONTACT_EMAIL,'contact_delivery_status':CONTACT_DELIVERY_STATUS,
            'pages':plan['pages'],'files':{name:digest(value) for name,value in sorted(artifacts.items())},
        }
        (output/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
        errors=validate_candidate(output,web)
        if errors: raise ValueError('; '.join(errors))
    except Exception:
        shutil.rmtree(output)
        raise
    return manifest


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True,help='new local directory outside web; never a deployment destination')
    parser.add_argument('--check',action='store_true',help='validate an existing candidate without changing it')
    args=parser.parse_args()
    if args.check:
        errors=validate_candidate(args.output)
        if errors: parser.exit(1,'FAIL: '+'; '.join(errors)+'\n')
    else: build_candidate(args.output)
    print('PASS: public-format candidate validated locally; publication/indexing remain unauthorized')


if __name__=='__main__': main()
