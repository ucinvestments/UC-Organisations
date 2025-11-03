"""
Category model.

Single Responsibility: Provide data access methods for categories table.
"""

from typing import List, Optional, Dict, Any
from ..base.repository import BaseRepository


class CategoryModel(BaseRepository):
    """
    Model for categories (UCOP, Campuses, Labs, Academic Senate, Board of Regents).

    Extends BaseRepository with category-specific queries.
    """

    def __init__(self, db):
        """
        Initialize category model.

        Args:
            db: DatabaseConnection instance
        """
        super().__init__(db, 'categories')

    def find_by_slug(self, slug: str) -> Optional[Dict[str, Any]]:
        """
        Find category by slug.

        Args:
            slug: Category slug (e.g., 'campuses', 'ucop')

        Returns:
            Category dict or None
        """
        with self.db.get_cursor() as cur:
            cur.execute("""
                SELECT * FROM categories
                WHERE slug = %s;
            """, (slug,))
            return cur.fetchone()

    def find_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Find category by name (case-insensitive).

        Args:
            name: Category name (e.g., 'Campuses', 'UCOP')

        Returns:
            Category dict or None
        """
        with self.db.get_cursor() as cur:
            cur.execute("""
                SELECT * FROM categories
                WHERE LOWER(name) = LOWER(%s);
            """, (name,))
            return cur.fetchone()

    def get_all_active(self) -> List[Dict[str, Any]]:
        """
        Get all categories ordered by name.

        Returns:
            List of category dicts
        """
        with self.db.get_cursor() as cur:
            cur.execute("""
                SELECT * FROM categories
                ORDER BY name;
            """)
            return cur.fetchall()

    def get_organization_count(self, category_id: int) -> int:
        """
        Count organizations in this category.

        Args:
            category_id: Category ID

        Returns:
            Number of organizations
        """
        with self.db.get_cursor() as cur:
            cur.execute("""
                SELECT COUNT(*) as count
                FROM organizations
                WHERE category_id = %s;
            """, (category_id,))
            result = cur.fetchone()
            return result['count'] if result else 0

    def upsert_category(self, slug: str, name: str, description: str = None) -> int:
        """
        Insert or update category by slug.

        Args:
            slug: Unique slug
            name: Category name
            description: Optional description

        Returns:
            Category ID
        """
        return self.upsert(
            unique_fields=['slug'],
            data={
                'slug': slug,
                'name': name,
                'description': description
            }
        )
