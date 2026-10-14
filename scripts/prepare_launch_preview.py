"""Build a separate local preview candidate; never deploy or approve product facts."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

from scripts.validate_local_site import validate_site

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / 'web'
ASSETS = (
    '404.html', 'information.html',
    'monitor-v3.html', 'monitor-v3.css', 'monitor-purpose.css', 'monitor-v3.js',
    'monitor-v3-data.js', 'monitor-value-format.js', 'monitor-search.js',
    'monitor-local-comments.js', 'monitor-local-comments.css',
    'monitor-review-links-data.js', 'monitor-review-links.css',
    'monitor-detail-v3.css', 'monitor-index.css',
    'monitor10-review.html', 'monitor10-review.css',
    'tech-news.html', 'tech-news.css', 'tech-news.js', 'tech-news-data.js',
    'product-news.js', 'product-news-data.js',
    'guides/monitor-buying.html', 'guides/monitor-buying.css',
)


def validate_display_artifacts(web):
    """Rebuild expected data in memory from validated originals; no source writes/network."""
    from scripts.build_monitor_v3 import serialized, load, SOURCE
    from scripts.build_monitor_review_links import build
    from scripts.tech_news import asset as news_asset, CACHE
    from scripts.product_news import asset as product_asset, DATA
    expected = {
        'monitor-v3-data.js': serialized(load(SOURCE))[1],
        'monitor-review-links-data.js': 'window.CONNECTABLE_REVIEW_LINKS = ' +
            json.dumps(build(), ensure_ascii=False).replace('<', '\\u003c') + ';\n',
        'tech-news-data.js': news_asset(json.loads(CACHE.read_text())),
        'product-news-data.js': product_asset(json.loads(DATA.read_text())),
    }
    for name, text in expected.items():
        if (web / name).read_bytes() != text.encode('utf-8'):
            raise ValueError('stale or altered generated display data: ' + name)


def prepare(output, web=WEB):
    """Only explicit current-site assets enter the candidate; legacy source stays intact."""
    output, web = Path(output).resolve(), Path(web).resolve()
    if output.exists():
        raise ValueError('output must be a new directory; existing files are never overwritten')
    if output == web or web in output.parents:
        raise ValueError('output must be outside the original web directory')
    errors = validate_site(web)
    if errors:
        raise ValueError('source validation failed: ' + '; '.join(errors))
    files = sorted(set(ASSETS) | {'monitors/index.html'} | {str(p.relative_to(web)) for p in (web / 'monitors').glob('*/index.html')})
    for relative in files:
        source = web / relative
        if not source.is_file() or source.is_symlink() or web not in source.resolve().parents:
            raise ValueError('missing or unsafe source: ' + relative)
    html_pages = [relative for relative in files if relative.endswith('.html')]
    errors = validate_site(web, html_pages)
    if errors:
        raise ValueError('full candidate source validation failed: ' + '; '.join(errors))
    validate_display_artifacts(web)
    site = output / 'site'
    site.mkdir(parents=True)
    try:
        for relative in files:
            target = site / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(web / relative, target)
        # The original root remains untouched; the candidate opens the current design.
        shutil.copyfile(site / 'monitor-v3.html', site / 'index.html')
        errors = validate_site(site, html_pages) + validate_site(site, ['index.html'])
        if errors:
            raise ValueError('candidate validation failed: ' + '; '.join(errors))
        validate_display_artifacts(site)
        manifest = {
            'purpose': 'LOCAL_PREVIEW_ONLY',
            'deployment_authorized': False,
            'domain': None,
            'entry': 'index.html',
            'source_entry': 'monitor-v3.html',
            'files': {str(p.relative_to(site)): hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in sorted(site.rglob('*')) if p.is_file()},
        }
        # Inventory is outside the document root, not another product-data source.
        (output / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    except Exception:
        shutil.rmtree(output)
        raise
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, help='new local directory outside web')
    args = parser.parse_args()
    manifest = prepare(args.output)
    print(f'PASS: local preview only; {len(manifest["files"])} files; no deployment')


if __name__ == '__main__':
    main()
