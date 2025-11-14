"""Monitoring endpoints exposing scraper status data."""

from flask import Blueprint, jsonify

from common import state
from common.utils import get_all_scrapers, get_scrape_statistics

monitoring_api = Blueprint("monitoring_api", __name__, url_prefix="/api")


@monitoring_api.get("/status")
def get_status():
    """Provide status information for all detected scrapers."""
    scrapers = get_all_scrapers()
    payload = []

    for scraper in scrapers:
        stats = get_scrape_statistics(scraper["org_dir"])
        stats["display_name"] = scraper["name"]
        stats["is_running"] = scraper["org_dir"] in state.running_scrapers
        if scraper["org_dir"] in state.scraper_results:
            stats["last_result"] = state.scraper_results[scraper["org_dir"]]
        payload.append(stats)

    return jsonify(payload)
