"""
Analytics repository for complex cross-table queries.

Single Responsibility: Complex analytical queries across multiple tables.

Models handle single-table operations.
This repository handles multi-table analytics and aggregations.
"""

from typing import List, Dict, Any, Optional
from decimal import Decimal


class AnalyticsRepository:
    """
    Repository for complex analytical queries.

    Provides insights across organizations, people, and compensation.
    """

    def __init__(self, db):
        """
        Initialize analytics repository.

        Args:
            db: DatabaseConnection instance
        """
        self.db = db

    def get_organization_overview(self, organization_id: int, fiscal_year: Optional[int] = None) -> Dict[str, Any]:
        """
        Get comprehensive overview of an organization.

        Includes:
        - Organization details with hierarchy
        - Employee count
        - Compensation statistics
        - Department count (if parent org)

        Args:
            organization_id: Organization ID
            fiscal_year: Optional fiscal year for compensation stats

        Returns:
            Overview dict
        """
        with self.db.get_cursor() as cur:
            # Get organization details
            cur.execute("""
                SELECT
                    o.*,
                    c.name as category_name,
                    c.slug as category_slug,
                    parent.name as parent_name
                FROM organizations o
                LEFT JOIN categories c ON o.category_id = c.id
                LEFT JOIN organizations parent ON o.parent_id = parent.id
                WHERE o.id = %s;
            """, (organization_id,))
            org = cur.fetchone()

            if not org:
                return {}

            # Get current employee count
            cur.execute("""
                SELECT COUNT(*) as employee_count
                FROM person_organizations
                WHERE organization_id = %s
                AND is_current = TRUE;
            """, (organization_id,))
            employee_data = cur.fetchone()
            org['current_employee_count'] = employee_data['employee_count'] if employee_data else 0

            # Get compensation stats for fiscal year
            comp_query = """
                SELECT
                    COUNT(*) as compensation_records,
                    AVG(gross_pay) as avg_salary,
                    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY gross_pay) as median_salary,
                    MIN(gross_pay) as min_salary,
                    MAX(gross_pay) as max_salary,
                    SUM(gross_pay) as total_payroll
                FROM compensation
                WHERE organization_id = %s
                AND gross_pay IS NOT NULL
            """
            params = [organization_id]

            if fiscal_year:
                comp_query += " AND fiscal_year = %s"
                params.append(fiscal_year)

            cur.execute(comp_query, params)
            comp_stats = cur.fetchone()
            org['compensation_stats'] = comp_stats or {}

            # Get department count (children)
            cur.execute("""
                SELECT COUNT(*) as department_count
                FROM organizations
                WHERE parent_id = %s
                AND is_active = TRUE;
            """, (organization_id,))
            dept_data = cur.fetchone()
            org['department_count'] = dept_data['department_count'] if dept_data else 0

            return org

    def get_compensation_trends(
        self,
        organization_id: Optional[int] = None,
        start_year: Optional[int] = None,
        end_year: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get compensation trends over time.

        Args:
            organization_id: Optional filter by organization
            start_year: Optional start fiscal year
            end_year: Optional end fiscal year

        Returns:
            List of yearly statistics
        """
        with self.db.get_cursor() as cur:
            query = """
                SELECT
                    fiscal_year,
                    COUNT(*) as employee_count,
                    AVG(gross_pay) as avg_salary,
                    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY gross_pay) as median_salary,
                    MIN(gross_pay) as min_salary,
                    MAX(gross_pay) as max_salary,
                    SUM(gross_pay) as total_payroll
                FROM compensation
                WHERE gross_pay IS NOT NULL
            """
            params = []

            if organization_id:
                query += " AND organization_id = %s"
                params.append(organization_id)

            if start_year:
                query += " AND fiscal_year >= %s"
                params.append(start_year)

            if end_year:
                query += " AND fiscal_year <= %s"
                params.append(end_year)

            query += " GROUP BY fiscal_year ORDER BY fiscal_year;"

            cur.execute(query, params)
            return cur.fetchall()

    def get_salary_distribution(
        self,
        organization_id: Optional[int] = None,
        fiscal_year: Optional[int] = None,
        bin_size: Decimal = Decimal('10000')
    ) -> List[Dict[str, Any]]:
        """
        Get salary distribution in bins.

        Args:
            organization_id: Optional filter by organization
            fiscal_year: Optional filter by fiscal year
            bin_size: Size of salary bins (default $10,000)

        Returns:
            List of bins with counts
        """
        with self.db.get_cursor() as cur:
            query = """
                SELECT
                    FLOOR(gross_pay / %s) * %s as salary_bin_start,
                    (FLOOR(gross_pay / %s) + 1) * %s as salary_bin_end,
                    COUNT(*) as count
                FROM compensation
                WHERE gross_pay IS NOT NULL
            """
            params = [bin_size, bin_size, bin_size, bin_size]

            if organization_id:
                query += " AND organization_id = %s"
                params.append(organization_id)

            if fiscal_year:
                query += " AND fiscal_year = %s"
                params.append(fiscal_year)

            query += """
                GROUP BY FLOOR(gross_pay / %s)
                ORDER BY salary_bin_start;
            """
            params.append(bin_size)

            cur.execute(query, params)
            return cur.fetchall()

    def get_top_titles_by_count(
        self,
        organization_id: Optional[int] = None,
        fiscal_year: Optional[int] = None,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Get most common job titles.

        Args:
            organization_id: Optional filter by organization
            fiscal_year: Optional filter by fiscal year
            limit: Max results

        Returns:
            List of titles with counts and avg salary
        """
        with self.db.get_cursor() as cur:
            query = """
                SELECT
                    title,
                    COUNT(*) as employee_count,
                    AVG(gross_pay) as avg_salary,
                    MIN(gross_pay) as min_salary,
                    MAX(gross_pay) as max_salary
                FROM compensation
                WHERE title IS NOT NULL
                AND gross_pay IS NOT NULL
            """
            params = []

            if organization_id:
                query += " AND organization_id = %s"
                params.append(organization_id)

            if fiscal_year:
                query += " AND fiscal_year = %s"
                params.append(fiscal_year)

            query += """
                GROUP BY title
                ORDER BY employee_count DESC
                LIMIT %s;
            """
            params.append(limit)

            cur.execute(query, params)
            return cur.fetchall()

    def get_organization_hierarchy_with_stats(
        self,
        root_organization_id: int,
        fiscal_year: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get full organization hierarchy with employee/salary stats.

        Uses recursive CTE to traverse hierarchy.

        Args:
            root_organization_id: Root organization ID
            fiscal_year: Optional fiscal year for stats

        Returns:
            List of organizations with stats
        """
        with self.db.get_cursor() as cur:
            # Build the query
            query = """
                WITH RECURSIVE org_hierarchy AS (
                    -- Base case: root organization
                    SELECT
                        id,
                        parent_id,
                        name,
                        slug,
                        hierarchy_level,
                        full_path,
                        ARRAY[id] as path_ids
                    FROM organizations
                    WHERE id = %s

                    UNION ALL

                    -- Recursive case: children
                    SELECT
                        o.id,
                        o.parent_id,
                        o.name,
                        o.slug,
                        o.hierarchy_level,
                        o.full_path,
                        oh.path_ids || o.id
                    FROM organizations o
                    INNER JOIN org_hierarchy oh ON o.parent_id = oh.id
                    WHERE o.is_active = TRUE
                )
                SELECT
                    oh.*,
                    COUNT(DISTINCT po.person_id) as current_employee_count,
                    COUNT(DISTINCT c.id) as compensation_record_count,
                    AVG(c.gross_pay) as avg_salary,
                    SUM(c.gross_pay) as total_payroll
                FROM org_hierarchy oh
                LEFT JOIN person_organizations po ON oh.id = po.organization_id AND po.is_current = TRUE
                LEFT JOIN compensation c ON oh.id = c.organization_id
            """

            params = [root_organization_id]

            if fiscal_year:
                query += " AND c.fiscal_year = %s"
                params.append(fiscal_year)

            query += """
                GROUP BY oh.id, oh.parent_id, oh.name, oh.slug, oh.hierarchy_level, oh.full_path, oh.path_ids
                ORDER BY oh.hierarchy_level, oh.name;
            """

            cur.execute(query, params)
            return cur.fetchall()

    def get_person_career_timeline(self, person_id: int) -> Dict[str, Any]:
        """
        Get complete career timeline for a person.

        Includes all affiliations and compensation records.

        Args:
            person_id: Person ID

        Returns:
            Dict with person info, affiliations timeline, compensation timeline
        """
        with self.db.get_cursor() as cur:
            # Get person details
            cur.execute("""
                SELECT * FROM people WHERE id = %s;
            """, (person_id,))
            person = cur.fetchone()

            if not person:
                return {}

            # Get affiliations timeline
            cur.execute("""
                SELECT
                    po.*,
                    o.name as org_name,
                    o.slug as org_slug,
                    o.hierarchy_level,
                    parent.name as parent_org_name
                FROM person_organizations po
                JOIN organizations o ON po.organization_id = o.id
                LEFT JOIN organizations parent ON o.parent_id = parent.id
                WHERE po.person_id = %s
                ORDER BY po.start_date DESC NULLS LAST;
            """, (person_id,))
            affiliations = cur.fetchall()

            # Get compensation timeline
            cur.execute("""
                SELECT
                    c.*,
                    o.name as org_name
                FROM compensation c
                LEFT JOIN organizations o ON c.organization_id = o.id
                WHERE c.person_id = %s
                ORDER BY c.fiscal_year DESC;
            """, (person_id,))
            compensation = cur.fetchall()

            return {
                'person': person,
                'affiliations': affiliations,
                'compensation_history': compensation
            }

    def search_people_with_context(
        self,
        query: str,
        organization_id: Optional[int] = None,
        title_query: Optional[str] = None,
        min_salary: Optional[Decimal] = None,
        max_salary: Optional[Decimal] = None,
        fiscal_year: Optional[int] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Advanced people search with organizational and compensation context.

        Args:
            query: Name search query
            organization_id: Optional filter by organization
            title_query: Optional filter by title
            min_salary: Optional minimum salary
            max_salary: Optional maximum salary
            fiscal_year: Optional fiscal year for salary filters
            limit: Max results

        Returns:
            List of people with current affiliation and compensation
        """
        with self.db.get_cursor() as cur:
            sql = """
                SELECT DISTINCT
                    p.*,
                    po.title as current_title,
                    o.name as current_org_name,
                    o.id as current_org_id,
                    c.gross_pay as current_salary,
                    c.fiscal_year as salary_year
                FROM people p
                LEFT JOIN person_organizations po ON p.id = po.person_id AND po.is_current = TRUE
                LEFT JOIN organizations o ON po.organization_id = o.id
                LEFT JOIN compensation c ON p.id = c.person_id
                WHERE p.is_active = TRUE
                AND (
                    LOWER(p.first_name) LIKE LOWER(%s)
                    OR LOWER(p.last_name) LIKE LOWER(%s)
                    OR to_tsvector('english',
                        COALESCE(p.first_name, '') || ' ' ||
                        COALESCE(p.last_name, '')
                    ) @@ plainto_tsquery('english', %s)
                )
            """
            params = [f'%{query}%', f'%{query}%', query]

            if organization_id:
                sql += " AND po.organization_id = %s"
                params.append(organization_id)

            if title_query:
                sql += " AND LOWER(po.title) LIKE LOWER(%s)"
                params.append(f'%{title_query}%')

            if min_salary or max_salary:
                # Need fiscal year for salary filtering
                if fiscal_year:
                    sql += " AND c.fiscal_year = %s"
                    params.append(fiscal_year)

                if min_salary:
                    sql += " AND c.gross_pay >= %s"
                    params.append(min_salary)

                if max_salary:
                    sql += " AND c.gross_pay <= %s"
                    params.append(max_salary)

            sql += " ORDER BY p.last_name, p.first_name LIMIT %s;"
            params.append(limit)

            cur.execute(sql, params)
            return cur.fetchall()

    def get_category_statistics(self) -> List[Dict[str, Any]]:
        """
        Get statistics for all categories.

        Returns:
            List of categories with org count, employee count, avg salary
        """
        with self.db.get_cursor() as cur:
            cur.execute("""
                SELECT
                    c.id,
                    c.name,
                    c.slug,
                    COUNT(DISTINCT o.id) as organization_count,
                    COUNT(DISTINCT po.person_id) as current_employee_count,
                    AVG(comp.gross_pay) as avg_salary,
                    SUM(comp.gross_pay) as total_payroll
                FROM categories c
                LEFT JOIN organizations o ON c.id = o.category_id AND o.is_active = TRUE
                LEFT JOIN person_organizations po ON o.id = po.organization_id AND po.is_current = TRUE
                LEFT JOIN compensation comp ON po.person_id = comp.person_id
                GROUP BY c.id, c.name, c.slug
                ORDER BY c.name;
            """)
            return cur.fetchall()

    def get_data_quality_report(self) -> Dict[str, Any]:
        """
        Get data quality statistics across all tables.

        Returns:
            Dict with completeness metrics
        """
        with self.db.get_cursor() as cur:
            # People stats
            cur.execute("""
                SELECT
                    COUNT(*) as total_people,
                    SUM(CASE WHEN first_name IS NOT NULL THEN 1 ELSE 0 END) as with_first_name,
                    SUM(CASE WHEN last_name IS NOT NULL THEN 1 ELSE 0 END) as with_last_name,
                    SUM(CASE WHEN bio IS NOT NULL THEN 1 ELSE 0 END) as with_bio,
                    SUM(CASE WHEN photo_url IS NOT NULL THEN 1 ELSE 0 END) as with_photo,
                    SUM(CASE WHEN is_active THEN 1 ELSE 0 END) as active_count
                FROM people;
            """)
            people_stats = cur.fetchone()

            # Organization stats
            cur.execute("""
                SELECT
                    COUNT(*) as total_orgs,
                    SUM(CASE WHEN description IS NOT NULL THEN 1 ELSE 0 END) as with_description,
                    SUM(CASE WHEN main_url IS NOT NULL THEN 1 ELSE 0 END) as with_url,
                    SUM(CASE WHEN parent_id IS NULL THEN 1 ELSE 0 END) as root_orgs,
                    SUM(CASE WHEN is_active THEN 1 ELSE 0 END) as active_count
                FROM organizations;
            """)
            org_stats = cur.fetchone()

            # Compensation stats
            cur.execute("""
                SELECT
                    COUNT(*) as total_records,
                    COUNT(DISTINCT person_id) as unique_people,
                    COUNT(DISTINCT fiscal_year) as unique_years,
                    SUM(CASE WHEN person_id IS NOT NULL THEN 1 ELSE 0 END) as linked_to_person,
                    SUM(CASE WHEN organization_id IS NOT NULL THEN 1 ELSE 0 END) as linked_to_org,
                    SUM(CASE WHEN is_verified THEN 1 ELSE 0 END) as verified_count
                FROM compensation;
            """)
            comp_stats = cur.fetchone()

            # Contact info stats
            cur.execute("""
                SELECT
                    COUNT(*) as total_contacts,
                    COUNT(DISTINCT CONCAT(entity_type, '-', entity_id)) as unique_entities,
                    SUM(CASE WHEN is_public THEN 1 ELSE 0 END) as public_count,
                    SUM(CASE WHEN is_verified THEN 1 ELSE 0 END) as verified_count
                FROM contact_info;
            """)
            contact_stats = cur.fetchone()

            return {
                'people': people_stats or {},
                'organizations': org_stats or {},
                'compensation': comp_stats or {},
                'contact_info': contact_stats or {}
            }
