# Database Module

Refactored following **SOLID** principles and **UNIX** philosophy for maintainability and scalability.

## Architecture

The database module is organized into distinct layers, each with a single responsibility:

```
database/
├── connection.py          # Connection pooling & transaction management
├── __init__.py           # Public API exports
├── setup.py              # Database initialization CLI
├── base/                 # Reusable patterns
│   ├── repository.py     # Abstract repository base classes
│   └── query_builder.py  # Composable SQL query builder
├── schema/               # Table definitions (DDL)
│   ├── categories.py
│   ├── organizations.py
│   ├── people.py
│   ├── person_organizations.py
│   ├── compensation.py
│   ├── contact_info.py
│   ├── social_media.py
│   └── data_sources.py
├── models/               # Single-table operations (CRUD)
│   ├── category.py
│   ├── organization.py
│   ├── person.py
│   ├── person_organization.py
│   ├── compensation.py
│   ├── contact_info.py
│   ├── social_media.py
│   └── data_source.py
├── repositories/         # Multi-table queries & analytics
│   └── analytics.py
└── migrations/           # Schema versioning
    ├── runner.py
    └── 001_initial_schema.py
```

## Layers

### 1. Connection Layer (connection.py:1)

Manages PostgreSQL connection pooling with Neon database.

**Features:**
- Connection pooling (min/max connections)
- Auto-commit/rollback with `get_cursor()`
- Explicit transaction control with `transaction()`
- Raw connection access with `get_connection()`
- Convenience `execute()` method

**Usage:**

```python
from database import get_db_connection

db = get_db_connection()

# Simple query
with db.get_cursor() as cur:
    cur.execute("SELECT * FROM people WHERE id = %s", (123,))
    person = cur.fetchone()

# Explicit transaction
with db.transaction() as (conn, cur):
    cur.execute("INSERT INTO people ...")
    person_id = cur.fetchone()['id']
    cur.execute("INSERT INTO person_organizations ...")
    # Both commit together

# Convenience method
results = db.execute("SELECT * FROM people LIMIT 10")
```

### 2. Schema Layer (schema/)

Defines table structures. **One file per table**, following Single Responsibility Principle.

Each file provides:
- `create_<table>_table(db)` - Creates table with indexes
- `drop_<table>_table(db)` - Drops table

**Key Tables:**

- **organizations** (schema/organizations.py:20): Hierarchical structure using `parent_id` self-reference
  - Consolidates organizations AND departments into one table
  - Example: `UC Berkeley > CS Department > AI Lab`

- **compensation** (schema/compensation.py:15): Designed for UCLA salary JSON structure
  - Uses `DECIMAL` types (not strings) for money
  - Tracks `fiscal_year`, `source_employee_id`, `source_location`
  - Supports deduplication via unique constraint

- **Polymorphic tables** (contact_info, social_media, data_sources):
  - Work for both people AND organizations
  - Use `entity_type` + `entity_id` pattern

**Usage:**

```python
from database import create_all_tables, drop_all_tables

# Create all tables
create_all_tables(db)

# Drop all tables
drop_all_tables(db)
```

### 3. Model Layer (models/)

Provides CRUD operations for single tables. **One file per model**.

Each model extends `BaseRepository` with:
- `find_by_id(id)` - Get record by ID
- `create(data)` - Insert new record
- `update(id, data)` - Update existing record
- `delete(id)` - Delete record
- `upsert(unique_fields, data)` - Insert or update
- `find_all(limit)` - Get all records
- Table-specific query methods

**Usage:**

```python
from database import PersonModel, OrganizationModel

db = get_db_connection()
person_model = PersonModel(db)
org_model = OrganizationModel(db)

# Find person by name
people = person_model.find_by_name(first_name="John", last_name="Doe")

# Full-text search
results = person_model.search_full_text("computer science")

# Get organization hierarchy
descendants = org_model.get_all_descendants(org_id=123)
ancestors = org_model.get_ancestors(org_id=456)

# Upsert organization
org_id = org_model.upsert_organization(
    slug="cs-dept",
    name="Computer Science Department",
    parent_id=123,
    category_id=1
)
```

### 4. Repository Layer (repositories/)

Handles complex multi-table queries and analytics.

**Analytics Repository** (repositories/analytics.py:1):

```python
from database import get_analytics

analytics = get_analytics()

# Organization overview with stats
overview = analytics.get_organization_overview(org_id=123, fiscal_year=2023)

# Compensation trends over time
trends = analytics.get_compensation_trends(
    organization_id=123,
    start_year=2018,
    end_year=2023
)

# Person career timeline
timeline = analytics.get_person_career_timeline(person_id=456)

# Advanced people search
results = analytics.search_people_with_context(
    query="John",
    organization_id=123,
    title_query="Professor",
    min_salary=100000,
    fiscal_year=2023
)

# Category statistics
stats = analytics.get_category_statistics()
```

### 5. Base Layer (base/)

Reusable patterns for extending functionality.

**BaseRepository** (base/repository.py:1):

Abstract base class implementing Repository Pattern. Provides:
- `ReadRepository` interface (find_by_id, find_all)
- `WriteRepository` interface (create, update, delete, upsert, bulk_insert)

**QueryBuilder** (base/query_builder.py:1):

Composable SQL query builder following UNIX philosophy.

```python
from database import QueryBuilder

query = (QueryBuilder('organizations')
    .select(['name', 'slug', 'main_url'])
    .where('category_id', '=', 1)
    .where('is_active', '=', True)
    .order_by('name', 'ASC')
    .limit(50))

sql, params = query.build()
# Returns: (SQL string, parameter list)
```

### 6. Migrations Layer (migrations/)

Schema version management with up/down migrations.

**Migration Runner** (migrations/runner.py:1):

```python
from database import get_db_connection
from database.migrations.runner import MigrationRunner

db = get_db_connection()
runner = MigrationRunner(db)

# Check status
status = runner.status()
# {'applied': ['001'], 'pending': ['002', '003'], 'current_version': '001'}

# Apply all pending migrations
runner.migrate_up()

# Apply to specific version
runner.migrate_up(target_version='002')

# Rollback last migration
runner.migrate_down(target_version='001')
```

**Creating Migrations:**

Create file: `migrations/002_add_field.py`

```python
def up(db_connection):
    """Apply migration."""
    with db_connection.get_cursor() as cur:
        cur.execute("""
            ALTER TABLE people
            ADD COLUMN linkedin_url VARCHAR(500);
        """)

def down(db_connection):
    """Rollback migration."""
    with db_connection.get_cursor() as cur:
        cur.execute("""
            ALTER TABLE people
            DROP COLUMN linkedin_url;
        """)
```

## Database Schema

### Core Tables

**categories**
- UC organizational categories (UCOP, Campuses, Labs, Academic Senate, Board of Regents)

**organizations**
- Hierarchical structure using `parent_id`
- Consolidates organizations + departments
- Fields: `name`, `slug`, `parent_id`, `category_id`, `directory_path`, `hierarchy_level`, `full_path`

**people**
- Individual persons separate from organizational affiliations
- Split name fields: `first_name`, `last_name`, `middle_name`, `preferred_name`
- Full-text search index on names

**person_organizations** (junction)
- Links people to organizations with role/title
- Date ranges: `start_date`, `end_date` (NULL = current)
- Flags: `is_current` (generated), `is_primary_affiliation`

**compensation**
- Annual salary data from public records
- Designed for UCLA JSON structure: `{"basepay": "48687.00", "overtimepay": "2184.00", ...}`
- Uses `DECIMAL(12,2)` for all money fields
- Deduplication: `UNIQUE(source_employee_id, source_location, fiscal_year)`

### Polymorphic Tables

Work for both people AND organizations using `entity_type` + `entity_id`.

**contact_info**
- Emails, phones, addresses, fax
- Fields: `contact_type`, `contact_value`, `is_primary`, `is_public`

**social_media**
- LinkedIn, Twitter, Instagram, GitHub, etc.
- Fields: `platform`, `handle`, `profile_url`, `is_verified`

**data_sources**
- Data provenance tracking
- Fields: `source_type`, `source_url`, `scraper_name`, `confidence_level`, `is_verified`
- Freshness tracking: `last_checked_at`, `next_check_at`

## CLI Usage

### Setup Database

```bash
# Create tables and seed categories
python database/setup.py setup

# Drop all tables and recreate (WARNING: deletes data)
python database/setup.py reset

# Sync organizations from filesystem
python database/setup.py sync

# Test database connection
python database/setup.py test
```

### Run Migrations

```bash
# Apply all pending migrations
python -c "from database import get_db_connection; from database.migrations.runner import MigrationRunner; MigrationRunner(get_db_connection()).migrate_up()"

# Check migration status
python -c "from database import get_db_connection; from database.migrations.runner import MigrationRunner; print(MigrationRunner(get_db_connection()).status())"
```

## Convenience Functions

The public API provides helper functions:

```python
from database import init_database, get_models, get_analytics

# Initialize database (create all tables)
db = init_database()

# Get all model instances at once
models = get_models()
# Returns: {'categories': CategoryModel, 'organizations': OrganizationModel, ...}

people = models['people'].find_by_name(first_name="John")

# Get analytics repository
analytics = get_analytics()
overview = analytics.get_organization_overview(org_id=123)
```

## Design Principles

### SOLID Principles

1. **Single Responsibility**: Each file has one job
   - `categories.py` only handles categories table
   - `CategoryModel` only handles category CRUD
   - `AnalyticsRepository` only handles analytics queries

2. **Open/Closed**: Extend via inheritance
   - New models extend `BaseRepository`
   - New tables follow same pattern

3. **Liskov Substitution**: Models are interchangeable
   - All models implement same repository interface

4. **Interface Segregation**: Split read/write interfaces
   - `ReadRepository` vs `WriteRepository`

5. **Dependency Inversion**: Depend on abstractions
   - Models depend on `BaseRepository` interface
   - Database connection injected via constructor

### UNIX Philosophy

1. **Do one thing well**: Each module has single purpose
2. **Composability**: Models/queries can be combined
3. **Text interfaces**: SQL queries, not ORM magic
4. **Separation of concerns**: Schema ≠ Models ≠ Repositories

## Migration from Old Schema

Old monolithic files:
- `database/schema.py` - All table definitions
- `database/models.py` - All models

New structure:
- `database/schema/*.py` - One file per table
- `database/models/*.py` - One file per model

Benefits:
- Easier to find code (search by table name)
- Smaller files, easier to review
- Can modify one table without touching others
- Clear dependency graph
