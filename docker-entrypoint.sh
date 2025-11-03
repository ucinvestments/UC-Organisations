#!/bin/bash
set -e

echo "Starting UC Organizations Scraper..."

# Test database connection once
echo "Testing database connection..."
if timeout 10 python3 -c "
import psycopg
import os
try:
    conn = psycopg.connect(os.getenv('DATABASE_URL'), connect_timeout=5)
    conn.close()
    print('✓ Database connected')
    exit(0)
except Exception as e:
    print(f'✗ Connection failed: {e}')
    exit(1)
" 2>&1; then
    echo "✓ Database ready"
else
    echo "⚠ Database connection failed, continuing anyway..."
fi

# Run database setup (creates tables if they don't exist)
echo ""
echo "Setting up database..."
if python3 database/setup.py setup 2>&1; then
    echo "✓ Database setup complete"
else
    echo "⚠ Database setup encountered issues (may be transient)"
fi

# Sync organizations from filesystem to database
echo ""
echo "Syncing organizations..."
if python3 database/setup.py sync 2>&1; then
    echo "✓ Organizations synced"
else
    echo "⚠ Organization sync encountered issues"
fi

# Start the Flask application
echo ""
echo "=========================================="
echo "Starting Flask application on port 5000..."
echo "=========================================="
exec python3 app.py
