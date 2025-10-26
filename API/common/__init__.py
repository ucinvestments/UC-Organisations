"""
Common utilities and base classes for UCOP scrapers.
"""

from .base_scraper import BaseScraper
from .utils import (
    normalize_name,
    clean_text,
    clean_phone,
    clean_email,
    get_all_scrapers,
    load_organization_data,
    get_scrape_statistics
)

__all__ = [
    'BaseScraper',
    'normalize_name',
    'clean_text',
    'clean_phone',
    'clean_email',
    'get_all_scrapers',
    'load_organization_data',
    'get_scrape_statistics'
]
