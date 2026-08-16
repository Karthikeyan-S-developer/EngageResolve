import sqlite3
from typing import Dict, Any
from app.core.validation import validate_event_payload, ValidationError
from app.core.fingerprint import check_event_idempotency
from app.core.identity_resolution import resolve_student_identity
from app.core.state_reconstruction import reconstruct_student_timeline
from app.database.repositories import EventRepository, StudentRepository, AuditRepository

def process_incoming_event(conn: sqlite3.Connection, raw_payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Core Ingestion Pipeline:
    1. Validation
    2. Deduplication / Idempotency Check
    3. Identity Resolution
    4. Database Event Persistence
    5. State Reconstruction & Out-of-Order Versioning
    6. Audit Trace Generation
    """
    # 1. Validation
    validated = validate_event_payload(raw_payload)

    # 2. Idempotency Check
    is_dup, existing_id, fingerprint = check_event_idempotency(conn, validated)
    if is_dup:
        return {
            "success": True,
            "status": "duplicate",
            "event_id": existing_id,
            "event_fingerprint": fingerprint,
            "message": "Event already processed. Idempotent request ignored."
        }

    # 3. Identity Resolution
    raw_student_id = validated["student_id"]
    resolved_student_id, identity_info = resolve_student_identity(
        conn,
        raw_student_id=raw_student_id,
        camera_id=validated["camera_id"],
        timestamp=validated["timestamp"],
        spatial_x=validated.get("spatial_x"),
        spatial_y=validated.get("spatial_y")
    )

    # 4. Save Event Record
    event_data = {
        "event_fingerprint": fingerprint,
        "camera_id": validated["camera_id"],
        "timestamp": validated["timestamp"],
        "student_id_raw": raw_student_id,
        "resolved_student_id": resolved_student_id,
        "engagement_score": validated["engagement_score"],
        "confidence": validated["confidence"],
        "source": validated["source"],
        "spatial_x": validated.get("spatial_x"),
        "spatial_y": validated.get("spatial_y"),
        "is_replay": validated.get("is_replay", False)
    }

    event_repo = EventRepository(conn)
    created_event = event_repo.create(event_data)

    # Log Identity Resolution Audit if non-trivial mapping
    audit_repo = AuditRepository(conn)
    if identity_info.get("decision") in ("RESOLVED", "NEW_STUDENT"):
        audit_repo.create_log({
            "student_id": resolved_student_id,
            "event_id": created_event["id"],
            "decision_type": "IDENTITY_RESOLUTION",
            "input_events": [created_event],
            "resolution_logic": identity_info,
            "selected_event_id": created_event["id"],
            "final_score": created_event["engagement_score"],
            "previous_score": None,
            "timestamp": created_event["timestamp"]
        })

    # 5. State Reconstruction & Out-of-Order Handling
    reconstructed_states, out_of_order_audit = reconstruct_student_timeline(
        conn,
        student_id=resolved_student_id,
        newly_added_event=created_event
    )

    # Update student updated_at timestamp
    student_repo = StudentRepository(conn)
    student_repo.update_timestamp(resolved_student_id)

    latest_state = reconstructed_states[-1] if reconstructed_states else None

    return {
        "success": True,
        "status": "processed",
        "event": created_event,
        "resolved_student_id": resolved_student_id,
        "latest_state": latest_state,
        "total_versions": len(reconstructed_states),
        "is_out_of_order": out_of_order_audit is not None
    }
