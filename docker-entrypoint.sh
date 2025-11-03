#!/bin/bash
set -e

echo "Starting UC Organizations Scraper..."

# Function to wait for database with retries
wait_for_database() {
    echo "Waiting for Neon database connection..."

    # Try connection test with timeout
    MAX_ATTEMPTS=5
    ATTEMPT=1

    while [ $ATTEMPT -le $MAX_ATTEMPTS ]; do
        echo "Connection attempt $ATTEMPT/$MAX_ATTEMPTS..."

        if timeout 15 python3 -c "
import psycopg
import os
try:
    conn = psycopg.connect(
        os.getenv('DATABASE_URL'),
        connect_timeout=10,
        application_name='uc-scraper-startup'
    )
    conn.close()
    print('✓ Database connection successful')
    exit(0)
except Exception as e:
    print(f'✗ Connection failed: {e}')
    exit(1)
" 2>&1; then
            echo "✓ Database is ready!"
            return 0
        fi

        if [ $ATTEMPT -lt $MAX_ATTEMPTS ]; then
            WAIT_TIME=$((ATTEMPT * 3))
            echo "Waiting ${WAIT_TIME}s before retry..."
            sleep $WAIT_TIME
        fi

        ATTEMPT=$((ATTEMPT + 1))
    done

    echo "WARNING: Could not confirm database connection after $MAX_ATTEMPTS attempts."
    echo "Application will start anyway and retry connections internally."
    return 1
}

# Wait for database (non-blocking if it fails)
wait_for_database || true

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
