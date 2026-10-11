"""Offline guards for the modern local preview; not a publication approval.

Only explicit HTML href/src references are checked. Runtime DOM, CSS imports,
external URL reachability, privacy and factual accuracy require other checks.
"""
import argparse
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1] / 'web'
ENTRY_PAGES = ('monitor-v3.html', 'monitors/index.html', 'guides/monitor-buying.html', 'tech-news.html')


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.lang = None
        self.meta = {}
        self.ids = set()
        self.duplicate_ids = set()
        self.links = []
        self.canonicals = []
        self.titles = []
        self.jsonld = []
        self._capture = None
        self._parts = []
        self.feed(text)
        self.close()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'html':
            self.lang = attrs.get('lang', '')
        if tag == 'meta':
            self.meta.setdefault(attrs.get('name', '').lower(), []).append(attrs.get('content', ''))
        if attrs.get('id'):
            value = attrs['id']
            if value in self.ids:
                self.duplicate_ids.add(value)
            self.ids.add(value)
        if tag == 'a' and attrs.get('name'):
            self.ids.add(attrs['name'])
        if tag == 'base':
            self.links.append(('base', attrs.get('href', '')))
        elif tag in ('a', 'link', 'area') and 'href' in attrs:
            self.links.append((tag, attrs['href'] or ''))
        if 'src' in attrs:
            self.links.append((tag, attrs['src'] or ''))
        if tag == 'link' and 'canonical' in attrs.get('rel', '').lower().split():
            self.canonicals.append(attrs.get('href', ''))
        if tag == 'title' or (tag == 'script' and attrs.get('type', '').lower() == 'application/ld+json'):
            self._capture, self._parts = tag, []

    def handle_data(self, data):
        if self._capture:
            self._parts.append(data)

    def handle_endtag(self, tag):
        if tag == self._capture:
            target = self.titles if tag == 'title' else self.jsonld
            target.append(''.join(self._parts).strip())
            self._capture = None


def forbidden_schema(value):
    if isinstance(value, dict):
        for key, child in value.items():
            if key.lower() in ('offers', 'aggregaterating', 'review', 'reviewrating'):
                yield key
            if key == '@type':
                types = child if isinstance(child, list) else [child]
                for type_name in types:
                    if not isinstance(type_name, str):
                        continue
                    normalized = type_name
                    for prefix in ('https://schema.org/', 'http://schema.org/'):
                        if normalized.startswith(prefix):
                            normalized = normalized[len(prefix):]
                            break
                    if normalized in ('AggregateRating', 'Rating', 'Offer', 'AggregateOffer', 'Review'):
                        yield f'@type {type_name}'
            yield from forbidden_schema(child)
    elif isinstance(value, list):
        for child in value:
            yield from forbidden_schema(child)


def validate_site(root=ROOT, pages=None):
    root = Path(root).resolve()
    pages = list(pages) if pages is not None else [*ENTRY_PAGES, *sorted(str(p.relative_to(root)) for p in (root / 'monitors').glob('*/index.html'))]
    errors, docs, titles, descriptions = [], {}, {}, {}

    def issue(page, message):
        errors.append(f'{page}: {message}')

    def read(path):
        if path not in docs:
            docs[path] = Document(path.read_text(encoding='utf-8'))
        return docs[path]

    for page in pages:
        path = (root / page).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            issue(page, 'missing page or path outside document root')
            continue
        try:
            doc = read(path)
        except (OSError, UnicodeError) as exc:
            issue(page, f'unreadable HTML: {exc}')
            continue
        if not doc.lang or doc.lang.lower().split('-')[0] != 'ko':
            issue(page, 'Korean html lang required')
        viewport = doc.meta.get('viewport', [])
        if len(viewport) != 1 or 'width=device-width' not in viewport[0].replace(' ', '').lower():
            issue(page, 'one responsive viewport required')
        robots = doc.meta.get('robots', [])
        tokens = {word for value in robots for word in value.lower().replace(',', ' ').split()}
        if not robots or not tokens.intersection({'noindex', 'none'}) or 'index' in tokens or 'all' in tokens:
            issue(page, 'local preview must preserve unambiguous noindex')
        for label, values, seen in (('title', doc.titles, titles), ('description', doc.meta.get('description', []), descriptions)):
            if len(values) != 1 or not values[0].strip():
                issue(page, f'exactly one nonempty {label} required')
            else:
                normalized = ' '.join(values[0].split()).casefold()
                if normalized in seen:
                    issue(page, f'duplicate {label} with {seen[normalized]}')
                seen[normalized] = page
        if doc.canonicals:
            issue(page, 'canonical deferred until approved production URL exists')
        if doc.duplicate_ids:
            issue(page, f'duplicate HTML ids: {sorted(doc.duplicate_ids)}')
        for payload in doc.jsonld:
            try:
                data = json.loads(payload)
                for field in sorted(set(forbidden_schema(data))):
                    issue(page, f'publication-gated structured data: {field}')
            except ValueError:
                issue(page, 'invalid JSON-LD')
        for tag, href in doc.links:
            if tag == 'base':
                issue(page, 'base element not supported in local preview')
                continue
            if any(ord(char) < 32 for char in href) or '\\' in href:
                issue(page, f'unsafe link syntax: {href!r}')
                continue
            try:
                url = urlsplit(href)
            except ValueError:
                issue(page, f'invalid URL: {href!r}')
                continue
            if url.scheme and url.scheme not in ('http', 'https', 'mailto', 'tel'):
                issue(page, f'unsupported URL scheme: {url.scheme}')
                continue
            if url.scheme or url.netloc:
                continue  # Allowed external schemes/protocol-relative URLs; no fetch.
            decoded = unquote(url.path)
            if '\\' in decoded or any(ord(char) < 32 for char in decoded):
                issue(page, f'unsafe decoded path: {href!r}')
                continue
            target = (root / decoded.lstrip('/') if decoded.startswith('/') else path.parent / decoded).resolve() if decoded else path
            if not target.is_relative_to(root):
                issue(page, f'link escapes document root: {href!r}')
                continue
            if target.is_dir():
                target = (target / 'index.html').resolve()
            if not target.is_relative_to(root):
                issue(page, f'link escapes document root: {href!r}')
                continue
            if not target.is_file():
                issue(page, f'missing local target: {href!r}')
                continue
            if url.fragment and target.suffix.lower() in ('.html', '.htm'):
                fragment = unquote(url.fragment)
                try:
                    if fragment not in read(target).ids:
                        issue(page, f'missing fragment: {href!r}')
                except (OSError, UnicodeError):
                    issue(page, f'unreadable fragment target: {href!r}')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    errors = validate_site(args.root)
    if errors:
        print('\n'.join(errors))
        return 1
    print('PASS: modern local preview metadata, HTML references and publication guards (offline)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
