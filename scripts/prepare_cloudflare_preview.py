"""Prepare Pages preview files locally; this command never uploads or deploys."""
import argparse
import hashlib
import json
from pathlib import Path

from scripts.prepare_launch_preview import WEB, prepare


PREVIEW_HEADERS = """/*
  X-Robots-Tag: noindex, nofollow, noarchive
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()
  Cache-Control: no-store
"""


def prepare_cloudflare(output, web=WEB, include_http_check=False):
    manifest = prepare(output, web=web)
    output = Path(output).resolve()
    site = output / 'site'
    additions = {
        '_headers': PREVIEW_HEADERS,
        'robots.txt': 'User-agent: *\nDisallow: /\n',
    }
    if include_http_check:
        for extension in ['html', 'js']:
            additions['__preview_http_check.' + extension] = (
                Path(__file__).parent / ('preview_http_check.' + extension)
            ).read_text(encoding='utf-8')
    for name, content in additions.items():
        target = site / name
        target.write_text(content, encoding='utf-8')
        manifest['files'][name] = hashlib.sha256(target.read_bytes()).hexdigest()
    manifest['hosting_target'] = 'CLOUDFLARE_PAGES_PREVIEW_CANDIDATE'
    manifest['access_control_verified'] = False
    # Headers and robots discourage indexing; they do not authenticate requests.
    manifest['requires_access_control_before_upload'] = True
    manifest['http_check_included'] = include_http_check
    (output / 'manifest.json').write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, help='new local directory outside web')
    parser.add_argument('--include-http-check', action='store_true',
                        help='include same-origin HTTP diagnostics for authenticated private review only')
    args = parser.parse_args()
    manifest = prepare_cloudflare(args.output, include_http_check=args.include_http_check)
    print(f'PASS: {len(manifest["files"])} preview files; access control unverified; no deployment')


if __name__ == '__main__':
    main()
