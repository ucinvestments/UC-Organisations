"""
Organizations table schema.

Single Responsibility: Define ONLY the organizations table structure.

IMPORTANT: This table consolidates both organizations AND departments into ONE table
using a parent_id self-referencing foreign key for hierarchy.

Example:
    UC Berkeley (parent_id=NULL, category='campuses')
    └── Department of Computer Science (parent_id=123, category='campuses')
        └── AI Research Lab (parent_id=456, category='campuses')
"""

import logging

logger = logging.getLogger(__name__)


def create_organizations_table(db_connection):
    """
    Create organizations table with self-referencing hierarchy.

    Consolidates organizations and departments into ONE table.
    Departments are just organizations with a non-NULL parent_id.

    Args:
        db_connection: DatabaseConnection instance
    """
    with db_connection.get_cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS organizations (
                id SERIAL PRIMARY KEY,

                -- Hierarchy (self-referencing FK)
                parent_id INTEGER REFERENCES organizations(id) ON DELETE CASCADE,
                category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,

                -- Basic info
                name VARCHAR(255) NOT NULL,
                slug VARCHAR(255) NOT NULL,
                description TEXT,
                directory_path VARCHAR(500) UNIQUE,

                -- URLs
                main_url VARCHAR(500),

                -- Hierarchy helpers
                hierarchy_level INTEGER DEFAULT 0,
                full_path TEXT,  -- e.g., "UC Berkeley > CS Department > AI Lab"

                -- Dates
                start_date DATE,
                end_date DATE,

                -- Status
                is_active BOOLEAN DEFAULT TRUE,

                -- Timestamps
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                -- Constraints
                UNIQUE(parent_id, slug),  -- Unique slug within same parent
                CHECK (parent_id != id)  -- Can't be parent of itself
            );
        """)

        # Indexes for common queries
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_organizations_parent
            ON organizations(parent_id);
        """)

        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_organizations_category
            ON organizations(category_id);
        """)

        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_organizations_directory_path
            ON organizations(directory_path);
        """)

        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_organizations_slug
            ON organizations(slug);
        """)

        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_organizations_active
            ON organizations(is_active) WHERE is_active = TRUE;
        """)

        # Index for hierarchy queries
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_organizations_hierarchy_level
            ON organizations(hierarchy_level);
        """)

        logger.info("Organizations table created")


def drop_organizations_table(db_connection):
    """
    Drop organizations table.

    Args:
        db_connection: DatabaseConnection instance
    """
    with db_connection.get_cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS organizations CASCADE;")
        logger.info("Organizations table dropped")
