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
    site = output / 'site'
    site.mkdir(parents=True)
    try:
        for relative in files:
            target = site / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(web / relative, target)
        # The original root remains untouched; the candidate opens the current design.
        shutil.copyfile(site / 'monitor-v3.html', site / 'index.html')
        errors = validate_site(site)
        if errors:
            raise ValueError('candidate validation failed: ' + '; '.join(errors))
        html_files = list(site.rglob('*.html'))
        for page in html_files:
            if 'noindex' not in page.read_text():
                raise ValueError('candidate must remain noindex: ' + str(page.relative_to(site)))
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
