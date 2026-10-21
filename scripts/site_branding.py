"""Presentation metadata only; does not grant publication or factual approval."""
from html import escape

SITE_NAME = '모니픽'


def social_metadata(title, description):
    """Keep shares descriptive, without assigning an unapproved production URL."""
    values = (
        ('property', 'og:site_name', SITE_NAME),
        ('property', 'og:locale', 'ko_KR'),
        ('property', 'og:type', 'website'),
        ('property', 'og:title', title),
        ('property', 'og:description', description),
        ('name', 'twitter:card', 'summary'),
        ('name', 'twitter:title', title),
        ('name', 'twitter:description', description),
    )
    return '\n'.join(f'<meta {attr}="{key}" content="{escape(value, quote=True)}">'
                     for attr, key, value in values)
