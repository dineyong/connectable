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

PRODUCTION_BRANCH='codex/monipick-production'
PREVIEW_BRANCH='codex/monipick-private-preview'
APPROVAL=Path(__file__).resolve().parents[1]/'deploy/monipick-public-release.json'


def read_approval():
    return json.loads(APPROVAL.read_text())


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


def build_for_branch(branch,output):
    if branch==PREVIEW_BRANCH:
        return prepare_cloudflare(output,include_http_check=True)
    if branch!=PRODUCTION_BRANCH:
        raise ValueError('branch not allowed to build or publish this site')
    _,artifacts=expected_artifacts()
    expected={name:digest(value) for name,value in artifacts.items()}
    approval=read_approval()
    validate_approval(approval,expected)
    manifest=build_candidate(output)
    validate_approval(approval,manifest['files'])
    manifest.update({
        'purpose':'AUTHORIZED_MONIPICK_PUBLIC_RELEASE','domain':'monipick.com',
        'deployment_authorized':True,'publication_authorized':True,'indexing_authorized':True,
        'advertising_enabled':False,'analytics_enabled':False,'blockers':[],
        'approval_date':approval['approved_on'],
        'reviewed_candidate_commit':approval['reviewed_candidate_commit'],
        'approved_content_fingerprint':approval['approved_content_fingerprint'],
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
