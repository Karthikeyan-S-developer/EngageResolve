# EngageResolve REST API Documentation

All API responses follow a strict, predictable JSON format:

### Success Standard
```json
{
  "success": true,
  "data": {}
}
```

### Error Standard
```json
{
  "success": false,
  "error": {
    "code": "INVALID_EVENT",
    "message": "engagement_score must be between 0 and 1"
  }
}
```

---

## Endpoints

### 1. System Health
- **URL**: `GET /health`
- **Response**: `200 OK`
```json
{
  "status": "healthy",
  "system": "EngageResolve Engine",
  "version": "1.0.0"
}
```

### 2. Ingest Engagement Event
- **URL**: `POST /events`
- **Payload**:
```json
{
  "camera_id": "cam-01",
  "timestamp": "2024-06-01T10:00:00Z",
  "student_id": "student-123",
  "engagement_score": 0.75,
  "confidence": 0.90,
  "source": "front_camera",
  "spatial_x": 12.5,
  "spatial_y": 45.0
}
```
- **Response (Processed)**: `201 Created`
- **Response (Duplicate)**: `200 OK` (`"status": "duplicate"`)

### 3. List Students
- **URL**: `GET /students`
- **Response**: `200 OK` - Array of students with current engagement scores, trends, status, and conflict counts.

### 4. Get Student Profile
- **URL**: `GET /student/{id}`
- **Response**: `200 OK` - Detailed engagement profile, averages, min/max scores.

### 5. Get Student Timeline
- **URL**: `GET /student/{id}/timeline`
- **Response**: `200 OK` - Reconstructed versioned timeline states ($v_1, v_2, v_3 \dots$).

### 6. Get Student Audit Logs
- **URL**: `GET /student/{id}/audit`
- **Response**: `200 OK` - Audit decision records with human-readable explanations.

### 7. Replay Engine Run
- **URL**: `POST /replay`
- **Payload**: `{ "student_id": "student-123" }`
- **Response**: `200 OK` - Returns `replay_id`, `event_count`, and deterministic `result_hash`.

### 8. Dashboard Summary
- **URL**: `GET /dashboard/summary`
- **Response**: `200 OK` - Total students, active cameras, total events, conflicts, duplicates, out-of-order count, average engagement.

### 9. Exports
- **GET `/export/engagement.csv`**: Engagement timeline CSV download.
- **GET `/export/audit.csv`**: Audit log CSV download.
