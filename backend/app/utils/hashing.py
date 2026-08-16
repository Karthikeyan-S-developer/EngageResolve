import hashlib
import json
from typing import Dict, Any, List
from app.utils.datetime_utils import normalize_to_iso_utc

def generate_event_fingerprint(
    camera_id: str,
    timestamp: str,
    student_id: str,
    engagement_score: float,
    confidence: float,
    source: str
) -> str:
    """
    Generate a deterministic SHA-256 fingerprint for an engagement event.
    Canonicalizes string fields and formats floating point values consistently.
    """
    normalized_ts = normalize_to_iso_utc(timestamp)
    canonical_data = {
        "camera_id": str(camera_id).strip(),
        "confidence": round(float(confidence), 4),
        "engagement_score": round(float(engagement_score), 4),
        "source": str(source).strip(),
        "student_id": str(student_id).strip(),
        "timestamp": normalized_ts
    }
    canonical_str = json.dumps(canonical_data, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(canonical_str.encode('utf-8')).hexdigest()

def calculate_state_result_hash(student_states: List[Dict[str, Any]], audit_logs: List[Dict[str, Any]]) -> str:
    """
    Calculate a canonical SHA-256 hash representing the full student state timeline & audit history.
    Used for verifying deterministic replay.
    """
    cleaned_states = []
    for s in student_states:
        cleaned_states.append({
            "confidence": round(float(s["confidence"]), 4),
            "effective_timestamp": str(s["effective_timestamp"]),
            "engagement_score": round(float(s["engagement_score"]), 4),
            "state_status": str(s["state_status"]),
            "student_id": str(s["student_id"]),
            "version": int(s["version"])
        })
    # Sort states deterministically by student_id and version
    cleaned_states.sort(key=lambda x: (x["student_id"], x["version"]))

    cleaned_audits = []
    for a in audit_logs:
        cleaned_audits.append({
            "decision_type": str(a["decision_type"]),
            "final_score": round(float(a["final_score"]), 4),
            "previous_score": round(float(a["previous_score"])) if a.get("previous_score") is not None else None,
            "student_id": str(a["student_id"]),
            "timestamp": str(a["timestamp"])
        })
    cleaned_audits.sort(key=lambda x: (
        x["student_id"],
        x["timestamp"],
        x["decision_type"],
        x["final_score"],
        str(x["previous_score"])
    ))

    combined_payload = {
        "audit_logs": cleaned_audits,
        "student_states": cleaned_states
    }
    canonical_str = json.dumps(combined_payload, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(canonical_str.encode('utf-8')).hexdigest()
