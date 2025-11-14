"""Minimal utility functions."""

import importlib.util
import json
import re
import unicodedata
from pathlib import Path
from typing import Dict, List, Optional


def get_all_scrapers() -> List[Dict]:
    """Get all scraper modules."""
    scrapers = []
    handlers_dir = Path('handlers')

    if not handlers_dir.exists():
        return []

    for scraper_file in handlers_dir.rglob('scraper.py'):
        org_dir = str(scraper_file.parent).replace('\\', '/')
        org_name = scraper_file.parent.name.replace('_', ' ').title()

        scrapers.append({
            'org_dir': org_dir,
            'name': org_name,
            'scraper_path': str(scraper_file)
        })

    return scrapers


def load_organization_data(org_dir: str) -> Optional[Dict]:
    """Load organization data from JSON file."""
    data_file = Path(org_dir) / 'data.json'

    if not data_file.exists():
        return None

    try:
        with open(data_file, 'r') as f:
            return json.load(f)
    except:
        return None


def get_scrape_statistics(org_dir: str) -> Dict:
    """Get scraping statistics for an organization."""
    org_path = Path(org_dir)

    if not org_path.exists():
        return {
            'org_dir': org_dir,
            'staff_count': 0,
            'last_scraped': None,
            'status': 'not_found'
        }

    # Count staff files
    staff_count = len(list(org_path.rglob('staff/**/*.json')))

    # Check for data.json
    data_file = org_path / 'data.json'
    last_scraped = None

    if data_file.exists():
        try:
            last_scraped = data_file.stat().st_mtime
        except:
            pass

    return {
        'org_dir': org_dir,
        'staff_count': staff_count,
        'last_scraped': last_scraped,
        'status': 'ok' if data_file.exists() else 'not_scraped'
    }


def load_scraper_module(org_dir: str):
    """Load scraper module dynamically."""
    scraper_path = Path(org_dir) / 'scraper.py'

    if not scraper_path.exists():
        return None

    try:
        spec = importlib.util.spec_from_file_location("scraper", scraper_path)
        if not spec or not spec.loader:
            return None

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except:
        return None


def normalize_name(name: Optional[str]) -> str:
    """
    Normalize names into filesystem-safe, slug-friendly tokens.

    Converts to lowercase ASCII, swaps ampersands for "and", replaces
    non-alphanumeric characters with underscores, and collapses repeats.
    """
    if not name:
        return "unknown"

    normalized = unicodedata.normalize('NFKD', str(name))
    ascii_name = normalized.encode('ascii', 'ignore').decode('ascii')
    ascii_name = ascii_name.replace('&', ' and ')

    slug = re.sub(r'[^a-z0-9]+', '_', ascii_name.lower())
    slug = re.sub(r'_+', '_', slug).strip('_')

    return slug or "unknown"


def clean_text(text: str) -> str:
    """Clean text by removing extra whitespace."""
    if not text:
        return ""
    return ' '.join(text.split())


def clean_phone(phone: str) -> str:
    """Clean phone number."""
    if not phone:
        return ""
    # Remove everything except digits, spaces, dashes, parentheses, plus
    return re.sub(r'[^0-9\s\-\(\)\+]', '', phone).strip()


def clean_email(email: str) -> str:
    """Clean email address."""
    if not email:
        return ""
    return email.strip().lower()
