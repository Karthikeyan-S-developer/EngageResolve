from typing import Dict, Any, List

def format_human_readable_explanation(audit_record: Dict[str, Any]) -> str:
    """
    Translates structured decision logic into non-technical, human-readable explanations.
    """
    decision_type = audit_record.get("decision_type")
    logic = audit_record.get("resolution_logic") or {}
    
    if decision_type == "CONFLICT_RESOLUTION":
        winning_id = logic.get("winning_event_id") or audit_record.get("selected_event_id")
        final_score = audit_record.get("final_score", 0.0)
        tiebreaker = logic.get("tiebreaker_used", "CONFIDENCE")
        reason = logic.get("reason", "")
        candidates = logic.get("candidate_events", [])

        lines = [f"Why was engagement score {final_score:.2f} selected?"]
        for c in candidates:
            score = c.get("score", 0.0)
            conf = c.get("confidence", 0.0) * 100
            cam = c.get("camera_id", "Unknown Camera")
            lines.append(f"• Camera {cam} reported score {score:.2f} with {conf:.0f}% confidence.")

        lines.append(f"\nDecision Summary: {reason}")
        return "\n".join(lines)

    elif decision_type == "OUT_OF_ORDER_EVENT":
        ts = audit_record.get("timestamp")
        return (
            f"An out-of-order event arrived with timestamp {ts}. "
            f"The system automatically re-ordered all observations chronologically "
            f"and recalculated versioned student states to preserve timeline determinism."
        )

    elif decision_type == "IDENTITY_RESOLUTION":
        raw = logic.get("raw_student_id", "")
        resolved = logic.get("resolved_student_id", "")
        score = logic.get("combined_score", 0.0)
        return (
            f"Raw camera observation for '{raw}' was matched to canonical student '{resolved}' "
            f"with a spatio-temporal match score of {score:.2f}."
        )

    elif decision_type == "DUPLICATE_EVENT":
        return "Duplicate event fingerprint detected. Event ignored to maintain state idempotency."

    return f"Decision type '{decision_type}' recorded at {audit_record.get('timestamp')}."
