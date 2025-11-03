"""
Compensation table schema.

Single Responsibility: Define ONLY the compensation table structure.

Stores salary/wage data for people at organizations.
Designed for UC employee salary data from public records.
"""

import logging

logger = logging.getLogger(__name__)


def create_compensation_table(db_connection):
    """
    Create compensation table.

    Stores annual compensation data including:
    - Base salary, overtime, bonuses
    - Benefits value
    - Fiscal year tracking
    - Source verification

    Designed for UCLA salary JSON structure:
    {"basepay": "48687.00", "overtimepay": "2184.00", "grosspay": "50871.00", "year": 2018}

    Args:
        db_connection: DatabaseConnection instance
    """
    with db_connection.get_cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS compensation (
                id SERIAL PRIMARY KEY,

                -- Links to entities
                person_id INTEGER REFERENCES people(id) ON DELETE CASCADE,
                organization_id INTEGER REFERENCES organizations(id) ON DELETE CASCADE,

                -- Source identifiers (for deduplication)
                source_employee_id INTEGER,  -- Original employee ID from source
                source_record_id INTEGER,    -- Original record ID from source
                source_location VARCHAR(100), -- e.g., "ASUCLA", "UC Berkeley"

                -- Time period
                fiscal_year INTEGER NOT NULL,
                effective_start_date DATE,
                effective_end_date DATE,

                -- Compensation breakdown (DECIMAL for proper math)
                base_pay DECIMAL(12,2),
                overtime_pay DECIMAL(12,2),
                adjustment_pay DECIMAL(12,2),  -- Adjustments/corrections
                bonus_pay DECIMAL(12,2),
                other_pay DECIMAL(12,2),
                gross_pay DECIMAL(12,2),
                benefits_value DECIMAL(12,2),
                total_compensation DECIMAL(12,2),

                -- Currency
                currency VARCHAR(3) DEFAULT 'USD',

                -- Position details
                title VARCHAR(255),
                title_normalized VARCHAR(255),  -- Cleaned/expanded title
                position_type VARCHAR(50),  -- 'full_time', 'part_time', 'contract'

                -- Data provenance
                data_source VARCHAR(100),  -- e.g., 'transparency_ca', 'state_controller'
                scraped_at TIMESTAMP,
                uploaded_at TIMESTAMP,

                -- Data quality
                is_verified BOOLEAN DEFAULT FALSE,
                is_public BOOLEAN DEFAULT TRUE,  -- Public record data
                is_historical BOOLEAN DEFAULT FALSE,
                original_publish_date DATE,

                -- Notes
                notes TEXT,

                -- Timestamps
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                -- Constraints
                UNIQUE(source_employee_id, source_location, fiscal_year),
                CHECK (base_pay >= 0),
                CHECK (gross_pay >= 0),
                CHECK (fiscal_year >= 1900 AND fiscal_year <= 2100)
            );
        """)

        # Indexes for common queries
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_compensation_person
            ON compensation(person_id);
        """)

        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_compensation_organization
            ON compensation(organization_id);
        """)

        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_compensation_fiscal_year
            ON compensation(fiscal_year);
        """)

        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_compensation_source
            ON compensation(source_employee_id, source_location);
        """)

        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_compensation_public
            ON compensation(is_public) WHERE is_public = TRUE;
        """)

        # Index for salary range queries
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_compensation_gross_pay
            ON compensation(gross_pay) WHERE gross_pay IS NOT NULL;
        """)

        logger.info("Compensation table created")


def drop_compensation_table(db_connection):
    """
    Drop compensation table.

    Args:
        db_connection: DatabaseConnection instance
    """
    with db_connection.get_cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS compensation CASCADE;")
        logger.info("Compensation table dropped")
