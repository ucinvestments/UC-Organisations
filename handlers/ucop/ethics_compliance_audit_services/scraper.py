"""
Scraper for Ethics, Compliance and Audit Services organization.
"""

import sys
from pathlib import Path

# Add parent directory to path to import common modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from common.base_scraper import BaseScraper
from common.utils import clean_text, clean_phone, clean_email
from config import ORGANIZATIONS


class EthicsComplianceAuditScraper(BaseScraper):
    """Scraper for Ethics, Compliance and Audit Services."""

    def __init__(self):
        org_config = ORGANIZATIONS['handlers/ucop/ethics_compliance_audit_services']
        super().__init__(
            org_name=org_config['name'],
            org_dir='handlers/ucop/ethics_compliance_audit_services',
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

        # Extract description - typically in the first few paragraphs
        content_area = soup.find('div', class_='content') or soup.find('main')
        if content_area:
            paragraphs = content_area.find_all('p', limit=3)
            description_parts = [clean_text(p.get_text()) for p in paragraphs if p.get_text().strip()]
            org_data['description'] = ' '.join(description_parts[:2])

        # Extract sub-departments from staff URLs
        for dept_name in self.staff_urls.keys():
            if dept_name != 'main':
                org_data['sub_departments'].append({
                    'name': dept_name.replace('_', ' ').title()
                })

        return org_data

    def scrape_staff(self):
        """Scrape all staff directory pages."""
        all_staff = []

        for department, url in self.staff_urls.items():
            self.logger.info(f"Scraping {department} staff from {url}")

            html = self.fetch_page(url)
            if not html:
                continue

            soup = self.parse_html(html)
            staff_members = self.extract_staff_from_page(soup, department)

            for staff in staff_members:
                self.save_staff_member(staff, department if department != 'main' else None)
                all_staff.append(staff)

        return all_staff

    def extract_staff_from_page(self, soup, department):
        """Extract staff members from a page."""
        staff_list = []

        # Look for staff listings - they might be in various formats
        # Common pattern: staff info in sidebar or main content

        # Try to find staff entries - adjust selectors based on actual HTML structure
        # This is a generic approach that looks for common patterns

        # Method 1: Look for headings followed by contact info
        headings = soup.find_all(['h3', 'h4'])

        for heading in headings:
            name = clean_text(heading.get_text())

            # Skip if it's a section heading
            if not name or name.lower() in ['staff', 'contact', 'team']:
                continue

            # Get the next few siblings for contact info
            staff_data = {
                'name': name,
                'title': '',
                'department': department.replace('_', ' ').title() if department != 'main' else 'Staff',
                'organization': self.org_name,
                'contact': {},
                'data_source': self.staff_urls[department]
            }

            # Look for title, phone, email in next siblings
            current = heading.next_sibling
            attempts = 0

            while current and attempts < 10:
                attempts += 1

                if hasattr(current, 'get_text'):
                    text = clean_text(current.get_text())

                    # Extract phone
                    if 'phone' in text.lower() or '(' in text:
                        phone = clean_phone(text)
                        if phone:
                            staff_data['contact']['phone'] = phone

                    # Extract email
                    if '@' in text:
                        email = clean_email(text)
                        if email:
                            staff_data['contact']['email'] = email

                    # Extract title (usually the first text after name)
                    if not staff_data['title'] and text and '@' not in text and '(' not in text:
                        if len(text) > 10 and len(text) < 100:  # Reasonable title length
                            staff_data['title'] = text

                current = current.next_sibling

            # Only add if we got at least a title or contact info
            if staff_data['title'] or staff_data['contact']:
                staff_list.append(staff_data)

        return staff_list


if __name__ == '__main__':
    scraper = EthicsComplianceAuditScraper()
    scraper.run()
