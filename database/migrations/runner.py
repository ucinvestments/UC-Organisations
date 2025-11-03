"""
Migration runner.

Manages database schema versions and applies migrations in order.
"""

import logging
import importlib
from pathlib import Path
from typing import List, Tuple, Optional

logger = logging.getLogger(__name__)


class MigrationRunner:
    """
    Runs database migrations in order.

    Tracks schema version in a migrations table.
    """

    def __init__(self, db_connection):
        """
        Initialize migration runner.

        Args:
            db_connection: DatabaseConnection instance
        """
        self.db = db_connection
        self._ensure_migrations_table()

    def _ensure_migrations_table(self):
        """Create migrations tracking table if it doesn't exist."""
        with self.db.get_cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    id SERIAL PRIMARY KEY,
                    version VARCHAR(50) NOT NULL UNIQUE,
                    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    description TEXT
                );
            """)
            logger.debug("Migrations table ensured")

    def get_applied_migrations(self) -> List[str]:
        """
        Get list of applied migration versions.

        Returns:
            List of version strings (e.g., ['001', '002'])
        """
        with self.db.get_cursor() as cur:
            cur.execute("""
                SELECT version FROM schema_migrations
                ORDER BY version;
            """)
            return [row['version'] for row in cur.fetchall()]

    def get_available_migrations(self) -> List[Tuple[str, str]]:
        """
        Get list of available migration files.

        Returns:
            List of (version, file_path) tuples
        """
        migrations_dir = Path(__file__).parent
        migration_files = sorted(migrations_dir.glob('[0-9][0-9][0-9]_*.py'))

        migrations = []
        for file_path in migration_files:
            # Extract version from filename (e.g., '001' from '001_initial_schema.py')
            version = file_path.stem.split('_')[0]
            migrations.append((version, str(file_path)))

        return migrations

    def get_pending_migrations(self) -> List[Tuple[str, str]]:
        """
        Get list of migrations that haven't been applied.

        Returns:
            List of (version, file_path) tuples
        """
        applied = set(self.get_applied_migrations())
        available = self.get_available_migrations()

        return [(v, p) for v, p in available if v not in applied]

    def mark_migration_applied(self, version: str, description: str = ""):
        """
        Mark migration as applied in database.

        Args:
            version: Migration version
            description: Optional description
        """
        with self.db.get_cursor() as cur:
            cur.execute("""
                INSERT INTO schema_migrations (version, description)
                VALUES (%s, %s)
                ON CONFLICT (version) DO NOTHING;
            """, (version, description))
            logger.info(f"Marked migration {version} as applied")

    def mark_migration_rolled_back(self, version: str):
        """
        Remove migration from applied list.

        Args:
            version: Migration version
        """
        with self.db.get_cursor() as cur:
            cur.execute("""
                DELETE FROM schema_migrations
                WHERE version = %s;
            """, (version,))
            logger.info(f"Marked migration {version} as rolled back")

    def apply_migration(self, version: str, file_path: str):
        """
        Apply a single migration.

        Args:
            version: Migration version
            file_path: Path to migration file
        """
        # Import migration module
        module_name = Path(file_path).stem
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Run migration
        logger.info(f"Applying migration {version}...")
        module.up(self.db)

        # Mark as applied
        description = module.__doc__.split('\n')[0] if module.__doc__ else ""
        self.mark_migration_applied(version, description)

    def rollback_migration(self, version: str, file_path: str):
        """
        Rollback a single migration.

        Args:
            version: Migration version
            file_path: Path to migration file
        """
        # Import migration module
        module_name = Path(file_path).stem
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Run rollback
        logger.info(f"Rolling back migration {version}...")
        module.down(self.db)

        # Mark as rolled back
        self.mark_migration_rolled_back(version)

    def migrate_up(self, target_version: Optional[str] = None):
        """
        Apply all pending migrations up to target version.

        Args:
            target_version: Optional target version (applies all if None)
        """
        pending = self.get_pending_migrations()

        if not pending:
            logger.info("No pending migrations")
            return

        for version, file_path in pending:
            if target_version and version > target_version:
                break

            self.apply_migration(version, file_path)

        logger.info("All migrations applied successfully")

    def migrate_down(self, target_version: Optional[str] = None):
        """
        Rollback migrations down to target version.

        Args:
            target_version: Target version to rollback to (rolls back all if None)
        """
        applied = self.get_applied_migrations()
        available = dict(self.get_available_migrations())

        # Rollback in reverse order
        for version in reversed(applied):
            if target_version and version <= target_version:
                break

            file_path = available.get(version)
            if not file_path:
                logger.warning(f"Migration file not found for version {version}, skipping...")
                continue

            self.rollback_migration(version, file_path)

        logger.info("Rollback completed successfully")

    def status(self) -> dict:
        """
        Get migration status.

        Returns:
            Dict with applied and pending migrations
        """
        applied = self.get_applied_migrations()
        pending = self.get_pending_migrations()

        return {
            'applied': applied,
            'pending': [v for v, _ in pending],
            'current_version': applied[-1] if applied else None
        }
