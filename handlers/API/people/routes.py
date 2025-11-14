"""People endpoints for creating and updating person records."""

from flask import Blueprint, jsonify, request

from database import (
    get_db_connection,
    PersonModel,
    SocialMediaModel,
    ContactInfoModel,
)

people_api = Blueprint("people_api", __name__, url_prefix="/api/people")

PERSON_FIELDS = {
    "first_name",
    "last_name",
    "middle_name",
    "preferred_name",
    "bio",
    "photo_url",
    "profile_url",
    "is_active",
}

SOCIAL_EXTRA_FIELDS = {
    "follower_count",
    "following_count",
    "last_post_date",
    "is_active",
    "is_public",
    "data_source",
    "scraped_at",
}

CONTACT_EXTRA_FIELDS = {
    "contact_label",
    "extension",
    "country_code",
    "is_primary",
    "is_public",
    "is_verified",
    "data_source",
    "scraped_at",
}


def _load_models():
    """Instantiate database-backed models."""
    db = get_db_connection()
    return (
        db,
        PersonModel(db),
        SocialMediaModel(db),
        ContactInfoModel(db),
    )


def _serialize_person(person_model, social_model, contact_model, person_id):
    """Return a hydrated person record with social/contact metadata."""
    person = person_model.find_by_id(person_id)
    if not person:
        return None

    social = social_model.get_by_entity("person", person_id)
    contact = contact_model.get_by_entity("person", person_id)

    person["social_media"] = social or None
    person["contact_info"] = contact or None
    return person


@people_api.post("")
def create_person():
    """Create a person record with optional social media & contact data."""
    payload = request.get_json(silent=True) or {}

    first_name = payload.get("first_name")
    last_name = payload.get("last_name")
    if not first_name or not last_name:
        return (
            jsonify({"error": "first_name and last_name are required"}),
            400,
        )

    person_data = {
        key: payload.get(key)
        for key in PERSON_FIELDS
        if payload.get(key) is not None
    }
    person_data["first_name"] = first_name
    person_data["last_name"] = last_name

    db, person_model, social_model, contact_model = _load_models()
    try:
        person_id = person_model.create(person_data)

        for entry in payload.get("social_media") or []:
            platform = entry.get("platform")
            profile_url = entry.get("profile_url")
            if not platform or not profile_url:
                continue

            social_kwargs = {
                key: entry.get(key)
                for key in SOCIAL_EXTRA_FIELDS
                if entry.get(key) is not None
            }
            social_model.upsert_profile(
                entity_type="person",
                entity_id=person_id,
                platform=platform,
                profile_url=profile_url,
                handle=entry.get("handle"),
                display_name=entry.get("display_name"),
                is_verified=entry.get("is_verified", False),
                **social_kwargs,
            )

        for entry in payload.get("contact_info") or []:
            contact_type = entry.get("contact_type")
            contact_value = entry.get("contact_value")
            if not contact_type or contact_value is None:
                continue

            contact_kwargs = {
                key: entry.get(key)
                for key in CONTACT_EXTRA_FIELDS
                if entry.get(key) is not None
            }
            contact_model.upsert_contact(
                entity_type="person",
                entity_id=person_id,
                contact_type=contact_type,
                contact_value=contact_value,
                **contact_kwargs,
            )

        person = _serialize_person(person_model, social_model, contact_model, person_id)
        return jsonify(person), 201

    except Exception as exc:  # pragma: no cover - surfaced via API
        return jsonify({"error": str(exc)}), 500


def _resolve_person(person_model, identifier, lookup):
    """Resolve a person record by id or name."""
    if identifier is not None:
        try:
            identifier = int(identifier)
        except (TypeError, ValueError):
            identifier = None

    if identifier:
        person = person_model.find_by_id(identifier)
        if person:
            return person

    first_name = lookup.get("first_name")
    last_name = lookup.get("last_name")

    if not first_name and not last_name:
        return None

    matches = person_model.find_by_name(first_name, last_name, limit=2)
    if not matches:
        return None

    exact_matches = [
        match
        for match in matches
        if (first_name or "").lower() in (match.get("first_name") or "").lower()
        and (last_name or "").lower() in (match.get("last_name") or "").lower()
    ]

    if len(matches) > 1 and len(exact_matches) != 1:
        raise ValueError("Multiple people matched the supplied name; provide an ID.")

    return exact_matches[0] if exact_matches else matches[0]


@people_api.put("")
def update_person():
    """Update core person fields and optional social/contact records."""
    payload = request.get_json(silent=True) or {}
    if not payload:
        return jsonify({"error": "Request body is required"}), 400

    lookup = payload.get("lookup", {})
    identifier = payload.get("id") or payload.get("person_id")

    # Allow lookup fields at top level when lookup dict omitted.
    for key in ("first_name", "last_name"):
        if payload.get(key) and key not in lookup:
            lookup[key] = payload[key]

    db, person_model, social_model, contact_model = _load_models()
    try:
        person = _resolve_person(person_model, identifier, lookup)
    except ValueError as err:
        return jsonify({"error": str(err)}), 409

    if not person:
        return jsonify({"error": "Person not found"}), 404

    updates_source = payload.get("updates", payload)
    update_data = {
        key: updates_source.get(key)
        for key in PERSON_FIELDS
        if updates_source.get(key) is not None
    }

    if update_data:
        person_model.update(person["id"], update_data)

    if payload.get("social_media") is not None:
        for entry in payload.get("social_media") or []:
            platform = entry.get("platform")
            profile_url = entry.get("profile_url")
            if not platform or not profile_url:
                continue

            social_kwargs = {
                key: entry.get(key)
                for key in SOCIAL_EXTRA_FIELDS
                if entry.get(key) is not None
            }
            social_model.upsert_profile(
                entity_type="person",
                entity_id=person["id"],
                platform=platform,
                profile_url=profile_url,
                handle=entry.get("handle"),
                display_name=entry.get("display_name"),
                is_verified=entry.get("is_verified", False),
                **social_kwargs,
            )

    if payload.get("contact_info") is not None:
        for entry in payload.get("contact_info") or []:
            contact_type = entry.get("contact_type")
            contact_value = entry.get("contact_value")
            if not contact_type or contact_value is None:
                continue

            contact_kwargs = {
                key: entry.get(key)
                for key in CONTACT_EXTRA_FIELDS
                if entry.get(key) is not None
            }
            contact_model.upsert_contact(
                entity_type="person",
                entity_id=person["id"],
                contact_type=contact_type,
                contact_value=contact_value,
                **contact_kwargs,
            )

    updated_person = _serialize_person(person_model, social_model, contact_model, person["id"])
    return jsonify(updated_person), 200
