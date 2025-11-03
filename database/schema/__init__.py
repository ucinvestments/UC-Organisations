"""
Database schema definitions split by table.

Each file contains schema for ONE table following Single Responsibility Principle.
"""

from .categories import create_categories_table, drop_categories_table
from .organizations import create_organizations_table, drop_organizations_table
from .people import create_people_table, drop_people_table
from .person_organizations import create_person_organizations_table, drop_person_organizations_table
from .compensation import create_compensation_table, drop_compensation_table
from .contact_info import create_contact_info_table, drop_contact_info_table
from .social_media import create_social_media_table, drop_social_media_table
from .data_sources import create_data_sources_table, drop_data_sources_table

__all__ = [
    'create_categories_table',
    'create_organizations_table',
    'create_people_table',
    'create_person_organizations_table',
    'create_compensation_table',
    'create_contact_info_table',
    'create_social_media_table',
    'create_data_sources_table',
    'drop_categories_table',
    'drop_organizations_table',
    'drop_people_table',
    'drop_person_organizations_table',
    'drop_compensation_table',
    'drop_contact_info_table',
    'drop_social_media_table',
    'drop_data_sources_table',
]


def create_all_tables(db_connection):
    """
    Create all database tables in correct dependency order.

    Args:
        db_connection: DatabaseConnection instance
    """
    # Create in dependency order (no foreign keys first)
    create_categories_table(db_connection)
    create_organizations_table(db_connection)  # References categories
    create_people_table(db_connection)
    create_person_organizations_table(db_connection)  # References people & orgs
    create_compensation_table(db_connection)  # References people & orgs
    create_contact_info_table(db_connection)  # Polymorphic
    create_social_media_table(db_connection)  # Polymorphic
    create_data_sources_table(db_connection)  # Polymorphic


def drop_all_tables(db_connection):
    """
    Drop all database tables in reverse dependency order.

    Args:
        db_connection: DatabaseConnection instance
    """
    # Drop in reverse order (tables with foreign keys first)
    drop_data_sources_table(db_connection)
    drop_social_media_table(db_connection)
    drop_contact_info_table(db_connection)
    drop_compensation_table(db_connection)
    drop_person_organizations_table(db_connection)
    drop_people_table(db_connection)
    drop_organizations_table(db_connection)
    drop_categories_table(db_connection)
