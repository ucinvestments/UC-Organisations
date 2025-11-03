"""
People table schema.

Single Responsibility: Define ONLY the people table structure.

Stores individual people separate from their organizational relationships.
"""

import logging

logger = logging.getLogger(__name__)


def create_people_table(db_connection):
    """
    Create people table.

    Stores core person information.
    Relationships to organizations stored in person_organizations table.

    Args:
        db_connection: DatabaseConnection instance
    """
    with db_connection.get_cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS people (
                id SERIAL PRIMARY KEY,

                -- Name (split for better search/sort)
                first_name VARCHAR(100),
                last_name VARCHAR(100),
                middle_name VARCHAR(100),
                preferred_name VARCHAR(100),

                -- Profile
                bio TEXT,
                photo_url VARCHAR(500),
                profile_url VARCHAR(500),

                -- Status
                is_active BOOLEAN DEFAULT TRUE,

                -- Timestamps
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Indexes for searching/sorting
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_people_last_name
            ON people(last_name);
        """)

        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_people_first_name
            ON people(first_name);
        """)

        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_people_full_name
            ON people(last_name, first_name);
        """)

        # Full-text search index for names
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_people_name_search
            ON people USING gin(
                to_tsvector('english',
                    COALESCE(first_name, '') || ' ' ||
                    COALESCE(middle_name, '') || ' ' ||
                    COALESCE(last_name, '') || ' ' ||
                    COALESCE(preferred_name, '')
                )
            );
        """)

        logger.info("People table created")


def drop_people_table(db_connection):
    """
    Drop people table.

    Args:
        db_connection: DatabaseConnection instance
    """
    with db_connection.get_cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS people CASCADE;")
        logger.info("People table dropped")
