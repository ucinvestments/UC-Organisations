"""Database connection for Neon PostgreSQL."""

import os
from contextlib import contextmanager

import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()


@contextmanager
def get_connection():
    """Get database connection."""
    with psycopg.connect(os.getenv("DATABASE_URL")) as conn:
        yield conn


@contextmanager
def get_cursor(row_factory=dict_row):
    """Get database cursor with dict rows."""
    with psycopg.connect(os.getenv("DATABASE_URL")) as conn:
        with conn.cursor(row_factory=row_factory) as cur:
            yield cur


# Legacy compatibility
class DatabaseConnection:
    def get_cursor(self, row_factory=dict_row):
        return get_cursor(row_factory)


def get_db_connection():
    return DatabaseConnection()


def close_db():
    pass
