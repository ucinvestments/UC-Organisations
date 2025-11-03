"""
Compensation model.

Single Responsibility: Provide data access methods for compensation table.

Designed for UCLA salary JSON structure and public records data.
"""

from typing import List, Optional, Dict, Any
from decimal import Decimal
from ..base.repository import BaseRepository


class CompensationModel(BaseRepository):
    """
    Model for compensation/salary data.

    Stores annual compensation records from public sources.
    Designed to match UCLA salary JSON structure.
    """

    def __init__(self, db):
        """
        Initialize compensation model.

        Args:
            db: DatabaseConnection instance
        """
        super().__init__(db, 'compensation')

    def get_by_person(self, person_id: int, fiscal_year: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get compensation records for a person.

        Args:
            person_id: Person ID
            fiscal_year: Optional filter by fiscal year

        Returns:
            List of compensation records
        """
        with self.db.get_cursor() as cur:
            if fiscal_year:
                cur.execute("""
                    SELECT
                        c.*,
                        o.name as org_name,
                        o.slug as org_slug
                    FROM compensation c
                    LEFT JOIN organizations o ON c.organization_id = o.id
                    WHERE c.person_id = %s
                    AND c.fiscal_year = %s
                    ORDER BY c.fiscal_year DESC;
                """, (person_id, fiscal_year))
            else:
                cur.execute("""
                    SELECT
                        c.*,
                        o.name as org_name,
                        o.slug as org_slug
                    FROM compensation c
                    LEFT JOIN organizations o ON c.organization_id = o.id
                    WHERE c.person_id = %s
                    ORDER BY c.fiscal_year DESC;
                """, (person_id,))
            return cur.fetchall()

    def get_by_organization(
        self,
        organization_id: int,
        fiscal_year: Optional[int] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get compensation records for an organization.

        Args:
            organization_id: Organization ID
            fiscal_year: Optional filter by fiscal year
            limit: Optional max results

        Returns:
            List of compensation records with person details
        """
        with self.db.get_cursor() as cur:
            query = """
                SELECT
                    c.*,
                    p.first_name,
                    p.last_name
                FROM compensation c
                LEFT JOIN people p ON c.person_id = p.id
                WHERE c.organization_id = %s
            """
            params = [organization_id]

            if fiscal_year:
                query += " AND c.fiscal_year = %s"
                params.append(fiscal_year)

            query += " ORDER BY c.gross_pay DESC, c.fiscal_year DESC"

            if limit:
                query += " LIMIT %s"
                params.append(limit)

            cur.execute(query, params)
            return cur.fetchall()

    def get_by_source(
        self,
        source_employee_id: int,
        source_location: str,
        fiscal_year: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Get compensation record by source identifiers (for deduplication).

        Args:
            source_employee_id: Original employee ID from source
            source_location: Source location (e.g., "ASUCLA")
            fiscal_year: Optional fiscal year

        Returns:
            Compensation record or None
        """
        with self.db.get_cursor() as cur:
            if fiscal_year:
                cur.execute("""
                    SELECT * FROM compensation
                    WHERE source_employee_id = %s
                    AND source_location = %s
                    AND fiscal_year = %s
                    LIMIT 1;
                """, (source_employee_id, source_location, fiscal_year))
            else:
                cur.execute("""
                    SELECT * FROM compensation
                    WHERE source_employee_id = %s
                    AND source_location = %s
                    ORDER BY fiscal_year DESC
                    LIMIT 1;
                """, (source_employee_id, source_location))
            return cur.fetchone()

    def get_salary_statistics(
        self,
        organization_id: Optional[int] = None,
        fiscal_year: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get salary statistics (avg, median, min, max).

        Args:
            organization_id: Optional filter by organization
            fiscal_year: Optional filter by fiscal year

        Returns:
            Statistics dict
        """
        with self.db.get_cursor() as cur:
            query = """
                SELECT
                    COUNT(*) as count,
                    AVG(gross_pay) as avg_gross_pay,
                    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY gross_pay) as median_gross_pay,
                    MIN(gross_pay) as min_gross_pay,
                    MAX(gross_pay) as max_gross_pay,
                    AVG(total_compensation) as avg_total_comp,
                    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY total_compensation) as median_total_comp
                FROM compensation
                WHERE gross_pay IS NOT NULL
            """
            params = []

            if organization_id:
                query += " AND organization_id = %s"
                params.append(organization_id)

            if fiscal_year:
                query += " AND fiscal_year = %s"
                params.append(fiscal_year)

            cur.execute(query, params)
            return cur.fetchone() or {}

    def get_top_earners(
        self,
        organization_id: Optional[int] = None,
        fiscal_year: Optional[int] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get top earners by gross pay.

        Args:
            organization_id: Optional filter by organization
            fiscal_year: Optional filter by fiscal year
            limit: Max results

        Returns:
            List of compensation records with person details
        """
        with self.db.get_cursor() as cur:
            query = """
                SELECT
                    c.*,
                    p.first_name,
                    p.last_name,
                    o.name as org_name
                FROM compensation c
                LEFT JOIN people p ON c.person_id = p.id
                LEFT JOIN organizations o ON c.organization_id = o.id
                WHERE c.gross_pay IS NOT NULL
            """
            params = []

            if organization_id:
                query += " AND c.organization_id = %s"
                params.append(organization_id)

            if fiscal_year:
                query += " AND c.fiscal_year = %s"
                params.append(fiscal_year)

            query += " ORDER BY c.gross_pay DESC LIMIT %s"
            params.append(limit)

            cur.execute(query, params)
            return cur.fetchall()

    def search_by_title(
        self,
        title_query: str,
        organization_id: Optional[int] = None,
        fiscal_year: Optional[int] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Search compensation records by job title.

        Args:
            title_query: Title search query
            organization_id: Optional filter by organization
            fiscal_year: Optional filter by fiscal year
            limit: Max results

        Returns:
            List of matching compensation records
        """
        with self.db.get_cursor() as cur:
            query = """
                SELECT
                    c.*,
                    p.first_name,
                    p.last_name
                FROM compensation c
                LEFT JOIN people p ON c.person_id = p.id
                WHERE LOWER(c.title) LIKE LOWER(%s)
            """
            params = [f'%{title_query}%']

            if organization_id:
                query += " AND c.organization_id = %s"
                params.append(organization_id)

            if fiscal_year:
                query += " AND c.fiscal_year = %s"
                params.append(fiscal_year)

            query += " ORDER BY c.gross_pay DESC LIMIT %s"
            params.append(limit)

            cur.execute(query, params)
            return cur.fetchall()

    def get_salary_range(
        self,
        min_salary: Decimal,
        max_salary: Decimal,
        organization_id: Optional[int] = None,
        fiscal_year: Optional[int] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get compensation records within salary range.

        Args:
            min_salary: Minimum gross pay
            max_salary: Maximum gross pay
            organization_id: Optional filter by organization
            fiscal_year: Optional filter by fiscal year
            limit: Max results

        Returns:
            List of compensation records
        """
        with self.db.get_cursor() as cur:
            query = """
                SELECT
                    c.*,
                    p.first_name,
                    p.last_name
                FROM compensation c
                LEFT JOIN people p ON c.person_id = p.id
                WHERE c.gross_pay BETWEEN %s AND %s
            """
            params = [min_salary, max_salary]

            if organization_id:
                query += " AND c.organization_id = %s"
                params.append(organization_id)

            if fiscal_year:
                query += " AND c.fiscal_year = %s"
                params.append(fiscal_year)

            query += " ORDER BY c.gross_pay DESC LIMIT %s"
            params.append(limit)

            cur.execute(query, params)
            return cur.fetchall()

    def upsert_compensation(
        self,
        source_employee_id: int,
        source_location: str,
        fiscal_year: int,
        person_id: Optional[int] = None,
        organization_id: Optional[int] = None,
        base_pay: Optional[Decimal] = None,
        overtime_pay: Optional[Decimal] = None,
        gross_pay: Optional[Decimal] = None,
        **kwargs
    ) -> int:
        """
        Insert or update compensation record.

        Uses source_employee_id + source_location + fiscal_year as unique constraint.

        Args:
            source_employee_id: Original employee ID from source
            source_location: Source location (e.g., "ASUCLA")
            fiscal_year: Fiscal year
            person_id: Optional person ID
            organization_id: Optional organization ID
            base_pay: Base salary
            overtime_pay: Overtime pay
            gross_pay: Gross pay
            **kwargs: Additional fields

        Returns:
            Compensation ID
        """
        data = {
            'source_employee_id': source_employee_id,
            'source_location': source_location,
            'fiscal_year': fiscal_year,
            'person_id': person_id,
            'organization_id': organization_id,
            'base_pay': base_pay,
            'overtime_pay': overtime_pay,
            'gross_pay': gross_pay,
            **kwargs
        }

        return self.upsert(
            unique_fields=['source_employee_id', 'source_location', 'fiscal_year'],
            data=data
        )
