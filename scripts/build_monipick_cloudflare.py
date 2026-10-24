"""Branch-specific Pages build. Produces files; never uploads or changes DNS.

Only the user's 2026-10-24 approved content fingerprint can be public. Original
candidate/preview builders retain their independent non-publication contracts.
"""
import argparse
from datetime import date
import hashlib
import json
import os
from pathlib import Path

from scripts.build_monipick_public_candidate import build_candidate, expected_artifacts, digest
from scripts.prepare_cloudflare_preview import prepare_cloudflare
from scripts.prepare_monipick_content_candidate import polished_artifacts, build_content_candidate

PRODUCTION_BRANCH='codex/monipick-production'
PREVIEW_BRANCH='codex/monipick-private-preview'
APPROVAL=Path(__file__).resolve().parents[1]/'deploy/monipick-public-release.json'
SEARCH_VERIFICATION=APPROVAL.with_name('monipick-search-verification.json')
CONTENT_APPROVAL=APPROVAL.with_name('monipick-content-release.json')
SEO_APPROVAL=APPROVAL.with_name('monipick-seo-release.json')
NAVER_PROOF='naverb7d1be496d4d21a4cf88c23246e48079.html'


def read_approval():
    return json.loads(APPROVAL.read_text())


def read_search_verification():
    return json.loads(SEARCH_VERIFICATION.read_text())


def search_verification_artifacts(record):
    # Explicit user-requested ownership proof only. No paths, redirects, scripts,
    # new origins, or changes to the reviewed UI may enter through this record.
    expected={NAVER_PROOF:'naver-site-verification: '+NAVER_PROOF}
    if (not isinstance(record,dict) or record.get('approval_status')!='USER_APPROVED' or
            record.get('origin')!='https://monipick.com' or
            record.get('files')!=expected):
        raise ValueError('unapproved search ownership proof')
    date.fromisoformat(record['approved_on'])
    return {name:value.encode('utf-8') for name,value in expected.items()}


def content_fingerprint(hashes):
    return hashlib.sha256(json.dumps(hashes,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def validate_approval(record,hashes):
    if (not isinstance(record,dict) or record.get('approval_status')!='USER_APPROVED' or
            record.get('origin')!='https://monipick.com' or
            record.get('production_branch')!=PRODUCTION_BRANCH or
            any(record.get(flag) is not False for flag in (
                'advertising_enabled','analytics_enabled','main_merge_authorized','compatibility_approval_authorized'))):
        raise ValueError('missing or inconsistent publication scope')
    date.fromisoformat(record['approved_on'])
    if record['approved_content_fingerprint']!=content_fingerprint(hashes):
        raise ValueError('served content differs from user-reviewed release; new review required')


def read_content_approval():
    return json.loads(CONTENT_APPROVAL.read_text())


def validate_content_approval(record, baseline, hashes):
    if (not isinstance(record,dict) or record.get('approval_status')!='USER_APPROVED' or
            record.get('origin')!='https://monipick.com' or
            record.get('reviewed_candidate_commit')!='89dd4ec' or
            record.get('baseline_content_fingerprint')!=baseline['approved_content_fingerprint'] or
            any(record.get(k) is not False for k in ('advertising_enabled','analytics_enabled','main_merge_authorized')) or
            record.get('approved_content_fingerprint')!=content_fingerprint(hashes)):
        raise ValueError('content polish differs from separately user-approved candidate')
    date.fromisoformat(record['approved_on'])


def read_seo_approval():
    return json.loads(SEO_APPROVAL.read_text())


def validate_seo_approval(record,baseline,hashes):
    if (not isinstance(record,dict) or record.get('approval_status')!='USER_APPROVED' or
            record.get('origin')!='https://monipick.com' or
            record.get('reviewed_candidate_commit')!='6b933d1cae75f64ae84ea096b1274ab50597c2d9' or
            record.get('baseline_content_fingerprint')!=baseline['approved_content_fingerprint'] or
            any(record.get(k) is not False for k in ('advertising_enabled','analytics_enabled',
                'main_merge_authorized','compatibility_approval_authorized')) or
            record.get('approved_content_fingerprint')!=content_fingerprint(hashes)):
        raise ValueError('SEO release differs from the separately reviewed 30-model candidate')
    date.fromisoformat(record['approved_on'])


def build_for_branch(branch,output):
    if branch==PREVIEW_BRANCH:
        return prepare_cloudflare(output,include_http_check=True)
    if branch!=PRODUCTION_BRANCH:
        raise ValueError('branch not allowed to build or publish this site')
    _,artifacts=expected_artifacts()
    expected={name:digest(value) for name,value in artifacts.items()}
    approval=read_approval()
    validate_approval(approval,expected)
    proofs=search_verification_artifacts(read_search_verification())
    if set(proofs)&set(expected):
        raise ValueError('ownership proof cannot replace reviewed files')
    _,content=polished_artifacts()
    hashes={n:digest(v) for n,v in content.items()}
    content_approval=read_content_approval()
    validate_content_approval(content_approval,approval,hashes)
    # Preserve both earlier release gates, then authorize only the new reviewed bytes.
    from scripts.prepare_monipick_seo_review import review_artifacts,build_review
    _,seo=review_artifacts()
    seo_hashes={n:digest(v) for n,v in seo.items() if n not in proofs}
    seo_approval=read_seo_approval()
    validate_seo_approval(seo_approval,content_approval,seo_hashes)
    manifest=build_review(output)
    validate_seo_approval(seo_approval,content_approval,{n:v for n,v in manifest['files'].items() if n not in proofs})
    for name,content in proofs.items():
        (Path(output)/'site'/name).write_bytes(content)
    proof_hashes={name:digest(value) for name,value in proofs.items()}
    manifest['files'].update(proof_hashes)
    manifest['search_verification_files']=proof_hashes
    manifest.update({
        'purpose':'AUTHORIZED_MONIPICK_PUBLIC_RELEASE','domain':'monipick.com',
        'deployment_authorized':True,'publication_authorized':True,'indexing_authorized':True,
        'advertising_enabled':False,'analytics_enabled':False,'blockers':[],
        'approval_date':seo_approval['approved_on'],
        'reviewed_candidate_commit':seo_approval['reviewed_candidate_commit'],
        'content_baseline_reviewed_candidate_commit':content_approval['reviewed_candidate_commit'],
        'baseline_approved_content_fingerprint':approval['approved_content_fingerprint'],
        'previous_approved_content_fingerprint':content_approval['approved_content_fingerprint'],
        'approved_content_fingerprint':seo_approval['approved_content_fingerprint'],
    })
    (Path(output)/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    return manifest


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    manifest=build_for_branch(os.environ.get('CF_PAGES_BRANCH',''),args.output)
    print('PASS: '+manifest['purpose']+'; file generation only, no upload')


if __name__=='__main__':main()
