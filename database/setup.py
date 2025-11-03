#!/usr/bin/env python3
"""
Database setup and migration script.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import logging
from dotenv import load_dotenv

from database import (
    get_db_connection,
    create_all_tables,
    drop_all_tables,
    CategoryModel,
    OrganizationModel,
)
from database.schema.categories import seed_categories
from database.connection import close_db

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def setup_database(drop_existing=False):
    """
    Setup database tables and seed initial data.

    Args:
        drop_existing: If True, drop existing tables first (WARNING: deletes all data)
    """
    # Load environment variables
    load_dotenv()

    logger.info("Connecting to database...")
    db = get_db_connection()

    try:
        if drop_existing:
            logger.warning("Dropping existing tables...")
            response = input("This will DELETE ALL DATA. Type 'yes' to confirm: ")
            if response.lower() != 'yes':
                logger.info("Aborted.")
                return
            drop_all_tables(db)

        logger.info("Creating database tables...")
        create_all_tables(db)

        logger.info("Seeding categories...")
        seed_categories(db)

        logger.info("Database setup completed successfully!")

    except Exception as e:
        logger.error(f"Database setup failed: {e}")
        raise
    finally:
        close_db()


def sync_organizations_from_filesystem():
    """
    Sync organizations from filesystem to database.
    Reads the handlers directory and creates organization records.
    """
    load_dotenv()

    from common.utils import get_all_scrapers
    from config import ORGANIZATIONS

    logger.info("Syncing organizations from filesystem...")
    db = get_db_connection()

    try:
        # Initialize models
        category_model = CategoryModel(db)
        org_model = OrganizationModel(db)

        scrapers = get_all_scrapers()
        synced_count = 0

        for scraper_info in scrapers:
            org_dir = scraper_info['org_dir']
            org_name = scraper_info['name']

            # Extract category from path
            path_parts = org_dir.split('/')
            if len(path_parts) < 2:
                logger.warning(f"Invalid path structure for {org_dir}")
                continue

            category_slug = path_parts[1]

            # Get category ID
            category = category_model.find_by_slug(category_slug)
            if not category:
                logger.warning(f"Category not found: {category_slug}")
                continue

            # Get organization config if available
            org_config = ORGANIZATIONS.get(org_dir, {})

            # Create slug from org name
            slug = path_parts[-1] if len(path_parts) > 0 else org_dir.replace('/', '_')

            # Create/update organization
            org_id = org_model.upsert_organization(
                slug=slug,
                name=org_config.get('name', org_name),
                category_id=category['id'],
                directory_path=org_dir,
                description=org_config.get('description', ''),
                main_url=org_config.get('main_url')
            )

            logger.info(f"Synced: {org_name} (ID: {org_id})")
            synced_count += 1

        logger.info(f"Successfully synced {synced_count} organizations")

    except Exception as e:
        logger.error(f"Sync failed: {e}")
        raise
    finally:
        close_db()


def test_connection():
    """Test database connection."""
    load_dotenv()

    logger.info("Testing database connection...")

    try:
        db = get_db_connection()

        with db.get_cursor() as cur:
            cur.execute("SELECT version();")
            version = cur.fetchone()
            logger.info(f"Connected to PostgreSQL: {version['version']}")

        logger.info("Connection test successful!")

    except Exception as e:
        logger.error(f"Connection test failed: {e}")
        raise
    finally:
        close_db()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Database setup and migration')
    parser.add_argument('command', choices=['setup', 'reset', 'sync', 'test'],
                        help='Command to run')

    args = parser.parse_args()

    if args.command == 'setup':
        setup_database(drop_existing=False)
    elif args.command == 'reset':
        setup_database(drop_existing=True)
    elif args.command == 'sync':
        sync_organizations_from_filesystem()
    elif args.command == 'test':
        test_connection()
