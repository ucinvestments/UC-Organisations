"""
Database package for UC Organizations scraper system.

Following SOLID and UNIX philosophy:
- Connection layer: Database connection management
- Schema layer: Table creation/migration (database/schema/)
- Model layer: Single-table CRUD operations (database/models/)
- Repository layer: Complex cross-table queries (database/repositories/)
- Base layer: Reusable patterns (database/base/)

Public API provides clean access to all layers.
"""

# Connection management
from .connection import DatabaseConnection, get_db_connection

# Schema functions (table creation/migration)
from .schema import (
    create_all_tables,
    drop_all_tables,
    create_categories_table,
    create_organizations_table,
    create_people_table,
    create_person_organizations_table,
    create_compensation_table,
    create_contact_info_table,
    create_social_media_table,
    create_data_sources_table,
)

# Models (single-table operations)
from .models import (
    CategoryModel,
    OrganizationModel,
    PersonModel,
    PersonOrganizationModel,
    CompensationModel,
    ContactInfoModel,
    SocialMediaModel,
    DataSourceModel,
)

# Repositories (complex multi-table operations)
from .repositories import (
    AnalyticsRepository,
)

# Base classes for extension
from .base.repository import BaseRepository, ReadRepository, WriteRepository
from .base.query_builder import QueryBuilder


__all__ = [
    # Connection
    'DatabaseConnection',
    'get_db_connection',

    # Schema
    'create_all_tables',
    'drop_all_tables',
    'create_categories_table',
    'create_organizations_table',
    'create_people_table',
    'create_person_organizations_table',
    'create_compensation_table',
    'create_contact_info_table',
    'create_social_media_table',
    'create_data_sources_table',

    # Models
    'CategoryModel',
    'OrganizationModel',
    'PersonModel',
    'PersonOrganizationModel',
    'CompensationModel',
    'ContactInfoModel',
    'SocialMediaModel',
    'DataSourceModel',

    # Repositories
    'AnalyticsRepository',

    # Base classes
    'BaseRepository',
    'ReadRepository',
    'WriteRepository',
    'QueryBuilder',
]


def init_database(db_connection=None):
    """
    Initialize database with all tables.

    Args:
        db_connection: Optional DatabaseConnection instance (creates new if None)

    Returns:
        DatabaseConnection instance
    """
    if db_connection is None:
        db_connection = get_db_connection()

    create_all_tables(db_connection)
    return db_connection


def get_models(db_connection=None):
    """
    Get all model instances.

    Convenience function to instantiate all models at once.

    Args:
        db_connection: Optional DatabaseConnection instance (creates new if None)

    Returns:
        Dict of model instances
    """
    if db_connection is None:
        db_connection = get_db_connection()

    return {
        'categories': CategoryModel(db_connection),
        'organizations': OrganizationModel(db_connection),
        'people': PersonModel(db_connection),
        'person_organizations': PersonOrganizationModel(db_connection),
        'compensation': CompensationModel(db_connection),
        'contact_info': ContactInfoModel(db_connection),
        'social_media': SocialMediaModel(db_connection),
        'data_sources': DataSourceModel(db_connection),
    }


def get_analytics(db_connection=None):
    """
    Get analytics repository instance.

    Args:
        db_connection: Optional DatabaseConnection instance (creates new if None)

    Returns:
        AnalyticsRepository instance
    """
    if db_connection is None:
        db_connection = get_db_connection()

    return AnalyticsRepository(db_connection)
