"""
Composable SQL Query Builder.

Follows UNIX philosophy:
- Do one thing well: Build SQL queries
- Composability: Chain methods to build complex queries
- Text interface: Outputs SQL strings

Example:
    query = (QueryBuilder('organizations')
        .select(['name', 'slug'])
        .where('category_id', '=', 1)
        .where('is_active', '=', True)
        .order_by('name', 'ASC')
        .limit(10))

    sql, params = query.build()
"""

from typing import List, Dict, Any, Tuple, Optional
from enum import Enum


class JoinType(Enum):
    """SQL join types."""
    INNER = "INNER JOIN"
    LEFT = "LEFT JOIN"
    RIGHT = "RIGHT JOIN"
    FULL = "FULL OUTER JOIN"


class QueryBuilder:
    """
    Composable query builder for SELECT statements.

    Follows builder pattern for chainable method calls.
    """

    def __init__(self, table: str):
        """
        Initialize query builder.

        Args:
            table: Base table name
        """
        self._table = table
        self._select_fields: List[str] = ['*']
        self._joins: List[Dict[str, Any]] = []
        self._where_clauses: List[Dict[str, Any]] = []
        self._order_by_clauses: List[Tuple[str, str]] = []
        self._group_by_fields: List[str] = []
        self._having_clauses: List[Dict[str, Any]] = []
        self._limit_value: Optional[int] = None
        self._offset_value: Optional[int] = None
        self._params: List[Any] = []

    def select(self, fields: List[str]) -> 'QueryBuilder':
        """
        Select specific fields.

        Args:
            fields: List of field names or expressions

        Returns:
            Self for chaining
        """
        self._select_fields = fields
        return self

    def join(
        self,
        table: str,
        on_clause: str,
        join_type: JoinType = JoinType.INNER
    ) -> 'QueryBuilder':
        """
        Add a JOIN clause.

        Args:
            table: Table to join
            on_clause: ON condition (e.g., "users.id = posts.user_id")
            join_type: Type of join

        Returns:
            Self for chaining
        """
        self._joins.append({
            'table': table,
            'on': on_clause,
            'type': join_type
        })
        return self

    def where(self, field: str, operator: str, value: Any) -> 'QueryBuilder':
        """
        Add a WHERE clause.

        Args:
            field: Field name
            operator: Comparison operator (=, !=, >, <, >=, <=, LIKE, IN, etc.)
            value: Comparison value

        Returns:
            Self for chaining
        """
        self._where_clauses.append({
            'field': field,
            'operator': operator,
            'value': value,
            'connector': 'AND'
        })
        return self

    def where_or(self, field: str, operator: str, value: Any) -> 'QueryBuilder':
        """
        Add a WHERE clause with OR connector.

        Args:
            field: Field name
            operator: Comparison operator
            value: Comparison value

        Returns:
            Self for chaining
        """
        self._where_clauses.append({
            'field': field,
            'operator': operator,
            'value': value,
            'connector': 'OR'
        })
        return self

    def where_in(self, field: str, values: List[Any]) -> 'QueryBuilder':
        """
        Add a WHERE IN clause.

        Args:
            field: Field name
            values: List of values

        Returns:
            Self for chaining
        """
        self._where_clauses.append({
            'field': field,
            'operator': 'IN',
            'value': values,
            'connector': 'AND'
        })
        return self

    def where_null(self, field: str, is_null: bool = True) -> 'QueryBuilder':
        """
        Add a WHERE NULL/NOT NULL clause.

        Args:
            field: Field name
            is_null: True for IS NULL, False for IS NOT NULL

        Returns:
            Self for chaining
        """
        operator = 'IS NULL' if is_null else 'IS NOT NULL'
        self._where_clauses.append({
            'field': field,
            'operator': operator,
            'value': None,
            'connector': 'AND'
        })
        return self

    def order_by(self, field: str, direction: str = 'ASC') -> 'QueryBuilder':
        """
        Add an ORDER BY clause.

        Args:
            field: Field name
            direction: 'ASC' or 'DESC'

        Returns:
            Self for chaining
        """
        self._order_by_clauses.append((field, direction.upper()))
        return self

    def group_by(self, fields: List[str]) -> 'QueryBuilder':
        """
        Add a GROUP BY clause.

        Args:
            fields: List of field names

        Returns:
            Self for chaining
        """
        self._group_by_fields = fields
        return self

    def having(self, field: str, operator: str, value: Any) -> 'QueryBuilder':
        """
        Add a HAVING clause (for GROUP BY queries).

        Args:
            field: Field name or aggregate function
            operator: Comparison operator
            value: Comparison value

        Returns:
            Self for chaining
        """
        self._having_clauses.append({
            'field': field,
            'operator': operator,
            'value': value,
            'connector': 'AND'
        })
        return self

    def limit(self, limit: int) -> 'QueryBuilder':
        """
        Add a LIMIT clause.

        Args:
            limit: Maximum number of results

        Returns:
            Self for chaining
        """
        self._limit_value = limit
        return self

    def offset(self, offset: int) -> 'QueryBuilder':
        """
        Add an OFFSET clause.

        Args:
            offset: Number of results to skip

        Returns:
            Self for chaining
        """
        self._offset_value = offset
        return self

    def build(self) -> Tuple[str, List[Any]]:
        """
        Build the SQL query and parameter list.

        Returns:
            Tuple of (SQL string, parameter list)
        """
        self._params = []
        parts = []

        # SELECT
        fields_str = ', '.join(self._select_fields)
        parts.append(f"SELECT {fields_str}")

        # FROM
        parts.append(f"FROM {self._table}")

        # JOINs
        for join in self._joins:
            parts.append(f"{join['type'].value} {join['table']} ON {join['on']}")

        # WHERE
        if self._where_clauses:
            where_parts = []
            for i, clause in enumerate(self._where_clauses):
                connector = clause['connector'] if i > 0 else ''

                if clause['operator'] == 'IN':
                    placeholders = ', '.join(['%s'] * len(clause['value']))
                    where_parts.append(f"{connector} {clause['field']} IN ({placeholders})")
                    self._params.extend(clause['value'])
                elif clause['operator'] in ('IS NULL', 'IS NOT NULL'):
                    where_parts.append(f"{connector} {clause['field']} {clause['operator']}")
                else:
                    where_parts.append(f"{connector} {clause['field']} {clause['operator']} %s")
                    self._params.append(clause['value'])

            parts.append("WHERE " + ' '.join(where_parts))

        # GROUP BY
        if self._group_by_fields:
            group_str = ', '.join(self._group_by_fields)
            parts.append(f"GROUP BY {group_str}")

        # HAVING
        if self._having_clauses:
            having_parts = []
            for i, clause in enumerate(self._having_clauses):
                connector = clause['connector'] if i > 0 else ''
                having_parts.append(f"{connector} {clause['field']} {clause['operator']} %s")
                self._params.append(clause['value'])

            parts.append("HAVING " + ' '.join(having_parts))

        # ORDER BY
        if self._order_by_clauses:
            order_parts = [f"{field} {direction}" for field, direction in self._order_by_clauses]
            parts.append("ORDER BY " + ', '.join(order_parts))

        # LIMIT
        if self._limit_value is not None:
            parts.append(f"LIMIT {self._limit_value}")

        # OFFSET
        if self._offset_value is not None:
            parts.append(f"OFFSET {self._offset_value}")

        sql = ' '.join(parts) + ';'
        return sql, self._params

    def __str__(self) -> str:
        """String representation (returns SQL)."""
        sql, _ = self.build()
        return sql

    def __repr__(self) -> str:
        """Repr showing query details."""
        sql, params = self.build()
        return f"QueryBuilder('{self._table}')\nSQL: {sql}\nParams: {params}"


class InsertBuilder:
    """Builder for INSERT statements."""

    def __init__(self, table: str):
        """
        Initialize insert builder.

        Args:
            table: Table name
        """
        self._table = table
        self._data: Dict[str, Any] = {}
        self._on_conflict_fields: Optional[List[str]] = None
        self._update_on_conflict: bool = False

    def values(self, data: Dict[str, Any]) -> 'InsertBuilder':
        """
        Set values to insert.

        Args:
            data: Dict of column: value

        Returns:
            Self for chaining
        """
        self._data = data
        return self

    def on_conflict(self, fields: List[str], update: bool = True) -> 'InsertBuilder':
        """
        Add ON CONFLICT clause (UPSERT).

        Args:
            fields: Conflict target fields
            update: Whether to update on conflict (vs DO NOTHING)

        Returns:
            Self for chaining
        """
        self._on_conflict_fields = fields
        self._update_on_conflict = update
        return self

    def build(self) -> Tuple[str, List[Any]]:
        """
        Build the INSERT SQL and parameters.

        Returns:
            Tuple of (SQL string, parameter list)
        """
        columns = list(self._data.keys())
        values = list(self._data.values())
        placeholders = ', '.join(['%s'] * len(columns))
        columns_str = ', '.join(columns)

        parts = [f"INSERT INTO {self._table} ({columns_str}) VALUES ({placeholders})"]

        if self._on_conflict_fields:
            conflict_target = ', '.join(self._on_conflict_fields)
            parts.append(f"ON CONFLICT ({conflict_target})")

            if self._update_on_conflict:
                update_fields = [col for col in columns if col not in self._on_conflict_fields]
                update_clause = ', '.join([f"{col} = EXCLUDED.{col}" for col in update_fields])
                parts.append(f"DO UPDATE SET {update_clause}, updated_at = CURRENT_TIMESTAMP")
            else:
                parts.append("DO NOTHING")

        parts.append("RETURNING id")

        sql = ' '.join(parts) + ';'
        return sql, values
