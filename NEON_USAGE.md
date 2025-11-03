# Neon PostgreSQL Integration Guide

This project uses [Neon](https://neon.com) as its serverless PostgreSQL database provider, with [psycopg3](https://www.psycopg.org/psycopg3/) as the database adapter.

## Quick Start

### 1. Get Your Neon Connection String

1. Go to [Neon Console](https://console.neon.tech)
2. Select your project
3. Navigate to **Connection Details**
4. Copy the connection string (it looks like this):
   ```
   postgresql://user:password@ep-xxxxx-xxxxx.region.aws.neon.tech/neondb?sslmode=require
   ```

### 2. Configure Your Environment

Create a `.env` file in the project root (copy from `.env.example`):

```bash
cp .env.example .env
```

Edit `.env` and add your Neon connection string:

```bash
DATABASE_URL=postgresql://your-user:your-password@ep-xxxxx-xxxxx.us-east-2.aws.neon.tech/neondb?sslmode=require
```

### 3. Install Dependencies

Since you don't want to use venv, install dependencies directly:

```bash
pip install -r requirements.txt
```

This installs:
- `psycopg[binary,pool]` - PostgreSQL adapter with connection pooling
- `python-dotenv` - Environment variable management
- Other project dependencies

### 4. Test Your Connection

```bash
python database/setup.py test
```

This should output something like:
```
INFO:database.connection:Database connection pool created successfully (min=1, max=10)
INFO:database.setup:Testing database connection...
INFO:database.connection:Connection test successful: neondb as your-user
INFO:database.setup:Connected to PostgreSQL: PostgreSQL 16.x on x86_64-pc-linux-gnu
INFO:database.setup:Connection test successful!
```

## Usage Examples

### Basic Query Execution

```python
from database.connection import get_db_connection
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database connection (singleton)
db = get_db_connection()

# Execute a simple SELECT query
results = db.execute(
    "SELECT * FROM organizations WHERE id = %s",
    (1,)
)
print(results)
# Output: [{'id': 1, 'name': 'Academic Affairs', ...}]

# Execute an INSERT query
rows_affected = db.execute(
    "INSERT INTO organizations (name, slug) VALUES (%s, %s)",
    ("New Org", "new-org")
)
print(f"Inserted {rows_affected} rows")
```

### Using Cursor Context Manager

For more control over query execution:

```python
from database.connection import get_db_connection

db = get_db_connection()

# Context manager handles commits and rollbacks automatically
with db.get_cursor() as cur:
    # Execute query with parameters
    cur.execute(
        "SELECT name, description FROM organizations WHERE category_id = %s",
        (5,)
    )

    # Fetch all results
    orgs = cur.fetchall()

    for org in orgs:
        print(f"- {org['name']}: {org['description']}")
```

### Transactions (Multiple Related Queries)

When you need multiple queries to succeed or fail together:

```python
from database.connection import get_db_connection

db = get_db_connection()

# Transaction context manager ensures atomicity
with db.transaction() as (conn, cur):
    # Insert a person
    cur.execute(
        "INSERT INTO people (name, email) VALUES (%s, %s) RETURNING id",
        ("John Doe", "john@example.com")
    )
    person_id = cur.fetchone()['id']

    # Link person to organization
    cur.execute(
        "INSERT INTO person_organizations (person_id, organization_id, title) VALUES (%s, %s, %s)",
        (person_id, 123, "Director")
    )

    # Both queries commit together, or both roll back on error
```

### Simple Scripts

For one-off scripts that don't need the singleton pattern:

```python
from database.connection import create_simple_connection
from dotenv import load_dotenv

load_dotenv()

# Create a new connection pool
db = create_simple_connection()

# Do your work
results = db.execute("SELECT COUNT(*) as total FROM organizations")
print(f"Total organizations: {results[0]['total']}")

# Clean up
db.close_all()
```

### Testing Connection Health

```python
from database.connection import get_db_connection

db = get_db_connection()

# Get connection information
info = db.test_connection()

print(f"Database: {info['database']}")
print(f"User: {info['user']}")
print(f"PostgreSQL Version: {info['version']}")
print(f"Backend PID: {info['backend_pid']}")
```

## Connection Pooling

This application uses `psycopg_pool.ConnectionPool` for efficient connection management:

- **Min connections**: 1 (default)
- **Max connections**: 10 (default)
- **Connection timeout**: 60 seconds
- **Connect timeout**: 30 seconds (allows time for Neon compute activation)

You can customize pool size when creating connections:

```python
from database.connection import DatabaseConnection

# Custom pool size
db = DatabaseConnection(min_conn=2, max_conn=20)
```

## Neon-Specific Optimizations

This integration includes several optimizations for Neon's serverless architecture:

### 1. Extended Connect Timeout (30 seconds)
Allows time for Neon to activate idle databases ("wake from sleep"). This is normal behavior for serverless databases.

### 2. TCP Keepalives
Maintains connection health through Neon's connection pooler:
- Starts checking after 30 seconds of inactivity
- Checks every 10 seconds
- Considers connection dead after 5 failed checks

### 3. Application Name
Set to "uc-organizations-scraper" for easy identification in Neon Console monitoring.

### 4. SSL Enforcement
Automatically adds `sslmode=require` if not present in connection string (Neon requirement).

## Database Schema Setup

### Initialize Database

Create all tables and seed initial data:

```bash
python database/setup.py setup
```

### Reset Database (WARNING: Deletes all data)

```bash
python database/setup.py reset
```

### Sync Organizations

Sync organizations from filesystem to database:

```bash
python database/setup.py sync
```

## Error Handling

The connection module provides detailed error handling:

```python
from database.connection import get_db_connection
import psycopg

db = get_db_connection()

try:
    results = db.execute("SELECT * FROM nonexistent_table")
except psycopg.Error as e:
    print(f"Database error: {e}")
    # Handle database-specific errors
except Exception as e:
    print(f"Unexpected error: {e}")
    # Handle other errors
```

## Best Practices

### ✅ DO

1. **Use parameterized queries** to prevent SQL injection:
   ```python
   # ✅ Good
   db.execute("SELECT * FROM users WHERE id = %s", (user_id,))
   ```

2. **Load environment variables** at application startup:
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

3. **Use transactions** for related operations:
   ```python
   with db.transaction() as (conn, cur):
       # Multiple related queries
   ```

4. **Close connections** when shutting down:
   ```python
   from database.connection import close_db
   close_db()
   ```

### ❌ DON'T

1. **Don't use string formatting** for queries:
   ```python
   # ❌ Bad - SQL injection vulnerability!
   db.execute(f"SELECT * FROM users WHERE id = {user_id}")
   ```

2. **Don't create new connections repeatedly**:
   ```python
   # ❌ Bad - creates new pool each time
   for i in range(100):
       db = DatabaseConnection()  # Don't do this!
   ```

3. **Don't commit inside loops**:
   ```python
   # ❌ Bad - commits after every insert
   for item in items:
       db.execute("INSERT INTO table VALUES (%s)", (item,))

   # ✅ Good - use batch insert or transaction
   with db.transaction() as (conn, cur):
       for item in items:
           cur.execute("INSERT INTO table VALUES (%s)", (item,))
   ```

## Troubleshooting

### Connection Timeout

If you see timeouts, it might be due to:
1. **Cold start**: Neon is waking up from idle state (wait 2-3 seconds and retry)
2. **Network issues**: Check your internet connection
3. **Invalid credentials**: Verify your DATABASE_URL in `.env`

### SSL Required Error

Neon requires SSL connections. The connection module automatically adds `sslmode=require` if missing, but if you still see SSL errors:

1. Check that your connection string includes `?sslmode=require`
2. Verify you're using the correct connection string from Neon Console

### IP Allowlist

If you configured an IP allowlist in Neon:
1. Ensure your current IP is allowed
2. Check [Neon Console > Settings > IP Allow](https://console.neon.tech)

### Database Not Found

If the database doesn't exist:
1. Verify the database name in your connection string
2. Create the database in Neon Console if needed

## Migration from Other Databases

If you're migrating from another PostgreSQL provider:

1. **Export your data** from the old database:
   ```bash
   pg_dump -h old-host -U user -d dbname -f dump.sql
   ```

2. **Import to Neon**:
   ```bash
   psql "postgresql://user:pass@ep-xxx.neon.tech/db?sslmode=require" -f dump.sql
   ```

3. **Update your `.env`** with Neon connection string

4. **Test the connection**:
   ```bash
   python database/setup.py test
   ```

## Additional Resources

- [Neon Documentation](https://neon.com/docs)
- [Neon Python Guide](https://neon.com/docs/guides/python)
- [psycopg3 Documentation](https://www.psycopg.org/psycopg3/docs/)
- [Connection Pooling Guide](https://www.psycopg.org/psycopg3/docs/advanced/pool.html)

## Support

For Neon-specific issues:
- [Neon Community](https://community.neon.tech)
- [Neon Discord](https://discord.gg/neon)
- [Neon Support](https://neon.tech/docs/introduction/support)

For application issues:
- Check the logs in your application
- Review error messages in database/connection.py
- Verify your DATABASE_URL configuration
