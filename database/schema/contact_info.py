"""
Contact info table schema.

Single Responsibility: Define ONLY the contact_info table structure.

Polymorphic table for storing contact information (email, phone, address)
for both people and organizations.
"""

import logging

logger = logging.getLogger(__name__)


def create_contact_info_table(db_connection):
    """
    Create contact_info polymorphic table.

    Stores contact information for both people and organizations:
    - Email addresses
    - Phone numbers
    - Physical addresses
    - Fax numbers
    - Other contact methods

    Uses polymorphic pattern (entity_type + entity_id).

    Args:
        db_connection: DatabaseConnection instance
    """
    with db_connection.get_cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS contact_info (
                id SERIAL PRIMARY KEY,

                -- Polymorphic relationship
                entity_type VARCHAR(50) NOT NULL,  -- 'person' or 'organization'
                entity_id INTEGER NOT NULL,

                -- Contact details
                contact_type VARCHAR(50) NOT NULL,  -- 'email', 'phone', 'address', 'fax', 'mobile', 'office'
                contact_value TEXT NOT NULL,

                -- Additional fields for structured data
                contact_label VARCHAR(100),  -- 'Work', 'Personal', 'Main Office', etc.
                extension VARCHAR(20),  -- Phone extensions
                country_code VARCHAR(10),  -- For international phone numbers

                -- Flags
                is_primary BOOLEAN DEFAULT FALSE,  -- Primary contact method
                is_public BOOLEAN DEFAULT TRUE,  -- Publicly visible
                is_verified BOOLEAN DEFAULT FALSE,

                -- Source tracking
                data_source VARCHAR(100),
                scraped_at TIMESTAMP,

                -- Timestamps
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                -- Constraints
                CHECK (entity_type IN ('person', 'organization')),
                CHECK (contact_type IN ('email', 'phone', 'mobile', 'office', 'fax', 'address', 'other')),
                UNIQUE(entity_type, entity_id, contact_type, contact_value)
            );
        """)

        # Indexes for polymorphic queries
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_contact_info_entity
            ON contact_info(entity_type, entity_id);
        """)

        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_contact_info_type
            ON contact_info(contact_type);
        """)

        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_contact_info_primary
            ON contact_info(is_primary) WHERE is_primary = TRUE;
        """)

        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_contact_info_public
            ON contact_info(is_public) WHERE is_public = TRUE;
        """)

        # Index for searching by contact value (e.g., find person by email)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_contact_info_value
            ON contact_info(contact_value);
        """)

        logger.info("Contact info table created")


def drop_contact_info_table(db_connection):
    """
    Drop contact_info table.

    Args:
        db_connection: DatabaseConnection instance
    """
    with db_connection.get_cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS contact_info CASCADE;")
        logger.info("Contact info table dropped")
