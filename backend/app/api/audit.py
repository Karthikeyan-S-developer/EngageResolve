from flask import Blueprint, jsonify, request
from app.database.connection import get_db_connection
from app.database.repositories import AuditRepository, StudentRepository
from app.core.audit_engine import format_human_readable_explanation
from app.utils.serializers import format_api_success, format_api_error

audit_bp = Blueprint("audit", __name__)

@audit_bp.route("/student/<student_id>/audit", methods=["GET"])
def get_student_audit_logs(student_id: str):
    conn = get_db_connection()
    try:
        student_repo = StudentRepository(conn)
        if not student_repo.get_by_id(student_id):
            return format_api_error("STUDENT_NOT_FOUND", f"Student '{student_id}' not found.", 404)

        repo = AuditRepository(conn)
        logs = repo.get_logs_for_student(student_id)

        enhanced_logs = []
        for l in logs:
            explanation = format_human_readable_explanation(l)
            enhanced_logs.append({
                **l,
                "human_readable_explanation": explanation
            })

        return format_api_success({
            "student_id": student_id,
            "total_records": len(enhanced_logs),
            "audit_logs": enhanced_logs
        })
    finally:
        conn.close()

@audit_bp.route("/audit/conflicts", methods=["GET"])
def get_conflict_audits():
    limit = request.args.get("limit", 100, type=int)
    conn = get_db_connection()
    try:
        repo = AuditRepository(conn)
        conflicts = repo.get_conflicts(limit=limit)

        enhanced = []
        for c in conflicts:
            explanation = format_human_readable_explanation(c)
            enhanced.append({
                **c,
                "human_readable_explanation": explanation
            })

        return format_api_success({
            "total_conflicts": len(enhanced),
            "conflicts": enhanced
        })
    finally:
        conn.close()

@audit_bp.route("/audit/all", methods=["GET"])
def get_all_audits():
    limit = request.args.get("limit", 200, type=int)
    conn = get_db_connection()
    try:
        repo = AuditRepository(conn)
        logs = repo.list_all(limit=limit)
        enhanced = []
        for l in logs:
            explanation = format_human_readable_explanation(l)
            enhanced.append({
                **l,
                "human_readable_explanation": explanation
            })
        return format_api_success({"total": len(enhanced), "audit_logs": enhanced})
    finally:
        conn.close()
