from flask import Blueprint, request, jsonify
from app.database.connection import get_db_connection
from app.core.replay_engine import execute_replay_run
from app.database.repositories import ReplayRepository
from app.utils.serializers import format_api_success, format_api_error

replay_bp = Blueprint("replay", __name__)

@replay_bp.route("/replay", methods=["POST"])
def start_replay():
    payload = request.get_json(silent=True) or {}
    student_id = payload.get("student_id")
    from_ts = payload.get("from")
    to_ts = payload.get("to")

    conn = get_db_connection()
    try:
        replay_result = execute_replay_run(
            prod_conn=conn,
            student_id=student_id,
            from_timestamp=from_ts,
            to_timestamp=to_ts
        )
        return format_api_success(replay_result, 200)
    except Exception as e:
        return format_api_error("REPLAY_ERROR", str(e), 500)
    finally:
        conn.close()

@replay_bp.route("/replay/<replay_id>", methods=["GET"])
def get_replay_details(replay_id: str):
    conn = get_db_connection()
    try:
        repo = ReplayRepository(conn)
        record = repo.get_run(replay_id)
        if not record:
            return format_api_error("REPLAY_NOT_FOUND", f"Replay run '{replay_id}' not found.", 404)
        return format_api_success(record)
    finally:
        conn.close()
