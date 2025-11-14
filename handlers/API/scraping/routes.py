"""Endpoints for triggering scraper runs."""

import threading
from datetime import datetime
from typing import Optional, Type

from flask import Blueprint, jsonify

from common import state
from common.utils import get_all_scrapers, load_scraper_module


scraping_api = Blueprint("scraping_api", __name__, url_prefix="/scrape")


def _find_scraper_class(module) -> Optional[Type]:
    """Locate the concrete scraper class within a module."""
    for attr_name in dir(module):
        attr = getattr(module, attr_name)
        if (
            isinstance(attr, type)
            and hasattr(attr, "__bases__")
            and any("BaseScraper" in str(base) for base in attr.__bases__)
        ):
            return attr
    return None


def _schedule_scraper(org_dir: str):
    """Schedule a scraper run for the given organization."""
    if org_dir in state.running_scrapers:
        return False, {"error": "Scraper already running for this organization"}, 400

    module = load_scraper_module(org_dir)
    if not module:
        return False, {"error": f"Scraper not found for {org_dir}"}, 404

    scraper_class = _find_scraper_class(module)
    if not scraper_class:
        return False, {"error": "Scraper class not found in module"}, 500

    def run_scraper():
        try:
            state.running_scrapers[org_dir] = {
                "start_time": datetime.now().isoformat(),
                "status": "running",
            }

            scraper = scraper_class()
            scraper.run()

            state.scraper_results[org_dir] = {
                "status": "completed",
                "end_time": datetime.now().isoformat(),
                "stats": scraper.stats,
            }
        except Exception as exc:  # pragma: no cover - logging could be added later
            state.scraper_results[org_dir] = {
                "status": "failed",
                "end_time": datetime.now().isoformat(),
                "error": str(exc),
            }
        finally:
            state.running_scrapers.pop(org_dir, None)

    thread = threading.Thread(target=run_scraper, daemon=True)
    thread.start()

    return True, {"message": f"Started scraping for {org_dir}", "org_dir": org_dir}, 200


@scraping_api.post("/<path:org_dir>")
def trigger_scrape(org_dir: str):
    """Trigger scraping for a specific organization."""
    success, payload, status = _schedule_scraper(org_dir)
    return jsonify(payload), status


@scraping_api.post("/all")
def trigger_all_scrapes():
    """Trigger scraping for all available organizations."""
    scrapers = get_all_scrapers()
    triggered = []
    skipped = []

    for scraper in scrapers:
        org_dir = scraper["org_dir"]
        success, payload, status = _schedule_scraper(org_dir)
        if success:
            triggered.append(org_dir)
        else:
            skipped.append(org_dir)

    return jsonify(
        {
            "message": f"Triggered {len(triggered)} scrapers",
            "triggered": triggered,
            "skipped": skipped,
        }
    )
