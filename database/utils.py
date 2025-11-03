"""
Database utilities for Neon PostgreSQL.

Handles Neon-specific connection patterns like compute activation delays.
"""

import sys
import time
import os
import logging
import psycopg
from typing import Tuple

logger = logging.getLogger(__name__)


def wait_for_neon_database(
    database_url: str,
    max_retries: int = 10,
    initial_timeout: int = 60,
    retry_timeout: int = 20,
) -> Tuple[bool, str]:
    """
    Wait for Neon database to be ready, handling compute activation delays.

    Neon databases use "scale to zero" - they go idle after 5 min of inactivity.
    Waking up an idle compute can take a few hundred milliseconds, plus network latency.

    Strategy:
    1. First attempt: Long timeout (60s) to allow compute activation
    2. Subsequent attempts: Moderate timeout (20s) with incremental backoff
    3. Return detailed error on final failure

    Args:
        database_url: PostgreSQL connection string
        max_retries: Maximum connection attempts (default: 10)
        initial_timeout: Timeout for first connection attempt in seconds (default: 60)
        retry_timeout: Timeout for retry attempts in seconds (default: 20)

    Returns:
        Tuple of (success: bool, message: str)
    """
    if not database_url:
        return False, "DATABASE_URL not provided"

    # Extract host for logging (hide password)
    host = "unknown"
    try:
        url_parts = database_url.split("@")
        if len(url_parts) > 1:
            host = url_parts[1].split("/")[0]
    except Exception:
        pass

    logger.info(f"Connecting to Neon database: {host}")

    # First attempt with long timeout (wake up idle compute)
    logger.info(
        f"Attempt 1/{max_retries} (timeout: {initial_timeout}s - allowing for compute activation)..."
    )
    try:
        with psycopg.connect(
        ) as conn:
            version_info = (
                conn.info.parameter_status("server_version") or conn.info.server_version
            )
        logger.info(f"✓ Connection successful! PostgreSQL version: {version_info}")
        return True, "Connected successfully"
    except psycopg.OperationalError as e:
        error_msg = str(e).strip()
        logger.warning(f"✗ First attempt failed: {error_msg}")
        logger.info("Database may be activating from idle state, retrying...")
    except Exception as e:
        logger.error(f"✗ Unexpected error on first attempt: {type(e).__name__}: {e}")

    # Subsequent attempts with shorter timeout and exponential backoff
    backoff_intervals = [2, 4, 8, 16]  # Exponential backoff in seconds

    for i in range(1, max_retries):
        # Calculate wait time with exponential backoff
        if i - 1 < len(backoff_intervals):
            wait_time = backoff_intervals[i - 1]
        else:
            wait_time = backoff_intervals[-1]  # Cap at max backoff

        logger.info(f"Waiting {wait_time}s before retry...")
        time.sleep(wait_time)

        attempt_num = i + 1
        attempt_timeout = min(retry_timeout + (i - 1) * 5, 45)
        logger.info(
            f"Attempt {attempt_num}/{max_retries} (timeout: {attempt_timeout}s)..."
        )

        try:
            with psycopg.connect(
                conninfo=database_url,
                connect_timeout=attempt_timeout,
                autocommit=True,
                keepalives=1,
                keepalives_idle=30,
                keepalives_interval=10,
                keepalives_count=5,
            ) as conn:
                version_info = (
                    conn.info.parameter_status("server_version")
                    or conn.info.server_version
                )
            logger.info(f"✓ Connection successful! PostgreSQL version: {version_info}")
            return True, "Connected successfully"
        except psycopg.OperationalError as e:
            error_msg = str(e).strip()

            # Check for specific error types
            if "timeout expired" in error_msg.lower():
                logger.warning(
                    f"✗ Connection timeout (compute may still be activating)"
                )
            elif "could not translate host name" in error_msg.lower():
                logger.error(f"✗ DNS resolution failed - check DATABASE_URL")
                return False, f"DNS error: {error_msg}"
            elif "authentication failed" in error_msg.lower():
                logger.error(f"✗ Authentication failed - check credentials")
                return False, f"Auth error: {error_msg}"
            else:
                logger.warning(f"✗ Connection failed: {error_msg}")

        except Exception as e:
            logger.error(f"✗ Unexpected error: {type(e).__name__}: {e}")

    # All retries exhausted
    final_message = (
        f"Failed to connect after {max_retries} attempts. "
        f"Possible causes:\n"
        f"1. Neon database is not active (check Neon dashboard)\n"
        f"2. Network connectivity issue (firewall/proxy)\n"
        f"3. Invalid DATABASE_URL credentials\n"
        f"4. Neon compute is experiencing issues"
    )
    logger.error(final_message)
    return False, final_message


def test_connection_from_env():
    """
    Test database connection using DATABASE_URL from environment.

    Returns:
        Exit code (0 = success, 1 = failure)
    """
    from dotenv import load_dotenv

    load_dotenv()

    database_url = os.getenv("DATABASE_URL")
    success, message = wait_for_neon_database(database_url)

    if success:
        print("✓ Database connection test passed")
        return 0
    else:
        print(f"✗ Database connection test failed: {message}")
        return 1


if __name__ == "__main__":
    # Allow running this module directly to test connection
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    sys.exit(test_connection_from_env())
