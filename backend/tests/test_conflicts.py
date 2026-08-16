from app.core.ingestion import process_incoming_event
from app.core.conflict_resolution import resolve_conflict_between_events
from app.database.repositories import StudentStateRepository, AuditRepository

def test_confidence_conflict_resolution(db_conn):
    s_id = "student-104"
    evt_a = {
        "camera_id": "cam-01",
        "timestamp": "2024-06-01T10:00:00Z",
        "student_id": s_id,
        "engagement_score": 0.90,
        "confidence": 0.95,
        "source": "front_camera"
    }
    evt_b = {
        "camera_id": "cam-02",
        "timestamp": "2024-06-01T10:00:00Z",
        "student_id": s_id,
        "engagement_score": 0.40,
        "confidence": 0.60,
        "source": "side_camera"
    }

    process_incoming_event(db_conn, evt_a)
    process_incoming_event(db_conn, evt_b)

    state_repo = StudentStateRepository(db_conn)
    latest = state_repo.get_latest_state(s_id)
    
    # Higher confidence (0.95 vs 0.60) must win!
    assert latest["engagement_score"] == 0.90
    assert latest["confidence"] == 0.95

def test_timestamp_tiebreak(db_conn):
    s_id = "student-tie-ts"
    evt_earlier = {
        "id": "evt-early",
        "camera_id": "cam-01",
        "timestamp": "2024-06-01T10:00:01Z",
        "student_id": s_id,
        "engagement_score": 0.80,
        "confidence": 0.90,
        "source": "front_camera",
        "event_fingerprint": "fp1"
    }
    evt_later = {
        "id": "evt-late",
        "camera_id": "cam-02",
        "timestamp": "2024-06-01T10:00:02Z",
        "student_id": s_id,
        "engagement_score": 0.30,
        "confidence": 0.90, # Same confidence
        "source": "side_camera",
        "event_fingerprint": "fp2"
    }

    winner, trace = resolve_conflict_between_events(evt_earlier, evt_later)
    assert winner["id"] == "evt-early"
    assert trace["tiebreaker_used"] == "TIMESTAMP"

def test_camera_reliability_tiebreak(db_conn):
    s_id = "student-tie-cam"
    evt_front = {
        "id": "evt-front",
        "camera_id": "front_camera",
        "timestamp": "2024-06-01T10:00:00Z",
        "student_id": s_id,
        "engagement_score": 0.85,
        "confidence": 0.90,
        "source": "front_camera",
        "event_fingerprint": "fp1"
    }
    evt_rear = {
        "id": "evt-rear",
        "camera_id": "rear_camera",
        "timestamp": "2024-06-01T10:00:00Z",
        "student_id": s_id,
        "engagement_score": 0.40,
        "confidence": 0.90, # Same confidence & timestamp
        "source": "rear_camera",
        "event_fingerprint": "fp2"
    }

    winner, trace = resolve_conflict_between_events(evt_front, evt_rear)
    assert winner["id"] == "evt-front"
    assert trace["tiebreaker_used"] == "CAMERA_RELIABILITY"

def test_fingerprint_tiebreak(db_conn):
    s_id = "student-tie-fp"
    evt_a = {
        "id": "evt-a",
        "camera_id": "front_camera",
        "timestamp": "2024-06-01T10:00:00Z",
        "student_id": s_id,
        "engagement_score": 0.85,
        "confidence": 0.90,
        "source": "front_camera",
        "event_fingerprint": "aaaa1111"
    }
    evt_b = {
        "id": "evt-b",
        "camera_id": "front_camera",
        "timestamp": "2024-06-01T10:00:00Z",
        "student_id": s_id,
        "engagement_score": 0.40,
        "confidence": 0.90,
        "source": "front_camera",
        "event_fingerprint": "zzzz9999"
    }

    winner, trace = resolve_conflict_between_events(evt_a, evt_b)
    assert winner["id"] == "evt-a" # Lexicographically lower fingerprint wins
    assert trace["tiebreaker_used"] == "FINGERPRINT"
