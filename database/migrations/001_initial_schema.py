"""
Migration 001: Initial schema.

Creates all base tables following SOLID/UNIX refactored structure.

Up:
  - Creates categories table
  - Creates organizations table (with parent_id for hierarchy)
  - Creates people table
  - Creates person_organizations junction table
  - Creates compensation table
  - Creates contact_info polymorphic table
  - Creates social_media polymorphic table
  - Creates data_sources polymorphic table

Down:
  - Drops all tables in reverse order
"""

import logging

logger = logging.getLogger(__name__)


def up(db_connection):
    """
    Apply migration: Create all tables.

    Args:
        db_connection: DatabaseConnection instance
    """
    from database.schema import create_all_tables

    logger.info("Running migration 001: Creating initial schema...")
    create_all_tables(db_connection)
    logger.info("Migration 001 complete: All tables created")


def down(db_connection):
    """
    Rollback migration: Drop all tables.

    Args:
        db_connection: DatabaseConnection instance
    """
    from database.schema import drop_all_tables

    logger.info("Rolling back migration 001: Dropping all tables...")
    drop_all_tables(db_connection)
    logger.info("Migration 001 rolled back: All tables dropped")
