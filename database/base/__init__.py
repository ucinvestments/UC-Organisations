"""
Base infrastructure for database operations.

Provides abstract base classes and utilities following SOLID principles.
"""

from .repository import BaseRepository, ReadRepository, WriteRepository
from .query_builder import QueryBuilder

__all__ = [
    'BaseRepository',
    'ReadRepository',
    'WriteRepository',
    'QueryBuilder'
]
