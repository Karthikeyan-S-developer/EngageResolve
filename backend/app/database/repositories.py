import uuid
import json
import sqlite3
from typing import List, Dict, Any, Optional
from app.utils.serializers import row_to_dict
from app.utils.datetime_utils import get_current_iso_utc

class StudentRepository:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def get_by_id(self, student_id: str) -> Optional[Dict[str, Any]]:
        cursor = self.conn.execute("SELECT * FROM students WHERE id = ?;", (student_id,))
        row = cursor.fetchone()
        return row_to_dict(row)

    def list_all(self) -> List[Dict[str, Any]]:
        cursor = self.conn.execute("SELECT * FROM students ORDER BY id ASC;")
        return [row_to_dict(r) for r in cursor.fetchall()]

    def ensure_exists(self, student_id: str, display_name: Optional[str] = None) -> Dict[str, Any]:
        existing = self.get_by_id(student_id)
        if existing:
            return existing
        now = get_current_iso_utc()
        name = display_name or f"Student {student_id.replace('student-', '').replace('stu-', '')}"
        self.conn.execute(
            "INSERT INTO students (id, display_name, created_at, updated_at) VALUES (?, ?, ?, ?);",
            (student_id, name, now, now)
        )
        return {"id": student_id, "display_name": name, "created_at": now, "updated_at": now}

    def update_timestamp(self, student_id: str) -> None:
        now = get_current_iso_utc()
        self.conn.execute("UPDATE students SET updated_at = ? WHERE id = ?;", (now, student_id))


class EventRepository:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def get_by_fingerprint(self, fingerprint: str) -> Optional[Dict[str, Any]]:
        cursor = self.conn.execute("SELECT * FROM events WHERE event_fingerprint = ?;", (fingerprint,))
        return row_to_dict(cursor.fetchone())

    def get_by_id(self, event_id: str) -> Optional[Dict[str, Any]]:
        cursor = self.conn.execute("SELECT * FROM events WHERE id = ?;", (event_id,))
        return row_to_dict(cursor.fetchone())

    def create(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        event_id = event_data.get("id") or f"evt-{event_data['event_fingerprint'][:12]}"
        now = get_current_iso_utc()
        self.conn.execute(
            """
            INSERT INTO events (
                id, event_fingerprint, camera_id, timestamp, received_at,
                student_id_raw, resolved_student_id, engagement_score, confidence,
                source, spatial_x, spatial_y, is_replay, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """,
            (
                event_id,
                event_data["event_fingerprint"],
                event_data["camera_id"],
                event_data["timestamp"],
                event_data.get("received_at", now),
                event_data["student_id_raw"],
                event_data["resolved_student_id"],
                float(event_data["engagement_score"]),
                float(event_data["confidence"]),
                event_data["source"],
                event_data.get("spatial_x"),
                event_data.get("spatial_y"),
                1 if event_data.get("is_replay") else 0,
                now
            )
        )
        return self.get_by_id(event_id)

    def get_events_for_student(self, student_id: str) -> List[Dict[str, Any]]:
        cursor = self.conn.execute(
            "SELECT * FROM events WHERE resolved_student_id = ? ORDER BY timestamp ASC, id ASC;",
            (student_id,)
        )
        return [row_to_dict(r) for r in cursor.fetchall()]

    def list_all(self, limit: int = 500) -> List[Dict[str, Any]]:
        cursor = self.conn.execute(
            "SELECT * FROM events ORDER BY timestamp DESC LIMIT ?;",
            (limit,)
        )
        return [row_to_dict(r) for r in cursor.fetchall()]

    def get_camera_summaries(self) -> List[Dict[str, Any]]:
        cursor = self.conn.execute(
            """
            SELECT 
                camera_id,
                COUNT(*) as total_events,
                MAX(timestamp) as last_event_at,
                AVG(engagement_score) as avg_engagement,
                AVG(confidence) as avg_confidence
            FROM events
            GROUP BY camera_id
            ORDER BY camera_id ASC;
            """
        )
        return [row_to_dict(r) for r in cursor.fetchall()]


class StudentStateRepository:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def get_latest_state(self, student_id: str) -> Optional[Dict[str, Any]]:
        cursor = self.conn.execute(
            "SELECT * FROM student_states WHERE student_id = ? ORDER BY version DESC LIMIT 1;",
            (student_id,)
        )
        return row_to_dict(cursor.fetchone())

    def get_states_for_student(self, student_id: str) -> List[Dict[str, Any]]:
        cursor = self.conn.execute(
            "SELECT * FROM student_states WHERE student_id = ? ORDER BY version ASC;",
            (student_id,)
        )
        return [row_to_dict(r) for r in cursor.fetchall()]

    def clear_states_for_student(self, student_id: str) -> None:
        self.conn.execute("DELETE FROM student_states WHERE student_id = ?;", (student_id,))

    def save_state(self, state_data: Dict[str, Any]) -> Dict[str, Any]:
        state_id = state_data.get("id") or f"state-{state_data['student_id']}-v{state_data['version']}"
        now = get_current_iso_utc()
        self.conn.execute(
            """
            INSERT INTO student_states (
                id, student_id, version, event_id, effective_timestamp,
                engagement_score, confidence, state_status, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
            """,
            (
                state_id,
                state_data["student_id"],
                int(state_data["version"]),
                state_data["event_id"],
                state_data["effective_timestamp"],
                float(state_data["engagement_score"]),
                float(state_data["confidence"]),
                state_data["state_status"],
                now
            )
        )
        return {
            "id": state_id,
            "student_id": state_data["student_id"],
            "version": int(state_data["version"]),
            "event_id": state_data["event_id"],
            "effective_timestamp": state_data["effective_timestamp"],
            "engagement_score": float(state_data["engagement_score"]),
            "confidence": float(state_data["confidence"]),
            "state_status": state_data["state_status"],
            "created_at": now
        }

    def list_all_latest_states(self) -> List[Dict[str, Any]]:
        cursor = self.conn.execute(
            """
            SELECT s1.* 
            FROM student_states s1
            INNER JOIN (
                SELECT student_id, MAX(version) as max_ver
                FROM student_states
                GROUP BY student_id
            ) s2 ON s1.student_id = s2.student_id AND s1.version = s2.max_ver;
            """
        )
        return [row_to_dict(r) for r in cursor.fetchall()]


class AuditRepository:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def create_log(self, log_data: Dict[str, Any]) -> Dict[str, Any]:
        log_id = log_data.get("id") or f"audit-{uuid.uuid4().hex[:12]}"
        now = get_current_iso_utc()
        input_events_json = json.dumps(log_data.get("input_events", []))
        resolution_logic_json = json.dumps(log_data.get("resolution_logic", {}))
        
        self.conn.execute(
            """
            INSERT INTO audit_logs (
                id, student_id, event_id, decision_type, input_events,
                resolution_logic, selected_event_id, final_score, previous_score,
                timestamp, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """,
            (
                log_id,
                log_data["student_id"],
                log_data.get("event_id"),
                log_data["decision_type"],
                input_events_json,
                resolution_logic_json,
                log_data.get("selected_event_id"),
                float(log_data["final_score"]),
                float(log_data["previous_score"]) if log_data.get("previous_score") is not None else None,
                log_data["timestamp"],
                now
            )
        )
        return self.get_by_id(log_id)

    def get_by_id(self, log_id: str) -> Optional[Dict[str, Any]]:
        cursor = self.conn.execute("SELECT * FROM audit_logs WHERE id = ?;", (log_id,))
        return row_to_dict(cursor.fetchone())

    def get_logs_for_student(self, student_id: str) -> List[Dict[str, Any]]:
        cursor = self.conn.execute(
            "SELECT * FROM audit_logs WHERE student_id = ? ORDER BY timestamp DESC, id DESC;",
            (student_id,)
        )
        return [row_to_dict(r) for r in cursor.fetchall()]

    def get_conflicts(self, limit: int = 100) -> List[Dict[str, Any]]:
        cursor = self.conn.execute(
            """
            SELECT * FROM audit_logs 
            WHERE decision_type = 'CONFLICT_RESOLUTION'
            ORDER BY timestamp DESC
            LIMIT ?;
            """,
            (limit,)
        )
        return [row_to_dict(r) for r in cursor.fetchall()]

    def list_all(self, limit: int = 500) -> List[Dict[str, Any]]:
        cursor = self.conn.execute(
            "SELECT * FROM audit_logs ORDER BY timestamp DESC, id DESC LIMIT ?;",
            (limit,)
        )
        return [row_to_dict(r) for r in cursor.fetchall()]


class IdentityRepository:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def create_match(self, match_data: Dict[str, Any]) -> Dict[str, Any]:
        match_id = match_data.get("id") or f"idmatch-{uuid.uuid4().hex[:12]}"
        now = get_current_iso_utc()
        self.conn.execute(
            """
            INSERT INTO identity_matches (
                id, raw_student_id, resolved_student_id, camera_id,
                temporal_score, spatial_score, combined_score, decision, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
            """,
            (
                match_id,
                match_data["raw_student_id"],
                match_data["resolved_student_id"],
                match_data["camera_id"],
                float(match_data["temporal_score"]),
                float(match_data["spatial_score"]),
                float(match_data["combined_score"]),
                match_data["decision"],
                now
            )
        )
        return {**match_data, "id": match_id, "created_at": now}

    def find_mapping_for_raw_id(self, raw_student_id: str) -> Optional[str]:
        cursor = self.conn.execute(
            """
            SELECT resolved_student_id 
            FROM identity_matches 
            WHERE raw_student_id = ? AND decision = 'RESOLVED'
            ORDER BY created_at DESC 
            LIMIT 1;
            """,
            (raw_student_id,)
        )
        row = cursor.fetchone()
        return row["resolved_student_id"] if row else None


class ReplayRepository:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def create_run(self, event_count: int, started_at: str) -> Dict[str, Any]:
        replay_id = f"replay-{uuid.uuid4().hex[:12]}"
        self.conn.execute(
            """
            INSERT INTO replay_runs (id, started_at, completed_at, event_count, result_hash, status)
            VALUES (?, ?, NULL, ?, '', 'RUNNING');
            """,
            (replay_id, started_at, event_count)
        )
        return {"id": replay_id, "started_at": started_at, "event_count": event_count, "status": "RUNNING"}

    def complete_run(self, replay_id: str, result_hash: str, completed_at: str) -> Dict[str, Any]:
        self.conn.execute(
            """
            UPDATE replay_runs
            SET completed_at = ?, result_hash = ?, status = 'COMPLETED'
            WHERE id = ?;
            """,
            (completed_at, result_hash, replay_id)
        )
        cursor = self.conn.execute("SELECT * FROM replay_runs WHERE id = ?;", (replay_id,))
        return row_to_dict(cursor.fetchone())

    def get_run(self, replay_id: str) -> Optional[Dict[str, Any]]:
        cursor = self.conn.execute("SELECT * FROM replay_runs WHERE id = ?;", (replay_id,))
        return row_to_dict(cursor.fetchone())
