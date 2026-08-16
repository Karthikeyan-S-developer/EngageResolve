import json

def test_health_endpoint(client):
    res = client.get("/health")
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "healthy"

def test_ingest_event_api(client):
    payload = {
        "camera_id": "cam-01",
        "timestamp": "2024-06-01T10:00:00Z",
        "student_id": "student-api-1",
        "engagement_score": 0.85,
        "confidence": 0.90,
        "source": "front_camera"
    }
    res = client.post("/events", data=json.dumps(payload), content_type="application/json")
    assert res.status_code == 201
    data = res.get_json()
    assert data["success"] is True

def test_list_students_api(client):
    res = client.get("/students")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True

def test_dashboard_summary_api(client):
    res = client.get("/dashboard/summary")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "total_students" in data["data"]

def test_export_csv_api(client):
    res = client.get("/export/engagement.csv")
    assert res.status_code == 200
    assert res.content_type == "text/csv; charset=utf-8"
