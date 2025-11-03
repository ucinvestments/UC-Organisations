"""
Database models for UC Organizations scraper.
Provides high-level interface for database operations.
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class Organization:
    """Organization model."""

    @staticmethod
    def create(db, category_id: int, name: str, slug: str, directory_path: str,
               description: str = None, main_url: str = None, data_source: str = None):
        """
        Create a new organization.

        Args:
            db: DatabaseConnection instance
            category_id: Category ID
            name: Organization name
            slug: URL-friendly slug
            directory_path: File system path (e.g., 'handlers/ucop/academic_affairs')
            description: Organization description
            main_url: Main organization URL
            data_source: Data source URL

        Returns:
            Organization ID
        """
        with db.get_cursor() as cur:
            cur.execute("""
                INSERT INTO organizations
                (category_id, name, slug, directory_path, description, main_url, data_source)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (directory_path)
                DO UPDATE SET
                    name = EXCLUDED.name,
                    description = EXCLUDED.description,
                    main_url = EXCLUDED.main_url,
                    data_source = EXCLUDED.data_source,
                    updated_at = CURRENT_TIMESTAMP
                RETURNING id;
            """, (category_id, name, slug, directory_path, description, main_url, data_source))

            return cur.fetchone()['id']

    @staticmethod
    def get_by_path(db, directory_path: str):
        """Get organization by directory path."""
        with db.get_cursor() as cur:
            cur.execute("""
                SELECT o.*, c.name as category_name, c.slug as category_slug
                FROM organizations o
                JOIN categories c ON o.category_id = c.id
                WHERE o.directory_path = %s;
            """, (directory_path,))

            return cur.fetchone()

    @staticmethod
    def get_by_id(db, org_id: int):
        """Get organization by ID."""
        with db.get_cursor() as cur:
            cur.execute("""
                SELECT o.*, c.name as category_name, c.slug as category_slug
                FROM organizations o
                JOIN categories c ON o.category_id = c.id
                WHERE o.id = %s;
            """, (org_id,))

            return cur.fetchone()

    @staticmethod
    def list_all(db, category_id: int = None):
        """List all organizations, optionally filtered by category."""
        with db.get_cursor() as cur:
            if category_id:
                cur.execute("""
                    SELECT o.*, c.name as category_name, c.slug as category_slug
                    FROM organizations o
                    JOIN categories c ON o.category_id = c.id
                    WHERE o.category_id = %s
                    ORDER BY o.name;
                """, (category_id,))
            else:
                cur.execute("""
                    SELECT o.*, c.name as category_name, c.slug as category_slug
                    FROM organizations o
                    JOIN categories c ON o.category_id = c.id
                    ORDER BY c.name, o.name;
                """)

            return cur.fetchall()

    @staticmethod
    def get_stats(db, org_id: int):
        """Get statistics for an organization."""
        with db.get_cursor() as cur:
            cur.execute("""
                SELECT
                    COUNT(DISTINCT s.id) as staff_count,
                    COUNT(DISTINCT d.id) as department_count,
                    (SELECT MAX(end_time) FROM scraper_runs WHERE organization_id = %s) as last_scraped
                FROM organizations o
                LEFT JOIN staff s ON o.id = s.organization_id
                LEFT JOIN departments d ON o.id = d.organization_id
                WHERE o.id = %s
                GROUP BY o.id;
            """, (org_id, org_id))

            return cur.fetchone()


class Department:
    """Department model."""

    @staticmethod
    def create(db, organization_id: int, name: str, slug: str, url: str = None):
        """Create a new department."""
        with db.get_cursor() as cur:
            cur.execute("""
                INSERT INTO departments (organization_id, name, slug, url)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (organization_id, slug)
                DO UPDATE SET
                    name = EXCLUDED.name,
                    url = EXCLUDED.url,
                    updated_at = CURRENT_TIMESTAMP
                RETURNING id;
            """, (organization_id, name, slug, url))

            return cur.fetchone()['id']

    @staticmethod
    def get_by_slug(db, organization_id: int, slug: str):
        """Get department by organization and slug."""
        with db.get_cursor() as cur:
            cur.execute("""
                SELECT * FROM departments
                WHERE organization_id = %s AND slug = %s;
            """, (organization_id, slug))

            return cur.fetchone()

    @staticmethod
    def list_by_organization(db, organization_id: int):
        """List all departments for an organization."""
        with db.get_cursor() as cur:
            cur.execute("""
                SELECT * FROM departments
                WHERE organization_id = %s
                ORDER BY name;
            """, (organization_id,))

            return cur.fetchall()


class Staff:
    """Staff model."""

    @staticmethod
    def create(db, organization_id: int, name: str, title: str = None,
               email: str = None, phone: str = None, department_id: int = None,
               office_location: str = None, data_source: str = None, raw_data: dict = None):
        """Create a new staff member."""
        with db.get_cursor() as cur:
            cur.execute("""
                INSERT INTO staff
                (organization_id, department_id, name, title, email, phone,
                 office_location, data_source, raw_data)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id;
            """, (organization_id, department_id, name, title, email, phone,
                  office_location, data_source, raw_data))

            return cur.fetchone()['id']

    @staticmethod
    def upsert(db, organization_id: int, name: str, email: str = None, **kwargs):
        """
        Create or update staff member (matched by name and organization).

        Args:
            db: DatabaseConnection instance
            organization_id: Organization ID
            name: Staff member name
            email: Email (optional, used for matching)
            **kwargs: Other staff fields

        Returns:
            Staff ID
        """
        with db.get_cursor() as cur:
            # Try to find existing staff by name and org (and email if provided)
            if email:
                cur.execute("""
                    SELECT id FROM staff
                    WHERE organization_id = %s AND (name = %s OR email = %s);
                """, (organization_id, name, email))
            else:
                cur.execute("""
                    SELECT id FROM staff
                    WHERE organization_id = %s AND name = %s;
                """, (organization_id, name))

            existing = cur.fetchone()

            if existing:
                # Update existing staff
                staff_id = existing['id']
                update_fields = []
                update_values = []

                for key, value in kwargs.items():
                    if value is not None:
                        update_fields.append(f"{key} = %s")
                        update_values.append(value)

                if email:
                    update_fields.append("email = %s")
                    update_values.append(email)

                if update_fields:
                    update_fields.append("updated_at = CURRENT_TIMESTAMP")
                    update_values.append(staff_id)

                    cur.execute(f"""
                        UPDATE staff
                        SET {', '.join(update_fields)}
                        WHERE id = %s;
                    """, update_values)

                return staff_id
            else:
                # Create new staff
                return Staff.create(db, organization_id, name, email=email, **kwargs)

    @staticmethod
    def list_by_organization(db, organization_id: int):
        """List all staff for an organization."""
        with db.get_cursor() as cur:
            cur.execute("""
                SELECT s.*, d.name as department_name
                FROM staff s
                LEFT JOIN departments d ON s.department_id = d.id
                WHERE s.organization_id = %s
                ORDER BY s.name;
            """, (organization_id,))

            return cur.fetchall()

    @staticmethod
    def list_by_department(db, department_id: int):
        """List all staff for a department."""
        with db.get_cursor() as cur:
            cur.execute("""
                SELECT * FROM staff
                WHERE department_id = %s
                ORDER BY name;
            """, (department_id,))

            return cur.fetchall()

    @staticmethod
    def search(db, query: str):
        """Search staff by name, title, or email."""
        with db.get_cursor() as cur:
            search_pattern = f"%{query}%"
            cur.execute("""
                SELECT s.*, o.name as organization_name, d.name as department_name
                FROM staff s
                JOIN organizations o ON s.organization_id = o.id
                LEFT JOIN departments d ON s.department_id = d.id
                WHERE s.name ILIKE %s
                   OR s.title ILIKE %s
                   OR s.email ILIKE %s
                ORDER BY s.name
                LIMIT 100;
            """, (search_pattern, search_pattern, search_pattern))

            return cur.fetchall()


class ScraperRun:
    """Scraper run tracking model."""

    @staticmethod
    def create(db, organization_id: int, status: str = 'running'):
        """Start a new scraper run."""
        with db.get_cursor() as cur:
            cur.execute("""
                INSERT INTO scraper_runs (organization_id, status, start_time)
                VALUES (%s, %s, %s)
                RETURNING id;
            """, (organization_id, status, datetime.now()))

            return cur.fetchone()['id']

    @staticmethod
    def update(db, run_id: int, status: str = None, staff_scraped: int = None,
               departments_scraped: int = None, errors_count: int = None,
               error_log: str = None, stats: dict = None):
        """Update scraper run."""
        with db.get_cursor() as cur:
            updates = []
            values = []

            if status:
                updates.append("status = %s")
                values.append(status)
                if status in ['completed', 'failed']:
                    updates.append("end_time = %s")
                    values.append(datetime.now())

            if staff_scraped is not None:
                updates.append("staff_scraped = %s")
                values.append(staff_scraped)

            if departments_scraped is not None:
                updates.append("departments_scraped = %s")
                values.append(departments_scraped)

            if errors_count is not None:
                updates.append("errors_count = %s")
                values.append(errors_count)

            if error_log:
                updates.append("error_log = %s")
                values.append(error_log)

            if stats:
                updates.append("stats = %s")
                values.append(stats)

            if updates:
                values.append(run_id)
                cur.execute(f"""
                    UPDATE scraper_runs
                    SET {', '.join(updates)}
                    WHERE id = %s;
                """, values)

    @staticmethod
    def get_latest(db, organization_id: int):
        """Get latest scraper run for an organization."""
        with db.get_cursor() as cur:
            cur.execute("""
                SELECT * FROM scraper_runs
                WHERE organization_id = %s
                ORDER BY start_time DESC
                LIMIT 1;
            """, (organization_id,))

            return cur.fetchone()

    @staticmethod
    def list_by_organization(db, organization_id: int, limit: int = 10):
        """List scraper runs for an organization."""
        with db.get_cursor() as cur:
            cur.execute("""
                SELECT * FROM scraper_runs
                WHERE organization_id = %s
                ORDER BY start_time DESC
                LIMIT %s;
            """, (organization_id, limit))

            return cur.fetchall()


class Category:
    """Category model."""

    @staticmethod
    def get_by_slug(db, slug: str):
        """Get category by slug."""
        with db.get_cursor() as cur:
            cur.execute("SELECT * FROM categories WHERE slug = %s;", (slug,))
            return cur.fetchone()

    @staticmethod
    def get_by_id(db, category_id: int):
        """Get category by ID."""
        with db.get_cursor() as cur:
            cur.execute("SELECT * FROM categories WHERE id = %s;", (category_id,))
            return cur.fetchone()

    @staticmethod
    def list_all(db):
        """List all categories."""
        with db.get_cursor() as cur:
            cur.execute("SELECT * FROM categories ORDER BY name;")
            return cur.fetchall()
