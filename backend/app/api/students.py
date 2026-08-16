from flask import Blueprint, jsonify
from app.database.connection import get_db_connection
from app.database.repositories import StudentRepository, StudentStateRepository, EventRepository, AuditRepository
from app.utils.serializers import format_api_success, format_api_error
from app.config import Config

students_bp = Blueprint("students", __name__)

@students_bp.route("/students", methods=["GET"])
def list_students():
    conn = get_db_connection()
    try:
        student_repo = StudentRepository(conn)
        state_repo = StudentStateRepository(conn)
        audit_repo = AuditRepository(conn)

        students = student_repo.list_all()
        latest_states = {s["student_id"]: s for s in state_repo.list_all_latest_states()}

        result = []
        for s in students:
            s_id = s["id"]
            state = latest_states.get(s_id)
            score = state["engagement_score"] if state else 0.0
            
            # Status classification
            if score >= Config.HIGH_ENGAGEMENT_THRESHOLD:
                status_label = "HIGH"
            elif score >= Config.LOW_ENGAGEMENT_THRESHOLD:
                status_label = "MODERATE"
            else:
                status_label = "LOW"

            all_states = state_repo.get_states_for_student(s_id)
            
            # Trend calculation
            if len(all_states) >= 2:
                prev_score = all_states[-2]["engagement_score"]
                diff = score - prev_score
                trend = "UP" if diff > 0.05 else ("DOWN" if diff < -0.05 else "STABLE")
            else:
                trend = "STABLE"

            audits = audit_repo.get_logs_for_student(s_id)
            conflicts_count = sum(1 for a in audits if a["decision_type"] == "CONFLICT_RESOLUTION")

            result.append({
                "id": s_id,
                "display_name": s["display_name"],
                "current_engagement": round(score, 4),
                "status": status_label,
                "trend": trend,
                "confidence": round(state["confidence"], 4) if state else 0.0,
                "state_version": state["version"] if state else 0,
                "total_states": len(all_states),
                "conflicts_count": conflicts_count,
                "last_updated": s["updated_at"]
            })

        return format_api_success(result)
    finally:
        conn.close()

@students_bp.route("/student/<student_id>", methods=["GET"])
def get_student_profile(student_id: str):
    conn = get_db_connection()
    try:
        student_repo = StudentRepository(conn)
        state_repo = StudentStateRepository(conn)
        event_repo = EventRepository(conn)
        audit_repo = AuditRepository(conn)

        student = student_repo.get_by_id(student_id)
        if not student:
            return format_api_error("STUDENT_NOT_FOUND", f"Student '{student_id}' not found.", 404)

        states = state_repo.get_states_for_student(student_id)
        events = event_repo.get_events_for_student(student_id)
        audits = audit_repo.get_logs_for_student(student_id)

        scores = [s["engagement_score"] for s in states] if states else [0.0]
        avg_score = sum(scores) / len(scores) if scores else 0.0

        latest = states[-1] if states else None
        curr_score = latest["engagement_score"] if latest else 0.0

        if curr_score >= Config.HIGH_ENGAGEMENT_THRESHOLD:
            status_label = "HIGH"
        elif curr_score >= Config.LOW_ENGAGEMENT_THRESHOLD:
            status_label = "MODERATE"
        else:
            status_label = "LOW"

        conflicts = [a for a in audits if a["decision_type"] == "CONFLICT_RESOLUTION"]
        out_of_orders = [a for a in audits if a["decision_type"] == "OUT_OF_ORDER_EVENT"]

        profile = {
            "id": student["id"],
            "display_name": student["display_name"],
            "current_engagement": round(curr_score, 4),
            "average_engagement": round(avg_score, 4),
            "highest_engagement": round(max(scores), 4),
            "lowest_engagement": round(min(scores), 4),
            "status": status_label,
            "observations_count": len(events),
            "state_versions_count": len(states),
            "conflicts_count": len(conflicts),
            "out_of_order_count": len(out_of_orders),
            "latest_state": latest,
            "created_at": student["created_at"],
            "updated_at": student["updated_at"]
        }

        return format_api_success(profile)
    finally:
        conn.close()

@students_bp.route("/student/<student_id>/timeline", methods=["GET"])
def get_student_timeline(student_id: str):
    conn = get_db_connection()
    try:
        student_repo = StudentRepository(conn)
        if not student_repo.get_by_id(student_id):
            return format_api_error("STUDENT_NOT_FOUND", f"Student '{student_id}' not found.", 404)

        state_repo = StudentStateRepository(conn)
        event_repo = EventRepository(conn)

        states = state_repo.get_states_for_student(student_id)
        events = event_repo.get_events_for_student(student_id)

        # Merge states with event details
        events_by_id = {e["id"]: e for e in events}
        timeline = []

        for s in states:
            evt = events_by_id.get(s["event_id"], {})
            timeline.append({
                "version": s["version"],
                "effective_timestamp": s["effective_timestamp"],
                "engagement_score": round(s["engagement_score"], 4),
                "confidence": round(s["confidence"], 4),
                "state_status": s["state_status"],
                "event_id": s["event_id"],
                "camera_id": evt.get("camera_id", "N/A"),
                "source": evt.get("source", "N/A"),
                "spatial_x": evt.get("spatial_x"),
                "spatial_y": evt.get("spatial_y")
            })

        return format_api_success({
            "student_id": student_id,
            "total_versions": len(timeline),
            "timeline": timeline
        })
    finally:
        conn.close()
