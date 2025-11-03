"""
Person-Organization model.

Single Responsibility: Provide data access methods for person_organizations junction table.
"""

from typing import List, Optional, Dict, Any
from datetime import date
from ..base.repository import BaseRepository


class PersonOrganizationModel(BaseRepository):
    """
    Model for person-organization relationships.

    Links people to organizations with titles and date ranges.
    Supports many-to-many relationships.
    """

    def __init__(self, db):
        """
        Initialize person-organization model.

        Args:
            db: DatabaseConnection instance
        """
        super().__init__(db, 'person_organizations')

    def get_by_person(self, person_id: int, current_only: bool = False) -> List[Dict[str, Any]]:
        """
        Get all organizational affiliations for a person.

        Args:
            person_id: Person ID
            current_only: Only return current affiliations

        Returns:
            List of affiliation dicts with organization details
        """
        with self.db.get_cursor() as cur:
            if current_only:
                cur.execute("""
                    SELECT
                        po.*,
                        o.name as org_name,
                        o.slug as org_slug,
                        o.directory_path as org_directory_path,
                        o.hierarchy_level as org_hierarchy_level
                    FROM person_organizations po
                    JOIN organizations o ON po.organization_id = o.id
                    WHERE po.person_id = %s
                    AND po.is_current = TRUE
                    ORDER BY po.is_primary_affiliation DESC, po.start_date DESC;
                """, (person_id,))
            else:
                cur.execute("""
                    SELECT
                        po.*,
                        o.name as org_name,
                        o.slug as org_slug,
                        o.directory_path as org_directory_path,
                        o.hierarchy_level as org_hierarchy_level
                    FROM person_organizations po
                    JOIN organizations o ON po.organization_id = o.id
                    WHERE po.person_id = %s
                    ORDER BY po.is_current DESC, po.start_date DESC;
                """, (person_id,))
            return cur.fetchall()

    def get_by_organization(self, organization_id: int, current_only: bool = False) -> List[Dict[str, Any]]:
        """
        Get all people affiliated with an organization.

        Args:
            organization_id: Organization ID
            current_only: Only return current affiliations

        Returns:
            List of affiliation dicts with person details
        """
        with self.db.get_cursor() as cur:
            if current_only:
                cur.execute("""
                    SELECT
                        po.*,
                        p.first_name,
                        p.last_name,
                        p.middle_name,
                        p.preferred_name,
                        p.photo_url,
                        p.profile_url
                    FROM person_organizations po
                    JOIN people p ON po.person_id = p.id
                    WHERE po.organization_id = %s
                    AND po.is_current = TRUE
                    AND p.is_active = TRUE
                    ORDER BY po.title, p.last_name, p.first_name;
                """, (organization_id,))
            else:
                cur.execute("""
                    SELECT
                        po.*,
                        p.first_name,
                        p.last_name,
                        p.middle_name,
                        p.preferred_name,
                        p.photo_url,
                        p.profile_url
                    FROM person_organizations po
                    JOIN people p ON po.person_id = p.id
                    WHERE po.organization_id = %s
                    AND p.is_active = TRUE
                    ORDER BY po.is_current DESC, po.start_date DESC;
                """, (organization_id,))
            return cur.fetchall()

    def get_primary_affiliation(self, person_id: int) -> Optional[Dict[str, Any]]:
        """
        Get person's primary organizational affiliation.

        Args:
            person_id: Person ID

        Returns:
            Primary affiliation dict or None
        """
        with self.db.get_cursor() as cur:
            cur.execute("""
                SELECT
                    po.*,
                    o.name as org_name,
                    o.slug as org_slug,
                    o.directory_path as org_directory_path
                FROM person_organizations po
                JOIN organizations o ON po.organization_id = o.id
                WHERE po.person_id = %s
                AND po.is_primary_affiliation = TRUE
                AND po.is_current = TRUE
                LIMIT 1;
            """, (person_id,))
            return cur.fetchone()

    def search_by_title(self, title_query: str, organization_id: Optional[int] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Search affiliations by title.

        Args:
            title_query: Title search query
            organization_id: Optional filter by organization
            limit: Max results

        Returns:
            List of matching affiliations with person and org details
        """
        with self.db.get_cursor() as cur:
            if organization_id:
                cur.execute("""
                    SELECT
                        po.*,
                        p.first_name,
                        p.last_name,
                        o.name as org_name
                    FROM person_organizations po
                    JOIN people p ON po.person_id = p.id
                    JOIN organizations o ON po.organization_id = o.id
                    WHERE LOWER(po.title) LIKE LOWER(%s)
                    AND po.organization_id = %s
                    ORDER BY po.is_current DESC, p.last_name, p.first_name
                    LIMIT %s;
                """, (f'%{title_query}%', organization_id, limit))
            else:
                cur.execute("""
                    SELECT
                        po.*,
                        p.first_name,
                        p.last_name,
                        o.name as org_name
                    FROM person_organizations po
                    JOIN people p ON po.person_id = p.id
                    JOIN organizations o ON po.organization_id = o.id
                    WHERE LOWER(po.title) LIKE LOWER(%s)
                    ORDER BY po.is_current DESC, p.last_name, p.first_name
                    LIMIT %s;
                """, (f'%{title_query}%', limit))
            return cur.fetchall()

    def get_affiliations_in_date_range(
        self,
        start_date: date,
        end_date: date,
        organization_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get affiliations active during a date range.

        Args:
            start_date: Range start date
            end_date: Range end date
            organization_id: Optional filter by organization

        Returns:
            List of affiliations active during the period
        """
        with self.db.get_cursor() as cur:
            if organization_id:
                cur.execute("""
                    SELECT
                        po.*,
                        p.first_name,
                        p.last_name,
                        o.name as org_name
                    FROM person_organizations po
                    JOIN people p ON po.person_id = p.id
                    JOIN organizations o ON po.organization_id = o.id
                    WHERE po.organization_id = %s
                    AND (
                        (po.start_date IS NULL OR po.start_date <= %s)
                        AND (po.end_date IS NULL OR po.end_date >= %s)
                    )
                    ORDER BY p.last_name, p.first_name;
                """, (organization_id, end_date, start_date))
            else:
                cur.execute("""
                    SELECT
                        po.*,
                        p.first_name,
                        p.last_name,
                        o.name as org_name
                    FROM person_organizations po
                    JOIN people p ON po.person_id = p.id
                    JOIN organizations o ON po.organization_id = o.id
                    WHERE (
                        (po.start_date IS NULL OR po.start_date <= %s)
                        AND (po.end_date IS NULL OR po.end_date >= %s)
                    )
                    ORDER BY o.name, p.last_name, p.first_name;
                """, (end_date, start_date))
            return cur.fetchall()

    def upsert_affiliation(
        self,
        person_id: int,
        organization_id: int,
        title: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        **kwargs
    ) -> int:
        """
        Insert or update person-organization affiliation.

        Args:
            person_id: Person ID
            organization_id: Organization ID
            title: Job title/role
            start_date: Start date
            end_date: End date (None = current)
            **kwargs: Additional fields

        Returns:
            Affiliation ID
        """
        data = {
            'person_id': person_id,
            'organization_id': organization_id,
            'title': title,
            'start_date': start_date,
            'end_date': end_date,
            **kwargs
        }

        return self.upsert(
            unique_fields=['person_id', 'organization_id', 'start_date'],
            data=data
        )
