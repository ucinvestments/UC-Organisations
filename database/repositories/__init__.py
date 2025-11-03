"""
Repository layer for complex cross-table queries.

Models handle single-table operations.
Repositories handle complex multi-table operations and analytics.
"""

from .analytics import AnalyticsRepository

__all__ = [
    'AnalyticsRepository',
]
