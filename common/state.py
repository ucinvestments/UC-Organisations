"""Shared mutable state for scraper execution tracking."""

from typing import Dict, Any

# Track active scraper threads keyed by org_dir.
running_scrapers: Dict[str, Dict[str, Any]] = {}

# Store last known scraper results keyed by org_dir.
scraper_results: Dict[str, Dict[str, Any]] = {}
