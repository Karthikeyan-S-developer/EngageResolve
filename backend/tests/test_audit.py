from app.core.ingestion import process_incoming_event
from app.database.repositories import AuditRepository

def test_audit_log_generation(db_conn):
    s_id = "student-audit-test"
    
    # Conflict events
    evt1 = {"camera_id": "cam-01", "timestamp": "2024-06-01T10:00:00Z", "student_id": s_id, "engagement_score": 0.85, "confidence": 0.95, "source": "front"}
    evt2 = {"camera_id": "cam-02", "timestamp": "2024-06-01T10:00:00Z", "student_id": s_id, "engagement_score": 0.30, "confidence": 0.60, "source": "side"}

    process_incoming_event(db_conn, evt1)
    process_incoming_event(db_conn, evt2)

    audit_repo = AuditRepository(db_conn)
    logs = audit_repo.get_logs_for_student(s_id)
    assert len(logs) > 0

    conflict_log = next(l for l in logs if l["decision_type"] == "CONFLICT_RESOLUTION")
    assert conflict_log["final_score"] == 0.85
    assert conflict_log["selected_event_id"] is not None
