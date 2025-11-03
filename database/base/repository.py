"""
Abstract base repository implementing the Repository Pattern.

Follows SOLID principles:
- Single Responsibility: Each repository handles ONE entity
- Open/Closed: Extend via inheritance, not modification
- Liskov Substitution: All repos implement same interface
- Interface Segregation: Separate read/write interfaces
- Dependency Inversion: Depend on abstractions, not concrete DB
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)


class ReadRepository(ABC):
    """
    Abstract interface for read operations.

    Follows Interface Segregation Principle - read-only repositories
    can implement just this interface.
    """

    @abstractmethod
    def find_by_id(self, id: int) -> Optional[Dict[str, Any]]:
        """Find entity by ID."""
        pass

    @abstractmethod
    def find_all(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Find all entities with pagination."""
        pass

    @abstractmethod
    def count(self) -> int:
        """Count total entities."""
        pass


class WriteRepository(ABC):
    """
    Abstract interface for write operations.

    Follows Interface Segregation Principle - write-only repositories
    can implement just this interface.
    """

    @abstractmethod
    def create(self, data: Dict[str, Any]) -> int:
        """Create new entity, return ID."""
        pass

    @abstractmethod
    def update(self, id: int, data: Dict[str, Any]) -> bool:
        """Update entity, return success."""
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        """Delete entity, return success."""
        pass


class BaseRepository(ReadRepository, WriteRepository):
    """
    Abstract base repository providing common CRUD operations.

    Concrete repositories extend this class and provide table-specific logic.
    Follows SOLID principles:
    - Single Responsibility: Handles data access for ONE entity type
    - Open/Closed: Override methods to extend behavior
    - Dependency Inversion: Depends on DatabaseConnection abstraction

    Attributes:
        table_name: Name of the database table
        db: DatabaseConnection instance
    """

    def __init__(self, db, table_name: str):
        """
        Initialize repository.

        Args:
            db: DatabaseConnection instance (dependency injection)
            table_name: Name of the database table
        """
        self.db = db
        self.table_name = table_name
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    @contextmanager
    def transaction(self):
        """
        Context manager for database transactions.

        Usage:
            with repo.transaction():
                repo.create(...)
                repo.update(...)
                # Commits on success, rolls back on exception
        """
        with self.db.get_cursor() as cur:
            try:
                yield cur
            except Exception as e:
                self.logger.error(f"Transaction failed: {e}")
                raise

    # Read operations

    def find_by_id(self, id: int) -> Optional[Dict[str, Any]]:
        """
        Find entity by ID.

        Args:
            id: Entity ID

        Returns:
            Entity dict or None if not found
        """
        with self.db.get_cursor() as cur:
            cur.execute(
                f"SELECT * FROM {self.table_name} WHERE id = %s;",
                (id,)
            )
            return cur.fetchone()

    def find_all(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """
        Find all entities with pagination.

        Args:
            limit: Maximum number of results
            offset: Number of results to skip

        Returns:
            List of entity dicts
        """
        with self.db.get_cursor() as cur:
            cur.execute(
                f"SELECT * FROM {self.table_name} ORDER BY id LIMIT %s OFFSET %s;",
                (limit, offset)
            )
            return cur.fetchall()

    def count(self) -> int:
        """
        Count total entities.

        Returns:
            Total count
        """
        with self.db.get_cursor() as cur:
            cur.execute(f"SELECT COUNT(*) as count FROM {self.table_name};")
            result = cur.fetchone()
            return result['count'] if result else 0

    def exists(self, id: int) -> bool:
        """
        Check if entity exists.

        Args:
            id: Entity ID

        Returns:
            True if exists
        """
        with self.db.get_cursor() as cur:
            cur.execute(
                f"SELECT EXISTS(SELECT 1 FROM {self.table_name} WHERE id = %s) as exists;",
                (id,)
            )
            result = cur.fetchone()
            return result['exists'] if result else False

    # Write operations

    def create(self, data: Dict[str, Any]) -> int:
        """
        Create new entity.

        Args:
            data: Entity data dict (column: value)

        Returns:
            Created entity ID
        """
        columns = list(data.keys())
        values = list(data.values())
        placeholders = ', '.join(['%s'] * len(columns))
        columns_str = ', '.join(columns)

        with self.db.get_cursor() as cur:
            cur.execute(
                f"""
                INSERT INTO {self.table_name} ({columns_str})
                VALUES ({placeholders})
                RETURNING id;
                """,
                values
            )
            result = cur.fetchone()
            return result['id'] if result else None

    def update(self, id: int, data: Dict[str, Any]) -> bool:
        """
        Update entity.

        Args:
            id: Entity ID
            data: Updated data dict (column: value)

        Returns:
            True if updated
        """
        if not data:
            return False

        set_clause = ', '.join([f"{col} = %s" for col in data.keys()])
        values = list(data.values()) + [id]

        with self.db.get_cursor() as cur:
            cur.execute(
                f"""
                UPDATE {self.table_name}
                SET {set_clause}, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s;
                """,
                values
            )
            return cur.rowcount > 0

    def delete(self, id: int) -> bool:
        """
        Delete entity.

        Args:
            id: Entity ID

        Returns:
            True if deleted
        """
        with self.db.get_cursor() as cur:
            cur.execute(
                f"DELETE FROM {self.table_name} WHERE id = %s;",
                (id,)
            )
            return cur.rowcount > 0

    def upsert(self, unique_fields: List[str], data: Dict[str, Any]) -> int:
        """
        Insert or update on conflict.

        Args:
            unique_fields: List of field names that determine uniqueness
            data: Entity data

        Returns:
            Entity ID
        """
        columns = list(data.keys())
        values = list(data.values())
        placeholders = ', '.join(['%s'] * len(columns))
        columns_str = ', '.join(columns)
        conflict_target = ', '.join(unique_fields)

        # Update all fields except the unique ones
        update_fields = [col for col in columns if col not in unique_fields]
        update_clause = ', '.join([f"{col} = EXCLUDED.{col}" for col in update_fields])

        with self.db.get_cursor() as cur:
            cur.execute(
                f"""
                INSERT INTO {self.table_name} ({columns_str})
                VALUES ({placeholders})
                ON CONFLICT ({conflict_target})
                DO UPDATE SET {update_clause}, updated_at = CURRENT_TIMESTAMP
                RETURNING id;
                """,
                values
            )
            result = cur.fetchone()
            return result['id'] if result else None

    # Bulk operations

    def create_many(self, data_list: List[Dict[str, Any]]) -> List[int]:
        """
        Create multiple entities in one transaction.

        Args:
            data_list: List of entity data dicts

        Returns:
            List of created IDs
        """
        if not data_list:
            return []

        ids = []
        with self.transaction():
            for data in data_list:
                entity_id = self.create(data)
                ids.append(entity_id)

        return ids

    def delete_many(self, ids: List[int]) -> int:
        """
        Delete multiple entities.

        Args:
            ids: List of entity IDs

        Returns:
            Number of deleted entities
        """
        if not ids:
            return 0

        placeholders = ', '.join(['%s'] * len(ids))

        with self.db.get_cursor() as cur:
            cur.execute(
                f"DELETE FROM {self.table_name} WHERE id IN ({placeholders});",
                ids
            )
            return cur.rowcount
