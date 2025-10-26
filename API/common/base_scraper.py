"""
Base scraper class providing common functionality for all UCOP organization scrapers.
"""

import os
import json
import time
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import requests
from bs4 import BeautifulSoup

from .utils import normalize_name, clean_text, clean_phone, clean_email


class BaseScraper(ABC):
    """Abstract base class for organization scrapers."""

    def __init__(self, org_name: str, org_dir: str, base_url: str):
        """
        Initialize the base scraper.

        Args:
            org_name: Full name of the organization
            org_dir: Directory name for the organization
            base_url: Base URL for the organization website
        """
        self.org_name = org_name
        self.org_dir = org_dir
        self.base_url = base_url
        self.base_path = Path(org_dir)

        # Setup logging
        self.setup_logging()

        # HTTP session with retry logic
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'UCOP-Scraper/1.0 (Educational Research)'
        })

        # Statistics
        self.stats = {
            'start_time': None,
            'end_time': None,
            'staff_scraped': 0,
            'errors': []
        }

    def setup_logging(self):
        """Setup logging for this scraper."""
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / f"{self.org_dir}.log"

        self.logger = logging.getLogger(self.org_dir)
        self.logger.setLevel(logging.INFO)

        # File handler
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.INFO)

        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def fetch_page(self, url: str, max_retries: int = 3, delay: int = 2) -> Optional[str]:
        """
        Fetch a webpage with retry logic.

        Args:
            url: URL to fetch
            max_retries: Maximum number of retry attempts
            delay: Delay between requests in seconds

        Returns:
            HTML content as string, or None if failed
        """
        for attempt in range(max_retries):
            try:
                self.logger.info(f"Fetching: {url} (attempt {attempt + 1}/{max_retries})")
                time.sleep(delay)  # Rate limiting

                response = self.session.get(url, timeout=10)
                response.raise_for_status()

                return response.text

            except requests.exceptions.RequestException as e:
                self.logger.error(f"Error fetching {url}: {e}")
                if attempt == max_retries - 1:
                    self.stats['errors'].append({
                        'url': url,
                        'error': str(e),
                        'timestamp': datetime.now().isoformat()
                    })
                    return None
                time.sleep(delay * (attempt + 1))  # Exponential backoff

        return None

    def parse_html(self, html: str) -> BeautifulSoup:
        """Parse HTML content with BeautifulSoup."""
        return BeautifulSoup(html, 'lxml')

    def create_directories(self):
        """Create necessary directory structure."""
        self.base_path.mkdir(exist_ok=True)
        staff_path = self.base_path / 'staff'
        staff_path.mkdir(exist_ok=True)
        self.logger.info(f"Created directory structure for {self.org_name}")

    def save_json(self, data: Dict, filepath: Path):
        """
        Save data to JSON file.

        Args:
            data: Dictionary to save
            filepath: Path to save to
        """
        try:
            filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Saved: {filepath}")
        except Exception as e:
            self.logger.error(f"Error saving {filepath}: {e}")
            self.stats['errors'].append({
                'file': str(filepath),
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })

    def save_staff_member(self, staff_data: Dict, department: str = None):
        """
        Save individual staff member JSON file.

        Args:
            staff_data: Staff member data dictionary
            department: Department subdirectory name
        """
        filename = normalize_name(staff_data['name']) + '.json'

        if department:
            dept_path = self.base_path / 'staff' / department
            dept_path.mkdir(parents=True, exist_ok=True)
            filepath = dept_path / filename
        else:
            filepath = self.base_path / 'staff' / filename

        self.save_json(staff_data, filepath)
        self.stats['staff_scraped'] += 1

    @abstractmethod
    def scrape_organization(self) -> Dict:
        """
        Scrape main organization page.

        Returns:
            Dictionary containing organization data
        """
        pass

    @abstractmethod
    def scrape_staff(self) -> List[Dict]:
        """
        Scrape staff directory pages.

        Returns:
            List of staff member dictionaries
        """
        pass

    def run(self):
        """Main execution method."""
        self.stats['start_time'] = datetime.now().isoformat()
        self.logger.info(f"Starting scraper for {self.org_name}")

        try:
            # Create directory structure
            self.create_directories()

            # Scrape organization data
            self.logger.info("Scraping organization data...")
            org_data = self.scrape_organization()

            if org_data:
                org_file = self.base_path / 'organization.json'
                self.save_json(org_data, org_file)

            # Scrape staff
            self.logger.info("Scraping staff data...")
            staff_list = self.scrape_staff()

            self.logger.info(f"Scraped {self.stats['staff_scraped']} staff members")

        except Exception as e:
            self.logger.error(f"Fatal error during scraping: {e}")
            self.stats['errors'].append({
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })

        finally:
            self.stats['end_time'] = datetime.now().isoformat()
            self.log_statistics()

    def log_statistics(self):
        """Log scraping statistics."""
        stats_file = self.base_path / 'scrape_stats.json'
        self.save_json(self.stats, stats_file)

        self.logger.info("=" * 50)
        self.logger.info(f"Scraping completed for {self.org_name}")
        self.logger.info(f"Staff scraped: {self.stats['staff_scraped']}")
        self.logger.info(f"Errors: {len(self.stats['errors'])}")
        self.logger.info("=" * 50)
