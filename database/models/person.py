"""
Person model.

Single Responsibility: Provide data access methods for people table.
"""

from typing import List, Optional, Dict, Any
from ..base.repository import BaseRepository


class PersonModel(BaseRepository):
    """
    Model for people.

    Stores individuals separate from their organizational relationships.
    Use PersonOrganizationModel for linking people to organizations.
    """

    def __init__(self, db):
        """
        Initialize person model.

        Args:
            db: DatabaseConnection instance
        """
        super().__init__(db, 'people')

    def find_by_name(
        self,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Find people by first and/or last name (case-insensitive, partial match).

        Args:
            first_name: Optional first name to search
            last_name: Optional last name to search
            limit: Max results

        Returns:
            List of matching people
        """
        with self.db.get_cursor() as cur:
            if first_name and last_name:
                cur.execute("""
                    SELECT * FROM people
                    WHERE LOWER(first_name) LIKE LOWER(%s)
                    AND LOWER(last_name) LIKE LOWER(%s)
                    ORDER BY last_name, first_name
                    LIMIT %s;
                """, (f'%{first_name}%', f'%{last_name}%', limit))
            elif first_name:
                cur.execute("""
                    SELECT * FROM people
                    WHERE LOWER(first_name) LIKE LOWER(%s)
                    ORDER BY last_name, first_name
                    LIMIT %s;
                """, (f'%{first_name}%', limit))
            elif last_name:
                cur.execute("""
                    SELECT * FROM people
                    WHERE LOWER(last_name) LIKE LOWER(%s)
                    ORDER BY last_name, first_name
                    LIMIT %s;
                """, (f'%{last_name}%', limit))
            else:
                return []

            return cur.fetchall()

    def search_full_text(self, query: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Full-text search across all name fields.

        Uses PostgreSQL full-text search index.

        Args:
            query: Search query
            limit: Max results

        Returns:
            List of matching people ordered by relevance
        """
        with self.db.get_cursor() as cur:
            cur.execute("""
                SELECT *,
                    ts_rank(
                        to_tsvector('english',
                            COALESCE(first_name, '') || ' ' ||
                            COALESCE(middle_name, '') || ' ' ||
                            COALESCE(last_name, '') || ' ' ||
                            COALESCE(preferred_name, '')
                        ),
                        plainto_tsquery('english', %s)
                    ) as relevance
                FROM people
                WHERE to_tsvector('english',
                    COALESCE(first_name, '') || ' ' ||
                    COALESCE(middle_name, '') || ' ' ||
                    COALESCE(last_name, '') || ' ' ||
                    COALESCE(preferred_name, '')
                ) @@ plainto_tsquery('english', %s)
                ORDER BY relevance DESC, last_name, first_name
                LIMIT %s;
            """, (query, query, limit))
            return cur.fetchall()

    def get_active_people(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get all active people.

        Args:
            limit: Optional max results

        Returns:
            List of active people
        """
        with self.db.get_cursor() as cur:
            if limit:
                cur.execute("""
                    SELECT * FROM people
                    WHERE is_active = TRUE
                    ORDER BY last_name, first_name
                    LIMIT %s;
                """, (limit,))
            else:
                cur.execute("""
                    SELECT * FROM people
                    WHERE is_active = TRUE
                    ORDER BY last_name, first_name;
                """)
            return cur.fetchall()

    def get_with_organizations(self, person_id: int) -> Optional[Dict[str, Any]]:
        """
        Get person with their organizational affiliations.

        Joins with person_organizations and organizations tables.

        Args:
            person_id: Person ID

        Returns:
            Person dict with 'affiliations' list
        """
        person = self.find_by_id(person_id)
        if not person:
            return None

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
                ORDER BY po.is_current DESC, po.start_date DESC;
            """, (person_id,))
            affiliations = cur.fetchall()

        person['affiliations'] = affiliations
        return person

    def get_with_compensation(self, person_id: int, fiscal_year: Optional[int] = None) -> Optional[Dict[str, Any]]:
        """
        Get person with their compensation records.

        Args:
            person_id: Person ID
            fiscal_year: Optional filter by fiscal year

        Returns:
            Person dict with 'compensation' list
        """
        person = self.find_by_id(person_id)
        if not person:
            return None

        with self.db.get_cursor() as cur:
            if fiscal_year:
                cur.execute("""
                    SELECT * FROM compensation
                    WHERE person_id = %s
                    AND fiscal_year = %s
                    ORDER BY fiscal_year DESC;
                """, (person_id, fiscal_year))
            else:
                cur.execute("""
                    SELECT * FROM compensation
                    WHERE person_id = %s
                    ORDER BY fiscal_year DESC;
                """, (person_id,))
            compensation = cur.fetchall()

        person['compensation'] = compensation
        return person

    def upsert_person(
        self,
        first_name: str,
        last_name: str,
        middle_name: Optional[str] = None,
        preferred_name: Optional[str] = None,
        **kwargs
    ) -> int:
        """
        Insert or update person by name.

        Note: This uses first_name + last_name as unique constraint,
        which may not be suitable for all use cases (name changes, duplicates).
        Consider adding additional unique identifiers if needed.

        Args:
            first_name: First name
            last_name: Last name
            middle_name: Optional middle name
            preferred_name: Optional preferred name
            **kwargs: Additional fields (bio, photo_url, etc.)

        Returns:
            Person ID
        """
        data = {
            'first_name': first_name,
            'last_name': last_name,
            'middle_name': middle_name,
            'preferred_name': preferred_name,
            **kwargs
        }

        return self.upsert(
            unique_fields=['first_name', 'last_name'],
            data=data
        )
