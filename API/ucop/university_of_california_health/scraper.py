"""
Scraper for University of California Health organization.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from common.base_scraper import BaseScraper
from common.utils import clean_text, clean_phone, clean_email
from config import ORGANIZATIONS


class UCHealthScraper(BaseScraper):
    """Scraper for University of California Health."""

    def __init__(self):
        org_config = ORGANIZATIONS['ucop/university_of_california_health']
        super().__init__(
            org_name=org_config['name'],
            org_dir='ucop/university_of_california_health',
            base_url=org_config['main_url']
        )
        self.staff_urls = org_config['staff_urls']

    def scrape_organization(self):
        """Scrape main organization page."""
        html = self.fetch_page(self.base_url)
        if not html:
            return None

        soup = self.parse_html(html)
        org_data = {
            'name': self.org_name,
            'data_source': self.base_url,
            'description': '',
            'leadership': [],
            'sub_departments': [],
            'contact': {},
            'scraped_at': self.stats['start_time']
        }

        content_area = soup.find('div', class_='content') or soup.find('main')
        if content_area:
            paragraphs = content_area.find_all('p', limit=3)
            description_parts = [clean_text(p.get_text()) for p in paragraphs if p.get_text().strip()]
            org_data['description'] = ' '.join(description_parts[:2])

        return org_data

    def scrape_staff(self):
        """Scrape staff directory."""
        all_staff = []
        for department, url in self.staff_urls.items():
            html = self.fetch_page(url)
            if not html:
                continue
            soup = self.parse_html(html)
            staff_members = self.extract_staff_from_page(soup, department)
            for staff in staff_members:
                self.save_staff_member(staff, 'leadership')
                all_staff.append(staff)
        return all_staff

    def extract_staff_from_page(self, soup, department):
        """Extract staff members from a page."""
        staff_list = []
        headings = soup.find_all(['h3', 'h4'])
        for heading in headings:
            name = clean_text(heading.get_text())
            if not name or len(name) < 3:
                continue
            staff_data = {
                'name': name,
                'title': '',
                'department': 'Leadership',
                'organization': self.org_name,
                'contact': {},
                'data_source': self.staff_urls[department]
            }
            current = heading.next_sibling
            attempts = 0
            while current and attempts < 10:
                attempts += 1
                if hasattr(current, 'get_text'):
                    text = clean_text(current.get_text())
                    if '(' in text:
                        staff_data['contact']['phone'] = clean_phone(text)
                    if '@' in text:
                        staff_data['contact']['email'] = clean_email(text)
                    if not staff_data['title'] and text and '@' not in text and '(' not in text and len(text) > 10:
                        staff_data['title'] = text
                current = current.next_sibling
            if staff_data['title'] or staff_data['contact']:
                staff_list.append(staff_data)
        return staff_list


if __name__ == '__main__':
    scraper = UCHealthScraper()
    scraper.run()
