from typing import Dict, Any, Tuple, Optional
from app.utils.datetime_utils import normalize_to_iso_utc

class ValidationError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(message)

def validate_event_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate incoming event payload according to strict business rules.
    Returns sanitized dictionary with normalized timestamp if valid.
    Raises ValidationError if invalid.
    """
    if not isinstance(payload, dict):
        raise ValidationError("INVALID_PAYLOAD", "Payload must be a valid JSON object.")

    required_fields = ["camera_id", "timestamp", "student_id", "engagement_score", "confidence", "source"]
    for field in required_fields:
        if field not in payload:
            raise ValidationError("MISSING_FIELD", f"Missing required field: '{field}'")

    # IDs & Strings must be non-empty strings
    camera_id = str(payload.get("camera_id", "")).strip()
    if not camera_id:
        raise ValidationError("INVALID_CAMERA_ID", "camera_id must be a non-empty string.")

    student_id = str(payload.get("student_id", "")).strip()
    if not student_id:
        raise ValidationError("INVALID_STUDENT_ID", "student_id must be a non-empty string.")

    source = str(payload.get("source", "")).strip()
    if not source:
        raise ValidationError("INVALID_SOURCE", "source must be a non-empty string.")

    # Numeric score validations
    try:
        score = float(payload.get("engagement_score"))
    except (ValueError, TypeError):
        raise ValidationError("INVALID_ENGAGEMENT_SCORE", "engagement_score must be a numeric float.")
    
    if not (0.0 <= score <= 1.0):
        raise ValidationError("INVALID_ENGAGEMENT_SCORE", "engagement_score must be between 0.0 and 1.0.")

    try:
        confidence = float(payload.get("confidence"))
    except (ValueError, TypeError):
        raise ValidationError("INVALID_CONFIDENCE", "confidence must be a numeric float.")
    
    if not (0.0 <= confidence <= 1.0):
        raise ValidationError("INVALID_CONFIDENCE", "confidence must be between 0.0 and 1.0.")

    # Timestamp validation & normalization
    ts_raw = str(payload.get("timestamp", "")).strip()
    try:
        normalized_ts = normalize_to_iso_utc(ts_raw)
    except Exception as e:
        raise ValidationError("INVALID_TIMESTAMP", f"timestamp must be a valid ISO-8601 string: {str(e)}")

    # Optional Spatial Coordinates
    spatial_x = payload.get("spatial_x")
    spatial_y = payload.get("spatial_y")
    if spatial_x is not None:
        try:
            spatial_x = float(spatial_x)
        except (ValueError, TypeError):
            raise ValidationError("INVALID_SPATIAL_COORDINATES", "spatial_x must be numeric.")

    if spatial_y is not None:
        try:
            spatial_y = float(spatial_y)
        except (ValueError, TypeError):
            raise ValidationError("INVALID_SPATIAL_COORDINATES", "spatial_y must be numeric.")

    return {
        "camera_id": camera_id,
        "timestamp": normalized_ts,
        "student_id": student_id,
        "engagement_score": score,
        "confidence": confidence,
        "source": source,
        "spatial_x": spatial_x,
        "spatial_y": spatial_y,
        "is_replay": bool(payload.get("is_replay", False))
    }
