import os
import sqlite3
from typing import Dict, Any, Optional, List
from app.database.connection import get_db_connection, init_db
from app.database.repositories import EventRepository, StudentStateRepository, AuditRepository, ReplayRepository
from app.core.ingestion import process_incoming_event
from app.utils.hashing import calculate_state_result_hash
from app.utils.datetime_utils import get_current_iso_utc

def execute_replay_run(
    prod_conn: sqlite3.Connection,
    student_id: Optional[str] = None,
    from_timestamp: Optional[str] = None,
    to_timestamp: Optional[str] = None
) -> Dict[str, Any]:
    """
    Executes a side-effect-free replay run of historical events in an isolated in-memory SQLite sandbox.
    Calculates deterministic result hash of the reconstructed timeline & audit trail.
    """
    started_at = get_current_iso_utc()
    
    # 1. Query production events to replay
    query_parts = ["SELECT * FROM events WHERE is_replay = 0"]
    params: List[Any] = []

    if student_id:
        query_parts.append("AND resolved_student_id = ?")
        params.append(student_id)

    if from_timestamp:
        query_parts.append("AND timestamp >= ?")
        params.append(from_timestamp)

    if to_timestamp:
        query_parts.append("AND timestamp <= ?")
        params.append(to_timestamp)

    query_parts.append("ORDER BY timestamp ASC, camera_id ASC, event_fingerprint ASC;")
    
    cursor = prod_conn.execute(" ".join(query_parts), params)
    raw_events = cursor.fetchall()
    event_count = len(raw_events)

    # 2. Record run start in production replay_runs table
    replay_repo = ReplayRepository(prod_conn)
    replay_run = replay_repo.create_run(event_count=event_count, started_at=started_at)
    replay_id = replay_run["id"]

    # 3. Create isolated in-memory sandbox DB and initialize schema on same connection
    sandbox_conn = sqlite3.connect(":memory:", isolation_level=None)
    sandbox_conn.row_factory = sqlite3.Row
    sandbox_conn.execute("PRAGMA foreign_keys = ON;")
    
    schema_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "schema.sql")
    with open(schema_file, "r", encoding="utf-8") as f:
        sandbox_conn.executescript(f.read())

    # 4. Re-process events through core engine in sandbox
    for evt_row in raw_events:
        evt_dict = {
            "camera_id": evt_row["camera_id"],
            "timestamp": evt_row["timestamp"],
            "student_id": evt_row["student_id_raw"],
            "engagement_score": float(evt_row["engagement_score"]),
            "confidence": float(evt_row["confidence"]),
            "source": evt_row["source"],
            "spatial_x": evt_row["spatial_x"],
            "spatial_y": evt_row["spatial_y"],
            "is_replay": True
        }
        process_incoming_event(sandbox_conn, evt_dict)

    # 5. Extract sandbox states and audit logs to generate canonical result hash
    sb_state_repo = StudentStateRepository(sandbox_conn)
    sb_audit_repo = AuditRepository(sandbox_conn)

    sandbox_states = sb_state_repo.list_all_latest_states() if not student_id else sb_state_repo.get_states_for_student(student_id)
    sandbox_audits = sb_audit_repo.list_all(limit=10000) if not student_id else sb_audit_repo.get_logs_for_student(student_id)

    result_hash = calculate_state_result_hash(sandbox_states, sandbox_audits)
    completed_at = get_current_iso_utc()

    # 6. Complete replay run in production DB
    completed_record = replay_repo.complete_run(replay_id, result_hash, completed_at)
    sandbox_conn.close()

    return {
        "replay_id": replay_id,
        "event_count": event_count,
        "result_hash": result_hash,
        "deterministic": True,
        "status": "completed",
        "started_at": started_at,
        "completed_at": completed_at,
        "student_id": student_id,
        "reconstructed_state_count": len(sandbox_states),
        "reconstructed_audit_count": len(sandbox_audits)
    }
