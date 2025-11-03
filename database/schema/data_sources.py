"""
Data sources table schema.

Single Responsibility: Define ONLY the data_sources table structure.

Polymorphic table for tracking data provenance and sources
for all entities in the database.
"""

import logging

logger = logging.getLogger(__name__)


def create_data_sources_table(db_connection):
    """
    Create data_sources polymorphic table.

    Tracks where data came from for:
    - People
    - Organizations
    - Compensation records
    - Any other entity

    Supports data quality, verification, and compliance tracking.

    Args:
        db_connection: DatabaseConnection instance
    """
    with db_connection.get_cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS data_sources (
                id SERIAL PRIMARY KEY,

                -- Polymorphic relationship
                entity_type VARCHAR(50) NOT NULL,  -- 'person', 'organization', 'compensation', etc.
                entity_id INTEGER NOT NULL,

                -- Source details
                source_type VARCHAR(50) NOT NULL,  -- 'web_scrape', 'api', 'public_records', 'manual_entry', 'import'
                source_url VARCHAR(500),
                source_name VARCHAR(255),  -- e.g., "Transparency California", "UCLA Org Chart"
                source_description TEXT,

                -- Scraping details
                scraper_name VARCHAR(100),  -- Which scraper collected this
                scraper_version VARCHAR(50),
                scraped_at TIMESTAMP,

                -- Import details
                import_batch_id VARCHAR(100),  -- Group related imports
                import_file_name VARCHAR(255),
                imported_at TIMESTAMP,

                -- Data quality
                confidence_level VARCHAR(20),  -- 'high', 'medium', 'low'
                is_verified BOOLEAN DEFAULT FALSE,
                verified_by VARCHAR(255),
                verified_at TIMESTAMP,

                -- Legal/compliance
                is_public_record BOOLEAN DEFAULT FALSE,
                license VARCHAR(100),  -- Data license if applicable
                terms_url VARCHAR(500),  -- Terms of use URL

                -- Freshness tracking
                last_checked_at TIMESTAMP,
                next_check_at TIMESTAMP,  -- When to re-scrape
                check_frequency_days INTEGER,  -- How often to check

                -- Notes
                notes TEXT,

                -- Timestamps
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                -- Constraints
                CHECK (source_type IN (
                    'web_scrape', 'api', 'public_records',
                    'manual_entry', 'import', 'derived', 'other'
                )),
                CHECK (confidence_level IN ('high', 'medium', 'low', 'unknown'))
            );
        """)

        # Indexes for polymorphic queries
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_data_sources_entity
            ON data_sources(entity_type, entity_id);
        """)

        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_data_sources_type
            ON data_sources(source_type);
        """)

        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_data_sources_scraper
            ON data_sources(scraper_name);
        """)

        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_data_sources_batch
            ON data_sources(import_batch_id);
        """)

        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_data_sources_verified
            ON data_sources(is_verified) WHERE is_verified = TRUE;
        """)

        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_data_sources_scraped_at
            ON data_sources(scraped_at);
        """)

        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_data_sources_next_check
            ON data_sources(next_check_at)
            WHERE next_check_at IS NOT NULL;
        """)

        logger.info("Data sources table created")


def drop_data_sources_table(db_connection):
    """
    Drop data_sources table.

    Args:
        db_connection: DatabaseConnection instance
    """
    with db_connection.get_cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS data_sources CASCADE;")
        logger.info("Data sources table dropped")
