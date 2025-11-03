"""
Data Source model.

Single Responsibility: Provide data access methods for data_sources table.

Polymorphic table for tracking data provenance across all entities.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from ..base.repository import BaseRepository


class DataSourceModel(BaseRepository):
    """
    Model for data sources and provenance tracking.

    Polymorphic: works for people, organizations, compensation, etc.
    """

    def __init__(self, db):
        """
        Initialize data source model.

        Args:
            db: DatabaseConnection instance
        """
        super().__init__(db, 'data_sources')

    def get_by_entity(
        self,
        entity_type: str,
        entity_id: int,
        source_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get all data sources for an entity.

        Args:
            entity_type: Entity type (e.g., 'person', 'organization', 'compensation')
            entity_id: Entity ID
            source_type: Optional filter by source type

        Returns:
            List of data source records
        """
        with self.db.get_cursor() as cur:
            if source_type:
                cur.execute("""
                    SELECT * FROM data_sources
                    WHERE entity_type = %s
                    AND entity_id = %s
                    AND source_type = %s
                    ORDER BY scraped_at DESC NULLS LAST, created_at DESC;
                """, (entity_type, entity_id, source_type))
            else:
                cur.execute("""
                    SELECT * FROM data_sources
                    WHERE entity_type = %s
                    AND entity_id = %s
                    ORDER BY scraped_at DESC NULLS LAST, created_at DESC;
                """, (entity_type, entity_id))
            return cur.fetchall()

    def get_verified_sources(
        self,
        entity_type: str,
        entity_id: int
    ) -> List[Dict[str, Any]]:
        """
        Get all verified data sources for an entity.

        Args:
            entity_type: Entity type
            entity_id: Entity ID

        Returns:
            List of verified data source records
        """
        with self.db.get_cursor() as cur:
            cur.execute("""
                SELECT * FROM data_sources
                WHERE entity_type = %s
                AND entity_id = %s
                AND is_verified = TRUE
                ORDER BY verified_at DESC;
            """, (entity_type, entity_id))
            return cur.fetchall()

    def get_by_scraper(
        self,
        scraper_name: str,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get all data sources from a specific scraper.

        Args:
            scraper_name: Scraper name
            limit: Optional max results

        Returns:
            List of data source records
        """
        with self.db.get_cursor() as cur:
            query = """
                SELECT * FROM data_sources
                WHERE scraper_name = %s
                ORDER BY scraped_at DESC
            """
            params = [scraper_name]

            if limit:
                query += " LIMIT %s"
                params.append(limit)

            cur.execute(query, params)
            return cur.fetchall()

    def get_by_import_batch(self, import_batch_id: str) -> List[Dict[str, Any]]:
        """
        Get all data sources from an import batch.

        Args:
            import_batch_id: Import batch ID

        Returns:
            List of data source records
        """
        with self.db.get_cursor() as cur:
            cur.execute("""
                SELECT * FROM data_sources
                WHERE import_batch_id = %s
                ORDER BY imported_at, entity_type, entity_id;
            """, (import_batch_id,))
            return cur.fetchall()

    def get_sources_needing_refresh(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get data sources that need to be re-scraped.

        Returns sources where next_check_at is in the past.

        Args:
            limit: Max results

        Returns:
            List of data source records needing refresh
        """
        with self.db.get_cursor() as cur:
            cur.execute("""
                SELECT * FROM data_sources
                WHERE next_check_at IS NOT NULL
                AND next_check_at <= NOW()
                ORDER BY next_check_at
                LIMIT %s;
            """, (limit,))
            return cur.fetchall()

    def get_public_record_sources(
        self,
        entity_type: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get all public record data sources.

        Args:
            entity_type: Optional filter by entity type
            limit: Optional max results

        Returns:
            List of public record data sources
        """
        with self.db.get_cursor() as cur:
            query = "SELECT * FROM data_sources WHERE is_public_record = TRUE"
            params = []

            if entity_type:
                query += " AND entity_type = %s"
                params.append(entity_type)

            query += " ORDER BY scraped_at DESC"

            if limit:
                query += " LIMIT %s"
                params.append(limit)

            cur.execute(query, params)
            return cur.fetchall()

    def search_by_source_url(
        self,
        url_query: str,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Search data sources by source URL.

        Args:
            url_query: URL search query
            limit: Max results

        Returns:
            List of matching data sources
        """
        with self.db.get_cursor() as cur:
            cur.execute("""
                SELECT * FROM data_sources
                WHERE LOWER(source_url) LIKE LOWER(%s)
                ORDER BY scraped_at DESC
                LIMIT %s;
            """, (f'%{url_query}%', limit))
            return cur.fetchall()

    def get_source_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about data sources.

        Returns:
            Statistics dict with counts by source type, scraper, etc.
        """
        with self.db.get_cursor() as cur:
            cur.execute("""
                SELECT
                    COUNT(*) as total_sources,
                    COUNT(DISTINCT entity_type) as entity_types_count,
                    COUNT(DISTINCT scraper_name) as scrapers_count,
                    COUNT(DISTINCT import_batch_id) as import_batches_count,
                    SUM(CASE WHEN is_verified THEN 1 ELSE 0 END) as verified_count,
                    SUM(CASE WHEN is_public_record THEN 1 ELSE 0 END) as public_record_count
                FROM data_sources;
            """)
            return cur.fetchone() or {}

    def get_sources_by_confidence(
        self,
        confidence_level: str,
        entity_type: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get data sources by confidence level.

        Args:
            confidence_level: 'high', 'medium', 'low', or 'unknown'
            entity_type: Optional filter by entity type
            limit: Max results

        Returns:
            List of data sources
        """
        with self.db.get_cursor() as cur:
            query = "SELECT * FROM data_sources WHERE confidence_level = %s"
            params = [confidence_level]

            if entity_type:
                query += " AND entity_type = %s"
                params.append(entity_type)

            query += " ORDER BY scraped_at DESC LIMIT %s"
            params.append(limit)

            cur.execute(query, params)
            return cur.fetchall()

    def mark_as_verified(
        self,
        source_id: int,
        verified_by: str
    ) -> bool:
        """
        Mark a data source as verified.

        Args:
            source_id: Data source ID
            verified_by: Who verified it

        Returns:
            True if successful
        """
        with self.db.get_cursor() as cur:
            cur.execute("""
                UPDATE data_sources
                SET is_verified = TRUE,
                    verified_by = %s,
                    verified_at = NOW(),
                    updated_at = NOW()
                WHERE id = %s;
            """, (verified_by, source_id))
            return cur.rowcount > 0

    def schedule_next_check(
        self,
        source_id: int,
        check_frequency_days: int
    ) -> bool:
        """
        Schedule next check for a data source.

        Args:
            source_id: Data source ID
            check_frequency_days: Days until next check

        Returns:
            True if successful
        """
        with self.db.get_cursor() as cur:
            cur.execute("""
                UPDATE data_sources
                SET check_frequency_days = %s,
                    next_check_at = NOW() + INTERVAL '%s days',
                    last_checked_at = NOW(),
                    updated_at = NOW()
                WHERE id = %s;
            """, (check_frequency_days, check_frequency_days, source_id))
            return cur.rowcount > 0

    def upsert_source(
        self,
        entity_type: str,
        entity_id: int,
        source_type: str,
        source_url: Optional[str] = None,
        source_name: Optional[str] = None,
        scraper_name: Optional[str] = None,
        confidence_level: str = 'unknown',
        **kwargs
    ) -> int:
        """
        Insert or update data source.

        Args:
            entity_type: Entity type
            entity_id: Entity ID
            source_type: Source type
            source_url: Optional source URL
            source_name: Optional source name
            scraper_name: Optional scraper name
            confidence_level: Confidence level
            **kwargs: Additional fields

        Returns:
            Data source ID
        """
        data = {
            'entity_type': entity_type,
            'entity_id': entity_id,
            'source_type': source_type,
            'source_url': source_url,
            'source_name': source_name,
            'scraper_name': scraper_name,
            'confidence_level': confidence_level,
            **kwargs
        }

        # Use source_url as unique constraint if provided
        # Otherwise data sources are not deduplicated (multiple sources per entity allowed)
        if source_url:
            return self.upsert(
                unique_fields=['entity_type', 'entity_id', 'source_url'],
                data=data
            )
        else:
            # Just insert without deduplication
            return self.create(data)
