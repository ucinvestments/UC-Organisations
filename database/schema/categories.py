"""
Categories table schema.

Single Responsibility: Define ONLY the categories table structure.
"""

import logging

logger = logging.getLogger(__name__)


def create_categories_table(db_connection):
    """
    Create categories table.

    Categories: UCOP, Campuses, Labs, Academic Senate, Board of Regents

    Args:
        db_connection: DatabaseConnection instance
    """
    with db_connection.get_cursor() as cur:
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

        logger.info("Categories table created")


def drop_categories_table(db_connection):
    """
    Drop categories table.

    Args:
        db_connection: DatabaseConnection instance
    """
    with db_connection.get_cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS categories CASCADE;")
        logger.info("Categories table dropped")


def seed_categories(db_connection):
    """
    Seed initial category data.

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
