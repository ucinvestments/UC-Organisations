"""
Person-Organizations junction table schema.

Single Responsibility: Define ONLY the person_organizations table structure.

Links people to organizations with role/title and date ranges.
Supports many-to-many relationships (one person can work in multiple orgs/depts).
"""

import logging

logger = logging.getLogger(__name__)


def create_person_organizations_table(db_connection):
    """
    Create person_organizations junction table.

    Links people to organizations with:
    - Title/role at that organization
    - Date ranges for time-bounded affiliations
    - Primary affiliation tracking

    Args:
        db_connection: DatabaseConnection instance
    """
    with db_connection.get_cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS person_organizations (
                id SERIAL PRIMARY KEY,

                -- Foreign keys
                person_id INTEGER NOT NULL REFERENCES people(id) ON DELETE CASCADE,
                organization_id INTEGER NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,

                -- Role details
                title VARCHAR(255),
                title_normalized VARCHAR(255),  -- Cleaned/expanded title
                position_type VARCHAR(50),  -- 'full_time', 'part_time', 'contract', 'visiting'

                -- Time period
                start_date DATE,
                end_date DATE,  -- NULL means current
                is_current BOOLEAN GENERATED ALWAYS AS (end_date IS NULL) STORED,

                -- Flags
                is_primary_affiliation BOOLEAN DEFAULT FALSE,
                is_public BOOLEAN DEFAULT TRUE,

                -- Source tracking
                data_source VARCHAR(100),
                scraped_at TIMESTAMP,

                -- Timestamps
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                -- Constraints
                UNIQUE(person_id, organization_id, start_date),
                CHECK (end_date IS NULL OR end_date >= start_date)
            );
        """)

        # Indexes for common queries
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_person_orgs_person
            ON person_organizations(person_id);
        """)

        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_person_orgs_organization
            ON person_organizations(organization_id);
        """)

        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_person_orgs_current
            ON person_organizations(is_current) WHERE is_current = TRUE;
        """)

        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_person_orgs_primary
            ON person_organizations(is_primary_affiliation)
            WHERE is_primary_affiliation = TRUE;
        """)

        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_person_orgs_date_range
            ON person_organizations(start_date, end_date);
        """)

        logger.info("Person-organizations junction table created")


def drop_person_organizations_table(db_connection):
    """
    Drop person_organizations table.

    Args:
        db_connection: DatabaseConnection instance
    """
    with db_connection.get_cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS person_organizations CASCADE;")
        logger.info("Person-organizations table dropped")
