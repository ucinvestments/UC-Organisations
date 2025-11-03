"""
Social media table schema.

Single Responsibility: Define ONLY the social_media table structure.

Polymorphic table for storing social media profiles
for both people and organizations.
"""

import logging

logger = logging.getLogger(__name__)


def create_social_media_table(db_connection):
    """
    Create social_media polymorphic table.

    Stores social media profiles for both people and organizations:
    - LinkedIn
    - Twitter/X
    - Instagram
    - Facebook
    - YouTube
    - Google Calendar
    - GitHub
    - etc.

    Uses polymorphic pattern (entity_type + entity_id).

    Args:
        db_connection: DatabaseConnection instance
    """
    with db_connection.get_cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS social_media (
                id SERIAL PRIMARY KEY,

                -- Polymorphic relationship
                entity_type VARCHAR(50) NOT NULL,  -- 'person' or 'organization'
                entity_id INTEGER NOT NULL,

                -- Social media details
                platform VARCHAR(50) NOT NULL,  -- 'linkedin', 'twitter', 'instagram', 'facebook', 'youtube', 'github', 'google_calendar'
                handle VARCHAR(255),  -- @username or handle
                profile_url VARCHAR(500) NOT NULL,

                -- Profile metadata
                display_name VARCHAR(255),  -- Display name on platform
                follower_count INTEGER,
                following_count INTEGER,
                last_post_date DATE,

                -- Flags
                is_verified BOOLEAN DEFAULT FALSE,  -- Platform-verified account
                is_active BOOLEAN DEFAULT TRUE,
                is_public BOOLEAN DEFAULT TRUE,

                -- Source tracking
                data_source VARCHAR(100),
                scraped_at TIMESTAMP,

                -- Timestamps
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                -- Constraints
                CHECK (entity_type IN ('person', 'organization')),
                CHECK (platform IN (
                    'linkedin', 'twitter', 'x', 'instagram', 'facebook',
                    'youtube', 'github', 'google_calendar', 'reddit',
                    'tiktok', 'mastodon', 'bluesky', 'other'
                )),
                UNIQUE(entity_type, entity_id, platform, profile_url)
            );
        """)

        # Indexes for polymorphic queries
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_social_media_entity
            ON social_media(entity_type, entity_id);
        """)

        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_social_media_platform
            ON social_media(platform);
        """)

        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_social_media_verified
            ON social_media(is_verified) WHERE is_verified = TRUE;
        """)

        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_social_media_handle
            ON social_media(handle);
        """)

        # Index for searching by profile URL
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_social_media_url
            ON social_media(profile_url);
        """)

        logger.info("Social media table created")


def drop_social_media_table(db_connection):
    """
    Drop social_media table.

    Args:
        db_connection: DatabaseConnection instance
    """
    with db_connection.get_cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS social_media CASCADE;")
        logger.info("Social media table dropped")
