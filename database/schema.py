"""
Database schema definitions for UC Organizations scraper.
"""

import logging

logger = logging.getLogger(__name__)


def create_tables(db_connection):
    """
    Create all database tables.

    Args:
        db_connection: DatabaseConnection instance
    """
    with db_connection.get_cursor() as cur:
        # Enable UUID extension
        cur.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")

        # Categories table (UCOP, Campuses, Labs, etc.)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) UNIQUE NOT NULL,
                slug VARCHAR(100) UNIQUE NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Organizations table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS organizations (
                id SERIAL PRIMARY KEY,
                category_id INTEGER REFERENCES categories(id) ON DELETE CASCADE,
                name VARCHAR(255) NOT NULL,
                slug VARCHAR(255) NOT NULL,
                directory_path VARCHAR(500) UNIQUE NOT NULL,
                description TEXT,
                main_url VARCHAR(500),
                data_source VARCHAR(500),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(category_id, slug)
            );
        """)

        # Create index on directory_path for faster lookups
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_organizations_directory_path
            ON organizations(directory_path);
        """)

        # Departments table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS departments (
                id SERIAL PRIMARY KEY,
                organization_id INTEGER REFERENCES organizations(id) ON DELETE CASCADE,
                name VARCHAR(255) NOT NULL,
                slug VARCHAR(255) NOT NULL,
                url VARCHAR(500),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(organization_id, slug)
            );
        """)

        # Staff table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS staff (
                id SERIAL PRIMARY KEY,
                organization_id INTEGER REFERENCES organizations(id) ON DELETE CASCADE,
                department_id INTEGER REFERENCES departments(id) ON DELETE SET NULL,
                name VARCHAR(255) NOT NULL,
                title VARCHAR(255),
                email VARCHAR(255),
                phone VARCHAR(50),
                office_location VARCHAR(255),
                data_source VARCHAR(500),
                raw_data JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Create indexes for staff searches
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_staff_organization
            ON staff(organization_id);
        """)

        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_staff_department
            ON staff(department_id);
        """)

        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_staff_name
            ON staff(name);
        """)

        # Scraper runs table (tracking)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS scraper_runs (
                id SERIAL PRIMARY KEY,
                organization_id INTEGER REFERENCES organizations(id) ON DELETE CASCADE,
                status VARCHAR(50) NOT NULL,
                start_time TIMESTAMP NOT NULL,
                end_time TIMESTAMP,
                staff_scraped INTEGER DEFAULT 0,
                departments_scraped INTEGER DEFAULT 0,
                errors_count INTEGER DEFAULT 0,
                error_log TEXT,
                stats JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Create index on scraper runs
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_scraper_runs_organization
            ON scraper_runs(organization_id);
        """)

        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_scraper_runs_status
            ON scraper_runs(status);
        """)

        # Organization metadata table (for flexible key-value data)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS organization_metadata (
                id SERIAL PRIMARY KEY,
                organization_id INTEGER REFERENCES organizations(id) ON DELETE CASCADE,
                key VARCHAR(100) NOT NULL,
                value TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(organization_id, key)
            );
        """)

        logger.info("All database tables created successfully")


def drop_tables(db_connection):
    """
    Drop all database tables (use with caution!).

    Args:
        db_connection: DatabaseConnection instance
    """
    with db_connection.get_cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS organization_metadata CASCADE;")
        cur.execute("DROP TABLE IF EXISTS scraper_runs CASCADE;")
        cur.execute("DROP TABLE IF EXISTS staff CASCADE;")
        cur.execute("DROP TABLE IF EXISTS departments CASCADE;")
        cur.execute("DROP TABLE IF EXISTS organizations CASCADE;")
        cur.execute("DROP TABLE IF EXISTS categories CASCADE;")

        logger.warning("All database tables dropped")


def seed_categories(db_connection):
    """
    Seed initial categories.

    Args:
        db_connection: DatabaseConnection instance
    """
    categories = [
        ('UCOP', 'ucop', 'UC Office of the President organizations'),
        ('Campuses', 'campuses', 'UC Campus organizations'),
        ('Labs', 'labs', 'National Laboratory organizations'),
        ('Academic Senate', 'academic_senate', 'UC Academic Senate'),
        ('Board of Regents', 'board_of_regents', 'UC Board of Regents')
    ]

    with db_connection.get_cursor() as cur:
        for name, slug, description in categories:
            cur.execute("""
                INSERT INTO categories (name, slug, description)
                VALUES (%s, %s, %s)
                ON CONFLICT (slug) DO NOTHING;
            """, (name, slug, description))

    logger.info(f"Seeded {len(categories)} categories")
