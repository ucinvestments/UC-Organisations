"""
Contact Info model.

Single Responsibility: Provide data access methods for contact_info table.

Polymorphic table for both people and organizations.
"""

from typing import List, Optional, Dict, Any
from ..base.repository import BaseRepository


class ContactInfoModel(BaseRepository):
    """
    Model for contact information (emails, phones, addresses).

    Polymorphic: works for both people and organizations.
    """

    def __init__(self, db):
        """
        Initialize contact info model.

        Args:
            db: DatabaseConnection instance
        """
        super().__init__(db, 'contact_info')

    def get_by_entity(
        self,
        entity_type: str,
        entity_id: int,
        contact_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get all contact info for an entity.

        Args:
            entity_type: 'person' or 'organization'
            entity_id: Entity ID
            contact_type: Optional filter by contact type

        Returns:
            List of contact info records
        """
        with self.db.get_cursor() as cur:
            if contact_type:
                cur.execute("""
                    SELECT * FROM contact_info
                    WHERE entity_type = %s
                    AND entity_id = %s
                    AND contact_type = %s
                    ORDER BY is_primary DESC, contact_type, created_at;
                """, (entity_type, entity_id, contact_type))
            else:
                cur.execute("""
                    SELECT * FROM contact_info
                    WHERE entity_type = %s
                    AND entity_id = %s
                    ORDER BY is_primary DESC, contact_type, created_at;
                """, (entity_type, entity_id))
            return cur.fetchall()

    def get_primary_contact(
        self,
        entity_type: str,
        entity_id: int,
        contact_type: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get primary contact of a specific type.

        Args:
            entity_type: 'person' or 'organization'
            entity_id: Entity ID
            contact_type: Contact type (e.g., 'email', 'phone')

        Returns:
            Primary contact record or None
        """
        with self.db.get_cursor() as cur:
            cur.execute("""
                SELECT * FROM contact_info
                WHERE entity_type = %s
                AND entity_id = %s
                AND contact_type = %s
                AND is_primary = TRUE
                LIMIT 1;
            """, (entity_type, entity_id, contact_type))
            return cur.fetchone()

    def get_public_contacts(
        self,
        entity_type: str,
        entity_id: int
    ) -> List[Dict[str, Any]]:
        """
        Get all public contact info for an entity.

        Args:
            entity_type: 'person' or 'organization'
            entity_id: Entity ID

        Returns:
            List of public contact info records
        """
        with self.db.get_cursor() as cur:
            cur.execute("""
                SELECT * FROM contact_info
                WHERE entity_type = %s
                AND entity_id = %s
                AND is_public = TRUE
                ORDER BY is_primary DESC, contact_type;
            """, (entity_type, entity_id))
            return cur.fetchall()

    def find_by_value(
        self,
        contact_value: str,
        entity_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Find entities by contact value (e.g., find person by email).

        Args:
            contact_value: Contact value to search
            entity_type: Optional filter by entity type

        Returns:
            List of contact info records
        """
        with self.db.get_cursor() as cur:
            if entity_type:
                cur.execute("""
                    SELECT * FROM contact_info
                    WHERE contact_value = %s
                    AND entity_type = %s;
                """, (contact_value, entity_type))
            else:
                cur.execute("""
                    SELECT * FROM contact_info
                    WHERE contact_value = %s;
                """, (contact_value,))
            return cur.fetchall()

    def search_contacts(
        self,
        query: str,
        entity_type: Optional[str] = None,
        contact_type: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Search contact info by partial match.

        Args:
            query: Search query
            entity_type: Optional filter by entity type
            contact_type: Optional filter by contact type
            limit: Max results

        Returns:
            List of matching contact info
        """
        with self.db.get_cursor() as cur:
            where_clauses = ["LOWER(contact_value) LIKE LOWER(%s)"]
            params = [f'%{query}%']

            if entity_type:
                where_clauses.append("entity_type = %s")
                params.append(entity_type)

            if contact_type:
                where_clauses.append("contact_type = %s")
                params.append(contact_type)

            query_sql = f"""
                SELECT * FROM contact_info
                WHERE {' AND '.join(where_clauses)}
                ORDER BY is_primary DESC, entity_type, entity_id
                LIMIT %s;
            """
            params.append(limit)

            cur.execute(query_sql, params)
            return cur.fetchall()

    def upsert_contact(
        self,
        entity_type: str,
        entity_id: int,
        contact_type: str,
        contact_value: str,
        contact_label: Optional[str] = None,
        is_primary: bool = False,
        is_public: bool = True,
        **kwargs
    ) -> int:
        """
        Insert or update contact info.

        Args:
            entity_type: 'person' or 'organization'
            entity_id: Entity ID
            contact_type: Contact type
            contact_value: Contact value
            contact_label: Optional label
            is_primary: Primary contact flag
            is_public: Public visibility flag
            **kwargs: Additional fields

        Returns:
            Contact info ID
        """
        data = {
            'entity_type': entity_type,
            'entity_id': entity_id,
            'contact_type': contact_type,
            'contact_value': contact_value,
            'contact_label': contact_label,
            'is_primary': is_primary,
            'is_public': is_public,
            **kwargs
        }

        return self.upsert(
            unique_fields=['entity_type', 'entity_id', 'contact_type', 'contact_value'],
            data=data
        )
