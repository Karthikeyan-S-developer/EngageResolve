from app.core.ingestion import process_incoming_event
from app.core.replay_engine import execute_replay_run
from app.database.repositories import StudentStateRepository, EventRepository

def test_replay_determinism_and_side_effect_freedom(db_conn):
    s_id = "student-replay-test"
    events = [
        {"camera_id": "cam-01", "timestamp": "2024-06-01T10:00:00Z", "student_id": s_id, "engagement_score": 0.80, "confidence": 0.90, "source": "front"},
        {"camera_id": "cam-02", "timestamp": "2024-06-01T10:00:05Z", "student_id": s_id, "engagement_score": 0.85, "confidence": 0.95, "source": "side"},
        {"camera_id": "cam-01", "timestamp": "2024-06-01T10:00:02Z", "student_id": s_id, "engagement_score": 0.60, "confidence": 0.80, "source": "front"}
    ]
    for e in events:
        process_incoming_event(db_conn, e)

    state_repo = StudentStateRepository(db_conn)
    initial_states = state_repo.get_states_for_student(s_id)
    initial_event_count = len(EventRepository(db_conn).list_all())

    # Run replay 1
    run1 = execute_replay_run(db_conn, student_id=s_id)
    assert run1["status"] == "completed"
    hash1 = run1["result_hash"]

    # Run replay 2
    run2 = execute_replay_run(db_conn, student_id=s_id)
    assert run2["status"] == "completed"
    hash2 = run2["result_hash"]

    # Assert 100% deterministic hash match
    assert hash1 == hash2

    # Assert production state was NOT mutated
    after_states = state_repo.get_states_for_student(s_id)
    assert initial_states == after_states

    after_event_count = len(EventRepository(db_conn).list_all())
    assert initial_event_count == after_event_count
