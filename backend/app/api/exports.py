import csv
import io
import os
from flask import Blueprint, Response
from app.database.connection import get_db_connection
from app.database.repositories import StudentStateRepository, AuditRepository, EventRepository

exports_bp = Blueprint("exports", __name__)

EXPORT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "exports")

def ensure_export_dir():
    if not os.path.exists(EXPORT_DIR):
        os.makedirs(EXPORT_DIR, exist_ok=True)

@exports_bp.route("/export/engagement.csv", methods=["GET"])
def export_engagement_csv():
    conn = get_db_connection()
    try:
        cursor = conn.execute(
            """
            SELECT 
                s.id as state_id,
                s.student_id,
                s.version as state_version,
                s.effective_timestamp as timestamp,
                s.engagement_score,
                s.confidence,
                s.state_status,
                e.camera_id,
                e.source,
                e.event_fingerprint
            FROM student_states s
            LEFT JOIN events e ON s.event_id = e.id
            ORDER BY s.effective_timestamp ASC, s.student_id ASC;
            """
        )
        rows = cursor.fetchall()

        ensure_export_dir()
        file_path = os.path.join(EXPORT_DIR, "engagement_timeline.csv")

        output = io.StringIO()
        writer = csv.writer(output)
        headers = [
            "state_id", "student_id", "state_version", "timestamp",
            "engagement_score", "confidence", "state_status",
            "camera_id", "source", "event_fingerprint"
        ]
        writer.writerow(headers)

        file_output = open(file_path, "w", newline="", encoding="utf-8")
        file_writer = csv.writer(file_output)
        file_writer.writerow(headers)

        for r in rows:
            row_data = [
                r["state_id"], r["student_id"], r["state_version"], r["timestamp"],
                r["engagement_score"], r["confidence"], r["state_status"],
                r["camera_id"], r["source"], r["event_fingerprint"]
            ]
            writer.writerow(row_data)
            file_writer.writerow(row_data)

        file_output.close()

        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment; filename=engagement_timeline.csv"}
        )
    finally:
        conn.close()

@exports_bp.route("/export/audit.csv", methods=["GET"])
def export_audit_csv():
    conn = get_db_connection()
    try:
        cursor = conn.execute(
            """
            SELECT 
                id as audit_id,
                student_id,
                event_id,
                decision_type,
                selected_event_id,
                final_score,
                previous_score,
                timestamp,
                created_at
            FROM audit_logs
            ORDER BY timestamp DESC;
            """
        )
        rows = cursor.fetchall()

        ensure_export_dir()
        file_path = os.path.join(EXPORT_DIR, "audit_log.csv")

        output = io.StringIO()
        writer = csv.writer(output)
        headers = [
            "audit_id", "student_id", "event_id", "decision_type",
            "selected_event_id", "final_score", "previous_score",
            "timestamp", "created_at"
        ]
        writer.writerow(headers)

        file_output = open(file_path, "w", newline="", encoding="utf-8")
        file_writer = csv.writer(file_output)
        file_writer.writerow(headers)

        for r in rows:
            row_data = [
                r["audit_id"], r["student_id"], r["event_id"], r["decision_type"],
                r["selected_event_id"], r["final_score"], r["previous_score"],
                r["timestamp"], r["created_at"]
            ]
            writer.writerow(row_data)
            file_writer.writerow(row_data)

        file_output.close()

        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment; filename=audit_log.csv"}
        )
    finally:
        conn.close()
