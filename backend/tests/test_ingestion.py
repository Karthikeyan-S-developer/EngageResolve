import pytest
from app.core.ingestion import process_incoming_event
from app.core.validation import ValidationError

def test_valid_ingestion(db_conn):
    event = {
        "camera_id": "cam-01",
        "timestamp": "2024-06-01T10:00:00Z",
        "student_id": "student-101",
        "engagement_score": 0.85,
        "confidence": 0.90,
        "source": "front_camera"
    }
    result = process_incoming_event(db_conn, event)
    assert result["success"] is True
    assert result["status"] == "processed"
    assert result["total_versions"] == 1

def test_missing_camera_id(db_conn):
    event = {
        "timestamp": "2024-06-01T10:00:00Z",
        "student_id": "student-101",
        "engagement_score": 0.85,
        "confidence": 0.90,
        "source": "front_camera"
    }
    with pytest.raises(ValidationError) as excinfo:
        process_incoming_event(db_conn, event)
    assert excinfo.value.code == "MISSING_FIELD"

def test_score_out_of_range(db_conn):
    event = {
        "camera_id": "cam-01",
        "timestamp": "2024-06-01T10:00:00Z",
        "student_id": "student-101",
        "engagement_score": 1.5,
        "confidence": 0.90,
        "source": "front_camera"
    }
    with pytest.raises(ValidationError) as excinfo:
        process_incoming_event(db_conn, event)
    assert excinfo.value.code == "INVALID_ENGAGEMENT_SCORE"

def test_invalid_confidence(db_conn):
    event = {
        "camera_id": "cam-01",
        "timestamp": "2024-06-01T10:00:00Z",
        "student_id": "student-101",
        "engagement_score": 0.5,
        "confidence": -0.1,
        "source": "front_camera"
    }
    with pytest.raises(ValidationError) as excinfo:
        process_incoming_event(db_conn, event)
    assert excinfo.value.code == "INVALID_CONFIDENCE"

def test_invalid_timestamp(db_conn):
    event = {
        "camera_id": "cam-01",
        "timestamp": "not-a-timestamp",
        "student_id": "student-101",
        "engagement_score": 0.5,
        "confidence": 0.90,
        "source": "front_camera"
    }
    with pytest.raises(ValidationError) as excinfo:
        process_incoming_event(db_conn, event)
    assert excinfo.value.code == "INVALID_TIMESTAMP"
