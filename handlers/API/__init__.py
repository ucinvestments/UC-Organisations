"""API blueprints exposing domain-specific endpoints."""

from .monitoring.routes import monitoring_api
from .organizations.routes import organizations_api
from .people.routes import people_api
from .scraping.routes import scraping_api

__all__ = [
    "monitoring_api",
    "organizations_api",
    "people_api",
    "scraping_api",
]
