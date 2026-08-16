from typing import Dict, Any, List, Tuple, Optional
from app.config import Config

def resolve_conflict_between_events(
    event_a: Dict[str, Any],
    event_b: Dict[str, Any]
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Deterministically resolves conflicts between two engagement events for the same student.
    Returns: (winning_event, decision_trace_dict)
    """
    rules_evaluated = ["validity_check", "duplicate_check"]
    
    # 1. Rule 3: Confidence Comparison
    conf_a = float(event_a["confidence"])
    conf_b = float(event_b["confidence"])
    rules_evaluated.append("confidence_comparison")

    if abs(conf_a - conf_b) > 1e-6:
        if conf_a > conf_b:
            winner = event_a
            loser = event_b
            reason = f"Event {event_a['id']} selected because confidence {conf_a:.2f} exceeded {conf_b:.2f}."
        else:
            winner = event_b
            loser = event_a
            reason = f"Event {event_b['id']} selected because confidence {conf_b:.2f} exceeded {conf_a:.2f}."
        
        trace = {
            "decision_type": "CONFLICT_RESOLUTION",
            "student_id": event_a.get("resolved_student_id") or event_a.get("student_id"),
            "candidate_events": [
                {
                    "event_id": event_a["id"],
                    "camera_id": event_a["camera_id"],
                    "score": event_a["engagement_score"],
                    "confidence": conf_a,
                    "timestamp": event_a["timestamp"]
                },
                {
                    "event_id": event_b["id"],
                    "camera_id": event_b["camera_id"],
                    "score": event_b["engagement_score"],
                    "confidence": conf_b,
                    "timestamp": event_b["timestamp"]
                }
            ],
            "rules_evaluated": rules_evaluated,
            "winning_event_id": winner["id"],
            "final_score": winner["engagement_score"],
            "reason": reason,
            "tiebreaker_used": "CONFIDENCE"
        }
        return winner, trace

    # 2. Rule 4: Timestamp Comparison (Earlier timestamp wins)
    rules_evaluated.append("timestamp_tiebreak")
    ts_a = event_a["timestamp"]
    ts_b = event_b["timestamp"]

    if ts_a != ts_b:
        if ts_a < ts_b:
            winner = event_a
            reason = f"Confidence tied ({conf_a:.2f}). Event {event_a['id']} selected due to earlier timestamp ({ts_a} < {ts_b})."
        else:
            winner = event_b
            reason = f"Confidence tied ({conf_b:.2f}). Event {event_b['id']} selected due to earlier timestamp ({ts_b} < {ts_a})."

        trace = {
            "decision_type": "CONFLICT_RESOLUTION",
            "student_id": event_a.get("resolved_student_id") or event_a.get("student_id"),
            "candidate_events": [
                {"event_id": event_a["id"], "score": event_a["engagement_score"], "confidence": conf_a, "timestamp": ts_a},
                {"event_id": event_b["id"], "score": event_b["engagement_score"], "confidence": conf_b, "timestamp": ts_b}
            ],
            "rules_evaluated": rules_evaluated,
            "winning_event_id": winner["id"],
            "final_score": winner["engagement_score"],
            "reason": reason,
            "tiebreaker_used": "TIMESTAMP"
        }
        return winner, trace

    # 3. Rule 5: Camera Reliability Comparison
    rules_evaluated.append("camera_reliability_tiebreak")
    rel_a = Config.get_camera_reliability(event_a["camera_id"])
    rel_b = Config.get_camera_reliability(event_b["camera_id"])

    if abs(rel_a - rel_b) > 1e-6:
        if rel_a > rel_b:
            winner = event_a
            reason = f"Confidence & timestamp tied. Event {event_a['id']} selected because camera '{event_a['camera_id']}' reliability ({rel_a:.2f}) > '{event_b['camera_id']}' ({rel_b:.2f})."
        else:
            winner = event_b
            reason = f"Confidence & timestamp tied. Event {event_b['id']} selected because camera '{event_b['camera_id']}' reliability ({rel_b:.2f}) > '{event_a['camera_id']}' ({rel_a:.2f})."

        trace = {
            "decision_type": "CONFLICT_RESOLUTION",
            "student_id": event_a.get("resolved_student_id") or event_a.get("student_id"),
            "candidate_events": [
                {"event_id": event_a["id"], "camera_id": event_a["camera_id"], "score": event_a["engagement_score"], "confidence": conf_a, "timestamp": ts_a, "reliability": rel_a},
                {"event_id": event_b["id"], "camera_id": event_b["camera_id"], "score": event_b["engagement_score"], "confidence": conf_b, "timestamp": ts_b, "reliability": rel_b}
            ],
            "rules_evaluated": rules_evaluated,
            "winning_event_id": winner["id"],
            "final_score": winner["engagement_score"],
            "reason": reason,
            "tiebreaker_used": "CAMERA_RELIABILITY"
        }
        return winner, trace

    # 4. Rule 6: Stable Fingerprint Tie-breaker (Lexicographically smaller SHA-256 fingerprint wins)
    rules_evaluated.append("fingerprint_tiebreak")
    fp_a = event_a["event_fingerprint"]
    fp_b = event_b["event_fingerprint"]

    if fp_a <= fp_b:
        winner = event_a
        reason = f"All attributes tied. Event {event_a['id']} selected by deterministic SHA-256 fingerprint ordering."
    else:
        winner = event_b
        reason = f"All attributes tied. Event {event_b['id']} selected by deterministic SHA-256 fingerprint ordering."

    trace = {
        "decision_type": "CONFLICT_RESOLUTION",
        "student_id": event_a.get("resolved_student_id") or event_a.get("student_id"),
        "candidate_events": [
            {"event_id": event_a["id"], "fingerprint": fp_a, "score": event_a["engagement_score"], "confidence": conf_a, "timestamp": ts_a},
            {"event_id": event_b["id"], "fingerprint": fp_b, "score": event_b["engagement_score"], "confidence": conf_b, "timestamp": ts_b}
        ],
        "rules_evaluated": rules_evaluated,
        "winning_event_id": winner["id"],
        "final_score": winner["engagement_score"],
        "reason": reason,
        "tiebreaker_used": "FINGERPRINT"
    }
    return winner, trace
