from app.core.ingestion import process_incoming_event
from app.core.identity_resolution import resolve_student_identity
from app.database.repositories import IdentityRepository

def test_spatio_temporal_identity_resolution(db_conn):
    # Anchor observation for canonical student-105
    evt1 = {
        "camera_id": "cam-01",
        "timestamp": "2024-06-01T10:04:00Z",
        "student_id": "student-105",
        "engagement_score": 0.88,
        "confidence": 0.90,
        "source": "front_camera",
        "spatial_x": 10.0,
        "spatial_y": 20.0
    }
    process_incoming_event(db_conn, evt1)

    # Raw unmapped camera observation 2 seconds later in close spatial proximity
    evt2 = {
        "camera_id": "cam-02",
        "timestamp": "2024-06-01T10:04:02Z",
        "student_id": "raw-desk-105",
        "engagement_score": 0.85,
        "confidence": 0.88,
        "source": "side_camera",
        "spatial_x": 10.5,
        "spatial_y": 20.5
    }
    res2 = process_incoming_event(db_conn, evt2)
    assert res2["resolved_student_id"] == "student-105"

def test_distinct_student_separation(db_conn):
    # Observation for student-A
    evt_a = {
        "camera_id": "cam-01",
        "timestamp": "2024-06-01T10:00:00Z",
        "student_id": "student-A",
        "engagement_score": 0.80,
        "confidence": 0.90,
        "source": "front_camera",
        "spatial_x": 0.0,
        "spatial_y": 0.0
    }
    process_incoming_event(db_conn, evt_a)

    # Observation for student-B far away in space (1000m)
    evt_b = {
        "camera_id": "cam-02",
        "timestamp": "2024-06-01T10:00:01Z",
        "student_id": "student-B",
        "engagement_score": 0.50,
        "confidence": 0.85,
        "source": "side_camera",
        "spatial_x": 500.0,
        "spatial_y": 500.0
    }
    res_b = process_incoming_event(db_conn, evt_b)
    assert res_b["resolved_student_id"] == "student-B"
