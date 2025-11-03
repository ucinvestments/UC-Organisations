"""
Organization model.

Single Responsibility: Provide data access methods for organizations table.

Handles hierarchical organizations (orgs with departments as children).
"""

from typing import List, Optional, Dict, Any
from ..base.repository import BaseRepository


class OrganizationModel(BaseRepository):
    """
    Model for organizations with hierarchical support.

    Organizations can have parent organizations (parent_id).
    Consolidates both organizations and departments into one table.

    Example hierarchy:
        UC Berkeley (parent_id=NULL)
        └── CS Department (parent_id=123)
            └── AI Lab (parent_id=456)
    """

    def __init__(self, db):
        """
        Initialize organization model.

        Args:
            db: DatabaseConnection instance
        """
        super().__init__(db, 'organizations')

    def find_by_slug(self, slug: str, parent_id: Optional[int] = None) -> Optional[Dict[str, Any]]:
        """
        Find organization by slug (within parent if specified).

        Args:
            slug: Organization slug
            parent_id: Optional parent organization ID

        Returns:
            Organization dict or None
        """
        with self.db.get_cursor() as cur:
            if parent_id is not None:
                cur.execute("""
                    SELECT * FROM organizations
                    WHERE slug = %s AND parent_id = %s;
                """, (slug, parent_id))
            else:
                cur.execute("""
                    SELECT * FROM organizations
                    WHERE slug = %s AND parent_id IS NULL;
                """, (slug,))
            return cur.fetchone()

    def find_by_directory_path(self, directory_path: str) -> Optional[Dict[str, Any]]:
        """
        Find organization by directory path.

        Args:
            directory_path: Full directory path (e.g., "handlers/campuses/ucla")

        Returns:
            Organization dict or None
        """
        with self.db.get_cursor() as cur:
            cur.execute("""
                SELECT * FROM organizations
                WHERE directory_path = %s;
            """, (directory_path,))
            return cur.fetchone()

    def get_root_organizations(self, category_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get all root (top-level) organizations.

        Args:
            category_id: Optional filter by category

        Returns:
            List of organization dicts
        """
        with self.db.get_cursor() as cur:
            if category_id is not None:
                cur.execute("""
                    SELECT * FROM organizations
                    WHERE parent_id IS NULL
                    AND category_id = %s
                    AND is_active = TRUE
                    ORDER BY name;
                """, (category_id,))
            else:
                cur.execute("""
                    SELECT * FROM organizations
                    WHERE parent_id IS NULL
                    AND is_active = TRUE
                    ORDER BY name;
                """)
            return cur.fetchall()

    def get_children(self, parent_id: int) -> List[Dict[str, Any]]:
        """
        Get direct children of an organization.

        Args:
            parent_id: Parent organization ID

        Returns:
            List of child organization dicts
        """
        with self.db.get_cursor() as cur:
            cur.execute("""
                SELECT * FROM organizations
                WHERE parent_id = %s
                AND is_active = TRUE
                ORDER BY name;
            """, (parent_id,))
            return cur.fetchall()

    def get_all_descendants(self, org_id: int) -> List[Dict[str, Any]]:
        """
        Get all descendants (children, grandchildren, etc.) recursively.

        Uses PostgreSQL recursive CTE.

        Args:
            org_id: Root organization ID

        Returns:
            List of all descendant organizations
        """
        with self.db.get_cursor() as cur:
            cur.execute("""
                WITH RECURSIVE descendants AS (
                    -- Base case: direct children
                    SELECT * FROM organizations
                    WHERE parent_id = %s

                    UNION ALL

                    -- Recursive case: children of children
                    SELECT o.* FROM organizations o
                    INNER JOIN descendants d ON o.parent_id = d.id
                )
                SELECT * FROM descendants
                ORDER BY hierarchy_level, name;
            """, (org_id,))
            return cur.fetchall()

    def get_ancestors(self, org_id: int) -> List[Dict[str, Any]]:
        """
        Get all ancestors (parent, grandparent, etc.) recursively.

        Uses PostgreSQL recursive CTE.

        Args:
            org_id: Organization ID

        Returns:
            List of ancestor organizations (root to immediate parent)
        """
        with self.db.get_cursor() as cur:
            cur.execute("""
                WITH RECURSIVE ancestors AS (
                    -- Base case: the organization itself
                    SELECT * FROM organizations
                    WHERE id = %s

                    UNION ALL

                    -- Recursive case: parent organizations
                    SELECT o.* FROM organizations o
                    INNER JOIN ancestors a ON o.id = a.parent_id
                )
                SELECT * FROM ancestors
                WHERE id != %s
                ORDER BY hierarchy_level;
            """, (org_id, org_id))
            return cur.fetchall()

    def get_full_hierarchy_path(self, org_id: int) -> str:
        """
        Get full hierarchy path string (e.g., "UC Berkeley > CS Dept > AI Lab").

        Args:
            org_id: Organization ID

        Returns:
            Full path string
        """
        ancestors = self.get_ancestors(org_id)
        org = self.find_by_id(org_id)
        if not org:
            return ""

        path_parts = [a['name'] for a in ancestors] + [org['name']]
        return " > ".join(path_parts)

    def search_by_name(self, query: str, category_id: Optional[int] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Search organizations by name (case-insensitive, partial match).

        Args:
            query: Search query
            category_id: Optional filter by category
            limit: Max results

        Returns:
            List of matching organizations
        """
        with self.db.get_cursor() as cur:
            if category_id is not None:
                cur.execute("""
                    SELECT * FROM organizations
                    WHERE LOWER(name) LIKE LOWER(%s)
                    AND category_id = %s
                    AND is_active = TRUE
                    ORDER BY name
                    LIMIT %s;
                """, (f'%{query}%', category_id, limit))
            else:
                cur.execute("""
                    SELECT * FROM organizations
                    WHERE LOWER(name) LIKE LOWER(%s)
                    AND is_active = TRUE
                    ORDER BY name
                    LIMIT %s;
                """, (f'%{query}%', limit))
            return cur.fetchall()

    def upsert_organization(
        self,
        slug: str,
        name: str,
        parent_id: Optional[int] = None,
        category_id: Optional[int] = None,
        directory_path: Optional[str] = None,
        **kwargs
    ) -> int:
        """
        Insert or update organization.

        Args:
            slug: Unique slug (within parent)
            name: Organization name
            parent_id: Optional parent organization ID
            category_id: Optional category ID
            directory_path: Optional directory path
            **kwargs: Additional fields (description, main_url, etc.)

        Returns:
            Organization ID
        """
        data = {
            'slug': slug,
            'name': name,
            'parent_id': parent_id,
            'category_id': category_id,
            'directory_path': directory_path,
            **kwargs
        }

        # If directory_path provided, use it as unique constraint
        if directory_path:
            return self.upsert(
                unique_fields=['directory_path'],
                data=data
            )
        else:
            # Otherwise use parent_id + slug
            return self.upsert(
                unique_fields=['parent_id', 'slug'],
                data=data
            )
