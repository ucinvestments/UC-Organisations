"""
Utility functions for UCOP scrapers.
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Optional
import importlib.util


def normalize_name(name: str) -> str:
    """
    Convert a person's name to filename format.

    Args:
        name: Person's name (e.g., "John Doe", "Mary-Jane Smith, Ph.D.")

    Returns:
        Normalized filename (e.g., "john_doe", "mary_jane_smith")
    """
    # Remove titles and degrees
    name = re.sub(r',?\s+(Ph\.?D\.?|M\.?D\.?|J\.?D\.?|M\.?S\.?C\.?E\.?|Esq\.?)', '', name, flags=re.IGNORECASE)

    # Convert to lowercase and replace spaces/hyphens with underscores
    name = name.lower()
    name = re.sub(r'[^\w\s-]', '', name)  # Remove special characters
    name = re.sub(r'[-\s]+', '_', name)   # Replace spaces and hyphens with underscores

    return name.strip('_')


def clean_text(text: str) -> str:
    """
    Clean and normalize text content.

    Args:
        text: Raw text

    Returns:
        Cleaned text
    """
    if not text:
        return ""

    # Remove extra whitespace
    text = ' '.join(text.split())

    # Remove special characters but keep common punctuation
    text = text.strip()

    return text


def clean_phone(phone: str) -> str:
    """
    Clean and normalize phone numbers.

    Args:
        phone: Raw phone number

    Returns:
        Cleaned phone number in (XXX) XXX-XXXX format
    """
    if not phone:
        return ""

    # Extract digits only
    digits = re.sub(r'\D', '', phone)

    # Format if we have 10 digits
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"

    # Return as-is if not standard format
    return phone.strip()


def clean_email(email: str) -> str:
    """
    Clean and validate email addresses.

    Args:
        email: Raw email address

    Returns:
        Cleaned email or empty string if invalid
    """
    if not email:
        return ""

    email = email.strip().lower()

    # Basic email validation
    if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return email

    return ""


def decode_protected_email(js_code: str) -> Optional[str]:
    """
    Decode JavaScript-protected email addresses.
    Many UCOP pages use protectAddress() function to obfuscate emails.

    Args:
        js_code: JavaScript code containing email

    Returns:
        Decoded email address or None
    """
    # This is a placeholder - actual implementation would need to parse
    # the specific JavaScript obfuscation used by UCOP
    # For now, look for common patterns
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', js_code)
    if email_match:
        return email_match.group(0)

    return None


def get_all_scrapers() -> List[Dict[str, str]]:
    """
    Discover all scraper.py files in organization directories.
    Supports multi-level organization structure:
    - handlers/ucop/*/scraper.py (UCOP organizations)
    - handlers/academic_senate/scraper.py
    - handlers/board_of_regents/scraper.py
    - handlers/campuses/*/scraper.py
    - handlers/labs/*/scraper.py

    Returns:
        List of dicts with scraper information
    """
    scrapers = []
    base_path = Path('handlers')

    # Define organization categories that contain subdirectories
    multi_level_orgs = ['ucop', 'campuses', 'labs']

    # Define single-level organizations
    single_level_orgs = ['academic_senate', 'board_of_regents']

    # Search in multi-level organization directories
    for org_category in multi_level_orgs:
        category_path = base_path / org_category
        if category_path.exists() and category_path.is_dir():
            for item in category_path.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    scraper_file = item / 'scraper.py'
                    if scraper_file.exists():
                        org_path = f"handlers/{org_category}/{item.name}"
                        scrapers.append({
                            'org_dir': org_path,
                            'scraper_path': str(scraper_file),
                            'name': f"{org_category.upper()}: {item.name.replace('_', ' ').title()}"
                        })

    # Search in single-level organization directories
    for org_name in single_level_orgs:
        org_path = base_path / org_name
        if org_path.exists() and org_path.is_dir():
            scraper_file = org_path / 'scraper.py'
            if scraper_file.exists():
                scrapers.append({
                    'org_dir': f"handlers/{org_name}",
                    'scraper_path': str(scraper_file),
                    'name': org_name.replace('_', ' ').title()
                })

    return sorted(scrapers, key=lambda x: x['name'])


def load_organization_data(org_dir: str) -> Optional[Dict]:
    """
    Load organization data from JSON file.

    Args:
        org_dir: Organization directory name

    Returns:
        Organization data dict or None if not found
    """
    org_file = Path(org_dir) / 'organization.json'

    if not org_file.exists():
        return None

    try:
        with open(org_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {org_file}: {e}")
        return None


def get_scrape_statistics(org_dir: str) -> Dict:
    """
    Get scraping statistics for an organization.

    Args:
        org_dir: Organization directory name

    Returns:
        Statistics dictionary
    """
    stats = {
        'org_dir': org_dir,
        'has_organization_file': False,
        'staff_count': 0,
        'departments': [],
        'last_scraped': None
    }

    org_path = Path(org_dir)

    # Check for organization.json
    org_file = org_path / 'organization.json'
    stats['has_organization_file'] = org_file.exists()

    # Count staff files
    staff_path = org_path / 'staff'
    if staff_path.exists():
        staff_files = list(staff_path.rglob('*.json'))
        stats['staff_count'] = len(staff_files)

        # Get departments
        departments = set()
        for f in staff_files:
            if f.parent != staff_path:
                departments.add(f.parent.name)
        stats['departments'] = sorted(list(departments))

    # Get last scrape time
    scrape_stats = org_path / 'scrape_stats.json'
    if scrape_stats.exists():
        try:
            with open(scrape_stats, 'r', encoding='utf-8') as f:
                scrape_data = json.load(f)
                stats['last_scraped'] = scrape_data.get('end_time')
                stats['last_scrape_stats'] = scrape_data
        except Exception:
            pass

    return stats


def load_scraper_module(org_dir: str):
    """
    Dynamically load a scraper module.

    Args:
        org_dir: Organization directory name

    Returns:
        Loaded module or None
    """
    scraper_path = Path(org_dir) / 'scraper.py'

    if not scraper_path.exists():
        return None

    try:
        spec = importlib.util.spec_from_file_location(f"{org_dir}.scraper", scraper_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        print(f"Error loading scraper for {org_dir}: {e}")
        return None
