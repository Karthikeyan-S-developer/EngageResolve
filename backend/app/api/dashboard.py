from flask import Blueprint
from app.database.connection import get_db_connection
from app.database.repositories import (
    StudentRepository, StudentStateRepository, EventRepository, AuditRepository
)
from app.config import Config
from app.utils.serializers import format_api_success

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard/summary", methods=["GET"])
def get_dashboard_summary():
    conn = get_db_connection()
    try:
        student_repo = StudentRepository(conn)
        state_repo = StudentStateRepository(conn)
        event_repo = EventRepository(conn)
        audit_repo = AuditRepository(conn)

        students = student_repo.list_all()
        events = event_repo.list_all(limit=10000)
        audits = audit_repo.list_all(limit=10000)
        latest_states = state_repo.list_all_latest_states()

        total_students = len(students)
        total_events = len(events)

        cameras = set(e["camera_id"] for e in events)
        active_cameras_count = len(cameras)

        conflicts_count = sum(1 for a in audits if a["decision_type"] == "CONFLICT_RESOLUTION")
        duplicates_count = sum(1 for a in audits if a["decision_type"] == "DUPLICATE_EVENT")
        out_of_order_count = sum(1 for a in audits if a["decision_type"] == "OUT_OF_ORDER_EVENT")

        scores = [s["engagement_score"] for s in latest_states] if latest_states else [0.0]
        avg_engagement = sum(scores) / len(scores) if scores else 0.0

        high_count = sum(1 for s in scores if s >= Config.HIGH_ENGAGEMENT_THRESHOLD)
        low_count = sum(1 for s in scores if s < Config.LOW_ENGAGEMENT_THRESHOLD)
        moderate_count = total_students - high_count - low_count

        return format_api_success({
            "total_students": total_students,
            "active_cameras": active_cameras_count,
            "total_events": total_events,
            "conflicts_detected": conflicts_count,
            "duplicates_detected": duplicates_count,
            "out_of_order_events": out_of_order_count,
            "average_engagement": round(avg_engagement, 4),
            "high_engagement_students": high_count,
            "moderate_engagement_students": moderate_count,
            "low_engagement_students": low_count
        })
    finally:
        conn.close()

@dashboard_bp.route("/dashboard/cameras", methods=["GET"])
def get_camera_summaries():
    conn = get_db_connection()
    try:
        event_repo = EventRepository(conn)
        raw_summaries = event_repo.get_camera_summaries()

        result = []
        for cam in raw_summaries:
            c_id = cam["camera_id"]
            reliability = Config.get_camera_reliability(c_id)
            result.append({
                "camera_id": c_id,
                "total_events": cam["total_events"],
                "last_event_at": cam["last_event_at"],
                "avg_engagement": round(cam["avg_engagement"], 4) if cam["avg_engagement"] else 0.0,
                "avg_confidence": round(cam["avg_confidence"], 4) if cam["avg_confidence"] else 0.0,
                "reliability": reliability,
                "status": "ONLINE"
            })

        return format_api_success(result)
    finally:
        conn.close()
