"""Organization data endpoints."""

from flask import Blueprint, jsonify, request

from common.utils import load_organization_data, normalize_name
from database import get_db_connection, OrganizationModel, CategoryModel

organizations_api = Blueprint("organizations_api", __name__, url_prefix="/api")

ORGANIZATION_FIELDS = {
    "name",
    "slug",
    "description",
    "main_url",
    "hierarchy_level",
    "full_path",
    "parent_id",
    "category_id",
    "directory_path",
    "start_date",
    "end_date",
    "is_active",
}


@organizations_api.get("/organization/<path:org_dir>")
def get_organization(org_dir: str):
    """Return stored organization data for a given directory."""
    org_data = load_organization_data(org_dir)
    if not org_data:
        return jsonify({"error": "Organization not found"}), 404
    return jsonify(org_data)


def _resolve_category(category_model, payload):
    """Resolve category using provided identifiers."""
    if payload.get("category_id") is not None:
        return payload["category_id"]

    category_slug = payload.get("category_slug")
    if not category_slug:
        return None

    category = category_model.find_by_slug(category_slug)
    if not category:
        raise ValueError(f"Category not found for slug '{category_slug}'")
    return category["id"]


def _resolve_parent(org_model, payload):
    """Resolve parent organization id using supplied identifiers."""
    if payload.get("parent_id") is not None:
        return payload["parent_id"]

    directory_path = payload.get("parent_directory_path")
    if directory_path:
        parent = org_model.find_by_directory_path(directory_path)
        if parent:
            return parent["id"]

    parent_slug = payload.get("parent_slug")
    if parent_slug:
        parent = org_model.find_by_slug(parent_slug)
        if parent:
            return parent["id"]

    return None


@organizations_api.post("/organizations")
def create_organization_entry():
    """Create or upsert an organization record."""
    payload = request.get_json(silent=True) or {}
    name = payload.get("name")
    if not name:
        return jsonify({"error": "Organization name is required"}), 400

    slug = payload.get("slug") or normalize_name(name)

    db = get_db_connection()
    org_model = OrganizationModel(db)
    category_model = CategoryModel(db)

    try:
        category_id = _resolve_category(category_model, payload)
        parent_id = _resolve_parent(org_model, payload)

        extra_fields = {
            key: payload.get(key)
            for key in ORGANIZATION_FIELDS
            if key not in {"name", "slug", "parent_id", "category_id", "directory_path"}
            and payload.get(key) is not None
        }

        org_id = org_model.upsert_organization(
            slug=slug,
            name=name,
            parent_id=parent_id,
            category_id=category_id,
            directory_path=payload.get("directory_path"),
            **extra_fields,
        )

        record = org_model.find_by_id(org_id)
        return jsonify(record), 201

    except ValueError as err:
        return jsonify({"error": str(err)}), 400
    except Exception as exc:  # pragma: no cover - surfaced to client
        return jsonify({"error": str(exc)}), 500


def _resolve_organization(org_model, payload):
    """
    Locate an organization using id, directory_path, slug, or name.

    Raises:
        ValueError when multiple matches occur.
    """
    identifier = payload.get("id") or payload.get("organization_id")
    if identifier is not None:
        try:
            identifier = int(identifier)
        except (TypeError, ValueError):
            identifier = None

    if identifier:
        record = org_model.find_by_id(identifier)
        if record:
            return record

    directory_path = payload.get("directory_path")
    if directory_path:
        record = org_model.find_by_directory_path(directory_path)
        if record:
            return record

    slug = payload.get("slug")
    if slug:
        parent_id = payload.get("parent_id")
        record = org_model.find_by_slug(slug, parent_id)
        if record:
            return record
        # Fallback to root-level slug when parent unspecified
        record = org_model.find_by_slug(slug)
        if record:
            return record

    name = payload.get("name")
    if not name and payload.get("lookup"):
        name = payload["lookup"].get("name")
        if payload["lookup"].get("slug") and not slug:
            slug = payload["lookup"]["slug"]

    if not name and slug:
        matches = org_model.search_by_name(slug, limit=2)
    elif name:
        matches = org_model.search_by_name(name, limit=2)
    else:
        matches = []

    if not matches:
        return None

    exact_matches = [
        match for match in matches if match.get("name", "").lower() == (name or slug or "").lower()
    ]

    if len(matches) > 1 and len(exact_matches) != 1:
        raise ValueError("Multiple organizations matched the supplied identifier; provide an ID.")

    return exact_matches[0] if exact_matches else matches[0]


@organizations_api.put("/organizations")
def update_organization_entry():
    """Update organization details."""
    payload = request.get_json(silent=True) or {}
    if not payload:
        return jsonify({"error": "Request body is required"}), 400

    db = get_db_connection()
    org_model = OrganizationModel(db)
    category_model = CategoryModel(db)

    try:
        record = _resolve_organization(org_model, payload)
    except ValueError as err:
        return jsonify({"error": str(err)}), 409

    if not record:
        return jsonify({"error": "Organization not found"}), 404

    updates_source = payload.get("updates", payload)

    try:
        category_id = _resolve_category(category_model, updates_source)
    except ValueError as err:
        return jsonify({"error": str(err)}), 400

    if category_id is not None:
        updates_source["category_id"] = category_id

    parent_id = _resolve_parent(org_model, updates_source)
    if parent_id is not None:
        updates_source["parent_id"] = parent_id

    update_data = {
        key: updates_source.get(key)
        for key in ORGANIZATION_FIELDS
        if updates_source.get(key) is not None
    }

    if not update_data:
        return jsonify({"error": "No updatable fields supplied"}), 400

    org_model.update(record["id"], update_data)
    refreshed = org_model.find_by_id(record["id"])
    return jsonify(refreshed), 200
