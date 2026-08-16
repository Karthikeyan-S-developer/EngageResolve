# Replay Engine & Determinism Verification

## Overview

The EngageResolve Replay Engine allows system administrators and evaluators to re-execute historical classroom events through an isolated sandbox engine instance.

## Key Properties

1. **Side-Effect-Free Execution**:
   - Replay runs take place inside an in-memory SQLite sandbox database connection (`sqlite3.connect(":memory:")`).
   - Production `student_states` and `events` tables remain 100% un-mutated.
2. **Deterministic Result Hashing**:
   - Computes a canonical SHA-256 hash over all reconstructed versioned student states and audit logs.
   - Running replay multiple times over identical historical event datasets produces **100% identical SHA-256 result hashes**.

## API Execution

### Request
```http
POST /replay
Content-Type: application/json

{
  "student_id": "student-001"
}
```

### Response
```json
{
  "success": true,
  "data": {
    "replay_id": "replay-9a8b7c6d",
    "event_count": 42,
    "result_hash": "424ce3c86c6b87ba7a4204a1d18cec0da01e021026250741991e8333c44a2c1b",
    "deterministic": true,
    "status": "completed",
    "started_at": "2024-06-01T10:00:00Z",
    "completed_at": "2024-06-01T10:00:01Z"
  }
}
```
