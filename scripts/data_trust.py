"""Bounded identity and official-URL checks. No network or fact approval.

Host/route entries are reviewed policy, not substring/domain-family inference.
Unknown aliases, SKUs, hosts and redirect destinations never become approvals.
"""
import re
from urllib.parse import parse_qsl, unquote, urlsplit

# Only known product/support publishers; unknown CDNs require separate review.
OFFICIAL_ROUTES = {
    'Dell': {
        'www.dell.com': r'^/(?:[a-z]{2}-[a-z]{2}/shop/|support/)',
        'dl.dell.com': r'^/content/',
    },
    'LG': {'www.lg.com': r'^/[a-z]{2}/(?:monitors/|monitori/|monitores/|support/)'},
    '주연테크': {'www.jooyon.co.kr': r'^/bbs/board\.php$'},
    '크로스오버': {
        'www.crosslcd.co.kr': r'^/shop/item\.php$',
        'crosslcd.co.kr': r'^/shop/item\.php$',
    },
    'MSI': {'www.msi.com': r'^/(?:Business-Productivity-Monitor/|support/)'},
}
ROUTE_QUERY_KEYS = {
    '주연테크': {'bo_table', 'page', 'wr_id'},
    '크로스오버': {'it_id'},
    'Dell': {'language'},
    'LG': set(),
    'MSI': set(),
}

# Already directly checked labels in monitor-batch-1 review_links. This is an
# explicit label crosswalk, not a rule to strip manufacturers or SKU suffixes.
# Adding any label requires source-backed review; variant_match remains UNKNOWN.
REVIEWED_MODEL_LABELS = {
    ('주연테크', 'V32UE'): {'V32UE', '주연테크 V32UE'},
    ('크로스오버', '27ULD950'): {'27ULD950', '크로스오버 27ULD950'},
    ('MSI', 'MD271UL'): {'MD271UL', 'MSI MD271UL'},
}


def linked_model_identity(manufacturer, target_model, *labels):
    allowed = REVIEWED_MODEL_LABELS.get((manufacturer, target_model), {target_model})
    if not labels or any(model_identity(label, label) != 'EXACT_MODEL_LABEL' or label not in allowed for label in labels):
        return 'MANUAL_REVIEW'
    return 'EXACT_MODEL_LABEL'


def model_identity(*labels):
    """Literal agreement only; no case/space/suffix/alias/SKU guessing."""
    if (len(labels) < 2 or any(not isinstance(x, str) or not x.strip()
                              or x != x.strip() or x == 'UNKNOWN' for x in labels)):
        return 'MANUAL_REVIEW'
    return 'EXACT_MODEL_LABEL' if len(set(labels)) == 1 else 'MANUAL_REVIEW'


def official_url_status(url, manufacturer):
    """A narrow URL authority policy, not a live redirect/content verifier."""
    try:
        if not isinstance(url, str) or any(c.isspace() or ord(c) < 32 or ord(c) == 127 for c in url) or '\\' in url:
            return 'UNKNOWN'
        u = urlsplit(url)
        route = OFFICIAL_ROUTES.get(manufacturer, {}).get(u.hostname)
        if (u.scheme != 'https' or u.username or u.password or u.port not in (None, 443)
                or not route or u.fragment):
            return 'UNKNOWN'
        # Encoded separators/dot segments can change routing after browser decoding.
        path = unquote(u.path, errors='strict')
        if (re.search(r'(?i)%(?:2f|5c|2e|3f|23|25)|%(?![0-9a-f]{2})', u.path)
                or any(p in ('.', '..') for p in path.split('/')) or not re.search(route, path)):
            return 'UNKNOWN'
        if any(c.isspace() or ord(c) < 32 or ord(c) == 127 for c in path):
            return 'UNKNOWN'
        if re.search(r'(?i)(?:^|/)(?:redirect|redir|out|go|url|away)(?:[./]|$)', path):
            return 'UNKNOWN'
        if u.query and (any(not part or '=' not in part for part in u.query.split('&'))
                        or re.search(r'%(?![0-9A-Fa-f]{2})', u.query)):
            return 'UNKNOWN'
        query = parse_qsl(u.query, keep_blank_values=True, strict_parsing=True, errors='strict')
        keys = [k for k, _ in query]
        if len(keys) != len(set(keys)) or not set(keys) <= ROUTE_QUERY_KEYS[manufacturer]:
            return 'UNKNOWN'
        values = dict(query)
        if manufacturer == 'Dell' and 'language' in values and not re.fullmatch(r'[a-z]{2}(?:-[a-z]{2})?', values['language']):
            return 'UNKNOWN'
        if manufacturer == '주연테크' and (values.get('bo_table') != 'press'
                or not re.fullmatch(r'[0-9]+', values.get('wr_id', ''))
                or ('page' in values and not re.fullmatch(r'[0-9]+', values['page']))):
            return 'UNKNOWN'
        if manufacturer == '크로스오버' and not re.fullmatch(r'[0-9]+', values.get('it_id', '')):
            return 'UNKNOWN'
        for _, value in query:
            decoded = value
            for _ in range(3):
                decoded = unquote(decoded)
            if re.search(r'(?i)(?:https?:|//|\\)', decoded):
                return 'UNKNOWN'
        return 'OFFICIAL_URL_SCOPE'
    except (TypeError, ValueError, UnicodeError):
        return 'UNKNOWN'


def require_official_source(source, manufacturer, path):
    """Check source URL and any recorded redirect chain/final URL, without I/O.

Legacy DIRECT_CHECK records contain no chain. Do not fabricate one or claim
that this offline check verifies their current HTTP destination.
"""
    urls = [source.get('url')]
    if 'redirect_chain' in source:
        chain = source['redirect_chain']
        if not isinstance(chain, list) or not chain:
            raise ValueError(f'{path}: UNKNOWN official redirect chain; manual review required')
        urls.extend(chain)
    if 'final_url' in source:
        urls.append(source['final_url'])
    if any(official_url_status(u, manufacturer) != 'OFFICIAL_URL_SCOPE' for u in urls):
        raise ValueError(f'{path}: UNKNOWN manufacturer URL authority/redirect; manual review required')
