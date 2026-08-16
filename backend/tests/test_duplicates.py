from app.core.ingestion import process_incoming_event
from app.database.repositories import StudentStateRepository, AuditRepository

def test_idempotency_duplicate_submission(db_conn):
    event = {
        "camera_id": "cam-01",
        "timestamp": "2024-06-01T10:00:00Z",
        "student_id": "student-102",
        "engagement_score": 0.75,
        "confidence": 0.90,
        "source": "front_camera"
    }

    # First submission
    res1 = process_incoming_event(db_conn, event)
    assert res1["status"] == "processed"

    state_repo = StudentStateRepository(db_conn)
    states1 = state_repo.get_states_for_student("student-102")
    assert len(states1) == 1

    # Duplicate submission
    res2 = process_incoming_event(db_conn, event)
    assert res2["status"] == "duplicate"

    states2 = state_repo.get_states_for_student("student-102")
    assert len(states2) == 1 # Assert no duplicate state version was created!
