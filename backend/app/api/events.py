from flask import Blueprint, request, jsonify
from app.database.connection import get_db_connection
from app.core.ingestion import process_incoming_event
from app.core.validation import ValidationError
from app.database.repositories import EventRepository
from app.utils.serializers import format_api_success, format_api_error

events_bp = Blueprint("events", __name__)

@events_bp.route("/events", methods=["POST"])
def ingest_event():
    payload = request.get_json(silent=True)
    if not payload:
        return format_api_error("INVALID_JSON", "Request body must be valid JSON", 400)

    conn = get_db_connection()
    try:
        result = process_incoming_event(conn, payload)
        if result.get("status") == "duplicate":
            return jsonify({
                "success": True,
                "status": "duplicate",
                "event_id": result["event_id"],
                "message": result["message"]
            }), 200
        return jsonify({"success": True, "data": result}), 201
    except ValidationError as ve:
        return format_api_error(ve.code, ve.message, 400)
    except Exception as e:
        return format_api_error("INTERNAL_ERROR", str(e), 500)
    finally:
        conn.close()

@events_bp.route("/events/<event_id>", methods=["GET"])
def get_event_details(event_id: str):
    conn = get_db_connection()
    try:
        repo = EventRepository(conn)
        event = repo.get_by_id(event_id)
        if not event:
            return format_api_error("EVENT_NOT_FOUND", f"Event '{event_id}' not found.", 404)
        return format_api_success(event)
    finally:
        conn.close()
