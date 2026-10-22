"""Build inactive release drafts outside the protected preview's document root.

No deployment, DNS, approval or indexing activation is implemented here.
"""
import argparse
import hashlib
import json
from pathlib import Path
from xml.etree import ElementTree as ET

from scripts.prepare_cloudflare_preview import prepare_cloudflare
from scripts.prepare_launch_preview import ASSETS, WEB

ORIGIN = 'https://monipick.com'
CONTACT_EMAIL = 'contact@monipick.com'
CONTACT_DELIVERY_STATUS = 'ROUTING_CONFIGURED_DELIVERY_TEST_PENDING'
EXCLUDED = {'404.html', 'tech-news.html', 'monitor10-review.html'}
CSP = ("default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; "
       "connect-src 'self'; object-src 'none'; base-uri 'none'; form-action 'none'; "
       "frame-ancestors 'none'")


def route_for(source):
    if source == 'monitor-v3.html':
        return '/'
    if source.endswith('/index.html'):
        return '/' + source.removesuffix('index.html')
    return '/' + source.removesuffix('.html')


def release_plan(web):
    web = Path(web)
    sources = sorted({name for name in ASSETS if name.endswith('.html')} |
                     {str(p.relative_to(web)) for p in (web / 'monitors').rglob('index.html')})
    pages = []
    for source in sources:
        path = web / source
        route = route_for(source)
        pages.append({
            'source': source, 'source_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'route': route, 'proposed_canonical': None if source == '404.html' else ORIGIN + route,
            'proposed_robots': 'noindex,follow' if source in EXCLUDED else 'index,follow',
            'sitemap_candidate': source not in EXCLUDED,
        })
    return {'status': 'INACTIVE_DRAFT', 'origin': ORIGIN, 'analytics_enabled': False,
            'contact_email': CONTACT_EMAIL, 'contact_delivery_status': CONTACT_DELIVERY_STATUS, 'publication_authorized': False, 'indexing_authorized': False,
            'blockers': ['CONTACT_ROUTING_PENDING', 'FINAL_PUBLICATION_APPROVAL_PENDING'],
            'pages': pages}


def validate_plan(plan):
    if (plan.get('status') != 'INACTIVE_DRAFT' or plan.get('origin') != ORIGIN or
            plan.get('analytics_enabled') is not False or plan.get('contact_email') != CONTACT_EMAIL or
            plan.get('contact_delivery_status') != CONTACT_DELIVERY_STATUS or
            plan.get('publication_authorized') is not False or
            plan.get('indexing_authorized') is not False):
        raise ValueError('draft must preserve pending contact, analytics exclusion and approval holds')
    if plan.get('blockers') != ['CONTACT_ROUTING_PENDING', 'FINAL_PUBLICATION_APPROVAL_PENDING']:
        raise ValueError('missing release blockers')
    routes, sources = set(), set()
    for page in plan['pages']:
        source, route = page['source'], page['route']
        if source in sources or route in routes:
            raise ValueError('duplicate source or route')
        if route != route_for(source) or any(char in route for char in ('?', '#', '\\')):
            raise ValueError('invalid canonical route')
        expected = None if source == '404.html' else ORIGIN + route
        if page['proposed_canonical'] != expected:
            raise ValueError('canonical origin/path mismatch')
        included = source not in EXCLUDED
        if page['sitemap_candidate'] is not included or page['proposed_robots'] != (
                'index,follow' if included else 'noindex,follow'):
            raise ValueError('indexing scope mismatch')
        sources.add(source)
        routes.add(route)
    if not EXCLUDED.issubset(sources) or 'monitor-v3.html' not in sources:
        raise ValueError('required current-site routes missing')


def sitemap(plan):
    # Deliberately no lastmod: a build date is not an evidence recheck date.
    ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    root = ET.Element('{http://www.sitemaps.org/schemas/sitemap/0.9}urlset')
    for page in plan['pages']:
        if page['sitemap_candidate']:
            url = ET.SubElement(root, '{http://www.sitemaps.org/schemas/sitemap/0.9}url')
            ET.SubElement(url, '{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text = page['proposed_canonical']
    return ET.tostring(root, encoding='unicode', xml_declaration=True) + '\n'


def proposed_headers(plan):
    headers = ('/*\n  X-Content-Type-Options: nosniff\n  X-Frame-Options: DENY\n'
               '  Referrer-Policy: strict-origin-when-cross-origin\n'
               '  Permissions-Policy: camera=(), microphone=(), geolocation=()\n'
               f'  Content-Security-Policy: {CSP}\n')
    for page in plan['pages']:
        if not page['sitemap_candidate']:
            for route in [page['route'], '/' + page['source']]:
                headers += f'\n{route}\n  X-Robots-Tag: noindex, follow\n'
    headers += '\nhttps://monipick.pages.dev/*\n  X-Robots-Tag: noindex, nofollow\n'
    return headers


def prepare_release(output, web=WEB):
    output = Path(output).resolve()
    # Existing validated preview is copied as-is and keeps all noindex/robots/header holds.
    manifest = prepare_cloudflare(output, web=web)
    plan = release_plan(web)
    validate_plan(plan)
    if any(page['source'] not in manifest['files'] for page in plan['pages']):
        raise ValueError('planned page is outside the validated preview inventory')
    drafts = output / 'activation-drafts'
    drafts.mkdir()
    artifacts = {
        'page-metadata.proposed.json': json.dumps(plan, ensure_ascii=False, indent=2) + '\n',
        'sitemap.xml.proposed': sitemap(plan),
        'robots.txt.proposed': 'User-agent: *\nAllow: /\nSitemap: ' + ORIGIN + '/sitemap.xml\n',
        '_headers.proposed': proposed_headers(plan),
        '_redirects.proposed': '/monitor-v3.html / 301\n/monitor-v3 / 301\n',
    }
    for name, text in artifacts.items():
        (drafts / name).write_text(text, encoding='utf-8')
    manifest.update({
        'purpose': 'INACTIVE_PUBLIC_RELEASE_PREPARATION', 'planned_origin': ORIGIN,
        'analytics_enabled': False, 'contact_email': CONTACT_EMAIL, 'contact_delivery_status': CONTACT_DELIVERY_STATUS,
        'publication_authorized': False, 'indexing_authorized': False,
        'blockers': plan['blockers'], 'activation_drafts_outside_document_root': True,
        'draft_files': {name: hashlib.sha256((drafts / name).read_bytes()).hexdigest()
                        for name in artifacts},
    })
    (output / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, help='new local directory, never a deployment target')
    args = parser.parse_args()
    manifest = prepare_release(args.output)
    print(f'PASS: {len(manifest["files"])} held preview files + 5 inactive drafts; no deployment')


if __name__ == '__main__':
    main()
