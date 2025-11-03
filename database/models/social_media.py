"""
Social Media model.

Single Responsibility: Provide data access methods for social_media table.

Polymorphic table for both people and organizations.
"""

from typing import List, Optional, Dict, Any
from ..base.repository import BaseRepository


class SocialMediaModel(BaseRepository):
    """
    Model for social media profiles.

    Polymorphic: works for both people and organizations.
    """

    def __init__(self, db):
        """
        Initialize social media model.

        Args:
            db: DatabaseConnection instance
        """
        super().__init__(db, 'social_media')

    def get_by_entity(
        self,
        entity_type: str,
        entity_id: int,
        platform: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get all social media profiles for an entity.

        Args:
            entity_type: 'person' or 'organization'
            entity_id: Entity ID
            platform: Optional filter by platform

        Returns:
            List of social media records
        """
        with self.db.get_cursor() as cur:
            if platform:
                cur.execute("""
                    SELECT * FROM social_media
                    WHERE entity_type = %s
                    AND entity_id = %s
                    AND platform = %s
                    ORDER BY is_verified DESC, is_active DESC, created_at;
                """, (entity_type, entity_id, platform))
            else:
                cur.execute("""
                    SELECT * FROM social_media
                    WHERE entity_type = %s
                    AND entity_id = %s
                    ORDER BY is_verified DESC, is_active DESC, platform;
                """, (entity_type, entity_id))
            return cur.fetchall()

    def get_verified_profiles(
        self,
        entity_type: str,
        entity_id: int
    ) -> List[Dict[str, Any]]:
        """
        Get all verified social media profiles for an entity.

        Args:
            entity_type: 'person' or 'organization'
            entity_id: Entity ID

        Returns:
            List of verified social media records
        """
        with self.db.get_cursor() as cur:
            cur.execute("""
                SELECT * FROM social_media
                WHERE entity_type = %s
                AND entity_id = %s
                AND is_verified = TRUE
                ORDER BY platform;
            """, (entity_type, entity_id))
            return cur.fetchall()

    def find_by_handle(
        self,
        handle: str,
        platform: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Find social media profiles by handle.

        Args:
            handle: Social media handle (e.g., "@username")
            platform: Optional filter by platform

        Returns:
            List of matching social media records
        """
        with self.db.get_cursor() as cur:
            if platform:
                cur.execute("""
                    SELECT * FROM social_media
                    WHERE LOWER(handle) = LOWER(%s)
                    AND platform = %s;
                """, (handle, platform))
            else:
                cur.execute("""
                    SELECT * FROM social_media
                    WHERE LOWER(handle) = LOWER(%s);
                """, (handle,))
            return cur.fetchall()

    def find_by_url(self, profile_url: str) -> Optional[Dict[str, Any]]:
        """
        Find social media profile by URL.

        Args:
            profile_url: Profile URL

        Returns:
            Social media record or None
        """
        with self.db.get_cursor() as cur:
            cur.execute("""
                SELECT * FROM social_media
                WHERE profile_url = %s
                LIMIT 1;
            """, (profile_url,))
            return cur.fetchone()

    def search_profiles(
        self,
        query: str,
        entity_type: Optional[str] = None,
        platform: Optional[str] = None,
        verified_only: bool = False,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Search social media profiles by handle or display name.

        Args:
            query: Search query
            entity_type: Optional filter by entity type
            platform: Optional filter by platform
            verified_only: Only return verified profiles
            limit: Max results

        Returns:
            List of matching social media profiles
        """
        with self.db.get_cursor() as cur:
            where_clauses = [
                "(LOWER(handle) LIKE LOWER(%s) OR LOWER(display_name) LIKE LOWER(%s))"
            ]
            params = [f'%{query}%', f'%{query}%']

            if entity_type:
                where_clauses.append("entity_type = %s")
                params.append(entity_type)

            if platform:
                where_clauses.append("platform = %s")
                params.append(platform)

            if verified_only:
                where_clauses.append("is_verified = TRUE")

            query_sql = f"""
                SELECT * FROM social_media
                WHERE {' AND '.join(where_clauses)}
                ORDER BY is_verified DESC, follower_count DESC NULLS LAST
                LIMIT %s;
            """
            params.append(limit)

            cur.execute(query_sql, params)
            return cur.fetchall()

    def get_by_platform(
        self,
        platform: str,
        verified_only: bool = False,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get all profiles for a specific platform.

        Args:
            platform: Platform name
            verified_only: Only return verified profiles
            limit: Optional max results

        Returns:
            List of social media records
        """
        with self.db.get_cursor() as cur:
            query = "SELECT * FROM social_media WHERE platform = %s"
            params = [platform]

            if verified_only:
                query += " AND is_verified = TRUE"

            query += " ORDER BY follower_count DESC NULLS LAST"

            if limit:
                query += " LIMIT %s"
                params.append(limit)

            cur.execute(query, params)
            return cur.fetchall()

    def get_active_profiles(
        self,
        entity_type: str,
        entity_id: int
    ) -> List[Dict[str, Any]]:
        """
        Get active social media profiles for an entity.

        Args:
            entity_type: 'person' or 'organization'
            entity_id: Entity ID

        Returns:
            List of active social media records
        """
        with self.db.get_cursor() as cur:
            cur.execute("""
                SELECT * FROM social_media
                WHERE entity_type = %s
                AND entity_id = %s
                AND is_active = TRUE
                ORDER BY is_verified DESC, platform;
            """, (entity_type, entity_id))
            return cur.fetchall()

    def upsert_profile(
        self,
        entity_type: str,
        entity_id: int,
        platform: str,
        profile_url: str,
        handle: Optional[str] = None,
        display_name: Optional[str] = None,
        is_verified: bool = False,
        **kwargs
    ) -> int:
        """
        Insert or update social media profile.

        Args:
            entity_type: 'person' or 'organization'
            entity_id: Entity ID
            platform: Platform name
            profile_url: Profile URL
            handle: Optional handle
            display_name: Optional display name
            is_verified: Verified flag
            **kwargs: Additional fields

        Returns:
            Social media ID
        """
        data = {
            'entity_type': entity_type,
            'entity_id': entity_id,
            'platform': platform,
            'profile_url': profile_url,
            'handle': handle,
            'display_name': display_name,
            'is_verified': is_verified,
            **kwargs
        }

        return self.upsert(
            unique_fields=['entity_type', 'entity_id', 'platform', 'profile_url'],
            data=data
        )
