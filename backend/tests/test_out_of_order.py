from app.core.ingestion import process_incoming_event
from app.database.repositories import StudentStateRepository, AuditRepository

def test_out_of_order_event_reconstruction(db_conn):
    s_id = "student-103"
    
    # Submit 10:00:10
    evt10 = {
        "camera_id": "cam-01",
        "timestamp": "2024-06-01T10:00:10Z",
        "student_id": s_id,
        "engagement_score": 0.60,
        "confidence": 0.85,
        "source": "front_camera"
    }
    process_incoming_event(db_conn, evt10)

    # Submit 10:00:20
    evt20 = {
        "camera_id": "cam-01",
        "timestamp": "2024-06-01T10:00:20Z",
        "student_id": s_id,
        "engagement_score": 0.40,
        "confidence": 0.80,
        "source": "front_camera"
    }
    process_incoming_event(db_conn, evt20)

    # Submit 10:00:05 (out of order!)
    evt05 = {
        "camera_id": "cam-01",
        "timestamp": "2024-06-01T10:00:05Z",
        "student_id": s_id,
        "engagement_score": 0.90,
        "confidence": 0.95,
        "source": "front_camera"
    }
    res_ooo = process_incoming_event(db_conn, evt05)
    assert res_ooo["is_out_of_order"] is True

    state_repo = StudentStateRepository(db_conn)
    states = state_repo.get_states_for_student(s_id)

    # Assert reconstructed timeline order: 5s, 10s, 20s
    assert len(states) == 3
    assert states[0]["effective_timestamp"] == "2024-06-01T10:00:05Z"
    assert states[0]["version"] == 1
    assert states[0]["engagement_score"] == 0.90

    assert states[1]["effective_timestamp"] == "2024-06-01T10:00:10Z"
    assert states[1]["version"] == 2
    assert states[1]["engagement_score"] == 0.60

    assert states[2]["effective_timestamp"] == "2024-06-01T10:00:20Z"
    assert states[2]["version"] == 3
    assert states[2]["engagement_score"] == 0.40

    # Assert OUT_OF_ORDER audit log created
    audit_repo = AuditRepository(db_conn)
    audits = audit_repo.get_logs_for_student(s_id)
    ooo_logs = [a for a in audits if a["decision_type"] == "OUT_OF_ORDER_EVENT"]
    assert len(ooo_logs) == 1
